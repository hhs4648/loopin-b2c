"""2026년 9월 모의평가(2027학년도) 39번 레슨 + 대사를 만든다 (주어진 문장 넣기, 3점). 오답률 41% · Top 6 (메가스터디).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_39.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/insertion.md — 주어진 문장 상황 → 단서(However · melody alone) → 앞에 올 내용 → ①~⑤ 흐름 확인 → 정답 열쇠.
정답 ③. 주어진 문장: However, melody alone would not normally keep the listener’s attention for long because a piece of music needs
some variety and contrasting elements from time to time.
열쇠 — ① However + melody alone: 앞에는 「선율에 집중하려면 대조되는 변화를 줄여야 한다」(②~③ 사이 For instance 문장)가 와야 한다.
② ③ 뒤 「반복과 다양성(diversity)의 균형」은 앞에 다양성이 필요하다는 말이 있어야 하는데 ③ 앞 문장엔 없다 → 주어진 문장의
variety and contrasting elements가 받아 준다.
선택률(메가스터디): ① 2 · ② 13 · ③ 59 · ④ 19 · ⑤ 7 — 많이 고른 오답 ④(contrasting elements ↔ ④ 뒤 contrasts가 비슷해 보임),
②(For instance 앞) 둘 다 option_review.
주어진 문장 정석(insertion-given-sentence-order): However가 무엇과 맞서는지 → melody alone이 받을 말 → 그러니 앞에는 선율에 집중하라는 말.
「뒤에 무엇?」은 묻지 않는다. diversity 이야기는 ③ 자리 흐름 확인과 그 뒤 「정답 열쇠」(s5_key)에서만 다룬다.
timbre는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다(문장 뜻에만 둔다).
해설지(content/tutor/exam-source/2027-09-평가원/해설.txt) 해석과 대조함 — parameter 요소, should be accompanied by 틀림없이 동반한다,
beyond which 이를 넘어서면, perceived as lacking order or direction 질서나 방향성이 결여된 것으로 인식, pitch 음의 높낮이,
콜론(:) 뒤 「그 이유는 ~ 때문이다」, this unfolding 이러한 전개, results from ~에서 비롯된다, be preceded by 선행되다, builds upon 기반으로 한다.
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음), 「앞과 반대」 Tip은 맞힌 뒤에만(praise_tips).
Claude 초안(2026-10-21) — 선생님 검토 전.

선생님이 확인할 점
1. 단서를 However · melody alone 두 개로 찾게 했다(g_clue). 해설지 풀이도 「앞에는 선율에 집중하도록 … 변화를 피해야 한다는 내용」이라고 한다.
2. 앞 내용 그림은 대조 칠판(contrast: 선율에 집중 → 변화 줄이기 ↔ However 선율만으로는 부족 → 변화 필요)으로 했다. 따로 그림(svg)은 만들지 않았다.
3. ③ 자리 끊김 뒤 「정답 열쇠」(s5_key)는 주어진 문장을 띄워(display) diversity와 같은 뜻의 말을 고르게 했다 — 답이 보이는 화면이라 너무 쉬우면 빼도 된다.
4. 헷갈리는 단어(trap): piece(한 곡, 조각 X) · certain(특정한, 확실한 X) · order(질서, 주문·순서 X) · pitch(음의 높낮이, 던지다 X). 엑셀에는 안 넣었다.
5. 해석 맞추기는 ⑤ 뒤 문장(Such contrasts …)에만 넣었다.
6. 많이 고른 오답 ④는 「주어진 문장의 contrasting elements와 ④ 뒤 contrasts가 비슷해 보여서」로 봤다(추측).
7. 끊어읽기 roles: 1문장(If … then one should avoid …; otherwise …)은 if·while 절 S·V까지 쳤다. 관계사 whereby/beyond which·which·that·where 절은 [ ].
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, tip, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-09-39-musical-attention"

GIVEN = ("However, melody alone would not normally keep the listener’s attention for long because a piece of music needs some "
         "variety and contrasting elements from time to time.")
S = [
    "Regardless of musical style, an increase of focus on certain parameters in a musical passage should be accompanied by a "
    "decrease in focus on others.",
    "(①) The human mind has an attention limit, beyond which music is most likely to be perceived as lacking order or direction.",
    "(②) For instance, if the intention is to focus on melodic lines, then one should avoid making too many contrasting timbre "
    "variations while the melodies are unfolding; otherwise, the timbre may distract attention away from the pitch.",
    "(③) One of the most difficult issues in the practice of composition is to find the right balance between repetition and "
    "diversity: a well-balanced piece of music should unfold naturally to listeners.",
    "(④) In most Western musical styles, this unfolding results from a network of relationships between musical attributes that "
    "combine in different ways to create situations where contrasts can take place.",
    "(⑤) Such contrasts are normally preceded by a preparatory stage, which builds upon the listener’s expectations.",
]
# 해설지 해석 (2027-09-평가원/해설.txt 39번)
KO_GIVEN = ("하지만 선율만으로는 보통 듣는 사람의 주의를 오랫동안 끌지 못할 것인데, 그 이유는 음악 한 곡은 때때로 어느 정도의 다양성과 "
            "대조적인 요소들을 필요로 하기 때문이다.")
KO = [
    "음악 양식과 상관없이, 음악의 한 악절에서 특정 요소에 대한 집중도의 상승은 다른 요소에 대한 집중도의 감소를 틀림없이 동반한다.",
    "인간의 정신에는 주의력의 한계가 있으며, 이를 넘어서면 음악은 질서나 방향성이 결여된 것으로 인식될 가능성이 매우 높다.",
    "예를 들어, 의도가 선율에 집중하는 것이라면, 멜로디가 전개되는 동안 대조되는 음색 변화를 너무 많이 만드는 것을 피해야 하는데, "
    "그렇지 않으면 음색이 주의를 음의 높낮이로부터 딴 데로 돌리게 만들 수 있다.",
    "작곡 실무에서 가장 어려운 문제 중 하나는 반복과 다양성 사이의 적절한 균형을 찾는 것인데, 그 이유는 균형이 잘 잡힌 음악 한 곡은 "
    "듣는 사람에게 자연스럽게 전개되어야 하기 때문이다.",
    "대부분의 서양 음악 양식에서, 이러한 전개는 대조가 일어날 수 있는 상황을 만들어 내기 위해 다양한 방식으로 결합되는 음악적 속성들 간의 "
    "관계망에서 비롯된다.",
    "그러한 대조에는 일반적으로 준비 단계가 선행되는데, 이는 듣는 사람의 기대감을 기반으로 한다.",
]


def flow(id, place, before, after, ok, why, praise="맞아요!"):
    """①~⑤ 자리마다 — 앞 문장과 뒤 문장이 그대로 이어지나. 끊김은 정답 자리 하나뿐"""
    return choice(id, f"{place} 자리예요. '{before}' → '{after}', 자연스럽게 이어지나요?",
                  [("o0", "네, 이어져요", ok), ("o1", "아니요, 끊겨요", not ok)], why, why=why, praise=praise,
                  highlight=[f"({place})"], method=2)


sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN, "model_translation": KO_GIVEN, "teaching_value": "high",
        "glosses": [g("However", "하지만"), g("melody alone", "선율만으로는"), g("melody", "선율, 멜로디"), g("alone", "~만으로"),
                    g("would not normally keep", "보통 붙잡아 두지 못할 것이다"), g("normally", "보통"), g("keep", "유지하다, 붙잡아 두다"),
                    g("the listener’s attention", "듣는 사람의 주의"), g("listener’s", "듣는 사람의"), g("attention", "주의, 관심"),
                    g("for long", "오랫동안"), g("a piece of music", "음악 한 곡"), g("piece", "(음악·글) 한 편, 한 곡"),
                    g("music", "음악"), g("needs", "필요로 하다"), g("some variety", "어느 정도의 다양성"), g("variety", "다양성, 변화"),
                    g("contrasting elements", "대조적인 요소들"), g("contrasting", "대조되는"), g("elements", "요소"),
                    g("from time to time", "때때로")],
        "emphasis": ["However", "melody alone", "variety"],
        "slashes": ["However,", "melody alone", "the listener’s attention", "for long", "a piece of music", "contrasting elements"],
        "roles": [r("melody alone", "S"), r("would not normally keep", "V"), r("the listener’s attention", "O"),
                  r("a piece of music", "S"), r("needs", "V")],
        "steps": [
            choice("g_situation",
                   "주어진 문장은 무슨 말일까요?",
                   [("o0", "선율만으로는 주의를 오래 끌지 못한다, 음악에는 가끔 변화가 필요하기 때문이다", True),
                    ("o1", "선율만 있어도 듣는 사람은 오래 집중한다, 변화는 방해가 되기 때문이다", False),
                    ("o2", "음악에는 변화보다 반복이 더 필요하다", False)],
                   "would not keep ~ for long은 '오래 붙잡아 두지 못한다'예요. because 뒤에 이유가 나와요.",
                   why="'melody alone would not normally keep the listener’s attention for long', 선율만으로는 주의를 오래 끌지 못한대요. 음악에는 때때로 다양성과 대조적인 요소가 필요하니까요.",
                   highlight=["melody alone", "for long", "variety"],
                   tips=[tip("A alone", "'A만으로는'이에요. melody alone = 선율만으로는.", "melody alone"),
                         tip("from time to time", "'때때로, 가끔'이에요.", "from time to time")],
                   point="주어진 문장 = 하지만 선율만으로는 주의를 오래 못 끈다 (음악엔 때때로 다양성·대조가 필요)"),
            pick("g_clue", "앞 문장과 이어 주는 단서 두 개를 찾아 눌러 볼까요?",
                 ["However", "melody alone", "the listener’s attention", "from time to time"], ["However", "melody alone"],
                 "그건 이 문장 안에서 뜻이 끝나는 말이에요. 앞 문장이 무슨 이야기였는지 알려 주는 말을 찾아봐요.",
                 "However(하지만)는 앞과 반대 방향으로 간다는 뜻이고, melody alone(선율만으로는)은 앞에 선율 이야기가 있었다는 뜻이에요.",
                 praise="다 찾았어요!",
                 wrong_by={"the listener’s attention": "the listener’s attention은 이 문장이 새로 하는 말이에요. 앞 이야기와 잇는 말을 찾아봐요.",
                           "from time to time": "from time to time은 '때때로'예요. 앞 문장과 잇는 말을 찾아봐요."},
                 praise_tips=[{"label": "However", "text": "However(하지만)가 맨 앞에 오면, 바로 앞 문장은 이 문장과 반대 방향의 말이어야 해요."}],
                 point="단서 = However(앞과 반대) · melody alone(앞에 선율 이야기)"),
            choice("g_before",
                   "그럼 이 문장 바로 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "선율에 집중하려면 다른 변화를 줄여야 한다는 내용", True),
                    ("o1", "음악에는 다양한 변화가 꼭 필요하다는 내용", False),
                    ("o2", "작곡할 때 균형을 찾기가 어렵다는 내용", False)],
                   "However(하지만)는 앞과 반대 방향이에요. 이 문장은 '변화가 필요하다'고 하니, 앞은 그 반대쪽이에요.",
                   why="이 문장이 However로 '선율만으로는 부족하다, 변화가 필요하다'고 하니, 앞에는 그 반대로 선율에 집중하고 변화를 줄이라는 말이 와요.",
                   highlight=["However", "melody alone"],
                   point="주어진 문장 앞 = 선율에 집중하라, 변화는 줄여라 (However · melody alone)"),
            show("g_before_note",
                 "지문을 읽으며 선율에 집중하라는 문장을 찾아봐요.",
                 panel={"kind": "contrast", "title": "However → 앞과 반대", "between": "↔",
                        "left": {"title": "바로 앞 문장 (찾을 곳)", "text": "melody에 집중 → 변화는 줄이기"},
                        "right": {"title": "주어진 문장", "text": "However, melody alone → 변화(variety)가 필요"}},
                 highlight=["However"], button="지문 읽어 볼게요"),
        ],
    },
    {
        "id": 2, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("Regardless of musical style", "음악 양식과 상관없이"), g("Regardless of", "~와 상관없이"),
                    g("musical", "음악의"), g("style", "양식, 스타일"), g("an increase of focus", "집중의 증가"),
                    g("increase", "증가, 상승"), g("focus", "집중"), g("on certain parameters", "특정 요소에 대한"),
                    g("certain", "특정한"), g("parameters", "요소"), g("in a musical passage", "음악의 한 악절에서"),
                    g("passage", "악절, (음악의) 한 부분"), g("should be accompanied by", "~을 (틀림없이) 동반한다"),
                    g("accompanied", "동반된"), g("a decrease", "감소"), g("decrease", "감소"),
                    g("in focus on others", "다른 요소에 대한 집중의"), g("others", "다른 것들(다른 요소)")],
        "slashes": ["Regardless of musical style,", "an increase of focus", "certain parameters", "in a musical passage",
                    "should be accompanied", "by a decrease"],
        "roles": [r("an increase of focus on certain parameters in a musical passage", "S"), r("should be accompanied", "V")],
        "steps": [
            choice("s2_mean",
                   "이 문장은 무슨 말일까요?",
                   [("o0", "어떤 요소에 더 집중하면 다른 요소에는 덜 집중하게 된다", True),
                    ("o1", "모든 요소에 똑같이 집중해야 한다", False),
                    ("o2", "한 요소에 집중하면 다른 요소에도 더 집중하게 된다", False)],
                   "an increase(증가)와 a decrease(감소)를 봐요. be accompanied by는 '~을 동반하다'예요.",
                   why="'an increase of focus on certain parameters … accompanied by a decrease in focus on others', 특정 요소에 더 집중하면 다른 요소에 대한 집중은 줄어든대요.",
                   highlight=["increase", "decrease"],
                   tips=[tip("A is accompanied by B", "'A에는 B가 따른다, A는 B를 동반한다'예요.", "should be accompanied by"),
                         tip("Regardless of", "'~와 상관없이'예요.", "Regardless of")]),
        ],
    },
    {
        "id": 3, "text": S[1], "model_translation": KO[1], "teaching_value": "medium",
        "glosses": [g("The human mind", "인간의 정신"), g("human", "인간의"), g("mind", "정신, 마음"),
                    g("an attention limit", "주의력의 한계"), g("attention", "주의"), g("limit", "한계"),
                    g("beyond which", "그것(그 한계)을 넘어서면"), g("beyond", "~을 넘어서"), g("music", "음악"),
                    g("is most likely to be perceived", "~로 인식될 가능성이 매우 높다"), g("likely", "~할 것 같은"),
                    g("perceived", "인식된, 받아들여진"), g("as lacking order or direction", "질서나 방향성이 없는 것으로"),
                    g("lacking", "~이 없는, 부족한"), g("order", "질서"), g("direction", "방향(성)")],
        "slashes": ["an attention limit,", "beyond which music", "most likely", "be perceived"],
        "roles": [r("The human mind", "S"), r("has", "V"), r("an attention limit", "O")],
        "modifiers": ["beyond which music is most likely to be perceived as lacking order or direction"],
        "steps": [
            choice("s3_mean",
                   "주의력의 한계를 넘어서면 음악은 어떻게 들린대요?",
                   [("o0", "질서나 방향이 없는 것처럼 들린다", True), ("o1", "더 질서 있게 들린다", False),
                    ("o2", "더 아름답게 들린다", False)],
                   "beyond which는 '그 한계를 넘어서면'이에요. lacking은 '~이 없는'이에요.",
                   why="'perceived as lacking order or direction', 질서나 방향이 없는 것으로 받아들여진대요. 한꺼번에 너무 많은 데 집중할 수는 없다는 말이에요.",
                   highlight=["beyond which", "lacking order or direction"],
                   tips=[tip("be perceived as ~", "'~로 인식되다, ~로 받아들여지다'예요.", "is most likely to be perceived")]),
            flow("s3_flow", "①", "한 요소에 더 집중하면 다른 요소엔 덜 집중하게 된다", "인간의 정신에는 주의력의 한계가 있다", True,
                 "왜 한쪽을 늘리면 다른 쪽을 줄여야 하는지, 주의력의 한계로 이유를 대요. 그대로 이어져요."),
        ],
    },
    {
        "id": 4, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("For instance", "예를 들어"), g("the intention", "의도"), g("intention", "의도"),
                    g("to focus on melodic lines", "선율에 집중하는 것"), g("focus", "집중하다"), g("melodic lines", "선율"),
                    g("melodic", "선율의"), g("lines", "선, (음악의) 가락"), g("then", "그러면"), g("one", "(일반적인) 사람"),
                    g("should avoid", "피해야 한다"), g("avoid", "피하다"),
                    g("making too many contrasting timbre variations", "대조되는 음색 변화를 너무 많이 만드는 것"),
                    g("making", "만드는 것"), g("too many", "너무 많은"), g("contrasting", "대조되는"),
                    g("timbre", "음색 (시험지 아래 풀이)"), g("variations", "변화"), g("the melodies", "멜로디"),
                    g("melodies", "멜로디"), g("are unfolding", "전개되고 있다, 펼쳐지고 있다"), g("unfolding", "펼쳐지는, 전개되는"),
                    g("otherwise", "그렇지 않으면"), g("the timbre", "음색"), g("may distract", "(주의를) 딴 데로 돌릴 수 있다"),
                    g("distract", "(주의를) 딴 데로 돌리다"), g("attention", "주의"), g("away from the pitch", "음의 높낮이로부터"),
                    g("away", "떨어져"), g("pitch", "음의 높낮이")],
        "slashes": ["For instance,", "if the intention is", "melodic lines,", "then one should avoid", "contrasting timbre variations",
                    "are unfolding;", "otherwise,", "distract attention"],
        "roles": [r("the intention", "S"), r("is", "V"), r("to focus on melodic lines", "C"), r("one", "S"), r("should avoid", "V"),
                  r("making too many contrasting timbre variations", "O"), r("the melodies", "S"), r("are unfolding", "V"),
                  r("the timbre", "S"), r("may distract", "V"), r("attention", "O")],
        "steps": [
            choice("s4_mean",
                   "선율에 집중하려면 무엇을 피해야 한대요?",
                   [("o0", "대조되는 음색 변화를 너무 많이 만드는 것", True), ("o1", "같은 선율을 되풀이하는 것", False),
                    ("o2", "음의 높낮이를 바꾸는 것", False)],
                   "should avoid 바로 뒤를 봐요. timbre는 시험지 아래에 '음색'으로 풀어 줬어요.",
                   why="'avoid making too many contrasting timbre variations', 대조되는 음색 변화를 너무 많이 만들지 말래요. 그러지 않으면 음색이 주의를 딴 데로 돌린대요.",
                   highlight=["should avoid", "contrasting timbre variations"],
                   tips=[tip("otherwise", "'그렇지 않으면'이에요. 앞에서 하라고 한 것을 안 했을 때 생기는 일이 뒤에 와요.", "otherwise")]),
            flow("s4_flow", "②", "인간의 정신에는 주의력의 한계가 있다", "예를 들어, 선율에 집중하려면 음색 변화를 줄여야 한다", True,
                 "For instance(예를 들어)로 '한쪽에 집중하면 다른 쪽은 줄인다'의 예를 들어요. 그대로 이어져요."),
        ],
    },
    {
        "id": 5, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("One of the most difficult issues", "가장 어려운 문제 중 하나"), g("difficult", "어려운"), g("issues", "문제"),
                    g("in the practice of composition", "작곡 실무에서"), g("practice", "실무, 실제로 하는 일"),
                    g("composition", "작곡"), g("to find the right balance", "적절한 균형을 찾는 것"), g("find", "찾다"),
                    g("right", "적절한, 알맞은"), g("balance", "균형"), g("between repetition and diversity", "반복과 다양성 사이의"),
                    g("repetition", "반복"), g("diversity", "다양성"), g("a well-balanced piece of music", "균형이 잘 잡힌 음악 한 곡"),
                    g("well-balanced", "균형이 잘 잡힌"), g("piece", "(음악) 한 곡"), g("music", "음악"),
                    g("should unfold naturally", "자연스럽게 펼쳐져야 한다"), g("unfold", "펼쳐지다, 전개되다"),
                    g("naturally", "자연스럽게"), g("listeners", "듣는 사람들")],
        "slashes": ["the most difficult issues", "of composition", "the right balance", "and diversity:", "should unfold naturally"],
        "roles": [r("One of the most difficult issues in the practice of composition", "S"), r("is", "V"),
                  r("to find the right balance between repetition and diversity", "C"), r("a well-balanced piece of music", "S"),
                  r("should unfold", "V")],
        "steps": [
            choice("s5_mean",
                   "작곡에서 가장 어려운 문제 중 하나는 무엇이래요?",
                   [("o0", "반복과 다양성 사이의 알맞은 균형을 찾는 것", True), ("o1", "반복을 모두 없애는 것", False),
                    ("o2", "새 선율을 만들어 내는 것", False)],
                   "is to find ~ 뒤를 봐요. repetition은 '반복', diversity는 '다양성'이에요.",
                   why="'to find the right balance between repetition and diversity', 반복과 다양성 사이에서 알맞은 균형을 찾는 거래요.",
                   highlight=["the right balance", "repetition", "diversity"],
                   tips=[tip("콜론(:)", "콜론 뒤는 앞말을 풀어 주거나 이유를 대요. 여기서는 균형이 왜 중요한지 말해요.", "diversity:")]),
            flow("s5_flow", "③", "선율에 집중하려면 음색 변화를 줄여야 한다", "작곡에서는 반복과 다양성의 균형을 찾기가 어렵다", False,
                 "앞은 변화를 줄이라는 말뿐인데, 갑자기 다양성(diversity)과의 균형이 나와요. 다양성이 왜 필요한지가 빠져 있어서 흐름이 끊겨요.",
                 praise="맞아요! 여기서 흐름이 끊겨요."),
            choice("s5_key",
                   "주어진 문장에서 diversity(다양성)와 같은 쪽의 말은 무엇일까요?",
                   [("o0", "melody alone", False), ("o1", "the listener’s attention", False),
                    ("o2", "variety and contrasting elements", True)],
                   "diversity는 여러 가지로 바뀌는 것이에요. 주어진 문장에서 변화를 뜻하는 말을 찾아봐요.",
                   why="variety(다양성)와 contrasting elements(대조적인 요소)가 diversity와 같은 쪽이에요. 주어진 문장이 다양성이 필요하다고 먼저 말해 줘야 균형 이야기로 이어져요.",
                   display=GIVEN, tag="주어진 문장",
                   point="③ 뒤 diversity(다양성)와의 균형 ← 주어진 문장의 variety and contrasting elements가 먼저 와야"),
        ],
    },
    {
        "id": 6, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("In most Western musical styles", "대부분의 서양 음악 양식에서"), g("most", "대부분의"), g("Western", "서양의"),
                    g("musical", "음악의"), g("styles", "양식"), g("this unfolding", "이러한 전개"), g("unfolding", "전개, 펼쳐짐"),
                    g("results from", "~에서 비롯되다"), g("results", "비롯되다, 생기다"),
                    g("a network of relationships", "관계망"), g("network", "망, 네트워크"), g("relationships", "관계"),
                    g("between musical attributes", "음악적 속성들 사이의"), g("attributes", "속성"),
                    g("combine", "결합되다, 합쳐지다"), g("in different ways", "다양한 방식으로"), g("different", "다른, 다양한"),
                    g("ways", "방식"), g("to create situations", "상황을 만들어 내기 위해"), g("create", "만들어 내다"),
                    g("situations", "상황"), g("contrasts", "대조"), g("can take place", "일어날 수 있다"), g("take place", "일어나다")],
        "slashes": ["musical styles,", "this unfolding results", "a network of relationships", "musical attributes",
                    "in different ways", "to create situations"],
        "roles": [r("this unfolding", "S"), r("results", "V")],
        "modifiers": ["that combine in different ways to create situations", "where contrasts can take place"],
        "steps": [
            choice("s6_this",
                   "'this unfolding(이러한 전개)'은 무엇을 가리킬까요?",
                   [("o0", "음악이 듣는 사람에게 자연스럽게 펼쳐지는 것", True), ("o1", "선율에만 집중하는 것", False),
                    ("o2", "음색이 주의를 딴 데로 돌리는 것", False)],
                   "this(이러한)는 바로 앞 문장에서 말한 것을 가리켜요. 앞 문장 끝의 unfold를 찾아봐요.",
                   why="this unfolding은 바로 앞 문장의 'should unfold naturally to listeners', 음악이 자연스럽게 펼쳐지는 것을 받아요.",
                   highlight=["this unfolding"],
                   tips=[tip("result from / result in", "result from은 '~에서 비롯되다', result in은 '~을 낳다'예요. 뒤에 오는 전치사로 방향이 바뀌어요.",
                             "results from")]),
            flow("s6_flow", "④", "균형 잡힌 음악은 자연스럽게 펼쳐져야 한다", "이러한 전개는 대조가 생기는 관계망에서 나온다", True,
                 "this unfolding(이러한 전개)이 바로 앞 unfold naturally를 받아요. 그대로 이어져요."),
        ],
    },
    {
        "id": 7, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("Such contrasts", "그러한 대조"), g("contrasts", "대조"), g("are normally preceded by", "보통 ~이 앞서 온다"),
                    g("normally", "보통"), g("preceded", "앞서 온, 선행된"), g("a preparatory stage", "준비 단계"),
                    g("preparatory", "준비의"), g("stage", "단계"), g("which builds upon", "그것은 ~을 기반으로 한다"),
                    g("builds upon", "~을 기반으로 하다"), g("builds", "쌓다"), g("the listener’s expectations", "듣는 사람의 기대"),
                    g("listener’s", "듣는 사람의"), g("expectations", "기대")],
        "slashes": ["Such contrasts", "are normally preceded", "a preparatory stage,"],
        "roles": [r("Such contrasts", "S"), r("are normally preceded", "V")],
        "modifiers": ["which builds upon the listener’s expectations"],
        "steps": [
            flow("s7_flow", "⑤", "이러한 전개는 대조가 생기는 상황을 만든다", "그러한 대조 앞에는 보통 준비 단계가 온다", True,
                 "Such contrasts(그러한 대조)가 바로 앞 contrasts can take place를 받아요. 그대로 이어져요."),
            show("s7_go", "①~⑤ 중 흐름이 끊긴 곳은 하나였어요. 주어진 문장의 However와 variety를 떠올리며 골라 봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — ⑤ 뒤 문장(짧은 문장, 모두에게). 덩어리는 문장에 그대로 있는 구절
add_match(sentences, 7, [m("Such contrasts", "그러한 대조에는"), " ", m("a preparatory stage", "준비 단계가"), " ",
                         m("are normally preceded by", "보통 앞서 오는데"), ", ", m("which builds upon", "그것은 ~을 기반으로 한다"),
                         " (", m("the listener’s expectations", "듣는 사람의 기대"), ")."])
# 가리키는 말
add_refers(sentences, 3, {"beyond which": "an attention limit(주의력의 한계)를 넘어서면"})
add_refers(sentences, 7, {"Such contrasts": "contrasts can take place의 contrasts(대조)"})

SENSES = {
    1: [sense("for", "for long", "~ 동안 (오래)", "for long = 오랫동안"),
        sense("to", "from time to time", "~까지", "from time to time = 때때로")],
    3: [sense("which", "beyond which", "그것(주의력의 한계)", "전치사 + 관계대명사 which — an attention limit을 받음"),
        sense("to", "to be perceived", "~하게 (될)", "be likely to + 동사원형 = ~할 가능성이 있다"),
        sense("as", "as lacking order", "~로", "perceive A as B = A를 B로 인식하다")],
    4: [sense("for", "For instance", "예를 들어", "for instance = 예를 들어"),
        sense("if", "if the intention is", "만약 ~라면", "조건의 if"),
        sense("to", "to focus on", "~하는 것", "to부정사 (명사 — 보어)"),
        sense("while", "while the melodies are unfolding", "~하는 동안", "시간의 while")],
    5: [sense("to", "to find", "~하는 것", "to부정사 (명사 — 보어)"),
        sense("to", "to listeners", "~에게", "전치사 to (대상)")],
    6: [sense("that", "attributes that combine", "~하는 (속성들)", "관계대명사 that — musical attributes를 꾸밈"),
        sense("to", "to create situations", "~하기 위해", "to부정사 (목적)")],
    7: [sense("which", "which builds upon", "그것은 (준비 단계)", "콤마 뒤 관계대명사 which — a preparatory stage를 받음")],
}

WORDS = {"however": "하지만", "melody": "선율", "alone": "~만으로", "normally": "보통", "keep": "붙잡아 두다", "listener’s": "듣는 사람의",
         "attention": "주의", "long": "오래", "piece": "한 곡", "music": "음악", "needs": "필요로 하다", "variety": "다양성",
         "contrasting": "대조되는", "elements": "요소", "time": "때", "regardless": "상관없이 · regardless of", "musical": "음악의",
         "style": "양식", "increase": "증가", "focus": "집중", "certain": "특정한", "parameters": "요소", "passage": "악절",
         "accompanied": "동반된", "decrease": "감소", "others": "다른 것들", "human": "인간의", "mind": "정신", "limit": "한계",
         "beyond": "~을 넘어서", "likely": "~할 것 같은", "perceived": "인식된", "lacking": "~이 없는", "order": "질서",
         "direction": "방향", "instance": "예 · for instance", "intention": "의도", "melodic": "선율의", "lines": "가락",
         "avoid": "피하다", "making": "만드는 것", "timbre": "음색", "variations": "변화", "melodies": "멜로디",
         "unfolding": "전개되는", "distract": "딴 데로 돌리다", "pitch": "음의 높낮이", "difficult": "어려운", "issues": "문제",
         "practice": "실무", "composition": "작곡", "right": "적절한", "balance": "균형", "repetition": "반복",
         "diversity": "다양성", "well-balanced": "균형이 잘 잡힌", "unfold": "펼쳐지다", "naturally": "자연스럽게",
         "listeners": "듣는 사람들", "western": "서양의", "styles": "양식", "results": "비롯되다", "network": "망",
         "relationships": "관계", "attributes": "속성", "combine": "결합되다", "different": "다양한", "ways": "방식",
         "create": "만들어 내다", "situations": "상황", "contrasts": "대조", "place": "자리 · take place = 일어나다",
         "preceded": "앞서 온", "preparatory": "준비의", "stage": "단계", "builds": "쌓다", "expectations": "기대",
         "one": "하나, (일반적인) 사람"}

STORIES = [
    (3, [sc("문장 1~2", "⚖️", "more focus here → less focus there · attention limit",
            "한쪽에 더 집중하면 다른 쪽은 줄어요. 주의력에는 한계가 있어요")]),
    (7, [sc("②~⑤", "🎵", "melody focus · balance · unfolding · contrasts",
            "선율에 집중하는 예, 반복과 다양성의 균형, 자연스러운 전개와 대조 이야기가 이어져요")]),
]

OPTIONS = [
    ("1", "The human mind has … 앞", "한 요소에 더 집중하면 다른 요소엔 덜 집중하게 된다 뒤", False),
    ("2", "For instance, if the intention … 앞", "인간의 정신에는 주의력의 한계가 있다 뒤", False),
    ("3", "One of the most difficult issues … 앞", "선율에 집중하려면 음색 변화를 줄여야 한다 뒤", True),
    ("4", "In most Western musical styles … 앞", "반복과 다양성의 균형을 찾기가 어렵다 뒤", False),
    ("5", "Such contrasts are … 앞", "이러한 전개는 대조가 생기는 관계망에서 나온다 뒤", False),
]
exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳을 고르시오. [3점]",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"], "numbers_only": True,
    "passage_keywords": ["However", "melody", "variety", "diversity"],
    "sentence": 1, "analysis_first": True, "wrong_rate": 41, "wrong_rank": 6,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "주어진 문장의 However·melody alone과 ③ 뒤 diversity를 떠올리며 들어갈 곳을 골라 봐요.",
        "정답이에요! 선율에 집중하려면 음색 변화를 줄여라(For instance …) → 하지만(However) 선율만으로는 부족, 다양성이 필요하다(주어진 문장) → "
        "그래서 반복과 다양성의 균형이 어렵다(One of the most difficult issues …), 순서예요.",
        "정답은 ③이에요. ③ 뒤 반복과 다양성(diversity)의 균형 이야기는, 주어진 문장이 다양성이 필요하다고 먼저 말해 줘야 이어져요.",
        {"1": "① 뒤 문장은 앞 문장(한쪽에 집중하면 다른 쪽은 줄어든다)의 이유를 대요. 아직 선율(melody) 이야기가 없어서 melody alone이 받을 말이 없어요.",
         "2": "② 뒤 For instance 문장에서 선율 이야기가 처음 나와요. 그 앞에 넣으면 melody alone(선율만으로는)이 받을 말이 없어요.",
         "4": "④ 뒤 this unfolding(이러한 전개)은 바로 앞 unfold naturally를 받아요. 사이에 넣으면 이 연결이 끊기고, ③의 끊김도 그대로예요.",
         "5": "⑤ 뒤 Such contrasts(그러한 대조)는 바로 앞 contrasts can take place를 받아요. 사이에 넣으면 이 연결이 끊겨요."},
        {"4": review(19,
                     "주어진 문장의 contrasting elements(대조적인 요소)가 ④ 뒤 contrasts(대조)와 비슷해 보여서 끌려요. 그런데 ④ 뒤 "
                     "this unfolding(이러한 전개)은 바로 앞 문장의 unfold naturally를 받아야 해요.\n주어진 문장은 선율에 집중하라는 말 바로 뒤, ③에 와야 해요.",
                     panel=rows(("③ 뒤", "… should unfold naturally to listeners", "자연스럽게 펼쳐져야 한다", "hl2"),
                                ("④ 뒤", "this unfolding results from …", "이러한 전개는 ~에서 비롯된다", "hl2"),
                                ("주어진 문장", "However, melody alone … variety", "하지만 선율만으로는 부족 · 다양성", "hl")),
                     rank_word="가장 많이 고른"),
         "2": review(13,
                     "②에 넣으면 주어진 문장이 For instance 문장보다 먼저 와요. 그런데 선율(melodic lines) 이야기는 ② 뒤에서 처음 나와서, "
                     "melody alone(선율만으로는)과 However가 맞설 말이 아직 없어요.\nHowever는 '선율에 집중하라'는 말 뒤에 와야 해요.",
                     panel=rows(("② 뒤", "For instance, … focus on melodic lines …", "선율에 집중하려면 변화를 줄여라", "hl2"),
                                ("주어진 문장", "However, melody alone …", "하지만 선율만으로는 부족", "hl")))}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 주어진 문장(위에서 넣음)과 열쇠 문장(4·5)만 ──
EMPHASIS = {
    4: ["melodic lines", "should avoid"],
    5: ["repetition", "diversity"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 39번 (주어진 문장 넣기, 3점)",
    topic="문장 넣기 푸는 법: 주어진 문장의 단서 → 앞에 올 내용 예측 → ①~⑤ 흐름이 끊기는 곳",
    method={"type": "sentence_insertion", "labels": ["주어진 문장 단서 찾기", "앞에 올 내용 예측하기", "흐름 끊기는 곳 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-musical-attention.svg", ("Melody", "선율"), "+", ("Variety", "다양성"),
                                       "듣는 사람의 귀를 오래 붙잡으려면?", "2026년 9월 모의평가 39번 도입 칠판"),
                      "alt": "칠판: Melody(선율) + Variety(다양성)", "kind": "drawing"},
            "method": METHOD_IMAGES["insert"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "음악을 들을 때 우리는 한꺼번에 얼마나 많은 것에 집중할 수 있을까요? 이번 글은 음악을 듣는 사람의 주의를 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "문장 넣기는 주어진 문장부터 꼼꼼히 봐야 해요. 그 안에 앞 문장과 이어지는 단서가 숨어 있어요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "단서를 찾고, 앞에 올 내용을 예측한 뒤, 흐름이 끊기는 곳을 찾아요."}}],
    exam=exam,
    # timbre는 시험지 아래 *로 풀어 준 말 — 핵심 단어가 아니라 뺐다
    key_words={"passage": [g("variety", "다양성"), g("contrasting", "대조되는"), g("from time to time", "때때로"),
                           g("regardless of", "~와 상관없이"), g("parameter", "요소"), g("accompany", "동반하다"),
                           g("perceive", "인식하다"), g("lack", "~이 없다, 부족하다"), g("intention", "의도"),
                           g("variation", "변화"), g("unfold", "펼쳐지다, 전개되다"), g("distract", "(주의를) 딴 데로 돌리다"),
                           g("pitch", "음의 높낮이"), g("composition", "작곡"), g("repetition", "반복"), g("diversity", "다양성"),
                           g("attribute", "속성"), g("precede", "앞서다, 선행하다"), g("preparatory", "준비의"),
                           g("expectation", "기대")],
               "options": []},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함:
# piece 한 곡 · certain 특정 · order 질서 · pitch 음의 높낮이.
TRAPS = {
    1: [tip("piece", "이 글에서는 → (음악) 한 곡  ('조각' 아님) · a piece of music = 음악 한 곡", "a piece of music", trap=True)],
    2: [tip("certain", "이 글에서는 → 특정한  ('확실한' 아님)", "certain", trap=True)],
    3: [tip("order", "이 글에서는 → 질서  ('주문·순서' 아님)", "order", trap=True)],
    4: [tip("pitch", "이 글에서는 → 음의 높낮이  ('던지다·경기장' 아님)", "pitch", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="문장 넣기 푸는 법")
