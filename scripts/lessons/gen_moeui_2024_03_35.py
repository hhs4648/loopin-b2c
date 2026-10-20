"""2024년 3월 고3 35번 레슨 + 대사를 만든다 (흐름과 무관한 문장, 2점). 오답률 자료 없음(Top 15 밖).

    python3 scripts/lessons/gen_moeui_2024_03_35.py   (→ npm run policy:copy stamp <id> → npm run build)

무관한 문장 유형은 처음 — Claude 초안(2026-10-18, 미니 모의고사 연결용). 푸는 법: 첫 문장(번호 없는 문장)으로 화제 잡기 →
①~⑤ 문장마다 글의 방향(언어 차이를 '가능성'으로 본다)과 같은 쪽인지 칠판 두 칸에 나누기 → 다른 쪽 한 문장.
같은 단어(error)가 나와도 방향이 반대일 수 있다. 정답 ④. 해설지와 대조함.
disparity, rhetorical, inferior는 시험지 아래 *로 풀어 준 단어(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, finish)

ID = "moeui-2024-03-35-translingual-approach"

S = [
    "No doubt students collaborating with other speakers of English might encounter language variances, which may interfere with intentionality.",
    "①To address such disparities, Horner, Lu, Royster, and Trimbur (2011) call for a “translingual approach” in which language varieties are not perceived as barriers, but as avenues for meaning making.",
    "②Similarly, Galloway and Rose (2015) study of Global Englishes found that exposure to other Englishes helps normalize language differences.",
    "③Educators have to work with students to examine phrases, expressions, and other ranges of English language use for their rhetorical and communicative possibilities and not their perceived errors or inferior status.",
    "④Committing an error means unintentionally saying what isn’t true, so any linguistic or perspective error should be avoided at all cost.",
    "⑤After all, students are constantly reading texts and listening to speakers whose Englishes do not necessarily conform to what is considered standard in their own communities.",
]
KO = [
    "영어로 말하는 다른 사용자와 공동으로 일하는 학생들이 언어적 차이와 마주칠 수도 있다는 것은 의심의 여지가 없고, 그것은 의도성에 방해가 될 수도 있다.",
    "이러한 차이를 다루기 위해 Horner, Lu, Royster, Trimbur(2011)는 언어의 다양성이 의미 창출의 장벽이 아니라 수단으로 인식되는 '초언어적 접근법'을 요구한다.",
    "마찬가지로, 글로벌 영어들에 대한 Galloway와 Rose(2015)의 연구가 다른 영어들에 대한 노출이 언어 차이를 표준화하는 데 도움이 된다는 사실을 발견했다.",
    "교육자들은 그것들의 인식되는 오류나 열등한 지위가 아니라 그것들의 수사적, 의사소통적 가능성을 위한 구문, 표현 그리고 영어 사용의 다른 범주를 검토하기 위해 학생들과 함께해야 한다.",
    "오류를 범한다는 것은 사실이 아닌 것을 의도치 않게 말하는 것을 의미하고, 그래서 그 어떤 언어적 또는 관점적 오류는 무슨 수를 써서라도 피해야 한다.",
    "결국, 학생들은 계속해서 글을 읽고 화자의 말을 듣는데, 그들의 영어는 그들 자신의 공동체에서 표준으로 여겨지는 것과 반드시 일치하지는 않는다.",
]

PLUS = "왼쪽 · 차이 = 가능성 (+)"
MINUS = "오른쪽 · 차이 = 오류 (−)"


def board(left, right=(), fresh=(), sort=None):
    return groups("언어 차이를 어떻게 볼까", "차이 = 가능성 (+)", list(left), "차이 = 오류 (−)", list(right), fresh=fresh, between="↔",
                  sort={"words": sort, "left": PLUS, "right": MINUS} if sort else None)


def sort_step(id, n, word, right_side, why, highlight):
    return choice(id, f"{n} 문장은 언어 차이를 어떻게 보는지, 칠판 어느 쪽일까요?",
                  [("o0", PLUS, not right_side), ("o1", MINUS, right_side)], why, why=why,
                  panel=board(L_SO_FAR[n], R_SO_FAR[n], sort=[word]), highlight=highlight)


L_SO_FAR = {"①": [], "②": ["avenues"], "③": ["avenues", "normalize"], "④": ["avenues", "normalize", "possibilities"],
            "⑤": ["avenues", "normalize", "possibilities"]}
R_SO_FAR = {"①": [], "②": [], "③": [], "④": [], "⑤": ["avoided at all cost"]}

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("No doubt", "의심할 여지 없이"), g("students collaborating with other speakers of English", "다른 영어 사용자와 함께 일하는 학생들"),
                    g("might encounter", "마주칠 수도 있다"), g("language variances", "언어 차이"), g("which may interfere with", "그것은 ~을 방해할 수도 있다"),
                    g("intentionality", "의도(뜻한 대로 전달하기)")],
        "slashes": ["No doubt", "students", "speakers of English", "language variances,"],
        "roles": [r("students", "S"), r("might encounter", "V"), r("language variances", "O")],
        "modifiers": ["collaborating with other speakers of English", "which may interfere with intentionality"],
        "steps": [
            sv("s1_sv", ["students", "other speakers of English", "might encounter", "language variances"],
               {"students": "S", "might encounter": "V", "language variances": "O"},
               {"other speakers of English": "그건 collaborating with(~와 함께 일하는) 뒤 덩어리예요. students를 꾸며요."},
               "주어는 students (collaborating with …), 동사는 might encounter, 목적어는 language variances예요.",
               tips=[tip("무관한 문장 요령", "번호 없는 첫 문장으로 글의 화제와 방향을 잡아요. ①~⑤를 하나씩 그 방향과 같은 쪽인지 보고, 다른 쪽 한 문장을 골라요. 같은 단어가 나와도 방향이 다를 수 있어요.")]),
            show("s1_topic", "다른 영어를 쓰는 사람과 일하면 언어 차이를 만나게 된대요. 이 글은 그 언어 차이를 어떻게 볼지에 대한 이야기예요.",
                 highlight=["language variances"], panel=board([], []), button="다음 문장"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("To address such disparities", "그런 차이를 다루기 위해"), g("call for", "~을 요구하다"), g("a “translingual approach”", "'초언어적 접근법'"),
                    g("in which", "그 접근법에서는"), g("language varieties", "언어의 다양성"), g("are not perceived as barriers", "장벽으로 여겨지지 않는다"),
                    g("but as avenues", "통로로 (여겨진다)"), g("avenues", "통로, 수단"), g("for meaning making", "의미를 만드는")],
        "slashes": ["such disparities,", "Trimbur (2011)", "“translingual approach”", "language varieties", "as barriers,"],
        "roles": [r("Horner, Lu, Royster, and Trimbur (2011)", "S"), r("call for", "V")],
        "modifiers": ["in which language varieties are not perceived as barriers, but as avenues for meaning making"],
        "steps": [
            sort_step("s2_sort", "①", "avenues", False,
                      "'not perceived as barriers, but as avenues', 언어 차이를 장벽이 아니라 의미를 만드는 통로로 본대요. 가능성 쪽이에요.",
                      ["not perceived as barriers", "avenues"]),
            show("s2_dir", "not A but B — 장벽이 아니라 통로래요. 글의 방향이 나왔어요. 언어 차이를 좋은 가능성으로 보는 쪽이에요.",
                 panel=board(["avenues"], [], fresh=("avenues",)), button="다음 문장",
                 tips=[tip("not A but B", "'A가 아니라 B'예요. 글쓴이 생각은 B 쪽이에요.", "not perceived")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("Similarly", "마찬가지로"), g("Galloway and Rose (2015) study of Global Englishes", "글로벌 영어에 대한 갤러웨이와 로즈(2015)의 연구"),
                    g("found", "발견했다"), g("exposure to other Englishes", "다른 영어들에 노출되는 것"), g("helps normalize", "~을 자연스럽게(정상으로) 만드는 데 도움이 된다"),
                    g("language differences", "언어 차이")],
        "slashes": ["②Similarly,", "Global Englishes", "found", "other Englishes"],
        "roles": [r("Galloway and Rose (2015) study", "S"), r("found", "V"), r("exposure to other Englishes", "S"), r("helps", "V")],
        "steps": [
            sort_step("s3_sort", "②", "normalize", False,
                      "Similarly(마찬가지로)로 이어지고, 다른 영어에 노출되면 언어 차이가 자연스러워진대요(normalize). 가능성 쪽이에요.",
                      ["Similarly", "normalize"]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Educators", "교육자들"), g("have to work with students", "학생들과 함께해야 한다"), g("to examine", "살펴보기 위해"),
                    g("phrases, expressions, and other ranges of English language use", "구문, 표현, 그 밖의 영어 사용"),
                    g("for their rhetorical and communicative possibilities", "그것의 수사적·의사소통적 가능성을 보려고"),
                    g("possibilities", "가능성"), g("and not their perceived errors or inferior status", "여겨지는 오류나 열등함이 아니라")],
        "slashes": ["with students", "to examine phrases, expressions,", "English language use", "communicative possibilities"],
        "roles": [r("Educators", "S"), r("have to work", "V")],
        "steps": [
            sort_step("s4_sort", "③", "possibilities", False,
                      "'for their … possibilities and not their perceived errors', 오류가 아니라 가능성을 보래요. 가능성 쪽이에요.",
                      ["possibilities", "not their perceived errors"]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Committing an error", "오류를 범하는 것"), g("means", "뜻한다"), g("unintentionally saying what isn’t true", "의도치 않게 사실이 아닌 걸 말하는 것"),
                    g("so", "그래서"), g("any linguistic or perspective error", "어떤 언어적·관점적 오류도"),
                    g("should be avoided at all cost", "무슨 수를 써서라도 피해야 한다")],
        "slashes": ["Committing an error", "means unintentionally saying", "what isn’t true,", "should be avoided"],
        "roles": [r("Committing an error", "S"), r("means", "V"), r("any linguistic or perspective error", "S"), r("should be avoided", "V")],
        "steps": [
            sort_step("s5_sort", "④", "avoided at all cost", True,
                      "'any … error should be avoided at all cost', 어떤 오류든 무조건 피하래요. 차이를 오류로 보고 없애려는 쪽이에요.",
                      ["error", "avoided at all cost"]),
            show("s5_hold", "③에도 error가 나왔지만, ③은 '오류가 아니라 가능성'이었어요. 같은 단어여도 방향이 다를 수 있어요.",
                 panel=board(["avenues", "normalize", "possibilities"], ["avoided at all cost"], fresh=("avoided at all cost",)),
                 tips=[tip("at all cost", "'무슨 수를 써서라도, 어떻게든'이에요.", "at all cost")], button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("After all", "결국, 어쨌든"), g("students", "학생들"), g("are constantly reading texts", "늘 글을 읽는다"),
                    g("listening to speakers", "화자의 말을 듣다"), g("whose Englishes", "그들의 영어는"),
                    g("do not necessarily conform to", "반드시 ~에 맞지는 않는다"), g("what is considered standard", "표준으로 여겨지는 것"),
                    g("in their own communities", "그들 자신의 공동체에서")],
        "slashes": ["⑤After all,", "constantly reading texts", "listening to speakers", "conform to", "considered standard"],
        "roles": [r("students", "S"), r("are constantly reading", "V"), r("texts", "O"), r("listening", "V")],
        "modifiers": ["whose Englishes do not necessarily conform to what is considered standard in their own communities"],
        "steps": [
            sort_step("s6_sort", "⑤", "not necessarily standard", False,
                      "After all(결국), 학생들은 늘 표준과 다른 영어를 접한대요. 그러니 차이를 받아들여야 한다는 앞 문장들의 이유예요. 가능성 쪽이에요.",
                      ["After all", "do not necessarily conform to"]),
            show("s6_go", "①②③⑤는 언어 차이를 가능성으로 봐요. 다른 쪽에 놓인 한 문장을 문제에서 골라 봐요.",
                 panel=board(["avenues", "normalize", "possibilities", "not necessarily standard"], ["avoided at all cost"]),
                 button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 3, [m("Similarly", "마찬가지로"), ", 연구는 ", m("exposure to other Englishes", "다른 영어들에 노출되는 것이"), " ",
                         m("language differences", "언어 차이"), "를 ", m("helps normalize", "자연스럽게 만드는 데 도움이 된다"), "는 걸 ", m("found", "발견했다"), "."],
          sv_new=sv_step("s3_basic_sv", ["Galloway and Rose (2015) study", "found", "exposure", "helps"],
                         {"Galloway and Rose (2015) study": "S", "found": "V"},
                         {"exposure": "그건 that 뒤 덩어리 안의 주어예요.", "helps": "그건 that 뒤 덩어리 안의 동사예요."},
                         "주어는 Galloway and Rose (2015) study (of Global Englishes), 동사는 found예요."),
          meaning_after="s3_sort",
          meaning="다른 여러 영어를 접하면 언어 차이가 자연스러운 것이 된다는 연구래요.")
add_basic(sentences, 5, [m("Committing an error", "오류를 범하는 것은"), " ", m("unintentionally saying what isn’t true", "의도치 않게 사실이 아닌 걸 말하는 것"), "을 ",
                         m("means", "뜻한다"), ", ", m("so", "그래서"), " ", m("any linguistic or perspective error", "어떤 오류도"), " ",
                         m("should be avoided at all cost", "무슨 수를 써서라도 피해야 한다"), "."],
          sv_new=sv_step("s5_basic_sv", ["Committing an error", "means", "any linguistic or perspective error", "should be avoided"],
                         {"Committing an error": "S", "means": "V", "any linguistic or perspective error": "S", "should be avoided": "V"}, {},
                         "so 앞은 주어 Committing an error, 동사 means예요. so 뒤는 주어 any … error, 동사 should be avoided예요."),
          meaning_after="s5_sort",
          meaning="오류는 사실이 아닌 걸 말하는 거니, 어떤 오류든 무조건 피해야 한대요.")

SENSES = {
    1: [sense("which", "variances, which may interfere", "(그것은) ~하는", "콤마 + which = 앞 명사를 덧붙여 설명")],
    2: [sense("to", "To address", "~하기 위해", "to부정사 (목적)"),
        sense("for", "call for", "~을 (요구하다)", "call for + 명사"),
        sense("which", "in which", "그 (접근법)에서는", "전치사 + which"),
        sense("as", "as barriers", "~로", "be perceived as + 명사"),
        sense("but", "but as avenues", "~가 아니라 (B)", "not A but B"),
        sense("as", "as avenues", "~로", "be perceived as + 명사"),
        sense("for", "for meaning making", "~을 위한", "전치사 for + 명사")],
    3: [sense("that", "found that exposure", "~라는 것을", "명사절 that (find that …)"),
        sense("to", "exposure to other Englishes", "~에 (노출)", "exposure to + 명사")],
    4: [sense("to", "have to work", "~해야 (하다)", "have to + 동사원형"),
        sense("to", "to examine", "~하기 위해", "to부정사 (목적)"),
        sense("for", "for their rhetorical", "~을 위해, ~을 보려고", "전치사 for + 명사")],
    5: [sense("so", "so any linguistic", "그래서", "접속사 so (결과)")],
    6: [sense("to", "listening to speakers", "~을 (듣다)", "listen to + 명사"),
        sense("to", "conform to what", "~에 (맞다)", "conform to + 명사")],
}

WORDS = {"doubt": "의심", "students": "학생들", "collaborating": "함께 일하는", "speakers": "말하는 사람들", "english": "영어",
         "encounter": "마주치다", "language": "언어", "variances": "차이", "interfere": "방해하다", "intentionality": "의도",
         "address": "다루다", "such": "그런", "disparities": "차이", "call": "요구하다 · call for", "translingual": "초언어적인",
         "approach": "접근법", "varieties": "다양성", "perceived": "여겨지는", "barriers": "장벽", "avenues": "통로, 수단",
         "meaning": "의미", "making": "만드는 것", "similarly": "마찬가지로", "galloway": "갤러웨이", "rose": "로즈", "study": "연구",
         "global": "세계의", "englishes": "여러 영어", "found": "발견했다", "exposure": "노출", "helps": "돕다", "normalize": "정상으로(자연스럽게) 만들다",
         "differences": "차이", "educators": "교육자들", "work": "일하다", "examine": "살펴보다", "phrases": "구문", "expressions": "표현",
         "ranges": "범위", "use": "사용", "rhetorical": "수사적인", "communicative": "의사소통의", "possibilities": "가능성",
         "errors": "오류", "inferior": "열등한", "status": "지위", "committing": "범하는 것", "error": "오류", "means": "뜻하다",
         "unintentionally": "의도치 않게", "saying": "말하는 것", "isn’t": "~이 아니다", "true": "사실인", "linguistic": "언어적인",
         "perspective": "관점의", "avoided": "피해진", "cost": "대가 · at all cost = 무슨 수를 써서라도", "constantly": "늘",
         "reading": "읽는", "texts": "글", "listening": "듣는", "necessarily": "반드시", "conform": "맞다, 따르다", "considered": "여겨지는",
         "standard": "표준", "communities": "공동체", "study.": "연구", "2015": "2015년", "(2015)": "(2015년)"}

exam = {
    "question": "다음 글에서 전체 흐름과 관계 없는 문장은?",
    "underline": ["①", "②", "③", "④", "⑤"], "numbers_only": True, "sentence": 5, "analysis_first": True, "glosses": [],
    "passage_keywords": ["language variances", "avenues", "normalize", "possibilities", "error", "avoided at all cost", "standard"],
    "options": [{"id": str(i), "label": f"{'①②③④⑤'[i - 1]} 문장", "keywords": [], **({"correct": True} if i == 4 else {})} for i in range(1, 6)],
    "brief": exam_brief(
        "칠판 두 칸을 떠올려 봐요. 혼자 다른 쪽에 놓인 문장을 골라요.",
        "정답이에요! 글은 언어 차이를 장벽이 아니라 가능성으로 보자고 해요. ④만 오류는 무조건 피해야 한다며 반대쪽 이야기를 해요.",
        "정답은 ④예요. 나머지는 모두 언어 차이를 가능성으로 보는데, ④만 오류를 무조건 피하라고 해요.",
        {"1": "①은 언어 차이를 장벽이 아니라 통로로 보자는 주장, 글의 방향 그 자체예요.",
         "2": "②는 Similarly로 이어지는 같은 방향의 연구 결과예요.",
         "3": "③에 error가 나오지만 '오류가 아니라 가능성'을 보라는 말이라 같은 방향이에요.",
         "5": "⑤는 After all, 학생들이 늘 표준과 다른 영어를 접한다는 이유예요. 같은 방향이에요."}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 35번 (흐름과 무관한 문장, 2점)",
    topic="무관한 문장 푸는 법: 첫 문장으로 화제와 방향 잡기 → ①~⑤를 같은 쪽/다른 쪽으로 나누기 → 다른 쪽 한 문장",
    method={"type": "irrelevant", "labels": ["화제·방향 잡기", "문장마다 나누기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-translingual.svg", ("Difference", "언어 차이"), "→", ("Possibility?", "가능성?"),
                                       "다른 영어는 틀린 영어일까?", "2024년 3월 35번 도입 칠판"),
                      "alt": "칠판: Difference(언어 차이) → Possibility?(가능성?)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "나라마다 조금씩 다른 영어, 틀린 영어일까요? 이번 글은 언어 차이를 어떻게 볼지 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "무관한 문장 문제는 첫 문장으로 글의 방향을 잡고, ①~⑤를 같은 쪽과 다른 쪽으로 나눠요. 칠판에 하나씩 놓아 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("collaborate", "함께 일하다"), g("encounter", "마주치다"), g("variance", "차이"), g("interfere with", "~을 방해하다"),
                           g("address", "다루다"), g("call for", "~을 요구하다"), g("perceive A as B", "A를 B로 여기다"), g("barrier", "장벽"),
                           g("avenue", "통로, 수단"), g("exposure", "노출"), g("normalize", "정상으로 만들다"), g("examine", "살펴보다"),
                           g("at all cost", "무슨 수를 써서라도"), g("conform to", "~에 맞다")],
               "options": []},
    sentences=sentences, concept="medium")

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="무관한 문장 푸는 법",
       chunks={"students": "학생들", "other speakers of English": "다른 영어 사용자", "might encounter": "마주칠 수도 있다",
               "language variances": "언어 차이", "Galloway and Rose (2015) study": "갤러웨이와 로즈(2015)의 연구", "found": "발견했다",
               "exposure": "노출", "helps": "돕다", "Committing an error": "오류를 범하는 것", "means": "뜻한다",
               "any linguistic or perspective error": "어떤 언어적·관점적 오류", "should be avoided": "피해야 한다"})
