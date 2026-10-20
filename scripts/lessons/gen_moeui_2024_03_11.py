"""2024년 3월 고3 11번 레슨 + 대사를 만든다 (듣기 — 마지막 말에 대한 응답, 2점). 오답률 42.2% · Top 13.

    python3 scripts/lessons/gen_moeui_2024_03_11.py   (→ npm run policy:copy stamp <id> → npm run build)

12번과 같은 틀 — 대본(해설지)을 지문처럼 읽는다. 문장 아래 🔊 듣기로 소리도 듣는다.
정답 ③ No need. You can have your photo taken on the spot.
많이 고른 오답 ⑤ 14.8%(그 사무실은 재발급을 안 한다 — 여자가 거기서 새로 받았다고 했다), ② 13.9%(단체 사진 — photo만 겹친다).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, rows, sense, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)

ID = "moeui-2024-03-11-student-id-photo"

S = [
    "Rachel, I heard you got your student ID card reissued.",
    "Yeah, I lost my old one somewhere. So I went to the student services office and got a new one.",
    "Actually, I lost mine too, so I need to go there. Do I need to bring my photo for a new ID card?",
    "________",
]

sentences = [
    {
        "id": 1, "label": "남자의 첫 말", "text": S[0], "teaching_value": "medium",
        "model_translation": "(남자) Rachel, 너 학생증 재발급받았다고 들었어.",
        "glosses": [g("Rachel", "레이철 · 여자 이름"), g("I heard", "~라고 들었다"), g("you got", "네가 ~하게 했다"),
                    g("your student ID card", "너의 학생증"), g("reissued", "재발급된")],
        "slashes": ["Rachel,", "I heard"],
        "roles": [r("I", "S"), r("heard", "V"), r("you", "S"), r("got", "V"), r("your student ID card", "O")],
        "steps": [
            choice("s1_what",
                   "Rachel에게 무슨 일이 있었대요?",
                   [("o0", "학생증을 처음 만들었다", False), ("o1", "학생증을 다시 발급받았다", True), ("o2", "사진을 찍었다", False)],
                   "reissue는 're(다시) + issue(발급하다)'예요. got your card reissued는 '카드를 재발급받았다'예요.",
                   why="'got your student ID card reissued', 학생증을 재발급받았대요. re-는 '다시'예요.",
                   highlight=["reissued"],
                   tips=[tip("get + 물건 + p.p.", "'(남을 시켜) 물건이 ~되게 하다'예요. got my card reissued = 카드를 재발급받았다.", "got"),
                         tip("re-", "'다시'라는 뜻을 더해요. reissue = 다시 발급하다, rebuild = 다시 짓다.", "reissued")]),
        ],
    },
    {
        "id": 2, "label": "여자의 대답", "text": S[1], "teaching_value": "high",
        "model_translation": "(여자) 응, 예전 걸 어디서 잃어버렸어. 그래서 학생 지원실에 가서 새로 받았어.",
        "glosses": [g("Yeah", "응"), g("I lost my old one", "예전 것을 잃어버렸다"), g("somewhere", "어딘가에서"), g("So", "그래서"),
                    g("I went to", "~에 갔다"), g("the student services office", "학생 지원실"), g("got a new one", "새것을 받았다")],
        "slashes": ["Yeah,", "my old one", "somewhere.", "the student services office"],
        "roles": [r("I … I", "S"), r("lost", "V"), r("my old one", "O"), r("went", "V"), r("got", "V"), r("a new one", "O")],
        "steps": [
            show("s2_office", "예전 학생증을 잃어버려서 학생 지원실(student services office)에 가서 새로 받았대요. 그 사무실에서 재발급을 해 준다는 거예요.",
                 highlight=["the student services office", "got a new one"], button="다음 문장",
                 point="여자는 학생 지원실에서 새 학생증을 받았다 = 그곳에서 재발급해 준다"),
        ],
    },
    {
        "id": 3, "label": "남자의 마지막 말", "text": S[2], "teaching_value": "high",
        "model_translation": "(남자) 사실 나도 내 걸 잃어버려서 거기 가야 해. 새 학생증 만들려면 사진을 가져가야 해?",
        "glosses": [g("Actually", "사실"), g("I lost mine too", "나도 내 것을 잃어버렸다"), g("so", "그래서"), g("I need to go there", "거기 가야 한다"),
                    g("Do I need to bring", "내가 ~을 가져가야 하니"), g("my photo", "내 사진"), g("for a new ID card", "새 학생증을 위해")],
        "slashes": ["Actually,", "mine too,", "go there.", "Do I need to bring", "my photo"],
        "roles": [r("I … I … I", "S"), r("lost", "V"), r("mine", "O"), r("need to go", "V"), r("Do … need to bring", "V"), r("my photo", "O")],
        "steps": [
            choice("s3_q",
                   "남자의 마지막 질문은 무엇일까요?",
                   [("o0", "학생 지원실이 어디 있나요", False), ("o1", "새 학생증을 만들려면 사진을 가져가야 하나요", True),
                    ("o2", "네 학생증을 찾았나요", False)],
                   "마지막 문장 'Do I need to bring my photo …'를 봐요. bring은 '가져가다'예요.",
                   why="'Do I need to bring my photo for a new ID card', 새 학생증을 만들 때 사진을 가져가야 하는지 묻고 있어요.",
                   highlight=["Do I need to bring", "my photo"]),
            choice("s3_kind",
                   "Do I need to ~(~해야 하나요)라는 질문에는 어떤 대답이 자연스러울까요?",
                   [("o0", "필요한지 아닌지 말하고 이유를 덧붙인다", True), ("o1", "고맙다고만 한다", False), ("o2", "다른 질문으로 바꾼다", False)],
                   "Do I need to ~?는 해야 하는지 묻는 말이에요. 해야 한다/안 해도 된다가 먼저 와요.",
                   why="Do I need to ~?는 해야 하는지를 묻는 질문이에요. 그래서 필요한지 아닌지와 그 이유가 대답이 돼요.",
                   tips=[tip("No need", "'그럴 필요 없어'예요. Do I need to ~?에 대한 짧은 대답으로 자주 써요.")]),
        ],
    },
    {
        "id": 4, "label": "여자의 응답", "text": S[3], "teaching_value": "high",
        "model_translation": "(여자) ________",
        "glosses": [],
        "steps": [
            choice("s4_need",
                   "여자는 방금 그 사무실에서 직접 재발급받았어요. 사진을 가져가야 하냐는 질문에 어떤 응답이 자연스러울까요?",
                   [("o0", "그 사무실은 학생증을 재발급하지 않는다는 말", False), ("o1", "여기서 단체 사진을 찍자는 말", False),
                    ("o2", "가져갈 필요 없고 거기서 바로 찍어 준다는 말", True)],
                   "여자는 경험이 있어요. 질문(사진을 가져가야 하나)에 바로 답하는 말을 찾아봐요.",
                   why="여자는 그 사무실에서 새로 받았으니 재발급은 해 줘요. 단체 사진은 photo만 같아요. 사진이 필요한지에 답하는 말이 자연스러워요.",
                   point="응답 = 사진을 가져가야 하나? → 필요 없다, 거기서 찍어 준다"),
            show("s4_go", "이제 실제 보기 다섯 개에서 골라 봐요. 여자가 이미 겪은 일을 떠올려요.", button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 2, [m("I lost my old one", "예전 것을 잃어버렸다"), " ", m("somewhere", "어딘가에서"), ". ", m("So", "그래서"), " ",
                         m("the student services office", "학생 지원실"), "에 ", m("I went to", "갔고"), " ", m("got a new one", "새것을 받았다"), "."],
          sv_new=sv_step("s2_basic_sv", ["I", "went", "the student services office", "got", "a new one"],
                         {"I": "S", "went": "V", "got": "V", "a new one": "O"},
                         {"the student services office": "그건 to 뒤, 어디로 갔는지 알려 주는 말이에요."},
                         "두 번째 문장은 주어 I, 동사 went와 got, got의 목적어 a new one이에요."),
          meaning_ids=["s2_office"])
add_basic(sentences, 3, [m("Do I need to bring", "내가 ~을 가져가야 하나요"), " ", m("for a new ID card", "새 학생증을 위해"), " ", m("my photo", "내 사진"), "?"],
          sv_new=sv_step("s3_basic_sv", ["I", "need to go", "there", "my photo"],
                         {"I": "S", "need to go": "V"},
                         {"there": "그건 '거기(학생 지원실)', 어디로 가는지예요.", "my photo": "그건 마지막 질문 안의 말이에요."},
                         "so 뒤 문장은 주어 I, 동사 need to go예요(가야 한다)."),
          meaning_after="s3_q")

SENSES = {
    2: [sense("so", "So I went", "그래서", "접속사 so (결과)"), sense("to", "went to the student services office", "~에", "전치사 to (방향)")],
    3: [sense("so", "so I need", "그래서", "접속사 so (결과)"),
        sense("to", "need to go", "~해야 (하다)", "need + to부정사"),
        sense("to", "need to bring", "~해야 (하다)", "need + to부정사"),
        sense("for", "for a new ID card", "~을 위해", "전치사 for + 명사 (목적)")],
}

WORDS = {"heard": "들었다", "got": "받았다, ~하게 했다", "student": "학생", "id": "신분증", "card": "카드", "reissued": "재발급된",
         "lost": "잃어버렸다", "old": "예전의", "one": "것", "went": "갔다", "services": "지원, 서비스", "office": "사무실",
         "new": "새로운", "mine": "내 것", "need": "~해야 하다", "go": "가다", "there": "거기", "bring": "가져가다", "photo": "사진",
         "actually": "사실"}

OPTIONS = [
    ("1", "I’m sorry, but you can’t use it as a credit card.", "미안하지만, 그걸 신용 카드로 쓸 수는 없어.", False),
    ("2", "Yes, I think it’d be great to take a group photo here.", "응, 여기서 단체 사진을 찍으면 좋을 것 같아.", False),
    ("3", "No need. You can have your photo taken on the spot.", "필요 없어. 그 자리에서 사진을 찍을 수 있어.", True),
    ("4", "Fortunately, I found my ID card at the Lost and Found.", "다행히 분실물 센터에서 내 학생증을 찾았어.", False),
    ("5", "Right. The student services office doesn’t reissue ID cards.", "맞아. 학생 지원실은 학생증을 재발급해 주지 않아.", False),
]
exam = {
    "question": "대화를 듣고, 남자의 마지막 말에 대한 여자의 응답으로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 4, "analysis_first": True, "wrong_rate": 42.2, "wrong_rank": 13,
    "glosses": [g("credit card", "신용 카드"), g("group photo", "단체 사진"), g("No need", "필요 없어"),
                g("have your photo taken", "사진을 찍다(찍히다)"), g("on the spot", "그 자리에서"), g("Fortunately", "다행히"),
                g("the Lost and Found", "분실물 센터"), g("reissue", "재발급하다")],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "남자의 마지막 질문(사진을 가져가야 하나)과 여자가 이미 겪은 일을 떠올리며 골라 봐요.",
        "정답이에요! 사진을 가져가야 하냐는 질문에, 직접 재발급받아 본 여자가 '필요 없어, 거기서 바로 찍어 줘'라고 답하는 게 자연스러워요.",
        "정답은 ③이에요. 'No need(필요 없어)'로 질문에 바로 답하고, 그 자리에서 사진을 찍을 수 있다고 이유를 덧붙여요.",
        {"1": "신용 카드 이야기는 대화와 상관없어요.",
         "2": "photo가 겹쳐서 헷갈렸죠. 하지만 단체 사진은 새 학생증과 상관없어요.",
         "4": "여자는 학생증을 찾은 게 아니라 새로 받았어요.",
         "5": "여자는 바로 그 학생 지원실에서 새 학생증을 받았어요. 재발급을 안 해 준다는 말은 앞뒤가 안 맞아요."},
        {"5": review(14.8,
                     "⑤는 '학생 지원실은 학생증을 재발급해 주지 않아'예요. 그런데 여자는 바로 그 학생 지원실에 가서 새 학생증을 받았다고 했어요(got a new one). 그리고 남자가 물은 건 사진을 가져가야 하는지였어요.",
                     panel=rows(("여자의 대답", "went to the student services office and got a new one", "그 사무실에서 새로 받았다", "hl"),
                                ("남자의 마지막 말", "Do I need to bring my photo", "사진을 가져가야 하나?", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 11번 (듣기 — 마지막 말에 대한 응답, 2점)",
    topic="듣기 응답 푸는 법: 누가 무엇을 했는지 → 마지막 말이 무엇을 묻는지 → 거기에 맞는 응답",
    method={"type": "listening_response", "labels": ["누가 무엇을 하는지", "마지막 말 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-student-id.svg", ("Lost ID", "잃어버린 학생증"), "→", ("New card", "새 학생증"),
                                       "새 학생증을 만들려면 무엇이 필요할까?", "2024년 3월 11번 도입 칠판"),
                      "alt": "칠판: Lost ID(잃어버린 학생증) → New card(새 학생증)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "학생증을 잃어버리면 새로 만들 때 무엇을 챙겨야 할까요? 이번엔 듣기 문제를 대본으로 같이 읽어 봐요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "듣기 응답 문제는 누가 무엇을 했는지, 마지막 말이 무엇을 묻는지 잡는 게 핵심이에요. 문장 아래 🔊 듣기로 소리도 들어 봐요."}}],
    exam=exam,
    key_words={"passage": [g("reissue", "재발급하다"), g("student services office", "학생 지원실"), g("bring", "가져가다"),
                           g("get + 물건 + p.p.", "물건이 ~되게 하다")],
               "options": [g("on the spot", "그 자리에서"), g("Lost and Found", "분실물 센터"), g("No need.", "필요 없어."),
                           g("have one's photo taken", "사진을 찍다")]},
    sentences=sentences, english="medium", concept="low")

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="듣기 응답 푸는 법",
       chunks={"I": "나는", "went": "갔다", "the student services office": "학생 지원실", "got": "받았다", "a new one": "새것",
               "need to go": "가야 한다", "there": "거기", "my photo": "내 사진"})
