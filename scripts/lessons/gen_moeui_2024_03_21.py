"""2024년 3월 고3 21번 레슨 + 대사를 만든다 (밑줄 의미 추론, 2점). 오답률 49.9% · Top 10.

    python3 scripts/lessons/gen_moeui_2024_03_21.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: 기준 레슨 2026년 3월 21번(밑줄 의미) — 핵심 단어 → 관계(두 그룹) → 밑줄 뜻.
정답 ⑤ The perceived value of a product influences one's subjective experience of it.
많이 고른 오답 ① 23.9%(고객 평가가 가격을 정한다 — 방향이 거꾸로, 가격이 맛 평가를 바꾼다), ④ 12.5%.
열쇠: 감각(sensory input, sensory signals) ↔ 마음(psychological factors, labeled by price, believed expensive, placebo).
밑줄 you taste its price = 가격이라는 생각(지각된 가치)이 맛 경험 자체를 바꾼다. 해설지 해석과 대조함.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, add_that_sv, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2024-03-21-taste-its-price"

S = [
    "That perception is a construction is not true just of one’s perception of sensory input, such as visual and auditory information.",
    "It is true of your social perceptions as well―your perceptions of the people you meet, the food you eat, and even of the products you buy.",
    "For example, in a study of wine, when wines were tasted blind, there was little or no correlation between the ratings of a wine’s "
    "taste and its cost, but there was a significant correlation when the wines were labeled by price.",
    "That wasn’t because the subjects consciously believed that the higher-priced wines should be the better ones and thus revised "
    "whatever opinion they had accordingly.",
    "Or rather, it wasn’t true just at the conscious level.",
    "We know because as the subjects were tasting the wine, the researchers were imaging their brain activity, and the imaging showed "
    "that drinking what they believed was an expensive glass of wine really did activate their centers of taste for pleasure more than "
    "drinking a glass of the same wine that had been labeled as cheaper.",
    "That’s related to the placebo effect.",
    "Like pain, taste is not just the product of sensory signals; it depends also on psychological factors: you don’t just taste the wine; you taste its price.",
]
KO = [
    "인식이 구성이라는 것은 단지 시각 및 청각 정보와 같은 감각적 투입에 대한 한 사람의 인식에만 해당되는 것이 아니다.",
    "이것은 여러분의 사회적 인식, 즉 여러분이 만나는 사람, 여러분이 먹는 음식, 그리고 심지어 여러분이 사는 제품에 대한 여러분의 인식에도 해당된다.",
    "예를 들어, 와인에 대한 한 연구에서 와인이 조건을 숨긴 상태로 시음되었을 때 와인의 맛에 대한 평가와 그것의 가격 간의 상관관계가 거의 없거나 아예 없었지만, 와인이 가격에 따라 라벨이 붙었을 때는 유의미한 상관관계가 있었다.",
    "이는 피험자들이 가격이 더 비싼 와인이 더 좋은 와인일 것이라고 의식적으로 믿어서, 이에 따라 그들이 가졌던 어떠한 의견이든지 수정했기 때문은 아니었다.",
    "더 정확히 말하면, 이것은 단지 의식적인 수준에서만 그런 것이 아니었다.",
    "우리는 알 수 있는데, 왜냐하면 피험자들이 와인을 시음할 때 연구원들이 그들의 뇌 활동을 영상화했고, 그 영상은 그들이 고가의 와인 한 잔이라고 믿는 것을 마시는 것이 더 저렴하다고 라벨이 붙었던 같은 와인 한 잔을 마시는 것보다 그들의 만족감을 담당하는 미각 중추를 실제로 더 활성화했다는 것을 보여줬기 때문이다.",
    "이는 플라세보 효과와 관련이 있다.",
    "통증과 같이 미각은 단순히 감각 신호의 산물일 뿐만 아니라, 그것은 심리적 요인에도 좌우된다. 여러분은 와인을 단순히 맛보는 것이 아니다. 여러분은 그것의 가격을 맛보는 것이다.",
]

SENS = "왼쪽 · 감각 (몸으로 받는 신호)"
MIND = "오른쪽 · 마음 (생각·믿음)"


def board(left, right, fresh=(), sort=None):
    return groups("인식을 만드는 것", "감각 (sensory)", left, "마음 (psychological)", right, fresh=fresh, between="+",
                  sort={"words": sort, "left": SENS, "right": MIND} if sort else None)


L1 = [("sensory input", "감각 입력"), ("visual · auditory", "시각·청각")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("That perception is a construction", "인식이 (만들어진) 구성물이라는 것은"), g("perception", "인식, 지각"),
                    g("construction", "구성물, 만들어진 것"), g("is not true just of", "~에만 해당하는 것은 아니다"),
                    g("one’s perception of sensory input", "감각으로 들어오는 것에 대한 인식"), g("sensory input", "감각 입력"),
                    g("such as", "~ 같은"), g("visual and auditory information", "시각·청각 정보")],
        "slashes": ["is a construction", "is not true", "sensory input,"],
        "roles": [r("That perception is a construction", "S"), r("is not true", "V")],
        "steps": [
            sv("s1_sv", ["That perception is a construction", "is not true", "one’s perception of sensory input", "visual and auditory information"],
               {"That perception is a construction": "S", "is not true": "V"},
               {"one’s perception of sensory input": "그건 of 뒤 덩어리예요. 전치사 뒤라 주어가 아니에요.",
                "visual and auditory information": "그건 such as 뒤, 예시예요."},
               "주어는 That perception is a construction(인식이 구성물이라는 것), 동사는 is not true예요. That + 문장 전체가 주어예요.",
               ask="이 문장은 주어가 길어요. 주어(S)와 동사(V)를 찾아볼까요?"),
            show("s1_that", "That + 문장이 통째로 주어가 될 수 있어요. 'That perception is a construction'은 '인식이 만들어진 것이라는 것은'이에요.",
                 levels=["중", "초"], highlight=["That perception is a construction"],
                 tips=[tip("That + 문장 = 주어", "문장 맨 앞의 That 뒤에 주어·동사가 있고, 그 뒤에 또 동사가 오면 That 덩어리 전체가 주어예요. '~라는 것은'으로 읽어요.", "That")]),
            choice("s1_mean",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "인식은 감각 정보로만 만들어진다", False), ("o1", "시각과 청각은 서로 다르다", False),
                    ("o2", "인식이 만들어진 것이라는 건 감각 정보에만 해당하는 게 아니다", True)],
                   "not true just of는 '~에만 해당하는 건 아니다'예요. just(~만)가 핵심이에요.",
                   why="'is not true just of one’s perception of sensory input', 감각으로 들어오는 것에만 해당하는 건 아니라는 말이에요. 다른 데도 해당한다는 거예요.",
                   highlight=["construction", "not true just of", "sensory input"],
                   tips=[tip("not just", "'~만이 아니다'예요. 뒤에 '다른 것도'가 이어질 거라는 신호예요.", "just")],
                   panel=board(L1, [], fresh=("sensory input", "visual · auditory"))),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("It is true of", "그것은 ~에도 해당한다"), g("your social perceptions", "너의 사회적 인식"), g("as well", "~도 또한"),
                    g("the people you meet", "네가 만나는 사람들"), g("the food you eat", "네가 먹는 음식"),
                    g("the products you buy", "네가 사는 물건들")],
        "slashes": ["It is true", "as well―", "the people you meet,", "the food you eat,"],
        "roles": [r("It", "S"), r("is", "V"), r("true", "C")],
        "steps": [
            choice("s2_also",
                   "그럼 감각 정보 말고 무엇에도 해당한대요?",
                   [("o0", "오직 시각 정보", False), ("o1", "사회적 인식 — 만나는 사람, 먹는 음식, 사는 물건", True), ("o2", "과학 실험 결과", False)],
                   "'It is true of your social perceptions as well'을 봐요. 대시(―) 뒤가 그 예예요.",
                   why="'your social perceptions as well', 사회적 인식에도 해당한대요. 대시 뒤에 만나는 사람, 먹는 음식, 사는 물건이 예로 나와요.",
                   highlight=["social perceptions", "the products you buy"],
                   panel=board(L1, [("social perceptions", "사회적 인식"), ("the products you buy", "사는 물건")],
                               fresh=("social perceptions", "the products you buy"))),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("For example", "예를 들어"), g("in a study of wine", "와인 연구에서"), g("when wines were tasted blind", "와인을 가리고 맛보았을 때"),
                    g("there was little or no correlation", "상관관계가 거의 또는 전혀 없었다"), g("correlation", "상관관계"),
                    g("between", "~ 사이에"), g("the ratings of a wine’s taste", "와인 맛에 대한 평가"), g("its cost", "그것의 가격"),
                    g("there was a significant correlation", "뚜렷한 상관관계가 있었다"), g("when the wines were labeled by price", "와인에 가격표를 붙였을 때")],
        "slashes": ["For example,", "in a study of wine,", "tasted blind,", "little or no correlation", "and its cost,", "a significant correlation"],
        "roles": [r("was … was", "V"), r("little or no correlation", "S"), r("wines", "S"), r("were tasted", "V"),
                  r("a significant correlation", "S"), r("the wines", "S"), r("were labeled", "V")],
        "steps": [
            choice("s3_blind",
                   "와인을 가리고(blind) 맛봤을 때와 가격표를 붙였을 때, 결과가 어떻게 달랐대요?",
                   [("o0", "가리면 맛 평가와 가격이 거의 관계없고, 가격표를 붙이면 관계가 뚜렷했다", True),
                    ("o1", "둘 다 관계가 뚜렷했다", False), ("o2", "가리면 관계가 뚜렷했고, 가격표를 붙이면 없었다", False)],
                   "but 앞(blind → little or no correlation)과 뒤(labeled by price → significant correlation)를 나눠 봐요.",
                   why="가리고 마시면 'little or no correlation'(거의 관계없음), 가격표를 붙이면 'a significant correlation'(뚜렷한 관계)이래요. 가격을 알면 맛 평가가 가격을 따라가요.",
                   highlight=["tasted blind", "little or no correlation", "significant correlation", "labeled by price"],
                   tips=[tip("correlation", "'상관관계'예요. 하나가 커지면 다른 것도 커지는 것처럼 함께 움직이는 관계예요.", "correlation"),
                         tip("tasted blind", "'(정보를) 가리고 맛본'이에요. blind test = 상표·가격을 모르고 하는 시험.", "blind", trap=True)],
                   panel=board(L1, [("social perceptions", "사회적 인식"), ("the products you buy", "사는 물건"), ("labeled by price", "가격표")],
                               fresh=("labeled by price",)),
                   point="가리고 마시면 맛 평가 ≠ 가격, 가격표를 붙이면 맛 평가 = 가격을 따라감"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "medium",
        "glosses": [g("That wasn’t because", "그것은 ~ 때문이 아니었다"), g("the subjects", "실험 참가자들"), g("consciously believed", "의식적으로 믿었다"),
                    g("the higher-priced wines", "더 비싼 와인들"), g("should be the better ones", "더 좋은 것이어야 한다"),
                    g("thus", "그래서"), g("revised", "바꿨다"), g("whatever opinion they had", "그들이 가졌던 어떤 의견이든"), g("accordingly", "그에 맞춰")],
        "slashes": ["That wasn’t", "consciously believed", "the better ones", "and thus revised"],
        "roles": [r("That", "S"), r("wasn’t", "V"), r("the subjects", "S"), r("consciously believed", "V"), r("revised", "V"),
                  r("the higher-priced wines", "S"), r("should be", "V"), r("the better ones", "C")],
        "steps": [
            choice("s4_conscious",
                   "그건 참가자들이 '비싼 게 더 좋겠지' 하고 일부러(의식적으로) 의견을 바꿨기 때문이래요?",
                   [("o0", "그렇다, 일부러 바꿨다", False), ("o1", "아니다, 그것 때문만은 아니다", True)],
                   "문장 첫머리 'That wasn’t because …'를 봐요. wasn’t because는 '~ 때문이 아니었다'예요.",
                   why="'That wasn’t because …', 의식적으로 믿고 의견을 바꿨기 때문이 아니었대요. 다음 문장에서 더 깊은 이유가 나와요.",
                   highlight=["wasn’t because", "consciously"],
                   tips=[tip("subject", "실험 글에서 subject는 '주제'가 아니라 '실험 참가자(피험자)'예요.", "subjects", trap=True)]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("Or rather", "더 정확히 말하면"), g("it wasn’t true", "그건 사실이 아니었다"), g("just at the conscious level", "의식적인 수준에서만")],
        "slashes": ["Or rather,", "it wasn’t true"],
        "roles": [r("it", "S"), r("wasn’t", "V"), r("true", "C")],
        "steps": [
            show("s5_rather", "Or rather(더 정확히는), 의식적인 수준에서만 그런 게 아니었대요. 뇌 깊은 곳에서도 일어났다는 거예요.",
                 highlight=["Or rather", "just at the conscious level"], button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("We know", "우리는 안다"), g("because", "왜냐하면"), g("as the subjects were tasting the wine", "참가자들이 와인을 맛볼 때"),
                    g("the researchers", "연구자들"), g("were imaging", "영상으로 찍고 있었다"), g("their brain activity", "그들의 뇌 활동"),
                    g("the imaging", "그 영상"), g("showed", "보여 주었다"),
                    g("drinking what they believed was an expensive glass of wine", "비싼 와인이라고 믿은 것을 마시는 것"),
                    g("really did activate", "정말로 활성화했다"), g("their centers of taste for pleasure", "즐거움을 느끼는 미각 중추"),
                    g("more than", "~보다 더"), g("drinking a glass of the same wine", "같은 와인 한 잔을 마시는 것"),
                    g("that had been labeled as cheaper", "더 싸다고 붙여진")],
        "slashes": ["We know", "tasting the wine,", "were imaging", "their brain activity,", "the imaging showed", "an expensive glass of wine",
                    "really did activate", "taste for pleasure", "the same wine"],
        "roles": [r("We", "S"), r("know", "V"), r("the subjects", "S"), r("were tasting", "V"), r("the researchers", "S"), r("were imaging", "V"),
                  r("the imaging", "S"), r("showed", "V"), r("drinking what they believed was an expensive glass of wine", "S"),
                  r("really did activate", "V"), r("their centers of taste for pleasure", "O")],
        "modifiers": ["that had been labeled as cheaper"],
        "steps": [
            sv("s6_sv", ["We", "know", "the researchers", "were imaging", "the imaging", "showed"],
               {"the imaging": "S", "showed": "V"},
               {"We": "그건 맨 앞 '우리는 안다'의 주어예요. 결과는 and 뒤에 있어요.", "know": "그건 맨 앞 '우리는 안다'의 동사예요.",
                "the researchers": "그건 and 앞, 연구자들이 한 일의 주어예요.", "were imaging": "그건 and 앞, 연구자들이 한 일이에요."},
               "and 뒤는 주어 the imaging(그 영상), 동사 showed(보여 주었다)예요. that 뒤가 보여 준 내용이에요.",
               ask="아주 긴 문장이에요. 실험 결과가 나오는 and 뒤에서 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s6_result",
                   "뇌 영상은 무엇을 보여 줬대요?",
                   [("o0", "비싼 와인이 실제로 성분이 더 좋았다", False),
                    ("o1", "같은 와인인데도 비싸다고 믿고 마시면 즐거움의 맛 중추가 더 활발해졌다", True),
                    ("o2", "싸다고 믿은 와인이 더 활발하게 했다", False)],
                   "that 뒤 주어는 drinking what they believed was an expensive glass of wine, 동사는 really did activate예요. 마지막의 the same wine도 봐요.",
                   why="비싸다고 믿은(believed) 와인을 마시는 것이, 싸다고 붙인 같은(the same) 와인보다 즐거움의 맛 중추를 정말로 더 활성화했대요.",
                   highlight=["believed", "really did activate", "the same wine"],
                   panel=board(L1, [("social perceptions", "사회적 인식"), ("labeled by price", "가격표"), ("believed … expensive", "비싸다는 믿음")],
                               fresh=("believed … expensive",)),
                   point="같은 와인이어도 '비싸다고 믿으면' 뇌의 즐거움 맛 중추가 더 활성화 → 믿음이 맛을 바꾼다"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("That’s related to", "그것은 ~와 관련 있다"), g("the placebo effect", "플라세보(위약) 효과")],
        "slashes": ["That’s related"],
        "roles": [r("That", "S"), r("’s", "V"), r("related", "C")],
        "steps": [
            show("s7_placebo", "플라세보 효과와 관련 있대요. 가짜 약도 진짜라고 믿으면 몸이 나아지는 것처럼, 믿음이 실제 느낌을 바꾸는 거예요.",
                 highlight=["the placebo effect"],
                 tips=[tip("placebo effect", "'위약 효과'예요. 효과 없는 가짜 약도 진짜 약이라고 믿고 먹으면 실제로 나아지는 현상이에요.", "placebo")],
                 panel=board(L1, [("social perceptions", "사회적 인식"), ("labeled by price", "가격표"), ("believed … expensive", "비싸다는 믿음"),
                                  ("placebo effect", "플라세보 효과")], fresh=("placebo effect",)), button="다음 문장"),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("Like pain", "통증처럼"), g("taste", "맛, 미각"), g("is not just the product of", "~의 결과만은 아니다"),
                    g("sensory signals", "감각 신호"), g("it depends also on", "그것은 ~에도 달려 있다"), g("psychological factors", "심리적 요인"),
                    g("you don’t just taste the wine", "너는 와인을 맛보기만 하는 게 아니다"), g("you taste its price", "너는 그것의 가격을 맛본다")],
        "slashes": ["Like pain,", "is not just the product", "sensory signals;", "it depends also", "psychological factors:", "the wine;"],
        "roles": [r("taste", "S"), r("is", "V"), r("the product", "C"), r("it", "S"), r("depends", "V"), r("you … you", "S"),
                  r("don’t just taste … taste", "V"), r("the wine", "O"), r("its price", "O")],
        "steps": [
            choice("s8_factor",
                   "세미콜론(;) 앞을 봐요. 맛은 감각 신호의 결과만이 아니라 무엇에도 달려 있대요?",
                   [("o0", "와인의 원료", False), ("o1", "심리적 요인", True), ("o2", "마시는 장소", False)],
                   "'it depends also on …'을 봐요. depend on은 '~에 달려 있다'예요.",
                   why="'it depends also on psychological factors', 맛은 마음(psychological)에서 오는 것에도 달려 있대요.",
                   highlight=["sensory signals", "psychological factors"],
                   panel=board(L1 + [("sensory signals", "감각 신호")],
                               [("labeled by price", "가격표"), ("believed … expensive", "비싸다는 믿음"), ("placebo effect", "플라세보 효과"),
                                ("psychological factors", "심리적 요인")], fresh=("sensory signals", "psychological factors"))),
            choice("s8_underline",
                   "드디어 밑줄이에요. 'you don’t just taste the wine; you taste its price'는 무슨 뜻일까요?",
                   [("o0", "와인 가격은 맛 평가로 정해진다", False), ("o1", "비싼 와인일수록 실제로 성분이 좋다", False),
                    ("o2", "가격에 대한 생각(믿음)이 맛 경험 자체를 바꾼다", True)],
                   "taste the wine은 감각 쪽, its price는 마음 쪽이에요. 칠판 두 쪽을 이어 봐요.",
                   why="와인 자체(감각)만 맛보는 게 아니라, 가격이라는 생각(마음)까지 맛본다는 말이에요. 가격에 대한 믿음이 맛 경험을 바꿔요.",
                   highlight=["you taste its price"],
                   panel=board(L1 + [("sensory signals", "감각 신호"), ("taste the wine", "와인을 맛봄")],
                               [("labeled by price", "가격표"), ("believed … expensive", "비싸다는 믿음"), ("placebo effect", "플라세보 효과"),
                                ("psychological factors", "심리적 요인"), ("taste its price", "가격을 맛봄")],
                               fresh=("taste the wine", "taste its price")),
                   point="you taste its price = 가격(지각된 가치)이라는 생각이 맛이라는 주관적 경험을 바꾼다"),
            show("s8_go", "이 뜻을 다른 말로 바꿔 쓴 보기를 골라 봐요. 무엇이 무엇을 바꾸는지, 방향도 꼭 봐요.", button="문제 풀러 갈게요"),
        ],
    },
]

add_that_sv(sentences, 6, "s6_sv", "s6_that_sv",
            ["drinking what they believed was an expensive glass of wine", "really did activate", "their centers of taste for pleasure",
             "drinking a glass of the same wine"],
            {"drinking what they believed was an expensive glass of wine": "S", "really did activate": "V", "their centers of taste for pleasure": "O"},
            {"drinking a glass of the same wine": "그건 more than(~보다) 뒤, 비교하는 덩어리예요."},
            "that 안의 주어는 drinking …(비싸다고 믿은 와인을 마시는 것), 동사는 really did activate, 목적어는 their centers of taste for pleasure예요.",
            ask="that 뒤가 실험 결과예요. 그 안에서 주어(S), 동사(V), 목적어(O)를 찾아볼까요?")

add_basic(sentences, 2, [m("It is true of", "그것은 ~에도 해당한다"), " ", m("your social perceptions", "너의 사회적 인식"), " ", m("as well", "또한"),
                         " — ", m("the products you buy", "네가 사는 물건들"), "까지."],
          sv_new=sv_step("s2_basic_sv", ["It", "is", "true", "your social perceptions"], {"It": "S", "is": "V", "true": "C"},
                         {"your social perceptions": "그건 of 뒤 덩어리예요."},
                         "주어는 It(앞 문장의 '인식이 구성물이라는 것'), 동사는 is, 보어는 true예요."),
          meaning_after="s2_also")
add_basic(sentences, 4, [m("That wasn’t because", "그것은 ~ 때문이 아니었다"), " — ", m("the subjects", "참가자들이"), " ", m("the higher-priced wines", "더 비싼 와인이"),
                         " ", m("should be the better ones", "더 좋을 거라고"), " ", m("consciously believed", "의식적으로 믿었기"), " 때문이."],
          match_display="That wasn’t because the subjects consciously believed that the higher-priced wines should be the better ones.",
          sv_new=sv_step("s4_basic_sv", ["That", "wasn’t", "the subjects", "consciously believed"], {"That": "S", "wasn’t": "V"},
                         {"the subjects": "그건 because 뒤 덩어리 안의 주어예요.", "consciously believed": "그건 because 뒤 덩어리 안의 동사예요."},
                         "주어는 That(앞 문장의 결과), 동사는 wasn't예요. because 뒤가 '아니었던' 이유예요."),
          meaning_after="s4_conscious")
add_basic(sentences, 5, [m("Or rather", "더 정확히 말하면"), ", ", m("it wasn’t true", "그건 사실이 아니었다"), " — ", m("just at the conscious level", "의식적인 수준에서만"), "."],
          sv_new=sv_step("s5_basic_sv", ["it", "wasn’t", "true", "the conscious level"], {"it": "S", "wasn’t": "V", "true": "C"},
                         {"the conscious level": "그건 at 뒤 덩어리예요."},
                         "주어는 it, 동사는 wasn't, 보어는 true예요."),
          meaning_ids=["s5_rather"])
add_basic(sentences, 7, [m("That’s related to", "그것은 ~와 관련 있다"), " ", m("the placebo effect", "플라세보 효과"), "."],
          sv_new=sv_step("s7_basic_sv", ["That", "’s", "related", "the placebo effect"], {"That": "S", "’s": "V", "related": "C"},
                         {"the placebo effect": "그건 to 뒤 덩어리예요."},
                         "That’s = That is예요. 주어 That, 동사 ’s(is), 보어 related(관련 있는)예요.",
                         ask="That’s는 That is를 줄인 말이에요. 주어(S)·동사(V)·보어(C)를 찾아볼까요?"),
          meaning_ids=["s7_placebo"])

SENSES = {
    1: [sense("that", "That perception is a construction", "~라는 것(은)", "명사절 that + 완전한 문장 (주어 자리)"),
        sense("as", "such as visual", "~ 같은", "such as + 명사 (예시)")],
    2: [sense("as", "as well", "~도 또한", "as well (문장 끝) = 또한")],
    3: [sense("for", "For example", "(For example의 일부)", "For example = 예를 들어"),
        sense("but", "but there was", "하지만", "접속사 but + 주어·동사")],
    4: [sense("that", "That wasn’t because", "그것", "지시대명사 that (앞 문장의 결과)"),
        sense("that", "believed that the higher-priced", "~라고", "명사절 that (believe that …)")],
    6: [sense("as", "as the subjects were tasting", "~할 때, ~하는 동안", "접속사 as + 주어·동사 (시간)"),
        sense("that", "showed that drinking", "~라는 것을", "명사절 that (show that …)"),
        sense("for", "taste for pleasure", "~을 위한, ~의", "전치사 for + 명사"),
        sense("that", "wine that had been labeled", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("as", "labeled as cheaper", "~로", "label A as B = A에 B라고 붙이다")],
    7: [sense("that", "That’s related", "그것", "지시대명사 that (앞 내용)"), sense("to", "related to", "~와 (관련)", "be related to + 명사")],
}

WORDS = {"perception": "인식, 지각", "construction": "구성물", "true": "맞는, 해당하는", "one’s": "사람의", "sensory": "감각의",
         "input": "입력", "visual": "시각의", "auditory": "청각의", "information": "정보", "social": "사회적인", "perceptions": "인식",
         "people": "사람들", "meet": "만나다", "food": "음식", "eat": "먹다", "products": "물건, 제품", "buy": "사다", "example": "예",
         "study": "연구", "wine": "와인", "wines": "와인들", "tasted": "맛본", "blind": "가리고", "little": "거의 없는", "correlation": "상관관계",
         "ratings": "평가", "wine’s": "와인의", "taste": "맛, 맛보다", "cost": "가격", "significant": "뚜렷한", "labeled": "표가 붙은",
         "price": "가격", "subjects": "실험 참가자들", "consciously": "의식적으로", "believed": "믿었다", "higher-priced": "더 비싼",
         "better": "더 좋은", "ones": "것들", "revised": "바꿨다", "whatever": "무엇이든", "opinion": "의견", "accordingly": "그에 맞춰",
         "rather": "오히려 · Or rather = 더 정확히는", "conscious": "의식적인", "level": "수준", "know": "알다", "tasting": "맛보는",
         "researchers": "연구자들", "imaging": "영상으로 찍는, 영상", "brain": "뇌", "activity": "활동", "showed": "보여 주었다",
         "drinking": "마시는 것", "expensive": "비싼", "glass": "잔", "activate": "활성화하다", "centers": "중추", "pleasure": "즐거움",
         "same": "같은", "cheaper": "더 싼", "related": "관련 있는", "placebo": "위약, 플라세보", "effect": "효과", "pain": "통증",
         "product": "결과물", "signals": "신호", "depends": "~에 달려 있다", "psychological": "심리적인", "factors": "요인",
         "wasn’t": "~이 아니었다", "that’s": "그것은 ~이다", "don’t": "~하지 않다", "really": "정말로", "thus": "그래서",
         "had": "가졌다", "were": "~였다", "been": "(had been = ~되었던)"}

STORIES = [
    (3, [sc("문장 1~2", "🧠", "perception = construction", "인식은 만들어지는 것 — 감각뿐 아니라 사람·음식·물건에 대한 인식도요"),
         sc("문장 3", "🍷", "blind ↔ labeled by price", "가리고 마시면 맛 평가와 가격이 관계없고, 가격표를 붙이면 따라가요")]),
    (7, [sc("문장 4~6", "🔬", "not just conscious · brain activity", "일부러 의견을 바꾼 게 아니라, 비싸다고 믿으면 뇌의 즐거움 중추가 더 활발했어요"),
         sc("문장 7", "💊", "placebo effect", "믿음이 실제 느낌을 바꾸는 플라세보 효과와 같아요")]),
]

OPTIONS = [
    ("1", "Customer ratings determine the price of a product.", ["Customer ratings", "determine the price"], "고객 평가가 제품 가격을 정한다", False),
    ("2", "We fool ourselves into thinking our unplanned buying was reasonable.", ["unplanned buying", "reasonable"], "충동구매가 합리적이었다고 스스로를 속인다", False),
    ("3", "We immediately dismiss opposing opinions without any consideration.", ["dismiss opposing opinions"], "반대 의견을 생각도 않고 바로 무시한다", False),
    ("4", "The brain shows consistent response regardless of personal preference.", ["consistent response", "regardless"], "뇌는 개인 취향과 상관없이 같은 반응을 보인다", False),
    ("5", "The perceived value of a product influences one’s subjective experience of it.", ["perceived value", "influences", "subjective experience"],
     "제품의 지각된 가치가 그 제품에 대한 주관적 경험에 영향을 준다", True),
]
exam = {
    "question": "밑줄 친 you taste its price가 의미하는 바로 가장 적절한 것은?",
    "underline": "you taste its price", "analysis_first": True, "wrong_rate": 49.9, "wrong_rank": 10,
    "glosses": [g("customer", "고객"), g("ratings", "평가"), g("determine", "정하다"), g("fool", "속이다"), g("unplanned", "계획에 없던"),
                g("reasonable", "합리적인"), g("dismiss", "무시하다"), g("opposing", "반대하는"), g("consistent", "일관된"),
                g("regardless of", "~와 상관없이"), g("preference", "취향"), g("perceived", "지각된, 느껴진"), g("value", "가치"),
                g("influences", "영향을 주다"), g("subjective", "주관적인"), g("experience", "경험")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "보기도 다 해석할 필요 없어요. 색칠된 단어만 보고, 가격(생각)이 맛(경험)을 바꾼다는 방향을 떠올리며 골라 봐요.",
        "정답이에요! 가격이라는 지각된 가치(perceived value)가 맛이라는 주관적 경험(subjective experience)을 바꿔요. 그래서 와인이 아니라 가격을 맛본다고 한 거예요.",
        "정답은 ⑤예요. 가격(지각된 가치)이 맛 경험(주관적 경험)에 영향을 준다는 말이에요.",
        {"1": "방향이 거꾸로예요. 글은 가격이 맛 평가를 바꾼다고 했지, 평가가 가격을 정한다고 하지 않았어요.",
         "2": "충동구매 이야기는 글에 없어요.",
         "3": "반대 의견을 무시하는 이야기는 글에 없어요.",
         "4": "뇌가 같은 반응을 보인 게 아니라, 비싸다고 믿을 때 더 활성화됐어요. 반대예요."},
        {"1": review(23.9,
                     "①은 '고객 평가가 제품 가격을 정한다'예요. 글에 rating(평가)과 price(가격)가 다 나와서 그럴듯해 보여요. 하지만 글은 거꾸로, 가격표가 맛 평가를 바꾼다고 했어요. 무엇이 무엇을 바꾸는지 방향이 반대예요.",
                     panel=rows(("글", "labeled by price → ratings of taste", "가격이 맛 평가를 바꾼다", "hl"),
                                ("①", "Customer ratings → the price", "평가가 가격을 정한다 (거꾸로)", "hl2")),
                     rank_word="가장 많이 고른")}),
}

# ── 해석 맞추기(모두에게)·가리키는 말 — 2026-10-20 엔진: S·V 찾기·핵심어 자유 해석은 빠지고 맞추기가 대신 나온다 ──
from beginner import add_match, add_refers, m as _m  # noqa: E402
add_match(sentences, 1, [_m("That perception is a construction", "인식이 구성이라는 것은"), " 단지 ", _m("visual and auditory information", "시각 및 청각 정보"),
                         _m("such as", "와 같은"), " ", _m("one’s perception of sensory input", "감각적 투입에 대한 인식"),
                         _m("is not true just of", "에만 해당되는 것이 아니다"), "."])
add_match(sentences, 6, ["우리는 안다 — ", _m("the imaging", "그 영상은"), " ", _m("drinking what they believed was an expensive glass of wine", "비싼 와인이라고 믿은 것을 마시는 것이"), " ",
                         _m("their centers of taste for pleasure", "만족감을 담당하는 미각 중추를"), " ", _m("really did activate", "실제로 더 활성화했다는 것을"), " ",
                         _m("showed", "보여 줬다"), "."],
          display="We know because the imaging showed that drinking what they believed was an expensive glass of wine really did activate their centers of taste for pleasure.")
add_refers(sentences, 2, {"It is true of": "It = that perception is a construction(인식이 구성이라는 것)"})
add_refers(sentences, 4, {"That wasn’t because": "That = the correlation when wines were labeled by price(가격표를 붙이자 평가가 달라진 것)"})
add_refers(sentences, 5, {"it wasn’t true": "it = the effect of price on taste(가격이 맛 평가에 미친 영향)"})
add_refers(sentences, 7, {"That": "price activating the taste centers(가격이 미각 중추를 더 활성화한 것)"})
add_refers(sentences, 8, {"it": "taste(미각)"})

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 21번 (밑줄 의미 추론, 2점)",
    topic="밑줄 문제 푸는 법: 핵심 단어 → 관계(감각 + 마음) → 밑줄 뜻",
    method={"type": "underline_meaning", "labels": ["핵심 단어 찾기", "관계 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-wine-price.svg", ("Wine", "와인 맛"), "+", ("Price", "가격"),
                                       "같은 와인도 가격표에 따라 맛이 달라질까?", "2024년 3월 21번 도입 칠판"),
                      "alt": "칠판: Wine(와인 맛) + Price(가격)", "kind": "drawing"},
            "method": METHOD_IMAGES["underline"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "같은 와인인데 비싼 가격표가 붙으면 더 맛있을까요? 이번 글은 맛을 느끼는 데 무엇이 작용하는지 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네", "brief": {"say": "수능 문제는 시간 싸움이에요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "밑줄 문제는 핵심 단어 위주로 지문의 요지를 빠르게 파악하면 좋아요."}}],
    exam=exam,
    key_words={"passage": [g("perception", "인식, 지각"), g("construction", "구성물"), g("sensory", "감각의"), g("auditory", "청각의"),
                           g("correlation", "상관관계"), g("significant", "뚜렷한, 유의미한"), g("subject", "실험 참가자"),
                           g("consciously", "의식적으로"), g("revise", "수정하다"), g("accordingly", "그에 맞춰"), g("activate", "활성화하다"),
                           g("placebo effect", "위약 효과"), g("depend on", "~에 달려 있다"), g("psychological", "심리적인")],
               "options": [g("perceived value", "지각된 가치"), g("subjective", "주관적인"), g("dismiss", "무시하다"), g("consistent", "일관된")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# construction 구성(된 것) · product 산물, 결과물.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    1: [tip("construction", "이 글에서는 → 구성(된 것)  ('건설, 공사' 아님)", "construction", trap=True)],
    8: [tip("product", "이 글에서는 → 산물, 결과물  ('제품' 아님)", "product", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="밑줄 문제 푸는 법",
       chunks={"That perception is a construction": "인식이 구성물이라는 것은", "is not true": "해당하지 않는다",
               "one’s perception of sensory input": "감각 입력에 대한 인식", "visual and auditory information": "시각·청각 정보",
               "It": "그것", "is": "~이다", "true": "해당하는", "That": "그것", "wasn’t": "~이 아니었다", "the subjects": "실험 참가자들",
               "consciously believed": "의식적으로 믿었다", "it": "그것", "the conscious level": "의식적인 수준", "We": "우리는", "know": "안다",
               "the researchers": "연구자들", "were imaging": "영상으로 찍고 있었다", "the imaging": "그 영상", "showed": "보여 주었다",
               "drinking what they believed was an expensive glass of wine": "비싸다고 믿은 와인을 마시는 것",
               "really did activate": "정말로 활성화했다", "their centers of taste for pleasure": "즐거움을 느끼는 미각 중추",
               "drinking a glass of the same wine": "같은 와인 한 잔을 마시는 것", "That’s": "그것은 ~이다", "related": "관련 있는",
               "the placebo effect": "플라세보 효과", "It is true of": "그것은 ~에도 해당한다", "your social perceptions": "너의 사회적 인식",
               "as well": "또한", "the products you buy": "네가 사는 물건들", "That wasn’t because": "그것은 ~ 때문이 아니었다",
               "the higher-priced wines": "더 비싼 와인들", "should be the better ones": "더 좋은 것이어야 한다", "Or rather": "더 정확히 말하면",
               "it wasn’t true": "그건 사실이 아니었다", "just at the conscious level": "의식적인 수준에서만", "That’s related to": "그것은 ~와 관련 있다"})
