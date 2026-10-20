"""2024년 3월 고3 37번 레슨 + 대사를 만든다 (글의 순서, 2점). 오답률 67.3% · Top 4.

    python3 scripts/lessons/gen_moeui_2024_03_37.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/order.md — 주어진 글의 끝 → 단락 첫머리(앞에 무엇?) → 단락 끝(다음에 무엇?) → 순서 잇기.
정답 ⑤ (C)-(B)-(A). 많이 고른 오답 ④ (C)-(A)-(B) 31.3% — (C) 끝 Landscape Urbanism 바로 뒤에 (A) 'Landscape Urbanists'를 붙였다.
그러나 (A)의 these designs(자연을 중시하지 않는 설계)는 경관 도시론 설계가 아니고, both approaches는 두 방식이 다 나온 뒤라야 한다.
단서: (C) these approaches ← 주어진 글 various interpretations / (B) critics claim … Landscape Urbanists ← (C) 끝 경관 도시론 소개 /
(A) these designs ← (B) 끝 New Urbanism, both approaches = 경관 도시론 + 신도시론. 해설지 해석과 대조함.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, rows, sense, m, sv_step, add_basic, add_that_sv, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from order_tools import card, order_link  # noqa: E402

ID = "moeui-2024-03-37-urban-planning"

GIVEN = ("Today, historic ideas about integrating nature and urban/suburban space find expression in various interpretations "
         "of sustainable urban planning.")
A1 = ("(A) But Landscape Urbanists find that these designs do not prioritize the natural environment and often involve "
      "diverting streams and disrupting natural wetlands.")
A2 = ("Still others, such as those advocating for “just sustainabilities” or “complete streets,” find that both approaches are "
      "overly idealistic and neither pays enough attention to the realities of social dynamics and systemic inequality.")
B1 = "(B) However, critics claim that Landscape Urbanists prioritize aesthetic and ecological concerns over human needs."
B2 = ("In contrast, New Urbanism is an approach that was popularized in the 1980s and promotes walkable streets, compact design, "
      "and mixed-use developments.")
C1 = "(C) However, the role of social justice in these approaches remains highly controversial."
C2 = ("For example, Landscape Urbanism is a relatively recent planning approach that advocates for native habitat designs that "
      "include diverse species and landscapes that require very low resource use.")

sentences = [
    {
        "id": 1, "label": "주어진 글", "text": GIVEN, "teaching_value": "high",
        "model_translation": "오늘날, 자연과 도시/교외 공간의 통합에 대한 역사적인 생각들은 지속 가능한 도시 계획에 대한 다양한 해석의 모습으로 나타난다.",
        "glosses": [g("Today", "오늘날"), g("historic ideas", "역사적인 생각들"), g("integrating", "통합하는 것, 합치는 것"),
                    g("integrating nature and urban/suburban space", "자연과 도시·교외 공간을 합치는 것"), g("find", "찾다"),
                    g("expression", "표현"), g("find expression in", "~에서 표현되다, ~로 나타나다"),
                    g("various interpretations", "여러 가지 해석"), g("sustainable urban planning", "지속 가능한 도시 계획")],
        "slashes": ["Today,", "historic ideas", "urban/suburban space", "find expression"],
        "roles": [r("historic ideas", "S"), r("find", "V"), r("expression", "O")],
        "steps": [
            sv("g_sv", ["Today", "historic ideas", "integrating nature and urban/suburban space", "find", "expression", "various interpretations"],
               {"historic ideas": "S", "find": "V", "expression": "O"},
               {"Today": "그건 '오늘날', 때를 알려 주는 말이에요.",
                "integrating nature and urban/suburban space": "그건 about(~에 대한) 뒤 덩어리예요. 앞의 ideas를 꾸며요.",
                "various interpretations": "그건 in 뒤 덩어리예요. 전치사 뒤라 목적어(O)가 아니에요."},
               "주어는 historic ideas, 동사는 find, 목적어는 expression이에요. find expression in은 '~로 나타나다'예요.",
               ask="주어진 글의 주어(S), 동사(V), 목적어(O)를 찾아볼까요?"),
            choice("g_mean",
                   "주어·동사·목적어를 칠한 채로 봐요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "도시 계획은 자연을 무시해 왔다", False),
                    ("o1", "자연과 도시를 합치려는 생각이 오늘날 여러 도시 계획 방식으로 나타난다", True),
                    ("o2", "오래된 도시를 그대로 보존해야 한다", False)],
                   "find expression in은 '~에서 표현되다, ~로 나타나다'예요. in 뒤 various interpretations(여러 해석)를 봐요.",
                   why="historic ideas(자연과 도시를 합치려는 옛 생각)가 find expression in(~로 나타난다) various interpretations(여러 해석)라는 말이에요.",
                   highlight=["historic ideas", "find expression in", "various interpretations"],
                   tips=[tip("find expression in", "'~에서 표현되다, ~로 나타나다'예요. 생각이 어떤 모습으로 드러난다는 말이에요.", "find expression")]),
            choice("g_next",
                   "주어진 글은 '여러 가지 해석(various interpretations)'으로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "두 방식이 모두 지나치게 이상적이라는 결론", False), ("o1", "한 방식을 비판하는 사람들의 말", False),
                    ("o2", "그 여러 방식(접근법)들에 대한 이야기", True)],
                   "여러 해석이 있다고 했으니, 다음엔 그 해석들을 받는 말이 오기 쉬워요. 비판이나 결론은 방식이 소개된 뒤에야 나와요.",
                   why="여러 해석이 있다고 했으니, 다음엔 그 방식들을 가리키며 이야기가 이어지기 쉬워요. 비판이나 결론은 방식이 소개된 다음이에요.",
                   highlight=["various interpretations"],
                   tips=[tip("순서 문제 요령", "주어진 글의 마지막 말이 다음 단락의 첫머리와 이어져요. 단락 첫머리의 these, However, But 같은 말이 앞 내용을 가리켜요.")]),
            show("paper_order", "이제 (A)·(B)·(C)를 시험지 순서대로 읽어요. 단락마다 첫머리와 끝을 잘 봐 두면 좋아요.",
                 button="(A)부터 읽어 볼게요"),
        ],
    },
    {
        "id": 2, "text": A1, "teaching_value": "high",
        "model_translation": "(A) 그러나 경관 도시론자들은 이러한 설계가 자연 환경을 우선시하지 않으며, 하천의 우회와 자연 습지 파괴를 흔히 수반한다는 것을 알게 되었다.",
        "glosses": [g("But", "그러나"), g("Landscape Urbanists", "경관 도시론자들"), g("find", "알게 되다, 여기다"),
                    g("these designs", "이 설계들"), g("do not prioritize", "우선시하지 않는다"), g("the natural environment", "자연 환경"),
                    g("often involve", "흔히 수반하다"), g("diverting streams", "하천의 물길을 돌리는 것"),
                    g("disrupting natural wetlands", "자연 습지를 망가뜨리는 것")],
        "slashes": ["Landscape Urbanists find", "these designs", "the natural environment", "diverting streams"],
        "roles": [r("Landscape Urbanists", "S"), r("find", "V"), r("these designs", "S"), r("do not prioritize", "V"),
                  r("the natural environment", "O"), r("involve", "V")],
        "steps": [
            sv("a_sv", ["But", "Landscape Urbanists", "find", "these designs", "do not prioritize"],
               {"Landscape Urbanists": "S", "find": "V"},
               {"But": "그건 '그러나', 앞 단락과 잇는 말이에요.",
                "these designs": "그건 that 뒤 덩어리 안의 주어예요. 먼저 문장 전체의 주어를 찾아봐요.",
                "do not prioritize": "그건 that 뒤 덩어리 안의 동사예요."},
               "주어는 Landscape Urbanists, 동사는 find예요. that 뒤가 그들이 알게 된 내용이에요.",
               ask="(A) 단락의 첫 문장이에요. 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("a_before",
                   "경관 도시론자들이 these designs(이 설계들)가 자연을 우선하지 않는다고 비판해요. 그럼 (A) 앞에는 무엇이 와야 할까요?",
                   [("o0", "경관 도시론자의 설계 방식 소개", False), ("o1", "경관 도시론자가 아닌 다른 쪽의 설계 방식 소개", True),
                    ("o2", "사회 정의를 둘러싼 논란", False)],
                   "these designs는 앞에서 소개한 설계예요. 경관 도시론자가 자기 설계를 스스로 비판하지는 않겠죠.",
                   why="But으로 경관 도시론자들이 these designs를 비판해요. 자기 설계를 비판하진 않으니, 앞에는 다른 쪽 설계가 소개돼 있어야 해요.",
                   highlight=["these designs", "do not prioritize"],
                   point="(A) these designs = 경관 도시론자가 비판하는 '다른 쪽' 설계 → 앞에 다른 설계 방식이 소개돼야 한다"),
        ],
    },
    {
        "id": 3, "text": A2, "teaching_value": "high",
        "model_translation": "그럼에도 불구하고 다른 사람들은, 예를 들어 '정당한 지속 가능성'이나 '완전 도로'를 주장하는 이들은 두 접근 방식 모두 지나치게 이상주의적이며, 사회적 역학 관계와 구조적 불평등의 현실에 충분한 주의를 기울이지 않는다는 것을 알게 되었다.",
        "glosses": [g("Still others", "또 다른 사람들은"), g("such as", "~ 같은"), g("those advocating for", "~을 주장하는 사람들"),
                    g("just sustainabilities", "정당한 지속 가능성"), g("complete streets", "완전 도로"), g("find", "여기다"),
                    g("both approaches", "두 접근법 모두"), g("are overly idealistic", "지나치게 이상적이다"),
                    g("neither pays enough attention to", "어느 쪽도 ~에 충분히 주의를 기울이지 않는다"),
                    g("the realities", "현실"), g("social dynamics", "사회적 역학 관계"), g("systemic inequality", "구조적 불평등")],
        "slashes": ["Still others,", "“just sustainabilities”", "“complete streets,”", "find", "overly idealistic", "enough attention",
                    "social dynamics"],
        "roles": [r("Still others", "S"), r("find", "V"), r("both approaches", "S"), r("are", "V"), r("overly idealistic", "C"), r("neither", "S"),
                  r("pays", "V"), r("enough attention", "O")],
        "modifiers": ["such as those advocating for “just sustainabilities” or “complete streets,”"],
        "steps": [
            choice("a2_both",
                   "'both approaches(두 접근법 모두)'라고 하려면, 앞에서 무엇이 나왔어야 할까요?",
                   [("o0", "한 가지 접근법만", False), ("o1", "두 가지 접근법이 모두", True), ("o2", "아무 접근법도", False)],
                   "both는 '둘 다'예요. 둘 다라고 하려면 두 가지가 이미 소개됐어야 해요.",
                   why="both approaches는 '두 접근법 모두'예요. 두 방식이 다 소개된 뒤라야 '둘 다 이상적'이라고 묶을 수 있어요.",
                   highlight=["both approaches"],
                   tips=[tip("Still others", "'또 다른 사람들은'이에요. 앞에서 누군가의 의견이 나온 뒤, 또 다른 의견을 더할 때 써요.", "Still others")],
                   point="(A) 끝 both approaches = 두 방식이 모두 나온 뒤 → (A)는 두 방식이 다 소개된 다음"),
            show("a2_end", "(A)는 '두 방식 모두 지나치게 이상적이다'라는, 또 다른 사람들의 평가로 끝나요.",
                 highlight=["overly idealistic"], button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": B1, "teaching_value": "high",
        "model_translation": "(B) 그러나 비판가들은 경관 도시론자들이 인간의 필요보다 미적, 그리고 생태적 관심사를 우선시한다고 주장한다.",
        "glosses": [g("However", "그러나"), g("critics", "비판가들"), g("claim", "주장하다"), g("Landscape Urbanists", "경관 도시론자들"),
                    g("prioritize", "우선시하다"), g("aesthetic and ecological concerns", "미적·생태적 관심사"),
                    g("over human needs", "인간의 필요보다")],
        "slashes": ["However,", "critics claim", "Landscape Urbanists prioritize", "ecological concerns"],
        "roles": [r("critics", "S"), r("claim", "V"), r("Landscape Urbanists", "S"), r("prioritize", "V"), r("aesthetic and ecological concerns", "O")],
        "steps": [
            choice("b_before",
                   "(B)는 '비판가들은 경관 도시론자들이 인간의 필요보다 미적·생태적 관심을 우선한다고 주장한다'로 시작해요. 앞에는 무엇이 와야 할까요?",
                   [("o0", "경관 도시론이 어떤 방식인지 소개", True), ("o1", "두 방식이 모두 이상적이라는 평가", False),
                    ("o2", "주어진 글의 역사적인 생각", False)],
                   "비판하려면 먼저 그 대상이 소개돼야 해요. 무엇을 비판하는지 봐요.",
                   why="비판가들이 경관 도시론자들을 비판해요. 비판하려면 앞에서 경관 도시론이 무엇인지 먼저 소개돼야 해요.",
                   highlight=["critics claim", "Landscape Urbanists"],
                   tips=[tip("prioritize A over B", "'B보다 A를 우선시하다'예요. 여기서는 사람의 필요보다 아름다움·생태를 앞세운다는 비판이에요.", "prioritize")],
                   point="(B) critics claim that Landscape Urbanists … ← 앞에서 경관 도시론이 소개돼야 한다"),
        ],
    },
    {
        "id": 5, "text": B2, "teaching_value": "high",
        "model_translation": "대조적으로 신도시론은 1980년대에 대중화된 접근법이고 걸을 수 있는 거리, 고밀도 디자인, 그리고 복합 용도 개발을 장려한다.",
        "glosses": [g("In contrast", "그와 대조적으로"), g("New Urbanism", "신도시론"), g("is an approach", "~한 접근법이다"),
                    g("was popularized", "대중화되었다"), g("in the 1980s", "1980년대에"), g("promotes", "장려하다"),
                    g("walkable streets", "걷기 좋은 거리"), g("compact design", "고밀도(촘촘한) 설계"), g("mixed-use developments", "복합 용도 개발")],
        "slashes": ["In contrast,", "is an approach", "in the 1980s", "walkable streets,"],
        "roles": [r("New Urbanism", "S"), r("is", "V"), r("an approach", "C")],
        "modifiers": ["that was popularized in the 1980s and promotes walkable streets, compact design, and mixed-use developments"],
        "steps": [
            choice("b2_next",
                   "(B)는 새 방식 New Urbanism(신도시론) 소개로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "신도시론에 대한 다른 쪽의 반응이나 비판", True), ("o1", "경관 도시론이 무엇인지 처음 소개", False),
                    ("o2", "도시 계획의 역사적인 생각", False)],
                   "In contrast로 두 번째 방식이 나왔어요. 새 방식이 나오면 그 방식에 대한 반응이 이어지기 쉬워요.",
                   why="새 방식(신도시론)이 나왔으니, 다음엔 그 방식을 두고 누가 어떻게 보는지가 이어지기 쉬워요. 경관 도시론은 이미 비판까지 받았어요.",
                   highlight=["In contrast", "New Urbanism"]),
        ],
    },
    {
        "id": 6, "text": C1, "teaching_value": "high",
        "model_translation": "(C) 그러나 이러한 접근 방식에서 사회 정의의 역할은 논란의 소지가 많이 남아 있다.",
        "glosses": [g("However", "그러나"), g("the role of social justice", "사회 정의의 역할"), g("in these approaches", "이 접근법들에서"),
                    g("remains", "여전히 ~이다"), g("highly controversial", "논란이 많은")],
        "slashes": ["However,", "social justice", "these approaches"],
        "roles": [r("the role of social justice", "S"), r("remains", "V"), r("highly controversial", "C")],
        "steps": [
            choice("c_before",
                   "'these approaches(이 접근법들)'는 앞의 무엇을 받을까요?",
                   [("o0", "신도시론 한 가지", False), ("o1", "두 방식이 모두 이상적이라는 평가", False),
                    ("o2", "지속 가능한 도시 계획의 여러 해석(방식)", True)],
                   "approaches가 여러 개(복수)예요. 여러 방식이 한꺼번에 나온 곳을 떠올려 봐요.",
                   why="these approaches는 여러 방식이에요. 주어진 글 끝의 various interpretations(여러 해석)을 받아요.",
                   highlight=["these approaches"],
                   tips=[tip("these + 복수 명사", "these는 앞에서 말한 여러 개를 가리켜요. 바로 앞에 복수로 받을 말이 있어야 해요.", "these")],
                   point="(C) these approaches ← 주어진 글 various interpretations of sustainable urban planning"),
        ],
    },
    {
        "id": 7, "text": C2, "teaching_value": "high",
        "model_translation": "예를 들어, 경관 도시론은 매우 적은 자원 사용을 필요로 하고 다양한 종과 경관을 포함하면서 자연 서식지 설계를 옹호하는 비교적 최근에 등장한 계획 접근 방식이다.",
        "glosses": [g("For example", "예를 들어"), g("Landscape Urbanism", "경관 도시론"), g("is a relatively recent planning approach", "비교적 최근의 계획 방식이다"),
                    g("advocates for", "~을 옹호하다, 주장하다"), g("native habitat designs", "자연 서식지 설계"),
                    g("include diverse species and landscapes", "다양한 종과 경관을 포함하다"),
                    g("require very low resource use", "자원을 아주 적게 쓰다")],
        "slashes": ["For example,", "planning approach", "native habitat designs", "species and landscapes"],
        "roles": [r("Landscape Urbanism", "S"), r("is", "V"), r("a relatively recent planning approach", "C")],
        "modifiers": ["that advocates for native habitat designs that include diverse species and landscapes that require very low resource use"],
        "steps": [
            choice("c2_next",
                   "(C)는 경관 도시론 소개로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "경관 도시론자들이 다른 설계를 비판하는 내용", False),
                    ("o1", "경관 도시론이 사람의 필요를 뒷전으로 한다는 비판", True), ("o2", "도시 계획의 역사", False)],
                   "(C)는 '사회 정의의 역할이 논란'이라며 그 예로 경관 도시론을 들었어요. 그 논란이 무엇인지 이어지기 쉬워요.",
                   why="(C)는 사회 정의가 논란이라며 예로 경관 도시론을 소개했어요. 그러니 다음엔 경관 도시론이 사람의 필요를 뒤로 미룬다는 비판이 이어져야 자연스러워요.",
                   highlight=["For example", "Landscape Urbanism"],
                   point="(C) 끝 경관 도시론 소개 → 다음은 그 경관 도시론에 대한 비판(사람의 필요를 뒷전)"),
            order_link(
                card("given", "주어진 글", last=("… various interpretations of sustainable urban planning", "지속 가능한 도시 계획의 여러 해석")),
                [card("A", "(A)", first=("But Landscape Urbanists find that these designs do not prioritize …", "경관 도시론자들은 이 설계들이 자연을 우선하지 않는다고 본다"),
                      last=("… both approaches are overly idealistic", "두 방식 모두 지나치게 이상적")),
                 card("B", "(B)", first=("However, critics claim that Landscape Urbanists prioritize …", "비판가들은 경관 도시론자들이 ~을 우선한다고 주장"),
                      last=("In contrast, New Urbanism is an approach …", "대조적으로 신도시론은 ~한 방식")),
                 card("C", "(C)", first=("However, the role of social justice in these approaches …", "이 방식들에서 사회 정의의 역할은 논란"),
                      last=("For example, Landscape Urbanism is a relatively recent planning approach …", "예를 들어 경관 도시론은 최근의 방식"))],
                ["C", "B", "A"],
                "주어진 글(여러 해석) → (C) these approaches, 예: 경관 도시론 → (B) 경관 도시론 비판, 대조: 신도시론 → (A) these designs(신도시론) 비판, 두 방식 모두 이상적 순서예요."),
            show("c_go", "직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?", button="문제 풀러 갈게요"),
        ],
    },
]

add_that_sv(sentences, 2, "a_sv", "a_that_sv", ["Landscape Urbanists", "these designs", "do not prioritize", "the natural environment"],
            {"these designs": "S", "do not prioritize": "V", "the natural environment": "O"},
            {"Landscape Urbanists": "그건 문장 전체의 주어예요. that 뒤에서 찾아봐요."},
            "that 뒤는 주어 these designs, 동사 do not prioritize, 목적어 the natural environment예요.",
            ask="that 뒤가 핵심 내용이에요. that 안에서 주어(S), 동사(V), 목적어(O)를 찾아볼까요?")

add_basic(sentences, 4, [m("However", "그러나"), ", ", m("critics", "비판가들은"), " ", m("Landscape Urbanists", "경관 도시론자들이"), " ",
                         m("over human needs", "인간의 필요보다"), " ", m("aesthetic and ecological concerns", "미적·생태적 관심사"), "를 ",
                         m("prioritize", "우선시한다고"), " ", m("claim", "주장한다"), "."],
          sv_new=sv_step("b_basic_sv", ["critics", "claim", "Landscape Urbanists", "prioritize"],
                         {"critics": "S", "claim": "V"},
                         {"Landscape Urbanists": "그건 that 뒤 덩어리 안의 주어예요.", "prioritize": "그건 that 뒤 덩어리 안의 동사예요."},
                         "주어는 critics, 동사는 claim이에요. that 뒤가 주장하는 내용이에요."),
          meaning_after="b_before",
          meaning="비판가들은 경관 도시론자들이 사람의 필요보다 아름다움과 생태를 앞세운다고 주장한대요.")
add_basic(sentences, 5, [m("In contrast", "대조적으로"), ", ", m("New Urbanism", "신도시론은"), " ", m("walkable streets", "걷기 좋은 거리"), "와 ",
                         m("compact design", "촘촘한 설계"), "를 ", m("promotes", "장려한다"), "."],
          match_display="In contrast, New Urbanism promotes walkable streets, compact design, and mixed-use developments.",
          sv_new=sv_step("b2_basic_sv", ["New Urbanism", "is", "an approach", "was popularized", "promotes"],
                         {"New Urbanism": "S", "is": "V", "an approach": "C"},
                         {"was popularized": "그건 that 뒤 덩어리 안의 동사예요.", "promotes": "그건 that 뒤 덩어리 안의 동사예요(장려하는)."},
                         "주어는 New Urbanism, 동사는 is, 보어는 an approach예요. that 뒤가 어떤 방식인지 꾸며요."),
          meaning_after="b2_next",
          meaning="신도시론은 1980년대에 퍼진 방식으로, 걷기 좋은 거리와 촘촘한 설계, 여러 용도를 섞은 개발을 장려한대요.")
add_basic(sentences, 6, [m("However", "그러나"), ", ", m("in these approaches", "이 접근법들에서"), " ", m("the role of social justice", "사회 정의의 역할은"), " ",
                         m("highly controversial", "논란이 많은 채로"), " ", m("remains", "남아 있다"), "."],
          sv_new=sv_step("c_basic_sv", ["the role of social justice", "these approaches", "remains", "highly controversial"],
                         {"the role of social justice": "S", "remains": "V", "highly controversial": "C"},
                         {"these approaches": "그건 in 뒤 덩어리예요. 전치사 뒤라 주어가 아니에요."},
                         "주어는 the role of social justice, 동사는 remains, 보어는 highly controversial이에요."),
          meaning_after="c_before",
          meaning="이 방식들에서 사회 정의(공정함)가 어떤 역할을 하는지는 여전히 논란이 많대요.")
add_basic(sentences, 7, [m("For example", "예를 들어"), ", ", m("Landscape Urbanism", "경관 도시론은"), " ", m("native habitat designs", "자연 서식지 설계"), "를 ",
                         m("advocates for", "옹호하는"), " ", m("is a relatively recent planning approach", "비교적 최근의 계획 방식이다"), "."],
          match_display="For example, Landscape Urbanism is a relatively recent planning approach that advocates for native habitat designs.",
          sv_new=sv_step("c2_basic_sv", ["Landscape Urbanism", "is", "a relatively recent planning approach", "advocates for"],
                         {"Landscape Urbanism": "S", "is": "V", "a relatively recent planning approach": "C"},
                         {"advocates for": "그건 that 뒤 덩어리 안의 동사예요(옹호하는)."},
                         "주어는 Landscape Urbanism, 동사는 is, 보어는 a relatively recent planning approach예요."),
          meaning_after="c2_next",
          meaning="경관 도시론은 비교적 최근 방식으로, 다양한 생물이 사는 자연 서식지 설계를 옹호하고 자원을 아주 적게 쓴대요.")

SENSES = {
    2: [sense("but", "But Landscape Urbanists", "그러나", "접속사 but (문장 앞)"),
        sense("that", "find that these designs", "~라는 것을", "명사절 that (find that …)")],
    3: [sense("as", "such as those", "~ 같은", "such as + 명사 (예시)"),
        sense("for", "advocating for", "~을 (주장하는)", "advocate for + 명사 = ~을 지지·주장하다"),
        sense("that", "find that both approaches", "~라는 것을", "명사절 that (find that …)"),
        sense("to", "attention to the realities", "~에 (주의를 기울이다)", "pay attention to + 명사")],
    4: [sense("that", "claim that Landscape Urbanists", "~라고", "명사절 that (claim that …)")],
    5: [sense("that", "an approach that was popularized", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    7: [sense("for", "For example", "(For example의 일부)", "For example = 예를 들어"),
        sense("that", "approach that advocates", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("for", "advocates for", "~을 (옹호하다)", "advocate for + 명사"),
        sense("that", "designs that include", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("that", "landscapes that require", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
}

WORDS = {"historic": "역사적인", "ideas": "생각들", "nature": "자연", "urban/suburban": "도시·교외의", "space": "공간",
         "various": "여러 가지의", "interpretations": "해석", "sustainable": "지속 가능한", "urban": "도시의", "planning": "계획",
         "landscape": "경관, 풍경", "urbanists": "도시론자들", "designs": "설계들", "prioritize": "우선시하다", "natural": "자연의",
         "environment": "환경", "involve": "수반하다", "diverting": "방향을 바꾸는", "streams": "하천, 개울", "disrupting": "망가뜨리는",
         "wetlands": "습지", "advocating": "주장하는", "just": "정당한, 공정한", "sustainabilities": "지속 가능성",
         "complete": "완전한", "streets": "거리, 도로", "approaches": "접근법들", "overly": "지나치게", "idealistic": "이상적인",
         "pays": "기울이다(주의를)", "enough": "충분한", "attention": "주의", "realities": "현실", "social": "사회의",
         "dynamics": "역학 관계", "systemic": "구조적인, 체계의", "inequality": "불평등", "aesthetic": "미적인", "ecological": "생태적인",
         "concerns": "관심사", "human": "인간의", "needs": "필요", "contrast": "대조", "urbanism": "도시론", "approach": "접근법",
         "popularized": "대중화된", "1980s": "1980년대", "walkable": "걷기 좋은", "compact": "촘촘한, 고밀도의", "design": "설계",
         "mixed-use": "복합 용도의", "developments": "개발", "role": "역할", "justice": "정의", "highly": "매우",
         "controversial": "논란이 많은", "example": "예", "relatively": "비교적", "recent": "최근의", "advocates": "옹호하다",
         "native": "토종의, 자연 그대로의", "habitat": "서식지", "include": "포함하다", "diverse": "다양한", "species": "종(생물)",
         "landscapes": "경관", "require": "필요로 하다", "low": "적은", "resource": "자원", "very": "매우", "often": "흔히",
         "still": "그래도, 또", "neither": "어느 쪽도 ~않다", "both": "둘 다", "expression": "표현", "integrating": "합치는 것"}

OPTIONS = [("1", "(A)-(C)-(B)", False), ("2", "(B)-(A)-(C)", False), ("3", "(B)-(C)-(A)", False), ("4", "(C)-(A)-(B)", False), ("5", "(C)-(B)-(A)", True)]
exam = {
    "question": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?",
    "sentence": 1, "analysis_first": True, "wrong_rate": 67.3, "wrong_rank": 4, "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], **({"correct": True} if o[2] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "단락 첫머리 단서(these approaches, critics claim, these designs, both approaches)를 떠올리며 순서를 골라 봐요.",
        "정답이에요! 여러 해석 → (C) 이 방식들의 사회 정의 논란, 예: 경관 도시론 → (B) 경관 도시론 비판, 대조: 신도시론 → (A) 신도시론 설계 비판, 두 방식 모두 이상적, 순서예요.",
        "정답은 ⑤ (C)-(B)-(A)예요.",
        {"1": "(A)의 these designs와 both approaches가 받을 설계 방식이 주어진 글에는 아직 없어요.",
         "2": "(B)는 경관 도시론자들을 비판해요. 경관 도시론이 소개되기 전에 비판부터 올 수 없어요.",
         "3": "(B)가 주어진 글 바로 뒤에 오면, 아직 소개도 안 된 경관 도시론을 비판하게 돼요.",
         "4": "많이 고른 오답이에요. (A)의 these designs는 자연을 중시하지 않는 설계라 경관 도시론이 아니에요. 그리고 both approaches는 두 방식이 다 나온 뒤에 와야 해요."},
        {"4": review(31.3,
                     "(C) 끝이 Landscape Urbanism이라 바로 뒤에 Landscape Urbanists로 시작하는 (A)를 붙이기 쉬워요. 하지만 (A)는 경관 도시론자들이 these designs가 자연을 중시하지 않는다고 비판하는 말이에요. 자연 서식지를 옹호하는 경관 도시론의 설계를 가리킬 수 없고, both approaches도 두 방식이 다 나온 뒤라야 해요.",
                     "그래서 ④가 아니에요. 어디서 헷갈렸어요?",
                     [("같은 단어(Landscape)로 이었어요", ["same_word_link"],
                       "알려 줘서 고마워요. 같은 단어가 반복된다고 바로 이어지는 건 아니에요. these designs처럼 가리키는 말이 무엇을 받는지 봐야 해요. 앞으로 이 점을 강조해서 알려 줄게요."),
                      ("these designs가 무엇인지 못 봤어요", ["these_refers"],
                       "알려 줘서 고마워요. these designs는 '자연을 우선하지 않는' 설계라서 신도시론이에요. 앞으로 these가 가리키는 대상을 먼저 짚어 줄게요."),
                      ("둘 다요", ["same_word_link", "these_refers"], "알려 줘서 고마워요. 앞으로 가리키는 말부터 같이 짚어 볼게요.")],
                     panel=rows(("(C) 끝", "Landscape Urbanism … native habitat designs", "경관 도시론 = 자연 서식지 옹호", "hl"),
                                ("(A) 첫머리", "these designs do not prioritize the natural environment", "자연을 우선하지 않는 설계 = 신도시론", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 37번 (글의 순서, 2점)",
    topic="순서 푸는 법: 주어진 글의 끝 → 단락 첫머리 단서로 앞 내용 예측 → 단락 끝으로 다음 내용 예측 → 순서 잇기",
    method={"type": "order", "labels": ["단락 요지 잡기", "연결 단서 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-urban-planning.svg", ("Nature", "자연"), "+", ("City", "도시"),
                                       "자연과 도시를 합치는 방법은 하나일까?", "2024년 3월 37번 도입 칠판"),
                      "alt": "칠판: Nature(자연) + City(도시)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "도시에 자연을 들이는 방법은 하나뿐일까요? 이번 글은 지속 가능한 도시 계획의 여러 방식과 그 비판을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "순서 문제는 단락 첫머리의 단서가 앞 내용과 이어지는지 보는 거예요. these, However, But 같은 말이 무엇을 받는지 찾아볼게요."}}],
    exam=exam,
    key_words={"passage": [g("integrate", "통합하다"), g("sustainable", "지속 가능한"), g("interpretation", "해석"), g("prioritize", "우선시하다"),
                           g("divert", "방향을 바꾸다"), g("advocate for", "~을 옹호하다"), g("overly", "지나치게"), g("idealistic", "이상적인"),
                           g("inequality", "불평등"), g("critic", "비판가"), g("aesthetic", "미적인"), g("ecological", "생태적인"),
                           g("popularize", "대중화하다"), g("controversial", "논란이 많은"), g("habitat", "서식지"), g("diverse", "다양한")],
               "options": []},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="순서 푸는 법",
       chunks={"historic ideas": "역사적인 생각들", "find": "찾다", "expression": "표현", "various interpretations": "여러 가지 해석",
               "Today": "오늘날", "integrating nature and urban/suburban space": "자연과 도시·교외 공간을 합치는 것",
               "Landscape Urbanists": "경관 도시론자들", "these designs": "이 설계들", "do not prioritize": "우선시하지 않는다",
               "the natural environment": "자연 환경", "But": "그러나", "critics": "비판가들", "claim": "주장하다", "prioritize": "우선시하다",
               "New Urbanism": "신도시론", "is": "~이다", "an approach": "접근법", "was popularized": "대중화되었다", "promotes": "장려하다",
               "the role of social justice": "사회 정의의 역할", "these approaches": "이 접근법들", "remains": "여전히 ~이다",
               "highly controversial": "논란이 많은", "Landscape Urbanism": "경관 도시론",
               "a relatively recent planning approach": "비교적 최근의 계획 방식", "advocates for": "옹호하다"})
