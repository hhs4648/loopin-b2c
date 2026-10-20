"""2024년 3월 고3 36번 레슨 + 대사를 만든다 (글의 순서, 3점). 오답률 38.9% · Top 15.

    python3 scripts/lessons/gen_moeui_2024_03_36.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/order.md — 주어진 글의 끝 → 단락 첫머리(앞에 무엇?) → 단락 끝(다음에 무엇?) → 순서 잇기.
정답 ② (B)-(A)-(C). 많이 고른 오답 ③ (B)-(C)-(A) 20.6% — (C) 'Instead, he'의 he(한 사람)가 (B)의 재즈 음악가들(they)을 받을 수 없다.
단서: (B) They ← 주어진 글 끝 jazz musicians / (A) On the other end ← one end, (B)로 재즈 이야기를 마친 뒤 /
(C) Instead, he ← (A) 끝 '모차르트의 작품도 저절로 나온 게 아니다'. 해설지 해석과 대조함. improvisational, immerse는 *풀이 단어.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from order_tools import card, order_link  # noqa: E402

ID = "moeui-2024-03-36-creative-spectrum"

G1 = ("Different creative pursuits require varying degrees of unconscious flexible thinking, in combination with varying degrees "
      "of the conscious ability to adjust it and shape it through analytical thinking.")
G2 = "In music, for example, at one end of the creative spectrum are improvisational artists, such as jazz musicians."
A1 = ("(A) On the other end of the spectrum are those who compose complex forms, such as a symphony or concerto, that require "
      "not just imagination but also careful planning and exacting editing.")
A2 = ("We know, for example, through his letters and the reports of others, that even Mozart’s creations did not appear "
      "spontaneously, wholly formed in his consciousness, as the myths about him portray.")
B1 = "(B) They have to be particularly talented at lowering their inhibitions and letting in their unconsciously generated ideas."
B2 = ("And although the process of learning the fundamentals of jazz would require a high degree of analytical thought, that "
      "thinking style is not as big a factor during the performance.")
C1 = ("(C) Instead, he spent long, hard hours analyzing and reworking the ideas that arose in his unconscious, much as a scientist "
      "does when producing a theory from a germ of insight.")
C2 = "In Mozart’s own words: “I immerse myself in music... I think about it all day long―I like experimenting―studying―reflecting...”"

FREE = "왼쪽 · 무의식적·유연한 생각"
ANAL = "오른쪽 · 의식적·분석적 생각"


def board(left, right, fresh=(), sort=None):
    return groups("창의성의 스펙트럼", "무의식적·유연한 생각 (one end)", left, "의식적·분석적 생각", right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": FREE, "right": ANAL} if sort else None)


sentences = [
    {
        "id": 1, "label": "주어진 글", "text": f"{G1} {G2}", "teaching_value": "high",
        "model_translation": "서로 다른 창의적인 일들은 다양한 정도의 무의식적이고 유연한 사고를, 분석적인 사고를 통해서 그것을 조정하고 형성하는 다양한 정도의 의식적인 능력과 함께 결합하여 요구한다. 예를 들어, 음악에서 창의적인 스펙트럼의 한끝에는 재즈 음악가와 같은 즉흥 연주가들이 있다.",
        "glosses": [g("Different creative pursuits", "서로 다른 창의적인 일들"), g("require", "필요로 하다"),
                    g("varying degrees of unconscious flexible thinking", "다양한 정도의 무의식적이고 유연한 생각"),
                    g("in combination with", "~와 결합하여"), g("the conscious ability", "의식적인 능력"),
                    g("to adjust it and shape it", "그것을 조정하고 다듬는"), g("through analytical thinking", "분석적인 생각을 통해"),
                    g("In music", "음악에서"), g("at one end of the creative spectrum", "창의성 스펙트럼의 한쪽 끝에"),
                    g("the creative spectrum", "창의성의 스펙트럼"), g("are", "있다"), g("improvisational artists", "즉흥 연주가들"),
                    g("such as jazz musicians", "재즈 음악가 같은")],
        "slashes": ["Different creative pursuits require", "flexible thinking,", "in combination with", "the conscious ability",
                    "adjust it and shape it", "analytical thinking.", "In music, for example,", "creative spectrum", "improvisational artists,"],
        "roles": [r("Different creative pursuits", "S"), r("require", "V"), r("varying degrees of unconscious flexible thinking", "O"), r("are", "V"),
                  r("improvisational artists", "S")],
        "steps": [
            sv("g_sv", ["Different creative pursuits", "require", "varying degrees of unconscious flexible thinking",
                        "the creative spectrum", "are", "improvisational artists"],
               {"Different creative pursuits": "S", "require": "V", "varying degrees of unconscious flexible thinking": "O",
                "are": "V", "improvisational artists": "S"},
               {"the creative spectrum": "그건 at one end of 뒤, 어디인지 알려 주는 말이에요."},
               "첫 문장은 S Different creative pursuits, V require, O varying degrees of … thinking이에요. 둘째 문장은 장소가 앞에 나와 V are, S improvisational artists예요.",
               ask="주어진 글은 두 문장이에요. 주어(S), 동사(V), 목적어(O)를 모두 찾아볼까요?"),
            choice("g_two",
                   "창의적인 일에는 두 가지 생각이 섞인대요. 무엇과 무엇일까요?",
                   [("o0", "빠른 생각과 느린 생각", False), ("o1", "무의식적이고 유연한 생각과, 의식적이고 분석적인 생각", True),
                    ("o2", "혼자 하는 생각과 함께 하는 생각", False)],
                   "'unconscious flexible thinking'과 'in combination with … the conscious ability … through analytical thinking'을 봐요.",
                   why="'unconscious flexible thinking'(무의식적이고 유연한 생각)과 'the conscious ability … analytical thinking'(의식적이고 분석적인 생각)이 섞인대요.",
                   highlight=["unconscious flexible thinking", "analytical thinking"],
                   panel=board([("unconscious flexible thinking", "무의식·유연")], [("analytical thinking", "분석적")],
                               fresh=("unconscious flexible thinking", "analytical thinking"))),
            choice("g_one_end",
                   "음악에서 스펙트럼의 한쪽 끝(one end)에 있는 즉흥 연주가(재즈 음악가)는 칠판 어느 쪽일까요?",
                   [("o0", FREE, True), ("o1", ANAL, False)],
                   "improvisational은 '즉흥적인'이에요. 즉흥 연주는 미리 분석하기보다 그 자리에서 떠오르는 대로 해요.",
                   panel=board([("unconscious flexible thinking", "무의식·유연")], [("analytical thinking", "분석적")],
                               sort=["jazz musicians"]),
                   highlight=["at one end of the creative spectrum", "improvisational artists"],
                   tips=[tip("장소 + are + 주어", "at one end … are improvisational artists = 한쪽 끝에 즉흥 연주가들이 있다. 장소가 앞에 나오면 동사가 주어보다 먼저 와요.", "are")]),
            choice("g_next",
                   "주어진 글은 '한쪽 끝(one end)의 재즈 음악가들'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "모차르트의 편지 내용", False), ("o1", "과학자가 이론을 만드는 방법", False),
                    ("o2", "그 재즈 음악가들이 어떤지 더 자세한 설명", True)],
                   "방금 재즈 음악가를 처음 소개했어요. 소개 바로 뒤엔 그들을 받는 말이 오기 쉬워요.",
                   why="재즈 음악가를 막 소개했으니, 바로 뒤엔 그들(They)이 어떤지 설명이 오기 쉬워요. 모차르트나 과학자는 아직 나오지도 않았어요.",
                   tips=[tip("순서 문제 요령", "주어진 글의 마지막 말이 다음 단락의 첫머리와 이어져요. They, he, the other end, Instead 같은 말이 무엇을 받는지 봐요.")]),
            show("paper_order", "이제 (A)·(B)·(C)를 시험지 순서대로 읽어요. 단락마다 첫머리와 끝을 잘 봐 두면 좋아요.",
                 button="(A)부터 읽어 볼게요"),
        ],
    },
    {
        "id": 2, "text": A1, "teaching_value": "high",
        "model_translation": "(A) 스펙트럼의 다른 끝에는 심포니와 콘체르토와 같은, 상상력뿐만이 아니라 신중한 계획과 고된 편집을 요구하는 복잡한 형식을 작곡하는 자들이 있다.",
        "glosses": [g("On the other end of the spectrum", "스펙트럼의 다른 끝에는"), g("are", "있다"), g("those who compose", "~을 작곡하는 사람들"),
                    g("complex forms", "복잡한 형식"), g("such as a symphony or concerto", "교향곡이나 협주곡 같은"),
                    g("require", "필요로 하다"), g("not just imagination", "상상력뿐 아니라"),
                    g("but also careful planning and exacting editing", "꼼꼼한 계획과 고된 편집도")],
        "slashes": ["the spectrum", "are those", "complex forms,", "or concerto,", "not just imagination"],
        "roles": [r("are", "V"), r("those", "S")],
        "modifiers": ["who compose complex forms, such as a symphony or concerto, that require not just imagination but also careful planning and exacting editing"],
        "steps": [
            choice("a_before",
                   "(A)는 'On the other end of the spectrum(스펙트럼의 다른 끝에는)'으로 시작해요. 앞에는 무엇이 나와야 할까요?",
                   [("o0", "모차르트의 작업 방식", False), ("o1", "스펙트럼의 한쪽 끝 이야기", True), ("o2", "과학자의 이론", False)],
                   "the other end(다른 끝)라고 하려면, 먼저 한쪽 끝이 나왔어야 해요.",
                   why="'the other end'(다른 끝)는 앞에서 한쪽 끝(one end)을 말한 뒤에 나와요. 그러니 (A) 앞에는 한쪽 끝(재즈 쪽) 이야기가 있어야 해요.",
                   highlight=["On the other end of the spectrum"],
                   point="(A) On the other end ← 한쪽 끝(재즈) 이야기가 먼저 나온 뒤"),
            show("a_compose", "다른 끝에는 교향곡처럼 복잡한 곡을 쓰는 작곡가가 있대요. 상상력뿐 아니라 꼼꼼한 계획과 편집이 필요해요.",
                 highlight=["careful planning", "exacting editing"],
                 tips=[tip("not just A but also B", "'A뿐만 아니라 B도'예요. not just imagination but also careful planning = 상상력뿐 아니라 꼼꼼한 계획도.", "not just")],
                 panel=board([("unconscious flexible thinking", "무의식·유연"), ("jazz musicians", "재즈 음악가")],
                             [("analytical thinking", "분석적"), ("those who compose complex forms", "복잡한 곡의 작곡가")],
                             fresh=("those who compose complex forms",))),
        ],
    },
    {
        "id": 3, "text": A2, "teaching_value": "high",
        "model_translation": "예를 들어, 우리는 그의 편지와 다른 이들의 기록을 통해, 심지어 모차르트의 창작물 또한, 그에 관한 전설이 그려 내듯 즉흥적으로 발생한 것이 아니라는 것, 의식 속에서 완전히 만들어진 채로 나타난 것이 아니라는 것을 안다.",
        "glosses": [g("We know", "우리는 안다"), g("for example", "예를 들어"), g("through his letters", "그의 편지를 통해"),
                    g("the reports of others", "다른 사람들의 기록"), g("even Mozart’s creations", "모차르트의 작품조차"),
                    g("did not appear spontaneously", "저절로(즉흥적으로) 나타나지 않았다"), g("wholly formed in his consciousness", "의식 속에서 완전히 만들어진 채로"),
                    g("as the myths about him portray", "그에 관한 전설이 그리듯")],
        "slashes": ["We know,", "for example,", "through his letters", "the reports of others,", "Mozart’s creations", "appear spontaneously,",
                    "his consciousness,"],
        "roles": [r("We", "S"), r("know", "V"), r("Mozart’s creations", "S"), r("did not appear", "V"), r("the myths", "S"), r("portray", "V")],
        "steps": [
            choice("a2_myth",
                   "모차르트의 작품은 전설(myths)이 그리는 것처럼 저절로 완성돼 나왔대요?",
                   [("o0", "그렇다, 저절로 나왔다", False), ("o1", "아니다, 저절로 나온 게 아니다", True)],
                   "'did not appear spontaneously'를 봐요. 앞에 not이 있어요.",
                   why="'even Mozart’s creations did not appear spontaneously', 모차르트의 작품조차 저절로 나온 게 아니래요. 전설이 그리는 것과 달라요.",
                   highlight=["did not appear spontaneously", "the myths"],
                   tips=[tip("as + 주어 + 동사", "여기서 as는 '~하듯이, ~처럼'이에요. as the myths about him portray = 그에 관한 전설이 그리듯.", "as the myths")]),
            choice("a2_next",
                   "(A)는 '모차르트의 작품도 저절로 나온 게 아니다'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "재즈 음악가의 재능", False), ("o1", "그럼 모차르트는 대신 어떻게 작업했는지", True),
                    ("o2", "스펙트럼의 한쪽 끝 소개", False)],
                   "'저절로가 아니다'라고 했으면, 다음엔 '그 대신 어떻게 했는지'가 오기 쉬워요.",
                   why="'저절로 나온 게 아니다'라고 부정했으니, 다음엔 '그 대신(Instead) 모차르트는 어떻게 했는지'가 이어지기 쉬워요.",
                   highlight=["did not appear spontaneously"],
                   point="(A) 끝 '모차르트도 저절로가 아니다' → 다음은 '대신 어떻게 했는지'"),
        ],
    },
    {
        "id": 4, "text": B1, "teaching_value": "high",
        "model_translation": "(B) 그들은 그들의 억제를 낮추고 무의식적으로 생성된 생각들을 받아들이는 것에 특히 재능이 있어야 한다.",
        "glosses": [g("They", "그들은"), g("have to be", "~여야 한다"), g("particularly talented at", "특히 ~에 재능이 있는"),
                    g("lowering their inhibitions", "억제를 낮추는 것"), g("inhibitions", "억제, 거리낌"),
                    g("letting in", "받아들이는 것"), g("their unconsciously generated ideas", "무의식적으로 떠오른 생각들")],
        "slashes": ["particularly talented", "their inhibitions"],
        "roles": [r("They", "S"), r("have to be", "V"), r("particularly talented", "C")],
        "steps": [
            choice("b_before",
                   "(B)는 'They have to be particularly talented at lowering their inhibitions …'로 시작해요. They는 누구일까요?",
                   [("o0", "교향곡 작곡가들", False), ("o1", "과학자들", False), ("o2", "즉흥 연주하는 재즈 음악가들", True)],
                   "억제를 낮추고, 무의식적으로 떠오른 생각을 받아들인대요. 칠판 왼쪽(무의식·유연) 쪽 사람들이에요.",
                   why="'lowering their inhibitions and letting in their unconsciously generated ideas', 떠오르는 대로 받아들이는 건 즉흥 연주가, 재즈 음악가예요.",
                   highlight=["They", "unconsciously generated ideas"],
                   tips=[tip("inhibition", "'억제, 거리낌'이에요. lower one's inhibitions = 거리낌을 낮추다, 마음 가는 대로 하다.", "inhibitions")],
                   point="(B) They = 재즈 음악가들 ← 주어진 글 끝 jazz musicians"),
        ],
    },
    {
        "id": 5, "text": B2, "teaching_value": "high",
        "model_translation": "그리고 비록 재즈의 원리를 배우는 과정이 높은 정도의 분석적 사고를 요구할지라도, 그러한 사고방식은 공연 중에 그렇게 큰 요인이 아니다.",
        "glosses": [g("And although", "그리고 비록 ~이지만"), g("the process of learning the fundamentals of jazz", "재즈의 기초를 배우는 과정"),
                    g("would require", "필요로 할 것이다"), g("a high degree of analytical thought", "높은 수준의 분석적 생각"),
                    g("that thinking style", "그런 생각 방식"), g("is not as big a factor", "그만큼 큰 요소가 아니다"),
                    g("during the performance", "연주하는 동안")],
        "slashes": ["the process of learning", "the fundamentals of jazz", "would require", "analytical thought,", "that thinking style",
                    "as big a factor"],
        "roles": [r("the process", "S"), r("would require", "V"), r("a high degree of analytical thought", "O"), r("that thinking style", "S"),
                  r("is not", "V"), r("as big a factor", "C")],
        "steps": [
            show("b2_perf", "재즈 기초를 배울 땐 분석적 생각이 많이 필요하지만, 연주하는 동안엔 그게 큰 요소가 아니래요. 재즈 쪽 이야기를 마무리해요.",
                 highlight=["although", "not as big a factor", "during the performance"],
                 tips=[tip("although", "'비록 ~이지만'이에요. although 뒤(배울 땐 분석이 필요)보다 콤마 뒤(연주 중엔 아니다)가 하고 싶은 말이에요.", "although")]),
            choice("b2_next",
                   "재즈 쪽 이야기를 마쳤어요. (B) 다음엔 무엇이 오기 쉬울까요?",
                   [("o0", "스펙트럼의 반대쪽(분석적 생각이 큰 쪽) 이야기", True), ("o1", "'대신 그는 오랜 시간 분석했다'는 말", False),
                    ("o2", "주어진 글의 처음 내용", False)],
                   "주어진 글에서 스펙트럼의 '한쪽 끝'을 말했어요. 한쪽을 다 말했으면 다음은 어디일까요?",
                   why="한쪽 끝(재즈) 이야기가 끝났으니, 다음엔 다른 끝 이야기가 오기 쉬워요. '대신 그는'의 he(한 사람)는 재즈 음악가들(they)을 받을 수 없어요."),
        ],
    },
    {
        "id": 6, "text": C1, "teaching_value": "high",
        "model_translation": "(C) 대신, 그는 과학자가 통찰력의 기원으로부터 이론을 만들어 낼 때 그러하듯, 그의 무의식에 떠오른 생각들을 분석하고 재작업하는 데 길고 힘든 시간을 보냈다.",
        "glosses": [g("Instead", "대신에"), g("he spent long, hard hours", "그는 길고 힘든 시간을 보냈다"),
                    g("analyzing and reworking", "분석하고 다시 다듬는 데"), g("the ideas", "생각들"),
                    g("that arose in his unconscious", "그의 무의식에서 떠오른"), g("much as a scientist does", "과학자가 그러듯이"),
                    g("when producing a theory", "이론을 만들 때"), g("from a germ of insight", "통찰의 싹에서")],
        "slashes": ["Instead,", "hard hours", "the ideas", "his unconscious,", "a scientist does", "producing a theory"],
        "roles": [r("he", "S"), r("spent", "V"), r("long, hard hours", "O"), r("a scientist", "S"), r("does", "V")],
        "modifiers": ["that arose in his unconscious"],
        "steps": [
            choice("c_before",
                   "(C)는 'Instead, he spent long, hard hours analyzing …'으로 시작해요. he와 Instead(대신)가 받을 말은 무엇일까요?",
                   [("o0", "재즈 음악가들, 그리고 '억제를 낮춘다'는 말", False), ("o1", "주어진 글의 '창의적인 일들'", False),
                    ("o2", "모차르트, 그리고 '저절로 나온 게 아니다'라는 말", True)],
                   "he는 한 사람이에요. 그리고 Instead(대신)는 앞에 '~가 아니다'라는 말이 있어야 써요.",
                   why="he(한 사람, his unconscious)는 모차르트예요. Instead는 앞의 '저절로 나온 게 아니다(did not appear spontaneously)'를 받아 '대신 오랜 시간 분석했다'로 이어져요.",
                   highlight=["Instead", "he"],
                   tips=[tip("Instead", "'그 대신'이에요. 앞에 부정(not, never)이 오고, Instead 뒤에 실제로 한 일이 와요.", "Instead")],
                   point="(C) Instead, he = 모차르트, '저절로가 아니다' 대신 ← (A) 끝"),
            show("c_analyze", "모차르트는 무의식에서 떠오른 생각을 오랜 시간 분석하고 다듬었대요. 칠판 오른쪽(분석적 생각) 쪽이에요.",
                 panel=board([("unconscious flexible thinking", "무의식·유연"), ("jazz musicians", "재즈 음악가")],
                             [("analytical thinking", "분석적"), ("those who compose complex forms", "복잡한 곡의 작곡가"),
                              ("Mozart: analyzing and reworking", "모차르트: 분석·다듬기")],
                             fresh=("Mozart: analyzing and reworking",))),
        ],
    },
    {
        "id": 7, "text": C2, "teaching_value": "low",
        "model_translation": "모차르트의 말대로, '나는 음악에 몰두한다… 나는 그것에 대해 하루 종일 생각하고, 나는 시도하고, 공부하고, 성찰하는 것을 좋아한다…'",
        "glosses": [g("In Mozart’s own words", "모차르트 자신의 말로"), g("I immerse myself in music", "나는 음악에 몰두한다"),
                    g("I think about it all day long", "나는 하루 종일 그것을 생각한다"), g("I like experimenting", "나는 실험하기를 좋아한다"),
                    g("studying", "공부하기"), g("reflecting", "곰곰이 생각하기")],
        "slashes": ["own words:", "in music...", "all day long―"],
        "roles": [r("I … I … I", "S"), r("immerse", "V"), r("myself", "O"), r("think", "V"), r("like", "V")],
        "steps": [
            order_link(
                card("given", "주어진 글", last=("… at one end of the creative spectrum are improvisational artists, such as jazz musicians",
                                               "스펙트럼의 한쪽 끝에는 재즈 음악가 같은 즉흥 연주가")),
                [card("A", "(A)", first=("On the other end of the spectrum are those who compose …", "스펙트럼의 다른 끝에는 작곡가들이 있다"),
                      last=("… even Mozart’s creations did not appear spontaneously …", "모차르트의 작품도 저절로 나온 게 아니다")),
                 card("B", "(B)", first=("They have to be particularly talented at lowering their inhibitions …", "그들은 억제를 낮추는 데 재능이 있어야 한다"),
                      last=("… that thinking style is not as big a factor during the performance", "연주 중엔 분석적 생각이 큰 요소가 아니다")),
                 card("C", "(C)", first=("Instead, he spent long, hard hours analyzing …", "대신 그는 오랜 시간 분석했다"),
                      last=("In Mozart’s own words: “I immerse myself in music …”", "모차르트의 말: 나는 음악에 몰두한다"))],
                ["B", "A", "C"],
                "주어진 글(한쪽 끝: 재즈 음악가) → (B) They(재즈 음악가) → (A) the other end(작곡가), 모차르트도 저절로가 아니다 → (C) Instead, he(모차르트) 순서예요."),
            show("c_go", "직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?", button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 3, [m("We know", "우리는 안다"), " — ", m("even Mozart’s creations", "모차르트의 작품조차"), " ", m("did not appear spontaneously", "저절로 나타나지 않았다"),
                         "는 걸, ", m("as the myths about him portray", "그에 관한 전설이 그리듯"), " 그렇게."],
          match_display="We know that even Mozart’s creations did not appear spontaneously, as the myths about him portray.",
          sv_new=sv_step("s3_basic_sv", ["We", "know", "Mozart’s creations", "did not appear"], {"We": "S", "know": "V"},
                         {"Mozart’s creations": "그건 that 뒤 덩어리 안의 주어예요(무엇을 아는지).", "did not appear": "그건 that 뒤 덩어리 안의 동사예요."},
                         "주어는 We, 동사는 know예요. that 뒤가 아는 내용이에요."),
          meaning_after="a2_myth")
add_basic(sentences, 4, [m("They", "그들은"), " ", m("lowering their inhibitions", "억제를 낮추는 것"), "에 ", m("particularly talented at", "특히 재능이 있어"), " ",
                         m("have to be", "야 한다"), "."],
          sv_new=sv_step("s4_basic_sv", ["They", "have to be", "particularly talented", "their inhibitions"],
                         {"They": "S", "have to be": "V", "particularly talented": "C"},
                         {"their inhibitions": "그건 lowering(낮추는 것)의 대상이에요."},
                         "주어는 They, 동사는 have to be, 보어는 particularly talented예요."),
          meaning_after="b_before",
          meaning="그들(재즈 음악가)은 거리낌을 낮추고 무의식에서 떠오른 생각을 받아들이는 데 특히 재능이 있어야 한대요.")
add_basic(sentences, 5, [m("And although", "비록 ~이지만"), " 재즈 기초를 배울 땐 ", m("a high degree of analytical thought", "높은 수준의 분석적 생각"), "이 필요해도, ",
                         m("that thinking style", "그런 생각 방식은"), " ", m("during the performance", "연주하는 동안"), " ", m("is not as big a factor", "그만큼 큰 요소가 아니다"), "."],
          sv_new=sv_step("s5_basic_sv", ["the process", "would require", "that thinking style", "is not"],
                         {"that thinking style": "S", "is not": "V"},
                         {"the process": "그건 although 덩어리 안의 주어예요.", "would require": "그건 although 덩어리 안의 동사예요."},
                         "콤마 뒤 메인 문장은 주어 that thinking style, 동사 is not이에요."),
          meaning_ids=["b2_perf"])
add_basic(sentences, 7, [m("In Mozart’s own words", "모차르트 자신의 말로"), ": ", m("I immerse myself in music", "나는 음악에 몰두한다"), ". ",
                         m("I think about it all day long", "나는 하루 종일 그것을 생각한다"), "."],
          sv_new=sv_step("s7_basic_sv", ["I", "immerse", "myself", "music"], {"I": "S", "immerse": "V", "myself": "O"},
                         {"music": "그건 in 뒤 덩어리예요."}, "따옴표 안 첫 문장은 주어 I, 동사 immerse, 목적어 myself예요(나 자신을 몰두시키다)."))

SENSES = {
    1: [sense("to", "ability to adjust", "~할 (능력)", "명사 + to부정사"),
        sense("for", "for example", "(for example의 일부)", "for example = 예를 들어"),
        sense("as", "such as jazz musicians", "~ 같은", "such as + 명사 (예시)")],
    2: [sense("as", "such as a symphony", "~ 같은", "such as + 명사 (예시)"),
        sense("that", "concerto, that require", "(앞 명사 complex forms를 꾸밈)", "관계대명사 that + 동사"),
        sense("but", "but also careful planning", "~도 (not just A but also B)", "not just A but also B")],
    3: [sense("for", "for example", "(for example의 일부)", "for example = 예를 들어"),
        sense("that", "that even Mozart’s creations", "~라는 것을", "명사절 that (know that …)"),
        sense("as", "as the myths", "~하듯이", "접속사 as + 주어·동사 (방식)")],
    4: [sense("to", "have to be", "~해야 (하다)", "have to + 동사원형")],
    5: [sense("that", "that thinking style", "그", "지시형용사 that + 명사"),
        sense("as", "not as big a factor", "그만큼", "not as + 형용사 (+ a + 명사) = 그만큼 ~하지 않은")],
    6: [sense("that", "ideas that arose", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("as", "much as a scientist does", "~처럼, ~하듯이", "much as + 주어·동사 = 꼭 ~하듯")],
}

WORDS = {"different": "서로 다른", "creative": "창의적인", "pursuits": "일, 활동", "varying": "다양한", "degrees": "정도",
         "unconscious": "무의식적인, 무의식", "flexible": "유연한", "thinking": "생각", "combination": "결합", "conscious": "의식적인",
         "ability": "능력", "adjust": "조정하다", "shape": "다듬다", "analytical": "분석적인", "music": "음악", "end": "끝",
         "spectrum": "스펙트럼, 범위", "improvisational": "즉흥적인", "artists": "예술가, 연주가", "jazz": "재즈", "musicians": "음악가",
         "compose": "작곡하다", "complex": "복잡한", "forms": "형식", "symphony": "교향곡", "concerto": "협주곡", "imagination": "상상력",
         "careful": "꼼꼼한", "planning": "계획", "exacting": "고된, 까다로운", "editing": "편집", "letters": "편지", "reports": "기록, 보고",
         "others": "다른 사람들", "mozart’s": "모차르트의", "creations": "작품", "appear": "나타나다", "spontaneously": "저절로, 즉흥적으로",
         "wholly": "완전히", "formed": "만들어진", "consciousness": "의식", "myths": "전설, 신화", "portray": "그리다, 묘사하다",
         "particularly": "특히", "talented": "재능 있는", "lowering": "낮추는 것", "inhibitions": "억제", "letting": "들이는 것",
         "unconsciously": "무의식적으로", "generated": "만들어진", "ideas": "생각들", "process": "과정", "learning": "배우는 것",
         "fundamentals": "기초", "high": "높은", "degree": "정도", "thought": "생각", "style": "방식", "big": "큰", "factor": "요소",
         "performance": "연주", "spent": "보냈다", "long": "긴", "hard": "힘든", "hours": "시간", "analyzing": "분석하는 것",
         "reworking": "다시 다듬는 것", "arose": "떠올랐다", "scientist": "과학자", "producing": "만드는 것", "theory": "이론",
         "germ": "싹, 시작", "insight": "통찰", "words": "말", "immerse": "몰두시키다", "myself": "나 자신", "day": "날", "experimenting": "실험하기",
         "studying": "공부하기", "reflecting": "곰곰이 생각하기", "instead": "대신에", "know": "알다", "music.": "음악", "require": "필요로 하다",
         "although": "비록 ~이지만", "particularly talented": "특히 재능 있는"}

OPTIONS = [("1", "(A)-(C)-(B)", False), ("2", "(B)-(A)-(C)", True), ("3", "(B)-(C)-(A)", False), ("4", "(C)-(A)-(B)", False), ("5", "(C)-(B)-(A)", False)]
exam = {
    "question": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은? [3점]",
    "sentence": 1, "analysis_first": True, "wrong_rate": 38.9, "wrong_rank": 15, "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], **({"correct": True} if o[2] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "단락 첫머리 단서(They, On the other end, Instead, he)를 떠올리며 순서를 골라 봐요.",
        "정답이에요! 한쪽 끝의 재즈 음악가 → (B) They(재즈 음악가)의 특징 → (A) 다른 끝의 작곡가, 모차르트도 저절로가 아니다 → (C) Instead, he(모차르트)는 오래 분석했다, 순서예요.",
        "정답은 ② (B)-(A)-(C)예요.",
        {"1": "(A) 'the other end'가 주어진 글 바로 뒤에 오면, 재즈 음악가를 받는 (B) They가 뒤로 밀려 엉뚱한 사람을 가리켜요.",
         "3": "많이 고른 오답이에요. (C)의 he는 한 사람(모차르트)이라 (B)의 재즈 음악가들(they)을 받을 수 없어요.",
         "4": "(C)의 he와 Instead가 받을 '모차르트도 저절로가 아니다'가 주어진 글에는 없어요.",
         "5": "(C)가 맨 앞에 오면 he가 누구인지 알 수 없어요."},
        {"3": review(20.6,
                     "(B) 끝이 '연주 중엔 분석적 생각이 큰 요소가 아니다'라서, (C) 'Instead, he … analyzing'을 붙이고 싶었을 거예요. 하지만 he는 한 사람(his unconscious)이라 (B)의 재즈 음악가들(they)을 받을 수 없어요. he가 받을 모차르트는 (A) 끝에 처음 나와요.",
                     panel=rows(("(B) 끝", "They … that thinking style is not as big a factor", "재즈 음악가들(they)", "hl"),
                                ("(C) 첫머리", "Instead, he spent long, hard hours", "he = 한 사람 = 모차르트 ← (A) 끝", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 36번 (글의 순서, 3점)",
    topic="순서 푸는 법: 주어진 글의 끝 → 단락 첫머리 단서로 앞 내용 예측 → 단락 끝으로 다음 내용 예측 → 순서 잇기",
    method={"type": "order", "labels": ["단락 요지 잡기", "연결 단서 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-creative-spectrum.svg", ("Jazz", "즉흥 연주"), "↔", ("Mozart", "작곡"),
                                       "창의성은 번뜩임일까, 오랜 분석일까?", "2024년 3월 36번 도입 칠판"),
                      "alt": "칠판: Jazz(즉흥 연주) ↔ Mozart(작곡)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "모차르트의 곡은 머릿속에서 한 번에 완성됐을까요? 이번 글은 창의적인 일에 필요한 두 가지 생각을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "순서 문제는 단락 첫머리의 단서가 앞 내용과 이어지는지 보는 거예요. They, he, Instead 같은 말이 무엇을 받는지 찾아볼게요."}}],
    exam=exam,
    key_words={"passage": [g("pursuit", "일, 활동"), g("varying", "다양한"), g("flexible", "유연한"), g("in combination with", "~와 결합하여"),
                           g("analytical", "분석적인"), g("spectrum", "스펙트럼, 범위"), g("compose", "작곡하다"), g("exacting", "고된, 까다로운"),
                           g("spontaneously", "저절로"), g("portray", "그리다"), g("inhibition", "억제"), g("fundamental", "기초"),
                           g("factor", "요소"), g("insight", "통찰"), g("reflect", "곰곰이 생각하다")],
               "options": []},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# exacting 고된, 엄격한 · germ 싹, 기원.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    2: [tip("exacting", "이 글에서는 → 고된, 엄격한  ('정확한(exact)' 아님)", "exacting", trap=True)],
    6: [tip("germ", "이 글에서는 → 싹, 기원  ('세균' 아님)", "germ", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="순서 푸는 법",
       chunks={"Different creative pursuits": "서로 다른 창의적인 일들", "require": "필요로 하다",
               "varying degrees of unconscious flexible thinking": "다양한 정도의 무의식적이고 유연한 생각", "the creative spectrum": "창의성의 스펙트럼",
               "are": "있다", "improvisational artists": "즉흥 연주가들", "We": "우리는", "know": "안다", "Mozart’s creations": "모차르트의 작품",
               "did not appear": "나타나지 않았다", "They": "그들은", "have to be": "~여야 한다", "particularly talented": "특히 재능 있는",
               "their inhibitions": "그들의 억제", "the process": "과정", "would require": "필요로 할 것이다", "that thinking style": "그런 생각 방식",
               "is not": "~이 아니다", "I": "나는", "immerse": "몰두시키다", "myself": "나 자신", "music": "음악",
               "We know": "우리는 안다", "even Mozart’s creations": "모차르트의 작품조차", "did not appear spontaneously": "저절로 나타나지 않았다",
               "as the myths about him portray": "그에 관한 전설이 그리듯", "lowering their inhibitions": "억제를 낮추는 것",
               "particularly talented at": "특히 ~에 재능이 있는", "And although": "그리고 비록 ~이지만",
               "a high degree of analytical thought": "높은 수준의 분석적 생각", "during the performance": "연주하는 동안",
               "is not as big a factor": "그만큼 큰 요소가 아니다", "In Mozart’s own words": "모차르트 자신의 말로",
               "I immerse myself in music": "나는 음악에 몰두한다", "I think about it all day long": "나는 하루 종일 그것을 생각한다"})
