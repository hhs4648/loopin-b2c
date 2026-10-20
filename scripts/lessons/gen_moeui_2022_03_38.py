"""2022년 3월 고3 38번 레슨 + 대사를 만든다 (주어진 문장 넣기, 2점). 오답률 40.0% · Top 11.

    py scripts/lessons/gen_moeui_2022_03_38.py   (→ node scripts/policy_copy.mjs stamp <id> → npm run build)

틀: docs/tutor/templates/README.md + 2024년 3월 38·39번(문장 넣기) — 주어진 문장 단서 → 앞 내용 예측 → ①~⑤ 흐름 확인.
정답 ④. 많이 고른 오답 ⑤ 15% — ⑤ 뒤 문장에도 more elaborate가 있어 낱말만 보고 끌린다.
열쇠: 주어진 문장 But many signals … go through changes ↔ ④ 앞 Some signals … remain much the same.
④ 뒤 slight variations(약간의 차이)는 '변화'가 먼저 나와야 이어진다 — ③문장 '거의 똑같이 남는다' 바로 뒤엔 어색하다.
주어진 문장 정석(insertion-given-sentence-order): But → 앞은 반대(변하지 않음). 「뒤에 무엇?」은 묻지 않는다.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
bizarre는 시험지 아래 *로 풀어 준 단어라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt). Claude 초안 — 선생님 검토 전.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2022-03-38-animal-signals"

GIVEN = ("But many signals, as they are passed from generation to generation by whatever means, go through changes "
         "that make them either more elaborate or simply different.")
S = [
    "Many of the ritualized displays performed by animals look so bizarre to us that we wonder how they came about.",
    "(①) Most of the various forms of signaling that are used by different species of animals have not arisen afresh "
    "in each separate species.",
    "(②) As one species evolves into another, particular forms of signaling may be passed on, owing to the effects of "
    "both genes and learning or experience.",
    "(③) Some signals have significance across many species, and so remain much the same over generations and in a number of species.",
    "(④) If we examine closely related species, we can often see slight variations in a particular display and we can piece "
    "together an explanation for the spread of the display across species.",
    "(⑤) Some very elaborate displays may have begun as simpler versions of the same behavioral pattern that became more "
    "elaborate as they developed and were passed on from generation to generation.",
]
KO = [
    "동물들이 행하는 의례화된 표현 중에 많은 것이 우리에게 너무 기이하게 보여서 우리는 그런 표현이 어떻게 생겨났는지 궁금해 한다.",
    "여러 종의 동물들에 의해 사용되는 다양한 신호 보내기 형식의 대부분은 각 개별 종에서 새로 생겨나지 않았다.",
    "하나의 종이 다른 종으로 진화하면서, 유전자 및 학습이나 경험의 영향 때문에 특정한 신호 보내기 형식이 전달될 수도 있다.",
    "몇몇 신호들은 여러 종에 걸쳐서 중요성을 지니며, 그래서 세대를 넘어, 그리고 많은 종에 거의 똑같이 남아 있다.",
    "밀접하게 관련된 종을 조사하면, 우리는 하나의 특정한 표현에서 약간의 차이를 자주 볼 수 있고, 여러 종에 걸친 그 표현의 확산에 대한 설명을 종합할 수 있다.",
    "매우 정교한 몇몇 표현은 그것이 발전하고 대대로 전달될 때 더 정교해졌던, 똑같은 행동 양식의 더 단순한 형태로 시작했을지도 모른다.",
]

SAME = "왼쪽 · 거의 그대로 남는다"
CHANGE = "오른쪽 · 변한다"
R0 = [("go through changes", "변화를 겪는다"), ("more elaborate", "더 정교한")]


def board(left, right, fresh=(), sort=None):
    return groups("대대로 전해지는 신호", "거의 그대로 남는다", left, "변한다", right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": SAME, "right": CHANGE} if sort else None)


def flow(id, n, before, after, ok, why):
    """①~⑤ 자리마다 — 앞 문장과 뒤 문장이 그대로 이어지나"""
    return choice(id, f"{n} 자리예요. '{before}' → '{after}', 자연스럽게 이어지나요?",
                  [("o0", "네, 이어져요", ok), ("o1", "아니요, 끊겨요", not ok)], why, why=why)


sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN, "teaching_value": "high",
        "model_translation": "그러나 많은 신호가 어떤 방법에 의해서든 대대로 전달될 때 그것을 더욱 정교하게 또는 단순히 다르게 만드는 변화를 겪는다.",
        "glosses": [g("But", "하지만"), g("many signals", "많은 신호"), g("as they are passed", "그것들이 전해질 때"),
                    g("from generation to generation", "대대로, 세대에서 세대로"), g("by whatever means", "어떤 방법으로든"),
                    g("go through changes", "변화를 겪다"), g("go through", "겪다"), g("changes", "변화"),
                    g("make them", "그것들을 ~하게 만들다"), g("either more elaborate or simply different", "더 정교하게 또는 그냥 다르게"),
                    g("elaborate", "정교한, 공들인"), g("means", "방법, 수단")],
        "emphasis": ["go through changes"],
        "slashes": ["But many signals,", "are passed", "to generation", "whatever means,", "go through changes", "make them"],
        "roles": [r("many signals", "S"), r("go through", "V"), r("changes", "O"), r("they", "S"), r("are passed", "V")],
        "modifiers": ["that make them either more elaborate or simply different"],
        "steps": [
            sv("g_sv", ["many signals", "they", "are passed", "go through", "changes", "make"],
               {"many signals": "S", "go through": "V", "changes": "O"},
               {"they": "그건 콤마 사이 as(~할 때) 덩어리 안의 주어예요.",
                "are passed": "그건 콤마 사이 as(~할 때) 덩어리 안의 동사예요.",
                "make": "그건 that 뒤 덩어리 안의 동사예요. 앞의 changes를 꾸며 줘요."},
               "주어는 many signals, 동사는 go through, 목적어는 changes예요. 콤마 사이 as 덩어리는 '전해질 때'라는 때를 알려 줘요.",
               ask="긴 문장이에요. 콤마 사이 덩어리는 잠깐 두고 주어(S), 동사(V), 목적어(O)를 찾아볼까요?"),
            choice("g_elab",
                   "'changes that make them either more elaborate or simply different'는 무슨 뜻일까요?",
                   [("o0", "신호를 더 정교하게 또는 그냥 다르게 만드는 변화", True), ("o1", "신호를 더 단순하게 만드는 변화", False),
                    ("o2", "신호를 처음 그대로 지켜 주는 변화", False)],
                   "elaborate는 '정교한, 공들인'이에요. either A or B는 'A 또는 B'예요.",
                   why="elaborate는 '정교한'이에요. 신호가 대대로 전해지면서 더 정교해지거나 그냥 달라진대요.",
                   highlight=["either more elaborate or simply different"],
                   tips=[tip("either A or B", "'A 또는 B (둘 중 하나)'예요. either more elaborate or simply different = 더 정교하게 또는 그냥 다르게.", "either")]),
            show("g_board", "신호가 대대로 전해지면서 변한대요.",
                 panel=board([], R0, fresh=("go through changes", "more elaborate")), highlight=["go through changes"]),
            choice("g_before",
                   "주어진 문장은 But(하지만)으로 시작해요. 그럼 바로 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "신호가 더 정교해진다는 내용", False), ("o1", "동물이 신호를 보내는 이유", False),
                    ("o2", "신호가 변하지 않고 거의 그대로 남는다는 내용", True)],
                   "But은 앞 내용을 뒤집어요. go through changes(변화를 겪는다)와 반대되는 말을 떠올려 봐요.",
                   why="But은 앞 내용을 뒤집어요. 뒤가 '변화를 겪는다'니까, 바로 앞에는 '변하지 않고 그대로 남는다'가 와야 해요.",
                   highlight=["But", "go through changes"],
                   tips=[tip("But으로 시작하는 주어진 문장", "But, However로 시작하면 바로 앞에는 반대되는 내용이 있어야 해요.")],
                   point="But many signals … go through changes → 바로 앞 = 신호가 변하지 않는다는 내용"),
        ],
    },
    {
        "id": 2, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("Many of the ritualized displays", "의례화된 표현 중 많은 것"), g("performed by animals", "동물이 행하는"),
                    g("look so bizarre", "너무 기이해 보이다"), g("to us", "우리에게"), g("we wonder", "우리는 궁금해한다"),
                    g("how they came about", "그것들이 어떻게 생겨났는지"), g("came about", "생겨났다"),
                    g("ritualized", "의례화된 · 늘 같은 틀로 되풀이되는"),
                    g("displays", "표현 · 여기서는 동물이 몸짓으로 보여 주는 행동이에요"), g("bizarre", "기이한")],
        "slashes": ["ritualized displays", "performed by animals", "so bizarre to us", "we wonder"],
        "roles": [r("Many of the ritualized displays", "S"), r("look", "V"), r("so bizarre", "C"), r("we", "S"), r("wonder", "V")],
        "modifiers": ["performed by animals"],
        "steps": [
            choice("s1_display",
                   "여기서 displays는 무슨 뜻일까요?",
                   [("o0", "화면, 디스플레이", False), ("o1", "동물이 몸짓으로 보여 주는 행동", True), ("o2", "물건을 늘어놓은 전시회", False)],
                   "performed by animals(동물이 행하는)가 꾸며 줘요. 동물이 '하는' 것이에요.",
                   why="performed by animals(동물이 행하는)가 꾸며 줘요. 여기서 display는 동물이 몸짓으로 보여 주는 표현(행동)이에요.",
                   levels=["중", "초"], highlight=["displays"]),
            show("s1_show", "동물이 보여 주는 표현(displays) 중엔 너무 기이해서 어떻게 생겨났는지 궁금한 게 많대요.",
                 highlight=["how they came about"], button="다음 문장",
                 tips=[tip("so ~ that …", "'너무 ~해서 …하다'예요. so bizarre that we wonder = 너무 기이해서 우리는 궁금해한다.", "so")]),
        ],
    },
    {
        "id": 3, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Most of the various forms of signaling", "다양한 신호 형식의 대부분"), g("are used", "쓰이다"),
                    g("different species of animals", "여러 종의 동물들"), g("have not arisen", "생겨나지 않았다"),
                    g("afresh", "새로"), g("in each separate species", "각 개별 종에서"), g("arisen", "생겨난 · arise(생겨나다)의 과거분사"),
                    g("signaling", "신호 보내기"), g("species", "(생물의) 종")],
        "slashes": ["forms of signaling", "that are used", "species of animals", "have not arisen afresh"],
        "roles": [r("Most of the various forms of signaling", "S"), r("have not arisen", "V")],
        "modifiers": ["that are used by different species of animals"],
        "steps": [
            sv("s2_sv", ["Most of the various forms of signaling", "are used", "different species of animals", "have not arisen"],
               {"Most of the various forms of signaling": "S", "have not arisen": "V"},
               {"are used": "그건 that 뒤 덩어리 안의 동사예요. 앞의 forms를 꾸며 줘요.",
                "different species of animals": "그건 by 뒤, 누가 쓰는지 알려 주는 말이에요."},
               "주어는 Most of the various forms of signaling, 동사는 have not arisen이에요.",
               ask="이번에도 긴 문장이에요. 주어(S)와 동사(V)를 찾아볼까요?"),
            show("s2_mod", "초록 부분은 앞의 forms of signaling을 꾸며요. 아래 표처럼 읽어요.",
                 highlight=["Most of the various forms of signaling", "have not arisen"],
                 highlight_alt=["that are used by different species of animals"],
                 panel=rows(("S", "Most of the various forms of signaling", "다양한 신호 형식의 대부분은", "hl"),
                            ("↖ 꾸밈", "that are used by different species of animals", "여러 종의 동물들이 쓰는", "hl2"),
                            ("V", "have not arisen afresh", "새로 생겨나지 않았다", "hl"))),
            choice("s2_afresh",
                   "'have not arisen afresh in each separate species'는 무슨 말일까요?",
                   [("o0", "종마다 새로 생겨난 게 아니다", True), ("o1", "종마다 따로 새로 생겨났다", False),
                    ("o2", "어떤 종에서도 쓰이지 않는다", False)],
                   "arise는 '생겨나다', afresh는 '새로'예요. 앞에 not이 있어요.",
                   why="arise는 '생겨나다', afresh는 '새로'예요. not이 있으니 종마다 새로 생겨난 게 아니라는 말이에요.",
                   highlight=["have not arisen afresh"],
                   tips=[tip("arise", "'생겨나다, 일어나다'예요. arise – arose – arisen.", "arisen")]),
            flow("s2_flow", "①", "어떻게 생겨났는지 궁금하다", "종마다 새로 생겨난 게 아니다", True,
                 "어떻게 생겨났는지 궁금하다고 한 뒤, 그 답을 꺼내기 시작해요. 그대로 이어져요."),
        ],
    },
    {
        "id": 4, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("As one species evolves into another", "한 종이 다른 종으로 진화하면서"), g("evolves into", "~로 진화하다"),
                    g("particular forms of signaling", "특정한 신호 형식"), g("may be passed on", "전해질 수도 있다"),
                    g("passed on", "전해진"), g("owing to", "~ 때문에"), g("the effects", "영향"),
                    g("both genes and learning or experience", "유전자와 학습 또는 경험 둘 다"), g("genes", "유전자")],
        "slashes": ["into another,", "forms of signaling", "may be passed on,", "owing to the effects"],
        "roles": [r("particular forms of signaling", "S"), r("may be passed on", "V"), r("one species", "S"), r("evolves", "V")],
        "steps": [
            show("s3_pass",
                 "As는 '~하면서'예요. 한 종이 다른 종으로 진화하면서, 신호 형식이 다음 종으로 전해질 수 있대요.",
                 highlight=["may be passed on"],
                 tips=[tip("owing to", "'~ 때문에'예요. owing to the effects = 영향 때문에.", "owing to")]),
            flow("s3_flow", "②", "종마다 새로 생겨난 게 아니다", "진화하면서 신호가 전해진다", True,
                 "새로 생긴 게 아니라면 어디서 왔는지, 앞 종에서 전해진다고 풀어 줘요. 그대로 이어져요."),
        ],
    },
    {
        "id": 5, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Some signals", "몇몇 신호"), g("have significance", "중요성을 지니다"), g("significance", "중요성"),
                    g("across many species", "여러 종에 걸쳐"), g("and so", "그래서"),
                    g("remain much the same", "거의 똑같이 남아 있다"), g("remain", "남아 있다"), g("much the same", "거의 똑같은"),
                    g("over generations", "세대를 넘어"), g("in a number of species", "많은 종에서")],
        "slashes": ["have significance", "many species,", "remain much the same", "over generations"],
        "roles": [r("Some signals", "S"), r("have", "V"), r("significance", "O"), r("remain", "V")],
        "steps": [
            choice("s4_same",
                   "Some signals(몇몇 신호)는 세대를 넘어 어떻게 된대요?",
                   [("o0", "점점 더 정교해진다", False), ("o1", "거의 똑같이 남는다", True), ("o2", "사라진다", False)],
                   "remain은 '남아 있다', much the same은 '거의 똑같은'이에요.",
                   why="remain much the same은 '거의 똑같이 남아 있다'예요. 몇몇 신호는 대대로 거의 그대로래요.",
                   highlight=["remain much the same"]),
            flow("s4_flow", "③", "진화하면서 신호가 전해진다", "몇몇 신호는 거의 똑같이 남는다", True,
                 "전해진 신호 중 몇몇은 그대로 남는다고 이어 가요. 흐름이 끊기지 않아요."),
            show("s4_board", "몇몇 신호는 거의 그대로 남는대요.",
                 panel=board([("remain much the same", "거의 똑같이 남다")], R0, fresh=("remain much the same",)),
                 highlight=["Some signals", "remain much the same"]),
        ],
    },
    {
        "id": 6, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("If we examine", "우리가 살펴보면"), g("closely related species", "밀접하게 관련된 종"),
                    g("can often see", "자주 볼 수 있다"), g("slight variations", "약간의 차이"), g("variations", "차이, 변형"),
                    g("in a particular display", "한 특정한 표현에서"), g("can piece together", "종합할 수 있다, 짜 맞출 수 있다"),
                    g("piece together", "(조각을) 종합하다, 짜 맞추다"),
                    g("an explanation", "설명"), g("the spread of the display", "그 표현의 퍼짐"), g("across species", "여러 종에 걸쳐")],
        "slashes": ["closely related species,", "slight variations", "a particular display", "piece together", "an explanation",
                    "of the display"],
        "roles": [r("we … we", "S"), r("can often see", "V"), r("slight variations", "O"), r("can piece together", "V"),
                  r("an explanation", "O")],
        "steps": [
            choice("s5_sort",
                   "'slight variations(약간의 차이)'는 칠판 어느 쪽일까요?",
                   [("o0", SAME, False), ("o1", CHANGE, True)],
                   "variation은 '차이, 변형'이에요. 똑같이 남았다면 차이가 없겠죠.",
                   why="variation은 '차이, 변형'이에요. 차이가 보인다는 건 신호가 변했다는 뜻이라 오른쪽이에요.",
                   panel=board([("remain much the same", "거의 똑같이 남다")], R0, sort=["slight variations"]),
                   highlight=["slight variations"]),
            show("s5_break",
                 "그런데 바로 앞 문장은 '몇몇 신호는 거의 똑같이 남는다'였어요. 그대로 남는다더니 갑자기 차이가 보인다니 어색해요.",
                 panel=board([("remain much the same", "거의 똑같이 남다")], R0 + [("slight variations", "약간의 차이")],
                             fresh=("slight variations",)),
                 highlight=["slight variations"], point="④ 앞에서 '변한다'는 말이 먼저 나와야 slight variations가 이어진다"),
            flow("s5_flow", "④", "몇몇 신호는 거의 똑같이 남는다", "가까운 종에서 약간의 차이가 보인다", False,
                 "그대로 남는다는 말 뒤에 바로 차이 이야기가 나와요. 그 사이에 '하지만 변한다'가 빠져서 흐름이 끊겨요."),
        ],
    },
    {
        "id": 7, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("Some very elaborate displays", "아주 정교한 몇몇 표현"), g("may have begun", "시작했을지도 모른다"),
                    g("as simpler versions", "더 단순한 형태로"), g("simpler versions", "더 단순한 형태"),
                    g("the same behavioral pattern", "같은 행동 양식"), g("became more elaborate", "더 정교해졌다"),
                    g("as they developed", "그것들이 발전하면서"), g("were passed on", "전해졌다"),
                    g("from generation to generation", "대대로, 세대에서 세대로"), g("behavioral", "행동의"), g("versions", "형태, 판")],
        "slashes": ["elaborate displays", "may have begun", "simpler versions", "behavioral pattern", "more elaborate", "they developed",
                    "were passed on"],
        "roles": [r("Some very elaborate displays", "S"), r("may have begun", "V")],
        "modifiers": ["that became more elaborate as they developed and were passed on from generation to generation"],
        "steps": [
            show("s6_simple",
                 "아주 정교한 표현도 처음엔 더 단순한 모습이었다가, 대대로 전해지며 정교해졌을지도 모른대요.",
                 highlight=["simpler versions", "became more elaborate"],
                 tips=[tip("may have p.p.", "'~했을지도 모른다'예요. 지난 일을 짐작할 때 써요. may have begun = 시작했을지도 모른다.", "may have begun")]),
            flow("s6_flow", "⑤", "가까운 종에서 약간의 차이가 보인다", "정교한 표현도 단순하게 시작했을 수 있다", True,
                 "차이가 쌓여 정교해진 예를 들어 줘요. 그대로 이어져요."),
            show("s6_go", "①~⑤ 중 흐름이 끊긴 곳은 하나였어요. 주어진 문장의 But과 go through changes를 떠올리며 골라 봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 초급 기본 — 문장마다 「주어·동사 + 뜻」 또는 「해석 맞추기」 하나 (2026-10-15 선생님)
add_basic(sentences, 2, [m("Many of the ritualized displays", "의례화된 표현 중 많은 것이"), " ", m("look so bizarre", "너무 기이해 보여서"), " ",
                         m("how they came about", "어떻게 생겨났는지"), " ", m("we wonder", "우리는 궁금해한다"), "."],
          match_display="Many of the ritualized displays look so bizarre that we wonder how they came about.",
          sv_new=sv_step("s2_basic_sv", ["Many of the ritualized displays", "performed by animals", "look", "so bizarre"],
                         {"Many of the ritualized displays": "S", "look": "V", "so bizarre": "C"},
                         {"performed by animals": "그건 앞의 displays를 꾸며 주는 덩어리예요(동물이 행하는)."},
                         "주어는 Many of the ritualized displays, 동사는 look, 보어는 so bizarre예요."),
          meaning_ids=["s1_display", "s1_show"])
add_basic(sentences, 3, [m("Most of the various forms of signaling", "다양한 신호 형식의 대부분은"), " ", m("in each separate species", "각 개별 종에서"), " ",
                         m("have not arisen afresh", "새로 생겨나지 않았다"), "."],
          match_display="Most of the various forms of signaling have not arisen afresh in each separate species.",
          sv_id="s2_sv", meaning_ids=["s2_afresh"])
add_basic(sentences, 4, [m("As one species evolves into another", "한 종이 다른 종으로 진화하면서"), ", ",
                         m("particular forms of signaling", "특정한 신호 형식이"), " ", m("may be passed on", "전해질 수도 있다"), "."],
          match_display="As one species evolves into another, particular forms of signaling may be passed on.",
          sv_new=sv_step("s4_basic_sv", ["one species", "evolves", "particular forms of signaling", "may be passed on"],
                         {"particular forms of signaling": "S", "may be passed on": "V"},
                         {"one species": "그건 As(~하면서) 덩어리 안의 주어예요.", "evolves": "그건 As(~하면서) 덩어리 안의 동사예요."},
                         "주어는 particular forms of signaling, 동사는 may be passed on이에요."),
          meaning_ids=["s3_pass"])
add_basic(sentences, 5, [m("Some signals", "몇몇 신호는"), " ", m("across many species", "여러 종에 걸쳐"), " ", m("have significance", "중요성을 지니고"),
                         ", 그래서 ", m("remain much the same", "거의 똑같이 남아 있다"), "."],
          match_display="Some signals have significance across many species, and so remain much the same.",
          sv_new=sv_step("s5_basic_sv", ["Some signals", "have", "significance", "remain"],
                         {"Some signals": "S", "have": "V", "significance": "O", "remain": "V"}, {},
                         "주어는 Some signals, 동사는 have와 remain 두 개예요. have의 목적어는 significance예요."),
          meaning_ids=["s4_same"])
add_basic(sentences, 6, [m("If we examine closely related species", "밀접하게 관련된 종을 살펴보면"), ", ", m("slight variations", "약간의 차이"), "를 ",
                         m("can often see", "자주 볼 수 있다"), "."],
          match_display="If we examine closely related species, we can often see slight variations.")
add_basic(sentences, 7, [m("Some very elaborate displays", "아주 정교한 몇몇 표현은"), " ", m("as simpler versions", "더 단순한 형태로"), " ",
                         m("may have begun", "시작했을지도 모른다"), "."],
          match_display="Some very elaborate displays may have begun as simpler versions.",
          sv_new=sv_step("s7_basic_sv", ["Some very elaborate displays", "may have begun", "simpler versions", "became"],
                         {"Some very elaborate displays": "S", "may have begun": "V"},
                         {"simpler versions": "그건 as(~로서) 뒤 덩어리예요.", "became": "그건 that 뒤 덩어리 안의 동사예요. 앞의 pattern을 꾸며 줘요."},
                         "주어는 Some very elaborate displays, 동사는 may have begun이에요."),
          meaning_ids=["s6_simple"])

SENSES = {
    1: [sense("but", "But many signals", "하지만", "접속사 But — 앞 내용을 뒤집는다"),
        sense("as", "as they are passed", "~할 때", "접속사 as + 주어·동사 (때)"),
        sense("to", "from generation to generation", "~에게로", "from A to B = A에서 B로"),
        sense("that", "changes that make", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    2: [sense("so", "so bizarre", "너무", "so + 형용사 + that … = 너무 ~해서 …하다"),
        sense("to", "to us", "~에게", "전치사 to + 사람"),
        sense("that", "so bizarre to us that", "(그래서) ~하다", "so ~ that … 의 that — 결과")],
    3: [sense("that", "forms of signaling that are used", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    4: [sense("as", "As one species evolves", "~하면서", "접속사 as + 주어·동사 (동시·변화)"),
        sense("to", "owing to", "(owing to의 일부)", "owing to + 명사 = ~ 때문에")],
    5: [sense("so", "and so remain", "그래서", "and so = 그래서 (결과)")],
    6: [sense("if", "If we examine", "만약 ~하면", "접속사 if + 주어·동사 (조건)"),
        sense("for", "an explanation for", "~에 대한", "explanation for + 명사 = ~에 대한 설명")],
    7: [sense("as", "as simpler versions", "~로서", "전치사 as + 명사 (자격)"),
        sense("that", "pattern that became", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("as", "as they developed", "~하면서", "접속사 as + 주어·동사 (동시·변화)"),
        sense("to", "from generation to generation", "~에게로", "from A to B = A에서 B로")],
}

WORDS = {"many": "많은", "signals": "신호", "passed": "전해진", "generation": "세대", "whatever": "어떤 ~이든", "means": "방법, 수단",
         "changes": "변화", "make": "만들다", "elaborate": "정교한, 공들인", "simply": "그냥, 단순히", "different": "다른",
         "ritualized": "의례화된", "displays": "표현, 보여 주는 행동", "performed": "행해진", "animals": "동물들", "look": "~해 보이다",
         "bizarre": "기이한", "wonder": "궁금해하다", "came": "왔다 · come about = 생겨나다", "various": "다양한", "forms": "형식, 형태",
         "signaling": "신호 보내기", "used": "쓰이는", "species": "(생물의) 종", "arisen": "생겨난", "afresh": "새로", "separate": "별개의",
         "evolves": "진화하다", "another": "또 다른 것", "particular": "특정한", "owing": "~ 때문에 · owing to", "effects": "영향, 효과",
         "genes": "유전자", "learning": "학습", "experience": "경험", "significance": "중요성", "remain": "남아 있다",
         "generations": "세대들", "number": "수 · a number of = 많은", "examine": "살펴보다, 조사하다", "closely": "밀접하게",
         "related": "관련된", "often": "자주", "slight": "약간의", "variations": "차이, 변형", "display": "표현, 보여 주는 행동",
         "piece": "조각 · piece together = 종합하다", "together": "함께", "explanation": "설명", "spread": "퍼짐, 확산",
         "begun": "시작된", "simpler": "더 단순한", "versions": "형태, 판", "behavioral": "행동의", "pattern": "양식, 패턴",
         "became": "~이 되었다", "developed": "발전했다", "both": "둘 다", "most": "대부분", "different species": "여러 종",
         "very": "아주", "more": "더", "same": "같은", "much": "훨씬, 거의 · much the same = 거의 똑같은", "signal": "신호",
         "some": "몇몇", "see": "보다", "can": "~할 수 있다", "go": "가다", "through": "~을 통해 · go through = 겪다",
         "related species": "관련된 종", "versions.": "형태"}

STORIES = [
    (3, [sc("주어진 문장", "🔄", "But many signals · go through changes", "하지만 많은 신호는 대대로 전해지며 변화를 겪어요"),
         sc("문장 1~2", "🦚", "displays · not arisen afresh", "동물의 기이한 표현은 종마다 새로 생긴 게 아니래요")]),
    (5, [sc("②~③", "🧬", "passed on · remain much the same", "진화하며 신호가 전해지고, 몇몇은 거의 그대로 남아요")]),
    (7, [sc("④~⑤", "🔍", "slight variations · more elaborate", "가까운 종에서 약간의 차이가 보이고, 단순한 표현이 정교해졌을 수 있어요")]),
]

OPTIONS = [
    ("1", "Most of the various forms … 앞", "어떻게 생겨났는지 궁금하다 뒤", False),
    ("2", "As one species evolves … 앞", "종마다 새로 생긴 게 아니다 뒤", False),
    ("3", "Some signals have significance … 앞", "진화하며 신호가 전해진다 뒤", False),
    ("4", "If we examine closely related species … 앞", "몇몇 신호는 거의 그대로 남는다 뒤", True),
    ("5", "Some very elaborate displays … 앞", "가까운 종에서 약간의 차이가 보인다 뒤", False),
]
exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳을 고르시오.",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"], "numbers_only": True,
    "passage_keywords": ["But many signals", "go through changes", "more elaborate", "have not arisen afresh", "passed on",
                         "Some signals", "remain much the same", "slight variations", "simpler versions"],
    "sentence": 1, "analysis_first": True, "wrong_rate": 40.0, "wrong_rank": 11,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "주어진 문장의 But과 go through changes를 떠올리며 들어갈 곳을 골라 봐요.",
        "정답이에요! 몇몇 신호는 거의 그대로 남는다 → 하지만 많은 신호는 변화를 겪는다(주어진 문장) → 그래서 가까운 종을 보면 약간의 차이가 보인다, 순서예요.",
        "정답은 ④예요. '거의 그대로 남는다'를 But으로 뒤집고, 그 변화 덕분에 뒤에서 '약간의 차이'가 보여요.",
        {"1": "① 앞은 동물 표현이 어떻게 생겼는지 궁금하다는 말이에요. But이 뒤집을 '변하지 않는다'가 아직 안 나왔어요.",
         "2": "② 앞은 신호가 종마다 새로 생긴 게 아니라는 말이에요. 아직 '그대로 남는다'가 안 나왔어요.",
         "3": "③ 앞은 신호가 진화하며 전해진다는 말이에요. 그 뒤 '몇몇은 그대로 남는다'로 그대로 이어져서 끊긴 곳이 아니에요.",
         "5": "⑤ 앞에서 이미 '약간의 차이'가 나왔어요. 변화 이야기는 그 차이보다 먼저, ④에 와야 해요."},
        {"5": review(15,
                     "⑤ 뒤에도 more elaborate가 나와서 끌리기 쉬워요. 그런데 ⑤ 앞에서 이미 '약간의 차이가 보인다'가 나왔어요. '그대로 남는다' 바로 뒤에 차이가 나오는 ④가 먼저 끊겨요.",
                     "그래서 ⑤가 아니에요. 어디서 헷갈렸어요?",
                     [("elaborate가 같아서 골랐어요", ["word_match"],
                       "알려 줘서 고마워요. 같은 낱말만 보고 고르지 말고, 앞뒤 흐름이 어디서 끊기는지 확인해야 해요. 앞으로 이 점을 강조해서 알려 줄게요."),
                      ("slight variations가 변화인 줄 몰랐어요", ["variation_meaning"],
                       "알려 줘서 고마워요. variation은 '차이, 변형'이라 '변한다' 쪽 말이에요. 앞으로 비슷한 말이 나오면 같이 짚어 줄게요."),
                      ("둘 다요", ["word_match", "variation_meaning"], "알려 줘서 고마워요. 앞으로 낱말 뜻과 흐름을 같이 짚어 볼게요.")],
                     panel=rows(("③ 뒤", "Some signals … remain much the same", "몇몇 신호는 거의 그대로", "hl"),
                                ("주어진 문장", "But many signals … go through changes", "하지만 많은 신호는 변한다", "hl2"),
                                ("④ 뒤", "slight variations", "그래서 약간의 차이가 보인다", "hl")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 38번 (주어진 문장 넣기, 2점)",
    topic="문장 넣기 푸는 법: 주어진 문장의 단서 → 앞뒤 예측 → ①~⑤ 흐름이 끊기는 곳",
    method={"type": "sentence_insertion", "labels": ["주어진 문장 단서 찾기", "앞에 올 내용 예측하기", "흐름 끊기는 곳 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-animal-signals.svg", ("Signals", "신호"), "→", ("Generations", "세대"),
                                       "동물의 신호는 대대로 그대로 전해질까?", "2022년 3월 38번 도입 칠판"),
                      "alt": "칠판: Signals(신호) → Generations(세대)", "kind": "drawing"},
            "method": METHOD_IMAGES["insert"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "동물은 몸짓으로 신호를 보내요. 이번 글은 그 신호가 대대로 어떻게 전해지는지 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "문장 넣기는 주어진 문장부터 꼼꼼히 봐야 해요. 그 안에 앞 문장과 이어지는 단서가 숨어 있거든요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "단서를 찾고, 앞에 올 내용을 예측한 뒤, 흐름이 끊기는 곳을 찾을 거예요. 칠판 순서대로 해 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("go through", "겪다"), g("elaborate", "정교한, 공들인"), g("generation", "세대"),
                           g("ritualized", "의례화된"), g("display", "(동물의) 표현, 과시 행동"), g("arise", "생겨나다"),
                           g("afresh", "새로"), g("separate", "별개의"), g("evolve", "진화하다"), g("owing to", "~ 때문에"),
                           g("gene", "유전자"), g("significance", "중요성"), g("remain", "남아 있다"), g("examine", "조사하다"),
                           g("variation", "차이, 변형"), g("piece together", "종합하다")],
               "options": []},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="문장 넣기 푸는 법",
       chunks={"many signals": "많은 신호", "they": "그것들", "are passed": "전해지다", "go through": "겪다", "changes": "변화",
               "make": "만들다", "Many of the ritualized displays": "의례화된 표현 중 많은 것", "performed by animals": "동물이 행하는",
               "look": "~해 보이다", "so bizarre": "너무 기이한", "look so bizarre": "너무 기이해 보이다", "we wonder": "우리는 궁금해한다",
               "how they came about": "그것들이 어떻게 생겨났는지",
               "Most of the various forms of signaling": "다양한 신호 형식의 대부분", "are used": "쓰이다",
               "different species of animals": "여러 종의 동물들", "have not arisen": "생겨나지 않았다",
               "have not arisen afresh": "새로 생겨나지 않았다", "in each separate species": "각 개별 종에서",
               "As one species evolves into another": "한 종이 다른 종으로 진화하면서", "one species": "한 종", "evolves": "진화하다",
               "particular forms of signaling": "특정한 신호 형식", "may be passed on": "전해질 수도 있다",
               "Some signals": "몇몇 신호", "have": "가지다", "significance": "중요성", "remain": "남아 있다",
               "have significance": "중요성을 지니다", "across many species": "여러 종에 걸쳐", "remain much the same": "거의 똑같이 남아 있다",
               "If we examine closely related species": "밀접하게 관련된 종을 살펴보면", "slight variations": "약간의 차이",
               "can often see": "자주 볼 수 있다", "Some very elaborate displays": "아주 정교한 몇몇 표현", "may have begun": "시작했을지도 모른다",
               "simpler versions": "더 단순한 형태", "as simpler versions": "더 단순한 형태로", "became": "~이 되었다"})
