"""2024년 3월 고3 30번 레슨 + 대사를 만든다 (문맥상 낱말의 쓰임, 3점). 오답률 45.9% · Top 12.

    python3 scripts/lessons/gen_moeui_2024_03_30.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: 2026년 3월 30번(어휘) — 요지 → 두 그룹 → 밑줄 단어가 흐름에 맞는지. 정답이 아닌 밑줄은 「문맥에 맞아요」로 짚고,
정답 밑줄은 분석에서 흐름(+/−)만 잡게 하고 맞다/틀리다는 문제에서 고르게 한다(2026 30번과 같게).
정답 ③ invalid (→ privileged). 오답이 고르게 퍼졌다(⑤ 13.2 · ④ 12.5 · ② 11.4 · ① 8.8) — 가장 많은 ⑤만 같이 본다.
열쇠: because it is more stable(+) → 안정적이라 더 믿고 우선한다(privileged) ↔ invalid(타당하지 않은, −)는 반대.
해설지 해석과 대조함. geometric, enclosure는 시험지 아래 *로 풀어 준 단어(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2024-03-30-geometry-landmarks"

S = [
    "While it has been found that young children rely exclusively on geometric information to determine the location of an object "
    "hidden in a small enclosure, exclusive use of geometry does not occur in larger spaces.",
    "Although, in a small room, children ①failed to incorporate information about nongeometric features (i.e., a blue wall), they used both "
    "types of information in a larger room.",
    "These findings suggest that geometric and nongeometric information may be combined in a ②weighted fashion.",
    "Geometry may be ③invalid because it is more stable across time than is nongeometric information.",
    "Whether or not nongeometric landmark information is combined with geometry may depend on the ecological validity of nongeometric "
    "features; for example, larger features may be more stable and hence more ④reliable.",
    "Further, a variety of mobile animals give more weight to nearer than to farther landmarks in estimation, ⑤consistent with Weber’s "
    "law in which smaller distances would be coded more accurately than larger distances.",
]
KO = [
    "어린아이들은 작은 에워싸인 장소에 숨겨진 물체의 위치를 파악하는 데 오로지 기하학적 정보에만 의존하는 것으로 밝혀졌지만, 더 큰 공간에서는 기하학의 단독 사용이 일어나지 않는다.",
    "비록 작은 방에서 아이들은 비기하학적 특징(예를 들어, 파란색 벽)에 대한 정보를 포함하는 데 실패했지만, 그들은 더 큰 방에서 두 가지 유형의 정보를 모두 사용했다.",
    "이러한 연구 결과는 기하학적 그리고 비기하학적 정보가 가중된 방식으로 결합될 수 있음을 시사한다.",
    "기하학은 비기하학적 정보가 그러한 것보다 시간이 지나도 안정적이기 때문에 특혜가 주어질 수도 있다.",
    "비기하학적 랜드마크 정보가 기하학과 결합하는지 또는 아닌지의 여부는 비기하학적 특징의 생태학적 타당성에 달려 있을 수 있다. 예를 들어, 더 큰 특징은 더 안정적일 수 있고 그래서 더 일관된다.",
    "게다가, 다양한 이동하는 동물은 추정 시 더 멀리 있는 랜드마크보다 더 가까이 있는 것에 더 많은 가중치를 부여하는데, (이는) 적은 거리가 큰 거리보다 더 정확하게 부호화된다는 Weber의 법칙과도 모순되지 않는다.",
]
UNDER = ["①failed", "②weighted", "③invalid", "④reliable", "⑤consistent"]

GEO = "왼쪽 · 기하 정보 (공간의 모양)"
NON = "오른쪽 · 비기하 정보 (파란 벽 같은 특징)"


def board(left, right, fresh=(), sort=None):
    return groups("두 가지 정보", "geometry (기하: 공간의 모양)", left, "nongeometric (비기하: 파란 벽 같은 특징)", right,
                  fresh=fresh, between="+", sort={"words": sort, "left": GEO, "right": NON} if sort else None)


def check(*done):
    """밑줄 점검표 — 문맥에 맞는다고 확인한 밑줄만 쌓는다 (정답 밑줄은 쓰지 않는다)"""
    names = {"1": ("①", "failed to incorporate", "작은 방에선 파란 벽 정보를 못 넣었다"),
             "2": ("②", "weighted fashion", "무게를 달리해 섞는다"),
             "4": ("④", "more stable → more reliable", "더 안정적 → 더 믿을 만함"),
             "5": ("⑤", "consistent with Weber’s law", "가까울수록 정확 → 더 무게")}
    return rows(*[(names[d][0] + " 맞음", names[d][1], names[d][2], "hl") for d in done])


sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("While", "~이지만"), g("it has been found that", "~라는 것이 밝혀졌다"), g("young children", "어린아이들"),
                    g("rely exclusively on", "오로지 ~에만 의존하다"), g("geometric information", "기하 정보(공간의 모양)"),
                    g("to determine the location", "위치를 알아내려고"), g("an object hidden in a small enclosure", "작은 공간에 숨긴 물건"),
                    g("exclusive use of geometry", "기하 정보만 쓰는 것"), g("does not occur", "일어나지 않는다"), g("in larger spaces", "더 큰 공간에서는")],
        "slashes": ["it has been found", "rely exclusively", "geometric information", "the location of an object", "a small enclosure,",
                    "exclusive use of geometry"],
        "roles": [r("it", "S"), r("has been found", "V"), r("young children", "S"), r("rely", "V"), r("exclusive use of geometry", "S"),
                  r("does not occur", "V")],
        "modifiers": ["hidden in a small enclosure"],
        "steps": [
            sv("s1_sv", ["young children", "rely", "geometric information", "exclusive use of geometry", "does not occur"],
               {"exclusive use of geometry": "S", "does not occur": "V"},
               {"young children": "그건 While 덩어리 안, that 뒤의 주어예요. 콤마 뒤 메인 문장에서 찾아봐요.",
                "rely": "그건 While 덩어리 안의 동사예요.", "geometric information": "그건 on 뒤 덩어리예요."},
               "콤마 뒤 메인 문장은 주어 exclusive use of geometry, 동사 does not occur예요.",
               ask="While 덩어리가 길어요. 콤마 뒤 메인 문장의 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s1_mean",
                   "작은 공간과 큰 공간에서 아이들은 각각 어떻게 했대요?",
                   [("o0", "작은 곳·큰 곳 모두 기하 정보만 썼다", False), ("o1", "작은 곳에선 기하 정보만 쓰고, 큰 곳에선 그렇지 않았다", True),
                    ("o2", "작은 곳에선 아무 정보도 안 썼다", False)],
                   "While(~이지만) 앞은 small enclosure, 뒤는 larger spaces예요. exclusively는 '오로지'예요.",
                   why="작은 공간에선 'rely exclusively on geometric information', 기하 정보만 썼고, 큰 공간에선 'exclusive use … does not occur', 그것만 쓰지 않았대요.",
                   highlight=["exclusively", "small enclosure", "does not occur", "larger spaces"],
                   tips=[tip("While (대조)", "문장 앞 While은 '~이지만, ~인 반면'이에요. 앞뒤가 대조돼요.", "While")],
                   panel=board([("small space → only geometry", "작은 곳 → 기하만")], [], fresh=("small space → only geometry",)),
                   point="요지 시작: 작은 공간 → 기하 정보만, 큰 공간 → 기하만 쓰지는 않는다"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Although", "비록 ~이지만"), g("in a small room", "작은 방에서는"), g("children", "아이들"),
                    g("failed to incorporate", "포함하지 못했다"), g("information about nongeometric features", "비기하 특징에 대한 정보"),
                    g("nongeometric features", "비기하 특징"), g("i.e., a blue wall", "예를 들어 파란 벽"),
                    g("they used", "그들은 사용했다"), g("both types of information", "두 종류의 정보 모두"), g("in a larger room", "더 큰 방에서는")],
        "slashes": ["Although,", "in a small room,", "failed to incorporate information", "nongeometric features", "a blue wall),",
                    "both types of information"],
        "roles": [r("children", "S"), r("failed", "V"), r("they", "S"), r("used", "V"), r("both types of information", "O")],
        "steps": [
            choice("s2_sort",
                   "'a blue wall(파란 벽)' 같은 정보는 칠판 어느 쪽일까요?",
                   [("o0", GEO, False), ("o1", NON, True)],
                   "괄호 앞 'nongeometric features'를 봐요. non-은 '아님'이에요.",
                   why="'nongeometric features (i.e., a blue wall)', 파란 벽은 공간 모양이 아닌 특징이라 비기하 정보예요.",
                   panel=board([("small space → only geometry", "작은 곳 → 기하만")], [], sort=["a blue wall"]),
                   highlight=["nongeometric features"],
                   tips=[tip("i.e.", "'즉, 다시 말해'예요. 괄호 안에서 앞말의 예나 뜻을 풀어 줘요.", "i.e.")]),
            show("s2_check", "작은 방에선 기하 정보만 썼으니 파란 벽 정보는 '넣지 못했다(failed to incorporate)'가 맞아요. 큰 방에선 둘 다 썼고요. 그래서 ①은 문맥에 맞아요.",
                 highlight=["failed to incorporate", "both types of information"],
                 panel=board([("small space → only geometry", "작은 곳 → 기하만")], [("a blue wall", "파란 벽"), ("large room → both", "큰 방 → 둘 다")],
                             fresh=("a blue wall", "large room → both")),
                 tips=[tip("incorporate", "'포함하다, 넣다'예요. failed to incorporate = 포함하지 못했다.", "incorporate")], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("These findings", "이 연구 결과들은"), g("suggest", "시사하다"), g("geometric and nongeometric information", "기하·비기하 정보"),
                    g("may be combined", "결합될 수 있다"), g("in a weighted fashion", "무게를 달리한 방식으로"), g("fashion", "방식")],
        "slashes": ["These findings suggest", "nongeometric information", "may be combined"],
        "roles": [r("These findings", "S"), r("suggest", "V"), r("geometric and nongeometric information", "S"), r("may be combined", "V")],
        "steps": [
            choice("s3_weight",
                   "두 정보가 어떻게 합쳐질 수 있대요?",
                   [("o0", "늘 똑같이 반반", False), ("o1", "절대 섞이지 않는다", False), ("o2", "한쪽에 더 무게를 두는 식으로 섞인다", True)],
                   "weighted는 '무게(weight)가 실린, 가중된'이에요. fashion은 여기서 '방식'이에요.",
                   why="'combined in a weighted fashion', 무게를 달리하는 방식으로 합쳐진대요. 어느 쪽을 더 믿을지 정해서 섞는 거예요.",
                   highlight=["combined", "weighted"],
                   tips=[tip("fashion", "옷의 '패션'이 아니라 '방식'이에요. in a weighted fashion = 무게를 둔 방식으로.", "fashion")]),
            show("s3_check", "무게를 달리해 섞는다는 건, 앞으로 '어느 정보에 더 무게를 줄지'가 이어진다는 신호예요. ②weighted는 문맥에 맞아요.",
                 panel=check("1", "2"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Geometry", "기하 정보"), g("may be", "~일 수도 있다"), g("because", "~ 때문에"), g("it is more stable", "그것이 더 안정적이다"),
                    g("across time", "시간이 지나도"), g("than is nongeometric information", "비기하 정보보다")],
        "slashes": ["may be ③invalid", "more stable", "across time"],
        "roles": [r("Geometry", "S"), r("may be", "V"), r("invalid", "C"), r("it", "S"), r("is … is", "V"), r("more stable", "C"),
                  r("nongeometric information", "S")],
        "steps": [
            choice("s4_stable",
                   "because 뒤를 봐요. 기하 정보는 비기하 정보보다 어떻대요?",
                   [("o0", "시간이 지나도 더 안정적이다", True), ("o1", "더 빨리 변한다", False), ("o2", "더 크다", False)],
                   "'it is more stable across time'을 봐요. stable은 '안정적인, 잘 변하지 않는'이에요.",
                   why="'more stable across time than is nongeometric information', 기하 정보(방의 모양)는 시간이 지나도 잘 안 변해서 더 안정적이래요.",
                   highlight=["more stable"]),
            choice("s4_sign",
                   "더 안정적인(stable) 정보라면, 무게를 줄 때 어떤 대우를 받을까요?",
                   [("o0", "더 믿고 먼저 쓴다 (+)", True), ("o1", "믿을 수 없다며 버린다 (−)", False)],
                   "잘 안 변하는 정보는 길을 찾을 때 믿을 만해요. 앞 문장의 weighted(무게를 둠)도 떠올려 봐요.",
                   why="잘 안 변하는 정보일수록 믿을 만해서 더 무게를 받아요. stable은 좋은 쪽(+) 이유예요.",
                   signs=[{"text": "more stable", "sign": "+"}],
                   point="because it is more stable(+) → 기하 정보는 더 믿고 우선한다(+) — 이 흐름에 ③이 맞는지 문제에서 확인"),
            show("s4_hold", "because 뒤 이유(더 안정적, +)와 밑줄 ③이 같은 쪽인지는 마지막 문제에서 같이 확인해 봐요.",
                 signs=[{"text": "more stable", "sign": "+"}], button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Whether or not", "~인지 아닌지"), g("nongeometric landmark information", "비기하 랜드마크 정보"),
                    g("is combined with geometry", "기하 정보와 결합되다"), g("may depend on", "~에 달려 있을 수 있다"),
                    g("the ecological validity", "생태학적 타당성(실제 환경에서 믿을 만함)"), g("of nongeometric features", "비기하 특징의"),
                    g("for example", "예를 들어"), g("larger features", "더 큰 특징"), g("may be more stable", "더 안정적일 수 있다"),
                    g("hence", "그래서"), g("more reliable", "더 믿을 만한")],
        "slashes": ["landmark information", "combined with geometry", "may depend on", "nongeometric features;", "for example,", "more stable"],
        "roles": [r("Whether or not nongeometric landmark information is combined with geometry", "S"), r("may depend on", "V"),
                  r("larger features", "S"), r("may be", "V"), r("more stable", "C")],
        "steps": [
            sv("s5_sv", ["nongeometric landmark information", "is combined", "may depend on", "the ecological validity", "larger features"],
               {"may depend on": "V", "the ecological validity": "전목"},
               {"nongeometric landmark information": "그건 Whether or not 덩어리 안의 주어예요. Whether 덩어리 전체가 문장의 주어예요.",
                "is combined": "그건 Whether 덩어리 안의 동사예요.", "larger features": "그건 세미콜론(;) 뒤 문장의 주어예요."},
               "Whether or not … geometry 덩어리 전체가 주어예요. 동사는 may depend on, on 뒤 목적어는 the ecological validity예요.",
               ask="Whether or not(~인지 아닌지) 덩어리 전체가 주어예요. 그 뒤 동사(V)와 on 뒤 목적어(전목)를 찾아볼까요?"),
            choice("s5_reliable",
                   "세미콜론(;) 뒤 — 큰 특징은 더 안정적이고 그래서(hence) 더 ④reliable(믿을 만한)하대요. 이 흐름이 맞을까요?",
                   [("o0", "맞아요, 안정적이라 믿을 만해요", True), ("o1", "안 맞아요, 안정적인데 믿을 수 없어요", False)],
                   "hence는 '그래서'예요. 앞(stable, +)과 뒤(reliable)가 같은 쪽인지 봐요.",
                   why="stable(안정적, +) → hence(그래서) → reliable(믿을 만한, +), 같은 쪽으로 이어져요. ④는 문맥에 맞아요.",
                   highlight=["more stable", "hence"], signs=[{"text": "more stable", "sign": "+"}],
                   tips=[tip("hence", "'그래서, 따라서'예요. 앞이 원인, 뒤가 결과예요.", "hence")],
                   panel=check("1", "2"), panel_below=True),
            show("s5_check", "④reliable은 문맥에 맞아요. 안정적인 정보 = 믿을 만한 정보예요.",
                 panel=check("1", "2", "4"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Further", "게다가"), g("a variety of mobile animals", "여러 이동하는 동물들"), g("give more weight to", "~에 더 무게를 주다"),
                    g("nearer than to farther landmarks", "먼 랜드마크보다 가까운 것에"), g("in estimation", "추정할 때"),
                    g("consistent with", "~와 일치하는"), g("Weber’s law", "베버의 법칙"), g("in which", "그 법칙에서는"),
                    g("smaller distances", "더 짧은 거리"), g("would be coded more accurately", "더 정확하게 기록된다"), g("than larger distances", "더 긴 거리보다")],
        "slashes": ["Further,", "mobile animals", "more weight", "farther landmarks", "in estimation,", "Weber’s law", "smaller distances",
                    "more accurately"],
        "roles": [r("a variety of mobile animals", "S"), r("give", "V"), r("more weight", "O")],
        "modifiers": ["in which smaller distances would be coded more accurately than larger distances"],
        "steps": [
            choice("s6_weber",
                   "동물들은 먼 랜드마크보다 가까운 것에 더 무게를 둬요. Weber의 법칙은 짧은 거리가 더 정확히 기록된대요. 두 내용은 ⑤consistent(일치)할까요?",
                   [("o0", "일치하지 않는다", False), ("o1", "일치한다", True)],
                   "가까운 것 = 짧은 거리예요. 짧은 거리가 더 정확하면, 그쪽에 무게를 두는 게 자연스러울까요?",
                   why="가까운 랜드마크 = 짧은 거리 = 더 정확하게 기록돼요. 그러니 가까운 것에 무게를 두는 건 Weber의 법칙과 일치해요. ⑤는 문맥에 맞아요.",
                   highlight=["give more weight to", "smaller distances", "more accurately"],
                   tips=[tip("consistent with", "'~와 일치하는, 모순되지 않는'이에요.", "consistent with")]),
            show("s6_check", "①②④⑤는 모두 흐름에 맞았어요. 남은 하나, because it is more stable(+)과 짝이 맞지 않는 말을 문제에서 골라 봐요.",
                 panel=check("1", "2", "4", "5"), panel_below=True, button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 2, [m("in a small room", "작은 방에서는"), " 아이들이 ", m("nongeometric features", "비기하 특징"), " 정보를 ",
                         m("failed to incorporate", "포함하지 못했지만"), ", ", m("in a larger room", "더 큰 방에서는"), " ",
                         m("both types of information", "두 종류의 정보 모두"), "를 ", m("they used", "그들은 썼다"), "."],
          match_display="Although, in a small room, children failed to incorporate nongeometric features, they used both types of information in a larger room.",
          sv_new=sv_step("s2_basic_sv", ["children", "failed", "they", "used", "both types of information"],
                         {"they": "S", "used": "V", "both types of information": "O"},
                         {"children": "그건 Although 덩어리 안의 주어예요.", "failed": "그건 Although 덩어리 안의 동사예요."},
                         "콤마 뒤 메인 문장은 주어 they, 동사 used, 목적어 both types of information이에요.",
                         ask="콤마 뒤 메인 문장에서 주어(S), 동사(V), 목적어(O)를 찾아볼까요?"),
          meaning_ids=["s2_check"])
add_basic(sentences, 3, [m("These findings", "이 연구 결과들은"), " ", m("geometric and nongeometric information", "기하·비기하 정보가"), " ",
                         m("in a weighted fashion", "무게를 달리한 방식으로"), " ", m("may be combined", "결합될 수 있다"), "고 ", m("suggest", "시사한다"), "."],
          match_display="These findings suggest that geometric and nongeometric information may be combined in a weighted fashion.",
          sv_new=sv_step("s3_basic_sv", ["These findings", "suggest", "geometric and nongeometric information", "may be combined"],
                         {"These findings": "S", "suggest": "V"},
                         {"geometric and nongeometric information": "그건 that 뒤 덩어리 안의 주어예요.", "may be combined": "그건 that 뒤 덩어리 안의 동사예요."},
                         "주어는 These findings, 동사는 suggest예요. that 뒤가 시사하는 내용이에요."),
          meaning_after="s3_weight")
add_basic(sentences, 4, [m("Geometry", "기하 정보는"), " ", m("it is more stable", "더 안정적이기"), " ", m("because", "때문에"), " — ",
                         m("across time", "시간이 지나도"), "."],
          sv_new=sv_step("s4_basic_sv", ["Geometry", "may be", "it", "is"], {"Geometry": "S", "may be": "V"},
                         {"it": "그건 because 뒤 덩어리 안의 주어예요.", "is": "그건 because 뒤 덩어리 안의 동사예요."},
                         "주어는 Geometry, 동사는 may be예요. 그 뒤가 밑줄 ③이에요."),
          meaning_after="s4_stable")
add_basic(sentences, 6, [m("a variety of mobile animals", "여러 이동하는 동물들은"), " ", m("nearer than to farther landmarks", "먼 랜드마크보다 가까운 것에"), " ",
                         m("give more weight to", "더 무게를 준다"), "."],
          match_display="Further, a variety of mobile animals give more weight to nearer than to farther landmarks in estimation.",
          sv_new=sv_step("s6_basic_sv", ["a variety of mobile animals", "give", "more weight", "smaller distances"],
                         {"a variety of mobile animals": "S", "give": "V", "more weight": "O"},
                         {"smaller distances": "그건 in which(그 법칙에서는) 뒤 덩어리 안의 주어예요."},
                         "주어는 a variety of mobile animals, 동사는 give, 목적어는 more weight예요."),
          meaning_after="s6_weber")

SENSES = {
    1: [sense("while", "While it has been found", "~이지만, ~인 반면", "접속사 while (대조)"),
        sense("that", "found that young children", "~라는 것이", "명사절 that (it is found that …)"),
        sense("to", "to determine", "~하기 위해", "to부정사 (목적)")],
    2: [sense("to", "failed to incorporate", "~하지 (못하다)", "fail + to부정사 = ~하지 못하다")],
    3: [sense("that", "suggest that geometric", "~라는 것을", "명사절 that (suggest that …)")],
    5: [sense("for", "for example", "(for example의 일부)", "for example = 예를 들어")],
    6: [sense("to", "more weight to nearer", "~에 (무게를 주다)", "give weight to + 명사"),
        sense("to", "than to farther landmarks", "~에 (무게를 주다)", "give weight to (비교 대상 앞에 다시)"),
        sense("which", "in which smaller distances", "그 (법칙)에서는", "전치사 + which = 앞 명사(Weber’s law)를 받아 덧붙임")],
}

WORDS = {"found": "밝혀진", "young": "어린", "rely": "의존하다", "exclusively": "오로지", "geometric": "기하학의", "information": "정보",
         "determine": "알아내다", "location": "위치", "object": "물건", "hidden": "숨겨진", "small": "작은", "enclosure": "둘러싸인 공간",
         "exclusive": "오로지 그것만의", "use": "사용", "geometry": "기하 정보, 기하학", "occur": "일어나다", "larger": "더 큰",
         "spaces": "공간", "room": "방", "children": "아이들", "failed": "~하지 못했다", "incorporate": "포함하다",
         "nongeometric": "비기하학적인", "features": "특징", "blue": "파란", "wall": "벽", "used": "썼다", "types": "종류",
         "findings": "연구 결과", "suggest": "시사하다", "combined": "결합된", "weighted": "가중된, 무게가 실린", "fashion": "방식",
         "stable": "안정적인", "across": "~에 걸쳐", "time": "시간", "landmark": "랜드마크, 주요 지형지물", "depend": "달려 있다",
         "ecological": "생태학적인", "validity": "타당성", "example": "예", "hence": "그래서", "reliable": "믿을 만한", "variety": "다양함",
         "mobile": "이동하는", "animals": "동물들", "give": "주다", "weight": "무게, 가중치", "nearer": "더 가까운", "farther": "더 먼",
         "landmarks": "랜드마크들", "estimation": "추정", "consistent": "일치하는", "weber’s": "베버의", "law": "법칙",
         "smaller": "더 짧은", "distances": "거리", "coded": "기록된", "accurately": "정확하게", "invalid": "타당하지 않은",
         "may": "~일 수 있다", "both": "둘 다", "i.e": "즉, 다시 말해", "whether": "~인지 (아닌지)"}

STORIES = [
    (2, [sc("문장 1~2", "🧒", "small room → only geometry", "작은 공간에선 아이들이 방 모양(기하)만 쓰고, 큰 방에선 파란 벽 같은 특징도 써요")]),
    (5, [sc("문장 3", "⚖️", "combined in a weighted fashion", "두 정보는 무게를 달리해서 섞여요"),
         sc("문장 4~5", "🧱", "more stable · more reliable", "안정적인 정보일수록 믿을 만해요 — 큰 특징도 더 안정적이에요")]),
]

exam = {
    "question": "다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은? [3점]",
    "underline": UNDER, "sentence": 4, "analysis_first": True, "wrong_rate": 45.9, "wrong_rank": 12,
    "glosses": [g("failed", "~하지 못했다"), g("weighted", "가중된"), g("invalid", "타당하지 않은"), g("reliable", "믿을 만한"), g("consistent", "일치하는")],
    "options": [
        {"id": "1", "label": "failed", "keywords": ["failed"], "ko": "~하지 못했다"},
        {"id": "2", "label": "weighted", "keywords": ["weighted"], "ko": "가중된"},
        {"id": "3", "label": "invalid", "keywords": ["invalid"], "ko": "타당하지 않은", "correct": True},
        {"id": "4", "label": "reliable", "keywords": ["reliable"], "ko": "믿을 만한"},
        {"id": "5", "label": "consistent", "keywords": ["consistent"], "ko": "일치하는"},
    ],
    "brief": exam_brief(
        "밑줄 점검표를 떠올려 봐요. 흐름(+/−)과 짝이 맞지 않는 하나를 골라요.",
        "정답이에요! because 뒤 이유는 '더 안정적이다(+)'예요. 안정적이라서 기하 정보가 '타당하지 않다(invalid, −)'는 건 반대예요. 더 믿고 우선한다는 privileged(특혜를 받는)가 맞아요.",
        "정답은 ③이에요. 더 안정적이라서(+) 오히려 우선 대우를 받아요(privileged). invalid(−)는 반대예요.",
        {"1": "작은 방에선 기하 정보만 썼으니 파란 벽 정보를 넣지 못했다(failed)가 맞아요.",
         "2": "두 정보를 무게를 달리해 섞는다(weighted)는 뒤의 give more weight와 이어져요.",
         "4": "큰 특징은 더 안정적이고 그래서(hence) 더 믿을 만하다(reliable), 같은 쪽으로 이어져요.",
         "5": "가까운 것(짧은 거리)이 더 정확하게 기록되니, 가까운 것에 무게를 두는 건 Weber의 법칙과 일치해요(consistent)."},
        {"5": review(13.2,
                     "⑤ 앞뒤를 나란히 놓아 봐요. 동물은 가까운 랜드마크에 더 무게를 줘요. Weber의 법칙은 짧은 거리가 더 정확히 기록된대요. 가까운 것 = 짧은 거리 = 더 정확하니, 무게를 주는 게 법칙과 일치(consistent)해요.",
                     "그래서 ⑤는 문맥에 맞아요. 어디서 헷갈렸어요?",
                     [("Weber의 법칙 문장이 어려웠어요", ["long_relative"],
                       "알려 줘서 고마워요. in which 뒤는 그 법칙의 내용이에요. 앞으로 긴 덩어리는 끊어 읽기로 나눠서 보여 줄게요."),
                      ("가까운 것 = 짧은 거리로 못 이었어요", ["paraphrase_link"],
                       "알려 줘서 고마워요. nearer landmarks와 smaller distances는 같은 말을 바꿔 쓴 거예요. 앞으로 바꿔 쓴 말을 짝지어 보여 줄게요."),
                      ("둘 다요", ["long_relative", "paraphrase_link"], "알려 줘서 고마워요. 앞으로 긴 덩어리와 바꿔 쓴 말을 같이 짚어 줄게요.")],
                     panel=rows(("동물", "give more weight to nearer landmarks", "가까운 것에 더 무게", "hl"),
                                ("Weber’s law", "smaller distances … coded more accurately", "짧은 거리가 더 정확 → 일치", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 30번 (문맥상 낱말의 쓰임, 3점)",
    topic="어휘 문제 푸는 법: 요지 → 두 그룹·+/− 흐름 → 밑줄 단어가 흐름에 맞는지 하나씩 점검",
    method={"type": "word_in_context", "labels": ["요지 잡기", "두 그룹으로 나누기", "밑줄 단어 맞춰 보기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-geometry.svg", ("Room shape", "방 모양"), "+", ("Blue wall", "파란 벽"),
                                       "길을 찾을 때 어떤 정보를 더 믿을까?", "2024년 3월 30번 도입 칠판"),
                      "alt": "칠판: Room shape(방 모양) + Blue wall(파란 벽)", "kind": "drawing"},
            "method": METHOD_IMAGES["vocab"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "숨긴 물건을 찾을 때, 방의 모양과 파란 벽 중 무엇을 더 믿을까요? 이번 글은 위치를 찾을 때 쓰는 두 가지 정보를 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "어휘 문제는 단어 뜻만 보면 다 맞아 보여요. 문장마다 흐름을 잡아야 틀린 단어가 보여요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "요지를 잡고, 정보를 두 그룹으로 나눈 뒤, 밑줄 단어가 흐름에 맞는지 하나씩 볼 거예요. 칠판 순서대로 해 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("rely on", "~에 의존하다"), g("exclusively", "오로지"), g("determine", "알아내다"), g("incorporate", "포함하다"),
                           g("feature", "특징"), g("finding", "연구 결과"), g("combine", "결합하다"), g("weighted", "가중된"),
                           g("stable", "안정적인"), g("landmark", "랜드마크"), g("validity", "타당성"), g("hence", "그래서"),
                           g("reliable", "믿을 만한"), g("estimation", "추정"), g("consistent with", "~와 일치하는"), g("accurately", "정확하게")],
               "options": [g("invalid", "타당하지 않은"), g("privileged", "특혜를 받는, 우선시되는")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="어휘 문제 푸는 법",
       chunks={"young children": "어린아이들", "rely": "의존하다", "geometric information": "기하 정보",
               "exclusive use of geometry": "기하 정보만 쓰는 것", "does not occur": "일어나지 않는다", "children": "아이들", "failed": "~하지 못했다",
               "they": "그들", "used": "썼다", "both types of information": "두 종류의 정보 모두", "These findings": "이 연구 결과들",
               "suggest": "시사하다", "geometric and nongeometric information": "기하·비기하 정보", "may be combined": "결합될 수 있다",
               "Geometry": "기하 정보", "may be": "~일 수도 있다", "it": "그것", "is": "~이다",
               "nongeometric landmark information": "비기하 랜드마크 정보", "is combined": "결합되다", "may depend on": "~에 달려 있을 수 있다",
               "the ecological validity": "생태학적 타당성", "larger features": "더 큰 특징", "a variety of mobile animals": "여러 이동하는 동물들",
               "give": "주다", "more weight": "더 많은 무게", "smaller distances": "더 짧은 거리"})
