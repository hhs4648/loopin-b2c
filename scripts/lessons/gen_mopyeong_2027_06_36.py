"""2026년 6월 모의평가(2027학년도, 평가원) 36번 레슨 + 대사를 만든다 (글의 순서, 2점). 오답률 57% · Top 8 (메가스터디 풀서비스 채점 기준).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_36.py   (→ npm run policy:copy stamp <id> → npx vitest run src/tutor/policy)

틀: docs/tutor/templates/order.md — 주어진 글의 끝 → 단락 첫머리(앞에 무엇?) → 단락 끝(다음에 무엇?) → 순서 잇기.
정답 ⑤ (C)-(B)-(A). 많이 고른 오답 ③ (B)-(C)-(A) 26% — 주어진 글의 harsh compounds(독한 화합물)와 (B)의 chemical compounds(화학
화합물)가 같은 말이라 (B)를 바로 이었다. 그러나 (B)는 이웃·포식자와 「함께」 막는 방어라서 (C) 끝 Nor … on their own(혼자인 것도
아니다)이 먼저 와야 한다. (A) The back-and-forth(이 공방전)는 방어 이야기를 다 묶는 말이라 맨 끝.
해설지 해석·Words and Phrases와 대조함 (content/tutor/exam-source/2027-06-평가원/해설.txt) — back-and-forth '공방전', select for '~을 선택하다',
get around '우회하다', in turn '결국', shade into '(점차) ~으로 변해가다', call for '요청', altogether '아예'.
genera, resilient, stalemate는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다(뜻만 둠).
반영한 규칙: 2026-10-20 끊어읽기(slashes·roles·modifiers), S·V 찾기 없음, 핵심어 나열형 해석 없음, 2026-10-21 제출·보기 해설까지.

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- (B) 첫 문장엔 앞을 받는 말(This·also·Nor 같은)이 없어서 「앞에 무엇이 와야 할까요?」(_before)를 넣지 않았다 — 근거 없이 답에서 거꾸로
  맞춘 질문이 될까 봐(insertion-given-sentence-order). 대신 (B) 끝에서 「혼자 하는 방어인가, 함께 하는 방어인가」를 묻고 칠판에 나눴다
- 칠판 「식물의 방어」: 왼쪽 by itself(혼자) — harsh compounds · thick coats of wax / 오른쪽 with others(함께) — same-species neighbors ·
  insect predators. 칸 이름(혼자/함께)은 글에 그대로 나온 말이 아니라 (B)의 neighbors·collaborators를 보고 지은 것. (C) 끝 on their own을
  읽기 전에 「혼자」라는 말이 칠판에 먼저 나오는 셈이라, 빼야 하면 알려 주세요
- 주어진 글 g_next 「다음엔 다른 방어가 더 나오기 쉽다」 — 첫 문장 「방어가 아주 다양하다」 + Some(어떤 식물은)으로 하나만 들었다는 근거
- (C) 첫 문장은 Structural(구조적)이라고 종류를 밝힌 것을 근거로 「앞에 다른 종류(화학)의 방어」를 묻는다
- 헷갈리는 단어(trap): compound(복합의 ✕ → 화합물), back-and-forth(왔다 갔다 ✕ → 공방전)
- 해석 맞추기(add_match): (A) 첫 문장, (C) 끝 문장(Nor). Nor 문장은 맞추기가 뜻 확인을 대신해서 따로 설명 화면을 두지 않았다
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from order_tools import card, order_link  # noqa: E402
from beginner import add_match, add_refers, m  # noqa: E402

ID = "mopyeong-2027-06-36-plant-defenses"

G1 = "Plants have evolved defenses almost as diverse as the number of genera."
G2 = ("Some load their tissues with harsh compounds that either are unpleasant to insects or intoxicate them, encouraging the "
      "insects to go bother another plant or at least slowing down their eating.")
A1 = "(A) The back-and-forth is not a matter of natural balance, but more like a drawn-out evolutionary conversation."
A2 = ("New plant defenses unintentionally select for insects with ways to get around them, which in turn help bring about more "
      "resilient and resistant plant species.")
A3 = "New variations, shading into entire new forms and adaptations, maintain the stalemate."
B1 = ("(B) Plants can release chemical compounds that let their same-species neighbors know that an attack is likely coming, "
      "pushing those nearby plants to start building up defensive compounds in their tissues.")
B2 = ("Some of these cues even attract insect predators, a call for an assist that benefits both the plant and its bug-eating "
      "collaborators.")
C1 = ("(C) Structural defenses like thick coats of wax on leaves may prevent some insect species from damaging the plant tissues "
      "altogether.")
C2 = "Nor are individual plants entirely on their own while under attack."

ALONE = "by itself (혼자)"
TOGETHER = "with others (함께)"


def board(left, right, fresh=()):
    return groups("식물의 방어 (defenses)", ALONE, left, TOGETHER, right, fresh=fresh, between="/")


L_GIVEN = [("harsh compounds", "독한 화합물")]
R_B = [("same-species neighbors", "같은 종 이웃"), ("insect predators", "곤충의 포식자")]

sentences = [
    {
        "id": 1, "label": "주어진 글", "text": G1, "teaching_value": "high",
        "model_translation": "식물들은 거의 그 속의 수만큼이나 다양한 방어 기제를 진화시켜 왔다.",
        "glosses": [g("Plants", "식물들은"), g("have evolved", "진화시켜 왔다"), g("evolved", "진화시킨"), g("defenses", "방어 (기제)"),
                    g("almost as diverse as", "거의 ~만큼이나 다양한"), g("diverse", "다양한"),
                    g("the number of genera", "속(屬)의 수"), g("genera", "속(屬) · genus의 복수, 생물을 나누는 단위예요")],
        "slashes": ["Plants have evolved defenses"],
        "roles": [r("Plants", "S"), r("have evolved", "V"), r("defenses", "O")],
        "modifiers": ["almost as diverse as the number of genera"],
        "steps": [
            choice("g_diverse",
                   "식물의 방어(defenses)는 어떻대요?",
                   [("o0", "아주 여러 가지다", True), ("o1", "거의 다 비슷하다", False), ("o2", "곤충 한 종류만 막는다", False)],
                   "as diverse as를 봐요. as + 형용사 + as는 '~만큼 …한'이에요.",
                   why="'almost as diverse as the number of genera', 생물을 나누는 속(genera)의 수만큼이나 다양하대요.",
                   highlight=["defenses", "diverse"],
                   tips=[tip("as + 형용사 + as", "'~만큼 …한'이에요. as diverse as the number of genera = 속의 수만큼 다양한.", "as diverse")]),
        ],
    },
    {
        "id": 2, "text": G2, "teaching_value": "high",
        "model_translation": "어떤 식물은 자신의 조직을 곤충에게 불쾌감을 주거나 곤충을 취하게 만드는 독한 화합물로 채워서, 곤충이 다른 식물을 괴롭히러 가도록 유도하거나 적어도 곤충이 먹이를 먹는 속도를 늦춘다.",
        "glosses": [g("Some", "어떤 것들(식물들)은"), g("load", "채우다, 싣다"), g("their tissues", "자기 조직"), g("tissues", "(생물의) 조직"),
                    g("harsh compounds", "독한 화합물"), g("harsh", "독한"), g("compounds", "화합물"),
                    g("that either are unpleasant to insects or intoxicate them", "곤충에게 불쾌감을 주거나 곤충을 취하게 하는"),
                    g("unpleasant", "불쾌한"), g("intoxicate", "취하게 하다"),
                    g("encouraging the insects to go bother another plant", "곤충이 다른 식물을 괴롭히러 가도록 부추겨"),
                    g("bother", "괴롭히다"), g("at least", "적어도"), g("slowing down their eating", "먹는 속도를 늦추어"),
                    g("slowing down", "늦추는")],
        "slashes": ["Some load their tissues", "with harsh compounds", "unpleasant to insects", "intoxicate them,", "encouraging the insects",
                    "another plant"],
        "roles": [r("Some", "S"), r("load", "V"), r("their tissues", "O")],
        "modifiers": ["that either are unpleasant to insects or intoxicate them"],
        "steps": [
            choice("g_some",
                   "둘째 문장은 Some(어떤 식물은)으로 시작해요. 이 식물들은 곤충을 어떻게 막을까요?",
                   [("o0", "자기 조직을 독한 화합물로 채운다", True), ("o1", "곤충을 직접 잡아먹는다", False),
                    ("o2", "잎을 떨어뜨려 숨긴다", False)],
                   "load their tissues with harsh compounds를 봐요. load A with B는 'A를 B로 채우다'예요.",
                   why="'load their tissues with harsh compounds', 조직 안을 독한 화합물(harsh compounds)로 채운대요. 곤충은 불쾌하거나 취해서 다른 식물로 가게 돼요.",
                   highlight=["harsh compounds"],
                   tips=[tip("compound", "평소엔 '복합의, 합성의'로 알기 쉬워요. 여기서는 '화합물'이에요.", "compounds", trap=True),
                         tip("load A with B", "'A를 B로 채우다'예요. load their tissues with harsh compounds = 조직을 독한 화합물로 채우다.", "load"),
                         tip("either A or B", "'A이거나 B'예요. either are unpleasant to insects or intoxicate them = 곤충에게 불쾌하거나 곤충을 취하게 하다.", "either"),
                         tip("encourage + 대상 + to ~", "'~가 …하도록 부추기다'예요. encouraging the insects to go bother another plant = 곤충이 다른 식물을 괴롭히러 가게 하다.", "encouraging")]),
            choice("g_next",
                   "주어진 글은 '어떤 식물(Some)은 독한 화합물로 곤충을 쫓는다'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "독한 화합물이 곤충 몸에서 일으키는 변화", False), ("o1", "식물이 쓰는 또 다른 방어", True),
                    ("o2", "식물이 곤충을 막지 못하는 이유", False)],
                   "첫 문장에서 방어가 아주 다양하다고 했어요. Some(어떤 식물은)은 그중 하나만 보여 준 거예요.",
                   why="방어가 아주 다양하다고 하고 Some(어떤 식물은)으로 하나를 들었어요. 그러니 다음엔 다른 방어가 더 나오기 쉬워요.",
                   highlight=["Some", "harsh compounds"],
                   point="주어진 글 끝 '어떤 식물(Some)은 독한 화합물' → 다음은 또 다른 방어"),
            show("paper_order", "이제 (A)·(B)·(C)를 시험지 순서대로 읽어요. 단락마다 첫머리와 끝을 잘 봐 두면 좋아요.",
                 button="(A)부터 읽어 볼게요"),
        ],
    },
    {
        "id": 3, "text": A1, "teaching_value": "high",
        "model_translation": "(A) 이러한 공방전은 자연적 균형의 문제가 아니라 오히려 길게 이어지는 진화적 대화에 가깝다.",
        "glosses": [g("The back-and-forth", "이 공방전, 이 주고받기"), g("back-and-forth", "공방전 · 서로 주고받는 것"),
                    g("a matter of", "~의 문제"), g("natural balance", "자연적 균형"), g("balance", "균형"),
                    g("more like", "오히려 ~에 가까운"), g("drawn-out", "길게 이어지는"), g("evolutionary", "진화의, 진화적인"),
                    g("conversation", "대화")],
        "slashes": ["The back-and-forth", "natural balance,"],
        "roles": [r("The back-and-forth", "S"), r("is not", "V"), r("a matter of natural balance", "C"),
                  r("more like a drawn-out evolutionary conversation", "C")],
        "steps": [
            choice("a_before",
                   "(A)는 'The back-and-forth(이 주고받기)는 자연의 균형이 아니라 길게 이어지는 진화의 대화에 가깝다'로 시작해요. 앞에는 무엇이 와야 할까요?",
                   [("o0", "식물이 막고 곤충이 버티는, 주고받는 이야기", True), ("o1", "자연은 늘 균형을 이룬다는 설명", False),
                    ("o2", "곤충이 모두 사라졌다는 이야기", False)],
                   "The back-and-forth의 The를 봐요. 앞에서 이미 나온 주고받기를 가리켜요.",
                   why="The back-and-forth(그 주고받기)는 앞에서 식물과 곤충이 공격과 방어를 주고받은 것을 받는 말이에요. not a matter of natural balance는 글쓴이가 '균형 문제가 아니다'라고 바로잡는 말이에요.",
                   highlight=["The back-and-forth"],
                   tips=[tip("back-and-forth", "평소엔 '왔다 갔다'로 알기 쉬워요. 여기서는 식물과 곤충이 공격·방어를 주고받는 '공방전'이에요.", "back-and-forth", trap=True),
                         tip("not A but B", "'A가 아니라 B'예요. not a matter of natural balance, but more like … conversation = 균형의 문제가 아니라 대화에 가깝다.", "not")],
                   point="(A) The back-and-forth ← 앞에 식물과 곤충이 주고받은 방어 이야기"),
        ],
    },
    {
        "id": 4, "text": A2, "teaching_value": "medium",
        "model_translation": "식물의 새로운 방어 기제는 의도치 않게 그것을 우회할 방법을 지닌 곤충들을 선택하게 되고, 이는 결국 더 회복력과 저항력이 강한 식물 종이 나타나도록 돕는다.",
        "glosses": [g("New plant defenses", "식물의 새로운 방어"), g("unintentionally", "의도치 않게"),
                    g("select for", "~을 선택하다 · 그런 것이 살아남게 하다"), g("insects", "곤충들"), g("ways", "방법"),
                    g("get around", "우회하다, 피해 가다"), g("them", "그것들을"), g("in turn", "결국, 이번엔 또"),
                    g("help bring about", "~이 생겨나도록 돕다"), g("bring about", "생겨나게 하다, 일으키다"),
                    g("resilient", "회복 탄력성이 있는"), g("resistant", "저항력 있는"),
                    g("resistant plant species", "저항력 있는 식물 종"), g("species", "종")],
        "slashes": ["New plant defenses", "select for insects", "with ways", "get around them,", "in turn"],
        "roles": [r("New plant defenses", "S"), r("select for", "V"), r("insects", "O")],
        "modifiers": ["which in turn help bring about more resilient and resistant plant species"],
        "steps": [
            show("a2_mid", "식물이 새 방어를 만들면 그걸 피해 갈 방법을 지닌 곤충이 선택되고, 그 곤충이 다시 더 강한 식물 종이 나오게 돕는대요.",
                 highlight=["get around them", "resistant plant species"],
                 tips=[tip("select for", "'~을 (살아남도록) 선택하다'예요. 새 방어가 그걸 피할 수 있는 곤충을 남게 만든다는 말이에요.", "select"),
                       tip("in turn", "'결국, 이번엔 또'예요. 곤충이 다시 식물 쪽에 영향을 준다는 흐름이에요.", "in turn")],
                 panel=groups("The back-and-forth (공방전)", "Plants (식물)", [("new plant defenses", "새 방어"), ("resistant plant species", "더 강한 식물 종")],
                              "Insects (곤충)", [("ways to get around them", "피해 갈 방법")], between="⇄",
                              fresh=("new plant defenses", "resistant plant species", "ways to get around them"))),
        ],
    },
    {
        "id": 5, "text": A3, "teaching_value": "medium",
        "model_translation": "새로운 변이들은 완전히 새로운 형태와 적응으로 점차 변해가며 그 교착 상태를 유지한다.",
        "glosses": [g("New variations", "새로운 변이들"), g("variations", "변이"), g("shading into", "점차 ~으로 변해 가는"),
                    g("entire new forms and adaptations", "완전히 새로운 형태와 적응"), g("entire", "완전한"), g("forms", "형태"),
                    g("adaptations", "적응"), g("maintain", "유지하다"), g("the stalemate", "그 교착 상태"),
                    g("stalemate", "교착 상태 · 어느 쪽도 이기지 못하는 상태")],
        "slashes": ["New variations,", "and adaptations,"],
        "roles": [r("New variations", "S"), r("maintain", "V"), r("the stalemate", "O")],
        "modifiers": ["shading into entire new forms and adaptations"],
        "steps": [
            show("a3_end", "(A)는 새 변이들이 교착 상태(stalemate)를 계속 유지한다는 말로 끝나요. 어느 한쪽이 이기지 않고 주고받기가 이어진다는 뜻이에요.",
                 highlight=["maintain the stalemate"], faded=["shading into entire new forms and adaptations"],
                 tips=[tip("흐린 부분", "콤마(,) 두 개 사이의 shading into …는 빼고 읽어도 돼요. New variations … maintain the stalemate가 뼈대예요.")]),
        ],
    },
    {
        "id": 6, "text": B1, "teaching_value": "high",
        "model_translation": "(B) 식물은 동종의 이웃 식물에게 공격이 임박한 것 같다고 알려주는 화학 화합물을 방출하여, 그 주변의 식물들이 자신의 조직에 방어용 화합물을 축적하기 시작하도록 유도할 수 있다.",
        "glosses": [g("Plants", "식물은"), g("can release", "방출할 수 있다"), g("release", "방출하다, 내보내다"),
                    g("chemical compounds", "화학 화합물"), g("chemical", "화학의"),
                    g("same-species neighbors", "같은 종의 이웃 (식물)"), g("neighbors", "이웃"),
                    g("an attack", "공격"), g("is likely coming", "올 것 같다"), g("likely", "~할 것 같은"),
                    g("those nearby plants", "그 주변 식물들"), g("nearby", "근처의, 주변의"),
                    g("building up", "쌓는, 축적하는"), g("defensive compounds", "방어용 화합물"), g("defensive", "방어용의"),
                    g("in their tissues", "자기 조직 안에")],
        "slashes": ["chemical compounds", "neighbors know", "likely coming,", "nearby plants", "defensive compounds"],
        "roles": [r("Plants", "S"), r("can release", "V"),
                  r("chemical compounds that let their same-species neighbors know that an attack is likely coming", "O")],
        "modifiers": ["that let their same-species neighbors know that an attack is likely coming"],
        "steps": [
            choice("b_tell",
                   "식물이 화학 물질을 내보내면 같은 종 이웃(same-species neighbors)은 무엇을 알게 될까요?",
                   [("o0", "곧 공격이 올 것 같다는 것", True), ("o1", "곤충이 이미 떠났다는 것", False), ("o2", "물이 부족하다는 것", False)],
                   "let … know that 뒤를 봐요. let + 대상 + know는 '~에게 알려 주다'예요.",
                   why="'that an attack is likely coming', 공격이 올 것 같다고 알려 준대요. 그래서 주변 식물도 방어용 화합물을 쌓기 시작해요.",
                   highlight=["same-species neighbors", "an attack is likely coming"],
                   tips=[tip("let + 대상 + know", "'~에게 알려 주다'예요. let their same-species neighbors know that … = 같은 종 이웃에게 …라고 알려 주다.", "let"),
                         tip("push + 대상 + to ~", "'~가 …하도록 몰아가다'예요. pushing those nearby plants to start … = 주변 식물들이 …을 시작하게 하다.", "pushing")]),
        ],
    },
    {
        "id": 7, "text": B2, "teaching_value": "high",
        "model_translation": "이러한 신호 중 일부는 심지어 곤충의 포식자를 유인하기도 하는데, 이는 식물과 곤충을 잡아먹는 협력자 모두에게 이익이 되는 지원 요청이다.",
        "glosses": [g("these cues", "이 신호들"), g("cues", "신호"), g("even", "심지어"), g("attract", "끌어들이다, 유인하다"),
                    g("insect predators", "곤충의 포식자"), g("predators", "포식자"), g("a call for an assist", "지원 요청"),
                    g("call", "요청"), g("assist", "도움, 지원"), g("benefits", "~에게 이익이 되다"),
                    g("bug-eating collaborators", "곤충을 잡아먹는 협력자"), g("collaborators", "협력자")],
        "slashes": ["Some of these cues", "insect predators,", "for an assist"],
        "roles": [r("Some of these cues", "S"), r("attract", "V"), r("insect predators", "O")],
        "modifiers": ["that benefits both the plant and its bug-eating collaborators"],
        "steps": [
            choice("b_who",
                   "these cues(이 신호들) 중 일부는 무엇을 끌어들인대요?",
                   [("o0", "더 많은 곤충", False), ("o1", "곤충을 잡아먹는 포식자", True), ("o2", "다른 종의 식물", False)],
                   "attract insect predators를 봐요. predator는 '포식자, 잡아먹는 동물'이에요.",
                   why="'attract insect predators', 곤충의 포식자를 불러들인대요. 식물과 그 포식자(bug-eating collaborators) 모두에게 이익이에요.",
                   highlight=["insect predators", "collaborators"],
                   tips=[tip("a call for ~", "'~ 요청'이에요. a call for an assist = 도와 달라는 요청. 앞 문장 전체를 바꿔 말한 것이에요.", "a call")]),
            choice("b_together",
                   "(B)에 나온 방어는 식물이 혼자 하는 걸까요, 다른 생물과 함께 하는 걸까요?",
                   [("o0", "식물 혼자 하는 방어", False), ("o1", "다른 생물과 함께 하는 방어", True)],
                   "neighbors(이웃)와 collaborators(협력자)를 봐요.",
                   why="이웃 식물에게 알리고(neighbors), 포식자를 불러(collaborators) 같이 막아요. 혼자가 아니에요.",
                   highlight=["collaborators"],
                   panel=board(L_GIVEN, R_B, fresh=("same-species neighbors", "insect predators")),
                   point="(B) 이웃에게 알리고 포식자를 부르는 방어 = 함께 하는 방어"),
        ],
    },
    {
        "id": 8, "text": C1, "teaching_value": "high",
        "model_translation": "(C) 잎의 두꺼운 왁스층과 같은 구조적 방어 기제는 일부 곤충 종이 식물 조직을 아예 손상시키지 못하게 막을 수도 있다.",
        "glosses": [g("Structural defenses", "구조적 방어 (기제)"), g("structural", "구조적인"),
                    g("like thick coats of wax on leaves", "잎의 두꺼운 왁스층 같은"), g("thick coats of wax", "두꺼운 왁스층"),
                    g("coats", "막, 층"), g("wax", "왁스, 밀랍"), g("leaves", "잎들"), g("may prevent", "막을 수도 있다"),
                    g("prevent", "막다"), g("some insect species", "일부 곤충 종"),
                    g("from damaging the plant tissues", "식물 조직을 손상시키는 것을"), g("damaging", "손상시키는"),
                    g("altogether", "아예, 완전히")],
        "slashes": ["Structural defenses", "wax on leaves", "some insect species"],
        "roles": [r("Structural defenses", "S"), r("may prevent", "V"), r("some insect species", "O")],
        "steps": [
            choice("c_before",
                   "(C)는 'Structural defenses(구조적 방어)'로 시작해요. 이렇게 종류를 밝힌 걸 보면, 앞에는 어떤 방어가 나왔을까요?",
                   [("o0", "방어를 하지 않는 식물 이야기", False), ("o1", "곤충이 식물을 공격하는 방법", False),
                    ("o2", "구조가 아닌 다른 종류의 방어", True)],
                   "Structural(구조적인)이라고 굳이 종류를 밝혔어요. 잎의 왁스층처럼 몸의 구조로 막는 방어예요.",
                   why="Structural(구조적)이라고 종류를 밝힌 건, 앞에 다른 종류의 방어가 이미 나왔기 때문이에요. 몸 구조가 아니라 화학 물질로 막는 방어 같은 것이요.",
                   highlight=["Structural defenses"],
                   tips=[tip("prevent A from ~ing", "'A가 ~하지 못하게 막다'예요. prevent some insect species from damaging … = 일부 곤충 종이 … 손상시키지 못하게 막다.", "prevent"),
                         tip("altogether", "'아예, 완전히'예요.", "altogether")],
                   panel=board(L_GIVEN + [("thick coats of wax", "두꺼운 왁스층")], R_B, fresh=("thick coats of wax",)),
                   point="(C) Structural defenses ← 앞에 구조가 아닌 다른 방어(화학 물질)"),
        ],
    },
    {
        "id": 9, "text": C2, "teaching_value": "high",
        "model_translation": "또한 개별 식물은 공격을 받는 동안 완전히 혼자인 것도 아니다.",
        "glosses": [g("Nor", "~도 아니다 · 앞 내용에 부정을 하나 더 붙여요"), g("individual plants", "개별 식물"), g("individual", "개별의"),
                    g("entirely", "완전히"), g("on their own", "혼자서, 스스로"), g("under attack", "공격을 받는"),
                    g("attack", "공격")],
        "slashes": ["individual plants", "on their own"],
        "roles": [r("are", "V"), r("individual plants", "S"), r("entirely on their own", "C")],
        "steps": [
            choice("c_next",
                   "(C)는 '식물은 공격받는 동안 완전히 혼자인 것도 아니다'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "왁스층이 두꺼워지는 과정", False), ("o1", "식물이 다른 생물과 함께 공격을 막는 방법", True),
                    ("o2", "곤충이 혼자 사는 이유", False)],
                   "not … on their own(혼자가 아니다)이라고 했어요. 그럼 누구와 함께인지가 궁금해지죠.",
                   why="혼자가 아니라고 했으니, 다음엔 누구와 어떻게 함께 막는지가 이어지기 쉬워요.",
                   highlight=["Nor", "on their own"],
                   tips=[tip("Nor + 동사 + 주어", "'~도 아니다'예요. 앞 내용에 부정을 하나 더 붙이고, 동사 are가 주어 individual plants 앞에 와요.", "Nor"),
                         tip("on one's own", "'혼자서, 스스로'예요. not on their own = 혼자가 아닌.", "on their own")],
                   point="(C) 끝 '혼자인 것도 아니다' → 다음은 함께 막는 방법"),
            order_link(
                card("given", "주어진 글", last=("Some load their tissues with harsh compounds …", "어떤 식물은 조직을 독한 화합물로 채운다")),
                [card("A", "(A)", first=("The back-and-forth is not a matter of natural balance …", "이 공방전은 자연의 균형 문제가 아니다"),
                      last=("… New variations … maintain the stalemate.", "새 변이들이 교착 상태를 유지한다")),
                 card("B", "(B)", first=("Plants can release chemical compounds that let their same-species neighbors know …", "식물은 같은 종 이웃에게 알리는 화학 물질을 내보낸다"),
                      last=("… a call for an assist that benefits both the plant and its bug-eating collaborators", "식물과 협력자 모두에게 이익이 되는 지원 요청")),
                 card("C", "(C)", first=("Structural defenses like thick coats of wax on leaves …", "잎의 두꺼운 왁스층 같은 구조적 방어"),
                      last=("Nor are individual plants entirely on their own while under attack.", "식물은 공격받는 동안 혼자인 것도 아니다"))],
                ["C", "B", "A"],
                "주어진 글(어떤 식물은 독한 화합물로 방어) → (C) 또 다른 방어인 구조적 방어, 그리고 식물은 혼자가 아니다 → (B) 이웃에게 알리고 포식자를 부르는, 함께 하는 방어 → (A) 이런 공방전은 길게 이어지는 진화의 대화, 순서예요."),
            show("c_go", "직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?", button="문제 풀러 갈게요"),
        ],
    },
]

add_match(sentences, 3, [m("The back-and-forth", "이 공방전은"), " ", m("a matter of natural balance", "자연적 균형의 문제가"), " ",
                         m("is not", "아니라"), ", 오히려 ", m("a drawn-out evolutionary conversation", "길게 이어지는 진화적 대화에"), " 가깝다."])
add_match(sentences, 9, [m("individual plants", "개별 식물은"), " ", m("while under attack", "공격을 받는 동안"), " ",
                         m("entirely on their own", "완전히 혼자인"), " 것도 ", m("Nor are", "아니다"), "."])
add_refers(sentences, 2, {"Some": "some plants(어떤 식물들)"})
add_refers(sentences, 4, {"them": "new plant defenses(식물의 새 방어)"})
add_refers(sentences, 7, {"these cues": "the chemical compounds in (B)((B) 첫 문장의 알리는 화학 물질)"})

SENSES = {
    1: [sense("as", "as diverse as", "~만큼 (as … as의 앞)", "as + 형용사 + as = ~만큼 …한"),
        sense("as", "diverse as the number", "~만큼 (as … as의 뒤)", "as + 형용사 + as = ~만큼 …한")],
    2: [sense("that", "compounds that either are", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("to", "unpleasant to insects", "~에게", "전치사 to + 명사"),
        sense("to", "the insects to go", "~하도록", "encourage + 대상 + to 동사원형")],
    3: [sense("but", "but more like", "(A가 아니라) B", "not A but B = A가 아니라 B")],
    4: [sense("for", "select for insects", "~을 (선택하다)", "select for = ~을 선택하다(살아남게 하다)"),
        sense("to", "ways to get around", "~할 (방법)", "to부정사 (앞 명사를 꾸밈)"),
        sense("which", ", which in turn help", "그리고 그것(들)은", "콤마 + which (앞 내용을 이어 설명)")],
    6: [sense("that", "compounds that let", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("that", "know that an attack", "~라는 것을", "명사절 that + 주어·동사"),
        sense("to", "plants to start", "~하도록", "push + 대상 + to 동사원형")],
    7: [sense("for", "a call for an assist", "~을 (요청)", "a call for ~ = ~ 요청"),
        sense("that", "an assist that benefits", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    9: [sense("while", "while under attack", "~하는 동안", "while + (주어·be동사 생략) 상태")],
}

WORDS = {"plants": "식물들", "plant": "식물", "evolved": "진화시킨", "defenses": "방어", "almost": "거의", "diverse": "다양한",
         "number": "수", "genera": "속(屬)", "tissues": "조직", "harsh": "독한", "compounds": "화합물", "either": "~이거나",
         "unpleasant": "불쾌한", "insects": "곤충들", "intoxicate": "취하게 하다", "encouraging": "부추기는", "bother": "괴롭히다",
         "least": "가장 적은", "slowing": "늦추는", "eating": "먹기", "matter": "문제", "natural": "자연의", "balance": "균형",
         "drawn-out": "길게 이어지는", "evolutionary": "진화적인", "conversation": "대화", "unintentionally": "의도치 않게",
         "select": "선택하다", "ways": "방법", "turn": "차례", "bring": "가져오다", "resilient": "회복 탄력성이 있는",
         "resistant": "저항력 있는", "species": "종", "variations": "변이", "shading": "점차 변하는", "entire": "완전한",
         "forms": "형태", "adaptations": "적응", "maintain": "유지하다", "stalemate": "교착 상태", "release": "방출하다",
         "chemical": "화학의", "same-species": "같은 종의", "neighbors": "이웃", "attack": "공격", "likely": "~할 것 같은",
         "coming": "오는", "nearby": "주변의", "building": "쌓는", "defensive": "방어용의", "cues": "신호",
         "attract": "끌어들이다", "insect": "곤충", "predators": "포식자", "call": "요청", "assist": "도움, 지원",
         "benefits": "이익이 되다", "bug-eating": "곤충을 먹는", "collaborators": "협력자", "structural": "구조적인",
         "thick": "두꺼운", "coats": "막, 층", "wax": "왁스", "leaves": "잎들", "prevent": "막다", "damaging": "손상시키는",
         "tissue": "조직", "altogether": "아예", "individual": "개별의", "entirely": "완전히", "load": "채우다",
         "even": "심지어", "variation": "변이", "new": "새로운", "around": "돌아서, 피해서", "help": "돕다"}

OPTIONS = [("1", "(A)-(C)-(B)", False), ("2", "(B)-(A)-(C)", False), ("3", "(B)-(C)-(A)", False), ("4", "(C)-(A)-(B)", False), ("5", "(C)-(B)-(A)", True)]
exam = {
    "question": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?",
    "sentence": 1, "analysis_first": True, "wrong_rate": 57.0, "wrong_rank": 8,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], **({"correct": True} if o[2] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "단락 첫머리와 끝의 단서(Structural, Nor … on their own, The back-and-forth)를 떠올리며 순서를 골라 봐요.",
        "정답이에요! 독한 화합물 방어 → (C) 또 다른 구조적 방어, 그리고 식물은 혼자가 아니다 → (B) 이웃·포식자와 함께 하는 방어 → (A) 이 공방전은 길게 이어지는 진화의 대화, 순서예요.",
        "정답은 ⑤ (C)-(B)-(A)예요.",
        {"1": "(A)의 The back-and-forth(그 공방전)는 여러 방어가 다 나온 뒤에 묶어 말하는 말이에요. 주어진 글 바로 뒤에 오기엔 일러요.",
         "2": "(B)의 함께 하는 방어는 (C) 끝 '혼자인 것도 아니다' 뒤에 와야 자연스러워요. (A)는 공방을 묶는 말이라 맨 뒤예요.",
         "3": "많이 고른 오답이에요. (B)의 chemical compounds는 주어진 글의 화합물과 비슷해 보이지만, 이웃과 함께 막는 방어예요. (C) 끝 '혼자인 것도 아니다'가 먼저 와야 해요.",
         "4": "(A)는 공방을 묶어 말하는 단락이라 (C)와 (B)의 방어가 다 나온 뒤에 와요."},
        {"3": review(26,
                     "주어진 글의 harsh compounds(독한 화합물)와 (B)의 chemical compounds(화학 화합물)가 같은 말 같아서 바로 이었을 거예요. 하지만 (B)는 곤충을 쫓는 방어가 아니라, 이웃에게 알리고 포식자를 부르는 '함께 하는' 방어예요. 그래서 (C) 끝 'Nor are individual plants entirely on their own(혼자인 것도 아니다)'이 먼저 나와야 (B)로 이어져요.",
                     panel=rows(("주어진 글 끝", "Some load their tissues with harsh compounds", "혼자 하는 방어 ①", "hl"),
                                ("(C)", "Structural defenses … Nor are individual plants entirely on their own", "혼자 하는 방어 ② → 혼자가 아니다", "hl2"),
                                ("(B)", "release chemical compounds … attract insect predators", "함께 하는 방어", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 36번 (글의 순서, 2점)",
    topic="순서 푸는 법: 주어진 글의 끝 → 단락 첫머리 단서로 앞 내용 예측 → 단락 끝으로 다음 내용 예측 → 순서 잇기",
    method={"type": "order", "labels": ["단락 요지 잡기", "연결 단서 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-plant-defenses.svg", ("Plants", "식물"), "vs", ("Insects", "곤충"),
                                       "움직이지 못하는 식물은 곤충을 어떻게 막을까?", "2026년 6월 모의평가 36번 도입 칠판"),
                      "alt": "칠판: Plants(식물) vs Insects(곤충)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "식물은 도망칠 수 없는데, 곤충이 잎을 먹으러 오면 어떻게 할까요? 이번 글은 식물의 방어(defenses) 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "순서 문제는 단락 첫머리의 단서가 앞 내용과 이어지는지 보는 거예요. Structural, Nor, The 같은 말이 무엇을 받는지 찾아볼게요."}}],
    exam=exam,
    key_words={"passage": [g("defense", "방어 (기제)"), g("diverse", "다양한"), g("load", "채우다"), g("harsh", "독한"),
                           g("compound", "화합물"), g("intoxicate", "취하게 하다"), g("back-and-forth", "공방전"),
                           g("drawn-out", "길게 이어지는"), g("evolutionary", "진화적인"), g("unintentionally", "의도치 않게"),
                           g("select for", "~을 선택하다"), g("get around", "우회하다"), g("in turn", "결국"),
                           g("resistant", "저항력 있는"), g("variation", "변이"), g("adaptation", "적응"), g("maintain", "유지하다"),
                           g("release", "방출하다"), g("build up", "축적하다"), g("predator", "포식자"), g("cue", "신호"),
                           g("collaborator", "협력자"), g("structural", "구조적인"), g("altogether", "아예, 완전히"),
                           g("individual", "개별의"), g("on one's own", "혼자서")],
               "options": []},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="순서 푸는 법")
