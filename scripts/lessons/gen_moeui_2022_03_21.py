"""2022년 3월 고3 21번 레슨 + 대사를 만든다 (밑줄 의미 추론, 3점). 오답률 32.0% · Top 14.

    py scripts/lessons/gen_moeui_2022_03_21.py   (→ node scripts/policy_copy.mjs stamp <id> → npm run build)

틀: 기준 레슨 2026년 3월 21번(밑줄 의미) — 핵심 단어 → 관계(두 시대) → 밑줄 뜻. 2024년 3월 21번 생성기를 본보기로 (Claude 초안).
정답 ④ is under the influence of earlier electrical innovations.
많이 고른 오답 ② 11%(산업 시대의 한계를 극복하려 애쓴다 — this age를 industrial age로 잘못 잡음 + stamp를 극복으로 읽음) → option_review.
선택률 ① 7% · ② 11% · ③ 7% · ④ 68% · ⑤ 8% — 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
열쇠: 문장 4의 from an industrial age(철·석탄·증기) → to a post-industrial one(전기·석유·20세기).
this age = 바로 앞의 post-industrial one(전기가 이끈 20세기). carries the stamp of this age = 여전히 그 시대의 흔적(영향)을 지닌다.
alloy는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt — match=필적하다, stamp=흔적, dazzle=감탄하게 하다).
반영한 규칙: 끊어읽기(slashes·roles·modifiers, 2026-10-20), 긴 문장 S·V(문장 3·4·5), 칠판은 읽은 데까지만, 대사 핵심만.
문장 1(34단어)은 is가 두 번 나와 S·V 찾기를 넣지 않았다 — 배경 문장이라 뜻 확인만.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2022-03-21-edison-light"

S = [
    "Thomas Edison’s name is synonymous with invention, and his most famous invention, the electric light bulb, is a familiar symbol "
    "for that flash of inspired genius traditionally associated with the inventive act.",
    "Besides being the exemplar of the “bright idea,” however, Edison’s electric light is worthy of study for other reasons.",
    "The technical and economic importance of the light and of the electrical system that surrounded it matches that of any other "
    "invention we could name, at least from the last two hundred years.",
    "The introduction and spread of electric light and power was one of the key steps in the transformation of the world from an "
    "industrial age, characterized by iron and coal and steam, to a post-industrial one, in which electricity was joined by petroleum, "
    "light metals and alloys, and internal combustion engines to give the twentieth century its distinctive form and character.",
    "Our own time still largely carries the stamp of this age, however dazzled we may be by the electronic, computerized, and media "
    "wonders of the twenty-first century.",
]
KO = [
    "토머스 에디슨의 이름은 발명과 동의어이고, 그의 가장 유명한 발명품인 전구는 전통적으로 창의적 행위와 연관되는 영감을 받은 번득이는 그러한 천재성을 나타내는 친숙한 상징이다.",
    "그러나 에디슨의 전깃불은 '총명한 아이디어'의 표본이라는 것 외에도 다른 이유로 연구할 가치가 있다.",
    "전깃불과 그 주변을 둘러싸고 있는 전기 시스템의 기술적, 경제적 중요성은 적어도 지난 200년 이래 우리가 열거할 수 있는 다른 어떤 발명품의 기술적, 경제적 중요성에 필적한다.",
    "전깃불과 전력의 도입과 확산은 세상이 철, 석탄, 증기를 특징으로 하는 산업 시대에서, 전기가 석유, 경금속과 합금, 그리고 내연 기관과 결합해 20세기에 특유한 형태와 특성을 부여한 후기 산업 시대로의 전환에 핵심 단계 중 하나였다.",
    "우리가 21세기의 전자, 전산화, 그리고 미디어의 경이에 아무리 감탄할지라도, 우리 자신의 시대는 여전히 대체로 이 시대의 흔적을 지니고 있다.",
]

IND = "왼쪽 · 산업 시대 (industrial age)"
POST = "오른쪽 · 후기 산업 시대 (post-industrial)"


def board(left, right, fresh=(), sort=None):
    return groups("두 시대", "industrial age (산업 시대)", left, "post-industrial (후기 산업 시대)", right, fresh=fresh, between="→",
                  sort={"words": sort, "left": IND, "right": POST} if sort else None)


L4 = [("iron · coal · steam", "철·석탄·증기")]
R4 = [("petroleum · light metals", "석유·경금속"), ("internal combustion engines", "내연 기관")]
R4_ALL = R4 + [("electricity", "전기")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("Thomas Edison’s name", "토머스 에디슨의 이름"), g("is synonymous with", "~와 동의어이다"), g("synonymous", "동의어의, 같은 뜻인"),
                    g("invention", "발명, 발명품"), g("his most famous invention", "그의 가장 유명한 발명품"), g("the electric light bulb", "전구"),
                    g("is a familiar symbol for", "~의 친숙한 상징이다"), g("symbol", "상징"), g("familiar", "친숙한"),
                    g("that flash of inspired genius", "영감을 받은 번득이는 천재성"), g("flash", "번득임"), g("inspired", "영감을 받은"),
                    g("genius", "천재성"), g("traditionally associated with", "전통적으로 ~와 연관된"), g("associated", "연관된"),
                    g("the inventive act", "창의적 행위"), g("inventive", "창의적인")],
        "slashes": ["synonymous with invention,", "and his most famous invention,", "the electric light bulb,", "a familiar symbol", "inspired genius"],
        "roles": [r("Thomas Edison’s name", "S"), r("is … is", "V"), r("synonymous", "C"), r("his most famous invention", "S"),
                  r("a familiar symbol", "C")],
        "steps": [
            choice("s1_symbol",
                   "에디슨의 전구는 흔히 무엇의 상징이래요?",
                   [("o0", "산업 시대의 끝", False), ("o1", "번득이는 천재적 영감", True), ("o2", "값싼 전기", False)],
                   "'a familiar symbol for …' 뒤를 봐요. symbol for는 '~의 상징'이에요.",
                   why="'a familiar symbol for that flash of inspired genius', 전구는 영감을 받은 천재성이 번쩍하는 순간의 상징이래요.",
                   highlight=["symbol", "inspired genius"],
                   tips=[tip("synonymous with", "'~와 동의어인, ~의 대명사'예요. 에디슨 하면 곧 발명이라는 말이에요.", "synonymous")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Besides being", "~인 것 외에도"), g("Besides", "~ 외에도"), g("the exemplar", "표본, 본보기"), g("exemplar", "표본, 본보기"),
                    g("bright idea", "총명한(번뜩이는) 아이디어"), g("however", "그러나"), g("Edison’s electric light", "에디슨의 전깃불"),
                    g("is worthy of study", "연구할 가치가 있다"), g("worthy", "~의 가치가 있는"), g("study", "연구"),
                    g("for other reasons", "다른 이유로")],
        "slashes": ["“bright idea,”", "however,", "worthy of study"],
        "roles": [r("Edison’s electric light", "S"), r("is", "V"), r("worthy", "C")],
        "steps": [
            choice("s2_however",
                   "에디슨의 전깃불은 무엇 때문에 연구할 가치가 있대요?",
                   [("o0", "번뜩이는 아이디어의 본보기라서", False), ("o1", "그것 말고 다른 이유로", True), ("o2", "값이 싸서", False)],
                   "Besides(~ 외에도)와 문장 끝 for other reasons를 같이 봐요.",
                   why="'Besides being the exemplar of the bright idea', 번뜩이는 아이디어의 본보기라는 것 말고도 'for other reasons' 연구할 가치가 있대요.",
                   highlight=["Besides", "however", "other reasons"],
                   tips=[tip("Besides -ing", "'~인 것 외에도'예요. 앞 이야기(전구 = 천재성의 상징)에 다른 이야기를 더하겠다는 신호예요.", "Besides"),
                         tip("be worthy of", "'~할 가치가 있다'예요. worthy of study = 연구할 가치가 있는.", "worthy")]),
            show("s2_next", "그 다른 이유가 다음 문장부터 나와요. 글의 진짜 이야기는 여기서 시작해요.",
                 highlight=["other reasons"], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("The technical and economic importance", "기술적·경제적 중요성"), g("technical", "기술적인"), g("economic", "경제적인"),
                    g("importance", "중요성"), g("of the light", "전깃불의"), g("the electrical system", "전기 시스템"), g("electrical", "전기의"),
                    g("system", "체계, 시스템"), g("that surrounded it", "그것을 둘러싼"), g("surrounded", "둘러쌌다"), g("matches", "~에 필적한다"),
                    g("that of any other invention", "다른 어떤 발명품의 그것(중요성)"), g("we could name", "우리가 열거할 수 있는"),
                    g("at least", "적어도"), g("the last two hundred years", "지난 200년")],
        "slashes": ["The technical and economic importance", "of the electrical system", "that surrounded it", "any other invention", "we could name,"],
        "roles": [r("The technical and economic importance", "S"), r("matches", "V"), r("that of any other invention", "O")],
        "modifiers": ["that surrounded it", "we could name"],
        "steps": [
            sv("s3_sv", ["The technical and economic importance", "the electrical system", "surrounded", "matches",
                         "that of any other invention", "the last two hundred years"],
               {"The technical and economic importance": "S", "matches": "V", "that of any other invention": "O"},
               {"the electrical system": "그건 of 뒤 덩어리예요. 주어를 꾸며요.",
                "surrounded": "그건 that 덩어리 안의 동사예요. 앞의 system을 꾸며요.",
                "the last two hundred years": "그건 from 뒤 덩어리예요."},
               "주어는 The technical and economic importance(기술적·경제적 중요성), 동사는 matches(~에 필적한다), 목적어는 that of any other invention이에요.",
               ask="주어가 아주 길어요. 주어(S)·동사(V)·목적어(O)를 찾아볼까요?"),
            choice("s3_that",
                   "that of any other invention의 that은 무엇을 대신할까요?",
                   [("o0", "the importance (중요성)", True), ("o1", "the electrical system (전기 시스템)", False), ("o2", "the light (전깃불)", False)],
                   "무엇과 무엇을 견주는지 생각해 봐요. 전깃불의 ○○와 다른 발명품의 ○○예요.",
                   why="that은 주어의 핵심 명사를 다시 받아요. 전깃불의 중요성이 다른 발명품의 중요성에 필적한다는 말이에요.",
                   levels=["중", "초"], highlight=["that of any other invention"],
                   tips=[tip("that of ~", "앞에 나온 명사를 되풀이하지 않으려고 that(복수면 those)으로 받아요. 'that of + 다른 것' = '다른 것의 그것'.", "that of")]),
            choice("s3_mean",
                   "전깃불과 전기 시스템의 중요성은 어느 정도래요?",
                   [("o0", "다른 발명품보다 훨씬 덜하다", False), ("o1", "지난 200년의 어떤 발명품에도 뒤지지 않는다", True),
                    ("o2", "200년 뒤에야 알려질 것이다", False)],
                   "동사 matches(~에 필적한다)와 any other invention(다른 어떤 발명품)을 같이 봐요.",
                   why="'matches that of any other invention', 다른 어떤 발명품의 중요성과도 맞먹는대요. 적어도 지난 200년 동안의 발명품 중에서요.",
                   highlight=["importance", "matches", "any other invention"],
                   point="전깃불(과 전기 시스템)의 기술적·경제적 중요성 = 지난 200년의 어떤 발명품에도 필적"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("The introduction and spread", "도입과 확산"), g("introduction", "도입"), g("spread", "확산"),
                    g("electric light and power", "전깃불과 전력"), g("power", "전력"), g("was", "~였다"),
                    g("one of the key steps", "핵심 단계 중 하나"), g("key", "핵심적인"), g("steps", "단계"),
                    g("the transformation of the world", "세상의 전환"), g("transformation", "전환, 탈바꿈"),
                    g("from an industrial age", "산업 시대에서"), g("industrial", "산업의"), g("age", "시대"),
                    g("characterized by", "~을 특징으로 하는"), g("characterized", "특징지어진"),
                    g("iron and coal and steam", "철과 석탄과 증기"), g("iron", "철"), g("coal", "석탄"), g("steam", "증기"),
                    g("to a post-industrial one", "후기 산업 시대로"), g("post-industrial", "후기 산업의"), g("in which", "그 시대에는"),
                    g("electricity", "전기"), g("was joined", "결합되었다"), g("petroleum", "석유"),
                    g("light metals and alloys", "경금속과 합금"), g("metals", "금속"), g("alloys", "합금"),
                    g("internal combustion engines", "내연 기관"), g("internal", "내부의"), g("combustion", "연소"), g("engines", "엔진, 기관"),
                    g("to give the twentieth century", "20세기에 ~을 부여하여"), g("twentieth", "20번째의"), g("century", "세기"),
                    g("its distinctive form and character", "특유한 형태와 특성"), g("distinctive", "특유한, 뚜렷이 구별되는"),
                    g("form", "형태"), g("character", "특성")],
        "slashes": ["The introduction and spread", "electric light and power", "the key steps", "of the world", "an industrial age,",
                    "and steam,", "a post-industrial one,", "electricity was joined", "and alloys,", "combustion engines"],
        "roles": [r("The introduction and spread", "S"), r("was", "V"), r("one of the key steps", "C")],
        "modifiers": ["characterized by iron and coal and steam",
                      "in which electricity was joined by petroleum, light metals and alloys, and internal combustion engines to give the "
                      "twentieth century its distinctive form and character"],
        "steps": [
            sv("s4_sv", ["The introduction and spread", "electric light and power", "was", "one of the key steps",
                         "the transformation of the world", "electricity", "was joined"],
               {"The introduction and spread": "S", "was": "V", "one of the key steps": "C"},
               {"electric light and power": "그건 of 뒤 덩어리예요. 주어를 꾸며요.",
                "the transformation of the world": "그건 in 뒤 덩어리예요.",
                "electricity": "그건 in which 덩어리 안의 주어예요. 문장 전체의 주어가 아니에요.",
                "was joined": "그건 in which 덩어리 안의 동사예요. 문장 전체의 동사가 아니에요."},
               "주어는 The introduction and spread(도입과 확산), 동사는 was, 보어는 one of the key steps(핵심 단계 중 하나)예요. in which 뒤는 앞의 post-industrial one을 꾸며요.",
               ask="아주 긴 문장이에요. 주어(S)·동사(V)·보어(C)를 찾아볼까요?"),
            choice("s4_from_to",
                   "세상이 어느 시대에서 어느 시대로 바뀌었대요?",
                   [("o0", "후기 산업 시대에서 산업 시대로", False), ("o1", "산업 시대에서 후기 산업 시대로", True),
                    ("o2", "전기 시대에서 컴퓨터 시대로", False)],
                   "from A to B는 'A에서 B로'예요. from과 to 뒤를 찾아봐요.",
                   why="'from an industrial age … to a post-industrial one', 철·석탄·증기의 산업 시대를 지나 후기 산업 시대로 넘어갔대요. 전깃불이 그 핵심 단계였고요.",
                   highlight=["transformation", "industrial age", "post-industrial one"],
                   tips=[tip("post-industrial one", "one은 앞의 age를 받아요. a post-industrial one = 후기 산업 시대.", "post-industrial one"),
                         tip("characterized by", "'~을 특징으로 하는'이에요. 콤마 사이에서 앞의 industrial age를 설명해요.", "characterized")]),
            choice("s4_sort",
                   "'electricity(전기)'는 칠판 어느 시대 쪽일까요?",
                   [("o0", IND, False), ("o1", POST, True)],
                   "in which는 바로 앞의 post-industrial one을 꾸며요. 그 안에 electricity가 있어요.",
                   why="'a post-industrial one, in which electricity was joined by petroleum', 후기 산업 시대에 전기가 석유·경금속·내연 기관과 합쳐졌대요.",
                   highlight=["electricity", "petroleum"],
                   panel=board(L4, R4, sort=["electricity"])),
            show("s4_century", "전기가 석유, 내연 기관과 함께 20세기의 모습을 만들었대요. 철·석탄·증기의 산업 시대 다음 시대예요.",
                 highlight=["the twentieth century", "distinctive"],
                 panel=board(L4, R4_ALL + [("the twentieth century", "20세기")], fresh=("the twentieth century",)),
                 point="산업 시대(철·석탄·증기) → 후기 산업 시대(전기·석유·내연 기관 = 20세기의 모습), 전깃불은 그 전환의 핵심 단계",
                 button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Our own time", "우리 자신의 시대"), g("still", "여전히"), g("largely", "대체로"), g("carries", "지니고 있다"),
                    g("the stamp of this age", "이 시대의 흔적"), g("stamp", "도장, 찍힌 흔적"), g("however dazzled", "아무리 감탄하더라도"),
                    g("dazzled", "감탄한, 눈이 부신"), g("we", "우리는"), g("may be", "~일지도 모른다"),
                    g("the electronic, computerized, and media wonders", "전자·전산화·미디어의 경이"), g("electronic", "전자의"),
                    g("computerized", "전산화된"), g("media", "미디어"), g("wonders", "경이, 놀라운 것"),
                    g("the twenty-first century", "21세기"), g("twenty-first", "21번째의")],
        "slashes": ["the stamp of this age,", "we may be", "media wonders"],
        "roles": [r("Our own time", "S"), r("carries", "V"), r("the stamp of this age", "O"), r("we", "S"), r("may be", "V")],
        "steps": [
            sv("s5_sv", ["Our own time", "carries", "the stamp of this age", "we", "may be", "the twenty-first century"],
               {"Our own time": "S", "carries": "V", "the stamp of this age": "O"},
               {"we": "그건 however 덩어리 안의 주어예요. 문장 전체의 주어가 아니에요.",
                "may be": "그건 however 덩어리 안의 동사예요.",
                "the twenty-first century": "그건 of 뒤 덩어리예요."},
               "주어는 Our own time(우리 자신의 시대), 동사는 carries, 목적어는 the stamp of this age예요. 밑줄이 바로 이 동사와 목적어예요.",
               ask="밑줄이 있는 마지막 문장이에요. 주어(S)·동사(V)·목적어(O)를 찾아볼까요?",
               tips=[tip("stamp", "'도장, 찍힌 자국'이에요.", "stamp")]),
            choice("s5_this",
                   "this age(이 시대)는 어느 시대를 가리킬까요?",
                   [("o0", "철·석탄·증기의 산업 시대", False), ("o1", "전기·석유가 이끈 20세기 후기 산업 시대", True), ("o2", "21세기", False)],
                   "this는 바로 앞 문장에서 찾아요. 앞 문장 끝에서 이야기한 시대예요.",
                   why="this age는 앞 문장 끝의 post-industrial one이에요. 산업 시대는 그보다 앞선 시대이고, 21세기는 지금 우리 시대예요.",
                   highlight=["this age"],
                   panel=board(L4, R4_ALL + [("the twentieth century", "20세기")]),
                   point="this age = 앞 문장의 post-industrial one (전기·석유의 20세기)"),
            choice("s5_however",
                   "however dazzled we may be by … the twenty-first century는 무슨 뜻일까요?",
                   [("o0", "21세기의 경이에 아무리 감탄하더라도", True), ("o1", "21세기의 경이에는 감탄하지 않으므로", False),
                    ("o2", "21세기에는 경이로운 것이 없어서", False)],
                   "however + 형용사(dazzled) + 주어 + 동사는 '아무리 ~하더라도'예요.",
                   why="'however dazzled we may be', 우리가 아무리 감탄하더라도예요. 무엇에 감탄하는지는 by 뒤, 21세기의 전자·전산화·미디어의 경이예요.",
                   highlight=["however dazzled", "wonders"],
                   tips=[tip("however + 형용사 + 주어 + 동사", "'아무리 ~하더라도'예요. 콤마 앞 내용과 맞서는 양보의 말이에요.", "however"),
                         tip("dazzle", "'눈부시게 하다, 감탄하게 하다'예요. be dazzled by = ~에 감탄하다.", "dazzled")]),
            choice("s5_underline",
                   "드디어 밑줄이에요. 'Our own time still largely carries the stamp of this age'는 무슨 뜻일까요?",
                   [("o0", "우리 시대는 그 시대의 한계를 넘어서려 애쓴다", False),
                    ("o1", "우리 시대는 여전히 20세기 전기 시대의 영향 아래 있다", True),
                    ("o2", "우리 시대는 21세기 기술 덕에 그 시대와 완전히 달라졌다", False)],
                   "stamp는 도장 자국이에요. still(여전히)과 this age(앞 문장의 시대)를 이어 봐요.",
                   why="도장 자국처럼 그 시대의 흔적을 여전히 지니고 있다는 말이에요. 21세기 기술에 감탄해도, 우리 시대는 전기가 만든 20세기의 영향을 받고 있어요.",
                   highlight=["still", "the stamp of this age"],
                   panel=board(L4, R4_ALL + [("the twentieth century", "20세기")]),
                   point="carries the stamp of this age = 21세기에도 여전히 20세기 전기 시대(앞선 전기 혁신)의 영향을 받고 있다"),
            show("s5_go", "이 뜻을 다른 말로 바꿔 쓴 보기를 골라 봐요. this age가 어느 시대인지 꼭 기억해요.",
                 panel=rows(("그때", "this age", "전기·석유가 만든 20세기", "hl"),
                            ("지금", "Our own time", "21세기 — 여전히 그 흔적을 지님", "hl2")),
                 button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 2, [m("Edison’s electric light", "에디슨의 전깃불은"), " ", m("for other reasons", "다른 이유로"), " ",
                         m("is worthy of study", "연구할 가치가 있다"), "."],
          match_display="Edison’s electric light is worthy of study for other reasons.",
          sv_new=sv_step("s2_basic_sv", ["the exemplar", "Edison’s electric light", "is", "worthy"],
                         {"Edison’s electric light": "S", "is": "V", "worthy": "C"},
                         {"the exemplar": "그건 Besides being 뒤 덩어리예요. 주어가 아니에요."},
                         "주어는 Edison’s electric light(에디슨의 전깃불), 동사는 is, 보어는 worthy(가치가 있는)예요."),
          meaning_after="s2_however")

SENSES = {
    1: [sense("for", "symbol for that flash", "~의 (상징)", "a symbol for + 명사 = ~의 상징"),
        sense("that", "that flash of inspired genius", "그 (흔히 말하는)", "지시형용사 that + 명사")],
    2: [sense("for", "for other reasons", "~로, ~ 때문에", "for + 이유")],
    3: [sense("that", "system that surrounded it", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("that", "that of any other invention", "그것 (= the importance)", "앞 명사를 되풀이하지 않는 that of ~")],
    4: [sense("to", "to a post-industrial one", "~로", "from A to B = A에서 B로"),
        sense("which", "in which electricity", "그 시대에는 (앞 명사를 꾸밈)", "전치사 + 관계대명사 which + 완전한 문장"),
        sense("to", "to give the twentieth century", "~하여 (결과)", "to부정사 — 결과")],
}

WORDS = {"thomas": "토머스", "edison’s": "에디슨의", "name": "이름", "synonymous": "동의어의", "invention": "발명, 발명품",
         "famous": "유명한", "electric": "전기의", "light": "빛, 전깃불 · light metals = 경금속", "bulb": "전구", "familiar": "친숙한",
         "symbol": "상징", "flash": "번득임", "inspired": "영감을 받은", "genius": "천재성", "traditionally": "전통적으로",
         "associated": "연관된", "inventive": "창의적인", "act": "행위", "besides": "~ 외에도", "being": "~인 것", "exemplar": "표본",
         "bright": "총명한, 밝은", "idea": "아이디어", "however": "그러나 · however + 형용사 = 아무리 ~해도", "worthy": "가치가 있는",
         "study": "연구", "reasons": "이유", "technical": "기술적인", "economic": "경제적인", "importance": "중요성",
         "electrical": "전기의", "system": "시스템", "surrounded": "둘러쌌다", "matches": "~에 필적한다", "invention’s": "발명품의",
         "name’s": "이름의", "could": "~할 수 있었다", "least": "가장 적은 · at least = 적어도", "last": "지난", "hundred": "100",
         "years": "년", "introduction": "도입", "spread": "확산", "power": "전력", "key": "핵심적인", "steps": "단계",
         "transformation": "전환, 탈바꿈", "industrial": "산업의", "age": "시대", "characterized": "특징지어진", "iron": "철",
         "coal": "석탄", "steam": "증기", "post-industrial": "후기 산업의", "electricity": "전기", "joined": "결합된",
         "petroleum": "석유", "metals": "금속", "alloys": "합금", "internal": "내부의", "combustion": "연소", "engines": "기관, 엔진",
         "give": "주다, 부여하다", "twentieth": "20번째의", "century": "세기", "distinctive": "특유한", "form": "형태",
         "character": "특성", "own": "자신의", "time": "시대", "still": "여전히", "largely": "대체로", "carries": "지니고 있다",
         "stamp": "도장, 흔적", "dazzled": "감탄한", "electronic": "전자의", "computerized": "전산화된", "media": "미디어",
         "wonders": "경이", "twenty-first": "21번째의", "world": "세상", "study’s": "연구의"}

STORIES = [
    (2, [sc("문장 1", "💡", "light bulb = inspired genius", "에디슨의 전구는 번득이는 천재성의 상징이에요"),
         sc("문장 2", "🔍", "worthy of study for other reasons", "그것 말고도 연구할 이유가 더 있대요")]),
    (4, [sc("문장 3", "⚖️", "importance matches any other invention", "전깃불과 전기 시스템의 중요성은 어떤 발명품에도 필적해요"),
         sc("문장 4", "⚡", "industrial age → post-industrial one", "전깃불은 철·석탄·증기 시대에서 전기·석유의 20세기로 바뀌는 핵심 단계였어요")]),
]

OPTIONS = [
    ("1", "combines creative ideas from various disciplines", ["combines creative ideas", "various disciplines"],
     "다양한 분야의 창의적인 아이디어를 결합한다", False),
    ("2", "strives to overcome limitations of the industrial age", ["overcome limitations", "industrial age"],
     "산업 시대의 한계를 극복하려고 애쓴다", False),
    ("3", "is a theoretical background for academic exploration", ["theoretical background", "academic exploration"],
     "학문적 탐구를 위한 이론적 배경이다", False),
    ("4", "is under the influence of earlier electrical innovations", ["under the influence", "earlier electrical innovations"],
     "이전의 전기 혁신의 영향 아래 있다", True),
    ("5", "is dependent on resources reserved for future generations", ["dependent on resources", "future generations"],
     "미래 세대를 위해 남겨 둔 자원에 의존한다", False),
]
exam = {
    "question": "밑줄 친 carries the stamp of this age가 다음 글에서 의미하는 바로 가장 적절한 것은?",
    "underline": "carries the stamp of this age", "analysis_first": True, "wrong_rate": 32.0, "wrong_rank": 14,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("combines", "결합하다"), g("creative", "창의적인"), g("various", "다양한"), g("disciplines", "학문 분야"),
                g("strives", "애쓰다"), g("overcome", "극복하다"), g("limitations", "한계"), g("theoretical", "이론적인"),
                g("background", "배경"), g("academic", "학문적인"), g("exploration", "탐구"), g("under the influence of", "~의 영향 아래"),
                g("earlier", "이전의"), g("electrical", "전기의"), g("innovations", "혁신"), g("dependent on", "~에 의존하는"),
                g("resources", "자원"), g("reserved", "남겨 둔"), g("future generations", "미래 세대")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "보기도 다 해석할 필요 없어요. 색칠된 단어만 보고, this age가 어느 시대이고 우리 시대와 어떤 관계인지 떠올리며 골라 봐요.",
        "정답이에요! this age는 전기가 이끈 20세기 후기 산업 시대예요. 우리 시대가 여전히 그 흔적을 지닌다는 건, 앞선 전기 혁신의 영향 아래 있다는 뜻이에요.",
        "정답은 ④예요. 우리 시대는 여전히 앞선 전기 혁신(20세기 전기 시대)의 영향 아래 있다는 말이에요.",
        {"1": "여러 분야의 아이디어를 합친다는 이야기는 글에 없어요.",
         "2": "this age는 산업 시대가 아니라 그다음의 전기 시대예요. 그리고 흔적을 지닌다고 했지, 극복한다고 하지 않았어요.",
         "3": "학문적 탐구의 이론적 배경 이야기는 글에 없어요.",
         "5": "미래 세대를 위한 자원 이야기는 글에 없어요."},
        {"2": review(11,
                     "②는 '산업 시대의 한계를 극복하려 애쓴다'예요. industrial age가 글에 나와서 그럴듯해 보여요. 하지만 this age는 산업 시대 다음의 전기 시대이고, 우리 시대는 그 흔적을 극복하는 게 아니라 지니고 있어요.",
                     "그래서 ②가 아니에요. 어디서 헷갈렸어요?",
                     [("this age를 산업 시대로 봤어요", ["reference"],
                       "알려 줘서 고마워요. this는 바로 앞에서 말한 것을 가리켜요. 앞으로 this가 나오면 앞 문장 끝부터 같이 찾아볼게요."),
                      ("stamp를 극복으로 읽었어요", ["word_meaning"],
                       "알려 줘서 고마워요. carry the stamp of는 '~의 흔적을 지니다'예요. 앞으로 비유 표현은 뜻을 먼저 풀어 줄게요."),
                      ("둘 다요", ["reference", "word_meaning"], "알려 줘서 고마워요. 앞으로 가리키는 말과 비유 표현을 같이 짚어 줄게요.")],
                     panel=rows(("글", "this age = a post-industrial one", "전기·석유의 20세기 — 그 흔적을 지닌다", "hl"),
                                ("②", "industrial age · overcome", "산업 시대 · 극복 (다른 시대, 반대 방향)", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 21번 (밑줄 의미 추론, 3점)",
    topic="밑줄 문제 푸는 법: 핵심 단어 → 관계(산업 시대 → 후기 산업 시대 → 우리 시대) → 밑줄 뜻",
    method={"type": "underline_meaning", "labels": ["핵심 단어 찾기", "관계 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-edison-light.svg", ("Light bulb", "에디슨의 전구"), "→", ("Our time", "우리 시대"),
                                       "전구가 지금 우리와 무슨 상관일까?", "2022년 3월 21번 도입 칠판"),
                      "alt": "칠판: Light bulb(에디슨의 전구) → Our time(우리 시대)", "kind": "drawing"},
            "method": METHOD_IMAGES["underline"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "에디슨 하면 전구가 떠오르죠? 이번 글은 전깃불이 발명의 상징 말고 왜 또 중요한지 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네", "brief": {"say": "수능 문제는 시간 싸움이에요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "밑줄 문제는 핵심 단어 위주로 지문의 요지를 빠르게 파악하면 좋아요."}}],
    exam=exam,
    key_words={"passage": [g("synonymous", "동의어의"), g("inspired", "영감을 받은"), g("genius", "천재성"), g("associated with", "~와 연관된"),
                           g("exemplar", "표본"), g("be worthy of", "~의 가치가 있다"), g("surround", "둘러싸다"), g("match", "~에 필적하다"),
                           g("transformation", "전환, 탈바꿈"), g("characterize", "특징짓다"), g("post-industrial", "후기 산업의"),
                           g("petroleum", "석유"), g("distinctive", "특유한"), g("stamp", "흔적"), g("dazzle", "감탄하게 하다")],
               "options": [g("under the influence of", "~의 영향 아래"), g("innovation", "혁신"), g("strive", "애쓰다"),
                           g("overcome", "극복하다"), g("discipline", "학문 분야")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="밑줄 문제 푸는 법",
       chunks={"The technical and economic importance": "기술적·경제적 중요성", "the electrical system": "전기 시스템",
               "surrounded": "둘러쌌다", "matches": "~에 필적한다", "that of any other invention": "다른 어떤 발명품의 그것(중요성)",
               "the last two hundred years": "지난 200년", "The introduction and spread": "도입과 확산",
               "electric light and power": "전깃불과 전력", "was": "~였다", "one of the key steps": "핵심 단계 중 하나",
               "the transformation of the world": "세상의 전환", "electricity": "전기", "was joined": "결합되었다",
               "Our own time": "우리 자신의 시대", "carries": "지니고 있다", "the stamp of this age": "이 시대의 흔적", "we": "우리는",
               "may be": "~일지도 모른다", "the twenty-first century": "21세기", "the exemplar": "표본, 본보기",
               "Edison’s electric light": "에디슨의 전깃불", "is": "~이다", "worthy": "가치가 있는",
               "is worthy of study": "연구할 가치가 있다", "for other reasons": "다른 이유로"})
