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
