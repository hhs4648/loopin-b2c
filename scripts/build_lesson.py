"""
스펙 한 장을 레슨 JSON으로 부풀린다.

**손으로 쓰는 것과 만들어 내는 것을 나눈다.** 레슨 JSON은 문장 하나에 100줄쯤
되는데, 그중 사람이 판단할 것은 얼마 안 된다 — 문장·해석·채점 포인트·오해·단어 뜻.
나머지(유도 문구·답 알려주기·2지선다 응답·오류 우선순위)는 규칙이 정해져 있으므로
여기서 만든다. 규칙이 바뀌면 스펙은 그대로 두고 이 파일만 고쳐 다시 돌린다.

    python scripts/build_lesson.py scripts/specs/<이름>.json

`docs/tutor/BEHAVIOR.md`의 유도 문구 규칙을 그대로 따른다.
"""

import io
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

GLOSSARY = json.load(io.open("content/tutor/glossary.json", encoding="utf-8"))["words"]


def tokens(sentence):
    """앱이 낱말을 자르는 방식과 같게 자른다 (`src/tutor/glosses.ts`)."""
    return re.findall(r"[A-Za-z0-9]+(?:['.][A-Za-z0-9]+)*", sentence)


def occurs(en, lowered):
    return re.search(r"(?<![A-Za-z])" + re.escape(en.lower()) + r"(?![A-Za-z])", lowered)


def uncovered(text, glosses):
    """
    **앱이 훑는 방식 그대로 훑는다** (`src/tutor/glosses.ts`).

    긴 구부터 맞춰 가며 문장을 한 번 지나가고, 어디에도 안 걸린 낱말을 돌려준다.
    낱말 단위로 「이 단어는 어딘가에서 덮였다」고 세면 안 된다 — 「true of」가
    한 군데를 덮었다고 해서 문장 뒤쪽의 다른 `of`까지 덮이는 건 아니다.
    """
    ordered = sorted(glosses, key=lambda g: (-len(g[0]), -len(g[0].split())))
    missing, i = [], 0
    while i < len(text):
        rest = text[i:]
        ws = re.match(r"\s+", rest)
        if ws:
            i += len(ws.group())
            continue
        hit = None
        for en, _ in ordered:
            m = re.match(re.escape(en) + r"(?![A-Za-z0-9])", rest, re.IGNORECASE)
            if m:
                hit = m.group()
                break
        if hit:
            i += len(hit)
            continue
        tok = re.match(r"[A-Za-z0-9]+(?:['.][A-Za-z0-9]+)*", rest)
        if tok:
            missing.append(tok.group())
            i += len(tok.group())
        else:
            i += 1
    return missing


def fill_glosses(text, listed, lesson_wide=(), lesson_phrases=(), nouns=()):
    """
    **되풀이되는 낱말은 스펙에 안 적는다.**

    a·the·of 같은 것을 레슨마다 다시 적으면 250개 문장에 2천 번을 적게 된다.
    공용 사전(`content/tutor/glossary.json`)과 **같은 지문의 다른 문장**에서 채우되,
    스펙에 적힌 것이 이긴다 — 문맥에 따라 뜻이 달라지는 낱말이 있기 때문이다.
    """
    lowered = text.lower()
    listed = list(listed)
    have = {en.lower() for en, _ in listed}
    for en, ko in lesson_phrases:
        if en.lower() not in have and occurs(en, lowered):
            listed.append((en, ko))
            have.add(en.lower())
        elif en.lower() not in have and not occurs(en, lowered):
            pass

    """
    고유명사는 JSON에 안 적어도 앱이 칩과 같은 말로 채워 준다 (`glossesFor`).
    여기서도 같이 세어야 없는 구멍을 있다고 잘못 알리지 않는다.
    """
    for n in nouns:
        if n["en"].lower() not in have and occurs(n["en"], lowered):
            listed.append((n["en"], f"{n.get('ko', n['en'])}(이름)"))
            have.add(n["en"].lower())

    wide = dict(lesson_wide)

    """
    아포스트로피가 든 낱말을 **먼저** 넣는다.

    「wine」만 있으면 앱이 `wine's`에서 `wine`까지만 먹고 `s`가 뜻 없는 낱말로
    남는다. `you'll`의 `ll`도 같은 자리다 — 짧은 것이 긴 것을 잘라 먹는다.
    """
    SUFFIX = {
        "s": "{}의",
        "ll": "{}은 ~할 것이다",
        "re": "{}은 ~이다",
        "ve": "{}은 ~했다",
        "d": "{}은 ~했다",
        "m": "{}은 ~이다",
    }
    for m in re.finditer(r"[A-Za-z]+'[A-Za-z]+", text):
        form = m.group()
        low = form.lower()
        if low in have or low in wide or low in GLOSSARY:
            if low in wide or low in GLOSSARY:
                listed.append((form, wide.get(low) or GLOSSARY[low]))
                have.add(low)
            continue
        head, tail = low.split("'", 1)
        base = wide.get(head) or GLOSSARY.get(head)
        if not base:
            """
            「Grandpa Joe's」처럼 **이름 전체**에 소유격이 붙은 자리.
            `Joe's`만 넣으면 소용없다 — 더 긴 `Grandpa Joe`가 먼저 걸려서
            `'s`만 남는다. 이름째로 넣어야 앱이 통째로 먹는다.
            """
            for n in nouns:
                whole = f"{n['en']}'{tail}"
                if tokens(n["en"])[-1].lower() == head and occurs(whole, lowered):
                    if whole.lower() not in have:
                        listed.append((whole, f"{n.get('ko', n['en'])}의"))
                        have.add(whole.lower())
                    break
            continue
        if base and tail in SUFFIX:
            listed.append((form, SUFFIX[tail].format(base)))
            have.add(low)

    for tok in uncovered(text, listed):
        low = tok.lower()
        if low in have:
            continue
        ko = wide.get(low) or GLOSSARY.get(low)
        if not ko and tok.isdigit():
            # 연도·숫자는 사전에 담을 것이 아니라 그때그때 만든다
            ko = f"{tok}년" if 1000 <= int(tok) <= 2999 else tok
        if not ko and low.endswith("'s"):
            base = wide.get(low[:-2]) or GLOSSARY.get(low[:-2])
            if base:
                ko = f"{base}의"
        if ko:
            listed.append((tok, ko))
            have.add(low)

    out = [OrderedDict([("en", en), ("ko", ko)]) for en, ko in listed]
    for en, _ in listed:
        if len(tokens(en)) > 1 and not occurs(en, lowered):
            print(f"    (구가 문장에 없어 안 잡힘: \"{en}\")")
    return out, uncovered(text, listed)


def copula(word):
    """받침이 있으면 「이에요」. 「'기원전'예요」가 나오지 않게."""
    last = word.strip()[-1]
    code = ord(last) - 0xAC00
    if code < 0 or code > 11171:
        return "예요"
    return "예요" if code % 28 == 0 else "이에요"


def build_point(index, spec):
    """
    유도는 **남은 자리의 이름만** 말한다. 뜻은 두 번째로 막혔을 때 `tell`이 준다
    (2026-09-06). 그래서 nudge는 규칙이지 창작이 아니다.
    """
    en, answer = spec["en"], spec["answer"]
    if "?" in en:
        # 유도 문구에 물음표가 둘이 되면 「한 턴에 질문 하나」 규칙을 깬다
        raise SystemExit(f"항목 이름에 물음표를 넣지 마세요: {en!r}")
    return OrderedDict([
        ("id", index),
        ("text", f"{en} → {answer}"),
        ("check", spec["check"]),
        ("nudge", f"{en}{spec['sub']} 아직 해석에 안 나왔어요. 한번 더 해볼까요?"),
        ("tell", f"{en}{spec['top']} 여기서 '{answer}'{copula(answer)}."),
    ])


def build_error(spec):
    """
    2지선다는 실제로 틀렸을 때(C)와 좌절 방지 둘 다에서 쓰인다.
    보기 짝이 맞아야 좌절 방지가 그 문장에서 물어볼 게 생긴다.
    """
    right, wrong = spec["right"], spec["wrong"]
    return OrderedDict([
        ("id", spec["id"]),
        ("detect", spec["detect"]),
        ("signals", spec["signals"]),
        ("treatment", OrderedDict([
            ("message", f"{spec['ask']} '{wrong}'일까요, '{right}'일까요?"),
            ("choices", [
                OrderedDict([("id", "wrong"), ("label", wrong), ("correct", False)]),
                OrderedDict([("id", "right"), ("label", right), ("correct", True)]),
            ]),
            ("on_choice", OrderedDict([
                ("right", OrderedDict([
                    ("message", f"맞아요! '{right}'{copula(right)}. 그 뜻으로 다시 한번 해볼까요?"),
                    ("next", "retry_chunk"),
                ])),
                ("wrong", OrderedDict([
                    ("message", f"괜찮아요, 헷갈리기 쉬워요. '{right}'{copula(right)}. 그 뜻으로 다시 해볼까요?"),
                    ("reveal_answer", True),
                    ("next", "retry_chunk"),
                ])),
            ])),
        ])),
    ])


def build(spec):
    # 지문 전체에서 적은 낱말 뜻을 한 통에 모은다 (구는 낱말로 쪼개서)
    nouns = spec.get("proper_nouns", [])
    lesson_wide, lesson_phrases, seen = {}, [], set()
    for c in spec["chunks"]:
        for en, ko in c.get("glosses", []):
            parts = tokens(en)
            if len(parts) == 1:
                lesson_wide.setdefault(parts[0].lower(), ko)
            elif en.lower() not in seen:
                seen.add(en.lower())
                lesson_phrases.append((en, ko))

    chunks = []
    for i, c in enumerate(spec["chunks"], 1):
        chunk = OrderedDict([
            ("id", i),
            ("text", c["text"]),
            ("model_translation", c["ko"]),
            ("praise", c["praise"]),
        ])
        glosses, missing = fill_glosses(
            c["text"], c.get("glosses", []), lesson_wide, lesson_phrases, nouns
        )
        if missing:
            # 테스트가 잡기 전에 여기서 잡는다 — 누르면 빈칸이 나오는 낱말이다
            print(f"  ! 문장{i} 뜻 없음: {', '.join(missing)}")
        chunk["glosses"] = glosses
        chunk["scoring_points"] = [
            build_point(n, p) for n, p in enumerate(c["points"], 1)
        ]
        errors = c.get("errors", [])
        if errors:
            # 뒤에 적은 오해일수록 먼저 본다 — 나중 것이 더 치명적인 오해다
            chunk["error_priority"] = [e["id"] for e in reversed(errors)]
            chunk["expected_errors"] = [build_error(e) for e in errors]
        chunks.append(chunk)

    return OrderedDict([
        ("id", spec["id"]),
        ("version", "1.0"),
        ("updated", spec["updated"]),
        ("source", spec["source"]),
        ("category", spec.get("category", "리딩")),
        ("topic_intro", spec["topic_intro"]),
        ("sentence", spec["sentence"]),
        ("grammar_type", spec["grammar_type"]),
        ("split_rule", spec["split_rule"]),
        ("proper_nouns", spec.get("proper_nouns", [])),
        ("chunks", chunks),
    ])


def main():
    spec_path = Path(sys.argv[1])
    spec = json.load(io.open(spec_path, encoding="utf-8"), object_pairs_hook=OrderedDict)
    lesson = build(spec)
    out = Path("content/tutor/lessons") / f"{lesson['id']}.json"
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        json.dumps(lesson, ensure_ascii=False, indent=2) + "\n"
    )
    points = sum(len(c["scoring_points"]) for c in lesson["chunks"])
    errors = sum(len(c.get("expected_errors", [])) for c in lesson["chunks"])
    print(f"{out} — {len(lesson['chunks'])}문장 · 채점 포인트 {points} · 오해 {errors}")


if __name__ == "__main__":
    main()
