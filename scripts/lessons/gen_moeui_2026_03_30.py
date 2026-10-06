"""2026년 3월 30번 레슨 + 대사를 만든다.

레슨 JSON(content/tutor/policy-lessons/…)과 대사(content/tutor/policy-copy/dajung/…)는 이 스크립트의
생성물이다. 고칠 때는 여기를 고치고 다시 돌린 뒤 도장을 찍는다:

    python3 scripts/lessons/gen_moeui_2026_03_30.py
    npm run policy:copy stamp moeui-2026-03-30-names-and-differences

1~11문장 모두 선생님과 화면을 보며 정했다.
"""
import copy
import json
import os

ID = "moeui-2026-03-30-names-and-differences"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

LEFT = "이름 붙이기 · 같게 묶음"
RIGHT = "하나하나 다름"
CLUSTER = {"words": ["conceptualize", "categorize", "put a name on"]}


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
    """why: 틀렸을 때 「아쉽게도 틀렸어요.」 뒤의 이유 (없으면 힌트)"""
    feedback = {o[0]: why or hint for o in options if not o[2]}
    return {
        "id": id, "type": "choice", "interaction": "meaning_choice", "one_try": True,
        "brief": {"ask": ask, "reask": "그럼 하나 골라 봐요.", "hints": [hint, hint], "explain": hint, "praise": praise, "feedback": feedback},
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
R = ["particularities"]

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
        "emphasis": ["conceptualize", "categorize", "put a name on", "abstract away from", "particularities"],
        "steps": [
            show("s1_group",
                 "conceptualize, categorize, put a name on은 여기서 모두 '이름 붙여 묶는다'는 같은 뜻이에요. 셋 중 하나만 이해해도 충분해요.",
                 method=0, button="다음",
                 panel={"kind": "groups", "title": "단어 지도",
                        "left": {"label": LEFT, "cluster": {**CLUSTER, "fresh": True}, "words": []}},
                 highlight=["conceptualize", "categorize", "put a name on"],
                 faded=["that is not a proper name"]),
            choice("s1_q",
                   "이름을 붙이면 'abstract away from its particularities' 한대요. particularities는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", "오른쪽 · 반대쪽", True)],
                   "'abstract away from'은 '~에서 떼어 내다'예요. 이름을 붙이면 particularities와 멀어진다는 말이에요.",
                   why="'abstract away from'은 '~에서 떼어 내다'예요. 이름을 붙이면 particularities는 떨어져 나가니, 같은 그룹이 아니에요.",
                   method=0,
                   panel={**board([], [], right_label="반대쪽"), "sort": {"words": ["particularities"], "left": SORT_LEFT, "right": "오른쪽 · 반대쪽"}},
                   highlight=["abstract away from its particularities"],
                   faded=["that is not a proper name"]),
            show("s1_map",
                 "이름을 붙여 묶으면 하나하나의 특징은 무시된다, 이게 이 글의 요지예요. 오른쪽에서 왼쪽으로 가는 화살표, 이 과정이 'abstract away'예요.",
                 panel=board(["abstract away*"], ["particularities*"], "하나하나의 특징 → 이름으로 묶이며 무시"),
                 faded=["that is not a proper name"]),
        ],
    },
    {
        "id": 2, "text": "Picture daisies and clover flowers in a lawn.",
        "model_translation": "잔디에 있는 데이지와 클로버 꽃을 떠올려 보라.",
        "teaching_value": "medium",
        "glosses": [g("Picture", "상상해 보다 · 여기서는 '그림'이 아니라 동사예요"), g("daisies", "데이지 꽃"), g("clover", "클로버"), g("lawn", "잔디밭")],
        "emphasis": ["Picture"],
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
        "emphasis": ["ordinary nouns", "leave out"],
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
                 panel=board(L + ["four ordinary nouns", "leave out"], R + ["differences"], "① differences → 요지와 맞아요 ✓"),
                 highlight=["①differences"]),
        ],
    },
    {
        "id": 4, "text": "“Flower” co-categorizes the white and yellow types with the beige ones, and all the many other sorts to be found elsewhere.",
        "model_translation": "'꽃'이라는 말은 흰색과 노란색 종류를 베이지색 종류, 그리고 다른 곳의 수많은 종류와 함께 하나의 범주로 묶는다.",
        "teaching_value": "low",
        "glosses": [g("co-categorizes", "한 범주로 같이 묶다"), g("types", "종류"), g("beige", "베이지색"), g("sorts", "종류"), g("elsewhere", "다른 곳에서")],
        "emphasis": ["co-categorizes"],
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
        "emphasis": ["Lawn"],
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
        "emphasis": ["Zoom in", "individuality", "uniqueness"],
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
        "emphasis": ["and yet", "uniformly"],
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
        "emphasis": ["practical purposes"],
        "steps": [
            choice("s8_sort",
                   "'For most practical purposes(대부분의 실용적인 목적에서는)' 차이를 무시해도 된대요. practical purposes는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, True), ("o1", SORT_RIGHT, False)],
                   "대시(—) 뒤 예시를 봐요. 꽃목걸이를 만들거나 일광욕할 때 풀 종류를 따지나요?",
                   why="꽃목걸이나 일광욕 같은 보통 목적에서는 차이를 무시해요. 그래서 이름으로 묶는 쪽이에요.",
                   panel={**S8_BEFORE, "sort": {"words": ["practical purposes"], "left": SORT_LEFT, "right": SORT_RIGHT}},
                   faded=["—making a daisy chain, sunbathing, and the like"]),
            show("s8_map", "보통 때는 풀과 꽃의 차이를 무시해도 돼요.",
                 panel=S8_AFTER),
        ],
    },
    {
        "id": 9, "text": "Not so, however, for the groundskeeper of a sports stadium, where the constituent grasses and their stages of growth really do matter.",
        "model_translation": "그러나 스포츠 경기장 관리인에게는 그렇지 않은데, 그곳에서는 잔디를 이루는 풀들과 그 성장 단계가 정말 중요하다.",
        "teaching_value": "medium",
        "glosses": [g("Not so", "그렇지 않다 · 앞 문장의 '무시해도 된다'를 뒤집어요"), g("groundskeeper", "경기장 관리인"), g("stadium", "경기장"), g("constituent", "구성하는"), g("stages of growth", "성장 단계"), g("really do matter", "정말 중요하다")],
        "emphasis": ["Not so", "groundskeeper", "really do matter"],
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
        "emphasis": ["infinite mind", "need not be"],
        "helps": [{"id": "s10_subject", "label": "주어 찾기 헷갈려요",
                   "brief": "'to'처럼 전치사로 시작하는 덩어리는 보통 주어가 아니에요. 'with'로 시작하는 두 덩어리도 마찬가지예요. 그걸 빼면 주어는 'each blade of grass(각각의 풀잎)'예요."}],
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
                   highlight=["its own distinct life history"],
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
                   highlight=["⑤co-categorized with all its fellows"],
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
        "emphasis": ["its own name"],
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
                "ask": "그래서 ③alike는 문맥에 맞아요. 어디서 헷갈렸어요?",
                "choices": [
                    {"label": "No를 못 봤어요", "skills": ["no_negation"],
                     "reply": "알려 줘서 고마워요. 'No two … alike'처럼 No가 앞에 붙으면 뜻이 뒤집혀요. 앞으로 비슷한 문장이 나오면 No를 강조해서 알려 줄게요."},
                    {"label": "yet 앞뒤가 반대인 게 헷갈렸어요", "skills": ["yet_contrast"],
                     "reply": "알려 줘서 고마워요. yet 앞뒤는 반대 관계예요. 앞으로 비슷한 문장이 나오면 yet을 강조해서 알려 줄게요."},
                    {"label": "둘 다요", "skills": ["no_negation", "yet_contrast"],
                     "reply": "알려 줘서 고마워요. 앞으로 비슷한 문장이 나오면 No와 yet을 강조해서 알려 줄게요."},
                ],
            },
            # ④는 38%로 가장 많이 고른 오답 — 9문장 Not so로 반대 관계를 추측하게 한다
            "4": {
                "intro": "아쉽게도 틀렸어요. ④는 38%나 고른, 가장 많이 헷갈린 보기예요. 같이 자세히 볼까요?",
                "intro_button": "같이 볼게요",
                "say": "'Not so'는 앞 문장과 반대라는 신호예요. 9문장이 '풀 하나하나가 정말 중요하다(do matter)'니까, 8문장은 반대로 '개별 차이는 무시될 수 있다'가 맞아요.",
                "panel": {"kind": "contrast", "title": "Not so → 앞뒤가 반대", "between": "↔",
                          "left": {"title": "8 · the differences can be ④ignored", "text": "개별 차이는 무시될 수 있다"},
                          "right": {"title": "9 · the constituent grasses … really do matter", "text": "풀 하나하나가 정말 중요하다"}},
                "ask": "그래서 ④ignored는 문맥에 맞아요. 어디서 헷갈렸어요?",
                "choices": [
                    {"label": "ignored가 부정적인 말이라 틀려 보였어요", "skills": ["word_feeling"],
                     "reply": "알려 줘서 고마워요. 단어 느낌이 아니라 앞뒤 문장과의 관계로 판단해야 해요. 앞으로 비슷한 문제가 나오면 이 점을 강조해서 알려 줄게요."},
                    {"label": "Not so가 반대라는 걸 못 봤어요", "skills": ["not_so_contrast"],
                     "reply": "알려 줘서 고마워요. 'Not so'는 앞 문장과 반대라는 신호예요. 앞으로 비슷한 문장이 나오면 Not so를 강조해서 알려 줄게요."},
                    {"label": "둘 다요", "skills": ["word_feeling", "not_so_contrast"],
                     "reply": "알려 줘서 고마워요. 앞으로 비슷한 문제가 나오면 단어 느낌보다 앞뒤 관계를, 특히 Not so를 강조해서 알려 줄게요."},
                ],
            },
        },
        "option_feedback": {
            "1": "ordinary nouns(보통 명사)는 왼쪽, 즉 하나하나의 특성을 담지 않는 그룹이에요. 그런 이름이 차이(differences)를 빠뜨린다(leave out)는 건 자연스러우니, ①은 문맥에 맞아요.",
            "3": "'No two … are alike'는 똑같은 두 송이가 없다는 말이에요. 하나하나 다르다는 흐름에 맞아요.",
            "4": "보통 때는 차이를 무시해도 된다는 말이에요. 뒤의 'Not so … groundskeeper'가 그 반대 경우예요.",
            "5": "기억력이 무한한 사람은 풀을 굳이 묶지 않아도 하나하나 다 기억할 수 있어요. 그래서 묶일 필요가 없다는 ⑤는 문맥에 맞아요.",
        },
        "ask_first": "실제 시험처럼 풀어 봐요. 지문이 다시 보고 싶으면 아래 버튼을 눌러요.",
    },
}

lesson = {
    "id": ID, "kind": "policy", "version": "0.2",
    "source": "2026년 3월 고3 전국연합학력평가 영어 30번 (문맥상 낱말의 쓰임, 2점)",
    "brief": {"topic": "어휘 문제 푸는 법: 요지 → 두 그룹 → 밑줄 단어 맞춰 보기", "closing": "수고 인사"},
    "method": {"type": "word_in_context", "labels": ["요지 잡기", "두 그룹으로 나누기", "밑줄 단어 맞춰 보기"], "intro_times": 3},
    "read_button": "분석하러 갈게요",
    "images": {"method": {"src": "/assets/vocab-method.svg", "alt": "어휘 문제 푸는 법: ① 요지 잡기 ② 단어를 두 그룹으로 나누기 ③ 밑줄 단어가 맞는 쪽인지 보기", "kind": "drawing"}},
    "intro_board": "method",
    "intro": [
        {"id": "method1", "type": "say", "show_when": "first", "button": "네",
         "brief": {"say": "어휘 문제는 단어 뜻만 보면 다 맞아 보여요. 문장마다 흐름을 잡아야 틀린 단어가 보여요."}},
        {"id": "method2", "type": "say", "show_when": "first", "button": "좋아요",
         "brief": {"say": "요지를 잡고, 단어를 두 그룹으로 나눈 뒤, 밑줄 단어가 맞는 쪽에 있는지 볼 거예요. 칠판 순서대로 해 볼게요."}},
        {"id": "method_short", "type": "say", "show_when": "later", "button": "시작할게요",
         "brief": {"say": "칠판 순서대로 바로 시작해 볼게요."}},
    ],
    "exam": exam,
    "key_words": {
        "passage": [g("conceptualize", "개념화하다"), g("categorize", "범주화하다"), g("abstract away from", "~에서 떼어 내다, 무시하다"),
                    g("particularities", "세부 특징"), g("ordinary noun", "보통 명사"), g("co-categorize", "한 범주로 같이 묶다"),
                    g("individuality", "개별성"), g("uniqueness", "고유성"), g("uniformly", "균일하게"),
                    g("practical", "실용적인"), g("groundskeeper", "경기장 관리인"), g("matter", "중요하다"),
                    g("infinite", "무한한"), g("distinct", "독특한, 뚜렷이 다른"),
                    g("blade", "(풀의) 잎 · 원래는 칼날"), g("fellow", "동료, 같은 무리"), g("glance", "힐끗 봄")],
        "options": [g("difference", "차이"), g("acknowledge", "인정하다"), g("alike", "비슷한, 같은"), g("ignore", "무시하다"), g("neglect", "무시하다, 소홀히 하다")],
    },
    "context": {"mode": "paper_review", "exam_relevance": "high", "time_budget": "normal"},
    "item": {"english_difficulty": "high", "conceptual_difficulty": "high", "background_knowledge_required": "low",
             "exam_importance": "high", "teaching_value": "high", "intervention_density": "normal"},
    "sentences": sentences,
    "passage_on_try": True,
}

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
