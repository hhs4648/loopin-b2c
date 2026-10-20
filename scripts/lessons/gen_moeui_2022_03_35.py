"""2022년 3월 고3 35번 레슨 + 대사를 만든다 (흐름과 무관한 문장, 2점). 오답률 36.0% · Top 12.

    py scripts/lessons/gen_moeui_2022_03_35.py   (→ node scripts/policy_copy.mjs stamp <id> → npm run build)

틀: 무관한 문장 — 2024년 3월 35번(Claude 초안)과 같게. 푸는 법: 첫 문장(번호 없는 문장)으로 글의 방향 잡기
(처음 음악 수업은 악기 없이) → ①~⑤를 칠판 두 칸(악기 없이 시작 / 다른 이야기)에 나누기 → 다른 쪽 한 문장.
②의 instrument는 목소리를 악기에 빗댄 말 — 같은 단어여도 방향을 본다. 정답 ③(악기의 음질 = 악기 자체 이야기).
많이 고른 오답 ④ 16%(몸의 움직임 — 악기 말이 없어 엉뚱해 보이지만 ①의 body percussion과 이어진다), ② 11%(instrument라는 말).
둘 다 option_review로.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
instigate·coordination은 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt). Claude 초안(2026-10-20) — 선생님 검토 전.
반영한 규칙: 끊어읽기 S·V·O·C + [ ] 수식어(2026-10-20), 긴 문장 S·V 모두(2026-10-16), 5형식 보어까지, 꾸밈 구조 표, 초급 기본(add_basic).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)

ID = "moeui-2022-03-35-music-without-instruments"

S = [
    "When approaching practical music making for the first time in the classroom, it is a good idea to avoid using instruments altogether.",
    "①This will allow an inexperienced teacher to focus on the development of fundamental musical behaviour through listening, performing and "
    "composing; and allow the children to focus on the more controllable sound sources i.e. voices and body percussion (clapping, clicking, stamping etc).",
    "②Music starts with these both developmentally and historically: the most expressive and immediate musical instrument is the human voice.",
    "③The sound quality of an instrument is a direct result of the quality of the materials, design, and making.",
    "④Body movements are not only an instinctive response to music but also instigate music making.",
    "⑤Activities which develop many of the coordination skills, aural sensitivity, responses to visual cues and symbols, and the musical "
    "understanding necessary to play an instrument can all be established without instruments.",
]
KO = [
    "처음으로 교실에서 실제 음악을 만들어 내는 일에 접근할 때, 악기 사용을 완전히 피하는 것이 좋은 생각이다.",
    "이렇게 하면 경험이 많지 않은 교사는 듣기와 연주하기 그리고 작곡하기를 통해 기본적인 음악 행위 발달에 집중할 수 있고, 아이들은 더 통제 가능한 음원, "
    "즉 목소리와 몸을 두드려 내는 소리(손뼉 치기, 딸깍딸깍 소리를 내기, 발 구르기 등)에 집중할 수 있을 것이다.",
    "음악은 (아동의) 발달 측면에서뿐만 아니라 역사적으로도 이것들로 시작하는데, 가장 표현이 풍부하고 즉각 쓸 수 있는 악기는 인간의 목소리이다.",
    "악기의 음질은 재료, 디자인, 그리고 제작의 품질로 인한 직접적인 결과이다.",
    "몸의 움직임은 음악에 대한 본능적인 반응일 뿐만 아니라 음악을 만들어 내도록 부추긴다.",
    "조정 능력, 청각적 감수성, 시각적 신호와 기호에 대한 반응, 그리고 악기 연주에 필요한 음악적 이해의 많은 부분을 발달시키는 활동은 모두 악기 없이 자리 잡을 수 있다.",
]

LEFT = "왼쪽 · 악기 없이 시작"
RIGHT = "오른쪽 · 다른 이야기"


def board(left, right=(), fresh=(), sort=None):
    # 묶음 이름은 첫 문장에서 나온 방향까지만 — 오른쪽은 「다른 이야기」로만 둔다
    return groups("첫 음악 수업", "악기 없이 시작", list(left), "다른 이야기", list(right), fresh=fresh, between="↔",
                  sort={"words": sort, "left": LEFT, "right": RIGHT} if sort else None)


L_SO_FAR = {"①": [], "②": ["voices · body percussion"], "③": ["voices · body percussion", "the human voice"],
            "④": ["voices · body percussion", "the human voice"], "⑤": ["voices · body percussion", "the human voice", "body movements"]}
R_SO_FAR = {"①": [], "②": [], "③": [], "④": ["sound quality of an instrument"], "⑤": ["sound quality of an instrument"]}


def sort_step(id, n, word, right_side, why, highlight, **extra):
    return choice(id, f"{n} 문장은 칠판 어느 쪽일까요?",
                  [("o0", LEFT, not right_side), ("o1", RIGHT, right_side)], why, why=why,
                  panel=board(L_SO_FAR[n], R_SO_FAR[n], sort=[word]), highlight=highlight, **extra)


MOD = ("which develop many of the coordination skills, aural sensitivity, responses to visual cues and symbols, "
       "and the musical understanding necessary to play an instrument")

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("When approaching", "~에 다가갈(시작할) 때"), g("practical music making", "실제로 음악을 만드는 일"),
                    g("for the first time", "처음으로"), g("in the classroom", "교실에서"), g("it", "그것 · 뒤의 to avoid …를 대신 받는 말"),
                    g("is", "~이다"), g("a good idea", "좋은 생각"), g("to avoid using instruments altogether", "악기 사용을 완전히 피하는 것"),
                    g("altogether", "완전히, 아예")],
        "slashes": ["When approaching", "practical music making", "for the first time", "in the classroom,", "a good idea"],
        "roles": [r("it", "S"), r("is", "V"), r("a good idea", "C")],
        "modifiers": ["When approaching practical music making for the first time in the classroom"],
        "steps": [
            sv("s1_sv", ["practical music making", "it", "is", "a good idea", "instruments"],
               {"it": "S", "is": "V", "a good idea": "C"},
               {"practical music making": "그건 When approaching(~에 다가갈 때) 뒤의 말이에요. 문장 앞 덧붙인 덩어리예요.",
                "instruments": "그건 to avoid using 뒤의 말이에요."},
               "주어는 it, 동사는 is, 보어는 a good idea예요. it은 뒤의 to avoid …를 대신 받아요.",
               tips=[tip("무관한 문장 요령", "번호 없는 첫 문장으로 글의 방향을 잡아요. ①~⑤를 하나씩 그 방향과 같은 쪽인지 보고, 다른 쪽 한 문장을 골라요. 같은 단어가 나와도 방향이 다를 수 있어요.")]),
            choice("s1_dir",
                   "글쓴이는 교실에서 처음 음악 활동을 할 때 어떻게 하라고 할까요?",
                   [("o0", "악기를 아예 쓰지 않는다", True), ("o1", "좋은 악기부터 고른다", False), ("o2", "악기 연주부터 가르친다", False)],
                   "it은 뒤의 'to avoid using instruments altogether'를 받아요. altogether는 '완전히, 아예'예요.",
                   why="'to avoid using instruments altogether', 악기 사용을 완전히 피하는 게 좋은 생각이래요.",
                   highlight=["to avoid using instruments altogether"],
                   tips=[tip("가주어 it", "it is … to ~는 '~하는 것은 …이다'로 읽어요. it은 뒤의 to ~를 대신 받아요.", "it is")],
                   point="글의 방향 = 처음 음악 수업은 악기 없이 (avoid using instruments)"),
            show("s1_topic", "이 글의 방향은 '처음엔 악기 없이'예요. ①~⑤를 이 방향과 같은 쪽인지 칠판에 나눠 볼게요.",
                 panel=board([], []), button="다음 문장"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("This", "이것 · 앞 문장에서 말한 방법"), g("will allow", "~하게 해 줄 것이다"), g("an inexperienced teacher", "경험이 적은 교사"),
                    g("to focus on the development of fundamental musical behaviour", "기본적인 음악 행동의 발달에 집중하는 것"),
                    g("through listening, performing and composing", "듣기, 연주하기, 작곡하기를 통해"), g("allow", "~하게 해 주다"),
                    g("the children", "아이들"), g("to focus on the more controllable sound sources", "더 다루기 쉬운 소리 내는 것들에 집중하는 것"),
                    g("i.e.", "즉"), g("voices and body percussion", "목소리와 몸 두드리기 소리"),
                    g("clapping, clicking, stamping etc", "손뼉 치기, 딸깍 소리 내기, 발 구르기 등"), g("controllable", "통제할 수 있는, 다루기 쉬운")],
        "slashes": ["①This will allow", "an inexperienced teacher", "to focus on the development", "of fundamental musical behaviour",
                    "performing and composing;", "and allow the children", "to focus on", "controllable sound sources", "i.e.", "body percussion"],
        "roles": [r("This", "S"), r("will allow", "V"), r("an inexperienced teacher", "O"),
                  r("to focus on the development of fundamental musical behaviour", "C"), r("allow", "V"), r("the children", "O"),
                  r("to focus on the more controllable sound sources", "C")],
        "steps": [
            sv("s2_sv", ["This", "will allow", "an inexperienced teacher", "to focus on the development of fundamental musical behaviour",
                         "through listening, performing and composing", "allow", "the children", "to focus on the more controllable sound sources"],
               {"This": "S", "will allow": "V", "an inexperienced teacher": "O", "to focus on the development of fundamental musical behaviour": "C",
                "allow": "V", "the children": "O", "to focus on the more controllable sound sources": "C"},
               {"through listening, performing and composing": "그건 through(~을 통해) 뒤 덩어리예요. 어떻게 집중하는지 덧붙여요."},
               "주어 This, 동사 will allow와 allow, 목적어 an inexperienced teacher와 the children, 보어는 각각 to focus on … 덩어리예요.",
               ask="긴 문장이에요. 주어(S)·동사(V)·목적어(O)를 찾고, 목적어가 무엇을 하게 되는지(보어 C)까지 모두 찾아볼까요?",
               tips=[tip("allow + 사람 + to ~", "'사람이 ~하게 해 주다'예요. allow the children to focus = 아이들이 집중하게 해 준다.", "will allow")]),
            sort_step("s2_sort", "①", "voices · body percussion", False,
                      "'the more controllable sound sources i.e. voices and body percussion', 악기 대신 목소리와 몸 소리에 집중하게 된대요. 악기 없이 시작하는 쪽이에요.",
                      ["voices and body percussion"],
                      tips=[tip("i.e.", "'즉, 다시 말해'예요. 앞말을 풀어 줘요.", "i.e.")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("Music", "음악"), g("starts", "시작한다 · start with = ~로 시작하다"), g("these", "이것들"),
                    g("both developmentally and historically", "발달 면에서도 역사적으로도"),
                    g("the most expressive and immediate musical instrument", "가장 표현이 풍부하고 바로 쓸 수 있는 악기"),
                    g("is", "~이다"), g("the human voice", "인간의 목소리")],
        "slashes": ["②Music starts with these", "and historically:", "musical instrument"],
        "roles": [r("Music", "S"), r("starts", "V"), r("the most expressive and immediate musical instrument", "S"), r("is", "V"),
                  r("the human voice", "C")],
        "steps": [
            choice("s3_these",
                   "these(이것들)는 무엇을 가리킬까요?",
                   [("o0", "목소리와 몸으로 내는 소리", True), ("o1", "여러 가지 악기", False), ("o2", "교사와 아이들", False)],
                   "가리키는 것은 앞 문장에서 찾아요. ① 문장의 끝부분을 봐요.",
                   why="앞 문장 끝 'voices and body percussion'이에요. 음악은 여기서 시작한대요.",
                   highlight=["these"], levels=["중", "초"],
                   tips=[tip("both A and B", "'A와 B 둘 다'예요. both developmentally and historically = 발달 면에서도 역사적으로도.", "both")]),
            sort_step("s3_sort", "②", "the human voice", False,
                      "음악은 목소리와 몸 소리로 시작하고, 가장 표현이 풍부한 악기는 사람의 목소리래요. 악기 없이 시작하는 쪽이에요.",
                      ["these", "the human voice"],
                      tips=[tip("instrument = 목소리?", "여기서는 사람의 목소리를 '악기'에 빗댄 말이에요. 진짜 악기 이야기가 아니에요.", "musical instrument")]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("The sound quality", "음질, 소리의 질"), g("an instrument", "악기"), g("is", "~이다"), g("a direct result", "직접적인 결과"),
                    g("of the quality of the materials, design, and making", "재료, 디자인, 제작의 품질의")],
        "slashes": ["of an instrument", "a direct result", "materials, design,"],
        "roles": [r("The sound quality", "S"), r("is", "V"), r("a direct result", "C")],
        "steps": [
            sort_step("s4_sort", "③", "sound quality of an instrument", True,
                      "'The sound quality of an instrument', 악기의 음질은 재료·디자인·제작에 달렸대요. 악기 없이 시작하자는 말이 아니라 악기 자체 이야기예요.",
                      ["sound quality", "materials"]),
            show("s4_hold", "②에도 instrument가 나왔지만 목소리를 악기에 빗댄 말이었어요. ③은 진짜 악기의 음질 이야기라 방향에서 벗어나요.",
                 panel=board(["voices · body percussion", "the human voice"], ["sound quality of an instrument"],
                             fresh=("sound quality of an instrument",)), button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Body movements", "몸의 움직임"), g("are", "~이다"), g("not only", "~일 뿐만 아니라"),
                    g("an instinctive response", "본능적인 반응"), g("to music", "음악에 대한"), g("but also", "~도 (한다)"),
                    g("instigate", "부추기다"), g("music making", "음악 만들기")],
        "slashes": ["④Body movements", "are not only", "to music", "but also"],
        "roles": [r("Body movements", "S"), r("are", "V"), r("an instinctive response", "C"), r("instigate", "V"), r("music making", "O")],
        "steps": [
            sort_step("s5_sort", "④", "body movements", False,
                      "몸의 움직임이 음악을 만들게(music making) 부추긴대요. ①의 body percussion처럼 악기 없이 몸으로 하는 음악이에요.",
                      ["Body movements", "music making"],
                      tips=[tip("not only A but also B", "'A일 뿐만 아니라 B도'예요. 글쓴이가 더 말하고 싶은 쪽은 B예요.", "not only")]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Activities", "활동들"), g("which develop", "~을 발달시키는"), g("many of the coordination skills", "조정 능력의 많은 부분"),
                    g("aural sensitivity", "청각적 감수성(듣는 감각)"), g("responses to visual cues and symbols", "시각적 신호와 기호에 대한 반응"),
                    g("the musical understanding", "음악적 이해"), g("necessary to play an instrument", "악기를 연주하는 데 필요한"),
                    g("can all be established", "모두 자리 잡을 수 있다"), g("without instruments", "악기 없이")],
        "slashes": ["⑤Activities", "which develop", "coordination skills,", "aural sensitivity,", "visual cues and symbols,",
                    "the musical understanding", "to play an instrument", "can all be established"],
        "roles": [r("Activities", "S"), r("can all be established", "V")],
        "modifiers": [MOD],
        "steps": [
            sv("s6_sv", ["Activities", "develop", "can all be established", "without instruments"],
               {"Activities": "S", "can all be established": "V"},
               {"develop": "그건 which 덩어리 안의 동사예요. 앞의 Activities를 꾸며요.",
                "without instruments": "그건 without(~ 없이) 뒤 덩어리예요."},
               "주어는 Activities, 동사는 can (all) be established예요. 그 사이 which … instrument가 길게 Activities를 꾸며요.",
               ask="긴 문장이에요. 주어(S)와 동사(V)를 찾아볼까요?"),
            show("s6_modify", "초록 부분은 앞의 Activities를 꾸며요. 아래 표처럼 읽어요.",
                 highlight=["Activities"], highlight_alt=[MOD],
                 panel=rows(("S", "Activities", "활동들", "hl"),
                            ("↖ 꾸밈", "which develop … necessary to play an instrument", "악기 연주에 필요한 능력을 발달시키는", "hl2"),
                            ("V", "can all be established", "모두 자리 잡을 수 있다")),
                 panel_below=True),
            sort_step("s6_sort", "⑤", "without instruments", False,
                      "'can all be established without instruments', 악기 연주에 필요한 능력도 모두 악기 없이 기를 수 있대요. 악기 없이 시작하는 쪽이에요.",
                      ["without instruments"]),
            show("s6_go", "①②④⑤는 '악기 없이 시작' 쪽이에요. 다른 쪽에 놓인 한 문장을 문제에서 골라 봐요.",
                 panel=board(["voices · body percussion", "the human voice", "body movements", "without instruments"],
                             ["sound quality of an instrument"], fresh=("without instruments",)),
                 button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 3, [m("Music", "음악은"), " ", m("both developmentally and historically", "발달 면에서도 역사적으로도"), " ",
                         m("these", "이것들"), "로 ", m("starts", "시작한다"), ": ",
                         m("the most expressive and immediate musical instrument", "가장 표현이 풍부하고 바로 쓸 수 있는 악기는"), " ",
                         m("the human voice", "인간의 목소리"), m("is", "이다"), "."],
          sv_new=sv_step("s3_basic_sv", ["Music", "starts", "these", "the most expressive and immediate musical instrument", "is", "the human voice"],
                         {"Music": "S", "starts": "V", "the most expressive and immediate musical instrument": "S", "is": "V", "the human voice": "C"},
                         {"these": "그건 with 뒤의 말이에요. 무엇으로 시작하는지예요."},
                         "콜론(:) 앞은 주어 Music, 동사 starts예요. 뒤는 주어 the most … instrument, 동사 is, 보어 the human voice예요."),
          meaning_after="s3_sort",
          meaning="음악은 목소리와 몸 소리에서 시작하고, 가장 좋은 악기는 사람의 목소리래요.")
add_basic(sentences, 4, [m("The sound quality", "음질은"), " (", m("an instrument", "악기의"), ") ",
                         m("of the quality of the materials, design, and making", "재료·디자인·제작 품질의"), " ",
                         m("a direct result", "직접적인 결과"), m("is", "이다"), "."],
          sv_new=sv_step("s4_basic_sv", ["The sound quality", "an instrument", "is", "a direct result"],
                         {"The sound quality": "S", "is": "V", "a direct result": "C"},
                         {"an instrument": "그건 of 뒤 덩어리예요. 어떤 음질인지 꾸며요."},
                         "주어는 The sound quality (of an instrument), 동사는 is, 보어는 a direct result예요."),
          meaning_after="s4_sort",
          meaning="악기 소리가 좋은지는 재료·디자인·만듦새에 달렸대요.")
add_basic(sentences, 5, [m("Body movements", "몸의 움직임은"), " ", m("to music", "음악에 대한"), " ", m("an instinctive response", "본능적인 반응"),
                         m("are", "일"), " 뿐만 아니라, ", m("music making", "음악 만들기"), "를 ", m("instigate", "부추기기도 한다"), "."],
          sv_new=sv_step("s5_basic_sv", ["Body movements", "are", "an instinctive response", "instigate", "music making"],
                         {"Body movements": "S", "are": "V", "an instinctive response": "C", "instigate": "V", "music making": "O"}, {},
                         "주어는 Body movements, 동사는 are와 instigate예요. are의 보어는 an instinctive response, instigate의 목적어는 music making이에요."),
          meaning_after="s5_sort",
          meaning="몸의 움직임은 음악에 저절로 나오는 반응이면서, 음악을 만들게 부추기기도 한대요.")

SENSES = {
    1: [sense("for", "for the first time", "~ 만에, 처음으로", "for the first time = 처음으로"),
        sense("to", "to avoid using", "~하는 것", "to부정사 (진주어: it is … to ~)")],
    2: [sense("to", "to focus on the development", "~하게 (해 주다)", "allow + 사람 + to부정사"),
        sense("to", "to focus on the more controllable", "~하게 (해 주다)", "allow + 사람 + to부정사")],
    5: [sense("to", "response to music", "~에 대한", "response to + 명사"),
        sense("but", "but also instigate", "~도 (또한)", "not only A but also B")],
    6: [sense("which", "Activities which develop", "(앞 명사를 꾸밈) ~하는", "관계대명사 which + 동사"),
        sense("to", "responses to visual cues", "~에 대한", "response to + 명사"),
        sense("to", "necessary to play", "~하는 데 (필요한)", "necessary + to부정사")],
}

WORDS = {"approaching": "다가가는, 시작하는", "practical": "실제의", "music": "음악", "making": "만드는 것", "first": "첫", "classroom": "교실",
         "good": "좋은", "idea": "생각", "avoid": "피하다", "using": "쓰는 것", "instruments": "악기들", "altogether": "완전히",
         "inexperienced": "경험이 적은", "teacher": "교사", "focus": "집중하다", "development": "발달", "fundamental": "기본적인",
         "musical": "음악의", "behaviour": "행동", "listening": "듣기", "performing": "연주하기", "composing": "작곡하기", "allow": "~하게 해 주다",
         "children": "아이들", "controllable": "다루기 쉬운", "sound": "소리", "sources": "원천, 내는 것", "voices": "목소리",
         "body": "몸", "percussion": "두드려 내는 소리", "clapping": "손뼉 치기", "clicking": "딸깍 소리 내기", "stamping": "발 구르기",
         "etc": "등", "starts": "시작한다", "developmentally": "발달 면에서", "historically": "역사적으로", "expressive": "표현이 풍부한",
         "immediate": "즉각적인, 바로 쓸 수 있는", "instrument": "악기", "human": "인간의", "voice": "목소리", "quality": "질, 품질",
         "direct": "직접적인", "result": "결과", "materials": "재료", "design": "디자인", "movements": "움직임", "instinctive": "본능적인",
         "response": "반응", "instigate": "부추기다", "activities": "활동들", "develop": "발달시키다", "coordination": "조정",
         "skills": "능력", "aural": "청각의", "sensitivity": "감수성", "responses": "반응", "visual": "시각의", "cues": "신호",
         "symbols": "기호", "understanding": "이해", "necessary": "필요한", "play": "연주하다", "established": "자리 잡은", "will": "~할 것이다",
         "i.e.": "즉", "many": "많은"}

exam = {
    "question": "다음 글에서 전체 흐름과 관계 없는 문장은?",
    "underline": ["①", "②", "③", "④", "⑤"], "numbers_only": True, "sentence": 4, "analysis_first": True,
    "wrong_rate": 36.0, "wrong_rank": 12,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "passage_keywords": ["avoid using instruments", "voices and body percussion", "the human voice", "sound quality", "Body movements",
                         "without instruments"],
    "options": [{"id": str(i), "label": f"{'①②③④⑤'[i - 1]} 문장", "keywords": [], **({"correct": True} if i == 3 else {})} for i in range(1, 6)],
    "brief": exam_brief(
        "칠판 두 칸을 떠올려 봐요. 혼자 다른 쪽에 놓인 문장을 골라요.",
        "정답이에요! 글은 처음 음악 수업을 악기 없이, 목소리와 몸으로 시작하자고 해요. ③만 악기의 음질 이야기를 해요.",
        "정답은 ③이에요. 나머지는 모두 악기 없이 목소리·몸으로 시작하는 이야기인데, ③만 악기 자체의 음질을 말해요.",
        {"1": "①은 악기 없이 하면 아이들이 목소리와 몸 소리에 집중할 수 있다는 말이에요. 글의 방향 그대로예요.",
         "2": "②의 instrument는 사람의 목소리를 악기에 빗댄 말이에요. 목소리로 시작한다는 같은 방향이에요.",
         "4": "④의 몸의 움직임은 ①의 body percussion과 이어져요. 몸으로 음악을 시작하니 같은 방향이에요.",
         "5": "⑤는 악기 연주에 필요한 능력도 악기 없이 기를 수 있다는 말이에요. 같은 방향이에요."},
        {"4": review(16,
                     "④는 악기 말이 없어서 엉뚱해 보여요. 그런데 Body movements(몸의 움직임)는 ①의 body percussion(몸 두드리기)과 이어져요. 몸으로 음악을 시작하니 '악기 없이' 쪽이에요.",
                     "그래서 ④가 아니에요. 어디서 헷갈렸어요?",
                     [("악기 말이 없어서 상관없어 보였어요", ["direction"],
                       "알려 줘서 고마워요. 무관한 문장은 같은 단어가 있는지가 아니라 글의 방향과 같은 쪽인지로 봐요. 몸으로 하는 음악은 '악기 없이' 쪽이었어요. 앞으로 이 점을 짚어 줄게요."),
                      ("instigate가 어려웠어요", ["vocab"],
                       "알려 줘서 고마워요. instigate는 '부추기다'예요. 시험지 아래 풀이(*)도 꼭 같이 봐요. 앞으로 어려운 단어를 먼저 짚어 줄게요."),
                      ("③은 맞는 말 같았어요", ["true_vs_flow"],
                       "알려 줘서 고마워요. ③은 그 자체로는 맞는 말이에요. 하지만 이 글은 '처음엔 악기 없이'라는 흐름이라 악기의 음질 이야기는 벗어나요. 앞으로 사실인지보다 흐름을 보게 할게요.")],
                     panel=rows(("④", "Body movements … music making", "몸으로 음악 시작 → 악기 없이 (같은 쪽)", "hl"),
                                ("①", "voices and body percussion", "목소리·몸 소리 → 악기 없이 (같은 쪽)", "hl")),
                     rank_word="가장 많이 고른"),
         "2": review(11,
                     "②에는 instrument가 나와서 악기 이야기로 보일 수 있어요. 그런데 여기서 악기는 the human voice, 사람의 목소리예요. 목소리로 시작하니 '악기 없이' 쪽이에요.",
                     "그래서 ②가 아니에요. 어디서 헷갈렸어요?",
                     [("instrument가 나와서 악기 이야기인 줄 알았어요", ["word_trap"],
                       "알려 줘서 고마워요. 같은 단어여도 무엇을 가리키는지 봐야 해요. 여기서는 목소리를 악기에 빗댔어요. 앞으로 이런 단어를 먼저 짚어 줄게요."),
                      ("these가 무엇인지 몰랐어요", ["reference"],
                       "알려 줘서 고마워요. these는 앞 문장의 voices and body percussion이에요. 앞으로 가리키는 말을 같이 찾아볼게요.")],
                     panel=rows(("②", "the most expressive … instrument is the human voice", "가장 좋은 '악기' = 사람의 목소리", "hl"))),
         }),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 35번 (흐름과 무관한 문장, 2점)",
    topic="무관한 문장 푸는 법: 첫 문장으로 글의 방향 잡기 → ①~⑤를 같은 쪽/다른 쪽으로 나누기 → 다른 쪽 한 문장",
    method={"type": "irrelevant", "labels": ["방향 잡기", "문장마다 나누기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-2022-03-35-music-class.svg", ("Instruments", "악기"), "?", ("Voice & body", "목소리·몸"),
                                       "첫 음악 수업, 무엇으로 시작할까?", "2022년 3월 35번 도입 칠판"),
                      "alt": "칠판: Instruments(악기) ? Voice & body(목소리·몸)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "교실에서 처음 음악 수업을 한다면 무엇으로 시작할까요? 이번 글은 첫 음악 수업 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "무관한 문장 문제는 첫 문장으로 글의 방향을 잡고, ①~⑤를 같은 쪽과 다른 쪽으로 나눠요. 칠판에 하나씩 놓아 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("approach", "다가가다, 접근하다"), g("practical", "실제의"), g("avoid", "피하다"), g("altogether", "완전히"),
                           g("inexperienced", "경험이 적은"), g("fundamental", "기본적인"), g("compose", "작곡하다"), g("controllable", "통제할 수 있는"),
                           g("percussion", "두드려 내는 소리, 타악기"), g("developmentally", "발달 면에서"), g("expressive", "표현이 풍부한"),
                           g("immediate", "즉각적인"), g("instinctive", "본능적인"), g("aural", "청각의"), g("visual cue", "시각적 신호"),
                           g("establish", "자리 잡게 하다")],
               "options": []},
    sentences=sentences, concept="medium")

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="무관한 문장 푸는 법",
       chunks={"practical music making": "실제로 음악을 만드는 일", "it": "그것", "is": "~이다", "a good idea": "좋은 생각", "instruments": "악기들",
               "This": "이것", "will allow": "~하게 해 줄 것이다", "an inexperienced teacher": "경험이 적은 교사",
               "allow": "~하게 해 주다", "the children": "아이들", "Music": "음악", "starts": "시작한다", "these": "이것들",
               "the human voice": "인간의 목소리", "The sound quality": "음질", "an instrument": "악기", "a direct result": "직접적인 결과",
               "Body movements": "몸의 움직임", "are": "~이다", "an instinctive response": "본능적인 반응", "instigate": "부추기다",
               "music making": "음악 만들기", "Activities": "활동들", "develop": "발달시키다", "can all be established": "모두 자리 잡을 수 있다",
               "without instruments": "악기 없이"})
