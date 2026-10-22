"""2026년 6월 모의평가(2027학년도, 평가원) 영어 34번 레슨 + 대사를 만든다 (빈칸 추론, 3점). 오답률 76%(메가스터디) · Top 1.

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_34.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸이 마지막 문장(33번 꼴). 정답 ① he can predict where art is going.
선택률(메가스터디): ① 24 ② 24 ③ 27 ④ 8 ⑤ 16 — 많이 고른 오답 ③ the art work tells the story of his time 27%, ② the artist … reliable 24%.
열쇠: 3문장 his belief in the future presence of the work as a significant point attained by art as a whole
= 빈칸 문장 the conviction that ____ (not only A but B의 B). 그 사이 4·5문장은 반대 쪽(역사는 알 수 없고 지금의 합의는 바뀐다)이라
courageously(용기 있게)가 붙는다. 칠판: his belief(수집가의 믿음) ↔ shifting(변하는 가치) — 묶음 이름은 1·3문장에 나온 말.
시험지 아래 *풀이 단어: consensus, aesthetic — 핵심어·단어 체크에서 뺐다(뜻만 단다).
해설지(content/tutor/exam-source/2027-06-평가원/해설.txt 34번) 해석과 대조함 — uppermost 가장 우선적인, acquire 소장하다,
beyond 제외하면, that is 다시 말해, check 수표, attain 달성하다, merit 가치, validation 확인, all but 거의, displace 대체하다,
in the last analysis 결국, commit oneself to 헌신하다, affirm 확언하다, derive 유래하다, conviction 확신.
오답률·선택률은 메가스터디 풀서비스 채점 기준(wrong_rate_source).
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음). Claude 초안 — 선생님 검토 전.

선생님이 확인할 점
1. 「같은 쪽? 반대 쪽?」(s7_side)을 「글쓴이 주장」이 아니라 「칠판 어느 쪽(수집가의 믿음 / 변하는 가치)」으로 물었다.
   글쓴이는 가치가 변한다고 말하면서도, 빈칸은 수집가가 그래도 용기 있게(courageously) 지키는 믿음이라서.
2. 빈칸 앞에서 빈칸 내용을 3지로 미리 묻는 s7_fill의 정답 보기를 「자기가 고른 작품이 앞으로 미술 전체에서 중요한 지점이 될 것이다」
   (3문장 재진술)로 했다. 정답 ①(미술이 어디로 갈지 예측)과 한 번 더 바꿔 써야 이어지게 — 너무 쉬우면 빼도 된다.
3. ③을 가장 많이 고른 이유는 추측이다(art history·present-day가 「그 시대 이야기」로 보여서). ②는 「작품/작가를 믿는다」로 읽어서.
4. 4문장 —at best— 는 대시 두 개 사이지만 「기껏해야」가 뜻을 정하는 말이라 흐리지 않았다. 2문장 괄호(beyond …)는 흐렸다.
5. 7문장 끊어읽기 roles에 from whatever source it be derived 안의 S·V(it be derived)를 넣지 않았다 — it이 앞(Through it)에 먼저 나와
   표시가 엉뚱한 자리에 붙는다.
6. 헷갈리는 단어(trap): work(작품) · class(부류) · check(수표) · In the last analysis(결국). all but(거의)은 5문장에서 뜻을 3지로
   묻기 때문에(s5_allbut) trap·Tip으로 두지 않았다(읽는 화면에서 답이 샌다). 엑셀(함정단어.xlsx)에는 안 넣었다.
7. 해석 맞추기는 6문장(짧은 문장) 하나만. 칠판 정리(story)는 2·5문장 뒤 두 번.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-06-34-art-collector"

BLANK = ("Through it he courageously affirms not only his aesthetic judgment, from whatever source it be derived, "
         "but the conviction that ________.")
S = [
    "The dependent and shifting nature of art values, not only on the market but inherently, is uppermost in the mind of "
    "today’s art collector, whether he buys for himself or as the representative of an institution.",
    "Acquiring a work is acquiring a piece of art history, or it is acquiring nothing (beyond, that is, an object of personal "
    "enjoyment in the same class as a cat or a souvenir).",
    "In signing his check the collector asserts his belief in the future presence of the work as a significant point attained "
    "by art as a whole.",
    "History, however, is open to anything and the merit of the chosen painting or sculpture has —at best— only the validation "
    "of a present-day consensus.",
    "This consensus is all but certain to be displaced, as others have been in the past.",
    "In the last analysis, committing himself to a painting is the collector’s own act.",
    BLANK,
]
# 해설지 해석 (2027-06-평가원/해설.txt 34번)
KO = [
    "미술 작품의 가치가 단지 시장에서뿐만 아니라 본질적으로 의존적이며 가변적이라는 속성은, 오늘날의 미술 수집가가 자신을 위해 구매하든 "
    "한 기관의 대표자로서 구매하든 스스로의 마음 속에 가장 우선적으로 자리하고 있다.",
    "작품을 소장하는 것은 미술사의 한 부분을 소장하는 것이거나, (다시 말해, 고양이나 기념품과 같은 부류의 개인적 즐거움의 대상을 제외하면) "
    "아무것도 소장하지 않는 것이다.",
    "수표에 서명함으로써, 수집가는 미술 전체에 의해 달성된 하나의 중요한 지점으로서 그 작품이 미래에도 존재할 것이라는 자신의 믿음을 단언한다.",
    "하지만 역사는 어느 것에나 열려 있고, 선택된 그림이나 조각의 가치는 기껏해야 현재의 합의에 의한 확인에 불과하다.",
    "이러한 합의는, 과거에 다른 합의들이 그래왔듯이, 대체될 것이 거의 확실하다.",
    "결국, 그림 한 작품에 헌신하는 것은 수집가 자신의 행위이다.",
    "이러한 행위를 통해 그는, 그것(자신의 미학적 판단)이 어떤 근원으로부터 유래되었든, 자신의 미학적 판단뿐만 아니라 "
    "________라는 확신 또한 용기 있게 확언한다.",
]

LEFT = "왼쪽 · his belief (수집가의 믿음)"
RIGHT = "오른쪽 · shifting (변하는 가치)"


def board(left, right, fresh=(), sort=None):
    """단어 지도 — 묶음 이름은 1·3문장에 나온 말(his belief / shifting)까지만. 빈칸 보기 말(predict, where art is going)은 쓰지 않는다"""
    return groups("수집가의 믿음 ↔ 변하는 가치", "his belief (수집가의 믿음)", left, "shifting (변하는 가치)", right,
                  fresh=fresh, between="↔", sort={"words": sort, "left": LEFT, "right": RIGHT} if sort else None)


L3 = [("future presence", "미래에도 남아 있음"), ("a significant point", "중요한 지점")]
R1 = [("dependent and shifting", "달라지고 변하는")]
R4 = R1 + [("open to anything", "무엇에든 열려 있다")]
R5 = R4 + [("a present-day consensus", "지금의 합의일 뿐"), ("be displaced", "대체된다")]

SIDE_TIP = tip("같은 쪽? 반대 쪽?", "빈칸 문장에 But, However, not 같은 반전 단서가 있으면 반대 의견이 들어가요. "
               "앞에서 말한 생각을 다른 말(belief → conviction)로 받으면 같은 말이 들어가요.")

BLANK_GLOSSES = [g("Through it", "그것(그림 한 점에 헌신하는 행위)을 통해"), g("courageously", "용기 있게"),
                 g("affirms", "확언하다, 분명히 말하다"), g("not only", "~뿐 아니라"),
                 g("his aesthetic judgment", "자신의 미학적 판단"), g("aesthetic", "미학의"), g("judgment", "판단"),
                 g("from whatever source it be derived", "그것이 어떤 근원에서 유래했든"),
                 g("the conviction", "확신"), g("conviction", "확신"), g("but the conviction that", "~라는 확신도")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("The dependent and shifting nature", "의존적이며 가변적인 속성"), g("dependent", "의존적인 · 여기서는 '무언가에 따라 달라지는'"),
                    g("shifting", "가변적인, 변하는"), g("nature", "속성, 본질"), g("of art values", "미술 작품 가치의"),
                    g("art values", "미술 작품의 가치"), g("not only on the market but inherently", "시장에서뿐만 아니라 본질적으로"),
                    g("market", "시장"), g("inherently", "본질적으로"), g("is uppermost", "가장 우선적이다"),
                    g("uppermost", "가장 우선적인, 맨 위의"), g("in the mind of", "~의 마음속에서"),
                    g("today’s art collector", "오늘날의 미술 수집가"), g("collector", "수집가"),
                    g("whether he buys for himself", "자신을 위해 사든"), g("buys", "사다, 구매하다"),
                    g("as the representative of an institution", "한 기관의 대표자로서"), g("representative", "대표자"),
                    g("institution", "기관"), *BLANK_GLOSSES],
        "slashes": ["of art values,", "but inherently,", "is uppermost", "art collector,", "buys for himself"],
        "roles": [r("The dependent and shifting nature of art values", "S"), r("is", "V"), r("uppermost", "C"),
                  r("he", "S"), r("buys", "V")],
        "steps": [
            show("s1_passage", "빈칸은 마지막 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "그는 자기 미적 판단을 버리고 ____라는 확신만 갖는다", False),
                    ("o1", "그는 자기 미적 판단뿐 아니라 ____라는 확신도 용기 있게 확언한다", True),
                    ("o2", "그는 ____라는 확신이 없어서 미적 판단을 숨긴다", False)],
                   "not only A but B는 'A뿐 아니라 B도'예요. affirms는 '확언하다, 분명히 말하다'예요.",
                   why="'not only his aesthetic judgment … but the conviction', 미적 판단뿐 아니라 확신도래요. 콤마 사이 흐린 부분은 빼고 읽어요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["affirms", "not only", "the conviction", "________"],
                   faded=["from whatever source it be derived,"],
                   tips=[tip("not only A but B", "'A뿐 아니라 B도'예요. 더 중요한 말은 뒤의 B 쪽에 와요.", "not only")]),
            show("s1_where", "그럼 그(he)가 무엇을 확신하는지 생각하며 문장 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
            choice("s1_meaning",
                   "주어가 아주 길어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "작품 가치는 시장에서 정해지니, 수집가는 값을 가장 먼저 본다", False),
                    ("o1", "작품 가치는 늘 그대로라서, 수집가는 안심하고 산다", False),
                    ("o2", "작품 가치가 무언가에 따라 달라지고 변한다는 점을 오늘날 수집가는 가장 먼저 생각한다", True)],
                   "is 앞까지가 주어예요. shifting은 '변하는', uppermost는 '가장 우선적인'이에요.",
                   why="'The dependent and shifting nature of art values', 작품 가치가 달라지고 변한다는 성질이 주어예요. 그게 수집가 마음에 가장 우선(uppermost)이래요.",
                   highlight=["shifting", "uppermost"], faded=["not only on the market but inherently,"],
                   tips=[tip("uppermost", "'가장 우선적인, 맨 위의'예요. be uppermost in the mind = 마음속에 가장 먼저 자리하다.", "uppermost"),
                         tip("whether A or B", "'A든 B든'이에요. 자신을 위해 사든, 기관 대표로서 사든.", "whether he buys")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "medium",
        "glosses": [g("Acquiring a work", "작품을 소장하는 것"), g("Acquiring", "소장하는 것"), g("acquiring", "소장하는 것"),
                    g("work", "작품"), g("is", "~이다"), g("a piece of art history", "미술사의 한 부분"),
                    g("art history", "미술사"), g("it", "그것"), g("nothing", "아무것도 ~ 않음"),
                    g("acquiring nothing", "아무것도 소장하지 않는 것"), g("beyond", "~을 제외하면"), g("that is", "다시 말해, 즉"),
                    g("an object of personal enjoyment", "개인적 즐거움의 대상"), g("personal enjoyment", "개인적 즐거움"),
                    g("in the same class as", "~와 같은 부류의"), g("class", "부류, 종류"),
                    g("a cat or a souvenir", "고양이나 기념품"), g("souvenir", "기념품")],
        "slashes": ["Acquiring a work", "art history,", "acquiring nothing", "that is,", "personal enjoyment"],
        "roles": [r("Acquiring a work", "S"), r("is … is", "V"), r("acquiring a piece of art history", "C"), r("it", "S"),
                  r("acquiring nothing", "C")],
        "steps": [
            choice("s2_two",
                   "작품을 산다는 건 둘 중 하나래요. 무엇과 무엇일까요?",
                   [("o0", "미술사의 한 부분을 사는 것, 아니면 아무것도 사지 않는 것", True),
                    ("o1", "비싼 물건을 사는 것, 아니면 싼 물건을 사는 것", False),
                    ("o2", "작가의 이름을 사는 것, 아니면 그림을 사는 것", False)],
                   "A, or it is B는 'A이거나, 아니면 B'예요. 괄호 안은 빼고 읽어도 돼요.",
                   why="'acquiring a piece of art history, or it is acquiring nothing', 미술사의 한 부분을 소장하거나 아무것도 소장하지 않는 거래요.",
                   highlight=["a piece of art history", "nothing"],
                   faded=["(beyond, that is, an object of personal enjoyment in the same class as a cat or a souvenir)"],
                   tips=[tip("that is", "콤마 사이 that is는 '즉, 다시 말해'예요.", "that is,"),
                         tip("beyond", "여기서는 '~을 제외하면'이에요. 고양이나 기념품 같은 개인적 즐거움을 빼면 아무것도 아니래요.", "beyond")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("In signing his check", "수표에 서명할 때"), g("signing", "서명하는 것"), g("check", "수표"),
                    g("the collector", "수집가"), g("asserts", "단언하다, 분명히 말하다"), g("his belief", "자신의 믿음"),
                    g("belief", "믿음"), g("in the future presence", "미래에도 존재함에 대한"),
                    g("future presence", "미래에도 존재함, 남아 있음"), g("presence", "존재, 있음"), g("of the work", "그 작품의"),
                    g("a significant point", "하나의 중요한 지점"), g("significant point", "중요한 지점"),
                    g("significant", "중요한"), g("point", "지점"), g("attained by art", "미술에 의해 달성된"),
                    g("attained", "달성된, 이룬"), g("as a whole", "전체로서")],
        "slashes": ["In signing his check", "asserts his belief", "of the work", "a significant point", "by art"],
        "roles": [r("the collector", "S"), r("asserts", "V"), r("his belief", "O")],
        "modifiers": ["attained by art as a whole"],
        "steps": [
            choice("s3_belief",
                   "수표에 서명하며 수집가는 무엇을 믿는다고 할까요?",
                   [("o0", "이 작품 값이 곧 오를 것이다", False),
                    ("o1", "이 작품이 앞으로도 미술 전체가 이룬 중요한 지점으로 남을 것이다", True),
                    ("o2", "이 작품을 만든 작가는 믿을 만하다", False)],
                   "his belief in 뒤를 봐요. future presence는 '미래에도 남아 있음'이에요.",
                   why="'his belief in the future presence of the work', 작품이 미래에도 남는다는 믿음이에요. 'a significant point attained by art as a whole', 미술 전체가 이룬 중요한 지점으로서래요.",
                   highlight=["belief", "future presence", "significant point"],
                   tips=[tip("as a whole", "'전체로서'예요. art as a whole = 미술 전체.", "as a whole"),
                         tip("attained by ~", "'~에 의해 달성된'이에요. 앞의 a significant point를 꾸며요.", "attained")]),
            show("s3_board", "수집가는 작품이 미래에도(future) 남을 거라고 믿어요. 그런데 1문장에서 작품 가치는 변한다(shifting)고 했어요.",
                 panel=board(L3, R1, fresh=("future presence", "a significant point", "dependent and shifting")),
                 button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("History", "역사"), g("however", "하지만"), g("is open to anything", "무엇에든 열려 있다"),
                    g("open to anything", "무엇에든 열려 있는"), g("open", "열려 있는"), g("anything", "무엇이든"),
                    g("the merit", "가치"), g("merit", "가치"), g("of the chosen painting or sculpture", "선택된 그림이나 조각의"),
                    g("chosen", "선택된"), g("painting", "그림"), g("sculpture", "조각"), g("has", "가지다"),
                    g("at best", "기껏해야"), g("only", "~뿐"), g("the validation", "확인, 인정"), g("validation", "확인, 인정"),
                    g("of a present-day consensus", "현재의 합의에 의한"), g("present-day consensus", "현재의 합의"),
                    g("present-day", "현재의, 오늘날의"), g("consensus", "합의")],
        "slashes": ["History, however,", "open to anything", "or sculpture", "—at best—", "only the validation"],
        "roles": [r("History", "S"), r("is", "V"), r("open to anything", "C"),
                  r("the merit of the chosen painting or sculpture", "S"), r("has", "V"),
                  r("only the validation of a present-day consensus", "O")],
        "steps": [
            choice("s4_however",
                   "however(하지만)가 있어요. 수집가의 믿음과 비교하면 이 문장은 어떤 말일까요?",
                   [("o0", "역사가 수집가의 믿음을 확실히 지켜 준다", False),
                    ("o1", "작품 가치는 이미 역사가 정해 두었다", False),
                    ("o2", "역사는 어떻게 될지 모르고, 작품 가치도 기껏해야 지금의 합의일 뿐이다", True)],
                   "open to anything은 '무엇에든 열려 있다'예요. at best는 '기껏해야'예요.",
                   why="'History … is open to anything', 역사는 어떻게 될지 몰라요. 'only the validation of a present-day consensus', 작품 가치도 지금 사람들의 합의로 확인된 것뿐이래요.",
                   highlight=["however", "open to anything", "only", "present-day consensus"],
                   tips=[tip("at best", "'기껏해야, 잘해야'예요. at best only ~ = 기껏해야 ~일 뿐.", "at best")]),
            choice("s4_sort",
                   "'open to anything(무엇에든 열려 있다)'는 칠판 어느 쪽일까요?",
                   [("o0", LEFT, False), ("o1", RIGHT, True)],
                   "무엇에든 열려 있으면 앞날을 장담할 수 없어요.",
                   why="역사가 무엇에든 열려 있으면 작품이 미래에도 남는다고 장담할 수 없어요. 변하는 가치 쪽이에요.",
                   panel=board(L3, R1, sort=["open to anything"]), highlight=["open to anything"]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("This consensus", "이러한 합의"), g("consensus", "합의"), g("is", "~이다"),
                    g("all but certain", "거의 확실한"), g("all but", "거의"), g("certain", "확실한"),
                    g("to be displaced", "대체될"), g("displaced", "대체된"), g("have been", "그래 왔다"),
                    g("others", "다른 것들(다른 합의들)"), g("in the past", "과거에"), g("past", "과거")],
        "slashes": ["all but certain", "to be displaced,", "have been"],
        "roles": [r("This consensus", "S"), r("is", "V"), r("all but certain", "C"), r("others", "S"), r("have been", "V")],
        "steps": [
            choice("s5_allbut",
                   "all but certain은 무슨 뜻일까요?",
                   [("o0", "확실한 것 빼고 전부", False), ("o1", "거의 확실한", True), ("o2", "전혀 확실하지 않은", False)],
                   "all but + 형용사는 한 덩어리 표현이에요. '~ 빼고 전부'로 읽으면 뜻이 꼬여요.",
                   why="all but은 형용사 앞에서 '거의'예요. 지금의 합의도 과거의 다른 합의들처럼 거의 확실히 대체된대요.",
                   highlight=["all but certain", "displaced"]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("In the last analysis", "결국"), g("analysis", "분석"),
                    g("committing himself to a painting", "그림 한 점에 헌신하는 것"),
                    g("committing himself to", "~에 헌신하는 것"), g("committing", "헌신하는 것, 맡기는 것"),
                    g("a painting", "그림 한 점"), g("is", "~이다"), g("the collector’s own act", "수집가 자신의 행위"),
                    g("own", "자기 자신의"), g("act", "행위")],
        "slashes": ["In the last analysis,", "to a painting"],
        "roles": [r("committing himself to a painting", "S"), r("is", "V"), r("the collector’s own act", "C")],
        "steps": [
            show("s6_own", "가치가 바뀔지 모르니, 그림을 사는 건 결국 수집가가 스스로 정하고 책임지는 일이래요.",
                 highlight=["own act"], button="다음 문장",
                 tips=[tip("commit oneself to ~", "'~에 헌신하다, 전념하다'예요. 여기서는 그림 한 점을 골라 사기로 마음을 정하는 거예요.",
                           "committing himself")]),
        ],
    },
    {
        "id": 7, "text": BLANK, "model_translation": KO[6], "teaching_value": "high",
        "glosses": list(BLANK_GLOSSES),
        "slashes": ["Through it", "courageously affirms", "aesthetic judgment,", "it be derived,", "the conviction"],
        "roles": [r("he", "S"), r("affirms", "V"), r("his aesthetic judgment", "O"), r("the conviction", "O")],
        "steps": [
            choice("s7_side",
                   "빈칸은 수집가의 확신(the conviction)이에요. 칠판 어느 쪽과 같은 쪽일까요?",
                   [("o0", LEFT, True), ("o1", RIGHT, False)],
                   "3문장에서 수집가가 무엇을 믿는다고(belief) 했는지 떠올려 봐요.",
                   why="conviction(확신)은 3문장의 belief(믿음)를 다른 말로 받은 거예요. courageously(용기 있게)는 가치가 변해도 그 믿음을 지킨다는 뜻이에요.",
                   highlight=["courageously", "the conviction"], faded=["from whatever source it be derived,"],
                   panel=board(L3, R5), tips=[SIDE_TIP],
                   point="빈칸 = the conviction = 3문장 his belief(작품이 미래에도 중요한 지점으로 남는다) = 왼쪽, 같은 쪽"),
            choice("s7_fill",
                   "그럼 빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "지금 사람들의 평가가 앞으로도 그대로일 것이다", False),
                    ("o1", "자기가 고른 작품이 앞으로 미술 전체에서 중요한 지점이 될 것이다", True),
                    ("o2", "작품이 곧 큰돈을 벌어 줄 것이다", False)],
                   "칠판 왼쪽, 3문장의 future presence와 a significant point를 봐요.",
                   why="수집가는 작품이 미래에도 미술 전체가 이룬 중요한 지점으로 남는다고 믿어요. 지금의 합의는 바뀐다고 했고, 돈 이야기는 없어요.",
                   highlight=["the conviction", "________"]),
            show("s7_go", "빈칸은 수집가의 믿음 쪽이에요. 3문장의 믿음을 다른 말로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — 짧은 6문장만. 덩어리는 문장에 그대로 있는 구절
add_match(sentences, 6, [m("In the last analysis", "결국"), ", ", m("committing himself to a painting", "그림 한 점에 헌신하는 것은"), " ",
                         m("the collector’s own act", "수집가 자신의 행위"), m("is", "이다"), "."])
# 가리키는 말
add_refers(sentences, 2, {"it": "acquiring a work(작품을 소장하는 것)"})
add_refers(sentences, 5, {"This consensus": "a present-day consensus(현재의 합의)", "others": "other consensuses(과거의 다른 합의들)"})
add_refers(sentences, 7, {"Through it": "it = committing himself to a painting(그림 한 점에 헌신하는 것)"})

SENSES = {
    1: [sense("but", "not only on the market but inherently", "~뿐 아니라 (본질적으로도)", "not only A but (also) B"),
        sense("for", "for himself", "~을 위해", "전치사 for (목적·대상)"),
        sense("as", "as the representative", "~로서", "전치사 as (자격)")],
    2: [sense("that", "that is,", "즉, 다시 말해", "삽입 that is"),
        sense("as", "the same class as", "~와 같은", "the same A as B = B와 같은 A")],
    3: [sense("as", "as a significant point", "~로서", "전치사 as (자격)"),
        sense("as", "as a whole", "전체로서", "as a whole = 전체로서")],
    4: [sense("to", "open to anything", "~에 (열려 있다)", "be open to + 명사")],
    5: [sense("but", "all but certain", "거의", "all but + 형용사 = 거의 ~한"),
        sense("to", "to be displaced", "~될 (것이 확실한)", "be certain to + 동사원형"),
        sense("as", "as others have been", "~처럼, ~듯이", "접속사 as (같은 방식)")],
    6: [sense("to", "committing himself to", "~에 (헌신하다)", "commit oneself to + 명사")],
    7: [sense("but", "but the conviction", "~도 (B도)", "not only A but B"),
        sense("that", "the conviction that", "~라는 (확신)", "동격 that — the conviction의 내용")],
}

WORDS = {"dependent": "의존적인", "shifting": "가변적인", "nature": "속성", "art": "미술", "values": "가치",
         "market": "시장", "inherently": "본질적으로", "uppermost": "가장 우선적인", "mind": "마음", "today’s": "오늘날의",
         "collector": "수집가", "buys": "사다", "himself": "그 자신", "representative": "대표자", "institution": "기관",
         "acquiring": "소장하는 것", "work": "작품", "piece": "부분, 한 점", "history": "역사", "nothing": "아무것도 ~ 않음",
         "beyond": "~을 제외하면", "object": "대상", "personal": "개인적인", "enjoyment": "즐거움", "class": "부류",
         "cat": "고양이", "souvenir": "기념품", "signing": "서명하는 것", "check": "수표", "asserts": "단언하다",
         "belief": "믿음", "future": "미래의", "presence": "존재", "significant": "중요한", "point": "지점",
         "attained": "달성된", "whole": "전체", "open": "열려 있는", "anything": "무엇이든", "merit": "가치",
         "chosen": "선택된", "painting": "그림", "sculpture": "조각", "best": "최선 · at best = 기껏해야",
         "validation": "확인", "present-day": "현재의", "consensus": "합의", "certain": "확실한", "displaced": "대체된",
         "others": "다른 것들", "past": "과거", "last": "마지막의", "analysis": "분석", "committing": "헌신하는 것",
         "act": "행위", "courageously": "용기 있게", "affirms": "확언하다", "aesthetic": "미학의", "judgment": "판단",
         "whatever": "어떤 ~이든", "source": "근원", "derived": "유래된", "conviction": "확신", "history,": "역사",
         "enjoyment,": "즐거움", "collector’s": "수집가의"}

STORIES = [
    (2, [sc("문장 1", "🔄", "dependent and shifting art values", "작품 가치는 달라지고 변해요 — 수집가가 가장 먼저 생각하는 것"),
         sc("문장 2", "🖼️", "a piece of art history, or nothing", "작품을 사는 건 미술사의 한 부분을 사거나, 아무것도 아닌 것")]),
    (5, [sc("문장 3", "✍️", "belief in the future presence", "수표에 서명하며 작품이 미래에도 중요하게 남는다고 믿어요"),
         sc("문장 4~5", "🌀", "open to anything · all but certain to be displaced", "하지만 역사는 알 수 없고, 지금의 합의는 거의 확실히 바뀌어요")]),
]

OPTIONS = [
    ("1", "he can predict where art is going", ["predict", "where art is going"], "스스로 미술이 나아갈 방향을 예측할 수 있다", True),
    ("2", "the artist behind the work is reliable", ["artist", "reliable"], "그 작품 이면의 미술가는 신뢰할 수 있다", False),
    ("3", "the art work tells the story of his time", ["story of his time"], "그 미술 작품이 자신의 시대의 이야기를 말해 준다", False),
    ("4", "his choice will lead to immediate profits", ["immediate profits"], "자신의 선택이 즉각적인 이익을 초래할 것이다", False),
    ("5", "the originality of the work is unshakable", ["originality", "unshakable"], "그 작품의 독창성은 흔들리지 않는다", False),
]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오. [3점]",
    "underline": "________", "sentence": 7, "analysis_first": True, "wrong_rate": 76.0, "wrong_rank": 1,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("predict", "예측하다"), g("where art is going", "미술이 나아가는 방향"), g("artist", "미술가, 예술가"),
                g("behind the work", "작품 이면의"), g("reliable", "신뢰할 수 있는"), g("tells the story of his time", "자신의 시대 이야기를 말해 주다"),
                g("lead to", "~을 초래하다"), g("immediate profits", "즉각적인 이익"), g("originality", "독창성"),
                g("unshakable", "흔들리지 않는")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "칠판 왼쪽, 3문장에서 수집가가 믿은 것을 떠올리며 골라 봐요.",
        "정답이에요! 수집가는 작품이 미래에도 미술 전체가 이룬 중요한 지점으로 남는다고 믿어요. 그 믿음을 '미술이 어디로 갈지 예측할 수 있다'로 바꿔 썼어요.",
        "정답은 ①이에요. 가치가 변해도 수집가는 작품이 앞으로 미술에서 중요한 지점이 될 거라고 믿고 사요. 미술이 나아갈 방향을 내다본다는 확신이에요.",
        {"2": "글에 작가(artist) 이야기는 나오지 않아요. 수집가가 믿는 건 작품이 앞으로 미술에서 차지할 자리예요.",
         "3": "art history, present-day가 나와서 헷갈렸죠. 하지만 수집가의 믿음은 지금 시대가 아니라 미래(future)를 향해요.",
         "4": "즉각적인(immediate) 이익 이야기는 없어요. 수집가는 먼 미래의 미술을 보고 사요.",
         "5": "가치는 변하고 지금의 합의는 바뀐다고 했어요. 흔들리지 않는다는 말은 글과 반대예요."},
        {"3": review(27,
                     "③은 art history(미술사), present-day(현재의)와 겹쳐 보여서 끌려요. 하지만 수집가가 믿는 건 지금 시대 이야기가 아니라, 작품이 미래에도(future) 중요한 지점으로 남는다는 거예요.\n지금의 합의(present-day consensus)는 오히려 바뀐다고 했어요.",
                     panel=rows(("3문장", "belief in the future presence of the work", "작품이 미래에도 남는다는 믿음", "hl"),
                                ("4·5문장", "a present-day consensus … displaced", "지금의 합의는 바뀐다", "hl2")),
                     rank_word="가장 많이 고른"),
         "2": review(24,
                     "②는 무언가를 믿는다는 말이라 끌려요. 하지만 글에 작가(artist)는 한 번도 나오지 않아요.\n수집가가 믿는 건 작품이 앞으로 미술 전체에서 차지할 자리예요.",
                     panel=rows(("3문장", "a significant point attained by art as a whole", "미술 전체가 이룬 중요한 지점", "hl"),
                                ("②", "the artist behind the work", "글에 없는 말", "hl2")))}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(3·4·7)만 ──
EMPHASIS = {
    3: ["belief", "future presence", "significant point"],
    4: ["however", "open to anything"],
    7: ["not only", "the conviction"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 34번 (빈칸 추론, 3점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 두 쪽 말 모으기 → 빈칸이 어느 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-art-collector.svg", ("Art Collector", "미술 수집가"), "+", ("Art Values", "작품 가치"),
                                       "그림을 산다는 건 무엇을 사는 걸까?", "2026년 6월 모의평가 34번 도입 칠판"),
                      "alt": "칠판: Art Collector(미술 수집가) + Art Values(작품 가치)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "비싼 그림을 사는 사람은 무엇을 믿고 살까요? 이번 글은 미술 수집가와 작품 가치 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 위치를 살펴보고 가면 좋아요. 빈칸은 글쓴이 의견과 동일할 수도 있고, 반대일 수도 있어요."}}],
    exam=exam,
    key_words={"passage": [g("dependent", "의존적인"), g("shifting", "가변적인"), g("inherently", "본질적으로"),
                           g("uppermost", "가장 우선적인"), g("representative", "대표자"), g("institution", "기관"),
                           g("acquire", "소장하다"), g("souvenir", "기념품"), g("assert", "단언하다"), g("attain", "달성하다, 이루다"),
                           g("as a whole", "전체로서"), g("merit", "가치"), g("validation", "확인"), g("at best", "기껏해야"),
                           g("all but", "거의"), g("displace", "대체하다"), g("in the last analysis", "결국"),
                           g("commit oneself to", "~에 헌신하다"), g("courageously", "용기 있게"), g("affirm", "확언하다"),
                           g("derive", "유래하다"), g("conviction", "확신")],
               "options": [g("predict", "예측하다"), g("reliable", "신뢰할 수 있는"), g("immediate", "즉각적인"),
                           g("profit", "이익"), g("originality", "독창성"), g("unshakable", "흔들리지 않는")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함:
# work 작품 · class 부류 · check 수표 · In the last analysis 결국.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    2: [tip("work", "이 글에서는 → 작품  ('일' 아님)", "a work", trap=True),
        tip("class", "이 글에서는 → 부류, 종류  ('수업, 반' 아님)", "class", trap=True)],
    3: [tip("check", "이 글에서는 → 수표  ('확인' 아님)", "check", trap=True)],
    6: [tip("In the last analysis", "이 글에서는 → 결국  ('마지막 분석' 아님)", "In the last analysis", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법")
