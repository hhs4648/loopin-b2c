"""2024년 3월 고3 32번 레슨 + 대사를 만든다 (빈칸 추론, 2점). 오답률 66.3% · Top 5.

    python3 scripts/lessons/gen_moeui_2024_03_32.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md (빈칸이 가운데). 정답 ① had absolutely no choice but to act as they did.
많이 고른 오답 ⑤ 23.9%(위험한 상황엔 도덕적 의무가 안 맞는다 — 글과 반대: 의무를 다했을 뿐이라 한다), ④ 16.5%(감사를 받을 만했다 — 칭찬을 부인한다).
열쇠: 상식(우리는 스스로 결정할 권리) ↔ Yet 이타주의자들은 just the opposite → 빈칸 = '스스로 고른 게 아니다, 어쩔 수 없었다'.
빈칸 뒤 재진술: 칭찬받을 일이 아니다 · 누구라도 똑같이 했을 것 · 기대되는 만큼만 했다. 해설지 해석과 대조함.
altruistic, lest, shirk는 시험지 아래 *로 풀어 준 단어(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)

ID = "moeui-2024-03-32-altruists-no-choice"

BLANK = "They insist that they ________."
S = [
    "The commonsense understanding of the moral status of altruistic acts conforms to how most of us think about our responsibilities toward others.",
    "We tend to get offended when someone else or society determines for us how much of what we have should be given away; "
    "we are adults and should have the right to make such decisions for ourselves.",
    "Yet, when interviewed, altruists known for making the largest sacrifices—and bringing about the greatest benefits to their "
    "recipients—assert just the opposite.",
    BLANK,
    "Organ donors, and everyday citizens who risk their own lives to save others in mortal danger are remarkably consistent in their "
    "explicit denials that they have done anything deserving of high praise as well as in their assurance that anyone in their shoes "
    "should have done exactly the same thing.",
    "To be sure, it seems that the more altruistic someone is, the more they are likely to insist that they have done no more than "
    "all of us would be expected to do, lest we shirk our basic moral obligation to humanity.",
]
KO = [
    "이타적인 행위의 도덕적 상태에 대한 상식적인 이해는 우리 대부분이 다른 사람들을 향한 우리의 책임에 대해 어떻게 생각하는지에 따른다.",
    "우리는 다른 누군가 또는 사회가 우리를 대신하여 우리가 가진 것의 얼마만큼을 나누어줘야 하는지를 결정하면 그것을 불쾌하게 여기는 경향이 있다. 우리는 성인이고 스스로 그러한 결정을 내릴 권리가 있어야 한다.",
    "하지만, 인터뷰를 하면, 가장 큰 희생을 하고, 그들의 수혜자에게 가장 큰 이익을 가져다주는 것으로 알려진 이타주의자들은 정반대의 주장을 한다.",
    "그들은 자신들이 ________라고 주장한다.",
    "치명적인 위험에 처한 다른 사람들을 구하기 위해 자기 자신의 목숨을 거는 장기 기증자들과 평범한 시민들은 자신의 입장에 처한 사람이라면 누구나 정확하게 똑같은 것을 했을 것이라는 그들의 확신에서뿐만 아니라 자신이 찬사를 받을 만한 어떤 일을 했다는 것에 대한 그들의 명백한 부인에서도 놀랍게 일관된다.",
    "확실히, 누군가가 더 이타적일수록, 그들은 우리가 인류에 대한 우리의 기본적인 도덕적 의무를 회피하지 않도록, 우리 모두가 할 것으로 기대되는 만큼만 했을 뿐이라고 주장할 가능성이 더 높아 보인다.",
]

US = "왼쪽 · 보통 사람들 생각"
ALT = "오른쪽 · 이타주의자들의 말"


def board(left, right, fresh=(), sort=None):
    return groups("두 생각", "보통 사람들 (상식)", left, "이타주의자들", right, fresh=fresh, between="↔",
                  sort={"words": sort, "left": US, "right": ALT} if sort else None)


L2 = [("decide for ourselves", "스스로 결정"), ("the right", "권리")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("The commonsense understanding", "상식적인 이해"), g("the moral status", "도덕적 지위"),
                    g("altruistic acts", "이타적인 행동"), g("conforms to", "~에 따르다, ~와 일치하다"),
                    g("how most of us think", "우리 대부분이 생각하는 방식"), g("our responsibilities", "우리의 책임"),
                    g("toward others", "다른 사람들에 대한"), g("They", "그들"), g("insist", "주장하다")],
        "slashes": ["The commonsense understanding", "altruistic acts", "conforms to", "most of us think"],
        "roles": [r("The commonsense understanding", "S"), r("conforms to", "V"), r("most of us", "S"), r("think", "V")],
        "steps": [
            show("s1_passage", "빈칸은 여기, 넷째 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            show("s1_where",
                 "빈칸 문장은 짧아요. They(그들)가 누구이고 무엇을 주장(insist)하는지가 빈칸이에요. 그걸 생각하며 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                 highlight=["They", "insist", "________"],
                 tips=[tip("빈칸 문제 요령", "빈칸이 어디 있는지, 무엇을 묻는 문장인지 먼저 확인하고 처음부터 읽어요. 빈칸에는 글쓴이 주장과 같은 말이 올 때도, 반대 의견이 올 때도 있어요.")]),
            sv("s1_sv", ["The commonsense understanding", "the moral status", "altruistic acts", "conforms to", "our responsibilities"],
               {"The commonsense understanding": "S", "conforms to": "V"},
               {"the moral status": "그건 of 뒤 덩어리예요. 앞의 understanding을 꾸며요.",
                "altruistic acts": "그건 of 뒤 덩어리예요. 전치사 뒤라 주어가 아니에요.",
                "our responsibilities": "그건 about 뒤 덩어리예요."},
               "주어는 The commonsense understanding, 동사는 conforms to(~에 따르다)예요."),
            choice("s1_mean",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "이타적 행동은 상식과 정반대다", False),
                    ("o1", "이타적 행동을 보는 상식은 우리가 남에 대한 책임을 생각하는 방식과 같다", True),
                    ("o2", "책임감이 강한 사람만 이타적이다", False)],
                   "conforms to는 '~에 따르다, ~와 일치하다'예요. to 뒤 'how most of us think'를 봐요.",
                   why="'conforms to how most of us think about our responsibilities'는 우리 대부분이 책임에 대해 생각하는 방식과 일치한다는 말이에요.",
                   highlight=["commonsense", "conforms to", "how most of us think"],
                   tips=[tip("conform to", "'~에 따르다, ~와 일치하다'예요.", "conforms to")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("We tend to", "우리는 ~하는 경향이 있다"), g("get offended", "기분이 상하다"), g("when", "~할 때"),
                    g("someone else or society", "다른 누군가나 사회"), g("determines for us", "우리 대신 정하다"),
                    g("how much of what we have", "우리가 가진 것 중 얼마나"), g("should be given away", "나눠 줘야 하는지"),
                    g("we are adults", "우리는 어른이다"), g("should have the right", "권리가 있어야 한다"),
                    g("to make such decisions", "그런 결정을 내릴"), g("for ourselves", "스스로")],
        "slashes": ["get offended", "someone else or society", "determines for us", "what we have", "given away;", "we are adults", "the right"],
        "roles": [r("We … we", "S"), r("tend to get offended", "V"), r("someone else or society", "S"), r("determines", "V"),
                  r("how much of what we have should be given away", "O"), r("are", "V"), r("adults", "C"), r("should have", "V"), r("the right", "O")],
        "steps": [
            choice("s2_feel",
                   "다른 사람이나 사회가 우리 대신 얼마나 나눠 줄지 정하면, 우리는 어떻게 느낀대요?",
                   [("o0", "고마워한다", False), ("o1", "상관없어한다", False), ("o2", "기분 나빠한다", True)],
                   "get offended는 '기분이 상하다'예요.",
                   why="'We tend to get offended', 우리는 기분이 상하는 경향이 있대요. 내 것을 얼마나 나눌지는 내가 정하고 싶으니까요.",
                   highlight=["get offended"],
                   tips=[tip("get offended", "'기분이 상하다, 불쾌해하다'예요.", "offended")]),
            show("s2_board", "세미콜론(;) 뒤 — 우리는 어른이니 그런 결정은 스스로 내릴 권리가 있어야 한대요.",
                 panel=board(L2, [], fresh=("decide for ourselves", "the right")),
                 highlight=["the right", "for ourselves"], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("Yet", "하지만"), g("when interviewed", "인터뷰를 하면"), g("altruists", "이타주의자들"),
                    g("known for", "~로 알려진"), g("making the largest sacrifices", "가장 큰 희생을 하는 것"),
                    g("bringing about the greatest benefits", "가장 큰 이익을 가져다주는 것"), g("their recipients", "그들의 수혜자(도움받는 사람)"),
                    g("assert", "주장하다"), g("just the opposite", "정반대")],
        "slashes": ["Yet,", "when interviewed,", "altruists", "the largest sacrifices—", "recipients—"],
        "roles": [r("altruists", "S"), r("assert", "V"), r("just the opposite", "O")],
        "modifiers": ["known for making the largest sacrifices—and bringing about the greatest benefits to their recipients—"],
        "steps": [
            sv("s3_sv", ["Yet", "altruists", "making the largest sacrifices", "their recipients", "assert", "just the opposite"],
               {"altruists": "S", "assert": "V", "just the opposite": "O"},
               {"Yet": "그건 '하지만', 앞과 뒤집는 말이에요.",
                "making the largest sacrifices": "그건 known for(~로 알려진) 뒤 덩어리예요. 앞의 altruists를 꾸며요.",
                "their recipients": "그건 대시(—) 사이, to 뒤 덩어리예요."},
               "주어는 altruists, 동사는 assert, 목적어는 just the opposite(정반대)예요.",
               ask="대시(—) 사이는 흐리게 해 뒀어요. 주어(S), 동사(V), 목적어(O)를 찾아볼까요?",
               faded=["—and bringing about the greatest benefits to their recipients—"]),
            choice("s3_opp",
                   "Yet(하지만) — 이타주의자들은 무엇을 주장한대요?",
                   [("o0", "보통 사람들 생각과 같은 것", False), ("o1", "보통 사람들 생각과 정반대", True), ("o2", "희생은 쓸모없다는 것", False)],
                   "assert 뒤 'just the opposite'를 봐요. opposite은 '반대'예요.",
                   why="'assert just the opposite', 정반대를 주장한대요. 보통 사람들은 '스스로 결정할 권리'를 말했으니, 이타주의자들은 그 반대를 말해요.",
                   highlight=["Yet", "just the opposite"], faded=["—and bringing about the greatest benefits to their recipients—"],
                   point="Yet … altruists … assert just the opposite = 이타주의자들은 상식(스스로 결정)과 정반대를 주장한다"),
            show("s3_board", "보통 사람들 생각과 정반대예요.",
                 panel=board(L2, [("just the opposite", "정반대")], fresh=("just the opposite",)), button="다음 문장",
                 faded=["—and bringing about the greatest benefits to their recipients—"]),
        ],
    },
    {
        "id": 4, "text": BLANK, "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("They", "그들"), g("insist", "주장하다"), g("they", "그들")],
        "roles": [r("They … they", "S"), r("insist", "V")],
        "steps": [
            choice("s4_they",
                   "빈칸 문장의 They(그들)는 누구일까요?",
                   [("o0", "보통 사람들(우리)", False), ("o1", "도움을 받은 사람들", False), ("o2", "큰 희생을 한 이타주의자들", True)],
                   "바로 앞 문장의 주어를 떠올려 봐요. 무엇을 assert(주장)했는지도요.",
                   why="바로 앞 문장의 주어 altruists(이타주의자들)예요. assert가 insist로 이어져요.", highlight=["They", "insist"]),
            choice("s4_side",
                   "빈칸은 이타주의자들이 주장하는 내용이에요. 칠판 왼쪽(스스로 결정할 권리)과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 (스스로 결정)", False), ("o1", "반대 쪽 (스스로 고른 게 아님)", True)],
                   "앞 문장에서 이타주의자들은 just the opposite(정반대)를 주장했어요.",
                   why="이타주의자들은 just the opposite, 정반대를 주장한다고 했어요. 그러니 빈칸은 '스스로 결정한다'의 반대 쪽이에요.",
                   panel=board(L2, [("just the opposite", "정반대")]),
                   tips=[tip("같은 쪽? 반대 쪽?", "빈칸 문장에 But, However, opposite, not 같은 반전 단서가 걸려 있으면 반대 의견이 들어가요.")]),
            choice("s4_guess",
                   "'스스로 결정한다'의 반대라면, 빈칸에는 어떤 말이 올까요?",
                   [("o0", "충분히 고민해서 스스로 골랐다", False), ("o1", "그렇게 하는 것 말고는 선택할 수 없었다", True),
                    ("o2", "보상을 받으려고 했다", False)],
                   "스스로 결정할 권리의 반대예요. 내가 고를 수 있는 게 아니었다는 쪽이에요.",
                   why="스스로 결정할 권리의 반대는 '고를 수 있는 게 아니었다'예요. 이타주의자들은 그렇게 할 수밖에 없었다고 말해요.",
                   point="빈칸 = just the opposite → 스스로 고른 게 아니라 그렇게 할 수밖에 없었다"),
            show("s4_more", "빈칸 뒤 문장들이 같은 말을 반복하는지 확인하며 계속 읽어 봐요.", button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Organ donors, and everyday citizens", "장기 기증자들과 평범한 시민들"), g("risk their own lives", "자기 목숨을 걸다"),
                    g("risk", "걸다, 위험을 무릅쓰다"), g("their own lives", "자기 목숨"),
                    g("to save others", "다른 사람들을 구하려고"), g("in mortal danger", "목숨이 위험한"), g("are", "~이다"),
                    g("remarkably consistent", "놀랍도록 한결같은"), g("explicit denials", "분명한 부인"),
                    g("anything deserving of high praise", "큰 칭찬을 받을 만한 무언가"), g("as well as", "~뿐만 아니라"),
                    g("their assurance", "그들의 확신"), g("anyone in their shoes", "그들의 입장에 있는 누구라도"),
                    g("should have done exactly the same thing", "정확히 똑같이 했을 것이다")],
        "slashes": ["everyday citizens", "their own lives", "in mortal danger", "remarkably consistent", "explicit denials", "have done anything",
                    "high praise", "as well as", "their assurance", "in their shoes"],
        "roles": [r("Organ donors, and everyday citizens", "S"), r("are", "V"), r("remarkably consistent", "C"), r("they", "S"), r("have done", "V"),
                  r("anyone", "S"), r("should have done", "V")],
        "modifiers": ["who risk their own lives to save others in mortal danger"],
        "steps": [
            sv("s5_sv", ["Organ donors, and everyday citizens", "risk", "their own lives", "are", "remarkably consistent"],
               {"Organ donors, and everyday citizens": "S", "are": "V", "remarkably consistent": "C"},
               {"risk": "그건 who 뒤 덩어리 안의 동사예요. 앞의 citizens를 꾸며요.",
                "their own lives": "그건 who 뒤 덩어리 안의 말이에요."},
               "주어는 Organ donors, and everyday citizens, 동사는 are, 보어는 remarkably consistent예요.",
               ask="긴 문장이에요. 주어(S), 동사(V), 보어(C)를 찾아볼까요?"),
            choice("s5_deny",
                   "그들은 무엇을 부인(denials)하고, 무엇을 확신(assurance)한대요?",
                   [("o0", "칭찬받을 일을 했다는 걸 부인하고, 누구라도 똑같이 했을 거라 확신한다", True),
                    ("o1", "칭찬받아야 한다고 하고, 자기만 할 수 있었다고 확신한다", False),
                    ("o2", "위험한 줄 몰랐다고 부인한다", False)],
                   "denials that 뒤 'anything deserving of high praise', assurance that 뒤 'anyone in their shoes … the same thing'을 봐요.",
                   why="'denials that they have done anything deserving of high praise', 칭찬받을 일을 했다는 걸 부인하고, 'anyone in their shoes should have done exactly the same thing', 누구라도 똑같이 했을 거래요.",
                   highlight=["denials", "high praise", "anyone in their shoes", "the same thing"],
                   tips=[tip("in one's shoes", "'~의 입장에서'예요. anyone in their shoes = 그들의 입장이라면 누구라도.", "in their shoes")]),
            show("s5_board", "특별한 걸 한 게 아니라는 말이에요. 빈칸(어쩔 수 없었다)과 같은 쪽이죠. 칠판 오른쪽에 쌓아 둘게요.",
                 panel=board(L2, [("just the opposite", "정반대"), ("no high praise", "칭찬받을 일 아님"), ("anyone … the same thing", "누구라도 똑같이")],
                             fresh=("no high praise", "anyone … the same thing")), button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("To be sure", "확실히"), g("it seems that", "~인 것 같다"), g("the more altruistic someone is", "누군가 더 이타적일수록"),
                    g("the more they are likely to insist", "그들은 더 ~라고 주장할 것 같다"),
                    g("have done no more than", "~ 이상은 하지 않았다, ~만큼만 했다"), g("all of us", "우리 모두"),
                    g("would be expected to do", "하도록 기대될"), g("lest we shirk", "우리가 회피하지 않도록"),
                    g("our basic moral obligation", "우리의 기본적인 도덕적 의무"), g("to humanity", "인류에 대한")],
        "slashes": ["To be sure,", "it seems", "someone is,", "likely to insist", "no more than", "expected to do,", "lest we shirk"],
        "roles": [r("it", "S"), r("seems", "V"), r("someone", "S"), r("is", "V"), r("they … they", "S"), r("are likely to insist", "V"),
                  r("have done", "V"), r("all of us", "S"), r("would be expected", "V"), r("we", "S"), r("shirk", "V")],
        "steps": [
            show("s6_more",
                 "더 이타적인 사람일수록, '우리 모두에게 기대되는 만큼만 했다'고 더 주장한대요. 역시 특별한 선택이 아니었다는 말이에요.",
                 highlight=["the more altruistic someone is", "no more than"],
                 tips=[tip("the 비교급, the 비교급", "'~할수록 더 ~하다'예요. the more altruistic …, the more likely … = 더 이타적일수록 더 ~할 것 같다.", "the more"),
                       tip("no more than", "'~ 이상은 아닌, ~만큼만'이에요. done no more than … expected = 기대되는 만큼만 했다.", "no more than")],
                 panel=board(L2, [("just the opposite", "정반대"), ("no high praise", "칭찬받을 일 아님"), ("anyone … the same thing", "누구라도 똑같이"),
                                  ("no more than expected", "기대되는 만큼만")], fresh=("no more than expected",))),
            show("s6_go", "빈칸은 보통 사람들 생각과 반대 쪽이에요. 칠판 오른쪽 말을 다른 말로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 1, [m("The commonsense understanding", "상식적인 이해는"), " ", m("how most of us think", "우리 대부분이 생각하는 방식"), "에 ",
                         m("conforms to", "따른다"), "."],
          match_display="The commonsense understanding conforms to how most of us think.",
          sv_id="s1_sv", meaning_ids=["s1_mean"])
add_basic(sentences, 2, [m("We tend to", "우리는 ~하는 경향이 있다"), " — ", m("someone else or society", "다른 누군가나 사회가"), " ",
                         m("determines for us", "우리 대신 정하면"), " ", m("get offended", "기분이 상하는"), "."],
          match_display="We tend to get offended when someone else or society determines for us.",
          sv_new=sv_step("s2_basic_sv", ["We", "tend to get offended", "someone else or society", "determines"],
                         {"We": "S", "tend to get offended": "V"},
                         {"someone else or society": "그건 when 뒤 덩어리 안의 주어예요.", "determines": "그건 when 뒤 덩어리 안의 동사예요."},
                         "주어는 We, 동사는 tend to get offended(기분이 상하는 경향이 있다)예요."),
          meaning_after="s2_feel")
add_basic(sentences, 3, [m("Yet", "하지만"), ", ", m("altruists", "이타주의자들은"), " ", m("just the opposite", "정반대"), "를 ", m("assert", "주장한다"), "."],
          match_display="Yet, altruists assert just the opposite.",
          sv_id="s3_sv", meaning_ids=["s3_opp"])
add_basic(sentences, 5, [m("Organ donors, and everyday citizens", "장기 기증자들과 평범한 시민들은"), " ", m("explicit denials", "분명한 부인"), "에서 ",
                         m("remarkably consistent", "놀랍도록 한결같"), m("are", "다"), "."],
          match_display="Organ donors, and everyday citizens are remarkably consistent in their explicit denials.",
          sv_id="s5_sv", meaning_ids=["s5_deny"])
add_basic(sentences, 6, [m("the more altruistic someone is", "누군가 더 이타적일수록"), ", ", m("the more they are likely to insist", "더 주장할 것 같다"),
                         " — ", m("all of us", "우리 모두"), "가 ", m("would be expected to do", "하도록 기대될"), " 만큼만 ", m("have done no more than", "했을 뿐이라고"), "."],
          match_display="It seems that the more altruistic someone is, the more they are likely to insist that they have done no more than all of us would be expected to do.",
          sv_new=sv_step("s6_basic_sv", ["it", "seems", "someone", "they", "are likely to insist"],
                         {"it": "S", "seems": "V"},
                         {"someone": "그건 the more 덩어리 안의 주어예요.", "they": "그건 that 뒤 덩어리 안의 주어예요.",
                          "are likely to insist": "그건 that 뒤 덩어리 안의 동사예요."},
                         "주어는 it, 동사는 seems예요(~인 것 같다). that 뒤가 그 내용이에요."),
          meaning_ids=["s6_more"])

SENSES = {
    1: [sense("to", "conforms to", "~에 (따르다)", "conform to + 명사 = ~에 따르다, 일치하다")],
    2: [sense("to", "tend to get", "~하는 (경향)", "tend + to부정사 = ~하는 경향이 있다"),
        sense("for", "determines for us", "~ 대신, ~을 위해", "전치사 for + 사람"),
        sense("to", "the right to make", "~할 (권리)", "명사 + to부정사"),
        sense("for", "for ourselves", "스스로", "for oneself = 스스로")],
    3: [sense("yet", "Yet, when interviewed", "하지만", "접속사 yet (문장 앞, 반전)"),
        sense("for", "known for making", "~로 (알려진)", "be known for + 명사·-ing"),
        sense("to", "benefits to their recipients", "~에게", "전치사 to + 사람")],
    4: [sense("that", "insist that they", "~라고", "명사절 that (insist that …)")],
    5: [sense("to", "to save others", "~하기 위해", "to부정사 (목적)"),
        sense("that", "denials that they", "~라는 (부인)", "동격의 that + 완전한 문장"),
        sense("as", "as well as", "(as well as의 일부)", "A as well as B = B뿐만 아니라 A도"),
        sense("as", "as well as", "(as well as의 일부)", "A as well as B = B뿐만 아니라 A도"),
        sense("that", "assurance that anyone", "~라는 (확신)", "동격의 that + 완전한 문장")],
    6: [sense("to", "To be sure", "(To be sure의 일부)", "To be sure = 확실히, 물론"),
        sense("that", "it seems that", "~인 (것 같다)", "it seems that + 주어·동사"),
        sense("to", "likely to insist", "~할 (것 같은)", "be likely + to부정사"),
        sense("that", "insist that they", "~라고", "명사절 that (insist that …)"),
        sense("to", "expected to do", "~하도록 (기대되는)", "be expected + to부정사"),
        sense("to", "obligation to humanity", "~에 대한", "전치사 to + 명사")],
}

WORDS = {"commonsense": "상식적인", "understanding": "이해", "moral": "도덕적인", "status": "지위, 상태", "altruistic": "이타적인",
         "acts": "행동", "conforms": "따르다", "most": "대부분", "responsibilities": "책임", "toward": "~에 대한", "tend": "~하는 경향이 있다",
         "offended": "기분이 상한", "someone": "누군가", "society": "사회", "determines": "정하다", "much": "많이", "given": "주어진",
         "adults": "어른들", "right": "권리", "decisions": "결정", "ourselves": "우리 자신", "interviewed": "인터뷰를 받은",
         "altruists": "이타주의자들", "known": "알려진", "making": "하는 것", "largest": "가장 큰", "sacrifices": "희생",
         "bringing": "가져오는 것", "greatest": "가장 큰", "benefits": "이익", "recipients": "수혜자", "assert": "주장하다",
         "opposite": "반대", "insist": "주장하다", "organ": "장기", "donors": "기증자들", "everyday": "평범한", "citizens": "시민들",
         "risk": "걸다, 위험을 무릅쓰다", "lives": "목숨", "save": "구하다", "mortal": "치명적인", "danger": "위험",
         "remarkably": "놀랍도록", "consistent": "한결같은", "explicit": "분명한", "denials": "부인", "anything": "무언가",
         "deserving": "~을 받을 만한", "high": "큰, 높은", "praise": "칭찬", "assurance": "확신", "anyone": "누구라도",
         "shoes": "신발 · in one's shoes = ~의 입장에서", "done": "했다", "exactly": "정확히", "sure": "확실한", "seems": "~인 것 같다",
         "likely": "~할 것 같은", "expected": "기대되는", "lest": "~하지 않도록", "shirk": "회피하다", "basic": "기본적인",
         "obligation": "의무", "humanity": "인류", "well": "잘 · as well as = ~뿐만 아니라", "should": "~해야 한다",
         "would": "~할 것이다", "make": "하다(결정을)", "such": "그런", "have": "가지다", "thing": "일, 것", "all": "모두"}

STORIES = [
    (3, [sc("문장 1~2", "🙋", "decide for ourselves", "보통 우리는 내 것을 얼마나 나눌지 스스로 정할 권리가 있다고 봐요"),
         sc("문장 3", "🔄", "Yet · just the opposite", "그런데 큰 희생을 한 이타주의자들은 정반대를 말해요")]),
    (6, [sc("빈칸 문장", "🗣️", "They insist that they ____", "그들은 자신들이 ____라고 주장해요"),
         sc("문장 5~6", "🫀", "no high praise · the same thing", "칭찬받을 일이 아니고, 누구라도 똑같이 했을 거래요 — 기대되는 만큼만 했대요")]),
]

OPTIONS = [
    ("1", "had absolutely no choice but to act as they did", ["no choice but to"], "그렇게 행동할 수밖에 없었다", True),
    ("2", "should have been rewarded financially", ["rewarded financially"], "금전적으로 보상받았어야 했다", False),
    ("3", "regretted making such decisions", ["regretted"], "그런 결정을 후회했다", False),
    ("4", "deserved others’ appreciation in return", ["deserved", "appreciation"], "그 대가로 다른 사람들의 감사를 받을 만했다", False),
    ("5", "found the moral obligations inapplicable in risky situations", ["moral obligations inapplicable"], "위험한 상황에서는 도덕적 의무가 적용되지 않는다고 여겼다", False),
]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 4, "analysis_first": True, "wrong_rate": 66.3, "wrong_rank": 5,
    "glosses": [g("absolutely", "전혀, 완전히"), g("no choice but to", "~할 수밖에 없는"), g("rewarded", "보상받은"), g("financially", "금전적으로"),
                g("regretted", "후회했다"), g("deserved", "~을 받을 만했다"), g("appreciation", "감사"), g("in return", "그 대가로"),
                g("obligations", "의무"), g("inapplicable", "적용되지 않는"), g("risky", "위험한")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "보통 사람들 생각(스스로 결정)과 반대 쪽, 칠판 오른쪽 말을 떠올리며 골라 봐요.",
        "정답이에요! 보통 사람들은 '스스로 결정할 권리'를 말하지만, 이타주의자들은 정반대로 '그렇게 할 수밖에 없었다'고 해요. 칭찬받을 일도 아니고 누구라도 똑같이 했을 거라는 말이 같은 쪽이에요.",
        "정답은 ①이에요. 이타주의자들은 스스로 고른 게 아니라 그렇게 할 수밖에 없었다고 말해요.",
        {"2": "보상 이야기는 글에 없어요. 오히려 칭찬받을 일도 아니라고 했어요.",
         "3": "후회한다는 말은 글에 없어요. 누구라도 똑같이 했을 거라며 당연하게 여겨요.",
         "4": "그들은 칭찬받을 일을 했다는 걸 부인했어요(denials). 감사를 받을 만했다는 건 반대예요.",
         "5": "그들은 기본적인 도덕적 의무를 다했을 뿐이라고 했어요. 의무가 적용되지 않는다는 건 반대예요."},
        {"5": review(23.9,
                     "⑤는 '위험한 상황에서는 도덕적 의무가 적용되지 않는다고 여겼다'예요. 하지만 마지막 문장에서 이타주의자들은 '우리 모두에게 기대되는 만큼만 했다', 기본적인 도덕적 의무를 다했을 뿐이라고 해요. 의무가 그대로 적용된다고 본 거라 반대예요.",
                     "그래서 ⑤가 아니에요. 어디서 헷갈렸어요?",
                     [("moral obligation이 글에 나와서 골랐어요", ["word_overlap"],
                       "알려 줘서 고마워요. 글에 나온 단어가 보기에 있다고 정답은 아니에요. 그 단어를 어떻게 말하는지(적용된다/안 된다)를 봐야 해요. 앞으로 이 점을 강조해서 알려 줄게요."),
                      ("lest 뒤 문장이 어려웠어요", ["lest_clause"],
                       "알려 줘서 고마워요. lest we shirk는 '우리가 회피하지 않도록'이에요. 의무를 지킨다는 말이에요. 앞으로 비슷한 구문이 나오면 짚어 줄게요."),
                      ("둘 다요", ["word_overlap", "lest_clause"], "알려 줘서 고마워요. 앞으로 단어가 어떻게 쓰였는지와 어려운 구문을 같이 짚어 줄게요.")],
                     panel=rows(("마지막 문장", "done no more than … expected … our basic moral obligation", "기대되는 만큼, 도덕적 의무를 다했을 뿐", "hl"),
                                ("⑤", "moral obligations inapplicable", "도덕적 의무가 적용 안 됨 → 반대", "hl2"))),
         "4": review(16.5,
                     "④는 '그 대가로 감사를 받을 만했다'예요. 그런데 이타주의자들은 칭찬받을 만한 일을 했다는 걸 분명히 부인했어요(explicit denials). 누구라도 똑같이 했을 거라면서요.",
                     "그래서 ④가 아니에요. 어디서 헷갈렸어요?",
                     [("큰 희생을 했으니 감사받을 만하다고 생각했어요", ["own_opinion"],
                       "알려 줘서 고마워요. 내 생각이 아니라 글 속 이타주의자들이 뭐라고 주장하는지를 골라야 해요. 앞으로 '누구의 말인지'를 짚어 줄게요."),
                      ("denials를 못 봤어요", ["denial_word"],
                       "알려 줘서 고마워요. denial은 '부인, 부정'이에요. 앞으로 비슷한 단어가 나오면 강조해서 알려 줄게요."),
                      ("둘 다요", ["own_opinion", "denial_word"], "알려 줘서 고마워요. 앞으로 누구의 말인지와 부정의 말을 같이 짚어 줄게요.")])}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 32번 (빈칸 추론, 2점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 두 쪽 말 모으기 → 빈칸이 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-altruists.svg", ("Common sense", "보통 생각"), "↔", ("Altruists", "이타주의자"),
                                       "목숨을 건 사람들은 그 일을 어떻게 말할까?", "2024년 3월 32번 도입 칠판"),
                      "alt": "칠판: Common sense(보통 생각) ↔ Altruists(이타주의자)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "남을 구하려고 목숨을 건 사람은 자기 행동을 어떻게 말할까요? 이번 글은 이타적인 행동을 보는 두 생각을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("commonsense", "상식적인"), g("moral", "도덕적인"), g("conform to", "~에 따르다"), g("responsibility", "책임"),
                           g("get offended", "기분이 상하다"), g("determine", "정하다"), g("sacrifice", "희생"), g("recipient", "수혜자"),
                           g("assert", "주장하다"), g("insist", "주장하다"), g("organ donor", "장기 기증자"), g("mortal", "치명적인"),
                           g("consistent", "한결같은"), g("explicit", "분명한"), g("denial", "부인"), g("assurance", "확신"),
                           g("in one's shoes", "~의 입장에서"), g("obligation", "의무")],
               "options": [g("no choice but to", "~할 수밖에 없는"), g("appreciation", "감사"), g("inapplicable", "적용되지 않는")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법",
       chunks={"The commonsense understanding": "상식적인 이해", "the moral status": "도덕적 지위", "altruistic acts": "이타적인 행동",
               "conforms to": "~에 따르다", "our responsibilities": "우리의 책임", "We": "우리는", "tend to get offended": "기분이 상하는 경향이 있다",
               "someone else or society": "다른 누군가나 사회", "determines": "정하다", "Yet": "하지만", "altruists": "이타주의자들",
               "making the largest sacrifices": "가장 큰 희생을 하는 것", "their recipients": "그들의 수혜자", "assert": "주장하다",
               "just the opposite": "정반대", "Organ donors, and everyday citizens": "장기 기증자들과 평범한 시민들", "risk": "걸다",
               "their own lives": "자기 목숨", "are": "~이다", "remarkably consistent": "놀랍도록 한결같은", "it": "그것(가주어)",
               "seems": "~인 것 같다", "someone": "누군가", "they": "그들", "are likely to insist": "주장할 것 같다",
               "how most of us think": "우리 대부분이 생각하는 방식", "We tend to": "우리는 ~하는 경향이 있다", "get offended": "기분이 상하다",
               "determines for us": "우리 대신 정하다", "explicit denials": "분명한 부인"})
