"""초급 기본 — 문장마다 「주어·동사 찾기 + 뜻 풀어 주기」 또는 「해석 맞추기」 중 하나 (docs/tutor/templates/README.md §1-1).

같은 slot(`s<id>_basic`)에 두 방식을 두고 세션이 번갈아 낸다(최근에 덜 한 쪽). 해석 맞추기를 하면
주어·동사 찾기(roles 있는 pick)와 뜻 확인(`meaning_check`)은 건너뛴다. 긴 문장(20단어~)의 맞추기는
핵심어만 모은 문장(`display`)으로 한다.

    add_basic(sentences, 3, match_ko=[m("Nor are …", "…"), ": ", …], match_display="…",
              sv_new=sv_step(...), meaning="…", meaning_ids=["a2_nor"])
"""
import re


def m(en, ko):
    """해석 맞추기 칸 — 영어 덩어리와 그 칸의 한국어"""
    return {"en": en, "ko": ko}


def sv_ask(roles):
    """찾을 역할을 질문에 다 밝힌다 — 보어(C)·목적어(O)도 찾는데 「주어·동사」라고만 하면 안 된다 (2026-10-16 선생님)"""
    kinds = list(dict.fromkeys(roles.values()))
    names = {"S": "주어(S)", "V": "동사(V)", "O": "목적어(O)", "C": "보어(C)", "전목": "전치사 뒤 목적어(전목)"}
    parts = [names[k] for k in ["S", "V", "O", "C", "전목"] if k in kinds]
    many = len(roles) > len(kinds)
    return f"이 문장의 {'·'.join(parts)}를 {'모두 ' if many else ''}찾아볼까요?"


def sv_step(id, candidates, roles, wrong_by, explain, ask=None):
    """덩어리째 주어·동사(+O/C) 찾기 — 찾은 건 표시로 남는다"""
    return {
        "id": id, "type": "pick", "interaction": "word_pick", "shade": True, "no_unknown": True,
        "candidates": candidates, "answers": list(roles), "roles": roles,
        "brief": {"ask": ask or sv_ask(roles),
                  "wrong": "그건 주어·동사가 아니에요.", "wrong_by": wrong_by, "more": "좋아요! {n}개 남았어요.",
                  "praise": "다 찾았어요!", "explain": explain},
        "method": 0,
    }


def _in_order(text, chunks):
    def at(c):
        hit = re.search(r"(?<![A-Za-z])" + re.escape(c) + r"(?![A-Za-z])", text)
        return hit.start() if hit else text.index(c)
    return sorted(chunks, key=at)


def add_basic(sentences, sid, match_ko, *, sv_id=None, sv_new=None, meaning=None, meaning_ids=(),
              match_display=None, meaning_after=None):
    """
    sv_id: 이미 있는 주어·동사 찾기 스텝(모두에게 보이던 것) — 같은 자리에 묶기만 한다
    sv_new: 새 주어·동사 찾기(sv_step) — 초급에게만
    meaning: 새 뜻 풀기(초급만). 없으면 meaning_ids의 기존 화면이 뜻을 짚는다
    meaning_ids: 기존 뜻 질문·뜻 풀기 화면 — 맞추기를 하면 건너뛴다. 새 뜻 풀기는 그 뒤에 둔다
    meaning_after: 새 뜻 풀기를 이 스텝 뒤에 (그 스텝은 그대로 — 열쇠 질문이라 답을 먼저 말하면 안 될 때)
    """
    s_ = next(x for x in sentences if x["id"] == sid)
    steps = s_["steps"]
    slot = f"s{sid}_basic"
    if sv_id:
        sv = next(x for x in steps if x["id"] == sv_id)
        sv["slot"] = slot
        at = steps.index(sv)
    elif sv_new is None:
        # S·V 찾기 없이 해석 맞추기만 (It’s time to처럼 S·V를 묻기 어색한 문장 — 2026-10-18 선생님)
        sv = None
    else:
        sv = {**sv_new, "levels": ["초"], "slot": slot}
        at = 0
        while at < len(steps) and steps[at].get("before_read"):
            at += 1
        # 읽기 화면은 첫 스텝의 흐림을 따른다 — 원래 첫 스텝의 흐림을 이어받는다 (긴 문장은 이 찾기가 모두에게 나온다)
        if at < len(steps):
            for k in ("faded", "faded_note", "faded_tip"):
                if k in steps[at] and k not in sv:
                    sv[k] = steps[at][k]
        steps.insert(at, sv)
    shown = match_display or s_["text"]
    slots = [x for x in match_ko if not isinstance(x, str)]
    match = {
        "id": f"s{sid}_match", "type": "pick", "interaction": "word_pick", "levels": ["초"], **({"slot": slot} if sv else {}),
        "candidates": _in_order(shown, [x["en"] for x in slots]), "answers": [x["en"] for x in slots],
        "match": {"ko": match_ko},
        "brief": {"ask": "핵심어만 모았어요. 영어 덩어리를 끌어다 맞는 한국어 칸에 놓아 볼까요?" if match_display else
                  "영어 덩어리를 끌어다 맞는 한국어 칸에 놓아 볼까요?",
                  "wrong": "그 칸은 '{ko}'예요. 다른 덩어리를 놓아 봐요.", "more": "좋아요! {n}개 남았어요.",
                  "praise": "다 맞췄어요!", "explain": meaning or "칸마다 영어 덩어리의 뜻을 맞춰 봤어요."},
        "method": 0,
    }
    if match_display:
        match["display"] = match_display
    if sv:
        steps.insert(steps.index(sv) + 1, match)
    else:
        at = 0
        while at < len(steps) and steps[at].get("before_read"):
            at += 1
        steps.insert(at, match)
    last = steps.index(match)
    for mid in meaning_ids:
        x = next(x for x in steps if x["id"] == mid)
        x["meaning_check"] = True
        last = max(last, steps.index(x))
    if meaning_after:
        last = max(last, steps.index(next(x for x in steps if x["id"] == meaning_after)))
    share_tips(steps, [x for x in (sv, match) if x])
    if meaning:
        steps.insert(last + 1, {"id": f"s{sid}_basic_meaning", "type": "show", "interaction": "note",
                                "brief": {"say": meaning}, "method": 0, "button": "다음",
                                "levels": ["초"], "meaning_check": True})


def add_that_sv(sentences, sid, after_id, step_id, candidates, roles, wrong_by, explain, ask=None):
    """메인 주어·동사 다음, that(명사절) 안의 주어·동사(+O/C)를 한 번 더 — 그 절이 완전한 문장이고 내용이 핵심일 때
    (2026-10-16 선생님, 공통). 보이는 단계(levels)는 메인 주어·동사 찾기와 같게, 자리(slot)는 잇지 않는다"""
    s_ = next(x for x in sentences if x["id"] == sid)
    steps = s_["steps"]
    main = next(x for x in steps if x["id"] == after_id)
    st = sv_step(step_id, candidates, roles, wrong_by, explain,
                 ask=ask or "that 뒤가 핵심 내용이에요. that 안에서 주어(S)와 동사(V)를 찾아볼까요?")
    if main.get("levels"):
        st["levels"] = list(main["levels"])
    steps.insert(steps.index(main) + 1, st)
    return st


def share_tips(steps, targets):
    """그 문장의 💡 Tip을 초급 화면에도 — 초급은 Tip이 달린 화면을 건너뛸 수 있다 (2026-10-15 선생님)"""
    tips, seen = [], set()
    for st in steps:
        if st in targets:
            continue
        for tip in st.get("tips", []):
            if not tip.get("hint") and tip["label"] not in seen:
                seen.add(tip["label"])
                tips.append(tip)
    for st in targets:
        have = {x["label"] for x in st.get("tips", [])}
        add = [x for x in tips if x["label"] not in have]
        if add:
            st["tips"] = st.get("tips", []) + add


def fill_chunk_glosses(sentences, chunks):
    """찾기·맞추기 덩어리는 화면에서 따로 누를 수 있어야 한다 — 뜻이 없으면 채운다"""
    for s_ in sentences:
        have = {x["en"] for x in s_["glosses"]}
        for st in s_["steps"]:
            for c_ in ([] if st.get("order") else st.get("candidates", [])):
                if c_ not in have and c_ in chunks:
                    s_["glosses"].insert(0, {"en": c_, "ko": chunks[c_]})
                    have.add(c_)


def add_match(sentences, sid, match_ko, *, display=None, explain=None):
    """
    해석 맞추기만 더한다 — **모두에게**(levels 없음). 2026-10-20 엔진: 주어·동사 찾기(roles pick, _sv/_basic_sv)와
    핵심어 나열형 자유 해석(translate method 0)은 수업에서 빠지고, 그 문장에서는 해석 맞추기 pick이 단계와 상관없이 대신 나온다.
    맞추기 스텝이 없던 문장에 쓴다. slot은 그 문장의 `s<n>_basic`, 덩어리는 문장(또는 display)에 그대로 있는 구절,
    칸의 en은 candidates에 다 들어간다. 20단어 넘는 긴 문장은 핵심 덩어리 4~5개만(display로 줄인 문장).
    덩어리 뜻이 없으면 칸의 한국어로 glosses에 채운다(화면에서 따로 눌리게).
    """
    s_ = next(x for x in sentences if x["id"] == sid)
    steps = s_["steps"]
    assert not any(st.get("match") for st in steps), (sid, "해석 맞추기가 이미 있음")
    shown = display or s_["text"]
    slots = [x for x in match_ko if not isinstance(x, str)]
    for x in slots:
        assert x["en"] in shown, (sid, x["en"], "덩어리가 문장에 없음")
    have = {g["en"] for g in s_["glosses"]}
    for x in slots:
        if x["en"] not in have:
            s_["glosses"].insert(0, {"en": x["en"], "ko": x["ko"]})
            have.add(x["en"])
    match = {
        "id": f"s{sid}_match", "type": "pick", "interaction": "word_pick", "slot": f"s{sid}_basic",
        "candidates": _in_order(shown, [x["en"] for x in slots]), "answers": [x["en"] for x in slots],
        "match": {"ko": match_ko},
        "brief": {"ask": "핵심어만 모았어요. 영어 덩어리를 끌어다 맞는 한국어 칸에 놓아 볼까요?" if display else
                  "영어 덩어리를 끌어다 맞는 한국어 칸에 놓아 볼까요?",
                  "wrong": "그 칸은 '{ko}'예요. 다른 덩어리를 놓아 봐요.", "more": "좋아요! {n}개 남았어요.",
                  "praise": "다 맞췄어요!", "explain": explain or "칸마다 영어 덩어리의 뜻을 맞춰 봤어요."},
        "method": 0,
    }
    if display:
        match["display"] = display
    sv = next((st for st in steps if st["type"] == "pick" and (st.get("roles") or re.search(r"_svc?$", st["id"]))), None)
    if sv:
        at = steps.index(sv) + 1
    else:
        at = 0
        while at < len(steps) and steps[at].get("before_read"):
            at += 1
    steps.insert(at, match)
    share_tips(steps, [match])


REF_KO = {"it": "그것", "its": "그것의", "this": "이것", "that": "그것", "these": "이것들", "those": "그것들", "they": "그들(그것들)",
          "them": "그들을", "their": "그들의", "such": "그러한", "one": "하나", "so": "그렇게", "he": "그", "she": "그녀", "his": "그의",
          "her": "그녀의", "him": "그를"}


def add_refers(sentences, sid, refers, ko=None):
    """
    가리키는 말(it·its·this·that·they·these·such …) → 가리키는 것. 문장 필드 `refers` — 학생이 그 낱말을 누르면 뜻 뒤에
    「→ 가리키는 것: …」이 붙는다(session.ts glosses). 키는 문장에 나오는 그대로, 값은 영어+한국어 ("translation(번역)").
    그 낱말은 glosses에도 있어야 해서 없으면 채운다(ko 또는 기본 뜻). 더 긴 뜻 덩어리가 그 말을 품고 있으면 화면에서
    따로 안 눌리니 그 덩어리를 키로 쓴다 — 경고를 찍는다
    """
    s_ = next(x for x in sentences if x["id"] == sid)
    s_["refers"] = {**s_.get("refers", {}), **refers}
    have = {x["en"] for x in s_["glosses"]}
    for k in refers:
        assert k in s_["text"], (sid, k, "문장에 없음")
        if k not in have:
            s_["glosses"].append({"en": k, "ko": (ko or {}).get(k) or REF_KO.get(k.lower()) or k})
            have.add(k)
        longer = [x["en"] for x in s_["glosses"]
                  if x["en"] != k and re.search(r"(?<![A-Za-z])" + re.escape(k) + r"(?![A-Za-z’])", x["en"])]
        if longer and s_["text"].count(k) <= 1:
            print(f"  ⚠ refers s{sid} '{k}': 더 긴 뜻 덩어리 {longer} 안에 있어 따로 안 눌릴 수 있음")
