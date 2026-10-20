"""2024년 3월 고3 12번 레슨 + 대사를 만든다 (듣기 — 마지막 말에 대한 응답, 2점). 오답률 54.9% · Top 8.

    python3 scripts/lessons/gen_moeui_2024_03_12.py   (→ npm run policy:copy stamp <id> → npm run build)

듣기 문항이지만 대본(해설지)을 지문처럼 읽는 수업으로 만든다(2026-10-17 선생님: 「대본으로 독해식 수업」).
문장 아래 🔊 듣기로 소리를 들을 수 있다. 푸는 법: 누가 무엇을 하고 있는지 → 마지막 말이 요청·제안인지 → 그에 맞는 응답.
정답 ② You're right. Let's pull over at the next rest area.
많이 고른 오답 ⑤ 39.7% — 'I can take over driving after the break'. 운전하던 사람이 남자라 남자가 운전을 넘겨받을 수 없다.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, rows, sense, m, sv_step, add_basic, topic_svg, pick,  # noqa: E402
                      base_lesson, exam_brief, review, finish)

ID = "moeui-2024-03-12-driving-break"

S = [
    "Honey, you’ve been driving for over two hours. Why don’t we take a break?",
    "It’s okay. I’m not so tired yet.",
    "Still, it’s better to take a rest after every two hours of driving.",
    "________",
]

sentences = [
    {
        "id": 1, "label": "여자의 첫 말", "text": S[0], "teaching_value": "high",
        "model_translation": "(여자) 여보, 당신 두 시간 넘게 운전했어요. 우리 좀 쉬는 게 어때요?",
        "glosses": [g("Honey", "여보, 자기"), g("you’ve been driving", "당신은 계속 운전해 왔다"), g("you", "당신은"),
                    g("’ve been driving", "계속 운전해 왔다 (= have been driving)"), g("’ve", "= have"), g("for over two hours", "두 시간 넘게"),
                    g("Why don’t we", "우리 ~하는 게 어때요"), g("take a break", "잠깐 쉬다")],
        "slashes": ["Honey,", "been driving", "two hours.", "Why don’t we"],
        "roles": [r("you", "S"), r("’ve been driving", "V"), r("we", "S"), r("don’t … take", "V"), r("a break", "O")],
        "steps": [
            choice("s1_who",
                   "지금 운전하고 있는 사람은 누구일까요?",
                   [("o0", "여자", False), ("o1", "남자", True), ("o2", "둘 다 아니다", False)],
                   "여자가 상대에게 'you’ve been driving(당신은 계속 운전해 왔어요)'이라고 해요.",
                   why="여자가 대화 상대에게 'you’ve been driving'이라고 했어요. 계속 운전해 온 사람은 여자가 아니라 그 상대예요.",
                   highlight=["you’ve been driving"],
                   tips=[tip("have been -ing", "'계속 ~해 왔다(지금도 하는 중)'예요. you’ve been driving = 당신은 계속 운전하고 있어요.", "been driving")],
                   point="you’ve been driving = 지금까지 계속 운전한 사람은 남자 (대화에서 누가 무엇을 하는지 먼저)"),
            choice("s1_suggest",
                   "'Why don’t we take a break'는 무슨 말일까요?",
                   [("o0", "왜 쉬지 않았냐는 꾸중", False), ("o1", "운전을 바꾸자는 제안", False), ("o2", "잠깐 쉬자는 제안", True)],
                   "Why don’t we ~는 이유를 묻는 게 아니라 '우리 ~하는 게 어때요'라는 제안이에요.",
                   why="Why don’t we ~는 '우리 ~하는 게 어때요'라는 제안이에요. take a break는 '잠깐 쉬다'예요.",
                   highlight=["Why don’t we", "take a break"],
                   tips=[tip("Why don’t we ~?", "'우리 ~하는 게 어때요?'라는 제안이에요. 왜 안 하냐고 따지는 말이 아니에요.", "Why don’t we")]),
        ],
    },
    {
        "id": 2, "label": "남자의 대답", "text": S[1], "teaching_value": "medium",
        "model_translation": "(남자) 괜찮아요. 아직 그렇게 피곤하지 않아요.",
        "glosses": [g("It’s okay", "괜찮아요"), g("I’m not so tired", "그렇게 피곤하지 않아요"), g("yet", "아직")],
        "slashes": ["It’s okay."],
        "roles": [r("It", "S"), r("’s", "V"), r("okay", "C"), r("I", "S"), r("’m", "V"), r("tired", "C")],
        "steps": [
            show("s2_refuse", "남자는 괜찮다며 아직 그렇게 피곤하지 않대요. 쉬자는 제안을 한 번 거절했어요.",
                 highlight=["It’s okay", "not so tired"], button="다음 문장",
                 tips=[tip("not ~ yet", "'아직 ~ 않다'예요. not so tired yet = 아직 그렇게 피곤하지 않다.", "yet")]),
        ],
    },
    {
        "id": 3, "label": "여자의 마지막 말", "text": S[2], "teaching_value": "high",
        "model_translation": "(여자) 그래도 두 시간 운전할 때마다 쉬는 게 더 좋아요.",
        "glosses": [g("Still", "그래도"), g("it’s better to", "~하는 게 더 낫다"), g("take a rest", "쉬다"), g("to take a rest", "쉬는 것"),
                    g("every two hours", "두 시간마다"),
                    g("after every two hours of driving", "두 시간 운전할 때마다")],
        "slashes": ["Still,", "it’s better", "take a rest"],
        "roles": [r("it", "S"), r("’s", "V"), r("better", "C")],
        "steps": [
            choice("s3_still",
                   "Still(그래도)로 시작해요. 여자는 마지막에 무엇을 말하고 있나요?",
                   [("o0", "운전을 자기가 하겠다고 한다", False), ("o1", "그래도 두 시간마다 쉬는 게 낫다며 다시 쉬자고 한다", True),
                    ("o2", "더 빨리 가자고 한다", False)],
                   "Still은 '그래도'예요. 남자가 거절했지만 여자는 같은 말을 한 번 더 해요.",
                   why="Still(그래도), 'it’s better to take a rest', 두 시간마다 쉬는 게 낫다며 다시 쉬자고 해요. 운전을 바꾸자는 말은 없어요.",
                   highlight=["Still", "take a rest"],
                   tips=[tip("Still", "문장 맨 앞의 Still은 '그래도, 그렇다 해도'예요. '여전히'와 구별해요.", "Still")],
                   point="마지막 말 = 그래도 쉬자 (운전을 바꾸자는 말은 없다)"),
        ],
    },
    {
        "id": 4, "label": "남자의 응답", "text": S[3], "teaching_value": "high",
        "model_translation": "(남자) ________",
        "glosses": [],
        "steps": [
            choice("s4_need",
                   "운전하는 사람은 남자, 여자는 '그래도 쉬자'고 했어요. 남자의 응답은 어떤 말이 자연스러울까요?",
                   [("o0", "쉬고 나서 자기가 운전을 넘겨받겠다는 말", False), ("o1", "쉬자는 말에 동의하며 쉴 곳을 찾는 말", True),
                    ("o2", "길이 막혀서 늦었다는 말", False)],
                   "남자는 처음엔 거절했어요. 여자가 다시 권하면 이번엔 받아들이는 말이 자연스러워요.",
                   why="여자가 다시 쉬자고 했으니 받아들이는 말이 자연스러워요. 운전을 '넘겨받는' 건 운전하지 않던 여자가 할 말이에요.",
                   point="응답 = 쉬자는 제안에 동의 (운전하던 남자가 운전을 넘겨받을 수는 없다)"),
            show("s4_go", "이제 실제 보기 다섯 개에서 골라 봐요. 누가 운전하는지 꼭 떠올려요.", button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 1, [m("you’ve been driving", "당신은 계속 운전해 왔다"), " ", m("for over two hours", "두 시간 넘게"), ". ",
                         m("Why don’t we", "우리 ~하는 게 어때요"), " ", m("take a break", "잠깐 쉬다"), "?"],
          sv_new=sv_step("s1_basic_sv", ["you", "’ve been driving", "two hours", "we", "take"],
                         {"you": "S", "’ve been driving": "V"},
                         {"two hours": "그건 for over 뒤, 얼마나 오래인지 알려 주는 말이에요.", "we": "그건 뒤 문장(제안)의 주어예요.",
                          "take": "그건 뒤 문장(제안)의 동사예요."},
                         "첫 문장은 주어 you, 동사 ’ve been driving(= have been driving)이에요. you’ve = you have예요.",
                         ask="you’ve는 you have를 줄인 말이에요. 첫 문장의 주어(S)와 동사(V) 덩어리를 찾아볼까요?"),
          meaning_after="s1_suggest")
add_basic(sentences, 3, [m("Still", "그래도"), ", ", m("after every two hours of driving", "두 시간 운전할 때마다"), " ", m("take a rest", "쉬는"), " 게 ",
                         m("it’s better to", "더 낫다"), "."],
          sv_new=pick("s3_basic_sv", "it’s better to ~에서 it은 자리만 채우는 말이에요. 더 나은 게 무엇인지, 진짜 주어를 찾아볼까요?",
                      ["it’s", "to take a rest", "every two hours"], ["to take a rest"], "그건 진짜 주어가 아니에요.",
                      "it = to take a rest예요. 두 시간마다 쉬는 것이 더 낫대요.",
                      wrong_by={"it’s": "it’s의 it은 자리만 채우는 가주어예요. 뒤에서 to로 시작하는 덩어리를 찾아봐요.",
                                "every two hours": "그건 언제(얼마마다)인지 알려 주는 말이에요."},
                      no_unknown=True, tips=[tip("가주어 it ~ 진주어 to", "it’s better to ~처럼 it이 앞자리를 채우면, 진짜 주어는 뒤의 to 덩어리예요. 해석은 '~하는 것이 더 낫다'.", "it")]),
          meaning_after="s3_still")

SENSES = {
    1: [sense("for", "for over two hours", "~ 동안", "전치사 for + 기간")],
    2: [sense("so", "not so tired", "그렇게, 그다지", "부사 so + 형용사"), sense("yet", "tired yet", "아직", "부사 yet (부정문: 아직 ~ 않다)")],
    3: [sense("to", "better to take", "~하는 것", "가주어 it … 진주어 to부정사")],
}

WORDS = {"honey": "여보", "driving": "운전하는", "over": "~ 넘게", "two": "둘", "hours": "시간", "break": "휴식",
         "okay": "괜찮은", "tired": "피곤한", "still": "그래도", "better": "더 나은", "rest": "휴식", "every": "~마다",
         "take": "가지다 · take a break/rest = 쉬다", "why": "왜 · Why don’t we ~? = ~하는 게 어때요?", "you’ve": "당신은 ~해 왔다",
         "been": "(have been -ing = 계속 ~해 왔다)", "i’m": "나는 ~이다"}

OPTIONS = [
    ("1", "It wasn’t easy. It took over three hours to get there.", "쉽지 않았어요. 거기 가는 데 세 시간 넘게 걸렸어요.", False),
    ("2", "You’re right. Let’s pull over at the next rest area.", "당신 말이 맞아요. 다음 휴게소에서 차를 세워요.", True),
    ("3", "No problem. I got my car fixed before the trip.", "문제없어요. 여행 전에 차를 고쳤어요.", False),
    ("4", "Careful! You shouldn’t go over the speed limit.", "조심해요! 제한 속도를 넘으면 안 돼요.", False),
    ("5", "Okay. I can take over driving after the break.", "좋아요. 쉬고 나서 내가 운전을 넘겨받을 수 있어요.", False),
]
exam = {
    "question": "대화를 듣고, 여자의 마지막 말에 대한 남자의 응답으로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 4, "analysis_first": True, "wrong_rate": 54.9, "wrong_rank": 8,
    "glosses": [g("easy", "쉬운"), g("took", "(시간이) 걸렸다"), g("right", "옳은"), g("pull over", "차를 세우다"), g("rest area", "휴게소"),
                g("got my car fixed", "차를 고쳤다"), g("trip", "여행"), g("careful", "조심하는"), g("speed limit", "제한 속도"),
                g("take over", "넘겨받다, 교대하다")],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "누가 운전하는지, 여자의 마지막 말이 무엇을 권하는지 떠올리며 골라 봐요.",
        "정답이에요! 운전하던 남자에게 여자가 '그래도 두 시간마다 쉬자'고 했어요. 남자가 '맞아요, 다음 휴게소에서 차를 세워요'라고 받아들이는 게 자연스러워요.",
        "정답은 ②예요. 여자의 '그래도 쉬자'는 말에 남자가 동의하며 휴게소에 차를 세우자고 해요.",
        {"1": "여기까지 오는 데 걸린 시간 이야기는 마지막 말(쉬자)과 이어지지 않아요.",
         "3": "차를 고쳤다는 말은 쉬자는 제안과 상관없어요.",
         "4": "과속 이야기는 대화에 없어요.",
         "5": "운전하던 사람이 남자라서, 남자가 운전을 넘겨받는다는 건 말이 안 돼요. 그건 여자가 할 말이에요."},
        {"5": review(39.7,
                     "⑤ 'I can take over driving after the break'는 '쉬고 나서 내가 운전을 넘겨받을게요'예요. 그런데 대화 첫 줄에서 여자가 남자에게 'you’ve been driving'이라고 했어요. 이미 운전하고 있는 남자가 운전을 넘겨받을 수는 없어요.",
                     "그래서 ⑤가 아니에요. 어디서 헷갈렸어요?",
                     [("take over 뜻을 몰랐어요", ["take_over"],
                       "알려 줘서 고마워요. take over는 '(남이 하던 일을) 넘겨받다, 교대하다'예요. 앞으로 비슷한 표현이 나오면 짚어 줄게요."),
                      ("누가 운전하는지 놓쳤어요", ["who_does"],
                       "알려 줘서 고마워요. 듣기 응답 문제는 누가 무엇을 하고 있는지가 열쇠예요. 앞으로 첫 줄에서 그걸 먼저 짚어 줄게요."),
                      ("둘 다요", ["take_over", "who_does"], "알려 줘서 고마워요. 앞으로 누가 무엇을 하는지와 어려운 표현을 같이 짚어 줄게요.")],
                     panel=rows(("여자의 첫 말", "you’ve been driving", "운전하는 사람 = 남자", "hl"),
                                ("⑤", "I can take over driving", "운전을 넘겨받겠다 = 운전 안 하던 사람의 말", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 12번 (듣기 — 마지막 말에 대한 응답, 2점)",
    topic="듣기 응답 푸는 법: 누가 무엇을 하고 있는지 → 마지막 말이 무엇을 묻거나 권하는지 → 거기에 맞는 응답",
    method={"type": "listening_response", "labels": ["누가 무엇을 하는지", "마지막 말 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-driving-break.svg", ("Driving", "운전"), "→", ("Break?", "쉴까?"),
                                       "쉬자는 말에 운전하던 사람은 뭐라고 할까?", "2024년 3월 12번 도입 칠판"),
                      "alt": "칠판: Driving(운전) → Break?(쉴까?)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "두 시간 넘게 운전한 사람에게 쉬자고 하면 뭐라고 답할까요? 이번엔 듣기 문제를 대본으로 같이 읽어 봐요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "듣기 응답 문제는 누가 무엇을 하고 있는지, 마지막 말이 무엇을 권하는지 잡는 게 핵심이에요. 문장 아래 🔊 듣기로 소리도 들어 봐요."}}],
    exam=exam,
    key_words={"passage": [g("take a break", "잠깐 쉬다"), g("take a rest", "쉬다"), g("Why don’t we ~?", "우리 ~하는 게 어때요?"),
                           g("still", "그래도"), g("not ~ yet", "아직 ~ 않다")],
               "options": [g("pull over", "차를 세우다"), g("rest area", "휴게소"), g("take over", "넘겨받다, 교대하다"), g("speed limit", "제한 속도")]},
    sentences=sentences, english="medium", concept="medium")

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="듣기 응답 푸는 법",
       chunks={"you’ve been driving": "당신은 계속 운전해 왔다", "two hours": "두 시간", "we": "우리", "take": "하다(쉬다)",
               "Still": "그래도", "it’s": "그것은 ~이다", "better": "더 나은", "a rest": "휴식"})
