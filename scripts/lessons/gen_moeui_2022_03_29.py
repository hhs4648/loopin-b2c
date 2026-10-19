"""2022년 3월 고3 29번 레슨 + 대사를 만든다 (어법, 3점). 오답률 67.0% · Top 1.

    python3 scripts/lessons/gen_moeui_2022_03_29.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: 어법 유형(틀 문서 없음 — 2024년 3월 29번 선례를 따름, 둘 다 Claude 초안).
푸는 법: 밑줄마다 「무슨 문법을 묻는지」 이름 붙이기 → 그 문장의 뼈대(주어·동사·빈자리)로 확인.
정답이 아닌 밑줄은 「맞아요」로 짚어 밑줄 점검표(rows)에 쌓고, 정답 밑줄(②)은 **구조만** 확인하고
맞다/틀리다는 문제에서 고르게 한다 (2024년 3월 29번·어휘 30번과 같게).

정답 ② as → than (more … than 비교 구문). 해설지: "more가 사용된 비교 구문이므로 as를 than으로 바꿔야 한다."
많이 고른 오답 ③ 24%(동사가 둘로 보인다) · ④ 23%(considered에서 to be가 멀다) — 둘 다 option_review로.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
primer·lyre·coarse는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, choice, show, sv, tip, rows, sense, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)

ID = "moeui-2022-03-29-greek-music"

S = [
    "We don’t know what ancient Greek music sounded like, because there are no examples of it in written or notated form, "
    "nor ①has it survived in oral tradition.",
    "Much of it was probably improvised anyway, within certain rules and conventions.",
    "So we are forced largely to guess at its basis from the accounts of writers such as Plato and Aristotle, who were generally "
    "more concerned with writing about music as a philosophical and ethical exercise ②as with providing a technical primer on its practice.",
    "It seems Greek music was predominantly a vocal form, ③consisting of sung verse accompanied by instruments such as the lyre "
    "or the plucked kithara (the root of ‘guitar’).",
    "In fact, Plato considered music in which the lyre and flute played alone and not as the accompaniment of dance or song "
    "④to be ‘exceedingly coarse and tasteless’.",
    "The melodies seem to have had a very limited pitch range, since the instruments ⑤generally span only an octave, "
    "from one E (as we’d now define it) to the next.",
]
KO = [
    "우리는 고대 그리스 음악이 어떤 소리를 냈는지 알지 못하는데, 그 이유는 그것이 기록되거나 악보에 적힌 형태로 되어 있는 사례가 없고, 구전으로도 살아남지 못했기 때문이다.",
    "어쨌든 그것의 대부분은 아마도 특정 규칙과 관례 내에서 즉흥적으로 연주되었을 것이다.",
    "그래서 우리는 주로 플라톤과 아리스토텔레스와 같은 작가들의 설명으로부터 그것의 토대를 추측할 수밖에 없는데, 그들은 실제에 대한 기술적인 입문서를 "
    "제공하는 것보다 철학적이고 윤리적인 실천으로서의 음악에 대해 글을 쓰는 것에 대체로 더 관심이 있었다.",
    "그리스 음악은 대개 성악 형식이었고, 수금이나 퉁기는 키타라('기타'의 뿌리)와 같은 악기의 반주에 의해 노래되는 운문으로 구성되었던 것으로 보인다.",
    "사실, 플라톤은 춤이나 노래의 반주로서가 아닌 수금과 피리만 연주되는 음악을 '매우 조잡하고 무미건조하다'고 여겼다.",
    "그 선율은 매우 제한된 음역을 가지고 있었던 것으로 보이는데, 왜냐하면 그 악기들은 (우리가 그것을 현재 정의하는 대로) 한 E에서 다음 E까지 단지 한 옥타브에만 걸쳐 있기 때문이다.",
]
UNDER = ["①has", "②as", "③consisting", "④to be", "⑤generally"]

# 밑줄 점검표 — 맞다고 확인한 밑줄만 쌓는다 (정답 밑줄 ②는 끝까지 넣지 않는다)
NAMES = {
    "1": ("① 맞음", "nor has it survived", "부정어 nor가 앞에 와서 조동사 + 주어 순서"),
    "3": ("③ 맞음", "a vocal form, consisting of", "접속사 없이 이어 붙이는 분사(-ing)"),
    "4": ("④ 맞음", "considered music … to be", "consider + 목적어 + to be + 보어"),
    "5": ("⑤ 맞음", "generally span", "동사 span을 꾸미는 부사 generally"),
}


def check(*done):
    return rows(*[(NAMES[d][0], NAMES[d][1], NAMES[d][2], "hl") for d in done])


def r(text, role):
    """끊어읽기를 켜면 같이 보이는 S·V·O·C — 절 안의 것도 같은 진하기로"""
    return {"text": text, "role": role}


sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("We", "우리는"), g("don’t know", "알지 못한다"),
                    g("what ancient Greek music sounded like", "고대 그리스 음악이 어떤 소리였는지"), g("because", "~ 때문에"),
                    g("there are no examples of it", "그것의 사례가 없다"), g("in written or notated form", "기록되거나 악보에 적힌 형태로"),
                    g("nor", "~도 아니다"), g("has it survived", "그것이 살아남았다"), g("in oral tradition", "구전으로")],
        "slashes": ["We don’t know", "sounded like,", "no examples of it", "notated form,", "has it survived"],
        "roles": [r("We", "S"), r("don’t know", "V"), r("what ancient Greek music sounded like", "O"),
                  # because 절·nor 절의 주어·동사도 (2026-10-20 선생님). there are의 주어는 뒤의 no examples of it
                  r("are", "V"), r("no examples of it", "S"), r("has … survived", "V"), r("it", "S")],
        "steps": [
            sv("s1_sv", ["We", "don’t know", "what ancient Greek music sounded like", "there are no examples of it", "has it survived"],
               {"We": "S", "don’t know": "V", "what ancient Greek music sounded like": "O"},
               {"there are no examples of it": "그건 because 뒤 덩어리의 주어·동사예요. 먼저 메인 문장을 봐요.",
                "has it survived": "그건 nor 뒤 덩어리예요. 먼저 메인 문장을 봐요."},
               "주어는 We, 동사는 don’t know, 목적어는 what ancient Greek music sounded like예요. what 덩어리가 '무엇을' 모르는지예요.",
               ask="①이 든 문장이에요. 메인 문장의 주어(S), 동사(V), 목적어(O)를 찾아볼까요?",
               tips=[tip("어법 문제 요령", "밑줄마다 '무슨 문법을 묻는지' 먼저 이름을 붙여요(어순, 동사의 수, 부사/형용사, 분사, 관계사 뒤 빈자리 …). 그다음 그 문장의 뼈대로 확인해요.")]),
            choice("s1_nor",
                   "①has it survived를 봐요. 동사 has가 주어 it보다 앞에 나왔어요. 무엇 때문일까요?",
                   [("o0", "앞에 온 부정어 nor 때문에 어순이 바뀌어서", True),
                    ("o1", "현재완료는 늘 동사가 주어보다 앞에 와서", False),
                    ("o2", "it이 주어가 아니라 목적어라서", False)],
                   "바로 앞 nor는 '~도 아니다'예요. 부정하는 말이 문장 앞에 오면 어순이 달라져요.",
                   why="nor처럼 부정하는 말이 앞에 오면 의문문처럼 '조동사 + 주어 + 동사' 순서가 돼요. 그래서 ①has it survived는 맞아요.",
                   highlight=["nor", "has it survived"],
                   tips=[tip("부정어 + 조동사 + 주어", "nor·neither·never처럼 부정하는 말이 문장 앞에 오면 '조동사 + 주어 + 동사' 순서가 돼요. nor has it survived = 그것도 살아남지 못했다.", "nor")],
                   point="① 부정어 nor가 앞에 와서 조동사 + 주어 어순 → has it survived 맞음"),
            show("s1_check", "①has는 맞아요. 밑줄 점검표에 붙여 둘게요.", panel=check("1"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("Much of it", "그것의 많은 부분이"), g("was probably improvised", "아마 즉흥 연주였다"), g("anyway", "어쨌든"),
                    g("within certain rules and conventions", "특정 규칙과 관례 안에서")],
        "slashes": ["improvised anyway,"],
        "roles": [r("Much of it", "S"), r("was probably improvised", "V")],
        "steps": [
            show("s2_improvised", "악보가 없던 이유가 하나 더 있어요. 대부분 정해진 규칙 안에서 즉흥 연주였대요.",
                 highlight=["improvised"], button="다음 문장",
                 tips=[tip("improvise", "악보 없이 그 자리에서 즉흥으로 연주하는 거예요.", "improvised")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("So", "그래서"), g("we", "우리는"), g("are forced", "~할 수밖에 없다"), g("largely", "주로"),
                    g("to guess at its basis", "그 토대를 추측하도록"), g("from the accounts of writers", "작가들의 설명으로부터"),
                    g("such as Plato and Aristotle", "플라톤과 아리스토텔레스 같은"), g("who", "(그 작가들을 가리킴)"),
                    g("were generally more concerned with", "대체로 ~에 더 관심이 있었다"), g("writing about music", "음악에 대해 글 쓰는 것"),
                    g("as a philosophical and ethical exercise", "철학적이고 윤리적인 실천으로서"), g("as with", "~와 (견주어)"),
                    g("providing a technical primer on its practice", "실제에 대한 기술적인 입문서를 제공하는 것")],
        "slashes": ["forced largely", "guess at its basis", "accounts of writers", "and Aristotle,", "concerned with",
                    "writing about music", "ethical exercise", "technical primer"],
        "roles": [r("we", "S"), r("are forced", "V"), r("to guess at its basis", "O"), r("who", "S"), r("were generally more concerned with", "V")],
        "steps": [
            sv("s3_sv", ["we", "are forced", "to guess at its basis", "who", "were generally more concerned with"],
               {"we": "S", "are forced": "V", "to guess at its basis": "O"},
               {"who": "그건 앞의 작가들을 가리키며 꾸미는 덩어리의 시작이에요.",
                "were generally more concerned with": "그건 who 뒤 덩어리의 동사예요. 먼저 메인 문장을 봐요."},
               "주어는 we, 동사는 are forced, 그 뒤 to guess at its basis가 '무엇을 하도록' 강요받는지예요. 콤마 뒤 who부터는 작가들을 꾸며 줘요.",
               ask="아주 긴 문장이에요. 메인 문장의 주어(S), 동사(V), 목적어(O)를 찾아볼까요?"),
            choice("s3_more",
                   "who 뒤를 봐요. 'more concerned with A ②as with B'로 두 가지를 견주는데, 작가들이 더 관심 있던 쪽은 어디일까요?",
                   [("o0", "음악에 대해 철학적·윤리적으로 글 쓰는 것", True),
                    ("o1", "음악을 실제로 연주하는 기술적인 입문서를 제공하는 것", False),
                    ("o2", "두 쪽에 똑같이 관심이 있었다", False)],
                   "more concerned with 바로 뒤에 오는 쪽이 '더' 관심 있던 쪽이에요.",
                   why="'more concerned with writing about music …', 음악을 철학·윤리의 실천으로 보고 글 쓰는 쪽에 더 관심이 있었대요. 연주 기술 입문서 쪽이 아니고요.",
                   highlight=["more concerned with", "writing about music"],
                   point="작가들은 음악을 철학·윤리로 다루는 글쓰기에 더 관심 — 연주 기술 입문서 쪽이 아니다"),
            show("s3_hold",
                 "여기서 more는 두 가지를 견주는 말이에요. 견줄 때 more와 짝을 이루는 말이 무엇인지 떠올리며, ②가 그 짝으로 맞는지는 문제에서 골라 봐요.",
                 highlight=["more concerned with", "as with"], button="다음 문장",
                 tips=[tip("more A than B", "두 가지를 견줄 때 '더'는 more, 견주는 대상은 than으로 이어요. more concerned with A than with B = B보다 A에 더 관심이 있다.", "more")],
                 point="② more가 견주는 짝 — 비교 구문의 짝이 맞는지 문제에서 확인"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("It seems", "~인 것 같다"), g("Greek music was predominantly a vocal form", "그리스 음악은 대개 성악 형식이었다"),
                    g("consisting of sung verse", "노래되는 운문으로 구성된"), g("accompanied by instruments", "악기의 반주를 받는"),
                    g("such as the lyre", "수금 같은"), g("or the plucked kithara", "또는 퉁기는 키타라"),
                    g("(the root of ‘guitar’)", "('기타'의 뿌리)")],
        "slashes": ["It seems", "vocal form,", "sung verse", "accompanied by instruments", "plucked kithara"],
        "roles": [r("It", "S"), r("seems", "V"), r("Greek music", "S"), r("was", "V"), r("a vocal form", "C")],
        "steps": [
            choice("s4_consisting",
                   "콤마 앞에 이미 동사 was가 있어요. ③자리에 동사 consisted를 그냥 쓸 수 있을까요?",
                   [("o0", "쓸 수 없다 — 접속사 없이 동사를 둘 쓸 수 없어서 -ing로 이어 준다", True),
                    ("o1", "쓸 수 있다 — 콤마가 접속사 역할을 해서", False),
                    ("o2", "쓸 수 있다 — 주어가 같으면 동사를 두 번 써도 돼서", False)],
                   "한 문장에 동사를 둘 쓰려면 and 같은 접속사가 있어야 해요.",
                   why="접속사가 없으니 동사를 둘 쓸 수 없어요. 그래서 -ing(분사) consisting으로 이어 줘요. ③은 맞아요.",
                   highlight=["was", "consisting"],
                   tips=[tip("분사로 이어 붙이기", "접속사 없이 문장을 이어 붙일 때 동사를 -ing로 바꿔요. a vocal form, consisting of … = 성악 형식이었고, …로 구성되었다.", "consisting")],
                   point="③ 접속사 없이 이어 붙이는 자리 → 분사 consisting 맞음"),
            show("s4_check", "③consisting도 맞아요.", panel=check("1", "3"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("In fact", "사실"), g("Plato", "플라톤은"), g("considered", "여겼다"), g("music", "음악을"),
                    g("in which", "그 안에서"), g("the lyre and flute", "수금과 피리가"), g("played alone", "홀로 연주되는"),
                    g("and not as the accompaniment of dance or song", "춤이나 노래의 반주로서가 아니라"),
                    g("to be ‘exceedingly coarse and tasteless’", "'매우 조잡하고 무미건조하다'고")],
        "slashes": ["In fact,", "considered music", "played alone", "dance or song"],
        "roles": [r("Plato", "S"), r("considered", "V"), r("music", "O"), r("the lyre and flute", "S"), r("played", "V"), r("to be ‘exceedingly coarse and tasteless’", "C")],
        "steps": [
            sv("s5_sv", ["Plato", "considered", "music", "the lyre and flute", "played alone"],
               {"Plato": "S", "considered": "V", "music": "O"},
               {"the lyre and flute": "그건 in which 뒤, 음악을 꾸미는 덩어리의 주어예요.",
                "played alone": "그건 in which 뒤 덩어리의 동사예요. 먼저 메인 문장을 봐요."},
               "주어는 Plato, 동사는 considered, 목적어는 music이에요. in which부터 긴 덩어리가 그 music을 꾸며요.",
               ask="메인 문장의 주어(S), 동사(V), 목적어(O)를 찾아볼까요?"),
            choice("s5_tobe",
                   "④to be 뒤의 '매우 조잡하고 무미건조하다'는 무엇을 두고 한 말일까요?",
                   [("o0", "플라톤이 여긴 그 음악 (music)", True), ("o1", "춤이나 노래 (dance or song)", False),
                    ("o2", "플라톤 자신 (Plato)", False)],
                   "considered의 목적어가 무엇이었는지 떠올려 봐요. to be는 그 목적어가 어떻다는 말이에요.",
                   why="considered의 목적어가 music이니, to be 뒤는 그 음악이 어떻다는 말이에요. 수금과 피리만 연주되는 음악을 조잡하다고 여긴 거예요.",
                   highlight=["considered", "music", "to be ‘exceedingly coarse and tasteless’"],
                   tips=[tip("consider + 목적어 + to be", "'~을 …라고 여기다'예요. 목적어가 길면 to be가 멀리 떨어져 보여요. considered music … to be coarse = 그 음악을 조잡하다고 여겼다.", "to be")],
                   point="④ consider + 목적어(music) + to be + 보어 → to be 맞음 (목적어가 길어 멀리 떨어져 보인다)"),
            show("s5_check", "④to be도 맞아요. 목적어가 길어서 멀어 보였을 뿐이에요.", panel=check("1", "3", "4"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("The melodies", "그 선율은"), g("seem to have had", "가지고 있었던 것 같다"),
                    g("a very limited pitch range", "매우 제한된 음역을"), g("since", "~ 때문에"), g("the instruments", "그 악기들은"),
                    g("generally span", "일반적으로 걸쳐 있다"), g("only an octave", "단지 한 옥타브에만"), g("from one E", "한 E에서"),
                    g("(as we’d now define it)", "(우리가 지금 정의하는 대로)"), g("to the next", "다음 E까지")],
        "slashes": ["seem to have had", "pitch range,", "since the instruments", "an octave,", "from one E", "define it)"],
        "roles": [r("The melodies", "S"), r("seem to have had", "V"), r("a very limited pitch range", "O"), r("the instruments", "S"), r("span", "V")],
        "steps": [
            choice("s6_adverb",
                   "⑤generally는 바로 뒤의 span(걸쳐 있다)을 꾸며요. 동사를 꾸미는 말은 무엇이어야 할까요?",
                   [("o0", "부사 (generally)", True), ("o1", "형용사 (general)", False), ("o2", "명사 (generality)", False)],
                   "동사를 꾸미는 건 형용사가 아니에요.",
                   why="동사를 꾸미는 말은 부사예요. 그래서 generally가 맞아요. 형용사 general은 명사를 꾸밀 때 써요.",
                   highlight=["generally", "span"],
                   point="⑤ 동사 span을 꾸미는 자리 → 부사 generally 맞음"),
            show("s6_go",
                 "①③④⑤는 모두 맞았어요. 남은 하나, ②를 다시 떠올리며 문제를 골라 봐요.",
                 panel=check("1", "3", "4", "5"), panel_below=True, button="문제 풀러 갈게요"),
        ],
    },
]

SENSES = {
    3: [sense("so", "So we are forced", "그래서", "접속사 so (문장 앞, 결과)"),
        sense("to", "to guess", "~하도록", "be forced + to부정사"),
        sense("as", "such as Plato", "~ 같은", "such as + 예시"),
        sense("as", "as a philosophical and ethical exercise", "~로서", "전치사 as (자격·역할)"),
        sense("as", "as with providing", "~와 (견주어)", "비교 대상을 잇는 자리 — more와 짝이 맞는지 보기")],
    4: [sense("as", "such as the lyre", "~ 같은", "such as + 예시")],
    5: [sense("which", "in which the lyre and flute played", "그 안에서 (앞 명사를 꾸밈)", "전치사 + 관계대명사 (뒤 문장이 완전하다)"),
        sense("as", "as the accompaniment", "~로서", "전치사 as (자격·역할)"),
        sense("to", "to be", "~라고 (여기다)", "consider + 목적어 + to be + 보어")],
    6: [sense("to", "seem to have had", "~한 (것 같다)", "seem + to부정사 (완료형 to have + p.p.)"),
        sense("since", "since the instruments", "~ 때문에", "접속사 since (이유)"),
        sense("as", "as we’d now define it", "~하는 대로", "접속사 as (방식)"),
        sense("to", "to the next", "~까지", "from A to B")],
}

WORDS = {
    "ancient": "고대의", "greek": "그리스의", "music": "음악", "sounded": "소리가 났다", "like": "~처럼", "examples": "사례",
    "written": "기록된", "notated": "악보에 적힌", "form": "형태", "survived": "살아남았다", "oral": "입으로 전하는",
    "tradition": "전통 · oral tradition = 구전", "much": "많은 부분", "probably": "아마", "improvised": "즉흥 연주되었다",
    "anyway": "어쨌든", "certain": "특정한", "rules": "규칙", "conventions": "관례", "forced": "강요받는", "largely": "주로",
    "guess": "추측하다", "basis": "토대", "accounts": "설명", "writers": "작가들", "plato": "플라톤", "aristotle": "아리스토텔레스",
    "generally": "일반적으로, 대체로", "concerned": "관심이 있는 · be concerned with = ~에 관심이 있다", "writing": "글 쓰는 것",
    "philosophical": "철학적인", "ethical": "윤리적인", "exercise": "실천, 활동", "providing": "제공하는 것", "technical": "기술적인",
    "primer": "입문서", "practice": "실제, 실천", "seems": "~인 것 같다", "predominantly": "대개", "vocal": "목소리의, 성악의",
    "consisting": "구성된 · consist of = ~로 구성되다", "sung": "노래되는", "verse": "운문", "accompanied": "반주를 받는",
    "instruments": "악기", "lyre": "수금(현악기)", "plucked": "퉁기는", "kithara": "키타라(옛 현악기)", "root": "뿌리",
    "guitar": "기타", "fact": "사실 · in fact = 사실", "considered": "여겼다", "flute": "피리", "played": "연주되었다",
    "alone": "홀로", "accompaniment": "반주", "dance": "춤", "song": "노래", "exceedingly": "매우", "coarse": "조잡한",
    "tasteless": "무미건조한, 멋없는", "melodies": "선율", "seem": "~인 것 같다", "limited": "제한된", "pitch": "음(높이)",
    "range": "범위 · pitch range = 음역", "span": "걸쳐 있다", "octave": "옥타브", "define": "정의하다", "next": "다음 것",
    "e": "E (음 이름 '미')", "we’d": "우리가 ~하는 (we would)",
}

exam = {
    "question": "다음 글의 밑줄 친 부분 중, 어법상 틀린 것은? [3점]",
    "underline": UNDER, "sentence": 3, "analysis_first": True,
    "wrong_rate": 67.0, "wrong_rank": 1,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("has", "(현재완료의 조동사)"), g("as", "~와 (견주어)"), g("consisting", "구성된"), g("to be", "~라고 (여기다)"),
                g("generally", "일반적으로")],
    "options": [{"id": str(i + 1), "label": u[1:], "keywords": [u[1:]], **({"correct": True} if i == 1 else {})}
                for i, u in enumerate(UNDER)],
    "brief": exam_brief(
        "밑줄 점검표를 떠올리며, 어법상 틀린 하나를 골라 봐요.",
        "정답이에요! more로 두 가지를 견줬으니 짝이 되는 말은 than이어야 해요. ②as with → than with로 고쳐요.",
        "정답은 ②예요. 'more concerned with A … as with B'에서 more와 짝을 이루는 말은 than이에요. as with를 than with로 고쳐요.",
        {"1": "부정어 nor가 앞에 와서 '조동사 + 주어' 순서가 된 거라 ①has it survived는 맞아요.",
         "3": "앞에 이미 동사 was가 있어서 접속사 없이 이어 붙이려면 -ing가 와야 해요. ③consisting은 맞아요.",
         "4": "consider + 목적어 + to be + 보어예요. 목적어 music이 길어서 멀어 보일 뿐 ④to be는 맞아요.",
         "5": "동사 span을 꾸미는 자리라 부사 ⑤generally가 맞아요."},
        {"3": review(24,
                     "③ 앞에는 이미 동사 was가 있어서 '동사가 둘'로 보여요. 하지만 접속사 없이 문장을 이어 붙일 때는 동사를 -ing(분사)로 바꿔요. 그래서 consisting이 맞아요.",
                     "그래서 ③이 아니에요. 어디서 헷갈렸어요?",
                     [("동사가 둘이라 틀린 것 같았어요", ["participle"],
                       "알려 줘서 고마워요. 접속사가 없으면 뒤 동사는 -ing가 돼요. 앞으로 분사로 이어 붙이는 자리를 먼저 짚어 줄게요."),
                      ("consisting of 뜻을 몰랐어요", ["vocab"],
                       "알려 줘서 고마워요. consist of는 '~로 구성되다'예요. 앞으로 이런 숙어를 먼저 알려 줄게요."),
                      ("둘 다요", ["participle", "vocab"],
                       "알려 줘서 고마워요. 앞으로 분사 자리와 숙어를 같이 짚어 줄게요.")],
                     panel=rows(("앞", "a vocal form", "콤마 앞 — 이미 동사 was가 있다", "hl"),
                                ("뒤", "consisting of sung verse", "접속사가 없으니 -ing로 이어 붙인다", "hl2"))),
         "4": review(23,
                     "④to be는 considered와 멀리 떨어져 있어서 어색해 보여요. 목적어 music 뒤에 in which 덩어리가 길게 붙어서 그래요. consider + 목적어 + to be + 보어 모양이라 ④는 맞아요.",
                     "그래서 ④가 아니에요. 어디서 헷갈렸어요?",
                     [("considered와 to be가 멀어서 헷갈렸어요", ["long_object"],
                       "알려 줘서 고마워요. 목적어가 길면 보어가 멀어져요. 앞으로 긴 목적어를 먼저 묶어서 보여 줄게요."),
                      ("consider 뒤에 to be가 오는 걸 몰랐어요", ["verb_pattern"],
                       "알려 줘서 고마워요. consider + 목적어 + to be + 보어는 '~을 …라고 여기다'예요. 앞으로 동사 모양을 먼저 알려 줄게요."),
                      ("둘 다요", ["long_object", "verb_pattern"],
                       "알려 줘서 고마워요. 앞으로 긴 목적어와 동사 모양을 같이 짚어 줄게요.")],
                     panel=rows(("여긴 사람", "Plato considered", "주어 + 동사", "hl"),
                                ("여긴 대상", "music in which … dance or song", "목적어 — in which 덩어리가 길게 꾸민다", "hl2"),
                                ("여긴 어떻다", "to be ‘exceedingly coarse and tasteless’", "그 목적어가 어떻다는 보어", "hl")))}),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 29번 (어법, 3점)",
    topic="어법 푸는 법: 밑줄마다 무슨 문법을 묻는지 이름 붙이기 → 그 문장 뼈대(주어·동사·빈자리)로 확인",
    method={"type": "grammar", "labels": ["묻는 문법 이름 붙이기", "뼈대로 확인"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-greek-music.svg", ("Greek music", "고대 그리스 음악"), "?",
                                       ("No notation", "악보도 기록도 없음"),
                                       "그러면 어떤 소리였는지 어떻게 짐작할까?", "2022년 3월 29번 도입 칠판"),
                      "alt": "칠판: Greek music(고대 그리스 음악) ? No notation(악보도 기록도 없음)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "고대 그리스 음악은 어떤 소리였을까요? 악보도 녹음도 남아 있지 않아서, 글로 남은 설명으로 짐작할 수밖에 없대요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "어법 문제는 밑줄마다 무슨 문법을 묻는지 먼저 이름을 붙여요. 그다음 그 문장의 주어·동사·빈자리로 하나씩 확인할게요."}}],
    exam=exam,
    key_words={"passage": [g("notate", "악보에 적다"), g("oral tradition", "구전"), g("improvise", "즉흥 연주하다"),
                           g("convention", "관례, 관행"), g("account", "설명"), g("be concerned with", "~에 관심이 있다"),
                           g("philosophical", "철학적인"), g("predominantly", "대개"), g("consist of", "~로 구성되다"),
                           g("verse", "운문"), g("accompany", "반주하다"), g("accompaniment", "반주"), g("exceedingly", "매우"),
                           g("tasteless", "무미건조한"), g("pitch range", "음역"), g("span", "걸쳐 있다")],
               "options": []},
    sentences=sentences, concept="medium")

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="어법 푸는 법",
       chunks={"We": "우리는", "don’t know": "알지 못한다",
               "what ancient Greek music sounded like": "고대 그리스 음악이 어떤 소리였는지",
               "there are no examples of it": "그것의 사례가 없다", "has it survived": "그것이 살아남았다",
               "we": "우리는", "are forced": "~할 수밖에 없다", "to guess at its basis": "그 토대를 추측하도록",
               "who": "(앞의 작가들을 가리킴)", "were generally more concerned with": "대체로 ~에 더 관심이 있었다",
               "Plato": "플라톤은", "considered": "여겼다", "music": "음악을", "the lyre and flute": "수금과 피리가",
               "played alone": "홀로 연주되는"})
