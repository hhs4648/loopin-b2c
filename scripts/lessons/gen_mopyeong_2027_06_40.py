"""2026년 6월 모의평가(2027학년도) 40번 레슨 + 대사를 만든다 (요약문 완성, 2점). 오답률 61% · Top 4 (메가스터디).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_40.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/summary.md — 선생님이 고른 「지문 먼저 → 요약문」(2024년 3월 40번과 같게, method.type = summary).
지문을 처음부터 읽으며 칠판 두 칸에 말을 모은다 — 왼쪽 「the rich 쪽」(the rich · First World illnesses · diseases that “pay”),
오른쪽 「rare · poor 쪽」(rare diseases · poor · cannot afford to pay · neglected · neglected populations).
요약문 (A)는 less profitable diseases(수익이 덜 나는 병)가 불균형 때문에 겪은 일 → 오른쪽 → 무시(disregard),
(B)는 의학 연구의 초점이 넓혀져 포함할 사람들 → 오른쪽 → 서비스를 충분히 못 받는(underserved).
정답 ⑤ disregard ······ underserved.
선택률(메가스터디): ① 33 · ② 14 · ③ 7 · ④ 7 · ⑤ 39 — 많이 고른 오답 ① prevention·marginalized.
①은 (B) marginalized(소외된)는 맞고 (A) prevention(예방)만 틀림 — 「두 칸 다 맞아야」를 option_review로 짚는다.
offset·demographic은 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지(content/tutor/exam-source/2027-06-평가원/해설.txt) 해석과 대조함 — employ 활용하다, to date 지금까지, affect (병이) 걸리게 하다,
neglect 등한시하다, democratizing 민주화하는, 보기 뜻(① 예방–소외된 … ⑤ 무시–서비스를 충분히 받지 못하는).
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음), 칠판 묶음 이름은 지문 말까지만.
Claude 초안(2026-10-21) — 선생님 검토 전.

선생님이 확인할 점
1. 칠판 두 쪽 이름을 「the rich 쪽 ↔ rare · poor 쪽」(1~3문장에 나온 말)으로 했다. (A)·(B)가 둘 다 오른쪽이라
   「(A)는 어느 쪽?」 2지가 쉬운 편이다 — 쪽 고르기 대신 바로 뜻 3지로 갈지 정해 주세요.
2. ① prevention(예방)을 많이 고른 이유를 「AI가 병을 막아 준다는 좋은 이야기로 읽고 led to 뒤를 좋은 결과로 짐작」으로 봤다(추측).
   s6_a 오답 보기에 「미리 막음(예방)」을 넣어 그 오독을 직접 짚었다.
3. 칠판 정리(story)는 넣지 않았다 — 문장이 5개뿐이고 두 쪽 칠판이 이미 정리 역할을 해서(칠판이 너무 많다는 2026-10-20 피드백).
4. 3문장 even if 절 안의 S·V(a disease · is)는 끊어읽기 roles에서 뺐다 — 앞의 that is의 is와 화면 자리가 겹친다.
5. 헷갈리는 단어(trap): employed(활용되는, 고용된 X) · to date(지금까지, 날짜 X) · affect((병이) 걸리게 하다). 엑셀에는 안 넣었다.
6. 해석 맞추기는 2문장에만(문장 뜻 객관식 대신). 나머지 문장은 뜻 3지.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-06-40-ai-neglected-diseases"

SUMMARY = ("By lowering the cost of pharmaceutical research and development, AI can help reduce the imbalance in investment that has led to "
           "the (A) ________ of less profitable diseases, thereby broadening the focus of medical research to include (B) ________ populations.")
S = [
    "In the pharmaceutical industry, algorithms are being employed to find treatments and drugs for rare diseases that to date haven’t "
    "received much attention.",
    "The hard truth has always been that pharma devotes more research and development resources to diseases that affect the rich.",
    "The definition of rare has too often been associated with poor — that is, even if a disease is quite prevalent in a population that "
    "cannot afford to pay for it (for example, people living in the developing world), the disease has been neglected compared to First "
    "World illnesses.",
    "By lowering the cost of data collection, mining, and analysis in drug development and clinical trials, AI can help offset imbalances "
    "in the pharmaceutical industry that direct attention to diseases that “pay,” whether because the disease is more common or because "
    "it is prevalent among demographics that can pay more.",
    "We see the democratizing power of AI to broaden the attention of the medical and research communities to find cures to traditionally "
    "neglected health issues and among traditionally neglected populations.",
    SUMMARY,
]
# 해설지 해석 (2027-06-평가원/해설.txt 40번)
KO = [
    "제약 산업에서는 지금까지 많은 관심을 받지 못했던 희귀한 질병의 치료법과 의약품을 찾기 위해 알고리즘이 활용되고 있다.",
    "냉혹한 진실은 제약 회사들이 부유한 사람들이 걸리는 질병에 늘 더 많은 연구개발 자원을 쏟아 왔다는 점이다.",
    "희귀하다는 것의 정의는 빈곤과 연관된 경우가 아주 흔했는데, 즉, 어떤 질병이 비용을 감당할 수 없는 어떤 사람들(예를 들어 개발도상국에 살고 있는 "
    "사람들) 사이에 꽤 널리 퍼져있다 할지라도 그 질병은 부유한 선진국 질환에 비해 등한시되어왔다.",
    "AI는 신약 개발과 임상시험에서 데이터 수집, 데이터 마이닝, 그리고 데이터 분석 비용을 낮춤으로써, 그 질병이 더 흔하기 때문이든, 혹은 그것이 더 "
    "많은 돈을 낼 수 있는 인구 집단에 널리 퍼져있기 때문이든, ‘수익을 내는’ 질병에 관심을 향하게 하는, 제약 산업에서의 불균형을 상쇄하는 데 도움이 될 수 있다.",
    "우리는 의료계와 연구계의 관심을 넓혀 전통적으로 등한시되어 온 건강 문제의 해결책을 찾고, 전통적으로 등한시되어 온 사람들에게도 관심을 기울이게 할 "
    "AI의 민주화하는 힘을 보고 있다.",
    "제약 연구개발 비용을 낮춤으로써 AI는 수익성이 낮은 질병에 대한 (A)를 초래했던 투자에서의 불균형을 줄이고 그 결과 의학 연구의 초점을 (B) 사람들에게로 "
    "확대하는 데 도움을 줄 수 있다.",
]

LEFT = "왼쪽 · the rich 쪽"
RIGHT = "오른쪽 · rare · poor 쪽"


def board(left, right, fresh=(), sort=None):
    """두 쪽 칠판 — 묶음 이름은 1~3문장에 나온 말까지만. 요약문 (A)(B) 자리 말·보기 단어는 쓰지 않는다"""
    return groups("pharma의 attention(관심)", "the rich 쪽", left, "rare · poor 쪽", right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": LEFT, "right": RIGHT} if sort else None)


L3 = [("the rich", "부자들"), ("First World illnesses", "선진국 질병")]
R3 = [("rare diseases", "희귀 질병"), ("poor", "가난한"), ("cannot afford to pay", "돈을 낼 수 없다"), ("neglected", "등한시된")]
L4 = L3 + [("diseases that “pay”", "돈이 되는 병")]
R5 = R3 + [("neglected populations", "등한시된 사람들")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("In the pharmaceutical industry", "제약 산업에서"), g("pharmaceutical", "제약의"), g("industry", "산업"),
                    g("algorithms", "알고리즘"), g("are being employed", "활용되고 있다"), g("employed", "활용되는"),
                    g("to find treatments and drugs", "치료법과 의약품을 찾기 위해"), g("treatments", "치료법"), g("drugs", "의약품, 약"),
                    g("rare diseases", "희귀 질병"), g("rare", "희귀한, 드문"), g("diseases", "질병"),
                    g("to date", "지금까지"), g("haven’t received much attention", "많은 관심을 받지 못했다"),
                    g("received", "받았다"), g("attention", "관심")],
        "slashes": ["In the pharmaceutical industry,", "are being employed", "and drugs", "rare diseases"],
        "roles": [r("algorithms", "S"), r("are being employed", "V")],
        "modifiers": ["that to date haven’t received much attention"],
        "steps": [
            choice("s1_rare",
                   "알고리즘(algorithms)은 어떤 질병의 치료법을 찾는 데 쓰이고 있대요?",
                   [("o0", "지금까지 관심을 많이 받지 못한 희귀 질병", True), ("o1", "이미 치료법이 많이 나온 흔한 질병", False),
                    ("o2", "알고리즘 때문에 새로 생긴 질병", False)],
                   "rare diseases 뒤 'that to date haven’t received much attention'을 봐요. to date는 '지금까지'예요.",
                   why="'rare diseases that to date haven’t received much attention'이에요. 희귀하고, 지금까지 관심을 별로 못 받은 병이래요.",
                   highlight=["rare diseases", "haven’t received much attention"],
                   tips=[tip("요약문 문제 요령", "지문을 먼저 읽으며 글쓴이 주장을 잡고 같은 쪽 말을 모아요. 마지막에 요약문 (A)(B)가 각각 어느 쪽 말인지 보고 골라요.")],
                   point="rare diseases that to date haven’t received much attention = 지금까지 관심을 못 받은 희귀 질병"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("The hard truth", "냉혹한 진실"), g("hard", "냉혹한, 힘든"), g("truth", "진실"), g("has always been", "늘 ~였다"),
                    g("pharma", "제약 회사"), g("devotes", "쏟다, 바치다"),
                    g("more research and development resources", "더 많은 연구 개발 자원"), g("research", "연구"),
                    g("development", "개발"), g("resources", "자원"), g("diseases that affect the rich", "부자들이 걸리는 질병"),
                    g("affect", "(병이) 걸리게 하다, 침범하다"), g("the rich", "부자들")],
        "slashes": ["has always been", "pharma devotes", "development resources"],
        "roles": [r("The hard truth", "S"), r("has always been", "V"), r("pharma", "S"), r("devotes", "V"),
                  r("more research and development resources", "O")],
        "modifiers": ["that affect the rich"],
        "steps": [],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("The definition of rare", "'희귀하다'의 정의"), g("definition", "정의"),
                    g("has too often been associated with", "너무 자주 ~와 연관되어 왔다"), g("associated", "연관된"),
                    g("associated with poor", "가난과 연관된"), g("poor", "가난한, 가난"), g("that is", "즉, 다시 말해"),
                    g("even if", "비록 ~일지라도"), g("a disease", "어떤 질병"), g("quite prevalent", "꽤 널리 퍼진"),
                    g("prevalent", "널리 퍼진, 흔한"), g("in a population", "어떤 사람들 사이에"), g("population", "인구, 사람들"),
                    g("cannot afford to pay", "돈을 낼 여유가 없다"), g("cannot afford", "~할 여유가 없다"), g("afford", "(비용을) 감당하다"),
                    g("pay for it", "그 값을 치르다"), g("for example", "예를 들어"),
                    g("people living in the developing world", "개발도상국에 사는 사람들"), g("developing world", "개발도상국"),
                    g("the disease", "그 질병"), g("has been neglected", "등한시되어 왔다"), g("neglected", "등한시된, 방치된"),
                    g("compared to", "~에 비해"), g("First World illnesses", "선진국 질병"), g("illnesses", "질병")],
        "slashes": ["The definition of rare", "associated with poor", "— that is,", "even if a disease", "quite prevalent",
                    "in a population", "pay for it", "developing world),", "has been neglected"],
        "roles": [r("The definition of rare", "S"), r("has too often been associated with", "V"), r("the disease", "S"),
                  r("has been neglected", "V")],
        "modifiers": ["that cannot afford to pay for it", "living in the developing world"],
        "steps": [
            choice("s3_poor",
                   "'The definition of rare has too often been associated with poor'는 무슨 말일까요?",
                   [("o0", "'희귀하다'는 말이 너무 자주 가난과 연결되어 왔다", True),
                    ("o1", "가난한 사람들은 희귀한 병에 잘 걸리지 않는다", False),
                    ("o2", "희귀한 병일수록 가난한 나라에서 먼저 치료된다", False)],
                   "be associated with는 '~와 연관되다'예요. rare(희귀한)와 poor(가난한)가 묶여 왔대요.",
                   why="'associated with poor', 희귀하다는 말이 가난함과 너무 자주 묶여 왔대요. 대시(—) 뒤 that is(즉)가 그 뜻을 풀어 줘요.",
                   highlight=["rare", "associated with poor"],
                   tips=[tip("be associated with", "'~와 연관되다, ~와 결부되다'예요.", "associated with")]),
            choice("s3_neglect",
                   "대시(—) 뒤를 봐요. 돈을 낼 수 없는 사람들 사이에 널리 퍼진 병은 어떻게 되어 왔대요?",
                   [("o0", "선진국 질병에 비해 등한시되어 왔다", True), ("o1", "선진국 질병보다 먼저 치료되어 왔다", False),
                    ("o2", "널리 퍼져서 더는 희귀하지 않게 되었다", False)],
                   "문장 끝 'has been neglected compared to First World illnesses'를 봐요. neglect는 '등한시하다, 방치하다'예요.",
                   why="'the disease has been neglected', 그 병은 선진국 질병에 비해 방치되어 왔대요. 꽤 널리 퍼져 있어도 그랬대요.",
                   highlight=["cannot afford", "neglected"],
                   faded=["(for example, people living in the developing world)"],
                   tips=[tip("that is (대시 뒤)", "'즉, 다시 말해'예요. 앞말을 풀어 줘요.", "that is"),
                         tip("even if", "'비록 ~일지라도'예요. even if a disease is quite prevalent = 병이 꽤 널리 퍼져 있어도.", "even if")]),
            show("s3_board",
                 "희귀한(rare) 병은 사실상 돈을 낼 수 없는 가난한(poor) 사람들의 병이에요. 그래서 부자들(the rich)의 병에 비해 등한시돼 왔어요.",
                 panel=board(L3, R3, fresh=("the rich", "First World illnesses", "rare diseases", "poor", "cannot afford to pay", "neglected")),
                 highlight=["poor", "neglected"], button="다음 문장",
                 point="rare = poor(돈을 낼 수 없는 사람들의 병) → 선진국 질병에 비해 neglected(등한시됨)"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("By lowering the cost", "비용을 낮춤으로써"), g("lowering", "낮추는 것"), g("cost", "비용"),
                    g("data collection, mining, and analysis", "데이터 수집, 마이닝, 분석"), g("data", "데이터"), g("collection", "수집"),
                    g("mining", "(데이터) 마이닝 · 데이터에서 쓸모 있는 정보를 캐내는 일"), g("analysis", "분석"),
                    g("in drug development and clinical trials", "신약 개발과 임상 시험에서"), g("drug", "약"),
                    g("clinical trials", "임상 시험"), g("clinical", "임상의"), g("trials", "시험"),
                    g("AI", "인공지능"), g("can help offset", "상쇄하는 데 도움이 될 수 있다"), g("offset", "상쇄하다"),
                    g("imbalances", "불균형"), g("in the pharmaceutical industry", "제약 산업에서의"),
                    g("direct attention to", "~로 관심을 향하게 하다"), g("direct", "향하게 하다"),
                    g("diseases that “pay,”", "돈이 되는 질병"), g("pay", "돈이 되다, 돈을 내다"),
                    g("whether because", "~ 때문이든"), g("the disease", "그 질병"), g("more common", "더 흔한"), g("common", "흔한"),
                    g("or because", "또는 ~ 때문이든"), g("prevalent", "널리 퍼진"), g("among demographics", "인구 집단들 사이에"),
                    g("demographics", "인구 집단"), g("can pay more", "돈을 더 낼 수 있다")],
        "slashes": ["By lowering the cost", "data collection, mining,", "clinical trials,", "help offset imbalances", "pharmaceutical industry",
                    "direct attention", "“pay,”", "more common", "or because", "among demographics"],
        "roles": [r("AI", "S"), r("can help offset", "V"), r("imbalances", "O"), r("the disease … it", "S"), r("is … is", "V")],
        "modifiers": ["that direct attention to diseases that “pay,”", "that can pay more"],
        "steps": [
            choice("s4_ai",
                   "AI는 무엇에 도움이 될 수 있대요?",
                   [("o0", "돈이 되는 병에만 관심이 쏠리는 불균형을 줄이는 것", True),
                    ("o1", "돈이 되는 병에 관심을 더 모으는 것", False),
                    ("o2", "신약 개발 비용을 더 높이는 것", False)],
                   "'help offset imbalances'를 봐요. offset은 시험지 아래에 '상쇄하다'로 풀어 줬어요.",
                   why="offset은 '상쇄하다'예요. 'imbalances … that direct attention to diseases that “pay,”', 돈이 되는 병으로 관심을 돌리는 불균형을 AI가 상쇄할 수 있대요.",
                   highlight=["By lowering the cost", "offset imbalances"],
                   tips=[tip("By -ing", "'~함으로써'예요. By lowering the cost = 비용을 낮춤으로써.", "By lowering"),
                         tip("whether because A or because B", "'A 때문이든 B 때문이든'이에요.", "whether because")],
                   point="AI = 비용을 낮춰서, 돈이 되는(“pay”) 병에 관심이 쏠리는 불균형을 상쇄"),
            show("s4_board",
                 "돈이 되는(“pay”) 병은 더 흔한 병이거나, 돈을 더 낼 수 있는 사람들이 걸리는 병이에요.",
                 panel=board(L4, R3, fresh=("diseases that “pay”",)), highlight=["more common", "can pay more"], button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("We", "우리는"), g("see", "보다"), g("the democratizing power of AI", "AI의 민주화하는 힘"),
                    g("democratizing", "민주화하는"), g("power", "힘"), g("to broaden the attention", "관심을 넓힐"),
                    g("broaden", "넓히다"), g("the medical and research communities", "의료계와 연구계"), g("medical", "의료의"),
                    g("communities", "~계, 집단"), g("to find cures", "치료법을 찾도록"), g("cures", "치료법"),
                    g("traditionally neglected health issues", "전통적으로 등한시되어 온 건강 문제"), g("traditionally", "전통적으로, 예부터"),
                    g("neglected", "등한시된"), g("health issues", "건강 문제"), g("health", "건강"), g("issues", "문제"),
                    g("among traditionally neglected populations", "전통적으로 등한시되어 온 사람들 사이에서"),
                    g("populations", "사람들, 인구 집단")],
        "slashes": ["We see", "power of AI", "to broaden the attention", "research communities", "to find cures", "health issues"],
        "roles": [r("We", "S"), r("see", "V"), r("the democratizing power of AI", "O")],
        "modifiers": ["to broaden the attention of the medical and research communities"],
        "steps": [
            choice("s5_broaden",
                   "AI가 의료계와 연구계의 관심을 어디까지 넓힌대요?",
                   [("o0", "전통적으로 등한시되어 온 건강 문제와 사람들", True), ("o1", "이미 관심을 많이 받는 선진국 질병", False),
                    ("o2", "의료와 상관없는 다른 산업", False)],
                   "'to find cures to traditionally neglected health issues'와 문장 끝 populations를 봐요.",
                   why="'traditionally neglected health issues and … populations', 그동안 등한시되어 온 건강 문제와 사람들에게까지 관심을 넓힌대요.",
                   highlight=["broaden", "traditionally neglected health issues", "traditionally neglected populations"],
                   tips=[tip("democratize", "'민주화하다'예요. 여기서는 일부만 누리던 의료 연구의 관심을 더 많은 사람에게 넓힌다는 말이에요.",
                             "democratizing")],
                   point="AI의 democratizing power = 등한시되어 온(neglected) 건강 문제·사람들에게까지 관심을 넓힘"),
            show("s5_board",
                 "그동안 등한시된 사람들(neglected populations)에게까지 관심을 넓히는 게 AI의 힘이래요.",
                 panel=board(L4, R5, fresh=("neglected populations",)), highlight=["traditionally neglected populations"]),
            show("s5_summary", "이제 요약문을 읽어요. (A)와 (B)가 칠판의 어느 쪽 말인지 보고 고르면 돼요.", button="요약문 읽어 볼게요"),
        ],
    },
    {
        "id": 6, "label": "요약문", "text": SUMMARY, "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("By lowering the cost", "비용을 낮춤으로써"), g("lowering", "낮추는 것"), g("cost", "비용"),
                    g("pharmaceutical research and development", "제약 연구 개발"), g("pharmaceutical", "제약의"),
                    g("AI", "인공지능"), g("can help reduce", "줄이는 데 도움이 될 수 있다"), g("reduce", "줄이다"),
                    g("the imbalance", "불균형"), g("imbalance", "불균형"), g("in investment", "투자에서의"), g("investment", "투자"),
                    g("has led to", "~을 가져왔다, ~로 이어졌다"), g("less profitable diseases", "수익이 덜 나는 질병"),
                    g("profitable", "수익이 나는"), g("thereby", "그렇게 함으로써, 그 결과"), g("broadening", "넓히는"),
                    g("the focus", "초점"), g("focus", "초점"), g("medical research", "의학 연구"), g("medical", "의학의"),
                    g("include", "포함하다"), g("populations", "사람들, 인구 집단")],
        "slashes": ["By lowering the cost", "and development,", "AI can help reduce", "in investment", "less profitable diseases,",
                    "thereby broadening", "medical research"],
        "roles": [r("AI", "S"), r("can help reduce", "V"), r("the imbalance", "O")],
        "modifiers": ["that has led to the (A) ________ of less profitable diseases"],
        "steps": [
            choice("s6_a_side",
                   "(A)는 불균형이 less profitable diseases(수익이 덜 나는 병)에 가져온 일이에요. 칠판 어느 쪽 이야기일까요?",
                   [("o0", LEFT, False), ("o1", RIGHT, True)],
                   "수익이 덜 나는 병은 돈을 낼 수 없는 사람들의 병이에요. 그런 병이 어느 쪽이었는지 떠올려 봐요.",
                   why="돈이 덜 되는 병은 가난한(poor) 사람들의 병, 칠판 오른쪽이에요. 왼쪽은 돈이 되는(“pay”) 병이에요.",
                   highlight=["has led to", "less profitable diseases"],
                   panel=board(L4, R5),
                   tips=[tip("lead to", "'~을 가져오다, ~로 이어지다'예요. the imbalance that has led to (A) = (A)를 가져온 불균형.", "led to")]),
            choice("s6_a",
                   "그럼 (A)에는 어떤 뜻의 말이 와야 할까요?",
                   [("o0", "미리 막음(예방)", False), ("o1", "관심을 주지 않음(무시)", True), ("o2", "널리 퍼짐(확산)", False)],
                   "불균형이 가져온 일이라 좋은 일이 아니에요. 칠판 오른쪽 neglected(등한시된)를 떠올려 봐요.",
                   why="불균형 때문에 생긴 일이라 병을 막아 준 좋은 일이 아니에요. 오른쪽 neglected처럼, 수익이 덜 나는 병은 관심을 못 받아 왔어요.",
                   highlight=["(A) ________"],
                   point="(A) = 수익이 덜 나는 병이 받아 온 대접 = neglected(등한시됨) → 무시"),
            choice("s6_b",
                   "(B)는 의학 연구의 초점을 넓혀 포함하게 될 사람들(populations)이에요. 어떤 뜻의 말이 와야 할까요?",
                   [("o0", "돈을 많이 낼 수 있는", False), ("o1", "의료 혜택을 충분히 받지 못한", True), ("o2", "그 지역에 원래 사는", False)],
                   "칠판 오른쪽 'traditionally neglected populations'를 떠올려 봐요.",
                   why="초점을 넓혀 새로 포함하는 사람들은 그동안 등한시된(neglected) 사람들이에요. 오른쪽 말이에요.",
                   highlight=["broadening the focus", "(B) ________"],
                   point="(B) = traditionally neglected populations = 의료 혜택을 충분히 못 받은 사람들"),
            show("s6_go", "(A)와 (B)의 뜻을 둘 다 맞게 담은 보기를 골라 봐요. 한쪽만 맞으면 오답이에요.", button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — 2문장(모두에게). 덩어리는 문장에 그대로 있는 구절
add_match(sentences, 2, [m("The hard truth", "냉혹한 진실은"), " 제약 회사가 ", m("diseases that affect the rich", "부자들이 걸리는 질병에"), " ",
                         m("more research and development resources", "더 많은 연구 개발 자원을"), " ", m("devotes", "쏟는다"), "는 것이다."])
# 가리키는 말
add_refers(sentences, 3, {"it": "a disease(그 질병)"})
add_refers(sentences, 4, {"it": "the disease(그 질병)"})

SENSES = {
    1: [sense("to", "to find treatments", "~하기 위해", "to부정사 (목적)"),
        sense("for", "for rare diseases", "~을 위한", "전치사 for (치료법과 의약품이 어떤 병을 위한 것인지)"),
        sense("that", "rare diseases that to date", "(앞 명사를 꾸밈)", "관계대명사 that — rare diseases를 꾸민다"),
        sense("to", "to date", "지금까지", "to date = 지금까지 (숙어)")],
    2: [sense("that", "has always been that", "~라는 것", "명사절 접속사 that (보어: ~라는 점)"),
        sense("to", "to diseases", "~에", "devote A to B = A를 B에 쏟다"),
        sense("that", "diseases that affect", "(앞 명사를 꾸밈)", "관계대명사 that — diseases를 꾸민다")],
    3: [sense("that", "that is,", "즉", "that is = 즉, 다시 말해"),
        sense("if", "even if a disease", "비록 ~일지라도", "even if + 주어·동사 (양보)"),
        sense("that", "a population that cannot", "(앞 명사를 꾸밈)", "관계대명사 that — a population을 꾸민다"),
        sense("to", "afford to pay", "~할 (여유)", "afford to + 동사원형 = ~할 여유가 있다"),
        sense("for", "pay for it", "~의 값을", "pay for = ~의 값을 치르다"),
        sense("for", "for example", "예를 들어", "for example = 예를 들어"),
        sense("to", "compared to", "~에 (비해)", "compared to = ~에 비해")],
    4: [sense("that", "industry that direct", "(앞 명사를 꾸밈)", "관계대명사 that — imbalances를 꾸민다"),
        sense("to", "attention to diseases", "~로", "direct attention to = ~로 관심을 향하게 하다"),
        sense("that", "diseases that “pay,”", "(앞 명사를 꾸밈)", "관계대명사 that — diseases를 꾸민다"),
        sense("that", "demographics that can pay", "(앞 명사를 꾸밈)", "관계대명사 that — demographics를 꾸민다")],
    5: [sense("to", "to broaden", "~할 (힘)", "명사 + to부정사 (power to ~ = ~할 힘)"),
        sense("to", "to find cures", "~하도록", "to부정사 (목적: 치료법을 찾도록)"),
        sense("to", "cures to", "~에 대한 (치료법)", "cure to/for + 문제 = ~에 대한 해결책")],
    6: [sense("that", "investment that has led", "(앞 명사를 꾸밈)", "관계대명사 that — the imbalance를 꾸민다"),
        sense("to", "led to", "~로 (이어지다)", "lead to = ~을 가져오다"),
        sense("to", "to include", "~하도록", "to부정사 (broaden … to include = 넓혀서 ~을 포함하도록)")],
}

WORDS = {"pharmaceutical": "제약의", "industry": "산업", "algorithms": "알고리즘", "employed": "활용되는", "find": "찾다",
         "treatments": "치료법", "drugs": "의약품", "rare": "희귀한", "diseases": "질병", "date": "날짜 · to date = 지금까지",
         "haven’t": "~하지 않았다", "received": "받았다", "attention": "관심", "hard": "냉혹한", "truth": "진실",
         "always": "늘", "pharma": "제약 회사", "devotes": "쏟다", "research": "연구", "development": "개발", "resources": "자원",
         "affect": "(병이) 걸리게 하다", "rich": "부유한 · the rich = 부자들", "definition": "정의", "often": "자주",
         "associated": "연관된", "poor": "가난한", "disease": "질병", "quite": "꽤", "prevalent": "널리 퍼진", "population": "사람들, 인구",
         "afford": "감당하다", "pay": "(돈을) 내다", "example": "예", "people": "사람들", "living": "사는", "developing": "개발 중인",
         "world": "세계", "neglected": "등한시된", "compared": "비교된", "first": "첫째의 · First World = 선진국", "illnesses": "질병",
         "lowering": "낮추는 것", "cost": "비용", "data": "데이터", "collection": "수집", "mining": "마이닝", "analysis": "분석",
         "drug": "약", "clinical": "임상의", "trials": "시험", "ai": "인공지능", "help": "돕다", "offset": "상쇄하다",
         "imbalances": "불균형", "direct": "향하게 하다", "common": "흔한", "demographics": "인구 집단", "see": "보다",
         "democratizing": "민주화하는", "power": "힘", "broaden": "넓히다", "medical": "의료의", "communities": "~계, 집단",
         "cures": "치료법", "traditionally": "전통적으로", "health": "건강", "issues": "문제", "populations": "사람들",
         "reduce": "줄이다", "imbalance": "불균형", "investment": "투자", "led": "이어졌다 · lead to", "profitable": "수익이 나는",
         "thereby": "그 결과", "broadening": "넓히는", "focus": "초점", "include": "포함하다", "less": "덜", "more": "더",
         "much": "많은", "too": "너무", "even": "비록, ~조차", "can": "~할 수 있다", "cannot": "~할 수 없다", "help offset": "상쇄를 돕다"}

OPTIONS = [("1", "prevention ······ marginalized", "예방 ······ 소외된", False),
           ("2", "spread ······ general", "확산 ······ 일반적인", False),
           ("3", "overlook ······ native", "간과 ······ 현지의", False),
           ("4", "ignorance ······ wealthy", "무지 ······ 부유한", False),
           ("5", "disregard ······ underserved", "무시 ······ (의료) 서비스를 충분히 받지 못하는", True)]
exam = {
    "question": "다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?",
    "underline": ["(A) ________", "(B) ________"], "sentence": 6, "analysis_first": True, "wrong_rate": 61, "wrong_rank": 4,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("prevention", "예방"), g("marginalized", "소외된"), g("spread", "확산"), g("general", "일반적인"),
                g("overlook", "간과"), g("native", "현지의, 토박이의"), g("ignorance", "무지"), g("wealthy", "부유한"),
                g("disregard", "무시"), g("underserved", "(의료) 서비스를 충분히 받지 못하는")],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "(A)와 (B) 둘 다 칠판 오른쪽 이야기예요. 두 칸이 다 맞는 보기를 골라 봐요.",
        "정답이에요! 돈이 되는 병에 쏠린 불균형 때문에 수익이 덜 나는 병은 무시(disregard)되어 왔어요. AI는 그 초점을 의료 서비스를 충분히 못 받은(underserved) 사람들까지 넓혀요.",
        "정답은 ⑤예요. (A) 등한시되어 온 것 = disregard, (B) 등한시되어 온 사람들 = underserved예요.",
        {"1": "(B) marginalized(소외된)는 맞아요. 그런데 (A) prevention(예방)은 병을 막아 주는 좋은 일이라, 불균형이 가져온 일과 반대예요.",
         "2": "spread(확산)는 병이 퍼지는 거예요. general(일반적인) 사람들도 '그동안 등한시된 사람들'과 달라요.",
         "3": "(A) overlook(간과)은 맞는 쪽이에요. 그런데 (B) native(현지의)는 글에 없는 말이에요.",
         "4": "ignorance(무지)는 '알지 못함'이에요. (B) wealthy(부유한)는 칠판 왼쪽, 이미 관심을 받던 쪽이에요."},
        {"1": review(33,
                     "①은 (B) marginalized(소외된)는 맞아요. 그런데 (A) 자리는 불균형이 수익이 덜 나는 병에 '가져온(led to)' 일이에요. "
                     "prevention(예방)은 병을 막아 주는 좋은 일이라, 글의 neglected(등한시됨)와 반대예요.\n두 칸이 다 맞아야 정답이에요.",
                     panel=rows(("(A)", "has been neglected", "등한시됨 = disregard", "hl"),
                                ("(B)", "traditionally neglected populations", "서비스를 충분히 못 받은 = underserved", "hl2")),
                     rank_word="가장 많이 고른")}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(4·5)만 ──
EMPHASIS = {
    4: ["AI", "offset", "imbalances", "diseases that “pay,”"],
    5: ["broaden", "attention", "neglected", "populations"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 40번 (요약문 완성, 2점)",
    topic="요약문 푸는 법: 지문을 먼저 읽으며 두 쪽 말을 칠판에 모으기 → 요약문 (A)(B)가 각각 어느 쪽인지 → 그 뜻의 말 고르기",
    method={"type": "summary", "labels": ["지문 먼저 읽기", "두 쪽 말 모으기", "(A)(B) 맞추기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-ai-neglected-diseases.svg", ("Rare diseases", "희귀 질병"), "+", ("AI", "인공지능"),
                                       "돈이 안 되는 병에도 치료제가 나올까?", "2026년 6월 모의평가 40번 도입 칠판"),
                      "alt": "칠판: Rare diseases(희귀 질병) + AI(인공지능)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "돈이 안 되는 병에도 치료제가 나올까요? 이번 글은 제약 산업과 AI 이야기예요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "요약문 문제는 지문을 먼저 읽으며 글쓴이 주장을 잡아요. 같은 쪽 말을 칠판에 모아요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "마지막에 요약문을 읽고, (A)와 (B)가 칠판의 어느 쪽 말인지 보고 골라요."}}],
    exam=exam,
    # offset·demographic은 시험지 아래 *로 풀어 준 말 — 핵심 단어가 아니라 뺐다
    key_words={"passage": [g("pharmaceutical", "제약의"), g("employ", "활용하다"), g("treatment", "치료(법)"), g("to date", "지금까지"),
                           g("devote A to B", "A를 B에 쏟다"), g("affect", "(병이) 걸리게 하다"), g("the rich", "부자들"),
                           g("be associated with", "~와 연관되다"), g("prevalent", "널리 퍼진"), g("afford", "(비용을) 감당하다"),
                           g("neglect", "등한시하다"), g("clinical trial", "임상 시험"), g("imbalance", "불균형"),
                           g("direct attention to", "~로 관심을 향하게 하다"), g("democratize", "민주화하다"), g("broaden", "넓히다"),
                           g("cure", "치료법"), g("profitable", "수익성 있는")],
               "options": [g("prevention", "예방"), g("marginalized", "소외된"), g("overlook", "간과하다"), g("ignorance", "무지"),
                           g("disregard", "무시"), g("underserved", "서비스를 충분히 받지 못하는")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함:
# employed 활용되는 · to date 지금까지 · affect (병이) 걸리게 하다.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    1: [tip("employed", "이 글에서는 → 활용되는  ('고용된' 아님)", "employed", trap=True),
        tip("to date", "이 글에서는 → 지금까지  ('날짜' 아님)", "to date", trap=True)],
    2: [tip("affect", "이 글에서는 → (병이) 걸리게 하다  (diseases that affect the rich = 부자들이 걸리는 병)", "affect", trap=True),
        tip("the rich", "the + 형용사 = ~한 사람들이에요. the rich = 부자들.", "the rich")],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="요약문 푸는 법")
