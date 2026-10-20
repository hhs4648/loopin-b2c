"""2022년 3월 고3 42번 레슨 + 대사를 만든다 (41~42 장문 중 42번 — 문맥상 낱말의 쓰임). 오답률 34.0% · Top 13.

    py scripts/lessons/gen_moeui_2022_03_42.py   (→ node scripts/policy_copy.mjs stamp <id> → npm run build)

틀: 어휘(2024년 3월 42번·30번과 같다) — 요지 → 두 쪽(식물이 하는 일 vs 행동이라 부르기 꺼리는 쪽) → 밑줄 하나씩 점검.
정답 ④ (d) absence (→ presence). 해설지: 행동 능력 부재(→ 존재)를 일축해서는 안 된다.
많이 고른 오답 ③ (c) reluctant 18% — 글쓴이 생각으로 읽어서. Some(몇몇 사람들)의 반대 의견이고 바로 뒤 But에서 글쓴이가 반박한다.
열쇠: 글쓴이는 「식물은 행동한다」 쪽 → 신경이 없다는 이유만으로 행동 능력의 '존재'를 무시하면 안 된다.
41번(제목)은 이 레슨에서 다루지 않는다. 지문 아래 * 풀이 단어 없음.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2022-03-42-plant-behavior"

S = [
    "In What a Plant Knows, the biologist Daniel Chamovitz describes sophisticated information-processing capacities that plants use "
    "to control their movements in response to stimulation.",
    "Plants not only “follow the sun” by bending their stems, they also align their leaves in such a way as to (a)maximize exposure "
    "to light and thereby promote growth.",
    "Some plants actually anticipate sunrise from “memory,” and even when deprived of solar signals retain this information for several days.",
    "In Brilliant Green, Stefano Mancuso and Alessandra Viola argue that plants possess not only the senses of sight, touch, smell, and "
    "hearing, but more than a dozen other (b)sensory capacities that humans lack.",
    "For example, the roots of plants sense the mineral and water content of the soil and alter their direction of growth accordingly.",
    "Some are (c)reluctant to label plant movements as behaviors, since they lack nerves and muscles.",
    "But just as they are able to breathe without lungs and digest nutrients without a stomach, plants have the ability to move (behave).",
    "We should not dismiss the (d)absence of behavioral capacities in an organism simply because it lacks the physiological mechanism "
    "that is responsible for the behavior in animals.",
    "Plants clearly sense the environment, learn, store information, and use that information to guide movements; they behave.",
    "One might say that there is certain “intelligence” to their behavior.",
    "This is true as long as intelligence is defined in terms of the ability to solve problems through behavioral (e)interactions with "
    "the environment, rather than with respect to mental capacity.",
]
KO = [
    "『What a Plant Knows』에서 생물학자 Daniel Chamovitz는 식물이 자극에 반응하여 자신의 움직임을 조절하기 위해 사용하는 정교한 정보 처리 능력을 설명한다.",
    "식물은 자신의 줄기를 구부려 '태양을 따라갈' 뿐만 아니라, 빛에 최대한 노출되기 위한 방식으로 잎을 정렬하기도 하는데, 그렇게 함으로써 성장을 촉진한다.",
    "몇몇 식물은 실제로 '기억'으로 일출을 예상하며, 심지어 태양의 신호를 받지 못할 때도 며칠 동안 이 정보를 보유한다.",
    "『Brilliant Green』에서 Stefano Mancuso와 Alessandra Viola는 식물이 시각, 촉각, 후각, 그리고 청각뿐만 아니라 인간에게 없는 십여 개가 넘는 다른 감각 능력을 갖추고 있다고 주장한다.",
    "예를 들어, 식물의 뿌리는 토양의 미네랄과 수분 함량을 감지하고 그것에 맞게 자신의 성장 방향을 바꾼다.",
    "몇몇 사람은 식물에 신경과 근육이 없어서 식물의 움직임을 행동이라고 부르기를 꺼린다.",
    "하지만 식물이 폐 없이 숨을 쉴 수 있고 위 없이 영양분을 소화할 수 있는 것처럼, 식물은 움직일(행동할) 수 있는 능력도 지니고 있다.",
    "단지 어떤 유기체가 동물에게서 행동의 원인이 되는 생리학적 메커니즘이 없다는 이유로, 그 유기체의 행동 능력 존재를 일축해서는 안 된다.",
    "식물은 분명히 환경을 감지하고, 배우고, 정보를 저장하며, 움직임을 안내하기 위해 그 정보를 사용한다. 즉, 식물은 행동한다.",
    "어떤 사람은 식물의 행동에 어느 정도의 '지능'이 있다고 말할지도 모른다.",
    "지능이 정신적 능력보다 환경과의 행동적 상호 작용을 통한 문제 해결 능력이라는 측면에서 정의된다면, 이것은 사실이다.",
]
UNDER = ["(a)maximize", "(b)sensory", "(c)reluctant", "(d)absence", "(e)interactions"]

DO = "식물이 하는 일"
SOME = "Some · 행동이라 부르기 꺼림"


def board(left, right=None, fresh=()):
    """6문장 전에는 왼쪽만 (반대 의견은 6문장에서 처음 나온다)"""
    if right is None:
        return groups("식물이 하는 일", DO, left, fresh=fresh)
    return groups("식물의 움직임 = 행동?", DO, left, SOME, right, fresh=fresh, between="vs")


def check(*done):
    """밑줄 점검표 — 문맥에 맞는다고 확인한 밑줄만 (정답 밑줄 (d)는 쓰지 않는다)"""
    names = {"a": ("(a) 맞음", "maximize exposure to light → promote growth", "빛을 최대한 받아 성장을 돕는다"),
             "b": ("(b) 맞음", "a dozen other sensory capacities", "인간에게 없는 감각 능력이 열 개 넘게"),
             "c": ("(c) 맞음", "Some are reluctant … since they lack nerves", "신경이 없어서 행동이라 부르기 꺼린다 (Some의 생각)"),
             "e": ("(e) 맞음", "behavioral interactions with the environment", "환경과 행동으로 주고받으며 문제를 푼다")}
    return rows(*[(names[d][0], names[d][1], names[d][2], "hl") for d in done])


L1 = [("control their movements", "움직임을 조절")]
L2 = L1 + [("follow the sun", "해를 따라감")]
L3 = L2 + [("anticipate sunrise", "해 뜨는 걸 예상")]
L4 = L3 + [("sensory capacities", "감각 능력")]
L5 = L4 + [("alter their direction", "방향을 바꿈")]
R6 = [("lack nerves and muscles", "신경·근육 없음")]
L7 = L5 + [("ability to move", "움직이는 능력")]
L9 = L7 + [("they behave", "행동한다")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("In What a Plant Knows", "『식물은 무엇을 아는가』에서"), g("the biologist Daniel Chamovitz", "생물학자 Daniel Chamovitz는"),
                    g("describes", "설명한다"), g("sophisticated information-processing capacities", "정교한 정보 처리 능력"),
                    g("plants", "식물"), g("use", "사용하다"), g("to control their movements", "자기 움직임을 조절하려고"),
                    g("in response to stimulation", "자극에 반응해")],
        "slashes": ["In What a Plant Knows,", "Daniel Chamovitz", "describes", "information-processing capacities", "their movements"],
        "roles": [r("the biologist Daniel Chamovitz", "S"), r("describes", "V"), r("sophisticated information-processing capacities", "O")],
        "modifiers": ["that plants use to control their movements in response to stimulation"],
        "steps": [
            sv("s1_sv", ["the biologist Daniel Chamovitz", "describes", "sophisticated information-processing capacities", "plants", "use"],
               {"the biologist Daniel Chamovitz": "S", "describes": "V", "sophisticated information-processing capacities": "O"},
               {"plants": "그건 that 뒤 덩어리 안의 주어예요.", "use": "그건 that 뒤 덩어리 안의 동사예요."},
               "주어는 the biologist Daniel Chamovitz, 동사는 describes, 목적어는 sophisticated information-processing capacities예요."),
            choice("s1_use",
                   "식물은 그 정보 처리 능력을 어디에 쓴대요?",
                   [("o0", "자극에 반응해 움직임을 조절하는 데", True), ("o1", "열매를 더 크게 키우는 데", False),
                    ("o2", "다른 식물과 대화하는 데", False)],
                   "use 뒤 'to control their movements in response to stimulation'을 봐요.",
                   why="'to control their movements in response to stimulation', 자극에 반응해 자기 움직임을 조절하는 데 쓴대요.",
                   highlight=["control their movements", "in response to stimulation"],
                   tips=[tip("in response to", "'~에 반응하여'예요.", "in response to")],
                   point="요지 시작: 식물은 정보를 처리해 자기 움직임을 조절한다"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Plants", "식물은"), g("not only", "~뿐만 아니라"), g("follow the sun", "해를 따라가다"),
                    g("by bending their stems", "줄기를 구부려서"), g("they also align", "또한 정렬한다"), g("their leaves", "자기 잎을"),
                    g("in such a way as to", "~하는 방식으로"), g("maximize", "최대로 하다"), g("exposure to light", "빛에 노출됨"),
                    g("and thereby promote growth", "그렇게 함으로써 성장을 촉진하다"), g("they", "그것들(식물)은"), g("align", "정렬하다")],
        "slashes": ["“follow the sun”", "their stems,", "their leaves", "exposure to light"],
        "roles": [r("Plants", "S"), r("follow", "V"), r("they", "S"), r("align", "V"), r("their leaves", "O")],
        "steps": [
            sv("s2_sv", ["Plants", "follow", "their stems", "they", "align"],
               {"Plants": "S", "follow": "V", "they": "S", "align": "V"},
               {"their stems": "그건 by bending 뒤 덩어리예요."},
               "앞은 Plants가 follow하고, 콤마(,) 뒤는 they가 align해요. not only ~, also ~로 둘을 이었어요.",
               ask="not only ~, also ~로 두 문장이 이어져요. 주어(S)와 동사(V)를 모두 찾아볼까요?"),
            choice("s2_growth",
                   "잎을 빛에 최대한 닿게 정렬하면 그 결과 어떻게 된대요?",
                   [("o0", "성장이 촉진된다", True), ("o1", "잎이 빛을 피한다", False), ("o2", "줄기가 약해진다", False)],
                   "thereby(그렇게 함으로써) 뒤를 봐요.",
                   why="'thereby promote growth', 그렇게 해서 성장을 촉진한대요. 빛을 많이 받아야 잘 자라요.",
                   highlight=["thereby", "promote growth"],
                   tips=[tip("not only A, (but) also B", "'A뿐만 아니라 B도'예요. 이 문장은 but 없이 콤마(,)와 also로 이었어요.", "not only"),
                         tip("thereby", "'그렇게 함으로써, 그 결과'예요.", "thereby")],
                   panel=board(L2, fresh=("follow the sun",))),
            show("s2_check", "빛에 노출되는 걸 '최대로 해야(maximize)' 성장이 촉진되죠. 그래서 (a)maximize는 문맥에 맞아요.",
                 highlight=["maximize", "exposure to light"], panel=check("a"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("Some plants", "몇몇 식물은"), g("actually", "실제로"), g("anticipate", "예상하다"), g("sunrise", "해 뜨는 것"),
                    g("from “memory,”", "'기억'으로"), g("even when deprived of solar signals", "해 신호를 받지 못할 때도"),
                    g("retain", "보유하다, 간직하다"), g("this information", "이 정보"), g("for several days", "며칠 동안")],
        "slashes": ["anticipate sunrise", "“memory,”", "solar signals", "this information"],
        "roles": [r("Some plants", "S"), r("anticipate", "V"), r("sunrise", "O"), r("retain", "V"), r("this information", "O")],
        "steps": [
            sv("s3_sv", ["Some plants", "anticipate", "sunrise", "retain", "this information"],
               {"Some plants": "S", "anticipate": "V", "retain": "V"},
               {"sunrise": "그건 anticipate가 예상하는 것(목적어)이에요.", "this information": "그건 retain이 간직하는 것(목적어)이에요."},
               "주어는 Some plants, 동사는 anticipate와 retain 둘이에요. even when ~ signals는 동사 사이에 끼어든 말이에요.",
               ask="이 문장의 주어(S)와, and로 이어진 동사(V) 둘을 찾아볼까요?"),
            show("s3_memory", "해 뜨는 걸 '기억'으로 미리 알고, 해 신호가 없어도 며칠 동안 그 정보를 간직한대요.",
                 highlight=["anticipate sunrise", "retain"],
                 tips=[tip("deprived of ~", "'~을 빼앗긴, ~을 받지 못한'이에요. deprived of solar signals = 해 신호를 받지 못한.", "deprived of")],
                 panel=board(L3, fresh=("anticipate sunrise",)), button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("In Brilliant Green", "『찬란한 초록』에서"), g("Stefano Mancuso and Alessandra Viola", "Stefano Mancuso와 Alessandra Viola는"),
                    g("argue", "주장한다"), g("plants", "식물"), g("possess", "가지고 있다"), g("not only", "~뿐만 아니라"),
                    g("the senses of sight, touch, smell, and hearing", "시각·촉각·후각·청각"),
                    g("more than a dozen other", "십여 개가 넘는 다른"), g("sensory capacities", "감각 능력"),
                    g("humans", "인간"), g("lack", "~이 없다")],
        "slashes": ["In Brilliant Green,", "Alessandra Viola", "argue", "plants possess", "and hearing,", "a dozen other", "sensory capacities"],
        "roles": [r("Stefano Mancuso and Alessandra Viola", "S"), r("argue", "V"), r("plants", "S"), r("possess", "V")],
        "modifiers": ["that humans lack"],
        "steps": [
            sv("s4_sv", ["argue", "plants", "possess", "humans", "lack"],
               {"plants": "S", "possess": "V"},
               {"argue": "그건 두 사람이 '주장한다'는 메인 동사예요. that 뒤에서 찾아봐요.",
                "humans": "그건 capacities를 꾸미는 that 덩어리 안의 말이에요.", "lack": "그건 capacities를 꾸미는 that 덩어리 안의 말이에요."},
               "주장 내용의 주어는 plants, 동사는 possess예요. 식물이 무엇을 가지고 있는지가 뒤에 나와요.",
               ask="argue that 뒤가 두 사람의 주장이에요. 그 안의 주어(S)와 동사(V)를 찾아볼까요?"),
            show("s4_check", "식물에겐 오감 말고도 인간에게 없는 감각 능력(sensory capacities)이 열 개 넘게 있대요. 그래서 (b)sensory는 문맥에 맞아요.",
                 highlight=["sensory capacities", "humans lack"],
                 tips=[tip("not only A but (also) B", "'A뿐만 아니라 B도'예요. 이 문장은 not only the senses ~, but more than a dozen ~이에요.", "not only"),
                       tip("a dozen", "'12개, 열두어 개'예요. more than a dozen = 십여 개가 넘는.", "a dozen")],
                 panel=check("a", "b"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("For example", "예를 들어"), g("the roots of plants", "식물의 뿌리는"), g("sense", "감지하다"),
                    g("the mineral and water content of the soil", "흙의 미네랄과 수분 함량"), g("alter", "바꾸다"),
                    g("their direction of growth", "자라는 방향"), g("accordingly", "그에 맞게")],
        "slashes": ["For example,", "the roots of plants", "of the soil"],
        "roles": [r("the roots", "S"), r("sense", "V"), r("the mineral and water content", "O"), r("alter", "V"), r("their direction", "O")],
        "steps": [
            show("s5_roots", "뿌리는 흙 속 미네랄과 물을 느끼고, 그에 맞게(accordingly) 자라는 방향을 바꾼대요.",
                 highlight=["sense", "alter their direction of growth"],
                 tips=[tip("accordingly", "'그에 맞게, 그에 따라'예요.", "accordingly")],
                 panel=board(L5, fresh=("alter their direction",)), button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Some", "몇몇 사람들은"), g("are", "~이다"), g("reluctant", "꺼리는"), g("to label plant movements as behaviors", "식물의 움직임을 행동이라고 부르기를"),
                    g("since", "~ 때문에"), g("they lack nerves and muscles", "그것들(식물)은 신경과 근육이 없다")],
        "slashes": ["(c)reluctant", "as behaviors,"],
        "roles": [r("Some", "S"), r("are", "V"), r("reluctant", "C"), r("they", "S"), r("lack", "V"), r("nerves and muscles", "O")],
        "steps": [
            choice("s6_why",
                   "몇몇 사람들은 왜 식물의 움직임을 행동이라고 부르기를 꺼린대요?",
                   [("o0", "식물에게 신경과 근육이 없어서", True), ("o1", "식물은 전혀 움직이지 않아서", False),
                    ("o2", "식물의 움직임이 너무 느려서", False)],
                   "since(~ 때문에) 뒤를 봐요.",
                   why="'since they lack nerves and muscles', 신경과 근육이 없다는 이유래요.",
                   highlight=["Some", "lack nerves and muscles"],
                   tips=[tip("reluctant to + 동사", "'~하기를 꺼리는, 내키지 않는'이에요.", "reluctant"),
                         tip("label A as B", "'A를 B라고 부르다, A에 B라는 이름을 붙이다'예요.", "label")],
                   panel=board(L5, R6, fresh=("lack nerves and muscles",))),
            show("s6_check", "Some(몇몇 사람들)은 식물이 행동하지 않는다는 쪽이에요. 신경이 없으니 행동이라 부르기를 꺼린다(reluctant), 이유와 맞아서 (c)reluctant는 문맥에 맞아요.",
                 highlight=["Some", "reluctant"], panel=check("a", "b", "c"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("But", "하지만"), g("just as", "~인 것처럼"), g("they", "그것들(식물)이"), g("are", "~이다"),
                    g("able to breathe without lungs", "폐 없이 숨 쉴 수 있는"), g("digest nutrients without a stomach", "위 없이 영양분을 소화하다"),
                    g("plants", "식물은"), g("have", "가지고 있다"), g("the ability", "능력"), g("to move", "움직일"), g("behave", "행동하다")],
        "slashes": ["But just as", "without lungs", "without a stomach,", "the ability"],
        "roles": [r("they", "S"), r("are", "V"), r("plants", "S"), r("have", "V"), r("the ability", "O")],
        "steps": [
            sv("s7_sv", ["they", "are", "plants", "have", "the ability"],
               {"plants": "S", "have": "V", "the ability": "O"},
               {"they": "그건 just as(~인 것처럼) 덩어리 안의 주어예요.", "are": "그건 just as 덩어리 안의 동사예요."},
               "콤마(,) 뒤 메인 문장은 주어 plants, 동사 have, 목적어 the ability예요.",
               ask="just as 덩어리 뒤, 메인 문장의 주어(S)·동사(V)·목적어(O)를 찾아볼까요?"),
            choice("s7_but",
                   "But 뒤 글쓴이 생각은 어느 쪽이에요?",
                   [("o0", "폐 없이 숨 쉬듯, 신경 없이도 움직일(행동할) 수 있다", True), ("o1", "신경이 없으니 행동할 수 없다", False)],
                   "just as(~인 것처럼) 뒤 예를 봐요. 폐가 없는데도 숨을 쉬어요.",
                   why="'plants have the ability to move (behave)', 폐 없이 숨 쉬듯 신경 없이도 행동할 수 있대요. 글쓴이는 Some과 반대로 '식물은 행동한다' 쪽이에요.",
                   highlight=["But", "the ability to move (behave)"],
                   tips=[tip("just as A, B", "'A인 것처럼 B도'예요. 앞 예와 뒤 주장이 짝을 이뤄요.", "just as")],
                   panel=board(L7, R6, fresh=("ability to move",)),
                   point="글쓴이 입장: But 뒤 — 신경이 없어도 식물은 행동한다"),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("We", "우리는"), g("should not dismiss", "일축해서는 안 된다, 무시해서는 안 된다"), g("absence", "없음, 부재"),
                    g("of behavioral capacities", "행동 능력의"), g("in an organism", "어떤 생물에게서"),
                    g("simply because", "단지 ~라는 이유로"), g("it", "그것(그 생물)"), g("lacks", "~이 없다"),
                    g("the physiological mechanism", "생리적 장치(메커니즘)"), g("is responsible for", "~의 원인이 되다"),
                    g("the behavior in animals", "동물의 행동")],
        "slashes": ["We should not dismiss", "behavioral capacities", "in an organism", "the physiological mechanism"],
        "roles": [r("We", "S"), r("should not dismiss", "V"), r("it", "S"), r("lacks", "V"), r("the physiological mechanism", "O")],
        "modifiers": ["that is responsible for the behavior in animals"],
        "steps": [
            sv("s8_sv", ["We", "should not dismiss", "it", "lacks", "the physiological mechanism"],
               {"We": "S", "should not dismiss": "V"},
               {"it": "그건 because 뒤 덩어리 안의 주어예요.", "lacks": "그건 because 뒤 덩어리 안의 동사예요.",
                "the physiological mechanism": "그건 lacks 뒤, 없는 것이에요."},
               "주어는 We, 동사는 should not dismiss예요. '~을 일축해서는 안 된다'는 글쓴이의 주장이에요.",
               ask="문장이 길어요. 맨 앞 메인 문장의 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s8_flow",
                   "simply because 뒤를 봐요. 동물 같은 장치가 없다는 이유만으로, 글쓴이는 식물을 어떻게 판단하지 말라는 걸까요?",
                   [("o0", "행동 능력이 없다고 판단하지 마라", True), ("o1", "행동 능력이 있다고 판단하지 마라", False)],
                   "앞 문장에서 글쓴이는 '식물은 행동한다' 쪽이었어요. dismiss는 '일축하다, 무시하다'예요.",
                   why="글쓴이는 식물이 행동한다는 쪽이에요. 신경 같은 장치가 없다는 이유만으로 '행동 능력이 없다'고 판단하지 말라는 흐름이에요.",
                   highlight=["should not dismiss", "simply because"],
                   tips=[tip("dismiss", "'일축하다, (생각할 가치가 없다며) 무시하다'예요.", "dismiss"),
                         tip("be responsible for", "'~의 원인이 되다, ~을 맡다'예요.", "responsible for")],
                   point="장치가 없다는 이유만으로 행동 능력이 '없다'고 하지 마라 — 이 흐름에 (d)가 맞는지 문제에서 확인"),
            show("s8_hold", "밑줄 (d)가 이 흐름과 맞는지는 마지막 문제에서 같이 확인해 봐요.", button="다음 문장"),
        ],
    },
    {
        "id": 9, "text": S[8], "model_translation": KO[8], "teaching_value": "medium",
        "glosses": [g("Plants", "식물은"), g("clearly", "분명히"), g("sense the environment", "환경을 감지하다"), g("learn", "배우다"),
                    g("store information", "정보를 저장하다"), g("use that information", "그 정보를 쓰다"),
                    g("to guide movements", "움직임을 이끌려고"), g("they behave", "그것들(식물)은 행동한다")],
        "slashes": ["sense the environment,", "learn,", "store information,", "that information", "movements;"],
        "roles": [r("Plants", "S"), r("sense", "V"), r("learn", "V"), r("store", "V"), r("use", "V"), r("they", "S"), r("behave", "V")],
        "steps": [
            show("s9_behave", "환경을 느끼고, 배우고, 정보를 저장해 움직임에 쓴대요. 세미콜론(;) 뒤 결론은 they behave, 식물은 행동한다예요.",
                 highlight=["they behave"], panel=board(L9, R6, fresh=("they behave",)), button="다음 문장"),
        ],
    },
    {
        "id": 10, "text": S[9], "model_translation": KO[9], "teaching_value": "medium",
        "glosses": [g("One might say", "누군가는 ~라고 말할지도 모른다"), g("there is", "있다"), g("certain “intelligence”", "어느 정도의 '지능'"),
                    g("to their behavior", "그들의 행동에")],
        "slashes": ["One might say", "certain “intelligence”"],
        "roles": [r("One", "S"), r("might say", "V")],
        "steps": [
            show("s10_intel", "식물의 행동에 어느 정도 '지능(intelligence)'이 있다고도 말할 수 있대요.",
                 highlight=["certain “intelligence”"], button="다음 문장"),
        ],
    },
    {
        "id": 11, "text": S[10], "model_translation": KO[10], "teaching_value": "high",
        "glosses": [g("This", "이것은"), g("is", "~이다"), g("true", "사실인"), g("as long as", "~하는 한"), g("intelligence", "지능"),
                    g("is defined", "정의되다"), g("in terms of", "~의 측면에서"), g("the ability to solve problems", "문제를 해결하는 능력"),
                    g("through behavioral", "행동을 통한"), g("interactions", "상호 작용"), g("with the environment", "환경과의"),
                    g("rather than", "~보다는"), g("with respect to mental capacity", "정신적 능력과 관련해서")],
        "slashes": ["This is true", "is defined", "in terms of the ability", "solve problems", "with the environment,"],
        "roles": [r("This", "S"), r("is", "V"), r("true", "C"), r("intelligence", "S"), r("is defined", "V")],
        "steps": [
            sv("s11_sv", ["This", "is", "true", "intelligence", "is defined"],
               {"This": "S", "is": "V", "true": "C"},
               {"intelligence": "그건 as long as(~하는 한) 덩어리 안의 주어예요.", "is defined": "그건 as long as 덩어리 안의 동사예요."},
               "주어는 This, 동사는 is, 보어는 true예요. as long as 뒤가 '어떤 조건에서' 사실인지예요."),
            choice("s11_define",
                   "지능을 무엇으로 정의할 때 식물에게 지능이 있다는 말이 사실이래요?",
                   [("o0", "환경과 행동으로 주고받으며 문제를 푸는 능력", True), ("o1", "머릿속으로 생각하는 정신 능력", False)],
                   "rather than(~보다는) 앞뒤를 봐요. 앞이 고른 쪽, 뒤가 버린 쪽이에요.",
                   why="'solve problems through behavioral (e)interactions with the environment', 환경과 행동으로 상호 작용해 문제를 푸는 능력이래요. rather than 뒤 정신 능력은 버린 쪽이에요.",
                   highlight=["solve problems", "rather than"],
                   tips=[tip("as long as", "'~하는 한, ~이기만 하면'이에요. 조건을 달아요.", "as long as"),
                         tip("in terms of / with respect to", "둘 다 '~의 측면에서, ~에 관해서'예요.", "in terms of")]),
            show("s11_check", "식물은 환경을 느끼고 반응해 움직이니, 환경과의 상호 작용(interactions)이 맞아요. 그래서 (e)interactions는 문맥에 맞아요.",
                 highlight=["interactions"], panel=check("a", "b", "c", "e"), panel_below=True),
            show("s11_go", "(a)(b)(c)(e)는 흐름에 맞았어요. 남은 하나가 '식물은 행동한다'는 글쓴이 생각과 맞는지 문제에서 골라 봐요.",
                 panel=check("a", "b", "c", "e"), panel_below=True, button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 5, [m("the roots of plants", "식물의 뿌리는"), " ", m("the mineral and water content of the soil", "흙의 미네랄과 수분 함량"), "을 ",
                         m("sense", "감지하고"), ", ", m("their direction of growth", "자라는 방향"), "을 ", m("accordingly", "그에 맞게"), " ",
                         m("alter", "바꾼다"), "."],
          sv_new=sv_step("s5_basic_sv", ["the roots", "plants", "sense", "the mineral and water content", "alter"],
                         {"the roots": "S", "sense": "V", "alter": "V"},
                         {"plants": "그건 of 뒤 덩어리예요.", "the mineral and water content": "그건 sense가 감지하는 것(목적어)이에요."},
                         "주어는 the roots, 동사는 sense와 alter 둘이에요."),
          meaning_ids=["s5_roots"])
add_basic(sentences, 10, [m("to their behavior", "그들의 행동에"), " ", m("certain “intelligence”", "어느 정도의 '지능'"), "이 ",
                          m("there is", "있다"), "고 ", m("One might say", "누군가는 말할지도 모른다"), "."],
          meaning_ids=["s10_intel"])

SENSES = {
    1: [sense("that", "capacities that plants use", "(앞 명사를 꾸밈)", "관계대명사 that + 주어·동사"),
        sense("to", "use to control", "~하기 위해", "to부정사 (목적)"),
        sense("to", "in response to", "~에 (반응하여)", "in response to ~ = ~에 반응하여")],
    2: [sense("as", "such a way as to", "(~하는 방식으로)", "in such a way as to + 동사원형 = ~하는 방식으로"),
        sense("to", "as to maximize", "~하는 (방식으로)", "in such a way as to + 동사원형"),
        sense("to", "exposure to light", "~에 (노출)", "exposure to ~ = ~에 노출됨")],
    3: [sense("for", "for several days", "~ 동안", "전치사 for + 기간")],
    4: [sense("that", "argue that plants", "~라고", "명사절 that (argue that …)"),
        sense("but", "but more than a dozen", "(not only A but B의) B도", "not only A but B"),
        sense("that", "capacities that humans lack", "(앞 명사를 꾸밈)", "관계대명사 that + 주어·동사")],
    5: [sense("for", "For example", "(For example의 일부)", "For example = 예를 들어")],
    6: [sense("to", "reluctant to label", "~하기를 (꺼리는)", "reluctant + to부정사"),
        sense("as", "label plant movements as behaviors", "~라고 (부르다)", "label A as B = A를 B라고 부르다"),
        sense("since", "since they lack", "~ 때문에", "접속사 since (이유)")],
    7: [sense("but", "But just as", "하지만", "접속사 but (반박)"),
        sense("as", "just as they are", "~인 것처럼", "just as + 주어·동사"),
        sense("to", "able to breathe", "~할 (수 있는)", "be able to + 동사원형"),
        sense("to", "ability to move", "~할 (능력)", "to부정사 (앞 명사 ability를 꾸밈)")],
    8: [sense("that", "mechanism that is responsible", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("for", "responsible for the behavior", "~의 (원인이 되는)", "be responsible for ~")],
    9: [sense("that", "use that information", "그", "지시형용사 that + 명사"),
        sense("to", "to guide movements", "~하기 위해", "to부정사 (목적)")],
    10: [sense("that", "say that there is", "~라고", "명사절 that (say that …)"),
         sense("to", "to their behavior", "~에 (있는)", "전치사 to (~에 딸린)")],
    11: [sense("as", "as long as", "(as long as의 일부)", "as long as = ~하는 한"),
         sense("as", "long as intelligence", "~하는 한", "as long as + 주어·동사 (조건)"),
         sense("to", "ability to solve", "~할 (능력)", "to부정사 (앞 명사 ability를 꾸밈)"),
         sense("to", "with respect to", "~에 (관해서)", "with respect to ~ = ~에 관해서")],
}

WORDS = {"what": "무엇", "plant": "식물", "knows": "알다", "biologist": "생물학자", "daniel": "Daniel(이름)", "chamovitz": "Chamovitz(성)",
         "describes": "설명하다", "sophisticated": "정교한", "information-processing": "정보 처리의", "capacities": "능력",
         "plants": "식물", "use": "쓰다", "control": "조절하다", "movements": "움직임", "response": "반응", "stimulation": "자극",
         "follow": "따라가다", "sun": "해", "bending": "구부리는 것", "stems": "줄기", "align": "정렬하다", "leaves": "잎",
         "such": "그러한", "way": "방식", "maximize": "최대로 하다", "exposure": "노출", "light": "빛", "thereby": "그렇게 함으로써",
         "promote": "촉진하다", "growth": "성장", "actually": "실제로", "anticipate": "예상하다", "sunrise": "해돋이", "memory": "기억",
         "deprived": "빼앗긴", "solar": "태양의", "signals": "신호", "retain": "보유하다", "information": "정보", "several": "몇몇의",
         "days": "날", "brilliant": "찬란한", "green": "초록", "stefano": "Stefano(이름)", "mancuso": "Mancuso(성)",
         "alessandra": "Alessandra(이름)", "viola": "Viola(성)", "argue": "주장하다", "possess": "가지고 있다", "senses": "감각",
         "sight": "시각", "touch": "촉각", "smell": "후각", "hearing": "청각", "dozen": "12개, 십여 개", "sensory": "감각의",
         "humans": "인간", "lack": "~이 없다", "example": "예", "roots": "뿌리", "sense": "감지하다", "mineral": "미네랄",
         "water": "물", "content": "함량", "soil": "흙", "alter": "바꾸다", "direction": "방향", "accordingly": "그에 맞게",
         "reluctant": "꺼리는", "label": "~라고 부르다", "behaviors": "행동", "nerves": "신경", "muscles": "근육",
         "able": "~할 수 있는", "breathe": "숨 쉬다", "lungs": "폐", "digest": "소화하다", "nutrients": "영양분", "stomach": "위",
         "ability": "능력", "move": "움직이다", "behave": "행동하다", "dismiss": "일축하다", "absence": "없음, 부재",
         "behavioral": "행동의", "organism": "생물, 유기체", "simply": "단지", "lacks": "~이 없다", "physiological": "생리적인",
         "mechanism": "장치, 메커니즘", "responsible": "원인이 되는", "behavior": "행동", "animals": "동물", "clearly": "분명히",
         "environment": "환경", "learn": "배우다", "store": "저장하다", "guide": "이끌다", "one": "누군가", "might": "~할지도 모른다",
         "say": "말하다", "certain": "어느 정도의", "intelligence": "지능", "true": "사실인", "long": "(as long as = ~하는 한)",
         "defined": "정의된", "terms": "측면", "solve": "해결하다", "problems": "문제", "interactions": "상호 작용",
         "rather": "(rather than = ~보다는)", "respect": "관련, 측면", "mental": "정신의", "capacity": "능력", "should": "~해야 한다",
         "knows,": "알다", "is": "~이다", "are": "~이다", "have": "가지고 있다", "there": "(there is = ~이 있다)"}

STORIES = [
    (3, [sc("문장 1~3", "🌱", "control movements · follow the sun · memory", "식물은 정보를 처리해 움직여요 — 해를 따라가고, 해 뜨는 걸 기억해요")]),
    (5, [sc("문장 4~5", "🌿", "sensory capacities · alter direction", "인간에게 없는 감각까지 있어서, 흙을 느끼고 자라는 방향을 바꿔요")]),
    (9, [sc("문장 6", "🙅", "Some · lack nerves and muscles", "신경·근육이 없으니 행동이 아니라는 사람들이 있어요"),
         sc("문장 7~9", "🌻", "But · they behave", "하지만 폐 없이 숨 쉬듯, 신경 없이도 식물은 행동해요")]),
]

exam = {
    "question": "밑줄 친 (a)~(e) 중에서 문맥상 낱말의 쓰임이 적절하지 않은 것은?",
    "underline": UNDER, "sentence": 8, "analysis_first": True, "wrong_rate": 34.0, "wrong_rank": 13,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("maximize", "최대로 하다"), g("sensory", "감각의"), g("reluctant", "꺼리는"), g("absence", "없음, 부재"),
                g("interactions", "상호 작용")],
    "options": [
        {"id": "1", "label": "(a) maximize", "keywords": ["maximize"], "ko": "최대로 하다"},
        {"id": "2", "label": "(b) sensory", "keywords": ["sensory"], "ko": "감각의"},
        {"id": "3", "label": "(c) reluctant", "keywords": ["reluctant"], "ko": "꺼리는"},
        {"id": "4", "label": "(d) absence", "keywords": ["absence"], "ko": "없음, 부재", "correct": True},
        {"id": "5", "label": "(e) interactions", "keywords": ["interactions"], "ko": "상호 작용"},
    ],
    "brief": exam_brief(
        "글쓴이는 식물이 행동한다는 쪽이에요. 이 생각과 맞지 않는 하나를 골라요.",
        "정답이에요! 글쓴이는 식물이 행동한다는 쪽이라, 장치가 없다는 이유만으로 행동 능력의 '존재'를 무시하면 안 된다는 말이에요. absence(부재)가 아니라 presence(존재)여야 해요.",
        "정답은 ④ (d)예요. 식물에게 행동 능력이 있다는 걸 무시하지 말라는 말이라, absence(부재)가 아니라 presence(존재)가 맞아요.",
        {"1": "빛에 노출되는 걸 최대로 해야(maximize) 성장이 촉진된다는 말이라 맞아요.",
         "2": "인간에게 없는 감각(sensory) 능력이 열 개 넘게 있다는 말이라 맞아요.",
         "3": "Some(몇몇 사람들)이 신경이 없다는 이유로 행동이라 부르기를 꺼린다(reluctant)는 말이라 맞아요.",
         "5": "지능을 환경과의 행동적 상호 작용(interactions)으로 문제를 푸는 능력으로 본다는 말이라 맞아요."},
        {"3": review(18,
                     "(c)는 글쓴이가 아니라 Some(몇몇 사람들)의 생각이에요. 신경과 근육이 없으니 행동이라 부르기를 꺼린다(reluctant), 이유와 딱 맞아요. 바로 뒤 But에서 글쓴이가 반박해요.",
                     panel=rows(("(c)", "Some are reluctant … since they lack nerves", "Some의 생각 — 이유와 맞음", "hl"),
                                ("(d)", "should not dismiss the absence of behavioral capacities", "글쓴이는 '행동한다' 쪽 → presence여야", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 41~42번 중 42번 (문맥상 낱말의 쓰임)",
    topic="어휘 문제 푸는 법: 요지 → 두 쪽(식물이 하는 일 vs 행동이라 부르기 꺼리는 쪽) → 밑줄 단어가 흐름에 맞는지 하나씩 점검",
    method={"type": "word_in_context", "labels": ["요지 잡기", "두 그룹으로 나누기", "밑줄 단어 맞춰 보기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-plant-behavior.svg", ("Plants", "식물"), "?", ("Behavior", "행동"),
                                       "식물도 '행동'한다고 할 수 있을까?", "2022년 3월 42번 도입 칠판"),
                      "alt": "칠판: Plants(식물) ? Behavior(행동)", "kind": "drawing"},
            "method": METHOD_IMAGES["vocab"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "식물은 움직일까요? 이번 글은 식물의 움직임을 '행동'이라고 부를 수 있는지 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "어휘 문제는 단어 뜻만 보면 다 맞아 보여요. 문장마다 흐름을 잡아야 틀린 단어가 보여요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "요지를 잡고, 생각을 두 쪽으로 나눈 뒤, 밑줄 단어가 흐름에 맞는지 하나씩 볼 거예요. 칠판 순서대로 해 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("sophisticated", "정교한"), g("capacity", "능력"), g("stimulation", "자극"), g("align", "정렬하다"),
                           g("exposure", "노출"), g("thereby", "그렇게 함으로써"), g("anticipate", "예상하다"), g("deprive", "빼앗다"),
                           g("retain", "보유하다"), g("sensory", "감각의"), g("alter", "바꾸다"), g("accordingly", "그에 맞게"),
                           g("reluctant", "꺼리는"), g("label A as B", "A를 B라고 부르다"), g("digest", "소화하다"),
                           g("nutrient", "영양분"), g("dismiss", "일축하다"), g("physiological", "생리적인"),
                           g("intelligence", "지능"), g("in terms of", "~의 측면에서")],
               "options": [g("absence", "부재, 없음"), g("presence", "존재, 있음")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# content 함량 · store 저장하다 · certain 어느 정도의.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    5: [tip("content", "이 글에서는 → 함량  ('내용' 아님)", "content", trap=True)],
    9: [tip("store", "이 글에서는 → 저장하다  ('가게' 아님)", "store", trap=True)],
    10: [tip("certain", "이 글에서는 → 어느 정도의  ('확실한' 아님)", "certain", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="어휘 문제 푸는 법",
       chunks={"the biologist Daniel Chamovitz": "생물학자 Daniel Chamovitz는", "describes": "설명한다",
               "sophisticated information-processing capacities": "정교한 정보 처리 능력", "plants": "식물", "use": "사용하다",
               "Plants": "식물은", "follow": "따라가다", "their stems": "자기 줄기", "they": "그것들", "align": "정렬하다",
               "Some plants": "몇몇 식물은", "anticipate": "예상하다", "sunrise": "해돋이", "retain": "보유하다", "this information": "이 정보",
               "argue": "주장한다", "possess": "가지고 있다", "humans": "인간", "lack": "~이 없다", "the roots": "뿌리",
               "sense": "감지하다", "the mineral and water content": "미네랄과 수분 함량", "alter": "바꾸다", "are": "~이다",
               "have": "가지고 있다", "the ability": "능력", "We": "우리는", "should not dismiss": "일축해서는 안 된다", "it": "그것",
               "lacks": "~이 없다", "the physiological mechanism": "생리적 장치", "This": "이것은", "is": "~이다", "true": "사실인",
               "intelligence": "지능", "is defined": "정의되다", "the roots of plants": "식물의 뿌리는",
               "the mineral and water content of the soil": "흙의 미네랄과 수분 함량", "their direction of growth": "자라는 방향",
               "accordingly": "그에 맞게", "to their behavior": "그들의 행동에", "certain “intelligence”": "어느 정도의 '지능'",
               "there is": "있다", "One might say": "누군가는 말할지도 모른다"})
