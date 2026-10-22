"""2026년 6월 모의평가(2027학년도) 31번 레슨 + 대사를 만든다 (빈칸 추론, 2점). 오답률 69%(메가스터디) · Top 2.

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_31.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸이 가운데(넷째 문장). 정답 ① desired(바람직한).
선택률(메가스터디 풀서비스 채점): ① 31 ② 19 ③ 10 ④ 33 ⑤ 8 — 많이 고른 오답 ④ natural(자연스러운)이 정답보다 많다, 그다음 ② unstable.
④ 짐작: 6·7문장의 the original · “as found”(원래 그대로)를 「자연 그대로」로 읽고, 두 쪽(보존 ↔ 보전)을 거꾸로 붙였다.
   3문장 예시의 생태계(ecosystem)도 「자연」을 떠올리게 한다.
② 짐작: 빈칸 문장의 acknowledge change(변화를 인정)에서 「변하는 = 불안정한」을 떠올렸다. 하지만 불안정한 상태를 일부러 오래 가게(prolong) 하지는 않는다.
열쇠: 두 쪽 — conservation 쪽(restorative · acknowledge change · manage · yield or harvest or use · restore or repair)
↔ preservation 쪽(protectors · as minimally as possible · the original · “as found”). 빈칸 문장의 주어는 Conservationists → conservation 쪽.
시험지 아래 *풀이 단어: contemplation(주시), deteriorate(나쁘게 하다) — 핵심어·단어 체크에서 뺐다(뜻만 둠).
해설지(2027-06-평가원/해설.txt 31번) 해석·Words and Phrases와 대조함 — 단어 뜻·Tip은 해설 번역을 따랐다.
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음). Claude 초안 — 선생님 검토 전.

선생님이 확인할 점
1. 칠판 단어 지도는 3문장에서 conservation 쪽 한 칸만 먼저 연다(preservation 쪽 말이 아직 안 나와서 — 빈 칸 금지).
   5문장(Preservationists … protectors)에서 두 칸이 된다. 2문장의 「지금 상태로 유지·변화로부터 보호」는 두 말 공통 뜻이라 칠판에 넣지 않았다.
2. s4_side 「같은 쪽? 반대 쪽?」의 기준을 「글쓴이 주장」이 아니라 「칠판의 conservation 쪽(복원)과 같은 쪽?」으로 물었다.
   이 글은 글쓴이가 한쪽 편을 들지 않고 두 쪽을 비교하는 글이라서 — 빈칸이 어느 쪽 사람의 이야기인지가 열쇠다.
3. ④ natural을 많이 고른 이유(원래 그대로 = 자연 그대로, 생태계 예시)는 추측이다. option_review는 ④·② 둘 다 달았다.
4. 2문장 present(현재의)·state(상태), 6문장 yield(산출량)를 헷갈리는 단어(trap)로 두었다 — 엑셀(함정단어.xlsx)에는 안 넣었다.
5. 해석 맞추기는 1문장(짧은 문장)에만. 2문장은 길고(30단어 넘음) 뜻 질문이 있어서 뺐다.
6. 5문장 끊어읽기 roles에 목적어(themselves)를 넣지 않았다 — 괄호 안 call themselves와 겹쳐서 표시 자리가 어긋날 수 있다.
7. 시험지의 대시(―)는 앱 규칙대로 「—」로 바꿨다. 대시가 하나뿐이라 흐림(삽입)으로 두지 않았다.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, tip, groups, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-06-31-preserve-conserve"

BLANK = "Conservationists acknowledge change but try to manage it in order to prolong a(n) ________ state."
S = [
    "Ever since the early Enlightenment, preservation and conservation have been closely related.",
    "Taken as near synonyms, their meaning is to maintain an object or system insofar as possible in its present state, "
    "to protect it from change, usually for contemplation, research, display, and perhaps for use.",
    "Conservationists who distinguish their activities from preservation emphasize conservation’s restorative aspects — "
    "restoring a historical musical instrument, for example, or a painting, or a dinosaur, or an ecosystem.",
    BLANK,
    "Preservationists (who may nonetheless call themselves conservationists) think of themselves more as protectors.",
    "They sometimes criticize conservationists for setting an additional priority on yield or harvest or use, rather than "
    "interfering as minimally as possible in order to preserve the original object or system, as they would do.",
    "Preservationists would, for example, prefer to keep a historical musical instrument “as found” in a deteriorated state, "
    "for study, rather than to restore or repair it for display or use.",
]
# 해설지 해석 (2027-06-평가원/해설.txt 31번)
KO = [
    "초기 계몽주의 이후로 줄곧, 보존과 보전은 밀접하게 관련되어 왔다.",
    "거의 동의어로 받아들여질 때, 그것들의 의미는 보통 주시, 연구, 전시, 그리고 아마도 사용을 위해 사물이나 체계를 가능한 한 "
    "그것의 현재 상태로 유지하고, 그것을 변화로부터 보호하는 것이다.",
    "자신의 활동을 보존과 구별하는 보전주의자는 보전의 복원적인 측면을 강조하는데, 예를 들어 역사적인 악기나 그림, 공룡, "
    "또는 생태계를 복원하는 것을 강조한다.",
    "보전주의자는 변화를 인정하지만, ________ 상태를 연장하기 위해 그것을 관리하려고 한다.",
    "보존주의자는, (그럼에도 불구하고 자신을 보전주의자라고 부를 수도 있지만), 자신을 보호자에 더 가깝다고 생각한다.",
    "그들은 때때로 보전주의자가, 자신들처럼 원래의 사물이나 체계를 보존하기 위해 가능한 한 최소한으로 개입하기보다는 "
    "산출량이나 수확 또는 이용에 추가적인 우선순위를 둔다고 비판한다.",
    "예를 들어, 보존주의자는 역사적인 악기를 전시나 이용을 위해 복원하거나 수리하기보다는, 연구를 위해 ‘발견된 그대로’의 "
    "손상된 상태로 유지하는 것을 선호할 것이다.",
]

LEFT = "왼쪽 · conservation 쪽"
RIGHT = "오른쪽 · preservation 쪽"


def board(left, right=None, fresh=(), sort=None):
    """단어 지도 — 묶음 이름은 글에 나온 말(conservation / preservation)까지만. 빈칸 말은 쓰지 않는다.
    preservation 쪽 말이 나오기 전(3·4문장)에는 한 칸만"""
    if right is None:
        return groups("conservation과 preservation", "conservation 쪽", left, fresh=fresh)
    return groups("conservation과 preservation", "conservation 쪽", left, "preservation 쪽", right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": LEFT, "right": RIGHT} if sort else None)


L3 = [("restorative", "복원적인")]
L4 = L3 + [("acknowledge change", "변화를 인정"), ("manage", "관리")]
R5 = [("protectors", "보호자")]
L6 = L4 + [("yield or harvest or use", "산출량·수확·이용")]
R6 = R5 + [("as minimally as possible", "가능한 한 적게 손대기"), ("the original", "원래의 것")]
L7 = L6 + [("restore or repair", "복원·수리")]
R7 = R6 + [("“as found”", "발견된 그대로")]

SIDE_TIP = tip("같은 쪽? 반대 쪽?", "빈칸 문장의 주어가 누구인지, 그 사람이 앞에서 어느 쪽이었는지 보면 같은 쪽인지 알 수 있어요. "
               "But, However, not 같은 반전 단서가 있으면 반대 의견이 들어가요.")

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("Ever since the early Enlightenment", "초기 계몽주의 이후로 줄곧"), g("Ever since", "~ 이후로 줄곧"),
                    g("early", "초기의"), g("Enlightenment", "계몽주의"),
                    g("preservation and conservation", "보존과 보전"), g("preservation", "보존"), g("conservation", "보전"),
                    g("have been closely related", "밀접하게 관련되어 왔다"), g("closely", "밀접하게"), g("related", "관련된"),
                    # 빈칸 문장 (s1 화면에서 띄운다)
                    g("Conservationists", "보전주의자들 · 보전(conservation)을 하는 사람들"),
                    g("acknowledge change", "변화를 인정하다"), g("acknowledge", "인정하다"), g("change", "변화"),
                    g("try to manage", "관리하려고 하다"), g("manage", "관리하다"),
                    g("in order to prolong", "연장하기 위해"), g("prolong", "연장하다 · 더 오래 가게 하다"), g("state", "상태")],
        "slashes": ["Enlightenment,"],
        "roles": [r("preservation and conservation", "S"), r("have been closely related", "V")],
        "steps": [
            show("s1_passage", "빈칸은 여기, 넷째 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "보전주의자는 변화를 인정하지만, ____ 상태를 오래 가게 하려고 변화를 관리한다", True),
                    ("o1", "보전주의자는 변화를 막고, ____ 상태로 되돌리려 한다", False),
                    ("o2", "보전주의자는 변화를 인정해서, ____ 상태가 끝나도록 그냥 둔다", False)],
                   "acknowledge는 '인정하다', prolong은 '연장하다, 더 오래 가게 하다'예요. but 앞뒤를 나눠 봐요.",
                   why="'acknowledge change but try to manage it', 변화를 인정하지만 관리하려 해요. 'in order to prolong', 그 상태를 더 오래 가게 하려고요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["acknowledge change", "but", "manage", "prolong", "________"],
                   tips=[tip("in order to ~", "'~하기 위해'예요. in order to prolong = 연장하기 위해.", "in order to")]),
            show("s1_where", "보전주의자(Conservationists)가 어떤 상태를 오래 가게 하려는지가 빈칸이에요. 그걸 생각하며 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                 highlight=["Conservationists", "prolong"]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "medium",
        "glosses": [g("Taken as near synonyms", "거의 동의어로 받아들여질 때"), g("Taken", "받아들여진"),
                    g("near synonyms", "거의 동의어"), g("near", "거의 ~에 가까운"), g("synonyms", "동의어"),
                    g("their meaning", "그것들의 의미"), g("meaning", "의미"), g("is", "~이다"),
                    g("to maintain an object or system", "사물이나 체계를 유지하는 것"), g("maintain", "유지하다"),
                    g("object", "사물"), g("system", "체계"), g("insofar as possible", "가능한 한"), g("insofar", "~하는 한"),
                    g("possible", "가능한"), g("in its present state", "그것의 현재 상태로"), g("present", "현재의"),
                    g("state", "상태"), g("to protect it from change", "그것을 변화로부터 보호하는 것"), g("protect", "보호하다"),
                    g("change", "변화"), g("usually", "보통"), g("contemplation", "주시(注視) · 가만히 지켜봄"),
                    g("research", "연구"), g("display", "전시"), g("perhaps", "아마도"), g("for use", "사용을 위해"),
                    g("use", "사용, 이용")],
        "slashes": ["near synonyms,", "object or system", "insofar as possible", "present state,", "from change,", "research, display,"],
        "roles": [r("their meaning", "S"), r("is", "V"), r("to maintain an object or system", "C"), r("to protect it from change", "C")],
        "steps": [
            choice("s2_meaning",
                   "두 말을 거의 같은 말로 볼 때, 그 뜻은 무엇일까요?",
                   [("o0", "사물을 가능한 한 지금 상태로 유지하고, 변화로부터 보호하는 것", True),
                    ("o1", "사물을 새것으로 바꾸어 계속 발전시키는 것", False),
                    ("o2", "사물을 연구한 뒤 자연으로 돌려보내는 것", False)],
                   "is 뒤 'to maintain …'과 'to protect …' 두 덩어리를 봐요.",
                   why="'to maintain … in its present state', 현재 상태로 유지하고, 'to protect it from change', 변화로부터 보호하는 거예요.",
                   highlight=["maintain", "present state", "protect", "change"],
                   tips=[tip("Taken as ~", "'~로 받아들여질 때'예요. 두 말(preservation, conservation)이 거의 동의어로 받아들여질 때라는 뜻이에요.", "Taken as"),
                         tip("protect A from B", "'A를 B로부터 보호하다'예요. protect it from change = 그것을 변화로부터 보호하다.", "protect")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("Conservationists", "보전주의자들 · 보전을 하는 사람들"),
                    g("who distinguish their activities from preservation", "자기 활동을 보존과 구별하는"),
                    g("distinguish", "구별하다"), g("their activities", "자기 활동"), g("activities", "활동"),
                    g("from preservation", "보존과"), g("preservation", "보존"), g("emphasize", "강조하다"),
                    g("conservation’s restorative aspects", "보전의 복원적인 측면"), g("conservation’s", "보전의"),
                    g("restorative aspects", "복원적인 측면"), g("restorative", "복원적인 · 원래대로 되살리는"), g("aspects", "측면"),
                    g("restoring", "복원하는 것"), g("a historical musical instrument", "역사적인 악기"), g("historical", "역사적인"),
                    g("musical instrument", "악기"), g("musical", "음악의"), g("instrument", "기구, 악기"),
                    g("for example", "예를 들어"), g("example", "예"), g("a painting", "그림"), g("painting", "그림"),
                    g("a dinosaur", "공룡"), g("dinosaur", "공룡"), g("an ecosystem", "생태계"), g("ecosystem", "생태계")],
        "slashes": ["Conservationists", "from preservation", "restorative aspects", "musical instrument,", "for example,", "a painting,",
                    "a dinosaur,"],
        "roles": [r("Conservationists", "S"), r("emphasize", "V"), r("conservation’s restorative aspects", "O")],
        "modifiers": ["who distinguish their activities from preservation"],
        "steps": [
            pick("s3_find", "보전주의자가 보존과 달리 강조(emphasize)하는 것을 문장에서 찾아 눌러 볼까요?",
                 ["their activities", "restorative aspects", "a historical musical instrument", "an ecosystem"], ["restorative aspects"],
                 "그건 보전주의자가 강조하는 것이 아니에요.",
                 "restorative aspects(복원적인 측면)예요. 대시(—) 뒤는 악기·그림·공룡·생태계를 복원하는 예시예요.",
                 wrong_by={"their activities": "their activities는 보존과 구별하는 '자기 활동'이에요. emphasize 뒤를 봐요.",
                           "a historical musical instrument": "그건 대시(—) 뒤 예시 속 말이에요. 무엇의 예시인지 대시 앞을 봐요.",
                           "an ecosystem": "그건 대시(—) 뒤 예시 속 말이에요. 무엇의 예시인지 대시 앞을 봐요."},
                 tips=[tip("distinguish A from B", "'A를 B와 구별하다'예요. distinguish their activities from preservation = 자기 활동을 보존과 구별하다.",
                           "distinguish")]),
            show("s3_board", "보전(conservation)은 망가진 것을 원래대로 되살리는(restorative) 쪽이에요.",
                 panel=board(L3, fresh=("restorative",)), highlight=["restorative"], button="다음 문장",
                 tips=[tip("대시(—) 뒤 예시", "대시(—) 뒤에 for example이 있으면 앞말의 예시예요. 앞말을 이해했으면 가볍게 넘겨도 돼요.")]),
        ],
    },
    {
        "id": 4, "text": BLANK, "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Conservationists", "보전주의자들"), g("acknowledge change", "변화를 인정하다"), g("acknowledge", "인정하다"),
                    g("change", "변화"), g("try to manage", "관리하려고 하다"), g("manage", "관리하다"),
                    g("in order to prolong", "연장하기 위해"), g("prolong", "연장하다 · 더 오래 가게 하다"), g("state", "상태")],
        "slashes": ["acknowledge change", "manage it"],
        "roles": [r("Conservationists", "S"), r("acknowledge", "V"), r("change", "O"), r("try to manage", "V"), r("it", "O")],
        "steps": [
            choice("s4_side",
                   "빈칸 상태는 칠판의 conservation 쪽(복원) 이야기와 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 — 손보고 관리해서 지키는 상태", True), ("o1", "반대 쪽 — 손대지 않은 원래 그대로의 상태", False)],
                   "빈칸 문장의 주어는 Conservationists예요. 변화를 인정하고 관리(manage)한대요.",
                   why="주어 Conservationists는 3문장에서 복원을 강조한 사람들이에요. 변화를 막지 않고 관리하니, 손대지 않은 그대로의 상태가 아니에요.",
                   highlight=["Conservationists", "acknowledge change", "manage"], panel=board(L3), tips=[SIDE_TIP],
                   point="빈칸 = 주어 Conservationists(복원하는 쪽)가 관리해서 오래 가게 하려는 상태 = conservation 쪽"),
            choice("s4_fill",
                   "빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "손대지 않아 발견된 그대로인", False),
                    ("o1", "변화 때문에 흔들리는, 불안정한", False),
                    ("o2", "고쳐서라도 오래 지키고 싶은, 좋은", True)],
                   "보전주의자는 복원해서 그 상태를 일부러 오래 가게(prolong) 해요. 일부러 오래 가게 하는 상태라면 어떤 상태일지 생각해 봐요.",
                   why="보전주의자는 변화를 관리해서 그 상태를 일부러 오래 가게 해요. 오래 지키려는 상태니 좋은, 바라는 상태예요.",
                   highlight=["prolong", "________"], panel=board(L4),
                   point="빈칸 = 복원·관리해서 오래 가게 하려는 (좋은, 바라는) 상태"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("Preservationists", "보존주의자들 · 보존(preservation)을 하는 사람들"),
                    g("who may nonetheless call themselves conservationists", "그럼에도 자신을 보전주의자라고 부를 수도 있는"),
                    g("nonetheless", "그럼에도 불구하고"), g("call themselves", "자신을 ~라고 부르다"), g("call", "부르다"),
                    g("themselves", "자신"), g("conservationists", "보전주의자들"), g("think of themselves", "자신을 ~로 생각하다"),
                    g("more as protectors", "보호자에 더 가깝게"), g("protectors", "보호자")],
        "slashes": ["Preservationists", "conservationists)", "of themselves"],
        "roles": [r("Preservationists", "S"), r("think of", "V")],
        "modifiers": ["who may nonetheless call themselves conservationists"],
        "steps": [
            show("s5_board", "보존주의자(Preservationists)는 자신을 보호자(protectors)에 더 가깝게 생각해요. 괄호 안은 빼고 읽어도 돼요.",
                 panel=board(L4, R5, fresh=("protectors",)), highlight=["Preservationists", "protectors"],
                 faded=["(who may nonetheless call themselves conservationists)"], button="다음 문장",
                 tips=[tip("think of A as B", "'A를 B로 생각하다'예요. think of themselves more as protectors = 자신을 보호자에 더 가깝다고 생각하다.",
                           "think of")]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("sometimes", "때때로"), g("criticize", "비판하다"), g("conservationists", "보전주의자들"),
                    g("setting an additional priority on", "~에 추가적인 우선순위를 두는 것"), g("setting", "두는 것"),
                    g("additional", "추가적인"), g("priority", "우선순위"), g("yield or harvest or use", "산출량이나 수확 또는 이용"),
                    g("yield", "산출량"), g("harvest", "수확"), g("use", "이용"), g("rather than", "~하기보다는"),
                    g("interfering as minimally as possible", "가능한 한 최소한으로 개입하는 것"), g("interfering", "개입하는 것"),
                    g("minimally", "최소한으로"), g("possible", "가능한"), g("in order to preserve", "보존하기 위해"),
                    g("preserve", "보존하다"), g("the original object or system", "원래의 사물이나 체계"),
                    g("the original", "원래의 것"), g("original", "원래의"), g("object", "사물"), g("system", "체계"),
                    g("would do", "그렇게 할 것이다")],
        "slashes": ["conservationists", "additional priority", "or use,", "rather than", "as possible", "object or system,"],
        "roles": [r("They", "S"), r("criticize", "V"), r("conservationists", "O")],
        "steps": [
            choice("s6_crit",
                   "보존주의자는 보전주의자의 무엇을 비판한대요?",
                   [("o0", "산출량·수확·이용에 우선순위를 더 둔다", True),
                    ("o1", "너무 조금만 손댄다", False),
                    ("o2", "원래 상태를 그대로 지키려 한다", False)],
                   "criticize A for B는 'B라고 A를 비판하다'예요. for 뒤를 봐요.",
                   why="'setting an additional priority on yield or harvest or use', 산출량·수확·이용을 더 우선한다고 비판해요.",
                   highlight=["criticize", "priority", "yield or harvest or use"],
                   tips=[tip("criticize A for B", "'B라고(B 때문에) A를 비판하다'예요.", "criticize"),
                         tip("rather than ~", "'~하기보다는'이에요. A rather than B = B보다는 A.", "rather than")]),
            choice("s6_sort",
                   "'preserve the original(원래의 것을 보존하다)'은 칠판 어느 쪽 말일까요?",
                   [("o0", LEFT, False), ("o1", RIGHT, True)],
                   "문장 끝 'as they would do'를 봐요. they는 이 문장의 주어 They와 같은 사람들이에요.",
                   why="'as they would do', 보존주의자들이 그렇게 한대요. 가능한 한 적게 손대고 원래 것을 지키는 건 preservation 쪽이에요.",
                   panel=board(L4, R5, sort=["the original"]), highlight=["the original", "as they would do"]),
            show("s6_map", "보전 쪽은 이용(use)을 더 우선해요. 보존 쪽은 가능한 한 적게 손대고(minimally) 원래 것(the original)을 지켜요.",
                 panel=board(L6, R6, fresh=("yield or harvest or use", "as minimally as possible", "the original")),
                 highlight=["use", "minimally", "the original"], button="다음 문장",
                 tips=[tip("as ~ as possible", "'가능한 한 ~하게'예요. as minimally as possible = 가능한 한 최소한으로.", "as minimally")]),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("Preservationists", "보존주의자들"), g("would", "~할 것이다"), g("for example", "예를 들어"), g("example", "예"),
                    g("prefer to keep", "유지하는 것을 선호하다"), g("prefer", "선호하다"), g("keep", "유지하다"),
                    g("a historical musical instrument", "역사적인 악기"), g("historical", "역사적인"), g("musical", "음악의"),
                    g("instrument", "기구, 악기"), g("as found", "발견된 그대로"), g("found", "발견된"),
                    g("in a deteriorated state", "손상된 상태로"), g("deteriorated", "손상된 · 나빠진"), g("state", "상태"),
                    g("for study", "연구를 위해"), g("study", "연구"), g("rather than", "~하기보다는"),
                    g("restore or repair", "복원하거나 수리하다"), g("restore", "복원하다"), g("repair", "수리하다"),
                    g("for display or use", "전시나 이용을 위해"), g("display", "전시"), g("use", "이용")],
        "slashes": ["for example,", "prefer to keep", "musical instrument", "“as found”", "deteriorated state,", "for study,", "rather than",
                    "repair it"],
        "roles": [r("Preservationists", "S"), r("would … prefer", "V"), r("to keep a historical musical instrument", "O")],
        "steps": [
            choice("s7_prefer",
                   "보존주의자는 오래된 악기를 어떻게 하고 싶어 한대요?",
                   [("o0", "발견된 그대로, 손상된 상태로 두고 연구한다", True),
                    ("o1", "고쳐서 전시하고 연주한다", False),
                    ("o2", "새 악기로 바꾼다", False)],
                   "prefer to A rather than to B는 'B하기보다 A하기를 선호하다'예요. rather than 앞쪽이 하고 싶은 거예요.",
                   why="'keep … “as found” in a deteriorated state, for study', 발견된 그대로 손상된 상태로 두고 연구하고 싶어 해요. 고치는 건 rather than 뒤, 원하지 않는 쪽이에요.",
                   highlight=["prefer", "“as found”", "rather than"], faded=["for example,"],
                   tips=[tip("as found", "'발견된 그대로'예요. 손대지 않고 처음 찾았을 때 모습 그대로라는 뜻이에요.", "as found")]),
            show("s7_map", "보존 쪽은 '발견된 그대로(as found)' 둬요. 보전 쪽은 복원하거나 수리해서(restore or repair) 전시하고 이용해요.",
                 panel=board(L7, R7, fresh=("“as found”", "restore or repair")), highlight=["“as found”", "restore or repair"],
                 faded=["for example,"]),
            show("s7_go", "빈칸은 보전(conservation) 쪽, 손보고 관리해서 오래 가게 하려는 상태예요. 이 상태를 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — 짧은 1문장만 (모두에게). 덩어리는 문장에 그대로 있는 구절
add_match(sentences, 1, [m("Ever since the early Enlightenment", "초기 계몽주의 이후로 줄곧"), ", ",
                         m("preservation and conservation", "보존과 보전은"), " ", m("have been closely related", "밀접하게 관련되어 왔다"), "."])
# 가리키는 말
add_refers(sentences, 2, {"their meaning": "preservation and conservation(보존과 보전)의 의미"})
add_refers(sentences, 4, {"it": "change(변화)"})
add_refers(sentences, 6, {"They": "Preservationists(보존주의자들)", "they": "Preservationists(보존주의자들)"})
add_refers(sentences, 7, {"it": "a historical musical instrument(역사적인 악기)"})

SENSES = {
    1: [sense("since", "Ever since the early Enlightenment", "~ 이후로 줄곧", "전치사 since (ever since = ~ 이후로 줄곧)")],
    2: [sense("as", "Taken as near synonyms", "~로", "take A as B(A를 B로 받아들이다)의 수동 분사구문 — ~로 받아들여질 때"),
        sense("to", "to maintain", "~하는 것", "to부정사 보어 (their meaning is to ~)"),
        sense("as", "insofar as possible", "~하는 한", "insofar as possible = 가능한 한"),
        sense("to", "to protect it", "~하는 것", "앞의 to maintain과 나란한 둘째 보어"),
        sense("for", "for contemplation, research, display", "~을 위해", "전치사 for (목적)"),
        sense("for", "for use", "~을 위해", "전치사 for (목적)")],
    3: [sense("for", "for example", "예를 들어", "for example = 예를 들어")],
    4: [sense("but", "but try to manage", "하지만", "접속사 but — 인정하지만 관리하려 한다"),
        sense("to", "try to manage", "~하려고", "try to + 동사원형 = ~하려고 하다"),
        sense("to", "in order to prolong", "~하기 위해", "in order to + 동사원형 = ~하기 위해")],
    5: [sense("as", "more as protectors", "~로", "think of A as B = A를 B로 생각하다")],
    6: [sense("for", "criticize conservationists for setting", "~한다고 (~ 때문에)", "criticize A for B = B라고 A를 비판하다"),
        sense("as", "as minimally", "~만큼", "as ~ as possible = 가능한 한 ~하게 (앞 as)"),
        sense("as", "as possible", "~만큼", "as ~ as possible (뒤 as)"),
        sense("to", "in order to preserve", "~하기 위해", "in order to + 동사원형 = ~하기 위해"),
        sense("as", "as they would do", "~하듯이", "접속사 as — 그들(보존주의자들)이 그러듯이")],
    7: [sense("for", "for example", "예를 들어", "for example = 예를 들어"),
        sense("to", "prefer to keep", "~하는 것을", "prefer to + 동사원형 = ~하는 것을 선호하다"),
        sense("as", "“as found”", "~한 대로", "접속사 as — as found = 발견된 그대로"),
        sense("for", "for study", "~을 위해", "전치사 for (목적)"),
        sense("to", "rather than to restore", "~하는 것", "prefer to A rather than to B — 둘째 to부정사"),
        sense("for", "for display or use", "~을 위해", "전치사 for (목적)")],
}

WORDS = {"ever": "줄곧, 언제나", "early": "초기의", "enlightenment": "계몽주의", "preservation": "보존", "conservation": "보전",
         "closely": "밀접하게", "related": "관련된", "taken": "받아들여진", "near": "거의 ~에 가까운", "synonyms": "동의어",
         "meaning": "의미", "maintain": "유지하다", "object": "사물", "system": "체계", "insofar": "~하는 한", "possible": "가능한",
         "present": "현재의", "state": "상태", "protect": "보호하다", "change": "변화", "distinguish": "구별하다",
         "activities": "활동", "conservation’s": "보전의", "restorative": "복원적인", "aspects": "측면", "historical": "역사적인",
         "musical": "음악의", "instrument": "기구, 악기", "painting": "그림", "dinosaur": "공룡", "ecosystem": "생태계",
         "example": "예", "acknowledge": "인정하다", "try": "~하려고 하다", "manage": "관리하다", "order": "순서 · in order to = ~하기 위해",
         "prolong": "연장하다", "nonetheless": "그럼에도 불구하고", "call": "부르다", "themselves": "자신",
         "conservationists": "보전주의자들", "protectors": "보호자", "setting": "두는 것", "additional": "추가적인",
         "priority": "우선순위", "yield": "산출량", "harvest": "수확", "use": "이용", "rather": "오히려 · rather than = ~하기보다는",
         "interfering": "개입하는 것", "minimally": "최소한으로", "preserve": "보존하다", "original": "원래의", "would": "~할 것이다",
         "prefer": "선호하다", "found": "발견된", "deteriorated": "손상된", "study": "연구", "restore": "복원하다", "repair": "수리하다",
         "display": "전시", "research": "연구", "contemplation": "주시", "usually": "보통", "perhaps": "아마도"}

STORIES = [
    (2, [sc("문장 1~2", "🏛️", "preservation ≈ conservation", "보존과 보전은 거의 같은 말로 쓰여요 — 지금 상태로 유지하고 변화로부터 보호해요")]),
    (4, [sc("문장 3", "🔧", "conservation → restorative", "보전주의자는 보존과 달리 복원하는 면을 강조해요"),
         sc("문장 4", "⏳", "manage change → prolong a(n) ____ state", "변화를 인정하고 관리해서 ____ 상태를 오래 가게 해요")]),
]

OPTIONS = [("1", "desired", "바람직한", True), ("2", "unstable", "불안정한", False), ("3", "isolated", "고립된", False),
           ("4", "natural", "자연스러운", False), ("5", "delicate", "연약한", False)]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 4, "analysis_first": True, "wrong_rate": 69, "wrong_rank": 2,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("desired", "바람직한, 바라던"), g("unstable", "불안정한"), g("isolated", "고립된"),
                g("natural", "자연스러운, 자연 그대로의"), g("delicate", "연약한")],
    "options": [{"id": o[0], "label": o[1], "keywords": [o[1]], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "빈칸은 conservation 쪽, 손보고 관리해서 오래 가게 하려는 상태예요. 이 상태를 바꿔 쓴 보기를 골라 봐요.",
        "정답이에요! 보전주의자는 변화를 인정하고 복원·수리해서, 지키고 싶은 바람직한(desired) 상태를 오래 가게 해요. 원래 그대로 두는 건 보존주의자 쪽이에요.",
        "정답은 ① desired(바람직한)예요. 보전주의자는 복원·관리해서 보고 쓰기 좋은, 바라는 상태를 오래 가게 해요.",
        {"2": "acknowledge change(변화를 인정)에서 떠올리기 쉽지만, 불안정한 상태를 일부러 오래 가게 하지는 않아요.",
         "3": "isolated(고립된)는 글에 없는 이야기예요. 다른 것과 떨어져 있다는 말은 나오지 않아요.",
         "4": "natural(자연 그대로의)은 손대지 않은 원래 상태(the original, “as found”) 쪽이에요. 그건 보존주의자 쪽 말이에요.",
         "5": "delicate(연약한)는 글에 없는 이야기예요. 보전주의자는 연약한 상태가 아니라 지키고 싶은 상태를 오래 가게 해요."},
        {"4": review(33,
                     "natural(자연 그대로의)은 손대지 않은 원래 상태 쪽 말이에요. 그건 보존주의자가 지키려는 것(the original, “as found”)이에요.\n"
                     "빈칸의 주어는 보전주의자예요. 변화를 인정하고 복원·수리해서, 보고 쓰기 좋은 상태를 오래 가게 해요.",
                     panel=rows(("빈칸 문장", "Conservationists acknowledge change", "보전주의자는 변화를 인정한다", "hl"),
                                ("3·7문장", "restorative · restore or repair", "복원·수리하는 쪽", "hl"),
                                ("6·7문장", "the original · “as found”", "원래 그대로 — 보존 쪽", "hl2")),
                     rank_word="가장 많이 고른"),
         "2": review(19,
                     "unstable(불안정한)은 acknowledge change(변화를 인정)에서 떠올리기 쉬워요. 하지만 빈칸은 prolong(더 오래 가게 하다)의 목적어예요.\n"
                     "일부러 오래 가게 하려는 상태라면 불안정한 상태가 아니라 지키고 싶은 좋은 상태예요.",
                     panel=rows(("빈칸 문장", "try to manage it", "변화를 관리하려 한다", "hl"),
                                ("빈칸 문장", "in order to prolong a(n) ____ state", "____ 상태를 더 오래 가게 하려고", "hl")))}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(3·4)과 6문장만 ──
EMPHASIS = {
    3: ["Conservationists", "distinguish", "restorative aspects"],
    4: ["acknowledge change", "manage", "prolong", "state"],
    6: ["criticize", "the original"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 31번 (빈칸 추론, 2점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 같은 말 모으기 → 빈칸이 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-preserve-conserve.svg", ("Preservation", "보존"), "vs", ("Conservation", "보전"),
                                       "오래된 악기, 그대로 둘까 고쳐 쓸까?", "2026년 6월 모의평가 31번 도입 칠판"),
                      "alt": "칠판: Preservation(보존) vs Conservation(보전)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "오래된 악기는 그대로 둬야 할까요, 고쳐서 써야 할까요? 이번 글은 보존(preservation)과 보전(conservation) 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 위치를 살펴보고 가면 좋아요. 빈칸은 글쓴이 의견과 동일할 수도 있고, 반대일 수도 있어요."}}],
    exam=exam,
    key_words={"passage": [g("Enlightenment", "계몽주의"), g("preservation", "보존"), g("conservation", "보전"), g("synonym", "동의어"),
                           g("maintain", "유지하다"), g("insofar as possible", "가능한 한"), g("protect A from B", "A를 B로부터 보호하다"),
                           g("distinguish A from B", "A를 B와 구별하다"), g("emphasize", "강조하다"), g("restorative", "복원적인"),
                           g("aspect", "측면"), g("musical instrument", "악기"), g("ecosystem", "생태계"), g("acknowledge", "인정하다"),
                           g("manage", "관리하다"), g("prolong", "연장하다"), g("nonetheless", "그럼에도 불구하고"),
                           g("protector", "보호자"), g("criticize A for B", "B라고 A를 비판하다"), g("priority", "우선순위"),
                           g("yield", "산출량"), g("harvest", "수확"), g("rather than", "~하기보다는"), g("interfere", "개입하다"),
                           g("minimally", "최소한으로"), g("preserve", "보존하다"), g("original", "원래의"), g("prefer", "선호하다"),
                           g("restore", "복원하다"), g("repair", "수리하다")],
               "options": [g("desired", "바람직한"), g("unstable", "불안정한"), g("isolated", "고립된"), g("delicate", "연약한")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함: present 현재의 · state 상태 · yield 산출량.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    2: [tip("present", "이 글에서는 → 현재의  ('선물' 아님)", "present", trap=True),
        tip("state", "이 글에서는 → 상태  ('주(州)·국가' 아님)", "state", trap=True)],
    6: [tip("yield", "이 글에서는 → 산출량  ('양보하다' 아님)", "yield", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법")
