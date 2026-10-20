"""2022년 3월 고3 40번 레슨 + 대사를 만든다 (요약문 완성, 2점). 오답률 41.0% · Top 10.

    py scripts/lessons/gen_moeui_2022_03_40.py   (→ node scripts/policy_copy.mjs stamp <id> → npm run build)

틀: 요약문 — 선생님이 고른 「지문 먼저 → 요약문」(2024년 3월 40번과 같게, method.type = summary).
지문을 처음부터 읽으며 칠판 두 칸에 말을 모은다 — 왼쪽 「언어·종교」(increase rapidly → divide),
오른쪽 「이웃과의 교류」(5문장부터: stopped doing it → kept apart → don’t interact). 요약문에서 (A)는 「언어와 종교의 ~」라 왼쪽,
(B)는 「사람들의 교류를 ~함으로써」라 오른쪽 → 그 뜻의 말 3지 → 보기.
정답 ① diversification ······ discouraging.
선택률: ① 59 · ② extinction·delaying 12 · ③ extinction·expanding 12 · ⑤ diversification·expanding 11 · ④ 6.
②③은 (A)를 '병으로 언어가 사라짐'으로 짐작(글에 없음), ⑤는 (B)만 틀림(교류를 멈췄다 ↔ 넓힘) — 셋 다 option_review로.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
ethnocentrism·pathogen은 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (may well = 아마 ~했을지도 모른다, blame A for B = B를 A 탓으로 돌리다, divide = 갈라지다).
Claude 초안(2026-10-20) — 선생님 검토 전.
반영한 규칙: 끊어읽기 S·V·O·C + [ ] 수식어(2026-10-20), 긴 문장 S·V 모두, that 명사절 S·V, 칠판엔 읽은 데까지만, 초급 기본(add_basic).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, add_that_sv, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)

ID = "moeui-2022-03-40-pathogen-languages"

SUMMARY = ("High pathogen density can contribute to the (A) ________ of languages and religions by (B) ________ people’s interactions "
           "with their neighboring groups, as was shown in the regions around the equator.")
S = [
    "Why would languages and religions increase rapidly around the equator, and why is their frequency also related to ethnocentrism?",
    "The answer to these questions lies in the fact that pathogen density is much higher in the tropics than it is in temperate and cold climates.",
    "When you live in Sweden, chances are good that any group within five hundred miles has been exposed to the same few pathogens.",
    "In contrast, when you live in the Congo, the group on the other side of the valley may well have been exposed to a pathogen with which "
    "you’ve had no prior contact.",
    "For this reason, humans in the tropics learned that when they interacted with other groups they tended to get sick, so they would have "
    "stopped doing it.",
    "In a pre-scientific world, it was logical to blame their neighbors for their illness, and therefore to dislike them.",
    "Dislike and fear kept neighbors apart, and once you don’t interact with others anymore, your languages and religions naturally divide as well.",
    SUMMARY,
]
KO = [
    "왜 언어와 종교는 적도 주변에서 급증하며, 왜 그것의 빈도가 자민족 중심주의와 또한 관련이 있을까?",
    "이 질문들에 대한 답은 병원균의 밀도가 온대 기후나 한랭 기후보다 열대 지방에서 훨씬 더 높다는 사실에 있다.",
    "여러분이 스웨덴에 살면, 500마일 이내의 어떤 집단도 동일한 극히 소수의 병원균에 노출되어 왔을 가능성이 크다.",
    "반면에, 여러분이 콩고에 산다면, 계곡 반대편에 있는 집단은 아마 여러분이 이전에 접촉한 적이 없는 병원균에 노출되었을지도 모른다.",
    "이러한 이유로, 열대 지방의 사람들은 그들이 다른 집단과 교류할 때 병에 잘 걸린다는 것을 알게 되었고, 그래서 그들은 그것(교류)을 하는 것을 중단했을 것이다.",
    "과학 이전의 세계에서는 자신의 병을 이웃 탓으로 돌리고, 그 결과 그들(이웃)을 싫어하는 것이 논리적이었다.",
    "혐오와 두려움이 이웃을 계속 갈라놓았고, 일단 타인과 더는 교류하지 않게 되면, 언어와 종교도 역시 자연스럽게 갈라지게 된다.",
    "적도 주변 지역에서 드러났던 것처럼, 높은 병원균 밀도는 사람들이 이웃 집단과 교류하지 못하게 하여, 언어와 종교의 다양화를 초래할 수 있다.",
]

LANG = "왼쪽 · 언어·종교에 일어나는 일"
TALK = "오른쪽 · 이웃과의 교류에 일어나는 일"
TITLE = "적도 주변에서는?"


def board(left, right=None, fresh=(), sort=None):
    # 칠판엔 읽은 데까지만 — 「교류」 칸은 교류(interacted)가 나오는 5문장부터. 요약문의 (A)(B) 자리는 쓰지 않는다
    if right is None:
        return groups(TITLE, "언어·종교", left, fresh=fresh)
    return groups(TITLE, "언어·종교", left, "이웃과의 교류", right, fresh=fresh, between="←",
                  sort={"words": sort, "left": LANG, "right": TALK} if sort else None)


L1 = [("increase rapidly", "빠르게 늘어남")]
R5 = [("stopped doing it", "교류를 멈춤")]
L7 = L1 + [("naturally divide", "자연스럽게 갈라짐")]
R7 = R5 + [("kept neighbors apart", "이웃과 떨어져 지냄"), ("don’t interact anymore", "더는 교류 안 함")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Why would", "왜 ~할까"), g("languages and religions", "언어와 종교"), g("increase rapidly", "빠르게 늘어나다"),
                    g("around the equator", "적도 주변에서"), g("why is", "왜 ~일까"), g("their frequency", "그것들의 빈도(얼마나 많은지)"),
                    g("also related to", "~와도 관련된"), g("ethnocentrism", "자민족 중심주의")],
        "slashes": ["languages and religions", "increase rapidly", "around the equator,", "their frequency"],
        "roles": [r("languages and religions", "S"), r("increase", "V"), r("their frequency", "S"), r("is", "V"), r("related", "C")],
        "steps": [
            show("s1_q", "질문으로 시작해요. 적도 주변에서 언어와 종교가 왜 빠르게 늘어나는지, 그 답이 이 글의 중심이에요.",
                 highlight=["increase rapidly", "around the equator"],
                 panel=board(L1, fresh=("increase rapidly",)), button="다음 문장",
                 tips=[tip("요약문 문제 요령", "지문을 먼저 읽으며 글쓴이 주장을 잡고 말을 칠판에 모아요. 마지막에 요약문 (A)(B)가 각각 어느 쪽 말인지 보고 골라요."),
                       tip("질문으로 시작하는 글", "첫 문장이 질문이면 그 답이 글의 주제예요. 답이 나오는 문장을 꼭 잡아요.")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("The answer", "답"), g("these questions", "이 질문들"), g("lies", "놓여 있다 · lie in = ~에 있다"),
                    g("in the fact", "~라는 사실에"), g("pathogen density", "병원균 밀도"), g("is", "~이다"), g("much higher", "훨씬 더 높은"),
                    g("in the tropics", "열대 지방에서"), g("than it is", "~에서(의 병원균 밀도)보다"),
                    g("in temperate and cold climates", "온대 기후와 추운 기후에서"), g("density", "밀도")],
        "slashes": ["The answer to these questions", "lies in the fact", "pathogen density is", "much higher", "in the tropics",
                    "than it is"],
        "roles": [r("The answer", "S"), r("lies", "V"), r("pathogen density", "S"), r("is", "V"), r("much higher", "C")],
        "modifiers": ["to these questions"],
        "steps": [
            sv("s2_sv", ["The answer", "these questions", "lies", "pathogen density", "is"],
               {"The answer": "S", "lies": "V"},
               {"these questions": "그건 to 뒤 덩어리예요. The answer를 꾸며요.",
                "pathogen density": "그건 that 뒤 덩어리 안의 주어예요. 먼저 바깥 문장을 봐요.",
                "is": "그건 that 뒤 덩어리 안의 동사예요."},
               "주어는 The answer (to these questions), 동사는 lies예요. 답은 that 뒤 내용에 있대요.",
               ask="긴 문장이에요. 바깥 문장의 주어(S)와 동사(V)를 찾아볼까요?",
               tips=[tip("lie in", "'~에 있다'예요. The answer lies in ~ = 답은 ~에 있다.", "lies in")]),
            choice("s2_mean",
                   "그럼 그 답은 무엇이래요?",
                   [("o0", "열대 지방에 병원균이 훨씬 많다", True), ("o1", "열대 지방은 날씨가 따뜻하다", False),
                    ("o2", "추운 지방에 병원균이 더 많다", False)],
                   "'pathogen density is much higher in the tropics'를 봐요. pathogen은 시험지 아래 풀이처럼 '병원균'이에요.",
                   why="'pathogen density is much higher in the tropics', 병원균 밀도가 열대에서 온대·추운 기후보다 훨씬 높대요.",
                   highlight=["pathogen density", "much higher in the tropics"],
                   tips=[tip("than it is", "it is는 pathogen density is예요. 열대와 온대·추운 기후를 견줘요.", "than it is")],
                   point="질문의 답 = 열대 지방은 병원균 밀도가 훨씬 높다"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("When you live in Sweden", "스웨덴에 살면"), g("chances are good", "가능성이 크다"),
                    g("any group within five hundred miles", "500마일 안의 어떤 집단이든"), g("has been exposed to", "~에 노출되어 왔다"),
                    g("the same few pathogens", "같은 몇 안 되는 병원균")],
        "slashes": ["in Sweden,", "chances are good", "any group", "within five hundred miles", "has been exposed"],
        "roles": [r("chances", "S"), r("are", "V"), r("good", "C"), r("any group", "S"), r("has been exposed", "V")],
        "modifiers": ["within five hundred miles"],
        "steps": [
            choice("s3_sweden",
                   "스웨덴에 살면 500마일 안의 집단들은 어떤 병원균을 접해 왔대요?",
                   [("o0", "모두 같은 몇 가지 병원균", True), ("o1", "저마다 처음 보는 병원균", False), ("o2", "병원균은 하나도 없음", False)],
                   "'the same few pathogens'를 봐요. the same few = 같은 몇 안 되는.",
                   why="'has been exposed to the same few pathogens', 다들 같은 몇 가지 병원균만 접해 왔대요. 새 병원균을 만날 일이 적어요.",
                   highlight=["the same few pathogens"],
                   tips=[tip("chances are good that ~", "'~일 가능성이 크다'예요.", "chances are good")]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("In contrast", "반면에"), g("when you live in the Congo", "콩고에 살면"), g("the Congo", "콩고"),
                    g("the group on the other side of the valley", "계곡 건너편의 집단"), g("the group", "그 집단"), g("the valley", "계곡"),
                    g("may well have been exposed to", "아마 ~에 노출되었을지도 모른다"), g("may well have been exposed", "아마 노출되었을지도 모른다"),
                    g("a pathogen", "병원균"), g("with which you’ve had no prior contact", "네가 전에 접촉한 적 없는"), g("prior", "이전의")],
        "slashes": ["In contrast,", "in the Congo,", "the group", "on the other side of the valley", "may well have been exposed",
                    "to a pathogen", "with which"],
        "roles": [r("the group", "S"), r("may well have been exposed", "V")],
        "modifiers": ["on the other side of the valley", "with which you’ve had no prior contact"],
        "steps": [
            sv("s4_sv", ["the Congo", "the group", "the valley", "may well have been exposed"],
               {"the group": "S", "may well have been exposed": "V"},
               {"the Congo": "그건 when 덩어리 안, in 뒤의 말이에요.",
                "the valley": "그건 of 뒤 덩어리예요. 어느 쪽 집단인지 꾸며요."},
               "주어는 the group (on the other side of the valley), 동사는 may well have been exposed예요.",
               ask="긴 문장이에요. 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s4_congo",
                   "콩고에서 계곡 건너편 집단은 어떤 병원균에 노출되었을 수 있대요?",
                   [("o0", "내가 한 번도 접해 본 적 없는 병원균", True), ("o1", "나와 똑같은 병원균", False), ("o2", "이미 사라진 병원균", False)],
                   "'with which you’ve had no prior contact'를 봐요. prior는 '이전의'예요.",
                   why="'a pathogen with which you’ve had no prior contact', 내가 전에 접촉한 적 없는 병원균이래요. 스웨덴과 반대예요.",
                   highlight=["In contrast", "no prior contact"],
                   tips=[tip("may well have p.p.", "'아마 ~했을지도 모른다'예요. 과거 일을 꽤 그럴듯하게 짐작하는 말이에요.", "may well"),
                         tip("In contrast", "'반면에'예요. 앞 문장(스웨덴)과 반대 경우가 나와요.", "In contrast")]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("For this reason", "이런 이유로"), g("humans", "사람들"), g("the tropics", "열대 지방"), g("learned", "알게 되었다"),
                    g("interacted", "교류했다"), g("other groups", "다른 집단들"), g("tended to get sick", "병에 걸리는 경향이 있었다"),
                    g("would have stopped", "멈췄을 것이다"), g("doing it", "그것을 하는 것")],
        "slashes": ["For this reason,", "humans in the tropics", "learned", "when they interacted", "with other groups", "tended to get sick,"],
        "roles": [r("humans", "S"), r("learned", "V"), r("they … they … they", "S"), r("interacted", "V"), r("tended", "V"),
                  r("would have stopped", "V"), r("doing it", "O")],
        "modifiers": ["in the tropics"],
        "steps": [
            sv("s5_sv", ["humans", "the tropics", "learned", "interacted", "would have stopped"],
               {"humans": "S", "learned": "V", "would have stopped": "V"},
               {"the tropics": "그건 in 뒤 덩어리예요. 어디 사는 사람인지 꾸며요.",
                "interacted": "그건 when 덩어리 안의 동사예요. 배운 내용 속 말이에요."},
               "주어 humans, 동사 learned예요. so 뒤는 they가 주어, would have stopped가 동사예요.",
               ask="긴 문장이에요. 동사(V)가 두 개예요. 주어(S)와 동사(V)를 모두 찾아볼까요?",
               tips=[tip("would have p.p.", "'~했을 것이다'예요. 과거 일을 짐작하는 말이에요.", "would have stopped")]),
            choice("s5_it",
                   "doing it의 it은 무엇일까요?",
                   [("o0", "다른 집단과 교류하기", True), ("o1", "병에 걸리기", False), ("o2", "열대 지방에 살기", False)],
                   "가리키는 것은 앞에서 찾아요. when 뒤를 봐요.",
                   why="'when they interacted with other groups they tended to get sick', 교류하면 병에 걸리니 그 교류(interacted)를 멈췄을 거래요.",
                   highlight=["doing it"]),
            show("s5_board", "병에 걸리니 다른 집단과 만나는 걸 멈췄을 거래요. 칠판 오른쪽에 넣어 둘게요.",
                 highlight=["would have stopped"], panel=board(L1, R5, fresh=("stopped doing it",)), button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("In a pre-scientific world", "과학 이전의 세상에서는"), g("it was logical", "논리적이었다, 당연했다"),
                    g("to blame", "탓하는 것"), g("their neighbors", "그들의 이웃"), g("their illness", "그들의 병"),
                    g("and therefore", "그래서"), g("to dislike them", "그들을 싫어하는 것")],
        "slashes": ["pre-scientific world,", "it was logical", "to blame their neighbors", "for their illness,", "and therefore"],
        "roles": [r("it", "S"), r("was", "V"), r("logical", "C")],
        "steps": [
            show("s6_blame", "과학을 모르던 시절엔 병을 이웃 탓으로 돌리고, 그래서 이웃을 싫어하는 게 당연했대요.",
                 highlight=["blame", "dislike"],
                 tips=[tip("blame A for B", "'B를 A 탓으로 돌리다'예요. blame their neighbors for their illness = 병을 이웃 탓으로 돌리다.", "blame"),
                       tip("가주어 it", "it was … to ~는 '~하는 것은 …였다'로 읽어요. it은 뒤의 to ~를 대신 받아요.", "it was logical")],
                 button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("Dislike and fear", "혐오와 두려움"), g("kept", "계속 ~하게 했다 · keep A apart = A를 떼어 놓다"), g("neighbors", "이웃들"),
                    g("apart", "떨어져"), g("once", "일단 ~하면"), g("others", "다른 사람들"), g("anymore", "더는"),
                    g("your languages and religions", "너의 언어와 종교는"), g("naturally", "자연스럽게"), g("divide", "나뉘다, 갈라지다"),
                    g("as well", "~도 역시")],
        "slashes": ["Dislike and fear", "kept neighbors apart,", "and once", "you don’t interact", "with others anymore,",
                    "your languages and religions", "naturally divide"],
        "roles": [r("Dislike and fear", "S"), r("kept", "V"), r("neighbors", "O"), r("apart", "C"), r("you", "S"), r("don’t interact", "V"),
                  r("your languages and religions", "S"), r("divide", "V")],
        "steps": [
            sv("s7_sv", ["Dislike and fear", "kept", "neighbors", "apart", "others", "your languages and religions", "divide"],
               {"Dislike and fear": "S", "kept": "V", "neighbors": "O", "apart": "C", "your languages and religions": "S", "divide": "V"},
               {"others": "그건 with 뒤의 말이에요. once 덩어리 안이에요."},
               "앞은 주어 Dislike and fear, 동사 kept, 목적어 neighbors, 보어 apart예요. 뒤는 주어 your languages and religions, 동사 divide예요.",
               ask="긴 문장이에요. 주어(S)·동사(V)·목적어(O)·보어(C)를 모두 찾아볼까요? 두 쌍이 있어요."),
            choice("s7_divide",
                   "이웃과 더는 교류하지 않게 되면 언어와 종교는 어떻게 된대요?",
                   [("o0", "자연스럽게 여러 갈래로 나뉜다", True), ("o1", "하나로 합쳐진다", False), ("o2", "사라져 버린다", False)],
                   "'naturally divide as well'을 봐요. divide는 '나뉘다, 갈라지다'예요.",
                   why="'your languages and religions naturally divide', 언어와 종교도 자연스럽게 갈라진대요. 그래서 적도 주변에 언어와 종교가 많은 거예요.",
                   highlight=["naturally divide"],
                   tips=[tip("keep A apart", "'A를 떼어 놓다, 계속 떨어져 있게 하다'예요.", "kept")],
                   point="교류가 끊김(don’t interact) → 언어·종교가 갈라짐(divide)"),
            show("s7_board", "교류가 끊기니 언어와 종교가 갈라졌어요. 칠판 양쪽에 넣어 둘게요.",
                 panel=board(L7, R7, fresh=("naturally divide", "kept neighbors apart", "don’t interact anymore")), button="다음 문장"),
        ],
    },
    {
        "id": 8, "label": "요약문", "text": SUMMARY, "teaching_value": "high",
        "model_translation": KO[7],
        "glosses": [g("High pathogen density", "높은 병원균 밀도"), g("can contribute to", "~에 기여할 수 있다, ~을 낳을 수 있다"),
                    g("of languages and religions", "언어와 종교의"), g("people’s interactions", "사람들의 교류"),
                    g("with their neighboring groups", "이웃 집단과의"), g("as was shown", "보여진 것처럼"),
                    g("in the regions around the equator", "적도 주변 지역에서")],
        "slashes": ["High pathogen density", "can contribute to", "of languages and religions", "people’s interactions",
                    "with their neighboring groups,"],
        "roles": [r("High pathogen density", "S"), r("can contribute", "V")],
        "steps": [
            choice("s8_a_side",
                   "(A)는 '언어와 종교의 (A)'예요. 칠판 어느 쪽 말일까요?",
                   [("o0", LANG, True), ("o1", TALK, False)],
                   "(A) 바로 뒤 'of languages and religions'를 봐요.",
                   why="'the (A) of languages and religions', 언어와 종교에 일어나는 일이에요. (B)는 '사람들의 교류를 (B)함으로써'라 오른쪽이에요.",
                   highlight=["of languages and religions", "people’s interactions"],
                   panel=board(L7, R7),
                   tips=[tip("by -ing", "'~함으로써'예요. by (B) people’s interactions = 사람들의 교류를 (B)함으로써.")]),
            choice("s8_a",
                   "그럼 (A)에는 어떤 뜻의 말이 와야 할까요?",
                   [("o0", "여러 갈래로 나뉘어 다양해짐", True), ("o1", "사라져 없어짐", False), ("o2", "하나로 합쳐짐", False)],
                   "칠판 왼쪽 'increase rapidly, naturally divide'를 떠올려 봐요.",
                   why="왼쪽은 언어와 종교가 빠르게 늘고, 자연스럽게 갈라진다는 말이에요. 병 때문에 언어가 사라진다는 말은 글에 없어요.",
                   highlight=["(A) ________"],
                   point="(A) = 언어·종교가 갈라져 많아짐 → '다양화'"),
            choice("s8_b",
                   "(B)는 이웃과의 교류를 어떻게 하는 거예요?",
                   [("o0", "막고 줄임", True), ("o1", "넓히고 늘림", False), ("o2", "잠시 늦춤", False)],
                   "칠판 오른쪽 'stopped doing it, kept neighbors apart'를 떠올려 봐요.",
                   why="오른쪽은 교류를 멈추고, 이웃과 떨어져 지냈다는 말이에요. 잠깐 늦춘 게 아니라 아예 멈췄어요.",
                   highlight=["(B) ________"],
                   point="(B) = 교류를 멈춤·떨어져 지냄 → 교류를 '막음'"),
            show("s8_go", "(A)와 (B)의 뜻을 둘 다 맞게 담은 보기를 골라 봐요. 한쪽만 맞으면 오답이에요.", button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 3, [m("When you live in Sweden", "스웨덴에 살면"), ", ", m("any group within five hundred miles", "500마일 안의 어떤 집단이든"), " ",
                         m("the same few pathogens", "같은 몇 안 되는 병원균"), "에 ", m("has been exposed to", "노출되어 왔을"), " ",
                         m("chances are good", "가능성이 크다"), "."],
          meaning_after="s3_sweden")
add_basic(sentences, 6, [m("In a pre-scientific world", "과학 이전의 세상에서는"), " ", m("their illness", "자기 병"), "을 ",
                         m("their neighbors", "이웃"), " 탓으로 ", m("to blame", "돌리는 것"), ", ", m("and therefore", "그래서"), " ",
                         m("to dislike them", "그들을 싫어하는 것"), "이 ", m("it was logical", "논리적이었다"), "."],
          meaning_ids=["s6_blame"])

add_that_sv(sentences, 2, "s2_sv", "s2_that_sv", ["pathogen density", "is", "much higher", "the tropics"],
            {"pathogen density": "S", "is": "V", "much higher": "C"},
            {"the tropics": "그건 in 뒤의 말이에요. 어디서 높은지예요."},
            "that 안의 주어는 pathogen density, 동사는 is, 보어는 much higher예요.",
            ask="답은 that 뒤에 있어요. that 안의 주어(S)·동사(V)·보어(C)를 찾아볼까요?")

SENSES = {
    1: [sense("to", "related to ethnocentrism", "~와 (관련된)", "be related to + 명사")],
    2: [sense("to", "The answer to these questions", "~에 대한", "answer to + 명사"),
        sense("that", "the fact that pathogen density", "~라는 (사실)", "동격 that (the fact that …)")],
    3: [sense("that", "chances are good that any group", "~라는 (가능성)", "명사절 that (chances are good that …)"),
        sense("to", "exposed to the same", "~에 (노출된)", "be exposed to + 명사")],
    4: [sense("to", "exposed to a pathogen", "~에 (노출된)", "be exposed to + 명사"),
        sense("which", "with which you’ve had", "그 (병원균)과", "전치사 + which (관계대명사)")],
    5: [sense("for", "For this reason", "~ 때문에, ~로", "for this reason = 이런 이유로"),
        sense("that", "learned that when", "~라는 것을", "명사절 that (learn that …)"),
        sense("to", "tended to get sick", "~하는 (경향이 있다)", "tend to + 동사원형"),
        sense("so", "so they would have stopped", "그래서", "접속사 so (결과)")],
    6: [sense("to", "to blame their neighbors", "~하는 것", "to부정사 (진주어: it was … to ~)"),
        sense("for", "for their illness", "~에 대해, ~ 때문에", "blame A for B"),
        sense("to", "to dislike them", "~하는 것", "to부정사 (진주어: it was … to ~)")],
    7: [sense("as", "as well", "~도 역시", "as well = ~도 역시")],
    8: [sense("to", "contribute to the (A)", "~에 (기여하다)", "contribute to + 명사"),
        sense("as", "as was shown", "~처럼", "접속사 as (~처럼)")],
}

WORDS = {"why": "왜", "would": "~할까", "languages": "언어들", "religions": "종교들", "increase": "늘어나다", "rapidly": "빠르게",
         "around": "~ 주변에", "equator": "적도", "frequency": "빈도", "related": "관련된", "ethnocentrism": "자민족 중심주의",
         "answer": "답", "questions": "질문들", "lies": "놓여 있다", "fact": "사실", "pathogen": "병원균", "density": "밀도",
         "higher": "더 높은", "tropics": "열대 지방", "temperate": "온대의", "cold": "추운", "climates": "기후", "live": "살다",
         "sweden": "스웨덴", "chances": "가능성", "group": "집단", "five": "5", "hundred": "100", "miles": "마일", "exposed": "노출된",
         "few": "몇 안 되는", "pathogens": "병원균들", "contrast": "대조", "congo": "콩고", "side": "쪽, 편", "valley": "계곡",
         "well": "아마, 충분히", "prior": "이전의", "contact": "접촉", "you’ve": "너는 ~해 왔다", "reason": "이유", "humans": "사람들",
         "learned": "알게 되었다", "interacted": "교류했다", "groups": "집단들", "tended": "~하는 경향이 있었다", "sick": "아픈",
         "stopped": "멈췄다", "doing": "하는 것", "pre-scientific": "과학 이전의", "logical": "논리적인", "blame": "탓하다",
         "neighbors": "이웃들", "illness": "병", "therefore": "그래서", "dislike": "싫어하다, 혐오", "fear": "두려움", "kept": "계속 ~하게 했다",
         "apart": "떨어져", "interact": "교류하다", "anymore": "더는", "naturally": "자연스럽게", "divide": "나뉘다", "high": "높은",
         "contribute": "기여하다", "people’s": "사람들의", "interactions": "교류", "neighboring": "이웃한", "shown": "보여진",
         "regions": "지역들", "once": "일단 ~하면", "don’t": "~하지 않다", "other": "다른", "much": "훨씬"}

STORIES = [
    (4, [sc("문장 1~2", "🌍", "pathogen density ↑ in the tropics", "적도 주변에 언어·종교가 많은 이유 — 열대엔 병원균이 훨씬 많아요"),
         sc("문장 3~4", "🦠", "Sweden: the same few · Congo: no prior contact", "스웨덴은 늘 같은 병원균, 콩고는 처음 보는 병원균을 만날 수 있어요")]),
    (7, [sc("문장 5~6", "🤒", "interacted → get sick → stopped", "다른 집단과 만나면 병에 걸려서 교류를 멈추고, 이웃을 탓하고 싫어했어요"),
         sc("문장 7", "↔️", "kept apart → divide", "떨어져 지내니 언어와 종교도 갈라졌어요")]),
]

OPTIONS = [("1", "diversification ······ discouraging", "다양화 ······ 막음", True),
           ("2", "extinction ······ delaying", "소멸 ······ 늦춤", False),
           ("3", "extinction ······ expanding", "소멸 ······ 넓힘", False),
           ("4", "unification ······ discouraging", "통합 ······ 막음", False),
           ("5", "diversification ······ expanding", "다양화 ······ 넓힘", False)]
exam = {
    "question": "다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?",
    "underline": ["(A) ________", "(B) ________"], "sentence": 8, "analysis_first": True, "wrong_rate": 41.0, "wrong_rank": 10,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("diversification", "다양화"), g("discouraging", "막는 것, 단념시키는 것"), g("extinction", "소멸, 멸종"), g("delaying", "늦추는 것"),
                g("expanding", "넓히는 것, 늘리는 것"), g("unification", "통합, 하나로 합침")],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "(A)는 칠판 왼쪽(언어·종교), (B)는 오른쪽(교류)이에요. 둘 다 맞는 보기를 골라 봐요.",
        "정답이에요! 높은 병원균 밀도는 이웃과의 교류를 막아서(discouraging), 언어와 종교를 여러 갈래로 나눴어요(diversification).",
        "정답은 ①이에요. (A) 언어·종교가 갈라짐 = diversification, (B) 교류를 멈춤 = discouraging이에요.",
        {"2": "언어와 종교는 사라진(extinction) 게 아니라 갈라졌어요. 교류도 잠깐 늦춘(delaying) 게 아니라 멈췄어요.",
         "3": "언어와 종교는 사라진(extinction) 게 아니라 갈라졌어요. 교류도 넓힌(expanding) 게 아니라 멈췄어요.",
         "4": "(B) discouraging은 맞지만, 언어와 종교는 합쳐진(unification) 게 아니라 갈라졌어요.",
         "5": "(A) diversification은 맞지만, (B) expanding(넓힘)은 교류를 멈췄다는 말과 반대예요."},
        {"3": review(12,
                     "③은 두 칸 다 반대예요. 글은 교류를 멈추니 언어와 종교가 갈라졌다고 했어요. (A)는 다양화(diversification), (B)는 막음(discouraging)이에요.",
                     "그래서 ③이 아니에요. 어디서 헷갈렸어요?",
                     [("병 때문에 사람이 죽어 언어가 사라진다고 생각했어요", ["outside_guess"],
                       "알려 줘서 고마워요. 글에 없는 내용을 짐작하면 안 돼요. 글은 언어와 종교가 사라진 게 아니라 갈라졌다(divide)고 했어요. 앞으로 글에 나온 말로 확인하게 할게요."),
                      ("교류가 늘어서 병이 퍼진다고 생각했어요", ["cause_effect"],
                       "알려 줘서 고마워요. 교류하면 병에 걸린다는 건 맞아요. 그래서 교류를 멈췄다(stopped)는 게 글의 흐름이에요. 앞으로 원인과 결과를 끝까지 따라가게 할게요."),
                      ("둘 다요", ["outside_guess", "cause_effect"],
                       "알려 줘서 고마워요. 앞으로 글에 나온 말로 확인하고, 원인과 결과를 끝까지 따라가게 할게요.")],
                     panel=rows(("(A)", "naturally divide · increase rapidly", "갈라져 많아짐 = diversification", "hl"),
                                ("(B)", "stopped doing it · kept neighbors apart", "교류를 막음 = discouraging", "hl2")),
                     rank_word="가장 많이 고른"),
         "2": review(12,
                     "②는 (A) extinction(소멸)부터 맞지 않아요. 언어와 종교는 사라진 게 아니라 갈라졌어요(divide). (B) delaying(늦춤)도 교류를 아예 멈췄다는 말과 달라요.",
                     "그래서 ②가 아니에요. 어디서 헷갈렸어요?",
                     [("병 때문에 언어가 사라진다고 생각했어요", ["outside_guess"],
                       "알려 줘서 고마워요. 글에 없는 내용을 짐작하면 안 돼요. 마지막 문장의 divide(갈라지다)가 (A)의 근거예요. 앞으로 글에 나온 말로 확인하게 할게요."),
                      ("delaying이 '막음'과 비슷해 보였어요", ["word_nuance"],
                       "알려 줘서 고마워요. delay는 '늦추다'라 잠깐 미룬다는 말이에요. 글은 교류를 멈추고 떨어져 지냈다고 했어요. 앞으로 비슷해 보이는 말을 같이 견줘 볼게요.")],
                     panel=rows(("(A)", "naturally divide", "사라짐(extinction) X → 갈라짐", "hl"),
                                ("(B)", "stopped · kept apart", "늦춤(delaying) X → 멈춤", "hl2")),
                     rank_word="가장 많이 고른"),
         "5": review(11,
                     "⑤는 (A) diversification은 맞아요. 그런데 (B) expanding(넓힘)은 교류를 멈췄다(stopped)는 말과 반대예요. 두 칸이 다 맞아야 해요.",
                     "그래서 ⑤가 아니에요. 어디서 헷갈렸어요?",
                     [("(A)만 보고 골랐어요", ["two_blanks"],
                       "알려 줘서 고마워요. 요약문은 (A)와 (B)가 둘 다 맞아야 해요. 앞으로 두 칸을 하나씩 확인하게 할게요."),
                      ("교류가 늘어서 언어가 다양해진다고 생각했어요", ["cause_effect"],
                       "알려 줘서 고마워요. 글은 반대로 교류가 끊겨서 언어가 갈라졌다고 했어요. 앞으로 원인과 결과를 끝까지 따라가게 할게요.")],
                     panel=rows(("(B)", "stopped doing it · kept neighbors apart", "넓힘(expanding) X → 막음(discouraging)", "hl2"))),
         }),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 40번 (요약문 완성, 2점)",
    topic="요약문 푸는 법: 지문을 먼저 읽으며 말을 칠판 두 칸에 모으기 → 요약문 (A)(B)가 각각 어느 쪽인지 → 그 뜻의 말 고르기",
    method={"type": "summary", "labels": ["지문 먼저 읽기", "두 쪽 말 모으기", "(A)(B) 맞추기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-2022-03-40-pathogens.svg", ("Equator", "적도 주변"), "→", ("Languages", "언어·종교"),
                                       "적도 주변엔 왜 언어가 많을까?", "2022년 3월 40번 도입 칠판"),
                      "alt": "칠판: Equator(적도 주변) → Languages(언어·종교)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "적도 주변엔 왜 언어와 종교가 그렇게 많을까요? 이번 글은 그 이유를 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "요약문 문제는 지문을 먼저 읽으며 글쓴이 주장을 잡아요. 중요한 말을 칠판에 모아 둘 거예요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "마지막에 요약문을 읽고, (A)와 (B)가 칠판의 어느 쪽 말인지 보고 골라요."}}],
    exam=exam,
    key_words={"passage": [g("religion", "종교"), g("equator", "적도"), g("frequency", "빈도"), g("lie in", "~에 있다"), g("density", "밀도"),
                           g("tropics", "열대 지방"), g("temperate", "온대의"), g("be exposed to", "~에 노출되다"), g("in contrast", "반면에"),
                           g("prior", "이전의"), g("interact", "교류하다"), g("tend to", "~하는 경향이 있다"), g("logical", "논리적인"),
                           g("blame A for B", "B를 A 탓으로 돌리다"), g("keep A apart", "A를 떼어 놓다"), g("divide", "갈라지다")],
               "options": [g("diversification", "다양화"), g("discourage", "막다, 단념시키다"), g("extinction", "소멸"), g("delay", "늦추다"),
                           g("expand", "넓히다"), g("unification", "통합")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="요약문 푸는 법",
       chunks={"The answer": "답", "these questions": "이 질문들", "lies": "놓여 있다", "pathogen density": "병원균 밀도", "is": "~이다",
               "much higher": "훨씬 더 높은", "the tropics": "열대 지방", "the Congo": "콩고", "the group": "그 집단", "the valley": "계곡",
               "may well have been exposed": "아마 노출되었을지도 모른다", "humans": "사람들", "learned": "알게 되었다", "interacted": "교류했다",
               "would have stopped": "멈췄을 것이다", "Dislike and fear": "혐오와 두려움", "kept": "계속 ~하게 했다", "neighbors": "이웃들",
               "apart": "떨어져", "others": "다른 사람들", "your languages and religions": "너의 언어와 종교", "divide": "갈라지다",
               "When you live in Sweden": "스웨덴에 살면", "any group within five hundred miles": "500마일 안의 어떤 집단이든",
               "the same few pathogens": "같은 몇 안 되는 병원균", "has been exposed to": "~에 노출되어 왔다", "chances are good": "가능성이 크다",
               "In a pre-scientific world": "과학 이전의 세상에서는", "their illness": "그들의 병", "their neighbors": "그들의 이웃",
               "to blame": "탓하는 것", "and therefore": "그래서", "to dislike them": "그들을 싫어하는 것", "it was logical": "논리적이었다"})
