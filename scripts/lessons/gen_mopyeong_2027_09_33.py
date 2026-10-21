"""2026년 9월 모의평가(2027학년도, 평가원) 영어 33번 레슨 + 대사를 만든다 (빈칸 추론, 3점). 오답률 57%(메가스터디) · Top 3.

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_33.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸이 가운데(셋째 문장 One solution, proposed by Balzac, is to ____.).
정답 ③ tie description to a moving body(묘사를 움직이는 사람과 연결하는 것).
선택률(메가스터디 풀서비스 채점): ① 16 ② 23 ③ 43 ④ 10 ⑤ 8 — 많이 고른 오답 ② present small objects in detail 23%.
② 짐작: 1문장 detail by detail, 4문장 detailed portrayals처럼 「자세히」가 여러 번 나와서. 하지만 자세한 묘사는 독자를 묘사의 숲에서
   길을 잃게 할 수 있는 쪽(문제)이고, 해결책은 정확한 경로(a precise path)를 따라 움직이며 묘사하는 것.
열쇠: 2문장 물음(How can … without losing the reader in a descriptive forest?) → 빈칸 = 그 해결책(One solution).
빈칸 뒤 4·5·6문장이 재진술: trace a precise path · approaching / entering / walking from room to room(움직이는 사람) · a precise notion.
칠판: losing the reader(길을 잃음) ↔ a precise path(정확한 경로) — 두 말이 다 나온 4문장 뒤에 처음 연다. 묶음 이름은 2·4문장에 나온 말.
시험지 아래 *풀이 단어: topography(지형) — 핵심어·단어 체크에서 뺐다(뜻만 단다).
해설지(content/tutor/exam-source/2027-09-평가원/해설.txt 33번) 해석·Words and Phrases와 대조함 — transport 이동시키다, capture 담아내다,
portrayal 묘사, threaten 위협하다, sense of orientation 방향 감각, narrator 화자(서술자), inspect 점검하다, prospective 미래의,
notion 개념, layout 배치, all the way down to ~에 이르기까지, floor plan 평면도.
오답률·선택률은 메가스터디 풀서비스 채점 기준(wrong_rate_source).
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음). Claude 초안 — 선생님 검토 전.

선생님이 확인할 점
1. 「같은 쪽? 반대 쪽?」(s3_side)을 「빈칸은 2문장 물음의 해결책 — 길을 잃지 않게 하는 쪽 / 더 자세히 늘리는 쪽 / 묘사를 빼는 쪽」
   3지로 물었다. 이 글은 반전 단서 대신 물음 → 해결책(One solution) 짜임이라서. 오답 「더 길고 자세하게」는 ②를 겨냥했다.
2. 빈칸 뒤에서 빈칸 내용을 3지로 묻는 s6_fill의 정답 보기 「집 안을 걸어 다니는 사람의 길을 따라 묘사한다」가 정답 ③과 가깝다.
   문제 화면이 너무 쉬워지면 s6_fill을 빼도 된다.
3. ②를 많이 고른 이유(detail이 여러 번 나옴)는 추측이다. option_review는 ② 하나만 달았다(① 16%는 달지 않음).
4. 헷갈리는 단어(trap): open(시작하다) · setting(배경) · manner(방식) · feel(느낌, 명사). 엑셀(함정단어.xlsx)에는 안 넣었다.
5. 2문장은 시험지 그대로 물음표(?)로 끝나는 문장이다. 5문장 as would a real estate agent는 도치(as + 조동사 + 주어) — Tip으로만.
6. 해석 맞추기는 6문장 하나만(20단어, 덩어리 5개). 칠판 정리(story)는 2·5문장 뒤 두 번.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-09-33-balzac-path"

BLANK = "One solution, proposed by Balzac, is to ________."
S = [
    "While a picture transports the spectator almost instantly into a landscape, language can only describe it detail by detail, "
    "bringing it slowly into the reader’s mind.",
    "How can a literary work capture the feel of a place in both its atmosphere and its topography without losing the reader "
    "in a descriptive forest?",
    BLANK,
    "Balzac’s novels open with detailed portrayals of the setting, but the descriptions never threaten the reader’s sense of "
    "orientation because they trace a precise path through the fictional world.",
    "When the novel describes a house, the narrator inspects the building in a systematic manner, approaching it from the street, "
    "examining the garden and the front, entering through the main door, and walking from room to room, as would a real estate "
    "agent or a prospective resident.",
    "The reader ends up with a precise notion of the layout of the building, all the way down to the floor plan.",
]
# 해설지 해석 (2027-09-평가원/해설.txt 33번)
KO = [
    "그림은 보는 사람을 거의 즉시 풍경 속으로 이동시키지만, 언어는 그것을 세부 사항별로 하나하나 묘사하여 그것을 독자의 마음속에 "
    "서서히 떠오르게 할 수 있을 뿐이다.",
    "문학 작품은 독자가 묘사의 숲에서 길을 잃게 하지 않으면서, 어떤 장소의 분위기와 지형 모두에 깃든 그곳의 느낌을 어떻게 담아낼 수 있을까?",
    "Balzac이 제안한 한 가지 해결책은 ________ 것이다.",
    "Balzac의 소설은 배경에 대한 상세한 묘사로 시작하지만, 그 묘사는 허구의 세계 속에서 정확한 경로를 따라 이루어지기 때문에 "
    "독자의 방향 감각을 결코 위협하지 않는다.",
    "소설이 집을 묘사할 때, 화자는 부동산 중개인이나 미래의 거주자처럼 체계적인 방식으로 건물을 점검하는데, 거리에서 그 집으로 다가가 "
    "정원과 정면을 살펴보고, 현관문을 통해 들어가서 방에서 방으로 걸어 다닌다.",
    "결국 독자는 평면도에 이르기까지 그 건물의 배치에 대해 정확한 개념을 갖게 된다.",
]

LEFT = "왼쪽 · losing the reader (길을 잃음)"
RIGHT = "오른쪽 · a precise path (정확한 경로)"


def board(left, right, fresh=(), sort=None):
    """단어 지도 — 묶음 이름은 2·4문장에 나온 말(losing the reader / a precise path)까지만. 보기 말(moving body)은 쓰지 않는다"""
    return groups("길을 잃음 ↔ 정확한 경로", "losing the reader (길을 잃음)", left, "a precise path (정확한 경로)", right,
                  fresh=fresh, between="↔", sort={"words": sort, "left": LEFT, "right": RIGHT} if sort else None)


L2 = [("a descriptive forest", "묘사의 숲")]
R4 = [("trace a precise path", "정확한 경로를 따라가다")]
R5 = R4 + [("walking from room to room", "방에서 방으로 걸어 다니며")]
R6 = R5 + [("a precise notion", "정확한 개념")]

SIDE_TIP = tip("같은 쪽? 반대 쪽?", "빈칸 문장에 But, However, not 같은 반전 단서가 있으면 반대 의견이 들어가요. "
               "앞 물음을 solution(해결책)으로 받으면 그 물음에 답하는 말이 들어가요.")

BLANK_GLOSSES = [g("One solution", "한 가지 해결책"), g("solution", "해결책"), g("proposed by Balzac", "Balzac이 제안한"),
                 g("proposed", "제안된"), g("Balzac", "발자크 · 프랑스 소설가 이름"), g("is to", "~하는 것이다")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("While", "~이지만, ~인 반면"), g("a picture", "그림"), g("picture", "그림"),
                    g("transports", "이동시키다, 데려가다"), g("the spectator", "보는 사람"), g("spectator", "보는 사람, 관객"),
                    g("almost instantly", "거의 즉시"), g("instantly", "즉시"), g("into a landscape", "풍경 속으로"),
                    g("landscape", "풍경"), g("language", "언어"), g("can only describe", "묘사할 수 있을 뿐이다"),
                    g("describe", "묘사하다"), g("detail by detail", "세부 사항 하나하나"), g("detail", "세부 사항"),
                    g("bringing it slowly", "그것을 서서히 데려오며"), g("bringing", "가져오는, 떠오르게 하는"), g("slowly", "천천히, 서서히"),
                    g("into the reader’s mind", "독자의 마음속으로"), g("reader’s", "독자의"), g("mind", "마음"), *BLANK_GLOSSES],
        "slashes": ["almost instantly", "into a landscape,", "describe it", "detail by detail,", "bringing it slowly"],
        "roles": [r("a picture", "S"), r("transports", "V"), r("the spectator", "O"), r("language", "S"),
                  r("can only describe", "V"), r("it", "O")],
        "steps": [
            show("s1_passage", "빈칸은 여기, 셋째 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "아주 짧은 문장이에요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "Balzac이 풀지 못한 문제는 ____이다", False),
                    ("o1", "Balzac이 제안한 한 가지 해결책은 ____하는 것이다", True),
                    ("o2", "Balzac은 ____하는 것에 반대했다", False)],
                   "solution은 '해결책'이에요. 콤마 사이 proposed by Balzac은 '발자크가 제안한'이에요.",
                   why="'One solution … is to ____', 한 가지 해결책은 ____하는 것이래요. 해결책이면 앞에 풀어야 할 문제가 있어요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["One solution", "________"], faded=["proposed by Balzac,"]),
            show("s1_where", "그럼 무엇을 해결하려는 건지 생각하며 문장 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
            choice("s1_meaning",
                   "While 앞뒤를 비교하면 무슨 뜻일까요?",
                   [("o0", "그림도 언어도 풍경을 곧바로 보여 준다", False),
                    ("o1", "그림은 풍경을 곧바로 보여 주지만, 언어는 하나하나 묘사해서 천천히 떠올리게 한다", True),
                    ("o2", "언어가 그림보다 풍경을 더 빨리 보여 준다", False)],
                   "While은 여기서 '~이지만, ~인 반면'이에요. instantly는 '즉시', slowly는 '천천히'예요.",
                   why="'a picture transports the spectator almost instantly', 그림은 거의 즉시 보여 줘요. 'language can only describe it detail by detail', 언어는 하나하나 묘사할 수밖에 없대요.",
                   highlight=["While", "instantly", "detail by detail", "slowly"],
                   tips=[tip("can only + 동사", "'~할 수 있을 뿐이다'예요. 언어는 하나하나 묘사하는 것밖에 못 한다는 말이에요.", "can only describe")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("How can", "어떻게 ~할 수 있을까"), g("a literary work", "문학 작품"), g("literary", "문학의"), g("work", "작품"),
                    g("capture", "담아내다, 포착하다"), g("the feel of a place", "어떤 장소의 느낌"), g("feel", "느낌"),
                    g("place", "장소"), g("in both its atmosphere and its topography", "그곳의 분위기와 지형 모두에서"),
                    g("both", "둘 다"), g("atmosphere", "분위기"), g("topography", "지형"),
                    g("without losing the reader", "독자가 길을 잃게 하지 않고"), g("losing", "잃는 것, 길을 잃게 하는 것"),
                    g("reader", "독자"), g("in a descriptive forest", "묘사의 숲에서"), g("descriptive", "묘사의"),
                    g("forest", "숲")],
        "slashes": ["a literary work", "the feel of a place", "its topography", "losing the reader"],
        "roles": [r("a literary work", "S"), r("can … capture", "V"), r("the feel of a place", "O")],
        "steps": [
            choice("s2_question",
                   "묻는 문장이에요. 이 문장은 무엇을 묻고 있을까요?",
                   [("o0", "문학 작품은 숲을 어떻게 묘사할까", False),
                    ("o1", "독자가 왜 그림보다 글을 좋아할까", False),
                    ("o2", "문학 작품은 독자가 묘사 속에서 헤매지 않게 하면서 장소의 느낌을 어떻게 담을까", True)],
                   "a descriptive forest는 진짜 숲이 아니라 비유예요. without losing the reader는 '독자를 잃지 않고'예요.",
                   why="'How can a literary work capture the feel of a place', 장소의 느낌을 어떻게 담을지 물어요. 'without losing the reader in a descriptive forest', 묘사가 빽빽한 숲에서 독자가 길을 잃지 않게 하면서요.",
                   highlight=["How can", "capture", "without losing the reader", "descriptive forest"],
                   tips=[tip("lose A in B", "'A가 B에서 길을 잃게 하다'예요. 묘사가 너무 많으면 독자가 숲에서처럼 헤맨다는 비유예요.",
                             "losing the reader"),
                         tip("feel", "이 글에서는 → (장소의) 느낌  ('느끼다' 동사 아님)", "the feel", trap=True)]),
        ],
    },
    {
        "id": 3, "text": BLANK, "model_translation": KO[2], "teaching_value": "high",
        "glosses": list(BLANK_GLOSSES),
        "roles": [r("One solution", "S"), r("is", "V")],
        "steps": [
            choice("s3_side",
                   "빈칸은 2문장 물음에 대한 해결책(One solution)이에요. 빈칸에는 어떤 쪽 말이 올까요?",
                   [("o0", "묘사를 더 길고 자세하게 늘리는 방법", False),
                    ("o1", "장소 묘사를 아예 빼는 방법", False),
                    ("o2", "장소의 느낌을 담으면서도 독자가 길을 잃지 않게 하는 방법", True)],
                   "2문장은 '어떻게 하면 독자가 묘사의 숲에서 길을 잃지 않을까'를 물었어요.",
                   why="해결책은 물음에 답하는 말이에요. 장소의 느낌은 담고, 독자는 길을 잃지 않게 하는 방법이에요.",
                   highlight=["One solution", "________"], faded=["proposed by Balzac,"], tips=[SIDE_TIP],
                   point="빈칸 = One solution = 2문장 물음(길을 잃지 않게 하며 장소를 담는 법)에 답하는 쪽"),
            show("s3_next", "어떻게 하면 길을 잃지 않는지는 빈칸 뒤에 나와요. Balzac이 어떻게 묘사하는지 찾으며 읽어 봐요.",
                 button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Balzac’s novels", "Balzac의 소설"), g("novels", "소설"), g("open with", "~로 시작하다"), g("open", "시작하다"),
                    g("detailed portrayals", "상세한 묘사"), g("detailed", "상세한, 자세한"), g("portrayals", "묘사"),
                    g("of the setting", "배경에 대한"), g("setting", "배경"), g("the descriptions", "그 묘사"),
                    g("descriptions", "묘사"), g("never threaten", "결코 위협하지 않는다"), g("never", "결코 ~ 않다"),
                    g("threaten", "위협하다"), g("the reader’s sense of orientation", "독자의 방향 감각"),
                    g("sense of orientation", "방향 감각"), g("sense", "감각"), g("orientation", "방향, 방향 감각"),
                    g("because", "~ 때문에"), g("they", "그것들(그 묘사)"), g("trace a precise path", "정확한 경로를 따라가다"),
                    g("trace", "따라가다, 그리다"), g("a precise path", "정확한 경로"), g("precise", "정확한"), g("path", "경로, 길"),
                    g("through the fictional world", "허구의 세계 속에서"), g("fictional", "허구의, 소설 속의"), g("world", "세계")],
        "slashes": ["Balzac’s novels open", "of the setting,", "never threaten", "sense of orientation", "a precise path"],
        "roles": [r("Balzac’s novels", "S"), r("open", "V"), r("the descriptions", "S"), r("never threaten", "V"),
                  r("the reader’s sense of orientation", "O"), r("they", "S"), r("trace", "V"), r("a precise path", "O")],
        "steps": [
            choice("s4_why",
                   "자세한 묘사인데도 독자가 방향을 잃지 않는 이유는 무엇일까요?",
                   [("o0", "묘사가 짧고 간단해서", False),
                    ("o1", "묘사가 소설 속 세계에서 정확한 경로를 따라가서", True),
                    ("o2", "독자가 그 장소를 이미 알고 있어서", False)],
                   "because 뒤를 봐요. trace는 '따라가다', path는 '경로'예요.",
                   why="'because they trace a precise path through the fictional world', 묘사가 소설 속 세계에서 정확한 길을 따라가기 때문이래요.",
                   highlight=["but", "never threaten", "because", "precise path"],
                   tips=[tip("sense of orientation", "'방향 감각'이에요. 내가 어디쯤 있는지 아는 감각이에요.", "sense of orientation")]),
            show("s4_board", "묘사가 많으면 독자가 길을 잃을 수 있어요.\nBalzac의 묘사는 정확한 경로(a precise path)를 따라가서 길을 잃지 않아요.",
                 panel=board(L2, R4, fresh=("a descriptive forest", "trace a precise path")), button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("When", "~할 때"), g("the novel", "그 소설"), g("novel", "소설"), g("describes a house", "집을 묘사하다"),
                    g("describes", "묘사하다"), g("house", "집"), g("the narrator", "화자, 서술자"), g("narrator", "화자, 서술자"),
                    g("inspects the building", "건물을 점검하다"), g("inspects", "점검하다, 살펴보다"), g("building", "건물"),
                    g("in a systematic manner", "체계적인 방식으로"), g("systematic", "체계적인"), g("manner", "방식"),
                    g("approaching it from the street", "거리에서 그곳으로 다가가며"), g("approaching", "다가가는"),
                    g("street", "거리"), g("examining the garden and the front", "정원과 정면을 살펴보며"),
                    g("examining", "살펴보는"), g("garden", "정원"), g("front", "정면, 앞쪽"),
                    g("entering through the main door", "현관문으로 들어가며"), g("entering", "들어가는"),
                    g("main door", "현관문"), g("main", "주된"), g("door", "문"),
                    g("walking from room to room", "방에서 방으로 걸어 다니며"), g("walking", "걷는"), g("room", "방"),
                    g("as would a real estate agent", "부동산 중개인이 그러하듯"), g("real estate agent", "부동산 중개인"),
                    g("real", "실제의"), g("estate", "부동산, 토지"), g("agent", "중개인"),
                    g("a prospective resident", "미래의 거주자"), g("prospective", "미래의, 장래의"), g("resident", "거주자")],
        "slashes": ["describes a house,", "inspects the building", "a systematic manner,", "from the street,", "and the front,",
                    "the main door,", "room to room,"],
        "roles": [r("the novel", "S"), r("describes", "V"), r("a house", "O"), r("the narrator", "S"), r("inspects", "V"),
                  r("the building", "O")],
        "steps": [
            choice("s5_order",
                   "화자(the narrator)는 집을 어떤 순서로 묘사할까요?",
                   [("o0", "작은 물건부터 하나씩 아주 자세히", False),
                    ("o1", "집에 들어가는 사람이 걷는 순서대로", True),
                    ("o2", "하늘에서 내려다보듯 한눈에", False)],
                   "콤마 뒤 approaching, examining, entering, walking을 차례로 봐요.",
                   why="거리에서 다가가고(approaching), 정원과 정면을 보고(examining), 현관문으로 들어가(entering) 방에서 방으로 걸어요(walking). 집을 보러 온 사람처럼 움직이며 묘사해요.",
                   highlight=["approaching", "examining", "entering", "walking"],
                   tips=[tip("as would + 사람", "'(그 사람이) 그러하듯이'예요. as a real estate agent would (inspect)에서 순서가 바뀐 꼴이에요.",
                             "as would"),
                         tip("manner", "이 글에서는 → 방식  ('예의, 매너' 아님)", "manner", trap=True)]),
            choice("s5_sort",
                   "'walking from room to room(방에서 방으로 걸어 다니며)'는 칠판 어느 쪽일까요?",
                   [("o0", LEFT, False), ("o1", RIGHT, True)],
                   "걸어가는 길이 정해져 있으면 길을 잃을까요, 안 잃을까요?",
                   why="방에서 방으로 차례로 걸어가는 건 정해진 길을 따라가는 거예요. 정확한 경로 쪽이에요.",
                   panel=board(L2, R4, sort=["walking from room to room"]), highlight=["walking from room to room"]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("The reader", "독자"), g("ends up with", "결국 ~을 갖게 되다"), g("ends", "끝나다"),
                    g("a precise notion", "정확한 개념"), g("notion", "개념, 생각"),
                    g("of the layout of the building", "그 건물의 배치에 대한"), g("the layout of the building", "그 건물의 배치"),
                    g("layout", "배치, 구조"), g("all the way down to the floor plan", "평면도에 이르기까지"),
                    g("all the way down to", "~에 이르기까지"), g("way", "길, 방식"), g("floor plan", "평면도"),
                    g("floor", "바닥, 층"), g("plan", "도면, 계획")],
        "slashes": ["a precise notion", "of the building,"],
        "roles": [r("The reader", "S"), r("ends up with", "V"), r("a precise notion", "O")],
        "steps": [
            choice("s6_fill",
                   "그럼 빈칸 '해결책은 ____하는 것'에는 어떤 말이 와야 할까요?",
                   [("o0", "작은 물건 하나하나를 아주 자세히 그린다", False),
                    ("o1", "집 안을 걸어 다니는 사람의 길을 따라 묘사한다", True),
                    ("o2", "장면을 멀리서 한눈에 보여 준다", False)],
                   "칠판 오른쪽, 5문장에서 화자가 어떻게 움직였는지 떠올려 봐요.",
                   why="화자가 거리에서 다가가 문으로 들어가 방에서 방으로 걸으며 묘사해요. 그 길을 따라가니 독자는 길을 잃지 않고 평면도까지 정확히 알게 돼요.",
                   panel=board(L2, R6, fresh=("a precise notion",)), highlight=["a precise notion"]),
            show("s6_go", "빈칸은 해결책 쪽이에요. 4·5문장의 정확한 경로(a precise path)를 다른 말로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — 6문장(20단어)만. 덩어리는 문장에 그대로 있는 구절
add_match(sentences, 6, [m("The reader", "독자는"), " 결국 ", m("all the way down to the floor plan", "평면도에 이르기까지"), " ",
                         m("the layout of the building", "건물의 배치에 대해"), " ", m("a precise notion", "정확한 개념을"), " ",
                         m("ends up with", "갖게 된다"), "."])
# 가리키는 말
add_refers(sentences, 1, {"it": "a landscape(풍경)"})
add_refers(sentences, 4, {"they": "the descriptions(그 묘사)"})
add_refers(sentences, 5, {"approaching it from the street": "it = the building(그 건물)"})

SENSES = {
    1: [sense("while", "While a picture", "~이지만, ~인 반면", "접속사 While (대조)")],
    3: [sense("to", "is to ________", "~하는 것", "be to + 동사원형 = ~하는 것이다 (보어)")],
    4: [sense("but", "but the descriptions", "그러나", "등위접속사 but (대조)")],
    5: [sense("to", "from room to room", "~로 (방에서 방으로)", "from A to B = A에서 B로"),
        sense("as", "as would a real estate agent", "~처럼, ~하듯이", "접속사 as (같은 방식) + 도치")],
    6: [sense("to", "all the way down to", "~에 이르기까지", "all the way down to + 명사")],
}

WORDS = {"while": "~인 반면", "picture": "그림", "transports": "이동시키다", "spectator": "보는 사람", "almost": "거의",
         "instantly": "즉시", "landscape": "풍경", "language": "언어", "describe": "묘사하다", "detail": "세부 사항",
         "bringing": "떠오르게 하는", "slowly": "서서히", "reader’s": "독자의", "mind": "마음", "literary": "문학의",
         "work": "작품", "capture": "담아내다", "feel": "느낌", "place": "장소", "atmosphere": "분위기", "topography": "지형",
         "losing": "잃게 하는 것", "reader": "독자", "descriptive": "묘사의", "forest": "숲", "solution": "해결책",
         "proposed": "제안된", "balzac": "발자크", "balzac’s": "발자크의", "novels": "소설", "open": "시작하다",
         "detailed": "상세한", "portrayals": "묘사", "setting": "배경", "descriptions": "묘사", "threaten": "위협하다",
         "sense": "감각", "orientation": "방향 감각", "trace": "따라가다", "precise": "정확한", "path": "경로",
         "fictional": "허구의", "novel": "소설", "describes": "묘사하다", "house": "집", "narrator": "화자",
         "inspects": "점검하다", "building": "건물", "systematic": "체계적인", "manner": "방식", "approaching": "다가가는",
         "street": "거리", "examining": "살펴보는", "garden": "정원", "front": "정면", "entering": "들어가는", "main": "주된",
         "door": "문", "walking": "걷는", "room": "방", "real": "실제의", "estate": "부동산", "agent": "중개인",
         "prospective": "미래의", "resident": "거주자", "ends": "끝나다", "notion": "개념", "layout": "배치",
         "floor": "바닥", "plan": "도면", "house,": "집", "landscape,": "풍경"}

STORIES = [
    (2, [sc("문장 1", "🖼️", "picture: instantly ↔ language: detail by detail", "그림은 바로 보여 주지만, 글은 하나하나 묘사해야 해요"),
         sc("문장 2", "🌲", "without losing the reader in a descriptive forest?", "묘사의 숲에서 독자가 길을 잃지 않게 하려면?")]),
    (5, [sc("문장 3~4", "🧭", "One solution: ____ · a precise path", "Balzac의 해결책 — 묘사가 정확한 경로를 따라가요"),
         sc("문장 5", "🚶", "approaching → entering → room to room", "화자가 거리에서 다가가 문으로 들어가 방에서 방으로 걸어요")]),
]

OPTIONS = [
    ("1", "flood the reader’s mind with abstract images", ["flood", "abstract images"], "독자의 마음을 추상적인 이미지로 가득 채우는 것", False),
    ("2", "present small objects in detail", ["small objects", "in detail"], "작은 사물을 상세하게 표현하는 것", False),
    ("3", "tie description to a moving body", ["tie", "moving body"], "묘사를 움직이는 사람과 연결하는 것", True),
    ("4", "distance readers from a scene", ["distance"], "독자를 장면에서 멀어지게 하는 것", False),
    ("5", "portray a landscape from upward angles", ["upward angles"], "아래에서 위를 바라보는 시점으로 풍경을 묘사하는 것", False),
]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오. [3점]",
    "underline": "________", "sentence": 3, "analysis_first": True, "wrong_rate": 57.0, "wrong_rank": 3,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("flood", "가득 채우다, 넘치게 하다"), g("abstract images", "추상적인 이미지"), g("present", "보여 주다, 표현하다"),
                g("small objects", "작은 사물"), g("in detail", "상세하게"), g("tie", "묶다, 연결하다"),
                g("description", "묘사"), g("a moving body", "움직이는 몸(사람)"), g("distance", "멀어지게 하다"),
                g("scene", "장면"), g("portray", "묘사하다"), g("upward angles", "아래에서 위로 보는 각도")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "칠판 오른쪽, 화자가 집을 어떻게 묘사했는지 떠올리며 골라 봐요.",
        "정답이에요! 화자가 거리에서 다가가 문으로 들어가 방에서 방으로 걸으며 묘사해요. 움직이는 사람의 길을 따라 묘사하니 독자가 길을 잃지 않아요.",
        "정답은 ③이에요. Balzac의 묘사는 집으로 다가가 들어가 방에서 방으로 걷는 사람의 길을 따라가요. 그래서 독자는 묘사의 숲에서 길을 잃지 않아요.",
        {"1": "추상적인 이미지 이야기는 없어요. 글은 집 안을 걷는 구체적인 길을 따라가요.",
         "2": "detail이 여러 번 나와서 헷갈렸죠. 하지만 자세한 묘사는 길을 잃게 할 수 있는 쪽이고, 해결책은 정확한 경로를 따라가는 거예요.",
         "4": "반대예요. 화자는 독자를 데리고 집 안으로 들어가요.",
         "5": "보는 각도 이야기는 없어요. 화자는 한자리에서 보지 않고 걸어 다니며 묘사해요."},
        {"2": review(23,
                     "②는 detail by detail, detailed portrayals처럼 '자세히'가 여러 번 나와서 끌려요. 하지만 자세한 묘사는 독자가 묘사의 숲에서 길을 잃을 수 있는 문제 쪽이에요.\nBalzac의 해결책은 화자가 집 안을 걸어 다니는 길(a precise path)을 따라 묘사하는 거예요.",
                     panel=rows(("2문장", "losing the reader in a descriptive forest", "자세한 묘사 — 길을 잃을 수 있다", "hl2"),
                                ("4·5문장", "trace a precise path · walking from room to room", "걷는 길을 따라 묘사 — 해결책", "hl")),
                     rank_word="가장 많이 고른")}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(2·4·5)만 ──
EMPHASIS = {
    2: ["capture", "without losing the reader"],
    4: ["never threaten", "trace a precise path"],
    5: ["the narrator", "walking from room to room"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 33번 (빈칸 추론, 3점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 두 쪽 말 모으기 → 빈칸이 어느 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-balzac-path.svg", ("Picture", "그림"), "↔", ("Language", "언어"),
                                       "글은 장소를 어떻게 보여 줄까?", "2026년 9월 모의평가 33번 도입 칠판"),
                      "alt": "칠판: Picture(그림) ↔ Language(언어)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "그림은 한눈에 보이지만 글은 한 줄씩 읽어야 해요. 이번 글은 소설이 장소를 묘사하는 방법 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("transport", "이동시키다"), g("spectator", "보는 사람"), g("instantly", "즉시"),
                           g("literary", "문학의"), g("capture", "담아내다"), g("atmosphere", "분위기"),
                           g("descriptive", "묘사의"), g("solution", "해결책"), g("portrayal", "묘사"), g("setting", "배경"),
                           g("threaten", "위협하다"), g("sense of orientation", "방향 감각"), g("precise", "정확한"),
                           g("fictional", "허구의"), g("narrator", "화자, 서술자"), g("inspect", "점검하다"),
                           g("systematic", "체계적인"), g("prospective", "미래의, 장래의"), g("resident", "거주자"),
                           g("notion", "개념"), g("layout", "배치"), g("floor plan", "평면도")],
               "options": [g("flood", "가득 채우다"), g("abstract", "추상적인"), g("tie A to B", "A를 B와 연결하다"),
                           g("distance", "멀어지게 하다"), g("upward", "위쪽으로의")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함:
# feel 느낌(s2_question) · manner 방식(s5_order)은 스텝 안에 직접 달았다. open 시작하다 · setting 배경은 4문장 첫 스텝에
TRAPS = {
    4: [tip("open", "이 글에서는 → (~로) 시작하다  ('열다' 아님)", "open with", trap=True),
        tip("setting", "이 글에서는 → (소설의) 배경  ('설정' 아님)", "setting", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법")
