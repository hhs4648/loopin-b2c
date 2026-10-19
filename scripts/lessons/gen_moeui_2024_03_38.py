"""2024년 3월 고3 38번 레슨 + 대사를 만든다 (주어진 문장 넣기, 2점). 오답률 57.2% · Top 6.

    python3 scripts/lessons/gen_moeui_2024_03_38.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: 2026년 3월 39·38번(문장 넣기) — 주어진 문장 단서 → 앞뒤 예측 → ①~⑤ 흐름 확인. 정답 ④.
많이 고른 오답 ③ 28.0% — ③에 넣으면 뒤 'This type of classification'이 주어진 문장(실제 행동 기준 요금)을 가리키게 돼 말이 안 된다.
열쇠: But in the future(↔ For centuries 과거 방식) · as opposed to generalized stereotypes(↔ 고위험 집단 분류) /
④ 뒤 'individual drivers … regardless of men or women, young or old'는 새 방식의 결과 — 앞에 새 방식이 먼저 나와야 한다.
해설지 해석과 대조함. err on the safe side는 시험지 아래 *로 풀어 준 말(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2024-03-38-pay-as-you-drive"

GIVEN = ("But in the future, real-time data collection will enable insurance companies to charge pay-as-you-drive rates "
         "depending on people’s actual behavior on the road, as opposed to generalized stereotypes of certain “at-risk” groups.")
S = [
    "Insurance companies are expected to err on the safe side.",
    "They calculate risks thoroughly, carefully picking and choosing the customers they insure.",
    "They are boring because their role in the economy is to shield everyone and everything from disastrous loss.",
    "(①) Unlike manufacturing, nothing truly revolutionary ever happens in the insurance industry.",
    "(②) For centuries, insurers have charged higher premiums to people in “high-risk categories” such as smokers, male drivers "
    "under the age of thirty, and extreme-sports enthusiasts.",
    "(③) This type of classification frequently results in biases and outright discrimination against disadvantaged groups.",
    "(④) Bad or high-risk individual drivers will end up paying more for insurance, regardless of whether they are men or women, young or old.",
    "(⑤) The Big Brother connotations are threatening, but many people might agree to the real-time monitoring of their driving "
    "behavior if it means lower rates.",
]
KO = [
    "보험 회사들은 너무 만전을 기할 것으로 예상된다.",
    "그들은 위험성을 매우 철저하게 계산하고, 그들이 보험을 맡을 고객을 신중하게 고르고 선택한다.",
    "그들은 따분한데, 경제에서 그들의 역할이 모든 사람과 모든 것을 막심한 손실로부터 보호하는 것이기 때문이다.",
    "제조업과는 달리, 보험 산업에서는 진정으로 획기적인 일이 절대 일어나지 않는다.",
    "수 세기 동안 보험사들은 흡연자, 30세 미만의 남성 운전자, 그리고 익스트림 스포츠에 열성적인 사람과 같은 '고위험군'에 속한 사람들에게 더 높은 보험료를 부과해 왔다.",
    "이런 종류의 분류는 불이익을 받는 집단에 대한 편견과 노골적인 차별을 자주 초래한다.",
    "악질의 혹은 고위험 개인 운전자들은 그들이 남자든 여자든, 어리든지 나이가 많든지에 관계없이 결국 보험료를 더 내게 될 것이다.",
    "Big Brother(빅브라더)의 함축된 의미는 위협적이지만, 그것이 더 낮은 요금을 의미한다면 많은 사람이 그들의 운전 행동을 실시간 감시하는 것에 동의할 수도 있다.",
]

PAST = "왼쪽 · 예전 방식 (집단)"
FUT = "오른쪽 · 미래 방식 (개인)"


def board(left, right, fresh=(), sort=None):
    return groups("보험료 매기는 방식", "예전 방식 (집단)", left, "미래 방식 (개인)", right, fresh=fresh, between="→",
                  sort={"words": sort, "left": PAST, "right": FUT} if sort else None)


def flow(id, n, before, after, ok, why):
    return choice(id, f"{n} 자리예요. '{before}' → '{after}', 자연스럽게 이어지나요?",
                  [("o0", "네, 이어져요", ok), ("o1", "아니요, 끊겨요", not ok)], why, why=why)


R0 = [("real-time data", "실시간 데이터"), ("actual behavior", "실제 행동")]

sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN, "teaching_value": "high",
        "model_translation": "그러나 미래에는 실시간 데이터 수집이 보험사로 하여금 특정 '위험군' 집단의 일반화된 고정 관념과는 대조적으로 도로에서 사람들의 실제 행동에 따라 '운전하는 대로 내는' 요금을 부과할 수 있게 할 것이다.",
        "glosses": [g("But in the future", "하지만 미래에는"), g("real-time data collection", "실시간 데이터 수집"),
                    g("will enable", "~할 수 있게 할 것이다"), g("insurance companies", "보험 회사들"),
                    g("to charge pay-as-you-drive rates", "운전한 만큼 내는 요금을 매기도록"), g("depending on", "~에 따라"),
                    g("people’s actual behavior", "사람들의 실제 행동"), g("on the road", "도로에서"), g("as opposed to", "~와는 달리"),
                    g("generalized stereotypes", "일반화된 고정관념"), g("certain “at-risk” groups", "특정 '위험' 집단")],
        "slashes": ["in the future,", "insurance companies", "pay-as-you-drive rates", "on the road,"],
        "steps": [
            sv("g_sv", ["But in the future", "real-time data collection", "will enable", "insurance companies",
                        "to charge pay-as-you-drive rates", "people’s actual behavior"],
               {"real-time data collection": "S", "will enable": "V", "insurance companies": "O", "to charge pay-as-you-drive rates": "C"},
               {"But in the future": "그건 '하지만 미래에는', 때를 알려 주는 말이에요.",
                "people’s actual behavior": "그건 depending on(~에 따라) 뒤 덩어리예요."},
               "주어는 real-time data collection, 동사는 will enable, 목적어는 insurance companies, 보어는 to charge pay-as-you-drive rates예요.",
               ask="긴 문장이에요. 주어(S), 동사(V), 목적어(O), 보어(C)를 모두 찾아볼까요?"),
            show("g_enable", "enable + 회사 + to ~는 '회사가 ~할 수 있게 해 준다'로 읽어요. 실시간 데이터 덕분에 보험사가 운전한 만큼 요금을 매길 수 있대요.",
                 levels=["중", "초"], highlight=["will enable", "to charge pay-as-you-drive rates"],
                 tips=[tip("동사 + 사람 + to ~", "enable·allow·help + 사람 + to ~ = '사람이 ~하게 (해) 주다'예요.")]),
            choice("g_clue",
                   "주어진 문장은 'But in the future(하지만 미래에는)'로 시작해요. 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "미래의 또 다른 계획", False), ("o1", "예전부터 지금까지의 방식", True), ("o2", "보험 회사의 장점", False)],
                   "But은 앞과 뒤집는 말이에요. in the future(미래)와 반대되는 때를 떠올려 봐요.",
                   why="But in the future는 앞의 내용과 맞서는 '미래' 이야기예요. 그러니 앞에는 예전부터 해 온 방식이 있어야 해요.",
                   highlight=["But in the future"],
                   tips=[tip("앞을 가리키는 말·연결어", "But, However, This, Such처럼 앞과 이어지는 말이 주어진 문장에 있으면, 그 말이 받을 내용이 바로 앞에 있어야 해요.")]),
            choice("g_opposed",
                   "'as opposed to generalized stereotypes of certain at-risk groups'는 무슨 뜻일까요?",
                   [("o0", "특정 위험 집단에 대한 고정관념에 따라서", False), ("o1", "위험 집단을 더 보호하기 위해서", False),
                    ("o2", "특정 위험 집단에 대한 고정관념과는 달리", True)],
                   "as opposed to는 '~와는 달리, ~가 아니라'예요.",
                   why="as opposed to는 '~와는 달리'예요. 집단에 대한 고정관념이 아니라, 사람마다 실제 행동에 따라 요금을 매긴대요.",
                   highlight=["as opposed to", "generalized stereotypes"],
                   tips=[tip("as opposed to", "'~와는 달리, ~가 아니라'예요. A as opposed to B = B가 아니라 A.", "as opposed to")]),
            choice("g_sort",
                   "보험료 매기는 방식을 두 쪽으로 나눠 봐요. 'generalized stereotypes(일반화된 고정관념)'은 어느 쪽일까요?",
                   [("o0", PAST, True), ("o1", FUT, False)],
                   "as opposed to(~와는 달리) 뒤에 있어요. 미래 방식과 다른 쪽이에요.",
                   panel=board([], R0, sort=["generalized stereotypes"]), highlight=["generalized stereotypes"]),
            choice("g_before",
                   "그럼 주어진 문장 바로 앞에는 무엇이 와야 할까요?",
                   [("o0", "집단으로 묶어 보험료를 매기는 예전 방식과 그 문제", True), ("o1", "실시간 감시에 동의하는 사람들", False),
                    ("o2", "보험 회사가 따분한 이유", False)],
                   "But in the future와 as opposed to stereotypes를 같이 봐요. 그와 맞서는 예전 방식이 앞에 있어야 해요.",
                   why="But in the future(미래에는)와 as opposed to stereotypes(고정관념과 달리)가 맞서는 건, 집단으로 묶어 매기던 예전 방식이에요.",
                   panel=board(["generalized stereotypes"], R0)),
            choice("g_after",
                   "주어진 문장 바로 뒤에는 무엇이 오면 자연스러울까요?",
                   [("o0", "제조업 이야기", False), ("o1", "실제 운전 행동에 따라 요금이 정해진 결과", True), ("o2", "흡연자 예시", False)],
                   "새 방식(실제 행동에 따른 요금)이 나왔으니, 다음엔 그래서 어떻게 되는지가 이어지기 쉬워요.",
                   why="실제 행동에 따라 요금을 매기는 새 방식이 나왔으니, 그 결과(누가 더 내게 되는지)가 이어지기 쉬워요."),
        ],
    },
    {
        "id": 2, "text": S[0], "model_translation": KO[0], "teaching_value": "low",
        "glosses": [g("Insurance companies", "보험 회사들"), g("are expected to", "~할 것으로 예상된다"), g("err on the safe side", "너무 만전을 기하다")],
        "steps": [
            show("s1_safe", "보험 회사는 늘 안전한 쪽으로, 너무 조심한대요.", highlight=["err on the safe side"], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("They", "그들(보험 회사)"), g("calculate risks", "위험을 계산하다"), g("thoroughly", "철저하게"),
                    g("carefully picking and choosing", "신중하게 고르고 골라"), g("the customers", "고객들"), g("they insure", "그들이 보험을 맡는")],
        "steps": [
            show("s2_pick", "위험을 꼼꼼히 계산하고, 보험을 들어 줄 고객을 신중하게 고른대요.", highlight=["calculate risks"], button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[2], "model_translation": KO[2], "teaching_value": "medium",
        "glosses": [g("They", "그들(보험 회사)"), g("are boring", "따분하다"), g("because", "~ 때문에"), g("their role in the economy", "경제에서 그들의 역할"),
                    g("to shield", "보호하는 것"), g("everyone and everything", "모든 사람과 모든 것"), g("from disastrous loss", "막심한 손실로부터")],
        "steps": [
            choice("s3_boring",
                   "보험 회사가 따분한(boring) 이유는 무엇이래요?",
                   [("o0", "돈을 많이 못 벌어서", False), ("o1", "모두를 큰 손실에서 지키는 게 역할이라서", True), ("o2", "직원이 적어서", False)],
                   "because 뒤 'to shield everyone and everything from disastrous loss'를 봐요. shield는 '보호하다'예요.",
                   why="'their role … is to shield everyone and everything from disastrous loss', 모두를 큰 손실에서 지키는 게 역할이라 늘 조심스럽고 따분하대요.",
                   highlight=["are boring", "to shield"]),
        ],
    },
    {
        "id": 5, "text": S[3], "model_translation": KO[3], "teaching_value": "medium",
        "glosses": [g("Unlike manufacturing", "제조업과 달리"), g("nothing truly revolutionary", "정말 혁신적인 것은 아무것도"),
                    g("ever happens", "일어나지 않는다(nothing과 함께)"), g("in the insurance industry", "보험 업계에서")],
        "steps": [
            show("s4_nothing", "제조업과 달리 보험 업계에서는 정말 혁신적인 일이 일어나지 않는대요. 따분하다는 말을 이어 가요.",
                 highlight=["nothing truly revolutionary"]),
            flow("s4_flow", "①", "보험 회사는 늘 조심해서 따분하다", "보험 업계엔 혁신이 없다", True,
                 "둘 다 보험 업계가 따분하다는 말이에요. 그대로 이어져요."),
        ],
    },
    {
        "id": 6, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("For centuries", "수 세기 동안"), g("insurers", "보험사들"), g("have charged", "매겨 왔다"), g("higher premiums", "더 높은 보험료"),
                    g("to people", "사람들에게"), g("in “high-risk categories”", "'고위험군'에 속한"), g("such as", "~ 같은"),
                    g("smokers", "흡연자"), g("male drivers under the age of thirty", "30세 미만 남성 운전자"),
                    g("extreme-sports enthusiasts", "익스트림 스포츠 애호가")],
        "slashes": ["For centuries,", "higher premiums", "“high-risk categories”", "smokers,"],
        "steps": [
            choice("s5_who",
                   "수 세기 동안 보험사는 누구에게 더 높은 보험료를 매겼대요?",
                   [("o0", "'고위험군'으로 묶인 집단의 사람들", True), ("o1", "운전을 잘하는 개인", False), ("o2", "모든 고객에게 똑같이", False)],
                   "to people in 'high-risk categories'를 봐요. 그 뒤 such as가 예시예요.",
                   why="'to people in high-risk categories', 흡연자·30세 미만 남성 운전자처럼 고위험군으로 묶인 집단에 더 매겼대요.",
                   highlight=["For centuries", "“high-risk categories”"],
                   panel=board(["generalized stereotypes", "high-risk categories"], R0, fresh=("high-risk categories",)),
                   tips=[tip("premium", "보험에서는 '보험료'예요. '고급의(프리미엄)'만 있는 게 아니에요.", "premiums")]),
            flow("s5_flow", "②", "보험 업계엔 혁신이 없다", "수 세기 동안 고위험군에 비싸게 매겼다", True,
                 "수 세기 동안 똑같이 해 왔다는 건 혁신이 없다는 말의 예예요. 그대로 이어져요."),
        ],
    },
    {
        "id": 7, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("This type of classification", "이런 종류의 분류"), g("frequently", "자주"), g("results in", "~을 낳다, ~로 이어지다"),
                    g("biases and outright discrimination", "편견과 노골적인 차별"), g("against disadvantaged groups", "불리한 집단에 대한")],
        "steps": [
            choice("s6_this",
                   "This type of classification(이런 종류의 분류)은 무엇을 가리킬까요?",
                   [("o0", "실제 운전 행동에 따른 요금", False), ("o1", "앞 문장의 고위험군 나누기", True), ("o2", "제조업의 혁신", False)],
                   "This는 바로 앞 문장을 받아요. 앞 문장에서 사람들을 무엇으로 나눴는지 봐요.",
                   why="This는 바로 앞 문장의 'high-risk categories', 사람들을 고위험군으로 나누던 방식을 가리켜요.",
                   highlight=["This type of classification"],
                   point="This type of classification = 바로 앞의 고위험군 분류 (그 결과 편견·차별)"),
            show("s6_result", "그 분류가 불리한 집단에 대한 편견과 차별을 낳는대요. 예전 방식의 문제예요.",
                 panel=board(["generalized stereotypes", "high-risk categories", "discrimination"], R0, fresh=("discrimination",)),
                 highlight=["results in", "discrimination"]),
            flow("s6_flow", "③", "고위험군에 비싸게 매겼다", "이런 분류는 차별을 낳는다", True,
                 "This type of classification이 바로 앞 '고위험군 나누기'를 받아요. 그대로 이어져요."),
        ],
    },
    {
        "id": 8, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("Bad or high-risk individual drivers", "나쁘거나 위험한 개인 운전자"), g("will end up paying more", "결국 더 내게 될 것이다"),
                    g("for insurance", "보험료로"), g("regardless of", "~와 상관없이"), g("whether they are men or women", "남자든 여자든"),
                    g("young or old", "젊든 나이 들었든")],
        "slashes": ["individual drivers", "for insurance,"],
        "steps": [
            choice("s7_basis",
                   "나쁘게 운전하는 사람은 남녀노소 상관없이 더 낸대요. 무엇을 기준으로 요금을 매기는 걸까요?",
                   [("o0", "성별과 나이", False), ("o1", "개인의 실제 운전 행동", True), ("o2", "사는 지역", False)],
                   "regardless of whether they are men or women, young or old — 성별·나이와 상관없대요. individual drivers를 봐요.",
                   why="성별·나이와 상관없이(regardless of) 개인(individual) 운전자의 운전이 나쁘면 더 내요. 실제 운전 행동이 기준이에요.",
                   highlight=["individual drivers", "regardless of"],
                   tips=[tip("end up -ing", "'결국 ~하게 되다'예요. end up paying more = 결국 더 내게 되다.", "end up")]),
            show("s7_break", "그런데 바로 앞 문장은 집단 분류가 차별을 낳는다는 말이었어요. 갑자기 '개인 운전 행동' 기준이 나와요, 그 사이에 새 방식이 먼저 나와야 해요.",
                 panel=board(["generalized stereotypes", "high-risk categories", "discrimination"], R0 + [("individual drivers", "개인 운전자")],
                             fresh=("individual drivers",)),
                 highlight=["individual drivers"], point="④ 뒤 individual drivers(개인 기준)는 새 방식의 결과 → 앞에 미래 방식이 먼저 나와야 한다"),
            flow("s7_flow", "④", "이런 분류는 차별을 낳는다", "개인 운전자가 성별·나이와 상관없이 더 낸다", False,
                 "집단 분류 이야기에서 갑자기 개인 기준 결과로 넘어가요. 새 방식(실제 행동에 따른 요금)이 빠져서 흐름이 끊겨요."),
        ],
    },
    {
        "id": 9, "text": S[7], "model_translation": KO[7], "teaching_value": "medium",
        "glosses": [g("The Big Brother connotations", "빅브라더(감시 사회) 같은 느낌"), g("are threatening", "위협적이다"), g("but", "하지만"),
                    g("many people", "많은 사람들"), g("might agree to", "~에 동의할지도 모른다"),
                    g("the real-time monitoring", "실시간 감시"), g("of their driving behavior", "자기 운전 행동의"), g("if it means lower rates", "그게 더 낮은 요금을 뜻한다면")],
        "slashes": ["are threatening,", "real-time monitoring"],
        "steps": [
            show("s8_monitor", "실시간 감시는 위협적이지만, 요금이 낮아진다면 많은 사람이 동의할 수도 있대요. 주어진 문장의 real-time과 이어지는 이야기예요.",
                 highlight=["real-time monitoring", "lower rates"],
                 tips=[tip("Big Brother", "소설 『1984』에서 사람들을 늘 감시하는 권력이에요. 여기서는 '감시당하는 느낌'으로 이해하면 돼요.", "Big Brother")]),
            flow("s8_flow", "⑤", "개인 운전자가 운전 행동에 따라 더 낸다", "감시는 위협적이지만 요금이 낮으면 동의할 수도", True,
                 "운전 행동에 따라 요금을 매기려면 감시가 필요해요. 그 감시 이야기로 그대로 이어져요."),
            show("s8_go", "①~⑤ 중 흐름이 끊긴 곳은 하나였어요. 주어진 문장의 But in the future와 as opposed to를 떠올리며 골라 봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 2, [m("Insurance companies", "보험 회사들은"), " ", m("err on the safe side", "너무 만전을 기할"), " 것으로 ", m("are expected to", "예상된다"), "."],
          sv_new=sv_step("s1_basic_sv", ["Insurance companies", "are expected to err", "the safe side"],
                         {"Insurance companies": "S", "are expected to err": "V"},
                         {"the safe side": "그건 on 뒤 덩어리예요."},
                         "주어는 Insurance companies, 동사는 are expected to err예요."),
          meaning_ids=["s1_safe"])
add_basic(sentences, 3, [m("They", "그들은"), " ", m("calculate risks", "위험을 계산한다"), " ", m("thoroughly", "철저하게"), ", ",
                         m("the customers", "고객들"), "을 ", m("carefully picking and choosing", "신중하게 고르고 골라"), "."],
          sv_new=sv_step("s2_basic_sv", ["They", "calculate", "risks", "the customers"], {"They": "S", "calculate": "V", "risks": "O"},
                         {"the customers": "그건 picking and choosing(고르고 고르는)의 대상이에요."},
                         "주어는 They, 동사는 calculate, 목적어는 risks예요."),
          meaning_ids=["s2_pick"])
add_basic(sentences, 4, [m("They", "그들은"), " ", m("are boring", "따분하다"), " ", m("because", "왜냐하면"), " ", m("their role in the economy", "경제에서 그들의 역할이"),
                         " ", m("everyone and everything", "모든 사람과 모든 것"), "을 ", m("to shield", "보호하는 것"), "이기 때문이다."],
          match_display="They are boring because their role in the economy is to shield everyone and everything.",
          sv_new=sv_step("s3_basic_sv", ["They", "are", "boring", "their role in the economy", "is"],
                         {"They": "S", "are": "V", "boring": "C"},
                         {"their role in the economy": "그건 because 뒤 덩어리 안의 주어예요.", "is": "그건 because 뒤 덩어리 안의 동사예요."},
                         "주어는 They, 동사는 are, 보어는 boring이에요."),
          meaning_after="s3_boring")
add_basic(sentences, 5, [m("Unlike manufacturing", "제조업과 달리"), ", ", m("in the insurance industry", "보험 업계에서는"), " ",
                         m("nothing truly revolutionary", "정말 혁신적인 일은 아무것도"), " ", m("ever happens", "일어나지 않는다"), "."],
          sv_new=sv_step("s4_basic_sv", ["Unlike manufacturing", "nothing truly revolutionary", "ever happens", "the insurance industry"],
                         {"nothing truly revolutionary": "S", "ever happens": "V"},
                         {"Unlike manufacturing": "그건 '제조업과 달리'예요.", "the insurance industry": "그건 in 뒤 덩어리예요."},
                         "주어는 nothing truly revolutionary, 동사는 (ever) happens예요. nothing이 주어라 '아무것도 일어나지 않는다'예요."),
          meaning_ids=["s4_nothing"])
add_basic(sentences, 6, [m("For centuries", "수 세기 동안"), ", ", m("insurers", "보험사들은"), " ", m("in “high-risk categories”", "'고위험군'에 속한"), " ",
                         m("to people", "사람들에게"), " ", m("higher premiums", "더 높은 보험료"), "를 ", m("have charged", "매겨 왔다"), "."],
          match_display="For centuries, insurers have charged higher premiums to people in “high-risk categories” such as smokers.",
          sv_new=sv_step("s5_basic_sv", ["For centuries", "insurers", "have charged", "higher premiums", "people"],
                         {"insurers": "S", "have charged": "V", "higher premiums": "O"},
                         {"For centuries": "그건 '수 세기 동안', 때를 알려 주는 말이에요.", "people": "그건 to 뒤 덩어리 안의 말이에요."},
                         "주어는 insurers, 동사는 have charged, 목적어는 higher premiums예요."),
          meaning_after="s5_who")
add_basic(sentences, 7, [m("This type of classification", "이런 종류의 분류는"), " ", m("frequently", "자주"), " ", m("biases and outright discrimination", "편견과 노골적인 차별"),
                         "을 ", m("results in", "낳는다"), "."],
          sv_new=sv_step("s6_basic_sv", ["This type of classification", "results in", "biases and outright discrimination", "disadvantaged groups"],
                         {"This type of classification": "S", "results in": "V", "biases and outright discrimination": "전목"},
                         {"disadvantaged groups": "그건 against 뒤 덩어리예요."},
                         "주어는 This type of classification, 동사는 results in, in 뒤 목적어는 biases and outright discrimination이에요."),
          meaning_ids=["s6_result"])
add_basic(sentences, 8, [m("Bad or high-risk individual drivers", "나쁘거나 위험한 개인 운전자는"), " ", m("regardless of", "~와 상관없이"), " ",
                         m("for insurance", "보험료로"), " ", m("will end up paying more", "결국 더 내게 될 것이다"), "."],
          match_display="Bad or high-risk individual drivers will end up paying more for insurance, regardless of whether they are men or women.",
          sv_new=sv_step("s7_basic_sv", ["Bad or high-risk individual drivers", "will end up paying", "they", "are"],
                         {"Bad or high-risk individual drivers": "S", "will end up paying": "V"},
                         {"they": "그건 whether 뒤 덩어리 안의 주어예요.", "are": "그건 whether 뒤 덩어리 안의 동사예요."},
                         "주어는 Bad or high-risk individual drivers, 동사는 will end up paying이에요."),
          meaning_after="s7_basis")
add_basic(sentences, 9, [m("The Big Brother connotations", "빅브라더 같은 느낌은"), " ", m("are threatening", "위협적이다"), ", ", m("but", "하지만"), " ",
                         m("many people", "많은 사람들이"), " ", m("the real-time monitoring", "실시간 감시"), "에 ", m("might agree to", "동의할지도 모른다"), "."],
          match_display="The Big Brother connotations are threatening, but many people might agree to the real-time monitoring.",
          sv_new=sv_step("s8_basic_sv", ["The Big Brother connotations", "are", "threatening", "many people", "might agree to"],
                         {"The Big Brother connotations": "S", "are": "V", "threatening": "C", "many people": "S", "might agree to": "V"}, {},
                         "but 앞은 주어 The Big Brother connotations, 동사 are, 보어 threatening이에요. but 뒤는 주어 many people, 동사 might agree to예요."),
          meaning_ids=["s8_monitor"])

SENSES = {
    1: [sense("but", "But in the future", "하지만", "접속사 but (문장 앞)"),
        sense("to", "to charge", "~하도록", "enable + 목적어 + to부정사 = 목적어가 ~할 수 있게 하다"),
        sense("as", "pay-as-you-drive", "~하는 만큼", "pay-as-you-drive = 운전하는 만큼 내는"),
        sense("as", "as opposed to", "(as opposed to의 일부)", "as opposed to = ~와는 달리"),
        sense("to", "as opposed to", "(as opposed to의 일부)", "as opposed to + 명사")],
    2: [sense("to", "are expected to err", "~할 (것으로)", "be expected + to부정사")],
    4: [sense("to", "is to shield", "~하는 것", "be + to부정사 (보어: ~하는 것)")],
    6: [sense("for", "For centuries", "~ 동안", "전치사 for + 기간"),
        sense("to", "to people", "~에게", "charge A to B = B에게 A를 매기다"),
        sense("as", "such as smokers", "~ 같은", "such as + 명사 (예시)")],
    8: [sense("for", "paying more for insurance", "~에 대해, ~로", "pay for + 명사")],
    9: [sense("but", "but many people", "하지만", "접속사 but + 주어·동사"),
        sense("to", "agree to", "~에 (동의하다)", "agree to + 명사"),
        sense("if", "if it means", "만약 ~라면", "접속사 if + 주어·동사 (조건)")],
}

WORDS = {"future": "미래", "real-time": "실시간의", "data": "데이터", "collection": "수집", "enable": "~할 수 있게 하다",
         "insurance": "보험", "companies": "회사들", "charge": "(요금을) 매기다", "pay-as-you-drive": "운전한 만큼 내는", "rates": "요금",
         "depending": "~에 따라", "people’s": "사람들의", "actual": "실제의", "behavior": "행동", "road": "도로", "opposed": "반대되는",
         "generalized": "일반화된", "stereotypes": "고정관념", "certain": "특정한", "at-risk": "위험한", "groups": "집단",
         "expected": "예상되는", "err": "잘못하다 · err on the safe side = 너무 만전을 기하다", "safe": "안전한", "side": "쪽",
         "calculate": "계산하다", "risks": "위험", "carefully": "신중하게", "picking": "고르는", "choosing": "고르는", "customers": "고객",
         "insure": "보험을 들어 주다", "boring": "따분한", "role": "역할", "economy": "경제", "shield": "보호하다", "everyone": "모든 사람",
         "everything": "모든 것", "disastrous": "막심한, 처참한", "loss": "손실", "unlike": "~와 달리", "manufacturing": "제조업",
         "nothing": "아무것도 ~ 않다", "truly": "정말", "revolutionary": "혁신적인", "ever": "언제든, 결코", "happens": "일어나다",
         "industry": "업계, 산업", "centuries": "수 세기", "insurers": "보험사들", "charged": "매겼다", "higher": "더 높은",
         "premiums": "보험료", "people": "사람들", "high-risk": "고위험의", "categories": "범주, 집단", "smokers": "흡연자",
         "male": "남성의", "drivers": "운전자들", "age": "나이", "thirty": "30", "extreme-sports": "익스트림 스포츠", "enthusiasts": "애호가들",
         "type": "종류", "classification": "분류", "frequently": "자주", "results": "~을 낳다", "biases": "편견", "outright": "노골적인",
         "discrimination": "차별", "against": "~에 대한, ~에 맞서", "disadvantaged": "불리한", "bad": "나쁜", "individual": "개인의",
         "end": "끝 · end up -ing = 결국 ~하게 되다", "paying": "내는", "regardless": "상관없이", "whether": "~든 (아니든)",
         "men": "남자들", "women": "여자들", "young": "젊은", "old": "나이 든", "big": "큰", "brother": "형제 · Big Brother = 감시 권력",
         "connotations": "함축된 의미, 느낌", "threatening": "위협적인", "agree": "동의하다", "monitoring": "감시",
         "driving": "운전", "means": "뜻하다", "lower": "더 낮은", "thoroughly": "철저하게", "customers.": "고객", "many": "많은",
         "might": "~할지도 모른다", "will": "~할 것이다", "insurers.": "보험사", "male drivers": "남성 운전자"}

STORIES = [
    (4, [sc("주어진 문장", "📡", "But in the future · actual behavior", "미래엔 실시간 데이터로 실제 운전 행동에 따라 요금을 매긴대요 — 고정관념이 아니라"),
         sc("문장 1~3", "🛡️", "err on the safe side · boring", "보험 회사는 늘 조심해서 고객을 골라 받고, 따분해요")]),
    (7, [sc("①~③", "🏷️", "high-risk categories → discrimination", "수 세기 동안 고위험군으로 묶어 비싸게 받았고, 그 분류가 차별을 낳았어요")]),
    (9, [sc("④~⑤", "🚗", "individual drivers · real-time monitoring", "나쁜 운전자는 누구든 더 내고, 감시는 싫어도 요금이 낮으면 동의할 수도 있어요")]),
]

OPTIONS = [
    ("1", "Unlike manufacturing … 앞", "보험 회사는 따분하다 뒤", False),
    ("2", "For centuries, insurers … 앞", "보험 업계엔 혁신이 없다 뒤", False),
    ("3", "This type of classification … 앞", "고위험군에 비싸게 매겼다 뒤", False),
    ("4", "Bad or high-risk individual drivers … 앞", "그런 분류가 차별을 낳는다 뒤", True),
    ("5", "The Big Brother connotations … 앞", "개인 운전자가 더 낸다 뒤", False),
]
exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳을 고르시오.",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"], "numbers_only": True,
    "passage_keywords": ["But in the future", "actual behavior", "as opposed to", "generalized stereotypes", "For centuries",
                         "high-risk categories", "This type of classification", "discrimination", "individual drivers", "regardless of"],
    "sentence": 1, "analysis_first": True, "wrong_rate": 57.2, "wrong_rank": 6, "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "주어진 문장의 But in the future와 as opposed to stereotypes를 떠올리며 들어갈 곳을 골라 봐요.",
        "정답이에요! 예전엔 고위험군으로 묶어 비싸게 받았고, 그 분류는 차별을 낳았어요 → 하지만 미래엔 실제 행동에 따라 요금을 매겨요(주어진 문장) → 그래서 나쁜 운전자는 남녀노소 상관없이 더 내요.",
        "정답은 ④예요. 집단 분류의 문제 뒤에 But in the future, 새 방식이 오고, 그 결과(개인 운전자가 더 냄)가 이어져요.",
        {"1": "① 앞은 보험 회사가 따분하다는 말뿐이에요. But in the future가 맞설 예전 방식(집단 분류)이 아직 안 나왔어요.",
         "2": "② 앞은 보험 업계엔 혁신이 없다는 말이에요. 고정관념(stereotypes)이 무엇인지 아직 안 나왔어요.",
         "3": "③에 넣으면 뒤의 This type of classification이 주어진 문장(실제 행동 기준)을 가리키게 돼요. 그런데 차별을 낳는 건 고위험군 분류예요.",
         "5": "⑤ 앞에서 이미 개인 운전자가 더 낸다는 결과가 나왔어요. 새 방식은 그 결과보다 먼저 나와야 해요."},
        {"3": review(28.0,
                     "③에 넣으면 순서가 '고위험군에 비싸게 → 미래엔 실제 행동 기준 → 이런 종류의 분류가 차별을 낳는다'가 돼요. 그러면 This type of classification이 미래 방식을 가리켜서, 공정해지려는 새 방식이 차별을 낳는다는 말이 돼요. This는 바로 앞 고위험군 분류를 받아야 해요.",
                     "그래서 ③이 아니에요. 어디서 헷갈렸어요?",
                     [("This가 가리키는 걸 확인 안 했어요", ["this_refers"],
                       "알려 줘서 고마워요. 문장 넣기에서는 넣은 자리 뒤 문장의 This, Such가 무엇을 가리키게 되는지 꼭 확인해요. 앞으로 이 점을 강조해서 알려 줄게요."),
                      ("For centuries 뒤라서 바로 대조하는 줄 알았어요", ["contrast_guess"],
                       "알려 줘서 고마워요. 대조(예전↔미래)는 맞지만, 예전 방식의 이야기(분류와 그 문제)가 끝난 뒤에 와야 해요. 앞으로 단락이 어디서 끝나는지 짚어 줄게요."),
                      ("둘 다요", ["this_refers", "contrast_guess"], "알려 줘서 고마워요. 앞으로 가리키는 말과 이야기가 끝나는 곳을 같이 짚어 볼게요.")],
                     panel=rows(("③ 뒤", "This type of classification … discrimination", "이런 분류 = 바로 앞 고위험군 분류", "hl"),
                                ("④ 뒤", "individual drivers … regardless of men or women", "개인 기준 = 새 방식의 결과", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 38번 (주어진 문장 넣기, 2점)",
    topic="문장 넣기 푸는 법: 주어진 문장의 단서 → 앞뒤 예측 → ①~⑤ 흐름이 끊기는 곳",
    method={"type": "sentence_insertion", "labels": ["주어진 문장 단서 찾기", "앞에 올 내용 예측하기", "흐름 끊기는 곳 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-insurance.svg", ("Groups", "집단"), "→", ("Individuals", "개인"),
                                       "보험료는 무엇을 기준으로 매겨야 할까?", "2024년 3월 38번 도입 칠판"),
                      "alt": "칠판: Groups(집단) → Individuals(개인)", "kind": "drawing"},
            "method": METHOD_IMAGES["insert"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "운전을 잘하는데도 젊은 남자라서 보험료를 더 낸다면 공평할까요? 이번 글은 보험료를 매기는 예전 방식과 미래 방식을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "문장 넣기는 주어진 문장부터 꼼꼼히 봐야 해요. 그 안에 앞 문장과 이어지는 단서가 숨어 있거든요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "단서를 찾고, 앞에 올 내용을 예측한 뒤, 흐름이 끊기는 곳을 찾을 거예요. 칠판 순서대로 해 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("real-time", "실시간의"), g("enable", "~할 수 있게 하다"), g("charge", "(요금을) 매기다"), g("rate", "요금"),
                           g("as opposed to", "~와는 달리"), g("stereotype", "고정관념"), g("calculate", "계산하다"), g("insure", "보험을 들어 주다"),
                           g("shield", "보호하다"), g("disastrous", "막심한"), g("revolutionary", "혁신적인"), g("premium", "보험료"),
                           g("classification", "분류"), g("bias", "편견"), g("discrimination", "차별"), g("regardless of", "~와 상관없이"),
                           g("connotation", "함축된 의미"), g("monitoring", "감시")],
               "options": []},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="문장 넣기 푸는 법",
       chunks={"Insurance companies": "보험 회사들", "are expected to err": "~할 것으로 예상된다", "the safe side": "안전한 쪽",
               "They": "그들", "calculate": "계산하다", "risks": "위험", "the customers": "고객들", "are": "~이다", "boring": "따분한",
               "their role in the economy": "경제에서 그들의 역할", "is": "~이다", "Unlike manufacturing": "제조업과 달리",
               "nothing truly revolutionary": "정말 혁신적인 것은 아무것도", "ever happens": "일어나다", "the insurance industry": "보험 업계",
               "For centuries": "수 세기 동안", "insurers": "보험사들", "have charged": "매겨 왔다", "higher premiums": "더 높은 보험료",
               "people": "사람들", "This type of classification": "이런 종류의 분류", "results in": "~을 낳다",
               "biases and outright discrimination": "편견과 노골적인 차별", "disadvantaged groups": "불리한 집단",
               "Bad or high-risk individual drivers": "나쁘거나 위험한 개인 운전자", "will end up paying": "결국 내게 될 것이다",
               "they": "그들", "The Big Brother connotations": "빅브라더 같은 느낌", "threatening": "위협적인", "many people": "많은 사람들",
               "might agree to": "동의할지도 모른다", "calculate risks": "위험을 계산하다", "thoroughly": "철저하게",
               "carefully picking and choosing": "신중하게 고르고 골라", "are boring": "따분하다", "because": "~ 때문에",
               "to shield": "보호하는 것", "everyone and everything": "모든 사람과 모든 것", "in the insurance industry": "보험 업계에서",
               "to people": "사람들에게", "in “high-risk categories”": "'고위험군'에 속한", "frequently": "자주", "regardless of": "~와 상관없이",
               "for insurance": "보험료로", "will end up paying more": "결국 더 내게 될 것이다", "are threatening": "위협적이다",
               "but": "하지만", "the real-time monitoring": "실시간 감시", "err on the safe side": "너무 만전을 기하다"})
