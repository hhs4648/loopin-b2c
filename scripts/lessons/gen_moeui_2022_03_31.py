"""2022년 3월 고3 31번 레슨 + 대사를 만든다 (빈칸 추론 — 한 단어, 2점). 오답률 65.0% · Top 2.

    py scripts/lessons/gen_moeui_2022_03_31.py   (→ node scripts/policy_copy.mjs stamp <id> → npx vitest run)

틀: docs/tutor/templates/blank.md — 빈칸이 마지막 문장(2024년 3월 34번 꼴). 정답 ③ Compassion.
많이 고른 오답 ② Relaxation 42%가 정답(35%)보다 많다 — 글에 meditation(명상)이 나와서 '긴장 완화'로 끌린다.
열쇠: 빈칸 문장의 단서 — it(빈칸)을 싫은 사람에게도 사랑하는 사람만큼 '향하게(direct)' 한다 = 사람을 향한 마음.
재진술: benevolence · kindness · tenderness → this attitude → kindly messages (↔ 평소 마음: irritated · aggressive · cold · hostile).
배울 수 있다(learnable)는 foster(기르다) · rehearse(연습하다) · open to deliberate change(일부러 바꿀 수 있다)가 받친다.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
시험지 아래 *풀이 단어 없음. 해설지 해석과 대조함 — 다만 해설은 'kindly messages'를 「메시지를 기꺼이 연습하라」로
옮겼다(kindly를 부사로). 이 레슨은 형용사 「친절한 메시지」로 읽었다 → 선생님 확인 필요.
규칙 반영: 2026-10-20 끊어읽기(slashes·roles·modifiers)까지, 초급 기본(add_basic) 넣음. Claude 초안 — 선생님 검토 전.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic,  # noqa: E402
                      add_that_sv, topic_svg, base_lesson, exam_brief, review, finish)

ID = "moeui-2022-03-31-metta-meditation"

BLANK = ("________ is a learnable skill, and we need to direct it as much towards those we are tempted to dismiss and detest "
         "as to those we love.")
S = [
    "In the Indian language of pali, mettā means benevolence, kindness or tenderness.",
    "It is one of the most important ideas in Buddhism.",
    "Buddhism recommends a daily ritual meditation (known as mettā bhāvanā) to foster this attitude.",
    "The meditation begins with a call to think carefully every morning of an individual with whom one tends to get irritated "
    "or to whom one feels aggressive or cold and — in place of one’s normal hostile impulses — to rehearse kindly messages "
    "like ‘I hope you will find peace’ or ‘I wish you to be free from suffering’.",
    "This practice can be extended outwards ultimately to include pretty much everyone on Earth.",
    "The background assumption is that, with the right stimulus, our feelings towards people are not fixed and unalterable, "
    "but open to deliberate change and improvement.",
    BLANK,
]
KO = [
    "인도 팔리어에서 mettā는 자비심, 친절 혹은 다정함을 의미한다.",
    "그것은 불교에서 가장 중요한 관념 중 하나다.",
    "불교에서는 이러한 태도를 기르기 위해 매일 의례적으로 하는 (mettā bhāvanā로 알려진) 명상을 권한다.",
    "명상은 짜증이 나게 하거나, 공격적인 혹은 냉담한 기분이 들게 하는 경향이 있는 어떤 한 사람을 매일 아침 사려 깊게 생각하고, "
    "평소의 적대적인 충동 대신 '나는 당신이 평안을 찾길 바랍니다.' 또는 '나는 당신이 고통에서 벗어나기를 기원합니다.'와 같은 "
    "메시지를 기꺼이 연습하라는 요구로 시작한다.",
    "이 수행은 밖으로 확장되어 결국 지상의 거의 모든 사람을 포함할 수 있다.",
    "그 배경이 되는 가정은 적절한 자극으로 사람들을 향한 우리의 감정이 고정되어 바뀔 수 없는 게 아니라 의도적인 변화와 개선의 여지가 있다는 것이다.",
    "________은 학습 가능한 기술이며, 우리가 사랑하는 사람에게만큼이나 우리가 무시하고 혐오하고 싶은 마음이 생기는 사람에게도 그것을 향하게 할 필요가 있다.",
]

WARM = "왼쪽 · mettā 쪽"
COLD = "오른쪽 · 평소 마음 쪽"

W1 = [("benevolence", "자비심")]
W2 = W1 + [("kindness", "친절"), ("tenderness", "다정함")]
W3 = W2 + [("this attitude", "이 태도")]
W4 = W3 + [("kindly messages", "친절한 메시지")]
C4 = [("irritated", "짜증 난"), ("aggressive · cold", "공격적 · 냉담"), ("hostile impulses", "적대적인 충동")]


def board(warm, cold=None, fresh=(), sort=None):
    """단어 지도 — 왼쪽 mettā 쪽, 오른쪽 평소 마음 쪽(문장 4부터). 묶음 이름은 글에 나온 말까지만 — 빈칸 말(연민)은 쓰지 않는다"""
    return groups("mettā vs 평소 마음", "mettā 쪽", warm, "평소 마음 쪽" if cold is not None else None, cold,
                  fresh=fresh, between="↔" if cold is not None else None,
                  sort={"words": sort, "left": WARM, "right": COLD} if sort else None)


sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("In the Indian language of pali", "인도의 팔리어에서"), g("pali", "팔리어 · 고대 인도의 언어"),
                    g("mettā", "메타 · 팔리어 낱말"), g("means", "뜻하다"), g("benevolence", "자비심"), g("kindness", "친절"),
                    g("tenderness", "다정함"), g("benevolence, kindness or tenderness", "자비심, 친절 혹은 다정함"),
                    g("is a learnable skill", "배울 수 있는 기술이다"), g("learnable", "배울 수 있는"),
                    g("direct it", "그것을 향하게 하다"), g("as much towards", "~에게도 (…만큼) 똑같이"),
                    g("those we are tempted to dismiss and detest", "우리가 무시하고 혐오하고 싶은 사람들"),
                    g("as to those we love", "우리가 사랑하는 사람들에게만큼")],
        "slashes": ["of pali,", "means"],
        "roles": [r("mettā", "S"), r("means", "V"), r("benevolence, kindness or tenderness", "O")],
        "steps": [
            show("s1_passage", "빈칸은 마지막 문장, 맨 앞 주어 자리에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "____은 타고나는 거라서, 사랑하는 사람에게만 향한다", False),
                    ("o1", "____은 배울 수 있는 기술이고, 싫은 사람에게도 사랑하는 사람만큼 향하게 해야 한다", True),
                    ("o2", "____은 배울 수 있지만, 싫은 사람에게는 쓰지 않아도 된다", False)],
                   "learnable은 '배울 수 있는'이에요. as much towards A as to B는 'B에게만큼 A에게도'예요.",
                   why="a learnable skill은 배울 수 있는 기술이에요. 그것(it)을 무시하고 혐오하고 싶은 사람에게도, 사랑하는 사람에게만큼 향하게 해야 한대요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["________", "learnable", "direct"], highlight_alt=["detest", "love"],
                   tips=[tip("as much A as B", "'B만큼 A에도'예요. as much towards 싫은 사람 as to 사랑하는 사람 = 사랑하는 사람에게만큼 싫은 사람에게도.", "as much"),
                         tip("be tempted to ~", "'~하고 싶은 마음이 생기다'예요. those we are tempted to dismiss = 우리가 무시하고 싶은 사람들.", "tempted")]),
            show("s1_where_map", "빈칸(it)은 배울 수 있고, 사람에게 '향하게(direct)' 하는 거예요.",
                 button="다음", before_read=True, levels=["중", "초"], display=BLANK, tag="빈칸 문장", method=0,
                 highlight=["learnable", "direct"], highlight_alt=["detest", "love"], panel_below=True,
                 panel=rows(("빈칸 (it)", "a learnable skill", "배울 수 있는 기술", "hl"),
                            ("향하는 곳", "those we … detest = those we love", "싫은 사람에게도 = 사랑하는 사람만큼", "hl2"))),
            show("s1_where", "그럼 사람에게 향하는, 배울 수 있는 것이 무엇인지 생각하며 문장 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
            show("s1_board", "mettā는 benevolence(자비심)라는 뜻이래요.",
                 panel=board(W1, fresh=("benevolence",)), highlight=["benevolence"], button="다음"),
            # 단어 지도 — 첫 단어(benevolence)는 선생님, 다음 말은 학생이 찾아 넣는다
            pick("s1_same", "benevolence와 같은 쪽 말 두 개를 더 찾아 눌러 볼까요?",
                 ["pali", "mettā", "kindness", "tenderness"], ["kindness", "tenderness"],
                 "그건 benevolence와 같은 쪽 말이 아니에요.",
                 "kindness(친절), tenderness(다정함)도 benevolence와 같은 쪽이에요. 모두 사람을 따뜻하게 대하는 마음이에요.",
                 praise="다 찾았어요!",
                 wrong_by={"pali": "pali는 언어 이름이에요.", "mettā": "mettā는 뜻을 풀어 줄 낱말이에요. means(뜻하다) 뒤에서 찾아봐요."}),
            show("s1_map", "단어 지도에 넣었어요.", panel=board(W2, fresh=("kindness", "tenderness")), button="다음 문장"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("It", "그것(mettā)"), g("is", "~이다"), g("one of the most important ideas", "가장 중요한 생각 중 하나"),
                    g("in Buddhism", "불교에서"), g("Buddhism", "불교")],
        "slashes": ["important ideas"],
        "roles": [r("It", "S"), r("is", "V"), r("one of the most important ideas", "C")],
        "steps": [
            show("s2_note", "It은 앞 문장의 mettā예요. 불교에서 가장 중요한 생각 중 하나래요.",
                 highlight=["one of the most important ideas"], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("Buddhism", "불교는"), g("recommends", "권하다"), g("a daily ritual meditation", "매일 의례적으로 하는 명상"),
                    g("ritual", "의례적인"), g("meditation", "명상"), g("(known as mettā bhāvanā)", "(mettā bhāvanā로 알려진)"),
                    g("to foster this attitude", "이 태도를 기르기 위해"), g("foster", "기르다, 키우다"), g("this attitude", "이 태도"),
                    g("to foster", "기르기 위해")],
        "slashes": ["recommends", "ritual meditation", "mettā bhāvanā)"],
        "roles": [r("Buddhism", "S"), r("recommends", "V"), r("a daily ritual meditation", "O")],
        "steps": [
            choice("s3_attitude",
                   "this attitude(이 태도)는 무엇을 가리킬까요?",
                   [("o0", "명상할 때 앉는 자세", False), ("o1", "불교의 규칙", False),
                    ("o2", "mettā — 자비심, 친절, 다정함", True)],
                   "this는 앞에서 말한 것을 가리켜요. 지금까지 칠판에 모은 말을 떠올려 봐요.",
                   why="this attitude는 앞에서 말한 mettā, 즉 자비심·친절·다정함이에요. attitude는 '자세'보다 '태도, 마음가짐'이에요.",
                   levels=["중", "초"], highlight=["this attitude"], faded=["(known as mettā bhāvanā)"],
                   tips=[tip("this + 명사", "this attitude처럼 this가 붙으면 앞에서 말한 것을 가리켜요. 앞 문장에서 찾아요.", "this attitude")]),
            choice("s3_foster",
                   "to foster this attitude는 무슨 뜻일까요?",
                   [("o0", "이 태도를 버리기 위해", False), ("o1", "이 태도를 기르기 위해", True),
                    ("o2", "이 태도를 숨기기 위해", False)],
                   "foster는 '기르다, 키우다'예요. to 뒤 동사는 '~하기 위해'로 읽어요.",
                   why="foster는 '기르다', to foster는 '기르기 위해'예요. 명상으로 이 태도를 기른대요.",
                   highlight=["foster"], faded=["(known as mettā bhāvanā)"],
                   tips=[tip("foster", "'기르다, 키우다'예요. 마음이나 태도를 키울 때도 써요.", "foster")]),
            show("s3_map", "명상(meditation)은 방법이고, 기르는 건 this attitude(자비심 같은 마음)예요.",
                 panel=board(W3, fresh=("this attitude",)), highlight=["meditation", "this attitude"], button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("The meditation", "그 명상"), g("begins with", "~으로 시작하다"), g("a call", "요구, 요청"),
                    g("to think", "생각하라는"), g("carefully every morning", "매일 아침 사려 깊게"), g("of an individual", "어떤 한 사람을"),
                    g("an individual", "어떤 한 사람"), g("with whom one tends to get irritated", "함께 있으면 짜증이 나는"),
                    g("irritated", "짜증 난"), g("to whom one feels aggressive or cold", "공격적이거나 냉담한 기분이 드는"),
                    g("aggressive", "공격적인"), g("cold", "차가운, 냉담한"),
                    g("in place of one’s normal hostile impulses", "평소의 적대적인 충동 대신"), g("in place of", "~ 대신"),
                    g("hostile", "적대적인"), g("impulses", "충동"), g("hostile impulses", "적대적인 충동"),
                    g("to rehearse", "연습하라는"), g("rehearse", "연습하다, 되뇌다"), g("kindly messages", "친절한 메시지"),
                    g("like", "~ 같은"), g("‘I hope you will find peace’", "'당신이 평안을 찾길 바라요'"),
                    g("‘I wish you to be free from suffering’", "'당신이 고통에서 벗어나길 바라요'")],
        "slashes": ["begins with a call", "every morning", "of an individual", "get irritated", "aggressive or cold and", "hostile impulses —",
                    "kindly messages"],
        "roles": [r("The meditation", "S"), r("begins with", "V"), r("a call", "O")],
        "modifiers": ["with whom one tends to get irritated", "to whom one feels aggressive or cold"],
        "steps": [
            sv("s4_sv", ["The meditation", "begins with", "a call", "an individual", "kindly messages"],
               {"The meditation": "S", "begins with": "V", "a call": "전목"},
               {"an individual": "그건 think … of(~을 생각하다) 뒤, 생각할 대상이에요. 문장 맨 앞에서 찾아봐요.",
                "kindly messages": "그건 to rehearse(연습하라는) 뒤의 말이에요. 문장 맨 앞에서 찾아봐요."},
               "주어는 The meditation, 동사는 begins with, 전치사 뒤 목적어는 a call(요구)이에요.",
               ask="아주 긴 문장이에요. 주어(S), 동사(V), with 뒤 목적어(전목)를 찾아볼까요?",
               faded=["— in place of one’s normal hostile impulses —"]),
            choice("s4_two",
                   "a call(요구) 뒤에 to가 두 번 나와요. 무엇을 하라는 요구일까요?",
                   [("o0", "짜증 나는 사람을 떠올리고, 그 사람에게 친절한 말을 연습하라", True),
                    ("o1", "짜증 나는 사람을 멀리하고, 좋아하는 사람만 떠올려라", False),
                    ("o2", "마음을 편히 쉬고, 아무 생각도 하지 마라", False)],
                   "to think … of an individual과 to rehearse kindly messages, 두 덩어리를 봐요.",
                   why="'to think … of an individual'은 그 사람을 생각하라, 'to rehearse kindly messages'는 친절한 말을 연습하라예요. 싫은 사람을 피하지 않고 떠올려요.",
                   highlight=["to think", "to rehearse"], faded=["— in place of one’s normal hostile impulses —"],
                   tips=[tip("think … of A", "think of A는 'A를 생각하다'예요. 여기선 사이에 carefully every morning이 끼어 있어요.", "think"),
                         tip("with whom / to whom", "'그 사람과 함께 ~하는 / 그 사람에게 ~하는'이에요. 앞의 an individual을 꾸며요.", "with whom")]),
            choice("s4_sort",
                   "in place of(~ 대신) 뒤 'one’s normal hostile impulses(평소의 적대적인 충동)'는 칠판 어느 쪽일까요?",
                   [("o0", WARM, False), ("o1", COLD, True)],
                   "hostile은 '적대적인'이에요. 앞의 irritated(짜증 난), aggressive(공격적인), cold(냉담한)와 같은 쪽이에요.",
                   panel=board(W3, [], sort=["hostile impulses"]), highlight=["hostile"]),
            show("s4_map", "평소엔 짜증·공격·냉담 같은 마음이 들어요. 그 대신 친절한 말(kindly messages)을 연습해요.",
                 panel=board(W4, C4, fresh=("kindly messages", "irritated", "aggressive · cold", "hostile impulses")),
                 highlight=["kindly messages"], highlight_alt=["irritated", "hostile"], button="다음 문장",
                 tips=[tip("in place of", "'~ 대신에'예요. in place of A, B = A 대신 B.", "in place of")]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("This practice", "이 수행"), g("practice", "수행, 연습"), g("can be extended", "확장될 수 있다"),
                    g("outwards ultimately", "밖으로, 결국"), g("outwards", "밖으로"), g("ultimately", "결국"),
                    g("to include", "포함하도록"), g("pretty much", "거의"), g("everyone on Earth", "지구상의 모든 사람")],
        "slashes": ["can be extended", "outwards ultimately"],
        "roles": [r("This practice", "S"), r("can be extended", "V")],
        "steps": [
            show("s5_note", "이 연습은 결국 지구상의 거의 모든 사람으로 넓힐 수 있대요. 싫은 사람까지 다요.",
                 highlight=["extended", "everyone on Earth"], button="다음 문장",
                 tips=[tip("pretty much", "'거의'예요. pretty much everyone = 거의 모든 사람.", "pretty much")]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("The background assumption", "배경이 되는 가정"), g("assumption", "가정"), g("is", "~이다"),
                    g("with the right stimulus", "적절한 자극이 있으면"), g("the right stimulus", "적절한 자극"), g("stimulus", "자극"),
                    g("our feelings", "우리의 감정"), g("towards people", "사람들을 향한"), g("are", "~이다"),
                    g("not fixed and unalterable", "고정되어 바뀔 수 없는 게 아니라"), g("fixed", "고정된"), g("unalterable", "바꿀 수 없는"),
                    g("open to", "~의 여지가 있는, ~에 열려 있는"), g("deliberate", "의도적인, 계획적인"),
                    g("deliberate change and improvement", "의도적인 변화와 개선"), g("improvement", "개선"),
                    g("not fixed", "고정된 게 아니라"), g("open to change", "바뀔 여지가 있는")],
        "slashes": ["assumption is", "that,", "right stimulus,", "towards people", "unalterable,"],
        "roles": [r("The background assumption", "S"), r("is", "V"), r("our feelings", "S"), r("are", "V"),
                  r("not fixed and unalterable", "C"), r("open to deliberate change and improvement", "C")],
        "steps": [
            sv("s6_sv", ["The background assumption", "is", "the right stimulus", "our feelings"],
               {"The background assumption": "S", "is": "V"},
               {"the right stimulus": "그건 with(~이 있으면) 뒤 덩어리예요. 전치사 뒤라 주어가 아니에요.",
                "our feelings": "그건 that 뒤 덩어리 안의 주어예요. that 앞에서 찾아봐요."},
               "주어는 The background assumption, 동사는 is예요. is 뒤 that 덩어리가 그 가정의 내용이에요."),
            choice("s6_notbut",
                   "not A but B예요. 사람을 향한 우리 감정은 어떻다는 걸까요?",
                   [("o0", "고정돼 있어서 바꿀 수 없다", False), ("o1", "일부러 바꾸고 나아지게 할 수 있다", True),
                    ("o2", "자극이 없어도 저절로 바뀐다", False)],
                   "not A but B는 'A가 아니라 B'예요. but 뒤 'open to deliberate change'를 봐요.",
                   why="'not fixed and unalterable, but open to deliberate change and improvement', 고정된 게 아니라 의도적인 변화와 개선의 여지가 있대요.",
                   highlight=["not fixed", "but open"],
                   tips=[tip("not A but B", "'A가 아니라 B'예요. 글쓴이 생각은 B 쪽이에요.", "but"),
                         tip("open to ~", "'~의 여지가 있는, ~에 열려 있는'이에요. open to change = 바뀔 여지가 있는.", "open to")]),
            show("s6_note", "감정도 연습으로 바꿀 수 있대요. 그래서 평소 마음 대신 mettā 쪽 마음을 연습하는 거예요.",
                 panel=board(W4, C4), button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": BLANK, "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("is", "~이다"), g("a learnable skill", "배울 수 있는 기술"), g("learnable", "배울 수 있는"), g("we", "우리는"),
                    g("need", "~할 필요가 있다"), g("to direct it", "그것을 향하게 하는 것"), g("direct", "향하게 하다"),
                    g("as much towards", "~에게도 (…만큼) 똑같이"),
                    g("those we are tempted to dismiss and detest", "우리가 무시하고 혐오하고 싶은 사람들"),
                    g("tempted", "~하고 싶은 마음이 드는"), g("dismiss", "무시하다"), g("detest", "혐오하다"),
                    g("as to those we love", "우리가 사랑하는 사람들에게만큼")],
        "slashes": ["learnable skill,", "direct it", "towards those", "and detest", "as to those"],
        "roles": [r("is", "V"), r("a learnable skill", "C"), r("we", "S"), r("need", "V"), r("to direct it", "O")],
        "modifiers": ["we are tempted to dismiss and detest", "we love"],
        "steps": [
            sv("s7_sv", ["is", "a learnable skill", "we", "need", "to direct it", "those we are tempted to dismiss and detest"],
               {"is": "V", "a learnable skill": "C", "we": "S", "need": "V", "to direct it": "O"},
               {"those we are tempted to dismiss and detest": "그건 towards(~을 향해) 뒤 덩어리예요. 전치사 뒤라 주어·목적어가 아니에요."},
               "빈칸이 주어, is가 동사, a learnable skill이 보어예요. and 뒤는 주어 we, 동사 need, 목적어 to direct it이에요.",
               ask="빈칸이 주어예요. 빈칸 뒤 동사(V)·보어(C)와 and 뒤 주어(S)·동사(V)·목적어(O)를 찾아볼까요?"),
            choice("s7_fill",
                   "빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "마음을 편히 쉬게 하는 것", False), ("o1", "다른 사람을 따뜻하게 대하는 마음", True),
                    ("o2", "자기 생각이 옳다고 설명하는 것", False)],
                   "it(빈칸)을 싫은 사람에게도 '향하게(direct)' 한대요. 칠판 mettā 쪽 말을 떠올려 봐요.",
                   why="빈칸(it)은 싫은 사람에게도 사랑하는 사람만큼 향하게 하는 거예요. 사람을 향하는 마음, 칠판 mettā 쪽 말이에요.",
                   panel=board(W4, C4), highlight=["direct", "detest", "love"]),
            choice("s7_side",
                   "글쓴이 주장은 '사람을 향한 감정은 연습으로 바꿀 수 있다'예요. 빈칸은 이 주장과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 (배워서 기를 수 있는 마음)", True), ("o1", "반대 쪽 (바꿀 수 없는 마음)", False)],
                   "빈칸 바로 뒤 learnable(배울 수 있는)을 봐요. 앞 문장은 감정이 not fixed, but open to change라고 했어요.",
                   why="빈칸은 learnable(배울 수 있는) 기술이래요. 감정은 바꿀 수 있다는 주장과 같은 쪽이에요.",
                   highlight=["learnable"], point="빈칸 = 배울 수 있고(learnable), 싫은 사람에게도 향하게 할 마음 = mettā 쪽 = 주장과 같은 쪽"),
            show("s7_go", "빈칸은 mettā 쪽, 사람을 향한 따뜻한 마음이에요. 이 말을 한 단어로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 초급 기본 — 문장마다 하나 (빈칸 문장 제외)
add_basic(sentences, 1, [m("mettā", "mettā는"), " ", m("benevolence, kindness or tenderness", "자비심, 친절 혹은 다정함"), "을 ",
                         m("means", "뜻한다"), "."],
          sv_new=sv_step("s1_basic_sv", ["In the Indian language of pali", "mettā", "means", "benevolence, kindness or tenderness"],
                         {"mettā": "S", "means": "V", "benevolence, kindness or tenderness": "O"},
                         {"In the Indian language of pali": "그건 '어디에서'를 알려 주는 말이에요."},
                         "주어는 mettā, 동사는 means, 목적어는 benevolence, kindness or tenderness예요."),
          meaning_ids=["s1_board"])
add_basic(sentences, 2, [m("It", "그것은"), " ", m("in Buddhism", "불교에서"), " ", m("one of the most important ideas", "가장 중요한 생각 중 하나"),
                         m("is", "이다"), "."],
          sv_new=sv_step("s2_basic_sv", ["It", "is", "one of the most important ideas", "Buddhism"],
                         {"It": "S", "is": "V", "one of the most important ideas": "C"},
                         {"Buddhism": "그건 in 뒤 덩어리예요. 전치사 뒤라 주어가 아니에요."},
                         "주어는 It(mettā), 동사는 is, 보어는 one of the most important ideas예요."),
          meaning_ids=["s2_note"])
add_basic(sentences, 3, [m("Buddhism", "불교는"), " ", m("to foster this attitude", "이 태도를 기르기 위해"), " ",
                         m("a daily ritual meditation", "매일 의례적으로 하는 명상"), "을 ", m("recommends", "권한다"), "."],
          match_display="Buddhism recommends a daily ritual meditation to foster this attitude.",
          sv_new=sv_step("s3_basic_sv", ["Buddhism", "recommends", "a daily ritual meditation", "this attitude"],
                         {"Buddhism": "S", "recommends": "V", "a daily ritual meditation": "O"},
                         {"this attitude": "그건 to foster(기르기 위해) 뒤의 말이에요."},
                         "주어는 Buddhism, 동사는 recommends, 목적어는 a daily ritual meditation이에요."),
          meaning_ids=["s3_foster"])
add_basic(sentences, 4, [m("The meditation", "명상은"), " ", m("an individual", "어떤 한 사람"), "을 ", m("to think", "생각하고"), " ",
                         m("kindly messages", "친절한 메시지"), "를 ", m("to rehearse", "연습하라는"), " ", m("a call", "요구"), "으로 ",
                         m("begins with", "시작한다"), "."],
          match_display="The meditation begins with a call to think of an individual and to rehearse kindly messages.",
          sv_id="s4_sv", meaning_ids=["s4_two"])
add_basic(sentences, 5, [m("This practice", "이 수행은"), " ", m("everyone on Earth", "지구상의 모든 사람"), "을 ", m("to include", "포함하도록"),
                         " ", m("can be extended", "확장될 수 있다"), "."],
          match_display="This practice can be extended to include everyone on Earth.",
          sv_new=sv_step("s5_basic_sv", ["This practice", "can be extended", "everyone on Earth"],
                         {"This practice": "S", "can be extended": "V"},
                         {"everyone on Earth": "그건 to include(포함하도록) 뒤의 말이에요."},
                         "주어는 This practice, 동사는 can be extended예요."),
          meaning_ids=["s5_note"])
add_basic(sentences, 6, [m("The background assumption", "배경이 되는 가정은"), " — ", m("our feelings", "우리의 감정이"), " ",
                         m("not fixed", "고정된 게 아니라"), " ", m("open to change", "바뀔 여지가 있다"), "는 것."],
          match_display="The background assumption is that our feelings are not fixed, but open to change.",
          sv_id="s6_sv", meaning_ids=["s6_notbut"])
add_that_sv(sentences, 6, "s6_sv", "s6_that_sv", ["our feelings", "towards people", "are", "the right stimulus"],
            {"our feelings": "S", "are": "V"},
            {"towards people": "그건 앞의 our feelings를 꾸며 주는 말이에요(사람들을 향한).",
             "the right stimulus": "그건 with(~이 있으면) 뒤 덩어리예요."},
            "that 안의 주어는 our feelings, 동사는 are예요. 사람을 향한 우리 감정이 어떻다는 내용이에요.")

SENSES = {
    3: [sense("as", "known as", "~로 (알려진)", "be known as + 명사 = ~로 알려지다"),
        sense("to", "to foster", "~하기 위해", "to부정사 (목적)")],
    4: [sense("to", "a call to think", "~하라는", "명사 + to부정사 (a call to ~ = ~하라는 요구)"),
        sense("to", "tends to get", "~하는 (경향이 있다)", "tend to + 동사원형 = ~하는 경향이 있다"),
        sense("to", "to whom", "~에게", "전치사 to + whom (그 사람에게)"),
        sense("to", "to rehearse", "~하라는", "a call에 이어지는 둘째 to부정사"),
        sense("to", "wish you to be", "~하기를", "wish + 사람 + to부정사 = 사람이 ~하기를 바라다")],
    5: [sense("to", "to include", "~하도록, (결국) ~하게", "to부정사 (결과)")],
    6: [sense("that", "is that", "~라는 것", "명사절 that (be동사 뒤 보어)"),
        sense("but", "but open", "~이 아니라 (…이다)", "not A but B"),
        sense("to", "open to", "~에 (열려 있는)", "open to + 명사 = ~의 여지가 있는")],
    7: [sense("to", "to direct", "~하는 것을", "need + to부정사"),
        sense("as", "as much towards", "~만큼 (똑같이)", "as much A as B (앞 as)"),
        sense("to", "tempted to dismiss", "~하고 싶은", "be tempted to + 동사원형"),
        sense("as", "as to those", "~에게만큼", "as much A as B (뒤 as — 비교 대상 앞)"),
        sense("to", "as to those", "~에게", "전치사 to (direct it to ~)")],
}

WORDS = {"indian": "인도의", "language": "언어", "pali": "팔리어", "mettā": "메타 · 팔리어 낱말", "bhāvanā": "바와나 · 수행",
         "known": "알려진", "daily": "매일의", "ritual": "의례적인", "meditation": "명상", "attitude": "태도, 마음가짐",
         "important": "중요한", "ideas": "생각, 관념", "buddhism": "불교", "carefully": "사려 깊게, 신중히", "every": "모든, ~마다",
         "morning": "아침", "individual": "개인, 한 사람", "whom": "그 사람(을)", "tends": "~하는 경향이 있다", "feels": "느끼다",
         "normal": "평소의", "one’s": "자신의", "kindly": "친절한", "messages": "메시지", "hope": "바라다", "will": "~할 것이다",
         "peace": "평안", "wish": "바라다", "free": "벗어난, 자유로운", "suffering": "고통", "call": "요구, 요청",
         "begins": "시작하다", "think": "생각하다", "practice": "수행, 연습", "extended": "확장된", "include": "포함하다",
         "pretty": "꽤 · pretty much = 거의", "earth": "지구", "background": "배경", "right": "알맞은, 적절한",
         "feelings": "감정", "towards": "~을 향한", "change": "변화", "skill": "기술", "those": "사람들", "love": "사랑하다",
         "messages.": "메시지", "find": "찾다", "be": "~이다, ~하게 되다", "most": "가장", "people": "사람들", "can": "~할 수 있다",
         "meditation.": "명상", "get": "~하게 되다", "tempted": "~하고 싶은 마음이 드는", "dismiss": "무시하다", "detest": "혐오하다",
         "direct": "향하게 하다", "learnable": "배울 수 있는", "rehearse": "연습하다", "hostile": "적대적인", "impulses": "충동",
         "irritated": "짜증 난", "aggressive": "공격적인", "foster": "기르다", "fixed": "고정된", "unalterable": "바꿀 수 없는",
         "deliberate": "의도적인", "improvement": "개선", "stimulus": "자극", "assumption": "가정", "outwards": "밖으로", "ultimately": "결국", "open": "열려 있는"}

STORIES = [
    (3, [sc("문장 1~2", "🤲", "mettā = benevolence · kindness", "mettā는 자비심·친절·다정함 — 불교에서 가장 중요한 생각이에요"),
         sc("문장 3", "🧘", "meditation → foster this attitude", "매일 하는 명상으로 이 태도를 길러요")]),
    (5, [sc("문장 4", "💌", "irritated → kindly messages", "짜증 나는 사람을 떠올리고, 적대감 대신 친절한 말을 연습해요"),
         sc("문장 5", "🌍", "everyone on Earth", "결국 거의 모든 사람으로 넓혀요")]),
    (6, [sc("문장 6", "🔄", "not fixed, but open to change", "사람을 향한 감정은 고정된 게 아니라 바꿀 수 있어요"),
         sc("빈칸 문장", "🎯", "________ = a learnable skill", "____은 배울 수 있는 기술 — 싫은 사람에게도 향하게 해야 해요")]),
]

OPTIONS = [("1", "Creativity", "창의성", False), ("2", "Relaxation", "긴장 완화", False), ("3", "Compassion", "연민", True),
           ("4", "Justification", "정당화", False), ("5", "Empowerment", "권한 부여", False)]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 7, "analysis_first": True, "wrong_rate": 65.0, "wrong_rank": 2,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("Creativity", "창의성"), g("Relaxation", "긴장 완화, 휴식"), g("Compassion", "연민, 동정심"),
                g("Justification", "정당화"), g("Empowerment", "권한 부여")],
    "options": [{"id": o[0], "label": o[1], "keywords": [o[1]], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "칠판의 mettā 쪽 말을 한 단어로 바꾼 보기를 골라 봐요.",
        "정답이에요! mettā는 자비심·친절·다정함이고, 이런 마음은 연습으로 기를 수 있대요. 싫은 사람에게도 향하게 할 연민(Compassion)이에요.",
        "정답은 ③ Compassion(연민)이에요. 싫은 사람에게도 사랑하는 사람만큼 향하게 할, 배울 수 있는 따뜻한 마음이에요.",
        {"1": "창의성은 새것을 만들어 내는 힘이에요. 글은 사람을 향한 마음을 기르는 이야기예요.",
         "2": "명상(meditation)이 나와서 긴장 완화가 떠오르지만, 빈칸은 싫은 사람에게도 '향하게(direct)' 하는 마음이에요.",
         "4": "정당화는 옳다고 설명하는 거예요. 글에는 그런 이야기가 없어요.",
         "5": "권한 부여는 힘이나 자격을 주는 거예요. 글은 친절·다정함 같은 마음 이야기예요."},
        {"2": review(42,
                     "글에 meditation(명상)이 나와서 Relaxation(긴장 완화)을 가장 많이 골랐어요. 하지만 빈칸(it)은 싫은 사람에게도, 사랑하는 사람에게만큼 '향하게(direct)' 해야 하는 거예요. 긴장 완화는 사람에게 향하는 마음이 아니에요.",
                     panel=rows(("mettā 쪽", "benevolence · kindness · this attitude", "사람을 따뜻하게 대하는 마음", "hl"),
                                ("빈칸 문장", "direct it towards those we … detest", "싫은 사람에게도 향하게 한다", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 31번 (빈칸 추론, 2점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 같은 말 모으기 → 빈칸이 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-metta-meditation.svg", ("Mettā", "자비심 명상"), "→", ("Feelings", "사람을 향한 감정"),
                                       "싫은 사람에게도 따뜻해질 수 있을까?", "2022년 3월 31번 도입 칠판"),
                      "alt": "칠판: Mettā(자비심 명상) → Feelings(사람을 향한 감정)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "싫은 사람에게도 따뜻한 마음을 가질 수 있을까요? 이번 글은 불교의 mettā 명상 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("benevolence", "자비심"), g("tenderness", "다정함"), g("ritual", "의례적인"), g("meditation", "명상"),
                           g("foster", "기르다"), g("attitude", "태도"), g("irritated", "짜증 난"), g("aggressive", "공격적인"),
                           g("hostile", "적대적인"), g("impulse", "충동"), g("in place of", "~ 대신에"), g("rehearse", "연습하다"),
                           g("extend", "확장하다"), g("ultimately", "결국"), g("assumption", "가정"), g("stimulus", "자극"),
                           g("unalterable", "바꿀 수 없는"), g("deliberate", "의도적인"), g("be tempted to", "~하고 싶은 마음이 생기다"),
                           g("dismiss", "무시하다"), g("detest", "혐오하다")],
               "options": [g("compassion", "연민"), g("relaxation", "긴장 완화"), g("justification", "정당화"),
                           g("empowerment", "권한 부여")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# call 요구 · practice 수행 · direct 향하게 하다.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    4: [tip("call", "이 글에서는 → 요구  ('전화, 부르다' 아님)", "call", trap=True)],
    5: [tip("practice", "이 글에서는 → 수행  ('연습' 아님)", "practice", trap=True)],
    7: [tip("direct", "이 글에서는 → 향하게 하다  ('직접적인' 아님)", "direct", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법",
       chunks={"In the Indian language of pali": "인도의 팔리어에서", "mettā": "mettā", "means": "뜻하다",
               "benevolence, kindness or tenderness": "자비심, 친절 혹은 다정함", "It": "그것(mettā)", "is": "~이다",
               "one of the most important ideas": "가장 중요한 생각 중 하나", "Buddhism": "불교", "recommends": "권하다",
               "a daily ritual meditation": "매일 의례적으로 하는 명상", "this attitude": "이 태도", "The meditation": "그 명상",
               "begins with": "~으로 시작하다", "a call": "요구", "an individual": "어떤 한 사람", "kindly messages": "친절한 메시지",
               "This practice": "이 수행", "can be extended": "확장될 수 있다", "everyone on Earth": "지구상의 모든 사람",
               "The background assumption": "배경이 되는 가정", "the right stimulus": "적절한 자극", "our feelings": "우리의 감정",
               "towards people": "사람들을 향한", "are": "~이다", "a learnable skill": "배울 수 있는 기술", "we": "우리는",
               "need": "~할 필요가 있다", "to direct it": "그것을 향하게 하는 것",
               "those we are tempted to dismiss and detest": "우리가 무시하고 혐오하고 싶은 사람들", "pali": "팔리어",
               "kindness": "친절", "tenderness": "다정함", "in Buddhism": "불교에서", "to foster this attitude": "이 태도를 기르기 위해",
               "to think": "생각하라는", "to rehearse": "연습하라는", "to include": "포함하도록", "not fixed": "고정된 게 아니라",
               "open to change": "바뀔 여지가 있는"})
