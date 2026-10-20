"""2022년 3월 고3 39번 레슨 + 대사를 만든다 (주어진 문장 넣기, 3점). 오답률 52.0% · Top 6.

    py scripts/lessons/gen_moeui_2022_03_39.py   (→ node scripts/policy_copy.mjs stamp <id> → npm run build)

틀: docs/tutor/templates/README.md + 2024년 3월 38·39번(문장 넣기) — 주어진 문장 단서 → 앞뒤 예측 → ①~⑤ 흐름 확인.
정답 ③. 많이 고른 오답 ④ 23% — ⑤문장 how much the teacher covers가 주어진 문장 cover a set curriculum과 낱말이 겹쳐 끌린다.
열쇠: 주어진 문장엔 This·But 같은 앞을 가리키는 말이 없다 → 지문에서 가리킬 대상이 없는 말을 찾는다.
③ 뒤 But that’s unlikely … 의 that은 '질적 변화에 도움이 안 되는 방법' = 주어진 문장의 maximize time on task(양적 변화).
③ 앞(선생님의 생각·수업 방식)은 학생 태도를 만드는 쪽이라 that이 받을 수 없다.
주어진 문장 정석(insertion-given-sentence-order): 앞을 가리키는 말이 없으니 「앞에 무엇?」을 묻지 않고, 「뒤에 무엇?」도 묻지 않는다.
might seem은 단정하지 않는 말이라는 것만 짚는다(Tip).
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt). Claude 초안 — 선생님 검토 전.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2022-03-39-time-on-task"

GIVEN = ("If the goal is to figure out how best to cover a set curriculum — to fill students with facts — then it might seem "
         "appropriate to try to maximize time on task, such as by assigning homework.")
S = [
    "Carole Ames, dean of the college of education at Michigan State University, points out that it isn’t “quantitative changes "
    "in behavior” (such as requiring students to spend more hours in front of books or worksheets) that help children to learn better.",
    "(①) Rather, it’s “qualitative changes in the ways students view themselves in relation to the task, engage in the process of "
    "learning, and then respond to the learning activities and situation.”",
    "(②) In turn, these attitudes and responses on the part of students emerge from the way teachers think about learning and, "
    "as a result, the ways they’ve organized their classrooms.",
    "(③) But that’s unlikely to have a positive effect on the critical variables that Ames identifies.",
    "(④) Perhaps it makes sense to see education as being less about how much the teacher covers and more about what the students "
    "can be helped to discover.",
    "(⑤) More time won’t do a thing to bring about that shift.",
]
KO = [
    "미시간 주립 대학교의 사범 대학 학장인 Carole Ames는 아이들이 더 잘 배우도록 돕는 것은 (학생들이 책이나 학습지 앞에서 더 많은 시간을 보내도록 요구하는 것 같은) '행동의 양적 변화'가 아니라고 지적한다.",
    "오히려 (아이들이 더 잘 배우도록 돕는 것은) '학생들이 과제와 관련하여 자신을 바라보고, 학습 과정에 참여하며, 그런 다음 활동과 상황에 대응하는 방식에서의 질적 변화'이다.",
    "결국, 학생 쪽의 이런 태도와 반응은 교사가 학습에 대해 생각하는 방식과 그 결과로 교사들이 수업을 구성한 방식으로부터 생겨난다.",
    "하지만 그것은 Ames가 밝히고 있는 중요한 변수에 긍정적인 영향을 미칠 것 같지 않다.",
    "아마도 교육을 교사가 얼마나 많은 부분을 다루는가와는 관련이 더 적고 학생들이 무엇을 발견하도록 도움 받을 수 있는지와 더 관련이 있는 것으로 보는 것이 타당할 것이다.",
    "더 많은 (학습) 시간을 들인다 해도 그런 변화는 하나도 일어나지 않을 것이다.",
]

QUANT = "왼쪽 · 양적 변화 (시간·양)"
QUAL = "오른쪽 · 질적 변화 (대하는 방식)"
L1 = [("more hours", "더 많은 시간")]
R1 = [("view themselves", "자신을 보는 방식"), ("engage", "참여"), ("respond", "반응")]


def board(left, right=None, fresh=(), sort=None):
    if right is None:
        return groups("더 잘 배우게 돕는 것", "양적 변화 · 돕지 않는다", left, fresh=fresh)
    return groups("더 잘 배우게 돕는 것", "양적 변화 · 돕지 않는다", left, "질적 변화 · 돕는다", right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": QUANT, "right": QUAL} if sort else None)


def flow(id, n, before, after, ok, why):
    """①~⑤ 자리마다 — 앞 문장과 뒤 문장이 그대로 이어지나"""
    return choice(id, f"{n} 자리예요. '{before}' → '{after}', 자연스럽게 이어지나요?",
                  [("o0", "네, 이어져요", ok), ("o1", "아니요, 끊겨요", not ok)], why, why=why)


sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN, "teaching_value": "high",
        "model_translation": "만약 목표가 학생을 사실로 가득 채울, 정해진 교육과정을 다루는 가장 좋은 방법을 알아내는 것이라면, 숙제를 부여하는 것에 의하는 것처럼 과제에 들이는 시간을 최대화하려고 애쓰는 게 적절해 보일 수도 있다.",
        "glosses": [g("If the goal is", "만약 목표가 ~라면"), g("the goal", "목표"), g("to figure out", "알아내는 것"),
                    g("figure out", "알아내다"), g("how best to cover", "가장 잘 다루는 방법"),
                    g("cover", "다루다 · 여기서는 '수업에서 (내용을) 다 다루다'예요"),
                    g("a set curriculum", "정해진 교육과정"), g("set", "정해진"), g("curriculum", "교육과정"),
                    g("to fill students with facts", "학생을 사실로 채우는 것"),
                    g("then", "그러면"), g("it might seem appropriate", "~이 적절해 보일 수도 있다"), g("might seem", "~해 보일 수도 있다"),
                    g("appropriate", "적절한"), g("to try to maximize", "최대로 늘리려 애쓰는 것"), g("maximize", "최대로 늘리다"),
                    g("time on task", "과제에 쓰는 시간"), g("such as by assigning homework", "예를 들어 숙제를 내 주는 식으로"),
                    g("assigning", "(과제를) 내 주는 것")],
        "emphasis": ["time on task"],
        "slashes": ["If the goal is", "a set curriculum", "with facts", "— then", "seem appropriate", "time on task,"],
        "roles": [r("it", "S"), r("might seem", "V"), r("appropriate", "C"), r("the goal", "S"), r("is", "V")],
        "steps": [
            sv("g_sv", ["the goal", "is", "students", "it", "might seem", "appropriate"],
               {"it": "S", "might seem": "V", "appropriate": "C"},
               {"the goal": "그건 If(만약 ~라면) 덩어리 안의 주어예요. then 뒤에서 찾아봐요.",
                "is": "그건 If(만약 ~라면) 덩어리 안의 동사예요. then 뒤에서 찾아봐요.",
                "students": "그건 대시(—) 사이 덩어리 안의 말이에요."},
               "If 덩어리 뒤 then 다음이 메인이에요. 주어는 it, 동사는 might seem, 보어는 appropriate예요.",
               ask="긴 문장이에요. 메인 주어(S), 동사(V), 보어(C)를 찾아볼까요?",
               tips=[tip("가주어 it … to ~", "it은 뒤의 to try …를 대신하는 가짜 주어예요. it might seem appropriate to try = 애쓰는 것이 적절해 보일 수도 있다.")]),
            show("g_dash",
                 "대시(—) 사이 'to fill students with facts'는 앞의 'cover a set curriculum'을 다시 풀어 준 말이에요. 정해진 교육과정을 다룬다는 건 학생을 사실로 채운다는 뜻이에요.",
                 highlight=["cover a set curriculum", "to fill students with facts"],
                 tips=[tip("대시(—) 두 개 사이", "대시 두 개 사이는 앞말을 다시 풀어 주는 경우가 많아요. 한쪽을 이해했으면 다른 쪽은 가볍게 넘겨요.")]),
            choice("g_time",
                   "'try to maximize time on task, such as by assigning homework'는 무슨 뜻일까요?",
                   [("o0", "숙제를 줄여 쉬는 시간을 늘리려 애쓰기", False),
                    ("o1", "숙제를 내 주는 식으로 과제에 쓰는 시간을 최대한 늘리려 애쓰기", True),
                    ("o2", "과제를 더 재미있게 바꾸려 애쓰기", False)],
                   "maximize는 '최대로 늘리다', time on task는 '과제에 쓰는 시간'이에요.",
                   why="maximize는 '최대로 늘리다', time on task는 '과제에 쓰는 시간'이에요. 숙제를 내 줘서 공부 시간을 최대한 늘리는 거예요.",
                   highlight=["to try to maximize time on task"],
                   point="maximize time on task (by assigning homework) = 숙제로 공부 시간을 최대한 늘리기"),
            choice("g_seem",
                   "'it might seem appropriate'라고 했어요. 글쓴이는 이 방법이 정말 좋다고 단정할까요?",
                   [("o0", "네, 정말 좋은 방법이라고 단정해요", False), ("o1", "아니요, 그렇게 보일 수도 있다는 정도예요", True)],
                   "might seem은 '~해 보일 수도 있다'예요. 앞에 If(만약 목표가 ~라면)도 붙어 있어요.",
                   why="might seem은 '~해 보일 수도 있다'예요. 그것도 '만약 목표가 사실로 채우는 거라면'이라는 조건이 붙어서, 글쓴이가 단정한 게 아니에요.",
                   highlight=["If the goal is", "might seem"],
                   tips=[tip("might seem", "'~해 보일 수도 있다'예요. 글쓴이가 그렇다고 단정하지 않는 말이라, 뒤에서 반박하는 경우가 많아요.", "might seem")]),
            show("g_noclue",
                 "주어진 문장엔 This, But처럼 앞을 가리키는 말이 없어요. 이럴 땐 지문에서 가리킬 대상이 없는 말을 찾으면 돼요.",
                 tips=[tip("단서가 없는 주어진 문장", "주어진 문장에 지시어·연결어가 없으면, 지문 쪽의 that, this, But 같은 말이 받을 대상이 앞에 있는지 확인해요.")],
                 point="주어진 문장에 단서가 없으면 → 지문에서 가리킬 대상이 없는 말을 찾는다"),
        ],
    },
    {
        "id": 2, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Carole Ames", "캐롤 에임스 · 사람 이름"), g("dean of the college of education", "사범 대학 학장"),
                    g("at Michigan State University", "미시간 주립 대학교의"), g("points out", "지적하다"),
                    g("it isn’t", "~이 아니다"), g("quantitative changes in behavior", "행동의 양적 변화"),
                    g("quantitative", "양적인 · 양(시간·횟수)과 관련된"), g("such as requiring students", "예를 들어 학생들에게 요구하는 것"),
                    g("to spend more hours", "더 많은 시간을 보내도록"), g("in front of books or worksheets", "책이나 학습지 앞에서"),
                    g("that help children to learn better", "아이들이 더 잘 배우게 돕는"), g("dean", "학장"),
                    g("worksheets", "학습지")],
        "slashes": ["Carole Ames,", "education", "State University,", "points out", "it isn’t", "in behavior”", "or worksheets)"],
        "roles": [r("Carole Ames", "S"), r("points out", "V")],
        "steps": [
            sv("s1_sv", ["Carole Ames", "dean of the college of education", "points out", "students"],
               {"Carole Ames": "S", "points out": "V"},
               {"dean of the college of education": "그건 콤마 사이, Carole Ames가 누구인지 덧붙인 말이에요.",
                "students": "그건 괄호 안 예시 속 말이에요."},
               "주어는 Carole Ames, 동사는 points out(지적한다)이에요. that 뒤가 지적한 내용이에요.",
               ask="아주 긴 문장이에요. 주어(S)와 동사(V)를 찾아볼까요?"),
            show("s1_cleft",
                 "it isn’t A that ~는 '~하는 건 A가 아니다'예요. 아이들이 더 잘 배우게 돕는 건 행동의 양적 변화가 아니래요.",
                 highlight=["it isn’t", "quantitative changes in behavior", "that help children to learn better"],
                 faded=["(such as requiring students to spend more hours in front of books or worksheets)"],
                 tips=[tip("it is A that ~", "'~하는 것은 바로 A다'예요. A를 강조해요. it isn’t A that ~ = ~하는 건 A가 아니다.")]),
            choice("s1_quant",
                   "그럼 quantitative changes(양적 변화)의 예는 무엇일까요?",
                   [("o0", "학생이 스스로를 보는 방식 바꾸기", False), ("o1", "책이나 학습지 앞에서 더 오래 있게 하기", True),
                    ("o2", "학생끼리 토론하게 하기", False)],
                   "괄호 안 such as(예를 들어) 뒤를 봐요.",
                   why="괄호 안 such as 뒤, 책이나 학습지 앞에서 더 많은 시간을 보내게 하는 게 양적 변화의 예예요.",
                   highlight=["quantitative changes in behavior", "to spend more hours"]),
            show("s1_board", "더 오래 공부시키는 양적 변화는 돕지 않는대요.",
                 panel=board(L1, fresh=("more hours",)), highlight=["to spend more hours"]),
        ],
    },
    {
        "id": 3, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Rather", "오히려"), g("it’s", "그것은 ~이다"), g("qualitative changes", "질적 변화"),
                    g("qualitative", "질적인 · 방식·태도와 관련된"),
                    g("in the ways students view themselves", "학생이 자신을 바라보는 방식에서"),
                    g("in relation to the task", "과제와 관련하여"), g("engage in the process of learning", "학습 과정에 참여하다"),
                    g("engage in", "~에 참여하다"), g("and then respond to", "그런 다음 ~에 반응하다"),
                    g("the learning activities and situation", "학습 활동과 상황")],
        "slashes": ["Rather, it’s", "qualitative changes", "view themselves", "to the task,", "of learning,", "respond to"],
        "roles": [r("it", "S"), r("’s", "V"), r("qualitative changes", "C")],
        "steps": [
            choice("s2_rather",
                   "Rather(오히려) 뒤를 봐요. 아이들이 더 잘 배우게 돕는 건 무엇일까요?",
                   [("o0", "학생이 자신과 학습을 대하는 방식의 질적 변화", True), ("o1", "공부 시간을 늘리는 양적 변화", False),
                    ("o2", "선생님이 다루는 내용의 양", False)],
                   "qualitative는 '질적인'이에요. 학생이 자신을 보고(view), 참여하고(engage), 반응하는(respond) 방식을 봐요.",
                   why="qualitative changes(질적 변화), 학생이 자신을 보고, 학습에 참여하고, 반응하는 방식이 바뀌는 게 돕는대요.",
                   highlight=["qualitative changes"],
                   tips=[tip("Rather", "'오히려, 그게 아니라'예요. 앞에서 not으로 부정한 뒤 진짜를 말할 때 써요.", "Rather")]),
            show("s2_board", "양적 변화가 아니라 질적 변화가 돕는대요.",
                 panel=board(L1, R1, fresh=("view themselves", "engage", "respond"))),
            choice("s2_sort",
                   "주어진 문장의 'maximize time on task(과제 시간 최대로 늘리기)'는 칠판 어느 쪽일까요?",
                   [("o0", QUANT, True), ("o1", QUAL, False)],
                   "time(시간)을 늘리는 거예요. 더 많은 시간(more hours)과 같은 쪽이에요.",
                   why="과제에 쓰는 시간을 늘리는 건 more hours(더 많은 시간)처럼 양을 바꾸는 거라 왼쪽이에요.",
                   panel=board(L1, R1, sort=["maximize time on task"])),
            flow("s2_flow", "①", "돕는 건 양적 변화가 아니다", "오히려 질적 변화다", True,
                 "not(아니다)으로 부정한 뒤 Rather(오히려)로 진짜를 말해요. 그대로 이어져요."),
        ],
    },
    {
        "id": 4, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("In turn", "결국, 이번엔 그것이 또"), g("these attitudes and responses", "이런 태도와 반응"),
                    g("attitudes", "태도"), g("responses", "반응"),
                    g("on the part of students", "학생 쪽의"), g("emerge from", "~에서 나오다"), g("emerge", "나오다, 생겨나다"),
                    g("the way teachers think about learning", "선생님이 학습에 대해 생각하는 방식"),
                    g("as a result", "그 결과로"), g("the ways they’ve organized their classrooms", "선생님이 수업을 꾸린 방식"),
                    g("organized", "구성했다, 꾸렸다")],
        "slashes": ["In turn,", "attitudes and responses", "of students", "emerge from", "about learning and,", "as a result,"],
        "roles": [r("these attitudes and responses", "S"), r("emerge", "V"), r("teachers", "S"), r("think", "V")],
        "modifiers": ["on the part of students"],
        "steps": [
            sv("s3_sv", ["these attitudes and responses", "students", "emerge", "teachers", "think"],
               {"these attitudes and responses": "S", "emerge": "V"},
               {"students": "그건 on the part of(~ 쪽의) 뒤, 누구의 태도인지 알려 주는 말이에요.",
                "teachers": "그건 the way(~하는 방식)를 꾸며 주는 덩어리 안의 주어예요.",
                "think": "그건 the way(~하는 방식)를 꾸며 주는 덩어리 안의 동사예요."},
               "주어는 these attitudes and responses, 동사는 emerge (from)예요.",
               ask="긴 문장이에요. 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s3_these",
                   "these attitudes and responses(이런 태도와 반응)는 무엇을 가리킬까요?",
                   [("o0", "책 앞에서 보내는 시간", False), ("o1", "학생이 자신을 보고, 참여하고, 반응하는 방식", True),
                    ("o2", "선생님이 수업을 꾸린 방식", False)],
                   "these는 바로 앞 문장을 가리켜요. view·engage·respond를 봐요.",
                   why="these는 바로 앞 문장의 질적 변화, 학생이 자신을 보고 참여하고 반응하는 방식을 받아요.",
                   highlight=["these attitudes and responses"]),
            show("s3_from",
                 "학생의 이런 태도는 선생님이 학습을 어떻게 생각하고 수업을 어떻게 꾸리는지에서 나온대요.",
                 highlight=["emerge from", "the way teachers think about learning"],
                 tips=[tip("emerge from", "'~에서 나오다, 생겨나다'예요. A emerge from B = A는 B에서 나온다.", "emerge from")]),
            flow("s3_flow", "②", "질적 변화가 돕는다", "그 태도는 선생님의 생각·수업 방식에서 나온다", True,
                 "these attitudes가 바로 앞 질적 변화를 받아요. 그대로 이어져요."),
        ],
    },
    {
        "id": 5, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("But", "하지만"), g("that’s unlikely", "그것은 ~할 것 같지 않다"), g("unlikely", "~할 것 같지 않은"),
                    g("to have a positive effect", "좋은 영향을 주는 것"), g("positive", "긍정적인"),
                    g("the critical variables", "중요한 변수"), g("critical", "중요한, 결정적인"), g("variables", "변수, 요인"),
                    g("Ames identifies", "Ames가 밝혀낸"), g("identifies", "밝히다, 찾아내다")],
        "slashes": ["that’s unlikely", "a positive effect", "the critical variables"],
        "roles": [r("that", "S"), r("’s", "V"), r("unlikely", "C")],
        "steps": [
            choice("s4_mean",
                   "'that’s unlikely to have a positive effect on the critical variables'는 무슨 뜻일까요?",
                   [("o0", "그것은 중요한 변수에 꼭 좋은 영향을 준다", False), ("o1", "그것은 변수와 아무 상관이 없다", False),
                    ("o2", "그것은 중요한 변수에 좋은 영향을 줄 것 같지 않다", True)],
                   "unlikely to ~는 '~할 것 같지 않다'예요.",
                   why="unlikely to ~는 '~할 것 같지 않다'예요. 그것(that)은 Ames가 밝힌 중요한 변수에 좋은 영향을 줄 것 같지 않대요.",
                   highlight=["unlikely to have a positive effect"]),
            choice("s4_var",
                   "the critical variables that Ames identifies(Ames가 밝힌 중요한 변수)는 칠판 어느 쪽일까요?",
                   [("o0", QUANT, False), ("o1", QUAL, True)],
                   "Ames는 무엇이 아이들을 더 잘 배우게 돕는다고 했는지 떠올려 봐요.",
                   why="Ames는 질적 변화가 돕는다고 했어요. Ames가 밝힌 중요한 변수는 오른쪽, 질적 변화예요.",
                   panel=board(L1, R1, sort=["the critical variables"]), highlight=["the critical variables that Ames identifies"]),
            choice("s4_that",
                   "그럼 that(그것)은 질적 변화에 도움이 안 되는 것이어야 해요. 바로 앞 문장의 '선생님의 생각·수업 방식'이 that일 수 있을까요?",
                   [("o0", "네, 될 수 있어요", False), ("o1", "아니요, 안 돼요", True)],
                   "바로 앞 문장에서 학생의 태도(질적 변화)는 어디에서 나온다고 했는지 떠올려 봐요.",
                   why="학생의 태도(질적 변화)는 선생님의 생각·수업 방식에서 나온다고 했어요. 그게 질적 변화에 도움이 안 된다는 건 말이 안 맞아요.",
                   highlight=["But", "that’s"]),
            show("s4_break",
                 "That이 가리킬, 질적 변화에 도움이 안 되는 방법이 But 바로 앞에 있어야 해요. 지금 앞에는 그런 방법이 없어요.",
                 panel=board(L1 + [("that = ?", "도움 안 되는 방법")], R1, fresh=("that = ?",)),
                 highlight=["But that’s"], point="③ 앞에 that이 받을 '도움 안 되는 방법'이 없다 → 흐름이 끊긴다"),
            flow("s4_flow", "③", "태도는 선생님의 생각·수업 방식에서 나온다", "하지만 그것은 좋은 영향을 줄 것 같지 않다", False,
                 "that이 받을 '도움 안 되는 방법'이 앞에 없어요. 갑자기 But으로 반박해서 흐름이 끊겨요."),
        ],
    },
    {
        "id": 6, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("Perhaps", "아마도"), g("it makes sense", "타당하다, 말이 된다"), g("to see education", "교육을 보는 것"),
                    g("as being", "~인 것으로"), g("less about how much the teacher covers", "선생님이 얼마나 많이 다루는가와는 덜 관련되고"),
                    g("covers", "다루다"), g("more about what the students can be helped to discover", "학생이 무엇을 발견하도록 도움받을 수 있는가와 더 관련된"),
                    g("discover", "발견하다"), g("education", "교육")],
        "slashes": ["it makes sense", "to see education", "as being less about", "the teacher covers", "and more about",
                    "the students"],
        "roles": [r("it", "S"), r("makes", "V"), r("sense", "O")],
        "steps": [
            choice("s5_lessmore",
                   "'less about how much the teacher covers and more about what the students can be helped to discover'는 무슨 말일까요?",
                   [("o0", "교육은 선생님이 많이 다룰수록 좋다", False),
                    ("o1", "교육은 얼마나 많이 다루느냐보다, 학생이 무엇을 발견하게 돕느냐다", True),
                    ("o2", "학생은 스스로 무언가를 발견할 수 없다", False)],
                   "less about A and more about B는 'A보다는 B에 관한 것'이에요.",
                   why="less about A and more about B는 'A보다는 B에 관한 것'이에요. 교육은 얼마나 많이 다루느냐보다 학생이 무엇을 발견하게 돕느냐래요.",
                   highlight=["less about how much the teacher covers", "more about what the students can be helped to discover"],
                   tips=[tip("see A as B", "'A를 B로 보다'예요. see education as being … = 교육을 ~인 것으로 보다.", "see")]),
            flow("s5_flow", "④", "하지만 그것은 좋은 영향을 줄 것 같지 않다", "교육은 무엇을 발견하게 돕느냐다", True,
                 "도움 안 되는 방법을 반박한 뒤, 교육을 다르게 보자고 이어 가요. 흐름이 끊기지 않아요."),
        ],
    },
    {
        "id": 7, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("More time", "더 많은 시간"), g("won’t do a thing", "아무것도 하지 못할 것이다"), g("a thing", "어떤 것"),
                    g("to bring about", "일으키는 데"), g("bring about", "일으키다"), g("that shift", "그런 변화"), g("shift", "변화, 전환")],
        "slashes": ["More time", "won’t do a thing", "to bring about"],
        "roles": [r("More time", "S"), r("won’t do", "V"), r("a thing", "O")],
        "steps": [
            show("s6_shift",
                 "that shift(그런 변화)는 바로 앞, 교육을 보는 눈을 바꾸는 거예요. 시간만 더 쓴다고 그 변화가 생기진 않는대요.",
                 highlight=["More time", "that shift"],
                 tips=[tip("won’t do a thing", "'아무것도 하지 못할 것이다', 즉 전혀 도움이 안 된다는 말이에요.", "won’t do a thing")]),
            flow("s6_flow", "⑤", "교육은 무엇을 발견하게 돕느냐다", "시간만 늘려서는 그 변화가 안 생긴다", True,
                 "that shift가 바로 앞, 교육을 보는 눈의 변화를 받아요. 그대로 이어져요."),
            show("s6_go", "①~⑤ 중 흐름이 끊긴 곳은 하나였어요. 주어진 문장의 maximize time on task를 떠올리며 골라 봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 초급 기본 — 문장마다 「주어·동사 + 뜻」 또는 「해석 맞추기」 하나 (2026-10-15 선생님)
add_basic(sentences, 2, [m("Carole Ames", "Carole Ames는"), " ", m("help children to learn better", "아이들이 더 잘 배우게 돕는 것은"), " ",
                         m("quantitative changes in behavior", "행동의 양적 변화"), "가 아니라고 ", m("points out", "지적한다"), "."],
          match_display="Carole Ames points out that it isn’t quantitative changes in behavior that help children to learn better.",
          sv_id="s1_sv", meaning_ids=["s1_cleft"])
add_basic(sentences, 3, [m("Rather", "오히려"), " ", m("in the ways students view themselves", "학생이 자신을 바라보는 방식에서의"), " ",
                         m("qualitative changes", "질적 변화"), "예요."],
          match_display="Rather, it’s qualitative changes in the ways students view themselves.",
          meaning_ids=["s2_rather"])
add_basic(sentences, 4, [m("these attitudes and responses", "이런 태도와 반응은"), " ",
                         m("the way teachers think about learning", "선생님이 학습을 생각하는 방식"), " ", m("emerge from", "~에서 나온다"), "."],
          match_display="In turn, these attitudes and responses emerge from the way teachers think about learning.",
          sv_id="s3_sv", meaning_ids=["s3_from"])
add_basic(sentences, 5, [m("But", "하지만"), " ", m("the critical variables", "중요한 변수"), "에 ", m("to have a positive effect", "좋은 영향을 줄"), " — ",
                         m("that’s unlikely", "그것은 ~ 것 같지 않다"), "."],
          match_display="But that’s unlikely to have a positive effect on the critical variables.",
          meaning_ids=["s4_mean"])
add_basic(sentences, 6, [m("less about how much the teacher covers", "선생님이 얼마나 많이 다루는가와는 덜 관련되고"), " ",
                         m("more about what the students can be helped to discover", "학생이 무엇을 발견하게 도움받는가와 더 관련된 것으로"), " ",
                         m("to see education", "교육을 보는 것이"), " ", m("it makes sense", "타당하다"), "."],
          meaning_ids=["s5_lessmore"])
add_basic(sentences, 7, [m("More time", "더 많은 시간은"), " ", m("that shift", "그런 변화"), "를 ", m("to bring about", "일으키는 데"), " ",
                         m("won’t do a thing", "아무것도 하지 못할 것이다"), "."],
          sv_new=sv_step("s7_basic_sv", ["More time", "won’t do", "a thing", "that shift"],
                         {"More time": "S", "won’t do": "V", "a thing": "O"},
                         {"that shift": "그건 bring about(일으키다)의 목적어예요."},
                         "주어는 More time, 동사는 won’t do, 목적어는 a thing이에요."),
          meaning_ids=["s6_shift"])

SENSES = {
    1: [sense("if", "If the goal is", "만약 ~라면", "접속사 if + 주어·동사 (조건)"),
        sense("to", "is to figure out", "~하는 것", "be + to부정사 — 보어 '~하는 것'"),
        sense("to", "how best to cover", "~할 (방법)", "how + to부정사 = 어떻게 ~할지"),
        sense("to", "— to fill students", "~하는 것", "to부정사 '~하는 것' — 대시 사이, 앞말을 다시 풂"),
        sense("to", "appropriate to try", "~하는 것 (진짜 주어)", "가주어 it … to부정사"),
        sense("to", "try to maximize", "~하려고", "try + to부정사 = ~하려고 애쓰다"),
        sense("as", "such as by assigning", "예를 들어 ~ 같은", "such as = 예를 들어")],
    2: [sense("that", "points out that", "~라고", "명사절 접속사 that — 지적한 내용"),
        sense("as", "such as requiring", "예를 들어 ~ 같은", "such as = 예를 들어"),
        sense("to", "students to spend", "~하도록", "require + 사람 + to부정사 = 사람에게 ~하도록 요구하다"),
        sense("that", "that help children", "~하는 것은 (강조)", "it is A that ~ 강조 구문의 that"),
        sense("to", "children to learn", "~하도록", "help + 사람 + to부정사 = 사람이 ~하게 돕다")],
    3: [sense("to", "in relation to the task", "~와 (관련하여)", "in relation to + 명사 = ~와 관련하여"),
        sense("to", "respond to", "~에 (반응하다)", "respond to + 명사 = ~에 반응하다")],
    4: [sense("as", "as a result", "~로서", "as a result = 그 결과로")],
    5: [sense("but", "But that’s", "하지만", "접속사 But — 앞 내용을 반박"),
        sense("that", "that’s unlikely", "그것", "지시대명사 that — 앞에 나온 것을 가리킴"),
        sense("to", "unlikely to have", "~할 (것 같지 않다)", "be unlikely to부정사 = ~할 것 같지 않다"),
        sense("that", "variables that Ames identifies", "(앞 명사를 꾸밈)", "관계대명사 that + 주어·동사 (목적어 빠짐)")],
    6: [sense("to", "makes sense to see", "~하는 것 (진짜 주어)", "가주어 it … to부정사"),
        sense("as", "see education as being", "~로", "see A as B = A를 B로 보다"),
        sense("to", "helped to discover", "~하도록", "be helped to부정사 = ~하도록 도움받다")],
    7: [sense("to", "to bring about", "~하는 데", "to부정사 — 목적 '~하는 데, ~하기 위해'"),
        sense("that", "that shift", "그 (변화)", "지시형용사 that + 명사")],
}

WORDS = {"goal": "목표", "figure": "모양 · figure out = 알아내다", "best": "가장 잘", "cover": "다루다", "set": "정해진",
         "curriculum": "교육과정", "fill": "채우다", "students": "학생들", "facts": "사실들", "seem": "~해 보이다",
         "appropriate": "적절한", "try": "애쓰다, 해 보다", "maximize": "최대로 늘리다", "time": "시간", "task": "과제",
         "assigning": "(과제를) 내 주는 것", "homework": "숙제", "carole": "캐롤 · 사람 이름", "ames": "에임스 · 사람 이름",
         "dean": "학장", "college": "단과 대학", "education": "교육", "michigan": "미시간 · 미국의 주 이름", "state": "주",
         "university": "대학교", "points": "가리키다 · point out = 지적하다", "quantitative": "양적인", "changes": "변화",
         "behavior": "행동", "requiring": "요구하는 것", "spend": "(시간을) 보내다", "hours": "시간", "front": "앞 · in front of = ~ 앞에",
         "books": "책", "worksheets": "학습지", "help": "돕다", "children": "아이들", "learn": "배우다", "better": "더 잘",
         "rather": "오히려", "qualitative": "질적인", "ways": "방식들", "view": "보다, 여기다", "themselves": "자기 자신",
         "relation": "관계 · in relation to = ~와 관련하여", "engage": "참여하다", "process": "과정", "learning": "학습",
         "respond": "반응하다", "activities": "활동", "situation": "상황", "turn": "차례 · in turn = 결국, 이번엔 또",
         "attitudes": "태도", "responses": "반응", "part": "부분, 쪽 · on the part of = ~ 쪽의", "emerge": "나오다",
         "teachers": "선생님들", "think": "생각하다", "result": "결과", "they’ve": "그들은 ~했다", "organized": "꾸렸다",
         "classrooms": "교실, 수업", "unlikely": "~할 것 같지 않은", "positive": "긍정적인", "effect": "영향, 효과",
         "critical": "중요한", "variables": "변수", "identifies": "밝히다", "perhaps": "아마도", "makes": "만들다 · make sense = 말이 되다",
         "sense": "감각, 의미 · make sense = 타당하다", "teacher": "선생님", "covers": "다루다", "helped": "도움받은",
         "discover": "발견하다", "won’t": "~하지 않을 것이다", "thing": "것", "bring": "가져오다 · bring about = 일으키다",
         "shift": "변화, 전환", "goal.": "목표", "student": "학생", "being": "~인 것", "how": "어떻게", "much": "많이",
         "what": "무엇", "can": "~할 수 있다", "less": "덜", "more": "더", "see": "보다", "it’s": "그것은 ~이다", "that’s": "그것은 ~이다",
         "way": "방식", "do": "하다", "if": "만약 ~라면", "then": "그러면", "might": "~일지도 모른다", "isn’t": "~이 아니다",
         "have": "가지다", "ames’": "에임스의"}

STORIES = [
    (3, [sc("주어진 문장", "📚", "maximize time on task · might seem", "목표가 사실로 채우는 거라면, 숙제로 공부 시간을 늘리는 게 맞아 보일 수도 있어요"),
         sc("문장 1~2", "🔄", "not quantitative · rather qualitative", "Ames: 더 잘 배우게 돕는 건 양적 변화가 아니라 질적 변화예요")]),
    (5, [sc("②~③", "👩‍🏫", "emerge from · But that’s unlikely", "학생 태도는 선생님의 생각·수업 방식에서 나오고, 무언가는 좋은 영향을 못 준대요")]),
    (7, [sc("④~⑤", "🔍", "less covers · more discover", "교육은 얼마나 다루느냐보다 무엇을 발견하게 돕느냐 — 시간만 늘려선 그 변화가 안 생겨요")]),
]

OPTIONS = [
    ("1", "Rather, it’s qualitative changes … 앞", "돕는 건 양적 변화가 아니다 뒤", False),
    ("2", "In turn, these attitudes … 앞", "오히려 질적 변화다 뒤", False),
    ("3", "But that’s unlikely … 앞", "태도는 선생님의 생각·수업 방식에서 나온다 뒤", True),
    ("4", "Perhaps it makes sense … 앞", "그것은 좋은 영향을 줄 것 같지 않다 뒤", False),
    ("5", "More time won’t do a thing … 앞", "교육은 무엇을 발견하게 돕느냐다 뒤", False),
]
exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳을 고르시오. [3점]",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"], "numbers_only": True,
    "passage_keywords": ["maximize time on task", "might seem", "quantitative changes", "qualitative changes", "Rather",
                         "these attitudes and responses", "But that’s unlikely", "the critical variables", "less about", "more about",
                         "More time"],
    "sentence": 1, "analysis_first": True, "wrong_rate": 52.0, "wrong_rank": 6,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "③ 뒤 But that’s의 that이 무엇을 가리켜야 하는지 떠올리며 들어갈 곳을 골라 봐요.",
        "정답이에요! 태도는 선생님의 생각·수업 방식에서 나온다 → 목표가 사실로 채우는 거라면 숙제로 시간을 늘리는 게 맞아 보일 수도 있다(주어진 문장) → 하지만 그것(시간 늘리기)은 질적 변화에 좋은 영향을 못 준다, 순서예요.",
        "정답은 ③이에요. But that’s unlikely의 that이 받을 '시간 늘리기'를 주어진 문장이 먼저 꺼내 줘야 해요.",
        {"1": "① 뒤 Rather는 바로 앞 '양적 변화가 아니다'를 받아 진짜를 말해요. 그 사이에 끼어들 자리가 아니에요.",
         "2": "② 뒤 these attitudes and responses는 바로 앞 질적 변화(보고·참여하고·반응하는 방식)를 받아요. 사이에 넣으면 these가 가리킬 게 없어져요.",
         "4": "④에 넣으면 ③ 뒤 But that’s의 that이 '선생님의 생각·수업 방식'을 가리키게 돼요. 질적 변화를 만드는 쪽이 좋은 영향을 못 준다는 건 말이 안 맞아요.",
         "5": "⑤ 앞은 교육을 다르게 보자는 말이고, 뒤 that shift가 바로 그 변화를 받아요. 사이에 넣으면 흐름이 끊겨요."},
        {"4": review(23,
                     "④에 넣으면 ③ 뒤 'But that’s unlikely …'의 that이 바로 앞 '선생님의 생각·수업 방식'을 가리켜요. 학생 태도(질적 변화)를 만드는 그 방식이 좋은 영향을 못 준다는 건 말이 안 맞아요. that이 받을 '시간 늘리기'(주어진 문장)가 But 앞, ③에 와야 해요.",
                     panel=rows(("② 뒤", "these attitudes … emerge from the way teachers think", "태도는 선생님의 생각에서 나온다", "hl"),
                                ("주어진 문장", "maximize time on task", "시간 늘리기 = 양적 변화", "hl2"),
                                ("③ 뒤", "But that’s unlikely to have a positive effect", "that = 시간 늘리기", "hl")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 39번 (주어진 문장 넣기, 3점)",
    topic="문장 넣기 푸는 법: 주어진 문장의 단서 → 앞뒤 예측 → ①~⑤ 흐름이 끊기는 곳",
    method={"type": "sentence_insertion", "labels": ["주어진 문장 단서 찾기", "앞에 올 내용 예측하기", "흐름 끊기는 곳 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-time-on-task.svg", ("More time", "더 많은 시간"), "→", ("Learning", "배움"),
                                       "공부 시간을 늘리면 더 잘 배울까?", "2022년 3월 39번 도입 칠판"),
                      "alt": "칠판: More time(더 많은 시간) → Learning(배움)", "kind": "drawing"},
            "method": METHOD_IMAGES["insert"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "숙제를 많이 내서 공부 시간을 늘리면 더 잘 배울까요? 이번 글은 무엇이 배움을 돕는지 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "문장 넣기는 주어진 문장부터 꼼꼼히 봐야 해요. 그 안에 앞 문장과 이어지는 단서가 숨어 있거든요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "단서를 찾고, 앞에 올 내용을 예측한 뒤, 흐름이 끊기는 곳을 찾을 거예요. 칠판 순서대로 해 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("figure out", "알아내다"), g("cover", "(내용을) 다루다"), g("curriculum", "교육과정"),
                           g("appropriate", "적절한"), g("maximize", "최대화하다"), g("assign", "(과제를) 내 주다"),
                           g("point out", "지적하다"), g("quantitative", "양적인"), g("qualitative", "질적인"),
                           g("in relation to", "~와 관련하여"), g("engage in", "~에 참여하다"), g("in turn", "결국, 차례로"),
                           g("emerge from", "~에서 생겨나다"), g("unlikely", "~할 것 같지 않은"), g("critical", "중요한"),
                           g("variable", "변수"), g("identify", "밝히다"), g("make sense", "타당하다"), g("bring about", "일으키다"),
                           g("shift", "변화, 전환")],
               "options": []},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# cover (교육과정을) 다루다 · set 정해진 · critical 중요한.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    1: [tip("cover", "이 글에서는 → (교육과정을) 다루다  ('덮다' 아님)", "cover", trap=True),
        tip("set", "이 글에서는 → 정해진  ('세트' 아님)", "set curriculum", trap=True)],
    5: [tip("critical", "이 글에서는 → 중요한  ('비판적인' 아님)", "critical", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="문장 넣기 푸는 법",
       chunks={"the goal": "목표", "is": "~이다", "students": "학생들", "it": "그것 · 가짜 주어", "might seem": "~해 보일 수도 있다",
               "appropriate": "적절한", "Carole Ames": "캐롤 에임스", "dean of the college of education": "사범 대학 학장",
               "points out": "지적하다", "help children to learn better": "아이들이 더 잘 배우게 돕다",
               "quantitative changes in behavior": "행동의 양적 변화", "Rather": "오히려", "qualitative changes": "질적 변화",
               "in the ways students view themselves": "학생이 자신을 바라보는 방식에서",
               "these attitudes and responses": "이런 태도와 반응", "emerge": "나오다", "teachers": "선생님들", "think": "생각하다",
               "emerge from": "~에서 나오다", "the way teachers think about learning": "선생님이 학습에 대해 생각하는 방식",
               "But": "하지만", "the critical variables": "중요한 변수", "to have a positive effect": "좋은 영향을 주는 것",
               "that’s unlikely": "그것은 ~할 것 같지 않다",
               "less about how much the teacher covers": "선생님이 얼마나 많이 다루는가와는 덜 관련되고",
               "more about what the students can be helped to discover": "학생이 무엇을 발견하도록 도움받을 수 있는가와 더 관련된",
               "to see education": "교육을 보는 것", "it makes sense": "타당하다", "More time": "더 많은 시간", "won’t do": "하지 않을 것이다",
               "a thing": "어떤 것", "that shift": "그런 변화", "to bring about": "일으키는 데", "won’t do a thing": "아무것도 하지 못할 것이다"})
