"""2026년 3월 36번 레슨 + 대사를 만든다 (글의 순서, 3점).

레슨 JSON(content/tutor/policy-lessons/…)과 대사(content/tutor/policy-copy/dajung/…)는 이 스크립트의
생성물이다. 고칠 때는 여기를 고치고 다시 돌린 뒤 도장을 찍는다:

    python3 scripts/lessons/gen_moeui_2026_03_36.py
    npm run policy:copy stamp moeui-2026-03-36-conversation-stoppers

순서 문제 푸는 법(초안, 선생님 확인 전): ① 단락마다 요지 잡기 ② 단락 첫머리 단서(This, in this manner,
The problem)로 앞에 올 내용 예측하기 → 마지막에 순서를 고른다.
정답 ④ (C)-(A)-(B). 많이 고른 오답 ③ (B)-(C)-(A) 25.7% · ② (B)-(A)-(C) 19.8% —
주어진 글의 '도덕적 고려'와 (B)의 '도덕적으로 잘못'이 비슷해 보여 (B)로 바로 간 학생이 많다.
"""
import copy
import json
import os

ID = "moeui-2026-03-36-conversation-stoppers"
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
    "g_role": "moral considerations = conversation-stoppers (대화를 끝내 주는 것) · 콜론 뒤 'bring deliberations to a close'",
    "g_sign": "ask for justification(이유를 요구함) → has served us well(+) · 좋은 말 뒤엔 보통 '그런데 문제는…'",
    "g_next": "주어진 글이 '이유를 늘 물을 수 있다(+)'로 끝나면 다음엔 그 반전(문제)이 온다",
    "a_before": "(A) This is a problem → 앞에 어떤 '문제'가 나와야 한다",
    "a_solution": "(A) consideration-generator-squelchers = 더 이상의 생각을 바로 멈추게 하는 말",
    "b_before": "(B) in this manner → 앞에 '생각을 멈추게 하는 방식'이 나와야 한다",
    "b_then": "(B) 그 주장이 받아들여지면 더 이상 이유를 찾을 필요도 여지도 없다",
    "c_problem": "(C) The problem = 이유를 끝없이 물어서 결정을 못 한다",
    "c_after": "(C) The problem is that … → '이유를 늘 물을 수 있고 도움이 됐다'(+) 뒤의 반전",
}

GIVEN = ("Daniel Dennett argues that one benefit of having moral considerations in our conceptual repertoire is that "
         "they can serve as conversation-stoppers: their value is to bring deliberations to a close. We are rational "
         "creatures, always able to ask for justification, and this is a trait that has served us well in many contexts.")
A1 = "(A) This is potentially as much a problem for our own private deliberations as for our public interpersonal ones."
A2 = ("Dennett suggests that it is useful to have “consideration-generator-squelchers”: items that, once introduced, "
      "stop any further deliberation in its tracks.")
B1 = "(B) “That would be morally wrong!” would appear to work in this manner."
B2 = ("Once the claim is accepted then there is no need or room for seeking further justification: the action mustn’t "
      "be done, even if it is tempting, and that’s all there is to it.")
C1 = ("(C) The problem is that upon receiving a perfectly good answer we can always sensibly respond “Okay, but what "
      "justifies that?”—and we can potentially do so endlessly, never coming to a decision, forever hesitant and "
      "doubting, undone by our own rational capacity.")

sentences = [
    {
        "id": 1, "label": "주어진 글", "text": GIVEN,
        "model_translation": "Daniel Dennett은 우리의 개념적 레퍼토리에 도덕적 고려 사항들을 포함하는 것의 한 가지 이점은 그것들이 '대화 중단자'의 역할을 할 수 있다는 것이라고 주장하는데, 즉 그것들의 가치는 심사숙고를 끝내는 데 있다. 우리는 이성적인 피조물로, 항상 타당한 이유를 요구할 수 있으며, 이것은 많은 맥락에서 우리에게 상당히 도움이 되어 온 특성이다.",
        "teaching_value": "high",
        "glosses": [g("Daniel Dennett", "대니얼 데닛 · 철학자 이름"), g("argues", "주장하다"), g("one benefit", "한 가지 이점"),
                    g("moral considerations", "도덕적 고려 사항"), g("conceptual repertoire", "개념의 목록, 생각의 도구들"),
                    g("serve as", "~의 역할을 하다"), g("conversation-stoppers", "대화를 끝내는 것"),
                    g("their value", "그것들의 가치"), g("bring deliberations to a close", "심사숙고를 끝내다"),
                    g("rational creatures", "이성적인 존재"), g("ask for justification", "타당한 이유를 요구하다"),
                    g("trait", "특성"), g("has served us well", "우리에게 도움이 되어 왔다"), g("contexts", "맥락, 상황")],
        "steps": [
            choice("g_role",
                   "Dennett은 도덕적 고려 사항(moral considerations)이 어떤 역할을 한다고 할까요?",
                   [("o0", "대화를 시작하게 하는 역할", False), ("o1", "대화를 끝내 주는 역할", True), ("o2", "새로운 이유를 찾게 하는 역할", False)],
                   "콜론(:) 뒤 'their value is to bring deliberations to a close'를 봐요. close는 '끝'이에요.",
                   why="'conversation-stoppers'는 대화를 멈추는 것이에요. 콜론 뒤에서 'bring deliberations to a close', 고민을 끝낸대요.",
                   highlight=["conversation-stoppers", "bring deliberations to a close"], method=0),
            choice("g_sign",
                   "'항상 이유를 요구할 수 있다(always able to ask for justification)'를 글쓴이는 좋게 볼까요, 나쁘게 볼까요?",
                   [("o0", "좋게 본다 (+)", True), ("o1", "나쁘게 본다 (−)", False)],
                   "'this is a trait that has served us well'을 봐요. served us well은 '우리에게 도움이 됐다'예요.",
                   highlight=["always able to ask for justification", "has served us well"], method=0),
            show("g_turn",
                 "has served us well은 +예요. 순서 문제에서 이렇게 좋은 말로 끝나면, 다음엔 '그런데 문제는…' 같은 반전이 오기 쉬워요.",
                 button="다음",
                 signs=[{"text": "has served us well", "sign": "+"}],
                 tips=[{"label": "순서 문제 요령",
                        "text": "주어진 글의 마지막 문장이 다음 단락의 첫 문장과 이어져요. 단락 첫머리의 This, The problem, in this manner 같은 말이 앞 내용을 가리켜요."}],
                 method=1),
            choice("g_next",
                   "그럼 주어진 글 바로 다음에는 어떤 내용이 오면 자연스러울까요?",
                   [("o0", "'그건 도덕적으로 잘못이야!'라는 예", False), ("o1", "이유를 끝없이 물으면 생기는 문제", True),
                    ("o2", "이성은 늘 옳다는 칭찬", False)],
                   "주어진 글은 '이유를 늘 물을 수 있다(+)'로 끝나요. 그다음엔 반전이 오기 쉬워요.",
                   why="주어진 글은 '이유를 늘 물을 수 있고 도움이 됐다(+)'로 끝나요. 그 바로 뒤엔 그 반대, 즉 그게 끝없으면 생기는 문제가 와야 자연스러워요.",
                   method=1),
        ],
    },
    {
        "id": 2, "text": A1,
        "model_translation": "(A) 이것은 우리의 공적인 대인 간 심사숙고에서만큼이나 우리 자신의 사적인 심사숙고에서도 잠재적으로 문제이다.",
        "teaching_value": "high",
        "glosses": [g("This", "이것 · 앞에 나온 것을 가리켜요"), g("potentially", "잠재적으로, 어쩌면"),
                    g("as much", "~만큼이나 · as much A as B = B만큼 A도"), g("a problem", "문제"),
                    g("private deliberations", "사적인 고민"), g("public interpersonal ones", "다른 사람과의 공적인 고민")],
        "steps": [
            choice("a_before",
                   "(A)는 'This is … a problem'으로 시작해요. 그럼 (A) 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "어떤 '문제'에 대한 설명", True), ("o1", "문제를 멈추는 해결책", False), ("o2", "도덕적인 말의 예", False)],
                   "This는 앞에 나온 걸 가리켜요. 'This is a problem'이니 This가 가리키는 게 바로 '문제'예요.",
                   highlight=["This is potentially", "a problem"],
                   tips=[{"label": "as much A as B", "mark": "as much",
                          "text": "'B만큼이나 A도'예요. 여기서는 공적인 고민만큼이나 사적인 고민에서도 문제라는 말이에요."}],
                   method=1),
        ],
    },
    {
        "id": 3, "text": A2,
        "model_translation": "Dennett은 '고려 사항 생성기를 찍소리 못하게 하는 말'을 갖는 것이 쓸모 있다고 말하는데, 이는 일단 도입되면 어떤 그 이상의 심사숙고도 즉시 멈추게 하는 항목이다.",
        "teaching_value": "high",
        "glosses": [g("suggests", "말하다, 제안하다"), g("useful", "쓸모 있는"),
                    g("consideration-generator-squelchers", "고민을 만들어 내는 걸 멈추게 하는 말"),
                    g("items", "항목, 것들"), g("once introduced", "일단 꺼내면"),
                    g("stop any further deliberation", "더 이상의 고민을 멈추다"), g("in its tracks", "그 자리에서, 즉시")],
        "steps": [
            choice("a_solution",
                   "그 문제에 대해 Dennett은 무엇이 쓸모 있다고 할까요?",
                   [("o0", "더 좋은 이유를 찾는 방법", False), ("o1", "더 이상의 생각을 바로 멈추게 하는 말", True),
                    ("o2", "공적인 토론 규칙", False)],
                   "콜론 뒤 'items that … stop any further deliberation in its tracks'를 봐요.",
                   why="콜론 뒤를 봐요. 'stop any further deliberation in its tracks', 더 이상의 고민을 그 자리에서 멈추게 하는 것이래요.",
                   highlight=["stop any further deliberation in its tracks"],
                   faded=[", once introduced,"],
                   method=0),
        ],
    },
    {
        "id": 4, "text": B1,
        "model_translation": "(B) \"그것은 도덕적으로 잘못된 것일 거야!\"는 이러한 방식으로 작동하는 것처럼 보일 것이다.",
        "teaching_value": "high",
        "glosses": [g("That would be morally wrong!", "그건 도덕적으로 잘못된 일일 거야!"), g("would appear to", "~하는 것처럼 보일 것이다"),
                    g("work", "작동하다"), g("in this manner", "이런 방식으로 · 앞에 나온 방식")],
        "steps": [
            choice("b_before",
                   "'in this manner(이런 방식으로)'가 있어요. 그럼 (B) 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "이유를 끝없이 묻는 문제", False), ("o1", "Dennett이 누구인지 소개", False),
                    ("o2", "생각을 멈추게 하는 어떤 방식", True)],
                   "this manner는 앞에 나온 '방식'을 가리켜요. '그건 도덕적으로 잘못이야!'라는 말이 무엇처럼 작동하는지 생각해 봐요.",
                   why="'그건 도덕적으로 잘못이야!' 한마디면 고민이 끝나죠. 그러니 앞에는 그런 '고민을 멈추는 방식'이 나와야 해요.",
                   highlight=["in this manner"], method=1),
        ],
    },
    {
        "id": 5, "text": B2,
        "model_translation": "일단 그 주장이 받아들여지면, 더 이상의 타당한 이유를 찾을 필요도 여지도 없고, 그 행동은 비록 솔깃해도 해서는 안 되며, 그저 그뿐이다.",
        "teaching_value": "medium",
        "glosses": [g("Once", "일단 ~하면"), g("the claim", "그 주장"), g("is accepted", "받아들여지다"),
                    g("no need or room", "필요도 여지도 없음"), g("seeking further justification", "더 이상의 이유를 찾는 것"),
                    g("mustn’t be done", "해서는 안 된다"), g("tempting", "솔깃한, 유혹적인"),
                    g("that’s all there is to it", "그저 그뿐이다")],
        "steps": [
            choice("b_then",
                   "그 주장이 받아들여지면 어떻게 된대요?",
                   [("o0", "더 이상 이유를 찾을 필요가 없다", True), ("o1", "더 좋은 이유를 찾아야 한다", False),
                    ("o2", "다시 처음부터 고민한다", False)],
                   "'there is no need or room for seeking further justification'을 봐요.",
                   why="'no need or room for seeking further justification', 더 이상 이유를 찾을 필요도 여지도 없대요. 고민이 멈춰요.",
                   highlight=["no need or room for seeking further justification"],
                   tips=[{"label": "that’s all there is to it", "mark": "that’s all there is to it",
                          "text": "'그게 다야, 그저 그뿐이야'예요. 더 따질 게 없다는 말이에요."}],
                   method=0),
        ],
    },
    {
        "id": 6, "text": C1,
        "model_translation": "(C) 문제는 우리가 충분히 타당한 답변을 받자마자 언제든지 \"좋아, 그런데 무엇이 '그것'의 타당함을 보여 주는가?\"라고 분별 있게 응수할 수 있다는 점이고, 우리는 어쩌면 무한히 그렇게 할 수 있으며 결코 결정을 내리지 못하고, 영원히 망설이고 의심하며, 우리 자신의 이성적 역량에 의해 완전히 좌절하고 만다.",
        "teaching_value": "high",
        "glosses": [g("The problem is that", "문제는 ~라는 것이다"), g("upon receiving", "~을 받자마자"),
                    g("a perfectly good answer", "충분히 좋은 답"), g("sensibly", "분별 있게, 그럴듯하게"), g("respond", "응수하다"),
                    g("what justifies that?", "무엇이 그걸 정당화하지?"), g("endlessly", "끝없이"),
                    g("never coming to a decision", "결코 결정을 내리지 못하고"), g("hesitant", "망설이는"), g("doubting", "의심하는"),
                    g("undone by", "~ 때문에 무너진"), g("rational capacity", "이성적 능력")],
        "steps": [
            choice("c_problem",
                   "(C)가 말하는 문제는 무엇일까요?",
                   [("o0", "좋은 답을 듣지 못하는 것", False), ("o1", "도덕을 지키지 않는 것", False),
                    ("o2", "이유를 끝없이 물어서 결정을 못 하는 것", True)],
                   "대시(—) 뒤 'do so endlessly, never coming to a decision'을 봐요.",
                   why="좋은 답을 받아도 '그건 왜?'라고 또 물을 수 있대요. 그렇게 끝없이 물어서 결정을 못 하는 게 문제예요.",
                   highlight=["we can potentially do so endlessly, never coming to a decision"],
                   method=0),
            choice("c_after",
                   "'The problem is that'으로 시작하는 (C)는 어떤 말 바로 뒤에 오면 자연스러울까요?",
                   [("o0", "이유를 늘 물을 수 있고 그게 도움이 됐다는 말", True), ("o1", "'이것도 문제다'라는 말", False),
                    ("o2", "'그건 도덕적으로 잘못이야!'라는 예", False)],
                   "'The problem'은 앞의 좋은 말을 뒤집는 반전이에요. 앞에 좋은 말(+)이 있어야 해요.",
                   why="'The problem is that'은 앞의 좋은 말을 뒤집는 반전이에요. '이유를 늘 물을 수 있고 도움이 됐다(+)' 뒤에 와야 자연스러워요.",
                   highlight=["The problem is that"], method=1),
            show("c_go",
                 "단락마다 첫머리의 단서를 다 찾았어요. 이제 주어진 글 다음에 이어질 순서를 직접 골라 봐요.",
                 button="문제 풀러 갈게요",
                 panel={"kind": "structure", "rows": [
                     {"label": "주어진 글", "text": "… always able to ask for justification (+)", "ko": "이유를 늘 물을 수 있다", "tone": "hl2"},
                     {"label": "(A)", "text": "This is … a problem", "ko": "앞에 '문제'가 있어야"},
                     {"label": "(B)", "text": "… in this manner", "ko": "앞에 '멈추는 방식'이 있어야"},
                     {"label": "(C)", "text": "The problem is that …", "ko": "앞에 좋은 말(+)이 있어야"},
                 ]},
                 method=1),
        ],
    },
]

OPTIONS = [
    ("1", "(A)-(C)-(B)", False), ("2", "(B)-(A)-(C)", False), ("3", "(B)-(C)-(A)", False),
    ("4", "(C)-(A)-(B)", True), ("5", "(C)-(B)-(A)", False),
]

exam = {
    "question": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은? [3점]",
    "sentence": 1,
    "analysis_first": True,
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], **({"correct": True} if o[2] else {})} for o in OPTIONS],
    "brief": {
        "ask": "단락 첫머리의 단서(This, in this manner, The problem)를 떠올리며 순서를 골라 봐요.",
        "first_correct": "맞았어요!",
        "first_wrong": "아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.",
        "final_correct": "정답이에요!",
        "answer_explain": "정답이에요! 이유를 늘 물을 수 있다 → (C) 그게 끝없으면 문제 → (A) 이 문제엔 고민을 멈추는 말이 쓸모 있다 → (B) '그건 도덕적으로 잘못이야!'가 바로 그런 방식이에요.",
        "final_wrong": "정답은 ④예요.",
        "option_feedback": {
            "1": "(A)의 'This is a problem'은 앞에 '문제'가 나와야 해요. 주어진 글은 이유를 묻는 게 도움이 됐다는 좋은 말로 끝나요.",
            "2": "(B)의 'in this manner'가 받을 '고민을 멈추는 방식'이 주어진 글에는 아직 없어요.",
            "3": "주어진 글의 '도덕적 고려'와 (B)의 '도덕적으로 잘못'이 비슷해 보여서 헷갈렸죠. 하지만 (B)의 'in this manner'가 받을 방식이 아직 안 나왔어요.",
            "5": "(B)의 'in this manner'는 (A)의 '고민을 멈추게 하는 말'을 받아요. (B)가 (A)보다 먼저 올 수 없어요.",
        },
        "ask_first": "실제 시험처럼 풀어 봐요. 위 보기에서 답을 골라요.",
    },
}

lesson = {
    "id": ID, "kind": "policy", "version": "0.1",
    "source": "2026년 3월 고3 전국연합학력평가 영어 36번 (글의 순서, 3점)",
    "brief": {"topic": "순서 푸는 법: 단락마다 요지 잡기 → 단락 첫머리 단서로 앞 내용 예측하기", "closing": "수고 인사"},
    "method": {"type": "order", "labels": ["단락 요지 잡기", "연결 단서 찾기"], "intro_times": 3},
    "read_button": "분석하러 갈게요",
    "read_first": True,
    "intro": [
        {"id": "topic", "type": "say", "button": "네",
         "brief": {"say": "왜 '그건 도덕적으로 잘못이야!' 한마디에 고민이 멈출까요? 이번 글은 끝없는 고민과 그걸 멈추는 말을 다뤄요."}},
        {"id": "method1", "type": "say", "button": "좋아요",
         "brief": {"say": "순서 문제는 단락 첫머리의 단서가 앞 내용과 이어지는지 보는 거예요. This, The problem 같은 말이 무엇을 받는지 찾아볼게요."}},
    ],
    "exam": exam,
    "key_words": {
        # squelcher는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
        "passage": [g("moral", "도덕적인"), g("consideration", "고려 사항"), g("deliberation", "심사숙고"),
                    g("rational", "이성적인"), g("justification", "타당한 이유, 정당화"), g("trait", "특성"),
                    g("potentially", "잠재적으로"), g("interpersonal", "대인 간의"), g("further", "더 이상의"),
                    g("tempting", "솔깃한"), g("sensibly", "분별 있게"), g("hesitant", "망설이는"), g("capacity", "능력")],
        "options": [],
    },
    "context": {"mode": "paper_review", "exam_relevance": "high", "time_budget": "normal"},
    "item": {"english_difficulty": "high", "conceptual_difficulty": "high", "background_knowledge_required": "low",
             "exam_importance": "high", "teaching_value": "high", "intervention_density": "normal"},
    "sentences": sentences,
    "passage_on_try": True,
}

json.dump(lesson, open(f"{ROOT}/content/tutor/policy-lessons/{ID}.json", "w"), ensure_ascii=False, indent=2)

ref = json.load(open(f"{ROOT}/content/tutor/policy-copy/dajung/moeui-2026-03-21-music-researchers.json"))
steps = {st["id"]: copy.deepcopy(st["brief"]) for s in sentences for st in s["steps"]}
c = {
    "lesson": ID, "character": "dajung", "note": "생성물",
    "topic_intro": "순서 푸는 법",
    "closing": ref["closing"],
    "helps": {h["id"]: {"answer": h["brief"]} for s_ in sentences for h in s_.get("helps", [])},
    "steps": steps,
    "exam": {k: v for k, v in exam["brief"].items()},
    "intro": {i["id"]: dict(i["brief"]) for i in lesson["intro"]},
    "ending": {**ref["ending"], "wrong": "이번엔 한 번 헷갈렸으니 {weeks} 뒤에 다시 한번 볼 거예요."},
}
json.dump(c, open(f"{ROOT}/content/tutor/policy-copy/dajung/{ID}.json", "w"), ensure_ascii=False, indent=2)
print("ok", ID)
