"""2026년 6월 모의평가(2027학년도, 평가원) 42번 레슨 + 대사를 만든다 (41~42 장문 중 42번 — 문맥상 낱말의 쓰임, 3점). 오답률 45% · Top 10 (메가스터디).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_42.py   (→ npm run policy:copy stamp <id> → npm run build)

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- 두 그룹 이름: 왼쪽 「Clear and perfect 쪽 (깔끔)」 ↔ 오른쪽 「a mess 쪽 (엉망)」 — 둘 다 1~2문장에 나온 말. 칠판은 둘이 다 나온 2문장에서 처음 연다
  (random ball-pit → 엉망, 9문장 struggle to comprehend → 엉망, 10문장 obey most molecular laws → 깔끔)
- 정답 ⑤ (e)obey(→ defy): 10문장에서는 「1~9문장에서 유리는 어느 쪽?」「obey most molecular laws는 어느 쪽?」만 묻고 맞다/틀리다는 말하지 않는다
- (a)(b)(c)(d)는 「그럼 (x)는 문맥에 맞을까요, 틀릴까요?」로 학생이 고른다(README §0-1)
- (a)(c)는 「고체 ↔ 액체」 흐름이라 그룹 지도 대신 문장 질문으로 짚었다: 4문장 the latter(후자) = solid → 5문장 never behaves as a liquid →
  6문장 not because … sinking → 7문장 진짜 이유(애초에 불어서 만들고 굳혀서)
- 많이 고른 오답 ③ (c)solidified 26% — 「유리는 오래 흘러내린다」는 생각과 안 맞아 보여서. 7문장 s7_reason + review로 짚었다
- 헷갈리는 단어(trap): term(용어), practice(in practice 실제로는), sheets(판), blown(불어서 만들다), put(말하다), state(상태) — 해설 번역과 대조함
- misshapen = 해설 「보기 흉한」, solidify = 「응고시키다」, paradox = 「역설」, given = 「고려하면」, the chances are = 「아마」, in the first place = 「애초에」 — 해설과 대조함
- molecular·amorphous·viscous는 시험지 아래 * 풀이 단어 — 핵심어(key_words)에서 뺐다. 다만 obey most molecular laws는 정답 단서라 칠판에는 썼다
- 평가 뒤집기(+/−)는 넣지 않았다 — 글쓴이가 유리를 좋게/나쁘게 평가하는 글이 아님
- 해석 맞추기(add_match)는 넣지 않았다. S·V 찾기 스텝은 만들지 않았다(2026-10-20 삭제), 끊어읽기 roles·slashes·modifiers만
- 4문장 두 번째 절(in practice it’s really the latter)·11문장 두 번째 절(it’s a state)은 it이 앞에도 나와 끊어읽기 S·V 표시를 붙이지 않았다
- 41번(제목)은 만들지 않았다 (Top 10 밖)
반영한 규칙: README §0-1(2026-10-20~21), vocab.md v1, 칠판은 읽은 데까지만·화면마다 X, 대사 핵심만, 칭찬 분리(엔진), 화면 중계 말 없음.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, sc, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)
from beginner import add_refers  # noqa: E402

ID = "mopyeong-2027-06-42-glass-state"

S = [
    "The structure of glass is, frankly, a bit of a mess.",
    "Clear and perfect as it might appear to our eyes, down at the molecular level, glass looks more like a random ball-pit of atoms.",
    "The technical term for this mess depends on who you’re asking: for some scientists it is an “amorphous solid,” for others a "
    "“supercooled liquid.”",
    "In theory it’s both liquid and solid, though, given the way it behaves, in practice it’s really the latter.",
    "In fact, at room temperature glass never behaves as a (a)liquid, even an imperceptibly viscous one, even over long periods of time "
    "(though it can “sweat” if you don’t add enough lime to the mix).",
    "Those (b)misshapen sheets of glass you sometimes see in old stained-glass windows, thicker at the bottom than the top, are generally "
    "not that way because the glass is slowly sinking over time.",
    "Unless the church has endured temperatures of more than 400˚C, the chances are they are uneven because that’s the way they were "
    "blown and (c)solidified in the first place.",
    "Flat glass was only developed in the nineteenth century and we had to wait until the middle of the twentieth century for truly "
    "flat, thin sheets of glass.",
    "The (d)paradox is that, despite it being one of the very oldest human-made substances, scientists still struggle to comprehend why "
    "glass behaves the way it does.",
    "Glass seems to (e)obey most molecular laws.",
    "As one glassmaker put it, glass is not a material; it’s a state.",
]
# 해설지 번역 (10문장의 obey는 해설대로 정답 낱말 defy로 옮긴 번역 — 「따르는(→ 거부하는)」)
KO = [
    "유리의 구조는, 솔직히 말해서, 다소 엉망진창이다.",
    "우리 눈에는 투명하고 완벽해 보일지 몰라도, 분자 수준으로 내려가 보면, 유리는 원자들이 마구잡이로 있는 볼풀에 더 가까워 보인다.",
    "이러한 엉망진창인 상태를 뜻하는 전문 용어는 여러분이 누구에게 묻고 있느냐에 따라 달라지는데, 어떤 과학자들에게는 그것이 '무정형의 고체'이고, 다른 이들에게는 '과냉각 액체'이다.",
    "이론적으로 그것은 액체이면서 동시에 고체이지만, 그것이 작용하는 방식을 고려하면 실제로는 후자(고체)이다.",
    "사실, 상온에서 유리는, 심지어 (알아차릴 수 없을 정도로) 미세하게 점성이 있는 것이라 해도, 심지어 오랜 시간이 지나더라도, 결코 액체처럼 행동하지 않는다(비록 혼합물에 석회를 충분히 넣지 않으면 유리가 '땀을 흘릴' 수는 있지만).",
    "여러분이 오래된 스테인드글라스 창문에서 가끔 보는, 윗부분보다 아랫부분이 더 두꺼운 보기 흉한 유리판들은 대개 시간이 지나면서 유리가 천천히 아래로 가라앉고 있기 때문에 그렇게 된 것이 아니다.",
    "교회가 400°C가 넘는 온도를 견뎌낸 것이 아니라면, 아마 그것들이 애초에 그런 방식으로 불어서 만들어지고 응고되었기 때문에 고르지 않은 것이다.",
    "판유리는 19세기가 되어서야 겨우 개발되었고, 정말로 평평하고 얇은 유리판을 얻기 위해서는 20세기 중반까지 기다려야 했다.",
    "역설은 유리가 인간이 만든 가장 오래된 물질 중 하나임에도 불구하고, 과학자들은 유리가 왜 그런 방식으로 작용하는지 이해하는 데 여전히 애를 먹고 있다는 점이다.",
    "유리는 대부분의 분자 법칙을 따르는(→ 거부하는) 것처럼 보인다.",
    "한 유리 제조업자가 말했듯이, 유리는 재료가 아니라 상태이다.",
]
UNDER = ["(a)liquid", "(b)misshapen", "(c)solidified", "(d)paradox", "(e)obey"]

# 두 그룹 — 이름은 1~2문장에서 나온 말로만 (칠판엔 읽은 데까지만)
LEFT = "Clear and perfect 쪽 (깔끔)"
RIGHT = "a mess 쪽 (엉망)"
SORT_LEFT = "왼쪽 · Clear and perfect (깔끔)"
SORT_RIGHT = "오른쪽 · a mess (엉망)"


def board(left, right, fresh=(), sort=None):
    """단어 지도. sort = 학생이 끌어 넣을 말 — 맞는 쪽에 fresh로 넣어 두면 답하기 전엔 숨고 맞히면 붙는다"""
    return groups("유리의 정체", LEFT, left, RIGHT, right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": SORT_LEFT, "right": SORT_RIGHT} if sort else None)


def ok_or_not(id, under, hint, why, point, **extra):
    """정답이 아닌 밑줄 — 알려 주지 않고 학생이 「맞을까요, 틀릴까요?」로 고른다 (README §0-1)"""
    return choice(id, f"그럼 {under}는 문맥에 맞을까요, 틀릴까요?",
                  [("o0", "문맥에 맞아요", True), ("o1", "문맥에 안 맞아요", False)],
                  hint, why=why, point=point, **extra)


L2 = [("Clear and perfect", "투명하고 완벽한")]
R2 = [("a mess", "엉망")]
R2B = R2 + [("random ball-pit", "마구잡이 볼풀")]
R9 = R2B + [("struggle to comprehend", "이해하는 데 애를 먹음")]
L10 = L2 + [("obey most molecular laws", "대부분의 분자 법칙을 따름")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("The structure of glass", "유리의 구조"), g("structure", "구조"), g("glass", "유리"), g("frankly", "솔직히"),
                    g("a bit of a mess", "다소 엉망"), g("mess", "엉망")],
        "slashes": ["The structure of glass", "frankly,"],
        "roles": [r("The structure of glass", "S"), r("is", "V"), r("a bit of a mess", "C")],
        "emphasis": ["a bit of a mess"],
        "steps": [
            show("s1_mess", "유리의 구조는 솔직히(frankly) 좀 엉망(a mess)이래요. 이 글의 요지가 여기서 시작해요.",
                 highlight=["mess"], button="다음 문장",
                 tips=[tip("a bit of a ~", "'다소 ~한 것'이에요. a bit of a mess = 다소 엉망.", "a bit of")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Clear and perfect", "투명하고 완벽한"), g("clear", "투명한, 분명한"), g("perfect", "완벽한"),
                    g("as it might appear", "~해 보일지 몰라도"), g("appear", "~처럼 보이다"), g("to our eyes", "우리 눈에"),
                    g("down at the molecular level", "분자 수준으로 내려가 보면"), g("molecular", "분자의 (*풀이 단어)"), g("level", "수준"),
                    g("looks more like", "~에 더 가까워 보인다"), g("random", "마구잡이의"), g("ball-pit", "볼풀 · 공이 가득 찬 놀이 풀"),
                    g("atoms", "원자")],
        "slashes": ["Clear and perfect", "to our eyes,", "molecular level,", "more like"],
        "roles": [r("it", "S"), r("might appear", "V"), r("glass", "S"), r("looks", "V"), r("more like a random ball-pit of atoms", "C")],
        "emphasis": ["Clear and perfect", "random"],
        "steps": [
            choice("s2_as",
                   "Clear and perfect as it might appear to our eyes는 무슨 뜻일까요?",
                   [("o0", "우리 눈에는 투명하고 완벽해 보일지 몰라도", True), ("o1", "우리 눈에 투명하고 완벽해 보이기 때문에", False),
                    ("o2", "우리 눈처럼 투명하고 완벽하게", False)],
                   "형용사가 맨 앞에 나오고 as + 주어 + 동사가 이어져요. 콤마(,) 뒤 내용(볼풀 같다)과 어떻게 이어지는지 봐요.",
                   why="형용사 + as + 주어 + 동사는 '비록 ~이지만'이에요. 겉으로는 깔끔해 보여도, 분자 수준에선 마구잡이 볼풀 같대요.",
                   highlight=["Clear and perfect", "as it might appear"],
                   tips=[tip("형용사 + as + 주어 + 동사", "'비록 ~이지만'이에요. Clear and perfect as it might appear = 투명하고 완벽해 보일지 몰라도.", "as it might")],
                   point="Clear and perfect as it might appear = 투명하고 완벽해 보일지 몰라도 (양보의 as)"),
            show("s2_board", "겉보기(Clear and perfect)와 1문장의 a mess를 두 그룹으로 나눠 봐요.\n유리의 구조는 오른쪽, 엉망이에요.",
                 button="다음", panel=board(L2, R2, fresh=("Clear and perfect", "a mess"))),
            choice("s2_sort",
                   "random ball-pit of atoms(원자들의 마구잡이 볼풀)는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "random은 '마구잡이의'예요. 깔끔하게 정돈된 모습일지 생각해 봐요.",
                   why="원자들이 마구잡이로 섞인 볼풀은 정돈된 모습이 아니에요. 1문장의 a mess와 같은 쪽이에요.",
                   highlight=["random"],
                   panel=board(L2, R2B, fresh=("random ball-pit",), sort=["random ball-pit"]),
                   point="random ball-pit(마구잡이 볼풀) → a mess(엉망) 쪽"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("The technical term", "전문 용어"), g("technical", "전문적인"), g("term", "기간, 학기 · 여기서는 '용어'"),
                    g("for this mess", "이 엉망인 상태에 대한"), g("depends on", "~에 따라 달라진다"), g("who you’re asking", "누구에게 묻느냐"),
                    g("for some scientists", "어떤 과학자들에게는"), g("amorphous", "무정형의 (*풀이 단어)"), g("solid", "고체"),
                    g("for others", "다른 이들에게는"), g("supercooled", "과냉각된"), g("liquid", "액체")],
        "slashes": ["The technical term", "for this mess", "depends on", "you’re asking:", "for some scientists", "“amorphous solid,”"],
        "roles": [r("The technical term for this mess", "S"), r("depends", "V"), r("it", "S"), r("is", "V"), r("an “amorphous solid", "C")],
        "steps": [
            choice("s3_term",
                   "과학자들은 이 엉망인 상태(this mess)를 뭐라고 부를까요?",
                   [("o0", "어떤 이는 고체, 어떤 이는 액체라고 부른다", True), ("o1", "모두 고체라고 부른다", False),
                    ("o2", "모두 액체라고 부른다", False)],
                   "for some scientists ~, for others ~는 '어떤 과학자에게는 ~, 다른 이들에게는 ~'예요.",
                   why="'amorphous solid'(무정형의 고체)라고도, 'supercooled liquid'(과냉각 액체)라고도 불러요. 묻는 사람에 따라 이름이 달라요.",
                   highlight=["solid", "liquid"],
                   tips=[tip("depend on who ~", "'누구에게 ~하느냐에 따라 달라지다'예요.", "depends on"),
                         tip("term", "이 글에서는 → 용어  ('기간·학기' 아님)", "term", trap=True)],
                   point="같은 유리를 어떤 과학자는 고체(solid), 어떤 과학자는 액체(liquid)라고 부른다"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("In theory", "이론상으로는"), g("theory", "이론"), g("it’s", "그것은 ~이다"), g("both liquid and solid", "액체이면서 고체"),
                    g("though", "하지만 · 문장 가운데 though"), g("given the way it behaves", "그것이 작용하는 방식을 고려하면"),
                    g("given", "~을 고려하면"), g("behaves", "작용하다, 행동하다"), g("in practice", "실제로는"),
                    g("practice", "연습 · in practice = 실제로는"), g("really", "정말로"), g("the latter", "후자 · 둘 중 뒤의 것")],
        "slashes": ["In theory", "both liquid and solid,", "though,", "the way it behaves,", "in practice"],
        "roles": [r("it", "S"), r("’s", "V"), r("both liquid and solid", "C")],
        "emphasis": ["In theory", "in practice", "the latter"],
        "steps": [
            choice("s4_latter",
                   "이론상(In theory) 유리는 액체이면서 고체래요. 실제로는(in practice) 그중 the latter(후자)라는데, 무엇일까요?",
                   [("o0", "solid (고체)", True), ("o1", "liquid (액체)", False), ("o2", "둘 다", False)],
                   "the latter는 '후자', 앞에 나온 둘 중 뒤의 것이에요. both liquid and solid의 순서를 봐요.",
                   why="both liquid and solid에서 뒤에 나온 건 solid예요. 실제로 작용하는 걸 보면 고체래요.",
                   highlight=["both liquid and solid", "the latter"],
                   tips=[tip("the former / the latter", "'전자 / 후자'예요. 앞에 나온 둘 중 앞의 것과 뒤의 것이에요.", "the latter"),
                         tip("given ~", "'~을 고려하면'이에요. given the way it behaves = 그것이 작용하는 방식을 고려하면.", "given"),
                         tip("practice", "이 글에서는 → in practice = 실제로는  ('연습' 아님)", "practice", trap=True)],
                   point="In theory 액체 + 고체 ↔ in practice the latter = 고체"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("In fact", "사실"), g("at room temperature", "상온에서"), g("temperature", "온도"),
                    g("never behaves as", "결코 ~처럼 행동하지 않는다"), g("never", "결코 ~ 않다"), g("liquid", "액체"),
                    g("even an imperceptibly viscous one", "알아차릴 수 없을 만큼 조금 들러붙는 것이라 해도"),
                    g("imperceptibly", "알아차릴 수 없을 정도로"), g("viscous", "들러붙는 (*풀이 단어)"),
                    g("even over long periods of time", "심지어 오랜 시간이 지나도"), g("periods", "기간"), g("sweat", "땀을 흘리다"),
                    g("if you don’t add", "~을 넣지 않으면"), g("enough lime", "충분한 석회"), g("lime", "석회"), g("the mix", "혼합물")],
        "slashes": ["In fact,", "at room temperature", "a (a)liquid,", "viscous one,", "periods of time", "“sweat”"],
        "roles": [r("glass", "S"), r("behaves", "V")],
        "emphasis": ["never"],
        "steps": [
            ok_or_not("s5_check", "(a)liquid",
                      "4문장에서 실제로는 후자, 고체라고 했어요. 상온에서 결코(never) 액체처럼 행동하지 않는다는 말이 그 흐름과 이어지는지 봐요.",
                      "실제로는 고체니까, 상온에서 아무리 오래 지나도 결코 액체처럼 행동하지 않는다는 말이 이어져요. (a)liquid는 맞는 낱말이에요.",
                      "(a) liquid: 실제로는 고체 → never behaves as a liquid (결코 액체처럼 행동하지 않음)",
                      highlight=["never", "liquid"],
                      faded=["(though it can “sweat” if you don’t add enough lime to the mix)"],
                      tips=[tip("never ~, even …, even …", "'심지어 ~라도, 심지어 ~해도 결코 ~ 않다'예요. even을 겹쳐 never를 더 세게 말해요.", "even")]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("misshapen", "보기 흉한, 모양이 일그러진"), g("sheets of glass", "유리판"), g("sheets", "시트 · 여기서는 '판'"),
                    g("you sometimes see", "여러분이 가끔 보는"), g("in old stained-glass windows", "오래된 스테인드글라스 창문에서"),
                    g("stained-glass", "스테인드글라스"), g("windows", "창문"),
                    g("thicker at the bottom than the top", "윗부분보다 아랫부분이 더 두꺼운"), g("thicker", "더 두꺼운"),
                    g("bottom", "아랫부분"), g("top", "윗부분"), g("are generally not that way", "대개 그렇게 된 것이 아니다"),
                    g("generally", "대개"), g("because the glass is slowly sinking", "유리가 천천히 가라앉고 있기 때문에"),
                    g("slowly", "천천히"), g("sinking", "가라앉는"), g("over time", "시간이 지나면서")],
        "slashes": ["sheets of glass", "stained-glass windows,", "than the top,", "not that way", "slowly sinking"],
        "roles": [r("Those (b)misshapen sheets of glass", "S"), r("are", "V"), r("that way", "C"), r("the glass", "S"),
                  r("is slowly sinking", "V")],
        "modifiers": ["you sometimes see in old stained-glass windows", "thicker at the bottom than the top"],
        "steps": [
            choice("s6_why",
                   "아래가 더 두꺼운 오래된 유리판, 유리가 천천히 가라앉아서(sinking) 그렇게 된 걸까요?",
                   [("o0", "가라앉아서 그런 게 아니다", True), ("o1", "천천히 가라앉아서 그렇다", False)],
                   "are generally not that way because ~를 봐요. not이 붙어서 '~ 때문에 그런 게 아니다'예요.",
                   why="'are generally not that way because the glass is slowly sinking', not이 붙어서 '가라앉고 있기 때문에 그렇게 된 게 아니다'예요. 유리는 흐르지 않으니까요.",
                   highlight=["not", "sinking"],
                   tips=[tip("not ~ because …", "'… 때문에 ~한 것이 아니다'예요. not이 because 덩어리까지 부정해요.", "not that way"),
                         tip("sheets", "이 글에서는 → (유리)판  ('시트·종이' 아님)", "sheets", trap=True)],
                   point="아래가 두꺼운 유리판 ≠ 유리가 흘러내려서 (not … because … sinking)"),
            ok_or_not("s6_check", "(b)misshapen",
                      "thicker at the bottom than the top(윗부분보다 아랫부분이 더 두꺼운)을 봐요. 이런 유리판의 모양이 어떨지 봐요.",
                      "위아래 두께가 다르니 모양이 고르지 않아요. misshapen(보기 흉한, 일그러진)은 맞는 낱말이에요.",
                      "(b) misshapen: thicker at the bottom than the top → 모양이 일그러진 유리판",
                      highlight=["misshapen", "thicker"]),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("Unless", "~하지 않는 한"), g("the church", "교회"), g("has endured", "견뎌 왔다"), g("endured", "견뎠다"),
                    g("temperatures of more than 400˚C", "400℃가 넘는 온도"), g("temperatures", "온도"),
                    g("the chances are", "아마 ~일 것이다"), g("chances", "가능성"), g("uneven", "고르지 않은"),
                    g("that’s the way", "그것이 ~한 방식이다"), g("were blown", "불어서 만들어졌다"), g("blown", "(유리를) 불어서 만든"),
                    g("solidified", "응고된, 굳은"), g("in the first place", "애초에")],
        "slashes": ["Unless the church", "more than 400˚C,", "the chances are", "are uneven", "the way", "were blown"],
        "roles": [r("the church", "S"), r("has endured", "V"), r("the chances", "S"), r("are … are", "V"), r("they", "S"),
                  r("uneven", "C"), r("that", "S"), r("’s", "V"), r("the way", "C")],
        "modifiers": ["they were blown and (c)solidified in the first place"],
        "emphasis": ["uneven", "in the first place"],
        "steps": [
            choice("s7_reason",
                   "그럼 유리판이 고르지 않은(uneven) 진짜 이유는 무엇일까요?",
                   [("o0", "애초에 불어서 만들고 굳힐 때 그렇게 돼서", True), ("o1", "오랜 시간 천천히 흘러내려서", False),
                    ("o2", "교회가 400℃ 넘게 뜨거워서", False)],
                   "because 뒤 that’s the way they were blown and solidified를 봐요. in the first place는 '애초에'예요.",
                   why="'that’s the way they were blown and solidified in the first place', 처음 만들 때부터 그렇게 불어서 만들고 굳혔기 때문이래요. Unless는 '~하지 않는 한'이라 400℃는 이유가 아니에요.",
                   highlight=["uneven", "in the first place"],
                   tips=[tip("Unless ~", "'~하지 않는 한'이에요. 교회가 400℃ 넘는 열을 견딘 게 아니라면, 이라는 말이에요.", "Unless"),
                         tip("the chances are (that) ~", "'아마 ~일 것이다'예요.", "the chances are"),
                         tip("blown", "이 글에서는 → (유리를) 불어서 만든  ('바람에 날린' 아님)", "blown", trap=True)],
                   point="고르지 않은 진짜 이유 = 애초에(in the first place) 불어서 만들고 굳힐 때부터 (흘러내린 게 아님)"),
            ok_or_not("s7_check", "(c)solidified",
                      "6문장에서 유리가 흘러내린 게 아니라고 했어요. 처음 불어서 만든 유리가 어떻게 됐을지 봐요.",
                      "불어서 모양을 만든 다음 굳혀서(solidified) 처음부터 고르지 않았던 거예요. 흘러내린 게 아니라는 6문장과 이어져 (c)는 맞는 낱말이에요.",
                      "(c) solidified: 애초에 불어서 만들고 굳혀서 고르지 않음 → 흘러내린 게 아님(6문장)과 이어짐",
                      highlight=["solidified"]),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "low",
        "glosses": [g("Flat glass", "판유리"), g("flat", "평평한"), g("was only developed", "~에야 겨우 개발되었다"), g("developed", "개발된"),
                    g("in the nineteenth century", "19세기에"), g("nineteenth", "19번째의"), g("century", "세기"),
                    g("had to wait until", "~까지 기다려야 했다"), g("wait", "기다리다"), g("the middle of the twentieth century", "20세기 중반"),
                    g("middle", "중간"), g("twentieth", "20번째의"), g("truly", "정말로"), g("thin", "얇은")],
        "slashes": ["only developed", "nineteenth century", "had to wait", "twentieth century"],
        "roles": [r("Flat glass", "S"), r("was … developed", "V"), r("we", "S"), r("had to wait", "V")],
        "steps": [
            show("s8_skim", "판유리(flat glass)는 19세기에야 만들어졌대요. 유리 만드는 역사 이야기라 가볍게 넘어가요.",
                 shaded=[S[7]], button="다음 문장",
                 tips=[tip("only + 때", "'~에야 겨우'예요. was only developed in the nineteenth century = 19세기에야 겨우 개발되었다.", "only developed")]),
        ],
    },
    {
        "id": 9, "text": S[8], "model_translation": KO[8], "teaching_value": "high",
        "glosses": [g("paradox", "역설"), g("despite", "~에도 불구하고"), g("it being one of", "그것이 ~ 중 하나라는 것"),
                    g("the very oldest human-made substances", "인간이 만든 가장 오래된 물질"), g("oldest", "가장 오래된"),
                    g("human-made", "인간이 만든"), g("substances", "물질"), g("scientists", "과학자들"),
                    g("still struggle to comprehend", "여전히 이해하는 데 애를 먹는다"), g("struggle", "애쓰다, 애를 먹다"),
                    g("comprehend", "이해하다"), g("why glass behaves the way it does", "유리가 왜 그런 방식으로 작용하는지"), g("behaves", "작용하다")],
        "slashes": ["The (d)paradox is", "that,", "human-made substances,", "struggle to comprehend"],
        "roles": [r("The (d)paradox", "S"), r("is", "V"), r("scientists", "S"), r("struggle", "V")],
        "emphasis": ["despite", "struggle"],
        "steps": [
            choice("s9_mean",
                   "despite(~에도 불구하고) 앞뒤를 보면, 유리에 대해 무엇이 이상할까요?",
                   [("o0", "가장 오래된 물질인데도 아직 잘 이해하지 못한다", True), ("o1", "가장 새로운 물질이라 아직 모른다", False),
                    ("o2", "오래된 물질이라 이제 다 이해했다", False)],
                   "despite 뒤 one of the very oldest(가장 오래된 것 중 하나)와 still struggle to comprehend를 같이 봐요.",
                   why="'one of the very oldest human-made substances', 아주 오래된 물질인데 'still struggle to comprehend', 과학자들이 여전히 이해하는 데 애를 먹는대요.",
                   highlight=["oldest", "struggle to comprehend"],
                   tips=[tip("despite + 명사(-ing)", "'~에도 불구하고'예요. despite it being ~ = 그것이 ~임에도 불구하고.", "despite")],
                   point="아주 오래된 물질 ↔ 아직도 이해 못 함 (despite로 맞섬)"),
            ok_or_not("s9_check", "(d)paradox",
                      "paradox는 '역설'이에요. 서로 안 맞는 두 사실이 함께 있을 때 써요.",
                      "아주 오래된 물질인데 아직도 이해하지 못한다는, 서로 안 맞는 두 사실이에요. (d)paradox는 맞는 낱말이에요.",
                      "(d) paradox: 가장 오래된 물질 ↔ 아직 이해 못 함 → 역설",
                      highlight=["paradox"]),
            choice("s9_sort",
                   "struggle to comprehend(이해하는 데 애를 먹다)는 어느 그룹일까요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "깔끔하게 정돈된 것이라면 이해하기 어려울지 생각해 봐요.",
                   why="과학자들도 이해하기 어려울 만큼 정체가 뒤죽박죽이라는 말이에요. 1문장의 a mess와 같은 쪽이에요.",
                   highlight=["struggle to comprehend"],
                   panel=board(L2, R9, fresh=("struggle to comprehend",), sort=["struggle to comprehend"]),
                   point="struggle to comprehend → a mess(엉망) 쪽"),
        ],
    },
    {
        "id": 10, "text": S[9], "model_translation": KO[9], "teaching_value": "high",
        "glosses": [g("Glass", "유리"), g("seems to", "~하는 것 같다"), g("obey", "따르다"), g("most molecular laws", "대부분의 분자 법칙"),
                    g("molecular", "분자의 (*풀이 단어)"), g("laws", "법칙")],
        "roles": [r("Glass", "S"), r("seems", "V"), r("to (e)obey most molecular laws", "C")],
        "steps": [
            # 정답 문장 — 그룹만 묻고 (e)가 맞는지 틀린지는 말하지 않는다. 마지막 문제에서 학생이 고른다
            choice("s10_glass",
                   "1~9문장에서 유리는 칠판 어느 그룹이었나요?",
                   [("o0", SORT_LEFT, False), ("o1", SORT_RIGHT, True)],
                   "1문장 a mess, 2문장 random ball-pit, 9문장 struggle to comprehend를 떠올려 봐요.",
                   why="엉망인 구조, 마구잡이 볼풀, 과학자도 이해 못 함이 모두 유리 이야기였어요.",
                   panel=board(L2, R9),
                   point="1~9문장의 유리 = a mess(엉망) 쪽"),
            choice("s10_obey",
                   "obey most molecular laws(대부분의 분자 법칙을 따른다)는 어느 그룹 말일까요?",
                   [("o0", SORT_LEFT, True), ("o1", SORT_RIGHT, False)],
                   "법칙을 그대로 따르면 깔끔하게 설명될지, 뒤죽박죽일지 생각해 봐요.",
                   why="법칙을 그대로 따르면 정돈되어 깔끔하게 설명돼요. 엉망 쪽이 아니에요.",
                   highlight=["obey"],
                   panel=board(L10, R9, fresh=("obey most molecular laws",), sort=["obey most molecular laws"]),
                   point="obey most molecular laws → Clear and perfect(깔끔) 쪽"),
        ],
    },
    {
        "id": 11, "text": S[10], "model_translation": KO[10], "teaching_value": "medium",
        "glosses": [g("As one glassmaker put it", "한 유리 제조업자가 말했듯이"), g("glassmaker", "유리 제조업자"),
                    g("put", "놓다 · 여기서는 '말하다'"), g("glass", "유리"), g("material", "재료"), g("it’s", "그것은 ~이다"), g("state", "상태")],
        "slashes": ["As one glassmaker put it,", "not a material;"],
        "roles": [r("one glassmaker", "S"), r("put", "V"), r("glass", "S"), r("is", "V"), r("not a material", "C")],
        "steps": [
            show("s11_go", "유리는 재료(material)가 아니라 상태(state)래요.\n밑줄 다섯 개가 칠판의 어느 그룹 흐름과 맞는지 떠올리며 문제를 풀어 봐요.",
                 highlight=["state"], button="문제 풀러 갈게요",
                 tips=[tip("put", "이 글에서는 → As ~ put it = ~가 말했듯이  ('놓다' 아님)", "put", trap=True),
                       tip("state", "이 글에서는 → 상태  ('주(州)·말하다' 아님)", "state", trap=True)]),
        ],
    },
]

add_refers(sentences, 3, {"for this mess": "this mess = 유리의 엉망인 구조(1~2문장)"})
add_refers(sentences, 9, {"it being one of": "it = glass(유리)"})

SENSES = {
    2: [sense("as", "Clear and perfect as it might appear", "비록 ~이지만", "형용사 + as + 주어 + 동사 = 비록 ~이지만 (양보)"),
        sense("to", "appear to our eyes", "~에게", "appear to ~ = ~에게 ~해 보이다")],
    3: [sense("for", "term for this mess", "~에 대한, ~을 뜻하는", "명사 + for ~ = ~에 대한 명사"),
        sense("for", "for some scientists", "~에게는", "for + 사람 = ~에게는"),
        sense("for", "for others", "~에게는", "for some ~, for others ~ = 어떤 이에게는 ~, 다른 이에게는 ~")],
    5: [sense("as", "behaves as a (a)liquid", "~처럼, ~로서", "behave as ~ = ~처럼 행동하다"),
        sense("if", "if you don’t add", "만약 ~라면", "접속사 if + 주어·동사"),
        sense("to", "add enough lime to the mix", "~에", "add A to B = A를 B에 넣다")],
    6: [sense("that", "not that way", "그렇게 (그런)", "지시형용사 that + 명사 = 그 ~ (that way = 그렇게)")],
    7: [sense("that", "that’s the way", "그것", "지시대명사 that (= 그것이 ~한 방식이다)")],
    8: [sense("to", "had to wait", "~해야 (했다)", "have to + 동사원형 = ~해야 한다"),
        sense("for", "for truly flat, thin sheets", "~을 (얻으려고)", "wait for ~ = ~을 기다리다")],
    9: [sense("that", "The (d)paradox is that", "~라는 것", "명사절 that — be동사 뒤 보어 (역설은 ~라는 것이다)"),
        sense("to", "struggle to comprehend", "~하는 데", "struggle to + 동사원형 = ~하는 데 애를 먹다")],
    10: [sense("to", "seems to (e)obey", "~하는 것 (같다)", "seem to + 동사원형 = ~하는 것 같다")],
    11: [sense("as", "As one glassmaker put it", "~대로, ~듯이", "As + 주어 + put it = ~가 말했듯이")],
}

WORDS = {
    "structure": "구조", "glass": "유리", "frankly": "솔직히", "bit": "조금 · a bit of a ~ = 다소 ~", "mess": "엉망",
    "clear": "투명한, 분명한", "perfect": "완벽한", "appear": "~처럼 보이다", "eyes": "눈", "molecular": "분자의", "level": "수준",
    "looks": "~해 보이다", "random": "마구잡이의", "ball-pit": "볼풀", "atoms": "원자", "technical": "전문적인", "term": "용어",
    "depends": "~에 달려 있다", "asking": "묻는", "you’re": "너는 ~이다", "scientists": "과학자들", "amorphous": "무정형의",
    "solid": "고체", "supercooled": "과냉각된", "liquid": "액체", "theory": "이론", "given": "~을 고려하면", "behaves": "작용하다",
    "practice": "실제, 연습", "really": "정말로", "latter": "후자", "room": "방 · room temperature = 상온", "temperature": "온도",
    "imperceptibly": "알아차릴 수 없을 정도로", "viscous": "들러붙는", "long": "긴", "periods": "기간", "sweat": "땀을 흘리다",
    "add": "넣다, 더하다", "enough": "충분한", "lime": "석회", "mix": "혼합물", "misshapen": "보기 흉한", "sheets": "판",
    "sometimes": "때때로", "stained-glass": "스테인드글라스", "windows": "창문", "thicker": "더 두꺼운", "bottom": "아랫부분",
    "top": "윗부분", "generally": "대개", "slowly": "천천히", "sinking": "가라앉는", "church": "교회", "endured": "견뎠다",
    "temperatures": "온도", "chances": "가능성", "uneven": "고르지 않은", "blown": "불어서 만든", "solidified": "응고된",
    "place": "자리 · in the first place = 애초에", "flat": "평평한", "developed": "개발된", "nineteenth": "19번째의",
    "century": "세기", "wait": "기다리다", "middle": "중간", "twentieth": "20번째의", "truly": "정말로", "thin": "얇은",
    "paradox": "역설", "despite": "~에도 불구하고", "being": "~인 것", "oldest": "가장 오래된", "human-made": "인간이 만든",
    "substances": "물질", "struggle": "애를 먹다", "comprehend": "이해하다", "seems": "~인 것 같다", "obey": "따르다",
    "laws": "법칙", "glassmaker": "유리 제조업자", "put": "말하다", "material": "재료", "state": "상태", "unless": "~하지 않는 한",
    "fact": "사실", "one": "하나", "has": "~해 왔다", "400˚c": "섭씨 400도",
}

# 칠판 정리 — 2~3문장마다, 밑줄 맞고 틀림 없이 내용만
STORIES = [
    (4, [sc("문장 1~2", "🧊", "a mess · random ball-pit of atoms", "유리는 깔끔해 보여도 분자 수준에선 엉망이에요"),
         sc("문장 3~4", "⚖️", "both liquid and solid · in practice the latter", "이론상 액체이면서 고체, 실제로는 고체예요")]),
    (7, [sc("문장 5~7", "🪟", "never behaves as a liquid · uneven in the first place", "유리는 흐르지 않아요 — 오래된 유리판이 고르지 않은 건 처음 만들 때부터예요")]),
]

exam = {
    "question": "밑줄 친 (a)~(e) 중에서 문맥상 낱말의 쓰임이 적절하지 않은 것은? [3점]",
    "underline": UNDER, "sentence": 10, "analysis_first": True, "wrong_rate": 45.0, "wrong_rank": 10,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("liquid", "액체"), g("misshapen", "보기 흉한"), g("solidified", "응고된"), g("paradox", "역설"), g("obey", "따르다")],
    "options": [
        {"id": "1", "label": "(a) liquid", "keywords": ["liquid"], "ko": "액체"},
        {"id": "2", "label": "(b) misshapen", "keywords": ["misshapen"], "ko": "보기 흉한"},
        {"id": "3", "label": "(c) solidified", "keywords": ["solidified"], "ko": "응고된"},
        {"id": "4", "label": "(d) paradox", "keywords": ["paradox"], "ko": "역설"},
        {"id": "5", "label": "(e) obey", "keywords": ["obey"], "ko": "따르다", "correct": True},
    ],
    "brief": exam_brief(
        "밑줄 단어마다 칠판의 어느 그룹 흐름인지 떠올려 봐요. 흐름과 안 맞는 것 하나를 골라요.",
        "정답이에요! 과학자들도 유리가 왜 그렇게 작용하는지 이해하지 못하니, 유리는 분자 법칙을 따르는(obey) 게 아니라 거스르는(defy) 것처럼 보인다고 해야 맞아요.",
        "정답은 ⑤ (e)예요. 과학자들도 유리를 이해하지 못한다고 했으니, obey(따르다)가 아니라 defy(거스르다)가 맞아요.",
        {"1": "실제로는 고체라서, 상온에서 결코 액체처럼 행동하지 않는다는 말이라 맞아요.",
         "2": "위보다 아래가 두꺼운 유리판이니 모양이 일그러진(misshapen) 게 맞아요.",
         "3": "유리판이 고르지 않은 건 애초에 불어서 만들고 굳힐(solidified) 때 그렇게 돼서예요. 맞는 낱말이에요.",
         "4": "아주 오래된 물질인데 아직 이해하지 못한다는, 서로 안 맞는 사실이라 역설(paradox)이 맞아요."},
        {"3": review(26,
                     "solidified(굳은)가 '유리는 오래 흘러내린다'는 생각과 안 맞아 보여서 많이 골라요. 하지만 글은 유리가 액체처럼 흐르지 않는다고 해요. "
                     "유리판이 고르지 않은 건 애초에 불어서 만들고 굳힐 때 그렇게 된 거예요.",
                     panel=rows(("5문장", "never behaves as a liquid", "결코 액체처럼 행동하지 않음", "hl"),
                                ("6문장", "not … because the glass is slowly sinking", "흘러내려서 그런 게 아님", "hl"),
                                ("7문장", "blown and (c)solidified in the first place", "애초에 불어서 만들고 굳혀서", "hl")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 42번 (문맥상 낱말의 쓰임, 3점)",
    topic="어휘 문제 푸는 법: 요지 → 두 그룹(Clear and perfect ↔ a mess) → 밑줄 단어가 흐름에 맞는지",
    method={"type": "word_in_context", "labels": ["요지 잡기", "두 그룹으로 나누기", "밑줄 단어 맞춰 보기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-glass-state.svg", ("Solid", "고체"), "?", ("Liquid", "액체"),
                                       "유리는 고체일까, 액체일까?", "2026년 6월 모의평가 41~42번 도입 칠판"),
                      "alt": "칠판: Solid(고체) ? Liquid(액체) — 유리는 고체일까, 액체일까?", "kind": "drawing"},
            "method": METHOD_IMAGES["vocab"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "유리창은 단단하고 투명해 보이죠? 이번 글은 유리의 정체를 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "어휘 문제는 단어 뜻만 보면 다 맞아 보여요. 문장마다 흐름을 잡아야 틀린 단어가 보여요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "요지를 잡고, 단어를 두 그룹으로 나눈 뒤, 밑줄 단어가 흐름에 맞는지 볼 거예요."}}],
    exam=exam,
    # molecular, amorphous, viscous는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
    key_words={"passage": [g("structure", "구조"), g("frankly", "솔직히"), g("mess", "엉망"), g("random", "마구잡이의"),
                           g("technical term", "전문 용어"), g("depend on", "~에 따라 달라지다"), g("in theory", "이론상으로는"),
                           g("in practice", "실제로는"), g("the latter", "후자"), g("imperceptibly", "알아차릴 수 없을 정도로"),
                           g("misshapen", "보기 흉한"), g("endure", "견디다"), g("uneven", "고르지 않은"), g("solidify", "응고시키다"),
                           g("in the first place", "애초에"), g("paradox", "역설"), g("substance", "물질"), g("comprehend", "이해하다"),
                           g("obey", "따르다")],
               "options": [g("defy", "거스르다, 거부하다"), g("solidified", "응고된"), g("misshapen", "보기 흉한")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="어휘 문제 푸는 법")
