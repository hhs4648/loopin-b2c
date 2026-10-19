"""2024년 3월 고3 42번 레슨 + 대사를 만든다 (41~42 장문 중 42번 — 문맥상 낱말의 쓰임, 3점). 오답률 40.2% · Top 14.

    python3 scripts/lessons/gen_moeui_2024_03_42.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: 어휘(2026년 3월 30번·2024년 3월 30번과 같다) — 요지 → 두 쪽(부정적 혼잣말 → 불안) → 밑줄 하나씩 점검.
정답 ④ (d) relieve (→ fuel). 많이 고른 오답 ⑤ (e) cloud 18.7% — cloud를 명사 '구름'으로만 알아서. 동사 cloud = 흐리게 하다, 망치다.
열쇠: 예시 속 자동적 사고('Oh no, I don't like this', '날 거부할 거야')는 불안을 키운다 → relieve(덜어 주다)는 반대.
41번(제목)은 이 레슨에서 다루지 않는다. 해설지 해석과 대조함. fraught, taint는 시험지 아래 *로 풀어 준 단어(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2024-03-42-automatic-thoughts"

S = [
    "You are the narrator of your own life.",
    "The tone and perspective with which you describe each experience generates feelings associated with that narration.",
    "For example, if you find yourself constantly assuming, “This is hard,” “I wonder whether I’m going to survive,” or “It looks like "
    "this is going to turn out badly,” you’ll generate (a)anxious feelings.",
    "It’s time to restructure the way you think.",
    "Underlying this narration are the beliefs that (b)frame your experience and give it meaning.",
    "Think of your beliefs as having many layers.",
    "On the surface are your automatic thoughts.",
    "These are like short tapes that momentarily flash through your mind.",
    "Call these automatic thoughts a form of “self-talk” that you use as you navigate through the day.",
    "You (c)produce a wide variety of these automatic thoughts, some consciously and some unconsciously.",
    "For example, automatic thoughts that (d)relieve anxiety go something like this: You walk into a room, see a few new people, and "
    "say to yourself, “Oh no, I don’t like this. This is not good.”",
    "Or, “These people will soon find out that I am full of anxiety and will reject me.”",
    "Automatic thoughts are bad habits that (e)cloud fresh and positive experiences.",
    "They can turn a potentially good experience into one fraught with anxiety.",
    "If you tell yourself that you are always stressed or full of anxiety before doing something new, that new experience will be tainted by that anxiety.",
]
KO = [
    "여러분은 자기 자신의 삶의 내레이터이다.",
    "각 경험을 묘사하는 어조와 관점이 그 내레이션과 관련된 감정을 만들어 낸다.",
    "예를 들어, '이건 어려워.', '내가 살아남을 수 있을지 모르겠어.', 또는 '일이 안 좋게 되어갈 것 같아.'라고 계속해서 가정하는 자신의 모습을 알게 된다면, 여러분은 불안한 감정을 만들어 낼 것이다.",
    "이제는 여러분의 사고방식을 재구성할 때다.",
    "이러한 내레이션의 기저에는 여러분의 경험에 틀을 씌우고 그것에 의미를 부여하는 신념이 존재한다.",
    "여러분의 신념에 여러 층이 있다고 생각해 보자.",
    "그 표면에 바로 '자동적 사고'가 존재한다.",
    "이것은 순간적으로 여러분의 머릿속을 스쳐 가는 짧은 테이프와 같다.",
    "이 자동적 사고를 여러분이 하루를 항해해 나가며 사용하는 '자기 대화'의 한 종류로 부르자.",
    "여러분은 매우 다양한 자동적 사고를 일부는 의식적으로, 일부는 무의식적으로 만들어 낸다.",
    "예를 들어, 불안감에 기름을 붓는 자동적 사고는 이런 식으로 흘러간다. 여러분이 방에 들어가서 처음 보는 사람 몇 명을 보고, 자신에게 말한다. '이런, 나는 이거 싫어. 이건 좋지 않아.'",
    "또는 '이 사람들은 곧 내가 불안감이 가득하다는 것을 알아채고 날 거부할 거야.'",
    "자동적 사고는 새롭고 긍정적인 경험을 우울하게 만드는 나쁜 습관이다.",
    "그것들은 잠재적으로 좋은 경험을 불안감으로 가득 찬 것으로 바꿀 수 있다.",
    "만약 여러분이 새로운 무언가를 하기 전에 항상 스트레스를 받고 불안감으로 가득하다고 스스로에게 말한다면, 그 새로운 경험은 그 불안에 의해 오염될 것이다.",
]
UNDER = ["(a)anxious", "(b)frame", "(c)produce", "(d)relieve", "(e)cloud"]

TALK = "왼쪽 · 부정적인 혼잣말"
FEEL = "오른쪽 · 불안"


def board(left, right, fresh=()):
    return groups("혼잣말 → 감정", "부정적인 혼잣말 (narration)", left, "불안 (anxiety)", right, fresh=fresh, between="→")


def check(*done):
    names = {"a": ("(a) 맞음", "negative narration → anxious feelings", "부정적으로 말하면 불안한 감정"),
             "b": ("(b) 맞음", "beliefs frame your experience", "신념이 경험에 틀을 씌운다"),
             "c": ("(c) 맞음", "You produce automatic thoughts", "우리가 자동적 사고를 만들어 낸다"),
             "e": ("(e) 맞음", "bad habits cloud positive experiences", "나쁜 습관이 좋은 경험을 흐린다")}
    return rows(*[(names[d][0], names[d][1], names[d][2], "hl") for d in done])


L3 = [("This is hard", "이건 어려워"), ("turn out badly", "안 좋게 될 거야")]
R3 = [("anxious feelings", "불안한 감정")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("You", "너는"), g("are", "~이다"), g("the narrator", "이야기하는 사람, 내레이터"), g("of your own life", "자기 삶의")],
        "steps": [
            show("s1_narrator", "우리는 자기 삶을 말로 풀어 가는 내레이터래요. 내가 내 경험을 어떻게 말하는지가 이 글의 주제예요.",
                 highlight=["the narrator"], button="다음 문장"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("The tone and perspective", "어조와 관점"), g("with which you describe each experience", "각 경험을 묘사하는"),
                    g("generates", "만들어 낸다"), g("feelings", "감정"), g("associated with that narration", "그 이야기와 관련된")],
        "slashes": ["The tone and perspective", "each experience"],
        "steps": [
            sv("s2_sv", ["The tone and perspective", "you", "describe", "generates", "feelings"],
               {"The tone and perspective": "S", "generates": "V", "feelings": "O"},
               {"you": "그건 with which 뒤 덩어리 안의 주어예요.", "describe": "그건 with which 뒤 덩어리 안의 동사예요."},
               "주어는 The tone and perspective, 동사는 generates, 목적어는 feelings예요.",
               ask="주어(S), 동사(V), 목적어(O)를 찾아볼까요?"),
            choice("s2_mean",
                   "경험을 어떤 말투와 관점으로 말하느냐가 무엇을 만들어 낸대요?",
                   [("o0", "그 말과 관련된 감정", True), ("o1", "새로운 경험", False), ("o2", "다른 사람의 생각", False)],
                   "generates 뒤 'feelings associated with that narration'을 봐요.",
                   why="'generates feelings associated with that narration', 그렇게 말한 것과 관련된 감정을 만들어 낸대요. 말하는 방식이 감정을 바꿔요.",
                   highlight=["generates", "feelings"],
                   point="요지 시작: 경험을 말하는 방식(어조·관점) → 감정을 만든다"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("For example", "예를 들어"), g("if you find yourself constantly assuming", "자신이 계속 ~라고 가정하고 있다면"),
                    g("This is hard", "이건 어려워"), g("I wonder whether I’m going to survive", "내가 살아남을지 모르겠어"),
                    g("It looks like", "~인 것 같아"), g("this is going to turn out badly", "이게 안 좋게 될 거야"),
                    g("you’ll generate", "너는 만들어 낼 것이다"), g("anxious feelings", "불안한 감정")],
        "slashes": ["constantly assuming,", "“This is hard,”", "going to survive,”", "turn out badly,”"],
        "steps": [
            show("s3_check", "'이건 어려워', '안 좋게 될 거야'처럼 계속 부정적으로 말하면 불안한 감정이 생긴대요. 부정적인 말 → 불안, 그래서 (a)anxious는 문맥에 맞아요.",
                 highlight=["This is hard", "turn out badly", "anxious"],
                 panel=board(L3, R3, fresh=("This is hard", "turn out badly", "anxious feelings")),
                 tips=[tip("find oneself -ing", "'자신이 ~하고 있다는 걸 알게 되다'예요. find yourself assuming = 스스로 ~라고 가정하고 있다.", "find yourself")],
                 button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "medium",
        "glosses": [g("It’s time to", "~할 때다"), g("restructure", "다시 짜다, 재구성하다"), g("the way you think", "네가 생각하는 방식")],
        "steps": [
            show("s4_time", "이제 생각하는 방식을 다시 짤 때래요. 글쓴이가 바꾸자고 하는 건 이 부정적인 말하기예요.",
                 highlight=["restructure"], button="다음 문장",
                 tips=[tip("It’s time to ~", "'이제 ~할 때다'예요. 해야 할 일을 권할 때 써요.", "It’s time")]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Underlying this narration", "이 이야기의 밑바탕에"), g("are", "있다"), g("the beliefs", "신념, 믿음"),
                    g("frame your experience", "경험에 틀을 씌우다"), g("give it meaning", "그것에 의미를 주다")],
        "steps": [
            choice("s5_frame",
                   "Underlying ~ are the beliefs: 이야기 밑바탕에 신념이 있대요. 신념은 경험에 무엇을 한대요?",
                   [("o0", "경험을 지워 버린다", False), ("o1", "경험에 틀을 씌우고 의미를 준다", True), ("o2", "경험을 남에게 전한다", False)],
                   "that 뒤 '(b)frame your experience and give it meaning'을 봐요. frame은 동사로 '틀을 씌우다'예요.",
                   why="'frame your experience and give it meaning', 신념이 경험에 틀을 씌우고 의미를 준대요. 같은 일도 신념에 따라 다르게 보이는 거예요.",
                   highlight=["the beliefs", "give it meaning"],
                   tips=[tip("장소 + are + 주어 (도치)", "Underlying this narration are the beliefs = 이 이야기 밑바탕에 신념이 있다. 주어(the beliefs)가 동사 뒤로 갔어요.", "Underlying"),
                         tip("frame (동사)", "명사 '틀, 액자'뿐 아니라 동사로 '틀을 씌우다, (특정 방식으로) 표현하다'예요.", "frame")]),
            show("s5_check", "신념이 경험에 틀을 씌우고 의미를 준다, 이어지는 give it meaning과 같은 방향이라 (b)frame은 문맥에 맞아요.",
                 panel=check("a", "b"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "low",
        "glosses": [g("Think of", "~을 생각해 보라"), g("your beliefs", "너의 신념"), g("as having many layers", "여러 층을 가진 것으로")],
        "steps": [show("s6_layers", "신념에 여러 층이 있다고 생각해 보래요.", highlight=["many layers"], button="다음 문장")],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("On the surface", "맨 겉에"), g("are", "있다"), g("your automatic thoughts", "너의 자동적 사고")],
        "steps": [show("s7_surface", "맨 겉층에 '자동적 사고(automatic thoughts)'가 있대요. 저절로 떠오르는 생각이에요.",
                       highlight=["automatic thoughts"], button="다음 문장")],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "low",
        "glosses": [g("These are like", "이것들은 ~ 같다"), g("short tapes", "짧은 테이프"), g("momentarily", "순간적으로"),
                    g("flash through your mind", "머릿속을 스쳐 가다")],
        "steps": [show("s8_tapes", "자동적 사고는 머릿속을 순간 스쳐 가는 짧은 녹음테이프 같대요.", highlight=["short tapes"], button="다음 문장")],
    },
    {
        "id": 9, "text": S[8], "model_translation": KO[8], "teaching_value": "medium",
        "glosses": [g("Call", "~라고 불러라"), g("these automatic thoughts", "이 자동적 사고를"), g("a form of “self-talk”", "일종의 '혼잣말'"),
                    g("that you use", "네가 쓰는"), g("as you navigate through the day", "하루를 헤쳐 나가며")],
        "steps": [show("s9_selftalk", "자동적 사고를 하루를 지내며 쓰는 '혼잣말(self-talk)'이라고 부르자고 해요.",
                       highlight=["self-talk"], button="다음 문장")],
    },
    {
        "id": 10, "text": S[9], "model_translation": KO[9], "teaching_value": "high",
        "glosses": [g("You", "너는"), g("produce", "만들어 내다"), g("a wide variety of these automatic thoughts", "아주 다양한 자동적 사고"),
                    g("some consciously", "일부는 의식적으로"), g("and some unconsciously", "일부는 무의식적으로")],
        "steps": [
            show("s10_check", "우리는 아주 다양한 자동적 사고를 의식적으로도, 무의식적으로도 만들어 낸대요. 그래서 (c)produce는 문맥에 맞아요.",
                 highlight=["produce", "a wide variety"], panel=check("a", "b", "c"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 11, "text": S[10], "model_translation": KO[10], "teaching_value": "high",
        "glosses": [g("For example", "예를 들어"), g("automatic thoughts", "자동적 사고"), g("anxiety", "불안"),
                    g("go something like this", "대략 이런 식이다"), g("You walk into a room", "방에 들어간다"), g("see a few new people", "처음 보는 사람 몇 명을 본다"),
                    g("say to yourself", "혼잣말을 한다"), g("Oh no", "이런"), g("I don’t like this", "난 이게 싫어"), g("This is not good", "이건 좋지 않아")],
        "slashes": ["go something like this:", "a few new people,", "say to yourself,"],
        "steps": [
            choice("s11_effect",
                   "콜론(:) 뒤 예시를 봐요. 방에 들어가며 '이런, 난 이게 싫어, 좋지 않아'라고 혼잣말하면, 불안은 어떻게 될까요?",
                   [("o0", "더 커진다", True), ("o1", "줄어든다", False), ("o2", "아무 상관없다", False)],
                   "3문장에서 부정적으로 말하면 어떤 감정이 생긴다고 했는지 떠올려 봐요.",
                   why="'Oh no, I don’t like this', 이런 부정적인 혼잣말은 3문장처럼 불안을 만들어 내요. 불안이 더 커져요.",
                   highlight=["Oh no, I don’t like this", "This is not good"],
                   panel=board(L3 + [("Oh no, I don’t like this", "이런, 이거 싫어")], R3, fresh=("Oh no, I don’t like this",)),
                   point="예시 속 자동적 사고('Oh no …')는 불안을 키운다 — 이 흐름에 (d)가 맞는지 문제에서 확인"),
            show("s11_hold", "예시는 불안을 키우는 혼잣말이에요. 밑줄 (d)가 이 예시와 같은 방향인지는 마지막 문제에서 확인해 봐요.",
                 button="다음 문장"),
        ],
    },
    {
        "id": 12, "text": S[11], "model_translation": KO[11], "teaching_value": "medium",
        "glosses": [g("Or", "또는"), g("These people", "이 사람들은"), g("will soon find out", "곧 알아챌 것이다"),
                    g("I am full of anxiety", "내가 불안으로 가득하다"), g("will reject me", "나를 거부할 것이다")],
        "steps": [
            show("s12_reject", "'이 사람들은 내가 불안한 걸 곧 알아채고 날 거부할 거야' — 이것도 불안을 키우는 혼잣말이에요.",
                 highlight=["full of anxiety", "reject me"],
                 panel=board(L3 + [("Oh no, I don’t like this", "이런, 이거 싫어"), ("will reject me", "날 거부할 거야")], R3,
                             fresh=("will reject me",)), button="다음 문장"),
        ],
    },
    {
        "id": 13, "text": S[12], "model_translation": KO[12], "teaching_value": "high",
        "glosses": [g("Automatic thoughts", "자동적 사고는"), g("are bad habits", "나쁜 습관이다"), g("cloud", "흐리게 하다, 망치다"),
                    g("fresh and positive experiences", "새롭고 긍정적인 경험")],
        "steps": [
            choice("s13_cloud",
                   "자동적 사고는 '나쁜 습관(bad habits)'이래요. 그럼 새롭고 긍정적인 경험을 (e)cloud한다는 건 무슨 뜻일까요?",
                   [("o0", "좋은 경험을 흐리고 망친다", True), ("o1", "좋은 경험을 구름처럼 떠오르게 한다", False),
                    ("o2", "좋은 경험을 더 밝게 한다", False)],
                   "cloud는 명사 '구름'뿐 아니라 동사로 '흐리게 하다'예요. bad habits가 하는 일이니 나쁜 쪽이에요.",
                   why="cloud는 동사로 '흐리게 하다, 어둡게 하다'예요. 나쁜 습관이 새롭고 좋은 경험을 흐리게 망친다는 뜻이라 (e)는 문맥에 맞아요.",
                   highlight=["bad habits", "fresh and positive experiences"],
                   tips=[tip("cloud (동사)", "'흐리게 하다, (판단·기분을) 흐리다, 망치다'예요. cloud one's judgment = 판단을 흐리다.", "cloud")],
                   point="(e) cloud = 흐리게 하다(동사) — 나쁜 습관이 좋은 경험을 흐린다 → 문맥에 맞음"),
            show("s13_check", "그래서 (e)cloud는 문맥에 맞아요. 나쁜 습관(−)이 좋은 경험을 흐린다(−), 같은 방향이에요.",
                 panel=check("a", "b", "c", "e"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 14, "text": S[13], "model_translation": KO[13], "teaching_value": "medium",
        "glosses": [g("They", "그것들(자동적 사고)"), g("can turn", "바꿀 수 있다"), g("a potentially good experience", "좋을 수도 있는 경험"),
                    g("into one fraught with anxiety", "불안으로 가득한 것으로")],
        "steps": [
            show("s14_turn", "자동적 사고는 좋을 수도 있는 경험을 불안으로 가득한 경험으로 바꿀 수 있대요.",
                 highlight=["fraught with anxiety"],
                 panel=board(L3 + [("Oh no, I don’t like this", "이런, 이거 싫어"), ("will reject me", "날 거부할 거야")],
                             R3 + [("fraught with anxiety", "불안으로 가득")], fresh=("fraught with anxiety",)), button="다음 문장"),
        ],
    },
    {
        "id": 15, "text": S[14], "model_translation": KO[14], "teaching_value": "medium",
        "glosses": [g("If you tell yourself", "스스로에게 ~라고 말한다면"), g("you are always stressed", "늘 스트레스를 받는다"),
                    g("full of anxiety", "불안으로 가득한"), g("before doing something new", "새로운 일을 하기 전에"),
                    g("that new experience", "그 새로운 경험은"), g("will be tainted", "더럽혀질 것이다"), g("by that anxiety", "그 불안에 의해")],
        "slashes": ["full of anxiety", "something new,"],
        "steps": [
            show("s15_taint", "새 일을 앞두고 '난 늘 불안해'라고 말하면, 그 새 경험이 불안으로 물든대요. 처음부터 끝까지 부정적 혼잣말 → 불안이에요.",
                 highlight=["tainted"],
                 panel=board(L3 + [("Oh no, I don’t like this", "이런, 이거 싫어"), ("will reject me", "날 거부할 거야"), ("always stressed", "늘 스트레스")],
                             R3 + [("fraught with anxiety", "불안으로 가득"), ("tainted", "물듦")], fresh=("always stressed", "tainted"))),
            show("s15_go", "(a)(b)(c)(e)는 흐름에 맞았어요. 남은 하나가 예시(불안을 키우는 혼잣말)와 같은 방향인지 문제에서 골라 봐요.",
                 panel=check("a", "b", "c", "e"), panel_below=True, button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 1, [m("You", "너는"), " ", m("of your own life", "자기 삶의"), " ", m("the narrator", "내레이터"), m("are", "이다"), "."],
          sv_new=sv_step("s1_basic_sv", ["You", "are", "the narrator", "your own life"], {"You": "S", "are": "V", "the narrator": "C"},
                         {"your own life": "그건 of 뒤 덩어리예요."}, "주어는 You, 동사는 are, 보어는 the narrator예요."),
          meaning_ids=["s1_narrator"])
add_basic(sentences, 2, [m("The tone and perspective", "어조와 관점이"), " ", m("feelings", "감정"), "을 ", m("generates", "만들어 낸다"), "."],
          match_display="The tone and perspective generates feelings.",
          sv_id="s2_sv", meaning_ids=["s2_mean"])
add_basic(sentences, 4, [m("It’s time to", "~할 때다"), ": ", m("the way you think", "네가 생각하는 방식"), "을 ", m("restructure", "다시 짤"), "."],
          meaning_ids=["s4_time"])
add_basic(sentences, 7, [m("On the surface", "맨 겉에"), " ", m("your automatic thoughts", "너의 자동적 사고가"), " ", m("are", "있다"), "."],
          sv_new=sv_step("s7_basic_sv", ["the surface", "are", "your automatic thoughts"], {"are": "V", "your automatic thoughts": "S"},
                         {"the surface": "그건 On 뒤, 어디에 있는지예요."},
                         "장소(On the surface)가 앞으로 나와 순서가 바뀌었어요. 동사 are, 주어 your automatic thoughts예요.",
                         ask="장소가 맨 앞에 나왔어요. 동사(V)와 그 뒤 주어(S)를 찾아볼까요?"),
          meaning_ids=["s7_surface"])
add_basic(sentences, 10, [m("You", "너는"), " ", m("a wide variety of these automatic thoughts", "아주 다양한 자동적 사고"), "를 ", m("produce", "만들어 낸다"), " — ",
                          m("some consciously", "일부는 의식적으로"), ", ", m("and some unconsciously", "일부는 무의식적으로"), "."],
          sv_new=sv_step("s10_basic_sv", ["You", "produce", "a wide variety of these automatic thoughts"],
                         {"You": "S", "produce": "V", "a wide variety of these automatic thoughts": "O"}, {},
                         "주어는 You, 동사는 (c)produce, 목적어는 a wide variety of these automatic thoughts예요."),
          meaning_ids=["s10_check"])
add_basic(sentences, 13, [m("Automatic thoughts", "자동적 사고는"), " ", m("fresh and positive experiences", "새롭고 긍정적인 경험"), "을 흐리는 ",
                          m("are bad habits", "나쁜 습관이다"), "."],
          sv_new=sv_step("s13_basic_sv", ["Automatic thoughts", "are", "bad habits", "fresh and positive experiences"],
                         {"Automatic thoughts": "S", "are": "V", "bad habits": "C"},
                         {"fresh and positive experiences": "그건 that 뒤 덩어리 안의 말이에요."},
                         "주어는 Automatic thoughts, 동사는 are, 보어는 bad habits예요."),
          meaning_after="s13_cloud")

SENSES = {
    2: [sense("which", "with which you describe", "(그것으로) ~하는", "전치사 + which = 앞 명사(the tone and perspective)를 꾸밈"),
        sense("that", "that narration", "그", "지시형용사 that + 명사")],
    3: [sense("for", "For example", "(For example의 일부)", "For example = 예를 들어"),
        sense("if", "if you find yourself", "만약 ~라면", "접속사 if + 주어·동사"),
        sense("to", "going to survive", "~할 (것이다)", "be going to + 동사원형"),
        sense("to", "going to turn out", "~할 (것이다)", "be going to + 동사원형")],
    4: [sense("to", "time to restructure", "~할 (때)", "It’s time + to부정사")],
    5: [sense("that", "beliefs that frame", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    6: [sense("as", "as having many layers", "~로 (생각하다)", "think of A as B = A를 B로 생각하다")],
    8: [sense("that", "tapes that momentarily flash", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    9: [sense("that", "self-talk” that you use", "(앞 명사를 꾸밈)", "관계대명사 that + 주어·동사"),
        sense("as", "as you navigate", "~하면서", "접속사 as + 주어·동사 (동시)")],
    11: [sense("for", "For example", "(For example의 일부)", "For example = 예를 들어"),
         sense("that", "thoughts that relieve", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
         sense("to", "say to yourself", "~에게", "say to oneself = 혼잣말하다")],
    12: [sense("that", "find out that I am", "~라는 것을", "명사절 that (find out that …)")],
    13: [sense("that", "habits that cloud", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    15: [sense("if", "If you tell yourself", "만약 ~라면", "접속사 if + 주어·동사"),
         sense("that", "tell yourself that you are", "~라고", "명사절 that (tell oneself that …)"),
         sense("that", "that new experience", "그", "지시형용사 that + 명사"),
         sense("that", "that anxiety", "그", "지시형용사 that + 명사")],
}

WORDS = {"having": "가지고 있는", "oh": "아, 이런", "am": "~이다", "narrator": "이야기하는 사람", "own": "자기 자신의", "life": "삶", "tone": "어조, 말투", "perspective": "관점", "describe": "묘사하다",
         "each": "각각의", "experience": "경험", "generates": "만들어 내다", "feelings": "감정", "associated": "관련된", "narration": "이야기, 내레이션",
         "example": "예", "find": "알게 되다", "yourself": "너 자신", "constantly": "계속", "assuming": "가정하는", "hard": "어려운",
         "wonder": "궁금해하다", "whether": "~인지", "i’m": "나는 ~이다", "going": "(be going to = ~할 것이다)", "survive": "살아남다",
         "looks": "~처럼 보이다", "turn": "되다 · turn out = ~로 판명되다", "badly": "나쁘게", "you’ll": "너는 ~할 것이다", "generate": "만들어 내다",
         "anxious": "불안한", "time": "때", "restructure": "다시 짜다", "way": "방식", "think": "생각하다", "underlying": "밑바탕에 있는",
         "beliefs": "신념, 믿음", "frame": "틀을 씌우다", "give": "주다", "meaning": "의미", "layers": "층", "surface": "겉, 표면",
         "automatic": "자동적인", "thoughts": "생각", "short": "짧은", "tapes": "테이프", "momentarily": "순간적으로", "flash": "번쩍 스치다",
         "mind": "마음, 머릿속", "call": "부르다", "form": "형태, 종류", "self-talk": "혼잣말", "use": "쓰다", "navigate": "헤쳐 나가다",
         "day": "하루", "produce": "만들어 내다", "wide": "넓은", "variety": "다양함", "consciously": "의식적으로", "unconsciously": "무의식적으로",
         "relieve": "덜어 주다", "anxiety": "불안", "something": "무언가", "walk": "걷다", "room": "방", "few": "몇몇의", "new": "새로운",
         "people": "사람들", "say": "말하다", "no": "아니", "don’t": "~하지 않다", "like": "좋아하다", "good": "좋은", "soon": "곧",
         "full": "가득한", "reject": "거부하다", "bad": "나쁜", "habits": "습관", "cloud": "흐리게 하다", "fresh": "새로운",
         "positive": "긍정적인", "experiences": "경험들", "potentially": "잠재적으로", "fraught": "가득한", "tell": "말하다", "always": "늘",
         "stressed": "스트레스를 받는", "doing": "하는 것", "tainted": "더럽혀진", "it’s": "그것은 ~이다", "these": "이것들",
         "looks like": "~인 것 같다", "on": "~ 위에"}

STORIES = [
    (4, [sc("문장 1~3", "🎙️", "narrator · tone → feelings", "우리는 내 삶의 내레이터 — '어려워, 안 될 거야'라고 말하면 불안해져요"),
         sc("문장 4", "🔧", "restructure the way you think", "이제 생각하는 방식을 다시 짤 때예요")]),
    (10, [sc("문장 5~9", "🧅", "beliefs · automatic thoughts", "신념이 경험에 틀을 씌우고, 그 겉층엔 저절로 스치는 혼잣말(자동적 사고)이 있어요"),
          sc("문장 10", "📼", "produce a wide variety", "우리는 그런 생각을 의식적으로도 무의식적으로도 많이 만들어요")]),
    (14, [sc("문장 11~12", "😰", "Oh no · reject me", "방에 들어가며 '싫어, 날 거부할 거야'라고 혼잣말해요"),
          sc("문장 13~14", "🌫️", "bad habits · fraught with anxiety", "이런 생각은 좋은 경험을 흐리고 불안으로 가득 채우는 나쁜 습관이에요")]),
]

exam = {
    "question": "밑줄 친 (a)~(e) 중에서 문맥상 낱말의 쓰임이 적절하지 않은 것은? [3점]",
    "underline": UNDER, "sentence": 11, "analysis_first": True, "wrong_rate": 40.2, "wrong_rank": 14,
    "glosses": [g("anxious", "불안한"), g("frame", "틀을 씌우다"), g("produce", "만들어 내다"), g("relieve", "덜어 주다"), g("cloud", "흐리게 하다")],
    "options": [
        {"id": "1", "label": "(a) anxious", "keywords": ["anxious"], "ko": "불안한"},
        {"id": "2", "label": "(b) frame", "keywords": ["frame"], "ko": "틀을 씌우다"},
        {"id": "3", "label": "(c) produce", "keywords": ["produce"], "ko": "만들어 내다"},
        {"id": "4", "label": "(d) relieve", "keywords": ["relieve"], "ko": "덜어 주다", "correct": True},
        {"id": "5", "label": "(e) cloud", "keywords": ["cloud"], "ko": "흐리게 하다"},
    ],
    "brief": exam_brief(
        "예시 속 혼잣말이 불안을 키우는지 줄이는지 떠올리며, 흐름과 반대인 하나를 골라요.",
        "정답이에요! 콜론 뒤 예시('이런, 싫어', '날 거부할 거야')는 불안을 키우는 생각이에요. 그런데 (d)relieve는 '덜어 준다'라서 반대예요. fuel(부채질하다)이 맞아요.",
        "정답은 ④ (d)예요. 예시 속 혼잣말은 불안을 키워요. relieve(덜어 주다)가 아니라 fuel(부채질하다)이어야 해요.",
        {"1": "부정적으로 말하면 불안한(anxious) 감정이 생긴다는 흐름이라 맞아요.",
         "2": "신념이 경험에 틀을 씌우고(frame) 의미를 준다, 뒤의 give it meaning과 맞아요.",
         "3": "우리가 다양한 자동적 사고를 만들어 낸다(produce)는 말이라 맞아요.",
         "5": "cloud는 동사로 '흐리게 하다'예요. 나쁜 습관이 좋은 경험을 흐린다는 말이라 맞아요."},
        {"5": review(18.7,
                     "cloud를 명사 '구름'으로만 알면 어색해 보여요. 하지만 동사 cloud는 '흐리게 하다, 망치다'예요. 자동적 사고는 나쁜 습관(bad habits)이라서 새롭고 좋은 경험을 흐리게 망친다, 흐름에 딱 맞아요.",
                     "그래서 (e)는 문맥에 맞아요. 어디서 헷갈렸어요?",
                     [("cloud를 '구름'으로만 알았어요", ["word_sense_cloud"],
                       "알려 줘서 고마워요. cloud는 동사로 '흐리게 하다'예요. 앞으로 이런 단어가 나오면 헷갈리는 단어로 표시해 줄게요."),
                      ("(d) 예시를 불안을 줄이는 말로 읽었어요", ["example_direction"],
                       "알려 줘서 고마워요. 'Oh no, I don’t like this'는 불안을 키우는 말이에요. 앞으로 예시가 어느 방향인지 먼저 짚어 줄게요."),
                      ("둘 다요", ["word_sense_cloud", "example_direction"], "알려 줘서 고마워요. 앞으로 단어의 다른 뜻과 예시의 방향을 같이 짚어 줄게요.")],
                     panel=rows(("(e)", "bad habits that cloud fresh and positive experiences", "나쁜 습관이 좋은 경험을 흐린다 → 맞음", "hl"),
                                ("(d)", "thoughts that relieve anxiety: “Oh no …”", "불안을 키우는 예시인데 relieve(덜어 줌) → 반대", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 41~42번 중 42번 (문맥상 낱말의 쓰임, 3점)",
    topic="어휘 문제 푸는 법: 요지 → 두 쪽(부정적 혼잣말 → 불안) → 밑줄 단어가 흐름에 맞는지 하나씩 점검",
    method={"type": "word_in_context", "labels": ["요지 잡기", "두 그룹으로 나누기", "밑줄 단어 맞춰 보기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-self-talk.svg", ("Self-talk", "혼잣말"), "→", ("Feelings", "감정"),
                                       "내가 나에게 하는 말이 감정을 바꿀까?", "2024년 3월 42번 도입 칠판"),
                      "alt": "칠판: Self-talk(혼잣말) → Feelings(감정)", "kind": "drawing"},
            "method": METHOD_IMAGES["vocab"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "새로운 자리에 갈 때 속으로 어떤 말을 하나요? 이번 글은 혼잣말(자동적 사고)이 감정을 어떻게 바꾸는지 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "어휘 문제는 단어 뜻만 보면 다 맞아 보여요. 문장마다 흐름을 잡아야 틀린 단어가 보여요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "요지를 잡고, 말과 감정을 두 쪽으로 나눈 뒤, 밑줄 단어가 흐름에 맞는지 하나씩 볼 거예요. 칠판 순서대로 해 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("narrator", "이야기하는 사람"), g("perspective", "관점"), g("generate", "만들어 내다"), g("associated with", "~와 관련된"),
                           g("assume", "가정하다"), g("turn out", "~로 판명되다"), g("restructure", "재구성하다"), g("underlying", "밑바탕에 있는"),
                           g("frame", "틀을 씌우다"), g("layer", "층"), g("momentarily", "순간적으로"), g("navigate", "헤쳐 나가다"),
                           g("consciously", "의식적으로"), g("reject", "거부하다"), g("cloud", "흐리게 하다"), g("potentially", "잠재적으로")],
               "options": [g("relieve", "덜어 주다"), g("fuel", "부채질하다, 키우다")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="어휘 문제 푸는 법",
       chunks={"You": "너는", "are": "~이다", "the narrator": "내레이터", "your own life": "자기 삶", "The tone and perspective": "어조와 관점",
               "you": "너는", "describe": "묘사하다", "generates": "만들어 낸다", "feelings": "감정", "It’s": "그것은 ~이다", "time": "때",
               "the way you think": "네가 생각하는 방식", "the surface": "겉, 표면", "your automatic thoughts": "너의 자동적 사고",
               "produce": "만들어 내다", "a wide variety of these automatic thoughts": "아주 다양한 자동적 사고", "Automatic thoughts": "자동적 사고",
               "bad habits": "나쁜 습관", "fresh and positive experiences": "새롭고 긍정적인 경험", "of your own life": "자기 삶의",
               "It’s time to": "~할 때다", "restructure": "다시 짜다", "On the surface": "맨 겉에", "some consciously": "일부는 의식적으로",
               "and some unconsciously": "일부는 무의식적으로", "are bad habits": "나쁜 습관이다"})
