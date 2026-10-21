"""2026년 9월 모의평가(2027학년도, 평가원) 30번 레슨 + 대사를 만든다 (문맥상 낱말의 쓰임, 3점). 오답률 38% · Top 7 (메가스터디).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_30.py   (→ npm run policy:copy stamp <id> → npm run build)

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- 두 그룹 이름: 왼쪽 「on its own 쪽 (스스로)」 ↔ 오른쪽 「you planted 쪽 (내가 손댐)」 — 둘 다 3문장에 나온 말이라 칠판은 3문장에서 처음 연다.
  ②altering을 그룹 이름에 쓰지 않았다(맞는 밑줄인지 학생이 판단해야 해서)
  끌어 넣기: wave after wave of pests → 오른쪽(4문장), balance out → 왼쪽(6문장), Immediately attempting to remove → 오른쪽 ·
  grow better on its own → 왼쪽(7문장). balance out을 「스스로」 쪽으로 둔 것이 어색하면 알려 주세요
- 정답 ⑤ shorten(→ prolong): 7문장에서는 그룹과 further(심화시키다)만 묻고 맞다/틀리다는 말하지 않는다
- ①~④는 「그럼 보기 ○는 문맥에 맞을까요, 틀릴까요?」로 학생이 고른다(README §0-1). 정답이 아닌 밑줄 화면엔 칠판을 띄우지 않았다
- 많이 고른 오답이 고르게 퍼져 있어(③ 13 · ④ 12 · ② 11) 셋 다 review를 달았다
- 헷갈리는 단어(trap): check(in check = 억제), couple(a couple of = 두어 개), wave(파도처럼 잇달아 밀려옴), further(동사 심화시키다)
  — 해설 번역(억제하는·첫 몇 년·파도처럼 밀려와·심화시키고)과 대조함
- keep ~ in check = 억제하다, overtake = 장악하다·뒤덮다, cultivate = 조성하다, balance out = 균형을 이루다, imbalance = 불균형,
  When it comes to = ~에 관해 말하자면 — 해설 Words and Phrases·번역과 대조함
- repel·pollinator는 시험지 아래 * 풀이 단어 — 핵심어(key_words)에서 뺐다
- 3문장 it’s important to remember(가주어)는 끊어읽기 S·V 표시를 붙이지 않았다(it이 앞 When it comes to에도 나옴, 가주어 논란 메모)
- 평가 뒤집기(+/−)는 넣지 않았다 — 해충(pests)을 좋게 보는 게 아니라 '성가신(annoying)' 것도 균형 안에 두자는 글이라 평가가 뒤집히지 않는다고 봄
- 해석 맞추기(add_match)는 5문장(This is normal.) 하나만. S·V 찾기 스텝은 만들지 않았다(2026-10-20 삭제), 끊어읽기 roles·slashes·modifiers만
반영한 규칙: README §0-1(2026-10-20~21), vocab.md v1, 칠판은 읽은 데까지만·화면마다 X, 대사 핵심만, 칭찬 분리(엔진), 화면 중계 말 없음.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, sc, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)
from beginner import add_match, add_refers, m  # noqa: E402

ID = "mopyeong-2027-09-30-garden-pests"

S = [
    "There is good news about pests and medicinal herbs: Most herbs either repel pests or attract beneficial insects that help keep "
    "pest populations in check.",
    "So the more herbs you grow, the more you will attract pollinators and “good” bugs that like to eat the more ①destructive pests, "
    "which will lead to a more successful garden!",
    "When it comes to managing pests in the garden, it’s important to remember that you are ②altering the ecosystem of an area that "
    "existed on its own before you planted anything into it.",
    "So the first couple years in a new garden can feel like wave after wave of pests are ③overtaking your plants.",
    "This is normal.",
    "The goal of a long-term healthy garden is to work with the environment you are trying to cultivate to ④allow the plants, "
    "pollinators, and even the annoying pests to balance out.",
    "Immediately attempting to remove a new pest entirely from your garden will only further these initial imbalances and "
    "⑤shorten the process of helping your garden grow better on its own.",
]
# 해설지 번역 (7문장의 shorten은 해설대로 「단축시킬(→ 연장시킬)」)
KO = [
    "해충과 약초에 관한 좋은 소식이 있는데, 대부분의 허브가 해충을 쫓아버리거나, 해충 개체 수를 억제하는 데 도움을 주는 익충을 유인한다는 것이다.",
    "따라서 허브를 더 많이 키울수록 여러분은 꽃가루 매개자와 더 파괴적인 해충을 잡아먹길 좋아하는 '유익한' 곤충을 더 많이 유인하게 되며, 이는 더 성공적인 정원으로 이어질 것이다!",
    "정원의 해충을 관리하는 것에 관해 말하자면, 여러분이 거기에 어떤 것을 심기 전부터 그 자리에 자체적으로 존재했던 생태계를 변화시키고 있다는 점을 기억하는 것이 중요하다.",
    "그래서 새로운 정원에서의 첫 몇 년은 해충들이 파도처럼 밀려와 여러분의 식물을 장악하고 있는 듯한 느낌이 들 수 있다.",
    "이는 정상적이다.",
    "장기적으로 건강한 정원을 위한 목표는, 여러분이 조성하려는 환경과 조화를 이루어 식물, 꽃가루 매개자, 심지어 성가신 해충들까지 균형을 이룰 수 있도록 하는 것이다.",
    "여러분의 정원에 새로 나타난 해충을 즉시 완전히 제거하려고 시도하는 것은 초기 불균형을 심화시키고, 여러분의 정원이 스스로 더 잘 자라도록 돕는 과정을 단축시킬(→ 연장시킬) 뿐일 것이다.",
]
UNDER = ["①destructive", "②altering", "③overtaking", "④allow", "⑤shorten"]

# 두 그룹 — 이름은 3문장에서 나온 말로만 (칠판엔 읽은 데까지만, 밑줄 낱말은 이름에 쓰지 않는다)
LEFT = "on its own 쪽 (스스로)"
RIGHT = "you planted 쪽 (내가 손댐)"
SORT_LEFT = "왼쪽 · on its own (스스로)"
SORT_RIGHT = "오른쪽 · you planted (내가 손댐)"


def board(left, right, fresh=(), sort=None):
    """단어 지도. sort = 학생이 끌어 넣을 말 — 맞는 쪽에 fresh로 넣어 두면 답하기 전엔 숨고 맞히면 붙는다"""
    return groups("정원의 생태계", LEFT, left, RIGHT, right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": SORT_LEFT, "right": SORT_RIGHT} if sort else None)


def ok_or_not(id, under, hint, why, point, **extra):
    """정답이 아닌 밑줄 — 알려 주지 않고 학생이 「맞을까요, 틀릴까요?」로 고른다 (README §0-1)"""
    return choice(id, f"그럼 보기 {under}는 문맥에 맞을까요, 틀릴까요?",
                  [("o0", "문맥에 맞아요", True), ("o1", "문맥에 안 맞아요", False)],
                  hint, why=why, point=point, **extra)


L3 = [("existed on its own", "스스로 있던 생태계")]
R3 = [("you planted anything", "내가 무언가를 심음")]
R4 = R3 + [("wave after wave of pests", "잇달아 밀려오는 해충")]
L6 = L3 + [("balance out", "균형을 이루다")]
R7 = R4 + [("Immediately attempting to remove", "즉시 없애려는 시도")]
L7 = L6 + [("grow better on its own", "스스로 더 잘 자람")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("There is good news", "좋은 소식이 있다"), g("good news", "좋은 소식"), g("news", "소식"),
                    g("about pests and medicinal herbs", "해충과 약초에 관한"), g("pests", "해충"), g("medicinal", "약용의"),
                    g("herbs", "허브, 약초"), g("Most herbs", "대부분의 허브"), g("either", "~이거나"),
                    g("repel", "쫓아버리다 (*풀이 단어)"), g("attract", "끌어들이다, 유인하다"), g("beneficial insects", "익충, 이로운 곤충"),
                    g("beneficial", "이로운"), g("insects", "곤충"), g("help keep", "유지하도록 돕다"),
                    g("pest populations", "해충 개체 수"), g("pest", "해충"), g("populations", "개체 수"),
                    g("in check", "억제된 · keep ~ in check = ~을 억제하다"), g("check", "확인 · 여기서는 in check = 억제된")],
        "slashes": ["good news", "medicinal herbs:", "repel pests", "beneficial insects"],
        "roles": [r("is", "V"), r("good news", "S"), r("Most herbs", "S"), r("repel", "V"), r("attract", "V"),
                  r("beneficial insects", "O")],
        "modifiers": ["that help keep pest populations in check"],
        "emphasis": ["good news", "beneficial insects", "in check"],
        "steps": [
            choice("s1_good",
                   "허브가 정원에 좋은 소식(good news)인 까닭은 무엇일까요?",
                   [("o0", "해충을 쫓거나, 해충을 줄여 주는 곤충을 부른다", True), ("o1", "해충을 먹이로 끌어모은다", False),
                    ("o2", "모든 곤충이 오지 못하게 막는다", False)],
                   "콜론(:) 뒤가 좋은 소식의 내용이에요. either A or B는 'A하거나 B하다'예요.",
                   why="'either repel pests or attract beneficial insects', 해충을 쫓거나 이로운 곤충을 부른대요. 그 곤충이 해충 수를 억제(keep in check)해요.",
                   highlight=["repel", "beneficial insects", "in check"],
                   tips=[tip("either A or B", "'A하거나 B하다'예요.", "either"),
                         tip("keep ~ in check", "'~을 억제하다'예요. 해충 수가 늘지 않게 막는다는 말이에요.", "in check"),
                         tip("check", "이 글에서는 → in check = 억제된  ('확인' 아님)", "check", trap=True)],
                   point="허브 = 해충을 쫓거나(repel), 해충을 억제하는 익충을 부른다"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "medium",
        "glosses": [g("the more herbs you grow", "허브를 더 많이 키울수록"), g("grow", "키우다, 자라다"),
                    g("the more you will attract", "더 많이 유인하게 된다"), g("attract", "유인하다"),
                    g("pollinators", "꽃가루 매개자 (*풀이 단어)"), g("“good” bugs", "'유익한' 곤충"), g("bugs", "벌레, 곤충"),
                    g("like to eat", "먹기를 좋아하다"), g("eat", "먹다"), g("destructive", "파괴적인"), g("pests", "해충"),
                    g("will lead to", "~으로 이어질 것이다"), g("lead", "이끌다"), g("a more successful garden", "더 성공적인 정원"),
                    g("successful", "성공적인"), g("garden", "정원")],
        "slashes": ["you grow,", "will attract", "“good” bugs", "to eat", "①destructive pests,"],
        "roles": [r("you … you", "S"), r("grow", "V"), r("will attract", "V"), r("pollinators and “good” bugs", "O")],
        "modifiers": ["that like to eat the more ①destructive pests", "which will lead to a more successful garden"],
        "steps": [
            ok_or_not("s2_check", "①destructive",
                      "“good” bugs(유익한 곤충)가 잡아먹는 해충이에요. 그 해충이 정원에 어떤 해충일지 봐요.",
                      "유익한 곤충이 잡아먹는 건 정원을 망치는, 더 파괴적인(destructive) 해충이에요. 그래서 정원이 더 성공적이 돼요.",
                      "① destructive: 유익한 곤충이 잡아먹는 해충 = 정원을 망치는 해충",
                      highlight=["“good” bugs", "destructive"],
                      tips=[tip("the more A, the more B", "'A할수록 더 B하다'예요. 허브를 많이 키울수록 유익한 곤충이 더 많이 온대요.", "the more herbs")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("When it comes to", "~에 관해 말하자면"), g("comes", "오다"), g("managing pests", "해충을 관리하는 것"),
                    g("managing", "관리하는 것"), g("in the garden", "정원의"), g("garden", "정원"), g("it’s important", "~이 중요하다"),
                    g("important", "중요한"), g("to remember", "기억하는 것"), g("remember", "기억하다"), g("altering", "변화시키는"),
                    g("the ecosystem of an area", "어떤 지역의 생태계"), g("ecosystem", "생태계"), g("area", "지역, 자리"),
                    g("existed on its own", "스스로(자체적으로) 존재했던"), g("existed", "존재했다"), g("on its own", "스스로, 자체적으로"),
                    g("you planted anything", "여러분이 무언가를 심었다"), g("planted", "심었다"), g("anything", "무언가")],
        "slashes": ["managing pests", "in the garden,", "to remember", "②altering", "of an area", "on its own"],
        "roles": [r("it", "S"), r("comes", "V"), r("you", "S"), r("are ②altering", "V"),
                  r("the ecosystem of an area that existed on its own before you planted anything into it", "O")],
        "modifiers": ["that existed on its own before you planted anything into it"],
        "emphasis": ["on its own", "you planted anything"],
        "steps": [
            choice("s3_before",
                   "that existed on its own before you planted anything은 어떤 생태계일까요?",
                   [("o0", "내가 무언가를 심기 전부터 스스로 있던 생태계", True), ("o1", "내가 처음부터 새로 만든 생태계", False),
                    ("o2", "해충이 없어서 텅 빈 생태계", False)],
                   "on its own은 '스스로, 자체적으로'예요. before you planted anything을 같이 봐요.",
                   why="'existed on its own before you planted anything', 여러분이 무엇을 심기 전부터 그 자리에 스스로 있던 생태계래요.",
                   highlight=["on its own", "you planted anything"],
                   tips=[tip("When it comes to ~", "'~에 관해 말하자면'이에요.", "When it comes to"),
                         tip("on its own", "'스스로, 자체적으로'예요. 사람이 손대지 않아도 있던 것이에요.", "on its own")],
                   point="원래 생태계 = 내가 심기 전부터 스스로(on its own) 있던 것"),
            show("s3_board", "두 그룹으로 나눠 봐요.\n원래 스스로 있던 생태계(on its own)와, 거기에 무언가를 심는 나(you planted)예요.",
                 button="다음", panel=board(L3, R3, fresh=("existed on its own", "you planted anything"))),
            ok_or_not("s3_check", "②altering",
                      "원래 스스로 있던 생태계에 내가 무언가를 심어요. 그러면 그 생태계가 그대로일지 봐요.",
                      "스스로 있던 생태계에 무언가를 심으면 그 생태계는 바뀌어요. 그래서 altering(변화시키다)은 맞는 낱말이에요.",
                      "② altering: 스스로 있던 생태계 + 내가 심음 → 생태계가 바뀜",
                      highlight=["altering"]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("the first couple years", "첫 몇 년"), g("first", "첫"), g("couple", "커플 · 여기서는 '두어 개, 몇'"),
                    g("years", "해, 년"), g("in a new garden", "새 정원에서"), g("can feel like", "~인 것처럼 느껴질 수 있다"),
                    g("feel", "느끼다"), g("wave after wave of pests", "파도처럼 잇달아 밀려오는 해충"),
                    g("wave", "흔들다 · 여기서는 '파도'"), g("overtaking", "장악하는, 뒤덮는"), g("your plants", "여러분의 식물"),
                    g("plants", "식물")],
        "slashes": ["in a new garden", "can feel like", "of pests"],
        "roles": [r("the first couple years in a new garden", "S"), r("can feel", "V"), r("wave after wave of pests", "S"),
                  r("are ③overtaking", "V"), r("your plants", "O")],
        "emphasis": ["wave after wave of pests"],
        "steps": [
            choice("s4_sort",
                   "So로 이어져요. wave after wave of pests(잇달아 밀려오는 해충)는 칠판 어느 쪽에서 생긴 일일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "So는 앞 문장의 결과예요. 3문장에서 무엇을 했기 때문인지 봐요.",
                   why="내가 무언가를 심어 원래 생태계를 건드렸기 때문에(So) 생긴 일이에요. 오른쪽이에요.",
                   highlight=["So", "wave after wave of pests"],
                   panel=board(L3, R4, fresh=("wave after wave of pests",), sort=["wave after wave of pests"]),
                   tips=[tip("wave", "이 글에서는 → 파도 (wave after wave = 파도처럼 잇달아)  ('손을 흔들다' 아님)", "wave", trap=True),
                         tip("couple", "이 글에서는 → the first couple years = 첫 몇 년  ('커플' 아님)", "couple", trap=True)],
                   point="wave after wave of pests ← 내가 심어서 생태계를 건드린 결과(So)"),
            ok_or_not("s4_check", "③overtaking",
                      "해충이 파도처럼 잇달아 밀려와요. 그 해충이 내 식물을 어떻게 하는 것처럼 느껴질지 봐요.",
                      "해충이 파도처럼 밀려오면 식물을 뒤덮는(overtaking) 것처럼 느껴져요. 다음 문장 This is normal과도 이어져서 맞는 낱말이에요.",
                      "③ overtaking: 해충이 잇달아 밀려옴 → 식물을 뒤덮는 것 같다 (그래도 정상)",
                      highlight=["overtaking"]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("This", "이것 · 4문장, 해충이 밀려오는 일"), g("normal", "정상적인")],
        "roles": [r("This", "S"), r("is", "V"), r("normal", "C")],
        "steps": [],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("The goal", "목표"), g("goal", "목표"), g("of a long-term healthy garden", "장기적으로 건강한 정원의"),
                    g("long-term", "장기적인"), g("healthy", "건강한"), g("garden", "정원"),
                    g("work with the environment", "환경과 함께 해 나가다"), g("environment", "환경"),
                    g("you are trying to cultivate", "여러분이 조성하려는"), g("trying", "애쓰는"), g("cultivate", "조성하다, 경작하다"),
                    g("allow", "허용하다, ~하게 두다"), g("the plants", "식물"), g("plants", "식물"), g("pollinators", "꽃가루 매개자 (*풀이 단어)"),
                    g("even the annoying pests", "심지어 성가신 해충까지"), g("annoying", "성가신"), g("pests", "해충"),
                    g("balance out", "균형을 이루다"), g("balance", "균형을 이루다")],
        "slashes": ["healthy garden", "with the environment", "to cultivate", "pollinators,", "annoying pests"],
        "roles": [r("The goal of a long-term healthy garden", "S"), r("is", "V"),
                  r("to work with the environment you are trying to cultivate to ④allow the plants, pollinators, and even the annoying pests to balance out", "C")],
        "modifiers": ["you are trying to cultivate"],
        "emphasis": ["work with the environment", "balance out"],
        "steps": [
            choice("s6_with",
                   "work with the environment는 무슨 뜻일까요?",
                   [("o0", "환경과 함께 맞춰 간다", True), ("o1", "환경과 맞서 싸운다", False), ("o2", "환경을 새로 바꿔 버린다", False)],
                   "with는 '~와 함께'예요. 싸운다면 against를 써요.",
                   why="'work with the environment', 환경과 함께, 환경에 맞춰 일한다는 말이에요.",
                   highlight=["work with the environment"],
                   tips=[tip("cultivate", "'(땅을) 경작하다, (환경을) 조성하다'예요. 여기서는 내가 가꾸려는 정원 환경이에요.", "cultivate"),
                         tip("allow A to B", "'A가 B하도록 두다, 허용하다'예요.", "allow")],
                   point="목표 = 환경과 함께(work with) — 맞서 싸우지 않는다"),
            choice("s6_sort",
                   "balance out(균형을 이루다)은 칠판 어느 쪽 말일까요?",
                   [("o0", SORT_LEFT, True), ("o1", SORT_RIGHT, False)],
                   "식물, 꽃가루 매개자, 해충까지 모두 균형을 이뤄요. 내가 하나하나 손대는 건지 봐요.",
                   why="균형은 식물과 곤충이 스스로 맞춰 가는 거예요. 원래 스스로 있던 생태계 쪽이에요.",
                   highlight=["balance out"],
                   panel=board(L6, R4, fresh=("balance out",), sort=["balance out"]),
                   point="balance out → on its own(스스로) 쪽"),
            ok_or_not("s6_check", "④allow",
                      "목표는 balance out(균형을 이루다)이에요. 식물, 꽃가루 매개자, 심지어 해충(even the annoying pests)까지 어떻게 해야 균형이 될지 봐요.",
                      "해충까지 다 없애지 않고 함께 균형을 이루도록 두는(allow) 게 목표예요. 그래서 맞는 낱말이에요.",
                      "④ allow: 식물·곤충·해충까지 균형을 이루도록 둔다",
                      highlight=["allow", "even"]),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("Immediately attempting to remove", "즉시 없애려고 시도하는 것"), g("immediately", "즉시"),
                    g("attempting", "시도하는 것"), g("remove", "없애다, 제거하다"), g("a new pest entirely", "새 해충을 완전히"),
                    g("pest", "해충"), g("entirely", "완전히"), g("from your garden", "여러분의 정원에서"), g("garden", "정원"),
                    g("will only further", "심화시킬 뿐이다"), g("further", "더 먼 · 여기서는 동사 '심화시키다'"),
                    g("these initial imbalances", "이 초기 불균형"), g("initial", "초기의"), g("imbalances", "불균형"),
                    g("shorten", "단축시키다, 줄이다"), g("the process", "과정"), g("process", "과정"),
                    g("of helping your garden", "정원을 돕는"), g("helping", "돕는 것"),
                    g("grow better on its own", "스스로 더 잘 자라다"), g("grow", "자라다"), g("better", "더 잘"),
                    g("on its own", "스스로")],
        "slashes": ["a new pest entirely", "from your garden", "initial imbalances", "the process"],
        "roles": [r("Immediately attempting to remove a new pest entirely from your garden", "S"), r("will only further", "V"),
                  r("these initial imbalances", "O"), r("⑤shorten", "V"),
                  r("the process of helping your garden grow better on its own", "O")],
        "emphasis": ["Immediately attempting to remove", "further"],
        "steps": [
            # 정답 문장 — 그룹과 further만 묻고 ⑤가 맞는지 틀린지는 말하지 않는다. 마지막 문제에서 학생이 고른다
            choice("s7_sort",
                   "Immediately attempting to remove(즉시 없애려는 시도)는 칠판 어느 쪽 말일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "새 해충을 즉시, 완전히(entirely) 없애려는 건 누가 하는 일인지 봐요.",
                   why="해충을 바로 없애려는 건 내가 정원에 손대는 일이에요. 오른쪽이에요.",
                   highlight=["Immediately attempting to remove"],
                   panel=board(L6, R7, fresh=("Immediately attempting to remove",), sort=["Immediately attempting to remove"]),
                   point="Immediately attempting to remove → you planted(내가 손댐) 쪽"),
            choice("s7_further",
                   "그렇게 하면 these initial imbalances(이 초기 불균형)는 어떻게 된대요?",
                   [("o0", "더 심해진다", True), ("o1", "사라진다", False), ("o2", "그대로다", False)],
                   "will only further를 봐요. 여기서 further는 동사예요.",
                   why="'will only further these initial imbalances', further는 동사로 '심화시키다'예요. 불균형을 더 키울 뿐이래요.",
                   highlight=["further", "imbalances"],
                   tips=[tip("further", "이 글에서는 → 동사 '심화시키다, 더 키우다'  ('더 먼' 아님)", "further", trap=True)],
                   point="해충을 즉시 없애려 함 → 초기 불균형을 더 키울 뿐(further)"),
            choice("s7_sort2",
                   "helping your garden grow better on its own(정원이 스스로 더 잘 자라게 돕기)은 칠판 어느 쪽 말일까요?",
                   [("o0", SORT_LEFT, True), ("o1", SORT_RIGHT, False)],
                   "on its own은 '스스로'예요.",
                   why="정원이 스스로(on its own) 자라는 거예요. 왼쪽이에요.",
                   highlight=["grow better on its own"],
                   panel=board(L7, R7, fresh=("grow better on its own",), sort=["grow better on its own"]),
                   point="grow better on its own → on its own(스스로) 쪽"),
            show("s7_go", "밑줄 다섯 개가 칠판의 흐름과 맞는지 떠올리며 문제를 풀어 봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

add_match(sentences, 5, [m("This", "이것은"), " ", m("is normal", "정상이다"), "."])
add_refers(sentences, 5, {"This": "This = 4문장, 해충이 잇달아 밀려오는 일"})

SENSES = {
    1: [sense("that", "insects that help keep", "(앞 명사를 꾸밈)", "관계대명사 that + 동사 — 앞의 beneficial insects를 꾸밈")],
    2: [sense("so", "So the more herbs", "그래서", "앞 문장의 결과를 잇는 So"),
        sense("that", "bugs that like to eat", "(앞 명사를 꾸밈)", "관계대명사 that + 동사 — 앞의 pollinators and “good” bugs를 꾸밈"),
        sense("to", "like to eat", "~하기를", "like to + 동사원형 = ~하기를 좋아하다"),
        sense("which", "pests, which will lead", "(그런데) 그것은", "콤마 + which — 앞 내용 전체를 덧붙여 설명"),
        sense("to", "lead to a more successful garden", "~으로", "lead to ~ = ~으로 이어지다")],
    3: [sense("to", "When it comes to managing", "~에 관해", "When it comes to ~ = ~에 관해 말하자면 (to 뒤에 -ing)"),
        sense("to", "important to remember", "~하는 것", "it ~ to부정사 — 기억하는 것이 중요하다"),
        sense("that", "remember that you are", "~라는 것", "명사절 that (remember that … = ~라는 것을 기억하다)"),
        sense("that", "an area that existed", "(앞 명사를 꾸밈)", "관계대명사 that + 동사 — 앞의 an area를 꾸밈")],
    4: [sense("so", "So the first couple years", "그래서", "앞 문장의 결과를 잇는 So")],
    6: [sense("to", "is to work", "~하는 것", "be동사 + to부정사 = ~하는 것이다 (목표는 ~하는 것)"),
        sense("to", "trying to cultivate", "~하려고", "try to + 동사원형 = ~하려고 애쓰다"),
        sense("to", "to ④allow", "~하도록", "to부정사 — ~하도록 (목적)"),
        sense("to", "pests to balance out", "~하도록 (두다)", "allow A to B = A가 B하도록 두다")],
    7: [sense("to", "attempting to remove", "~하려고", "attempt to + 동사원형 = ~하려고 시도하다")],
}

WORDS = {
    "good": "좋은", "news": "소식", "pests": "해충", "pest": "해충", "medicinal": "약용의", "herbs": "허브", "repel": "쫓아버리다",
    "attract": "유인하다", "beneficial": "이로운", "insects": "곤충", "help": "돕다", "keep": "유지하다", "populations": "개체 수",
    "check": "억제 · in check", "grow": "키우다, 자라다", "pollinators": "꽃가루 매개자", "bugs": "곤충", "eat": "먹다",
    "destructive": "파괴적인", "lead": "이끌다", "successful": "성공적인", "garden": "정원", "comes": "오다", "managing": "관리하는 것",
    "important": "중요한", "remember": "기억하다", "altering": "변화시키는", "ecosystem": "생태계", "area": "지역", "existed": "존재했다",
    "planted": "심었다", "anything": "무언가", "couple": "두어 개", "years": "년", "feel": "느끼다", "wave": "파도",
    "overtaking": "장악하는", "plants": "식물", "normal": "정상적인", "goal": "목표", "long-term": "장기적인", "healthy": "건강한",
    "work": "일하다", "environment": "환경", "trying": "애쓰는", "cultivate": "조성하다", "allow": "허용하다", "annoying": "성가신",
    "balance": "균형을 이루다", "immediately": "즉시", "attempting": "시도하는 것", "remove": "없애다", "entirely": "완전히",
    "further": "심화시키다", "initial": "초기의", "imbalances": "불균형", "shorten": "단축시키다", "process": "과정",
    "helping": "돕는 것", "better": "더 잘", "it’s": "그것은 ~이다", "its": "그것의 · on its own = 스스로", "own": "자신의",
    "new": "새로운", "first": "첫", "will": "~할 것이다", "can": "~할 수 있다", "only": "~할 뿐", "most": "대부분의",
}

# 칠판 정리 — 2~3문장마다, 밑줄이 맞는지 틀린지 없이 내용만
STORIES = [
    (2, [sc("문장 1~2", "🌿", "herbs · beneficial insects · in check", "허브는 해충을 쫓거나, 해충을 억제하는 이로운 곤충을 불러요")]),
    (5, [sc("문장 3~5", "🐛", "you planted · wave after wave of pests · normal",
            "내가 무언가를 심으면 처음 몇 년은 해충이 잇달아 밀려와요 — 그건 정상이에요")]),
]

exam = {
    "question": "다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은? [3점]",
    "underline": UNDER, "sentence": 1, "analysis_first": True, "wrong_rate": 38.0, "wrong_rank": 7,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("destructive", "파괴적인"), g("altering", "변화시키는"), g("overtaking", "장악하는"), g("allow", "허용하다"),
                g("shorten", "단축시키다")],
    "options": [
        {"id": "1", "label": "destructive", "keywords": ["destructive"], "ko": "파괴적인"},
        {"id": "2", "label": "altering", "keywords": ["altering"], "ko": "변화시키는"},
        {"id": "3", "label": "overtaking", "keywords": ["overtaking"], "ko": "장악하는"},
        {"id": "4", "label": "allow", "keywords": ["allow"], "ko": "허용하다"},
        {"id": "5", "label": "shorten", "keywords": ["shorten"], "ko": "단축시키다", "correct": True},
    ],
    "brief": exam_brief(
        "밑줄 단어마다 칠판의 어느 쪽 흐름인지 떠올려 봐요. 흐름과 안 맞는 것 하나를 골라요.",
        "정답이에요! 해충을 바로 다 없애려 하면 불균형만 커져요. 그러면 정원이 스스로 균형을 찾는 과정은 짧아지는(shorten) 게 아니라 길어져요(prolong).",
        "정답은 ⑤예요. 해충을 바로 없애려 하면 불균형이 커지니, 정원이 스스로 자라는 과정은 짧아지는 게 아니라 길어져요(prolong).",
        {"1": "유익한 곤충이 잡아먹는 건 정원을 망치는 해충이라 destructive(파괴적인)가 맞아요.",
         "2": "스스로 있던 생태계에 무언가를 심으면 생태계가 바뀌니 altering(변화시키는)이 맞아요.",
         "3": "생태계를 건드린 뒤라 해충이 밀려와 식물을 뒤덮는 것 같대요. 다음 문장이 그게 정상이래요.",
         "4": "해충까지 다 없애지 않고 함께 균형을 이루도록 두는(allow) 게 목표라 맞아요."},
        {"3": review(13,
                     "overtaking(장악하는)이 1문장의 '허브가 해충을 쫓는다'와 안 맞아 보여서 골라요. "
                     "하지만 4문장은 So로 이어져요. 내가 생태계를 바꿨으니 처음엔 해충이 식물을 뒤덮는 것 같고, 5문장이 그게 정상이래요.",
                     panel=rows(("3문장", "you are altering the ecosystem", "내가 생태계를 바꿈", "hl"),
                                ("4문장", "So … wave after wave of pests are overtaking", "그래서 해충이 밀려와 식물을 뒤덮는 것 같음", "hl"),
                                ("5문장", "This is normal.", "그건 정상", "hl")),
                     rank_word="가장 많이 고른"),
         "4": review(12,
                     "allow(허용하다)가 '성가신 해충까지 허용한다'로 읽혀서 이상해 보여요. "
                     "하지만 목표는 balance out, 해충까지 함께 균형을 이루게 하는 거예요. 해충을 다 없애는 게 아니에요.",
                     panel=rows(("6문장", "allow … even the annoying pests to balance out", "해충까지 균형을 이루도록 둠", "hl"),
                                ("7문장", "Immediately attempting to remove … will only further these initial imbalances", "바로 없애면 불균형만 커짐", "hl"))),
         "2": review(11,
                     "altering(변화시키는)이 '원래 스스로 있던(on its own)'과 안 맞아 보여서 골라요. "
                     "하지만 스스로 있던 생태계에 내가 무언가를 심으면 그 생태계는 바뀌어요. 그래서 4문장에서 해충이 밀려와요.")}),
}

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 30번 (문맥상 낱말의 쓰임, 3점)",
    topic="어휘 문제 푸는 법: 요지 → 두 그룹(on its own ↔ you planted) → 밑줄 단어가 흐름에 맞는지",
    method={"type": "word_in_context", "labels": ["요지 잡기", "두 그룹으로 나누기", "밑줄 단어 맞춰 보기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-garden-pests.svg", ("Pests", "해충"), "?", ("Garden", "정원"),
                                       "정원의 해충, 어떻게 다룰까?", "2026년 9월 모의평가 30번 도입 칠판"),
                      "alt": "칠판: Pests(해충) ? Garden(정원) — 정원의 해충, 어떻게 다룰까?", "kind": "drawing"},
            "method": METHOD_IMAGES["vocab"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "정원에 벌레가 생기면 어떻게 할까요? 이번 글은 정원의 해충(pests)을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "어휘 문제는 단어 뜻만 보면 다 맞아 보여요. 문장마다 흐름을 잡아야 틀린 단어가 보여요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "요지를 잡고, 단어를 두 그룹으로 나눈 뒤, 밑줄 단어가 흐름에 맞는지 볼 거예요."}}],
    exam=exam,
    # repel, pollinator는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
    key_words={"passage": [g("pest", "해충"), g("medicinal herb", "약초"), g("beneficial insect", "익충"),
                           g("keep ~ in check", "~을 억제하다"), g("destructive", "파괴적인"), g("when it comes to", "~에 관해 말하자면"),
                           g("alter", "변화시키다"), g("ecosystem", "생태계"), g("on its own", "스스로, 자체적으로"),
                           g("overtake", "장악하다, 뒤덮다"), g("cultivate", "조성하다, 경작하다"), g("balance out", "균형을 이루다"),
                           g("entirely", "완전히"), g("further", "심화시키다"), g("initial", "초기의"), g("imbalance", "불균형")],
               "options": [g("shorten", "단축시키다"), g("prolong", "연장시키다"), g("allow", "허용하다")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="어휘 문제 푸는 법")
