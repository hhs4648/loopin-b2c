"""2026년 3월 30번 레슨 + 대사를 만든다.

레슨 JSON(content/tutor/policy-lessons/…)과 대사(content/tutor/policy-copy/dajung/…)는 이 스크립트의
생성물이다. 고칠 때는 여기를 고치고 다시 돌린 뒤 도장을 찍는다:

    python3 scripts/lessons/gen_moeui_2026_03_30.py
    npm run policy:copy stamp moeui-2026-03-30-names-and-differences

1~11문장 모두 선생님과 화면을 보며 정했다.
"""
import sys
import copy
import json
import os

ID = "moeui-2026-03-30-names-and-differences"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

LEFT = "이름 붙이기 · 같게 묶음"
RIGHT = "하나하나 다름"
CLUSTER = {"words": ["conceptualize", "categorize", "put a name on"]}


# 수업 끝 「오늘 헷갈렸던 곳」 — 틀렸거나 힌트를 본 질문만 이 한 줄로 모아 보여 준다
POINTS = {
    "s1_q": "abstract away from = ~에서 떼어 내다 → 이름을 붙이면 하나하나의 특징(particularities)은 무시된다 (글의 요지)",
    "s3_q": "leave out = abstract away → 보통 명사는 차이(differences)를 빠뜨린다",
    "s5_sort": "'Lawn'도 보통 명사(이름) → 이름 붙이기 그룹",
    "s6_sort": "Zoom in(가까이 보면) → individuality(개별성)·uniqueness(고유성) = 하나하나 다름",
    "s7_q": "No two A are alike = 똑같은 A 두 개는 없다 → 하나하나 다 다르다",
    "s8_sort": "For most practical purposes = 대부분의 실용적인 목적에서는 → 차이를 무시해도 된다",
    "s9_sort": "Not so = 앞 문장과 반대 · do matter = 정말 중요하다(강조의 do) → 관리인에겐 차이가 중요",
    "s10_q": "need not be = ~될 필요가 없다 → 무한한 기억력이면 풀잎을 묶을 필요가 없다",
    "s10_distinct": "distinct = 독특한, 뚜렷이 다른 · with = ~를 가진",
    "s10_fellows": "fellows = 같은 무리 → 여기서는 다른 풀잎들",
    "s10_cocat": "co-categorize = 한 범주로 같이 묶다 (need not이 붙어 '묶을 필요가 없다')",
    "s11_each": "Each = 10문장의 each blade of grass(각각의 풀잎)",
    "s11_do": "as you yourself do의 do = have your own name (앞 동사를 반복하지 않으려고 do)",
    "s11_could": "could = 불가능한 가정 '~할 수 있을 텐데' (실제로 그렇다는 게 아님)",
}

SORT_LEFT = "왼쪽 · 이름 붙이기"
SORT_RIGHT = "오른쪽 · 하나하나 다름"


def board(left_words, right_words=None, caption=None, fresh_cluster=False, between="≠", right_label=None, sort=None):
    """지도 — 단어 뒤에 '*'가 붙으면 이번 문장에서 새로 붙은 것"""
    def words(ws):
        return [{"text": w.rstrip("*"), **({"fresh": True} if w.endswith("*") else {})} for w in ws]
    p = {
        "kind": "groups",
        "title": "단어 지도",
        "left": {"label": LEFT, "cluster": {**CLUSTER, **({"fresh": True} if fresh_cluster else {})}, "words": words(left_words)},
    }
    if right_words is not None:
        p["right"] = {"label": right_label or RIGHT, "words": words(right_words)}
        # abstract away · leave out은 그룹 단어가 아니라 오른쪽 → 왼쪽 화살표(과정)
        proc = [w for w in left_words if w.rstrip("*") in ("abstract away", "leave out")]
        p["left"]["words"] = [w for w in p["left"]["words"] if w["text"] not in ("abstract away", "leave out")]
        if proc:
            p["process"] = {"arrow": "←", "words": [
                {"text": ("= " if w.startswith("leave") else "") + w.rstrip("*"), **({"fresh": True} if w.endswith("*") else {})} for w in proc]}
        else:
            p["between"] = ""
    if sort:
        # 학생이 끌어 넣을 단어 — 왼쪽/오른쪽 보기 글은 SORT_LEFT/SORT_RIGHT
        p["sort"] = {"words": sort, "left": SORT_LEFT, "right": SORT_RIGHT}
    if caption:
        p["caption"] = caption
    return p


def choice(id, ask, options, hint, praise="맞아요!", method=1, why=None, **extra):
    """why: 틀렸을 때 「아쉽게도 틀렸어요.」 뒤의 이유 (없으면 힌트). point: 수업 끝 「헷갈린 포인트」 한 줄 (POINTS)"""
    feedback = {o[0]: why or hint for o in options if not o[2]}
    brief = {"ask": ask, "reask": "그럼 하나 골라 봐요.", "hints": [hint, hint], "explain": hint, "praise": praise, "feedback": feedback}
    if id in POINTS:
        brief["point"] = POINTS[id]
    return {
        "id": id, "type": "choice", "interaction": "meaning_choice", "one_try": True,
        "brief": brief,
        "options": [{"id": o[0], "label": o[1], **({"correct": True} if o[2] else {})} for o in options],
        "method": method, **extra,
    }


def show(id, say, method=1, button="다음 문장", **extra):
    return {"id": id, "type": "show", "interaction": "note", "brief": {"say": say}, "method": method, "button": button, **extra}


def g(en, ko):
    return {"en": en, "ko": ko}


FOUR_NOUNS = {"kind": "picture", "title": "칠판 그림", "src": "/assets/daisies-clover.svg", "alt": "잔디밭에 핀 데이지와 클로버 꽃",
              "words": [{"text": f"“{w}”", "quote": True} for w in ["daisies", "clover", "flower", "lawn"]],
              "words_label": "Those four ordinary nouns · 그 네 개의 보통 명사"}

S1 = "Every time you conceptualize, categorize, and put a name on something that is not a proper name, you abstract away from its particularities."
L = ["abstract away"]
R = ["proper name", "particularities"]

S5_LEFT = L + ["four ordinary nouns", "leave out", "“Flower”"]
S5_BEFORE = board(S5_LEFT, R + ["differences"])
S5_AFTER = board(S5_LEFT + ["“Lawn”*"], R + ["differences"], "'잔디'도 이름")
S7_LEFT = L + ["four ordinary nouns", "leave out", "“Flower”", "“Lawn”", "quick glance", "uniformly"]
S7_RIGHT = R + ["differences", "individuality", "uniqueness", "no two … alike"]
S8_BEFORE = board(S7_LEFT, S7_RIGHT)
S8_AFTER = board(S7_LEFT + ["practical purposes*"], S7_RIGHT, "보통 목적 → 차이를 무시해도 됨")
S9_BEFORE = board(S7_LEFT + ["practical purposes"], S7_RIGHT)
S9_AFTER = board(S7_LEFT + ["practical purposes"], S7_RIGHT + ["groundskeeper*"], "관리인에겐 → 차이가 중요")
S10_LEFT = S7_LEFT + ["practical purposes"]
S10_RIGHT = S7_RIGHT + ["groundskeeper"]
S10_BEFORE = board(S10_LEFT, S10_RIGHT)
S10_MID = board(S10_LEFT, S10_RIGHT + ["distinct"])
S10_AFTER = board(S10_LEFT + ["co-categorize*"], S10_RIGHT + ["distinct"], "need not + co-categorize → 묶을 필요 없음")
S6_LEFT = L + ["four ordinary nouns", "leave out", "“Flower”", "“Lawn”"]
S6_BEFORE = board(S6_LEFT, R + ["differences"])
S6_AFTER = board(S6_LEFT, R + ["differences", "individuality*", "uniqueness*"], "가까이 보면 → 하나하나 다름")

sentences = [
    {
        "id": 1, "text": S1,
        "model_translation": "고유 명사가 아닌 이름을 붙여 무언가를 개념화하고, 범주화하고, 명명할 때마다, 우리는 그 대상의 세부 특징을 무시한다.",
        "teaching_value": "high",
        "glosses": [
            g("conceptualize", "개념화하다"),
            g("categorize", "범주화하다, 분류하다"),
            g("put a name on", "~에 이름을 붙이다"),
            g("proper name", "고유명사 · 하나뿐인 대상의 이름이에요 (철수, 서울)"),
            g("abstract away from", "~에서 떼어 내다 · 여기서는 '무시하다'로 이해하면 돼요"),
            g("particularities", "세부 특징 · 하나하나가 가진 특성"),
        ],
        "steps": [
            # 처음부터 「같은 뜻이에요」라고 알려 주면 갑작스럽다 → 학생이 고른다 (2026-10-21 선생님):
            # 네 말 중 비슷한 뜻 셋(노랑) → 반대 뜻 하나(민트) → 그다음 설명·칠판
            {"id": "s1_similar", "type": "pick", "interaction": "word_pick", "method": 0,
             "candidates": ["conceptualize", "categorize", "put a name on", "proper name"],
             "answers": ["conceptualize", "categorize", "put a name on"], "found_tone": "hl",
             "brief": {"ask": "이 네 말 중에서 비슷한 뜻을 가진 말 세 개를 골라 볼까요?",
                       "wrong": "proper name은 '고유명사'예요. 나머지 셋과 뜻이 달라요.",
                       "more": "좋아요! {n}개 남았어요.",
                       "praise": "맞아요! 셋 다 '이름 붙여 묶는다'는 뜻이에요.",
                       "explain": "conceptualize, categorize, put a name on, 셋 다 '이름 붙여 묶는다'는 뜻이에요.",
                       "point": "conceptualize = categorize = put a name on (이름 붙여 묶다)"}},
            {"id": "s1_opposite", "type": "pick", "interaction": "word_pick", "method": 0,
             "candidates": ["conceptualize", "categorize", "put a name on", "proper name"],
             "answers": ["proper name"],
             "highlight": ["conceptualize", "categorize", "put a name on"],
             "brief": {"ask": "그럼 이 셋과 반대 의미를 가진 말은 무엇일까요?",
                       "wrong": "그건 앞에서 고른 비슷한 말이에요.",
                       "more": "좋아요! {n}개 남았어요.",
                       "praise": "맞아요!",
                       "explain": "'not a proper name'처럼 not이 붙어 있어서, proper name이 반대 의미예요."}},
            # 비슷한 말 셋은 노랑, 반대 말은 민트, not은 크게 움직이게(엔진이 부정어를 알아서).
            # 칠판은 아래에 두면 대사·문장이 잘려서 열고 닫는 서랍으로, 긴 대사는 두 화면으로 (2026-10-23 선생님)
            show("s1_board",
                 "'something that is not a proper name' — not이 붙었으니 proper name(고유 명사)은 이름 붙여 묶는 것의 반대편이에요.",
                 method=0, button="다음",
                 panel=board([], ["proper name*"], fresh_cluster=True, right_label="반대쪽"),
                 highlight=["conceptualize", "categorize", "put a name on", "not"], highlight_alt=["proper name"]),
            show("s1_not_tip",
                 "시험 꿀팁! not, isn't, don't가 붙은 말은 바로 반대 그룹에 놓으면 돼요.",
                 method=0, button="다음",
                 highlight=["not"], highlight_alt=["proper name"]),
            show("s1_abstract",
                 "이름을 붙이면 'abstract away from its particularities' 한대요.",
                 method=0, button="다음",
                 highlight=["abstract away from its particularities"]),
            choice("s1_q",
                   "particularities는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", "오른쪽 · 반대쪽", True)],
                   "'abstract away from'은 '~에서 떼어 내다'예요. 이름을 붙이면 particularities와 멀어진다는 말이에요.",
                   why="'abstract away from'은 '~에서 떼어 내다'예요. 이름을 붙이면 particularities는 떨어져 나가니, 같은 그룹이 아니에요.",
                   method=0,
                   panel={**board([], ["proper name"], right_label="반대쪽"), "sort": {"words": ["particularities"], "left": SORT_LEFT, "right": "오른쪽 · 반대쪽"}},
                   highlight=["abstract away", "particularities"]),
            show("s1_map",
                 "이름을 붙여 묶으면 하나하나의 특징은 무시된다, 이게 이 글의 요지예요. 오른쪽에서 왼쪽으로 가는 화살표, 이 과정이 'abstract away'예요.",
                 panel=board(["abstract away*"], ["proper name", "particularities*"], "하나하나의 특징 → 이름으로 묶이며 무시")),
        ],
    },
    {
        "id": 2, "text": "Picture daisies and clover flowers in a lawn.",
        "model_translation": "잔디에 있는 데이지와 클로버 꽃을 떠올려 보라.",
        "teaching_value": "medium",
        "glosses": [g("Picture", "상상해 보다 · 여기서는 '그림'이 아니라 동사예요"), g("daisies", "데이지 꽃"), g("clover", "클로버"), g("lawn", "잔디밭")],
        "steps": [
            show("s2_picture", "여기서 'Picture'는 '그림'이 아니라 '상상해 보다'라는 동사예요. 잔디밭에 핀 데이지와 클로버를 한번 상상해 보래요.",
                 method=0,
                 panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/daisies-clover.svg",
                        "alt": "잔디밭에 핀 데이지와 클로버 꽃",
                        "words": [{"text": f"“{w}”", "quote": True, "fresh": True} for w in ["daisies", "clover", "flower", "lawn"]]},
                 highlight=["Picture"],
                 tips=[{"label": "명령문", "text": "문장 맨 앞에 주어 없이 동사가 오면 명령문이에요. '~해 봐라'로 읽으면 돼요. 여기선 'Picture …'가 '~을 상상해 봐라'예요."}]),
        ],
    },
    {
        "id": 3, "text": "Those four ordinary nouns leave out their ①differences.",
        "model_translation": "그 네 개의 보통 명사는 그것들의 차이를 생략한다.",
        "teaching_value": "high",
        "glosses": [g("Those four ordinary nouns", "그 네 개의 보통 명사 · 앞 문장의 daisies, clover, flower, lawn이에요"), g("ordinary nouns", "보통 명사"), g("leave out", "빠뜨리다, 생략하다"), g("differences", "차이")],
        "steps": [
            show("s3_nouns", "'Those four ordinary nouns'는 앞 문장의 네 단어예요. daisies, clover, flower, lawn 모두 보통 명사, 즉 이름이에요.",
                 method=0, button="다음",
                 panel=FOUR_NOUNS,
                 highlight=["Those four ordinary nouns"]),
            choice("s3_q",
                   "이 네 이름은 그것들의 differences를 빠뜨린대요(leave out). differences는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "1문장에서 이름을 붙이면 무엇이 떨어져 나갔는지 떠올려 봐요.",
                   why="이름은 차이를 빠뜨려요(leave out). 이름 쪽이 아니라, 빠져나가는 particularities와 같은 쪽이에요.",
                   method=1,
                   panel=board(L + ["four ordinary nouns*"], R, sort=["differences"]),
                   highlight=["leave out their ①differences"]),
            show("s3_map", "'leave out'은 1문장의 'abstract away'와 같은 말, 같은 화살표예요. 데이지도 송이마다 모양이 다른데, 다 '데이지'라고 부르면 그 차이는 빠져 버려요.",
                 button="다음",
                 panel=board(L + ["four ordinary nouns", "leave out*"], R + ["differences*"], "abstract away = leave out")),
            show("s3_check", "그래서 ①differences는 문맥에 맞아요. 이름은 하나하나의 차이를 빠뜨린다는 1문장 요지와 그대로 이어지거든요.",
                 method=2,
                 # 결론 화면엔 칠판 없이 지문만 — 칠판이 너무 많으면 영어를 못 읽는다 (2026-10-20 선생님)
                 highlight=["①differences"]),
        ],
    },
    {
        "id": 4, "text": "“Flower” co-categorizes the white and yellow types with the beige ones, and all the many other sorts to be found elsewhere.",
        "model_translation": "'꽃'이라는 말은 흰색과 노란색 종류를 베이지색 종류, 그리고 다른 곳의 수많은 종류와 함께 하나의 범주로 묶는다.",
        "teaching_value": "low",
        "glosses": [g("co-categorizes", "한 범주로 같이 묶다"), g("types", "종류"), g("beige", "베이지색"), g("sorts", "종류"), g("elsewhere", "다른 곳에서")],
        "steps": [
            show("s4_skim", "앞 문장의 반복이에요. 'Flower'도 세세한 차이를 무시하고 꽃을 다 묶어요. 앞을 이해했다면 깊게 안 읽어도 돼요.",
                 panel=board(L + ["four ordinary nouns", "leave out", "“Flower”*"], R + ["differences"], "'꽃' → 색이 달라도 한데 묶음"),
                 shaded=["“Flower” co-categorizes the white and yellow types with the beige ones, and all the many other sorts to be found elsewhere."]),
        ],
    },
    {
        "id": 5, "text": "“Lawn” ②acknowledges the varieties of grass and all the nongrassy plants that are there.",
        "model_translation": "'잔디'라는 말은 그곳의 다양한 풀과 풀이 아닌 모든 식물을 인정한다(→ 무시한다).",
        "teaching_value": "high",
        "glosses": [g("acknowledges", "인정하다"), g("varieties", "다양한 종류"), g("nongrassy plants", "풀이 아닌 식물")],
        "steps": [
            # 정답 문장이지만 ②는 여기서 말하지 않는다 — 마지막 문제에서 학생이 맞힌다
            choice("s5_sort",
                   "이번엔 'Lawn(잔디)'이에요. 'Lawn'은 어느 그룹일까요?",
                   [("o0", SORT_LEFT, True), ("o1", SORT_RIGHT, False)],
                   "2문장의 네 이름(daisies, clover, flower, lawn)을 떠올려 봐요.",
                   why="'Lawn'은 2문장의 네 이름 중 하나예요. 이름이니까 이름 붙이는 쪽이에요.",
                   panel={**S5_BEFORE, "sort": {"words": ["“Lawn”"], "left": SORT_LEFT, "right": SORT_RIGHT}}),
            show("s5_map", "'Lawn'도 2문장의 네 이름 중 하나라서 왼쪽 그룹이에요.",
                 panel=S5_AFTER),
        ],
    },
    {
        "id": 6, "text": "Zoom in, and you will find individuality and uniqueness everywhere.",
        "model_translation": "확대해 보면, 개별성과 고유성을 어디에서나 발견할 것이다.",
        "teaching_value": "high",
        "glosses": [g("Zoom in", "확대하다, 가까이 보다"), g("individuality", "개별성 · 하나하나가 따로인 성질"), g("uniqueness", "고유성 · 하나뿐인 성질"), g("everywhere", "어디에서나")],
        "steps": [
            choice("s6_sort",
                   "가까이 보면(Zoom in) individuality와 uniqueness가 보인대요. 이 두 단어는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "individuality는 '개별성', uniqueness는 '고유성'이에요. 이름으로 묶는 쪽일지, 하나하나 따로인 쪽일지 생각해 봐요.",
                   panel={**S6_BEFORE, "sort": {"words": ["individuality", "uniqueness"], "left": SORT_LEFT, "right": SORT_RIGHT}},
                   why="individuality는 '개별성', uniqueness는 '고유성'이에요. 이름으로 묶는 게 아니라 하나하나 따로라는 말이에요.",
                   highlight=["individuality and uniqueness"]),
            show("s6_map", "가까이 들여다보면 하나하나 다 달라요. 그래서 개별성과 고유성은 오른쪽 그룹이에요.",
                 panel=S6_AFTER),
        ],
    },
    {
        "id": 7, "text": "No two daisies, no two clovers, are exactly ③alike, and yet they present to a quick glance a carpet patterned uniformly enough.",
        "model_translation": "어떤 데이지 두 송이도, 어떤 클로버 두 개도 정확히 같지 않지만, 힐끗 보면 충분히 균일한 무늬의 카펫으로 보인다.",
        "teaching_value": "high",
        "glosses": [g("alike", "비슷한, 같은"), g("and yet", "그러나 · yet이 문장 앞에 오면 '그러나'예요"), g("present", "(모습을) 보이다, 나타내다 · 여기서는 '~처럼 보이다'"), g("to a quick glance", "힐끗 보기에"), g("quick glance", "힐끗 보기"), g("patterned", "무늬가 있는"), g("uniformly", "균일하게")],
        "steps": [
            choice("s7_q",
                   "'No two daisies … are exactly alike'는 무슨 뜻일까요?",
                   [("o0", "모든 데이지가 똑같다", False), ("o1", "두 송이만 똑같다", False), ("o2", "똑같은 두 송이는 없다", True)],
                   "'No'가 'two daisies' 앞에 붙어 있어요. 그런 두 송이가 '없다'는 말이에요.",
                   tips=[{"label": "No two A are alike", "text": "'똑같은 A 두 개는 없다', 즉 'A는 하나하나 다 다르다'예요. 부정이 주어에 붙어서 거꾸로 읽기 쉬워요."}]),
            show("s7_yet", "'yet'이 문장 앞에 나오면 '그러나'라는 뜻이에요. 'and yet' 앞은 '다 다르다', 뒤는 '균일해 보인다'로 서로 반대예요.",
                 button="다음",
                 highlight=["and yet"],
                 tips=[{"label": "to a quick glance", "text": "'to + 보는 눈'은 '~가 보기에'예요 (to the naked eye: 맨눈으로 보기에). 그래서 'they present to a quick glance a carpet'은 '힐끗 보기에 그것들은 카펫의 모습을 보인다', 즉 '힐끗 보면 카펫처럼 보인다'예요."}]),
            show("s7_map", "가까이 보면 다 다르지만, 힐끗 보면 균일한(uniformly) 카펫처럼 보인대요.",
                 panel=board(L + ["four ordinary nouns", "leave out", "“Flower”", "“Lawn”", "quick glance*", "uniformly*"],
                             R + ["differences", "individuality", "uniqueness", "no two … alike*"], "가까이 → 다름 ↔ 힐끗 → 균일")),
        ],
    },
    {
        "id": 8, "text": "For most practical purposes, the differences can be ④ignored—making a daisy chain, sunbathing, and the like.",
        "model_translation": "데이지 꽃 사슬 만들기, 일광욕 같은 대부분의 실용적인 목적에서는 그 차이를 무시할 수 있다.",
        "teaching_value": "high",
        "glosses": [g("practical purposes", "실용적인 목적"), g("ignored", "무시되는"), g("daisy chain", "데이지 꽃목걸이"), g("sunbathing", "일광욕"), g("and the like", "~ 등")],
        "steps": [
            choice("s8_sort",
                   "'For most practical purposes(대부분의 실용적인 목적에서는)' 차이를 무시해도 된대요. practical purposes는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, True), ("o1", SORT_RIGHT, False)],
                   "대시(—) 뒤 예시를 봐요. 꽃목걸이를 만들거나 일광욕할 때 풀 종류를 따지나요?",
                   why="꽃목걸이나 일광욕 같은 보통 목적에서는 차이를 무시해요. 그래서 이름으로 묶는 쪽이에요.",
                   # 대시(—)가 하나뿐 — 삽입이 아니라 앞말의 예시라 흐리지 않는다 (힌트도 대시 뒤를 보라고 한다)
                   panel={**S8_BEFORE, "sort": {"words": ["practical purposes"], "left": SORT_LEFT, "right": SORT_RIGHT}}),
            show("s8_map", "보통 때는 풀과 꽃의 차이를 무시해도 돼요.",
                 panel=S8_AFTER),
        ],
    },
    {
        "id": 9, "text": "Not so, however, for the groundskeeper of a sports stadium, where the constituent grasses and their stages of growth really do matter.",
        "model_translation": "그러나 스포츠 경기장 관리인에게는 그렇지 않은데, 그곳에서는 잔디를 이루는 풀들과 그 성장 단계가 정말 중요하다.",
        "teaching_value": "medium",
        "glosses": [g("Not so", "그렇지 않다 · 앞 문장의 '무시해도 된다'를 뒤집어요"), g("groundskeeper", "경기장 관리인"), g("stadium", "경기장"), g("constituent", "구성하는"), g("stages of growth", "성장 단계"), g("really do matter", "정말 중요하다")],
        "steps": [
            choice("s9_sort",
                   "경기장 관리인(groundskeeper)에게는 풀 종류와 자라는 단계가 정말 중요하대요. groundskeeper는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "'really do matter(정말 중요하다)'를 봐요. 관리인에게 무엇이 중요한지 생각해 봐요.",
                   why="관리인에게는 풀 하나하나의 차이가 중요해요. 그래서 하나하나 다른 쪽이에요.",
                   panel={**S9_BEFORE, "sort": {"words": ["groundskeeper"], "left": SORT_LEFT, "right": SORT_RIGHT}},
                   tips=[{"label": "do matter", "text": "matter는 동사로 '중요하다'예요. 'do matter'의 do는 '하다'가 아니라 강조의 do라서, '정말 중요하다'로 읽어요."}]),
            show("s9_map", "관리인에게는 풀 하나하나의 차이가 중요해요.",
                 button="다음",
                 panel=S9_AFTER),
            # 단어 그룹은 잠시 치우고 8·9문장의 반대 관계만 보여 준다
            show("s9_contrast", "'Not so'는 '그렇지 않다'예요. 그래서 8문장과 9문장은 서로 반대 관계예요.",
                 panel={"kind": "contrast", "title": "Not so → 반대 관계", "between": "↔",
                        "left": {"title": "8문장 · practical purposes", "text": "꽃목걸이, 일광욕 → 차이를 무시해도 돼요"},
                        "right": {"title": "9문장 · groundskeeper", "text": "경기장 관리 → 차이가 정말 중요해요"}},
                 highlight=["Not so"]),
        ],
    },
    {
        "id": 10, "text": "And to an infinite mind, with infinite memory, each blade of grass, with its own distinct life history, need not be ⑤co-categorized with all its fellows.",
        "model_translation": "그리고 무한한 기억력을 지닌 무한한 정신에게, 고유한 생애를 지닌 각각의 풀잎은 다른 모든 풀잎과 한 범주로 묶일 필요가 없다.",
        "teaching_value": "high",
        "glosses": [g("infinite mind", "무한한 정신 · 여기서는 기억력이 무한한 사람이에요"), g("blade", "칼날 · 여기서는 '풀잎'이에요"), g("distinct", "독특한, 뚜렷이 다른"), g("need not be", "~될 필요가 없다"), g("co-categorized", "한 범주로 같이 묶인"), g("fellows", "동료, 같은 무리")],
        "steps": [
            choice("s10_q",
                   "무한한 정신(infinite mind)이라면, 풀잎을 모두 한 범주로 묶어야 할까요?",
                   [("o0", "묶어야 해요", False), ("o1", "묶을 필요가 없어요", True)],
                   "'need not be'를 봐요. 'must'와 반대예요.",
                   # infinite mind = 무한한 기억력을 가진 사람. 학생이 모를 테니 그림으로
                   panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/infinite-mind-blades.svg",
                          "alt": "무한한 기억력을 가진 사람(infinite mind)과, 모양이 하나하나 다른 풀잎들. 화살표가 풀잎 하나(blade of grass)를 가리킨다"},
                   faded=[", with infinite memory,", ", with its own distinct life history,"],
                   tips=[{"label": "blade", "text": "'blade'는 원래 '칼날'이라는 뜻이에요. 'blade of grass'처럼 쓰면 칼날처럼 가늘고 긴 '풀잎'을 말해요."}]),
            show("s10_imagine", "사람은 무한한 기억력을 가질 수 없어요. 그러니 이 문장은 '만약 그런 정신이 있다면'이라는 불가능한 상황을 가정하고 있어요.",
                 method=1, button="다음",
                 panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/infinite-mind-blades.svg",
                        "alt": "무한한 기억력을 가진 사람(infinite mind)과, 모양이 하나하나 다른 풀잎들. 화살표가 풀잎 하나(blade of grass)를 가리킨다"},
                 highlight=["to an infinite mind"],
                 faded=[", with its own distinct life history,"]),
            choice("s10_distinct",
                   "풀잎마다 'its own distinct life history'가 있대요. distinct는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "distinct는 '독특한, 뚜렷이 다른'이에요. 풀잎끼리 묶이는 말일지, 따로인 말일지 생각해 봐요.",
                   why="distinct는 '독특한, 뚜렷이 다른'이에요. 풀잎 하나하나가 따로라는 말이라 하나하나 다른 쪽이에요.",
                   method=1,
                   panel={**S10_BEFORE, "sort": {"words": ["distinct"], "left": SORT_LEFT, "right": SORT_RIGHT}},
                   highlight=["distinct"],
                   faded=[", with infinite memory,"],
                   tips=[{"label": "with = ~를 가진", "text": "'with'는 여기서 '~를 가진'이라는 뜻이에요. 'with infinite memory'는 '무한한 기억력을 가진', 'with its own distinct life history'는 '자기만의 독특한 생애를 가진'이에요."}]),
            choice("s10_fellows",
                   "'all its fellows'의 its는 풀잎을 가리켜요. 여기서 fellows는 무엇일까요?",
                   [("o0", "사람 친구들", False), ("o1", "다른 풀잎들", True), ("o2", "무한한 정신", False)],
                   "fellow는 원래 '동료, 같은 무리'예요. 풀잎의 동료라면 누구일까요?",
                   why="fellow는 '동료, 같은 무리'예요. its가 풀잎이니까, 같은 잔디밭에서 함께 자라는 같은 무리를 말해요.",
                   method=1,
                   panel=S10_MID,
                   highlight=["all its fellows"],
                   faded=[", with infinite memory,", ", with its own distinct life history,"]),
            choice("s10_cocat",
                   "'co-categorized with all its fellows'의 co-categorize는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, True), ("o1", SORT_RIGHT, False)],
                   "4문장의 '“Flower” co-categorizes …'를 떠올려 봐요. 꽃들을 어떻게 했죠?",
                   why="co-categorize는 '한 범주로 같이 묶다'예요. 이름으로 묶는 쪽이에요.",
                   method=1,
                   panel={**S10_MID, "sort": {"words": ["co-categorize"], "left": SORT_LEFT, "right": SORT_RIGHT}},
                   highlight=["⑤co-categorized"],
                   faded=[", with infinite memory,", ", with its own distinct life history,"]),
            show("s10_map", "co-categorize는 '묶는' 쪽 말이에요. 그런데 앞에 'need not'이 있어서, 다른 풀잎들과 묶을 필요가 없다는 뜻이 돼요.",
                 panel=S10_AFTER,
                 highlight=["need not be"],
                 faded=[", with infinite memory,", ", with its own distinct life history,"]),
        ],
    },
    {
        "id": 11, "text": "Each could have its own name, as you yourself do.",
        "model_translation": "여러분 자신이 그러하듯, 각각은 자기만의 이름을 가질 수 있다.",
        "teaching_value": "medium",
        "glosses": [g("its own name", "자기만의 이름 · 고유명사처럼"), g("as you yourself do", "여러분 자신이 그러하듯")],
        "steps": [
            # 끌어 넣기는 여기까지 충분했다 — 확인 질문 세 개로 짧게. proper name은 꺼내지 않는다
            choice("s11_each",
                   "마지막 문장이에요. 'Each'는 무엇을 가리킬까요?",
                   [("o0", "각각의 사람", False), ("o1", "각각의 풀잎", True), ("o2", "각각의 이름", False)],
                   "10문장의 주어를 떠올려 봐요.",
                   why="10문장의 주어 'each blade of grass'를 받아요. 풀잎 하나하나를 말해요.",
                   highlight=["Each"]),
            choice("s11_do",
                   "'as you yourself do'의 do는 무엇을 받을까요?",
                   [("o0", "이름을 붙이다", False), ("o1", "자기 이름을 가지다", True), ("o2", "풀잎이 되다", False)],
                   "앞에 나온 동사를 다시 쓰지 않으려고 do로 받았어요. 앞의 동사구를 찾아봐요.",
                   why="do는 앞의 'have its own name'을 받아요. 여러분도 저마다 이름이 있잖아요.",
                   highlight=["as you yourself do"]),
            choice("s11_could",
                   "사람이 저마다 이름을 갖듯, 풀잎도 그럴 수 있대요. 실제로 풀잎마다 이름이 있다는 말일까요?",
                   [("o0", "실제로 그렇다", False), ("o1", "그럴 수 있다는 가정이다", True)],
                   "'could'를 봐요. 10문장의 '무한한 기억력'을 떠올려 봐요.",
                   why="'could'는 10문장의 불가능한 가정을 이어받아요. 실제로 그렇다는 게 아니에요.",
                   highlight=["could"]),
            show("s11_end", "'could'는 10문장의 불가능한 가정을 이어받아요. 무한한 기억력이 있다면, 풀잎도 사람처럼 저마다 이름을 가질 수 있을 텐데요.",
                 button="문제 풀러 갈게요",
                 highlight=["could"]),
        ],
    },
]

# 학생이 막힐 만한 단어는 다 누를 수 있게 — 뜻이 없으면 점선 밑줄도 없다
MORE_GLOSSES = {
    1: [("Every time", "~할 때마다"), ("something", "무언가")],
    2: [("flowers", "꽃")],
    3: [("their", "그것들의")],
    4: [("Flower", "꽃"), ("white and yellow", "흰색과 노란색"), ("ones", "것들 · 여기서는 types(종류)를 받아요"), ("many", "많은"), ("other", "다른"), ("to be found", "발견되는")],
    5: [("Lawn", "잔디"), ("grass", "풀"), ("that are there", "거기 있는")],
    6: [("find", "발견하다")],
    7: [("No two daisies", "어떤 데이지 두 송이도 ~않다"), ("no two clovers", "어떤 클로버 두 개도 ~않다"), ("exactly", "정확히"), ("carpet", "카펫, 양탄자"), ("enough", "충분히")],
    8: [("For most", "대부분의 ~에서는"), ("differences", "차이"), ("can be", "~될 수 있다"), ("making", "만들기")],
    9: [("however", "그러나"), ("sports", "스포츠"), ("where", "그곳에서는"), ("grasses", "풀들")],
    10: [("grass", "풀"), ("infinite memory", "무한한 기억력"), ("each", "각각의"), ("life history", "생애, 살아온 이력"), ("its own", "그 자신의")],
    11: [("Each", "각각"), ("could have", "가질 수 있다")],
}
for s_ in sentences:
    have = {x["en"].lower() for x in s_["glosses"]}
    s_["glosses"] += [g(en, ko) for en, ko in MORE_GLOSSES.get(s_["id"], []) if en.lower() not in have]

UNDERLINES = ["①differences", "②acknowledges", "③alike", "④ignored", "⑤co-categorized"]

exam = {
    "question": "다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?",
    "underline": UNDERLINES,
    "sentence": 1,
    "analysis_first": True,
    "glosses": [g("differences", "차이"), g("acknowledges", "인정하다"), g("alike", "비슷한, 같은"), g("ignored", "무시되는"), g("co-categorized", "한 범주로 같이 묶인")],
    "options": [
        {"id": "1", "label": "differences", "keywords": ["differences"], "ko": "차이"},
        {"id": "2", "label": "acknowledges", "keywords": ["acknowledges"], "ko": "인정한다", "correct": True},
        {"id": "3", "label": "alike", "keywords": ["alike"], "ko": "같은"},
        {"id": "4", "label": "ignored", "keywords": ["ignored"], "ko": "무시되는"},
        {"id": "5", "label": "co-categorized", "keywords": ["co-categorized"], "ko": "한 범주로 묶인"},
    ],
    "brief": {
        "ask": "밑줄 단어마다 칠판의 어느 그룹 말인지 떠올려 봐요. 문장 흐름과 안 맞는 걸 골라요.",
        "first_correct": "맞았어요!",
        "first_wrong": "아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.",
        "final_correct": "정답이에요!",
        # 분석 뒤 ②를 맞히면 다시 볼 주기 전에 이 해설을 한 화면 보여 준다
        "answer_explain": "정답이에요! 'Lawn'은 왼쪽, 'the varieties of grass …'는 오른쪽 그룹이에요. 개개의 차이를 따지지 않는 보통 명사가 다양함을 '인정한다(acknowledges)'는 건 맞지 않아요(→ neglects).",
        "final_wrong": "정답은 ②예요. 'Lawn'은 왼쪽, 'the varieties of grass …'는 오른쪽 그룹이에요. 개개의 차이를 따지지 않는 보통 명사가 다양함을 '인정한다(acknowledges)'는 건 맞지 않아요(→ neglects).",
        # ③은 29%가 고른 오답 — 한 줄 해설 대신 같이 자세히 보고, 어디서 헷갈렸는지 기록한다
        "option_review": {
            "3": {
                "intro": "아쉽게도 틀렸어요. ③은 29%나 고른, 많은 학생이 헷갈린 보기예요. 같이 자세히 볼까요?",
                "intro_button": "같이 볼게요",
                "say": "yet은 앞뒤를 반대로 잇는 말이에요. 앞은 '어떤 데이지도 똑같지 않다', 즉 모두 제각각 다르고 고유하다는 뜻이에요. 뒤는 그래도 힐끗 보면 균일한(uniformly) 무늬로 보일 수 있다는 거예요.",
                "panel": {"kind": "contrast", "title": "yet → 앞뒤가 반대", "between": "↔",
                          "left": {"title": "No two daisies … are exactly ③alike", "text": "모두 제각각 다르고 고유하다"},
                          "right": {"title": "a carpet patterned uniformly enough", "text": "힐끗 보면 균일한 무늬로 보인다"}},
            },
            # ④는 38%로 가장 많이 고른 오답 — 9문장 Not so로 반대 관계를 추측하게 한다
            "4": {
                "intro": "아쉽게도 틀렸어요. ④는 38%나 고른, 가장 많이 헷갈린 보기예요. 같이 자세히 볼까요?",
                "intro_button": "같이 볼게요",
                "say": "'Not so'는 앞 문장과 반대라는 신호예요. 9문장이 '풀 하나하나가 정말 중요하다(do matter)'니까, 8문장은 반대로 '개별 차이는 무시될 수 있다'가 맞아요.",
                "panel": {"kind": "contrast", "title": "Not so → 앞뒤가 반대", "between": "↔",
                          "left": {"title": "8 · the differences can be ④ignored", "text": "개별 차이는 무시될 수 있다"},
                          "right": {"title": "9 · the constituent grasses … really do matter", "text": "풀 하나하나가 정말 중요하다"}},
            },
        },
        "option_points": {
            "1": "① differences: 보통 명사(왼쪽)가 차이를 빠뜨린다 → 문맥에 맞음",
            "3": "③ alike: No two … alike = 다 다르다 · yet 앞뒤는 반대 → 문맥에 맞음",
            "4": "④ ignored: Not so로 8·9문장은 반대 → 보통 때는 차이를 무시해도 됨",
            "5": "⑤ co-categorized: 무한한 기억력이면 묶을 필요가 없음 → 문맥에 맞음",
        },
        "option_feedback": {
            "1": "ordinary nouns(보통 명사)는 왼쪽, 즉 하나하나의 특성을 담지 않는 그룹이에요. 그런 이름이 차이(differences)를 빠뜨린다(leave out)는 건 자연스러우니, ①은 문맥에 맞아요.",
            "3": "'No two … are alike'는 똑같은 두 송이가 없다는 말이에요. 하나하나 다르다는 흐름에 맞아요.",
            "4": "보통 때는 차이를 무시해도 된다는 말이에요. 뒤의 'Not so … groundskeeper'가 그 반대 경우예요.",
            "5": "기억력이 무한한 사람은 풀을 굳이 묶지 않아도 하나하나 다 기억할 수 있어요. 그래서 묶일 필요가 없다는 ⑤는 문맥에 맞아요.",
        },
        "ask_first": "실제 시험처럼 풀어 봐요. 풀지 않고 분석 먼저 하고 풀어도 돼요.",
    },
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) + 끊어읽기(slashes)·S·V·O·C(roles)·[ ] 수식어(modifiers) — 2026-10-20 ──
# 핵심어 = S·V·O·C + 이해에 필요한 말, 최소한(덩어리 말고 핵심 단어). 모두 glosses에 뜻이 있는 말로 (exam_kit check)
def _r(text, role):
    return {"text": text, "role": role}

SLASHES = {  # 이 말 뒤에 /
    1: ["put a name on something", "proper name,"],
    4: ["yellow types", "beige ones,", "other sorts"],
    5: ["varieties of grass", "nongrassy plants"],
    6: ["Zoom in,", "will find"],
    7: ["no two clovers,", "alike,", "and yet", "a quick glance"],
    8: ["practical purposes,", "ignored—", "daisy chain,"],
    9: ["Not so,", "however,", "sports stadium,", "stages of growth"],
    10: ["infinite mind,", "infinite memory,", "blade of grass,", "life history,", "co-categorized"],
    11: ["its own name,"],
}
ROLES = {  # 끊어읽기를 켜면 같이 보이는 S·V·O·C (sv 스텝의 roles 글자와 같게)
    1: [_r("you … you", "S"), _r("conceptualize", "V"), _r("categorize", "V"), _r("put", "V"), _r("abstract away from", "V")],
    2: [_r("Picture", "V"), _r("daisies and clover flowers", "O")],
    3: [_r("Those four ordinary nouns", "S"), _r("leave out", "V"), _r("differences", "O")],
    4: [_r("Flower", "S"), _r("co-categorizes", "V"), _r("the white and yellow types", "O")],
    5: [_r("Lawn", "S"), _r("acknowledges", "V"), _r("the varieties of grass", "O")],
    6: [_r("Zoom in", "V"), _r("you", "S"), _r("will find", "V"), _r("individuality and uniqueness", "O")],
    7: [_r("No two daisies", "S"), _r("are", "V"), _r("alike", "C"), _r("they", "S"), _r("present", "V"), _r("a carpet", "O")],
    8: [_r("the differences", "S"), _r("can be", "V"), _r("ignored", "V")],
    9: [_r("the constituent grasses", "S"), _r("really do matter", "V")],
    10: [_r("each blade of grass", "S"), _r("need not be", "V"), _r("co-categorized", "V")],
    11: [_r("Each", "S"), _r("could have", "V"), _r("its own name", "O"), _r("you", "S"), _r("do", "V")],
}
MODIFIERS = {  # [ ]로 묶는 수식어 — 관계사절·분사 덩어리 (안의 S·V는 안 적는다)
    1: ["that is not a proper name"],
    4: ["to be found elsewhere"],
    5: ["that are there"],
    7: ["patterned uniformly enough"],
}
EMPHASIS = {
    # 선생님 기준(2026-10-20, 33번): 지문당 10개 안팎 — 주장이 서는 1~2문장의 S·V·O·C와 연결어만, 나머지 문장은 없음
    1: ["put a name on", "abstract away from", "particularities"],
    3: ["ordinary nouns", "leave out", "differences"],
    6: ["Zoom in", "individuality", "uniqueness"],
}

for _s in sentences:
    for _c in SLASHES.get(_s["id"], []) if "SLASHES" in globals() else []:
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if "SLASHES" in globals() and SLASHES.get(_s["id"]):
        _s["slashes"] = SLASHES[_s["id"]]
    if "ROLES" in globals() and ROLES.get(_s["id"]):
        _s["roles"] = ROLES[_s["id"]]
    if "MODIFIERS" in globals() and MODIFIERS.get(_s["id"]):
        _s["modifiers"] = MODIFIERS[_s["id"]]
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = {
    "id": ID, "kind": "policy", "version": "0.2",
    "source": "2026년 3월 고3 전국연합학력평가 영어 30번 (문맥상 낱말의 쓰임, 2점)",
    "brief": {"topic": "어휘 문제 푸는 법: 요지 → 두 그룹 → 밑줄 단어 맞춰 보기", "closing": "수고 인사"},
    "method": {"type": "word_in_context", "labels": ["요지 잡기", "두 그룹으로 나누기", "밑줄 단어 맞춰 보기"], "intro_times": 3},
    "read_button": "분석하러 갈게요",
    # 문장마다 영어 문장부터 — 질문·보기는 「다 읽었어요」 뒤에
    "read_first": True,
    "images": {"topic": {"src": "/assets/topic-names.svg", "alt": "칠판: Name(이름) → Differences(차이)는 흐려진다", "kind": "drawing"}, "method": {"src": "/assets/vocab-method.svg", "alt": "어휘 문제 푸는 법: ① 요지 잡기 ② 단어를 두 그룹으로 나누기 ③ 밑줄 단어가 맞는 쪽인지 보기", "kind": "drawing"}},
    "intro_board": "method",
    "intro": [
        {"id": "topic", "type": "say", "button": "네", "image": "topic",
         "brief": {"say": "이름을 붙이면 무엇이 사라질까요? 이번 글은 이름 붙이기와 하나하나의 차이를 다뤄요."}},
        {"id": "method1", "type": "say", "button": "네",
         "brief": {"say": "어휘 문제는 단어 뜻만 보면 다 맞아 보여요. 문장마다 흐름을 잡아야 틀린 단어가 보여요."}},
        {"id": "method2", "type": "say", "button": "좋아요",
         "brief": {"say": "요지를 잡고, 단어를 두 그룹으로 나눈 뒤, 밑줄 단어가 맞는 쪽에 있는지 볼 거예요. 칠판 순서대로 해 볼게요."}},
    ],
    "exam": exam,
    "key_words": {
        "passage": [g("conceptualize", "개념화하다"), g("categorize", "범주화하다"), g("abstract away from", "~에서 떼어 내다, 무시하다"),
                    g("particularities", "세부 특징"), g("ordinary noun", "보통 명사"), g("co-categorize", "한 범주로 같이 묶다"),
                    g("individuality", "개별성"), g("uniqueness", "고유성"), g("uniformly", "균일하게"),
                    g("practical", "실용적인"), g("groundskeeper", "경기장 관리인"), g("matter", "중요하다"),
                    g("distinct", "독특한, 뚜렷이 다른"), g("fellow", "동료, 같은 무리"), g("glance", "힐끗 봄")],
        # infinite, blade는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
        "options": [g("difference", "차이"), g("acknowledge", "인정하다"), g("alike", "비슷한, 같은"), g("ignore", "무시하다"), g("neglect", "무시하다, 소홀히 하다")],
    },
    "context": {"mode": "paper_review", "exam_relevance": "high", "time_budget": "normal"},
    "item": {"english_difficulty": "high", "conceptual_difficulty": "high", "background_knowledge_required": "low",
             "exam_importance": "high", "teaching_value": "high", "intervention_density": "normal"},
    "sentences": sentences,
    "passage_on_try": True,
}

# 초급 기본 — 문장마다 「주어·동사 + 뜻」 또는 「해석 맞추기」 하나 (2026-10-15 선생님).
# 밑줄 낱말(②acknowledges 등)의 맞고 틀림을 드러내지 않게 — 맞추기 칸에 밑줄 낱말 뜻을 넣지 않는 곳도 있다
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beginner import add_basic, fill_chunk_glosses, m, sv_step  # noqa: E402

add_basic(sentences, 1, [m("Every time", "~할 때마다"), " 무언가에 ", m("put a name on", "이름을 붙일"), " 때마다, 우리는 ",
                         m("its particularities", "그것의 특징들"), "을 ", m("abstract away from", "떼어 내 빼 버린다"), "."],
          match_display="Every time you put a name on something, you abstract away from its particularities.",
          sv_new=sv_step("s1_basic_sv", ["Every time", "something", "abstract away from", "its particularities"],
                         {"abstract away from": "V", "its particularities": "전목"},
                         {"Every time": "그건 '~할 때마다' 덩어리를 여는 말이에요.", "something": "그건 put a name on의 대상이에요."},
                         "콤마 뒤 문장은 주어 you, 동사 abstract away from(떼어 내다), from 뒤 목적어 its particularities예요.",
                         ask="콤마 뒤 문장의 주어는 you예요. 그 동사(V)와 from 뒤의 목적어(전목)를 찾아볼까요?"))
add_basic(sentences, 2, [m("in a lawn", "잔디밭에 있는"), " ", m("daisies and clover flowers", "데이지와 클로버 꽃"), "을 ", m("Picture", "상상해 봐요"), "."],
          sv_new=sv_step("s2_basic_sv", ["Picture", "daisies and clover flowers", "in a lawn"],
                         {"Picture": "V", "daisies and clover flowers": "O"},
                         {"in a lawn": "그건 '어디에' 있는지 알려 주는 말이에요."},
                         "명령문이라 주어가 없어요. 동사는 Picture(상상해 보다), 목적어는 daisies and clover flowers예요.",
                         ask="이 문장은 주어 없이 시작해요. 동사(V)와 목적어(O)를 찾아볼까요?"),
          meaning_ids=["s2_picture"])
add_basic(sentences, 3, [m("Those four ordinary nouns", "그 네 개의 보통 명사는"), " 그것들의 ", m("differences", "차이"), "를 ",
                         m("leave out", "빠뜨린다"), "."],
          sv_new=sv_step("s3_basic_sv", ["Those four ordinary nouns", "leave out", "differences"],
                         {"Those four ordinary nouns": "S", "leave out": "V", "differences": "O"}, {},
                         "주어는 Those four ordinary nouns, 동사는 leave out(빠뜨리다), 목적어는 differences예요."))
add_basic(sentences, 4, [m("Flower", "'꽃'이라는 말은"), " ", m("the white and yellow types", "흰색과 노란색 종류"), "를 ",
                         m("the beige ones", "베이지색 종류"), "와 ", m("co-categorizes", "한 범주로 묶는다"), "."],
          match_display="“Flower” co-categorizes the white and yellow types with the beige ones.",
          sv_new=sv_step("s4_basic_sv", ["Flower", "co-categorizes", "the white and yellow types"],
                         {"Flower": "S", "co-categorizes": "V", "the white and yellow types": "O"}, {},
                         "주어는 “Flower”라는 말, 동사는 co-categorizes(한 범주로 묶다), 목적어는 the white and yellow types예요."))
add_basic(sentences, 5, [m("Lawn", "'잔디'라는 말에는"), " ", m("the varieties of grass", "여러 종류의 풀"), "과 ", m("that are there", "거기 있는"), " ",
                         m("nongrassy plants", "풀이 아닌 식물들"), "까지 다 들어가요."],
          sv_new=sv_step("s5_basic_sv", ["Lawn", "acknowledges", "the varieties of grass"],
                         {"Lawn": "S", "acknowledges": "V", "the varieties of grass": "O"}, {},
                         "주어는 “Lawn”이라는 말, 동사는 밑줄 친 ②, 목적어는 the varieties of grass예요."))
add_basic(sentences, 6, [m("Zoom in", "가까이 들여다봐요"), ", 그러면 ", m("everywhere", "어디에서나"), " ", m("individuality and uniqueness", "개별성과 고유성"),
                         "을 ", m("will find", "발견할 거예요"), "."],
          sv_new=sv_step("s6_basic_sv", ["Zoom in", "you", "will find", "individuality and uniqueness"],
                         {"you": "S", "will find": "V", "individuality and uniqueness": "O"},
                         {"Zoom in": "그건 and 앞, 주어 없이 시작하는 명령이에요. and 뒤에서 찾아봐요."},
                         "and 뒤는 주어 you, 동사 will find, 목적어 individuality and uniqueness예요."))
add_basic(sentences, 7, [m("No two daisies", "어떤 두 데이지도"), " ", m("exactly", "똑같이"), " ", m("alike", "같지"), " 않아요. ",
                         m("and yet", "그런데도"), " ", m("to a quick glance", "얼핏 보면"), " ", m("a carpet", "카펫"), "처럼 ",
                         m("uniformly", "균일하게"), " 보여요."],
          match_display="No two daisies are exactly alike, and yet they present to a quick glance a carpet patterned uniformly enough.",
          sv_new=sv_step("s7_basic_sv", ["No two daisies", "are", "alike", "they", "present"],
                         {"No two daisies": "S", "are": "V", "alike": "C", "they": "S", "present": "V"}, {},
                         "and yet 앞은 주어 No two daisies, 동사 are, 보어 alike예요. 뒤는 주어 they, 동사 present예요."),
          meaning_ids=["s7_q"])
add_basic(sentences, 8, [m("For most", "대부분의"), " ", m("practical purposes", "실용적인 목적"), "에서는 ", m("the differences", "차이"), "가 ",
                         m("ignored", "무시될"), " ", m("can be", "수 있다"), "."],
          sv_new=sv_step("s8_basic_sv", ["the differences", "can be", "ignored", "practical purposes"],
                         {"the differences": "S", "can be": "V", "ignored": "V"},
                         {"practical purposes": "그건 For most 뒤, '어떤 목적에서' 인지 알려 주는 말이에요."},
                         "주어는 the differences, 동사는 can be ④ignored(무시될 수 있다)예요."))
add_basic(sentences, 9, [m("Not so", "그렇지 않다"), " — ", m("groundskeeper", "경기장 관리인"), "에게는 ", m("the constituent grasses", "풀의 종류"),
                         "와 ", m("stages of growth", "자라는 단계"), "가 ", m("really do matter", "정말 중요하다"), "."],
          sv_new=sv_step("s9_basic_sv", ["Not so", "groundskeeper", "the constituent grasses", "really do matter"],
                         {"the constituent grasses": "S", "really do matter": "V"},
                         {"Not so": "그건 '그렇지 않다'는 짧은 말이에요. where 뒤에서 찾아봐요.", "groundskeeper": "그건 for 뒤, 누구에게인지 알려 주는 말이에요."},
                         "where 뒤 주어는 the constituent grasses (and their stages of growth), 동사는 really do matter(정말 중요하다)예요.",
                         ask="where 뒤에서 주어(S)와 동사(V)를 찾아볼까요?"))
add_basic(sentences, 10, [m("to an infinite mind", "무한한 정신에게는"), " ", m("each blade of grass", "풀잎 하나하나가"), " ",
                          m("all its fellows", "모든 동료(다른 풀잎)"), "와 ", m("co-categorized", "한 범주로 묶일"), " ", m("need not be", "필요가 없다"), "."],
          match_display="And to an infinite mind, each blade of grass need not be co-categorized with all its fellows.",
          sv_new=sv_step("s10_basic_sv", ["an infinite mind", "each blade of grass", "need not be", "co-categorized"],
                         {"each blade of grass": "S", "need not be": "V", "co-categorized": "V"},
                         {"an infinite mind": "그건 to 뒤, '누구에게'인지 알려 주는 말이에요."},
                         "주어는 each blade of grass, 동사는 need not be ⑤co-categorized(묶일 필요가 없다)예요."),
          meaning_ids=["s10_q"])
add_basic(sentences, 11, [m("Each", "각각(풀잎)은"), " ", m("as you yourself do", "당신이 그렇듯"), " ", m("its own name", "자기만의 이름"), "을 ",
                          m("could have", "가질 수 있다"), "."],
          sv_new=sv_step("s11_basic_sv", ["Each", "could have", "its own name"],
                         {"Each": "S", "could have": "V", "its own name": "O"}, {},
                         "주어는 Each(각각), 동사는 could have(가질 수 있다), 목적어는 its own name이에요."))
fill_chunk_glosses(sentences, {
    "Every time": "~할 때마다", "something": "무언가", "abstract away from": "~에서 떼어 내다", "its particularities": "그것의 특징들",
    "put a name on": "~에 이름을 붙이다", "Picture": "상상해 보다", "daisies and clover flowers": "데이지와 클로버 꽃", "in a lawn": "잔디밭에",
    "Those four ordinary nouns": "그 네 개의 보통 명사", "leave out": "빠뜨리다", "differences": "차이",
    "Flower": "꽃", "co-categorizes": "한 범주로 묶다", "the white and yellow types": "흰색과 노란색 종류", "the beige ones": "베이지색 종류",
    "Lawn": "잔디", "acknowledges": "인정하다", "the varieties of grass": "여러 종류의 풀", "that are there": "거기 있는",
    "nongrassy plants": "풀이 아닌 식물들", "Zoom in": "가까이 들여다보다", "you": "너, 사람", "will find": "발견할 것이다",
    "individuality and uniqueness": "개별성과 고유성", "everywhere": "어디에서나", "No two daisies": "어떤 두 데이지도 ~ 않다",
    "are": "~이다", "alike": "같은", "they": "그것들", "present": "보여 주다", "and yet": "그런데도", "to a quick glance": "얼핏 보면",
    "a carpet": "카펫", "uniformly": "균일하게", "exactly": "정확히", "the differences": "그 차이", "can be": "~될 수 있다",
    "ignored": "무시된", "practical purposes": "실용적인 목적", "For most": "대부분의", "Not so": "그렇지 않다", "groundskeeper": "경기장 관리인",
    "the constituent grasses": "구성하는 풀들", "really do matter": "정말 중요하다", "stages of growth": "자라는 단계",
    "an infinite mind": "무한한 정신", "to an infinite mind": "무한한 정신에게는", "each blade of grass": "풀잎 하나하나",
    "need not be": "~일 필요가 없다", "co-categorized": "한 범주로 묶인", "all its fellows": "모든 동료들",
    "Each": "각각", "could have": "가질 수 있다", "its own name": "자기만의 이름", "as you yourself do": "당신이 그렇듯",
})

# 칠판 정리 — 2~3문장마다 지금까지 상황을 칠판에 (공통 틀)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# ── 해석 맞추기(모두에게)·가리키는 말 — 2026-10-20 엔진: S·V 찾기·핵심어 자유 해석은 빠지고 맞추기가 대신 나온다 ──
from beginner import add_match, add_refers, m as _m  # noqa: E402
add_refers(sentences, 1, {"its particularities": "its = something you named(이름 붙인 그 대상의)"})
add_refers(sentences, 3, {"their": "the daisies, clovers, flowers and lawn(데이지·클로버·꽃·잔디)"})
add_refers(sentences, 4, {"the beige ones": "ones = types of flowers(꽃의 종류)"})
add_refers(sentences, 7, {"they": "daisies and clovers(데이지와 클로버)"})
add_refers(sentences, 9, {"Not so": "the differences cannot be ignored(차이를 무시할 수 없다 — 앞 문장의 반대)"})
add_refers(sentences, 10, {"its": "each blade of grass(각 풀잎)"})

from story_boards import add_story_boards  # noqa: E402
add_story_boards(ID, lesson["sentences"])

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# proper name 고유 명사 (proper = 고유한) · Picture 떠올려 보다, 상상하다.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    1: [{"label": "proper name", "text": "이 글에서는 → 고유 명사 (proper = 고유한)  ('적절한' 아님)", "mark": "proper name", "trap": True}],
    2: [{"label": "Picture", "text": "이 글에서는 → 떠올려 보다, 상상하다  ('그림' 아님)", "mark": "Picture", "trap": True}],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

json.dump(lesson, open(f"{ROOT}/content/tutor/policy-lessons/{ID}.json", "w"), ensure_ascii=False, indent=2)

# 대사 — brief가 이미 해요체라 그대로 옮기고 도장만 찍는다
ref = json.load(open(f"{ROOT}/content/tutor/policy-copy/dajung/moeui-2026-03-21-music-researchers.json"))
steps = {st["id"]: copy.deepcopy(st["brief"]) for s in sentences for st in s["steps"]}
c = {
    "lesson": ID, "character": "dajung", "note": "생성물",
    "topic_intro": "어휘 문제 푸는 법",
    "closing": ref["closing"],
    "helps": {h["id"]: {"answer": h["brief"]} for s_ in sentences for h in s_.get("helps", [])},
    "steps": steps,
    "exam": {k: v for k, v in exam["brief"].items()},
    "intro": {i["id"]: dict(i["brief"]) for i in lesson["intro"]},
    # 정답 해설이 이미 「정답이에요!」로 시작하니, 다시 볼 주기 말에서는 빼 둔다
    "ending": {**ref["ending"], "wrong": "이번엔 한 번 헷갈렸으니 {weeks} 뒤에 다시 한번 볼 거예요."},
}
json.dump(c, open(f"{ROOT}/content/tutor/policy-copy/dajung/{ID}.json", "w"), ensure_ascii=False, indent=2)
print("ok", ID)
