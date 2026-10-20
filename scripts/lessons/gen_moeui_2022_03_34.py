"""2022년 3월 고3 34번 레슨 + 대사를 만든다 (빈칸 추론, 3점). 오답률 53.0% · Top 4.

    py scripts/lessons/gen_moeui_2022_03_34.py   (→ node scripts/policy_copy.mjs stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸 위치 먼저 → 처음부터 읽으며 재진술 모으기 → 빈칸이 같은 쪽/반대 쪽 → 바꿔 쓴 보기.
빈칸이 가운데(다섯째, It is common to ____.). 정답 ② feel social pressure to comply with them.
많이 고른 오답 ③ apply them to create inspirational artworks 16% (painting·artists가 겹치고, Just as 비유를 놓침) — option_review로.
열쇠: Just as 화가들이 그 시대 양식에 순응하듯(conform to) 우리도 사회 관습에 순응한다(similarly conform to) → 칠판 화가 = 우리.
같은 말: conform to · prevailing social conventions · unwritten rules · dominant conventions · accepted with little questioning ·
trapped in the perspective of our own time. 빈칸은 주장과 같은 쪽(common + 바로 뒤 문장이 「거의 의문 없이 받아들임」).
perspective는 1문장 '원근법', 8문장 '관점' — 해설지 번역대로 8문장에서 뜻 3지.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
mortgage는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt) — conform to = 순응하다, prevailing = 지배적인,
aspiration = 염원, much as = ~처럼, be trapped in = ~에 갇혀 있다.
6문장 끝 much as Vermeer … accepted의 S·V는 끊어읽기 roles에 넣지 않았다 — accepted가 관계절(have accepted)에 먼저 나와
표시가 엉뚱한 자리에 붙는다.
반영한 규칙: 2026-10-20 끊어읽기(slashes·roles·modifiers)까지. 초급 기본(add_basic)은 짧은 문장(4·8)만.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic,  # noqa: E402
                      topic_svg, base_lesson, exam_brief, review, finish)

ID = "moeui-2022-03-34-social-conventions"

BLANK = "It is common to ________."
S = [
    "The history of perspective in Western painting matters because of what it reveals for the art of living.",
    "Just as most artists conform to the stylistic conventions of the era into which they are born, we similarly conform to "
    "prevailing social conventions about how to live.",
    "These unwritten rules typically include getting married and having children, owning your own home and having a mortgage, "
    "having a regular job and commuting to work, and flying abroad for holidays.",
    "For some people these are realities, for others they remain aspirations.",
    BLANK,
    "At this point in Western history, they are amongst the dominant conventions that most of us have accepted with little "
    "questioning, much as Vermeer and other Dutch baroque painters of the seventeenth century accepted linear perspective without question.",
    "It is difficult to see beyond the limitations of the culture that has shaped our ways of looking at the world and at ourselves.",
    "We are trapped in the perspective of our own time.",
]
KO = [
    "서양화에서 원근법의 역사는 그것이 삶의 기술에 대해 드러내는 것 때문에 중요하다.",
    "대부분 예술가가 자신이 태어나는 시대의 양식적 관습에 순응하듯이, 우리도 어떻게 살아야 하는지에 대한 지배적인 사회적 관습에 비슷하게 순응한다.",
    "이러한 불문율에는 일반적으로 결혼해서 아이를 갖는 것, 자기 집을 소유하고 담보 대출을 받는 것, 일정한 직업을 갖고 통근하는 것, 휴가를 위해 비행기로 해외에 가는 것이 포함된다.",
    "어떤 사람들에게는 이것이 현실이고, 다른 사람들에게는 염원으로 남는다.",
    "________은 일반적이다.",
    "17세기 Vermeer와 다른 네덜란드 바로크 화가들이 선형 원근법을 문제없이 받아들였던 것처럼, 서구 역사의 현시점에서, 그것은 우리 대부분이 거의 의문 없이 받아들여 온 지배적인 관습 중 하나이다.",
    "세상과 자신을 바라보는 우리의 방식을 형성해 온 문화의 한계 그 너머를 보기는 어렵다.",
    "우리는 우리 시대의 관점에 갇혀 있다.",
]

ART = "왼쪽 · 화가들"
US = "오른쪽 · 우리"


def board(left, right, fresh=(), sort=None):
    """칠판 — 왼쪽 화가들, 오른쪽 우리 (Just as A, B similarly — 같은 모양). 묶음 이름은 2문장에서 나온 말까지만"""
    return groups("화가들 = 우리", "화가들 (artists)", left, "우리 (we)", right, fresh=fresh, between="=",
                  sort={"words": sort, "left": ART, "right": US} if sort else None)


L2 = [("conform to stylistic conventions", "그 시대 양식을 따른다")]
R2 = [("conform to social conventions", "사회 관습을 따른다")]
R3 = R2 + [("unwritten rules", "불문율 — 결혼·내 집·직장·해외여행")]
L6 = L2 + [("accepted linear perspective without question", "원근법을 의문 없이 받아들였다")]
R6 = R3 + [("accepted with little questioning", "거의 의문 없이 받아들였다")]
R8 = R6 + [("trapped in the perspective of our own time", "우리 시대의 관점에 갇혀 있다")]

BLANK_GLOSSES = [g("It is common to", "~하는 것은 흔하다")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("The history of perspective", "원근법의 역사"), g("perspective", "원근법 · 관점"),
                    g("in Western painting", "서양 그림에서"), g("matters", "중요하다"), g("because of", "~ 때문에"),
                    g("what it reveals", "그것이 드러내는 것"), g("for the art of living", "삶의 기술에 대해"),
                    *BLANK_GLOSSES, g("common", "흔한")],
        "slashes": ["in Western painting", "matters", "it reveals"],
        "roles": [r("The history", "S"), r("matters", "V")],
        "steps": [
            show("s1_passage", "빈칸은 여기, 다섯째 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "아주 짧은 문장이에요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "____하는 것은 드문 일이다", False),
                    ("o1", "____하는 것은 흔한(많은 사람이 하는) 일이다", True),
                    ("o2", "____하는 것은 어려운 일이다", False)],
                   "common은 '흔한, 보통의'예요. It은 뒤의 to 이하를 받는 말이에요.",
                   why="It은 뒤의 to ____를 받아요. common은 '흔한'이라, 많은 사람이 ____한다는 말이에요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0, highlight=["common", "________"],
                   tips=[tip("It is ~ to …", "it은 뒤의 to …를 대신 받는 말(가주어)이에요. It is common to ~ = ~하는 것은 흔하다.", "It is common to")]),
            show("s1_where", "그럼 사람들이 흔히 무엇을 한다는 건지 생각하며 문장 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
            choice("s1_matters",
                   "여기서 matters는 무슨 뜻일까요?",
                   [("o0", "문제가 된다", False), ("o1", "중요하다", True), ("o2", "물질이다", False)],
                   "matter는 명사로 '문제, 물질'이지만, 주어 뒤 동사 자리에 오면 뜻이 달라요.",
                   why="The history … matters에서 matters는 동사예요. 동사 matter는 '중요한 의미가 있다'는 뜻이에요.",
                   highlight=["matters"], levels=["중", "초"],
                   tips=[tip("matter (동사)", "명사로는 '문제, 물질'이지만 동사로는 '중요하다'예요. It doesn't matter = 상관없다.", "matters")]),
            show("s1_art", "원근법 그림의 역사가 '삶의 기술'에 대해 무언가를 보여 준대요. 그림 이야기가 삶 이야기로 이어져요.",
                 highlight=["perspective", "the art of living"], button="다음 문장"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Just as", "~하듯이"), g("most artists", "대부분의 화가"), g("conform to", "~에 따르다, 순응하다"),
                    g("the stylistic conventions", "양식의 관습(그림 그리는 방식의 관례)"), g("of the era", "그 시대의"),
                    g("into which they are born", "그들이 태어나는"), g("we", "우리는"),
                    g("similarly conform to", "비슷하게 ~에 순응한다"), g("prevailing social conventions", "널리 퍼진(지배적인) 사회 관습"),
                    g("about how to live", "어떻게 살지에 대한"), g("conventions", "관습, 관례"), g("prevailing", "지배적인, 널리 퍼진")],
        "slashes": ["Just as most artists conform", "stylistic conventions", "of the era", "they are born,", "we similarly conform",
                    "social conventions"],
        "roles": [r("most artists", "S"), r("conform to", "V"), r("we", "S"), r("similarly conform to", "V")],
        "modifiers": ["into which they are born"],
        "steps": [
            sv("s2_sv", ["most artists", "the stylistic conventions", "we", "similarly conform to", "prevailing social conventions"],
               {"we": "S", "similarly conform to": "V", "prevailing social conventions": "전목"},
               {"most artists": "그건 Just as(~하듯이) 덩어리 안의 주어예요. 콤마 뒤 메인 문장에서 찾아봐요.",
                "the stylistic conventions": "그건 Just as 덩어리 안의 말이에요."},
               "주어 we, 동사 (similarly) conform to, 전치사 뒤 목적어는 prevailing social conventions예요.",
               ask="콤마 뒤 메인 문장에서 주어(S), 동사(V), 전치사 뒤 목적어(전목)를 찾아볼까요?"),
            choice("s2_same",
                   "Just as(~하듯이)로 화가와 우리를 나란히 놓았어요. 우리는 무엇에 순응한대요?",
                   [("o0", "그 시대 화가들의 그림 양식", False),
                    ("o1", "어떻게 살지에 대한 널리 퍼진 사회 관습", True),
                    ("o2", "스스로 정한 삶의 규칙", False)],
                   "conform to는 '~에 따르다, 순응하다'예요. 콤마 뒤 we similarly conform to 다음을 봐요.",
                   why="'we similarly conform to prevailing social conventions about how to live', 화가가 시대 양식을 따르듯 우리도 사회 관습을 따른대요.",
                   highlight=["Just as", "conform to", "similarly", "social conventions"],
                   tips=[tip("Just as A, (so) B", "'A하듯이 B도 그렇다'예요. 앞 A는 비유, 진짜 하고 싶은 말은 뒤 B예요.", "Just as"),
                         tip("conform to", "'~에 따르다, 순응하다'예요. 정해진 틀에 맞춰 산다는 말이에요.", "similarly conform to")]),
            show("s2_board", "화가 이야기는 비유예요. 칠판에 화가와 우리를 나란히 적어 둘게요.",
                 panel=board(L2, R2, fresh=("conform to stylistic conventions", "conform to social conventions")), button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("These unwritten rules", "이런 불문율(글로 적지 않은 규칙)"), g("unwritten", "글로 적지 않은"),
                    g("typically", "보통, 일반적으로"), g("include", "포함한다"), g("getting married", "결혼하는 것"),
                    g("having children", "아이를 갖는 것"), g("owning your own home", "자기 집을 갖는 것"), g("your own home", "자기 집"),
                    g("having a mortgage", "담보 대출을 받는 것"), g("mortgage", "담보 대출"), g("a regular job", "일정한 직업"),
                    g("having a regular job", "일정한 직업을 갖는 것"), g("commuting to work", "직장에 통근하는 것"),
                    g("flying abroad for holidays", "휴가 때 비행기로 해외에 가는 것")],
        "slashes": ["These unwritten rules", "typically include", "having children,", "having a mortgage,", "commuting to work,"],
        "roles": [r("These unwritten rules", "S"), r("include", "V")],
        "steps": [
            sv("s3_sv", ["These unwritten rules", "include", "your own home", "a regular job"],
               {"These unwritten rules": "S", "include": "V"},
               {"your own home": "그건 owning(갖는 것)의 대상이에요. 목록 안의 말이에요.",
                "a regular job": "그건 having(갖는 것)의 대상이에요. 목록 안의 말이에요."},
               "주어 These unwritten rules, 동사 include예요. 그 뒤 -ing 목록 전체가 목적어예요.",
               ask="주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s3_these",
                   "These unwritten rules(이런 불문율)는 앞 문장의 무엇을 다시 말한 걸까요?",
                   [("o0", "the stylistic conventions (화가들의 양식)", False),
                    ("o1", "prevailing social conventions (널리 퍼진 사회 관습)", True),
                    ("o2", "the art of living (삶의 기술)", False)],
                   "These(이런)가 가리키는 건 앞 문장에서 찾아요. 뒤의 예가 결혼·집·직장이에요.",
                   why="결혼·내 집·직장·해외여행은 어떻게 살지에 대한 규칙이에요. 앞 문장의 사회 관습을 These unwritten rules로 다시 말했어요.",
                   highlight=["These unwritten rules"]),
            show("s3_board", "사회 관습 = 불문율이에요. 결혼, 내 집, 직장, 해외여행 같은 거래요.",
                 panel=board(L2, R3, fresh=("unwritten rules",)), button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "low",
        "glosses": [g("For some people", "어떤 사람들에게는"), g("these are realities", "이것들이 현실이다"), g("realities", "현실"),
                    g("for others", "다른 사람들에게는"), g("they remain aspirations", "그것들은 바람(염원)으로 남는다"),
                    g("aspirations", "열망, 염원")],
        "slashes": ["For some people", "are realities,"],
        "roles": [r("these", "S"), r("are", "V"), r("realities", "C"), r("they", "S"), r("remain", "V"), r("aspirations", "C")],
        "steps": [
            show("s4_dream", "어떤 사람에겐 이미 현실, 다른 사람에겐 바라는 것(aspirations)이래요. 어느 쪽이든 이 규칙을 목표로 삼아요.",
                 highlight=["realities", "aspirations"], button="다음 문장",
                 tips=[tip("for some …, for others …", "'어떤 사람들에게는 ~, 다른 사람들에게는 ~'예요.", "for others")]),
        ],
    },
    {
        "id": 5, "text": BLANK, "model_translation": KO[4], "teaching_value": "high",
        "glosses": list(BLANK_GLOSSES) + [g("common", "흔한")],
        "roles": [r("It", "S"), r("is", "V"), r("common", "C")],
        "steps": [
            choice("s5_side",
                   "빈칸은 사람들이 이 규칙들에 대해 흔히 하는 일이에요. 앞에서 말한 우리 모습과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 — 규칙을 따르는 쪽", True), ("o1", "반대 쪽 — 규칙에서 벗어나는 쪽", False)],
                   "common(흔한)이라고 했어요. 칠판 오른쪽에서 우리가 사회 관습을 어떻게 한다고 했는지 봐요.",
                   why="우리 대부분은 사회 관습에 순응한대요(conform to). 많은 사람이 흔히 하는 일이니 같은 쪽이에요.",
                   highlight=["common"], panel=board(L2, R3)),
            show("s5_next", "빈칸 바로 뒤 문장이 이 규칙들 이야기를 이어 가요. 확인하며 읽어 봐요.", button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("At this point", "지금 시점에"), g("in Western history", "서양 역사에서"), g("they", "그것들(불문율)은"),
                    g("are", "~이다"), g("amongst", "~ 중에 (= among)"), g("the dominant conventions", "지배적인 관습"),
                    g("dominant", "지배적인"), g("that most of us have accepted", "우리 대부분이 받아들여 온"),
                    g("most of us", "우리 대부분"), g("with little questioning", "거의 의문 없이"),
                    g("much as", "~와 마찬가지로, ~처럼"), g("Vermeer", "페르메이르 · 17세기 네덜란드 화가"),
                    g("and other Dutch baroque painters", "그리고 다른 네덜란드 바로크 화가들"),
                    g("of the seventeenth century", "17세기의"), g("accepted", "받아들였다"),
                    g("linear perspective", "선 원근법"), g("without question", "의문 없이")],
        "slashes": ["At this point", "Western history,", "the dominant conventions", "little questioning,", "much as Vermeer",
                    "the seventeenth century", "linear perspective"],
        "roles": [r("they", "S"), r("are", "V")],
        "modifiers": ["that most of us have accepted with little questioning"],
        "steps": [
            sv("s6_sv", ["At this point", "they", "are", "the dominant conventions", "most of us"],
               {"they": "S", "are": "V"},
               {"At this point": "그건 '지금 시점에'라는 때를 말해 주는 덩어리예요.",
                "the dominant conventions": "그건 amongst(~ 중에) 뒤 덩어리예요.",
                "most of us": "그건 that 뒤, the dominant conventions를 꾸미는 덩어리 안의 주어예요."},
               "주어 they(그 불문율들), 동사 are예요. that 뒤가 the dominant conventions를 꾸며요.",
               ask="주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s6_accept",
                   "우리 대부분은 이 관습들을 어떻게 받아들였대요?",
                   [("o0", "오랫동안 따져 본 뒤에", False), ("o1", "거의 의문 없이", True), ("o2", "억지로 마지못해", False)],
                   "with little questioning을 봐요. little은 '거의 없는'이에요.",
                   why="'accepted with little questioning', 거의 따져 보지 않고 받아들였대요. 화가들이 원근법을 의문 없이 받아들인 것처럼요.",
                   highlight=["accepted", "little questioning", "without question"],
                   tips=[tip("much as ~", "'~와 마찬가지로, ~처럼'이에요. 뒤에 비교하는 예가 와요.", "much as"),
                         tip("little + 명사", "a 없이 little이면 '거의 없는'이에요. with little questioning = 거의 의문 없이.", "little questioning")]),
            show("s6_board", "화가도 우리도 의문 없이 받아들였어요. 칠판 양쪽에 붙여 둘게요.",
                 panel=board(L6, R6, fresh=("accepted linear perspective without question", "accepted with little questioning")),
                 button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("It", "그것 (뒤의 to ~를 받음)"), g("is", "~이다"), g("difficult", "어려운"), g("to see beyond", "~ 너머를 보는 것"),
                    g("the limitations", "한계"), g("of the culture", "문화의"), g("the culture", "문화"),
                    g("that has shaped", "~을 만들어 온"), g("our ways of looking", "우리가 보는 방식"),
                    g("at the world and at ourselves", "세상과 우리 자신을")],
        "slashes": ["It is difficult", "to see beyond", "of the culture", "our ways of looking"],
        "roles": [r("It", "S"), r("is", "V"), r("difficult", "C")],
        "modifiers": ["that has shaped our ways of looking at the world and at ourselves"],
        "steps": [
            sv("s7_sv", ["It", "is", "difficult", "the limitations", "the culture"],
               {"It": "S", "is": "V", "difficult": "C"},
               {"the limitations": "그건 to see beyond(~ 너머를 보는 것) 뒤의 말이에요.", "the culture": "그건 of 뒤 덩어리예요."},
               "주어 It, 동사 is, 보어 difficult예요. It은 뒤의 to see beyond ~를 받아요.",
               ask="주어(S), 동사(V), 보어(C)를 찾아볼까요?"),
            show("s7_culture", "우리를 만든 문화의 한계 너머를 보기는 어렵대요. 문화가 우리가 세상과 자신을 보는 방식을 만들었으니까요.",
                 highlight=["difficult", "see beyond", "the limitations"], button="다음 문장"),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("We", "우리는"), g("are trapped in", "~에 갇혀 있다"), g("the perspective", "관점"),
                    g("of our own time", "우리 시대의"), g("perspective", "관점 · 1문장에서는 '원근법'")],
        "roles": [r("We", "S"), r("are trapped", "V")],
        "steps": [
            choice("s8_persp",
                   "perspective는 첫 문장에서 '원근법'이었어요. 여기서는 무슨 뜻일까요?",
                   [("o0", "관점, 세상을 보는 방식", True), ("o1", "원근법 그림", False), ("o2", "시대의 역사", False)],
                   "앞 문장의 our ways of looking at the world(세상을 보는 방식)를 떠올려 봐요.",
                   why="여기서 perspective는 '관점'이에요. 우리는 우리 시대의 관점에 갇혀 있대요.",
                   highlight=["trapped", "perspective"],
                   tips=[tip("perspective", "그림에선 '원근법', 생각에선 '관점'이에요. 이 글은 두 뜻을 겹쳐 썼어요.", "perspective"),
                         tip("be trapped in ~", "'~에 갇혀 있다'예요.", "are trapped in")]),
            show("s8_board", "우리는 우리 시대의 관점에 갇혀 있대요. 칠판 오른쪽에 붙일게요.",
                 panel=board(L6, R8, fresh=("trapped in the perspective of our own time",))),
            choice("s8_what",
                   "빈칸 문장으로 돌아가요. 칠판을 보면, 사람들은 이 규칙들에 대해 흔히 어떻다는 말이 와야 할까요?",
                   [("o0", "규칙을 깨려고 애쓴다", False), ("o1", "규칙을 따라야 한다고 느낀다", True),
                    ("o2", "규칙을 잘 모른다", False)],
                   "칠판 오른쪽의 conform to, accepted with little questioning을 봐요.",
                   why="우리는 사회 관습에 순응하고, 거의 의문 없이 받아들였대요. 빈칸도 그 말이에요.",
                   display=BLANK, tag="빈칸 문장", highlight=["common", "________"], panel=board(L6, R8)),
            show("s8_go", "같은 쪽이에요. 칠판 오른쪽 말(conform to, accepted)을 다른 말로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요", panel=board(L6, R8)),
        ],
    },
]

add_basic(sentences, 4, [m("For some people", "어떤 사람들에게는"), " ", m("these are realities", "이것들이 현실이고"), ", ",
                         m("for others", "다른 사람들에게는"), " ", m("they remain aspirations", "바람으로 남는다"), "."],
          sv_new=sv_step("s4_basic_sv", ["these", "are", "realities", "they", "remain"],
                         {"these": "S", "are": "V", "realities": "C"},
                         {"they": "그건 콤마 뒤 두 번째 문장의 주어예요. 먼저 앞 문장을 봐요.",
                          "remain": "그건 콤마 뒤 두 번째 문장의 동사예요."},
                         "앞 문장은 주어 these, 동사 are, 보어 realities예요. 뒤 문장도 they / remain / aspirations로 같은 모양이에요."),
          meaning_ids=["s4_dream"])
add_basic(sentences, 8, [m("We", "우리는"), " ", m("the perspective", "관점"), " ", m("of our own time", "우리 시대의"), "에 ",
                         m("are trapped in", "갇혀 있다"), "."],
          sv_new=sv_step("s8_basic_sv", ["We", "are trapped", "the perspective"],
                         {"We": "S", "are trapped": "V"},
                         {"the perspective": "그건 in 뒤 덩어리예요."},
                         "주어 We, 동사 are trapped예요. in 뒤가 갇힌 곳이에요."),
          meaning_after="s8_persp")

SENSES = {
    1: [sense("for", "for the art of living", "~에 대해", "전치사 for (대상)")],
    2: [sense("as", "Just as", "~하듯이", "Just as A, B (비유·같은 모양)"),
        sense("to", "conform to the stylistic", "~에 (따르다)", "conform to + 명사"),
        sense("which", "into which", "(그 시대) 안으로", "전치사 + 관계대명사 which (the era를 꾸밈)"),
        sense("to", "similarly conform to", "~에 (순응하다)", "conform to + 명사"),
        sense("to", "how to live", "~해야 할지", "how + to부정사")],
    3: [sense("to", "commuting to work", "~로 (통근하다)", "전치사 to (방향)"),
        sense("for", "for holidays", "~을 위해, ~ 때", "전치사 for (목적)")],
    4: [sense("for", "For some people", "~에게는", "전치사 for (대상)"),
        sense("for", "for others", "~에게는", "전치사 for (대상)")],
    5: [sense("to", "common to", "~하는 것은", "가주어 it … 진주어 to부정사")],
    6: [sense("that", "conventions that most of us", "(앞 명사를 꾸밈)", "관계대명사 that + 주어 + 동사"),
        sense("as", "much as", "~와 마찬가지로", "much as + 주어 + 동사")],
    7: [sense("to", "to see beyond", "~하는 것은", "가주어 it … 진주어 to부정사"),
        sense("that", "culture that has shaped", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
}

WORDS = {"history": "역사", "perspective": "원근법, 관점", "western": "서양의", "painting": "그림", "matters": "중요하다",
         "reveals": "드러내다", "art": "기술, 예술", "living": "삶, 사는 것", "artists": "화가, 예술가", "conform": "따르다, 순응하다",
         "stylistic": "양식의", "conventions": "관습, 관례", "era": "시대", "born": "태어난", "similarly": "비슷하게",
         "prevailing": "지배적인", "social": "사회의", "live": "살다", "unwritten": "글로 적지 않은", "rules": "규칙",
         "typically": "보통", "include": "포함하다", "getting": "~하게 되는 것", "married": "결혼한", "having": "가지는 것",
         "children": "아이들", "owning": "소유하는 것", "home": "집", "mortgage": "담보 대출", "regular": "일정한", "job": "직업",
         "commuting": "통근하는 것", "work": "직장", "flying": "비행기로 가는 것", "abroad": "해외로", "holidays": "휴가",
         "realities": "현실", "remain": "남다", "aspirations": "열망, 염원", "common": "흔한", "point": "시점",
         "amongst": "~ 중에", "dominant": "지배적인", "accepted": "받아들였다", "little": "거의 없는", "questioning": "의문, 따져 묻기",
         "vermeer": "페르메이르", "dutch": "네덜란드의", "baroque": "바로크 양식의", "painters": "화가들", "seventeenth": "17번째의",
         "century": "세기", "linear": "선의, 선형의", "question": "의문", "difficult": "어려운", "see": "보다", "beyond": "~ 너머",
         "limitations": "한계", "culture": "문화", "shaped": "만들었다", "ways": "방식", "looking": "보는 것", "ourselves": "우리 자신",
         "trapped": "갇힌", "own": "자기 자신의", "time": "시대", "most": "대부분의", "some": "어떤", "people": "사람들"}

STORIES = [
    (3, [sc("문장 1~2", "🖼️", "artists conform = we conform", "화가가 그 시대 양식을 따르듯, 우리도 사회 관습을 따라요"),
         sc("문장 3", "💍", "unwritten rules", "결혼·내 집·직장·해외여행 같은 불문율")]),
    (6, [sc("문장 4~5", "🎯", "realities · aspirations · It is common to ____", "누구에겐 현실, 누구에겐 바람 — 흔히 ____해요"),
         sc("문장 6", "🤐", "accepted with little questioning", "우리 대부분은 거의 의문 없이 받아들였어요")]),
]

OPTIONS = [
    ("1", "distinguish them from ideas and wishes", ["distinguish", "ideas and wishes"], "그것을 생각 및 바람과 구분하는", False),
    ("2", "feel social pressure to comply with them", ["social pressure", "comply with"], "그것에 순응해야 한다는 사회적 압박을 느끼는", True),
    ("3", "apply them to create inspirational artworks", ["apply", "inspirational artworks"], "영감을 주는 예술품을 만들기 위해 그것을 적용하는", False),
    ("4", "ignore them on account of their complexity", ["ignore", "complexity"], "그것의 복잡성 때문에 그것을 무시하는", False),
    ("5", "have an objection to being controlled by them", ["objection", "being controlled"], "그것에 의해 통제되는 것을 거부하는", False),
]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오. [3점]",
    "underline": "________", "sentence": 5, "analysis_first": True, "wrong_rate": 53.0, "wrong_rank": 4,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("distinguish", "구분하다"), g("ideas and wishes", "생각과 바람"), g("social pressure", "사회적 압박"),
                g("comply with", "~에 따르다, 순응하다"), g("apply", "적용하다"), g("inspirational artworks", "영감을 주는 예술품"),
                g("ignore", "무시하다"), g("on account of", "~ 때문에"), g("complexity", "복잡성"), g("objection", "반대, 거부"),
                g("being controlled", "통제되는 것")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "빈칸은 우리가 사회 규칙(them)에 대해 흔히 하는 일이에요. 칠판 오른쪽 말을 떠올리며 골라 봐요.",
        "정답이에요! 우리는 사회 관습에 순응하고(conform to) 의문 없이 받아들여요. 그걸 '순응해야 한다는 압박을 느낀다'로 바꿔 썼어요.",
        "정답은 ②예요. comply with는 conform to와 같은 말이에요. 우리는 사회 관습을 따르고 거의 의문 없이 받아들인다고 했어요.",
        {"1": "aspirations(바람)가 나와서 헷갈렸죠. 하지만 규칙을 생각·바람과 구분한다는 말은 글에 없어요.",
         "3": "painting·artists가 나와서 헷갈렸죠. 그림은 우리를 설명하려고 든 비유예요. 빈칸은 우리가 사회 규칙에 대해 하는 일이에요.",
         "4": "복잡해서 무시한다는 말은 없어요. 오히려 거의 의문 없이 받아들인다고 했어요.",
         "5": "반대쪽 말이에요. 우리는 규칙을 거부하지 않고 받아들인다고 했어요."},
        {"3": review(16,
                     "③에는 artworks(예술품)가 있어서 그림 이야기와 겹쳐 보여요. 하지만 화가는 우리를 설명하려고 든 비유예요(Just as ~, we similarly). 빈칸은 우리가 사회 규칙(them)에 대해 흔히 하는 일이고, 우리는 그 규칙을 따른다고 했어요.",
                     "그래서 ③이 아니에요. 어디서 헷갈렸어요?",
                     [("그림 이야기와 겹쳐서 골랐어요", ["word_overlap"],
                       "알려 줘서 고마워요. 겹치는 단어보다 빈칸이 누구에 대한 말인지를 봐야 해요. 앞으로 이 점을 강조해서 알려 줄게요."),
                      ("Just as 비유를 못 봤어요", ["analogy"],
                       "알려 줘서 고마워요. Just as A, B에서 A는 비유, 하고 싶은 말은 B예요. 앞으로 비유를 같이 짚어 줄게요."),
                      ("둘 다요", ["word_overlap", "analogy"], "알려 줘서 고마워요. 앞으로 겹치는 단어와 비유를 같이 짚어 줄게요.")],
                     panel=rows(("화가 (비유)", "conform to the stylistic conventions", "그 시대 양식을 따른다", "hl2"),
                                ("우리 (빈칸)", "conform to prevailing social conventions", "사회 관습을 따른다", "hl")))}),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 34번 (빈칸 추론, 3점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 두 쪽 말 모으기 → 빈칸이 어느 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-social-conventions.svg", ("Painters", "화가들"), "=", ("Us", "우리"),
                                       "화가와 우리는 무엇이 닮았을까?", "2022년 3월 34번 도입 칠판"),
                      "alt": "칠판: Painters(화가들) = Us(우리)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "한 시대의 화가들은 비슷한 방식으로 그림을 그렸어요. 이번 글은 그림 이야기로 우리가 사는 방식을 말해요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("perspective", "원근법, 관점"), g("matter", "중요하다"), g("reveal", "드러내다"), g("conform to", "~에 순응하다"),
                           g("stylistic", "양식의"), g("convention", "관습"), g("era", "시대"), g("prevailing", "지배적인"),
                           g("unwritten", "글로 적지 않은"), g("commute", "통근하다"), g("aspiration", "열망, 염원"),
                           g("dominant", "지배적인"), g("much as", "~와 마찬가지로"), g("linear", "선의, 선형의"),
                           g("limitation", "한계"), g("be trapped in", "~에 갇혀 있다")],
               "options": [g("distinguish", "구분하다"), g("comply with", "~에 따르다"), g("inspirational", "영감을 주는"),
                           g("on account of", "~ 때문에"), g("complexity", "복잡성"), g("objection", "반대")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법",
       chunks={"most artists": "대부분의 화가", "the stylistic conventions": "양식의 관습", "we": "우리는",
               "similarly conform to": "비슷하게 ~에 순응한다", "prevailing social conventions": "널리 퍼진 사회 관습",
               "These unwritten rules": "이런 불문율", "include": "포함한다", "your own home": "자기 집", "a regular job": "일정한 직업",
               "At this point": "지금 시점에", "they": "그것들은", "are": "~이다", "the dominant conventions": "지배적인 관습",
               "most of us": "우리 대부분", "It": "그것", "is": "~이다", "difficult": "어려운", "the limitations": "한계",
               "the culture": "문화", "We": "우리는", "are trapped": "갇혀 있다", "the perspective": "관점",
               "these": "이것들은", "realities": "현실", "remain": "남는다",
               "For some people": "어떤 사람들에게는", "these are realities": "이것들이 현실이다", "for others": "다른 사람들에게는",
               "they remain aspirations": "그것들은 바람으로 남는다", "of our own time": "우리 시대의", "are trapped in": "~에 갇혀 있다"})
