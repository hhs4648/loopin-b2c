"""2024년 3월 고3 22번 레슨 + 대사를 만든다 (요지, 2점). 오답률 자료 없음(Top 15 밖).

    python3 scripts/lessons/gen_moeui_2024_03_22.py   (→ npm run policy:copy stamp <id> → npm run build)

요지 유형은 처음 — 제목(24번) 틀을 따른 Claude 초안(2026-10-18, 미니 모의고사 「분석하기」 연결용):
첫 문장에서 글쓴이 주장 잡기 → 뒤 문장이 그 주장의 근거·예시인지 확인 → 글 전체 한 줄 → 바꿔 쓴 보기.
정답 ③ 다중 언어 사용자는 사용하는 언어에 따라 다르게 느끼고 반응한다. 해설지 해석과 대조함.
rattle, connotation, persecution은 시험지 아래 *로 풀어 준 단어(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, finish)

ID = "moeui-2024-03-22-multilingual-feelings"

S = [
    "Though it may seem extreme, a multilingual can quite literally feel differently about people, events or things when using one language versus another.",
    "The likelihood of being rattled by curse words or taboo words changes across native and second languages.",
    "Speakers of multiple languages not only report feeling different, but their bodies have different physiological reactions and their minds make different emotionally driven decisions across languages.",
    "The exact relationship between positive and negative emotions and language varies across people.",
    "For some, the second language carries more positive connotations because it is associated with freedom, opportunity, financial well-being and escape from persecution, whereas the native language is associated with poverty and hardship.",
    "For others, the opposite is true―the second language is associated with post-immigration challenges, discrimination and lack of close relationships, whereas the native language is associated with family, friends and parental love.",
    "And many are somewhere in between, having a mix of positive and negative experiences associated with each language.",
]
KO = [
    "극단적으로 보일 수도 있지만, 다중 언어 사용자는 한 언어를 사용할 때에 비해 다른 언어를 사용할 때 사람, 사건 또는 사물에 대해 말 그대로 꽤 다르게 느낄 수 있다.",
    "악담이나 금기어에 당황할 가능성은 모국어와 제2 외국어에 따라 달라진다.",
    "다중 언어 사용자는 언어에 따라 다르게 느낀다고 말할 뿐만 아니라, 그들의 신체는 서로 다른 생리적 반응을 보이고, 그들의 생각은 감정에 이끌린 서로 다른 판단을 내린다.",
    "긍정적, 그리고 부정적 감정과 언어 사이의 정확한 관계는 사람에 따라 다르다.",
    "어떤 사람들에게는 제2 외국어가 자유, 기회, 재정적 풍요와 박해로부터의 탈출과 관련이 있기 때문에 더 긍정적인 함축(된 의미)을 지니고 있지만, 모국어는 빈곤과 고난과 관련이 있다.",
    "다른 사람들에게는 그 반대가 참이다. 제2 외국어는 이민 후의 어려움, 차별, 그리고 친밀한 관계의 부재와 관련이 있지만, 모국어는 가족, 친구, 그리고 부모의 사랑과 관련이 있다.",
    "그리고 많은 사람은 그 사이 어딘가에 있는데, 각 언어와 관련된 혼재되어 있는 긍정적이고 부정적인 경험들을 가지고 있다.",
]


def board(second, native, fresh=()):
    return groups("언어마다 다른 느낌", "제2 언어 (second language)", second, "모국어 (native language)", native, fresh=fresh, between="↔")


sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Though it may seem extreme", "극단적으로 보일 수도 있지만"), g("a multilingual", "여러 언어를 쓰는 사람"),
                    g("can quite literally feel differently", "말 그대로 꽤 다르게 느낄 수 있다"),
                    g("about people, events or things", "사람, 사건, 사물에 대해"), g("when using one language", "한 언어를 쓸 때"),
                    g("versus another", "다른 언어에 비해")],
        "slashes": ["seem extreme,", "a multilingual", "feel differently", "events or things"],
        "roles": [r("it", "S"), r("may seem", "V"), r("extreme", "C"), r("a multilingual", "S"), r("can quite literally feel differently", "V")],
        "steps": [
            sv("s1_sv", ["Though it may seem extreme", "a multilingual", "can quite literally feel differently", "people, events or things"],
               {"a multilingual": "S", "can quite literally feel differently": "V"},
               {"Though it may seem extreme": "그건 Though(~지만) 덩어리예요. 콤마 뒤 메인 문장에서 찾아봐요.",
                "people, events or things": "그건 about 뒤, 무엇에 대해 느끼는지예요."},
               "주어는 a multilingual(여러 언어를 쓰는 사람), 동사는 can (quite literally) feel differently예요.",
               ask="콤마 뒤 메인 문장에서 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s1_mean",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "외국어를 쓰면 감정이 사라진다", False), ("o1", "여러 언어를 쓰는 사람은 어떤 언어를 쓰느냐에 따라 같은 대상도 다르게 느낄 수 있다", True),
                    ("o2", "모국어를 쓸 때만 감정을 느낀다", False)],
                   "feel differently는 '다르게 느끼다', one language versus another는 '한 언어와 다른 언어를 비교하면'이에요.",
                   why="'can feel differently … when using one language versus another', 어떤 언어를 쓰느냐에 따라 사람·사건·사물을 다르게 느낄 수 있대요.",
                   highlight=["feel differently", "one language versus another"],
                   tips=[tip("A versus B", "'A 대 B, A에 비해 B'예요. one language versus another = 한 언어를 쓸 때와 다른 언어를 쓸 때.", "versus")]),
            choice("s1_claim",
                   "이 첫 문장은 글쓴이의 주장일까요, 예시일까요?",
                   [("o0", "글쓴이 주장 (하고 싶은 말)", True), ("o1", "구체적인 예시", False)],
                   "Though it may seem extreme(극단적으로 보이겠지만)은 강한 주장을 꺼낼 때 쓰는 말이에요.",
                   why="'Though it may seem extreme'으로 시작해 일반적인 사실을 말해요. 뒤 문장들이 이 말을 받쳐 주는지 확인하면 요지가 돼요.",
                   tips=[tip("요지 문제 요령", "요지는 글쓴이가 가장 하고 싶은 말 한 줄이에요. 주장 문장을 찾고, 뒤 문장이 그 근거·예시인지 확인해요.")],
                   point="첫 문장 = 주장: 다중 언어 사용자는 쓰는 언어에 따라 다르게 느낀다"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("The likelihood", "가능성"), g("of being rattled", "당황할"), g("by curse words or taboo words", "욕이나 금기어에"),
                    g("changes", "달라진다"), g("across native and second languages", "모국어와 제2 언어에 따라")],
        "slashes": ["The likelihood", "being rattled", "taboo words"],
        "roles": [r("The likelihood", "S"), r("changes", "V")],
        "steps": [
            show("s2_example", "욕이나 금기어에 당황하는 정도도 모국어냐 제2 언어냐에 따라 달라진대요. 첫 문장의 예예요.",
                 highlight=["changes", "native and second languages"], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("Speakers of multiple languages", "여러 언어를 쓰는 사람들"), g("not only report feeling different", "다르게 느낀다고 말할 뿐 아니라"),
                    g("but", "~도"), g("their bodies", "그들의 몸"), g("have different physiological reactions", "서로 다른 생리적 반응을 보인다"),
                    g("their minds", "그들의 생각"), g("make different emotionally driven decisions", "감정에 이끌린 서로 다른 판단을 한다"),
                    g("across languages", "언어마다")],
        "slashes": ["multiple languages", "not only report", "feeling different,", "their bodies have", "physiological reactions", "their minds make",
                    "driven decisions"],
        "roles": [r("Speakers", "S"), r("report", "V"), r("feeling different", "O"), r("their bodies", "S"), r("have", "V"),
                  r("different physiological reactions", "O"), r("their minds", "S"), r("make", "V"), r("different emotionally driven decisions", "O")],
        "steps": [
            choice("s3_more",
                   "not only A but B예요. 말로만 다르다고 하는 게 아니라 무엇도 다르대요?",
                   [("o0", "발음과 문법", False), ("o1", "몸의 반응과 감정에 따른 판단", True), ("o2", "사는 나라", False)],
                   "but 뒤 'their bodies …'와 'their minds …'를 봐요.",
                   why="but 뒤에 'their bodies have different physiological reactions'(몸의 반응)와 'their minds make different emotionally driven decisions'(감정에 따른 판단)가 나와요.",
                   highlight=["not only", "their bodies", "their minds"],
                   tips=[tip("not only A but B", "'A뿐만 아니라 B도'예요. 말로 다르다고 하는 것에 더해 몸과 판단도 다르대요.", "not only")]),
            show("s3_same", "말, 몸, 판단까지 모두 언어에 따라 달라진다는 거예요. 첫 문장의 주장을 더 세게 받쳐 줘요.", button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "medium",
        "glosses": [g("The exact relationship", "정확한 관계"), g("between positive and negative emotions and language", "긍정·부정 감정과 언어 사이의"),
                    g("varies across people", "사람마다 다르다")],
        "slashes": ["The exact relationship", "and language"],
        "roles": [r("The exact relationship", "S"), r("varies", "V")],
        "steps": [
            show("s4_varies", "다만 어느 언어가 좋은 감정, 어느 언어가 나쁜 감정과 이어지는지는 사람마다 다르대요. 이제 그 예가 나와요.",
                 highlight=["varies across people"], button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("For some", "어떤 사람들에게는"), g("the second language", "제2 언어"), g("carries more positive connotations", "더 긍정적인 느낌을 지닌다"),
                    g("because", "~ 때문에"), g("is associated with", "~와 관련되다"), g("freedom, opportunity, financial well-being", "자유, 기회, 경제적 풍요"),
                    g("escape from persecution", "박해에서 벗어남"), g("whereas", "반면에"), g("the native language", "모국어"),
                    g("poverty and hardship", "가난과 고난")],
        "slashes": ["For some,", "the second language carries", "positive connotations", "because it is associated with", "financial well-being",
                    "persecution,", "the native language"],
        "roles": [r("the second language", "S"), r("carries", "V"), r("more positive connotations", "O"), r("it", "S"),
                  r("is associated … is associated", "V"), r("the native language", "S")],
        "steps": [
            show("s5_some", "어떤 사람에게는 제2 언어가 자유·기회 같은 좋은 느낌이고, 모국어는 가난·고난과 이어진대요.",
                 panel=board([("+ freedom, opportunity", "자유·기회")], [("− poverty, hardship", "가난·고난")], fresh=("+ freedom, opportunity", "− poverty, hardship")),
                 tips=[tip("whereas", "'반면에'예요. 앞뒤를 맞대어 비교해요.", "whereas")], button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("For others", "다른 사람들에게는"), g("the opposite is true", "그 반대가 맞다"), g("the second language", "제2 언어"),
                    g("is associated with", "~와 관련되다"), g("post-immigration challenges", "이민 후의 어려움"), g("discrimination", "차별"),
                    g("lack of close relationships", "가까운 관계가 없음"), g("whereas", "반면에"), g("the native language", "모국어"),
                    g("family, friends and parental love", "가족, 친구, 부모의 사랑")],
        "slashes": ["For others,", "is true―", "the second language", "post-immigration challenges,", "close relationships,", "the native language"],
        "roles": [r("the opposite", "S"), r("is", "V"), r("true", "C"), r("the second language", "S"), r("is associated … is associated", "V"),
                  r("the native language", "S")],
        "steps": [
            choice("s6_opposite",
                   "For others, the opposite is true예요. 다른 사람들에게는 어떻대요?",
                   [("o0", "제2 언어가 더 좋은 느낌이다", False), ("o1", "모국어가 가족·사랑 같은 좋은 느낌이다", True), ("o2", "두 언어 모두 느낌이 없다", False)],
                   "the opposite는 '그 반대'예요. 앞 문장과 반대로 뒤집어 봐요.",
                   why="'the opposite is true', 앞 문장과 반대예요. 제2 언어는 이민 뒤 어려움·차별과, 모국어는 가족·친구·부모의 사랑과 이어진대요.",
                   highlight=["the opposite is true"],
                   panel=board([("+ freedom, opportunity", "자유·기회")], [("− poverty, hardship", "가난·고난")])),
            show("s6_flip", "제2 언어 쪽엔 어려움·차별이, 모국어 쪽엔 가족·사랑이 붙었어요. 같은 언어라도 사람마다 느낌이 반대예요.",
                 panel=board([("+ freedom, opportunity", "자유·기회"), ("− challenges, discrimination", "어려움·차별")],
                             [("− poverty, hardship", "가난·고난"), ("+ family, parental love", "가족·사랑")],
                             fresh=("− challenges, discrimination", "+ family, parental love")), button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("And many are somewhere in between", "그리고 많은 사람은 그 사이 어딘가에 있다"),
                    g("having a mix of positive and negative experiences", "좋고 나쁜 경험이 섞여 있으면서"),
                    g("associated with each language", "각 언어와 관련된")],
        "slashes": ["in between,", "negative experiences"],
        "roles": [r("many", "S"), r("are", "V")],
        "steps": [
            show("s7_between", "많은 사람은 그 사이 어딘가, 언어마다 좋고 나쁜 경험이 섞여 있대요.", highlight=["somewhere in between"]),
            choice("s7_gist",
                   "글 전체를 한 줄로 묶으면 어떤 말일까요?",
                   [("o0", "모국어가 늘 더 긍정적인 느낌을 준다", False), ("o1", "긍정적인 단어가 부정적인 단어보다 많다", False),
                    ("o2", "어떤 언어를 쓰느냐에 따라 느낌과 반응이 달라진다", True)],
                   "첫 문장(주장)을 떠올려 봐요. 뒤 문장들은 모두 그 주장의 근거와 예였어요.",
                   why="첫 문장이 주장이고, 욕설·몸·판단·사람마다 다른 예가 모두 '언어에 따라 다르게 느끼고 반응한다'를 받쳐 줘요. 모국어가 늘 긍정적인 건 아니에요(the opposite).",
                   point="요지 = 다중 언어 사용자는 쓰는 언어에 따라 다르게 느끼고 반응한다"),
            show("s7_go", "이 한 줄을 다른 말로 바꿔 쓴 보기를 골라 봐요.", button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 2, [m("The likelihood", "가능성은"), " ", m("by curse words or taboo words", "욕이나 금기어에"), " ", m("of being rattled", "당황할"), " — ",
                         m("across native and second languages", "모국어와 제2 언어에 따라"), " ", m("changes", "달라진다"), "."],
          sv_new=sv_step("s2_basic_sv", ["The likelihood", "curse words or taboo words", "changes"], {"The likelihood": "S", "changes": "V"},
                         {"curse words or taboo words": "그건 by 뒤 덩어리예요."}, "주어는 The likelihood, 동사는 changes예요."),
          meaning_ids=["s2_example"])
add_basic(sentences, 4, [m("The exact relationship", "정확한 관계는"), " ", m("varies across people", "사람마다 다르다"), "."],
          sv_new=sv_step("s4_basic_sv", ["The exact relationship", "positive and negative emotions", "varies"], {"The exact relationship": "S", "varies": "V"},
                         {"positive and negative emotions": "그건 between 뒤 덩어리예요."}, "주어는 The exact relationship, 동사는 varies예요."),
          meaning_ids=["s4_varies"])
add_basic(sentences, 7, [m("And many are somewhere in between", "그리고 많은 사람은 그 사이 어딘가에 있다"), ", ",
                         m("having a mix of positive and negative experiences", "좋고 나쁜 경험이 섞여 있으면서"), "."],
          sv_new=sv_step("s7_basic_sv", ["many", "are", "somewhere in between"], {"many": "S", "are": "V"},
                         {"somewhere in between": "그건 어디에 있는지 알려 주는 말이에요."}, "주어는 many(많은 사람), 동사는 are예요."),
          meaning_ids=["s7_between"])

SENSES = {
    3: [sense("but", "but their bodies", "~도 (not only A but B)", "not only A but (also) B")],
    5: [sense("for", "For some", "~에게는", "전치사 for + 사람")],
    6: [sense("for", "For others", "~에게는", "전치사 for + 사람")],
}

WORDS = {"seem": "~처럼 보이다", "extreme": "극단적인", "multilingual": "여러 언어를 쓰는 사람", "literally": "말 그대로",
         "differently": "다르게", "events": "사건", "using": "쓰는", "language": "언어", "versus": "~에 비해", "likelihood": "가능성",
         "rattled": "당황한", "curse": "욕", "words": "단어", "taboo": "금기의", "changes": "달라지다", "native": "모국의",
         "second": "두 번째의", "languages": "언어들", "speakers": "말하는 사람들", "multiple": "여럿의", "report": "말하다, 보고하다",
         "feeling": "느끼는 것", "different": "다른", "bodies": "몸", "physiological": "생리적인", "reactions": "반응",
         "minds": "생각, 마음", "emotionally": "감정적으로", "driven": "이끌린", "decisions": "판단, 결정", "exact": "정확한",
         "relationship": "관계", "positive": "긍정적인", "negative": "부정적인", "emotions": "감정", "varies": "다르다",
         "carries": "지니다", "connotations": "함축된 의미, 느낌", "associated": "관련된", "freedom": "자유", "opportunity": "기회",
         "financial": "경제적인", "well-being": "풍요, 행복", "escape": "벗어남", "persecution": "박해", "poverty": "가난",
         "hardship": "고난", "opposite": "반대", "true": "맞는", "post-immigration": "이민 후의", "challenges": "어려움",
         "discrimination": "차별", "lack": "부족", "close": "가까운", "relationships": "관계", "family": "가족", "friends": "친구",
         "parental": "부모의", "love": "사랑", "somewhere": "어딘가", "between": "사이에", "mix": "섞인 것", "experiences": "경험",
         "each": "각각의", "quite": "꽤", "things": "사물"}

STORIES = [
    (3, [sc("문장 1~3", "🗣️", "feel differently across languages", "여러 언어를 쓰면 언어에 따라 느낌·몸의 반응·판단이 달라요")]),
    (6, [sc("문장 4~6", "🔄", "varies across people · the opposite", "어느 언어가 좋은 느낌인지는 사람마다 달라요 — 정반대인 사람도 있어요")]),
]

OPTIONS = [
    ("1", "다중 언어 환경은 모국어 학습 발달을 지연시킨다.", ["모국어 학습", "지연"], False),
    ("2", "모국어 실력이 뛰어날수록 외국어를 습득하는 속도가 빠르다.", ["외국어를 습득하는 속도"], False),
    ("3", "다중 언어 사용자는 사용하는 언어에 따라 다르게 느끼고 반응한다.", ["언어에 따라", "다르게 느끼고 반응"], True),
    ("4", "부정적인 어휘가 긍정적인 어휘보다 감정에 미치는 영향이 크다.", ["부정적인 어휘"], False),
    ("5", "긍정적인 감정을 나타내는 어휘량이 문화권마다 다르다.", ["어휘량", "문화권마다"], False),
]
exam = {
    "question": "다음 글의 요지로 가장 적절한 것은?", "sentence": 1, "analysis_first": True, "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "첫 문장의 주장(언어에 따라 다르게 느낀다)을 떠올리며 골라 봐요.",
        "정답이에요! 첫 문장이 주장이고, 욕설·몸의 반응·판단·사람마다 다른 예가 모두 '언어에 따라 다르게 느끼고 반응한다'를 받쳐 줘요.",
        "정답은 ③이에요. 다중 언어 사용자는 쓰는 언어에 따라 다르게 느끼고 반응한다는 글이에요.",
        {"1": "모국어 학습이 늦어진다는 이야기는 글에 없어요.",
         "2": "외국어를 배우는 속도 이야기는 글에 없어요.",
         "4": "부정적인 단어의 영향이 더 크다는 비교는 없어요. 긍정·부정은 사람마다 다르다고 했어요.",
         "5": "어휘의 양이나 문화권 이야기는 글에 없어요."}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 22번 (요지, 2점)",
    topic="요지 푸는 법: 주장 문장 찾기 → 뒤 문장이 근거·예시인지 확인 → 글 전체 한 줄 → 바꿔 쓴 보기",
    method={"type": "gist", "labels": ["주장 문장 찾기", "근거·예시 확인"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-multilingual.svg", ("Language A", "한 언어"), "↔", ("Language B", "다른 언어"),
                                       "언어를 바꾸면 느낌도 바뀔까?", "2024년 3월 22번 도입 칠판"),
                      "alt": "칠판: Language A(한 언어) ↔ Language B(다른 언어)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "같은 욕도 모국어로 들을 때와 외국어로 들을 때 느낌이 같을까요? 이번 글은 언어와 감정의 관계를 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "요지 문제는 글쓴이가 가장 하고 싶은 말 한 줄을 찾는 거예요. 주장 문장을 잡고, 뒤 문장이 그걸 받쳐 주는지 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("multilingual", "여러 언어를 쓰는 사람"), g("literally", "말 그대로"), g("versus", "~에 비해"), g("likelihood", "가능성"),
                           g("taboo", "금기"), g("physiological", "생리적인"), g("emotionally driven", "감정에 이끌린"), g("vary", "다르다"),
                           g("be associated with", "~와 관련되다"), g("whereas", "반면에"), g("hardship", "고난"), g("discrimination", "차별")],
               "options": [g("acquire", "습득하다"), g("delay", "지연시키다")]},
    sentences=sentences, concept="medium")

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="요지 푸는 법",
       chunks={"Though it may seem extreme": "극단적으로 보일 수도 있지만", "a multilingual": "여러 언어를 쓰는 사람",
               "can quite literally feel differently": "말 그대로 꽤 다르게 느낄 수 있다", "people, events or things": "사람, 사건, 사물",
               "The likelihood": "가능성", "curse words or taboo words": "욕이나 금기어", "changes": "달라지다",
               "The exact relationship": "정확한 관계", "positive and negative emotions": "긍정·부정 감정", "varies": "다르다",
               "many": "많은 사람", "are": "있다", "somewhere in between": "그 사이 어딘가"})
