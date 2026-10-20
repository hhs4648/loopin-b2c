"""모의고사 레슨 생성기 공용 도구 (2024년 3월 고3부터).

예전 생성기는 g·choice·show·sv_pick을 파일마다 복사해 썼다. 틀이 굳어서(docs/tutor/templates/) 여기 모았다.
생성기는 문장·스텝·보기만 적고 `finish()`를 부른다. finish는

1. 규칙 테스트(src/tutor/policy/policy.test.ts)가 볼 것을 **미리** 검사한다 — 물음표 하나·세 문장, 보기 2~3개·정답 미리 말하지 않기,
   찾기 후보가 화면에서 따로 눌리는지, 강조 구절이 문장 안에 있는지, 덩어리 안 내용어 뜻, 다의 기능어 쓰임 개수
2. 덩어리 안 내용어 뜻이 없으면 `words`(레슨) → `WORDS`(아래 공용)에서 단어 뜻을 채운다
3. 칠판 정리(story)를 끼우고, 레슨·대사·기능어 쓰임 JSON을 쓴다 — brief가 이미 다정쌤 해요체라 대사는 그대로 옮긴다

그다음 `npm run policy:copy stamp <id>` (regen_all이 해 준다) → `npm run build`.
"""
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import story_boards  # noqa: E402
from beginner import add_basic, fill_chunk_glosses, m, sv_step, add_that_sv  # noqa: E402,F401

SHARED = json.load(open(f"{ROOT}/content/tutor/word-glosses.json"))["words"]

# src/tutor/glosses.ts 와 같게
FUNCTION_WORDS = set("""a an the and or but so nor yet if than all both each every either neither some any no such own same other else
another here there those it its itself they them their themselves he him his she her we us our you your yourself i me my one ones
who whom whose something anything everything everyone someone just too very quite really also even much""".split())
CONTEXT_WORDS = set("""to of for in on with from into at by as about toward towards be is are was were been being has have had do does
did not will would may might can could should must which that it this these""".split())
ARTICLES = {"a", "an", "the"}
SENSE_WORDS = ["to", "for", "as", "since", "while", "that", "which", "so", "but", "yet", "if"]

# 덩어리 안에 자주 나오는 말 — 레슨 words에 없을 때 마지막으로 쓴다 (문맥 뜻이 다르면 레슨 words에 적는다)
KIT_WORDS = {
    "over": "~ 위에, ~에 대해", "when": "~할 때", "through": "~을 통해", "between": "~ 사이의", "without": "~ 없이", "after": "~ 뒤에",
    "before": "~ 전에", "under": "~ 아래", "because": "~ 때문에", "where": "~하는 곳", "how": "어떻게", "what": "무엇", "why": "왜",
    "not": "~ 않다", "never": "결코 ~ 않다", "more": "더", "most": "가장, 대부분의", "less": "덜", "many": "많은", "few": "거의 없는",
    "only": "오직, ~만", "still": "여전히", "now": "지금", "then": "그때, 그러면", "up": "위로", "down": "아래로", "out": "밖으로",
    "off": "떨어져", "back": "뒤로, 다시", "away": "멀리", "first": "처음, 첫째", "new": "새로운", "old": "오래된", "same": "같은",
    "good": "좋은", "great": "큰, 훌륭한", "own": "자기 자신의", "people": "사람들", "person": "사람", "thing": "것", "things": "것들",
    "time": "시간", "way": "방식, 길", "life": "삶", "world": "세상", "day": "날", "make": "만들다", "take": "가지다, 받다",
    "get": "얻다, ~하게 되다", "give": "주다", "go": "가다", "come": "오다", "see": "보다", "know": "알다", "think": "생각하다",
    "feel": "느끼다", "say": "말하다", "tell": "말하다", "find": "찾다, 알게 되다", "use": "쓰다", "need": "필요, 필요하다",
    "it’s": "그것은 ~이다", "that’s": "그것은 ~이다", "don’t": "~하지 않다", "doesn’t": "~하지 않다", "can’t": "~할 수 없다",
    "cannot": "~할 수 없다", "isn’t": "~이 아니다", "won’t": "~하지 않을 것이다", "i’m": "나는 ~이다", "you’re": "너는 ~이다",
    "keep": "유지하다, 계속하다", "again": "다시", "sometimes": "때때로", "always": "늘", "often": "흔히", "very": "매우",
    "though": "~이지만", "although": "비록 ~이지만", "across": "~에 걸쳐, ~마다", "having": "가지고 있는", "while": "~하는 동안, ~인 반면",
    "whether": "~인지", "whose": "그의, 그것의", "among": "~ 사이에서", "within": "~ 안에", "upon": "~하자마자, ~ 위에",
    "during": "~ 동안", "until": "~까지", "since": "~ 이후로", "about": "~에 대해", "into": "~ 안으로", "toward": "~을 향해",
    "want": "원하다", "like": "~처럼, 좋아하다", "other": "다른", "others": "다른 사람들", "also": "또한", "too": "너무, ~도",
}


# ── 스텝 ──────────────────────────────────────────────────────────────

def g(en, ko):
    return {"en": en, "ko": ko}


def choice(id, ask, options, hint, praise="맞아요!", method=1, why=None, point=None, **extra):
    """3지(2~3개) 객관식. options = [(id, 보기 글, 정답?)]. why = 틀렸을 때 「아쉽게도 틀렸어요.」 뒤 이유 (없으면 hint)"""
    feedback = {o[0]: why or hint for o in options if not o[2]}
    brief = {"ask": ask, "reask": "그럼 하나 골라 봐요.", "hints": [hint, hint], "explain": why or hint, "praise": praise,
             "feedback": feedback}
    if point:
        brief["point"] = point
    return {"id": id, "type": "choice", "interaction": "meaning_choice", "one_try": True, "brief": brief,
            "options": [{"id": o[0], "label": o[1], **({"correct": True} if o[2] else {})} for o in options],
            "method": method, **extra}


def show(id, say, method=1, button="다음", point=None, **extra):
    brief = {"say": say, **({"point": point} if point else {})}
    return {"id": id, "type": "show", "interaction": "note", "brief": brief, "method": method, "button": button, **extra}


def pick(id, ask, candidates, answers, wrong, explain, praise="맞아요!", wrong_by=None, point=None, **extra):
    """문장에서 찾아 누르기 (가리키는 말·같은 쪽 말·핵심어). 후보는 문장 뜻(glosses)에 덩어리로 있어야 한다"""
    brief = {"ask": ask, "wrong": wrong, "more": "좋아요! {n}개 남았어요.", "praise": praise, "explain": explain}
    if wrong_by:
        brief["wrong_by"] = wrong_by
    if point:
        brief["point"] = point
    return {"id": id, "type": "pick", "interaction": "word_pick", "shade": True, "candidates": candidates,
            "answers": answers, "brief": brief, "method": extra.pop("method", 0), **extra}


def sv(id, candidates, roles, wrong_by, explain, ask=None, point=None, **extra):
    """덩어리째 주어·동사(+O/C/전목) 찾기 — 모두에게(긴 문장). 짧은 문장의 초급용은 basic()의 sv"""
    st = sv_step(id, candidates, roles, wrong_by, explain, ask=ask)
    if point:
        st["brief"]["point"] = point
    st.update(extra)
    return st


def translate(id, ask, model, rules, highlight=None, point=None, praise="잘 해석했어요! 핵심이 잘 잡혔어요.", **extra):
    """자유 해석 — 규칙 채점(LLM 없음). rules = [(id, need[], wrong[] | None, 고친 해석의 구절, 피드백)]"""
    return {
        "id": id, "type": "translate", "interaction": "free_translation", "model": model,
        "rules": [{"id": r[0], **({"need": r[1]} if r[1] else {}), **({"wrong": r[2]} if r[2] else {}), "fix": r[3]} for r in rules],
        **({"highlight": highlight} if highlight else {}),
        "brief": {"ask": ask, "praise": praise, "wrong": "고친 부분을 같이 봐요.",
                  "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                  "feedback": {r[0]: r[4] for r in rules}, "placeholder": "자유롭게 해석해 보세요",
                  "point": point or f"해석 = {model}"},
        "method": extra.pop("method", 0), **extra,
    }


def keywords(id, candidates, answers, wrong, explain, ask=None, **extra):
    """핵심어 찾기 — 틀려도 「더 좋은 선택이 있어요」(keyword). 함정은 뜻을 덧붙이기만 하는 말로"""
    return {"id": id, "type": "pick", "interaction": "word_pick", "candidates": candidates, "answers": answers, "keyword": True,
            "brief": {"ask": ask or f"이 문장의 핵심어 {len(answers)}개를 찾아볼까요?", "wrong": wrong, "more": "좋아요! {n}개 남았어요.",
                      "praise": "다 찾았어요!", "explain": explain, "point": "핵심어 = " + " · ".join(answers)},
            "method": extra.pop("method", 0), **extra}


def tip(label, text, mark=None):
    return {"label": label, "text": text, **({"mark": mark} if mark else {})}


def groups(title, left_label, left, right_label=None, right=None, fresh=(), sort=None, between=None, caption=None):
    """단어 지도(두 그룹) — 단어는 (영어, 한국어) 또는 영어. fresh = 이번에 붙은 단어"""
    def words(ws):
        out = []
        for w in ws:
            en, ko = (w if isinstance(w, tuple) else (w, None))
            out.append({"text": en, **({"ko": ko} if ko else {}), **({"fresh": True} if en in fresh else {})})
        return out
    p = {"kind": "groups", "title": title, "left": {"label": left_label, "words": words(left)}}
    if right_label is not None:
        p["right"] = {"label": right_label, "words": words(right or [])}
    if between is not None:
        p["between"] = between
    if sort:
        p["sort"] = sort
    if caption:
        p["caption"] = caption
    return p


def rows(*rs):
    """문장 아래 작은 표 — (label, text, ko, tone)"""
    out = []
    for r in rs:
        label, text = r[0], r[1]
        d = {"label": label, "text": text}
        if len(r) > 2 and r[2]:
            d["ko"] = r[2]
        if len(r) > 3 and r[3]:
            d["tone"] = r[3]
        out.append(d)
    return {"kind": "structure", "rows": out}


def r(text, role):
    """끊어읽기(「/ 끊어읽기」)를 켜면 같이 보이는 S·V·O·C — 문장 필드 roles. 메인 문장 S·V·O·C + 절 안의 S·V, 모두 같은 진하기,
    주어·동사 찾기 전에도 보인다 (2026-10-20 선생님 전체 규칙). 떨어진 동사는 "has … survived"처럼 「 … 」로 잇는다.
    같은 낱말이 여러 번 나오면 화면은 긴 덩어리부터 자리를 잡고 짧은 것은 아직 안 잡힌 첫 자리로 간다 — 앞쪽 같은 낱말을
    더 긴 덩어리로 먼저 잡아 두거나, 둘 다 같은 역할이면 "we … we"로 차례로 잡는다"""
    return {"text": text, "role": role}


def sense(word, phrase, sense_, usage):
    return {"word": word, "phrase": phrase, "sense": sense_, "usage": usage}


def sc(label, icon, en, ko):
    return story_boards.sc(label, icon, en, ko)


# ── 도입 칠판 그림 ─────────────────────────────────────────────────────

def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def topic_svg(name, left, op, right, question, note=""):
    """도입 칠판 — [왼쪽 상자] op [오른쪽 상자] + 아래 물음 한 줄. left/right = (영어, 한국어)
    칠판 글자는 영어(괄호 한국어). 물음은 글을 암시만 한다 (답을 말하지 않는다)"""
    def box(x, w, en, ko, fill, stroke, ink):
        size = 19 if len(en) <= 9 else 16 if len(en) <= 13 else 13
        return (f'    <rect x="{x}" y="52" width="{w}" height="70" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>\n'
                f'    <text x="{x + w / 2}" y="88" text-anchor="middle" font-size="{size}" fill="{ink}">{_esc(en)}</text>\n'
                f'    <text x="{x + w / 2}" y="107" text-anchor="middle" font-size="12" fill="{ink}">({_esc(ko)})</text>\n')
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170" fill="none">\n'
           f'  <!-- {_esc(note)} -->\n'
           '  <g font-family="\'Gowun Dodum\',\'Noto Sans KR\',sans-serif" font-weight="700">\n'
           '    <text x="170" y="30" text-anchor="middle" font-size="16" fill="#8a7f88">이번 글</text>\n'
           + box(14, 132, left[0], left[1], "#f2fbf8", "#8fd0c0", "#2f7d6c")
           + f'    <text x="170" y="94" text-anchor="middle" font-size="22" fill="#8a7f88">{_esc(op)}</text>\n'
           + box(194, 132, right[0], right[1], "#fff5f7", "#ef7a93", "#c0455f")
           + f'    <text x="170" y="158" text-anchor="middle" font-size="14" fill="#5b4f57">{_esc(question)}</text>\n'
           '  </g>\n</svg>\n')
    path = f"{ROOT}/public/assets/{name}"
    open(path, "w").write(svg)
    return f"/assets/{name}"


# ── 검사 (테스트와 같은 규칙) ──────────────────────────────────────────

def _gloss_re(en):
    esc = re.escape(en).replace("\\ ", " ")
    esc = re.sub(r"\s+", r"\\s+", esc)
    return re.compile(r"^(" + esc + r")(?![A-Za-z0-9])", re.I)


def gloss_spans(sentence, glosses):
    srt = sorted(glosses, key=lambda x: (-len(x["en"]), -len(x["en"].split())))
    regs = [(x, _gloss_re(x["en"])) for x in srt]
    spans, i = [], 0
    while i < len(sentence):
        rest = sentence[i:]
        ws = re.match(r"^\s+", rest)
        if ws:
            spans.append((ws.group(0), None))
            i += len(ws.group(0))
            continue
        hit = None
        for x, r in regs:
            mm = r.match(rest)
            if mm and mm.group(1):
                hit = (x, len(mm.group(1)))
                break
        if hit:
            spans.append((rest[:hit[1]], hit[0]))
            i += hit[1]
            continue
        tok = re.match(r"^[A-Za-z0-9]+(?:['.][A-Za-z0-9]+)*", rest)
        tok = tok.group(0) if tok else rest[0]
        spans.append((tok, None))
        i += len(tok)
    return spans


def split_phrase_glosses(glosses, keep=()):
    keep = {k.lower() for k in keep}
    piece = lambda p: any(k == p or k.startswith(p + " ") for k in keep)  # noqa: E731 — ’s, ’ve been driving
    singles = {x["en"].lower(): x for x in glosses if not re.search(r"\s", x["en"].strip())}
    out, added = [], set()
    for x in glosses:
        words = x["en"].strip().split()
        cut = x["en"].find("’")
        if len(words) == 1 and cut > 0 and x["en"][:cut].lower() in keep and piece(x["en"][cut:].lower()):
            continue  # 줄임말 통째 뜻(it’s)은 빼고 조각(it, ’s)으로 누르게
        if len(words) < 2 or x["en"].lower() in keep:
            out.append(x)
            continue
        for raw in words:
            w = re.sub(r"^[“\"‘'(]+|[”\"’'),.;:!?]+$", "", raw)
            key = w.lower()
            if not w or key in added:
                continue
            cut = w.find("’")
            if cut > 0 and w[:cut].lower() in keep and piece(w[cut:].lower()):
                # 줄임말을 주어·동사로 나눠 찾을 때 (it’s → it + ’s)
                for part in (w[:cut], w[cut:]):
                    if part.lower() not in added:
                        added.add(part.lower())
                        if part.lower() not in singles:
                            out.append({"en": part, "ko": ""})
                continue
            own = singles.get(key, {}).get("ko") or (None if key in CONTEXT_WORDS else SHARED.get(key))
            if not own:
                if key in ARTICLES:
                    continue
                added.add(key)
                out.append({"en": w, "ko": ""})
                continue
            added.add(key)
            if key not in singles:
                out.append({"en": w, "ko": own})
    return out


def _lines(brief):
    out = []
    for k in ("ask", "reask", "explain", "praise", "say", "hint", "summary"):
        if brief.get(k):
            out.append(brief[k])
    out += brief.get("hints", []) or []
    out += list((brief.get("feedback") or {}).values())
    return out


def _check_line(where, line, errs):
    if line.count("?") > 1:
        errs.append(f"{where}: 물음표 둘 — {line}")
    if len(re.findall(r"[.?!~](\s|$)", line)) > 3:
        errs.append(f"{where}: 네 문장 이상 — {line}")


def check(lesson, senses):
    errs = []
    for it in lesson.get("intro", []):
        for v in it["brief"].values():
            _check_line(f"intro {it['id']}", v, errs)
    texts = [s["text"] for s in lesson["sentences"]]
    for s in lesson["sentences"]:
        known = [x["en"] for x in s["glosses"]] + [c["en"] for c in s.get("concepts", [])]
        for w in s.get("emphasis", []):
            if w not in known:
                errs.append(f"{s['id']}: emphasis {w} 뜻 없음")
        for c in s.get("slashes", []):
            if c not in s["text"]:
                errs.append(f"{s['id']}: 끊는 자리 {c} 없음")
        for m_ in s.get("modifiers", []):
            if m_ not in s["text"]:
                errs.append(f"{s['id']}: 수식어 [ ] {m_} 없음")
        for r in s.get("roles", []):
            # 「has … survived」처럼 떨어진 조각은 조각마다
            if any(part not in s["text"] for part in r["text"].split(" … ")):
                errs.append(f"{s['id']}: 끊어읽기 S·V {r['text']} 없음")
        for st in s["steps"]:
            b = st["brief"]
            for line in _lines(b):
                _check_line(st["id"], line, errs)
            shown = st.get("display") or s["text"]
            for ph in st.get("highlight", []) + st.get("highlight_alt", []) + st.get("faded", []) + st.get("shaded", []):
                if ph not in shown:
                    errs.append(f"{st['id']}: 강조 '{ph}'가 화면 문장에 없음")
            for f in st.get("faded", []):
                if f.strip().startswith("—") and "—" not in f.strip()[1:]:
                    errs.append(f"{st['id']}: 대시 하나 흐림 {f}")
            if st.get("bracket") and st["bracket"] not in shown:
                errs.append(f"{st['id']}: bracket 없음")
            if st["type"] == "choice":
                n = len(st["options"])
                right = [o for o in st["options"] if o.get("correct")]
                if not 2 <= n <= 3 or len(right) != 1:
                    errs.append(f"{st['id']}: 보기 {n}개 / 정답 {len(right)}개")
                elif re.search(r"[가-힣]", right[0]["label"]):
                    for line in [b["ask"], *b["hints"], *b.get("feedback", {}).values()]:
                        if right[0]["label"] in line:
                            errs.append(f"{st['id']}: 정답 보기를 미리 말함 — {line}")
            if st["type"] == "pick" and not st.get("order"):
                sp = [t.rstrip(".,;:!?") for t, gl in gloss_spans(shown, split_phrase_glosses(s["glosses"], st["candidates"])) if gl]
                for c in st["candidates"]:
                    if c not in sp:
                        errs.append(f"{st['id']}: 후보 '{c}'가 따로 안 눌림")
                for a in st["answers"]:
                    if a not in st["candidates"] and not st.get("match"):
                        errs.append(f"{st['id']}: 답 {a}가 후보에 없음")
        # 덩어리 안 내용어 뜻
        singles = {x["en"].lower() for x in s["glosses"] if not re.search(r"\s", x["en"].strip())}
        for x in s["glosses"]:
            ws = x["en"].strip().split()
            if len(ws) < 2:
                continue
            for raw in ws:
                k = re.sub(r"^[“\"‘'(]+|[”\"’'),.;:!?]+$", "", raw).lower()
                if not k or re.fullmatch(r"[\W\d_]+", k) or k in FUNCTION_WORDS or k in CONTEXT_WORDS:
                    continue
                if k not in singles and k not in SHARED:
                    errs.append(f"{s['id']}: 단어 뜻 없음 '{k}' ({x['en']})")
        # 다의 기능어
        toks = [t.lower() for t in re.findall(r"[A-Za-z]+", s["text"])]
        have = [x["word"].lower() for x in senses.get(s["id"], [])]
        for w in SENSE_WORDS:
            if toks.count(w) != have.count(w):
                errs.append(f"{s['id']}: 기능어 {w} 문장 {toks.count(w)}개 / 적은 것 {have.count(w)}개")
    ex = lesson.get("exam")
    if ex:
        und = ex.get("underline")
        for u in ([] if not und else und if isinstance(und, list) else [und]):
            if not any(u in t for t in texts):
                errs.append(f"exam: 밑줄 '{u}'가 문장에 없음")
        for line in [ex["brief"].get("ask", "")] + list(ex["brief"].get("option_feedback", {}).values()):
            _check_line("exam", line, errs)
    return errs


def fill_words(sentences, words):
    """덩어리 안 내용어에 단어 뜻이 없으면 채운다 — words(레슨 문맥 뜻) 먼저, 없으면 그대로 둔다(check가 잡는다)"""
    for s in sentences:
        singles = {x["en"].lower() for x in s["glosses"] if not re.search(r"\s", x["en"].strip())}
        for x in list(s["glosses"]):
            ws = x["en"].strip().split()
            if len(ws) < 2:
                continue
            for raw in ws:
                w = re.sub(r"^[“\"‘'(]+|[”\"’'),.;:!?]+$", "", raw)
                k = w.lower()
                if not k or re.fullmatch(r"[\W\d_]+", k) or k in FUNCTION_WORDS or k in CONTEXT_WORDS or k in singles or k in SHARED:
                    continue
                ko = words.get(k) or words.get(w) or KIT_WORDS.get(k)
                if ko:
                    s["glosses"].append({"en": w, "ko": ko})
                    singles.add(k)


# ── 마무리: 검사 → 칠판 정리 → 쓰기 ────────────────────────────────────

def finish(ID, lesson, *, senses, words=None, stories=None, topic_intro, chunks=None):
    sentences = lesson["sentences"]
    for s in sentences:
        for st in s["steps"]:
            for k in [k for k, v in st.items() if v is None]:
                st.pop(k)
    if chunks:
        fill_chunk_glosses(sentences, chunks)
    fill_words(sentences, words or {})
    if stories:
        story_boards.STORIES[ID] = stories
        story_boards.add_story_boards(ID, sentences)
    ids = [st["id"] for s in sentences for st in s["steps"]]
    dup = {x for x in ids if ids.count(x) > 1}
    errs = [f"스텝 id 겹침: {sorted(dup)}"] if dup else []
    errs += check(lesson, senses)
    if errs:
        print(f"✗ {ID}", file=sys.stderr)
        for e in errs:
            print("  " + e, file=sys.stderr)
        sys.exit(1)
    json.dump(lesson, open(f"{ROOT}/content/tutor/policy-lessons/{ID}.json", "w"), ensure_ascii=False, indent=2)
    json.dump({str(k): v for k, v in sorted(senses.items())},
              open(f"{ROOT}/content/tutor/function-senses/{ID}.json", "w"), ensure_ascii=False, indent=1)
    ref = json.load(open(f"{ROOT}/content/tutor/policy-copy/dajung/moeui-2026-03-21-music-researchers.json"))
    c = {
        "lesson": ID, "character": "dajung", "note": "생성물",
        "topic_intro": topic_intro,
        "closing": ref["closing"],
        "helps": {h["id"]: {"answer": h["brief"]} for s in sentences for h in s.get("helps", [])},
        "steps": {st["id"]: copy.deepcopy(st["brief"]) for s in sentences for st in s["steps"]},
        "exam": dict(lesson["exam"]["brief"]),
        "intro": {i["id"]: dict(i["brief"]) for i in lesson["intro"]},
        "ending": {**ref["ending"], "wrong": "이번엔 한 번 헷갈렸으니 {weeks} 뒤에 다시 한번 볼 거예요."},
    }
    json.dump(c, open(f"{ROOT}/content/tutor/policy-copy/dajung/{ID}.json", "w"), ensure_ascii=False, indent=2)
    print("ok", ID, len(ids), "steps")


def base_lesson(ID, *, source, topic, method, images, intro, exam, key_words, sentences, english="high", concept="high"):
    return {
        "id": ID, "kind": "policy", "version": "0.1", "source": source,
        "brief": {"topic": topic, "closing": "수고 인사"},
        "method": method,
        "read_button": "분석하러 갈게요",
        "read_first": True,
        "images": images,
        **({"intro_board": "method"} if "method" in images else {}),
        "intro": intro,
        "exam": exam,
        "key_words": key_words,
        "context": {"mode": "paper_review", "exam_relevance": "high", "time_budget": "normal"},
        "item": {"english_difficulty": english, "conceptual_difficulty": concept, "background_knowledge_required": "low",
                 "exam_importance": "high", "teaching_value": "high", "intervention_density": "normal"},
        "sentences": sentences,
        "passage_on_try": True,
    }


def exam_brief(ask, answer_explain, final_wrong, option_feedback, option_review=None):
    b = {"ask": ask, "first_correct": "맞았어요!", "first_wrong": "아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.",
         "final_correct": "정답이에요!", "answer_explain": answer_explain, "final_wrong": final_wrong,
         "option_feedback": option_feedback, "ask_first": "실제 시험처럼 풀어 봐요. 위 보기에서 답을 골라요."}
    if option_review:
        b["option_review"] = option_review
    return b


def review(rate, say, ask, choices, panel=None, rank_word="많은 학생이 헷갈린"):
    """많이 고른 오답 — 「같이 볼까요?」 → 설명(그림) → 어디서 헷갈렸는지 (버튼) → 답. choices = [(label, [skills], reply)]"""
    r = {"intro": f"아쉽게도 틀렸어요. 이 보기는 {rate}%나 고른, {rank_word} 보기예요. 같이 자세히 볼까요?",
         "intro_button": "같이 볼게요", "say": say, "ask": ask,
         "choices": [{"label": a, "skills": b, "reply": c} for a, b, c in choices]}
    if panel:
        r["panel"] = panel
    return r


METHOD_IMAGES = {
    "underline": {"src": "/assets/underline-method.svg", "alt": "밑줄 문제 푸는 법: ① 핵심 단어 찾기 ② 단어 사이의 관계 잡기", "kind": "drawing"},
    "vocab": {"src": "/assets/vocab-method.svg", "alt": "어휘 문제 푸는 법: ① 요지 잡기 ② 단어를 두 그룹으로 나누기 ③ 밑줄 단어가 맞는 쪽인지 보기", "kind": "drawing"},
    "insert": {"src": "/assets/insert-method.svg", "alt": "문장 넣기 푸는 법: ① 주어진 문장의 단서 찾기 ② 앞에 올 내용 예측하기 ③ 흐름이 끊기는 곳 찾기", "kind": "drawing"},
}
