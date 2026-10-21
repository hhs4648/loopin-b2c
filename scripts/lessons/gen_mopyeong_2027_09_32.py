"""2026년 9월 모의평가(2027학년도) 32번 레슨 + 대사를 만든다 (빈칸 추론, 2점). 오답률 61%(메가스터디) · Top 2.

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_32.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸이 마지막 문장. 정답 ⑤ better at anticipating stimuli(자극을 더 잘 예상하는).
선택률(메가스터디 풀서비스 채점): ① 8 ② 37 ③ 5 ④ 11 ⑤ 39 — 많이 고른 오답 ② less sensitive to others’ reactions가 정답과 거의 같다.
② 짐작: 글에 나온 말(less noticeable · another individual · someone else · emotional reaction)이 보기에 섞여 있어 그럴듯하다.
   하지만 글은 남의 「반응」이 아니라 남이 만든 「자극」 이야기이고, 빈칸은 hence(그래서) 뒤 「놀라게 하기 더 어렵다」의 이유다.
열쇠: 두 쪽 — 덜 느끼는 쪽(you move your body · your own legs · tickle yourself) ↔ 크게 느끼는 쪽(unexpected and surprising ·
   another individual · someone sitting next to you · eyes closed · someone else). 어른 = 놀라게 하기 어렵다 → 덜 느끼는 쪽
   (스스로 간지럽힐 때처럼 무엇이 올지 안다).
시험지 아래 *풀이 단어: tactile(촉각의), tickle(간질이다) — 핵심어·단어 체크에서 뺐다(뜻만 둠).
해설지(2027-09-평가원/해설.txt 32번) 해석·Words and Phrases와 대조함 — tune to ~에 맞추다, noticeable 두드러진, anticipate 예상하다.
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음). Claude 초안 — 선생님 검토 전.

선생님이 확인할 점
1. 「같은 쪽? 반대 쪽?」(s8_side)을 글쓴이 주장 대신 「어른은 칠판의 어느 쪽(덜 느낌 ↔ 크게 느낌)에 가까울까?」로 물었다.
   빈칸이 「놀라게 하기 어려운 이유」라서, 덜 느끼는 쪽(스스로 간지럽히기)과 같은 쪽이라는 게 열쇠다.
2. 칠판 묶음 이름은 글에 나온 말 less noticeable(덜 두드러짐) ↔ surprising(놀라운)으로 했다. 정답 말(anticipate, 예상)은 칠판에 쓰지 않았다.
   다만 s8_fill 힌트·s8_go·문제 안내는 「스스로 간지럽힐 때 덜 놀라는 까닭」으로 이끈다 — 답에 너무 가까운지 봐 주세요.
3. ② 를 많이 고른 이유(글에 나온 말이 섞인 보기)는 추측이다. option_review는 ② 하나만 달았다(④ 11%는 option_feedback만).
4. 헷갈리는 단어(trap): 1문장 tuned(맞춰진), 3문장 cross(꼬다)·brushed(스쳤다) — 엑셀(함정단어.xlsx)에는 안 넣었다.
5. 해석 맞추기는 7문장(짧은 문장)에만. 1문장 「Not only are … (도치)」는 Tip으로만 짚었다.
6. 8문장(빈칸)의 that절은 the fact와 동격 — 핵심이라 안의 adults(S)·are(V)도 끊어읽기 roles에 넣었다.
7. 5문장(방어 기제)은 문제 풀이에 덜 중요해서 한 줄 정리만 했다.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, tip, groups, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-09-32-tickle-surprise"

BLANK = "This is likely due to the fact that adults are ________, and hence are more difficult to surprise, than are children."
S = [
    "Not only are our sensory systems organized to detect change, but they are most tuned to stimuli that are unexpected and surprising.",
    "When you move your body and produce tactile sensations, these stimuli are less noticeable to you than are sensations produced "
    "by another individual.",
    "The sensations of your own legs touching one another when you cross your legs, for example, are generally less noticeable than "
    "a similar touch on your leg would be if someone sitting next to you brushed their leg against yours.",
    "Likewise, your reaction to your cat jumping onto your lap is likely to be much greater if you have your eyes closed when it happens.",
    "This differential response to surprising tactile stimuli appears to be a defense mechanism that has adaptive significance.",
    "It is probably also the reason why being tickled by someone else is more effective at producing an emotional reaction than "
    "trying to tickle yourself.",
    "Our enjoyment of being tickled generally diminishes as we age.",
    BLANK,
]
# 해설지 해석 (2027-09-평가원/해설.txt 32번)
KO = [
    "우리의 감각 체계는 변화를 감지하도록 구성되어 있을 뿐만 아니라, 예상치 못하고 놀라운 자극에 가장 맞춰져 있다.",
    "여러분이 몸을 움직여 촉각의 감각을 만들어 낼 때, 여러분에게 이 자극은 또 다른 사람이 만들어 내는 감각보다 덜 두드러진다.",
    "예를 들어, 여러분이 다리를 꼬았을 때 여러분 자신의 다리가 서로 닿는 감각은, 여러분 옆에 앉아 있는 어떤 사람이 자신의 다리를 "
    "여러분의 다리에 스치는 경우에 여러분의 다리에 느껴지는 유사한 접촉이 그러한 경우보다 일반적으로 덜 두드러진다.",
    "마찬가지로, 고양이가 여러분의 무릎 위로 뛰어오르는 것에 대한 여러분의 반응은 그 일이 발생할 때 여러분이 눈을 감는다면 훨씬 더 클 것이다.",
    "놀라운 촉각의 자극에 대한 이러한 상이한 반응은 적응의 의미를 지닌 방어 기제인 것으로 보인다.",
    "그것은 아마도 또한 스스로를 간지럽히려고 할 때보다 어떤 다른 사람에 의해 간지럼을 당하는 것이 감정적 반응을 일으키는 데에 "
    "더 효과적인 이유일 것이다.",
    "간지럼을 당하는 것에 대한 우리의 즐거움은 나이가 들어가면서 일반적으로 감소한다.",
    "이것은 아마도 어린이가 그러한 것보다 성인이 ________, 따라서 놀라게 하기가 더 어렵다는 사실 때문일 것이다.",
]

LEFT = "왼쪽 · less noticeable 쪽"
RIGHT = "오른쪽 · surprising 쪽"


def board(left, right, fresh=(), sort=None):
    """단어 지도 — 묶음 이름은 글에 나온 말(less noticeable / surprising)까지만. 빈칸 말(예상하다)은 쓰지 않는다"""
    return groups("덜 느끼는 감각과 크게 느끼는 감각", "less noticeable (덜 두드러짐)", left, "surprising (놀라움)", right,
                  fresh=fresh, between="↔", sort={"words": sort, "left": LEFT, "right": RIGHT} if sort else None)


L2 = [("you move your body", "내가 몸을 움직임")]
R2 = [("unexpected and surprising", "예상 못 한, 놀라운"), ("another individual", "다른 사람")]
L3 = L2 + [("your own legs", "내 다리끼리")]
R3 = R2 + [("someone sitting next to you", "옆에 앉은 사람")]
R4 = R3 + [("eyes closed", "눈을 감고")]
L6 = L3 + [("tickle yourself", "스스로 간지럽히기")]
R6 = R4 + [("someone else", "다른 사람")]

SIDE_TIP = tip("같은 쪽? 반대 쪽?", "빈칸 문장에 But, However, not 같은 반전 단서가 있으면 반대 의견이 들어가요. "
               "and hence(그래서)처럼 결과를 잇는 말이 있으면, 그 결과와 같은 쪽 말이 들어가요.")

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Not only", "~일 뿐만 아니라"), g("our sensory systems", "우리의 감각 체계"), g("sensory", "감각의"),
                    g("systems", "체계"), g("organized", "구성된"), g("to detect change", "변화를 감지하도록"), g("detect", "감지하다"),
                    g("change", "변화"), g("are most tuned to", "~에 가장 맞춰져 있다"), g("most", "가장"), g("tuned", "맞춰진"),
                    g("stimuli", "자극 (stimulus의 복수)"), g("unexpected and surprising", "예상치 못하고 놀라운"),
                    g("unexpected", "예상치 못한"), g("surprising", "놀라운"),
                    # 빈칸 문장 (s1 화면에서 띄운다)
                    g("is likely due to", "아마 ~ 때문일 것이다"), g("likely", "아마"), g("due to", "~ 때문에"),
                    g("the fact that", "~라는 사실"), g("fact", "사실"), g("adults", "성인, 어른"), g("hence", "따라서, 그래서"),
                    g("more difficult to surprise", "놀라게 하기가 더 어려운"), g("difficult", "어려운"), g("surprise", "놀라게 하다"),
                    g("than are children", "어린이가 그러한 것보다"), g("children", "어린이")],
        "slashes": ["systems organized", "detect change,", "most tuned", "to stimuli"],
        "roles": [r("our sensory systems", "S"), r("are … organized", "V"), r("they", "S"), r("are most tuned", "V")],
        "modifiers": ["that are unexpected and surprising"],
        "steps": [
            show("s1_passage", "빈칸은 마지막 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "어른은 아이보다 더 ____하고, 그래서 놀라게 하기가 더 어렵다", True),
                    ("o1", "어른은 아이보다 덜 ____해서, 놀라게 하기가 더 쉽다", False),
                    ("o2", "아이는 어른보다 더 ____하고, 그래서 놀라게 하기가 더 어렵다", False)],
                   "hence는 '그래서'예요. 'adults are ____, and hence …'의 주어는 adults, 비교 대상은 끝의 children이에요.",
                   why="'adults are ____, and hence are more difficult to surprise', 어른은 ____해서 놀라게 하기가 더 어렵대요. 'than are children'은 아이보다라는 뜻이에요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["adults", "________", "hence", "difficult", "surprise", "children"],
                   tips=[tip("A, and hence B", "'A이고, 그래서 B'예요. 빈칸(A)은 놀라게 하기 어려운 것(B)의 이유예요.", "hence"),
                         tip("than are children", "than children are를 뒤집은 꼴이에요. '아이들이 그런 것보다'로 읽어요.", "than are")]),
            show("s1_where", "빈칸은 어른을 놀라게 하기 어려운 이유예요. 무엇이 사람을 놀라게 하는지 생각하며 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                 highlight=["hence", "difficult", "surprise"]),
            choice("s1_tuned",
                   "우리 감각 체계는 어떤 자극에 가장 맞춰져 있대요?",
                   [("o0", "예상하지 못한, 놀라운 자극", True),
                    ("o1", "늘 반복되는 익숙한 자극", False),
                    ("o2", "아주 약하고 작은 자극", False)],
                   "but 뒤 'are most tuned to stimuli that …'을 봐요. that 뒤가 어떤 자극인지 말해요.",
                   why="'most tuned to stimuli that are unexpected and surprising', 예상치 못하고 놀라운 자극에 가장 맞춰져 있대요.",
                   highlight=["most tuned", "unexpected", "surprising"],
                   tips=[tip("Not only are ~", "Not only가 문장 맨 앞에 오면 주어와 동사 순서가 바뀌어요. are our sensory systems = our sensory systems are.",
                             "Not only"),
                         tip("be tuned to ~", "'~에 맞춰져 있다'예요. 라디오 주파수를 맞추듯 그 자극을 잘 잡는다는 뜻이에요.", "tuned to")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("When", "~할 때"), g("you move your body", "몸을 움직이다"), g("move", "움직이다"), g("body", "몸"),
                    g("produce", "만들어 내다"), g("tactile sensations", "촉각의 감각"), g("tactile", "촉각의"),
                    g("sensations", "감각"), g("these stimuli", "이 자극"), g("stimuli", "자극"),
                    g("less noticeable", "덜 두드러진"), g("noticeable", "두드러진, 눈에 띄는"),
                    g("than are sensations", "감각보다"), g("produced by another individual", "다른 사람이 만들어 내는"),
                    g("produced", "만들어진"), g("another individual", "다른 사람"), g("individual", "개인, 사람")],
        "slashes": ["your body", "tactile sensations,", "to you", "than are sensations"],
        "roles": [r("you", "S"), r("move", "V"), r("these stimuli", "S"), r("are", "V"), r("less noticeable", "C")],
        "modifiers": ["produced by another individual"],
        "steps": [
            choice("s2_which",
                   "어느 쪽 감각이 덜 두드러진대요?",
                   [("o0", "내가 몸을 움직여 만든 감각", True),
                    ("o1", "다른 사람이 만든 감각", False),
                    ("o2", "둘 다 똑같다", False)],
                   "'these stimuli are less noticeable … than ~'에서 these stimuli가 무엇인지 앞을 봐요.",
                   why="these stimuli는 내가 몸을 움직여(you move your body) 만든 감각이에요. 이게 다른 사람이 만든 감각보다 덜 두드러져요.",
                   highlight=["less noticeable", "another individual"],
                   tips=[tip("than are sensations", "than sensations … are를 뒤집은 꼴이에요. '다른 사람이 만든 감각보다'로 읽어요.", "than are")]),
            show("s2_board", "내가 만든 감각은 덜 느끼고, 다른 사람이 만든 감각은 더 크게 느껴요.",
                 panel=board(L2, R2, fresh=("you move your body", "another individual")),
                 highlight=["less noticeable", "another individual"], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("The sensations", "감각"), g("sensations", "감각"), g("your own legs", "자기 자신의 다리"), g("legs", "다리"),
                    g("touching one another", "서로 닿는"), g("touching", "닿는"), g("one another", "서로"),
                    g("cross your legs", "다리를 꼬다"), g("cross", "꼬다"), g("for example", "예를 들어"), g("example", "예"),
                    g("generally", "일반적으로"), g("less noticeable", "덜 두드러진"), g("noticeable", "두드러진"),
                    g("a similar touch on your leg", "다리에 느껴지는 비슷한 접촉"), g("similar", "비슷한"), g("touch", "접촉"),
                    g("leg", "다리"), g("would be", "~일 것이다"), g("someone sitting next to you", "옆에 앉아 있는 사람"),
                    g("someone", "어떤 사람"), g("sitting", "앉아 있는"), g("next to", "~ 옆에"), g("brushed", "스쳤다"),
                    g("against yours", "너의 것(다리)에"), g("against", "~에 닿게"), g("yours", "너의 것")],
        "slashes": ["The sensations", "one another", "your legs,", "for example,", "less noticeable", "would be", "next to you"],
        "roles": [r("The sensations", "S"), r("are", "V"), r("less noticeable", "C"), r("someone", "S"), r("brushed", "V")],
        "modifiers": ["of your own legs touching one another", "sitting next to you"],
        "steps": [
            choice("s3_sort",
                   "'someone sitting next to you(옆에 앉은 사람)'의 다리가 스치는 건 칠판 어느 쪽일까요?",
                   [("o0", LEFT, False), ("o1", RIGHT, True)],
                   "'less noticeable than ~'을 봐요. 내 다리끼리 닿는 감각이 그것보다 덜 두드러진대요.",
                   why="내 다리끼리 닿는 건 덜 느끼고, 옆 사람 다리가 스치는 건 더 크게 느껴요. 다른 사람이 만든 감각이에요.",
                   panel=board(L2, R2, sort=["someone sitting next to you"]),
                   highlight=["your own legs", "less noticeable", "someone"]),
            show("s3_board", "2문장의 예시예요. 내 다리끼리 닿는 건 덜 느끼고, 옆 사람 다리가 스치면 더 크게 느껴요.",
                 panel=board(L3, R3, fresh=("your own legs", "someone sitting next to you")),
                 highlight=["your own legs", "someone"], faded=["for example,"], button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "medium",
        "glosses": [g("Likewise", "마찬가지로"), g("your reaction", "너의 반응"), g("reaction", "반응"),
                    g("to your cat jumping onto your lap", "고양이가 무릎 위로 뛰어오르는 것에 대한"), g("cat", "고양이"),
                    g("jumping", "뛰어오르는"), g("onto", "~ 위로"), g("lap", "무릎 (앉았을 때 허벅지 위)"),
                    g("is likely to be", "~일 것이다"), g("likely", "~할 것 같은"), g("much greater", "훨씬 더 큰"),
                    g("greater", "더 큰"), g("have your eyes closed", "눈을 감고 있다"), g("eyes", "눈"), g("closed", "감은"),
                    g("eyes closed", "눈을 감고"), g("when it happens", "그 일이 일어날 때"), g("happens", "일어나다")],
        "slashes": ["Likewise,", "onto your lap", "much greater", "eyes closed"],
        "roles": [r("your reaction", "S"), r("is likely to be", "V"), r("much greater", "C"), r("you", "S"), r("have", "V")],
        "modifiers": ["to your cat jumping onto your lap"],
        "steps": [
            choice("s4_when",
                   "고양이가 무릎에 뛰어오를 때, 언제 반응이 훨씬 클까요?",
                   [("o0", "눈을 감고 있을 때", True), ("o1", "눈을 뜨고 고양이를 보고 있을 때", False),
                    ("o2", "고양이를 직접 안아 올릴 때", False)],
                   "문장 끝 'if you have your eyes …'를 봐요.",
                   why="'much greater if you have your eyes closed', 눈을 감고 있으면 반응이 훨씬 더 크대요.",
                   highlight=["much greater", "eyes closed"],
                   tips=[tip("have + 목적어 + p.p.", "have your eyes closed = 눈을 감은 상태로 두다, 눈을 감고 있다.", "have your eyes")]),
            show("s4_board", "눈을 감고 있으면(eyes closed) 반응이 훨씬 커요. 이것도 surprising 쪽이에요.",
                 panel=board(L3, R4, fresh=("eyes closed",)), highlight=["eyes closed"], button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "low",
        "glosses": [g("This differential response", "이러한 상이한 반응"), g("differential", "상이한, 차이를 보이는"),
                    g("response", "반응"), g("to surprising tactile stimuli", "놀라운 촉각의 자극에 대한"),
                    g("appears to be", "~인 것으로 보인다"), g("appears", "~인 것 같다"), g("a defense mechanism", "방어 기제"),
                    g("defense", "방어"), g("mechanism", "기제, 구조"), g("adaptive significance", "적응의 의미"),
                    g("adaptive", "적응의"), g("significance", "의미, 중요성")],
        "slashes": ["differential response", "tactile stimuli", "defense mechanism"],
        "roles": [r("This differential response", "S"), r("appears to be", "V"), r("a defense mechanism", "C")],
        "modifiers": ["that has adaptive significance"],
        "steps": [
            show("s5_note", "놀라운 자극에 이렇게 더 크게 반응하는 건, 몸을 지키는 방어 기제(defense mechanism)래요.",
                 highlight=["differential response", "defense mechanism"], button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("It", "그것"), g("probably", "아마"), g("the reason why", "~하는 이유"), g("reason", "이유"),
                    g("being tickled", "간지럼을 당하는 것"), g("tickled", "간지럼을 당한"), g("by someone else", "다른 사람에 의해"),
                    g("someone else", "다른 사람"), g("more effective at producing", "일으키는 데 더 효과적인"),
                    g("effective", "효과적인"), g("producing", "일으키는 것"), g("an emotional reaction", "감정적 반응"),
                    g("emotional", "감정적인"), g("reaction", "반응"), g("trying to tickle yourself", "스스로 간지럽히려고 하는 것"),
                    g("trying", "~하려고 하는 것"), g("tickle", "간지럽히다"), g("yourself", "자기 자신"),
                    g("tickle yourself", "스스로 간지럽히다")],
        "slashes": ["the reason", "someone else", "emotional reaction"],
        "roles": [r("It", "S"), r("is", "V"), r("the reason", "C")],
        "modifiers": ["why being tickled by someone else is more effective at producing an emotional reaction than trying to tickle yourself"],
        "steps": [
            pick("s6_same", "칠판의 another individual(다른 사람)과 같은 쪽 말을 이 문장에서 찾아 눌러 볼까요?",
                 ["being tickled", "someone else", "an emotional reaction", "tickle yourself"], ["someone else"],
                 "그건 surprising 쪽, 남이 만드는 쪽 말이 아니에요.",
                 "someone else(다른 사람)예요. 남이 간지럽히면 스스로 간지럽힐 때보다 반응이 커요.",
                 wrong_by={"being tickled": "간지럼을 당하는 건 두 쪽 모두에 있어요. 누가 간지럽히는지(by ~) 봐요.",
                           "an emotional reaction": "감정적 반응은 결과예요. 누가 간지럽힐 때 반응이 큰지 봐요.",
                           "tickle yourself": "스스로 간지럽히는 건 내가 만드는 쪽, 덜 느끼는 쪽이에요."},
                 tips=[tip("It", "It은 앞 문장의 This differential response(놀라운 자극에 다르게 반응하는 것)를 가리켜요.", "It is"),
                       tip("more ~ than …", "'…보다 더 ~한'이에요. being tickled by someone else가 trying to tickle yourself보다 더 효과적이래요.",
                           "more effective")]),
            show("s6_board", "남이 간지럽히면(someone else) 크게 느끼고, 스스로 간지럽히면(tickle yourself) 덜 느껴요.",
                 panel=board(L6, R6, fresh=("tickle yourself", "someone else")), highlight=["someone else", "tickle yourself"],
                 button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("Our enjoyment", "우리의 즐거움"), g("enjoyment", "즐거움"), g("of being tickled", "간지럼을 당하는 것에 대한"),
                    g("being tickled", "간지럼을 당하는 것"), g("tickled", "간지럼을 당한"), g("generally", "일반적으로"),
                    g("generally diminishes", "일반적으로 감소한다"), g("diminishes", "감소하다, 줄어들다"),
                    g("as we age", "나이가 들어가면서"), g("age", "나이가 들다")],
        "slashes": ["of being tickled"],
        "roles": [r("Our enjoyment", "S"), r("diminishes", "V")],
        "modifiers": ["of being tickled"],
        "steps": [],
    },
    {
        "id": 8, "text": BLANK, "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("This", "이것"), g("is likely due to", "아마 ~ 때문일 것이다"), g("likely", "아마"), g("due to", "~ 때문에"),
                    g("the fact that", "~라는 사실"), g("fact", "사실"), g("adults", "성인, 어른"), g("hence", "따라서, 그래서"),
                    g("more difficult to surprise", "놀라게 하기가 더 어려운"), g("difficult", "어려운"), g("surprise", "놀라게 하다"),
                    g("than are children", "어린이가 그러한 것보다"), g("children", "어린이")],
        "slashes": ["This is likely", "the fact", "________,", "to surprise,"],
        "roles": [r("This", "S"), r("is", "V"), r("adults", "S"), r("are", "V")],
        "steps": [
            choice("s8_side",
                   "빈칸 속 어른은 놀라게 하기 어렵대요. 어른은 칠판의 어느 쪽에 더 가까울까요?",
                   [("o0", "less noticeable 쪽 — 스스로 간지럽힐 때처럼 덜 놀란다", True),
                    ("o1", "surprising 쪽 — 남이 간지럽힐 때처럼 크게 놀란다", False)],
                   "빈칸 바로 뒤 'and hence are more difficult to surprise'를 봐요. 반전 단서 없이 결과를 이어요.",
                   why="'more difficult to surprise', 놀라게 하기가 더 어렵대요. 덜 놀라는 쪽이니, 스스로 간지럽힐 때와 같은 쪽이에요.",
                   highlight=["hence", "difficult", "surprise"], panel=board(L6, R6), tips=[SIDE_TIP],
                   point="빈칸 = 놀라게 하기 어려운 이유 = 덜 느끼는 쪽(스스로 간지럽히기)과 같은 쪽"),
            choice("s8_fill",
                   "그럼 빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "남의 반응을 덜 신경 쓰는", False),
                    ("o1", "자극이 올 것을 미리 아는", True),
                    ("o2", "한 가지에 더 오래 집중하는", False)],
                   "빈칸은 hence(그래서) 앞, 놀라게 하기 어려운 이유예요. 스스로 간지럽힐 때 덜 놀라는 까닭을 떠올려 봐요.",
                   why="스스로 간지럽히면 어디를 언제 간지럽힐지 이미 알아서 덜 놀라요. 어른도 무엇이 올지 더 잘 알아서 놀라게 하기 어려워요.",
                   highlight=["________", "hence", "surprise"],
                   point="빈칸 = 무엇이 올지 미리 앎 → 그래서 놀라게 하기 어렵다"),
            show("s8_go", "빈칸은 어른을 놀라게 하기 어려운 이유, 스스로 간지럽힐 때와 같은 쪽이에요. 이 말을 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — 짧은 7문장만 (모두에게)
add_match(sentences, 7, [m("Our enjoyment of being tickled", "간지럼을 당하는 것에 대한 우리의 즐거움은"), " ",
                         m("generally diminishes", "일반적으로 줄어든다"), " ", m("as we age", "나이가 들어가면서"), "."])
# 가리키는 말
add_refers(sentences, 1, {"they": "our sensory systems(우리의 감각 체계)"})
add_refers(sentences, 2, {"these stimuli": "내가 몸을 움직여 만든 촉각의 감각"})
add_refers(sentences, 4, {"when it happens": "it = 고양이가 무릎 위로 뛰어오르는 일"})
add_refers(sentences, 5, {"This differential response": "놀라운 자극에 더 크게 반응하는 것(2~4문장)"})
add_refers(sentences, 6, {"It": "This differential response(놀라운 자극에 다르게 반응하는 것)"})
add_refers(sentences, 8, {"This": "나이가 들면서 간지럼이 덜 즐거워지는 것(7문장)"})

SENSES = {
    1: [sense("to", "organized to detect change", "~하도록", "to부정사 (목적) — 변화를 감지하도록 구성된"),
        sense("but", "Not only …, but they are …", "~뿐만 아니라", "not only A but (also) B = A일 뿐만 아니라 B"),
        sense("to", "tuned to stimuli", "~에", "be tuned to ~ = ~에 맞춰져 있다"),
        sense("that", "stimuli that are unexpected", "~한 (자극)", "관계대명사 that — stimuli를 꾸민다")],
    2: [sense("to", "less noticeable to you", "~에게", "전치사 to (대상)")],
    3: [sense("for", "for example", "예를 들어", "for example = 예를 들어"),
        sense("if", "if someone … brushed", "만약 ~라면", "가정 if (과거형 brushed — would be와 짝)"),
        sense("to", "next to you", "~ 옆에", "next to ~ = ~ 옆에")],
    4: [sense("to", "reaction to your cat", "~에 대한", "전치사 to — reaction to ~ = ~에 대한 반응"),
        sense("to", "is likely to be", "~할 (것 같다)", "be likely to + 동사원형 = ~할 것 같다"),
        sense("if", "if you have your eyes closed", "만약 ~라면", "조건 if")],
    5: [sense("to", "response to surprising tactile stimuli", "~에 대한", "전치사 to — response to ~ = ~에 대한 반응"),
        sense("to", "appears to be", "~인 (것 같다)", "appear to + 동사원형 = ~인 것 같다"),
        sense("that", "a defense mechanism that has", "~한 (기제)", "관계대명사 that — a defense mechanism을 꾸민다")],
    6: [sense("to", "trying to tickle yourself", "~하려고", "try to + 동사원형 = ~하려고 하다")],
    7: [sense("as", "as we age", "~하면서", "접속사 as — 나이가 들어가면서")],
    8: [sense("to", "due to the fact", "~ 때문에", "due to ~ = ~ 때문에"),
        sense("that", "the fact that adults are", "~라는 (사실)", "동격 that — the fact의 내용"),
        sense("to", "difficult to surprise", "~하기 (어려운)", "형용사 + to부정사 = ~하기에 …한")],
}

WORDS = {"sensory": "감각의", "systems": "체계", "organized": "구성된", "detect": "감지하다", "change": "변화", "tuned": "맞춰진",
         "stimuli": "자극", "unexpected": "예상치 못한", "surprising": "놀라운", "likely": "~할 것 같은", "due": "~ 때문인",
         "fact": "사실", "adults": "어른", "hence": "따라서", "difficult": "어려운", "surprise": "놀라게 하다", "children": "어린이",
         "move": "움직이다", "body": "몸", "produce": "만들어 내다", "tactile": "촉각의", "sensations": "감각",
         "noticeable": "두드러진", "produced": "만들어진", "individual": "개인, 사람", "legs": "다리", "touching": "닿는",
         "cross": "꼬다", "example": "예", "generally": "일반적으로", "similar": "비슷한", "touch": "접촉", "leg": "다리",
         "someone": "어떤 사람", "sitting": "앉아 있는", "next": "옆의", "brushed": "스쳤다", "yours": "너의 것",
         "likewise": "마찬가지로", "reaction": "반응", "cat": "고양이", "jumping": "뛰어오르는", "lap": "무릎",
         "greater": "더 큰", "eyes": "눈", "closed": "감은", "happens": "일어나다", "differential": "상이한", "response": "반응",
         "appears": "~인 것 같다", "defense": "방어", "mechanism": "기제", "adaptive": "적응의", "significance": "의미",
         "probably": "아마", "reason": "이유", "being": "~인 것", "tickled": "간지럼을 당한", "effective": "효과적인",
         "producing": "일으키는 것", "emotional": "감정적인", "trying": "~하려고 하는 것", "tickle": "간지럽히다",
         "yourself": "자기 자신", "enjoyment": "즐거움", "diminishes": "감소하다", "age": "나이가 들다", "much": "훨씬",
         "else": "다른", "would": "~일 것이다", "one": "하나 · one another = 서로", "another": "또 다른"}

STORIES = [
    (5, [sc("문장 1", "🎯", "most tuned to unexpected and surprising stimuli", "감각은 예상 못 한 놀라운 자극에 가장 맞춰져 있어요"),
         sc("문장 2~4", "🐈", "your own touch < someone else’s touch · eyes closed", "내가 만든 감각보다 남이 만든 감각, 눈을 감았을 때를 더 크게 느껴요"),
         sc("문장 5", "🛡️", "a defense mechanism", "놀라운 자극에 더 크게 반응하는 건 방어 기제예요")]),
]

OPTIONS = [("1", "more cautious of acting immediately", "즉각적으로 행동하는 것에 더 조심하는", False, ["cautious", "acting immediately"]),
           ("2", "less sensitive to others’ reactions", "다른 사람들의 반응에 덜 민감한", False, ["less sensitive", "others’ reactions"]),
           ("3", "stronger in their ability to focus", "자신의 집중하는 능력에서 더 강한", False, ["ability to focus"]),
           ("4", "slower in adapting to changes", "변화에 적응하는 데에 더 느린", False, ["slower", "adapting"]),
           ("5", "better at anticipating stimuli", "자극을 더 잘 예상하는", True, ["anticipating", "stimuli"])]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 8, "analysis_first": True, "wrong_rate": 61, "wrong_rank": 2,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("cautious", "조심하는"), g("acting immediately", "즉각적으로 행동하는 것"), g("immediately", "즉각적으로"),
                g("sensitive", "민감한"), g("others’ reactions", "다른 사람들의 반응"), g("ability to focus", "집중하는 능력"),
                g("ability", "능력"), g("focus", "집중하다"), g("adapting to changes", "변화에 적응하는 것"), g("adapting", "적응하는 것"),
                g("anticipating", "예상하는 것"), g("stimuli", "자극")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[4], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "빈칸은 어른을 놀라게 하기 어려운 이유, 스스로 간지럽힐 때와 같은 쪽이에요. 이 말을 바꿔 쓴 보기를 골라 봐요.",
        "정답이에요! 스스로 간지럽힐 때처럼, 무엇이 올지 미리 알면 덜 놀라요. 어른은 아이보다 자극을 더 잘 예상해서(better at anticipating stimuli) 놀라게 하기가 더 어려워요.",
        "정답은 ⑤ better at anticipating stimuli(자극을 더 잘 예상하는)예요. 어른은 무엇이 올지 더 잘 알아서 놀라게 하기가 더 어려워요.",
        {"1": "cautious of acting(행동하는 것에 조심하는)은 글에 없는 이야기예요. 글은 행동이 아니라 자극을 느끼는 이야기예요.",
         "2": "less·others·reactions는 글에 나온 말이라 헷갈리기 쉬워요. 하지만 글은 남의 반응이 아니라 남이 만든 자극 이야기예요.",
         "3": "ability to focus(집중하는 능력)는 글에 나오지 않아요. 빈칸은 놀라게 하기 어려운 이유예요.",
         "4": "change(변화)·adaptive(적응의)는 1·5문장에 나와서 헷갈리기 쉬워요. 하지만 적응이 느리다는 말은 글에 없어요."},
        {"2": review(37,
                     "less sensitive to others’ reactions에는 글에 나온 말(less, another individual, emotional reaction)이 섞여 있어 그럴듯해 보여요.\n"
                     "하지만 글은 남의 '반응'이 아니라 남이 만든 '자극' 이야기예요. 빈칸은 hence(그래서) 뒤 '놀라게 하기 더 어렵다'의 이유라서, 무엇이 올지 미리 아는 쪽이에요.",
                     panel=rows(("빈칸 문장", "adults are ____, and hence are more difficult to surprise", "____ 그래서 놀라게 하기 더 어렵다", "hl"),
                                ("2·6문장", "you move your body · tickle yourself", "내가 만든 자극 → 덜 느낌", "hl"),
                                ("2·6문장", "another individual · someone else", "남이 만든 자극 → 크게 느낌", "hl2")),
                     rank_word="가장 많이 고른")}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(1·2)과 빈칸 문장만 ──
EMPHASIS = {
    1: ["tuned", "unexpected and surprising"],
    2: ["less noticeable", "another individual"],
    6: ["someone else", "tickle yourself"],
    8: ["hence", "more difficult to surprise"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 32번 (빈칸 추론, 2점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 같은 말 모으기 → 빈칸이 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-tickle-surprise.svg", ("Tickle yourself", "스스로 간지럽히기"), "vs",
                                       ("Tickled by others", "남이 간지럽히기"), "왜 스스로 간지럽히면 덜 간지러울까?",
                                       "2026년 9월 모의평가 32번 도입 칠판"),
                      "alt": "칠판: Tickle yourself(스스로 간지럽히기) vs Tickled by others(남이 간지럽히기)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "스스로 간지럽히면 왜 별로 안 간지러울까요? 이번 글은 우리 감각이 어떤 자극에 크게 반응하는지 이야기해요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("sensory", "감각의"), g("detect", "감지하다"), g("be tuned to", "~에 맞춰져 있다"),
                           g("stimulus", "자극 (pl. stimuli)"), g("unexpected", "예상치 못한"), g("sensation", "감각"),
                           g("noticeable", "두드러진"), g("individual", "개인, 사람"), g("cross one’s legs", "다리를 꼬다"),
                           g("brush", "스치다"), g("likewise", "마찬가지로"), g("lap", "무릎"), g("differential", "상이한"),
                           g("defense mechanism", "방어 기제"), g("adaptive", "적응의"), g("significance", "의미"),
                           g("effective", "효과적인"), g("emotional", "감정적인"), g("diminish", "감소하다"),
                           g("due to", "~ 때문에"), g("hence", "따라서")],
               "options": [g("cautious", "조심하는"), g("immediately", "즉각적으로"), g("sensitive", "민감한"),
                           g("ability", "능력"), g("adapt to", "~에 적응하다"), g("anticipate", "예상하다")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함: tune to 맞추다 · 다리를 꼬다 · 스치다.
TRAPS = {
    1: [tip("tuned", "이 글에서는 → (~에) 맞춰진  ('곡조·노래' 아님)", "tuned", trap=True)],
    3: [tip("cross", "이 글에서는 → (다리를) 꼬다  ('건너다' 아님)", "cross", trap=True),
        tip("brushed", "이 글에서는 → 스쳤다  ('솔질했다' 아님)", "brushed", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        # 1문장은 앞의 빈칸 화면(before_read) 뒤, 그 문장을 읽는 첫 스텝에 붙인다
        _first = next(st for st in _s["steps"] if not st.get("before_read"))
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법")
