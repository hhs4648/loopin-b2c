"""2026년 6월 모의평가(2027학년도, 평가원) 영어 33번 레슨 + 대사를 만든다 (빈칸 추론, 3점). 오답률 58%(메가스터디) · Top 7.

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_33.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸이 가운데(일곱째, The more affected one is, ____.). 정답 ② the less similarity is required
for the thing to appear. 선택률(메가스터디): ① 15 ② 42 ③ 15 ④ 16 ⑤ 11 — 많이 고른 오답 ④ 16%, ①·③ 15%(셋 다 option_review).
열쇠: 5문장 a small similarity … can lead to the misidentification(약간만 비슷해도 기대한 것으로 오인) — 빈칸은 이걸
The 비교급, the 비교급으로 바꿔 쓴 말. 빈칸은 감정의 영향 쪽(distorted · misidentification · inaccurately · biased)과 같은 쪽.
④(세상을 있는 그대로)는 반대 쪽, ①(차이 찾기)은 8문장의 보통 감각 기관 쪽, ③은 similarity만 겹친 말.
칠판: 한 묶음 「Emotions (감정)」 — 2문장 distorted(선생님) → 5문장 misidentification(학생이 찾아 누름). 묶음 이름은 2문장에 나온 말.
시험지 아래 *풀이 단어: discern — 핵심어·단어 체크에서 뺐다(뜻만 단다).
해설지(content/tutor/exam-source/2027-06-평가원/해설.txt 33번) 해석과 대조함 — dispose ~하도록 이끌다, distorted 왜곡된,
disposition 성향, misidentification 오인, organ 기관, investment 몰입, biased 편향된.
오답률·선택률은 메가스터디 풀서비스 채점 기준(wrong_rate_source).
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음). Claude 초안 — 선생님 검토 전.

선생님이 확인할 점
1. 많이 고른 오답이 고르게 퍼져 있어서(④16 ①15 ③15) 셋 다 option_review를 달았다. 하나만 남긴다면 ④(반대 쪽).
2. 빈칸 앞에서 빈칸 내용을 3지로 묻는 s7_fill의 정답 보기 「더 적게 비슷해도 기대한 것으로 보인다」가 정답 ②와 아주 가깝다.
   문제 화면이 너무 쉬워지면 s7_fill을 빼고 s7_side(같은 쪽?)만 둬도 된다.
3. 9문장(The greater the emotional investment, the more biased one’s perception)은 동사가 빠진 꼴이라 끊어읽기 roles를 넣지 않았다.
   빈칸 문장도 S·V(one · is)만 넣었다.
4. 헷갈리는 단어(trap): dispose(~하도록 이끌다, '처분하다' 아님) · disposition(성향) · investment(몰입). 엑셀(함정단어.xlsx)에는 안 넣었다.
   dispose는 2문장 해석 맞추기에서 뜻이 나오니 맞추기 다음 화면(s2_note)에 달았다.
5. 해석 맞추기는 짧은 2·4문장만. 칠판 정리(story)는 3·6문장 뒤 두 번.
6. 도입 물음 「무서울 때 그림자가 사람처럼 보인 적 있나요?」가 글 내용을 너무 많이 알려 주는지.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, tip, groups, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-06-33-emotion-perception"

BLANK = "The more affected one is, ________."
S = [
    "Imagination continues to function when perception is not actively discerning objects, in cases of emotion, disease, and sleep.",
    "Emotions dispose one to see the world in a distorted way.",
    "A coward’s perceptual disposition is affected by his disposition to experience fear.",
    "A lover’s expectations are affected by desire.",
    "In such cases, a small similarity between a perceived object and the thing one expects to see can lead to the "
    "misidentification of the perceived object as that thing.",
    "The coward sees the enemy, while the lover sees the object of desire everywhere.",
    BLANK,
    "While the central organ of sense normally functions by comparing similarities and differences, emotions dispose one to "
    "discern objects inaccurately.",
    "The greater the emotional investment, the more biased one’s perception.",
]
# 해설지 해석 (2027-06-평가원/해설.txt 33번)
KO = [
    "감정, 질병, 수면의 경우처럼 지각이 대상을 적극적으로 분별하지 않을 때에도 상상력은 계속 기능한다.",
    "감정은 사람이 세상을 왜곡된 방식으로 바라보도록 이끈다.",
    "겁쟁이의 지각적 성향은 두려움을 경험하는 자신의 성향에 영향을 받는다.",
    "사랑에 빠진 사람의 기대는 욕망에 의해 영향을 받는다.",
    "그러한 경우, 지각된 대상과 자신이 보기를 기대하는 것 사이의 약간의 유사성만으로도 지각된 대상을 바로 그것(볼 것을 기대한 것)으로 "
    "오인하게 만들 수 있다.",
    "겁쟁이는 어디에서나 적을 보고, 사랑에 빠진 사람은 어디에서나 욕망의 대상을 바라본다.",
    "감정의 영향을 더 많이 받을수록, ________.",
    "감각의 중추 기관은 보통 유사점과 차이점을 비교함으로써 기능하지만, 감정은 사람이 대상을 부정확하게 분별하도록 이끈다.",
    "감정적 몰입이 더 클수록, 지각은 더 편향된다.",
]


def board(words, fresh=()):
    """단어 지도 — 한 묶음. 묶음 이름은 2문장에 나온 말(Emotions)까지만. 빈칸 보기 말(less similarity)은 쓰지 않는다"""
    return groups("감정이 하는 일", "Emotions (감정)", words, fresh=fresh)


B5 = [("distorted", "왜곡된"), ("misidentification", "잘못 알아봄, 오인")]

SIDE_TIP = tip("같은 쪽? 반대 쪽?", "빈칸 문장에 But, However, not 같은 반전 단서가 있으면 반대 의견이 들어가요. "
               "반전 단서 없이 앞 이야기를 '~할수록 더'로 이어 가면 같은 말이 들어가요.")

BLANK_GLOSSES = [g("The more affected one is", "사람이 더 영향을 받을수록"), g("The more", "더 ~할수록"),
                 g("affected", "영향을 받은"), g("one", "사람")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("Imagination", "상상력"), g("continues to function", "계속 기능하다, 계속 작동하다"),
                    g("function", "기능하다, 작동하다"), g("continues", "계속하다"),
                    g("when perception is not actively discerning objects", "지각이 대상을 적극적으로 분별하지 않을 때"),
                    g("perception", "지각 · 눈·귀 같은 감각으로 알아차리는 것"),
                    g("not actively discerning", "적극적으로 분별하지 않는"), g("actively", "적극적으로"),
                    g("discerning", "분별하는"), g("objects", "대상"),
                    g("in cases of emotion, disease, and sleep", "감정, 질병, 수면의 경우처럼"), g("cases", "경우"),
                    g("emotion", "감정"), g("disease", "질병"), g("sleep", "수면, 잠"), *BLANK_GLOSSES],
        "slashes": ["continues to function", "actively discerning objects,"],
        "roles": [r("Imagination", "S"), r("continues to function", "V"), r("perception", "S"),
                  r("is not actively discerning", "V"), r("objects", "O")],
        "steps": [
            show("s1_passage", "빈칸은 여기, 일곱째 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "아주 짧은 문장이에요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "영향을 받지 않으면, ____하다", False),
                    ("o1", "사람이 더 영향을 받을수록, (더) ____하다", True),
                    ("o2", "영향을 받는 것보다 ____하는 게 낫다", False)],
                   "The more ~, (the) …는 '~할수록 더 …하다'예요. affected는 '영향을 받은'이에요.",
                   why="'The more affected one is'는 '사람이 더 영향을 받을수록'이에요. 빈칸에는 그러면 무엇이 더하거나 덜한지가 와요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0, highlight=["The more", "affected", "________"],
                   tips=[tip("The 비교급 ~, the 비교급 …", "'~할수록 더 …하다'예요. 빈칸 안에도 the more, the less 같은 비교급이 와요.", "The more")]),
            show("s1_where", "그럼 무엇에 영향을 받으면 어떻게 되는지 생각하며 문장 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
            choice("s1_when",
                   "상상력(Imagination)은 언제 계속 작동한대요?",
                   [("o0", "눈으로 대상을 정확히 볼 때만", False),
                    ("o1", "지각이 대상을 적극적으로 분별하지 않을 때", True),
                    ("o2", "아무 감정도 없을 때", False)],
                   "when 뒤를 봐요. perception은 '지각', discerning은 '분별하는'이에요.",
                   why="'when perception is not actively discerning objects', 지각이 대상을 애써 가려 보지 않는 때래요. 감정, 질병, 잠이 그런 경우예요.",
                   highlight=["Imagination", "not actively discerning"]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Emotions", "감정"), g("dispose one", "사람이 ~하도록 이끌다"), g("dispose", "~하도록 이끌다"),
                    g("to see the world", "세상을 보도록"), g("world", "세상"),
                    g("in a distorted way", "왜곡된 방식으로"), g("distorted", "왜곡된, 비뚤어진"), g("way", "방식")],
        "slashes": ["dispose one", "see the world"],
        "roles": [r("Emotions", "S"), r("dispose", "V"), r("one", "O"), r("to see the world in a distorted way", "C")],
        "steps": [
            show("s2_note", "감정은 세상을 비뚤어지게(distorted) 보게 한대요. 이 글이 하려는 말이에요.",
                 highlight=["Emotions", "distorted"], button="다음 문장",
                 tips=[tip("dispose", "이 글에서는 → ~하도록 이끌다  ('처분하다' 아님)", "dispose", trap=True),
                       tip("dispose + 사람 + to ~", "'사람이 ~하도록 이끌다'예요. dispose of(처분하다)와 다른 말이에요.", "dispose one")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("A coward’s perceptual disposition", "겁쟁이의 지각적 성향"), g("coward’s", "겁쟁이의"), g("coward", "겁쟁이"),
                    g("perceptual", "지각의"), g("disposition", "성향, 경향"), g("is affected by", "~에 영향을 받다"),
                    g("is affected", "영향을 받는다"), g("affected by", "~에 영향을 받는"),
                    g("his disposition to experience fear", "두려움을 경험하는 자신의 성향"),
                    g("experience", "경험하다"), g("fear", "두려움")],
        "slashes": ["perceptual disposition", "is affected", "his disposition"],
        "roles": [r("A coward’s perceptual disposition", "S"), r("is affected", "V")],
        "steps": [
            choice("s3_fear",
                   "겁쟁이(coward)가 세상을 보는 방식은 무엇에 영향을 받는대요?",
                   [("o0", "두려움을 느끼는 성향", True), ("o1", "적을 이기고 싶은 욕망", False), ("o2", "잠과 질병", False)],
                   "is affected by 뒤를 봐요. disposition은 '성향'이에요.",
                   why="'is affected by his disposition to experience fear', 겁쟁이는 두려움을 잘 느끼는 성향 때문에 다르게 봐요. 감정이 보는 방식을 바꾸는 예예요.",
                   highlight=["affected by", "fear"],
                   tips=[tip("disposition", "이 글에서는 → 성향, 경향  ('처분, 배치' 아님)", "perceptual disposition", trap=True)]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "low",
        "glosses": [g("A lover’s expectations", "사랑에 빠진 사람의 기대"), g("lover’s", "사랑에 빠진 사람의"),
                    g("expectations", "기대"), g("are affected", "영향을 받는다"), g("by desire", "욕망에 의해"),
                    g("desire", "욕망")],
        "roles": [r("A lover’s expectations", "S"), r("are affected", "V")],
        "steps": [],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("In such cases", "그러한 경우"), g("such", "그러한"), g("a small similarity", "약간의 유사성"),
                    g("small similarity", "약간의 유사성"), g("similarity", "유사성, 비슷함"), g("small", "약간의, 작은"),
                    g("between", "~ 사이의"), g("a perceived object", "지각된(눈에 보인) 대상"), g("perceived", "지각된"),
                    g("the thing one expects to see", "자신이 보기를 기대하는 것"), g("expects", "기대하다"),
                    g("can lead to", "~로 이어질 수 있다"), g("the misidentification", "오인, 잘못 알아봄"),
                    g("misidentification", "오인, 잘못 알아봄"), g("of the perceived object", "지각된 대상을"),
                    g("as that thing", "바로 그것으로")],
        "slashes": ["In such cases,", "a small similarity", "a perceived object", "expects to see", "the misidentification",
                    "the perceived object"],
        "roles": [r("a small similarity", "S"), r("can lead to", "V"), r("the misidentification", "O")],
        "modifiers": ["one expects to see"],
        "steps": [
            choice("s5_meaning",
                   "In such cases(그러한 경우), 무슨 일이 생길 수 있대요?",
                   [("o0", "아주 많이 비슷해야만 대상을 잘못 알아본다", False),
                    ("o1", "조금만 비슷해도 보이는 대상을 기대한 것으로 잘못 알아본다", True),
                    ("o2", "조금 비슷하면 대상을 더 정확히 알아본다", False)],
                   "a small similarity(약간의 유사성)가 주어예요. can lead to 뒤 misidentification은 '잘못 알아봄'이에요.",
                   why="'a small similarity … can lead to the misidentification', 약간만 비슷해도 잘못 알아보게 될 수 있대요. 보이는 대상을 기대한 것(that thing)으로 착각하는 거예요.",
                   highlight=["small similarity", "misidentification"],
                   tips=[tip("misidentification of A as B", "'A를 B로 잘못 알아봄, 오인'이에요. mis-는 '잘못'이라는 뜻이에요.", "misidentification"),
                         tip("lead to ~", "'~로 이어지다, ~을 낳다'예요.", "can lead to")]),
            pick("s5_same", "distorted(왜곡된)와 같은 쪽 말을 이 문장에서 하나 찾아 눌러 볼까요?",
                 ["a small similarity", "a perceived object", "the misidentification"], ["the misidentification"],
                 "그건 왜곡과 같은 쪽 말이 아니에요.",
                 "the misidentification(잘못 알아봄)이에요. 감정이 세상을 비뚤어지게 보게 한다는 말과 같은 쪽이에요.",
                 wrong_by={"a small similarity": "a small similarity는 잘못 알아보게 만드는 계기예요. 그 결과를 찾아봐요.",
                           "a perceived object": "a perceived object는 '지각된 대상', 눈에 보이는 것이에요."}),
            show("s5_board", "감정에 영향을 받으면 조금만 비슷해도 잘못 알아봐요.",
                 panel=board(B5, fresh=("misidentification",)), button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "low",
        "glosses": [g("The coward", "겁쟁이"), g("sees", "보다"), g("the enemy", "적"), g("enemy", "적"),
                    g("the lover", "사랑에 빠진 사람"), g("lover", "사랑에 빠진 사람"),
                    g("the object of desire", "욕망의 대상"), g("everywhere", "어디에서나")],
        "slashes": ["the enemy,"],
        "roles": [r("The coward", "S"), r("sees … sees", "V"), r("the enemy", "O"), r("the lover", "S"), r("the object of desire", "O")],
        "steps": [
            show("s6_note", "겁쟁이는 어디서나 적을, 사랑에 빠진 사람은 어디서나 원하는 대상을 본대요. 3·4문장 예시가 이어진 거예요.",
                 highlight=["everywhere"], button="다음 문장",
                 tips=[tip("while", "여기서는 '~하는 반면'이에요. 두 사람을 나란히 놓고 비교해요.", "while")]),
        ],
    },
    {
        "id": 7, "text": BLANK, "model_translation": KO[6], "teaching_value": "high",
        "glosses": list(BLANK_GLOSSES) + [g("is", "~이다")],
        "roles": [r("one", "S"), r("is", "V")],
        "steps": [
            choice("s7_side",
                   "빈칸은 감정에 더 영향을 받으면 어떻게 되는지예요. 칠판의 말과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 — 더 잘못 알아보는 쪽", True), ("o1", "반대 쪽 — 더 정확히 보는 쪽", False)],
                   "affected(영향을 받은)는 3·4문장에서 감정의 영향이었어요. But이나 not 같은 반전 단서도 없어요.",
                   why="감정은 세상을 비뚤어지게 보게 하고, 조금만 비슷해도 잘못 알아보게 해요. 영향을 더 받을수록 그 일이 더 심해지니 같은 쪽이에요.",
                   highlight=["affected", "________"], panel=board(B5), tips=[SIDE_TIP],
                   point="빈칸 = 감정의 영향을 더 받을수록 → 더 잘못 알아봄 = 칠판 Emotions 쪽 = 같은 쪽"),
            choice("s7_fill",
                   "그럼 빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "차이를 찾을 기회가 더 많아진다", False),
                    ("o1", "세상을 있는 그대로 더 쉽게 본다", False),
                    ("o2", "더 적게 비슷해도 기대한 것으로 보인다", True)],
                   "5문장의 a small similarity(약간의 유사성)를 떠올려 봐요.",
                   why="영향을 받으면 조금만 비슷해도 잘못 알아본다고 했어요. 영향을 더 받을수록 필요한 비슷함은 더 적어져요.",
                   highlight=["The more", "________"]),
            show("s7_next", "빈칸 뒤 두 문장도 같은 이야기를 이어 가요. 확인하며 읽어 봐요.", button="다음 문장"),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("While", "~이지만, ~인 반면"), g("the central organ of sense", "감각의 중추 기관"), g("central", "중추의, 중심의"),
                    g("organ", "기관"), g("sense", "감각"), g("normally", "보통, 평소에"), g("functions", "기능하다, 작동하다"),
                    g("by comparing similarities and differences", "유사점과 차이점을 비교함으로써"), g("comparing", "비교하는 것"),
                    g("similarities", "유사점"), g("differences", "차이점"), g("emotions", "감정"),
                    g("dispose one", "사람이 ~하도록 이끌다"), g("dispose", "~하도록 이끌다"),
                    g("to discern objects inaccurately", "대상을 부정확하게 분별하도록"), g("discern", "분별하다"),
                    g("objects", "대상"), g("inaccurately", "부정확하게")],
        "slashes": ["the central organ of sense", "normally functions", "and differences,", "dispose one"],
        "roles": [r("the central organ of sense", "S"), r("functions", "V"), r("emotions", "S"), r("dispose", "V"),
                  r("one", "O"), r("to discern objects inaccurately", "C")],
        "steps": [
            choice("s8_while",
                   "While 앞뒤를 비교하면 무슨 뜻일까요?",
                   [("o0", "감각 기관도 감정도 대상을 정확히 분별한다", False),
                    ("o1", "감각 기관은 보통 비슷한 점과 다른 점을 비교하지만, 감정은 대상을 부정확하게 분별하게 한다", True),
                    ("o2", "감정이 비슷한 점과 다른 점을 더 잘 비교하게 한다", False)],
                   "While은 여기서 '~이지만, ~인 반면'이에요. inaccurately는 '부정확하게'예요.",
                   why="'normally functions by comparing similarities and differences', 보통은 비슷한 점과 다른 점을 비교해요. 하지만 'emotions dispose one to discern objects inaccurately', 감정은 대상을 부정확하게 분별하게 해요.",
                   highlight=["While", "normally", "inaccurately"],
                   tips=[tip("While (문장 앞)", "문장 앞 While이 두 내용을 맞세우면 '~이지만, ~인 반면'이에요. 시간의 '~하는 동안'이 아니에요.", "While")]),
        ],
    },
    {
        "id": 9, "text": S[8], "model_translation": KO[8], "teaching_value": "high",
        "glosses": [g("The greater", "더 클수록"), g("greater", "더 큰"), g("the emotional investment", "감정적 몰입"),
                    g("emotional", "감정적인"), g("investment", "몰입 · 감정을 쏟는 것"),
                    g("the more biased", "더 편향된"), g("biased", "편향된, 치우친"), g("one’s perception", "사람의 지각")],
        "slashes": ["the emotional investment,"],
        "steps": [
            choice("s9_meaning",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "감정적 몰입이 클수록 지각은 더 치우친다", True),
                    ("o1", "감정을 많이 쏟을수록 더 정확히 본다", False),
                    ("o2", "감정적 몰입이 클수록 지각은 덜 치우친다", False)],
                   "The 비교급 ~, the 비교급 …은 '~할수록 더 …'예요. biased는 '편향된, 치우친'이에요.",
                   why="'The greater the emotional investment, the more biased', 감정적 몰입이 클수록 지각이 더 편향된대요. 빈칸 문장과 같은 모양이에요.",
                   highlight=["The greater", "the more biased"],
                   tips=[tip("investment", "이 글에서는 → (감정의) 몰입  ('투자' 아님)", "investment", trap=True),
                         tip("is가 빠진 비교급", "The greater (is) the investment, the more biased (is) one’s perception — is가 빠진 꼴이에요.",
                             "The greater")]),
            show("s9_go", "빈칸은 감정의 영향 쪽이에요. 5문장의 '조금만 비슷해도 잘못 알아본다'를 다른 말로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 4문장은 짧은 예시라 해석 맞추기만 (모두에게). 2문장도 짧아서 맞추기 — 칭찬 뒤 s2_note
add_match(sentences, 2, [m("Emotions", "감정은"), " 사람이 ", m("in a distorted way", "왜곡된 방식으로"), " ",
                         m("to see the world", "세상을 보도록"), " ", m("dispose one", "이끈다"), "."])
add_match(sentences, 4, [m("A lover’s expectations", "사랑에 빠진 사람의 기대는"), " ", m("by desire", "욕망에 의해"), " ",
                         m("are affected", "영향을 받는다"), "."],
          explain="사랑에 빠진 사람의 기대도 욕망에 영향을 받는대요. 3문장 겁쟁이와 같은 예시예요.")
# 가리키는 말
add_refers(sentences, 3, {"his disposition to experience fear": "his = the coward’s(겁쟁이의)"})
add_refers(sentences, 5, {"In such cases": "감정의 영향을 받는 경우(겁쟁이·사랑에 빠진 사람)", "as that thing": "that thing = the thing one expects to see(보기를 기대하는 것)"})

SENSES = {
    1: [sense("to", "continues to function", "~하는 것을 (계속하다)", "continue to + 동사원형")],
    2: [sense("to", "to see the world", "~하도록", "dispose + 사람 + to부정사 = ~가 …하도록 이끌다")],
    3: [sense("to", "disposition to experience", "~하는 (성향)", "명사 + to부정사 (disposition to ~ = ~하는 성향)")],
    5: [sense("to", "expects to see", "~하기를 (기대하다)", "expect to + 동사원형"),
        sense("to", "lead to", "~로 (이어지다)", "lead to + 명사"),
        sense("as", "as that thing", "~로 (잘못 알아봄)", "misidentification of A as B = A를 B로 오인함"),
        sense("that", "that thing", "그 (것)", "지시형용사 that — 앞의 the thing one expects to see")],
    6: [sense("while", "while the lover", "~하는 반면", "접속사 while (대조)")],
    8: [sense("while", "While the central organ", "~이지만, ~인 반면", "접속사 While (대조)"),
        sense("to", "to discern", "~하도록", "dispose + 사람 + to부정사")],
}

WORDS = {"imagination": "상상력", "continues": "계속하다", "function": "기능하다", "perception": "지각", "actively": "적극적으로",
         "discerning": "분별하는", "objects": "대상", "cases": "경우", "emotion": "감정", "disease": "질병", "sleep": "수면",
         "emotions": "감정", "dispose": "~하도록 이끌다", "see": "보다", "world": "세상", "distorted": "왜곡된", "way": "방식",
         "coward’s": "겁쟁이의", "coward": "겁쟁이", "perceptual": "지각의", "disposition": "성향", "affected": "영향을 받은",
         "experience": "경험하다", "fear": "두려움", "lover’s": "사랑에 빠진 사람의", "lover": "사랑에 빠진 사람",
         "expectations": "기대", "desire": "욕망", "cases,": "경우", "small": "약간의", "similarity": "유사성",
         "perceived": "지각된", "object": "대상", "thing": "것", "expects": "기대하다", "lead": "이어지다",
         "misidentification": "오인", "sees": "보다", "enemy": "적", "everywhere": "어디에서나", "more": "더",
         "central": "중추의", "organ": "기관", "sense": "감각", "normally": "보통", "functions": "기능하다",
         "comparing": "비교하는 것", "similarities": "유사점", "differences": "차이점", "discern": "분별하다",
         "inaccurately": "부정확하게", "greater": "더 큰", "emotional": "감정적인", "investment": "몰입",
         "biased": "편향된", "one’s": "사람의", "one": "사람"}

STORIES = [
    (3, [sc("문장 1~2", "🌫️", "Emotions → a distorted way", "감정은 세상을 왜곡해서 보게 해요"),
         sc("문장 3", "😨", "coward ← fear", "겁쟁이는 두려움 때문에 다르게 봐요")]),
    (6, [sc("문장 4", "💘", "lover ← desire", "사랑에 빠진 사람은 욕망 때문에 다르게 봐요"),
         sc("문장 5~6", "👀", "a small similarity → misidentification", "조금만 비슷해도 기대한 것으로 잘못 봐요 — 어디서나 적, 어디서나 원하는 대상")]),
]

OPTIONS = [
    ("1", "the more chances one gets to find differences", ["find differences"], "차이점을 발견할 기회를 더 많이 얻는다", False),
    ("2", "the less similarity is required for the thing to appear", ["less similarity", "required"],
     "그 대상이 (볼 것을 기대한 것으로) 나타나는 데에 필요한 유사성은 더 적다", True),
    ("3", "the sooner the perceived similarity fades away", ["sooner", "fades away"], "지각된 유사성은 더 빨리 사라진다", False),
    ("4", "the more easily one can sense the world the way it is", ["the way it is"], "사람은 세상을 있는 그대로 더 쉽게 지각할 수 있다", False),
    ("5", "the less slowly different emotions are released", ["less slowly", "released"], "서로 다른 감정들이 덜 느리게 표출된다", False),
]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오. [3점]",
    "underline": "________", "sentence": 7, "analysis_first": True, "wrong_rate": 58.0, "wrong_rank": 7,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("chances", "기회"), g("find differences", "차이점을 발견하다"), g("less similarity", "더 적은 유사성"),
                g("is required", "필요하다"), g("for the thing to appear", "그 대상이 (기대한 것으로) 나타나는 데"),
                g("sooner", "더 빨리"), g("fades away", "사라지다"), g("easily", "쉽게"), g("sense", "지각하다, 느끼다"),
                g("the way it is", "있는 그대로"), g("less slowly", "덜 느리게"), g("released", "표출된, 풀려난")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "감정에 더 영향을 받을수록 어떻게 되는지, 5문장을 떠올리며 골라 봐요.",
        "정답이에요! 감정에 영향을 받으면 조금만 비슷해도 기대한 것으로 잘못 봐요. 영향을 더 받을수록 그렇게 보이는 데 필요한 비슷함은 더 적어져요.",
        "정답은 ②예요. 감정에 영향을 받으면 약간만 비슷해도 잘못 알아본다고 했어요(5문장). 영향을 더 받을수록 필요한 유사성은 더 적어요.",
        {"1": "차이점을 비교하는 건 보통의 감각 기관이 하는 일이에요(8문장). 감정은 오히려 대상을 부정확하게 분별하게 해요.",
         "3": "similarity가 나와서 헷갈렸죠. 하지만 비슷함이 사라진다는 말은 없어요. 조금만 비슷해도 잘못 본다는 게 핵심이에요.",
         "4": "반대 쪽 말이에요. 감정에 영향을 받을수록 세상을 왜곡해서 보고, 지각은 더 편향된다고 했어요.",
         "5": "감정이 표출되는 빠르기는 글에 없어요. 글은 감정이 보는 방식을 바꾼다는 이야기예요."},
        {"4": review(16,
                     "④는 '~할수록 더 쉽게'라는 모양이 빈칸 문장과 잘 맞아 보여요. 하지만 감정은 세상을 왜곡된 방식으로(in a distorted way) 보게 하고, 몰입이 클수록 지각은 더 편향돼요(biased).\n세상을 있는 그대로 보는 건 반대 쪽이에요.",
                     panel=rows(("2문장", "see the world in a distorted way", "세상을 왜곡해서 본다", "hl"),
                                ("9문장", "the more biased one’s perception", "지각이 더 편향된다", "hl"),
                                ("④", "sense the world the way it is", "있는 그대로 본다 — 반대 쪽", "hl2")),
                     rank_word="가장 많이 고른"),
         "1": review(15,
                     "①은 8문장의 similarities and differences가 떠올라 끌려요. 하지만 차이를 비교하는 건 보통 때(normally) 감각 기관이 하는 일이에요.\n감정은 오히려 대상을 부정확하게(inaccurately) 분별하게 해요.",
                     panel=rows(("8문장", "normally … comparing similarities and differences", "보통 때 — 비교한다", "hl2"),
                                ("8문장", "emotions … discern objects inaccurately", "감정 — 부정확하게 분별한다", "hl"))),
         "3": review(15,
                     "③은 similarity(유사성)가 있어서 끌려요. 하지만 글은 비슷함이 사라진다는 게 아니라, 약간만 비슷해도(a small similarity) 잘못 알아본다는 이야기예요.\n영향을 더 받을수록 필요한 비슷함이 줄어들어요.",
                     panel=rows(("5문장", "a small similarity → misidentification", "약간만 비슷해도 잘못 알아봄", "hl"),
                                ("③", "the perceived similarity fades away", "비슷함이 사라진다 — 글에 없음", "hl2")))}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(2·5·9)만 ──
EMPHASIS = {
    2: ["Emotions", "dispose", "distorted"],
    5: ["small similarity", "misidentification"],
    9: ["The greater", "the more biased"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 33번 (빈칸 추론, 3점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 같은 말 모으기 → 빈칸이 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-emotion-perception.svg", ("Emotion", "감정"), "→", ("Perception", "지각"),
                                       "감정은 우리가 보는 것을 어떻게 바꿀까?", "2026년 6월 모의평가 33번 도입 칠판"),
                      "alt": "칠판: Emotion(감정) → Perception(지각)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "무서울 때 그림자가 사람처럼 보인 적 있나요? 이번 글은 감정과 지각(보고 알아차리는 일) 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("imagination", "상상력"), g("perception", "지각"), g("dispose A to B", "A가 B하도록 이끌다"),
                           g("distorted", "왜곡된"), g("coward", "겁쟁이"), g("perceptual", "지각의"), g("disposition", "성향"),
                           g("be affected by", "~에 영향을 받다"), g("desire", "욕망"), g("similarity", "유사성"),
                           g("misidentification", "오인"), g("organ", "기관"), g("inaccurately", "부정확하게"),
                           g("investment", "몰입"), g("biased", "편향된")],
               "options": [g("be required", "필요하다"), g("fade away", "사라지다"), g("release", "표출하다")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함:
# dispose ~하도록 이끌다(s2_note) · disposition 성향(s3_fear) · investment 몰입(s9_meaning) — 스텝 안에 직접 달았다

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법")
