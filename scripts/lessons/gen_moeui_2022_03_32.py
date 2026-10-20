"""2022년 3월 고3 32번 레슨 + 대사를 만든다 (빈칸 추론, 3점). 오답률 58.0% · Top 3.

    py scripts/lessons/gen_moeui_2022_03_32.py   (→ node scripts/policy_copy.mjs stamp <id> → npx vitest run)

틀: docs/tutor/templates/blank.md — 빈칸이 마지막 문장(2024년 3월 34번 꼴). 정답 ① must have taken place.
많이 고른 오답 ② was not reported at all 24% — 문장 1의 'the sources become fewer, the journeys less well known'에 끌린다.
하지만 페니키아인들은 돌아와 보고했고(reported) Herodotus가 기록했다. ③ 15% · ④ 12% · ⑤ 7%.
열쇠: It is this that ~(강조) — this = 앞 문장(당시 천문 과학으로는 그런 세부 사항을 꾸며 낼 수 없었다)
→ 보고한 '태양이 오른쪽에' 는 직접 본 것 → 여행은 실제로 있었다. Contemporary = 「현대의」가 아니라 「당시의」(뜻이 뒤집히는 함정).
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
fabricate·prosaic는 시험지 아래 *로 풀어 준 단어(핵심어·단어 체크에서 뺐다). 해설지 해석과 대조함.
규칙 반영: 2026-10-20 끊어읽기(slashes·roles·modifiers)까지, 초급 기본(add_basic) 넣음. Claude 초안 — 선생님 검토 전.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic,  # noqa: E402
                      topic_svg, base_lesson, exam_brief, review, finish)

ID = "moeui-2022-03-32-sun-on-right"

BLANK = "It is this that leads many of today’s historians to conclude that the journey ________."
S = [
    "When trying to understand the role of the sun in ancient journeys, the sources become fewer and the journeys less well known.",
    "Herodotus writes about an exploratory voyage commissioned by the ancient Egyptian King Necho II in about 600 BC.",
    "Necho II reportedly ordered a Phoenician expedition to sail clockwise around Africa, starting at the Red Sea and returning "
    "to the mouth of the Nile.",
    "They were gone for three years.",
    "Herodotus writes that the Phoenicians, upon returning from their heroic expedition, reported that after sailing south and "
    "then turning west, they found the sun was on their right, the opposite direction to where they were used to seeing it or "
    "expecting it to be.",
    "Contemporary astronomical science was simply not strong enough to fabricate such an accurate, fundamental and yet prosaic "
    "detail of where the sun would be after sailing past the equator and into the southern hemisphere.",
    BLANK,
]
KO = [
    "고대 여행에서 태양의 역할을 이해하려고 할 때, 자료는 더 적어지고 알려진 여행은 더 적어진다.",
    "Herodotus는 기원전 600년경 고대 이집트 왕 Necho 2세가 의뢰한 탐험 항해에 대해 기록한다.",
    "전해 오는 바에 따르면, Necho 2세는 페니키아 원정대에게 홍해에서 출발해 나일강 하구로 돌아오도록, 아프리카 주위를 시계 방향으로 항해하라고 명령했다고 한다.",
    "그들은 3년간 (원정을) 나가 있었다.",
    "Herodotus는 페니키아인들이 영웅적인 탐험을 마치고 돌아와, 남쪽으로 항해를 한 다음 서쪽으로 방향을 바꾼 후에 태양이 자신들이 늘 보았거나 "
    "떠 있으리라고 예상했던 곳과는 정반대 방향인 자신들의 오른편에 있는 것을 발견했노라고 보고했다고 기록한다.",
    "당시의 천문 과학은 적도를 지나 남반구로 항해한 후 태양이 어디에 있을지에 대해 그렇게 정확하고 기초적이지만 평범한 세부 사항을 꾸며 낼 만큼 결코 충분히 뛰어나지 않았다.",
    "오늘날의 역사가 중 많은 이들이 그 여행이 ________라고 결론을 내리게 되는 것이 바로 이 때문이다.",
]

SEEN = "왼쪽 · 그들이 본 것"
SCIENCE = "오른쪽 · 당시 과학"

B5 = [("the sun on their right", "태양이 오른쪽에"), ("the opposite direction", "늘 보던 곳과 정반대")]
B6 = B5 + [("accurate · prosaic detail", "정확하지만 평범한 세부 사항")]
SC6 = [("not strong enough to fabricate", "꾸며 낼 만큼 뛰어나지 않음")]


def board(seen, science=None, fresh=()):
    """칠판 — 왼쪽 그들이 보고한 것, 오른쪽 당시 과학(문장 6부터). 결론(빈칸)은 칠판에 쓰지 않는다"""
    return groups("보고한 것 ↔ 당시 과학", "그들이 본 것 (reported)", seen,
                  "당시 과학 (contemporary science)" if science is not None else None, science,
                  fresh=fresh, between="↔" if science is not None else None)


sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("When trying to understand", "이해하려고 할 때"), g("the role of the sun", "태양의 역할"),
                    g("in ancient journeys", "고대 여행에서"), g("the sources", "자료, 출처"), g("become", "~해지다"),
                    g("fewer", "더 적은"), g("the journeys", "그 여행들"), g("less well known", "덜 알려진"),
                    g("become fewer", "더 적어지다"),
                    g("It is this that", "~하는 것은 바로 이것이다"), g("leads", "이끌다, ~하게 하다"),
                    g("many of today’s historians", "오늘날 역사가 중 많은 이들"), g("to conclude", "결론 내리도록"),
                    g("conclude", "결론 내리다"), g("that the journey", "그 여행이 ~라고"), g("the journey", "그 여행")],
        "slashes": ["When trying to understand", "of the sun", "ancient journeys,", "become fewer"],
        "roles": [r("the sources", "S"), r("become", "V"), r("fewer", "C"), r("the journeys", "S"), r("less well known", "C")],
        "steps": [
            show("s1_passage", "빈칸은 마지막 문장, 맨 끝에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "바로 이것 때문에 오늘날 역사가들은 그 여행이 ____라고 결론 내린다", True),
                    ("o1", "오늘날 역사가들은 이것을 결론 내리지 못하고, 그 여행은 ____", False),
                    ("o2", "그 여행이 오늘날 역사가들을 ____로 이끌었다", False)],
                   "It is this that ~은 '~하는 것은 바로 이것이다'예요. lead + 사람 + to ~는 '사람이 ~하게 하다'예요.",
                   why="It is this that leads historians to conclude는 '역사가들이 결론 내리게 하는 것은 바로 이것'이에요. 무엇을 결론 내리는지가 that the journey ____예요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["this", "conclude", "________"], highlight_alt=["the journey"],
                   tips=[tip("It is A that ~", "'~하는 것은 바로 A다'예요. A를 강조하는 모양이에요.", "It is this that"),
                         tip("lead + 사람 + to ~", "'사람이 ~하게 하다'예요. leads historians to conclude = 역사가들이 결론 내리게 한다.", "leads")]),
            show("s1_where_map", "this가 가리키는 어떤 사실 때문에, 역사가들이 그 여행에 대해 결론을 내린대요.",
                 button="다음", before_read=True, levels=["중", "초"], display=BLANK, tag="빈칸 문장", method=0,
                 highlight=["this", "conclude"], highlight_alt=["the journey"], panel_below=True,
                 panel=rows(("this", "앞에 나온 어떤 사실", "바로 이것 때문에", "hl"),
                            ("결론", "the journey ________", "그 여행이 ____라고", "hl2"))),
            show("s1_where", "그럼 '이것'이 무엇인지, 역사가들이 그 여행을 어떻게 봤을지 생각하며 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
            sv("s1_sv", ["When trying to understand", "the sources", "become", "fewer", "the journeys", "less well known"],
               {"the sources": "S", "become": "V", "fewer": "C", "the journeys": "S", "less well known": "C"},
               {"When trying to understand": "그건 When(~할 때) 덩어리예요. 콤마 뒤에서 찾아봐요."},
               "주어는 the sources, 동사는 become, 보어는 fewer예요. and 뒤는 주어 the journeys, 보어 less well known이고, 같은 동사 become은 빠졌어요.",
               ask="콤마 뒤에서 주어(S), 동사(V), 보어(C)를 모두 찾아볼까요?"),
            show("s1_note", "고대 여행에서 태양의 역할을 알아보려 하면, 자료도 적고 알려진 여행도 적대요.",
                 highlight=["fewer", "less well known"], button="다음 문장",
                 tips=[tip("and 뒤 생략", "and 뒤 the journeys (become) less well known — 앞과 같은 동사 become이 빠졌어요.", "less well known")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("Herodotus", "헤로도토스 · 고대 그리스의 역사가"), g("writes about", "~에 대해 쓰다"),
                    g("an exploratory voyage", "탐험 항해"), g("exploratory", "탐험의"), g("voyage", "항해"),
                    g("commissioned by", "~가 의뢰한"), g("commissioned", "의뢰된, 맡겨진"),
                    g("the ancient Egyptian King Necho II", "고대 이집트 왕 네코 2세"), g("in about 600 BC", "기원전 600년경")],
        "slashes": ["exploratory voyage", "King Necho II"],
        "roles": [r("Herodotus", "S"), r("writes about", "V"), r("an exploratory voyage", "O")],
        "modifiers": ["commissioned by the ancient Egyptian King Necho II"],
        "steps": [
            show("s2_note", "헤로도토스가 이집트 왕 네코 2세가 맡긴 탐험 항해를 기록했대요.",
                 highlight=["writes about", "exploratory voyage"], button="다음 문장",
                 tips=[tip("명사 + p.p. by ~", "voyage commissioned by ~ = ~가 의뢰한 항해예요. 과거분사가 앞 명사를 꾸며요.", "commissioned")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("Necho II", "네코 2세"), g("reportedly", "전해 오는 바에 따르면"), g("ordered", "명령했다"),
                    g("a Phoenician expedition", "페니키아 원정대"), g("Phoenician", "페니키아(사람)의"), g("expedition", "탐험(여행), 원정대"),
                    g("to sail clockwise around Africa", "아프리카 주위를 시계 방향으로 항해하라고"), g("clockwise", "시계 방향으로"),
                    g("starting at the Red Sea", "홍해에서 출발해"), g("the Red Sea", "홍해"),
                    g("returning to the mouth of the Nile", "나일강 하구로 돌아오도록"), g("mouth", "(강의) 어귀, 하구"),
                    g("to sail around Africa", "아프리카를 돌아 항해하라고")],
        "slashes": ["a Phoenician expedition", "around Africa,", "the Red Sea"],
        "roles": [r("Necho II", "S"), r("ordered", "V"), r("a Phoenician expedition", "O"), r("to sail clockwise around Africa", "C")],
        "steps": [
            sv("s3_sv", ["Necho II", "reportedly", "ordered", "a Phoenician expedition", "to sail clockwise around Africa", "the Red Sea"],
               {"Necho II": "S", "ordered": "V", "a Phoenician expedition": "O", "to sail clockwise around Africa": "C"},
               {"reportedly": "그건 '전해 오는 바에 따르면'이라는 말이에요. 주어·동사가 아니에요.",
                "the Red Sea": "그건 starting at(~에서 출발해) 뒤, 출발한 곳이에요."},
               "주어는 Necho II, 동사는 ordered, 목적어는 a Phoenician expedition, 보어는 to sail clockwise around Africa예요.",
               ask="주어(S), 동사(V), 목적어(O), 보어(C)를 찾아볼까요?"),
            show("s3_how", "order + 사람 + to ~는 '사람에게 ~하라고 명령하다'로 읽어요. 원정대에게 아프리카를 돌라고 명령한 거예요.",
                 levels=["중", "초"], highlight=["ordered"], highlight_alt=["to sail clockwise around Africa"],
                 tips=[tip("동사 + 사람 + to ~", "order/ask/tell + 사람 + to ~ = 사람에게 ~하라고 명령하다/부탁하다/말하다.", "ordered")]),
            choice("s3_report",
                   "여기서 reportedly는 무슨 뜻일까요?",
                   [("o0", "확실히, 틀림없이", False), ("o1", "전해 오는 바에 따르면", True), ("o2", "몰래, 비밀리에", False)],
                   "report(보고하다, 전하다)에 -ly가 붙었어요. 누군가 그렇게 전했다는 말이에요.",
                   why="reportedly는 누군가 그렇게 전했다는 말이에요. 확인된 사실이 아니라 그렇게 전해진다는 말이라서, 이 기록이 진짜인지가 이 글의 물음이에요.",
                   highlight=["reportedly"],
                   tips=[tip("reportedly", "'전해 오는 바에 따르면'이에요. 사실인지 아직 확실하지 않다는 느낌이 있어요.", "reportedly")]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "low",
        "glosses": [g("They", "그들(페니키아 원정대)"), g("were gone", "떠나 있었다"), g("for three years", "3년 동안"),
                    g("three years", "3년")],
        "roles": [r("They", "S"), r("were gone", "V")],
        "steps": [
            show("s4_note", "They는 앞 문장의 원정대예요. 3년 동안 떠나 있었대요.", highlight=["They"], button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Herodotus", "헤로도토스"), g("writes", "쓰다, 기록하다"), g("the Phoenicians", "페니키아인들"),
                    g("upon returning from their heroic expedition", "영웅적인 탐험에서 돌아오자마자"), g("heroic", "영웅적인"),
                    g("reported", "보고했다"), g("after sailing south", "남쪽으로 항해한 뒤"), g("then turning west", "그다음 서쪽으로 돌고 나서"),
                    g("they found", "그들은 알게 되었다"), g("the sun", "태양"), g("was on their right", "그들의 오른쪽에 있었다"),
                    g("on their right", "그들의 오른쪽에"), g("the opposite direction", "정반대 방향"),
                    g("to where they were used to seeing it", "그들이 늘 그것(태양)을 보던 곳과"),
                    g("were used to", "~하는 데 익숙했다"), g("or expecting it to be", "또는 있으리라 예상하던 (곳과)")],
        "slashes": ["Herodotus writes", "that the Phoenicians,", "heroic expedition,", "reported", "turning west,", "on their right,",
                    "the opposite direction", "seeing it"],
        "roles": [r("Herodotus", "S"), r("writes", "V"), r("the Phoenicians", "S"), r("reported", "V"), r("they", "S"), r("found", "V"),
                  r("the sun", "S"), r("was", "V")],
        "modifiers": ["where they were used to seeing it or expecting it to be"],
        "steps": [
            sv("s5_sv", ["Herodotus", "writes", "the Phoenicians", "reported", "the sun"],
               {"Herodotus": "S", "writes": "V", "the Phoenicians": "S", "reported": "V"},
               {"the sun": "그건 reported that 뒤, 보고한 내용 안의 주어예요."},
               "주어 Herodotus, 동사 writes — 무엇을 썼는지가 that 뒤예요. 그 안의 주어는 the Phoenicians, 동사는 reported예요.",
               ask="writes that 앞뒤로 주어(S)·동사(V)가 두 쌍 있어요. 모두 찾아볼까요?",
               faded=["upon returning from their heroic expedition"]),
            choice("s5_found",
                   "페니키아인들은 무엇을 보고했대요?",
                   [("o0", "남쪽으로 갔다가 서쪽으로 돌자, 태양이 늘 보던 곳과 정반대인 오른쪽에 있었다", True),
                    ("o1", "항해 내내 태양이 늘 보던 자리에 그대로 있었다", False),
                    ("o2", "남쪽 바다에서는 태양을 전혀 볼 수 없었다", False)],
                   "they found the sun was on their right를 봐요. the opposite direction은 '정반대 방향'이에요.",
                   why="'they found the sun was on their right, the opposite direction', 태양이 오른쪽, 늘 보던 곳과 정반대 방향에 있었대요.",
                   highlight=["on their right", "the opposite direction"],
                   tips=[tip("be used to -ing", "'~하는 데 익숙하다'예요. were used to seeing it = 늘 그것을 보던.", "were used to")]),
            show("s5_board", "그들이 본 건 늘 보던 것과 정반대였어요. 칠판에 넣어 둘게요.",
                 panel=board(B5, fresh=("the sun on their right", "the opposite direction")), button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Contemporary astronomical science", "당시의 천문 과학"), g("Contemporary", "동시대의 · 여기서는 '그 당시의'"),
                    g("astronomical", "천문학의"), g("was", "~였다"), g("simply", "결코, 전혀 (not 강조)"),
                    g("not strong enough", "충분히 뛰어나지 않은"), g("strong", "강한 · 여기서는 '뛰어난'"),
                    g("to fabricate", "꾸며 낼"), g("fabricate", "꾸며 내다, 만들어 내다"),
                    g("such an accurate, fundamental and yet prosaic detail", "그렇게 정확하고 기초적이지만 평범한 세부 사항"),
                    g("accurate", "정확한"), g("fundamental", "기초적인"), g("prosaic", "평범한"), g("detail", "세부 사항"),
                    g("of where the sun would be", "태양이 어디에 있을지에 대한"), g("after sailing past the equator", "적도를 지나 항해한 뒤"),
                    g("equator", "적도"), g("into the southern hemisphere", "남반구로"), g("southern hemisphere", "남반구"),
                    g("such a detail", "그런 세부 사항")],
        "slashes": ["astronomical science", "not strong enough", "to fabricate", "prosaic detail", "the sun would be", "past the equator"],
        "roles": [r("Contemporary astronomical science", "S"), r("was", "V"), r("not strong enough", "C")],
        "steps": [
            sv("s6_sv", ["Contemporary astronomical science", "was", "not strong enough",
                         "such an accurate, fundamental and yet prosaic detail", "the sun"],
               {"Contemporary astronomical science": "S", "was": "V", "not strong enough": "C"},
               {"such an accurate, fundamental and yet prosaic detail": "그건 to fabricate(꾸며 낼) 뒤의 목적어예요. 문장 전체의 주어·보어가 아니에요.",
                "the sun": "그건 where 뒤 덩어리 안의 주어예요."},
               "주어는 Contemporary astronomical science, 동사는 was, 보어는 not strong enough예요.",
               ask="주어(S), 동사(V), 보어(C)를 찾아볼까요?"),
            choice("s6_meaning",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "현대 천문학은 그 세부 사항을 꾸며 낼 만큼 뛰어나다", False),
                    ("o1", "그 시대 천문학은 그렇게 정확한 세부 사항을 꾸며 낼 만큼 뛰어나지 않았다", True),
                    ("o2", "그 시대 천문학은 남반구에서 태양이 어디 있을지 정확히 알았다", False)],
                   "Contemporary는 여기서 '현대의'가 아니라 '그 당시의'예요. not 형용사 enough to ~는 '~할 만큼 …하지 않다'예요.",
                   why="Contemporary astronomical science는 '당시의 천문 과학'이에요. 그때 과학은 이런 정확한 세부 사항을 꾸며 낼 만큼 뛰어나지 않았대요.",
                   highlight=["Contemporary", "not strong enough", "fabricate"],
                   tips=[tip("contemporary", "'현대의'로 많이 알지만, 옛날 이야기 속에서는 '그 당시의, 동시대의'예요.", "Contemporary"),
                         tip("not 형용사 enough to ~", "'~할 만큼 충분히 …하지 않다'예요. not strong enough to fabricate = 꾸며 낼 만큼 뛰어나지 않다.", "enough")]),
            choice("s6_so",
                   "그때 과학으로 꾸며 낼 수 없었다면, 페니키아인들의 보고는 어떻게 나온 걸까요?",
                   [("o0", "그때 과학책을 보고 지어냈다", False), ("o1", "직접 가서 보고 겪었다", True),
                    ("o2", "헤로도토스가 대신 지어냈다", False)],
                   "당시엔 누구도 이런 세부 사항을 머리로 지어낼 수 없었어요. 그럼 어디서 알았을지 생각해 봐요.",
                   why="당시 과학으로는 '남반구에서 태양이 오른쪽에 있다'를 지어낼 수 없었어요. 그러니 그들이 실제로 가서 본 거예요.",
                   panel=board(B6, SC6)),
            show("s6_board", "그들이 본 것은 당시 과학으로는 꾸며 낼 수 없는 것이었어요. 칠판에 정리해 둘게요.",
                 panel=board(B6, SC6, fresh=("accurate · prosaic detail", "not strong enough to fabricate")), button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": BLANK, "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("It is this that", "~하는 것은 바로 이것이다"), g("leads", "이끌다, ~하게 하다"),
                    g("many of today’s historians", "오늘날 역사가 중 많은 이들"), g("to conclude", "결론 내리도록"),
                    g("conclude", "결론 내리다"), g("that the journey", "그 여행이 ~라고"), g("the journey", "그 여행")],
        "slashes": ["It is this", "today’s historians", "to conclude"],
        "roles": [r("this", "S"), r("leads", "V"), r("many of today’s historians", "O"), r("to conclude", "C")],
        "steps": [
            choice("s7_this",
                   "It is this that ~의 this는 무엇을 가리킬까요?",
                   [("o0", "자료가 적고 알려진 여행이 적다는 것", False),
                    ("o1", "당시 과학으로는 그런 세부 사항을 꾸며 낼 수 없었다는 것", True),
                    ("o2", "원정대가 3년 동안 떠나 있었다는 것", False)],
                   "this는 바로 앞 문장을 가리키는 경우가 많아요. 칠판 오른쪽을 떠올려 봐요.",
                   why="this는 바로 앞 문장이에요. 당시 천문 과학은 태양 위치 같은 세부 사항을 지어낼 만큼 뛰어나지 않았다는 사실이에요.",
                   highlight=["this"], panel=board(B6, SC6),
                   tips=[tip("It is A that ~", "'~하는 것은 바로 A다'예요. It is this that = 바로 이것이 ~하게 한다.", "It is this that")]),
            choice("s7_fill",
                   "그럼 역사가들은 그 여행이 어땠다고 결론 내렸을까요?",
                   [("o0", "실제로 있었다", True), ("o1", "기록이 남지 않았다", False), ("o2", "중간에 멈췄다", False)],
                   "결론의 근거는 '당시엔 꾸며 낼 수 없었다'는 사실이에요. 꾸며 낸 게 아니라면 어떻게 된 걸지 생각해 봐요.",
                   why="꾸며 낼 수 없는 세부 사항을 보고했으니, 정말 아프리카를 돌며 직접 봤다는 뜻이에요. 그래서 여행은 진짜였다고 결론 내려요.",
                   panel=board(B6, SC6), highlight=["conclude", "the journey"]),
            choice("s7_side",
                   "빈칸은 '페니키아인들의 보고는 진짜다'와 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 (보고는 진짜다)", True), ("o1", "반대 쪽 (보고는 꾸며 낸 것이다)", False)],
                   "this(당시엔 꾸며 낼 수 없었다)가 이 결론을 이끌었어요(leads).",
                   why="꾸며 낼 수 없었다는 사실(this)이 결론을 이끌어요. 그러니 빈칸은 보고가 진짜라는 쪽이에요.",
                   highlight=["this", "leads"], point="this(당시엔 꾸며 낼 수 없었다) → 결론 = 보고는 진짜, 여행은 실제로 있었다 = 같은 쪽"),
            show("s7_go", "빈칸은 '그 여행은 정말 있었다'는 쪽이에요. 이 말을 바꿔 쓴 보기를 찾아봐요.", button="문제 풀러 갈게요"),
        ],
    },
]

# 초급 기본 — 문장마다 하나 (빈칸 문장 제외)
add_basic(sentences, 1, [m("the role of the sun", "태양의 역할"), "을 ", m("When trying to understand", "이해하려고 할 때"), ", ",
                         m("the sources", "자료가"), " ", m("become fewer", "더 적어진다"), "."],
          match_display="When trying to understand the role of the sun, the sources become fewer.",
          sv_id="s1_sv", meaning_ids=["s1_note"])
add_basic(sentences, 2, [m("Herodotus", "헤로도토스는"), " ", m("an exploratory voyage", "탐험 항해"), "에 ", m("writes about", "대해 쓴다"), "."],
          match_display="Herodotus writes about an exploratory voyage.",
          sv_new=sv_step("s2_basic_sv", ["Herodotus", "writes about", "an exploratory voyage", "the ancient Egyptian King Necho II"],
                         {"Herodotus": "S", "writes about": "V", "an exploratory voyage": "전목"},
                         {"the ancient Egyptian King Necho II": "그건 commissioned by(~가 의뢰한) 뒤의 말이에요."},
                         "주어는 Herodotus, 동사는 writes about, about 뒤 목적어는 an exploratory voyage예요."),
          meaning_ids=["s2_note"])
add_basic(sentences, 3, [m("Necho II", "네코 2세는"), " ", m("reportedly", "전해 오는 바로는"), " ", m("a Phoenician expedition", "페니키아 원정대"),
                         "에게 ", m("to sail around Africa", "아프리카를 돌아 항해하라고"), " ", m("ordered", "명령했다"), "."],
          match_display="Necho II reportedly ordered a Phoenician expedition to sail around Africa.",
          sv_id="s3_sv", meaning_ids=["s3_how"])
add_basic(sentences, 4, [m("They", "그들은"), " ", m("for three years", "3년 동안"), " ", m("were gone", "떠나 있었다"), "."],
          sv_new=sv_step("s4_basic_sv", ["They", "were gone", "three years"], {"They": "S", "were gone": "V"},
                         {"three years": "그건 for(~ 동안) 뒤의 말이에요."},
                         "주어는 They(원정대), 동사는 were gone이에요."),
          meaning_ids=["s4_note"])
add_basic(sentences, 5, [m("Herodotus", "헤로도토스는"), " — ", m("the Phoenicians", "페니키아인들이"), " ", m("the sun", "태양이"), " ",
                         m("was on their right", "오른쪽에 있었다"), "고 ", m("reported", "보고했다"), "고 ", m("writes", "쓴다"), "."],
          match_display="Herodotus writes that the Phoenicians reported that the sun was on their right.",
          sv_id="s5_sv", meaning_ids=["s5_found"])
add_basic(sentences, 6, [m("Contemporary astronomical science", "당시의 천문 과학은"), " ", m("such a detail", "그런 세부 사항"), "을 ",
                         m("to fabricate", "꾸며 낼"), " 만큼 ", m("not strong enough", "충분히 뛰어나지 않았다"), "."],
          match_display="Contemporary astronomical science was not strong enough to fabricate such a detail.",
          sv_id="s6_sv", meaning_ids=["s6_meaning"])

SENSES = {
    1: [sense("to", "trying to understand", "~하려고", "try + to부정사 = ~하려고 애쓰다")],
    3: [sense("to", "to sail", "~하라고", "order + 사람 + to부정사 = 사람에게 ~하라고 명령하다"),
        sense("to", "returning to the mouth", "~로", "전치사 to (방향)")],
    4: [sense("for", "for three years", "~ 동안", "전치사 for + 기간")],
    5: [sense("that", "writes that", "~라고", "명사절 that (write that …)"),
        sense("that", "reported that", "~라고", "명사절 that (report that …)"),
        sense("to", "direction to where", "~와 (반대인)", "the opposite direction to ~ = ~와 정반대 방향"),
        sense("to", "used to seeing", "~하는 데 (익숙한)", "be used to + -ing = ~하는 데 익숙하다"),
        sense("to", "expecting it to be", "~하기를, ~할 것이라고", "expect + 목적어 + to부정사")],
    6: [sense("to", "to fabricate", "~할 (만큼)", "형용사 + enough + to부정사 = ~할 만큼 충분히 …한"),
        sense("yet", "and yet prosaic", "그러면서도, 그런데도", "and yet = 그렇지만 (대조를 잇는 말)")],
    7: [sense("that", "It is this that", "(강조 — 바로 ~가)", "It is A that ~ 강조 구문"),
        sense("to", "to conclude", "~하도록", "lead + 사람 + to부정사 = 사람이 ~하게 하다"),
        sense("that", "conclude that", "~라고", "명사절 that (conclude that …)")],
}

WORDS = {"trying": "애쓰는, ~하려는", "understand": "이해하다", "role": "역할", "sun": "태양", "ancient": "고대의", "journeys": "여행들",
         "sources": "자료, 출처", "fewer": "더 적은", "journey": "여행", "less": "덜", "well": "잘", "known": "알려진",
         "herodotus": "헤로도토스", "writes": "쓰다", "exploratory": "탐험의", "voyage": "항해", "commissioned": "의뢰된",
         "egyptian": "이집트의", "king": "왕", "necho": "네코 (이집트 왕 이름)", "ii": "2세", "600": "600", "bc": "기원전",
         "reportedly": "전해 오는 바에 따르면", "ordered": "명령했다", "phoenician": "페니키아의", "expedition": "탐험, 원정대",
         "sail": "항해하다", "clockwise": "시계 방향으로", "around": "~ 주위를", "africa": "아프리카", "starting": "출발하는",
         "red": "붉은", "sea": "바다", "returning": "돌아오는", "mouth": "어귀, 하구", "nile": "나일강", "three": "3, 셋의",
         "years": "해, 년", "gone": "떠나 있는", "phoenicians": "페니키아인들", "heroic": "영웅적인", "reported": "보고했다",
         "sailing": "항해하는 것", "south": "남쪽으로", "turning": "방향을 바꾸는 것", "west": "서쪽으로", "found": "알게 되었다",
         "right": "오른쪽", "opposite": "정반대의", "direction": "방향", "used": "be used to -ing = ~하는 데 익숙하다",
         "seeing": "보는 것", "expecting": "예상하는 것", "contemporary": "그 당시의, 동시대의", "astronomical": "천문학의",
         "science": "과학", "simply": "결코 (not 강조)", "strong": "뛰어난", "enough": "충분히", "fabricate": "꾸며 내다",
         "accurate": "정확한", "fundamental": "기초적인", "prosaic": "평범한", "detail": "세부 사항", "past": "~을 지나",
         "equator": "적도", "southern": "남쪽의", "hemisphere": "반구", "leads": "이끌다", "today’s": "오늘날의",
         "historians": "역사가들", "conclude": "결론 내리다", "many": "많은 사람", "role.": "역할", "it": "그것(태양)",
         "be": "있다", "would": "~일 것이다", "their": "그들의", "they": "그들", "then": "그다음", "upon": "~하자마자"}

STORIES = [
    (2, [sc("문장 1", "📜", "sources become fewer", "고대 여행 속 태양 이야기는 자료가 적어요"),
         sc("문장 2", "✍️", "Herodotus writes", "헤로도토스가 네코 2세가 맡긴 탐험 항해를 기록했어요")]),
    (4, [sc("문장 3~4", "⛵", "sail clockwise around Africa", "원정대가 아프리카를 시계 방향으로 돌아 3년 만에 돌아왔대요 (reportedly)")]),
    (6, [sc("문장 5", "☀️", "the sun on their right", "돌아와서, 태양이 늘 보던 곳과 정반대인 오른쪽에 있었다고 보고했어요"),
         sc("문장 6", "🔭", "not strong enough to fabricate", "당시 과학으로는 이런 세부 사항을 꾸며 낼 수 없었어요")]),
]

OPTIONS = [
    ("1", "must have taken place", ["must have taken place"], "일어났음이 틀림없다", True),
    ("2", "was not reported at all", ["not reported"], "전혀 보고되지 않았다", False),
    ("3", "was not worth the time", ["not worth"], "시간을 들일 가치가 없었다", False),
    ("4", "should have been planned better", ["planned better"], "더 잘 계획되었어야 했다", False),
    ("5", "could be stopped at any moment", ["stopped"], "언제고 중단될 수 있었다", False),
]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오. [3점]",
    "underline": "________", "sentence": 7, "analysis_first": True, "wrong_rate": 58.0, "wrong_rank": 3,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("must have taken place", "일어났음이 틀림없다"), g("take place", "일어나다"), g("reported", "보고된"),
                g("at all", "전혀"), g("worth the time", "시간을 들일 가치가 있는"), g("should have been planned", "계획되었어야 했다"),
                g("at any moment", "언제든지")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "this(당시엔 꾸며 낼 수 없었다)가 이끄는 결론을 떠올리며 골라 봐요.",
        "정답이에요! 당시 과학으로는 '태양이 오른쪽에 있다'는 걸 꾸며 낼 수 없었어요. 그러니 직접 가서 본 것이고, 여행은 실제로 일어났음이 틀림없어요.",
        "정답은 ① must have taken place예요. must have p.p.는 '~했음이 틀림없다'예요. 꾸며 낼 수 없는 사실을 보고했으니 여행은 정말 있었어요.",
        {"2": "페니키아인들은 돌아와서 보고했고(reported), 헤로도토스가 그걸 기록했어요. 보고되지 않았다면 이 이야기 자체가 없어요.",
         "3": "여행이 시간을 들일 만했는지는 글에 나오지 않아요. 글은 이 기록이 진짜인지를 말해요.",
         "4": "계획을 더 잘했어야 했다는 이야기는 없어요. 꾸며 낼 수 없는 세부 사항 때문에 내린 결론이에요.",
         "5": "언제든 멈출 수 있었다는 말은 글에 없어요. 원정대는 3년 동안 아프리카를 돌고 돌아왔어요."},
        {"2": review(24,
                     "문장 1의 '자료가 적고 덜 알려졌다'를 보고 '보고되지 않았다'를 고르기 쉬워요. 하지만 페니키아인들은 돌아와서 보고했고(reported), 헤로도토스가 그걸 기록했어요. 빈칸은 this(당시엔 꾸며 낼 수 없었다) 때문에 내린 결론이라, 여행이 정말 있었다는 쪽이에요.",
                     "그래서 ②가 아니에요. 어디서 헷갈렸어요?",
                     [("문장 1을 보고 골랐어요", ["first_sentence_trap"],
                       "알려 줘서 고마워요. 빈칸은 바로 앞의 this가 이끄는 결론이에요. 앞으로 빈칸 바로 앞 문장을 먼저 짚어 줄게요."),
                      ("this가 무엇인지 몰랐어요", ["reference"],
                       "알려 줘서 고마워요. It is this that ~의 this는 앞 문장, 당시 과학으로는 꾸며 낼 수 없었다는 사실이에요. 앞으로 가리키는 말을 먼저 짚어 줄게요."),
                      ("둘 다요", ["first_sentence_trap", "reference"],
                       "알려 줘서 고마워요. 앞으로 this가 가리키는 앞 문장과 빈칸의 관계를 같이 짚어 줄게요.")],
                     panel=rows(("this", "not strong enough to fabricate", "당시엔 꾸며 낼 수 없었다", "hl"),
                                ("그래서", "the journey ________", "여행은 정말 있었다", "hl2")))}),
}

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 32번 (빈칸 추론, 3점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 근거 모으기 → 빈칸이 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-sun-on-right.svg", ("Ancient voyage", "옛 항해 기록"), "?", ("Sun on the right", "오른쪽에 뜬 해"),
                                       "이 기록은 진짜였을까?", "2022년 3월 32번 도입 칠판"),
                      "alt": "칠판: Ancient voyage(옛 항해 기록) ? Sun on the right(오른쪽에 뜬 해)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "2600년 전 아프리카를 한 바퀴 돌았다는 항해 기록이 있어요. 이 기록이 진짜인지 어떻게 알 수 있을까요?"}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("source", "자료, 출처"), g("exploratory", "탐험의"), g("voyage", "항해"), g("commission", "의뢰하다"),
                           g("reportedly", "전해 오는 바에 따르면"), g("expedition", "탐험, 원정대"), g("clockwise", "시계 방향으로"),
                           g("heroic", "영웅적인"), g("opposite", "정반대의"), g("be used to -ing", "~하는 데 익숙하다"),
                           g("contemporary", "당시의, 동시대의"), g("astronomical", "천문학의"), g("accurate", "정확한"),
                           g("fundamental", "기초적인"), g("equator", "적도"), g("southern hemisphere", "남반구"),
                           g("conclude", "결론 내리다")],
               "options": [g("take place", "일어나다"), g("worth", "~할 가치가 있는"), g("at any moment", "언제든지")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법",
       chunks={"When trying to understand": "이해하려고 할 때", "the sources": "자료", "become": "~해지다", "fewer": "더 적은",
               "the journeys": "그 여행들", "less well known": "덜 알려진", "Herodotus": "헤로도토스", "writes about": "~에 대해 쓰다",
               "an exploratory voyage": "탐험 항해", "the ancient Egyptian King Necho II": "고대 이집트 왕 네코 2세",
               "Necho II": "네코 2세", "reportedly": "전해 오는 바에 따르면", "ordered": "명령했다",
               "a Phoenician expedition": "페니키아 원정대", "to sail clockwise around Africa": "아프리카 주위를 시계 방향으로 항해하라고",
               "the Red Sea": "홍해", "They": "그들", "were gone": "떠나 있었다", "three years": "3년", "writes": "쓰다",
               "the Phoenicians": "페니키아인들", "reported": "보고했다", "the sun": "태양",
               "Contemporary astronomical science": "당시의 천문 과학", "was": "~였다", "not strong enough": "충분히 뛰어나지 않은",
               "such an accurate, fundamental and yet prosaic detail": "그렇게 정확하고 기초적이지만 평범한 세부 사항",
               "the role of the sun": "태양의 역할", "become fewer": "더 적어지다", "to sail around Africa": "아프리카를 돌아 항해하라고",
               "for three years": "3년 동안", "was on their right": "그들의 오른쪽에 있었다", "to fabricate": "꾸며 낼",
               "such a detail": "그런 세부 사항"})
