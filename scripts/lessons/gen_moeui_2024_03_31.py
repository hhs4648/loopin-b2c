"""2024년 3월 고3 31번 레슨 + 대사를 만든다 (빈칸 추론, 2점). 오답률 71.0% · Top 3.

    python3 scripts/lessons/gen_moeui_2024_03_31.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md (빈칸이 가운데 — 6월 34번 꼴). 정답 ① loss.
② sense 30.0%가 정답(29.0%)보다 많다 — 'an accompanying sense of …'가 말로는 자연스러워서. ③ increase 24.2%.
열쇠: 두 그룹 — 지금(8~16세: conventional, literal, correctness, 남들이 쓰는 단어) ↔ 예전(어릴 때: spontaneity, originality,
metaphor, 줄기 없는 꽃). 지금 쪽이 늘어나면서 예전 쪽은 '잃는다'.
해설지 해석과 대조함. dexterity, spontaneity는 시험지 아래 *로 풀어 준 단어(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)

ID = "moeui-2024-03-31-conventional-writing"

BLANK = ("As a result, our writing and oral storying become increasingly conventional and literal, with an accompanying "
         "________ of the spontaneity and originality that characterized our earlier efforts.")
S = [
    "From about ages eight through sixteen, our manual dexterity has strengthened through continually improving eye-hand coordination.",
    "There is considerable improvement in handwriting skills.",
    "We gain mastery over the mechanics of language.",
    "We also gradually eliminate the logical gaps in our stories―characteristic of our earlier stage of perception―as intense "
    "preoccupation with the whole vision gives way to preoccupation with correctness.",
    BLANK,
    "At this stage our vocabulary is firmly grounded.",
    "We use words everyone else uses.",
    "We have little need to invent metaphors to communicate.",
    "By now we know that a star is “a hot gaseous mass floating in space” in contrast to our innocent stage, when we noticed, "
    "“Look that star is like a flower without a stem!”",
]
KO = [
    "약 8세부터 16세까지, 우리의 손재주는 눈과 손의 협응을 지속적으로 향상시키면서 강화되어 왔다.",
    "필기 능력에 상당한 향상이 있다.",
    "우리는 언어의 기술에 대한 숙달을 얻는다.",
    "우리는 또한 전체 시각에 대한 강렬한 집착이 정확성에 대한 집착으로 바뀌면서, (우리의 초기 지각 단계의 특징인) 우리 이야기의 논리적 공백을 점차적으로 제거한다.",
    "그 결과, 우리의 글쓰기와 구술은 점점 더 상투적이며 사실에 충실하게 되고, 우리의 초기 노력의 특징이었던 즉흥성과 독창성의 ________을 수반하게 된다.",
    "이 단계에서 우리의 어휘는 확고하게 기반을 갖는다.",
    "우리는 모든 사람이 사용하는 단어를 사용한다.",
    "우리는 의사소통하기 위해 은유를 지어낼 필요가 거의 없다.",
    "이제 우리는 '봐 저 별은 줄기가 없는 꽃과 같아!'라고 말했던 순진한 단계와 대조하여, 별이 '우주를 떠다니는 뜨거운 기체 덩어리'라는 것을 알고 있다.",
]

NOW = "오른쪽 · 자라고 난 뒤 (16살)"
EARLY = "왼쪽 · 어릴 때 (8살)"


def board(now, early, fresh=(), sort=None):
    """칠판 — 왼쪽 어릴 때(8살), 오른쪽 자라고 난 뒤(16살) (2026-10-18 선생님). 부르는 쪽은 (자란 뒤 말, 어릴 때 말) 순서 그대로"""
    return groups("어릴 때 vs 자라고 난 뒤", "어릴 때 (8살)", early, "자라고 난 뒤 (16살)", now, fresh=fresh, between="→",
                  sort={"words": sort, "left": EARLY, "right": NOW} if sort else None)


L4 = ["correctness"]
R4 = ["the whole vision", "logical gaps"]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("From about ages eight through sixteen", "약 8세부터 16세까지"), g("our manual dexterity", "우리의 손재주"),
                    g("dexterity", "재주, 솜씨"), g("has strengthened", "강해졌다"), g("through", "~을 통해"),
                    g("continually improving", "계속 좋아지는"), g("eye-hand coordination", "눈과 손의 협응"),
                    g("As a result", "그 결과"), g("our writing and oral storying", "우리의 글쓰기와 말로 하는 이야기"),
                    g("become", "~해지다"), g("increasingly", "점점 더"), g("conventional", "관습적인, 틀에 박힌"),
                    g("literal", "글자 그대로의, 사실에 충실한"), g("with an accompanying", "~이 함께 따라오면서"),
                    g("the spontaneity and originality", "즉흥성과 독창성"), g("characterized", "~의 특징이었다"),
                    g("our earlier efforts", "우리의 예전 노력(어릴 때 쓴 것)")],
        "slashes": ["through sixteen,", "has strengthened"],
        "roles": [r("our manual dexterity", "S"), r("has strengthened", "V")],
        "steps": [
            show("s1_passage", "빈칸은 여기, 다섯째 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "글쓰기가 자유로워지면서, 즉흥성이 ____ 된다", False),
                    ("o1", "글쓰기가 틀에 박혀 가면서, 예전의 즉흥성·독창성에 ____이 함께 생긴다", True),
                    ("o2", "어릴 때 글쓰기가 더 틀에 박혀 있었다", False)],
                   "conventional은 '틀에 박힌', literal은 '글자 그대로의'예요. with an accompanying ____ of는 '~의 ____이 함께 따라오면서'예요.",
                   why="become increasingly conventional and literal은 점점 틀에 박히고 글자 그대로가 된다는 말이에요. 그러면서 예전 노력의 즉흥성·독창성에 ____이 함께 따라온대요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["conventional and literal", "________"],
                   highlight_alt=["spontaneity and originality", "earlier efforts"],
                   tips=[tip("with an accompanying ~", "'~이 함께 따라오면서, ~을 수반하며'예요. 앞 일이 일어나면서 같이 생기는 일이 뒤에 와요.", "accompanying")]),
            show("s1_where_map", "이 문장에는 '지금(자라면서)'과 '예전(어릴 때)' 두 쪽 말이 같이 있어요.",
                 button="다음", before_read=True, levels=["중", "초"], display=BLANK, tag="빈칸 문장", method=0,
                 highlight=["conventional and literal"], highlight_alt=["spontaneity and originality", "earlier efforts"],
                 panel_below=True,
                 panel=rows(("어릴 때", "spontaneity and originality", "즉흥성과 독창성 (earlier efforts)", "hl2"),
                            ("자라고 난 뒤", "conventional and literal", "틀에 박히고 글자 그대로", "hl"))),
            show("s1_where", "그럼 자라면서 어릴 때의 즉흥성·독창성이 어떻게 되는지 생각하며 문장 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
            show("s1_board", "8살부터 16살 사이에 손재주가 좋아진대요. 이 글은 자라면서 생기는 변화를 말해요. 칠판을 두 쪽으로 나눠 둘게요.",
                 panel=board([("manual dexterity ↑", "손재주가 좋아짐")], [], fresh=("manual dexterity ↑",)),
                 highlight=["has strengthened"], button="다음 문장"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("There is", "~이 있다"), g("considerable improvement", "상당한 향상"), g("in handwriting skills", "글씨 쓰는 실력에")],
        "slashes": ["considerable improvement"],
        "roles": [r("is", "V"), r("considerable improvement", "S")],
        "steps": [
            show("s2_hand", "글씨 쓰는 실력도 많이 좋아진대요.", highlight=["considerable improvement"], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("We", "우리는"), g("gain mastery over", "~을 익히다, 숙달하다"), g("the mechanics of language", "언어의 기술(문법·맞춤법)"),
                    g("mechanics", "기법, 기술")],
        "slashes": ["gain mastery"],
        "roles": [r("We", "S"), r("gain", "V"), r("mastery", "O")],
        "steps": [
            choice("s3_mech",
                   "We gain mastery over the mechanics of language는 무슨 뜻일까요?",
                   [("o0", "언어로 기계를 다루게 된다", False), ("o1", "언어를 쓰는 기술(문법·맞춤법)을 익힌다", True),
                    ("o2", "언어를 점점 잊는다", False)],
                   "mechanics는 여기서 '기계'가 아니라 '기법, 기술'이에요. gain mastery over는 '~을 익히다'예요.",
                   why="gain mastery over는 '~을 숙달하다', the mechanics of language는 '언어의 기술'이에요. 문법·맞춤법 같은 걸 익힌다는 말이에요.",
                   highlight=["gain mastery over", "mechanics"],
                   tips=[tip("mechanics", "'기계학'만 있는 게 아니에요. the mechanics of ~ = ~의 기법, 작동 방식.", "mechanics")]),
            show("s3_board", "손재주, 글씨, 언어 기술이 모두 좋아져요. 칠판 오른쪽(자라고 난 뒤)에 쌓아 둘게요.",
                 panel=board([("manual dexterity ↑", "손재주"), ("mechanics of language", "언어 기술")], [],
                             fresh=("mechanics of language",)), button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("We", "우리는"), g("also gradually", "또한 점점"), g("eliminate", "없애다"), g("the logical gaps", "논리적 빈틈"),
                    g("in our stories", "우리 이야기 속의"), g("characteristic of our earlier stage of perception", "어릴 적 인식 단계의 특징인"),
                    g("intense preoccupation", "강한 집착"), g("with the whole vision", "전체 그림에 대한"),
                    g("gives way to", "~에 자리를 내주다, ~로 바뀌다"), g("preoccupation with correctness", "정확성에 대한 집착"),
                    g("correctness", "정확성")],
        "slashes": ["gradually eliminate", "in our stories―", "stage of perception―", "the whole vision", "gives way"],
        "roles": [r("We", "S"), r("eliminate", "V"), r("the logical gaps", "O"), r("intense preoccupation", "S"), r("gives way", "V")],
        "steps": [
            sv("s4_sv", ["We", "eliminate", "the logical gaps", "intense preoccupation", "gives way to"],
               {"We": "S", "eliminate": "V", "the logical gaps": "O"},
               {"intense preoccupation": "그건 as(~하면서) 뒤 덩어리 안의 주어예요. as 앞에서 찾아봐요.",
                "gives way to": "그건 as 뒤 덩어리 안의 동사예요. as 앞에서 찾아봐요."},
               "주어는 We, 동사는 eliminate, 목적어는 the logical gaps(논리적 빈틈)예요.",
               ask="as 앞에서 주어(S), 동사(V), 목적어(O)를 찾아볼까요?",
               faded=["―characteristic of our earlier stage of perception―"]),
            choice("s4_shift",
                   "as 뒤를 봐요. 전체 그림에 대한 집착(the whole vision)이 무엇에 대한 집착으로 바뀐대요?",
                   [("o0", "상상력", False), ("o1", "이야기의 길이", False), ("o2", "정확성(correctness)", True)],
                   "gives way to는 '~로 바뀌다'예요. to 뒤를 봐요.",
                   why="'gives way to preoccupation with correctness', 전체 그림 대신 정확성에 집착하게 된대요.",
                   highlight=["gives way to", "correctness"],
                   tips=[tip("give way to", "'~에 자리를 내주다, ~로 바뀌다'예요. A gives way to B = A가 B로 바뀌다.", "gives way to")]),
            show("s4_board", "어릴 땐 전체 그림을 보고 논리적 빈틈도 있었는데, 자라면서 정확성을 따지게 돼요.",
                 panel=board([("manual dexterity ↑", "손재주"), ("mechanics of language", "언어 기술"), ("correctness", "정확성")],
                             [("the whole vision", "전체 그림"), ("logical gaps", "논리적 빈틈")],
                             fresh=("correctness", "the whole vision", "logical gaps")), button="다음 문장",
                 faded=["―characteristic of our earlier stage of perception―"]),
        ],
    },
    {
        "id": 5, "text": BLANK, "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("As a result", "그 결과"), g("our writing and oral storying", "우리의 글쓰기와 말로 하는 이야기"),
                    g("become", "~해지다"), g("increasingly conventional and literal", "점점 틀에 박히고 글자 그대로인"),
                    g("conventional and literal", "틀에 박히고 글자 그대로인"),
                    g("with an accompanying", "~이 함께 따라오면서"), g("the spontaneity and originality", "즉흥성과 독창성"),
                    g("spontaneity and originality", "즉흥성과 독창성"),
                    g("that characterized our earlier efforts", "예전 노력의 특징이었던"), g("earlier efforts", "예전 노력")],
        "slashes": ["As a result,", "oral storying", "conventional and literal,", "an accompanying ________", "and originality"],
        "roles": [r("our writing and oral storying", "S"), r("become", "V"), r("increasingly conventional and literal", "C")],
        "modifiers": ["that characterized our earlier efforts"],
        "steps": [
            sv("s5_sv", ["our writing and oral storying", "become", "increasingly conventional and literal", "the spontaneity and originality"],
               {"our writing and oral storying": "S", "become": "V", "increasingly conventional and literal": "C"},
               {"the spontaneity and originality": "그건 with an accompanying ____ of 뒤 덩어리예요. 전치사 뒤라 주어가 아니에요."},
               "주어는 our writing and oral storying, 동사는 become, 보어는 increasingly conventional and literal이에요.",
               ask="빈칸 문장이에요. 주어(S), 동사(V), 보어(C)를 찾아볼까요?"),
            choice("s5_sort_now",
                   "'conventional and literal(틀에 박히고 글자 그대로인)'은 칠판 어느 쪽일까요?",
                   [("o0", EARLY, False), ("o1", NOW, True)],
                   "As a result(그 결과) — 정확성에 집착하게 된 결과예요.",
                   panel=board([("manual dexterity ↑", "손재주"), ("mechanics of language", "언어 기술"), ("correctness", "정확성")],
                               [("the whole vision", "전체 그림"), ("logical gaps", "논리적 빈틈")], sort=["conventional and literal"]),
                   highlight=["conventional and literal"]),
            choice("s5_sort_early",
                   "그럼 'spontaneity and originality(즉흥성과 독창성)'는 어느 쪽일까요?",
                   [("o0", EARLY, True), ("o1", NOW, False)],
                   "바로 뒤 'that characterized our earlier efforts'를 봐요. earlier는 '예전의'예요.",
                   why="'that characterized our earlier efforts', 예전 노력의 특징이었대요. 그러니 어릴 때 쪽이에요.",
                   panel=board([("manual dexterity ↑", "손재주"), ("mechanics of language", "언어 기술"), ("correctness", "정확성"),
                                ("conventional and literal", "틀에 박힌")],
                               [("the whole vision", "전체 그림"), ("logical gaps", "논리적 빈틈")], sort=["spontaneity and originality"]),
                   highlight=["spontaneity and originality", "earlier efforts"]),
            choice("s5_side",
                   "자라면서 틀에 박힌 쪽이 늘어나요. 그럼 어릴 때의 즉흥성·독창성은 어떻게 될까요?",
                   [("o0", "함께 늘어난다", False), ("o1", "그대로 남는다", False), ("o2", "줄어들고 사라진다", True)],
                   "두 쪽은 서로 반대예요. 한쪽이 늘면 다른 쪽은 어떻게 될지 생각해 봐요.",
                   why="틀에 박히고(conventional) 글자 그대로(literal)가 되는 건 즉흥성·독창성과 반대예요. 한쪽이 늘면 다른 쪽은 줄어들어요.",
                   panel=board([("manual dexterity ↑", "손재주"), ("mechanics of language", "언어 기술"), ("correctness", "정확성"),
                                ("conventional and literal", "틀에 박힌")],
                               [("the whole vision", "전체 그림"), ("logical gaps", "논리적 빈틈"), ("spontaneity and originality", "즉흥성·독창성")],
                               fresh=("conventional and literal", "spontaneity and originality")),
                   point="빈칸 = 자라면서(conventional, literal) 어릴 때의 즉흥성·독창성이 줄어든다 → 잃음"),
            show("s5_check", "빈칸 뒤 문장들도 같은 이야기인지 확인하며 계속 읽어 봐요.", button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "low",
        "glosses": [g("At this stage", "이 단계에서"), g("our vocabulary", "우리의 어휘"), g("is firmly grounded", "단단히 자리 잡혀 있다")],
        "slashes": ["At this stage"],
        "roles": [r("our vocabulary", "S"), r("is firmly grounded", "V")],
        "steps": [
            show("s6_ground", "이 시기엔 어휘가 단단히 자리 잡혀 있대요.", highlight=["firmly grounded"], button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("We", "우리는"), g("use", "쓰다"), g("words", "단어들"), g("everyone else uses", "다른 모든 사람이 쓰는")],
        "roles": [r("We", "S"), r("use", "V"), r("words", "O")],
        "modifiers": ["everyone else uses"],
        "steps": [
            show("s7_same", "남들이 다 쓰는 단어를 쓴대요. conventional(틀에 박힌)과 같은 말이에요.",
                 panel=board([("correctness", "정확성"), ("conventional and literal", "틀에 박힌"), ("words everyone else uses", "남들이 쓰는 단어")],
                             [("logical gaps", "논리적 빈틈"), ("spontaneity and originality", "즉흥성·독창성")],
                             fresh=("words everyone else uses",)),
                 highlight=["everyone else uses"], button="다음"),
            show("s7_example", "어릴 땐 자동차를 '빵빵이'처럼 내가 지어낸 말로 불러요. 자라고 나면 남들이 다 쓰는 '자동차'라고 불러요.",
                 panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/ppangppang-car.svg",
                        "alt": "작은 아이(어릴 때, 8살)가 자동차를 보고 '빵빵이!', 조금 큰 아이는 '빵빵… 차?', 다 큰 사람(16살)은 '자동차'. 내가 지어낸 말 → 남들이 다 쓰는 말",
                        "words": [{"text": "words everyone else uses"}]},
                 button="다음 문장"),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("We", "우리는"), g("have little need", "필요가 거의 없다"), g("to invent metaphors", "은유를 지어낼"),
                    g("metaphors", "은유"), g("to communicate", "의사소통하기 위해")],
        "slashes": ["little need"],
        "roles": [r("We", "S"), r("have", "V"), r("little need", "O")],
        "steps": [
            choice("s8_little",
                   "We have little need to invent metaphors는 무슨 뜻일까요?",
                   [("o0", "은유를 많이 지어내야 한다", False), ("o1", "은유를 지어낼 필요가 거의 없다", True),
                    ("o2", "은유를 조금은 지어낸다", False)],
                   "little은 a 없이 쓰면 '거의 없는'이에요. a little(조금 있는)과 달라요.",
                   why="little need는 '필요가 거의 없음'이에요. 남들이 쓰는 말로 충분하니 은유를 지어낼 일이 거의 없대요.",
                   highlight=["little need"],
                   tips=[tip("little vs a little", "little = 거의 없는(부정), a little = 조금 있는(긍정)이에요.", "little")]),
            show("s8_board", "은유를 지어내는 건 어릴 때 쪽이에요. 자라면서는 그럴 필요가 거의 없어요.",
                 panel=board([("correctness", "정확성"), ("conventional and literal", "틀에 박힌"), ("words everyone else uses", "남들이 쓰는 단어")],
                             [("logical gaps", "논리적 빈틈"), ("spontaneity and originality", "즉흥성·독창성"), ("invent metaphors", "은유 지어내기")],
                             fresh=("invent metaphors",)), button="다음 문장"),
        ],
    },
    {
        "id": 9, "text": S[8], "model_translation": KO[8], "teaching_value": "high",
        "glosses": [g("By now", "이제는"), g("we know", "우리는 안다"), g("a star", "별"), g("a hot gaseous mass", "뜨거운 기체 덩어리"),
                    g("floating in space", "우주를 떠다니는"), g("in contrast to", "~와 대조적으로"), g("our innocent stage", "우리의 순진한 단계"),
                    g("when we noticed", "그때 우리는 ~라고 알아챘다"), g("Look", "봐"), g("that star", "저 별"), g("is like", "~ 같다"),
                    g("a flower without a stem", "줄기 없는 꽃")],
        "slashes": ["By now we know", "gaseous mass", "floating in space”", "innocent stage,", "we noticed,"],
        "roles": [r("we … we", "S"), r("know", "V"), r("a star", "S"), r("is … is", "V"), r("a hot gaseous mass", "C"), r("noticed", "V"),
                  r("that star", "S")],
        "steps": [
            show("s9_star",
                 "지금은 별을 '뜨거운 기체 덩어리'라고 사실 그대로 말해요. 어릴 땐 '줄기 없는 꽃 같다'고 은유로 말했어요.",
                 highlight=["a hot gaseous mass"], highlight_alt=["a flower without a stem"],
                 panel=board([("conventional and literal", "틀에 박힌"), ("words everyone else uses", "남들이 쓰는 단어"),
                              ("a hot gaseous mass", "뜨거운 기체 덩어리")],
                             [("spontaneity and originality", "즉흥성·독창성"), ("invent metaphors", "은유 지어내기"),
                              ("like a flower without a stem", "줄기 없는 꽃 같다")],
                             fresh=("a hot gaseous mass", "like a flower without a stem")),
                 tips=[tip("in contrast to", "'~와 대조적으로'예요. 앞뒤가 반대라는 신호예요.", "in contrast to")]),
            show("s9_go", "빈칸은 자라면서 어릴 때의 즉흥성·독창성이 어떻게 되는지였어요. 그 말을 보기에서 골라 봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 1, [m("From about ages eight through sixteen", "약 8세부터 16세까지"), ", ", m("our manual dexterity", "우리의 손재주는"), " ",
                         m("has strengthened", "강해졌다"), "."],
          match_display="From about ages eight through sixteen, our manual dexterity has strengthened.",
          sv_new=sv_step("s1_basic_sv", ["From about ages eight through sixteen", "our manual dexterity", "has strengthened", "eye-hand coordination"],
                         {"our manual dexterity": "S", "has strengthened": "V"},
                         {"From about ages eight through sixteen": "그건 '언제'를 알려 주는 말이에요.",
                          "eye-hand coordination": "그건 through(~을 통해) 뒤 덩어리 안의 말이에요."},
                         "주어는 our manual dexterity, 동사는 has strengthened예요."),
          meaning_ids=["s1_board"])
add_basic(sentences, 2, [m("There is", "~이 있다"), " — ", m("in handwriting skills", "글씨 쓰는 실력에"), " ", m("considerable improvement", "상당한 향상"), "."],
          # 동사는 is만 — there는 표시하지 않는다 (there was가 둘인 21번 3문장과 같게, 2026-10-20 선생님)
          sv_new=sv_step("s2_basic_sv", ["is", "considerable improvement", "handwriting skills"],
                         {"is": "V", "considerable improvement": "S"},
                         {"handwriting skills": "그건 in 뒤 덩어리예요. 전치사 뒤라 주어가 아니에요."},
                         "There is 문장은 동사 뒤가 진짜 주어예요. 동사는 is, 주어는 considerable improvement예요.",
                         ask="there is(~이 있다) 문장이에요. 동사(V)와 그 뒤의 진짜 주어(S)를 찾아볼까요?"),
          meaning_ids=["s2_hand"])
add_basic(sentences, 3, [m("We", "우리는"), " ", m("the mechanics of language", "언어의 기술"), "을 ", m("gain mastery over", "익힌다"), "."],
          sv_new=sv_step("s3_basic_sv", ["We", "gain", "mastery", "the mechanics of language"],
                         {"We": "S", "gain": "V", "mastery": "O"},
                         {"the mechanics of language": "그건 over 뒤 덩어리예요."},
                         "주어는 We, 동사는 gain, 목적어는 mastery예요(숙달을 얻다 = 익히다)."),
          meaning_after="s3_mech")
add_basic(sentences, 4, [m("We", "우리는"), " ", m("in our stories", "우리 이야기 속의"), " ", m("the logical gaps", "논리적 빈틈"), "을 ",
                         m("also gradually", "또한 점점"), " ", m("eliminate", "없앤다"), "."],
          match_display="We also gradually eliminate the logical gaps in our stories.",
          sv_id="s4_sv", meaning_ids=["s4_board"])
add_basic(sentences, 6, [m("At this stage", "이 단계에서"), " ", m("our vocabulary", "우리의 어휘는"), " ", m("is firmly grounded", "단단히 자리 잡혀 있다"), "."],
          sv_new=sv_step("s6_basic_sv", ["At this stage", "our vocabulary", "is firmly grounded"],
                         {"our vocabulary": "S", "is firmly grounded": "V"},
                         {"At this stage": "그건 '이 단계에서', 때를 알려 주는 말이에요."},
                         "주어는 our vocabulary, 동사는 is (firmly) grounded예요."),
          meaning_ids=["s6_ground"])
add_basic(sentences, 7, [m("We", "우리는"), " ", m("everyone else uses", "다른 모든 사람이 쓰는"), " ", m("words", "단어들"), "을 ", m("use", "쓴다"), "."],
          sv_new=sv_step("s7_basic_sv", ["We", "use", "words", "everyone else uses"], {"We": "S", "use": "V", "words": "O"},
                         {"everyone else uses": "그건 앞의 words를 꾸며 주는 덩어리예요(다른 모든 사람이 쓰는)."},
                         "주어는 We, 동사는 use, 목적어는 words예요."),
          meaning_ids=["s7_same"])
add_basic(sentences, 8, [m("We", "우리는"), " ", m("to communicate", "의사소통하기 위해"), " ", m("to invent metaphors", "은유를 지어낼"), " ",
                         m("have little need", "필요가 거의 없다"), "."],
          sv_new=sv_step("s8_basic_sv", ["We", "have", "little need", "metaphors"], {"We": "S", "have": "V", "little need": "O"},
                         {"metaphors": "그건 to invent(지어낼) 뒤의 말이에요."},
                         "주어는 We, 동사는 have, 목적어는 little need(거의 없는 필요)예요."),
          meaning_after="s8_little")
add_basic(sentences, 9, [m("By now", "이제는"), " ", m("we know", "우리는 안다"), " — ", m("a star", "별"), "이 ", m("a hot gaseous mass", "뜨거운 기체 덩어리"),
                         "라는 걸."],
          match_display="By now we know that a star is “a hot gaseous mass floating in space.”",
          sv_new=sv_step("s9_basic_sv", ["we", "know", "a star", "is", "a hot gaseous mass"],
                         {"we": "S", "know": "V"},
                         {"a star": "그건 that 뒤 덩어리 안의 주어예요(무엇을 아는지).", "is": "그건 that 뒤 덩어리 안의 동사예요.",
                          "a hot gaseous mass": "그건 that 뒤 덩어리 안의 말이에요."},
                         "주어는 we, 동사는 know예요. that 뒤가 아는 내용이에요."),
          meaning_ids=["s9_star"])

SENSES = {
    4: [sense("as", "as intense preoccupation", "~하면서", "접속사 as + 주어·동사 (동시·비례)"),
        sense("to", "gives way to", "~에게, ~로 (자리를 내주다)", "give way to + 명사 = ~로 바뀌다")],
    5: [sense("as", "As a result", "(As a result의 일부)", "As a result = 그 결과"),
        sense("that", "originality that characterized", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    8: [sense("to", "need to invent", "~할", "명사 + to부정사 (~할 필요)"),
        sense("to", "to communicate", "~하기 위해", "to부정사 (목적)")],
    9: [sense("that", "we know that", "~라는 것을", "명사절 that (know that …)"),
        sense("to", "in contrast to", "~와 (대조적으로)", "in contrast to + 명사"),
        sense("that", "that star", "저", "지시형용사 that + 명사")],
}

WORDS = {"conventional": "틀에 박힌, 관습적인", "literal": "글자 그대로의", "ages": "나이", "eight": "8", "sixteen": "16", "about": "약", "manual": "손의", "continually": "계속", "improving": "좋아지는",
         "eye-hand": "눈과 손의", "coordination": "협응", "writing": "글쓰기", "oral": "말로 하는", "storying": "이야기하기",
         "accompanying": "함께 따라오는", "spontaneity": "즉흥성", "originality": "독창성", "earlier": "예전의", "efforts": "노력",
         "considerable": "상당한", "improvement": "향상", "handwriting": "손글씨", "skills": "실력", "gain": "얻다",
         "mastery": "숙달", "language": "언어", "gradually": "점점", "logical": "논리적인", "gaps": "빈틈", "stories": "이야기",
         "characteristic": "특징적인", "stage": "단계", "perception": "인식", "intense": "강한", "preoccupation": "집착",
         "whole": "전체의", "vision": "그림, 시각", "gives": "주다", "way": "길 · give way to = ~로 바뀌다", "stage.": "단계",
         "vocabulary": "어휘", "firmly": "단단히", "grounded": "자리 잡은", "words": "단어들", "uses": "쓰다", "need": "필요",
         "invent": "지어내다", "communicate": "의사소통하다", "know": "알다", "star": "별", "hot": "뜨거운", "gaseous": "기체의",
         "mass": "덩어리", "floating": "떠다니는", "space": "우주", "contrast": "대조", "innocent": "순진한", "noticed": "알아챘다",
         "flower": "꽃", "without": "~ 없이", "stem": "줄기", "like": "~ 같은", "now": "지금", "little": "거의 없는",
         "increasingly": "점점 더", "also": "또한", "characterized": "특징지었다", "strengthened": "강해졌다", "mechanics": "기법, 기술",
         "result": "결과", "everyone": "모든 사람", "look": "봐"}

STORIES = [
    (4, [sc("문장 1~3", "✍️", "dexterity · handwriting · mechanics", "8~16세에 손재주, 글씨, 언어 기술이 좋아져요"),
         sc("문장 4", "🎯", "whole vision → correctness", "전체 그림 대신 정확성을 따지게 돼요")]),
    (7, [sc("빈칸 문장", "📏", "conventional and literal · ____", "글이 틀에 박히고 글자 그대로가 되면서, 예전의 즉흥성·독창성에 ____"),
         sc("문장 6~7", "📚", "words everyone else uses", "어휘가 자리 잡고, 남들이 쓰는 단어를 써요")]),
    (9, [sc("문장 8~9", "⭐", "no metaphors · gaseous mass", "은유를 지어낼 필요가 없어요 — 별은 '줄기 없는 꽃'이 아니라 '기체 덩어리'")]),
]

OPTIONS = [("1", "loss", "잃음, 손실", True), ("2", "sense", "감각", False), ("3", "increase", "증가", False),
           ("4", "recovery", "회복", False), ("5", "demonstration", "보여 줌, 시연", False)]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 5, "analysis_first": True, "wrong_rate": 71.0, "wrong_rank": 3,
    "glosses": [g("loss", "잃음, 손실"), g("sense", "감각"), g("increase", "증가"), g("recovery", "회복"), g("demonstration", "보여 줌, 시연")],
    "options": [{"id": o[0], "label": o[1], "keywords": [o[1]], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "자라면서 쪽이 늘 때 어릴 때 쪽(즉흥성·독창성)이 어떻게 되는지 떠올리며 골라 봐요.",
        "정답이에요! 글이 틀에 박히고 글자 그대로가 되면서, 어릴 때의 즉흥성과 독창성은 함께 사라져요. 그래서 loss(잃음)예요.",
        "정답은 ① loss예요. 틀에 박힌 쪽이 늘면서 즉흥성·독창성은 잃어 가요.",
        {"2": "'an accompanying sense of …'는 말로는 자연스럽지만, 즉흥성의 '감각'이 함께 생긴다면 즉흥성이 남는다는 말이 돼요. 글은 틀에 박혀 간다고 했어요.",
         "3": "즉흥성·독창성이 늘어난다면 틀에 박힌다는 앞말과 반대예요.",
         "4": "회복은 잃었던 걸 되찾는 거예요. 글은 이제 막 잃어 가는 중이에요.",
         "5": "즉흥성을 보여 준다면 은유도 지어낼 텐데, 은유를 지어낼 필요가 거의 없대요."},
        {"2": review(30.0,
                     "'an accompanying sense of the spontaneity'는 영어로 자연스럽게 들려서 가장 많이 골랐어요. 하지만 그러면 '즉흥성의 감각이 함께 생긴다', 즉흥성이 살아 있다는 말이 돼요. 글은 틀에 박히고 글자 그대로가 된다고 했으니, 반대쪽인 즉흥성은 줄어야 해요.",
                     "그래서 ②가 아니에요. 어디서 헷갈렸어요?",
                     [("말이 자연스러워 보여서 골랐어요", ["collocation_trap"],
                       "알려 줘서 고마워요. 빈칸은 말이 자연스러운지보다 앞뒤 흐름(어느 쪽이 늘고 주는지)으로 정해요. 앞으로 이 점을 강조해서 알려 줄게요."),
                      ("두 쪽이 반대인 걸 못 봤어요", ["two_sides"],
                       "알려 줘서 고마워요. conventional(틀에 박힌)과 spontaneity(즉흥성)는 반대 쪽이에요. 앞으로 두 쪽을 칠판에 나눠서 보여 줄게요."),
                      ("둘 다요", ["collocation_trap", "two_sides"], "알려 줘서 고마워요. 앞으로 두 쪽을 먼저 나누고 빈칸을 보게 할게요.")],
                     panel=rows(("어릴 때", "spontaneity and originality", "즉흥성·독창성 → ↓ (loss)", "hl2"),
                                ("자라고 난 뒤", "conventional and literal", "틀에 박히고 글자 그대로 ↑", "hl")),
                     rank_word="가장 많이 고른"),
         "3": review(24.2,
                     "increase(증가)를 넣으면 '즉흥성과 독창성이 함께 늘어난다'가 돼요. 그런데 글은 점점 틀에 박히고 남들이 쓰는 단어만 쓴대요. 즉흥성은 늘 수가 없어요.",
                     "그래서 ③이 아니에요. 어디서 헷갈렸어요?",
                     [("자라면 다 좋아진다고 생각했어요", ["growth_all_good"],
                       "알려 줘서 고마워요. 손재주·글씨는 좋아지지만, 그 대가로 즉흥성은 줄어요. 앞으로 좋아지는 것과 잃는 것을 나눠 보여 줄게요."),
                      ("of 뒤가 누구 쪽인지 헷갈렸어요", ["two_sides"],
                       "알려 줘서 고마워요. that characterized our earlier efforts, 예전의 특징이에요. 앞으로 earlier 같은 시간 단서를 짚어 줄게요."),
                      ("둘 다요", ["growth_all_good", "two_sides"], "알려 줘서 고마워요. 앞으로 두 쪽을 먼저 나누고 빈칸을 보게 할게요.")])}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 31번 (빈칸 추론, 2점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 두 쪽 말 모으기 → 빈칸이 어느 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-growing-writing.svg", ("Growing up", "자라면서"), "→", ("Writing", "글쓰기"),
                                       "자라면 글쓰기에서 무엇을 얻고 무엇을 잃을까?", "2024년 3월 31번 도입 칠판"),
                      "alt": "칠판: Growing up(자라면서) → Writing(글쓰기)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "어릴 땐 별을 '줄기 없는 꽃'이라고 했는데, 지금은 뭐라고 할까요? 이번 글은 자라면서 글쓰기가 어떻게 바뀌는지 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("manual", "손의"), g("coordination", "협응"), g("considerable", "상당한"), g("mastery", "숙달"),
                           g("mechanics", "기법, 기술"), g("eliminate", "없애다"), g("characteristic of", "~의 특징인"),
                           g("perception", "인식, 지각"), g("preoccupation", "집착"), g("give way to", "~로 바뀌다"),
                           g("conventional", "틀에 박힌, 관습적인"), g("literal", "글자 그대로의"), g("accompanying", "수반하는"),
                           g("originality", "독창성"), g("grounded", "자리 잡은"), g("metaphor", "은유"), g("innocent", "순진한")],
               "options": [g("loss", "잃음, 손실"), g("recovery", "회복"), g("demonstration", "보여 줌, 시연")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법",
       chunks={"From about ages eight through sixteen": "약 8세부터 16세까지", "our manual dexterity": "우리의 손재주",
               "has strengthened": "강해졌다", "eye-hand coordination": "눈과 손의 협응", "There is": "~이 있다",
               "considerable improvement": "상당한 향상", "handwriting skills": "글씨 쓰는 실력", "We": "우리는", "gain": "얻다",
               "mastery": "숙달", "the mechanics of language": "언어의 기술", "eliminate": "없애다", "the logical gaps": "논리적 빈틈",
               "intense preoccupation": "강한 집착", "gives way to": "~로 바뀌다", "our writing and oral storying": "글쓰기와 말로 하는 이야기",
               "become": "~해지다", "increasingly conventional and literal": "점점 틀에 박히고 글자 그대로인",
               "the spontaneity and originality": "즉흥성과 독창성", "At this stage": "이 단계에서", "our vocabulary": "우리의 어휘",
               "is firmly grounded": "단단히 자리 잡혀 있다", "use": "쓰다", "words": "단어들", "everyone else uses": "다른 모든 사람이 쓰는",
               "have": "가지다", "little need": "거의 없는 필요", "metaphors": "은유", "we": "우리는", "know": "알다", "a star": "별",
               "is": "~이다", "a hot gaseous mass": "뜨거운 기체 덩어리", "also gradually": "또한 점점", "in our stories": "우리 이야기 속의",
               "have little need": "필요가 거의 없다", "to invent metaphors": "은유를 지어낼", "to communicate": "의사소통하기 위해",
               "gain mastery over": "익히다"})
