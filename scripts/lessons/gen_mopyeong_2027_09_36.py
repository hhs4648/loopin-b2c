"""2026년 9월 모의평가(2027학년도, 평가원) 36번 레슨 + 대사를 만든다 (글의 순서, 2점). 오답률 30% · Top 9 (메가스터디 풀서비스 채점 기준).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_36.py   (→ npm run policy:copy stamp <id> → npx vitest run src/tutor/policy)

틀: docs/tutor/templates/order.md — 주어진 글의 끝 → 단락 첫머리(앞에 무엇?) → 단락 끝(다음에 무엇?) → 순서 잇기.
정답 ③ (B)-(C)-(A). 많이 고른 오답 ② (B)-(A)-(C) 12% · ④ (C)-(A)-(B) 10%.
② — (B)의 '통화 수대로 급여'와 (A)의 '보상은 측정하기 쉬운 한 측면에만'이 비슷해 보여 바로 이었다. 그러나 (C) Such mixed signals는
(B)의 두 신호('고객 응대가 가장 중요하다'는 말 ↔ '빨리 하라'는 급여)를 받아야 하고, (A)는 (C) 끝 물음 what should be rewarded?를 받는다.
④ — 주어진 글에는 신호가 하나(관리자의 말)뿐이라 Such mixed signals가 받을 것이 없다. (B)의 That이 그 말을 받는다.
해설지 해석·Words and Phrases와 대조함 (content/tutor/exam-source/2027-09-평가원/해설.txt) — multidimensional '다차원적인', compensation '보상',
aspect '측면', typically '일반적으로', regarding '~에 관하여', incentive '유인책', at the expense of '~을 희생하여', mixed '엇갈리는',
confused '혼란스러운', be channeled into '~으로 귀결되다', customer care '고객 응대'. 지문 아래 * 풀이 단어 없음.
반영한 규칙: 2026-10-20 끊어읽기(slashes·roles·modifiers), S·V 찾기 없음, 핵심어 나열형 해석 없음, 2026-10-21 제출·보기 해설까지.

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- (A) 첫 문장 In many cases에는 앞을 받는 말(This·Such·That)이 없어서 「앞에 무엇이 와야 할까요?」(_before)를 넣지 않고
  뜻 질문(보상은 어느 측면에만?)만 두었다. (A)와 (C)의 연결(rewarded ↔ compensation)은 (C) 끝 c_next에서 묻는다
- (A) 끝은 결론이라 「다음엔?」을 묻지 않고 한 줄 정리만 했다
- 칠판 「관리자가 보내는 신호」: says(말) — customer care / pays(급여) — the number of calls · being fast, 사이 ≠.
  (B) 끝 b_next 화면에 처음 연다. ≠는 (B)의 a very different signal을 옮긴 것이라 순서를 미리 알려 주지는 않는다고 봤다
- 주어진 글 g_next 「관리자의 그 말이 어떤 메시지(신호)인지」 — 첫 문장(선택과 행동은 가치관에 대한 메시지)과 Consider a manager로 든 예가 근거
- 헷갈리는 단어(trap): leave(떠나다 ✕ → ~한 상태로 두다, (C) 첫 문장)
- 해석 맞추기(add_match): (C) 첫 문장 하나
- 많이 고른 오답 보기 설명(option_review): ② 12%, ④ 10% 둘 다
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from order_tools import card, order_link  # noqa: E402
from beginner import add_match, add_refers, m  # noqa: E402

ID = "mopyeong-2027-09-36-mixed-signals"

G1 = "Our choices and actions send messages to others about our values."
G2 = ("Consider a manager who communicates to her employees in a call center that “customer care is the most important thing "
      "for our company.”")
A1 = ("(A) In many cases, performance is multidimensional, but compensation is only given to one aspect of performance, typically "
      "the one that is easiest to measure.")
A2 = ("Simple “one-aspect” compensation sends a clear message to the workers: concentrate on what we’re paying you for and ignore "
      "everything else.")
B1 = "(B) That’s a signal to others regarding values."
B2 = ("Now, imagine that the manager sets the incentives such that employees are paid by the number of calls they answer.")
B3 = ("This incentive sends a very different signal about what the manager is looking for: it’s about being fast, which comes at "
      "the expense of quality of care.")
C1 = "(C) Such mixed signals leave the employees confused about the manager’s values and expectations."
C2 = "This mixed signals problem is channeled into a simple question: what should be rewarded?"

sentences = [
    {
        "id": 1, "label": "주어진 글", "text": G1, "teaching_value": "high",
        "model_translation": "우리의 선택과 행동은 다른 사람들에게 우리의 가치관에 관한 메시지를 보낸다.",
        "glosses": [g("Our choices and actions", "우리의 선택과 행동은"), g("choices", "선택"), g("actions", "행동"),
                    g("send messages", "메시지를 보낸다"), g("messages", "메시지"), g("others", "다른 사람들"),
                    g("our values", "우리의 가치관"), g("values", "가치관")],
        "slashes": ["send messages", "to others"],
        "roles": [r("Our choices and actions", "S"), r("send", "V"), r("messages", "O")],
        "steps": [
            choice("g_main",
                   "우리의 선택과 행동은 다른 사람들에게 무엇에 관한 메시지를 보낸대요?",
                   [("o0", "우리가 중요하게 여기는 것", True), ("o1", "우리가 잘하는 일", False), ("o2", "우리의 그날 기분", False)],
                   "send messages to others about ~에서 about 뒤를 봐요.",
                   why="'about our values', 가치관(values)에 관한 메시지래요. 무엇을 고르고 어떻게 행동하는지가 그 사람의 가치관을 보여 준다는 말이에요.",
                   highlight=["messages", "values"]),
        ],
    },
    {
        "id": 2, "text": G2, "teaching_value": "high",
        "model_translation": "콜센터 직원들에게 “고객 응대가 우리 회사에 가장 중요한 일이다.”라고 전달하는 한 관리자를 생각해 보라.",
        "glosses": [g("Consider", "생각해 보라"), g("a manager", "한 관리자"), g("manager", "관리자"),
                    g("communicates", "전달하다"), g("her employees", "자기 직원들"), g("employees", "직원들"),
                    g("in a call center", "콜센터에서"), g("call center", "콜센터"),
                    g("customer care", "고객 응대"), g("customer", "고객"), g("care", "돌봄, 응대"),
                    g("the most important thing", "가장 중요한 일"), g("important", "중요한"), g("company", "회사")],
        "slashes": ["Consider a manager", "to her employees", "in a call center"],
        "roles": [r("Consider", "V"),
                  r("a manager who communicates to her employees in a call center that “customer care is the most important thing for our company", "O")],
        "modifiers": ["who communicates to her employees in a call center that “customer care is the most important thing for our company"],
        "steps": [
            choice("g_next",
                   "주어진 글은 관리자가 '고객 응대가 가장 중요하다'고 말하는 예로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "관리자의 그 말이 직원들에게 보내는 메시지", True), ("o1", "콜센터 직원을 뽑는 방법", False),
                    ("o2", "고객이 콜센터에 거는 전화의 종류", False)],
                   "첫 문장을 떠올려 봐요. 선택과 행동은 가치관에 관한 메시지를 보낸다고 했어요.",
                   why="첫 문장에서 선택과 행동이 가치관에 관한 메시지를 보낸다고 하고, Consider(생각해 보라)로 관리자의 예를 들었어요. 그러니 다음엔 이 관리자가 어떤 메시지를 보내는지 이어지기 쉬워요.",
                   highlight=["Consider", "customer care"],
                   tips=[tip("Consider ~", "'~를 생각해 보라'예요. 주장을 하고 예를 들 때 자주 써요.", "Consider")],
                   point="주어진 글 끝 '고객 응대가 가장 중요하다'는 관리자의 말 → 다음은 그 말이 보내는 메시지"),
            show("paper_order", "이제 (A)·(B)·(C)를 시험지 순서대로 읽어요. 단락마다 첫머리와 끝을 잘 봐 두면 좋아요.",
                 button="(A)부터 읽어 볼게요"),
        ],
    },
    {
        "id": 3, "text": A1, "teaching_value": "high",
        "model_translation": "(A) 많은 경우, 성과는 다차원적이지만 보상은 성과의 한 측면, 일반적으로 가장 측정하기 쉬운 측면에만 주어진다.",
        "glosses": [g("In many cases", "많은 경우"), g("cases", "경우"), g("performance", "성과"),
                    g("multidimensional", "다차원적인 · 여러 측면이 있는"), g("compensation", "보상"),
                    g("is only given", "~에만 주어진다"), g("given", "주어진"), g("one aspect of performance", "성과의 한 측면"),
                    g("aspect", "측면"), g("typically", "일반적으로, 보통"), g("easiest", "가장 쉬운"),
                    g("easiest to measure", "가장 측정하기 쉬운"), g("measure", "측정하다")],
        "slashes": ["In many cases,", "is multidimensional,", "is only given", "of performance,", "typically the one"],
        "roles": [r("performance", "S"), r("is", "V"), r("multidimensional", "C"), r("compensation", "S"), r("is only given", "V")],
        "modifiers": ["that is easiest to measure"],
        "steps": [
            choice("a_comp",
                   "(A)는 '성과는 여러 측면이 있지만, but 보상(compensation)은 …'으로 시작해요. 보상은 성과의 어느 쪽에 주어진대요?",
                   [("o0", "여러 측면 모두에 골고루", False), ("o1", "가장 측정하기 쉬운 한 측면에만", True),
                    ("o2", "직원이 스스로 고른 측면에", False)],
                   "but 뒤 is only given to one aspect of performance를 봐요.",
                   why="'is only given to one aspect of performance', 보상은 성과의 한 측면에만 주어진대요. typically the one that is easiest to measure, 보통 가장 측정하기 쉬운 것이에요.",
                   highlight=["compensation", "only", "one aspect"],
                   tips=[tip("multidimensional", "'다차원적인, 여러 측면이 있는'이에요. multi(여럿) + dimension(차원)이에요.", "multidimensional"),
                         tip("compensation", "'보상'이에요. 일한 대가로 주는 급여나 상을 말해요.", "compensation")],
                   point="(A) 보상(compensation)은 성과의 한 측면(가장 측정하기 쉬운 것)에만"),
        ],
    },
    {
        "id": 4, "text": A2, "teaching_value": "medium",
        "model_translation": "단순한 ‘단일 측면’에 대한 보상은 직원들에게 명확한 메시지를 보내는데, 즉 우리가 여러분에게 급여를 지불하는 대상에 집중하고 그 밖의 다른 모든 것은 무시하라는 것이다.",
        "glosses": [g("Simple “one-aspect” compensation", "단순한 '단일 측면' 보상은"), g("Simple", "단순한"),
                    g("one-aspect", "단일 측면의"), g("compensation", "보상"), g("a clear message", "명확한 메시지"),
                    g("clear", "명확한"), g("message", "메시지"), g("workers", "직원들"),
                    g("concentrate on", "~에 집중하다"), g("concentrate", "집중하다"),
                    g("what we’re paying you for", "우리가 여러분에게 급여를 주는 대상"), g("paying", "(돈을) 주는"),
                    g("ignore", "무시하다"), g("everything else", "그 밖의 모든 것")],
        "slashes": ["Simple “one-aspect” compensation", "sends a clear message", "to the workers:", "what we’re paying you for"],
        "roles": [r("Simple “one-aspect” compensation", "S"), r("sends", "V"), r("a clear message", "O"),
                  r("concentrate on", "V"), r("what we’re paying you for", "O"), r("ignore", "V"), r("everything else", "O")],
        "steps": [
            show("a2_end", "한 측면에만 보상하면 직원들은 '돈 받는 일에만 집중하고 나머지는 무시하라'는 메시지로 받아들인대요.",
                 highlight=["concentrate on", "ignore"],
                 tips=[tip("콜론(:)", "콜론(:) 뒤는 앞의 a clear message가 무엇인지 풀어 쓴 말이에요.", None),
                       tip("pay A for B", "'B에 대해 A에게 돈을 주다'예요. what we’re paying you for = 우리가 여러분에게 돈을 주는 대상.", "paying")]),
        ],
    },
    {
        "id": 5, "text": B1, "teaching_value": "high",
        "model_translation": "(B) 그것은 가치관에 관해 다른 사람들에게 보내는 하나의 신호이다.",
        "glosses": [g("That’s", "그것은 ~이다"), g("That", "그것은"), g("’s", "~이다"), g("a signal", "하나의 신호"),
                    g("signal", "신호"), g("others", "다른 사람들"), g("regarding values", "가치관에 관한"),
                    g("regarding", "~에 관하여"), g("values", "가치관")],
        "slashes": [],
        "roles": [r("That", "S"), r("’s", "V"), r("a signal", "C")],
        "steps": [
            choice("b_before",
                   "(B)는 'That’s a signal to others regarding values(그것은 가치관에 관한 신호다)'로 시작해요. That(그것)을 보면 앞에는 무엇이 와야 할까요?",
                   [("o0", "가치관을 드러내는 누군가의 말이나 행동", True), ("o1", "직원들이 혼란스러워한다는 내용", False),
                    ("o2", "성과를 측정하기 어렵다는 내용", False)],
                   "That은 앞에 나온 것을 가리켜요. 그것이 '가치관에 관한 신호'가 될 수 있어야 해요.",
                   why="That(그것)은 앞에 나온 것을 가리키고, 그것이 가치관에 관한 신호래요. 그러니 앞에 무엇을 중요하게 여기는지 보여 주는 말이나 행동이 있어야 해요.",
                   highlight=["That", "signal", "values"],
                   tips=[tip("regarding", "'~에 관하여'예요. a signal regarding values = 가치관에 관한 신호.", "regarding")],
                   point="(B) That ← 앞에 가치관을 보여 주는 말이나 행동"),
        ],
    },
    {
        "id": 6, "text": B2, "teaching_value": "medium",
        "model_translation": "이제 관리자가 직원들이 응답하는 통화 수에 따라 급여를 받도록 유인책을 설정한다고 상상해 보라.",
        "glosses": [g("Now", "이제"), g("imagine", "상상해 보라"), g("the manager", "그 관리자"), g("manager", "관리자"),
                    g("sets the incentives", "유인책을 정한다"), g("sets", "정하다"),
                    g("incentives", "유인책, 장려책 · 무엇을 하게 만드는 보상"), g("such that", "~하도록"),
                    g("employees", "직원들"), g("are paid", "급여를 받는다"), g("paid", "돈을 받는"),
                    g("the number of calls", "통화 수"), g("number", "수"), g("calls", "통화"), g("answer", "응답하다")],
        "slashes": ["Now,", "imagine", "sets the incentives", "are paid"],
        "roles": [r("imagine", "V"), r("the manager", "S"), r("sets", "V"), r("the incentives", "O"),
                  r("employees", "S"), r("are paid", "V")],
        "modifiers": ["they answer"],
        "steps": [
            show("b2_mid", "'imagine that …', 이번엔 그 관리자가 직원들이 받은 전화 수에 따라 급여를 준다고 상상해 보래요.",
                 highlight=["the number of calls"],
                 tips=[tip("such that", "'~하도록'이에요. sets the incentives such that employees are paid … = 직원들이 …에 따라 급여를 받도록 유인책을 정하다.", "such that"),
                       tip("incentive", "'유인책, 장려책'이에요. 사람이 어떤 일을 더 하게 만드는 보상이에요.", "incentives")]),
        ],
    },
    {
        "id": 7, "text": B3, "teaching_value": "high",
        "model_translation": "이러한 유인책은 관리자가 무엇을 원하는지에 관해 매우 다른 신호를 보내는데, 즉, 그것은 신속함에 관한 것이며, 고객 응대의 질을 희생하면서 이루어진다.",
        "glosses": [g("This incentive", "이 유인책은"), g("incentive", "유인책"), g("sends", "보낸다"),
                    g("a very different signal", "매우 다른 신호"), g("different", "다른"), g("signal", "신호"),
                    g("what the manager is looking for", "관리자가 원하는 것"), g("looking for", "찾는, 원하는"),
                    g("it’s", "그것은 ~이다"), g("it", "그것은"), g("’s", "~이다"),
                    g("about being fast", "빠른 것에 관한"), g("fast", "빠른"),
                    g("at the expense of", "~을 희생하여"), g("expense", "희생, 비용"),
                    g("quality of care", "고객 응대의 질"), g("quality", "질"), g("care", "응대")],
        "slashes": ["a very different signal", "is looking for:", "about being fast,"],
        "roles": [r("This incentive", "S"), r("sends", "V"), r("a very different signal", "O"),
                  r("it", "S"), r("’s", "V"), r("about being fast", "C")],
        "modifiers": ["which comes at the expense of quality of care"],
        "steps": [
            choice("b_next",
                   "(B)는 '이 유인책은 매우 다른 신호를 보낸다, 빨리 하라는 신호다'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "고객 응대의 질을 높이는 방법", False), ("o1", "서로 다른 두 신호 때문에 생기는 문제", True),
                    ("o2", "통화를 빨리 끝내는 요령", False)],
                   "a very different signal(매우 다른 신호)이라고 했어요. 무엇과 다른지 떠올려 봐요.",
                   why="관리자는 말로는 '고객 응대가 가장 중요하다'고 했는데, 급여는 '빨리 하라'는 아주 다른 신호를 보내요. 신호가 둘로 갈렸으니 다음엔 그 때문에 생기는 문제가 이어지기 쉬워요.",
                   highlight=["very different signal", "being fast"],
                   tips=[tip("at the expense of", "'~을 희생하여'예요. which comes at the expense of quality of care = 그것은 고객 응대의 질을 희생하면서 이루어진다.", "expense")],
                   panel=groups("관리자가 보내는 신호 (signal)", "says (말)", [("customer care", "고객 응대")],
                                "pays (급여)", [("the number of calls", "받은 통화 수"), ("being fast", "빠름")],
                                between="≠", fresh=("the number of calls", "being fast")),
                   point="(B) 끝 '매우 다른 신호(빨리 하라)' → 다음은 두 신호가 엇갈려 생기는 문제"),
        ],
    },
    {
        "id": 8, "text": C1, "teaching_value": "high",
        "model_translation": "(C) 그러한 엇갈리는 신호는 직원들을 관리자의 가치관과 기대에 대해 혼란스럽게 만든다.",
        "glosses": [g("Such mixed signals", "그러한 엇갈리는 신호는"), g("Such", "그러한"), g("mixed", "엇갈리는, 뒤섞인"),
                    g("signals", "신호"), g("leave", "(~한 상태로) 만들다, 두다"), g("the employees", "직원들을"),
                    g("employees", "직원들"), g("confused", "혼란스러운"),
                    g("about the manager’s values and expectations", "관리자의 가치관과 기대에 대해"),
                    g("manager’s", "관리자의"), g("values", "가치관"), g("expectations", "기대")],
        "slashes": ["Such mixed signals", "leave the employees confused"],
        "roles": [r("Such mixed signals", "S"), r("leave", "V"), r("the employees", "O"), r("confused", "C")],
        "steps": [
            choice("c_before",
                   "(C)는 'Such mixed signals(그러한 엇갈리는 신호)'로 시작해요. 앞에는 무엇이 와야 할까요?",
                   [("o0", "관리자가 한 가지 말을 하는 장면", False), ("o1", "서로 다른 신호가 둘 이상 나온 내용", True),
                    ("o2", "보상이 한 측면에만 주어진다는 설명", False)],
                   "Such(그러한)는 앞에 나온 것을 받아요. mixed(엇갈리는)는 서로 다른 것이 섞였다는 말이에요.",
                   why="Such mixed signals는 앞에 이미 서로 다른 신호가 나와 있어야 쓸 수 있어요. 신호 하나만으로는 '엇갈린다'고 할 수 없어요.",
                   highlight=["Such mixed signals"],
                   tips=[tip("leave", "평소엔 '떠나다'로 알기 쉬워요. 여기서는 leave + 사람 + 상태로 '~를 …한 상태로 만들다'예요. leave the employees confused = 직원들을 혼란스럽게 만들다.", "leave", trap=True)],
                   point="(C) Such mixed signals ← 앞에 서로 다른 신호 둘"),
        ],
    },
    {
        "id": 9, "text": C2, "teaching_value": "high",
        "model_translation": "이 엇갈리는 신호의 문제는 ‘무엇이 보상되어야 하는가?’라는 하나의 간단한 질문으로 귀결된다.",
        "glosses": [g("This mixed signals problem", "이 엇갈리는 신호의 문제는"), g("mixed", "엇갈리는"), g("signals", "신호"),
                    g("problem", "문제"), g("is channeled into", "~으로 귀결된다"), g("channeled", "(한 곳으로) 모인"),
                    g("a simple question", "하나의 간단한 질문"), g("simple", "간단한"), g("question", "질문"),
                    g("what should be rewarded", "무엇이 보상되어야 하는가"), g("rewarded", "보상받는")],
        "slashes": ["This mixed signals problem", "a simple question:"],
        "roles": [r("This mixed signals problem", "S"), r("is channeled", "V")],
        "steps": [
            choice("c_next",
                   "(C)는 '무엇이 보상되어야 하는가'라는 물음으로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "보상을 무엇에 어떻게 주는지에 대한 이야기", True), ("o1", "관리자가 직원들에게 하는 첫인사", False),
                    ("o2", "콜센터의 하루 통화 수", False)],
                   "what should be rewarded(무엇이 보상되어야 할까)라고 물었어요. 그 물음을 이어 받는 말을 찾아봐요.",
                   why="글이 '무엇을 보상해야 할까'라는 물음으로 끝났어요. 다음엔 그 물음을 받아 보상 이야기를 이어 가는 말이 오기 쉬워요.",
                   highlight=["rewarded"],
                   tips=[tip("be channeled into", "'~으로 귀결되다, 모이다'예요. 엇갈린 신호의 문제가 결국 하나의 질문으로 모인다는 말이에요.", "channeled"),
                         tip("reward", "'보상하다'예요. (A)의 compensation(보상)과 같은 쪽 말이에요.", "rewarded")],
                   point="(C) 끝 '무엇이 보상되어야 할까?' → 다음은 보상 이야기"),
            order_link(
                card("given", "주어진 글", last=("Consider a manager who communicates … “customer care is the most important thing …”", "'고객 응대가 가장 중요하다'고 말하는 관리자를 생각해 보라")),
                [card("A", "(A)", first=("In many cases, performance is multidimensional, but compensation is only given to one aspect …", "많은 경우, 성과는 여러 측면이지만 보상은 한 측면에만 주어진다"),
                      last=("… concentrate on what we’re paying you for and ignore everything else.", "돈 받는 일에 집중하고 나머지는 무시하라")),
                 card("B", "(B)", first=("That’s a signal to others regarding values.", "그것은 가치관에 관한 신호다"),
                      last=("… it’s about being fast, which comes at the expense of quality of care.", "빨리 하라는 신호, 고객 응대의 질을 희생하면서")),
                 card("C", "(C)", first=("Such mixed signals leave the employees confused …", "그러한 엇갈리는 신호는 직원들을 혼란스럽게 한다"),
                      last=("… a simple question: what should be rewarded?", "무엇이 보상되어야 하는가?"))],
                ["B", "C", "A"],
                "주어진 글('고객 응대가 가장 중요하다'는 관리자의 말) → (B) 그것도 신호인데, 통화 수로 급여를 주면 아주 다른 신호 → (C) 그런 엇갈린 신호, 무엇을 보상해야 할까 → (A) 보상이 한 측면에만 주어지면 그것에만 집중한다, 순서예요."),
            show("c_go", "직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?", button="문제 풀러 갈게요"),
        ],
    },
]

add_match(sentences, 8, [m("Such mixed signals", "그러한 엇갈리는 신호는"), " ", m("the employees", "직원들을"), " ",
                         m("about the manager’s values and expectations", "관리자의 가치관과 기대에 대해"), " ",
                         m("confused", "혼란스럽게"), " ", m("leave", "만든다"), "."])
add_refers(sentences, 5, {"That": "the manager’s words in the given text(주어진 글에서 관리자가 한 말)"})
add_refers(sentences, 7, {"This incentive": "paying by the number of calls(통화 수에 따라 급여를 주는 것)"})

SENSES = {
    1: [sense("to", "messages to others", "~에게", "전치사 to (받는 사람)")],
    2: [sense("to", "communicates to her employees", "~에게", "전치사 to (받는 사람)"),
        sense("that", "that “customer care", "~라고", "명사절 that (전달하는 내용)"),
        sense("for", "for our company", "~에 (있어)", "전치사 for")],
    3: [sense("but", "but compensation", "하지만", "접속사 but (두 문장을 이음)"),
        sense("to", "given to one aspect", "~에 (주어지다)", "be given to ~ = ~에 주어지다"),
        sense("that", "the one that is", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("to", "easiest to measure", "~하기에 (쉬운)", "easy to + 동사원형 = ~하기 쉬운")],
    4: [sense("to", "message to the workers", "~에게", "전치사 to (받는 사람)"),
        sense("for", "paying you for", "~에 대해 (돈을 주다)", "pay A for B = B에 대해 A에게 돈을 주다 (what이 for의 목적어)")],
    5: [sense("that", "That’s", "그것 (앞에서 한 말)", "지시대명사 that"),
        sense("to", "to others", "~에게", "전치사 to (받는 사람)")],
    6: [sense("that", "imagine that the manager", "~라고 (상상하다)", "명사절 that + 주어·동사"),
        sense("that", "such that employees", "~하도록", "such that + 주어·동사 = ~하도록")],
    7: [sense("for", "is looking for", "(look for = 찾다, 원하다)", "look for ~ = ~을 찾다, 원하다"),
        sense("which", ", which comes", "(앞 내용에 덧붙임) 그것은", "관계대명사 which (콤마 뒤 덧붙이는 설명)")],
}

WORDS = {"choices": "선택", "actions": "행동", "send": "보내다", "messages": "메시지", "values": "가치관", "consider": "생각해 보다",
         "manager": "관리자", "communicates": "전달하다", "employees": "직원들", "call": "전화", "center": "센터",
         "customer": "고객", "care": "응대", "important": "중요한", "company": "회사", "cases": "경우",
         "performance": "성과", "multidimensional": "다차원적인", "compensation": "보상", "given": "주어진", "aspect": "측면",
         "typically": "일반적으로", "easiest": "가장 쉬운", "measure": "측정하다", "simple": "단순한", "one-aspect": "단일 측면의",
         "clear": "명확한", "message": "메시지", "workers": "직원들", "concentrate": "집중하다", "paying": "(돈을) 주는",
         "ignore": "무시하다", "everything": "모든 것", "else": "그 밖의", "signal": "신호", "regarding": "~에 관하여",
         "imagine": "상상하다", "sets": "정하다", "incentives": "유인책", "incentive": "유인책", "paid": "돈을 받는",
         "number": "수", "calls": "통화", "answer": "응답하다", "sends": "보내다", "different": "다른", "looking": "찾는",
         "fast": "빠른", "being": "~인 것", "comes": "오다, 이루어지다", "expense": "희생", "quality": "질", "mixed": "엇갈리는",
         "signals": "신호", "leave": "~한 상태로 만들다", "confused": "혼란스러운", "manager’s": "관리자의",
         "expectations": "기대", "problem": "문제", "channeled": "모인", "question": "질문", "rewarded": "보상받는", "we’re": "우리가 ~하고 있다"}

OPTIONS = [("1", "(A)-(C)-(B)", False), ("2", "(B)-(A)-(C)", False), ("3", "(B)-(C)-(A)", True), ("4", "(C)-(A)-(B)", False), ("5", "(C)-(B)-(A)", False)]
exam = {
    "question": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?",
    "sentence": 1, "analysis_first": True, "wrong_rate": 30.0, "wrong_rank": 9,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], **({"correct": True} if o[2] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "단락 첫머리 단서(That, Such mixed signals)와 (C) 끝의 물음을 떠올리며 순서를 골라 봐요.",
        "정답이에요! 관리자의 말 → (B) 그것도 신호인데 통화 수로 급여를 주면 아주 다른 신호 → (C) 그런 엇갈린 신호, 무엇을 보상해야 하나 → (A) 한 측면에만 보상하면 그것에만 집중한다, 순서예요.",
        "정답은 ③ (B)-(C)-(A)예요.",
        {"1": "(A)는 보상(compensation) 이야기예요. 주어진 글 바로 뒤에는 보상 이야기가 나올 까닭이 아직 없어요.",
         "2": "가장 많이 고른 오답이에요. (C)의 Such mixed signals(그러한 엇갈리는 신호)는 (B)의 서로 다른 두 신호를 바로 받아요. (A)는 (C) 끝 물음 '무엇이 보상되어야 하는가'를 받아요.",
         "4": "많이 고른 오답이에요. 주어진 글에는 관리자의 말 하나뿐이라 (C)의 Such mixed signals가 받을 신호가 둘이 아니에요. 그 말은 (B)의 That이 받아요.",
         "5": "(C)의 Such mixed signals는 (B)의 두 신호를 받아요. (B)가 (C) 뒤에 오면 엇갈린 신호가 먼저 나오고 신호는 나중에 나와요."},
        {"2": review(12,
                     "(B)의 '통화 수대로 급여'와 (A)의 '보상은 측정하기 쉬운 한 측면에만'이 비슷해 보여서 바로 이었을 거예요. 하지만 (C)의 Such mixed signals는 (B)의 두 신호, 곧 '고객 응대가 가장 중요하다'는 말과 '빨리 하라'는 급여를 받아요. (A)는 (C) 끝 물음 what should be rewarded?를 받아 보상 이야기를 이어 가요.",
                     panel=rows(("(B) 끝", "This incentive sends a very different signal … being fast", "말과 다른 신호 → 신호 둘", "hl"),
                                ("(C) 첫머리", "Such mixed signals …", "그 엇갈린 신호", "hl"),
                                ("(C) 끝 → (A)", "what should be rewarded? → compensation is only given to …", "보상 물음 → 보상 이야기", "hl2")),
                     rank_word="가장 많이 고른"),
         "4": review(10,
                     "주어진 글의 관리자 말을 보고 (C)의 Such mixed signals를 바로 이었을 거예요. 하지만 주어진 글에는 신호가 '고객 응대가 가장 중요하다'는 말 하나뿐이에요. 그 말은 (B)의 That’s a signal이 받고, 엇갈리는 두 번째 신호도 (B)에서 나와요.",
                     panel=rows(("주어진 글", "“customer care is the most important thing …”", "신호 하나", "hl"),
                                ("(B)", "That’s a signal … a very different signal", "그것도 신호 + 아주 다른 신호", "hl2"),
                                ("(C)", "Such mixed signals …", "엇갈린 신호", "hl2")))}),
}

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 36번 (글의 순서, 2점)",
    topic="순서 푸는 법: 주어진 글의 끝 → 단락 첫머리 단서로 앞 내용 예측 → 단락 끝으로 다음 내용 예측 → 순서 잇기",
    method={"type": "order", "labels": ["단락 요지 잡기", "연결 단서 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-mixed-signals.svg", ("Words", "말"), "?", ("Pay", "급여"),
                                       "직원은 관리자의 무엇을 보고 움직일까?", "2026년 9월 모의평가 36번 도입 칠판"),
                      "alt": "칠판: Words(말) ? Pay(급여)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "회사가 직원에게 무엇을 바라는지는 말로만 전해질까요? 이번 글은 가치관과 보상(compensation) 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "순서 문제는 단락 첫머리의 단서가 앞 내용과 이어지는지 보는 거예요. That, Such 같은 말이 무엇을 받는지 찾아볼게요."}}],
    exam=exam,
    key_words={"passage": [g("values", "가치관"), g("communicate", "전달하다"), g("customer care", "고객 응대"),
                           g("performance", "성과"), g("multidimensional", "다차원적인"), g("compensation", "보상"),
                           g("aspect", "측면"), g("typically", "일반적으로"), g("measure", "측정하다"),
                           g("concentrate on", "~에 집중하다"), g("ignore", "무시하다"), g("signal", "신호"),
                           g("regarding", "~에 관하여"), g("incentive", "유인책"), g("at the expense of", "~을 희생하여"),
                           g("quality", "질"), g("mixed", "엇갈리는"), g("leave + 사람 + 상태", "~를 …한 상태로 만들다"),
                           g("confused", "혼란스러운"), g("expectation", "기대"), g("be channeled into", "~으로 귀결되다"),
                           g("reward", "보상하다")],
               "options": []},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="순서 푸는 법")
