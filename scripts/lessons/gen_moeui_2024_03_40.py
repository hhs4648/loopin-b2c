"""2024년 3월 고3 40번 레슨 + 대사를 만든다 (요약문 완성, 2점). 오답률 48.3% · Top 11.

    python3 scripts/lessons/gen_moeui_2024_03_40.py   (→ npm run policy:copy stamp <id> → npm run build)

요약문 유형은 처음 — 푸는 법은 선생님이 고른 「지문 먼저 → 요약문」(2026-10-17): 지문을 처음부터 읽으며 두 쪽 말을 칠판에 모으고
(plastic이라는 말이 주는 느낌 ↔ 뇌가 실제로 하는 일), 마지막에 요약문을 읽고 (A)·(B)가 각각 어느 쪽인지 → 그 뜻의 말을 고른다.
정답 ① permanence ······ transformation.
많이 고른 오답 ⑤ mobility·transformation 14.6%, ② flexibility·sympathizing 14.2% — plastic의 '잘 휘는' 느낌으로 (A)를 고른 경우.
(A) 자리는 '한 번 성형하면 영원히 그대로'(mold once, keep it that way forever)라서 변하지 않음(permanence)이어야 한다.
해설지 해석과 대조함. mold, inscription은 시험지 아래 *로 풀어 준 단어(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, add_that_sv, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)

ID = "moeui-2024-03-40-brain-plasticity"

SUMMARY = ("While some understand “brain plasticity” to mean (A) ________ upon molding, the brain is actually capable of (B) ________.")
S = [
    "“Brain plasticity” is a term we use in neuroscience.",
    "Whether intentionally or not, “plasticity” suggests that the key idea is to mold something once and keep it that way forever: "
    "to shape the plastic toy and never change it again.",
    "But that’s not what the brain does.",
    "It carries on remolding itself throughout your life.",
    "Think of a developing city, and note the way it grows, improves, and responds to the world around it.",
    "Observe where the city builds its truck stops, how it crafts its immigration policies, and how it modifies its education and legal systems.",
    "A city is always changing.",
    "A city is not designed by urban planners and then immobilized like a plastic object.",
    "It continually develops.",
    "Just like cities, brains never reach an end point.",
    "We spend our lives blossoming toward something, even as the target moves.",
    "Consider the feeling of encountering a diary that you wrote many years ago.",
    "It represents the thinking, opinions, and viewpoint of someone who was a bit different from who you are now, and that previous "
    "person can sometimes border on the unrecognizable.",
    "Despite having the same name and the same early history, in the years between inscription and interpretation the narrator has altered.",
    "The word “plastic” can be stretched to fit this notion of ongoing change.",
    SUMMARY,
]
KO = [
    "'뇌 가소성'은 우리가 신경 과학에서 사용하는 용어이다.",
    "의도적이든 아니든, '가소성'은 핵심 개념이 무언가를 한 번 성형하고 그것을 그대로 영원히 유지하는 것이라고 시사한다. 즉, 플라스틱 장난감의 모양을 만들고 다시는 그것을 바꾸지 않는 것이다.",
    "하지만 그것은 뇌가 하는 것이 아니다.",
    "뇌는 여러분의 생애 내내 그 자신을 재성형하는 것을 계속한다.",
    "개발 중인 도시를 생각해 보라, 그리고 그것이 성장하고, 진보하고, 주변 세상에 반응하는 방식에 주목하라.",
    "그 도시가 어디에 그것의 트럭 정류장을 짓고, 어떻게 그것의 이민 정책을 공들여 만들고, 어떻게 그것의 교육과 법률 체계를 수정하는지 관찰하라.",
    "도시는 항상 변화하고 있다.",
    "도시는 도시 계획자들에 의해 설계되고 나서 플라스틱 물건처럼 고정되지 않는다.",
    "그것은 끊임없이 발전한다.",
    "도시와 마찬가지로, 뇌는 결코 종점에 도달하지 않는다.",
    "심지어 우리는 목표물이 움직이더라도, 무언가를 향해 번성하며 삶을 보낸다.",
    "여러분이 수년 전에 쓴 일기를 우연히 발견했을 때의 감정을 생각해 보라.",
    "그것은 지금의 여러분과는 약간 다른 누군가의 생각, 의견, 그리고 관점을 나타내며, 그 이전의 사람은 때때로 거의 몰라볼 정도의 사람이라고 말할 수 있다.",
    "같은 이름과 같은 초기 역사를 가지고 있음에도 불구하고, 새겨진 글과 해석 사이의 세월 동안 화자가 달라졌다.",
    "'플라스틱'이라는 단어는 이러한 진행 중인 변화의 개념에 맞도록 확장될 수 있다.",
    "어떤 사람들은 성형되자마자 '뇌 가소성'이 (A)를 의미한다고 이해하는 반면, 뇌는 실제로 (B)할 수 있다.",
]

WORD = "왼쪽 · plastic이라는 말의 느낌"
REAL = "오른쪽 · 뇌가 실제로 하는 일"


def board(left, right, fresh=(), sort=None):
    # 묶음 이름은 지문에서 나온 말까지만 — 요약문의 (A)(B) 자리는 칠판에 쓰지 않는다
    return groups("plastic ↔ brain", "plastic이라는 말의 느낌", left, "뇌가 실제로 하는 일", right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": WORD, "right": REAL} if sort else None)


L2 = [("mold once", "한 번 성형"), ("keep it that way forever", "영원히 그대로"), ("never change it again", "다시는 안 바꿈")]
R4 = [("remolding itself", "스스로 다시 성형"), ("throughout your life", "평생")]
R7 = R4 + [("always changing", "늘 변함")]
R9 = R7 + [("not immobilized", "고정되지 않음"), ("continually develops", "계속 발전")]
R10 = R9 + [("never reach an end point", "끝이 없음")]
R14 = R10 + [("the narrator has altered", "화자가 달라짐")]
R15 = R14 + [("ongoing change", "계속되는 변화")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("Brain plasticity", "뇌 가소성 · 뇌가 바뀔 수 있는 성질"), g("is a term", "용어이다"), g("we use", "우리가 쓰는"),
                    g("in neuroscience", "신경 과학에서")],
        "slashes": ["is a term"],
        "roles": [r("Brain plasticity", "S"), r("is", "V"), r("a term", "C")],
        "modifiers": ["we use in neuroscience"],
        "steps": [
            show("s1_term", "뇌 가소성(brain plasticity)이라는 신경 과학 용어 이야기예요. plastic이라는 말에서 나온 용어예요.",
                 highlight=["Brain plasticity"], button="다음 문장",
                 tips=[tip("요약문 문제 요령", "지문을 먼저 읽으며 글쓴이 주장을 잡고 같은 쪽 말을 모아요. 마지막에 요약문 (A)(B)가 각각 어느 쪽 말인지 보고 골라요.")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Whether intentionally or not", "의도했든 아니든"), g("plasticity", "가소성"), g("suggests", "암시하다"),
                    g("the key idea", "핵심 개념"), g("is", "~이다"), g("to mold something once", "무언가를 한 번 성형하는 것"),
                    g("keep it that way forever", "영원히 그대로 두다"), g("to shape the plastic toy", "플라스틱 장난감의 모양을 만드는 것"),
                    g("never change it again", "다시는 바꾸지 않다")],
        "slashes": ["intentionally or not,", "“plasticity” suggests", "the key idea is", "mold something once", "that way forever:", "the plastic toy"],
        "roles": [r("plasticity", "S"), r("suggests", "V"), r("the key idea", "S"), r("is", "V")],
        "steps": [
            sv("s2_sv", ["Whether intentionally or not", "plasticity", "suggests", "the key idea", "is"],
               {"plasticity": "S", "suggests": "V"},
               {"Whether intentionally or not": "그건 '의도했든 아니든', 덧붙인 말이에요.",
                "the key idea": "그건 that 뒤 덩어리 안의 주어예요. 먼저 바깥 문장을 봐요.", "is": "그건 that 뒤 덩어리 안의 동사예요."},
               "주어는 “plasticity”, 동사는 suggests(암시하다)예요. that 뒤가 그 말이 떠올리게 하는 내용이에요.",
               ask="주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s2_mean",
                   "plasticity라는 말은 무엇을 떠올리게 한대요?",
                   [("o0", "계속해서 모양을 바꾸는 것", False), ("o1", "부드럽게 잘 휘는 것", False),
                    ("o2", "한 번 모양을 만들고 영원히 그대로 두는 것", True)],
                   "that 뒤 'to mold something once and keep it that way forever'를 봐요. 콜론(:) 뒤가 같은 말을 풀어 줘요.",
                   why="'to mold something once and keep it that way forever', 한 번 성형하고 영원히 그대로 두는 거래요. 콜론 뒤 '장난감을 만들고 다시는 안 바꾼다'도 같은 말이에요.",
                   highlight=["mold something once", "keep it that way forever", "never change it again"],
                   panel=board(L2, [], fresh=("mold once", "keep it that way forever", "never change it again")),
                   tips=[tip("keep it that way", "'그 상태 그대로 두다'예요. that way = 그런 식으로, 그 상태로.", "that way")],
                   point="plasticity라는 말의 느낌 = 한 번 성형하고(mold once) 영원히 그대로(keep it that way forever)"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("But", "하지만"), g("that’s not", "그것은 ~이 아니다"), g("what the brain does", "뇌가 하는 일")],
        "roles": [r("that", "S"), r("’s", "V"), r("what the brain does", "C")],
        "steps": [
            choice("s3_but",
                   "But — 'that’s not what the brain does'는 무슨 말일까요?",
                   [("o0", "뇌는 한 번 만들고 그대로 두지 않는다", True), ("o1", "뇌는 플라스틱 장난감과 똑같다", False),
                    ("o2", "뇌는 처음부터 완성돼 있다", False)],
                   "that은 앞 문장의 '한 번 성형하고 영원히 그대로'예요. 뇌는 그렇지 않대요.",
                   why="that(한 번 성형하고 그대로 두기)은 뇌가 하는 일이 아니래요. But으로 말의 느낌과 실제 뇌를 뒤집어요.",
                   highlight=["But", "not what the brain does"],
                   point="But that’s not what the brain does = 뇌는 '한 번 만들고 그대로'가 아니다 (글쓴이 주장 시작)"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("It", "그것(뇌)"), g("carries on", "계속하다"), g("remolding itself", "스스로를 다시 성형하는 것"),
                    g("throughout your life", "평생 동안")],
        "slashes": ["remolding itself"],
        "roles": [r("It", "S"), r("carries on", "V"), r("remolding itself", "O")],
        "steps": [
            show("s4_remold", "뇌는 평생 스스로를 다시 성형하기를 계속한대요.",
                 highlight=["carries on", "remolding itself"],
                 tips=[tip("carry on -ing", "'계속 ~하다'예요. carries on remolding = 계속 다시 성형한다.", "carries on"),
                       tip("re-", "'다시'예요. remold = 다시 성형하다.", "remolding")],
                 panel=board(L2, R4, fresh=("remolding itself", "throughout your life")), button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "low",
        "glosses": [g("Think of", "~을 떠올려 보라"), g("a developing city", "발전하는 도시"), g("note", "주목하라"), g("the way", "방식"),
                    g("grows, improves, and responds", "자라고, 나아지고, 반응한다"), g("the world around it", "그 주변 세상")],
        "slashes": ["a developing city,", "note the way", "and responds"],
        "roles": [r("Think", "V"), r("a developing city", "O"), r("note", "V"), r("the way", "O"), r("it", "S"), r("grows", "V"), r("improves", "V"),
                  r("responds", "V")],
        "steps": [
            show("s5_city", "뇌를 도시에 빗대요. 발전하는 도시는 자라고, 나아지고, 주변 세상에 반응한대요.",
                 highlight=["a developing city"], button="다음 문장",
                 tips=[tip("note", "동사로 '주목하다, 눈여겨보다'예요. 공책(노트)이 아니에요.", "note", trap=True)]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "low",
        "glosses": [g("Observe", "관찰하라"), g("its truck stops", "트럭 정류장"), g("crafts", "공들여 만들다"),
                    g("its immigration policies", "이민 정책"), g("modifies", "수정하다"), g("its education and legal systems", "교육·법률 제도")],
        "slashes": ["Observe", "its truck stops,", "immigration policies,"],
        "roles": [r("Observe", "V"), r("the city", "S"), r("builds", "V"), r("its truck stops", "O"), r("it … it", "S"), r("crafts", "V"),
                  r("modifies", "V")],
        "steps": [
            show("s6_skim", "트럭 정류장, 이민 정책, 교육·법률 제도 — 도시가 바뀌는 예시들이에요. 깊게 안 읽어도 돼요.",
                 highlight=["modifies"], button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("A city", "도시는"), g("is always changing", "늘 변하고 있다")],
        "roles": [r("A city", "S"), r("is always changing", "V")],
        "steps": [
            show("s7_change", "도시는 늘 변하고 있대요. 뇌도 그렇다는 말이에요.",
                 panel=board(L2, R7, fresh=("always changing",)), highlight=["always changing"], button="다음 문장"),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("A city", "도시는"), g("is not designed", "설계되지 않는다"), g("by urban planners", "도시 계획가들에 의해"),
                    g("and then immobilized", "그리고 나서 고정되다"), g("immobilized", "움직이지 못하게 된, 고정된"), g("like a plastic object", "플라스틱 물건처럼")],
        "slashes": ["is not designed", "urban planners"],
        "roles": [r("A city", "S"), r("is not designed", "V"), r("immobilized", "V")],
        "steps": [
            choice("s8_fixed",
                   "도시는 설계된 뒤 플라스틱 물건처럼 고정될까요?",
                   [("o0", "그렇다, 한 번 설계하면 고정된다", False), ("o1", "아니다, 고정되지 않는다", True)],
                   "문장 앞 'is not'을 봐요. immobilized는 '움직이지 못하게 된, 고정된'이에요.",
                   why="'is not designed … and then immobilized like a plastic object', 설계된 뒤 플라스틱처럼 고정되지 않는대요.",
                   highlight=["is not designed", "immobilized"],
                   tips=[tip("im- + mobile", "im-은 '아님'이에요. mobile(움직이는) → immobile(움직이지 않는) → immobilize(고정시키다).", "immobilized")],
                   panel=board(L2 + [("a plastic object", "플라스틱 물건")], R7, fresh=("a plastic object",))),
        ],
    },
    {
        "id": 9, "text": S[8], "model_translation": KO[8], "teaching_value": "medium",
        "glosses": [g("It", "그것(도시)"), g("continually develops", "계속 발전한다")],
        "roles": [r("It", "S"), r("continually develops", "V")],
        "steps": [
            show("s9_develop", "도시는 계속 발전한대요. 오른쪽에 쌓아 둘게요.",
                 panel=board(L2 + [("a plastic object", "플라스틱 물건")], R9, fresh=("not immobilized", "continually develops")),
                 highlight=["continually develops"], button="다음 문장"),
        ],
    },
    {
        "id": 10, "text": S[9], "model_translation": KO[9], "teaching_value": "high",
        "glosses": [g("Just like cities", "도시와 꼭 마찬가지로"), g("brains", "뇌는"), g("never reach", "결코 도달하지 않는다"),
                    g("an end point", "끝나는 지점")],
        "slashes": ["Just like cities,"],
        "roles": [r("brains", "S"), r("never reach", "V"), r("an end point", "O")],
        "steps": [
            choice("s10_end",
                   "Just like cities(도시처럼), 뇌는 어떻대요?",
                   [("o0", "언젠가 완성된다", False), ("o1", "도시처럼 계획가가 설계한다", False),
                    ("o2", "끝점에 도달하지 않고 계속 바뀐다", True)],
                   "'never reach an end point'를 봐요. never는 '결코 ~ 않다'예요.",
                   why="'brains never reach an end point', 뇌는 결코 끝점에 이르지 않아요. 도시처럼 계속 바뀐다는 거예요.",
                   highlight=["Just like cities", "never reach an end point"],
                   panel=board(L2 + [("a plastic object", "플라스틱 물건")], R10, fresh=("never reach an end point",))),
        ],
    },
    {
        "id": 11, "text": S[10], "model_translation": KO[10], "teaching_value": "low",
        "glosses": [g("We spend our lives", "우리는 평생을 보낸다"), g("blossoming toward something", "무언가를 향해 피어나며"),
                    g("even as", "~할 때조차"), g("the target moves", "목표가 움직이다")],
        "slashes": ["our lives", "toward something,"],
        "roles": [r("We", "S"), r("spend", "V"), r("our lives", "O"), r("the target", "S"), r("moves", "V")],
        "steps": [
            show("s11_bloom", "목표가 움직여도 우리는 평생 무언가를 향해 피어나며 산대요. 끝없이 자라는 모습이에요.",
                 highlight=["blossoming", "the target moves"], button="다음 문장"),
        ],
    },
    {
        "id": 12, "text": S[11], "model_translation": KO[11], "teaching_value": "low",
        "glosses": [g("Consider", "생각해 보라"), g("the feeling", "느낌"), g("encountering a diary", "일기를 우연히 발견하는 것"),
                    g("that you wrote", "네가 쓴"), g("many years ago", "여러 해 전에")],
        "slashes": ["the feeling", "a diary"],
        "roles": [r("Consider", "V"), r("the feeling", "O")],
        "modifiers": ["that you wrote many years ago"],
        "steps": [
            show("s12_diary", "몇 년 전에 쓴 일기를 우연히 발견했을 때의 느낌을 떠올려 보래요. 또 다른 예가 시작돼요.",
                 highlight=["a diary"], button="다음 문장"),
        ],
    },
    {
        "id": 13, "text": S[12], "model_translation": KO[12], "teaching_value": "high",
        "glosses": [g("It", "그것(일기)"), g("represents", "나타낸다"), g("the thinking, opinions, and viewpoint", "생각, 의견, 관점"),
                    g("of someone", "누군가의"), g("who was a bit different", "조금 달랐던"), g("from who you are now", "지금의 너와"),
                    g("that previous person", "그 이전의 사람"), g("can sometimes border on", "때때로 거의 ~에 가까울 수 있다"),
                    g("the unrecognizable", "알아볼 수 없는 것")],
        "slashes": ["It represents", "and viewpoint", "of someone", "a bit different", "who you are now,", "previous person"],
        "roles": [r("It", "S"), r("represents", "V"), r("the thinking, opinions, and viewpoint", "O"), r("that previous person", "S"),
                  r("can sometimes border on", "V")],
        "modifiers": ["who was a bit different from who you are now"],
        "steps": [
            choice("s13_diary",
                   "그 일기를 쓴 예전의 나는 지금의 나와 어떻대요?",
                   [("o0", "조금 달라서, 때로는 거의 못 알아볼 정도다", True), ("o1", "완전히 똑같다", False), ("o2", "아예 다른 사람이 쓴 것이다", False)],
                   "'a bit different from who you are now'와 'border on the unrecognizable'을 봐요.",
                   why="'a bit different from who you are now', 지금의 나와 조금 다르고, 'border on the unrecognizable', 때로는 거의 못 알아볼 정도래요.",
                   highlight=["a bit different", "border on the unrecognizable"],
                   tips=[tip("border on", "'거의 ~에 가깝다'예요. border on the unrecognizable = 거의 못 알아볼 정도다.", "border on")]),
        ],
    },
    {
        "id": 14, "text": S[13], "model_translation": KO[13], "teaching_value": "medium",
        "glosses": [g("Despite", "~에도 불구하고"), g("having the same name", "같은 이름을 가진 것"), g("the same early history", "같은 어린 시절"),
                    g("in the years", "세월 동안"), g("between inscription and interpretation", "쓴 때와 읽는 때 사이에"),
                    g("the narrator", "화자, 이야기하는 사람"), g("has altered", "달라졌다")],
        "slashes": ["the same name", "early history,", "in the years", "inscription and interpretation"],
        "roles": [r("the narrator", "S"), r("has altered", "V")],
        "steps": [
            show("s14_alter", "이름과 어린 시절이 같아도, 쓴 때와 읽는 때 사이에 화자(나)가 달라졌대요.",
                 highlight=["Despite", "has altered"],
                 panel=board(L2 + [("a plastic object", "플라스틱 물건")], R14, fresh=("the narrator has altered",)), button="다음 문장"),
        ],
    },
    {
        "id": 15, "text": S[14], "model_translation": KO[14], "teaching_value": "high",
        "glosses": [g("The word “plastic”", "'플라스틱'이라는 단어"), g("can be stretched", "넓혀질 수 있다"), g("to fit", "~에 맞도록"),
                    g("this notion", "이 개념"), g("of ongoing change", "계속되는 변화의")],
        "slashes": ["can be stretched", "this notion"],
        "roles": [r("The word “plastic”", "S"), r("can be stretched", "V")],
        "steps": [
            choice("s15_stretch",
                   "글쓴이는 plastic이라는 말을 이제 어떤 뜻에 맞게 넓혀 쓰자고 할까요?",
                   [("o0", "한 번 정해진 모양", False), ("o1", "계속되는 변화", True), ("o2", "플라스틱 장난감", False)],
                   "'to fit this notion of ongoing change'를 봐요. ongoing은 '계속되는, 진행 중인'이에요.",
                   why="'this notion of ongoing change', ongoing(계속되는) change(변화)라는 개념에 맞게 plastic의 뜻을 넓히자는 거예요.",
                   highlight=["ongoing change"],
                   panel=board(L2 + [("a plastic object", "플라스틱 물건")], R15, fresh=("ongoing change",)),
                   point="글쓴이 주장 = 뇌는 '한 번 성형하면 그대로'가 아니라 평생 계속 변한다 (ongoing change)"),
            show("s15_summary", "이제 요약문을 읽어요. (A)와 (B)가 칠판의 어느 쪽 말인지 보고 고르면 돼요.", button="요약문 읽어 볼게요"),
        ],
    },
    {
        "id": 16, "label": "요약문", "text": SUMMARY, "teaching_value": "high",
        "model_translation": KO[15],
        "glosses": [g("While", "~인 반면"), g("some understand", "어떤 사람들은 이해한다"), g("brain plasticity", "뇌 가소성"),
                    g("to mean", "~을 뜻한다고"), g("upon molding", "성형되자마자"), g("the brain", "뇌는"),
                    g("is actually capable of", "실제로는 ~할 수 있다")],
        "slashes": ["While some understand", "“brain plasticity”", "upon molding,", "is actually capable"],
        "roles": [r("some", "S"), r("understand", "V"), r("the brain", "S"), r("is", "V"), r("capable", "C")],
        "steps": [
            choice("s16_a_side",
                   "어떤 사람들은 brain plasticity가 '성형되자마자(upon molding) (A)'를 뜻한다고 이해한대요. (A)는 칠판 어느 쪽 말일까요?",
                   [("o0", WORD, True), ("o1", REAL, False)],
                   "While(~인 반면) 앞뒤는 반대예요. 뒤가 '뇌가 실제로(actually)'니까, 앞은 그와 다른 쪽이에요.",
                   why="While 앞은 '어떤 사람들이 이해하는 뜻', 뒤는 '뇌가 실제로 하는 일'이에요. (A)는 plastic이라는 말의 느낌 쪽이에요.",
                   highlight=["While", "some understand", "upon molding"],
                   panel=board(L2 + [("a plastic object", "플라스틱 물건")], R15),
                   tips=[tip("While (대조)", "문장 앞 While은 '~인 반면'이에요. 앞과 뒤가 반대 내용이에요.", "While")]),
            choice("s16_a",
                   "그럼 (A)에는 어떤 뜻의 말이 와야 할까요?",
                   [("o0", "부드럽게 잘 휨", False), ("o1", "변하지 않고 그대로임", True), ("o2", "이리저리 움직임", False)],
                   "칠판 왼쪽 'mold once, keep it that way forever, never change it again'을 떠올려 봐요.",
                   why="왼쪽은 한 번 성형하면 영원히 그대로, 다시는 안 바뀐다는 말이에요. (A)는 그 뜻, 변하지 않음이에요.",
                   highlight=["(A) ________"],
                   point="(A) = 성형되자마자 영원히 그대로 → '변하지 않음(영속성)'"),
            choice("s16_b",
                   "(B)는 '뇌가 실제로 할 수 있는 것'이에요. 어떤 뜻의 말이 와야 할까요?",
                   [("o0", "계속 바뀌는 것(변화)", True), ("o1", "남에게 공감하는 것", False), ("o2", "원래대로 되돌아가는 것", False)],
                   "칠판 오른쪽 'remolding, always changing, ongoing change'를 떠올려 봐요.",
                   why="오른쪽은 평생 다시 성형하고, 늘 변하고, 계속 변한다는 말이에요. (B)는 그 뜻, 변화예요.",
                   highlight=["(B) ________"],
                   point="(B) = 뇌가 실제로 하는 일 = 평생 계속되는 변화"),
            show("s16_go", "(A)와 (B)의 뜻을 둘 다 맞게 담은 보기를 골라 봐요. 한쪽만 맞으면 오답이에요.", button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 1, [m("Brain plasticity", "뇌 가소성은"), " ", m("in neuroscience", "신경 과학에서"), " ", m("we use", "우리가 쓰는"), " ",
                         m("is a term", "용어이다"), "."],
          sv_new=sv_step("s1_basic_sv", ["Brain plasticity", "is", "a term", "neuroscience"], {"Brain plasticity": "S", "is": "V", "a term": "C"},
                         {"neuroscience": "그건 in 뒤 덩어리예요."}, "주어는 “Brain plasticity”, 동사는 is, 보어는 a term이에요."),
          meaning_ids=["s1_term"])
add_basic(sentences, 3, [m("But", "하지만"), " ", m("that’s not", "그것은 ~이 아니다"), " ", m("what the brain does", "뇌가 하는 일"), "."],
          sv_new=sv_step("s3_basic_sv", ["that", "’s", "not", "what the brain does"], {"that": "S", "’s": "V", "what the brain does": "C"},
                         {"not": "그건 '~이 아니다', 동사 뒤에 붙은 부정어예요."},
                         "that’s = that is예요. 주어 that, 동사 ’s(is), not 뒤 what the brain does(뇌가 하는 일)가 보어 덩어리예요.",
                         ask="that’s는 that is를 줄인 말이에요. 주어(S)·동사(V)·보어(C)를 찾아볼까요?"),
          meaning_after="s3_but")
add_basic(sentences, 4, [m("It", "그것(뇌)은"), " ", m("throughout your life", "평생 동안"), " ", m("remolding itself", "스스로를 다시 성형하기"), "를 ",
                         m("carries on", "계속한다"), "."],
          sv_new=sv_step("s4_basic_sv", ["It", "carries on", "remolding itself", "your life"], {"It": "S", "carries on": "V", "remolding itself": "O"},
                         {"your life": "그건 throughout 뒤 덩어리예요."}, "주어는 It(뇌), 동사는 carries on, 목적어는 remolding itself예요."),
          meaning_ids=["s4_remold"])
add_basic(sentences, 7, [m("A city", "도시는"), " ", m("is always changing", "늘 변하고 있다"), "."],
          sv_new=sv_step("s7_basic_sv", ["A city", "is always changing"], {"A city": "S", "is always changing": "V"}, {},
                         "주어는 A city, 동사는 is (always) changing이에요."),
          meaning_ids=["s7_change"])
add_basic(sentences, 8, [m("A city", "도시는"), " ", m("by urban planners", "도시 계획가들에 의해"), " ", m("is not designed", "설계되고"), " ",
                         m("and then immobilized", "그다음 고정되지"), " 않는다 — ", m("like a plastic object", "플라스틱 물건처럼"), "."],
          sv_new=sv_step("s8_basic_sv", ["A city", "is not designed", "urban planners", "immobilized"], {"A city": "S", "is not designed": "V", "immobilized": "V"},
                         {"urban planners": "그건 by 뒤, 누가 설계하는지예요."},
                         "주어는 A city, 동사는 is not designed와 (is not) immobilized예요."),
          meaning_after="s8_fixed")
add_basic(sentences, 10, [m("Just like cities", "도시와 마찬가지로"), ", ", m("brains", "뇌는"), " ", m("an end point", "끝나는 지점"), "에 ", m("never reach", "결코 도달하지 않는다"), "."],
          sv_new=sv_step("s10_basic_sv", ["cities", "brains", "never reach", "an end point"], {"brains": "S", "never reach": "V", "an end point": "O"},
                         {"cities": "그건 Just like(~처럼) 뒤 덩어리예요."}, "주어는 brains, 동사는 never reach, 목적어는 an end point예요."),
          meaning_after="s10_end")
add_basic(sentences, 15, [m("The word “plastic”", "'플라스틱'이라는 단어는"), " ", m("of ongoing change", "계속되는 변화의"), " ", m("this notion", "이 개념"), "에 ",
                          m("to fit", "맞도록"), " ", m("can be stretched", "넓혀질 수 있다"), "."],
          sv_new=sv_step("s15_basic_sv", ["The word “plastic”", "can be stretched", "this notion"], {"The word “plastic”": "S", "can be stretched": "V"},
                         {"this notion": "그건 to fit(~에 맞도록) 뒤의 말이에요."}, "주어는 The word “plastic”, 동사는 can be stretched예요."),
          meaning_after="s15_stretch")

SENSES = {
    2: [sense("that", "suggests that the key idea", "~라는 것을", "명사절 that (suggest that …)"),
        sense("to", "to mold something", "~하는 것", "to부정사 (보어: ~하는 것)"),
        sense("that", "keep it that way", "그", "지시형용사 that + 명사 (that way = 그대로)"),
        sense("to", "to shape the plastic toy", "~하는 것", "to부정사 (콜론 뒤 풀이)")],
    3: [sense("but", "But that’s not", "하지만", "접속사 but (문장 앞)"), sense("that", "that’s not", "그것", "지시대명사 that (앞 내용)")],
    5: [sense("to", "responds to the world", "~에 (반응하다)", "respond to + 명사")],
    11: [sense("as", "even as the target moves", "~할 때조차", "even as + 주어·동사")],
    12: [sense("that", "a diary that you wrote", "(앞 명사를 꾸밈)", "관계대명사 that + 주어·동사")],
    13: [sense("that", "that previous person", "그", "지시형용사 that + 명사")],
    15: [sense("to", "to fit", "~하도록, ~에 맞게", "to부정사 (목적)")],
    16: [sense("while", "While some understand", "~인 반면", "접속사 while (대조)"),
         sense("to", "to mean", "~을 뜻한다고", "understand A to mean B = A가 B를 뜻한다고 이해하다")],
}

WORDS = {"keep": "유지하다", "again": "다시", "sometimes": "때때로", "brain": "뇌", "plasticity": "가소성", "term": "용어", "neuroscience": "신경 과학", "whether": "~이든", "intentionally": "의도적으로",
         "suggests": "암시하다", "key": "핵심의", "idea": "개념", "mold": "성형하다, 모양을 만들다", "once": "한 번", "forever": "영원히",
         "shape": "모양을 만들다", "plastic": "플라스틱", "toy": "장난감", "change": "바꾸다", "carries": "계속하다 · carry on",
         "remolding": "다시 성형하는 것", "itself": "그 자체", "throughout": "~ 내내", "life": "삶", "think": "생각하다", "developing": "발전하는",
         "city": "도시", "note": "주목하다", "grows": "자라다", "improves": "나아지다", "responds": "반응하다", "world": "세상", "around": "주변의",
         "observe": "관찰하다", "builds": "짓다", "truck": "트럭", "stops": "정류장", "crafts": "공들여 만들다", "immigration": "이민",
         "policies": "정책", "modifies": "수정하다", "education": "교육", "legal": "법률의", "systems": "제도", "always": "늘",
         "changing": "변하는", "designed": "설계된", "urban": "도시의", "planners": "계획가들", "immobilized": "고정된", "object": "물건",
         "continually": "계속", "develops": "발전하다", "cities": "도시들", "brains": "뇌들", "reach": "도달하다", "end": "끝", "point": "지점",
         "spend": "보내다", "lives": "삶", "blossoming": "피어나는", "toward": "~을 향해", "target": "목표", "moves": "움직이다",
         "consider": "생각해 보다", "feeling": "느낌", "encountering": "우연히 만나는 것", "diary": "일기", "wrote": "썼다", "years": "년",
         "ago": "전에", "represents": "나타내다", "thinking": "생각", "opinions": "의견", "viewpoint": "관점", "bit": "조금",
         "different": "다른", "previous": "이전의", "border": "경계 · border on = 거의 ~에 가깝다", "unrecognizable": "알아볼 수 없는",
         "despite": "~에도 불구하고", "having": "가지고 있는 것", "name": "이름", "early": "어린 시절의", "history": "역사",
         "inscription": "새겨진 글(쓴 것)", "interpretation": "해석(읽는 것)", "narrator": "화자", "altered": "달라진", "word": "단어",
         "stretched": "넓혀진", "fit": "맞다", "notion": "개념", "ongoing": "계속되는", "understand": "이해하다", "mean": "뜻하다",
         "molding": "성형", "actually": "실제로", "capable": "~할 수 있는", "use": "쓰다", "never": "결코 ~ 않다", "someone": "누군가",
         "that’s": "그것은 ~이다", "way": "방식, 상태", "a": "하나의"}

STORIES = [
    (4, [sc("문장 1~2", "🧸", "plasticity → mold once, keep forever", "plastic이라는 말은 한 번 만들고 영원히 그대로라는 느낌을 줘요"),
         sc("문장 3~4", "🧠", "remolding itself", "하지만 뇌는 평생 스스로를 다시 만들어요")]),
    (10, [sc("문장 5~9", "🏙️", "a developing city · always changing", "발전하는 도시처럼 — 늘 변하고, 고정되지 않고, 계속 발전해요"),
          sc("문장 10", "♾️", "never reach an end point", "뇌도 끝점에 이르지 않아요")]),
    (15, [sc("문장 11~14", "📔", "a diary · the narrator has altered", "옛 일기 속 나는 지금의 나와 달라요 — 그사이 내가 바뀌었어요"),
          sc("문장 15", "🔁", "ongoing change", "plastic이라는 말을 '계속되는 변화'에 맞게 넓힐 수 있어요")]),
]

OPTIONS = [("1", "permanence ······ transformation", "영속성(변하지 않음) ······ 변화", True),
           ("2", "flexibility ······ sympathizing", "유연성 ······ 공감하기", False),
           ("3", "adaptability ······ restoration", "적응성 ······ 회복", False),
           ("4", "firmness ······ sympathizing", "단단함 ······ 공감하기", False),
           ("5", "mobility ······ transformation", "이동성 ······ 변화", False)]
exam = {
    "question": "다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?",
    "underline": ["(A) ________", "(B) ________"], "sentence": 16, "analysis_first": True, "wrong_rate": 48.3, "wrong_rank": 11,
    "glosses": [g("permanence", "영속성, 변하지 않음"), g("transformation", "변화, 변형"), g("flexibility", "유연성"), g("sympathizing", "공감하기"),
                g("adaptability", "적응성"), g("restoration", "회복, 복원"), g("firmness", "단단함"), g("mobility", "이동성")],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "(A)는 칠판 왼쪽(변하지 않음), (B)는 오른쪽(계속되는 변화)이에요. 둘 다 맞는 보기를 골라 봐요.",
        "정답이에요! 어떤 사람들은 뇌 가소성을 성형되자마자 영원히 그대로(permanence)라고 이해하지만, 뇌는 실제로 평생 변할(transformation) 수 있어요.",
        "정답은 ①이에요. (A) 한 번 성형하면 그대로 = permanence, (B) 계속되는 변화 = transformation이에요.",
        {"2": "flexibility(유연성)는 plastic의 '잘 휘는' 느낌이지만, (A)는 '한 번 만들면 그대로'예요. 공감(sympathizing)도 글에 없어요.",
         "3": "adaptability(적응성)는 오히려 오른쪽 말에 가까워요. restoration(원래대로 되돌림)은 계속 바뀐다는 말과 달라요.",
         "4": "firmness(단단함)는 (A)에 가깝지만, (B)의 공감하기(sympathizing)는 글에 없어요.",
         "5": "(B) transformation은 맞지만, (A) mobility(이동성)는 '영원히 그대로'와 반대예요."},
        {"5": review(14.6,
                     "⑤는 (B) transformation은 맞아요. 그런데 (A) mobility(이동성, 움직임)는 '성형되자마자 영원히 그대로'와 반대예요. (A)에는 변하지 않음(permanence)이 와야 해요.",
                     panel=rows(("(A)", "mold once · keep it that way forever", "변하지 않음 = permanence", "hl"),
                                ("(B)", "remolding · always changing · ongoing change", "변화 = transformation", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 40번 (요약문 완성, 2점)",
    topic="요약문 푸는 법: 지문을 먼저 읽으며 두 쪽 말을 칠판에 모으기 → 요약문 (A)(B)가 각각 어느 쪽인지 → 그 뜻의 말 고르기",
    method={"type": "summary", "labels": ["지문 먼저 읽기", "두 쪽 말 모으기", "(A)(B) 맞추기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-brain-plastic.svg", ("Plastic toy", "플라스틱 장난감"), "↔", ("Brain", "뇌"),
                                       "뇌는 한 번 모양이 잡히면 그대로일까?", "2024년 3월 40번 도입 칠판"),
                      "alt": "칠판: Plastic toy(플라스틱 장난감) ↔ Brain(뇌)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "뇌는 한 번 모양이 잡히면 평생 그대로일까요? 이번 글은 '뇌 가소성'이라는 말의 진짜 뜻을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "요약문 문제는 지문을 먼저 읽으며 글쓴이 주장을 잡아요. 같은 쪽 말을 칠판에 모아 둘 거예요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "마지막에 요약문을 읽고, (A)와 (B)가 칠판의 어느 쪽 말인지 보고 골라요."}}],
    exam=exam,
    key_words={"passage": [g("plasticity", "가소성"), g("neuroscience", "신경 과학"), g("intentionally", "의도적으로"), g("suggest", "암시하다"),
                           g("carry on", "계속하다"), g("remold", "다시 성형하다"), g("respond to", "~에 반응하다"), g("modify", "수정하다"),
                           g("immobilize", "고정시키다"), g("continually", "계속해서"), g("blossom", "피어나다, 번성하다"), g("encounter", "우연히 만나다"),
                           g("viewpoint", "관점"), g("border on", "거의 ~에 가깝다"), g("narrator", "화자"), g("alter", "바뀌다"),
                           g("notion", "개념"), g("ongoing", "계속되는")],
               "options": [g("permanence", "영속성"), g("transformation", "변화"), g("flexibility", "유연성"), g("adaptability", "적응성"),
                           g("restoration", "회복"), g("mobility", "이동성")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# term 용어 · crafts 공들여 만들다.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    1: [tip("term", "이 글에서는 → 용어  ('학기' 아님)", "term", trap=True)],
    6: [tip("crafts", "이 글에서는 → 공들여 만들다  ('공예(품)' 아님)", "crafts", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="요약문 푸는 법",
       chunks={"Brain plasticity": "뇌 가소성", "is": "~이다", "a term": "용어", "neuroscience": "신경 과학",
               "Whether intentionally or not": "의도했든 아니든", "plasticity": "가소성", "suggests": "암시하다", "the key idea": "핵심 개념",
               "that’s": "그것은 ~이다", "not": "~이 아니다", "the brain": "뇌", "does": "하다", "It": "그것", "carries on": "계속하다",
               "remolding itself": "스스로를 다시 성형하는 것", "your life": "너의 삶", "A city": "도시는", "is always changing": "늘 변하고 있다",
               "is not designed": "설계되지 않는다", "urban planners": "도시 계획가들", "immobilized": "고정된", "cities": "도시들",
               "brains": "뇌는", "never reach": "결코 도달하지 않는다", "an end point": "끝나는 지점", "The word “plastic”": "'플라스틱'이라는 단어",
               "can be stretched": "넓혀질 수 있다", "this notion": "이 개념", "we use": "우리가 쓰는", "in neuroscience": "신경 과학에서",
               "But": "하지만", "that’s not": "그것은 ~이 아니다", "what the brain does": "뇌가 하는 일", "throughout your life": "평생 동안",
               "by urban planners": "도시 계획가들에 의해", "and then immobilized": "그리고 나서 고정되다", "like a plastic object": "플라스틱 물건처럼",
               "Just like cities": "도시와 마찬가지로", "of ongoing change": "계속되는 변화의", "to fit": "~에 맞도록"})
