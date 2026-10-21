"""2026년 6월 모의평가(2027학년도) 39번 레슨 + 대사를 만든다 (주어진 문장 넣기, 3점). 오답률 59% · Top 6 (메가스터디).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_39.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/insertion.md — 주어진 문장 상황 → 단서(also · they) → 앞에 올 내용 → ①~⑤ 흐름 확인 → 정답 열쇠.
정답 ③. 주어진 문장: It was also within the range of reds that they learned … , as the oldest known color terms demonstrate.
열쇠 두 개 — ① also + they: 앞에 「사람들이 빨간색으로 ~했다」(②~③ 사이 문장 It was with red that humans …)가 와야 한다.
② ③ 뒤 Here the lexicon(여기서 그 어휘 목록)은 앞에 단어 이야기가 있어야 하는데 ③ 앞 문장엔 없다 → 주어진 문장의 color terms가 받아 준다.
선택률(메가스터디): ① 2 · ② 9 · ③ 41 · ④ 29 · ⑤ 19 — 많이 고른 오답 ④(color terms 뒤에 어휘 예시가 바로 와서 끌림),
⑤(언어 예시 사이) 둘 다 option_review.
주어진 문장 정석(insertion-given-sentence-order): 「앞에 무엇?」은 also·they라는 근거가 있어서 묻고, 「뒤에 무엇?」은 묻지 않는다.
the lexicon 이야기는 ③ 자리의 흐름 확인과 그 뒤 「정답 열쇠」(s6_terms)에서만 다룬다.
hierarchical·chromatic·lexicon은 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다(lexicon은 정답 단서라 설명에는 남김).
해설지(content/tutor/exam-source/2027-06-평가원/해설.txt) 해석과 대조함 — worthy of that name 그 이름에 걸맞은, As much on the historical as
hierarchical level 위계상으로나 역사적으로나, Not that … but 존재하지 않았던 것은 아니고 다만, in keeping with ~와 일치하는, palette 색채의 범위,
tone 색조 · shade 명암, the case 이 경우.
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음), 「앞을 가리키는 말」 Tip은 맞힌 뒤에만(praise_tips).
Claude 초안(2026-10-21) — 선생님 검토 전.

선생님이 확인할 점
1. 주어진 문장 단서를 also·they 두 개로 찾게 했다(g_clue). 해설지 풀이도 also와 they(= 인간)를 든다.
   같은 모양(It was … that 강조)이라는 점은 정답을 너무 바로 알려 줘서 수업에서는 짚지 않고, 문제 뒤 정답 해설에만 넣었다.
2. ③ 자리에서 「Here the lexicon 앞에는 어떤 이야기?」(s6_here)를 먼저 묻고 흐름 확인, 그다음 「주어진 문장에서 the lexicon이 받을 말」(s6_terms)을 물었다.
   s6_terms는 주어진 문장을 띄워(display) 묻는다 — 정답 열쇠라 사실상 답이 보이는 화면이다. 너무 쉬우면 빼도 된다.
3. 끊어읽기 roles: 주어진 문장·5문장의 It was … that(강조 구문)은 It·was에 표시하지 않고 that 뒤 S·V만 쳤다(they learned / humans did …).
   강조 구문을 어떻게 표시할지 정해 주세요.
4. 헷갈리는 단어(trap): certain(어떤, 확실한 X) · case(경우, 상자 X) · shades(명암, 그늘 X). 엑셀에는 안 넣었다.
5. 해석 맞추기는 1문장(For thousands of years …)에만 넣었다.
6. 많이 고른 오답 ④를 「color terms 바로 뒤에 어휘 예시(In certain languages …)가 와서 그럴듯해 보임」으로 봤다(추측).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, tip, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-06-39-red-first-color"

GIVEN = ("It was also within the range of reds that they learned early on to diversify the palette and to produce varied tones and "
         "shades, as the oldest known color terms demonstrate.")
S = [
    "For thousands of years in the West, red was the only color worthy of that name, the only true color.",
    "As much on the historical as hierarchical level, it exceeded all others.",
    "(①) Not that they did not exist, but they had to wait a long time before they were considered colors and then played a comparable "
    "role in material culture, social codes, and systems of thought.",
    "(②) It was with red that humans did their first color experiments, achieved their first successes, and then constructed a "
    "chromatic universe.",
    "(③) Here the lexicon seems in keeping with pictorial practices and coloring techniques.",
    "(④) In certain languages, the same word can mean “red” or simply “colored,” depending on the context, such as coloratus in "
    "classical Latin or colorado in modern Castilian.",
    "(⑤) In other languages, the words meaning “red” and “beautiful” share a common root; for example, that is the case in Russian, "
    "in which the terms krasnyy (red) and krasivy (beautiful) belong to the same lexical family.",
]
# 해설지 해석 (2027-06-평가원/해설.txt 39번)
KO_GIVEN = ("가장 오래된 색채 용어가 보여주듯이, 그들(인간)이 일찍부터 색채의 범위를 다양화하고 다양한 색조와 명암을 만들어 내는 법을 "
            "배웠던 것도 역시 바로 빨간색 계열 안에서였다.")
KO = [
    "서양에서 수천 년 동안 빨간색은 그 이름에 걸맞은 유일한 색, 즉 유일한 진정한 색이었다.",
    "위계상으로나 역사적으로나 그것은 다른 모든 색을 뛰어넘었다.",
    "다른 색들이 존재하지 않았던 것은 아니고, 다만 그것들이 색으로 인정받고 그다음 물질문화, 사회 규범, 그리고 사상 체계에서 비슷한 역할을 하게 "
    "되기까지 오랜 시간을 기다려야 했다.",
    "인간이 최초의 색채 실험을 하고, 최초의 성공을 거두며, 나아가 색채의 세계를 구축했던 것은 바로 빨간색을 이용해서였다.",
    "여기서 그 어휘 목록은 회화 관행 및 채색 기법과 일치하는 것 같다.",
    "어떤 언어에서는 문맥에 따라, 고전 라틴어의 ‘coloratus’ 또는 현대 카스티야어의 ‘colorado’처럼 같은 단어가 ‘빨간색’을 의미하거나 단순히 "
    "‘색이 있는(유색의)’을 의미하기도 한다.",
    "다른 언어들에서는 ‘빨간’을 뜻하는 단어와 ‘아름다운’을 뜻하는 단어가 같은 어원을 공유하는데, 예를 들어 러시아어에서 ‘krasnyy’(빨간색의)와 "
    "‘krasivy’(아름다운)라는 용어가 같은 어족에 속하는 것이 이 경우이다.",
]


def flow(id, place, before, after, ok, why, praise="맞아요!"):
    """①~⑤ 자리마다 — 앞 문장과 뒤 문장이 그대로 이어지나. 끊김은 정답 자리 하나뿐"""
    return choice(id, f"{place} 자리예요. '{before}' → '{after}', 자연스럽게 이어지나요?",
                  [("o0", "네, 이어져요", ok), ("o1", "아니요, 끊겨요", not ok)], why, why=why, praise=praise,
                  highlight=[f"({place})"], method=2)


sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN, "model_translation": KO_GIVEN, "teaching_value": "high",
        "glosses": [g("It was", "~한 것은 바로 …였다 (강조)"), g("also", "~도 역시"),
                    g("within the range of reds", "빨간색 계열 안에서"), g("within", "~ 안에서"), g("range", "범위, 계열"),
                    g("reds", "빨간색들"), g("they", "그들"), g("learned early on", "일찍부터 배웠다"), g("learned", "배웠다"),
                    g("early on", "일찍부터"), g("diversify", "다양화하다"), g("the palette", "색채의 범위"),
                    g("palette", "색채의 범위 · 원래는 물감을 섞는 판"), g("produce", "만들어 내다"),
                    g("varied tones and shades", "다양한 색조와 명암"), g("varied", "다양한"), g("tones", "색조"),
                    g("shades", "명암"), g("the oldest known color terms", "가장 오래된 색 이름(색채 용어)"), g("color terms", "색 이름, 색채 용어"), g("oldest", "가장 오래된"),
                    g("known", "알려진"), g("color", "색"), g("terms", "용어, 이름"), g("demonstrate", "보여 주다")],
        "emphasis": ["also", "they", "color terms"],
        "slashes": ["It was also", "range of reds", "learned early on", "diversify the palette", "and shades,"],
        "roles": [r("they", "S"), r("learned", "V"), r("the oldest known color terms", "S"), r("demonstrate", "V")],
        "steps": [
            choice("g_situation",
                   "주어진 문장은 무슨 말일까요?",
                   [("o0", "사람들이 색을 다양하게 만드는 법을 일찍 배운 것도 빨간색 계열 안에서였다", True),
                    ("o1", "사람들은 빨간색보다 다른 색으로 먼저 색을 다양하게 만들었다", False),
                    ("o2", "가장 오래된 색 이름에는 빨간색이 없었다", False)],
                   "It was A that ~는 '~한 것은 바로 A였다'예요. within the range of reds는 '빨간색 계열 안에서'예요.",
                   why="'It was also within the range of reds that they learned …', 그들이 색조와 명암을 다양하게 만드는 법을 일찍 배운 것도 바로 빨간색 계열 안에서였대요.",
                   highlight=["within the range of reds", "diversify"],
                   tips=[tip("It was A that ~", "'~한 것은 바로 A였다'예요. A를 강조해요.", "It was"),
                         tip("as + 주어 + 동사 (끝)", "'~가 보여 주듯이'예요. as the oldest known color terms demonstrate = 가장 오래된 색 이름이 보여 주듯이.",
                             "demonstrate")],
                   point="주어진 문장 = 색을 다양하게 만드는 법을 배운 것도(also) 빨간색 안에서였다 (가장 오래된 색 이름이 보여 주듯이)"),
            pick("g_clue", "앞 문장과 이어 주는 단서 두 개를 찾아 눌러 볼까요?",
                 ["also", "they", "the palette", "the oldest known color terms"], ["also", "they"],
                 "그건 앞 문장과 잇는 말이 아니에요.",
                 "also(~도 역시)는 앞에도 비슷한 말이 있다는 뜻이고, they(그들)는 앞에 나온 사람들을 가리켜요.",
                 praise="다 찾았어요!",
                 wrong_by={"the palette": "the palette는 '색채의 범위'예요. 앞에 무엇이 나왔다고 알려 주는 말을 찾아봐요.",
                           "the oldest known color terms": "이건 이 문장 안에서 근거를 대는 말이에요. 앞 문장과 잇는 말을 찾아봐요."},
                 praise_tips=[{"label": "앞을 가리키는 말", "text": "they, this, such 같은 말이 가리키는 것과 also가 받는 비슷한 내용은 바로 앞 문장에 있어야 해요."}],
                 point="단서 = also(앞에도 비슷한 말) · they(앞에 나온 사람들)"),
            choice("g_before",
                   "그럼 이 문장 바로 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "사람들이 빨간색으로 해낸 또 다른 일", True), ("o1", "빨간색 말고 다른 색들이 먼저 쓰였다는 이야기", False),
                    ("o2", "여러 언어에서 빨간색을 뜻하는 단어 이야기", False)],
                   "also(~도 역시)와 they(그들)를 떠올려 봐요. 앞에도 비슷한 말과 they가 가리킬 사람들이 있어야 해요.",
                   why="also가 있으니 앞에도 '빨간색 안에서 무언가를 했다'는 비슷한 말이 와요. they가 가리킬 사람들도 앞에 나와야 해요.",
                   highlight=["also", "they"],
                   point="주어진 문장 앞 = 사람들이 빨간색으로 무언가를 했다는 비슷한 말 (also · they)"),
            show("g_before_note",
                 "지문을 읽으며 사람들이 빨간색으로 무언가를 했다는 문장을 찾아봐요.",
                 panel={"kind": "contrast", "title": "also → 앞에도 비슷한 말", "between": "+",
                        "left": {"title": "바로 앞 문장 (찾을 곳)", "text": "사람들이 빨간색으로 ~했다"},
                        "right": {"title": "주어진 문장", "text": "~한 것도(also) 빨간색 안에서였다"}},
                 highlight=["also"], button="지문 읽어 볼게요"),
        ],
    },
    {
        "id": 2, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("For thousands of years", "수천 년 동안"), g("thousands", "수천"), g("years", "년"),
                    g("in the West", "서양에서"), g("West", "서양"), g("red", "빨간색"), g("was", "~이었다"),
                    g("the only color", "유일한 색"), g("only", "유일한"), g("color", "색"),
                    g("worthy of that name", "그 이름에 걸맞은"), g("worthy", "~할 만한, ~에 걸맞은"), g("name", "이름"),
                    g("the only true color", "유일한 진정한 색"), g("true", "진정한, 진짜의")],
        "slashes": ["For thousands of years", "in the West,", "the only color", "worthy of that name,"],
        "roles": [r("red", "S"), r("was", "V"), r("the only color", "C")],
        "modifiers": ["worthy of that name"],
        "steps": [],
    },
    {
        "id": 3, "text": S[1], "model_translation": KO[1], "teaching_value": "medium",
        "glosses": [g("As much on the historical", "역사적으로도"), g("historical", "역사적인"), g("as hierarchical level", "위계상으로만큼"),
                    g("hierarchical", "위계의"), g("level", "수준, 차원"), g("it", "그것(빨간색)"), g("exceeded", "뛰어넘었다, 능가했다"),
                    g("all others", "다른 모든 것(색)")],
        "slashes": ["hierarchical level,"],
        "roles": [r("it", "S"), r("exceeded", "V"), r("all others", "O")],
        "steps": [
            choice("s3_exceed",
                   "'it exceeded all others'는 무슨 뜻일까요?",
                   [("o0", "빨간색이 다른 모든 색을 뛰어넘었다", True), ("o1", "다른 모든 색이 빨간색을 뛰어넘었다", False),
                    ("o2", "빨간색이 다른 색들과 똑같아졌다", False)],
                   "it은 앞 문장의 red예요. exceed는 '뛰어넘다, 능가하다'예요.",
                   why="it은 red, exceeded는 '뛰어넘었다', all others는 '다른 모든 색'이에요. 역사적으로나 위계상으로나 빨간색이 으뜸이었대요.",
                   highlight=["it exceeded all others"],
                   tips=[tip("as much A as B", "'B만큼 A도'예요. As much on the historical as hierarchical level = 위계상으로나 역사적으로나.",
                             "As much")]),
        ],
    },
    {
        "id": 4, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("Not that", "~라는 것은 아니고"), g("they", "그것들(다른 색들)"), g("did not exist", "존재하지 않았다"),
                    g("exist", "존재하다"), g("had to wait", "기다려야 했다"), g("wait", "기다리다"), g("a long time", "오랜 시간"),
                    g("before", "~하기 전에, ~하기까지"), g("were considered", "~로 여겨졌다"), g("considered", "여겨진"),
                    g("colors", "색"), g("and then played", "그다음 (역할을) 했다"), g("played", "(역할을) 했다"),
                    g("a comparable role", "비슷한 역할"), g("comparable", "비슷한, 비교할 만한"), g("role", "역할"),
                    g("material culture", "물질문화"), g("material", "물질의"), g("culture", "문화"),
                    g("social codes", "사회 규범"), g("social", "사회의"), g("codes", "규범, 규칙"),
                    g("systems of thought", "사상 체계"), g("systems", "체계"), g("thought", "사상, 생각")],
        "slashes": ["Not that they did not exist,", "had to wait", "a long time", "considered colors", "and then played", "comparable role",
                    "material culture,"],
        "roles": [r("they … they … they", "S"), r("did not exist", "V"), r("had to wait", "V"), r("were considered", "V"),
                  r("colors", "C"), r("played", "V"), r("a comparable role", "O")],
        "steps": [
            choice("s4_notthat",
                   "'Not that they did not exist, but …'는 무슨 말일까요?",
                   [("o0", "다른 색들이 없었던 건 아니지만, 색으로 인정받기까지 오래 기다려야 했다", True),
                    ("o1", "다른 색들은 아예 존재하지 않았다", False),
                    ("o2", "다른 색들이 빨간색보다 먼저 색으로 인정받았다", False)],
                   "Not that A, but B는 'A라는 건 아니고, B다'예요. they는 앞 문장의 all others(다른 색들)예요.",
                   why="'Not that they did not exist', 다른 색들이 없었던 건 아니래요. 'but they had to wait a long time', 다만 색으로 인정받기까지 오래 기다려야 했대요.",
                   highlight=["Not that", "had to wait a long time"],
                   tips=[tip("Not that A, but B", "'A라는 것은 아니고, (다만) B다'예요.", "Not that")]),
            flow("s4_flow", "①", "빨간색이 다른 모든 색을 뛰어넘었다", "다른 색들도 없었던 건 아니지만 오래 기다려야 했다", True,
                 "they가 바로 앞 all others(다른 색들)를 받아요. 그대로 이어져요."),
        ],
    },
    {
        "id": 5, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("It was with red", "바로 빨간색으로였다 (강조)"), g("red", "빨간색"), g("humans", "인간, 사람들"),
                    g("did their first color experiments", "첫 색채 실험을 했다"), g("first", "첫, 최초의"), g("experiments", "실험"),
                    g("achieved their first successes", "첫 성공을 거두었다"), g("achieved", "거두었다, 이루었다"), g("successes", "성공"),
                    g("and then constructed", "나아가 구축했다"), g("constructed", "구축했다, 만들었다"),
                    g("a chromatic universe", "색채의 세계"), g("chromatic", "색채의"), g("universe", "세계, 우주")],
        "slashes": ["It was with red", "color experiments,", "first successes,", "and then constructed"],
        "roles": [r("humans", "S"), r("did", "V"), r("their first color experiments", "O"), r("achieved", "V"),
                  r("their first successes", "O"), r("constructed", "V"), r("a chromatic universe", "O")],
        "steps": [
            choice("s5_mean",
                   "사람들(humans)이 빨간색으로 무엇을 했대요?",
                   [("o0", "처음으로 색 실험을 하고, 성공하고, 색의 세계를 만들었다", True),
                    ("o1", "빨간색만 쓰고 다른 색은 실험하지 않았다", False),
                    ("o2", "빨간색이라는 이름을 처음 지었다", False)],
                   "It was with red that ~는 '~한 것은 바로 빨간색으로였다'예요. did · achieved · constructed 세 동사를 봐요.",
                   why="'did their first color experiments, achieved their first successes, and then constructed a chromatic universe', 첫 실험, 첫 성공, 그리고 색의 세계까지 빨간색으로 해냈대요.",
                   highlight=["It was with red", "first color experiments", "first successes", "constructed"]),
            flow("s5_flow", "②", "다른 색들은 색으로 인정받기까지 오래 기다려야 했다", "사람들의 첫 색 실험은 빨간색으로 했다", True,
                 "다른 색들이 오래 기다리는 동안, 첫 색 실험은 빨간색으로 했다는 말이 이어져요. 빨간색이 먼저였다는 흐름이에요."),
        ],
    },
    {
        "id": 6, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Here", "여기서"), g("the lexicon", "그 어휘 목록"), g("lexicon", "어휘 목록"), g("seems", "~인 것 같다"),
                    g("in keeping with", "~와 일치하는, ~에 맞는"), g("pictorial practices", "회화 관행"), g("pictorial", "회화의, 그림의"),
                    g("practices", "관행"), g("coloring techniques", "채색 기법"), g("coloring", "채색"), g("techniques", "기법")],
        "slashes": ["Here the lexicon", "seems in keeping", "pictorial practices"],
        "roles": [r("the lexicon", "S"), r("seems", "V"), r("in keeping with", "C")],
        "steps": [
            choice("s6_here",
                   "'Here the lexicon(여기서 그 어휘 목록)'이라고 했어요. 바로 앞에는 어떤 이야기가 있어야 할까요?",
                   [("o0", "색을 부르는 말(단어) 이야기", True), ("o1", "색을 칠하는 기법 이야기", False),
                    ("o2", "다른 색들이 오래 기다린 이야기", False)],
                   "lexicon은 시험지 아래에 '어휘 목록'으로 풀어 줬어요. the와 Here는 앞에 나온 것을 받아요.",
                   why="the lexicon(그 어휘 목록)은 앞에 나온 단어 이야기를 받아요. Here(여기서)도 앞 내용을 가리켜요.",
                   highlight=["Here the lexicon"],
                   tips=[tip("in keeping with", "'~와 일치하는, ~에 맞는'이에요. seems in keeping with = ~와 일치하는 것 같다.", "in keeping with")]),
            flow("s6_flow", "③", "사람들의 첫 색 실험은 빨간색으로 했다", "여기서 그 어휘 목록은 회화 관행과 일치한다", False,
                 "앞 문장에는 단어·이름 이야기가 없어요. the lexicon(그 어휘 목록)이 받을 말이 없어서 흐름이 끊겨요.",
                 praise="맞아요! 여기서 흐름이 끊겨요."),
            choice("s6_terms",
                   "주어진 문장에서 the lexicon(어휘 목록)이 받을 수 있는 말은 무엇일까요?",
                   [("o0", "the palette", False), ("o1", "varied tones and shades", False), ("o2", "the oldest known color terms", True)],
                   "lexicon은 단어(말)를 모은 거예요. 주어진 문장에서 단어·이름을 뜻하는 말을 찾아봐요.",
                   why="terms는 '용어, 이름'이에요. 가장 오래된 색 이름이 단어 이야기라 the lexicon이 받을 수 있어요.",
                   display=GIVEN, tag="주어진 문장",
                   point="③ 뒤 the lexicon(어휘 목록) ← 주어진 문장의 color terms(색 이름)가 받아 준다"),
        ],
    },
    {
        "id": 7, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("In certain languages", "어떤 언어에서는"), g("certain", "어떤, 특정한"), g("languages", "언어"),
                    g("the same word", "같은 단어"), g("same", "같은"), g("word", "단어"), g("can mean", "~을 뜻할 수 있다"),
                    g("mean", "뜻하다"), g("red", "빨간"), g("simply", "단순히"), g("colored", "색이 있는, 유색의"),
                    g("depending on the context", "문맥에 따라"), g("depending on", "~에 따라"), g("context", "문맥"),
                    g("such as", "~처럼"), g("coloratus", "콜로라투스 · 라틴어 단어"), g("in classical Latin", "고전 라틴어의"),
                    g("classical", "고전의"), g("Latin", "라틴어"), g("colorado", "콜로라도 · 카스티야어(스페인어) 단어"),
                    g("in modern Castilian", "현대 카스티야어의"), g("modern", "현대의"), g("Castilian", "카스티야어 · 스페인어")],
        "slashes": ["In certain languages,", "can mean", "“colored,”", "the context,", "classical Latin"],
        "roles": [r("the same word", "S"), r("can mean", "V")],
        "steps": [
            show("s7_lang",
                 "어떤 언어에서는 같은 단어가 '빨간'도, 그냥 '색이 있는'도 뜻한대요. 빨간색이 곧 '색'이었다는 단어 예시예요.",
                 highlight=["the same word", "“red”", "“colored,”"], button="다음",
                 tips=[tip("depending on", "'~에 따라'예요. depending on the context = 문맥에 따라.", "depending on")]),
            flow("s7_flow", "④", "여기서 그 어휘 목록은 회화 관행과 일치한다", "어떤 언어에서는 같은 단어가 '빨간'과 '색이 있는'을 뜻한다", True,
                 "어휘 목록 이야기를 In certain languages(어떤 언어에서는)의 단어 예시로 이어 가요. 흐름이 끊기지 않아요."),
        ],
    },
    {
        "id": 8, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("In other languages", "다른 언어들에서는"), g("languages", "언어"), g("the words", "단어들"),
                    g("meaning", "~을 뜻하는"), g("beautiful", "아름다운"), g("share", "공유하다, 같이 가지다"),
                    g("a common root", "같은 어원(뿌리)"), g("common", "공통의"), g("root", "뿌리, 어원"),
                    g("for example", "예를 들어"), g("that", "그것(앞 내용)"), g("the case", "이 경우"), g("case", "경우"),
                    g("in Russian", "러시아어에서"), g("Russian", "러시아어"), g("in which", "그 안에서(러시아어에서)"),
                    g("the terms", "용어들"), g("terms", "용어"), g("krasnyy", "크라스니 · 러시아어 '빨간'"),
                    g("krasivy", "크라시비 · 러시아어 '아름다운'"), g("belong to", "~에 속하다"), g("belong", "속하다"),
                    g("the same lexical family", "같은 어족(어휘 집안)"), g("lexical", "어휘의"), g("family", "가족, 집안")],
        "slashes": ["In other languages,", "the words meaning", "share a common root;", "for example,", "the case in Russian,",
                    "and krasivy (beautiful)"],
        "roles": [r("the words", "S"), r("share", "V"), r("a common root", "O"), r("that", "S"), r("is", "V"), r("the case", "C")],
        "modifiers": ["meaning “red” and “beautiful”",
                      "in which the terms krasnyy (red) and krasivy (beautiful) belong to the same lexical family"],
        "steps": [
            show("s8_lang",
                 "다른 언어에서는 '빨간'과 '아름다운'을 뜻하는 단어가 같은 뿌리래요. 러시아어 krasnyy와 krasivy가 그 예예요.",
                 highlight=["a common root", "krasnyy", "krasivy"], button="다음"),
            flow("s8_flow", "⑤", "어떤 언어에서는 같은 단어가 '빨간'과 '색이 있는'을 뜻한다", "다른 언어에서는 '빨간'과 '아름다운'이 같은 뿌리다", True,
                 "In certain languages(어떤 언어에서는) → In other languages(다른 언어에서는)로 짝을 이뤄요. 그대로 이어져요."),
            show("s8_go", "①~⑤ 중 흐름이 끊긴 곳은 하나였어요. 주어진 문장의 also와 color terms를 떠올리며 골라 봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — 1문장(짧은 문장, 모두에게). 덩어리는 문장에 그대로 있는 구절
add_match(sentences, 2, [m("For thousands of years", "수천 년 동안"), " ", m("red", "빨간색은"), " ", m("worthy of that name", "그 이름에 걸맞은"), " ",
                         m("the only color", "유일한 색"), m("was", "이었다"), "."])
# 가리키는 말
add_refers(sentences, 3, {"it": "red(빨간색)"})
add_refers(sentences, 4, {"they": "all others = the other colors(다른 색들)"})
add_refers(sentences, 8, {"that": "the words for red and beautiful share a root(빨간·아름다운이 같은 어원)"})

SENSES = {
    1: [sense("that", "reds that they learned", "~한 것은 (강조)", "It was A that ~ 강조 구문의 that"),
        sense("to", "to diversify", "~하는 것(법)", "learn to + 동사원형 = ~하는 법을 배우다"),
        sense("to", "to produce", "~하는 것(법)", "learned에 이어지는 둘째 to부정사"),
        sense("as", "as the oldest known color terms demonstrate", "~가 보여 주듯이", "접속사 as (~하듯이)")],
    2: [sense("for", "For thousands of years", "~ 동안", "전치사 for (기간)"),
        sense("that", "that name", "그", "지시형용사 that — 앞의 color를 가리킴")],
    3: [sense("as", "As much on the historical", "~만큼", "as much A as B = B만큼 A도"),
        sense("as", "as hierarchical level", "~만큼", "as much A as B의 둘째 as")],
    4: [sense("that", "Not that they", "~라는 것은 (아니고)", "Not that A, but B = A라는 건 아니고 B"),
        sense("but", "but they had to wait", "다만, 그러나", "Not that A, but B의 but"),
        sense("to", "had to wait", "~해야 (했다)", "have to + 동사원형 = ~해야 하다")],
    5: [sense("that", "red that humans did", "~한 것은 (강조)", "It was A that ~ 강조 구문의 that")],
    7: [sense("as", "such as coloratus", "~처럼", "such as = ~ 같은, 예를 들어")],
    8: [sense("for", "for example", "예를 들어", "for example = 예를 들어"),
        sense("that", "that is the case", "그것", "지시대명사 that — 앞 내용(같은 어원을 가짐)"),
        sense("which", "in which the terms", "그 안에서 (러시아어에서)", "전치사 + 관계대명사 which — Russian을 받음"),
        sense("to", "belong to", "~에", "belong to = ~에 속하다")],
}

WORDS = {"range": "범위", "reds": "빨간색들", "learned": "배웠다", "early": "일찍", "diversify": "다양화하다", "palette": "색채의 범위",
         "produce": "만들어 내다", "varied": "다양한", "tones": "색조", "shades": "명암", "oldest": "가장 오래된", "known": "알려진",
         "color": "색", "terms": "용어", "demonstrate": "보여 주다", "thousands": "수천", "years": "년", "west": "서양",
         "red": "빨간색", "only": "유일한", "worthy": "걸맞은", "name": "이름", "true": "진정한", "historical": "역사적인",
         "hierarchical": "위계의", "level": "차원", "exceeded": "뛰어넘었다", "others": "다른 것들", "exist": "존재하다",
         "wait": "기다리다", "long": "긴", "considered": "여겨진", "colors": "색", "played": "(역할을) 했다", "comparable": "비슷한",
         "role": "역할", "material": "물질의", "culture": "문화", "social": "사회의", "codes": "규범", "systems": "체계",
         "thought": "사상", "humans": "인간", "experiments": "실험", "achieved": "거두었다", "successes": "성공",
         "constructed": "구축했다", "chromatic": "색채의", "universe": "세계", "lexicon": "어휘 목록", "seems": "~인 것 같다",
         "keeping": "일치 · in keeping with = ~와 일치하는", "pictorial": "회화의", "practices": "관행", "coloring": "채색",
         "techniques": "기법", "certain": "어떤", "languages": "언어", "word": "단어", "mean": "뜻하다", "simply": "단순히",
         "colored": "색이 있는", "depending": "~에 따라 · depending on", "context": "문맥", "classical": "고전의",
         "latin": "라틴어", "modern": "현대의", "castilian": "카스티야어", "words": "단어들", "meaning": "~을 뜻하는",
         "beautiful": "아름다운", "share": "공유하다", "common": "공통의", "root": "어원", "example": "예", "case": "경우",
         "russian": "러시아어", "belong": "속하다", "lexical": "어휘의", "family": "집안", "first": "첫"}

STORIES = [
    (3, [sc("문장 1~2", "🟥", "red = the only true color", "서양에서 수천 년 동안 빨간색만 진짜 색이었고, 다른 모든 색을 뛰어넘었어요")]),
    (5, [sc("①~②", "🧪", "others had to wait · with red → first experiments", "다른 색들은 오래 기다렸고, 사람들의 첫 색 실험은 빨간색으로 했어요")]),
    (8, [sc("③~⑤", "🔤", "red = colored · red ~ beautiful", "여러 언어에서 '빨간'은 '색이 있는', '아름다운'과 같은 말이에요")]),
]

OPTIONS = [
    ("1", "Not that they did not exist … 앞", "빨간색은 다른 모든 색을 뛰어넘었다 뒤", False),
    ("2", "It was with red that humans … 앞", "다른 색들은 오래 기다려야 했다 뒤", False),
    ("3", "Here the lexicon seems … 앞", "사람들의 첫 색 실험은 빨간색으로 했다 뒤", True),
    ("4", "In certain languages … 앞", "어휘 목록이 회화 관행과 일치한다 뒤", False),
    ("5", "In other languages … 앞", "같은 단어가 '빨간'과 '색이 있는'을 뜻한다 뒤", False),
]
exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳을 고르시오. [3점]",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"], "numbers_only": True,
    "passage_keywords": ["also", "color terms", "humans", "lexicon"],
    "sentence": 1, "analysis_first": True, "wrong_rate": 59, "wrong_rank": 6,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "주어진 문장의 also·they와 끝의 color terms를 떠올리며 들어갈 곳을 골라 봐요.",
        "정답이에요! 사람들의 첫 색 실험은 빨간색으로 했다(It was with red that humans …) → 색을 다양하게 만드는 법을 배운 것도(also) 빨간색 안에서였다, "
        "가장 오래된 색 이름(color terms)이 보여 주듯이 → 여기서 그 어휘 목록(the lexicon)은 …, 순서예요.",
        "정답은 ③이에요. ③ 뒤 Here the lexicon이 받을 color terms를 주어진 문장이 먼저 꺼내 줘야 해요.",
        {"1": "① 뒤 Not that they …의 they는 바로 앞 all others(다른 색들)를 받아요. 그 사이에 넣으면 they가 가리킬 게 바뀌어요.",
         "2": "② 뒤 It was with red that humans …가 먼저 와야 주어진 문장의 also와 they(사람들)가 받을 말이 생겨요.",
         "4": "④에 넣으면 ③ 뒤 Here the lexicon이 받을 단어 이야기가 여전히 앞에 없어요. 흐름이 ③에서 끊긴 채로 남아요.",
         "5": "⑤ 앞뒤는 In certain languages → In other languages로 짝을 이룬 예시예요. 사이에 넣으면 짝이 끊겨요."},
        {"4": review(29,
                     "④에 넣으면 color terms 바로 뒤에 언어 예시(In certain languages …)가 와서 그럴듯해 보여요. 그런데 그러면 ③ 뒤 "
                     "'Here the lexicon(여기서 그 어휘 목록)'이 받을 단어 이야기가 앞에 없어요.\nthe lexicon이 받을 color terms(주어진 문장)가 그보다 먼저, ③에 와야 해요.",
                     panel=rows(("② 뒤", "It was with red that humans …", "사람들의 첫 색 실험은 빨간색으로", "hl2"),
                                ("주어진 문장", "also … they … color terms", "그것도 빨간색 안에서 · 색 이름", "hl"),
                                ("③ 뒤", "Here the lexicon …", "그 어휘 목록 = 색 이름", "hl")),
                     rank_word="가장 많이 고른"),
         "5": review(19,
                     "⑤ 앞뒤는 'In certain languages(어떤 언어에서는) … / In other languages(다른 언어에서는) …'로 짝을 이룬 예시예요. "
                     "그 사이에 넣으면 짝이 끊기고, ③ 뒤 the lexicon도 여전히 받을 말이 없어요.",
                     panel=rows(("④ 뒤", "In certain languages …", "어떤 언어에서는", "hl"),
                                ("⑤ 뒤", "In other languages …", "다른 언어에서는", "hl")))}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 주어진 문장(위에서 넣음)과 열쇠 문장(5·6)만 ──
EMPHASIS = {
    5: ["It was with red", "humans"],
    6: ["Here", "the lexicon"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 39번 (주어진 문장 넣기, 3점)",
    topic="문장 넣기 푸는 법: 주어진 문장의 단서 → 앞에 올 내용 예측 → ①~⑤ 흐름이 끊기는 곳",
    method={"type": "sentence_insertion", "labels": ["주어진 문장 단서 찾기", "앞에 올 내용 예측하기", "흐름 끊기는 곳 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-red-first-color.svg", ("Red", "빨간색"), "↔", ("Other colors", "다른 색들"),
                                       "빨간색은 왜 특별한 색이었을까?", "2026년 6월 모의평가 39번 도입 칠판"),
                      "alt": "칠판: Red(빨간색) ↔ Other colors(다른 색들)", "kind": "drawing"},
            "method": METHOD_IMAGES["insert"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "옛날 서양 사람들에게 빨간색은 어떤 색이었을까요? 이번 글은 서양에서 빨간색이 가진 자리를 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "문장 넣기는 주어진 문장부터 꼼꼼히 봐야 해요. 그 안에 앞 문장과 이어지는 단서가 숨어 있어요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "단서를 찾고, 앞에 올 내용을 예측한 뒤, 흐름이 끊기는 곳을 찾아요."}}],
    exam=exam,
    # hierarchical·chromatic·lexicon은 시험지 아래 *로 풀어 준 말 — 핵심 단어가 아니라 뺐다
    key_words={"passage": [g("within", "~ 안에서"), g("diversify", "다양화하다"), g("palette", "색채의 범위"), g("varied", "다양한"),
                           g("tone", "색조"), g("shade", "명암"), g("demonstrate", "보여 주다"), g("worthy of", "~에 걸맞은"),
                           g("exceed", "뛰어넘다, 능가하다"), g("comparable", "비슷한"), g("material culture", "물질문화"),
                           g("construct", "구축하다"), g("in keeping with", "~와 일치하는"), g("pictorial", "회화의"),
                           g("depending on", "~에 따라"), g("context", "문맥"), g("share", "공유하다"), g("root", "어원"),
                           g("belong to", "~에 속하다")],
               "options": []},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함:
# shades 명암 · certain 어떤 · case 경우.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    1: [tip("shades", "이 글에서는 → 명암  ('그늘' 아님)", "shades", trap=True)],
    2: [tip("worthy of", "'~에 걸맞은, ~할 만한'이에요. worthy of that name = 그(색이라는) 이름에 걸맞은.", "worthy of")],
    7: [tip("certain", "이 글에서는 → 어떤  ('확실한' 아님)", "certain", trap=True)],
    8: [tip("case", "이 글에서는 → 경우  ('상자' 아님) · that is the case = 이 경우이다", "the case", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="문장 넣기 푸는 법")
