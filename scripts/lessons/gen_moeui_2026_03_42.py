"""2026년 3월 고3 42번 레슨 + 대사를 만든다 (41~42 장문 중 42번 — 문맥상 낱말의 쓰임, 3점). 오답률 57.7% · Top 10 (EBS).

    PYTHONUTF8=1 py scripts/lessons/gen_moeui_2026_03_42.py   (→ npm run policy:copy stamp <id> → npm run build)

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- 두 그룹 이름: 왼쪽 「있는 그대로 비춤」(direct reflection · coherent whole · naive realism) ↔ 오른쪽 「그대로 비추지 않음」
  (complex affair · flaws · blind spots · exclusions · absences · in pieces · Eliot의 defective). 둘 다 2문장에서 나온 말로 지었다
- 정답 ④ (d)praising(→ reproaching): 10문장에서는 「Eliot의 말은 어느 그룹?」「naive realism은 어느 그룹?」만 묻고 맞다/틀리다는 말하지 않는다
- (a)(b)(c)(e)는 「그럼 (x)는 문맥에 맞을까요, 틀릴까요?」로 학생이 고른다(README §0-1). 넷을 다 확인하니 (d)가 남는 건 30번·2024 42번과 같다
- 많이 고른 오답 ③ (c)absences 24.8% — absences(부재)와 present(존재하는)가 한 문장에 있어 모순처럼 보여서. these = 5문장 「거울에 나타나지 않는 것들」로 짚는다
  ⑤ (e)invisible 21.9% — 11문장 cannot be captured in the mirror(거울 안에 담기지 않음) = invisible로 짚는다
- coherent·discordant·defective는 시험지 아래 * 풀이 단어 — 핵심어(key_words)에서 뺐다. 다만 coherent whole·discordant·defective는
  그룹 나누기 칠판에는 썼다(정답 단서라서 — 39번 transparent와 같은 예외). 빼야 하면 알려 주세요
- 헷갈리는 단어(trap): work(작품), figure(나타나다), present(존재하는), holds(~라고 믿다) — 해설 번역과 대조함
- 평가 뒤집기(+/−): exclusions·distortions를 significant로 좋게 보는 4문장은 41번(제목)에서 짚고, 42번에선 그룹 나누기만 한다
- 해석 맞추기(add_match)는 넣지 않았다 — 데이터 세션이 채우는 자리
- 41번(제목)은 이 레슨의 생성물에서 문장·뜻·끊어읽기를 가져간다 → 42번을 고치면 41번도 다시 돌린다
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, sc, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)
from beginner import add_refers  # noqa: E402

ID = "moeui-2026-03-42-literary-mirror"

S = [
    "Writing of a commentary by Lenin on Leo Tolstoy, the critic Pierre Macherey agrees with Lenin’s claim that Tolstoy’s work holds up "
    "a mirror to the Russian revolution of 1905.",
    "Yet this mirroring, Macherey argues, is a complex affair, by no means a (a)direct reflection of the world as it stands.",
    "If literary works are in some sense mirrors, they are mirrors marked by flaws and blind spots.",
    "In fact, they are as significant for what they don’t reflect—for their exclusions and distortions—as for what they do.",
    "There are things which do not and cannot (b)figure in the mirror—in the case of Tolstoy, certain contradictions in society of which "
    "he could not be conscious.",
    "Even so, the mirror makes us aware of these (c)absences, which thus become faintly present.",
    "It is as though it allows us to see more clearly what isn’t there.",
    "There is also no reason to assume that what we see in the mirror must form a coherent whole.",
    "On the contrary, it may be in pieces and discordant.",
    "‘The mirror is doubtless defective; the outlines will sometimes be disturbed; the reflection faint or confused’, remarks George Eliot "
    "in Adam Bede, (d)praising the kind of naive realism which holds that art (or mirrors) always tell it like it is.",
    "A mirror offers us a version of reality, but it does so from a viewpoint which cannot be captured in the mirror itself.",
    "And because this viewpoint is (e)invisible to us, we might be tempted to take it as beyond question.",
]
# 해설지 번역 (10문장의 praising은 해설대로 정답 낱말 reproaching으로 옮긴 번역을 쓴다 — 「칭찬(→ 비난)한다」)
KO = [
    "Leo Tolstoy에 대한 Lenin의 논평에 관해 기술하며, 비평가 Pierre Macherey는 Tolstoy의 작품이 1905년 러시아 혁명에 거울을 비추고 있다는 Lenin의 주장에 동의한다.",
    "하지만 Macherey는 이러한 거울 비추기가 복잡한 일이며, 결코 있는 그대로의 세상에 대한 직접적인 상(像)이 아니라고 주장한다.",
    "만약 문학 작품이 어떤 의미에서 거울이라면, 그것은 결함과 사각지대에 의해 특징지어지는 거울이다.",
    "사실 그것은 그것이 비추는 것만큼이나 비추지 않는 것, 즉 배제와 왜곡으로 인해 중요하다.",
    "거울 속에 나타나지 않으며 나타날 수도 없는 것들이 있는데, Tolstoy의 경우 그가 의식할 수 없었던 사회의 특정 모순들이 그러하다.",
    "그렇다 하더라도, 거울은 우리에게 이러한 부재를 인식하게 하며, 그리하여 그것들은 희미하게 존재하게 된다.",
    "그것은 마치 거울이 우리가 그곳에 없는 것을 더 명확하게 볼 수 있게 해 주는 것과 같다.",
    "우리가 거울 속에서 보는 것이 틀림없이 일관된 전체를 형성할 것이라고 가정할 이유 또한 없다.",
    "그와는 반대로 그것은 단편적이고 조화를 이루지 못할 수도 있다.",
    "George Eliot은 Adam Bede에서 \"그 거울은 의심할 바 없이 불완전하고, 윤곽은 때때로 흐트러질 것이며, 상(像)은 희미하거나 분명치 않기도 할 것이다.\"라고 "
    "언급하며, 예술(또는 거울)이 언제나 있는 그대로를 말해 준다고 믿는 종류의 소박실재론을 비난한다.",
    "거울은 우리에게 현실의 한 버전을 제공하지만, 그것은 거울 그 자체에서는 포착될 수 없는 관점에서 그렇게 하는 것이다.",
    "그리고 이 관점은 우리에게 보이지 않기 때문에, 우리는 그것을 의심할 여지가 없는 것으로 받아들이고 싶은 유혹을 느낄지도 모른다.",
]
UNDER = ["(a)direct", "(b)figure", "(c)absences", "(d)praising", "(e)invisible"]

# 두 그룹 — 이름은 2문장에서 나온 말로만 (칠판엔 읽은 데까지만)
LEFT = "있는 그대로 비춤"
RIGHT = "그대로 비추지 않음"
SORT_LEFT = "왼쪽 · 있는 그대로 비춤"
SORT_RIGHT = "오른쪽 · 그대로 비추지 않음"


def board(left, right, fresh=(), sort=None):
    """단어 지도. sort = 학생이 끌어 넣을 말 — 그 말은 맞는 쪽에 fresh로 넣어 두면 답하기 전엔 숨고 맞히면 붙는다"""
    return groups("문학이라는 거울", LEFT, left, RIGHT, right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": SORT_LEFT, "right": SORT_RIGHT} if sort else None)


def ok_or_not(id, under, hint, why, point, **extra):
    """정답이 아닌 밑줄 — 알려 주지 않고 학생이 「맞을까요, 틀릴까요?」로 고른다 (README §0-1)"""
    return choice(id, f"그럼 {under}는 문맥에 맞을까요, 틀릴까요?",
                  [("o0", "문맥에 맞아요", True), ("o1", "문맥에 안 맞아요", False)],
                  hint, why=why, point=point, **extra)


L2 = [("direct reflection", "직접 비춤")]
R2 = [("complex affair", "복잡한 일")]
R3 = R2 + [("flaws", "결함"), ("blind spots", "사각지대")]
R4 = R3 + [("exclusions", "배제"), ("distortions", "왜곡")]
R6 = R4 + [("absences", "부재")]
L8 = L2 + [("coherent whole", "일관된 전체")]
R9 = R6 + [("in pieces", "조각난"), ("discordant", "조화롭지 못한")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("Writing of", "~에 관해 쓰면서"), g("a commentary", "논평"), g("by Lenin", "Lenin이 쓴 · Lenin은 사람 이름이에요"),
                    g("on Leo Tolstoy", "Tolstoy에 대한 · Tolstoy는 작가 이름이에요"), g("the critic Pierre Macherey", "비평가 Pierre Macherey"),
                    g("agrees with", "~에 동의한다"), g("Lenin’s claim", "Lenin의 주장"), g("Tolstoy’s work", "Tolstoy의 작품"),
                    g("holds up a mirror", "거울을 비추다 · 여기서는 '~을 거울처럼 비추어 보여 주다'"),
                    g("the Russian revolution of 1905", "1905년 러시아 혁명")],
        "slashes": ["by Lenin", "Leo Tolstoy,", "Pierre Macherey", "Lenin’s claim", "holds up a mirror"],
        "roles": [r("the critic Pierre Macherey", "S"), r("agrees", "V"), r("Tolstoy’s work", "S"), r("holds up", "V"), r("a mirror", "O")],
        "steps": [
            show("s1_mirror", "Tolstoy의 작품이 1905년 러시아 혁명을 비추는 거울이라는 주장에 Macherey도 동의한대요. 이 글은 '문학 = 거울'이라는 비유로 이어져요.",
                 highlight=["holds up a mirror"], button="다음 문장",
                 tips=[tip("Writing of ~, 주어 …", "Writing of ~는 '~에 관해 쓰면서'예요. 콤마(,) 뒤 the critic Pierre Macherey가 이 문장의 주어예요.", "Writing of"),
                       tip("work", "이 글에서는 → 작품  ('일' 아님)", "work", trap=True)]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Yet", "그러나 · 문장 앞의 yet은 '그러나'예요"), g("this mirroring", "이 거울 비추기"), g("Macherey argues", "Macherey는 주장한다"),
                    g("complex affair", "복잡한 일"), g("by no means", "결코 ~이 아닌"), g("direct reflection", "직접적인 상(像) · 그대로 비친 모습"),
                    g("of the world", "세상의"), g("as it stands", "있는 그대로의")],
        "slashes": ["Yet this mirroring,", "Macherey argues,", "complex affair,", "(a)direct reflection"],
        "roles": [r("this mirroring", "S"), r("Macherey", "S"), r("argues", "V"), r("is", "V"), r("a complex affair", "C")],
        "emphasis": ["complex affair", "by no means"],
        "steps": [
            choice("s2_mean",
                   "Macherey는 이 거울 비추기(this mirroring)가 세상을 있는 그대로 비춘다고 할까요?",
                   [("o0", "있는 그대로 비춘다", False), ("o1", "복잡하고, 결코 그대로 비추지 않는다", True)],
                   "by no means를 봐요. not보다 센 부정, '결코 ~이 아닌'이에요.",
                   why="'a complex affair, by no means a direct reflection', 복잡한 일이고 결코 직접 비추는 게 아니래요.",
                   highlight=["complex affair", "by no means"],
                   tips=[tip("by no means", "'결코 ~이 아닌'이에요. not보다 센 부정이에요.")],
                   point="요지 시작: 문학이라는 거울은 복잡하고, 세상을 결코 있는 그대로 비추지 않는다 (by no means = 결코 ~이 아닌)"),
            ok_or_not("s2_check", "(a)direct",
                      "by no means(결코 ~이 아닌)가 direct reflection 앞에 있어요. '직접 비추는 게 결코 아니다'가 앞의 complex affair와 이어지는지 봐요.",
                      "복잡한 일이지 결코 직접 비추는 게 아니라는 말이라 앞뒤가 이어져요. (a)direct는 맞는 낱말이에요.",
                      "(a) direct: by no means a direct reflection = 결코 직접 비추는 게 아니다 → complex affair와 이어짐",
                      highlight=["by no means", "direct"]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("If", "만약 ~라면"), g("literary works", "문학 작품"), g("in some sense", "어떤 의미에서"), g("mirrors", "거울"),
                    g("marked by", "~로 특징지어진 · 여기서는 '~이 있는'"), g("flaws", "결함"), g("blind spots", "사각지대 · 거울에 안 비치는 곳")],
        "slashes": ["If literary works", "in some sense mirrors,", "they are mirrors"],
        "roles": [r("literary works", "S"), r("are … are", "V"), r("mirrors marked by flaws and blind spots", "C"), r("mirrors", "C"), r("they", "S")],
        "modifiers": ["marked by flaws and blind spots"],
        "emphasis": ["literary works", "flaws", "blind spots"],
        "steps": [
            show("s3_board",
                 "2문장을 두 그룹으로 나눠 봐요. by no means(결코 ~이 아닌)가 붙은 direct reflection은 반대편이에요.\n시험 꿀팁: not, no, by no means가 붙은 말은 바로 반대 그룹이에요.",
                 button="다음", panel=board(L2, R2, fresh=("direct reflection", "complex affair"))),
            choice("s3_sort",
                   "문학 작품은 결함(flaws)과 사각지대(blind spots)가 있는 거울이래요. flaws와 blind spots는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "결함이 있는 거울이 세상을 있는 그대로 비출 수 있을지 생각해 봐요.",
                   why="결함과 사각지대가 있으면 그대로 비출 수 없어요. 2문장의 complex affair와 같은 쪽이에요.",
                   highlight=["flaws", "blind spots"],
                   panel=board(L2, R3, fresh=("flaws", "blind spots"), sort=["flaws", "blind spots"]),
                   point="flaws(결함)·blind spots(사각지대) → 그대로 비추지 않는 쪽"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("In fact", "사실"), g("significant", "중요한"), g("don’t reflect", "비추지 않다 · what they don’t reflect = 그것들이 비추지 않는 것"),
                    g("exclusions", "배제 · 빼놓은 것"), g("distortions", "왜곡 · 비틀어 보인 것"), g("what they do", "그것들이 비추는 것 · do = reflect")],
        "slashes": ["In fact,", "as significant", "don’t reflect—", "and distortions—"],
        "roles": [r("they", "S"), r("are", "V"), r("significant", "C")],
        "emphasis": ["significant", "don’t reflect", "exclusions", "distortions"],
        "steps": [
            choice("s4_mean",
                   "문학 작품은 비추는 것만 중요할까요?",
                   [("o0", "비추는 것만 중요하다", False), ("o1", "비추지 않는 것도 똑같이 중요하다", True)],
                   "as significant for A as for B는 'B만큼이나 A 때문에도 중요하다'예요. A 자리의 what they don’t reflect를 봐요.",
                   why="'as significant for what they don’t reflect … as for what they do', 비추는 것만큼이나 비추지 않는 것 때문에도 중요하대요.",
                   highlight=["significant", "don’t reflect"],
                   tips=[tip("as ~ for A as for B", "'B만큼이나 A 때문에도 ~하다'예요. 여기선 비추는 것(what they do)만큼이나 비추지 않는 것(what they don’t reflect) 때문에도 중요하다는 말이에요.")],
                   point="as significant for A as for B = B만큼이나 A 때문에도 중요하다 → 비추지 않는 것도 중요"),
            choice("s4_sort",
                   "대시(—) 사이의 exclusions(배제)와 distortions(왜곡)는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "대시(—) 사이는 앞의 what they don’t reflect를 다시 말한 거예요.",
                   why="대시(—) 사이는 '비추지 않는 것'을 다시 말한 거예요. 빼놓고 비튼 것이니 그대로 비추는 쪽이 아니에요.",
                   highlight=["exclusions", "distortions"],
                   panel=board(L2, R4, fresh=("exclusions", "distortions"), sort=["exclusions", "distortions"]),
                   point="대시(—) 사이 exclusions·distortions = what they don’t reflect → 그대로 비추지 않는 쪽"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("There are things", "~한 것들이 있다"), g("do not and cannot", "~하지 않고 ~할 수도 없다"),
                    g("figure", "숫자, 인물 · 여기서는 동사 '나타나다'예요"), g("in the mirror", "거울 속에"), g("in the case of", "~의 경우에"),
                    g("Tolstoy", "Tolstoy · 작가 이름"), g("certain contradictions", "어떤 모순들"), g("in society", "사회 속의"),
                    g("of which he could not be conscious", "그가 의식할 수 없었던")],
        "slashes": ["There are things", "(b)figure in the mirror—", "case of Tolstoy,", "in society"],
        "roles": [r("are", "V"), r("things", "S")],
        "modifiers": ["which do not and cannot (b)figure in the mirror", "of which he could not be conscious"],
        "steps": [
            ok_or_not("s5_check", "(b)figure",
                      "figure는 여기서 동사 '나타나다'예요. 거울에 나타나지 않는 것들이 4문장의 what they don’t reflect와 같은 말인지 봐요.",
                      "'things which do not and cannot figure in the mirror', 거울에 나타나지 않고 나타날 수도 없는 것들이에요. 4문장의 '비추지 않는 것'과 같은 말이라 (b)figure는 맞는 낱말이에요.",
                      "(b) figure = 나타나다 → 거울에 나타나지 않는 것 = 4문장의 what they don’t reflect",
                      highlight=["do not and cannot", "figure"],
                      tips=[tip("figure", "이 글에서는 → (동사) 나타나다  ('숫자·인물' 아님)", "figure", trap=True)]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Even so", "그렇다 하더라도"), g("the mirror", "거울은"), g("makes us aware of", "우리가 ~을 깨닫게 하다"),
                    g("these", "이러한"), g("absences", "없음, 부재"), g("thus", "그리하여"), g("become", "~이 되다"), g("faintly", "희미하게"),
                    g("present", "선물, 현재 · 여기서는 '존재하는'이에요")],
        "slashes": ["Even so,", "makes us aware", "(c)absences,"],
        "roles": [r("the mirror", "S"), r("makes", "V"), r("us", "O"), r("aware", "C")],
        "modifiers": ["which thus become faintly present"],
        "steps": [
            choice("s6_these",
                   "these (c)absences의 these는 무엇을 가리킬까요?",
                   [("o0", "거울에 비친 것들", False), ("o1", "거울에 나타나지 않는 것들", True), ("o2", "Tolstoy의 작품들", False)],
                   "these가 가리키는 것은 앞 문장에서 찾아요. 5문장 맨 앞 There are things which …를 떠올려 봐요.",
                   why="these는 5문장의 things which do not … figure in the mirror를 받아요. 거울에 없는 것들이라 absences(부재)라고 불렀어요.",
                   highlight=["these"],
                   tips=[tip("present", "이 글에서는 → 존재하는  ('선물·현재' 아님)", "present", trap=True)],
                   point="these absences = 5문장의 '거울에 나타나지 않는 것들' (this·these는 앞 문장에서 찾는다)"),
            show("s6_present",
                 "거울은 이런 부재(absences)를 깨닫게 해 줘서, 없는 것들이 희미하게나마 존재하게 된대요. 없는 것이 오히려 느껴진다는 말이에요.",
                 highlight=["aware", "faintly present"], button="다음",
                 panel=board(L2, R6, fresh=("absences",))),
            ok_or_not("s6_check", "(c)absences",
                      "absence는 '없음, 부재'예요. 5문장의 '거울에 나타나지 않는 것들'을 한 단어로 하면 무엇일지 봐요.",
                      "these는 5문장의 '거울에 나타나지 않는 것들'이에요. 그걸 absences(부재)로 받았으니 (c)는 맞는 낱말이에요.",
                      "(c) absences: these = 5문장의 거울에 나타나지 않는 것들 → 부재 · 거울이 그걸 깨닫게 해 희미하게 존재하게 됨"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("It is as though", "마치 ~인 것 같다"), g("allows us to see", "우리가 ~을 보게 해 주다"), g("more clearly", "더 분명하게"),
                    g("what isn’t there", "그곳에 없는 것")],
        "slashes": ["It is as though", "allows us"],
        "roles": [r("It", "S"), r("is", "V"), r("it", "S"), r("allows", "V"), r("us", "O"), r("to see", "C")],
        "steps": [
            show("s7_skim", "6문장을 다시 말한 거예요. 거울 덕분에 그곳에 없는 것(what isn’t there)이 더 잘 보인대요.",
                 highlight=["what isn’t there"], button="다음 문장",
                 tips=[tip("as though", "'마치 ~인 것처럼'이에요. It is as though ~ = 마치 ~인 것 같다.")]),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "medium",
        "glosses": [g("There is also no reason", "~할 이유도 없다"), g("to assume", "가정하다"), g("what we see in the mirror", "우리가 거울 속에서 보는 것"),
                    g("must form", "반드시 이루다"), g("coherent whole", "일관된 전체")],
        "slashes": ["no reason", "to assume", "in the mirror"],
        "roles": [r("is", "V"), r("no reason", "S"), r("what we see in the mirror", "S"), r("must form", "V"), r("a coherent whole", "O")],
        "steps": [
            choice("s8_sort",
                   "거울 속 모습이 반드시 일관된 전체(coherent whole)를 이룬다고 볼 이유는 없대요. coherent whole은 어느 그룹일까요?",
                   [("o0", SORT_LEFT, True), ("o1", SORT_RIGHT, False)],
                   "no reason to assume, 그렇게 생각할 이유가 없다는 말이에요. 부정이 붙은 말은 반대 그룹이에요.",
                   why="'no reason to assume', 그렇게 볼 이유가 없대요. 부정이 붙었으니 direct reflection과 같은 반대편이에요.",
                   highlight=["no reason", "coherent whole"],
                   panel=board(L8, R6, fresh=("coherent whole",), sort=["coherent whole"]),
                   point="no reason to assume ~ = ~라고 볼 이유가 없다 → coherent whole(일관된 전체)은 반대편"),
        ],
    },
    {
        "id": 9, "text": S[8], "model_translation": KO[8], "teaching_value": "medium",
        "glosses": [g("On the contrary", "그와는 반대로"), g("may be", "~일 수도 있다"), g("in pieces", "조각조각 난"), g("discordant", "조화를 이루지 못하는")],
        "slashes": ["On the contrary,"],
        "roles": [r("it", "S"), r("may be", "V"), r("in pieces and discordant", "C")],
        "steps": [
            show("s9_pieces", "On the contrary(그와는 반대로), 거울 속 모습은 조각나 있고(in pieces) 조화롭지 않을(discordant) 수도 있대요.",
                 highlight=["On the contrary", "in pieces"], button="다음 문장",
                 panel=board(L8, R9, fresh=("in pieces", "discordant"))),
        ],
    },
    {
        "id": 10, "text": S[9], "model_translation": KO[9], "teaching_value": "high",
        "glosses": [g("The mirror", "거울은"), g("doubtless", "의심할 바 없이"), g("defective", "불완전한"), g("the outlines", "윤곽"),
                    g("will sometimes be disturbed", "때때로 흐트러질 것이다"), g("the reflection", "(비친) 상"), g("faint or confused", "희미하거나 분명치 않은"),
                    g("remarks", "말하다, 언급하다"), g("George Eliot", "George Eliot · 작가 이름"), g("in Adam Bede", "『Adam Bede』라는 책에서"),
                    g("praising", "칭찬하는"), g("the kind of", "~한 종류의"),
                    g("naive realism", "소박실재론 · 예술이 현실을 있는 그대로 보여 준다고 믿는 생각"),
                    g("holds", "잡다 · 여기서는 '~라고 믿다, 주장하다'예요"), g("art (or mirrors)", "예술(또는 거울)"), g("always", "언제나"),
                    g("tell it like it is", "있는 그대로 말하다")],
        "slashes": ["doubtless defective;", "be disturbed;", "confused’,", "in Adam Bede,", "naive realism"],
        "roles": [r("‘The mirror is doubtless defective; the outlines will sometimes be disturbed; the reflection faint or confused’", "O"),
                  r("remarks", "V"), r("George Eliot", "S")],
        "modifiers": ["which holds that art (or mirrors) always tell it like it is"],
        "steps": [
            # 정답 문장 — 그룹만 묻고 (d)가 맞는지 틀린지는 말하지 않는다. 마지막 문제에서 학생이 고른다
            choice("s10_eliot",
                   "Eliot은 거울이 불완전하고(defective), 윤곽이 흐트러지고, 상이 희미하대요. Eliot의 이 말은 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "불완전하고 흐릿한 거울이 세상을 있는 그대로 비출 수 있을지 생각해 봐요.",
                   why="불완전하고 흐릿한 거울은 그대로 비출 수 없어요. 3문장의 flaws(결함)와 같은 쪽이에요.",
                   highlight=["defective", "disturbed", "faint or confused"],
                   panel=board(L8, R9 + [("defective", "불완전한")], fresh=("defective",), sort=["defective"]),
                   tips=[tip("‘인용’, remarks + 주어", "따옴표 말 뒤에 remarks George Eliot이 왔어요. 'Eliot이 ~라고 말한다'로 읽어요.")],
                   point="Eliot의 말(defective, disturbed, faint) → 그대로 비추지 않는 쪽"),
            choice("s10_realism",
                   "naive realism은 예술(거울)이 언제나 있는 그대로 말해 준다(always tell it like it is)고 믿는 생각이래요. naive realism은 어느 그룹일까요?",
                   [("o0", SORT_LEFT, True), ("o1", SORT_RIGHT, False)],
                   "always tell it like it is는 '언제나 있는 그대로 말한다'예요. 2문장의 direct reflection을 떠올려 봐요.",
                   why="'always tell it like it is', 언제나 있는 그대로 말해 준다는 생각이에요. direct reflection과 같은 쪽이에요.",
                   highlight=["naive realism", "tell it like it is"],
                   panel=board(L8 + [("naive realism", "소박실재론")], R9 + [("defective", "불완전한")], fresh=("naive realism",), sort=["naive realism"]),
                   tips=[tip("holds", "이 글에서는 → ~라고 믿다, 주장하다  ('잡다' 아님)", "holds", trap=True),
                         tip("tell it like it is", "'있는 그대로 말하다'예요.")],
                   point="naive realism = 예술이 언제나 있는 그대로 말해 준다는 생각 → 있는 그대로 비춤 쪽"),
        ],
    },
    {
        "id": 11, "text": S[10], "model_translation": KO[10], "teaching_value": "high",
        "glosses": [g("A mirror", "거울은"), g("offers us", "우리에게 제공하다"), g("a version of reality", "현실의 한 버전"), g("does so", "그렇게 하다"),
                    g("viewpoint", "관점"), g("cannot be captured", "포착될 수 없다, 담길 수 없다"), g("in the mirror itself", "거울 그 자체에서는")],
        "slashes": ["offers us", "of reality,", "does so", "a viewpoint"],
        "roles": [r("A mirror", "S"), r("offers", "V"), r("us", "O"), r("a version of reality", "O"), r("it", "S"), r("does", "V")],
        "modifiers": ["which cannot be captured in the mirror itself"],
        "steps": [
            show("s11_view", "거울은 현실의 한 버전(a version of reality)을 보여 주지만, 그 관점(viewpoint)은 거울 안에 담길 수 없대요.",
                 highlight=["viewpoint", "cannot be captured"], button="다음 문장",
                 tips=[tip("does so", "앞의 offers us a version of reality를 다시 쓰지 않으려고 does so로 받았어요.")]),
        ],
    },
    {
        "id": 12, "text": S[11], "model_translation": KO[11], "teaching_value": "high",
        "glosses": [g("And because", "그리고 ~ 때문에"), g("this viewpoint", "이 관점"), g("invisible", "보이지 않는"), g("to us", "우리에게"),
                    g("we might be tempted to", "우리는 ~하고 싶은 유혹을 느낄지도 모른다"), g("take it as", "그것을 ~로 받아들이다"),
                    g("beyond question", "의심할 여지가 없는")],
        "slashes": ["this viewpoint", "invisible to us,", "be tempted"],
        "roles": [r("this viewpoint", "S"), r("is", "V"), r("invisible", "C"), r("we", "S"), r("might be tempted", "V")],
        "steps": [
            ok_or_not("s12_check", "(e)invisible",
                      "11문장에서 관점은 거울 안에 담길 수 없다(cannot be captured)고 했어요. 담기지 않는 관점이 우리 눈에 어떨지 봐요.",
                      "11문장의 'cannot be captured in the mirror', 거울에 담기지 않으니 우리에게 보이지 않아요. 보이지 않아서 의심 없이 받아들이기 쉽다는 뒤 말과도 이어져 (e)는 맞는 낱말이에요.",
                      "(e) invisible: 11문장 cannot be captured in the mirror = 보이지 않음 → 그래서 의심 없이 받아들이기 쉽다",
                      highlight=["invisible", "beyond question"],
                      tips=[tip("be tempted to ~", "'~하고 싶은 유혹을 느끼다'예요."), tip("beyond question", "'의심할 여지가 없는'이에요.")]),
            show("s12_go", "밑줄 다섯 개가 칠판의 어느 그룹 흐름과 맞는지 떠올리며 문제를 풀어 봐요.", button="문제 풀러 갈게요"),
        ],
    },
]

add_refers(sentences, 2, {"this mirroring": "Tolstoy’s work holds up a mirror(톨스토이 작품이 거울을 비추는 것)"})
add_refers(sentences, 3, {"they": "literary works(문학 작품)"})
add_refers(sentences, 4, {"they": "literary works(문학 작품)"})
add_refers(sentences, 7, {"it": "the mirror(거울)"})
add_refers(sentences, 9, {"it": "what we see in the mirror(거울 속에서 보는 것)"})
add_refers(sentences, 11, {"does so": "offers us a version of reality(현실의 한 버전을 보여 주다)"})
add_refers(sentences, 12, {"take it as": "it = this viewpoint(이 관점)"})

SENSES = {
    1: [sense("that", "claim that Tolstoy’s work", "~라는", "동격 that — claim의 내용"),
        sense("to", "a mirror to the Russian revolution", "~에", "hold up a mirror to ~ = ~을 비추어 보여 주다")],
    2: [sense("yet", "Yet this mirroring", "그러나", "문장 앞 Yet = 그러나"),
        sense("as", "as it stands", "~대로", "as it stands = 있는 그대로")],
    3: [sense("if", "If literary works are", "만약 ~라면", "접속사 if + 주어·동사")],
    4: [sense("as", "as significant for", "~만큼 (앞 as)", "as A as B = B만큼 A한"),
        sense("for", "for what they don’t reflect", "~ 때문에", "be significant for ~ = ~ 때문에 중요하다"),
        sense("for", "for their exclusions", "~ 때문에", "앞 for what they don’t reflect를 대시 사이에서 다시 말함"),
        sense("as", "as for what they do", "~만큼 (뒤 as)", "as A as B의 뒤 as"),
        sense("for", "as for what they do", "~ 때문에", "be significant for ~ = ~ 때문에 중요하다")],
    5: [sense("which", "things which do not", "(앞 명사를 꾸밈)", "관계대명사 which + 동사"),
        sense("which", "of which he could not be conscious", "(그것을) ~하는", "전치사 + which = 앞 contradictions를 꾸밈 (be conscious of)")],
    6: [sense("so", "Even so", "그렇다 하더라도", "Even so = 그렇다 하더라도"),
        sense("which", ", which thus become", "그리고 그것들은", "콤마 + which = 앞 absences를 받아 덧붙임")],
    7: [sense("as", "as though", "마치 ~처럼", "as though = 마치 ~인 것처럼"),
        sense("to", "allows us to see", "~하도록", "allow + 사람 + to부정사 = 사람이 ~하게 해 주다")],
    8: [sense("to", "no reason to assume", "~할 (이유)", "명사 + to부정사 = ~할 명사"),
        sense("that", "assume that what we see", "~라고", "명사절 that (assume that …)")],
    10: [sense("which", "realism which holds", "(앞 명사를 꾸밈)", "관계대명사 which + 동사"),
         sense("that", "holds that art", "~라고", "명사절 that (hold that … = ~라고 믿다)")],
    11: [sense("but", "but it does so", "하지만", "접속사 but — 앞뒤가 반대"),
         sense("so", "does so", "그렇게", "do so = 앞 동사구(offers us a version of reality)를 받음"),
         sense("which", "viewpoint which cannot", "(앞 명사를 꾸밈)", "관계대명사 which + 동사")],
    12: [sense("to", "invisible to us", "~에게", "invisible to ~ = ~에게 보이지 않는"),
         sense("to", "tempted to take", "~하고 싶은", "be tempted to + 동사원형 = ~하고 싶은 유혹을 느끼다"),
         sense("as", "take it as beyond question", "~로", "take A as B = A를 B로 받아들이다")],
}

WORDS = {
    "writing": "쓰기, 쓰는 것", "commentary": "논평", "lenin": "레닌(사람 이름)", "leo": "레오(이름)", "tolstoy": "톨스토이(작가 이름)",
    "critic": "비평가", "pierre": "피에르(이름)", "macherey": "마슈레(사람 이름)", "agrees": "동의하다", "lenin’s": "레닌의", "claim": "주장",
    "tolstoy’s": "톨스토이의", "work": "작품", "holds": "~라고 믿다", "mirror": "거울", "russian": "러시아의", "revolution": "혁명",
    "mirroring": "거울 비추기", "argues": "주장하다", "complex": "복잡한", "affair": "일", "means": "방법 · by no means = 결코 ~이 아닌",
    "direct": "직접적인", "reflection": "(비친) 상", "world": "세상", "stands": "서 있다 · as it stands = 있는 그대로", "literary": "문학의",
    "works": "작품", "sense": "의미", "mirrors": "거울", "marked": "특징지어진", "flaws": "결함", "blind": "눈이 먼, 보이지 않는",
    "spots": "곳, 지점", "fact": "사실", "significant": "중요한", "reflect": "비추다", "don’t": "~하지 않다", "exclusions": "배제",
    "distortions": "왜곡", "things": "것들", "cannot": "~할 수 없다", "figure": "나타나다", "case": "경우", "certain": "어떤, 특정한",
    "contradictions": "모순", "society": "사회", "conscious": "의식하는", "even": "~조차", "makes": "~하게 만들다", "aware": "알고 있는, 깨닫는",
    "absences": "부재", "thus": "그리하여", "become": "~이 되다", "faintly": "희미하게", "present": "존재하는", "though": "~이지만 · as though = 마치 ~처럼",
    "allows": "허락하다, ~하게 해 주다", "see": "보다", "clearly": "분명하게", "isn’t": "~이 아니다, 없다", "there": "거기에", "reason": "이유",
    "assume": "가정하다", "form": "이루다, 형성하다", "coherent": "일관된", "whole": "전체", "contrary": "반대", "pieces": "조각",
    "discordant": "조화를 이루지 못하는", "doubtless": "의심할 바 없이", "defective": "불완전한", "outlines": "윤곽", "sometimes": "때때로",
    "disturbed": "흐트러진", "faint": "희미한", "confused": "분명치 않은, 혼란스러운", "remarks": "말하다", "george": "조지(이름)",
    "eliot": "엘리엇(작가 이름)", "adam": "애덤(책 이름의 일부)", "bede": "비드(책 이름의 일부)", "praising": "칭찬하는", "kind": "종류",
    "naive": "순진한, 소박한", "realism": "실재론, 사실주의", "art": "예술", "always": "언제나", "tell": "말하다", "like": "~처럼, ~대로",
    "offers": "제공하다", "version": "버전, 판", "reality": "현실", "does": "하다", "viewpoint": "관점", "captured": "포착된, 담긴",
    "itself": "그 자체", "invisible": "보이지 않는", "might": "~일지도 모른다", "tempted": "유혹을 느끼는", "take": "받아들이다",
    "beyond": "~을 넘어선", "question": "의문, 의심", "may": "~일 수도 있다", "must": "반드시 ~하다", "also": "또한", "more": "더",
    "could": "~할 수 있었다", "will": "~할 것이다",
}

# 칠판 정리 — 2~3문장마다, 답은 말하지 않는다 (밑줄 맞고 틀림 없이 내용만)
STORIES = [
    (4, [sc("문장 1~2", "🪞", "a mirror · by no means a direct reflection", "문학은 거울이지만, 세상을 결코 그대로 비추지 않아요"),
         sc("문장 3~4", "🕳️", "flaws · what they don’t reflect", "결함이 있는 거울 — 비추지 않는 것도 똑같이 중요해요")]),
    (7, [sc("문장 5~7", "👀", "absences · what isn’t there", "거울에 안 나타나는 것이 있고, 거울은 그 빈자리를 깨닫게 해요")]),
    (10, [sc("문장 8~9", "🧩", "no coherent whole · in pieces", "거울 속 모습은 하나로 딱 맞지 않고 조각나 있을 수도 있어요"),
          sc("문장 10", "🖋️", "Eliot: defective · naive realism", "Eliot은 거울이 불완전하다고 말해요")]),
]

exam = {
    "question": "밑줄 친 (a)~(e) 중에서 문맥상 낱말의 쓰임이 적절하지 않은 것은? [3점]",
    "underline": UNDER, "sentence": 10, "analysis_first": True, "wrong_rate": 57.7, "wrong_rank": 10, "wrong_rate_source": "EBS",
    "glosses": [g("direct", "직접적인"), g("figure", "나타나다"), g("absences", "부재"), g("praising", "칭찬하는"), g("invisible", "보이지 않는")],
    "options": [
        {"id": "1", "label": "(a) direct", "keywords": ["direct"], "ko": "직접적인"},
        {"id": "2", "label": "(b) figure", "keywords": ["figure"], "ko": "나타나다"},
        {"id": "3", "label": "(c) absences", "keywords": ["absences"], "ko": "부재"},
        {"id": "4", "label": "(d) praising", "keywords": ["praising"], "ko": "칭찬하는", "correct": True},
        {"id": "5", "label": "(e) invisible", "keywords": ["invisible"], "ko": "보이지 않는"},
    ],
    "brief": exam_brief(
        "밑줄 단어마다 칠판의 어느 그룹 흐름인지 떠올려 봐요. 흐름과 안 맞는 하나를 골라요.",
        "정답이에요! Eliot은 거울이 불완전하다(defective)고 하니, 언제나 있는 그대로 말해 준다는 naive realism을 칭찬할 수 없어요. reproaching(비난하는)이 맞아요.",
        "정답은 ④ (d)예요. Eliot은 거울이 불완전하다(defective)고 하니, naive realism을 칭찬(praising)이 아니라 비난(reproaching)해야 맞아요.",
        {"1": "결코(by no means) 직접 비추는 게 아니라 복잡한 일이라는 말이라 맞아요.",
         "2": "figure는 '나타나다'예요. 거울에 나타나지 않는 것, 4문장의 '비추지 않는 것'과 같은 말이라 맞아요.",
         "3": "these absences는 5문장의 '거울에 나타나지 않는 것들'이에요. 거울이 그 부재를 깨닫게 해 준다는 말이라 맞아요.",
         "5": "관점이 거울 안에 담길 수 없으니(cannot be captured) 우리에게 보이지 않아요. 그래서 의심 없이 받아들이기 쉽다는 흐름이라 맞아요."},
        {"3": review(24.8,
                     "absences(부재)와 present(존재하는)가 한 문장에 있어서 어색해 보여요. 하지만 these absences는 5문장의 '거울에 나타나지 않는 것들'이에요. "
                     "거울이 그 빈자리를 깨닫게 해 줘서, 없는 것이 희미하게나마 존재하게 된다는 말이에요.",
                     panel=rows(("5문장", "things which do not … figure in the mirror", "거울에 나타나지 않는 것들", "hl"),
                                ("6문장", "these (c)absences, which thus become faintly present", "그 부재를 깨닫게 됨 → 희미하게 존재", "hl"),
                                ("7문장", "what isn’t there", "그곳에 없는 것이 더 잘 보임", "hl")),
                     rank_word="가장 많이 고른"),
         "5": review(21.9,
                     "invisible(보이지 않는)이 거울 이야기와 안 맞아 보일 수 있어요. 하지만 11문장에서 관점은 거울 안에 담길 수 없대요(cannot be captured). "
                     "보이지 않으니 의심 없이 받아들이기 쉽다는 흐름이라 맞아요.",
                     panel=rows(("11문장", "a viewpoint which cannot be captured in the mirror itself", "거울 안에 담길 수 없는 관점", "hl"),
                                ("12문장", "this viewpoint is (e)invisible to us", "그래서 우리에게 보이지 않음 → 의심 없이 받아들임", "hl")))}),
}

lesson = base_lesson(
    ID, source="2026년 3월 고3 전국연합학력평가 영어 41~42번 중 42번 (문맥상 낱말의 쓰임, 3점)",
    topic="어휘 문제 푸는 법: 요지 → 두 그룹(있는 그대로 비춤 ↔ 그대로 비추지 않음) → 밑줄 단어가 흐름에 맞는지",
    method={"type": "word_in_context", "labels": ["요지 잡기", "두 그룹으로 나누기", "밑줄 단어 맞춰 보기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-literary-mirror.svg", ("Literature", "문학"), "=", ("Mirror", "거울"),
                                       "문학이라는 거울에는 무엇이 비칠까?", "2026년 3월 41~42번 도입 칠판"),
                      "alt": "칠판: Literature(문학) = Mirror(거울)", "kind": "drawing"},
            "method": METHOD_IMAGES["vocab"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "문학 작품이 세상을 비추는 거울이라면, 그 거울엔 무엇이 비칠까요? 이번 글은 문학이라는 거울을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "어휘 문제는 단어 뜻만 보면 다 맞아 보여요. 문장마다 흐름을 잡아야 틀린 단어가 보여요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "요지를 잡고, 단어를 두 그룹으로 나눈 뒤, 밑줄 단어가 흐름에 맞는지 볼 거예요. 칠판 순서대로 해 볼게요."}}],
    exam=exam,
    # coherent, discordant, defective는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
    key_words={"passage": [g("commentary", "논평"), g("claim", "주장"), g("hold up a mirror to", "~을 비추어 보여 주다"), g("affair", "일"),
                           g("by no means", "결코 ~이 아닌"), g("reflection", "(비친) 상"), g("flaw", "결함"), g("blind spot", "사각지대"),
                           g("significant", "중요한"), g("exclusion", "배제"), g("distortion", "왜곡"), g("figure", "나타나다"),
                           g("contradiction", "모순"), g("absence", "부재"), g("faintly", "희미하게"), g("outline", "윤곽"),
                           g("disturb", "흐트러뜨리다"), g("naive realism", "소박실재론"), g("viewpoint", "관점"), g("capture", "포착하다"),
                           g("be tempted to", "~하고 싶은 유혹을 느끼다"), g("beyond question", "의심할 여지가 없는")],
               "options": [g("direct", "직접적인"), g("praise", "칭찬하다"), g("reproach", "비난하다"), g("invisible", "보이지 않는")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="어휘 문제 푸는 법")
