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
import sys
import copy
import json
import os

ID = "moeui-2026-03-36-conversation-stoppers"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from order_tools import card, order_link  # noqa: E402


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


def sv(id, candidates, roles, ask, wrong_by, explain, wrong="그건 주어·동사·보어가 아니에요."):
    """읽은 뒤 덩어리째 주어·동사(+보어) 찾기 — 찾은 건 S·V·C 표시로 남는다"""
    return {"id": id, "type": "pick", "interaction": "word_pick", "shade": True, "no_unknown": True,
            "candidates": candidates, "answers": list(roles), "roles": roles,
            "brief": {"ask": ask, "wrong": wrong, "wrong_by": wrong_by, "more": "좋아요! {n}개 남았어요.",
                      "praise": "다 찾았어요!", "explain": explain}, "method": 0}


POINTS = {
    "g_role": "moral considerations = conversation-stoppers (대화를 끝내 주는 것) · 콜론 뒤 'bring deliberations to a close'",
    "g_next": "평소엔 이유를 따지는 게 좋지만(served us well in many contexts) 때로는 멈출 수 있는 게 좋다 → 다음은 끝없이 따질 때의 문제",
    "a_before": "(A) This is a problem → 앞에 어떤 '문제'가 나와야 한다",
    "a_meaning": "(A) consideration-generator-squelchers = 더 이상의 생각을 그 자리에서 멈추게 하는 것 (*풀이 단어)",
    "b_before": "(B) in this manner → 앞에 '생각을 멈추게 하는 방식'이 나와야 한다",
    "b_then": "(B) 그 주장이 받아들여지면 더 이상 이유를 찾을 필요도 여지도 없다",
    "c_problem": "(C) The problem = 이유를 끝없이 물어서 결정을 못 한다",
    "c_after": "(C) The problem is that … → '여러 상황에선 도움이 됐다'(인정) 뒤의 반전",
}

GIVEN = ("Daniel Dennett argues that one benefit of having moral considerations in our conceptual repertoire is that "
         "they can serve as conversation-stoppers: their value is to bring deliberations to a close. We are rational "
         "creatures, always able to ask for justification, and this is a trait that has served us well in many contexts.")
WE = GIVEN[GIVEN.index("We are"):]  # 주어진 글의 둘째 문장
A1 = "(A) This is potentially as much a problem for our own private deliberations as for our public interpersonal ones."
A2 = ("Dennett suggests that it is useful to have “consideration-generator-squelchers”: items that, once introduced, "
      "stop any further deliberation in its tracks.")
B1 = "(B) “That would be morally wrong!” would appear to work in this manner."
B2 = ("Once the claim is accepted then there is no need or room for seeking further justification: the action mustn’t "
      "be done, even if it is tempting, and that’s all there is to it.")
C1 = ("(C) The problem is that upon receiving a perfectly good answer we can always sensibly respond “Okay, but what "
      "justifies that?”—and we can potentially do so endlessly, never coming to a decision, forever hesitant and "
      "doubting, undone by our own rational capacity.")

# 주어진 글 칠판 — 읽은 데까지만, 핵심어 + 그림(이모지) 한 줄씩 쌓는다
_G_SCENES = [
    {"label": "Dennett의 주장", "icon": "⚖️", "en": "moral considerations", "ko": "도덕적 고려 사항(옳다·그르다를 따지는 생각)"},
    {"label": "역할", "icon": "🛑", "en": "= conversation-stoppers", "ko": "대화를 끝내 주는 것 · 고민을 끝냄(bring deliberations to a close)"},
    {"label": "평가", "icon": "👍", "en": "one benefit · their value", "ko": "이점 · 가치 → 멈추는 게 좋은 것(+)"},
]


def G_STORY(n):
    fresh_from = 0
    upto = 3
    return {"kind": "story", "title": "칠판",
            "scenes": [{**x, "fresh": i >= fresh_from} for i, x in enumerate(_G_SCENES[:upto])]}


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
                    g("trait", "특성"), g("has served us well", "우리에게 도움이 되어 왔다"), g("contexts", "맥락, 상황"),
                    g("is", "~이다"), g("having", "가지고 있는 것"), g("of having moral considerations", "도덕적 고려 사항을 갖는 것의"),
                    g("that they can serve as conversation-stoppers", "그것들이 대화를 끝내는 역할을 할 수 있다는 것")],
        "steps": [
            # 읽자마자 뜻을 묻지 않는다 — 주어·동사로 뼈대부터 (2026-10-15 선생님: 바로 물으니 갑작스럽다)
            sv("g_sv", ["Daniel Dennett", "argues", "one benefit", "moral considerations", "conversation-stoppers"],
               {"Daniel Dennett": "S", "argues": "V"},
               "주어진 글이 길어요. 먼저 첫 문장의 주어(S)와 동사(V)를 찾아볼까요?",
               {"one benefit": "그건 argues that 뒤, Dennett이 주장하는 내용 안의 주어예요. 문장 맨 앞을 봐요."},
               "주어는 Daniel Dennett, 동사는 argues(주장한다)예요. that 뒤가 그 주장이에요."),
            sv("g_claim_sv", ["one benefit", "of having moral considerations", "is", "that they can serve as conversation-stoppers", "their value"],
               {"one benefit": "S", "is": "V", "that they can serve as conversation-stoppers": "C"},
               "argues that 뒤가 Dennett의 주장이에요. 그 안의 주어(S), 동사(V), 보어(C)를 찾아볼까요?",
               {"of having moral considerations": "그건 one benefit을 꾸미는 말이에요. 주어는 그 앞이에요.",
                "their value": "그건 콜론(:) 뒤 문장의 주어예요. 콜론 앞에서 찾아봐요."},
               "주어는 one benefit(한 가지 이점), 동사는 is, 보어는 that they can serve as conversation-stoppers예요."),
            choice("g_role",
                   "찾은 뼈대를 보면, Dennett은 도덕적 고려 사항(moral considerations)이 어떤 역할을 한다고 할까요?",
                   [("o0", "대화를 시작하게 하는 역할", False), ("o1", "대화를 끝내 주는 역할", True), ("o2", "새로운 이유를 찾게 하는 역할", False)],
                   "콜론(:) 뒤 'their value is to bring deliberations to a close'를 봐요. close는 '끝'이에요.",
                   why="'conversation-stoppers'는 대화를 멈추는 것이에요. 콜론 뒤에서 'bring deliberations to a close', 고민을 끝낸대요.",
                   highlight=["moral considerations", "conversation-stoppers", "to a close"], method=0),
            # 보통은 나쁜 말(대화를 멈추게 함)인데 이 글은 좋게 본다 — 평가어(benefit, value)로 짚는다 (2026-10-15 선생님, 공통 규칙)
            choice("g_value_sign",
                   "그럼 글쓴이는 conversation-stoppers(대화를 멈추게 하는 것)를 좋게 볼까요, 나쁘게 볼까요?",
                   [("o0", "좋게 본다 (+)", True), ("o1", "나쁘게 본다 (−)", False)],
                   "같이 쓰인 one benefit(한 가지 이점), their value(그것들의 가치)를 봐요.",
                   why="one benefit(한 가지 이점), their value(그것들의 가치)를 봐요. 글쓴이가 이걸 '이점', '가치'라고 불러요.",
                   highlight=["one benefit", "conversation-stoppers", "their value"], method=0),
            # 역할·평가 질문 뒤 세 번째 설명 — 말로 늘어놓지 않고 칠판에 (2026-10-16 선생님: 설명·뜻 질문이 3번 이어지면 칠판, 주어·동사 찾기는 안 셈)
            show("g_value_note",
                 "보통 대화를 멈추는 건 나쁘게 보죠. 여기선 이점(benefit)·가치(value)라고 불러서 좋은 것(+)이에요.",
                 button="다음",
                 highlight=["one benefit", "their value"],
                 signs=[{"text": "conversation-stoppers", "sign": "+"}],
                 panel=G_STORY(2),
                 method=0),
            # We are 문장 — We = 인간 → 앞(멈추는 게 좋다)과 좀 반대인지 묻고 → 칠판에 「평소 / 때때로」 (2026-10-15 선생님)
            show("g_we",
                 "We는 우리 인간이에요. 인간은 이성적이라 늘 이유를 찾을 수 있고, 그게 많은 상황에서 도움이 됐대요.",
                 button="다음", highlight=["We are", "ask for justification", "has served us well"],
                 bracket=WE, method=0),
            # 어느 문장을 묻는지 분명하게 — We are 문장만 띄운다 (2026-10-15 선생님)
            choice("g_contrast",
                 "We are 문장은 앞 문장의 '대화를 멈추는 게 좋다'와 어떤 관계일까요?",
                 [("o0", "같은 내용을 이어 가는 말", False), ("o1", "대비되는 내용", True)],
                 "앞 문장은 멈추는 게 좋다, We are 문장은 이유를 따지는 게 도움이 됐다예요.",
                 why="앞 문장은 '멈추는 게 좋다', We are 문장은 '이유를 계속 따지는 게 도움이 됐다'예요. 서로 어긋나는 면이 있어요.",
                 highlight=["We", "rational creatures", "ask for justification", "has served us well"], bracket=WE, method=0),
            show("g_board",
                 "칠판에 정리해 볼게요. 평소엔 이유를 따지는 게 도움이 되지만, 때로는 멈추는 게 좋아요.",
                 button="다음",
                 panel={"kind": "groups", "title": "칠판",
                        "left": {"label": "평소", "words": [{"text": "ask for justification", "ko": "이유를 따지면 도움이 됨"}]},
                        "right": {"label": "때때로", "words": [{"text": "conversation-stoppers", "ko": "멈추는 게 좋음"}]},
                        "between": "↔"},
                 tips=[{"label": "순서 문제 요령",
                        "text": "주어진 글의 마지막 문장이 다음 단락의 첫 문장과 이어져요. 단락 첫머리의 This, The problem, in this manner 같은 말이 앞 내용을 가리켜요."}],
                 method=1),
            choice("g_next",
                   "그럼 주어진 글 바로 다음에는 어떤 내용이 오면 자연스러울까요?",
                   [("o0", "'그건 도덕적으로 잘못이야!'라는 예", False), ("o1", "이유를 끝없이 물으면 생기는 문제", True),
                    ("o2", "이성은 늘 옳다는 칭찬", False)],
                   "평소엔 이유를 따지는 게 좋지만, 때로는 멈추는 게 좋을 수도 있대요. 이유를 따지는 게 언제 곤란해질지 생각해 봐요.",
                   why="이유를 늘 따질 수 있는 건 많은 상황에서 도움이 되지만, 끝없이 따지면 곤란해질 수 있어요. 다음엔 그 곤란한 점이 와야 자연스러워요.",
                   method=1),
            # 주어진 글의 마지막 화면에서 — (A) 문장이 뜨기 전에 (2026-10-15 선생님)
            show("paper_order",
                 "이제 (A)·(B)·(C)를 시험지 순서대로 읽어요. 단락마다 첫머리와 끝을 잘 봐 두면 좋아요.",
                 button="(A)부터 읽어 볼게요", method=1),
        ],
    },
    {
        "id": 2, "text": A1,
        "model_translation": "(A) 이것은 우리의 공적인 대인 간 심사숙고에서만큼이나 우리 자신의 사적인 심사숙고에서도 잠재적으로 문제이다.",
        "teaching_value": "high",
        "glosses": [g("This", "이것 · 앞에 나온 것을 가리켜요"), g("potentially", "잠재적으로, 어쩌면"),
                    g("as much", "~만큼이나 · as much A as B = B만큼 A도"), g("a problem", "문제"),
                    g("private deliberations", "사적인 고민"), g("public interpersonal ones", "공적인 대인 간의 것들(= deliberations, 고민들)"), g("ones", "것들 · 여기서는 deliberations(고민들)"), g("interpersonal", "대인 간의 · inter(~ 사이에) + personal(사람의)")],
        "steps": [
            # 시험지 순서대로 (A)→(B)→(C)를 읽는다 — 실제 글 순서가 아니라 어색할 수 있다고 한 번 알려 준다
            choice("a_before",
                   "(A)는 'This is … a problem'으로 시작해요. 그럼 (A) 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "어떤 '문제'에 대한 설명", True), ("o1", "문제를 멈추는 해결책", False), ("o2", "도덕적인 말의 예", False)],
                   "This는 앞에 나온 걸 가리켜요. 'This is a problem'이니 This가 가리키는 게 바로 '문제'예요.",
                   highlight=["This is potentially", "a problem"],
                   tips=[{"label": "as much A as B", "mark": "as much",
                          "text": "'B만큼이나 A도'예요. 여기서는 공적인 고민만큼이나 사적인 고민에서도 문제라는 말이에요."},
                         {"label": "interpersonal", "mark": "interpersonal",
                          "text": "inter(~ 사이에) + personal(사람의) → '사람들 사이의, 대인 간의'예요."},
                         {"label": "ones", "mark": "ones",
                          "text": "ones는 앞에 나온 명사를 다시 가리켜요. 여기서는 deliberations(고민들) — public interpersonal ones는 '사람들 사이의 공적인 고민들'이에요."}],
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
            # 둘째 문장은 부연 — 핵심어만 짚는다 (2026-10-15 선생님)
            show("a_meaning",
                 "(A)는 메인 문장 하나와 그걸 뒷받침하는 문장이에요. 뒷받침 문장은 핵심어만 보면, 고민(deliberation)을 멈추게 하는(stop) 것들(items)이 쓸모 있대요(it is useful).",
                 button="다음", highlight=["it is useful", "consideration-generator-squelchers", "items", "stop", "deliberation"],
                 faded=[", once introduced,"],
                 panel={"kind": "structure", "rows": [
                     {"label": "메인 문장", "text": "This is … a problem", "ko": "이것(앞의 무엇)은 문제다", "tone": "hl"},
                     {"label": "뒷받침", "text": "it is useful … squelchers: items that … stop … deliberation", "ko": "고민을 멈추게 하는 것들이 쓸모 있다", "tone": "hl2"},
                 ]},
                 meaning_check=True, method=0),
            # 메인(problem)과 뒷받침(squelchers)의 관계 — 문제 −, 멈추는 것 + → 해결, 어떻게 보면 대비 (2026-10-15 선생님)
            choice("a_relation",
                   "a problem과 squelchers(생각을 멈추게 하는 것)는 어떤 관계일까요?",
                   [("o0", "squelchers가 그 문제를 더 키운다", False), ("o1", "squelchers가 그 문제를 해결해 준다", True),
                    ("o2", "둘은 서로 상관없다", False)],
                   "squelchers는 useful(쓸모 있다)이라고 했어요.",
                   why="squelchers는 useful(쓸모 있다), 즉 좋은 쪽(+)이에요. 문제(−)를 풀어 주는 쪽이에요.",
                   highlight=["a problem", "it is useful", "consideration-generator-squelchers"], method=0),
            show("a_relation_note",
                 "a problem은 −, squelchers는 useful이니 +예요. 그래서 squelchers는 그 문제를 해결해 주는 관계, 어떻게 보면 대비예요.",
                 button="다음",
                 signs=[{"text": "a problem", "sign": "−"}, {"text": "problem", "sign": "−"}, {"text": "consideration-generator-squelchers", "sign": "+"}],
                 method=0),
            # 단락 끝 — 다음에 올 내용 예측 (순서 틀: 첫·끝 문장만 자세히)
            choice("a_next",
                   "(A)는 '생각을 멈추게 하는 말이 쓸모 있다'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "이유를 끝없이 묻는 문제", False), ("o1", "그런 말이 실제로 어떻게 쓰이는지 예", True),
                    ("o2", "Dennett이 누구인지 소개", False)],
                   "쓸모 있는 '말'을 소개했으면, 다음엔 그런 말의 예가 오기 쉬워요.",
                   why="생각을 멈추는 '말'이 쓸모 있다고 했으니, 다음엔 그런 말의 예가 나와야 자연스러워요.",
                   method=1),
        ],
    },
    {
        "id": 4, "text": B1,
        "model_translation": "(B) \"그것은 도덕적으로 잘못된 것일 거야!\"는 이러한 방식으로 작동하는 것처럼 보일 것이다.",
        "teaching_value": "high",
        "glosses": [g("That would be morally wrong!", "그건 도덕적으로 잘못된 일일 거야!"), g("would appear to", "~하는 것처럼 보일 것이다"),
                    g("work", "작동하다"), g("in this manner", "이런 방식으로 · 앞에 나온 방식")],
        "steps": [
            # work·manner는 질문 말고 Tip으로만 — 늘어진다 (2026-10-15 선생님)
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
            # (B)도 통째로 — 메인 문장(in this manner)과 뒷받침(Once the claim …) (2026-10-15 선생님)
            # 첫 문장에 집중 — 설명은 한 줄, 표는 뺀다 (2026-10-16 선생님: 너무 길고 갑자기 쏟아낸다)
            show("b_then",
                 "첫 문장부터 봐요. '그건 도덕적으로 잘못이야!'라는 말이 이런 방식으로(in this manner) 효과를 낸대요(work). 어떤 방식인지는 다음 문장에 나와요.",
                 button="다음", highlight=["morally wrong", "in this manner"],
                 tips=[{"label": "Once", "mark": "Once", "text": "'일단 ~하면'이에요. '한 번'이 아니에요."},
                       {"label": "room", "mark": "room", "text": "'여지'예요. '방'이 아니에요."},
                       {"label": "even if", "mark": "even if", "text": "'비록 ~일지라도'예요."},
                       {"label": "that’s all there is to it", "mark": "that’s all there is to it",
                        "text": "'그게 다야, 그저 그뿐이야'예요. 더 따질 게 없다는 말이에요."}],
                 method=0),
            # in this manner만 보고는 「어떤 방식」인지 모른다 — 뒷받침 문장에서 「받아들이면 어떻게 되나」를 글로 직접 확인 (2026-10-16 선생님: (B) 설명이 이해 안 됨 → 추상적인 「어떤 방식」 대신 문장에 있는 것을 묻는다)
            choice("b_manner_kind",
                   "다음 문장을 봐요. 그 말을 받아들이고 나면(Once the claim is accepted) 어떻게 된대요?",
                   [("o0", "이유를 더 찾아봐야 한다", False), ("o1", "더 이상 이유를 찾을 필요가 없다", True),
                    ("o2", "그 행동을 해도 된다", False)],
                   "no need or room 뒤를 봐요. 필요(need)도 여지(room)도 없대요.",
                   why="'잘못이야!' 한마디면 더 따지지 않고 생각이 거기서 멈춰요. 이게 in this manner(이런 방식)예요.",
                   highlight=["Once the claim is accepted"], method=1),
            choice("b_before",
                   "this manner는 앞에서 이미 나온 방식을 가리켜요. 그럼 (B) 바로 앞에는 어떤 말이 있어야 할까요?",
                   [("o0", "이유를 끝없이 물을 수 있다는 문제", False),
                    ("o1", "생각을 그 자리에서 멈추게 하는 말이 쓸모 있다", True),
                    ("o2", "Dennett이 누구인지 소개", False)],
                   "'잘못이야!'처럼 생각을 멈추게 하는 말이 앞에서 먼저 나와야 '이런 방식'이라고 가리킬 수 있어요.",
                   why="(B)는 생각을 멈추게 하는 말의 예예요. 그러니 앞에는 '그런 말이 쓸모 있다'가 먼저 나와야 해요.",
                   highlight=["in this manner"],
                   tips=[{"label": "would appear to", "mark": "appear to",
                          "text": "'~처럼 보이다'(= seem to)예요. '나타나다'가 아니에요."},
                         {"label": "work", "mark": "work", "text": "여기서는 '효과가 있다, 작동하다'예요. '일하다'가 아니에요."},
                         {"label": "manner", "mark": "manner", "text": "'방식, 방법'이에요. 예절(매너)이 아니에요. in this manner = 이런 방식으로."}],
                   method=1),
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
                   highlight=["problem", "we", "can", "respond", "what justifies", "endlessly", "never", "decision", "doubting"],
                   tips=[{"label": "upon receiving", "mark": "upon receiving", "text": "'~을 받자마자'예요."},
                         {"label": "undone", "mark": "undone",
                          "text": "undo(되돌리다)에서 왔지만 여기서는 '무너진, 망가진'이에요. undone by ~ = ~ 때문에 무너진."}],
                   method=0),
            # 선생님 표시판: (C)는 − 말이 이어진다
            show("c_minus",
                 "(C)에는 부정적인 말(−)이 계속 이어져요. 끝없이 묻고(endlessly), 결정을 못 하고(never coming to a decision), 망설이고 의심해요(hesitant, doubting).",
                 button="다음",
                 signs=[{"text": "The problem is that", "sign": "−"}, {"text": "what justifies that", "sign": "−"},
                        {"text": "endlessly", "sign": "−"}, {"text": "never coming to a decision", "sign": "−"},
                        {"text": "hesitant", "sign": "−"}, {"text": "doubting", "sign": "−"}],
                 method=0),
            choice("c_after",
                   "'The problem is that'으로 시작하는 (C)는 어떤 말 바로 뒤에 오면 자연스러울까요?",
                   [("o0", "이유를 늘 물을 수 있고 그게 도움이 됐다는 말", True), ("o1", "'이것도 문제다'라는 말", False),
                    ("o2", "'그건 도덕적으로 잘못이야!'라는 예", False)],
                   "'The problem'은 앞에서 일단 인정한 말을 뒤집는 반전이에요. 앞에 '도움이 됐다' 같은 인정이 있어야 해요.",
                   why="'The problem is that'은 앞에서 인정한 말을 뒤집는 반전이에요. '늘 이유를 물을 수 있고 여러 상황에선 도움이 됐다' 뒤에 와야 자연스러워요.",
                   highlight=["The problem is that"], method=1),
            order_link(
                card("given", "주어진 글", last=("… always able to ask for justification … has served us well", "늘 이유를 물을 수 있고, 그게 도움이 됐다")),
                [card("A", "(A)", first=("This is potentially as much a problem …", "이것은 … 문제다"),
                      last=("… stop any further deliberation in its tracks", "더 이상의 생각을 그 자리에서 멈추게 한다")),
                 card("B", "(B)", first=("“That would be morally wrong!” would appear to work in this manner", "'도덕적으로 잘못이야!'가 이런 방식으로 작동한다"),
                      last=("… and that’s all there is to it", "그저 그뿐이다")),
                 card("C", "(C)", first=("The problem is that …", "문제는 ~라는 것이다"),
                      last=("… undone by our own rational capacity", "자신의 이성 능력 때문에 무너진다"))],
                ["C", "A", "B"],
                "주어진 글 끝(여러 상황에선 도움이 됐다, 인정) → (C) The problem(반전) → (A) This is a problem, 멈추는 말이 쓸모 있다 → (B) in this manner(그런 방식) 순서예요."),
            # 보기를 다시 풀게 하지 않는다 — 맞춘 순서가 몇 번 보기인지 보여 준다 (2026-10-16 선생님)
            show("c_go",
                 "직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?",
                 button="문제 풀러 갈게요", method=1),
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
            "1": "(A)의 'This is a problem'은 앞에 '문제'가 나와야 해요. 주어진 글은 이유를 묻는 게 여러 상황에선 도움이 됐다는 인정으로 끝나요.",
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
    "images": {"topic": {"src": "/assets/topic-why-stop.svg", "alt": "칠판: Why?(왜?)가 계속되다가 Morally wrong!(도덕적으로 잘못!) 표지판에서 멈춘다", "kind": "drawing"}},
    "intro": [
        {"id": "topic", "type": "say", "button": "네", "image": "topic",
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

# (A) 단락은 통째로 — 문장마다 쪼개 읽지 않는다. 첫 문장(This is … a problem)이 열쇠, 둘째 문장은 부연 (2026-10-15 선생님)
_a1, _a2 = sentences[1], sentences[2]
_a1["text"] = f"{A1} {A2}"
_a1["model_translation"] = f"{_a1['model_translation']} {_a2['model_translation']}"
_a1["glosses"] = _a1["glosses"] + [x for x in _a2["glosses"] if x["en"] not in {y["en"] for y in _a1["glosses"]}]
_a1["steps"] = _a1["steps"] + _a2["steps"]
sentences.remove(_a2)
# (B)도 통째로 — 첫 문장(in this manner)이 열쇠, 둘째 문장은 뒷받침
_b1, _b2 = sentences[2], sentences[3]
_b1["text"] = f"{B1} {B2}"
_b1["model_translation"] = f"{_b1['model_translation']} {_b2['model_translation']}"
_b1["glosses"] = _b1["glosses"] + [x for x in _b2["glosses"] if x["en"] not in {y["en"] for y in _b1["glosses"]}]
_b1["steps"] = _b1["steps"] + _b2["steps"]
sentences.remove(_b2)
for _i, _s in enumerate(sentences, 1):
    _s["id"] = _i

# 끊어읽기 — 「/ 끊어읽기」를 누르면 이 말들 뒤에 / (2026-10-16 선생님: 긴 문장을 의미 덩어리로 읽는 법을 모른다)
SLASHES = {
    1: ["Dennett argues", "conceptual repertoire", "repertoire is", "conversation-stoppers:", "to a close.", "rational creatures,",
        "ask for justification,", "is a trait", "served us well"],
    2: ["as much a problem", "private deliberations", "Dennett suggests", "it is useful", "squelchers”:", "items",
        "once introduced,", "further deliberation"],
    3: ["morally wrong!”", "appear to work", "in this manner.", "Once the claim is accepted", "no need or room", "further justification:",
        "mustn’t be done,", "is tempting,"],
    4: ["The problem is", "a perfectly good answer", "sensibly respond", "justifies that?”—", "do so endlessly,",
        "to a decision,", "and doubting,"],
}
for _sid, _cuts in SLASHES.items():
    _s = next(x for x in sentences if x["id"] == _sid)
    for _c in _cuts:
        assert _s["text"].count(_c) == 1, (_sid, _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    _s["slashes"] = _cuts

# 초급 기본 — 문장마다 「주어·동사 찾기 + 뜻 알려 주기」 또는 「해석 맞추기」 중 하나 (2026-10-15 선생님).
# 같은 자리(slot)에 두 방식을 두고 최근에 덜 한 쪽을 낸다. 긴 문장(20단어~)의 맞추기는 핵심어만 모은 문장으로.
# 맞추기를 하면 주어·동사 찾기와 뜻 확인(meaning_check)은 건너뛴다
from beginner import _in_order, add_that_sv, share_tips, sv_ask  # noqa: E402


def basic(sid, sv_cands, roles, sv_wrong_by, sv_explain, meaning, match_ko, match_display=None, after=None, own_meaning=True):
    s_ = next(x for x in sentences if x["id"] == sid)
    slot = f"s{sid}_basic"
    sv_step = sv(f"s{sid}_basic_sv", sv_cands, roles, sv_ask(roles), sv_wrong_by, sv_explain)
    sv_step.update({"levels": ["초"], "slot": slot})
    mean = show(f"s{sid}_basic_meaning", meaning, button="다음", levels=["초"], meaning_check=True)
    slots = [x for x in match_ko if not isinstance(x, str)]
    order = (match_display or s_["text"])
    match = {
        "id": f"s{sid}_match", "type": "pick", "interaction": "word_pick", "levels": ["초"], "slot": slot,
        "candidates": _in_order(order, [x["en"] for x in slots]),
        "answers": [x["en"] for x in slots],
        "match": {"ko": match_ko},
        "brief": {"ask": "영어 덩어리를 끌어다 맞는 한국어 칸에 놓아 볼까요?" if not match_display else
                  "핵심어만 모았어요. 영어 덩어리를 끌어다 맞는 한국어 칸에 놓아 볼까요?",
                  "wrong": "그 칸은 '{ko}'예요. 다른 덩어리를 놓아 봐요.", "more": "좋아요! {n}개 남았어요.",
                  "praise": "다 맞췄어요!", "explain": meaning},
        "method": 0,
    }
    if match_display:
        match["display"] = match_display
    steps = s_["steps"]
    steps[0:0] = [sv_step, match]
    share_tips(steps, [sv_step, match])
    if not own_meaning:
        # 모두에게 보이는 뜻 짚기가 이미 있다 (meaning_check — 맞추기를 하면 건너뜀)
        pass
    elif after:
        # 이미 있는 뜻 질문 뒤에 뜻을 풀어 준다 — 질문 전에 답을 말하지 않는다. 그 질문도 뜻 확인이라 맞추기를 하면 건너뛴다
        i = next(i for i, x in enumerate(steps) if x["id"] == after)
        steps[i]["meaning_check"] = True
        steps.insert(i + 1, mean)
    else:
        steps.insert(2, mean)


def m(en, ko):
    return {"en": en, "ko": ko}


basic(2, ["This", "is", "a problem", "our own private deliberations", "our public interpersonal ones"],
      {"This": "S", "is": "V", "a problem": "C"},
      {"our own private deliberations": "그건 for 뒤의 말이에요. 어디에서 문제인지 알려 줘요.",
       "our public interpersonal ones": "그건 for 뒤의 말이에요. 어디에서 문제인지 알려 줘요."},
      "주어는 This, 동사는 is, 보어는 a problem(문제)이에요.",
      "이것(This)은 다른 사람과의 공적인 고민만큼이나 혼자 하는 사적인 고민에서도 문제가 될 수 있다는 뜻이에요.",
      [m("This", "이것은"), " ", m("a problem", "문제"), "다. 그래서 ", m("deliberation", "고민"), "을 ", m("stop", "멈추게 하는"), " ",
       m("items", "것들"), "이 ", m("it is useful", "쓸모 있다"), "."])
basic(3, ["That would be morally wrong", "would appear to work", "in this manner"],
      {"That would be morally wrong": "S", "would appear to work": "V"},
      {"in this manner": "그건 '어떻게' 작동하는지 알려 주는 말이에요."},
      "주어는 “That would be morally wrong!”이라는 말, 동사는 would appear to work(작동하는 것 같다)예요.",
      "'그건 도덕적으로 잘못이야!'라는 말이 이런 방식으로 작동하는 것 같다는 뜻이에요. in this manner(이런 방식)는 앞에 나온 방식을 가리켜요.",
      [m("That would be morally wrong", "'그건 도덕적으로 잘못이야!'라는 말은"), " ", m("in this manner", "이런 방식으로"), " ",
       m("would appear to work", "작동하는 것 같다"), "."],
      match_display=B1)
basic(4, ["The problem", "is", "a perfectly good answer", "we", "can always sensibly respond"],
      {"The problem": "S", "is": "V"},
      {"we": "그건 that 뒤 덩어리 안의 주어예요. 문장 맨 앞을 봐요.", "can always sensibly respond": "그건 that 뒤 덩어리 안의 동사예요.",
       "a perfectly good answer": "그건 upon receiving(~을 받자마자) 뒤의 말이에요."},
      "주어는 The problem(문제), 동사는 is예요. that 뒤가 그 문제의 내용이에요.",
      "문제는, 좋은 답을 들어도 우리는 언제든 '그건 왜?'라고 또 물을 수 있다는 거예요. 그렇게 끝없이 물으면 결정을 못 내리고 계속 망설이게 돼요.",
      [m("The problem", "문제는"), " ", m("what justifies that", "'무엇이 그걸 정당화하지?'라고"), " ",
       m("we can always respond", "우리가 언제든 응수할 수 있다"), "는 것 — ", m("endlessly", "끝없이"), " 그래서 ",
       m("never coming to a decision", "결정을 내리지 못한다"), "."],
      match_display="(C) The problem is that we can always respond “what justifies that?”—endlessly, never coming to a decision.",
      after="c_problem")

# (C)는 that 안이 핵심 — 메인 주어·동사(The problem / is) 다음 that 안의 주어·동사 (2026-10-16 선생님, 공통)
add_that_sv(sentences, 4, "s4_basic_sv", "s4_that_sv", ["a perfectly good answer", "we", "can always sensibly respond"],
            {"we": "S", "can always sensibly respond": "V"},
            {"a perfectly good answer": "그건 upon receiving(~을 받자마자) 뒤의 말이에요."},
            "that 안의 주어는 we(우리), 동사는 can always sensibly respond(언제든 그럴듯하게 응수할 수 있다)예요. 응수하는 말은 “Okay, but what justifies that?”예요.")

# 찾기 후보 덩어리 뜻 — 없으면 채운다 (화면에서 따로 누를 수 있어야)
CHUNKS = {
    "is": "~이다", "our own private deliberations": "우리 자신의 사적인 고민", "our public interpersonal ones": "우리의 공적인 대인 간의 것들(= deliberations, 고민들)",
    "Dennett": "데닛(철학자)", "it": "그것(가주어)", "is useful": "쓸모 있다", "items that stop any further deliberation": "더 이상의 고민을 멈추게 하는 것들",
    "would appear to work": "작동하는 것처럼 보이다", "there is": "~이 있다", "the action": "그 행동",
    "Once the claim is accepted": "일단 그 주장이 받아들여지면", "further justification": "더 이상의 이유", "no need": "필요가 없음",
    "The problem": "문제", "we": "우리", "can always sensibly respond": "언제든 그럴듯하게 응수할 수 있다",
    "we can always respond": "우리는 언제든 응수할 수 있다",
    "it is useful": "쓸모 있다", "deliberation": "고민, 숙고", "stop": "멈추게 하다",
    "That would be morally wrong": "그건 도덕적으로 잘못된 일일 거야",
    "what justifies that": "무엇이 그걸 정당화하지",
}
next(x for x in sentences if x["id"] == 4)["glosses"].append(g("always", "언제나"))
for s_ in sentences:
    have = {x["en"] for x in s_["glosses"]}
    for st in s_["steps"]:
        for c_ in ([] if st.get("order") else st.get("candidates", [])):
            if c_ not in have:
                s_["glosses"].insert(0, g(c_, CHUNKS[c_]))
                have.add(c_)

# 칠판 정리 — 2~3문장마다 지금까지 상황을 칠판에 (공통 틀)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_boards import add_story_boards  # noqa: E402
add_story_boards(ID, lesson["sentences"])

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
