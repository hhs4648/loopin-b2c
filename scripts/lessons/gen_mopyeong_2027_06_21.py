"""2026년 6월 모의평가(2027학년도, 평가원) 21번 레슨 + 대사를 만든다 (밑줄 의미 추론, 3점). 오답률 60% · Top 5 (메가스터디).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_21.py   (→ npm run policy:copy stamp <id> → npm run build)

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- 두 그룹 축: 왼쪽 「Griffin 쪽 (동물에게도)」 ↔ 오른쪽 「반대 쪽」. 칠판은 반대 쪽 말(unique to humans)이 처음 나오는 8문장에서 처음 연다
  (빈 칠판 금지). 그 전(1~7문장)은 칠판 정리(story)만
- 1문장 「so recent that the internet is older」에서 「그 전 과학자들은 동물에게 의식이 없다고 봤다」를 추론하게 했다(s1_before) — 너무 앞서 나간 추론이면 빼 주세요
- 밑줄 문장에 3지 「the ghost가 가리키는 생각」(s9_q)을 두었다: 사람에게만 의식 / 사람이 더 똑똑함 / 동물에게도 내면 세계.
  많이 고른 오답 ④(우월하다, 25%)를 미리 가르는 화면이라 넣었지만, 보기 ②·④와 너무 비슷해 답을 거의 주는 셈이면 빼 주세요
  (밑줄 틀 「아직 정할 것: 밑줄 뜻 3지 화면을 따로 둘지」)
- 6문장 s6_same 「사람과 같은 능력」(누가 더 낫다가 아니라 같다)도 ④ 대비용
- 헷갈리는 단어(trap): exhibited(전시하다 ✕ → 보여 주다), reason(이유 ✕ → 판단력) — 해설 번역(「보여주었다」「사고력과 판단력」)과 대조함
- ghost = 「환상」(해설 Words and Phrases), on the fly = 즉석에서, hallmark = 특징, or = 즉, After all = 결국 — 해설과 대조함
- hallowed는 시험지 아래 *풀이 단어 → 핵심어(key_words)에서 뺐다
- 해석 맞추기(add_match)는 7문장 하나만 넣었다. S·V 찾기 스텝은 만들지 않았다(2026-10-20 삭제), 끊어읽기 roles·slashes·modifiers만
- 4문장 those creatures 가리키기(s4_those)는 중·초만
반영한 규칙: README §0-1(2026-10-20~21), underline.md v1, 칠판은 읽은 데까지만, 대사 핵심만, 칭찬 분리(엔진), 화면 중계 말 없음.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, sc, keywords, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)
from beginner import add_match, add_refers, m  # noqa: E402

ID = "mopyeong-2027-06-21-give-up-the-ghost"

S = [
    "In fact, scientists attributing consciousness to any animal is so recent that the internet is older.",
    "In 1976 a zoologist named Donald Griffin published The Question of Animal Awareness, a book arguing that animal cognition "
    "ought to be taken seriously.",
    "He and a colleague had been responsible in 1944 for discovering that bats navigate by echolocation.",
    "Now, after a lifetime spent watching those creatures, he became convinced they had inner worlds.",
    "They had flexible behavior, he said, or the ability to change their behavior as external circumstances changed, a hallmark of "
    "true intelligence.",
    "He’d watched bats develop clever techniques for finding food; they could clearly make decisions on the fly, and exhibited many "
    "of the same problem-solving abilities as humans did.",
    "Animal thought and reason ought to be seriously studied, he argued.",
    "After all, despite the flourishing of neuroscience, no one had yet found any part of the brain unique to humans that might be "
    "responsible for this hallowed “consciousness.”",
    "Wasn’t it time to give up the ghost?",
]
# 해설지 번역
KO = [
    "사실 과학자들이 어떤 동물이든 의식이 있다고 생각한 일이 너무 최근이어서 인터넷이 더 오래되었다.",
    "1976년에 Donald Griffin이라는 한 동물학자는 'The Question of Animal Awareness'라는 책을 출간했는데, 그 책은 동물의 인지를 진지하게 여겨야 한다고 주장했다.",
    "그와 한 동료는 1944년에 박쥐가 반향 위치 측정으로 길을 찾는다는 사실을 발견한 주역이었다.",
    "이제 평생 그 생물들을 지켜본 끝에 그는 박쥐들이 내면 세계를 가지고 있다고 확신하게 되었다.",
    "박쥐들이 유연한 행동, 즉 외부 환경의 변화에 따라 행동을 바꿀 수 있는 능력을 가지고 있으며, 이는 진정한 지능의 특징이라고 그는 말했다.",
    "그는 박쥐들이 먹이를 찾기 위해 영리한 기술을 개발하는 것을 관찰했는데, 박쥐들은 분명히 즉석에서 결정을 내릴 수 있었고, 인간이 보여주는 것과 동일한 문제 해결 능력을 다수 보여주었다.",
    "동물의 사고력과 판단력을 진지하게 연구해야 한다고 그는 주장했다.",
    "결국, 신경과학의 번영에도 불구하고, 이 신성한 '의식'을 담당할지도 모르는 인간에게만 유일무이한 뇌의 어떤 부위를 아직 아무도 발견하지 못했다.",
    "그 환상을 포기할 때가 되지 않았는가?",
]

LEFT = "Griffin 쪽 (동물에게도)"
RIGHT = "반대 쪽"
SORT_LEFT = "왼쪽 · Griffin 쪽"
SORT_RIGHT = "오른쪽 · 반대 쪽"


def board(left, right, fresh=(), sort=None):
    """단어 지도 — 읽은 데까지만, 단어만. sort = 학생이 끌어 넣을 말(맞는 쪽에 fresh로 넣어 두면 답하기 전엔 숨는다)"""
    return groups("동물의 의식", LEFT, left, RIGHT, right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": SORT_LEFT, "right": SORT_RIGHT} if sort else None)


L7 = [("consciousness to any animal", "동물에게도 의식"), ("inner worlds", "내면 세계"), ("true intelligence", "진정한 지능"),
      ("same problem-solving abilities", "같은 문제 해결 능력"), ("thought and reason", "사고력과 판단력")]
R8 = [("unique to humans", "인간에게만 있는")]
R9 = R8 + [("the ghost", "그 유령")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("In fact", "사실"), g("scientists", "과학자들"),
                    g("attributing consciousness", "의식이 있다고 보는 것 · attribute A to B = A가 B에게 있다고 보다"),
                    g("attributing", "~이 있다고 보는"), g("consciousness", "의식"), g("to any animal", "어떤 동물에게든"),
                    g("so recent", "너무 최근이라"), g("recent", "최근의"), g("the internet", "인터넷"), g("older", "더 오래된")],
        "slashes": ["In fact,", "attributing consciousness", "to any animal", "so recent"],
        "roles": [r("scientists attributing consciousness to any animal", "S"), r("is … is", "V"), r("so recent", "C"),
                  r("the internet", "S"), r("older", "C")],
        "emphasis": ["attributing consciousness", "so recent"],
        "steps": [
            keywords("s1_keys", ["In fact", "attributing consciousness", "to any animal", "so recent"],
                     ["attributing consciousness", "to any animal", "so recent"],
                     "그건 뜻을 덧붙이는 말이라 핵심은 아니에요.",
                     "핵심어는 attributing consciousness, to any animal, so recent예요. 동물에게 의식이 있다고 보는 게 아주 최근이라는 말이에요.",
                     ask="이 문장을 빠르게 이해하려면 모든 단어를 읽지 않아도 돼요. 핵심어 3개를 찾아볼까요?"),
            choice("s1_before",
                   "동물에게 의식이 있다고 본 게 인터넷보다도 최근이래요. 그럼 그 전 과학자들은 동물을 어떻게 봤을까요?",
                   [("o0", "동물에게는 의식이 없다고 봤다", True), ("o1", "동물에게도 의식이 있다고 봤다", False),
                    ("o2", "인터넷으로 동물을 연구했다", False)],
                   "so recent(아주 최근)를 봐요. 최근에야 생긴 생각이면 그 전엔 어땠을지 떠올려 봐요.",
                   why="'so recent that the internet is older', 동물에게 의식을 인정한 건 아주 최근 일이래요. 그 전 과학자들은 의식을 동물에게 주지 않았다는 말이에요.",
                   highlight=["so recent"],
                   tips=[tip("attribute A to B", "'A가 B에게 있다고 보다'예요. attributing consciousness to any animal = 어떤 동물에게든 의식이 있다고 보는 것.", "attributing"),
                         tip("so ~ that …", "'너무 ~해서 …하다'예요. 너무 최근이라 인터넷이 더 오래됐을 정도래요.", "so recent")],
                   point="동물에게 의식이 있다고 보는 건 아주 최근 → 그 전 과학자들은 동물에게 의식이 없다고 봤다"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("In 1976", "1976년에"), g("a zoologist", "동물학자"), g("zoologist", "동물학자"),
                    g("named Donald Griffin", "Donald Griffin이라는 이름의"), g("published", "출간했다"),
                    g("The Question of Animal Awareness", "『동물의 인식에 관한 질문』 · 책 제목이에요"),
                    g("a book arguing", "~라고 주장하는 책"), g("arguing", "주장하는"), g("animal cognition", "동물의 인지"),
                    g("cognition", "인지"), g("ought to be taken seriously", "진지하게 여겨져야 한다"), g("seriously", "진지하게")],
        "slashes": ["In 1976", "named Donald Griffin", "Animal Awareness,", "a book arguing"],
        "roles": [r("a zoologist", "S"), r("published", "V"), r("The Question of Animal Awareness", "O")],
        "modifiers": ["named Donald Griffin", "arguing that animal cognition ought to be taken seriously"],
        "emphasis": ["animal cognition", "seriously"],
        "steps": [
            choice("s2_claim",
                   "Griffin의 책은 무엇을 주장했을까요?",
                   [("o0", "동물의 인지를 진지하게 다뤄야 한다", True), ("o1", "동물에게는 인지 능력이 없다", False),
                    ("o2", "인터넷이 동물 연구를 바꿨다", False)],
                   "콤마(,) 뒤 a book arguing that ~이 책의 주장이에요. that 뒤를 봐요.",
                   why="'animal cognition ought to be taken seriously', 동물의 인지를 진지하게 여겨야 한대요. 1문장의 새로운 생각과 같은 쪽이에요.",
                   highlight=["animal cognition", "seriously"],
                   tips=[tip("책 제목, a book arguing that ~", "콤마(,) 뒤 a book은 앞의 책 제목을 다시 설명해요. arguing that ~ = ~라고 주장하는.", "a book arguing"),
                         tip("ought to", "'~해야 한다'예요. should와 비슷해요.", "ought to")],
                   point="Griffin = 동물의 인지를 진지하게 다뤄야 한다"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "low",
        "glosses": [g("He and a colleague", "그와 한 동료"), g("colleague", "동료"), g("had been responsible", "주역이었다, 책임이 있었다"),
                    g("responsible", "책임이 있는, 주역인"), g("in 1944", "1944년에"), g("for discovering", "~을 발견한 데에"),
                    g("discovering", "발견하는 것"), g("bats", "박쥐"), g("navigate", "길을 찾다"),
                    g("by echolocation", "반향 위치 측정으로 · 소리를 내고 돌아오는 메아리로 위치를 아는 것"), g("echolocation", "반향 위치 측정")],
        "slashes": ["He and a colleague", "in 1944", "for discovering"],
        "roles": [r("He and a colleague", "S"), r("had been", "V"), r("responsible", "C"), r("bats", "S"), r("navigate", "V")],
        "steps": [
            show("s3_skim", "Griffin은 박쥐(bats)가 소리로 길을 찾는다는 걸 밝힌 사람이에요. 이 글의 동물은 박쥐예요.",
                 highlight=["bats"], button="다음 문장",
                 tips=[tip("be responsible for ~", "'~을 한 주역이다, ~을 담당하다'예요. 여기선 박쥐의 길 찾기를 발견한 주역이었다는 말이에요.", "responsible")]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Now", "이제"), g("after a lifetime", "평생을 보낸 뒤"), g("lifetime", "평생"), g("spent watching", "지켜보며 보낸"),
                    g("watching", "지켜보는"), g("those creatures", "그 생물들"), g("creatures", "생물"), g("became convinced", "확신하게 되었다"),
                    g("convinced", "확신하는"), g("inner worlds", "내면 세계"), g("inner", "내면의")],
        "slashes": ["Now,", "after a lifetime", "those creatures,", "became convinced"],
        "roles": [r("he", "S"), r("became", "V"), r("convinced", "C"), r("they", "S"), r("had", "V"), r("inner worlds", "O")],
        "modifiers": ["spent watching those creatures"],
        "emphasis": ["inner worlds"],
        "steps": [
            choice("s4_those",
                   "those creatures(그 생물들)는 무엇을 가리킬까요?",
                   [("o0", "bats (박쥐들)", True), ("o1", "scientists (과학자들)", False), ("o2", "humans (사람들)", False)],
                   "those가 가리키는 것은 앞 문장에서 찾아요. Griffin이 무엇을 연구했는지 떠올려 봐요.",
                   why="those는 앞 문장에서 찾아요. 3문장에서 Griffin이 연구한 동물은 박쥐(bats)예요.",
                   levels=["중", "초"], highlight=["those creatures"]),
            choice("s4_conv",
                   "평생 박쥐를 지켜본 Griffin은 무엇을 확신하게 됐을까요?",
                   [("o0", "박쥐에게 내면 세계가 있다", True), ("o1", "박쥐는 본능으로만 움직인다", False),
                    ("o2", "박쥐와 사람은 전혀 다르다", False)],
                   "became convinced 뒤에 that이 빠져 있어요. they had inner worlds가 확신한 내용이에요.",
                   why="'he became convinced they had inner worlds', 박쥐들에게도 내면 세계가 있다고 확신하게 됐대요.",
                   highlight=["convinced", "inner worlds"],
                   tips=[tip("become convinced (that) ~", "'~라고 확신하게 되다'예요. 여기선 that이 빠졌어요.", "convinced")],
                   point="Griffin의 확신: 박쥐에게도 inner worlds(내면 세계)가 있다"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("They had", "그것들은 ~을 가졌다"), g("flexible behavior", "유연한 행동"), g("flexible", "유연한"), g("behavior", "행동"),
                    g("he said", "그는 말했다"), g("or", "또는 · 여기서는 앞말을 바꿔 말하는 '즉'이에요"), g("the ability to change", "~을 바꾸는 능력"),
                    g("ability", "능력"), g("their behavior", "그들의 행동"), g("as external circumstances changed", "외부 환경이 바뀜에 따라"),
                    g("external", "외부의"), g("circumstances", "환경, 상황"), g("a hallmark of", "~의 특징"), g("hallmark", "특징"),
                    g("true intelligence", "진정한 지능"), g("intelligence", "지능")],
        "slashes": ["flexible behavior,", "he said,", "or the ability", "their behavior", "circumstances changed,"],
        "roles": [r("They", "S"), r("had", "V"), r("flexible behavior", "O"), r("he", "S"), r("said", "V"),
                  r("external circumstances", "S"), r("changed", "V")],
        "emphasis": ["flexible behavior", "true intelligence"],
        "steps": [
            choice("s5_hallmark",
                   "Griffin은 박쥐의 유연한 행동(flexible behavior)을 무엇의 특징이라고 했을까요?",
                   [("o0", "진짜 지능", True), ("o1", "겁 많은 성격", False), ("o2", "타고난 본능", False)],
                   "문장 끝 a hallmark of ~를 봐요. hallmark는 '특징'이에요.",
                   why="'a hallmark of true intelligence', 진정한 지능의 특징이래요. 환경이 바뀌면 행동을 바꿀 줄 안다는 거예요.",
                   highlight=["flexible behavior", "true intelligence"],
                   tips=[tip("A, or B", "콤마(,) 뒤 or the ability …는 앞의 flexible behavior를 바꿔 말한 거예요. 이때 or는 '즉'이에요.", "or the ability")],
                   point="flexible behavior(환경에 따라 행동을 바꾸는 능력) = 진정한 지능의 특징"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("He’d watched", "그는 지켜봤었다 · He’d = He had"), g("bats", "박쥐들이"), g("develop", "개발하다"),
                    g("clever techniques", "영리한 기술"), g("clever", "영리한"), g("techniques", "기술"),
                    g("for finding food", "먹이를 찾기 위한"), g("finding", "찾는 것"), g("food", "먹이"),
                    g("could clearly make decisions", "분명히 결정을 내릴 수 있었다"), g("clearly", "분명히"), g("decisions", "결정"),
                    g("on the fly", "즉석에서"), g("exhibited", "보여 주었다"),
                    g("the same problem-solving abilities", "같은 문제 해결 능력"), g("problem-solving", "문제 해결의"), g("abilities", "능력"),
                    g("as humans did", "인간이 보여 준 것과"), g("humans", "인간")],
        "slashes": ["He’d watched bats", "clever techniques", "finding food;", "make decisions", "on the fly,", "and exhibited",
                    "problem-solving abilities"],
        "roles": [r("He", "S"), r("’d watched", "V"), r("bats", "O"), r("develop", "C"), r("they", "S"), r("could … make", "V"),
                  r("decisions", "O"), r("exhibited", "V"), r("many of the same problem-solving abilities", "O"), r("humans", "S"), r("did", "V")],
        "emphasis": ["the same problem-solving abilities"],
        "steps": [
            choice("s6_same",
                   "박쥐의 문제 해결 능력은 사람과 비교해 어떻대요?",
                   [("o0", "사람과 같은 능력을 많이 보였다", True), ("o1", "사람보다 훨씬 떨어졌다", False), ("o2", "사람보다 훨씬 뛰어났다", False)],
                   "the same A as B는 'B와 같은 A'예요. as humans did를 봐요.",
                   why="'many of the same problem-solving abilities as humans did', 사람과 같은 문제 해결 능력을 많이 보였대요. 누가 더 낫다는 비교가 아니라 '같다'는 말이에요.",
                   highlight=["the same problem-solving abilities", "humans"],
                   tips=[tip("the same A as B", "'B와 같은 A'예요. as humans did의 did는 exhibited를 대신해요.", "the same"),
                         tip("on the fly", "'즉석에서'예요. 그 자리에서 바로 결정한다는 말이에요.", "on the fly")],
                   point="박쥐 = 사람과 같은 문제 해결 능력 (더 낫다·못하다가 아니라 같다)"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("Animal thought and reason", "동물의 사고력과 판단력"), g("thought", "사고, 생각"), g("reason", "이성, 판단력"),
                    g("ought to be seriously studied", "진지하게 연구되어야 한다"), g("studied", "연구된"), g("he argued", "그는 주장했다"),
                    g("argued", "주장했다")],
        "slashes": ["Animal thought and reason", "seriously studied,"],
        "roles": [r("Animal thought and reason", "S"), r("ought to be seriously studied", "V"), r("he", "S"), r("argued", "V")],
        "steps": [],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("After all", "결국 · 앞 주장의 근거를 댈 때"), g("despite", "~에도 불구하고"),
                    g("the flourishing of neuroscience", "신경과학의 번영"), g("flourishing", "번영, 번성"), g("neuroscience", "신경과학"),
                    g("no one", "아무도 ~ 않다"), g("had yet found", "아직 찾았다 · no one과 함께 '아직 아무도 찾지 못했다'"),
                    g("any part of the brain", "뇌의 어떤 부위"), g("brain", "뇌"), g("unique to humans", "인간에게만 있는"),
                    g("unique", "유일무이한, 고유한"), g("might be responsible for", "~을 담당할지도 모르는"), g("hallowed", "신성한 (*풀이 단어)"),
                    g("consciousness", "의식")],
        "slashes": ["After all,", "of neuroscience,", "had yet found", "of the brain", "unique to humans", "might be responsible"],
        "roles": [r("no one", "S"), r("had … found", "V"),
                  r("any part of the brain unique to humans that might be responsible for this hallowed “consciousness", "O")],
        "modifiers": ["unique to humans", "that might be responsible for this hallowed “consciousness"],
        "emphasis": ["no one", "unique to humans"],
        "steps": [
            choice("s8_found",
                   "신경과학이 크게 발전했는데도, 의식을 담당하는 인간만의 뇌 부위를 찾았을까요?",
                   [("o0", "아직 아무도 못 찾았다", True), ("o1", "신경과학이 찾아냈다", False), ("o2", "동물의 뇌에서만 찾았다", False)],
                   "주어 no one(아무도 ~ 않다)을 봐요. 문장 전체가 부정이에요.",
                   why="'no one had yet found', 아직 아무도 발견하지 못했대요. 신경과학이 번성했는데도요(despite).",
                   highlight=["no one", "unique to humans"],
                   tips=[tip("no one + 동사", "'아무도 ~ 않다'예요. not이 없어도 문장 전체가 부정이에요.", "no one"),
                         tip("despite ~", "'~에도 불구하고'예요. 뒤에는 명사(the flourishing)가 와요.", "despite"),
                         tip("this hallowed “consciousness”", "따옴표는 '사람들이 그렇게 떠받드는' 정도로 거리를 두는 표시예요. hallowed는 *풀이 단어(신성한)예요.", "hallowed")],
                   point="인간에게만 있고 의식을 담당할 뇌 부위 → 아직 아무도 못 찾음"),
            choice("s8_sort",
                   "unique to humans(인간에게만 있는)는 칠판 어느 쪽 말일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "Griffin은 동물에게도 의식이 있다고 봐요. '인간에게만'이 그 생각과 같은지 봐요.",
                   why="Griffin은 의식이 동물에게도 있다고 봐요. 인간에게만 있다는 건 Griffin이 맞서는 생각이에요.",
                   highlight=["unique to humans"],
                   panel=board(L7, R8, fresh=("unique to humans",), sort=["unique to humans"]),
                   point="unique to humans(인간에게만) ↔ Griffin(동물에게도)"),
        ],
    },
    {
        "id": 9, "text": S[8], "model_translation": KO[8], "teaching_value": "high",
        "glosses": [g("Wasn’t it time to", "~할 때가 되지 않았는가"), g("give up", "포기하다, 버리다"), g("the ghost", "그 유령"),
                    g("ghost", "유령")],
        "roles": [r("Wasn’t", "V"), r("it", "S"), r("time", "C")],
        "steps": [
            choice("s9_sort",
                   "드디어 밑줄이에요. Griffin이 버리자는 the ghost(유령)는 칠판 어느 쪽 말일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "give up은 '버리다'예요. Griffin이 버리자고 할 생각은 자기 생각일지, 맞서는 생각일지 봐요.",
                   why="Griffin은 자기 생각을 버리자고 하지 않아요. 버리자는 건 Griffin이 맞서는 쪽 생각이에요.",
                   highlight=["the ghost"],
                   panel=board(L7, R9, fresh=("the ghost",), sort=["the ghost"]),
                   point="the ghost = Griffin이 버리자는 생각 → 반대 쪽"),
            choice("s9_q",
                   "그럼 the ghost가 가리키는 생각은 무엇일까요?",
                   [("o0", "사람에게만 의식이 있다는 생각", True), ("o1", "사람이 동물보다 더 똑똑하다는 생각", False),
                    ("o2", "동물에게도 내면 세계가 있다는 생각", False)],
                   "8문장의 unique to humans(인간에게만 있는)를 떠올려 봐요. 무엇이 인간에게만 있다고 했나요?",
                   why="'unique to humans', 의식을 담당하는 인간만의 뇌 부위를 아무도 못 찾았대요. 누가 더 똑똑한지가 아니라 의식이 인간에게만 있느냐는 이야기예요.",
                   highlight=["the ghost"],
                   point="the ghost = 의식은 인간에게만 있다는 믿음 (더 똑똑하다는 비교 X)"),
            show("s9_map",
                 "the ghost는 실체 없는 '환상'이에요. 의식이 인간에게만 있다는 믿음을 이제 버릴 때가 됐다는 말이에요.\n이 뜻을 바꿔 쓴 보기를 골라 봐요.",
                 button="문제 풀러 갈게요",
                 tips=[tip("Wasn’t it time to ~?", "'~할 때가 되지 않았나요?'예요. 묻는 말이지만 '이제 ~할 때다'라는 주장이에요.", "Wasn’t it time"),
                       tip("ghost", "원래 뜻은 '유령'이에요. 여기서는 실체가 없는 '환상'이에요.", "ghost"),
                       tip("give up", "'포기하다, 버리다'예요.", "give up")]),
        ],
    },
]

add_match(sentences, 7, [m("Animal thought and reason", "동물의 사고력과 판단력은"), " ", m("ought to be seriously studied", "진지하게 연구되어야 한다"),
                         ", ", m("he argued", "그는 주장했다"), "."])
add_refers(sentences, 3, {"He and a colleague": "He = Donald Griffin"})
add_refers(sentences, 5, {"They had": "They = bats(박쥐들)"})
add_refers(sentences, 6, {"they": "bats(박쥐들)"})

SENSES = {
    1: [sense("to", "attributing consciousness to any animal", "~에게 (있다고)", "attribute A to B = A가 B에게 있다고 보다"),
        sense("so", "so recent that", "너무 (~해서)", "so ~ that … = 너무 ~해서 …하다"),
        sense("that", "so recent that the internet", "(그래서) …할 정도로", "so ~ that …의 that")],
    2: [sense("that", "arguing that animal cognition", "~라고", "명사절 that (argue that … = ~라고 주장하다)"),
        sense("to", "ought to be taken", "~해야 (한다)", "ought to + 동사원형 = ~해야 한다")],
    3: [sense("for", "responsible in 1944 for discovering", "~에 대해, ~한 데에", "be responsible for ~ = ~의 주역이다"),
        sense("that", "discovering that bats navigate", "~라는 것", "명사절 that (discover that … = ~라는 것을 발견하다)")],
    5: [sense("to", "the ability to change", "~할 (능력)", "명사 + to부정사 = ~할 명사"),
        sense("as", "as external circumstances changed", "~함에 따라", "접속사 as + 주어·동사 = ~함에 따라")],
    6: [sense("for", "techniques for finding food", "~을 위한", "for + -ing = ~하기 위한"),
        sense("as", "the same problem-solving abilities as humans did", "~와 같은", "the same A as B = B와 같은 A")],
    7: [sense("to", "ought to be seriously studied", "~해야 (한다)", "ought to + 동사원형 = ~해야 한다")],
    8: [sense("yet", "had yet found", "아직", "부정문(no one)의 yet = 아직"),
        sense("to", "unique to humans", "~에게만 (있는)", "unique to ~ = ~에게만 있는"),
        sense("that", "humans that might be responsible", "(앞 명사를 꾸밈)", "관계대명사 that + 동사 — 앞의 any part of the brain을 꾸밈"),
        sense("for", "responsible for this hallowed", "~을 (담당하는)", "be responsible for ~ = ~을 담당하다")],
    9: [sense("to", "time to give up", "~할 (때)", "time to + 동사원형 = ~할 때")],
}

WORDS = {
    "fact": "사실", "scientists": "과학자들", "attributing": "~이 있다고 보는", "consciousness": "의식", "animal": "동물",
    "recent": "최근의", "internet": "인터넷", "older": "더 오래된", "zoologist": "동물학자", "named": "~라는 이름의",
    "donald": "도널드(이름)", "griffin": "그리핀(사람 이름)", "published": "출간했다", "question": "질문, 문제", "awareness": "인식",
    "book": "책", "arguing": "주장하는", "cognition": "인지", "ought": "~해야 한다", "taken": "여겨진", "seriously": "진지하게",
    "colleague": "동료", "responsible": "책임이 있는, 주역인", "discovering": "발견하는 것", "bats": "박쥐", "navigate": "길을 찾다",
    "echolocation": "반향 위치 측정", "lifetime": "평생", "spent": "보낸", "watching": "지켜보는", "creatures": "생물",
    "became": "~이 되었다", "convinced": "확신하는", "inner": "내면의", "worlds": "세계", "flexible": "유연한", "behavior": "행동",
    "said": "말했다", "ability": "능력", "change": "바꾸다", "external": "외부의", "circumstances": "환경, 상황", "changed": "바뀌었다",
    "hallmark": "특징", "true": "진정한", "intelligence": "지능", "watched": "지켜봤다", "develop": "개발하다", "clever": "영리한",
    "techniques": "기술", "finding": "찾는 것", "food": "먹이", "clearly": "분명히", "make": "내리다, 만들다", "decisions": "결정",
    "fly": "날다, 파리 · on the fly = 즉석에서", "exhibited": "보여 주었다", "problem-solving": "문제 해결의", "abilities": "능력",
    "humans": "인간", "did": "했다", "thought": "사고, 생각", "reason": "이성, 판단력", "studied": "연구된", "argued": "주장했다",
    "flourishing": "번영, 번성", "neuroscience": "신경과학", "found": "찾았다", "part": "부위, 부분", "brain": "뇌",
    "unique": "유일무이한, 고유한", "hallowed": "신성한", "ghost": "유령", "wasn’t": "~이 아니었다", "time": "때, 시간",
    "give": "주다 · give up = 포기하다", "one": "하나 · no one = 아무도 ~ 않다", "might": "~일지도 모른다", "could": "~할 수 있었다",
    "any": "어떤", "same": "같은", "he’d": "그는 ~했었다 (= he had)",
}

# 칠판 정리 — 2~3문장마다, 밑줄 문장 앞에서 멈춘다(요약이 곧 답). 8문장 내용도 넣지 않는다
STORIES = [
    (2, [sc("문장 1", "🧠", "consciousness to any animal · so recent", "동물에게 의식이 있다고 본 건 아주 최근 일이에요"),
         sc("문장 2", "📘", "animal cognition · taken seriously", "Griffin은 동물의 인지를 진지하게 다뤄야 한다고 했어요")]),
    (5, [sc("문장 3~4", "🦇", "bats · inner worlds", "박쥐를 평생 지켜본 Griffin은 박쥐에게 내면 세계가 있다고 확신했어요"),
         sc("문장 5", "🔄", "flexible behavior · true intelligence", "환경에 따라 행동을 바꾸는 건 진정한 지능의 특징이래요")]),
    (7, [sc("문장 6~7", "🧩", "the same problem-solving abilities as humans", "박쥐도 사람과 같은 문제 해결 능력을 보여요 — 동물의 생각을 연구해야 해요")]),
]

OPTIONS = [
    ("1", "the claim that animal consciousness should be studied", ["animal consciousness", "should be studied"],
     "동물의 의식을 연구해야 한다는 주장", False),
    ("2", "the belief that consciousness is a quality exclusive to humans", ["consciousness", "exclusive to humans"],
     "의식이 인간에게만 독점적으로 존재하는 특성이라는 믿음", True),
    ("3", "the illusion that animals possess truly conscious inner worlds", ["illusion", "truly conscious inner worlds"],
     "동물이 진정한 의식을 지닌 내면 세계를 가지고 있다는 착각", False),
    ("4", "the idea that human cognition is superior to that of animals", ["human cognition", "superior"],
     "인간의 인지가 동물의 인지보다 우월하다는 생각", False),
    ("5", "the concept that humans and animals are essentially alike", ["humans and animals", "essentially alike"],
     "인간과 동물은 본질적으로 비슷하다는 개념", False),
]
exam = {
    "question": "밑줄 친 the ghost가 다음 글에서 의미하는 바로 가장 적절한 것은? [3점]",
    "underline": "the ghost", "analysis_first": True, "wrong_rate": 60.0, "wrong_rank": 5,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("claim", "주장"), g("animal consciousness", "동물의 의식"), g("should be studied", "연구되어야 한다"), g("belief", "믿음"),
                g("quality", "특성"), g("exclusive to", "~에게만 독점적인"), g("illusion", "착각"), g("possess", "지니다, 가지다"),
                g("truly", "진정으로"), g("conscious", "의식이 있는"), g("inner worlds", "내면 세계"), g("idea", "생각"),
                g("human cognition", "인간의 인지"), g("superior to", "~보다 우월한"), g("concept", "개념"), g("essentially", "본질적으로"),
                g("alike", "비슷한")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "보기도 다 해석할 필요 없어요. 색칠된 단어만 보고, the ghost가 칠판 어느 쪽 생각인지 떠올리며 골라 봐요.",
        "정답이에요! the ghost는 인간에게만 있다고 떠받든 '의식'이에요. 의식이 인간에게만 있다는 믿음을 이제 버리자는 말이에요.",
        "정답은 ②예요. the ghost는 의식이 인간에게만 있다는 믿음이에요. 인간만의 뇌 부위를 아무도 못 찾았으니 버리자는 말이에요.",
        {"1": "동물의 의식을 연구하자는 건 Griffin의 주장이에요. 버리자는 생각이 아니에요.",
         "3": "Griffin은 동물에게 내면 세계가 있다고 확신했어요. 그걸 착각이라고 하지 않았어요.",
         "4": "누가 더 뛰어난지는 글에 없어요. 의식이 인간에게만 있느냐가 글의 이야기예요.",
         "5": "인간과 동물이 비슷하다는 건 Griffin 쪽 생각이에요. 버리자는 생각이 아니에요."},
        {"4": review(25,
                     "④는 '인간의 인지가 동물보다 우월하다'예요. 사람이 특별하다는 말처럼 들려서 그럴듯해요. "
                     "하지만 글은 박쥐가 사람과 '같은' 능력을 보였다고 하고, 인간에게만(unique to humans) 의식이 있느냐를 따져요.",
                     panel=rows(("6문장", "the same problem-solving abilities as humans", "사람과 같은 능력 — 더 낫다·못하다가 아님", "hl"),
                                ("8문장", "unique to humans … “consciousness”", "인간에게만 있다는 의식 → the ghost", "hl"),
                                ("④", "superior", "더 뛰어나다 — 글에 없는 비교", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 21번 (밑줄 의미 추론, 3점)",
    topic="밑줄 문제 푸는 법: 핵심 단어 → 관계(Griffin 쪽 ↔ 반대 쪽) → 밑줄 뜻",
    method={"type": "underline_meaning", "labels": ["핵심 단어 찾기", "관계 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-animal-consciousness.svg", ("Animals", "동물"), "?", ("Consciousness", "의식"),
                                       "동물에게도 의식이 있을까?", "2026년 6월 모의평가 21번 도입 칠판"),
                      "alt": "칠판: Animals(동물) ? Consciousness(의식) — 동물에게도 의식이 있을까?", "kind": "drawing"},
            "method": METHOD_IMAGES["underline"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "동물에게도 의식이 있을까요? 이번 글은 박쥐를 평생 지켜본 한 동물학자의 주장을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네", "brief": {"say": "수능 문제는 시간 싸움이에요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "밑줄 문제는 핵심 단어 위주로 지문의 요지를 빠르게 파악하면 좋아요."}}],
    exam=exam,
    # hallowed는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
    key_words={"passage": [g("consciousness", "의식"), g("attribute A to B", "A가 B에게 있다고 보다"), g("cognition", "인지"),
                           g("take ~ seriously", "~을 진지하게 여기다"), g("be responsible for", "~의 주역이다, ~을 담당하다"),
                           g("navigate", "길을 찾다"), g("echolocation", "반향 위치 측정"), g("convinced", "확신하는"),
                           g("inner world", "내면 세계"), g("flexible", "유연한"), g("circumstances", "환경, 상황"), g("hallmark", "특징"),
                           g("on the fly", "즉석에서"), g("exhibit", "보여 주다"), g("neuroscience", "신경과학"),
                           g("unique to", "~에게만 있는"), g("give up", "포기하다"), g("ghost", "유령, 환상")],
               "options": [g("exclusive to", "~에게만 독점적인"), g("superior to", "~보다 우월한"), g("illusion", "착각"),
                           g("possess", "지니다"), g("essentially", "본질적으로")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함: exhibited 보여주었다 · reason 판단력.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다
TRAPS = {
    6: [tip("exhibited", "이 글에서는 → 보여 주었다  ('전시했다' 아님)", "exhibited", trap=True)],
    7: [tip("reason", "이 글에서는 → 이성, 판단력  ('이유' 아님)", "reason", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="밑줄 문제 푸는 법")
