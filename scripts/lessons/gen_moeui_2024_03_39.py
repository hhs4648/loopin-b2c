"""2024년 3월 고3 39번 레슨 + 대사를 만든다 (주어진 문장 넣기, 3점). 오답률 78.1% · Top 1.

    python3 scripts/lessons/gen_moeui_2024_03_39.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/README.md + 2026년 3월 39·38번(문장 넣기) — 주어진 문장 단서 → 앞뒤 예측 → ①~⑤ 흐름 확인.
정답 ②. 많이 고른 오답 ④ 27.9% · ③ 25.8% (정답 21.9%보다 많다).
열쇠: 주어진 문장 This ↔ earlier figurative art. ② 뒤 These pictures는 '보이는 대로 나타내지 않는' 그림 = 예전 그림인데,
② 앞(①문장)까지는 원근법 그림 이야기뿐 — These pictures가 가리킬 예전 그림을 주어진 문장이 꺼내 줘야 한다.
해설지 해석과 대조함. foreshorten은 시험지 아래 *로 풀어 준 단어(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2024-03-39-perspective-painting"

GIVEN = ("This stands in contrast to earlier figurative art, which had been as focused on representing what the artist knew "
         "about the objects and the space he or she was painting as on how they looked.")
S = [
    "Almost all the figurative paintings we are familiar with now are in perspective.",
    "They present foreshortened figures and objects that diminish as they move away from the focal point of the painting.",
    "(①) A painting in perspective represents how the world looks to a person seeing the scene from a particular position in space.",
    "(②) These pictures are beautiful in their own right, but they do not represent scenes as we might see them if we were looking at them.",
    "(③) They are also less informative as to the layout of the space they represent.",
    "(④) The fact that perspective and information about spatial layout go together reveals something important about seeing.",
    "(⑤) Not only do we see the world through an egocentric frame but we also see it in a way that allows us to extract "
    "information about distances to, and sizes of, objects relative to us, and relative to one another.",
]
KO = [
    "지금 우리에게 익숙한 거의 모든 구상화는 원근법으로 그린 것이다.",
    "그것들은 그림의 초점에서 멀어짐에 따라 작아지는 축소된 인물들과 사물들을 나타낸다.",
    "원근법으로 그린 그림은 공간의 특정 위치에서 그 장면을 보는 사람에게 세상이 어떻게 '보이는지'를 나타낸다.",
    "이러한 그림들은 그 자체로 아름답지만, 그것들은 만약 우리가 그것들을 보고 있다면 우리가 보고 있을 것 같은 장면들을 나타내지는 않는다.",
    "그것들은 또한 그것들이 나타내는 공간의 배치에 대해서도 정보를 덜 준다.",
    "시점과 공간 배치에 대한 정보가 함께 어우러진다는 사실은 '보는 것'에 대한 중요한 무언가를 드러낸다.",
    "우리는 자기중심적인 틀을 통해 세상을 볼 뿐만 아니라, 우리로 하여금 우리에게 상대적인, 그리고 서로 상대적인 물체와의 거리와 (물체의) 크기에 대한 정보를 추출하도록 하는 방식으로 그것을 본다.",
]

NOW = "왼쪽 · 원근법 그림 (눈에 보이는 대로)"
OLD = "오른쪽 · 예전 그림 (아는 대로)"


def board(left, right, fresh=(), sort=None):
    return groups("두 가지 그림", "원근법 그림 · 눈에 보이는 대로", left, "예전 구상화 · 아는 대로", right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": NOW, "right": OLD} if sort else None)


def flow(id, n, before, after, ok, why):
    """①~⑤ 자리마다 — 앞 문장과 뒤 문장이 그대로 이어지나"""
    return choice(id, f"{n} 자리예요. '{before}' → '{after}', 자연스럽게 이어지나요?",
                  [("o0", "네, 이어져요", ok), ("o1", "아니요, 끊겨요", not ok)], why, why=why)


sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN, "teaching_value": "high",
        "model_translation": "이것은 그것들이 어떻게 '보였는지'만큼이나 화가들이 그리고 있던 사물과 공간에 대해 그들이 '알고 있던' 것을 나타내는 데 초점이 맞추어져 있었던 초기 구상화와는 대조적이다.",
        "glosses": [g("This", "이것"), g("stands in contrast to", "~와 대조를 이루다"), g("earlier figurative art", "초기(예전) 구상화"),
                    g("figurative", "구상의 · 사물을 알아볼 수 있게 그리는"), g("had been as focused on", "~만큼 ~에 초점을 맞춰 왔다"),
                    g("representing", "나타내는 것"), g("what the artist knew", "화가가 알고 있던 것"), g("the artist", "화가"),
                    g("knew", "알았다"), g("the objects and the space", "사물과 공간"), g("he or she was painting", "그(그녀)가 그리고 있던"),
                    g("how they looked", "그것들이 어떻게 보였는지"), g("stands", "서 있다 · stand in contrast to = ~와 대조되다")],
        "emphasis": ["earlier figurative art"],
        "steps": [
            sv("g_sv", ["This", "stands", "earlier figurative art", "the artist", "knew"],
               {"This": "S", "stands": "V", "earlier figurative art": "전목"},
               {"the artist": "그건 which 뒤 덩어리 안의 말이에요. 콤마 앞에서 찾아봐요.",
                "knew": "그건 what 덩어리 안의 동사예요. 콤마 앞에서 찾아봐요."},
               "주어는 This, 동사는 stands (in contrast to), to 뒤 목적어는 earlier figurative art예요.",
               ask="콤마 앞에서 주어(S), 동사(V), 그리고 to 뒤의 목적어(전목)를 찾아볼까요?"),
            choice("g_this",
                   "This(이것)는 earlier figurative art(예전 구상화)와 대조된대요. 그럼 This는 어떤 그림일까요?",
                   [("o0", "예전 구상화와는 다른, 다른 방식의 그림", True), ("o1", "예전 구상화 그 자체", False),
                    ("o2", "그림을 그린 화가", False)],
                   "stands in contrast to는 '~와 대조를 이룬다'예요. 대조라면 서로 달라야 해요.",
                   why="This는 예전 구상화와 '대조'된다고 했어요. 예전 그림 자체일 수는 없고, 그것과 다른 그림이에요.",
                   highlight=["This", "stands in contrast to"],
                   tips=[tip("앞을 가리키는 말", "This, These, Such처럼 앞 내용을 가리키는 말이 주어진 문장에 있으면, 가리키는 대상이 바로 앞 문장에 있어야 해요.")],
                   point="This stands in contrast to earlier figurative art — This는 예전 구상화와 '다른' 그림 (바로 앞 문장에 있어야 한다)"),
            # 선생님이 정한 정석 순서 (2026-10-18): This ↔ 예전 그림 → which = 예전 그림 → 예전 그림은 (안 보여도) 아는 것까지
            # → 그럼 This(앞 문장)는 예전 그림이 아닌 상대적으로 최근 기법. 뒤에 무엇이 올지는 묻지 않는다(답을 알고 맞춘 설명이 된다)
            choice("g_which",
                   "콤마 뒤 which는 앞의 무엇을 가리킬까요?",
                   [("o0", "This (이것)", False), ("o1", "earlier figurative art (예전 구상화)", True),
                    ("o2", "the objects (사물들)", False)],
                   "콤마 + which는 바로 앞 명사를 덧붙여 설명해요. 콤마 바로 앞을 봐요.",
                   why="콤마 + which는 바로 앞 명사, earlier figurative art(예전 구상화)를 덧붙여 설명해요. which 뒤는 모두 예전 그림 이야기예요.",
                   highlight=["earlier figurative art,", "which"],
                   point="earlier figurative art, which … = which 뒤는 예전 구상화에 대한 설명"),
            choice("g_knew",
                   "그럼 예전 구상화는 무엇까지 그렸대요?",
                   [("o0", "눈에 보이는 모습만", False), ("o1", "화가의 감정", False),
                    ("o2", "눈에 안 보여도 화가가 아는 것까지", True)],
                   "as A as B는 'B만큼 A'예요. what the artist knew(화가가 아는 것)와 how they looked(보이는 모습)를 봐요.",
                   why="'as focused on what the artist knew … as on how they looked', 보이는 모습만큼 화가가 아는 것도 나타내는 데 집중했대요. 보이지 않아도 아는 것까지 그린 거예요.",
                   highlight=["what the artist knew", "how they looked"],
                   tips=[tip("as A as B", "'B만큼 A'예요. as focused on X as on Y = Y만큼이나 X에도 초점을 맞춘", "as … as")],
                   point="earlier figurative art = 보이는 모습만큼, (눈에 안 보여도) 화가가 아는 것까지 그렸다"),
            show("g_knew_pic",
                 "그림으로 보면 이래요. 아는 대로 그리면 멀리 있는 사람도 실제 크기로, 보이는 대로 그리면 멀수록 작게 그려요.",
                 panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/knew-vs-looks.svg",
                        "alt": "왼쪽 예전 그림: 가까운 사람과 먼 사람을 같은 크기로(아는 대로). 오른쪽 원근법: 먼 사람을 작게(한 자리에서 보이는 대로)"},  # 아래 단어 칩은 그림 속 글자와 겹쳐 뺀다 (2026-10-19 선생님)
                 tips=[tip("아는 대로 vs 보이는 대로", "아는 대로 = 실제 크기·모양(멀리 있는 사람도 원래 크기로). 보이는 대로 = 한 자리에서 눈에 비친 모습(멀면 작게).")]),
            choice("g_before",
                   "This는 이 예전 그림과 대조된대요. 그럼 주어진 문장 바로 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "예전 구상화를 자세히 설명하는 내용", False), ("o1", "화가 한 사람의 생애", False),
                    ("o2", "예전 그림이 아닌, 상대적으로 최근의 다른 그림 방식", True)],
                   "This가 가리키는 앞 내용이 예전 그림과 '대조'돼야 해요. 대조라면 예전 그림 쪽이 아니에요.",
                   why="This(앞 문장의 내용)가 예전 그림과 대조된다고 했어요. 그러니 바로 앞에는 예전 그림이 아닌, 상대적으로 최근의 그림 방식 이야기가 와야 해요.",
                   highlight=["This", "earlier figurative art"],
                   point="주어진 문장 앞 = This = 예전 그림과 대조되는 '최근 기법' 이야기"),
        ],
    },
    {
        "id": 2, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("Almost all the figurative paintings", "거의 모든 구상화"), g("we are familiar with", "우리에게 익숙한"),
                    g("now", "지금"), g("are", "~이다"), g("in perspective", "원근법으로 그린"), g("perspective", "원근법")],
        "steps": [
            show("s1_now", "지금 우리에게 익숙한 그림은 거의 다 원근법으로 그렸대요. 칠판 왼쪽에 넣어 둘게요.",
                 panel=board(["in perspective"], ["what the artist knew"], fresh=("in perspective",)),
                 highlight=["in perspective"], button="다음 문장",
                 tips=[tip("perspective", "'원근법'이에요. 가까운 건 크게, 먼 건 작게 그리는 방법이에요. '관점'이라는 뜻도 있어요.", "perspective")]),
        ],
    },
    {
        "id": 3, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("They", "그것들(원근법 그림)"), g("present", "보여 주다, 나타내다"), g("foreshortened figures and objects", "축소된 인물과 사물"),
                    g("diminish", "작아지다"), g("move away from", "~에서 멀어지다"), g("the focal point", "초점")],
        "steps": [
            show("s2_small", "멀어질수록 작아지게 그린대요. 원근법 그림이 어떻게 생겼는지 설명하는 문장이에요.",
                 highlight=["diminish", "move away from"], button="다음 문장",
                 tips=[tip("as + 주어 + 동사", "여기서 as는 '~함에 따라'예요. as they move away = 그것들이 멀어짐에 따라.", "as")]),
        ],
    },
    {
        "id": 4, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("A painting in perspective", "원근법으로 그린 그림"), g("represents", "나타내다"),
                    g("how the world looks", "세상이 어떻게 보이는지"), g("to a person", "사람에게"), g("seeing the scene", "그 장면을 보는"),
                    g("from a particular position", "특정한 자리에서"), g("in space", "공간에서")],
        "steps": [
            choice("s3_what",
                   "원근법 그림은 무엇을 나타낸대요?",
                   [("o0", "화가가 사물에 대해 아는 것", False), ("o1", "한 자리에서 볼 때 세상이 보이는 모습", True),
                    ("o2", "공간의 정확한 크기", False)],
                   "represents 뒤 'how the world looks'를 봐요. looks는 '~하게 보이다'예요.",
                   why="'how the world looks to a person seeing the scene from a particular position'은 특정한 자리에서 보는 사람에게 세상이 어떻게 보이는지예요.",
                   highlight=["how the world looks"]),
            show("s3_board", "원근법 그림은 보이는 모습 그대로, 예전 그림은 아는 것까지 그렸어요. 칠판에 붙여 둘게요.",
                 panel=board(["in perspective", "how the world looks"], ["what the artist knew"], fresh=("how the world looks",))),
            flow("s3_flow", "①", "멀어질수록 작게 그린다", "원근법 그림은 보이는 모습을 나타낸다", True,
                 "둘 다 원근법 그림 이야기라 그대로 이어져요."),
        ],
    },
    {
        "id": 5, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("These pictures", "이 그림들"), g("are beautiful", "아름답다"), g("in their own right", "그 자체로"),
                    g("but", "하지만"), g("they do not represent", "그것들은 나타내지 않는다"), g("scenes", "장면들"),
                    g("as we might see them", "우리가 볼 법한 대로"), g("if we were looking at them", "우리가 그것들을 보고 있다면")],
        "steps": [
            choice("s4_these",
                   "These pictures(이 그림들)는 우리가 보는 대로 장면을 나타내지 않는대요. 그럼 어느 쪽 그림일까요?",
                   [("o0", NOW, False), ("o1", OLD, True)],
                   "원근법 그림은 보이는 모습 그대로를 나타냈어요. '보는 대로 나타내지 않는' 그림은 반대쪽이에요.",
                   why="원근법 그림은 보이는 모습 그대로를 나타냈어요. 보는 대로 나타내지 않는 These pictures는 예전 구상화예요.",
                   panel=board(["in perspective", "how the world looks"], ["what the artist knew"],
                               sort=["do not represent scenes as we might see them"]),
                   highlight=["These pictures", "do not represent"],
                   point="These pictures … do not represent scenes as we might see them = 예전 구상화"),
            show("s4_break",
                 "그런데 바로 앞 문장까지는 원근법 그림 이야기만 했어요. 예전 그림을 꺼낸 적이 없는데 These pictures가 예전 그림을 가리키니 어색해요.",
                 panel=board(["in perspective", "how the world looks"], ["what the artist knew", "do not represent"],
                             fresh=("do not represent",)),
                 highlight=["These pictures"], point="② 앞에서 예전 그림을 꺼내 줘야 These pictures가 그것을 가리킬 수 있다"),
            flow("s4_flow", "②", "원근법 그림은 보이는 모습을 나타낸다", "이 그림들은 보는 대로 나타내지 않는다", False,
                 "These pictures가 가리킬 예전 그림이 앞에 없어요. 갑자기 반대 그림 이야기로 넘어가서 흐름이 끊겨요."),
        ],
    },
    {
        "id": 6, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("They", "그것들(예전 그림)"), g("are also less informative", "또한 정보를 덜 준다"),
                    g("as to", "~에 관해서"), g("the layout of the space", "공간의 배치"), g("they represent", "그것들이 나타내는")],
        "steps": [
            show("s5_also",
                 "They도 앞 문장의 These pictures, 즉 예전 그림이에요. also(또한), 공간 배치에 대한 정보도 덜 준대요.",
                 panel=board(["in perspective", "how the world looks"], ["what the artist knew", "do not represent", "less informative"],
                             fresh=("less informative",)),
                 highlight=["also less informative"],
                 tips=[tip("as to", "'~에 관해서'예요. as to the layout = 배치에 관해서.", "as to")]),
            flow("s5_flow", "③", "이 그림들은 보는 대로 나타내지 않는다", "그것들은 또한 정보도 덜 준다", True,
                 "둘 다 예전 그림 이야기예요. also(또한)로 단점을 하나 더 보태서 그대로 이어져요."),
        ],
    },
    {
        "id": 7, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("The fact", "사실"), g("perspective and information about spatial layout", "원근법과 공간 배치에 대한 정보"),
                    g("go together", "함께 간다"), g("reveals", "드러내다"), g("something important", "중요한 무언가"),
                    g("about seeing", "보는 것에 대해"), g("spatial", "공간의"), g("layout", "배치")],
        "steps": [
            sv("s6_sv", ["The fact", "perspective and information about spatial layout", "go together", "reveals", "something important"],
               {"The fact": "S", "reveals": "V", "something important": "O"},
               {"perspective and information about spatial layout": "그건 that 뒤 덩어리 안의 주어예요. The fact가 무슨 사실인지 풀어 주는 덩어리예요.",
                "go together": "그건 that 뒤 덩어리 안의 동사예요. 문장 전체의 동사는 더 뒤에 있어요."},
               "주어는 The fact (that … go together), 동사는 reveals, 목적어는 something important예요.",
               ask="이번엔 주어(S), 동사(V), 목적어(O)를 찾아볼까요?"),
            choice("s6_together",
                   "'perspective and information about spatial layout go together'는 무슨 말일까요?",
                   [("o0", "원근법 그림이 공간 배치 정보도 함께 준다", True), ("o1", "원근법 그림은 공간 정보를 덜 준다", False),
                    ("o2", "원근법과 공간은 서로 상관없다", False)],
                   "go together는 '함께 간다'예요. 원근법이 있으면 공간 배치 정보도 같이 있다는 말이에요.",
                   why="go together는 '함께 간다'예요. 정보를 덜 주는 예전 그림과 달리, 원근법 그림은 배치 정보를 함께 준다는 말이에요."),
            flow("s6_flow", "④", "예전 그림은 정보도 덜 준다", "원근법과 공간 정보는 함께 간다", True,
                 "예전 그림은 정보를 덜 주고, 원근법은 정보와 함께 가요. 대조로 그대로 이어져요."),
        ],
    },
    {
        "id": 8, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("Not only do we see the world", "우리는 세상을 볼 뿐만 아니라"), g("through an egocentric frame", "자기중심적인 틀을 통해"),
                    g("egocentric", "자기중심적인"), g("frame", "틀"), g("but we also see it", "우리는 또한 그것을 본다"),
                    g("in a way", "~하는 방식으로"), g("allows us to extract", "우리가 뽑아낼 수 있게 해 주다"),
                    g("extract", "추출하다, 뽑아내다"), g("information", "정보"), g("distances to", "~까지의 거리"),
                    g("sizes of", "~의 크기"), g("objects", "물체들"), g("relative to us", "우리를 기준으로"),
                    g("relative to one another", "서로를 기준으로")],
        "slashes": ["egocentric frame", "in a way", "extract information", "objects relative to us,"],
        "steps": [
            show("s7_note",
                 "Not only A but also B는 'A뿐만 아니라 B도'예요. 우리는 나를 중심으로 세상을 볼 뿐 아니라, 거리와 크기 정보도 뽑아낸대요.",
                 highlight=["Not only do we see the world", "but we also see it"],
                 tips=[tip("Not only + 동사 + 주어", "Not only가 문장 맨 앞에 오면 순서가 바뀌어요. Not only do we see = we not only see.", "Not only")]),
            flow("s7_flow", "⑤", "원근법과 공간 정보는 함께 간다", "우리는 거리·크기 정보도 뽑아내며 본다", True,
                 "앞 문장이 '보는 것에 대해 중요한 걸 드러낸다'고 했고, 그 중요한 게 무엇인지 풀어 줘요. 그대로 이어져요."),
            show("s7_go", "①~⑤ 중 흐름이 끊긴 곳은 하나였어요. 주어진 문장의 This와 earlier figurative art를 떠올리며 골라 봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 초급 기본 — 문장마다 「주어·동사 + 뜻」 또는 「해석 맞추기」 하나 (2026-10-15 선생님)
add_basic(sentences, 2, [m("Almost all the figurative paintings", "거의 모든 구상화는"), " ", m("in perspective", "원근법으로 그린 것"), m("are", "이다"), "."],
          match_display="Almost all the figurative paintings are in perspective.",
          sv_new=sv_step("s2_basic_sv", ["Almost all the figurative paintings", "we are familiar with", "are", "in perspective"],
                         {"Almost all the figurative paintings": "S", "are": "V"},
                         {"we are familiar with": "그건 앞의 paintings를 꾸며 주는 덩어리예요(우리에게 익숙한).",
                          "in perspective": "그건 동사 뒤에서 어떤 상태인지 말해 주는 말이에요."},
                         "주어는 Almost all the figurative paintings, 동사는 are예요."),
          meaning_ids=["s1_now"])
add_basic(sentences, 3, [m("They", "그것들은"), " ", m("foreshortened figures and objects", "축소된 인물과 사물"), "을 ", m("present", "보여 준다"), "."],
          sv_new=sv_step("s3_basic_sv", ["They", "present", "foreshortened figures and objects", "diminish"],
                         {"They": "S", "present": "V", "foreshortened figures and objects": "O"},
                         {"diminish": "그건 that 뒤 덩어리 안의 동사예요(작아지는)."},
                         "주어는 They, 동사는 present, 목적어는 foreshortened figures and objects예요."),
          meaning_ids=["s2_small"])
add_basic(sentences, 4, [m("A painting in perspective", "원근법 그림은"), " ", m("how the world looks", "세상이 어떻게 보이는지"), "를 ",
                         m("represents", "나타낸다"), "."],
          match_display="A painting in perspective represents how the world looks.",
          sv_new=sv_step("s4_basic_sv", ["A painting in perspective", "represents", "how the world looks", "a person"],
                         {"A painting in perspective": "S", "represents": "V", "how the world looks": "O"},
                         {"a person": "그건 to 뒤, '누구에게' 보이는지 알려 주는 말이에요."},
                         "주어는 A painting in perspective, 동사는 represents, 목적어는 how the world looks예요."),
          meaning_after="s3_what")
add_basic(sentences, 5, [m("These pictures", "이 그림들은"), " ", m("are beautiful", "아름답다"), ", ", m("but", "하지만"), " ",
                         m("they do not represent", "그것들은 나타내지 않는다"), " — ", m("scenes", "장면들"), "을 ", m("as we might see them", "우리가 볼 법한 대로"), "."],
          match_display="These pictures are beautiful, but they do not represent scenes as we might see them.",
          sv_new=sv_step("s5_basic_sv", ["These pictures", "are", "beautiful", "they", "do not represent", "scenes"],
                         {"These pictures": "S", "are": "V", "beautiful": "C", "they": "S", "do not represent": "V", "scenes": "O"}, {},
                         "but 앞은 주어 These pictures, 동사 are, 보어 beautiful이에요. but 뒤는 주어 they, 동사 do not represent, 목적어 scenes예요."),
          meaning_after="s4_these")
add_basic(sentences, 6, [m("They", "그것들은"), " ", m("the layout of the space", "공간의 배치"), "에 관해서도 ", m("are also less informative", "정보를 덜 준다"), "."],
          sv_new=sv_step("s6_basic_sv", ["They", "are", "less informative", "the layout of the space"],
                         {"They": "S", "are": "V", "less informative": "C"},
                         {"the layout of the space": "그건 as to(~에 관해) 뒤 덩어리예요."},
                         "주어는 They, 동사는 are, 보어는 (also) less informative예요."),
          meaning_ids=["s5_also"])
add_basic(sentences, 7, [m("The fact", "~라는 사실은"), " ", m("go together", "함께 간다"), "는 — ", m("something important", "중요한 무언가"), "를 ",
                         m("reveals", "드러낸다"), "."],
          match_display="The fact that perspective and information about spatial layout go together reveals something important.",
          sv_id="s6_sv", meaning_ids=["s6_together"])

SENSES = {
    1: [sense("to", "stands in contrast to", "~와 (대조)", "stand in contrast to + 명사 = ~와 대조를 이루다"),
        sense("which", "art, which had been", "(그것은) ~했던", "콤마 + which = 앞 명사를 덧붙여 설명"),
        sense("as", "as focused on", "~만큼", "as + 형용사 + as … (원급 비교의 앞 as)"),
        sense("as", "as on how they looked", "~만큼", "원급 비교의 뒤 as — 비교 대상 앞")],
    3: [sense("that", "objects that diminish", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("as", "as they move away", "~함에 따라", "접속사 as + 주어·동사 (비례)")],
    4: [sense("to", "to a person", "~에게", "전치사 to + 사람")],
    5: [sense("but", "but they do not", "하지만", "접속사 but + 주어·동사"),
        sense("as", "as we might see them", "~대로, ~처럼", "접속사 as + 주어·동사 (방식)"),
        sense("if", "if we were looking", "만약 ~라면", "가정법 과거 if + 주어 + were")],
    6: [sense("as", "as to the layout", "~에 관해서", "as to + 명사"), sense("to", "as to the layout", "(as to의 일부)", "as to = ~에 관해서")],
    7: [sense("that", "The fact that", "~라는 (사실)", "동격의 that + 완전한 문장")],
    8: [sense("but", "but we also see", "~도 (Not only A but also B)", "Not only A but (also) B"),
        sense("that", "a way that allows", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("to", "allows us to extract", "~하도록", "allow + 사람 + to부정사 = 사람이 ~하게 해 주다"),
        sense("to", "distances to", "~까지의", "전치사 to (거리)"),
        sense("to", "relative to us", "~에 비해, ~을 기준으로", "relative to + 명사"),
        sense("to", "relative to one another", "~에 비해, ~을 기준으로", "relative to + 명사")],
}

WORDS = {"earlier": "초기의, 예전의", "art": "미술, 예술", "focused": "초점이 맞춰진", "artist": "화가, 예술가", "objects": "사물, 물체",
         "space": "공간", "painting": "그리는, 그림", "looked": "보였다", "contrast": "대조", "almost": "거의", "paintings": "그림들",
         "familiar": "익숙한", "foreshortened": "축소된 · 원근법으로 짧아 보이게 그린", "figures": "인물들", "move": "움직이다",
         "focal": "초점의", "point": "점", "world": "세상", "looks": "~하게 보이다", "person": "사람", "seeing": "보는", "scene": "장면",
         "particular": "특정한", "position": "자리, 위치", "pictures": "그림들", "beautiful": "아름다운", "right": "권리 · in one's own right = 그 자체로",
         "represent": "나타내다", "see": "보다", "looking": "보는", "less": "덜", "informative": "정보를 주는", "fact": "사실",
         "together": "함께", "important": "중요한", "seeing.": "보는 것", "way": "방식", "allows": "허락하다, ~하게 해 주다",
         "distances": "거리", "sizes": "크기", "relative": "상대적인 · relative to = ~에 비해", "go": "가다", "now": "지금",
         "knew": "알았다", "figurative": "구상의", "through": "~을 통해", "perspective": "원근법", "information": "정보", "spatial": "공간의", "layout": "배치", "scenes": "장면들",
         "something": "무언가", "away": "멀리", "only": "오직, ~만", "also": "또한"}

STORIES = [
    (3, [sc("주어진 문장", "🖼️", "This ↔ earlier figurative art", "예전 구상화는 보이는 모습만큼 '아는 것'도 그렸어요"),
         sc("문장 1~2", "📐", "in perspective · diminish", "지금 그림은 거의 원근법 — 멀어질수록 작게 그려요")]),
    (6, [sc("①~③", "👀", "how the world looks", "원근법 그림은 한 자리에서 보이는 모습을 나타내요"),
         sc("", "🧩", "do not represent · less informative", "보는 대로 나타내지 않고, 공간 배치 정보도 덜 주는 그림이 있어요")]),
    (8, [sc("④~⑤", "📏", "go together · distances and sizes", "원근법과 공간 정보는 함께 가요 — 우리는 거리·크기 정보를 뽑아내며 봐요")]),
]

OPTIONS = [
    ("1", "A painting in perspective … 앞", "원근법 그림이 작게 그린다 뒤", False),
    ("2", "These pictures are beautiful … 앞", "원근법 그림은 보이는 모습을 나타낸다 뒤", True),
    ("3", "They are also less informative … 앞", "이 그림들은 보는 대로 나타내지 않는다 뒤", False),
    ("4", "The fact that perspective … 앞", "그것들은 정보를 덜 준다 뒤", False),
    ("5", "Not only do we see … 앞", "원근법과 공간 정보는 함께 간다 뒤", False),
]
exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은? [3점]",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"],
    "numbers_only": True,
    "passage_keywords": ["This", "earlier figurative art", "knew", "looked", "in perspective", "how the world looks",
                         "These pictures", "do not represent", "also less informative", "go together"],
    "sentence": 1, "analysis_first": True, "wrong_rate": 78.1, "wrong_rank": 1,
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "주어진 문장의 This와 earlier figurative art를 떠올리며 들어갈 곳을 골라 봐요.",
        "정답이에요! 원근법 그림은 보이는 모습을 나타낸다(①문장) → 이것은 아는 것까지 그린 예전 구상화와 대조된다(주어진 문장) → 이 그림들(예전 그림)은 보는 대로 나타내지 않는다, 순서예요.",
        "정답은 ②예요. These pictures가 가리킬 예전 구상화를 주어진 문장이 먼저 꺼내 줘야 해요.",
        {"1": "① 앞은 아직 원근법 그림의 생김새 이야기예요. This가 가리킬 '보이는 모습 그대로'가 아직 안 나왔어요.",
         "3": "③에 넣으면 ② 뒤 These pictures가 원근법 그림을 가리키게 돼요. 그런데 원근법 그림은 보는 대로 나타낸다고 했으니 말이 안 맞아요.",
         "4": "④에 넣으면 This가 '정보를 덜 준다'를 가리켜요. 그 앞의 These pictures는 이미 예전 그림 이야기라, 예전 그림을 다시 꺼낼 필요가 없어요.",
         "5": "⑤ 앞은 원근법과 공간 정보가 함께 간다는 결론이에요. 예전 그림을 새로 꺼낼 자리가 아니에요."},
        {"4": review(27.9,
                     "④에 넣으면 This가 바로 앞 '예전 그림은 정보도 덜 준다'를 가리켜요. 그런데 ② 뒤 These pictures부터 이미 예전 그림 이야기였어요. 예전 그림을 처음 꺼내는 주어진 문장은 These pictures보다 앞, ②에 와야 해요.",
                     "그래서 ④가 아니에요. 어디서 헷갈렸어요?",
                     [("These pictures가 원근법 그림인 줄 알았어요", ["these_refers"],
                       "알려 줘서 고마워요. These pictures는 '보는 대로 나타내지 않는' 그림이라 예전 그림이에요. 앞으로 비슷한 문장이 나오면 These가 가리키는 걸 먼저 짚어 줄게요."),
                      ("less informative와 대조라 이어지는 줄 알았어요", ["contrast_guess"],
                       "알려 줘서 고마워요. 대조 느낌만으로 정하지 말고, 가리키는 말(This, These)이 무엇을 받는지 확인해야 해요. 앞으로 이 점을 강조해서 알려 줄게요."),
                      ("둘 다요", ["these_refers", "contrast_guess"],
                       "알려 줘서 고마워요. 앞으로 These가 가리키는 대상부터 같이 짚어 볼게요.")],
                     panel=rows(("② 뒤", "These pictures … do not represent scenes as we see", "보는 대로 나타내지 않는 그림 = 예전 그림", "hl"),
                                ("주어진 문장", "This ↔ earlier figurative art", "예전 그림을 처음 꺼낸다", "hl2"))),
         "3": review(25.8,
                     "③에 넣으면 ② 뒤 'These pictures … do not represent scenes as we might see them'이 원근법 그림을 가리켜요. 그런데 원근법 그림은 보이는 모습 그대로를 나타낸다고 했어요. 그래서 These pictures 앞에서 예전 그림이 나와야 해요.",
                     "그래서 ③이 아니에요. 어디서 헷갈렸어요?",
                     [("These pictures가 원근법 그림인 줄 알았어요", ["these_refers"],
                       "알려 줘서 고마워요. 앞으로 These·They가 가리키는 대상을 먼저 짚어 줄게요."),
                      ("but 뒤 내용을 놓쳤어요", ["but_after"],
                       "알려 줘서 고마워요. but 뒤 'do not represent scenes as we might see them'이 열쇠였어요. 앞으로 but 뒤를 강조해서 알려 줄게요."),
                      ("둘 다요", ["these_refers", "but_after"], "알려 줘서 고마워요. 앞으로 가리키는 말과 but 뒤를 같이 짚어 줄게요.")])}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 39번 (주어진 문장 넣기, 3점)",
    topic="문장 넣기 푸는 법: 주어진 문장의 단서 → 앞뒤 예측 → ①~⑤ 흐름이 끊기는 곳",
    method={"type": "sentence_insertion", "labels": ["주어진 문장 단서 찾기", "앞에 올 내용 예측하기", "흐름 끊기는 곳 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-perspective.svg", ("Perspective", "원근법"), "↔", ("Earlier art", "예전 그림"),
                                       "그림은 보이는 대로만 그려야 할까?", "2024년 3월 39번 도입 칠판"),
                      "alt": "칠판: Perspective(원근법) ↔ Earlier art(예전 그림)", "kind": "drawing"},
            "method": METHOD_IMAGES["insert"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "그림은 눈에 보이는 대로만 그려야 할까요? 이번 글은 원근법 그림과 예전 그림을 견줘요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "문장 넣기는 주어진 문장부터 꼼꼼히 봐야 해요. 그 안에 앞 문장과 이어지는 단서가 숨어 있거든요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "단서를 찾고, 앞에 올 내용을 예측한 뒤, 흐름이 끊기는 곳을 찾을 거예요. 칠판 순서대로 해 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("stand in contrast to", "~와 대조를 이루다"), g("figurative", "구상의"), g("represent", "나타내다"),
                           g("perspective", "원근법, 시점"), g("diminish", "작아지다, 줄어들다"), g("focal point", "초점"),
                           g("particular", "특정한"), g("in one's own right", "그 자체로"), g("informative", "정보를 주는"),
                           g("layout", "배치"), g("spatial", "공간의"), g("reveal", "드러내다"), g("egocentric", "자기중심적인"),
                           g("extract", "추출하다"), g("relative to", "~에 비해, ~에 상대적인")],
               "options": []},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="문장 넣기 푸는 법",
       chunks={"Almost all the figurative paintings": "거의 모든 구상화", "we are familiar with": "우리에게 익숙한", "are": "~이다",
               "They": "그것들", "present": "보여 주다", "foreshortened figures and objects": "축소된 인물과 사물", "diminish": "작아지다",
               "A painting in perspective": "원근법 그림", "represents": "나타내다", "how the world looks": "세상이 어떻게 보이는지",
               "a person": "사람", "These pictures": "이 그림들", "beautiful": "아름다운", "they": "그것들",
               "do not represent": "나타내지 않는다", "scenes": "장면들", "less informative": "정보를 덜 주는",
               "the layout of the space": "공간의 배치", "are also less informative": "또한 정보를 덜 준다", "are beautiful": "아름답다",
               "they do not represent": "그것들은 나타내지 않는다", "as we might see them": "우리가 볼 법한 대로"})
