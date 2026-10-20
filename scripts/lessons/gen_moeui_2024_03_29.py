"""2024년 3월 고3 29번 레슨 + 대사를 만든다 (어법, 2점). 오답률 자료 없음(Top 15 밖).

    python3 scripts/lessons/gen_moeui_2024_03_29.py   (→ npm run policy:copy stamp <id> → npm run build)

어법 유형은 처음 — Claude 초안(2026-10-18, 미니 모의고사 연결용). 푸는 법: 밑줄마다 「무슨 문법을 묻는지」 이름 붙이기 →
그 문장의 뼈대(주어·동사·빈자리)로 확인. 정답이 아닌 밑줄은 「맞아요」로 짚고, 정답 밑줄(④)은 구조만 확인하고
맞다/틀리다는 문제에서 고르게 한다(어휘 30번과 같게). 정답 ④ which → into which. 해설지와 대조함.
ambivalence는 시험지 아래 *로 풀어 준 단어(핵심어 아님). 밑줄이 없는 문장은 읽고 넘어간다.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, finish)

ID = "moeui-2024-03-29-crossing-cultures"

S = [
    "The process of crossing cultures challenges the very basis of who we are as cultural beings.",
    "It offers opportunities for new learning and growth.",
    "Being “uprooted” from our home ①brings us understanding not only of the people and their culture in our new environment, but of ourselves and our home culture.",
    "Although the difficulties that can arise from crossing cultures are often shocking, success stories are everywhere.",
    "Despite, or rather because of, the suffering and ambivalence we undergo when we cross cultures, we gradually find ourselves ②uniquely privileged to define ourselves and others anew with clarity and insight that we could not have cultivated without leaving home.",
    "③Adapting to a new and unfamiliar culture, then, is more than survival.",
    "It is a life-changing journey.",
    "It is a process of “becoming”—personal reinvention, transformation, growth, reaching out beyond the boundaries of our own existence.",
    "The process does not require that we abandon our former personalities and the cultures ④which we were born.",
    "Rather, it compels us to find ⑤ourselves as if for the first time, particularly those “cultural invariants” within us—aspects that we hold dear and refuse to compromise.",
]
KO = [
    "문화를 넘어가는 과정은 문화적 존재로서 우리가 누구인지에 대한 바로 그 기반에 도전한다.",
    "그것은 새로운 배움과 성장을 위한 기회를 제공한다.",
    "우리의 고향에서 '뿌리째 뽑히는' 것은 우리의 새로운 환경에 있는 사람들과 그들의 문화뿐만 아니라 우리 자신과 우리의 고향 문화에 대한 이해도 가져다준다.",
    "비록 문화를 넘어가는 것에서 발생할 수 있는 어려움이 흔히 충격적이더라도, 성공담은 어디에나 있다.",
    "우리가 문화를 넘어가면서 겪는 고통, 그리고 상반되는 감정에도 불구하고, 혹은 오히려 이것 때문에, 우리는 고향을 떠나지 않고는 기를 수 없었던 명확성과 통찰력으로 우리 자신과 다른 사람들을 새롭게 정의할 수 있는 특권을 특별히 누리고 있다는 것을 점차 알게 된다.",
    "새롭고 낯선 문화에 적응하는 것은, 그러니까, 생존 그 이상이다.",
    "그것은 삶을 바꾸는 여정이다.",
    "그것은 개인적인 재창조, 변화, 성장, 우리 자신의 존재의 경계 너머로 뻗어가는 '되어가는 것'의 과정이다.",
    "그 과정은 우리가 우리 이전의 개성과 우리가 태어난 문화를 버릴 것을 요구하지 않는다.",
    "오히려, 그것은 우리로 하여금 우리 자신을, 특히 우리 내면의 그 '문화의 불변하는 것들', 우리가 소중히 여기고 타협하기를 거부하는 측면들을 마치 처음인 것처럼 발견할 것을 강요한다.",
]
UNDER = ["①brings", "②uniquely", "③Adapting", "④which", "⑤ourselves"]


def check(*done):
    names = {"1": ("① 맞음", "Being uprooted … brings", "동명사 주어 = 단수 → brings"),
             "2": ("② 맞음", "find ourselves uniquely privileged", "형용사 privileged를 꾸미는 부사 uniquely"),
             "3": ("③ 맞음", "Adapting … is", "주어 자리 동명사 Adapting"),
             "5": ("⑤ 맞음", "compels us to find ourselves", "찾는 사람 us = 찾는 대상 → 재귀대명사 ourselves")}
    return rows(*[(names[d][0], names[d][1], names[d][2], "hl") for d in done])


sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "low",
        "glosses": [g("The process of crossing cultures", "문화를 넘어가는 과정"), g("challenges", "~에 도전하다, 흔들다"),
                    g("the very basis", "바로 그 기반"), g("of who we are", "우리가 누구인지의"), g("as cultural beings", "문화적 존재로서")],
        "slashes": ["crossing cultures", "the very basis"],
        "roles": [r("The process of crossing cultures", "S"), r("challenges", "V"), r("the very basis", "O")],
        "steps": [
            show("s1_topic", "문화를 넘어가면(다른 나라 문화 속으로 가면) 내가 누구인지의 바탕이 흔들린대요. 이 글의 이야기예요.",
                 highlight=["crossing cultures"], button="다음 문장",
                 tips=[tip("어법 문제 요령", "밑줄마다 '무슨 문법을 묻는지' 먼저 이름 붙여요(주어-동사 수, 부사/형용사, 동명사 주어, 관계사 뒤 빈자리, 재귀대명사 …). 그다음 그 문장 뼈대로 확인해요.")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("It offers", "그것은 준다"), g("opportunities", "기회"), g("for new learning and growth", "새로운 배움과 성장을 위한")],
        "slashes": ["offers opportunities"],
        "roles": [r("It", "S"), r("offers", "V"), r("opportunities", "O")],
        "steps": [show("s2_offer", "그 과정은 새로 배우고 자랄 기회를 준대요.", highlight=["opportunities"], button="다음 문장")],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("Being “uprooted” from our home", "고향에서 '뿌리째 뽑히는' 것"), g("Being", "~되는 것"), g("uprooted", "뿌리째 뽑힌"),
                    g("brings", "가져다준다"), g("us", "우리에게"), g("understanding", "이해"),
                    g("not only of the people and their culture", "사람들과 그들의 문화뿐만 아니라"), g("in our new environment", "새 환경의"),
                    g("but of ourselves and our home culture", "우리 자신과 고향 문화에 대한 것도")],
        "slashes": ["from our home", "us understanding", "and their culture", "new environment,"],
        "roles": [r("Being “uprooted” from our home", "S"), r("brings", "V"), r("understanding", "O")],
        "steps": [
            sv("s3_sv", ["Being “uprooted” from our home", "brings", "us", "understanding"],
               {"Being “uprooted” from our home": "S", "brings": "V", "understanding": "O"},
               {"us": "그건 '누구에게' 주는지예요(간접목적어). 무엇을 주는지 찾아봐요."},
               "주어는 Being “uprooted” from our home(고향에서 뿌리째 뽑히는 것), 동사는 ①brings, 목적어는 understanding이에요.",
               ask="①이 든 문장이에요. 주어(S), 동사(V), 목적어(O)를 찾아볼까요?"),
            choice("s3_number",
                   "주어 Being “uprooted” …는 '~되는 것'이라는 동명사 덩어리예요. 동사는 단수형일까요, 복수형일까요?",
                   [("o0", "단수형 (brings)", True), ("o1", "복수형 (bring)", False)],
                   "동명사(-ing) 덩어리가 주어면 '하나의 일'로 봐요.",
                   why="동명사 덩어리 주어는 '하나의 일'이라 단수 취급해요. 그래서 brings가 맞아요. 바로 앞 home은 from 뒤 명사라 주어가 아니에요.",
                   highlight=["Being", "brings"],
                   tips=[tip("동명사 주어 = 단수", "Being …, Adapting …처럼 -ing 덩어리가 주어면 단수 동사(is, brings)를 써요.", "Being")],
                   point="① 동명사 주어(Being uprooted …)는 단수 → brings 맞음"),
            show("s3_check", "①brings는 맞아요. 밑줄 점검표에 붙여 둘게요.", panel=check("1"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "low",
        "glosses": [g("Although", "비록 ~이지만"), g("the difficulties", "어려움"), g("that can arise from crossing cultures", "문화를 넘어가며 생길 수 있는"),
                    g("are often shocking", "흔히 충격적이다"), g("success stories", "성공담"), g("are everywhere", "어디에나 있다")],
        "slashes": ["the difficulties", "crossing cultures", "often shocking,"],
        "roles": [r("the difficulties", "S"), r("are … are", "V"), r("shocking", "C"), r("success stories", "S")],
        "modifiers": ["that can arise from crossing cultures"],
        "steps": [show("s4_success", "어려움은 충격적이지만 성공한 이야기도 어디에나 있대요.", highlight=["success stories"], button="다음 문장")],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Despite, or rather because of", "~에도 불구하고, 아니 오히려 ~ 때문에"), g("the suffering and ambivalence", "고통과 상반된 감정"),
                    g("we undergo", "우리가 겪는"), g("when we cross cultures", "문화를 넘어갈 때"), g("we", "우리는"), g("gradually", "점점"),
                    g("find", "알게 되다"), g("ourselves", "우리 자신을"), g("uniquely", "특별히, 남다르게"), g("privileged", "특권을 누리는"),
                    g("to define ourselves and others anew", "우리와 남을 새롭게 정의할"), g("with clarity and insight", "명확함과 통찰로"),
                    g("that we could not have cultivated", "우리가 기를 수 없었을"), g("without leaving home", "고향을 떠나지 않고는")],
        "slashes": ["Despite,", "because of,", "and ambivalence", "we undergo", "cross cultures,", "we gradually find ourselves",
                    "uniquely privileged", "ourselves and others anew", "clarity and insight", "cultivated"],
        "roles": [r("we … we … we … we", "S"), r("undergo", "V"), r("cross", "V"), r("find", "V"), r("ourselves", "O"), r("privileged", "C"),
                  r("could not have cultivated", "V")],
        "modifiers": ["we undergo when we cross cultures", "that we could not have cultivated without leaving home"],
        "steps": [
            sv("s5_sv", ["the suffering and ambivalence", "we", "find", "ourselves", "privileged"],
               {"we": "S", "find": "V", "ourselves": "O", "privileged": "C"},
               {"the suffering and ambivalence": "그건 Despite / because of 뒤 덩어리예요. 콤마 뒤 메인 문장에서 찾아봐요."},
               "콤마 뒤 메인 문장은 주어 we, 동사 find, 목적어 ourselves, 보어 (uniquely) privileged예요. find + O + C = O가 C하다는 걸 알게 되다.",
               ask="길어요. 콤마 뒤 메인 문장에서 주어(S), 동사(V), 목적어(O), 보어(C)를 모두 찾아볼까요?"),
            choice("s5_adverb",
                   "②uniquely는 바로 뒤 privileged(특권을 누리는)를 꾸며요. privileged가 형용사라면, 꾸미는 말은 무엇이어야 할까요?",
                   [("o0", "형용사 (unique)", False), ("o1", "부사 (uniquely)", True)],
                   "형용사를 꾸미는 건 부사예요. very happy의 very처럼요.",
                   why="형용사(privileged)를 꾸미는 건 부사예요. 그래서 uniquely가 맞아요. privileged 자체는 find의 보어라 형용사가 맞고요.",
                   highlight=["uniquely", "privileged"],
                   tips=[tip("find + O + 형용사", "find oneself privileged = 자신이 특권을 누린다는 걸 알게 되다. 보어 자리는 형용사, 그 형용사를 꾸미는 건 부사예요.", "find")],
                   point="② 형용사 privileged를 꾸미는 부사 uniquely → 맞음"),
            show("s5_check", "②uniquely는 맞아요.", panel=check("1", "2"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Adapting to a new and unfamiliar culture", "새롭고 낯선 문화에 적응하는 것"), g("Adapting", "적응하는 것"),
                    g("then", "그러니까"), g("is", "~이다"), g("more than survival", "생존 그 이상")],
        "slashes": ["unfamiliar culture,", "then,"],
        "roles": [r("Adapting to a new and unfamiliar culture", "S"), r("is", "V"), r("more than survival", "C")],
        "steps": [
            choice("s6_subject",
                   "③Adapting to a new and unfamiliar culture는 이 문장에서 무슨 역할일까요?",
                   [("o0", "동사 is의 주어", True), ("o1", "앞 문장을 꾸미는 말", False), ("o2", "is 뒤의 보어", False)],
                   "뒤에 동사 is가 있어요. is 앞에 무엇이 있어야 할까요?",
                   why="뒤에 동사 is가 있으니 그 앞 덩어리가 주어예요. 주어 자리엔 동명사(-ing) Adapting이 올 수 있어요. 그래서 ③은 맞아요.",
                   highlight=["Adapting to a new and unfamiliar culture", "is"],
                   point="③ 동사 is의 주어 자리 → 동명사 Adapting 맞음"),
            show("s6_check", "③Adapting은 맞아요.", panel=check("1", "2", "3"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "low",
        "glosses": [g("It is", "그것은 ~이다"), g("a life-changing journey", "삶을 바꾸는 여정")],
        "roles": [r("It", "S"), r("is", "V"), r("a life-changing journey", "C")],
        "steps": [show("s7_journey", "문화에 적응하는 건 삶을 바꾸는 여정이래요.", highlight=["life-changing"], button="다음 문장")],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "low",
        "glosses": [g("It is a process of “becoming”", "그것은 '되어 가는' 과정이다"), g("personal reinvention", "개인의 재창조"),
                    g("transformation", "변화"), g("growth", "성장"), g("reaching out beyond the boundaries", "경계 너머로 뻗어 가는 것"),
                    g("of our own existence", "우리 자신의 존재의")],
        "slashes": ["of “becoming”—", "transformation, growth,", "the boundaries"],
        "roles": [r("It", "S"), r("is", "V"), r("a process", "C")],
        "steps": [show("s8_becoming", "대시(—) 뒤는 '되어 가는 과정'을 풀어 쓴 말이에요. 앞을 이해했으면 가볍게 넘어가도 돼요.",
                       highlight=["“becoming”"], button="다음 문장")],
    },
    {
        "id": 9, "text": S[8], "model_translation": KO[8], "teaching_value": "high",
        "glosses": [g("The process", "그 과정은"), g("does not require", "요구하지 않는다"), g("that we abandon", "우리가 버리는 것을"),
                    g("our former personalities", "이전의 성격"), g("the cultures", "문화들"), g("which", "(그) ~하는"),
                    g("we were born", "우리가 태어났다"), g("abandon", "버리다")],
        "slashes": ["does not require", "former personalities"],
        "roles": [r("The process", "S"), r("does not require", "V"), r("we", "S"), r("abandon", "V"),
                  r("our former personalities and the cultures", "O")],
        "modifiers": ["which we were born"],
        "steps": [
            sv("s9_sv", ["The process", "does not require", "we", "abandon", "our former personalities and the cultures"],
               {"The process": "S", "does not require": "V"},
               {"we": "그건 that 뒤 덩어리 안의 주어예요.", "abandon": "그건 that 뒤 덩어리 안의 동사예요.",
                "our former personalities and the cultures": "그건 that 뒤 abandon의 목적어예요."},
               "주어는 The process, 동사는 does not require예요. that 뒤가 요구하지 않는 내용이에요.",
               ask="주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s9_gap",
                   "④which 뒤 'we were born'을 봐요. 이 덩어리에 빠진 자리(주어나 목적어)가 있나요?",
                   [("o0", "주어가 빠졌다", False), ("o1", "빠진 자리가 없다 (we 주어, were born 동사로 완전하다)", True),
                    ("o2", "목적어가 빠졌다", False)],
                   "be born은 '태어나다'라서 목적어를 받지 않아요. 주어 we도 있어요.",
                   why="we(주어) + were born(동사, 태어나다)으로 빠진 자리가 없는 완전한 문장이에요. be born은 목적어를 받지 않아요.",
                   highlight=["which we were born"],
                   tips=[tip("관계대명사 vs 전치사 + 관계대명사", "관계대명사(which·that) 뒤에는 주어나 목적어가 빠진 자리가 있어요. 빠진 게 없이 완전하면 '전치사 + which(= where)'를 써요. 예: the house in which I live", "which")],
                   point="④ which 뒤 we were born은 빠진 자리 없는 완전한 문장 — 관계대명사 which만으로는 안 되는지 문제에서 확인"),
            show("s9_hold", "관계대명사 which 뒤는 빠진 자리가 있어야 해요. 여기는 빠진 게 없어요. ④가 맞는지는 문제에서 골라 봐요.",
                 highlight=["which we were born"], button="다음 문장"),
        ],
    },
    {
        "id": 10, "text": S[9], "model_translation": KO[9], "teaching_value": "high",
        "glosses": [g("Rather", "오히려"), g("it compels us", "그것은 우리에게 강요한다"), g("to find", "찾도록"), g("ourselves", "우리 자신을"),
                    g("as if for the first time", "마치 처음인 것처럼"), g("particularly", "특히"),
                    g("those “cultural invariants” within us", "우리 안의 '문화적으로 변하지 않는 것들'"),
                    g("aspects that we hold dear", "우리가 소중히 여기는 측면들"), g("refuse to compromise", "타협하기를 거부하다")],
        "slashes": ["Rather,", "compels us", "find ⑤ourselves", "for the first time,", "within us—", "hold dear"],
        "roles": [r("it", "S"), r("compels", "V"), r("us", "O")],
        "modifiers": ["that we hold dear and refuse to compromise"],
        "steps": [
            choice("s10_reflexive",
                   "compels us to find ⑤ourselves — 찾는 사람(to find의 주체)은 누구일까요?",
                   [("o0", "it (그 과정)", False), ("o1", "us (우리)", True), ("o2", "the cultures", False)],
                   "compel + 사람 + to ~는 '사람이 ~하도록 강요하다'예요. 찾는 건 그 사람이에요.",
                   why="compel us to find, 찾는 사람은 us(우리)예요. 찾는 대상도 우리 자신이니 재귀대명사 ourselves가 맞아요.",
                   highlight=["compels us to find", "ourselves"],
                   tips=[tip("재귀대명사", "하는 사람과 받는 대상이 같으면 -self를 써요. 여기서는 to find의 주체 us = 대상 → ourselves.", "ourselves")],
                   point="⑤ 찾는 사람 us = 찾는 대상 → 재귀대명사 ourselves 맞음"),
            show("s10_go", "①②③⑤는 맞았어요. 남은 하나, ④를 다시 떠올리며 문제를 골라 봐요.",
                 panel=check("1", "2", "3", "5"), panel_below=True, button="문제 풀러 갈게요"),
        ],
    },
]

SENSES = {
    1: [sense("as", "as cultural beings", "~로서", "전치사 as (자격)")],
    2: [sense("for", "for new learning", "~을 위한", "전치사 for + 명사")],
    3: [sense("but", "but of ourselves", "~도 (not only A but B)", "not only A but (also) B")],
    4: [sense("that", "difficulties that can arise", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    5: [sense("to", "to define", "~할", "형용사(privileged) + to부정사"),
        sense("that", "insight that we could not", "(앞 명사를 꾸밈)", "관계대명사 that + 주어·동사")],
    6: [sense("to", "Adapting to a new", "~에 (적응하다)", "adapt to + 명사")],
    9: [sense("that", "require that we abandon", "~하는 것을", "명사절 that (require that …)"),
        sense("which", "the cultures which we were born", "(앞 명사를 꾸밈)", "관계사 which — 뒤 문장의 빈자리를 확인")],
    10: [sense("to", "compels us to find", "~하도록", "compel + 사람 + to부정사"),
         sense("as", "as if", "마치 (~인 것처럼)", "as if + 절·구"),
         sense("if", "as if for the first time", "(as if의 일부)", "as if = 마치 ~처럼"),
         sense("for", "for the first time", "~ 만에, 처음으로", "for the first time = 처음으로"),
         sense("that", "aspects that we hold", "(앞 명사를 꾸밈)", "관계대명사 that + 주어·동사"),
         sense("to", "refuse to compromise", "~하기를 (거부하다)", "refuse + to부정사")],
}

WORDS = {"rather": "오히려", "process": "과정", "crossing": "넘어가는 것", "cultures": "문화들", "very": "바로 그", "basis": "기반", "cultural": "문화적인",
         "beings": "존재", "offers": "주다", "opportunities": "기회", "learning": "배움", "growth": "성장", "home": "고향",
         "people": "사람들", "culture": "문화", "environment": "환경", "ourselves": "우리 자신", "difficulties": "어려움",
         "arise": "생기다", "often": "흔히", "shocking": "충격적인", "success": "성공", "stories": "이야기", "everywhere": "어디에나",
         "despite": "~에도 불구하고", "suffering": "고통", "ambivalence": "상반된 감정", "undergo": "겪다", "cross": "넘어가다",
         "define": "정의하다", "others": "다른 사람들", "anew": "새롭게", "clarity": "명확함", "insight": "통찰", "cultivated": "기른",
         "leaving": "떠나는 것", "unfamiliar": "낯선", "survival": "생존", "life-changing": "삶을 바꾸는", "journey": "여정",
         "becoming": "되어 가는 것", "personal": "개인의", "reinvention": "재창조", "reaching": "뻗어 가는 것", "beyond": "~ 너머로",
         "boundaries": "경계", "existence": "존재", "require": "요구하다", "former": "이전의", "personalities": "성격",
         "born": "태어난", "compels": "강요하다", "first": "첫", "invariants": "변하지 않는 것들", "aspects": "측면", "hold": "여기다",
         "dear": "소중한", "refuse": "거부하다", "compromise": "타협하다", "home.": "고향", "new": "새로운", "own": "자신의"}

exam = {
    "question": "다음 글의 밑줄 친 부분 중, 어법상 틀린 것은?",
    "underline": UNDER, "sentence": 9, "analysis_first": True,
    "glosses": [g("brings", "가져다준다"), g("uniquely", "특별히"), g("Adapting", "적응하는 것"), g("which", "(관계사)"), g("ourselves", "우리 자신")],
    "options": [{"id": str(i + 1), "label": u[1:], "keywords": [u[1:]], **({"correct": True} if i == 3 else {})} for i, u in enumerate(UNDER)],
    "brief": exam_brief(
        "밑줄 점검표를 떠올려 봐요. ④ which 뒤에 빠진 자리가 있었나요?",
        "정답이에요! which 뒤 'we were born'이 빠진 자리 없는 완전한 문장이라 into which(be born into = ~에 태어나다)로 고쳐요. in which로 써도 어법은 맞지만, 문화·집안에 '태어나다'는 born into라서 into which가 더 자연스러워요.",
        "정답은 ④예요. which 뒤가 완전한 문장이라 into which(be born into = ~에 태어나다)여야 해요. in which도 어법은 맞지만 into which가 더 자연스러워요.",
        {"1": "동명사 덩어리 주어(Being uprooted …)는 단수라 brings가 맞아요.",
         "2": "형용사 privileged를 꾸미는 부사 uniquely가 맞아요.",
         "3": "동사 is의 주어 자리라 동명사 Adapting이 맞아요.",
         "5": "찾는 사람 us와 찾는 대상이 같아서 재귀대명사 ourselves가 맞아요."}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 29번 (어법, 2점)",
    topic="어법 푸는 법: 밑줄마다 무슨 문법을 묻는지 이름 붙이기 → 그 문장 뼈대(주어·동사·빈자리)로 확인",
    method={"type": "grammar", "labels": ["문장 뼈대 찾기", "밑줄 문법 확인"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-crossing-cultures.svg", ("Home", "고향 문화"), "→", ("New culture", "새 문화"),
                                       "다른 문화로 가면 나는 어떻게 달라질까?", "2024년 3월 29번 도입 칠판"),
                      "alt": "칠판: Home(고향 문화) → New culture(새 문화)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "낯선 나라에 가서 살면 나는 어떻게 달라질까요? 이번 글은 문화를 넘어가는 경험을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "어법 문제는 밑줄마다 무슨 문법을 묻는지 먼저 이름을 붙여요. 그다음 그 문장의 주어·동사·빈자리로 확인할게요."}}],
    exam=exam,
    key_words={"passage": [g("challenge", "도전하다, 흔들다"), g("uprooted", "뿌리째 뽑힌"), g("arise", "생기다"), g("undergo", "겪다"),
                           g("privileged", "특권을 누리는"), g("anew", "새롭게"), g("cultivate", "기르다"), g("adapt to", "~에 적응하다"),
                           g("reinvention", "재창조"), g("abandon", "버리다"), g("be born into", "~에 태어나다"), g("compel", "강요하다"),
                           g("hold dear", "소중히 여기다"), g("compromise", "타협하다")],
               "options": []},
    sentences=sentences, concept="medium")

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="어법 푸는 법",
       chunks={"Being “uprooted” from our home": "고향에서 뿌리째 뽑히는 것", "brings": "가져다준다", "us": "우리에게", "understanding": "이해",
               "the suffering and ambivalence": "고통과 상반된 감정", "we": "우리는", "find": "알게 되다", "ourselves": "우리 자신을",
               "privileged": "특권을 누리는", "The process": "그 과정은", "does not require": "요구하지 않는다", "abandon": "버리다",
               "our former personalities and the cultures": "이전의 성격과 문화들"})
