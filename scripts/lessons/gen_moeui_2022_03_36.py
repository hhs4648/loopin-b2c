"""2022년 3월 고3 36번 레슨 + 대사를 만든다 (글의 순서, 2점). 오답률 53.0% · Top 5 (메가스터디 풀서비스 채점 기준).

    py scripts/lessons/gen_moeui_2022_03_36.py   (→ node scripts/policy_copy.mjs stamp <id> → npx vitest run)

틀: docs/tutor/templates/order.md — 주어진 글의 끝 → 단락 첫머리(앞에 무엇?) → 단락 끝(다음에 무엇?) → 순서 잇기.
정답 ⑤ (C)-(B)-(A). 많이 고른 오답 ③ (B)-(C)-(A) 21% — 주어진 글 끝(비난자를 공감으로 → 폭언이 멈춤) 바로 뒤에
(B) '비난자가 방어자의 마음을 알고 동맹이 된다'를 붙였다. 그러나 (B)는 however(그러나)·Suddenly and unexpectedly로 시작해
앞에 '비난자가 상대 마음을 몰랐다'가 있어야 하고, the defender도 앞에서 소개돼야 한다 → (C) 끝 the ignorant blamer is blind to it.
단서: (C) And what about the person who’s on the defensive? ← 주어진 글은 비난자 이야기만 / (B) however, the blamer knows ← (C) 비난자는 못 본다 /
(A) no longer feeling fear or hatred toward the blamer, the person’s quiet rage ← (B) 끝 방어자의 벽과 분노가 사라진다.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
rant, spontaneously는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt) — dead in its tracks '즉시', mirror outward '밖으로 잘 보여 주다',
human punching bag '인간 펀칭백', ally '동맹자'. 반영한 규칙: 2026-10-20 끊어읽기(slashes·roles·modifiers)까지. Claude 초안 — 선생님 검토 전.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from order_tools import card, order_link  # noqa: E402

ID = "moeui-2022-03-36-anger-empathy"

G1 = "Anger and empathy — like matter and antimatter — can’t exist in the same place at the same time."
G2 = "Let one in, and you have to let the other one go."
G3 = "So when you shift a blamer into empathy, you stop the person’s angry ranting dead in its tracks."
A1 = ("(A) The relief from no longer feeling “fear or hatred” toward the blamer spontaneously triggers a tremendous rush of "
      "gratitude and — miraculously — the person’s quiet rage turns into forgiveness and, beyond that, a willingness to work "
      "toward solutions.")
B1 = ("(B) Suddenly and unexpectedly, however, the blamer knows just how sad, angry, scared, or lonely the defender feels and "
      "spontaneously turns into an ally.")
B2 = ("When the defender feels understood by the blamer and that they are on the same side, there’s nothing to defend against.")
B3 = "The defender’s wall, and with it his unspoken rage and frustration, disappears."
C1 = "(C) And what about the person who’s on the defensive?"
C2 = ("Initially, this human punching bag is frustrated because no matter what he or she is trying to mirror outward the "
      "ignorant blamer is blind to it.")
C3 = "As a result, the person who’s under attack is usually in a state of quiet, barely controlled rage."

sentences = [
    {
        "id": 1, "label": "주어진 글", "text": f"{G1} {G2} {G3}", "teaching_value": "high",
        "model_translation": "분노와 공감은 물질과 반물질처럼 같은 시간 같은 장소에 존재할 수 없다. 하나를 들여보내면 다른 하나는 내보내야 한다. 따라서 비난자를 공감 속으로 이동시킬 때, 여러분은 그 사람의 분노에 찬 폭언을 즉시 멈추게 한다.",
        "glosses": [g("Anger and empathy", "분노와 공감"), g("Anger", "분노"), g("empathy", "공감"),
                    g("like matter and antimatter", "물질과 반물질처럼"), g("can’t exist", "존재할 수 없다"),
                    g("in the same place", "같은 장소에"), g("at the same time", "같은 시간에"),
                    g("Let one in", "하나를 들여보내면"), g("you have to let the other one go", "다른 하나는 내보내야 한다"),
                    g("shift a blamer into empathy", "비난하는 사람을 공감 속으로 옮기다"), g("a blamer", "비난하는 사람, 비난자"),
                    g("the person’s angry ranting", "그 사람의 화난 폭언"),
                    g("dead in its tracks", "그 자리에서 즉시 · stop ~ dead in its tracks = ~을 즉시 멈추게 하다")],
        "slashes": ["Anger and empathy", "antimatter —", "can’t exist", "the same place", "Let one in,", "into empathy,", "angry ranting"],
        "roles": [r("Anger and empathy", "S"), r("can’t exist", "V"), r("Let", "V"), r("you … you … you", "S"), r("have to let", "V"),
                  r("shift", "V"), r("stop", "V"), r("the person’s angry ranting", "O")],
        "steps": [
            sv("g_sv", ["Anger and empathy", "matter and antimatter", "can’t exist", "the same place"],
               {"Anger and empathy": "S", "can’t exist": "V"},
               {"matter and antimatter": "그건 대시(—) 두 개 사이, 'like(~처럼)' 뒤에 덧붙인 비유예요.",
                "the same place": "그건 in 뒤 덩어리예요. 어디인지 알려 주는 말이에요."},
               "주어는 Anger and empathy(분노와 공감), 동사는 can’t exist(존재할 수 없다)예요. 대시(—) 사이는 비유예요.",
               ask="주어진 글의 첫 문장이에요. 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("g_cant",
                   "Anger and empathy(분노와 공감)는 서로 어떤 관계라고 할까요?",
                   [("o0", "함께 있으면 서로 더 커진다", False), ("o1", "같은 곳에 함께 있을 수 없다", True),
                    ("o2", "서로 아무 상관이 없다", False)],
                   "둘째 문장 Let one in, and you have to let the other one go(하나를 들이면 다른 하나는 내보내야 한다)를 봐요.",
                   why="can’t exist in the same place at the same time, 같은 시간 같은 곳에 있을 수 없대요. 하나를 들이면 다른 하나는 나가야 해요.",
                   highlight=["can’t exist", "Let one in", "let the other one go"],
                   tips=[tip("명령문, and ~", "Let one in, and ~는 '하나를 들이면 ~'이에요. 명령문 뒤 and는 '그러면'으로 읽어요.", "Let one in")]),
            choice("g_stop",
                   "So 문장에서, 비난하는 사람(a blamer)을 공감으로 옮기면 어떻게 된대요?",
                   [("o0", "화난 폭언이 그 자리에서 멈춘다", True), ("o1", "더 크게 화를 낸다", False),
                    ("o2", "분노와 공감을 함께 느낀다", False)],
                   "분노와 공감은 함께 있을 수 없다고 했어요. 공감이 들어오면 분노는 나가야 해요.",
                   why="공감(empathy)이 들어오면 분노는 나가야 해요. 그래서 you stop the person’s angry ranting dead in its tracks, 화난 폭언이 즉시 멈춘대요.",
                   highlight=["shift a blamer into empathy", "stop", "dead in its tracks"], bracket=G3,
                   tips=[tip("dead in its tracks", "'그 자리에서 즉시'예요. stop ~ dead in its tracks = ~을 즉시 멈추게 하다.", "dead in its tracks"),
                         tip("shift A into B", "'A를 B로 옮기다'예요. 비난하는 사람을 공감 쪽으로 옮긴다는 말이에요.", "shift")],
                   panel=groups("칠판", "Anger (분노)", [("angry ranting", "화난 폭언")], "Empathy (공감)", [("a blamer → empathy", "비난자를 공감으로")],
                                between="↔", caption="하나가 들어오면 다른 하나는 나간다")),
            choice("g_next",
                   "주어진 글은 비난하는 사람(blamer) 이야기로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "물질과 반물질에 대한 과학 설명", False), ("o1", "다툼의 다른 한쪽, 비난받는 사람 이야기", True),
                    ("o2", "비난자가 다시 화를 내는 이유", False)],
                   "다툼에는 비난하는 사람과 비난받는 사람이 있어요. 지금까지 누구 이야기만 했는지 봐요.",
                   why="지금까지는 비난하는 사람(blamer)만 나왔어요. 다툼에는 비난받는 사람도 있으니, 그 사람 이야기가 이어지기 쉬워요.",
                   tips=[tip("순서 문제 요령", "주어진 글의 마지막 말이 다음 단락의 첫머리와 이어져요. however, What about, the defender 같은 말이 무엇을 받는지 봐요.")]),
            show("paper_order", "이제 (A)·(B)·(C)를 시험지 순서대로 읽어요. 단락마다 첫머리와 끝을 잘 봐 두면 좋아요.",
                 button="(A)부터 읽어 볼게요"),
        ],
    },
    {
        "id": 2, "text": A1, "teaching_value": "high",
        "model_translation": "(A) 비난자에 대해 더는 '두려움이나 증오'를 느끼지 않게 됨으로써 오는 안도감으로 인해 엄청난 고마움이 물밀듯이 자연스럽게 밀려오고, 기적적으로 그 사람의 조용한 분노는 용서로, 그리고 그것을 넘어 해결을 향해 기꺼이 일하고자 하는 의지로 바뀐다.",
        "glosses": [g("The relief", "안도감"), g("from no longer feeling “fear or hatred”", "더는 '두려움이나 증오'를 느끼지 않게 되어 오는"),
                    g("toward the blamer", "비난자에 대한"), g("the blamer", "비난자"), g("spontaneously", "자연스럽게"),
                    g("triggers", "촉발하다, 불러일으키다"), g("a tremendous rush of gratitude", "엄청나게 밀려오는 고마움"),
                    g("miraculously", "기적적으로"), g("the person’s quiet rage", "그 사람의 조용한 분노"), g("turns into", "~로 바뀌다"),
                    g("forgiveness", "용서"), g("beyond that", "그것을 넘어"),
                    g("a willingness to work toward solutions", "해결을 향해 기꺼이 노력하려는 마음")],
        "slashes": ["The relief", "toward the blamer", "of gratitude", "miraculously —", "quiet rage", "into forgiveness", "beyond that,"],
        "roles": [r("The relief", "S"), r("triggers", "V"), r("a tremendous rush of gratitude", "O"), r("the person’s quiet rage", "S"),
                  r("turns into", "V")],
        "steps": [
            sv("a_sv", ["The relief", "the blamer", "triggers", "a tremendous rush of gratitude", "the person’s quiet rage", "turns into",
                        "forgiveness"],
               {"The relief": "S", "triggers": "V", "a tremendous rush of gratitude": "O", "the person’s quiet rage": "S",
                "turns into": "V", "forgiveness": "전목"},
               {"the blamer": "그건 toward(~에 대한) 뒤 덩어리예요. 전치사 뒤라 주어가 아니에요."},
               "앞은 S The relief, V triggers, O a tremendous rush of gratitude예요. and 뒤는 S the person’s quiet rage, V turns into, 전목 forgiveness예요.",
               ask="(A)는 긴 한 문장이에요. and로 이어진 두 쌍의 주어(S)·동사(V)와 목적어(O)·전치사 뒤 목적어(전목)를 모두 찾아볼까요?",
               faded=["— miraculously —"]),
            choice("a_person",
                   "the person’s quiet rage(그 사람의 조용한 분노)에서 the person은 누구일까요?",
                   [("o0", "폭언하던 비난자(blamer)", False), ("o1", "비난자를 두려워하고 미워하던 사람", True)],
                   "toward the blamer(비난자에 대한)를 봐요. 누가 누구에게 두려움과 증오를 느꼈는지 생각해 봐요.",
                   why="'fear or hatred toward the blamer', 비난자를 향해 두려움과 증오를 느끼던 사람이에요. 비난자 자신이 아니라 비난받던 쪽이에요.",
                   highlight=["toward the blamer", "the person’s quiet rage"],
                   tips=[tip("no longer", "'더는 ~ 않는'이에요. no longer feeling fear = 더는 두려움을 느끼지 않는 것. 전에는 느꼈다는 말이에요.", "no longer")]),
            choice("a_before",
                   "(A)는 '비난자를 더는 두려워하지도 미워하지도 않게 된 안도감'으로 시작해요. 앞에는 무엇이 와야 할까요?",
                   [("o0", "비난자가 처음 화를 내기 시작하는 장면", False), ("o1", "비난받던 사람의 방어와 분노가 사라지는 내용", True),
                    ("o2", "비난자가 더 크게 폭언하는 장면", False)],
                   "no longer(더는 ~ 않는)는 그 마음이 이미 풀렸다는 말이에요. 앞에서 무엇이 먼저 풀렸어야 할까요?",
                   why="'더는 두려움이나 증오를 느끼지 않는다'는 안도감이 오려면, 앞에서 비난받던 사람의 방어와 분노가 먼저 풀려야 해요.",
                   highlight=["The relief", "no longer"],
                   point="(A) no longer feeling fear or hatred toward the blamer ← 앞에서 비난받던 사람의 방어·분노가 먼저 사라져야"),
            show("a_end", "(A)는 조용한 분노가 용서로, 나아가 해결하려는 마음으로 바뀌며 끝나요.",
                 highlight=["forgiveness", "a willingness to work toward solutions"],
                 tips=[tip("trigger", "'촉발하다, 불러일으키다'예요. 총의 방아쇠(trigger)처럼 어떤 일을 일으킨다는 말이에요.", "triggers"),
                       tip("beyond that", "'그것을 넘어'예요. 용서에서 한 걸음 더 나아간다는 말이에요.", "beyond that")]),
        ],
    },
    {
        "id": 3, "text": B1, "teaching_value": "high",
        "model_translation": "(B) 그러나 갑자기 뜻밖에도 그 비난자는 방어자가 정말 얼마나 슬픈지, 얼마나 화가 나 있는지, 얼마나 겁먹었는지, 또는 얼마나 외로운지를 알게 되고, 자연스럽게 동맹자로 바뀐다.",
        "glosses": [g("Suddenly and unexpectedly", "갑자기, 뜻밖에도"), g("however", "그러나"), g("the blamer", "비난자"),
                    g("knows", "알다"), g("just how sad, angry, scared, or lonely the defender feels", "방어자가 정말 얼마나 슬프고 화나고 겁나고 외로운지"),
                    g("the defender", "방어하는 사람, 방어자"), g("spontaneously", "자연스럽게"), g("turns into", "~로 바뀌다"),
                    g("an ally", "동맹자, 같은 편")],
        "slashes": ["Suddenly and unexpectedly,", "however,", "the blamer knows", "the defender feels", "spontaneously"],
        "roles": [r("the blamer", "S"), r("knows", "V"), r("just how sad, angry, scared, or lonely the defender feels", "O"), r("turns into", "V")],
        "steps": [
            sv("b_sv", ["Suddenly and unexpectedly", "the blamer", "knows", "just how sad, angry, scared, or lonely the defender feels",
                        "turns into", "an ally"],
               {"the blamer": "S", "knows": "V", "just how sad, angry, scared, or lonely the defender feels": "O", "turns into": "V",
                "an ally": "전목"},
               {"Suddenly and unexpectedly": "그건 '갑자기, 뜻밖에도', 어떻게 일어났는지 알려 주는 말이에요."},
               "주어는 the blamer, 동사는 knows와 turns into예요. how 덩어리 전체가 아는 내용(O)이고, an ally는 into 뒤 목적어예요.",
               ask="(B)의 첫 문장이에요. 주어(S)·동사(V)·목적어(O)·전치사 뒤 목적어(전목)를 모두 찾아볼까요?"),
            choice("b_before",
                   "(B)는 'Suddenly and unexpectedly, however(그러나 갑자기 뜻밖에도)'로 시작해요. 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "비난자가 상대의 마음을 전혀 몰랐다는 내용", True), ("o1", "비난자가 이미 상대의 편이 되었다는 내용", False),
                    ("o2", "분노가 용서로 바뀌었다는 내용", False)],
                   "however(그러나)는 앞과 반대되는 말을 이어요. 뒤는 '비난자가 상대 마음을 알게 된다'예요.",
                   why="however 뒤가 '비난자가 갑자기 상대 마음을 알게 된다'예요. 그러니 앞에는 그 반대, 비난자가 상대 마음을 몰랐다는 내용이 와야 해요.",
                   highlight=["Suddenly and unexpectedly", "however", "the defender"],
                   tips=[tip("the + 명사", "the defender처럼 the가 붙으면 앞에서 이미 나온 사람이에요. 방어하는 사람이 먼저 소개돼야 해요.", "the defender")],
                   point="(B) however, the blamer knows … the defender ← 앞에 '비난자가 몰랐다' + 방어하는 사람이 먼저 나와야"),
        ],
    },
    {
        "id": 4, "text": B2, "teaching_value": "medium",
        "model_translation": "방어자가 자신이 비난자에 의해 이해받고 있으며 서로가 같은 편이라고 느낄 때, 방어할 것은 아무것도 없다.",
        "glosses": [g("When the defender feels understood", "방어자가 이해받는다고 느낄 때"), g("by the blamer", "비난자에게"),
                    g("that they are on the same side", "서로 같은 편이라고"), g("there’s nothing", "아무것도 없다"),
                    g("to defend against", "방어할"), g("the defender", "방어자")],
        "slashes": ["understood", "by the blamer", "the same side,"],
        "roles": [r("the defender", "S"), r("feels", "V"), r("’s", "V"), r("nothing", "S")],
        "steps": [
            show("b2_side", "비난자가 알아주고 같은 편이라고 느끼면, 방어자는 더 막을 게 없대요.",
                 highlight=["feels understood", "on the same side", "nothing to defend against"],
                 tips=[tip("there’s nothing to ~", "'~할 것이 아무것도 없다'예요. there’s nothing to defend against = 방어할 것이 하나도 없다.", "there’s nothing")]),
        ],
    },
    {
        "id": 5, "text": B3, "teaching_value": "high",
        "model_translation": "방어자의 벽이, 그리고 그 벽과 함께 입 밖에 내지 못한 그의 분노와 좌절이 사라진다.",
        "glosses": [g("The defender’s wall", "방어자의 벽"), g("and with it", "그리고 그것과 함께"),
                    g("his unspoken rage and frustration", "입 밖에 내지 못한 그의 분노와 좌절"), g("disappears", "사라지다")],
        "slashes": ["The defender’s wall,", "frustration,"],
        "roles": [r("The defender’s wall", "S"), r("disappears", "V")],
        "steps": [
            choice("b3_wall",
                   "콤마(,) 사이를 빼고 읽어 봐요. 무엇이 사라진대요?",
                   [("o0", "비난자의 공감", False), ("o1", "방어자의 벽, 그리고 그와 함께 분노와 좌절", True),
                    ("o2", "비난자와 방어자 사이의 동맹", False)],
                   "주어는 The defender’s wall이고, 동사는 맨 끝 disappears예요.",
                   why="The defender’s wall … disappears, 방어자의 벽이 사라진대요. 콤마 사이 말대로 분노와 좌절도 함께 사라져요.",
                   highlight=["The defender’s wall", "disappears"], faded=[", and with it his unspoken rage and frustration,"],
                   tips=[tip("with it", "'그것과 함께'예요. with it의 it은 앞의 wall(벽)이에요.", "with it")]),
            choice("b3_next",
                   "(B)는 '방어자의 벽과 분노가 사라진다'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "방어자가 처음 공격당해 좌절하는 장면", False), ("o1", "분노가 사라진 뒤 찾아오는 마음의 변화", True),
                    ("o2", "분노와 공감이 함께 있을 수 없다는 원리", False)],
                   "벽과 분노가 사라졌어요. 그다음에 그 사람 마음이 어떻게 될지 생각해 봐요.",
                   why="벽과 분노가 사라졌으니, 다음엔 그 뒤 그 사람 마음이 어떻게 바뀌는지가 이어지기 쉬워요.",
                   highlight=["disappears"],
                   point="(B) 끝 방어자의 벽·분노가 사라진다 → 다음은 그 뒤의 마음 변화"),
        ],
    },
    {
        "id": 6, "text": C1, "teaching_value": "high",
        "model_translation": "(C) 그렇다면 방어하는 쪽에 있는 사람은 어떤가?",
        "glosses": [g("And what about", "그렇다면 ~은 어떤가"), g("the person", "그 사람"), g("who’s on the defensive", "방어하는 쪽에 있는"),
                    g("on the defensive", "방어하는 쪽에 있는, 수세에 몰린")],
        "slashes": [],
        "modifiers": ["who’s on the defensive"],
        "steps": [
            choice("c_before",
                   "(C)는 'And what about the person who’s on the defensive'(그럼 방어하는 쪽 사람은 어때요)로 시작해요. 앞에는 무엇이 와야 할까요?",
                   [("o0", "방어하는 사람의 분노가 풀리는 이야기", False), ("o1", "비난하는 쪽 사람 이야기", True),
                    ("o2", "두 사람이 같은 편이 되는 이야기", False)],
                   "What about ~는 한 사람 이야기를 마치고 다른 사람으로 넘어갈 때 써요. 방어하는 사람의 상대가 누구인지 떠올려 봐요.",
                   why="What about ~로 방어하는 사람을 처음 꺼내요. 그러니 앞에는 그 상대, 비난하는 사람 이야기가 있어야 해요.",
                   highlight=["what about", "on the defensive"],
                   tips=[tip("What about ~?", "'~은 어때요?'예요. 앞 이야기를 마치고 다른 대상으로 넘어갈 때 써요.", "what about")],
                   point="(C) And what about the person who’s on the defensive? ← 앞에 비난하는 사람 이야기"),
        ],
    },
    {
        "id": 7, "text": C2, "teaching_value": "medium",
        "model_translation": "처음에 이 인간 펀칭백은 자신이 그 무엇을 밖으로 잘 보여 주려 애써도 그 무지한 비난자가 그것을 보지 못하므로 좌절한다.",
        "glosses": [g("Initially", "처음에"), g("this human punching bag", "이 인간 펀칭백 · 방어하는 사람을 이렇게 불러요"),
                    g("is frustrated", "좌절한다"), g("because", "~ 때문에"), g("no matter what", "무엇을 ~하든"),
                    g("he or she is trying to mirror outward", "그 사람이 밖으로 보여 주려 애쓰다"),
                    g("mirror", "거울처럼 비추다 · 여기서는 '밖으로 잘 보여 주다'"), g("the ignorant blamer", "그 무지한 비난자"),
                    g("is blind to it", "그것을 보지 못한다")],
        "slashes": ["Initially,", "is frustrated", "no matter what", "mirror outward"],
        "roles": [r("this human punching bag", "S"), r("is frustrated", "V"), r("the ignorant blamer", "S"), r("is blind", "V")],
        "steps": [
            show("c2_blind", "this human punching bag(인간 펀칭백)은 방어하는 사람이에요. 무엇을 보여 주려 해도 비난자가 못 봐서 좌절한대요.",
                 highlight=["this human punching bag", "is frustrated", "is blind to it"],
                 tips=[tip("no matter what", "'무엇을 ~하든'이에요. no matter what he or she is trying to mirror = 무엇을 보여 주려 애쓰든.", "no matter what"),
                       tip("be blind to ~", "'~을 보지 못하다, 모르다'예요. 눈이 먼 게 아니라 알아채지 못한다는 말이에요.", "is blind to")]),
        ],
    },
    {
        "id": 8, "text": C3, "teaching_value": "high",
        "model_translation": "그 결과 공격당하는 사람은 대체로 조용한, 간신히 통제되고 있는 분노 상태에 있게 된다.",
        "glosses": [g("As a result", "그 결과"), g("the person", "그 사람"), g("who’s under attack", "공격당하는"),
                    g("is usually", "대체로 ~에 있다"), g("in a state of", "~한 상태에"), g("quiet, barely controlled rage", "조용한, 간신히 참고 있는 분노"),
                    g("barely", "간신히, 가까스로")],
        "slashes": ["As a result,", "under attack", "a state of"],
        "roles": [r("the person", "S"), r("is", "V")],
        "modifiers": ["who’s under attack"],
        "steps": [
            choice("c3_rage",
                   "그 결과 공격받는 사람은 어떤 상태래요?",
                   [("o0", "크게 소리 지르며 화를 낸다", False), ("o1", "겉으로는 조용하지만 간신히 분노를 참고 있다", True),
                    ("o2", "화가 다 풀려 편안하다", False)],
                   "quiet(조용한)와 barely controlled(간신히 통제되는)를 같이 봐요.",
                   why="'quiet, barely controlled rage', 조용하지만 간신히 참고 있는 분노래요. 겉으론 조용해도 속은 화가 나 있어요.",
                   highlight=["quiet, barely controlled rage"],
                   tips=[tip("barely", "'간신히, 가까스로'예요. barely controlled = 겨우 참고 있는.", "barely")]),
            choice("c3_next",
                   "(C)는 비난자는 못 보고, 방어자는 조용히 분노를 참는 상태로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "이 막힌 상황이 바뀌는 계기", True), ("o1", "비난자가 처음 화를 내기 시작하는 장면", False),
                    ("o2", "물질과 반물질의 원리", False)],
                   "지금은 비난자는 모르고 방어자는 참고만 있어요. 이 상태가 어떻게 될지 생각해 봐요.",
                   why="비난자는 못 보고 방어자는 분노를 참는, 막힌 상태예요. 다음엔 이 상황이 바뀌는 계기가 이어지기 쉬워요.",
                   highlight=["quiet, barely controlled rage"],
                   point="(C) 끝 비난자는 못 보고 방어자는 분노를 참는다 → 다음은 상황이 바뀌는 계기"),
            order_link(
                card("given", "주어진 글", last=("… you stop the person’s angry ranting dead in its tracks", "비난자를 공감으로 옮기면 폭언이 즉시 멈춘다")),
                [card("A", "(A)", first=("The relief from no longer feeling “fear or hatred” toward the blamer …", "비난자를 더는 두려워·미워하지 않는 안도감"),
                      last=("… the person’s quiet rage turns into forgiveness …", "조용한 분노가 용서로 바뀐다")),
                 card("B", "(B)", first=("Suddenly and unexpectedly, however, the blamer knows … the defender feels …", "그러나 갑자기 비난자가 방어자의 마음을 안다"),
                      last=("The defender’s wall, and with it his unspoken rage and frustration, disappears", "방어자의 벽과 분노·좌절이 사라진다")),
                 card("C", "(C)", first=("And what about the person who’s on the defensive?", "그럼 방어하는 쪽 사람은 어떨까?"),
                      last=("… is usually in a state of quiet, barely controlled rage", "조용히, 간신히 분노를 참는 상태"))],
                ["C", "B", "A"],
                "주어진 글(비난자) → (C) What about 방어자?, 비난자는 못 본다 → (B) however, 비난자가 알게 되고 벽이 사라진다 → (A) 더는 두렵지 않은 안도감, 분노가 용서로 순서예요."),
            show("c_go", "직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?", button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 4, [m("When the defender feels understood", "방어자가 이해받는다고 느낄 때"), ", ",
                         m("there’s nothing", "아무것도 없다"), " ", m("to defend against", "방어할"), "."],
          match_display="When the defender feels understood, there’s nothing to defend against.",
          meaning_ids=["b2_side"])
add_basic(sentences, 5, [m("The defender’s wall", "방어자의 벽이"), " ", m("disappears", "사라진다"), "."],
          sv_new=sv_step("s5_basic_sv", ["The defender’s wall", "his unspoken rage and frustration", "disappears"],
                         {"The defender’s wall": "S", "disappears": "V"},
                         {"his unspoken rage and frustration": "그건 콤마(,) 사이, with it(그것과 함께) 뒤에 덧붙인 말이에요."},
                         "주어는 The defender’s wall, 동사는 disappears예요. 콤마 사이는 덧붙인 말이에요."),
          meaning_ids=["b3_wall"])
add_basic(sentences, 6, [m("And what about", "그렇다면 ~은 어떤가"), " ", m("the person", "그 사람"), " ",
                         m("who’s on the defensive", "방어하는 쪽에 있는"), "?"])
add_basic(sentences, 7, [m("this human punching bag", "이 인간 펀칭백은"), " ", m("is frustrated", "좌절한다"), " — ",
                         m("the ignorant blamer", "그 무지한 비난자가"), " ", m("is blind to it", "그것을 보지 못해서"), "."],
          match_display="Initially, this human punching bag is frustrated because the ignorant blamer is blind to it.",
          sv_new=sv_step("s7_basic_sv", ["this human punching bag", "is frustrated", "the ignorant blamer"],
                         {"this human punching bag": "S", "is frustrated": "V"},
                         {"the ignorant blamer": "그건 because 덩어리 안의 주어예요."},
                         "주어는 this human punching bag, 동사는 is frustrated예요. because 뒤가 그 이유예요."),
          meaning_ids=["c2_blind"])
add_basic(sentences, 8, [m("As a result", "그 결과"), ", ", m("the person", "그 사람은"), " ", m("who’s under attack", "공격당하는"), " ",
                         m("quiet, barely controlled rage", "조용한, 간신히 참고 있는 분노"), " ", m("in a state of", "상태에"), " ",
                         m("is usually", "대체로 있다"), "."],
          sv_new=sv_step("s8_basic_sv", ["As a result", "the person", "is", "a state"],
                         {"the person": "S", "is": "V"},
                         {"As a result": "그건 '그 결과', 앞과 잇는 말이에요.", "a state": "그건 in 뒤 덩어리예요."},
                         "주어는 the person, 동사는 is예요. who’s under attack이 그 사람을 꾸며요."),
          meaning_after="c3_rage")

SENSES = {
    1: [sense("to", "have to let", "~해야 (하다)", "have to + 동사원형"),
        sense("so", "So when", "그래서, 따라서", "접속사 So (문장 앞, 결과)")],
    2: [sense("that", "beyond that", "그것", "지시대명사 that (앞의 용서)"),
        sense("to", "willingness to work", "~하려는 (마음)", "명사 + to부정사")],
    4: [sense("that", "and that they are", "~라고", "명사절 that (feels … that …)"),
        sense("to", "nothing to defend", "~할 (것)", "명사 + to부정사")],
    7: [sense("to", "trying to mirror", "~하려고 (애쓰다)", "try to + 동사원형"),
        sense("to", "blind to it", "~에 대해 (보지 못하다)", "be blind to + 명사")],
    8: [sense("as", "As a result", "(As a result의 일부)", "As a result = 그 결과")],
}

WORDS = {"anger": "분노", "empathy": "공감", "like": "~처럼", "matter": "물질", "antimatter": "반물질", "exist": "존재하다",
         "place": "장소", "let": "들이다, 두다", "shift": "옮기다", "blamer": "비난하는 사람", "stop": "멈추게 하다",
         "person’s": "그 사람의", "angry": "화난", "ranting": "폭언", "dead": "완전히, 딱", "tracks": "자국, 자리",
         "relief": "안도감", "longer": "더 이상", "feeling": "느끼는 것", "fear": "두려움", "hatred": "증오",
         "spontaneously": "자연스럽게", "triggers": "촉발하다", "tremendous": "엄청난", "rush": "밀려옴, 쇄도",
         "gratitude": "고마움, 감사", "miraculously": "기적적으로", "quiet": "조용한", "rage": "분노", "turns": "바뀌다",
         "forgiveness": "용서", "beyond": "~을 넘어", "willingness": "기꺼이 하려는 마음", "work": "노력하다, 일하다",
         "solutions": "해결책", "suddenly": "갑자기", "unexpectedly": "뜻밖에", "knows": "알다", "sad": "슬픈",
         "scared": "겁먹은", "lonely": "외로운", "defender": "방어하는 사람", "feels": "느끼다", "ally": "동맹자, 같은 편",
         "understood": "이해받는", "side": "편", "defend": "방어하다", "against": "~에 맞서", "defender’s": "방어자의",
         "wall": "벽", "unspoken": "입 밖에 내지 않은", "frustration": "좌절", "disappears": "사라지다",
         "defensive": "방어하는", "initially": "처음에", "human": "인간", "punching": "펀칭", "bag": "백, 가방",
         "frustrated": "좌절한", "matter.": "물질", "trying": "애쓰는", "mirror": "보여 주다, 비추다", "outward": "밖으로",
         "ignorant": "무지한", "blind": "보지 못하는", "result": "결과", "attack": "공격", "usually": "대체로",
         "state": "상태", "barely": "간신히", "controlled": "통제된", "nothing": "아무것도 ~ 없다", "same": "같은",
         "there’s": "~이 있다", "who’s": "~인 (who is)", "can’t": "~할 수 없다", "or": "또는", "she": "그녀",
         "result,": "결과"}

OPTIONS = [("1", "(A)-(C)-(B)", False), ("2", "(B)-(A)-(C)", False), ("3", "(B)-(C)-(A)", False), ("4", "(C)-(A)-(B)", False), ("5", "(C)-(B)-(A)", True)]
exam = {
    "question": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?",
    "sentence": 1, "analysis_first": True, "wrong_rate": 53.0, "wrong_rank": 5,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], **({"correct": True} if o[2] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "단락 첫머리 단서(What about, however, the defender, no longer)를 떠올리며 순서를 골라 봐요.",
        "정답이에요! 비난자 이야기 → (C) 그럼 방어자는?, 비난자는 못 본다 → (B) however, 비난자가 알게 되고 벽이 사라진다 → (A) 안도감, 분노가 용서로, 순서예요.",
        "정답은 ⑤ (C)-(B)-(A)예요.",
        {"1": "(A)의 '더는 두렵지 않은 안도감'은 방어자의 분노가 먼저 풀린 뒤라야 해요. 주어진 글 바로 뒤에는 올 수 없어요.",
         "2": "(B)의 however는 '비난자가 몰랐다'를 받아야 하는데, 주어진 글엔 그런 말이 없어요. the defender도 아직 소개되지 않았어요.",
         "3": "많이 고른 오답이에요. (B)는 however(그러나)로 시작해서 앞에 '비난자가 상대 마음을 몰랐다'가 있어야 해요. 그 말은 (C) 끝에 있어요.",
         "4": "(C) 끝은 아직 비난자가 상대 마음을 못 보는 상태예요. 비난자가 바뀌는 (B) 없이 (A)의 안도감이 바로 올 수 없어요."},
        {"3": review(21,
                     "주어진 글이 '비난자를 공감으로 옮기면 폭언이 멈춘다'라서, 비난자가 상대 편이 되는 (B)를 바로 붙이고 싶었을 거예요. 하지만 (B)는 however(그러나)와 Suddenly and unexpectedly(갑자기 뜻밖에)로 시작해서, 앞에 '비난자가 상대 마음을 몰랐다'가 있어야 해요. 그 말은 (C) 끝 the ignorant blamer is blind to it에 있어요.",
                     "그래서 ③이 아니에요. 어디서 헷갈렸어요?",
                     [("비난자 이야기끼리 이어 버렸어요", ["content_link_only"],
                       "알려 줘서 고마워요. 내용이 비슷해 보여도 however 같은 연결어가 앞과 맞아야 이어져요. 앞으로 이 점을 강조해서 알려 줄게요."),
                      ("however를 신경 안 썼어요", ["however_contrast"],
                       "알려 줘서 고마워요. however는 앞과 반대되는 내용이 있어야 써요. 앞으로 연결어가 무엇과 반대인지 먼저 짚어 줄게요."),
                      ("둘 다요", ["content_link_only", "however_contrast"], "알려 줘서 고마워요. 앞으로 연결어와 내용 연결을 같이 짚어 볼게요.")],
                     panel=rows(("(C) 끝", "the ignorant blamer is blind to it", "비난자는 방어자의 마음을 못 본다", "hl"),
                                ("(B) 첫머리", "Suddenly and unexpectedly, however, the blamer knows", "그러나 갑자기 비난자가 알게 된다 ← (C) 끝과 반대", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 36번 (글의 순서)",
    topic="순서 푸는 법: 주어진 글의 끝 → 단락 첫머리 단서로 앞 내용 예측 → 단락 끝으로 다음 내용 예측 → 순서 잇기",
    method={"type": "order", "labels": ["단락 요지 잡기", "연결 단서 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-anger-empathy.svg", ("Anger", "분노"), "↔", ("Empathy", "공감"),
                                       "다툼 속 두 사람의 마음은 어떻게 풀릴까?", "2022년 3월 36번 도입 칠판"),
                      "alt": "칠판: Anger(분노) ↔ Empathy(공감)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "화가 나서 남 탓하는 사람을 어떻게 멈출 수 있을까요? 이번 글은 분노와 공감, 그리고 다툼 속 두 사람의 마음을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "순서 문제는 단락 첫머리의 단서가 앞 내용과 이어지는지 보는 거예요. however, What about 같은 말이 무엇을 받는지 찾아볼게요."}}],
    exam=exam,
    key_words={"passage": [g("empathy", "공감"), g("matter", "물질"), g("in one’s tracks", "즉시"), g("relief", "안도감"),
                           g("hatred", "증오"), g("trigger", "촉발하다"), g("tremendous", "엄청난"), g("gratitude", "고마움, 감사"),
                           g("miraculously", "기적적으로"), g("rage", "분노"), g("forgiveness", "용서"), g("unexpectedly", "뜻밖에"),
                           g("ally", "동맹자"), g("frustration", "좌절"), g("initially", "처음에"), g("mirror", "잘 보여 주다, 반영하다"),
                           g("ignorant", "무지한"), g("barely", "간신히")],
               "options": []},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="순서 푸는 법",
       chunks={"Anger and empathy": "분노와 공감", "matter and antimatter": "물질과 반물질", "can’t exist": "존재할 수 없다",
               "the same place": "같은 장소", "The relief": "안도감", "the blamer": "비난자", "triggers": "촉발하다",
               "a tremendous rush of gratitude": "엄청나게 밀려오는 고마움", "the person’s quiet rage": "그 사람의 조용한 분노",
               "turns into": "~로 바뀌다", "forgiveness": "용서", "Suddenly and unexpectedly": "갑자기, 뜻밖에도", "knows": "알다",
               "just how sad, angry, scared, or lonely the defender feels": "방어자가 정말 얼마나 슬프고 화나고 겁나고 외로운지",
               "an ally": "동맹자, 같은 편", "When the defender feels understood": "방어자가 이해받는다고 느낄 때",
               "there’s nothing": "아무것도 없다", "to defend against": "방어할", "The defender’s wall": "방어자의 벽",
               "his unspoken rage and frustration": "입 밖에 내지 못한 그의 분노와 좌절", "disappears": "사라지다",
               "And what about": "그렇다면 ~은 어떤가", "the person": "그 사람", "who’s on the defensive": "방어하는 쪽에 있는",
               "this human punching bag": "이 인간 펀칭백", "is frustrated": "좌절한다", "the ignorant blamer": "그 무지한 비난자",
               "is blind to it": "그것을 보지 못한다", "As a result": "그 결과", "who’s under attack": "공격당하는",
               "quiet, barely controlled rage": "조용한, 간신히 참고 있는 분노", "in a state of": "~한 상태에", "is usually": "대체로 ~에 있다",
               "is": "~에 있다", "a state": "상태"})
