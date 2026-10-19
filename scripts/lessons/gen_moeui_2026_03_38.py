"""2026년 3월 38번 레슨 + 대사를 만든다 (주어진 문장 넣기, 3점).

레슨 JSON(content/tutor/policy-lessons/…)과 대사(content/tutor/policy-copy/dajung/…)는 이 스크립트의
생성물이다. 고칠 때는 여기를 고치고 다시 돌린 뒤 도장을 찍는다:

    python3 scripts/lessons/gen_moeui_2026_03_38.py
    npm run policy:copy stamp moeui-2026-03-38-gesture-glue

39번과 같은 유형 — 푸는 법도 같다: 주어진 문장 단서 → 앞 내용 예측 → 흐름 끊기는 곳. Claude 초안.
정답 ③. 많이 고른 오답 ④ 34.1% (정답 37.7%와 거의 같다) — 'Instead, it offers glue' 뒤에 넣은 학생이 많다.
그러면 Instead의 it이 바로 앞 문장의 language가 되어 말이 안 된다.
"""
import sys
import copy
import json
import os

ID = "moeui-2026-03-38-gesture-glue"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def g(en, ko):
    return {"en": en, "ko": ko}


def choice(id, ask, options, hint, praise="맞아요!", method=0, why=None, **extra):
    """why: 틀렸을 때 「아쉽게도 틀렸어요.」 뒤의 이유 (없으면 힌트)"""
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


def show(id, say, method=0, button="다음 문장", point=None, **extra):
    brief = {"say": say, **({"point": point} if point else {})}
    return {"id": id, "type": "show", "interaction": "note", "brief": brief, "method": method, "button": button, **extra}


def pick(id, ask, candidates, answers, wrong, explain, praise="맞아요!", shade=False, method=0, **extra):
    brief = {"ask": ask, "wrong": wrong, "more": "좋아요! {n}개 남았어요.", "praise": praise, "explain": explain}
    if id in POINTS:
        brief["point"] = POINTS[id]
    return {"id": id, "type": "pick", "interaction": "word_pick", **({"shade": True} if shade else {}),
            "candidates": candidates, "answers": answers, "brief": brief, "method": method, **extra}


POINTS = {
    "g_clue": "주어진 문장의 단서 = such choices (그러한 선택들) → 앞에 '선택' 이야기가 있어야",
    "g_before": "주어진 문장 앞 = 언어가 화자에게 선택을 하게 한다는 내용",
    "g_after": "주어진 문장 뒤 = 제스처가 선택 대신 하는 일 (Instead, it offers …)",
    "s1_what": "제스처는 말과 동시에 체계적으로 만들어진다 → co-expressive(함께 표현하는)",
    "s2_cat": "categorical(범주적) = 언어 쪽",
    "s2_img": "imagistic(심상적, 그림 같은) = 제스처 쪽",
    "s3_choice": "언어는 화자에게 완료인지 진행인지 고르게 한다 (must decide)",
    "s5_it": "Instead, it offers glue의 it = 제스처 (언어 요소를 묶어 주는 접착제)",
    "s5_need": "Instead, it(제스처)이 나오려면 바로 앞에 제스처 이야기가 있어야 한다",
    "s6_rel": "speech and gesture are not redundant nor … a translation = 말과 제스처는 중복도 번역도 아니다",
    "s7_unit": "생각을 표현하는 최소 단위 = 말과 제스처의 결합 (imagistic-categorial)",
}

GIVEN = "According to McNeil and Duncan, gesture is different from language in that it does not present the speaker with such choices."
S = [
    "Scholars have demonstrated that the gestures hearing people produce while they are speaking are systematically made at the same time with speech such that language and gesture must be considered “co-expressive”.",
    "This tightly integrated pairing of language and gesture enables speakers to conceptualize and formulate their thoughts in terms of both the “categorical” requirements of language, and the “imagistic” possibilities of gesture.",
    "(①) For example, in describing an event, one must decide if the event has been completed or is ongoing if the language being spoken at that moment has a verbal affix for each meaning and one or the other must be chosen.",
    "(②) This kind of choice is characteristic of language as a semiotic system.",
    "(③) Instead, it offers a kind of glue, which helps unite linguistic elements in a larger semiotic expression, which, as a whole, shares important characteristics with the represented objects.",
    "(④) In this view, speech and gesture are not redundant nor is one a “translation” of the other.",
    "(⑤) Rather, the minimal processing unit for the expression of thought is a combination of the two: it is “imagistic-categorial” in nature.",
]
KO = [
    "학자들은 들을 수 있는 사람이 말하는 동안 보여 주는 제스처가, 언어와 제스처를 반드시 '공동 표현적'이라고 간주해야 할 만큼, 말과 동시에 체계적으로 만들어진다는 것을 입증해 왔다.",
    "이러한 언어와 제스처의 단단히 결합된 한 쌍은 화자가 언어의 '범주적' 요구와 제스처의 '심상적' 가능성 두 관점 모두에서 자기 생각을 개념화하고 명확하게 말할 수 있게 한다.",
    "예를 들어, 어떤 사건을 묘사할 때, 만약 그 순간에 말해지고 있는 언어가 각 의미에 대한 동사에 붙는 접사를 가지고 있고 둘 중 하나를 반드시 선택해야 한다면, 화자는 그 사건이 완료되었는지 또는 진행 중인지를 반드시 결정해야 한다.",
    "이러한 종류의 선택은 기호 체계로서 언어의 특징이다.",
    "대신에, 그것은 일종의 접착제를 제공하는데, 그것은 언어적 요소들을 더 큰 기호 표현 안에서 결합하도록 돕고, 그것은, 전체로서, 표현된 대상과 중요한 특징을 공유한다.",
    "이러한 관점에서, 말과 제스처는 중복되는 것이 아니며 어느 하나가 다른 하나의 '번역'도 아니다.",
    "오히려, 사고 표현을 위한 최소 처리 단위는 이 둘의 결합이며, 그것은 본질적으로 '심상적-범주적'이다.",
]

LANG = "왼쪽 · 언어"
GEST = "오른쪽 · 제스처"


def board(left, right, caption=None, fresh=(), between="≠"):
    # 둘은 다르다(≠) → 끝에서 둘의 조합(+) — 글의 흐름을 기호로 (2026-10-16 선생님)
    p = {"kind": "groups", "title": "언어와 제스처", "between": between,
         "left": {"label": "언어 (language)", "words": [{"text": w, **({"fresh": True} if w in fresh else {})} for w in left]},
         "right": {"label": "제스처 (gesture)", "words": [{"text": w, **({"fresh": True} if w in fresh else {})} for w in right]}}
    if caption:
        p["caption"] = caption
    return p


sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN,
        "model_translation": "McNeil과 Duncan에 따르면, 제스처는 화자에게 그러한 선택을 제시하지 않는다는 점에서 언어와 다르다.",
        "teaching_value": "high",
        "glosses": [g("According to McNeil and Duncan", "McNeil과 Duncan에 따르면"), g("gesture", "제스처, 몸짓"),
                    g("is different from language", "언어와 다르다"), g("in that", "~라는 점에서"),
                    g("does not present", "제시하지 않다"), g("the speaker", "말하는 사람, 화자"), g("such choices", "그러한 선택들")],
        "steps": [
            # 단서부터 찾게 하면 뜬금없다 — 주어진 문장이 어떤 상황인지 먼저 (2026-10-16 선생님). 중·초는 그 앞에 해석 맞추기
            show("g_situation",
                 "주어진 문장은 제스처가 언어와 어떻게 다른지 말해요. 제스처는 말하는 사람에게 그런 선택을 주지 않는대요.",
                 button="다음",
                 highlight=["gesture", "is different from language", "does not present"],
                 panel={"kind": "structure", "rows": [
                     {"label": "누구 말", "text": "McNeil and Duncan", "ko": "두 학자에 따르면"},
                     {"label": "무엇이", "text": "gesture ≠ language", "ko": "제스처는 언어와 다르다", "tone": "hl"},
                     {"label": "어떤 점에서", "text": "does not present the speaker with such choices", "ko": "화자에게 그런 선택을 주지 않는다", "tone": "hl2"},
                 ]},
                 method=0),
            # 「이어지는 단서」가 아니라 앞 내용을 가리키는 말(지시어) 찾기
            pick("g_clue", "주어진 문장에 앞 내용을 가리키는 말이 하나 있어요. 찾아볼까요?",
                 ["According to McNeil and Duncan", "is different from language", "the speaker", "such choices"],
                 ["such choices"],
                 "그건 이 문장 안에서 뜻이 끝나는 말이에요. 앞에서 말한 걸 다시 가리키는 말을 찾아봐요.",
                 "'such choices(그러한 선택들)'예요. such는 앞에서 말한 걸 가리키니, 앞에 '선택' 이야기가 있어야 해요.",
                 praise="맞아요! such(그러한)처럼 앞 내용을 가리키는 말은 문장 넣기·순서 문제에서 주의 깊게 보면 좋아요.",
                 shade=True,
                 tips=[{"label": "in that", "mark": "in that", "text": "'~라는 점에서'예요. 뒤에 다른 점이 무엇인지 나와요."}],
                 # 찾기 전에 보이면 이르다 — 맞힌 화면에서만 (2026-10-16 선생님)
                 praise_tips=[{"label": "앞을 가리키는 말", "text": "this, that, such, these, the처럼 앞에 나온 것을 다시 가리키는 말이에요. 문장 넣기에서는 이 말이 가리키는 게 바로 앞 문장에 있어야 해요."}],
                 method=0),
            # 바로 「앞에 무엇?」을 물으면 와닿지 않는다 — 언어/제스처 두 그룹에 choices부터 나눠 보게 (2026-10-16 선생님)
            choice("g_sort",
                   "언어와 제스처를 두 그룹으로 나눠 봐요. 제스처는 그러한 선택을 주지 않는다는 점에서 언어와 다르대요. 그럼 choice는 어디 들어가야 할까요?",
                   [("o0", LANG, True), ("o1", GEST, False)],
                   "제스처는 선택을 주지 않는다(does not present)고 했어요. 그럼 선택을 주는 건 다른 쪽이에요.",
                   panel={**board([], []), "sort": {"words": ["choice"], "left": LANG, "right": GEST}},
                   highlight=["gesture", "does not present", "such choices"], method=1),
            choice("g_before",
                   "그럼 주어진 문장 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "제스처가 접착제 역할을 한다는 내용", False), ("o1", "언어가 화자에게 선택을 하게 한다는 내용", True),
                    ("o2", "말과 제스처가 중복된다는 내용", False)],
                   "such choices는 앞에 나온 '선택'을 받아요. 제스처는 그런 선택을 주지 않는대요.",
                   why="such choices는 앞에서 말한 선택이에요. 제스처는 선택을 주지 않는다고 했으니, 앞에는 선택을 주는 쪽 이야기가 와야 해요.",
                   panel=board(["choice"], [], fresh=("choice",)), method=1),
            choice("g_after",
                   "주어진 문장 바로 뒤에는 무엇이 오면 자연스러울까요?",
                   [("o0", "또 다른 언어의 선택 예시", False), ("o1", "McNeil이 누구인지 소개", False),
                    ("o2", "제스처가 선택 대신 하는 일", True)],
                   "제스처는 선택을 주지 않는대요. 그럼 대신 무엇을 하는지가 궁금해지죠.",
                   method=1),
        ],
    },
    {
        "id": 2, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("Scholars", "학자들"), g("have demonstrated", "입증해 왔다"), g("the gestures", "제스처들"),
                    g("hearing people", "들을 수 있는 사람들, 청인"), g("produce", "만들어 내다"), g("while they are speaking", "말하는 동안"),
                    g("systematically", "체계적으로"), g("at the same time with speech", "말과 동시에"),
                    g("such that", "~할 만큼"), g("co-expressive", "함께 표현하는")],
        "steps": [
            choice("s1_what",
                   "학자들이 입증한 건 무엇일까요?",
                   [("o0", "제스처는 말과 상관없이 나온다", False), ("o1", "제스처는 말보다 먼저 나온다", False),
                    ("o2", "제스처는 말과 동시에 만들어진다", True)],
                   "'at the same time with speech'를 봐요.",
                   why="'systematically made at the same time with speech', 말과 동시에 체계적으로 만들어진대요. 그래서 둘이 함께 표현한대요(co-expressive).",
                   highlight=["at the same time"],
                   tips=[{"label": "hearing people", "mark": "hearing people",
                          "text": "여기서 hearing은 '듣는 중인'이 아니라 '들을 수 있는'이에요. hearing people은 청각 장애가 없는 사람, 청인이에요."}],
                   method=1),
        ],
    },
    {
        "id": 3, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("This tightly integrated pairing", "이렇게 단단히 결합된 한 쌍"), g("enables", "~할 수 있게 하다"),
                    g("conceptualize", "개념화하다"), g("formulate", "명확하게 말하다"), g("in terms of", "~의 관점에서"),
                    g("categorical", "범주적인 · 딱 나눠 정하는"), g("requirements", "요구"),
                    g("imagistic", "심상적인 · 그림 같은"), g("possibilities", "가능성")],
        "steps": [
            choice("s2_cat",
                   "언어와 제스처를 두 그룹으로 나눠 봐요. 'categorical(범주적)'은 어느 쪽일까요?",
                   [("o0", LANG, True), ("o1", GEST, False)],
                   "'the categorical requirements of language'예요. of 뒤를 봐요.",
                   panel={**board(["choice"], []), "sort": {"words": ["categorical"], "left": LANG, "right": GEST}},
                   highlight=["“categorical” requirements of language"], method=1),
            choice("s2_img",
                   "그럼 'imagistic(심상적, 그림 같은)'은 어느 쪽일까요?",
                   [("o0", LANG, False), ("o1", GEST, True)],
                   "'the imagistic possibilities of gesture'예요. of 뒤를 봐요.",
                   panel={**board(["choice", "categorical"], [], fresh=("categorical",)), "sort": {"words": ["imagistic"], "left": LANG, "right": GEST}},
                   highlight=["“imagistic” possibilities of gesture"], method=1),
        ],
    },
    {
        "id": 4, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        # affix는 시험지 아래 *로 풀어 준 단어
        "glosses": [g("For example", "예를 들어"), g("in describing an event", "어떤 사건을 묘사할 때"),
                    g("one must decide", "화자는 정해야 한다"), g("has been completed", "끝났다, 완료되었다"), g("ongoing", "진행 중인"),
                    g("verbal affix", "동사에 붙는 접사"), g("for each meaning", "각 의미마다"), g("one or the other", "둘 중 하나"),
                    g("must be chosen", "골라야 한다")],
        "steps": [
            choice("s3_choice",
                   "이 예시에서 언어는 화자에게 무엇을 하게 할까요?",
                   [("o0", "사건을 그림으로 그리게 한다", False), ("o1", "완료인지 진행인지 꼭 고르게 한다", True),
                    ("o2", "아무것도 고르지 않게 한다", False)],
                   "'one must decide if the event has been completed or is ongoing'을 봐요.",
                   highlight=["decide", "completed or is ongoing"],
                   method=1),
        ],
    },
    {
        "id": 5, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        # semiotic은 시험지 아래 *로 풀어 준 단어
        "glosses": [g("This kind of choice", "이런 종류의 선택"), g("is characteristic of", "~의 특징이다"),
                    g("language", "언어"), g("as a semiotic system", "기호 체계로서")],
        "steps": [
            # choices는 주어진 문장에서 이미 언어 쪽에 넣었다 — 다시 나누지 않고 맞았다고 확인만
            show("s4_sort",
                 "This kind of choice is characteristic of language — 선택은 언어의 특징이래요. 주어진 문장에서 choice를 언어 쪽에 넣은 게 맞았어요.",
                 button="다음",
                 panel=board(["choice", "categorical"], ["imagistic"], fresh=("choice",)),
                 highlight=["This kind of choice", "language"], method=1),
        ],
    },
    {
        "id": 6, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Instead", "대신에"), g("it offers", "그것은 제공한다"), g("a kind of glue", "일종의 접착제"),
                    g("unite", "결합하다, 묶다"), g("linguistic elements", "언어적 요소"), g("larger", "더 큰"),
                    g("expression", "표현"), g("as a whole", "전체로서"), g("shares", "공유하다"),
                    g("important characteristics", "중요한 특징"), g("the represented objects", "표현된 대상")],
        "steps": [
            choice("s5_it",
                   "'Instead, it offers a kind of glue'의 it은 무엇일까요?",
                   [("o0", "언어 (language)", False), ("o1", "제스처 (gesture)", True), ("o2", "선택 (choice)", False)],
                   "언어 요소들(linguistic elements)을 묶어 주는 접착제예요. 언어가 자기를 묶을 리는 없어요.",
                   why="접착제(glue)처럼 언어 요소들을 묶어 주는 건 언어 바깥의 것이에요. Instead(대신에)는 선택을 주지 않는 쪽이 대신 하는 일이에요.",
                   highlight=["Instead", "glue"], method=1),
            choice("s5_need",
                   "그럼 'Instead, it(제스처)'이 나오려면 바로 앞에 무엇이 있어야 할까요?",
                   [("o0", "언어의 선택 이야기", False), ("o1", "접착제 이야기", False),
                    ("o2", "제스처는 선택을 주지 않는다는 이야기", True)],
                   "it이 제스처를 가리키려면 바로 앞에 제스처가 나와야 해요. Instead는 앞과 반대되는 걸 대신 말할 때 써요.",
                   why="it이 제스처를 가리키려면 바로 앞에 제스처가 나와야 해요. 그리고 Instead(대신에)니까, 앞에는 제스처가 '하지 않는' 일이 있어야 해요.",
                   highlight=["Instead, it"],
                   panel=board(["choice", "categorical"], ["imagistic"]),
                   method=2),
            show("s5_glue",
                 "제스처는 선택을 주는 대신, 언어 요소들을 묶어 주는 접착제 역할을 해요.",
                 panel=board(["choice", "categorical"], ["imagistic", "glue"], fresh=("glue",)),
                 method=1),
        ],
    },
    {
        "id": 7, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("In this view", "이런 관점에서"), g("speech and gesture", "말과 제스처"), g("redundant", "중복되는, 불필요한"),
                    g("nor is one", "어느 하나가 ~도 아니다"), g("a “translation”", "'번역'"), g("of the other", "다른 하나의")],
        "steps": [
            choice("s6_rel",
                   "이 관점에서 말과 제스처는 어떤 관계래요?",
                   [("o0", "서로 중복되지 않고 각자 다른 일을 한다", True), ("o1", "같은 말을 두 번 한다", False),
                    ("o2", "하나가 다른 하나의 번역이다", False)],
                   "'not redundant nor … a translation'이에요. not A nor B는 'A도 아니고 B도 아니다'예요.",
                   highlight=["not redundant", "nor"],
                   tips=[{"label": "not A nor B", "mark": "nor",
                          "text": "'A도 아니고 B도 아니다'예요. nor 뒤에서는 주어와 동사 순서가 바뀌어요(nor is one …)."}],
                   method=1),
        ],
    },
    {
        "id": 8, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("Rather", "오히려"), g("the minimal processing unit", "최소 처리 단위"),
                    g("for the expression of thought", "생각을 표현하기 위한"), g("a combination of the two", "둘의 결합"),
                    g("imagistic-categorial", "심상적-범주적"), g("in nature", "본질적으로")],
        "steps": [
            choice("s7_unit",
                   "생각을 표현하는 최소 단위는 무엇이래요?",
                   [("o0", "말 하나", False), ("o1", "제스처 하나", False), ("o2", "말과 제스처의 결합", True)],
                   "'a combination of the two'를 봐요. the two는 말과 제스처예요.",
                   highlight=["combination"], method=1),
            show("s7_go",
                 "언어는 고르게 하고(categorical), 제스처는 묶어 줘요(imagistic). 이제 주어진 문장이 들어갈 곳을 골라 봐요.",
                 button="문제 풀러 갈게요",
                 panel=board(["choice", "categorical"], ["imagistic", "glue"], "생각 = 언어 + 제스처 (imagistic-categorial)", between="+"),
                 method=2),
        ],
    },
]

exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은? [3점]",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"],
    # 보기 글이 「… 앞」뿐이라 숫자 ①~⑤만 가로로 보인다
    "numbers_only": True,
    # 답 고르기 화면 — 지문 전체에 칠해 둘 핵심어 (①~⑤ 자리를 찾는 단서)
    "passage_highlight": ["different from language", "such choices", "This kind of choice", "language", "Instead", "glue"],
    "sentence": 1,
    "analysis_first": True,
    "glosses": [],
    "options": [
        {"id": "1", "label": "For example … 앞", "keywords": [], "ko": "언어·제스처가 결합한다 뒤"},
        {"id": "2", "label": "This kind of choice … 앞", "keywords": [], "ko": "완료/진행을 골라야 한다는 예시 뒤"},
        {"id": "3", "label": "Instead, it offers … 앞", "keywords": [], "ko": "이런 선택은 언어의 특징 뒤", "correct": True},
        {"id": "4", "label": "In this view … 앞", "keywords": [], "ko": "대신 접착제를 제공한다 뒤"},
        {"id": "5", "label": "Rather, the minimal … 앞", "keywords": [], "ko": "말과 제스처는 중복도 번역도 아니다 뒤"},
    ],
    "brief": {
        "ask": "주어진 문장의 단서(such choices, gesture)를 떠올리며 들어갈 곳을 골라 봐요.",
        "first_correct": "맞았어요!",
        "first_wrong": "아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.",
        "final_correct": "정답이에요!",
        "answer_explain": "정답이에요! '이런 선택은 언어의 특징이다' 뒤에 '제스처는 그런 선택을 주지 않는다'가 오고, 이어서 'Instead, it(제스처)은 접착제를 준다'로 이어져요.",
        "final_wrong": "정답은 ③이에요.",
        "option_feedback": {
            "1": "이 자리 앞에는 아직 '선택' 이야기가 없어요. such choices가 받을 말이 없어요.",
            "2": "이 자리 앞은 선택의 예시까지예요. 바로 뒤 'This kind of choice'가 그 예시를 받아야 해서 끊기면 안 돼요.",
            "4": "많이 고른 오답이에요. 여기 넣으면 'Instead, it'의 it이 그 앞 문장의 language가 돼서 말이 안 돼요.",
            "5": "이 자리 앞은 이미 말과 제스처의 관계를 정리하는 중이에요. 선택 이야기로 돌아갈 자리가 아니에요.",
        },
        "ask_first": "실제 시험처럼 풀어 봐요. 위 보기에서 답을 골라요.",
    },
}

lesson = {
    "id": ID, "kind": "policy", "version": "0.1",
    "source": "2026년 3월 고3 전국연합학력평가 영어 38번 (주어진 문장 넣기, 3점)",
    "brief": {"topic": "문장 넣기 푸는 법: 주어진 문장의 단서 → 앞 내용 예측 → 흐름이 끊기는 곳", "closing": "수고 인사"},
    "method": {"type": "sentence_insertion", "labels": ["주어진 문장 단서 찾기", "앞에 올 내용 예측하기", "흐름 끊기는 곳 찾기"], "intro_times": 3},
    "read_button": "분석하러 갈게요",
    "read_first": True,
    "images": {"topic": {"src": "/assets/topic-gesture.svg", "alt": "칠판: Language(언어) + Gesture(제스처)", "kind": "drawing"}, "method": {"src": "/assets/insert-method.svg", "alt": "문장 넣기 푸는 법: ① 주어진 문장의 단서 찾기 ② 앞에 올 내용 예측하기 ③ 흐름이 끊기는 곳 찾기", "kind": "drawing"}},
    "intro_board": "method",
    "intro": [
        {"id": "topic", "type": "say", "button": "네", "image": "topic",
         "brief": {"say": "말할 때 손짓은 왜 저절로 나올까요? 이번 글은 언어와 제스처가 함께 생각을 표현하는 방식을 다뤄요."}},
        {"id": "method1", "type": "say", "button": "좋아요",
         "brief": {"say": "문장 넣기는 주어진 문장의 단서를 찾고, 앞에 올 내용을 예측한 뒤, 흐름이 끊기는 곳을 찾아요."}},
    ],
    "exam": exam,
    "key_words": {
        # affix, semiotic은 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
        "passage": [g("gesture", "제스처, 몸짓"), g("in that", "~라는 점에서"), g("demonstrate", "입증하다"),
                    g("systematically", "체계적으로"), g("integrated", "결합된"), g("conceptualize", "개념화하다"),
                    g("formulate", "명확하게 말하다"), g("categorical", "범주적인"), g("ongoing", "진행 중인"),
                    g("characteristic", "특징적인, 특징"), g("unite", "결합하다"), g("redundant", "중복되는"),
                    g("minimal", "최소의"), g("combination", "결합")],
        "options": [],
    },
    "context": {"mode": "paper_review", "exam_relevance": "high", "time_budget": "normal"},
    "item": {"english_difficulty": "high", "conceptual_difficulty": "high", "background_knowledge_required": "low",
             "exam_importance": "high", "teaching_value": "high", "intervention_density": "normal"},
    "sentences": sentences,
    "passage_on_try": True,
}

# 초급 기본 — 문장마다 「주어·동사 + 뜻」 또는 「해석 맞추기」 하나 (2026-10-15 선생님)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beginner import add_basic, add_that_sv, fill_chunk_glosses, m, sv_step  # noqa: E402

add_basic(sentences, 1, [m("According to McNeil and Duncan", "McNeil과 Duncan에 따르면"), " ", m("gesture", "제스처는"), " ",
                         m("the speaker", "화자에게"), " ", m("such choices", "그런 선택"), "을 ", m("does not present", "주지 않는다"), "는 ",
                         m("in that", "점에서"), " ", m("is different from language", "언어와 다르다"), "."],
          sv_new=sv_step("s1_basic_sv", ["gesture", "is different from language", "it", "does not present"],
                         {"gesture": "S", "is different from language": "V"},
                         {"it": "그건 in that(~라는 점에서) 뒤 덩어리 안의 주어예요.", "does not present": "그건 in that(~라는 점에서) 뒤 덩어리 안의 동사예요."},
                         "주어는 gesture(제스처), 동사는 is different from language(언어와 다르다)예요."),
)
# 주어진 문장 — 해석 맞추기는 중·초 (2026-10-16 선생님). 고는 상황 표(g_situation)만
next(x for x in sentences[0]["steps"] if x["id"] == "s1_match")["levels"] = ["중", "초"]
# 문장 1(31단어)은 길어서 단계 상관없이 주어·동사를 모두 찾는다 + the gestures를 꾸미는 덩어리 (2026-10-16 선생님)
_s2 = next(x for x in sentences if x["id"] == 2)
_s2["steps"][0:0] = [
    sv_step("s1_sv", ["Scholars", "have demonstrated", "the gestures", "hearing people", "produce", "are systematically made"],
            {"Scholars": "S", "have demonstrated": "V", "the gestures": "S", "are systematically made": "V"},
            {"hearing people": "그건 the gestures를 꾸미는 덩어리 안의 주어예요. 「듣는 사람들이 만드는」 제스처라는 말이에요.",
             "produce": "그건 the gestures를 꾸미는 덩어리 안의 동사예요."},
            "앞은 주어 Scholars, 동사 have demonstrated예요. that 뒤는 주어 the gestures, 동사 are systematically made예요.",
            ask="긴 문장이에요. 주어(S)와 동사(V)를 모두 찾아볼까요? that 뒤에도 한 쌍 있어요."),
    {"id": "s1_modify", "type": "show", "interaction": "note", "method": 0, "button": "다음",
     "brief": {"say": "초록 부분은 앞의 the gestures를 꾸며요. 아래 표처럼 읽어요."},
     "highlight": ["the gestures"], "highlight_alt": ["hearing people produce while they are speaking"],
     "panel": {"kind": "structure", "rows": [
         {"label": "S", "text": "the gestures", "ko": "제스처", "tone": "hl"},
         {"label": "↖ 꾸밈", "text": "(that) hearing people produce while they are speaking", "ko": "듣는 사람들이 말하는 동안 만드는", "tone": "hl2"},
         {"label": "V", "text": "are systematically made …", "ko": "(말과 동시에) 체계적으로 만들어진다"},
     ]},
     "panel_below": True},
]
add_basic(sentences, 3, [m("This tightly integrated pairing", "이렇게 꼭 붙은 짝(언어와 제스처)은"), " ", m("speakers", "화자가"), " ",
                         m("their thoughts", "자신의 생각"), "을 ", m("formulate", "정리하게"), " ", m("enables", "해 준다"), "."],
          match_display="This tightly integrated pairing of language and gesture enables speakers to formulate their thoughts.",
          sv_new=sv_step("s3_basic_sv", ["This tightly integrated pairing", "enables", "speakers", "to conceptualize and formulate"],
                         # 5형식(enable O to-V) — 보어까지 찾는다. 보어가 빠지면 「무엇을 하게 하는지」가 사라진다 (2026-10-16 선생님)
                         {"This tightly integrated pairing": "S", "enables": "V", "speakers": "O", "to conceptualize and formulate": "C"},
                         {},
                         "주어 This tightly integrated pairing, 동사 enables, 목적어 speakers, 보어 to conceptualize and formulate — 화자가 생각을 개념화하고 정리할 수 있게 해 준대요.",
                         ask="주어(S)·동사(V)·목적어(O)를 찾고, 목적어가 무엇을 하게 되는지(보어 C)까지 찾아볼까요?"),
          meaning_after="s2_img",
          meaning="이렇게 꼭 붙은 언어와 제스처 덕분에, 화자는 언어의 '범주적' 조건과 제스처의 '심상적' 가능성 둘 다로 생각을 정리할 수 있대요.")
# 5형식 읽는 법 — 문법 말 없이 「사람이 ~하게 해 주다」만 (중·초, 2026-10-16 선생님)
_s3 = next(x for x in sentences if x["id"] == 3)
_at = next(i for i, x in enumerate(_s3["steps"]) if x["id"] == "s3_basic_sv") + 1
_s3["steps"].insert(_at, {
    "id": "s3_svoc_note", "type": "show", "interaction": "note", "method": 0, "button": "다음", "levels": ["중", "초"],
    "brief": {"say": "enables + 사람 + to ~는 「사람이 ~하게 해 준다」로 읽어요. 그래서 이 짝은 화자가 생각을 개념화하고 정리할 수 있게 해 준대요."},
    "highlight": ["enables", "speakers", "to conceptualize and formulate"],
    "tips": [{"label": "동사 + 사람 + to ~", "text": "enable·allow·help·encourage·force + 사람 + to ~ = 「사람이 ~하게 (해) 주다」. 예: allow us to see = 우리가 보게 해 준다."}],
})

add_basic(sentences, 4, [m("For example", "예를 들어"), " ", m("in describing an event", "어떤 일을 말할 때"), " 그 일이 ",
                         m("has been completed", "끝났는지"), " ", m("ongoing", "진행 중인지"), "를 ", m("one must decide", "정해야 한다"), "."],
          match_display="For example, in describing an event, one must decide if the event has been completed or is ongoing.",
          sv_new=sv_step("s4_basic_sv", ["one", "must decide", "the event", "has been completed"],
                         {"one": "S", "must decide": "V"},
                         {"the event": "그건 if(~인지) 뒤 덩어리 안의 주어예요.", "has been completed": "그건 if(~인지) 뒤 덩어리 안의 동사예요."},
                         "주어는 one(사람), 동사는 must decide(정해야 한다)예요."),
          meaning_after="s3_choice",
          meaning="예를 들어 어떤 일을 말할 때, 언어에 뜻마다 붙는 꼬리말이 있으면 그 일이 끝났는지 진행 중인지 하나를 꼭 골라야 해요.")
add_basic(sentences, 5, [m("This kind of choice", "이런 종류의 선택은"), " ", m("as a semiotic system", "기호 체계로서"), "의 ",
                         m("language", "언어"), m("is characteristic of", "의 특징이다"), "."],
          sv_new=sv_step("s5_basic_sv", ["This kind of choice", "is characteristic of", "language"],
                         {"This kind of choice": "S", "is characteristic of": "V", "language": "전목"}, {},
                         "주어는 This kind of choice, 동사는 is characteristic of(~의 특징이다), of 뒤 목적어는 language예요."),
          meaning_after="s4_sort", meaning="이런 선택은 기호 체계로서 언어가 가진 특징이래요.")
add_basic(sentences, 6, [m("Instead", "대신에"), ", 그것은 ", m("linguistic elements", "언어 요소들"), "을 ", m("unite", "묶는"), " 걸 돕는 ",
                         m("a kind of glue", "일종의 접착제"), "를 ", m("offers", "준다"), "."],
          match_display="Instead, it offers a kind of glue, which helps unite linguistic elements.",
          sv_new=sv_step("s6_basic_sv", ["it", "offers", "a kind of glue", "linguistic elements"],
                         {"it": "S", "offers": "V", "a kind of glue": "O"},
                         {"linguistic elements": "그건 which 뒤에서 무엇을 묶는지 알려 주는 말이에요."},
                         "주어는 it, 동사는 offers(준다), 목적어는 a kind of glue(일종의 접착제)예요."),
          meaning_ids=["s5_glue"])
add_basic(sentences, 7, [m("In this view", "이 관점에서"), " ", m("speech and gesture", "말과 제스처는"), " ", m("redundant", "중복된 것"), "이 ",
                         m("are not", "아니고"), ", ", m("of the other", "다른 하나의"), " 번역인 ", m("nor is one", "하나가 ~인 것도 아니다"), "."],
          sv_new=sv_step("s7_basic_sv", ["speech and gesture", "are not", "redundant"],
                         {"speech and gesture": "S", "are not": "V", "redundant": "C"}, {},
                         "주어는 speech and gesture, 동사는 are not, 보어는 redundant(중복된)예요."),
          meaning_ids=["s6_rel"],
          meaning="이 관점에서 말과 제스처는 서로 겹치지(중복되지) 않고, 하나가 다른 하나의 '번역'도 아니래요.")
add_basic(sentences, 8, [m("Rather", "오히려"), " ", m("for the expression of thought", "생각을 표현하는"), " ",
                         m("the minimal processing unit", "최소 처리 단위는"), " ", m("a combination of the two", "둘의 조합"), m("is", "이다"), "."],
          match_display="Rather, the minimal processing unit for the expression of thought is a combination of the two.",
          sv_new=sv_step("s8_basic_sv", ["the minimal processing unit", "is", "a combination of the two"],
                         {"the minimal processing unit": "S", "is": "V", "a combination of the two": "C"}, {},
                         "주어는 the minimal processing unit, 동사는 is, 보어는 a combination of the two(둘의 조합)예요."),
          meaning_ids=["s7_unit"], meaning="오히려 생각을 표현하는 최소 단위는 둘(언어와 제스처)의 조합이래요.")
# in that / if 안이 핵심 — 메인 주어·동사 다음 그 안의 주어·동사 (2026-10-16 선생님, 공통)
add_that_sv(sentences, 1, "s1_basic_sv", "s1_that_sv", ["it", "does not present", "the speaker"],
            {"it": "S", "does not present": "V"},
            {"the speaker": "그건 present의 목적어예요. 주어·동사만 찾아요."},
            "in that 안의 주어는 it(= gesture, 제스처), 동사는 does not present(주지 않는다)예요.",
            ask="in that(~라는 점에서) 뒤가 어떻게 다른지예요. 그 안에서 주어(S)와 동사(V)를 찾아볼까요?")
add_that_sv(sentences, 4, "s4_basic_sv", "s4_that_sv", ["the event", "has been completed", "is ongoing"],
            {"the event": "S", "has been completed": "V", "is ongoing": "V"}, {},
            "if 안의 주어는 the event(그 일), 동사는 has been completed(끝났다) 또는 is ongoing(진행 중이다)예요.",
            ask="if(~인지) 뒤가 무엇을 정하는지예요. 그 안에서 주어(S)와 동사(V)를 모두 찾아볼까요?")
fill_chunk_glosses(sentences, {
    "gesture": "제스처", "is different from language": "언어와 다르다", "it": "그것", "does not present": "주지 않는다",
    "According to McNeil and Duncan": "McNeil과 Duncan에 따르면", "the speaker": "화자", "such choices": "그런 선택들", "in that": "~라는 점에서",
    "Scholars": "학자들", "have demonstrated": "입증했다", "the gestures": "그 제스처들", "are systematically made": "체계적으로 만들어진다",
    "at the same time with speech": "말과 동시에", "This tightly integrated pairing": "이 꼭 붙은 짝", "enables": "가능하게 하다",
    "speakers": "화자들", "to conceptualize and formulate": "개념화하고 정리하는 것", "their thoughts": "그들의 생각", "formulate": "정리하다",
    "one": "사람(일반)", "must decide": "정해야 한다", "is ongoing": "진행 중이다", "the event": "그 일", "has been completed": "끝났다",
    "For example": "예를 들어", "in describing an event": "어떤 일을 말할 때", "ongoing": "진행 중인", "one must decide": "사람은 정해야 한다",
    "This kind of choice": "이런 종류의 선택", "is characteristic of": "~의 특징이다", "language": "언어", "as a semiotic system": "기호 체계로서",
    "offers": "주다", "a kind of glue": "일종의 접착제", "linguistic elements": "언어 요소들", "unite": "묶다", "Instead": "대신에",
    "speech and gesture": "말과 제스처", "are not": "~이 아니다", "redundant": "중복된", "In this view": "이 관점에서",
    "of the other": "다른 하나의", "nor is one": "하나가 ~인 것도 아니다",
    "the minimal processing unit": "최소 처리 단위", "is": "~이다", "a combination of the two": "둘의 조합", "Rather": "오히려",
    "for the expression of thought": "생각을 표현하기 위한",
})
next(x for x in sentences if x["id"] == 2)["glosses"].append(g("made", "만들어진"))
next(x for x in sentences if x["id"] == 3)["glosses"].append(g("thoughts", "생각들"))

# 칠판 정리 — 2~3문장마다 지금까지 상황을 칠판에 (공통 틀)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_boards import add_story_boards  # noqa: E402
add_story_boards(ID, lesson["sentences"])

json.dump(lesson, open(f"{ROOT}/content/tutor/policy-lessons/{ID}.json", "w"), ensure_ascii=False, indent=2)

ref = json.load(open(f"{ROOT}/content/tutor/policy-copy/dajung/moeui-2026-03-21-music-researchers.json"))
steps = {st["id"]: copy.deepcopy(st["brief"]) for s in sentences for st in s["steps"]}
c = {
    "lesson": ID, "character": "dajung", "note": "생성물",
    "topic_intro": "문장 넣기 푸는 법",
    "closing": ref["closing"],
    "helps": {},
    "steps": steps,
    "exam": {k: v for k, v in exam["brief"].items()},
    "intro": {i["id"]: dict(i["brief"]) for i in lesson["intro"]},
    "ending": {**ref["ending"], "wrong": "이번엔 한 번 헷갈렸으니 {weeks} 뒤에 다시 한번 볼 거예요."},
}
json.dump(c, open(f"{ROOT}/content/tutor/policy-copy/dajung/{ID}.json", "w"), ensure_ascii=False, indent=2)
print("ok", ID)
