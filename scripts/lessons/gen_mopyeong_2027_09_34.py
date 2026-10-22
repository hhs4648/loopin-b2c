"""2026년 9월 모의평가(2027학년도, 평가원) 영어 34번 레슨 + 대사를 만든다 (빈칸 추론, 3점). 오답률 73%(메가스터디) · Top 1.

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_34.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸이 마지막 문장(The joke-hearers get far more pleasure from the joke ____.).
정답 ④ if they have to do a little work(약간의 노력을 해야 할 때).
선택률(메가스터디 풀서비스 채점): ① 24 ② 25 ③ 9 ④ 27 ⑤ 14 — 많이 고른 오답 ② when it matches their expectations 25%,
① if they feel relaxed enough to laugh 24%. 두 오답이 정답과 거의 같다.
② 짐작: 「예상과 맞을 때 즐겁다」는 상식으로 골랐다. 글은 반대 — 놀라움(surprise)이 기본이고, 두 절벽이 너무 가까우면(다 예상되면)
   그냥 걸어 건널 뿐 짜릿한 도약이 없다(8문장).
① 짐작: 4문장 how relaxed they appear to be에 relaxed가 나와서. 하지만 그건 농담하는 사람이 청중에 대해 짐작하는 것 중 하나일 뿐이다.
열쇠: 협곡 비유 — setup = 이쪽 절벽, punch line = 건너편 절벽. 너무 멀면(7문장) 못 건넌다 = 이해 못 함(⑤ 쪽),
너무 가까우면(8문장) 그냥 걸어 건넌다 = 놀라움이 없음(② 쪽). 빈칸 = 그 사이, 청중이 직접 뛰어야 하는 도약 = 약간의 노력.
칠판: 표(rows) — 6문장 비유 대응표, 8문장 「너무 멂 / 너무 가까움 / ?」 표. 두 쪽 단어 지도 대신 표로 했다(세 칸이라서).
시험지 아래 *풀이 단어: canyon(협곡) — 핵심어·단어 체크에서 뺐다(뜻만 단다).
해설지(content/tutor/exam-source/2027-09-평가원/해설.txt 34번) 해석·Words and Phrases와 대조함 — fundamental 기본적인,
punch line 농담의 결정적인 구절, assumption 가정, reference point 기준점, relaxed 편안한, metaphorical 은유적인, cliff 절벽,
leap 뛰어넘다/도약, compare A to B는 해설대로 「A를 B에 비유하다」.
오답률·선택률은 메가스터디 풀서비스 채점 기준(wrong_rate_source).
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음). Claude 초안 — 선생님 검토 전.

선생님이 확인할 점
1. 「같은 쪽? 반대 쪽?」(s9_side)을 두 쪽이 아니라 표의 세 줄(너무 멂 / 너무 가까움 / 그 사이 짜릿한 도약) 중 고르게 했다.
   빈칸의 far more pleasure(+)가 둘 다 −인 양 끝이 아니라 가운데라서. 두 쪽으로 줄이려면 「너무 가까움(다 예상됨) ↔ 도약」.
2. 빈칸 앞 3지 s9_fill의 정답 보기 「청중이 스스로 조금 생각해서 뛰어 건너야 할 때」가 정답 ④와 가깝다. 너무 쉬우면 빼도 된다.
3. ②·① 둘 다 option_review를 달았다(25%·24%). 고른 이유는 추측이다.
4. 4문장(relaxed)은 ① 함정이라 s4_note에서 「농담하는 사람이 짐작하는 것들」로만 짚고 relaxed를 칠하지 않았다.
5. 헷갈리는 단어(trap): punch line(농담의 결정적 구절) · lie in(~에 있다) · take(받아들이다) · make it(도달하다).
   엑셀(함정단어.xlsx)에는 안 넣었다. compare A to B(비유하다)는 Tip으로.
6. 2문장의 대시(―)는 앱 규칙대로 「—」로 바꿨다. 대시가 하나뿐이라 흐림(삽입)으로 두지 않았다.
   that’s why는 줄임말 규칙대로 that(S) + ’s(V) + why 절(C), 7문장 they’re도 they(S) + ’re(V).
7. 해석 맞추기는 짧은 1·6문장. 칠판 정리(story)는 3·5문장 뒤 두 번.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-09-34-joke-canyon"

BLANK = "The joke-hearers get far more pleasure from the joke ________."
S = [
    "Surprise is the fundamental joke mechanism.",
    "Most punch lines rely on an element of surprise for their effect — that’s why they’re not funny the third time you hear them.",
    "The joke-teller’s skill lies in judging exactly how much of a surprise the audience is prepared to take.",
    "He must make a series of assumptions about what they will understand, what their reference points are, and how relaxed "
    "they appear to be.",
    "Jerry Seinfeld once compared telling a joke to attempting to leap a metaphorical canyon, taking the audience with you.",
    "The setup to the joke is the near-side cliff, and the punch line is the far side.",
    "If they’re too far apart, the listeners don’t make it to the other side.",
    "And if they are too close together, the audience just steps across the gap and doesn’t experience a thrilling leap of any kind.",
    BLANK,
]
# 해설지 해석 (2027-09-평가원/해설.txt 34번)
KO = [
    "놀라움은 농담의 기본적인 작동 원리이다.",
    "농담의 결정적인 대부분의 구절은 그것의 효과를 위해 놀라움이라는 요소에 의존하는데, 여러분이 그것을 세 번째 들을 때에는 재미가 없는 "
    "이유가 바로 그것이다.",
    "농담을 하는 사람의 기술은 청중이 정확히 얼마만큼의 놀라움을 받아들일 준비가 되어 있는지를 판단하는 데 있다.",
    "그는 청중이 무엇을 이해할지, 그들의 기준점이 무엇인지, 그리고 그들이 얼마나 편안해 보이는지에 대해 일련의 가정을 세워야 한다.",
    "한때 Jerry Seinfeld는 농담하는 것을 청중을 데리고 은유적인 협곡을 뛰어넘으려고 하는 것에 비유했다.",
    "농담의 설정은 가까운 쪽 절벽이고, 농담의 결정적인 구절은 건너편 절벽이다.",
    "그것들이 너무 멀리 떨어져 있으면 청중은 반대편에 도달하지 못한다.",
    "그리고 그것들이 서로 너무 가깝다면, 청중은 그냥 그 틈을 걸어서 건너갈 뿐 어떠한 짜릿한 도약도 경험하지 못한다.",
    "농담을 듣는 사람들은 ________ 그 농담에서 훨씬 더 큰 즐거움을 얻는다.",
]

MAP = rows(("setup (농담의 설정)", "the near-side cliff", "이쪽 절벽", "hl"),
           ("punch line (결정적 구절)", "the far side", "건너편 절벽", "hl"),
           ("joke (농담하기)", "leap a canyon", "청중을 데리고 협곡을 뛰어넘기"))

FAR = ("too far apart", "don’t make it to the other side", "건너편에 닿지 못한다")
CLOSE = ("too close together", "just steps across the gap", "그냥 걸어 건넌다 — 짜릿한 도약이 없다")


def gap_table(close=True):
    """너무 멂 / 너무 가까움 / ? — 읽은 문장까지만"""
    rs = [(FAR[0], FAR[1], FAR[2], "hl2")]
    if close:
        rs.append((CLOSE[0], CLOSE[1], CLOSE[2], "hl2"))
        rs.append(("?", "a thrilling leap", "짜릿한 도약", "hl"))
    return rows(*rs)


SIDE_TIP = tip("같은 쪽? 반대 쪽?", "빈칸 문장에 But, However, not 같은 반전 단서가 있으면 반대 의견이 들어가요. "
               "far more pleasure(훨씬 더 큰 즐거움)처럼 좋은 말(+)이면 글에서 좋다고 한 쪽과 같은 말이 들어가요.")

BLANK_GLOSSES = [g("The joke-hearers", "농담을 듣는 사람들"), g("joke-hearers", "농담을 듣는 사람들"), g("get", "얻다"),
                 g("far more pleasure", "훨씬 더 큰 즐거움"), g("far more", "훨씬 더"), g("pleasure", "즐거움"),
                 g("from the joke", "그 농담에서"), g("joke", "농담")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Surprise", "놀라움"), g("is", "~이다"), g("the fundamental joke mechanism", "농담의 기본적인 작동 원리"),
                    g("fundamental", "기본적인, 근본적인"), g("mechanism", "작동 원리, 구조"), *BLANK_GLOSSES],
        "roles": [r("Surprise", "S"), r("is", "V"), r("the fundamental joke mechanism", "C")],
        "steps": [
            show("s1_passage", "빈칸은 마지막 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "농담을 듣는 사람들은 ____할 때 그 농담에서 훨씬 더 큰 즐거움을 얻는다", True),
                    ("o1", "농담을 하는 사람은 ____할 때 훨씬 더 즐겁다", False),
                    ("o2", "농담을 듣는 사람들은 ____ 농담보다 다른 데서 즐거움을 얻는다", False)],
                   "joke-hearers는 '농담을 듣는 사람들'이에요. far more는 '훨씬 더'예요.",
                   why="'The joke-hearers get far more pleasure from the joke', 듣는 사람들이 그 농담에서 훨씬 더 큰 즐거움을 얻는대요. 빈칸에는 언제 그런지가 와요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["joke-hearers", "far more pleasure", "________"],
                   tips=[tip("far + 비교급", "far more는 '훨씬 더'예요. far가 비교급을 세게 해요.", "far more")]),
            show("s1_where", "그럼 듣는 사람이 언제 농담을 더 즐기는지 생각하며 문장 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Most punch lines", "대부분의 농담의 결정적 구절"), g("punch lines", "농담의 결정적 구절 · 웃음이 터지는 마지막 한마디"),
                    g("punch", "펀치"), g("lines", "구절, 대사"), g("Most", "대부분의"), g("rely on", "~에 의존하다"),
                    g("rely", "의존하다"), g("an element of surprise", "놀라움이라는 요소"), g("element", "요소"),
                    g("surprise", "놀라움"), g("for their effect", "그 효과를 위해"), g("effect", "효과"),
                    g("that’s why", "그래서 ~이다, 그것이 ~하는 이유이다"), g("they’re not funny", "그것들은 재미가 없다"),
                    g("funny", "재미있는"), g("the third time", "세 번째에"), g("third", "세 번째의"),
                    g("you hear them", "여러분이 그것을 들을 때"), g("hear", "듣다")],
        "slashes": ["Most punch lines", "an element of surprise", "for their effect", "that’s why", "not funny"],
        "roles": [r("Most punch lines", "S"), r("rely on", "V"), r("an element of surprise", "O"), r("that", "S"), r("’s", "V"),
                  r("why they’re not funny the third time you hear them", "C")],
        "steps": [
            choice("s2_why",
                   "농담을 세 번째 들으면 재미가 없는 이유는 무엇일까요?",
                   [("o0", "이미 알고 있어서 놀라움이 없으니까", True),
                    ("o1", "듣는 사람이 지쳐서", False),
                    ("o2", "농담이 점점 길어져서", False)],
                   "that’s why 앞이 이유예요. rely on은 '~에 의존하다'예요.",
                   why="'Most punch lines rely on an element of surprise', 웃음은 놀라움에 기대요. 세 번째로 들으면 이미 아는 말이라 놀랄 게 없어요.",
                   highlight=["surprise", "that’s why", "not funny", "third time"],
                   tips=[tip("that’s why ~", "'그래서 ~이다'예요. 앞 말이 이유, why 뒤가 결과예요.", "that’s why"),
                         tip("punch line", "이 글에서는 → 농담의 결정적 구절, 웃음이 터지는 마지막 말  ('주먹' 아님)", "punch lines", trap=True)]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("The joke-teller’s skill", "농담하는 사람의 기술"), g("joke-teller’s", "농담하는 사람의"), g("skill", "기술"),
                    g("lies in", "~에 있다"), g("lies", "있다, 놓여 있다"), g("judging", "판단하는 것"), g("exactly", "정확히"),
                    g("how much of a surprise", "얼마만큼의 놀라움"), g("the audience", "청중"), g("audience", "청중"),
                    g("is prepared to take", "받아들일 준비가 되어 있다"), g("prepared", "준비가 된"), g("take", "받아들이다")],
        "slashes": ["The joke-teller’s skill", "judging exactly", "how much of a surprise"],
        "roles": [r("The joke-teller’s skill", "S"), r("lies", "V")],
        "modifiers": [],
        "steps": [
            choice("s3_skill",
                   "농담하는 사람의 기술은 무엇을 판단하는 데 있을까요?",
                   [("o0", "청중을 최대한 많이 놀라게 하는 방법", False),
                    ("o1", "청중이 놀라움을 정확히 얼마만큼 받아들일 준비가 됐는지", True),
                    ("o2", "같은 농담을 몇 번 들려줄지", False)],
                   "judging 뒤 how much of a surprise를 봐요. take는 여기서 '받아들이다'예요.",
                   why="'judging exactly how much of a surprise the audience is prepared to take', 청중이 받아들일 수 있는 놀라움이 정확히 얼마인지 판단하는 거래요. 많을수록 좋은 게 아니에요.",
                   highlight=["lies in", "how much", "prepared to take"],
                   tips=[tip("lie in ~", "이 글에서는 → ~에 있다  ('거짓말하다, 눕다' 아님)", "lies in", trap=True),
                         tip("take", "이 글에서는 → 받아들이다  ('가져가다' 아님)", "take", trap=True)]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "medium",
        "glosses": [g("He", "그(농담하는 사람)"), g("must make", "세워야 한다"), g("must", "~해야 한다"),
                    g("a series of assumptions", "일련의 가정"), g("series", "일련, 연속"), g("assumptions", "가정, 짐작"),
                    g("about what they will understand", "청중이 무엇을 이해할지에 대해"), g("understand", "이해하다"),
                    g("what their reference points are", "그들의 기준점이 무엇인지"), g("reference points", "기준점"),
                    g("reference", "참고, 기준"), g("points", "점"),
                    g("how relaxed they appear to be", "그들이 얼마나 편안해 보이는지"), g("relaxed", "편안한"),
                    g("appear", "~처럼 보이다")],
        "slashes": ["a series of assumptions", "will understand,", "reference points are,"],
        "roles": [r("He", "S"), r("must make", "V"), r("a series of assumptions", "O")],
        "steps": [
            show("s4_note", "얼마나 놀라게 할지 정하려고, 농담하는 사람이 청중에 대해 짐작해야(assumptions) 하는 것들이에요.",
                 highlight=["assumptions"], button="다음 문장",
                 tips=[tip("reference point", "'기준점'이에요. 청중이 무엇을 기준으로 알아듣는지예요.", "reference points")]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Jerry Seinfeld", "제리 사인펠드 · 미국 코미디언 이름"), g("Jerry", "제리 (이름)"), g("Seinfeld", "사인펠드 (이름)"),
                    g("once", "한때, 언젠가"), g("compared", "비유했다, 비교했다"), g("telling a joke", "농담하는 것"),
                    g("telling", "말하는 것"), g("to attempting to leap", "뛰어넘으려 하는 것에"), g("attempting", "시도하는 것"),
                    g("leap", "뛰어넘다"), g("a metaphorical canyon", "은유적인 협곡"), g("metaphorical", "은유적인, 비유의"),
                    g("canyon", "협곡"), g("taking the audience with you", "청중을 데리고"), g("taking", "데리고 가는"),
                    g("audience", "청중")],
        "slashes": ["once compared", "telling a joke", "to attempting to leap", "a metaphorical canyon,"],
        "roles": [r("Jerry Seinfeld", "S"), r("compared", "V"), r("telling a joke", "O")],
        "steps": [
            choice("s5_compare",
                   "Seinfeld는 농담하는 것을 무엇에 비유했을까요?",
                   [("o0", "혼자 협곡을 구경하는 것", False),
                    ("o1", "청중을 데리고 협곡을 뛰어넘는 것", True),
                    ("o2", "청중에게 협곡 사진을 보여 주는 것", False)],
                   "compared A to B를 봐요. leap은 '뛰어넘다', taking the audience with you는 '청중을 데리고'예요.",
                   why="'compared telling a joke to attempting to leap a metaphorical canyon', 농담하기를 협곡 뛰어넘기에 비유했어요. 'taking the audience with you', 청중을 데리고요.",
                   highlight=["compared", "leap", "canyon", "taking the audience"],
                   tips=[tip("compare A to B", "여기서는 'A를 B에 비유하다'예요. 농담하기(A)를 협곡 뛰어넘기(B)에 빗댔어요.", "compared")]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("The setup to the joke", "농담의 설정"), g("setup", "설정 · 웃음 전에 상황을 깔아 두는 앞부분"),
                    g("is", "~이다"), g("the near-side cliff", "가까운 쪽 절벽"), g("near-side", "가까운 쪽의"),
                    g("cliff", "절벽"), g("the punch line", "농담의 결정적 구절"), g("punch line", "농담의 결정적 구절"),
                    g("the far side", "건너편"), g("far", "먼"), g("side", "쪽, 편")],
        "slashes": ["The setup to the joke", "near-side cliff,"],
        "roles": [r("The setup to the joke", "S"), r("is … is", "V"), r("the near-side cliff", "C"), r("the punch line", "S"),
                  r("the far side", "C")],
        "steps": [
            show("s6_map", "농담 앞부분(setup)은 이쪽 절벽, 웃음이 터지는 말(punch line)은 건너편 절벽이래요.\n청중이 둘 사이를 뛰어 건너야 웃음이 나요.",
                 panel=MAP, highlight=["setup", "near-side cliff", "punch line", "far side"], button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("If", "만약 ~라면"), g("too far apart", "너무 멀리 떨어진"), g("too", "너무"), g("apart", "떨어져"),
                    g("the listeners", "듣는 사람들"), g("listeners", "듣는 사람들"),
                    g("don’t make it", "도달하지 못하다, 해내지 못하다"), g("make it", "도달하다, 해내다"),
                    g("to the other side", "반대편에"), g("other", "다른, 반대의"), g("side", "편")],
        "slashes": ["too far apart,"],
        "roles": [r("they", "S"), r("’re", "V"), r("too far apart", "C"), r("the listeners", "S"), r("don’t make", "V")],
        "steps": [
            choice("s7_far",
                   "두 절벽이 너무 멀면(too far apart), 농담에서는 어떤 상황일까요?",
                   [("o0", "청중이 너무 쉽게 다 알아챈다", False),
                    ("o1", "청중이 농담을 따라가지 못해 이해하지 못한다", True),
                    ("o2", "농담이 너무 짧게 끝난다", False)],
                   "don’t make it to the other side는 '건너편에 닿지 못한다'예요.",
                   why="앞부분과 웃음 포인트가 너무 떨어져 있으면 청중이 건너편에 닿지 못해요. 무슨 말인지 이해를 못 하는 거예요.",
                   highlight=["too far apart", "don’t make it"],
                   tips=[tip("make it", "이 글에서는 → (목적지에) 도달하다, 해내다  ('그것을 만들다' 아님)", "make it", trap=True)]),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("And if", "그리고 만약 ~라면"), g("they are", "그것들이 ~이다"), g("too close together", "서로 너무 가까운"),
                    g("close", "가까운"), g("together", "함께, 서로"), g("the audience", "청중"),
                    g("just steps across the gap", "그냥 그 틈을 걸어서 건너간다"), g("just", "그냥, 단지"),
                    g("steps", "걸어가다, 발을 내딛다"), g("across", "~을 가로질러"), g("the gap", "그 틈"), g("gap", "틈"),
                    g("doesn’t experience", "경험하지 못한다"), g("experience", "경험하다"),
                    g("a thrilling leap", "짜릿한 도약"), g("thrilling", "짜릿한, 신나는"), g("leap", "도약"),
                    g("of any kind", "어떤 종류의 ~도"), g("kind", "종류")],
        "slashes": ["too close together,", "across the gap", "doesn’t experience"],
        "roles": [r("they", "S"), r("are", "V"), r("too close together", "C"), r("the audience", "S"), r("steps", "V"),
                  r("doesn’t experience", "V"), r("a thrilling leap", "O")],
        "steps": [
            choice("s8_close",
                   "두 절벽이 너무 가까우면(too close together), 농담에서는 어떤 상황일까요?",
                   [("o0", "청중이 이해를 못 해서 웃지 못한다", False),
                    ("o1", "청중이 기분이 상한다", False),
                    ("o2", "청중이 다 예상해서 놀라움 없이 쉽게 넘어간다", True)],
                   "just steps across the gap은 '그냥 그 틈을 걸어서 건너간다'예요. thrilling은 '짜릿한'이에요.",
                   why="앞부분에서 웃음 포인트가 다 보이면 청중은 뛰지 않고 그냥 걸어서 건너요. 'doesn’t experience a thrilling leap', 짜릿한 도약이 없대요.",
                   highlight=["too close together", "just steps across", "thrilling leap"]),
            show("s8_table", "너무 멀어도, 너무 가까워도 재미가 없어요.\n둘 다 짜릿한 도약(a thrilling leap)이 없어요.",
                 panel=gap_table(), button="다음 문장"),
        ],
    },
    {
        "id": 9, "text": BLANK, "model_translation": KO[8], "teaching_value": "high",
        "glosses": list(BLANK_GLOSSES),
        "slashes": ["far more pleasure"],
        "roles": [r("The joke-hearers", "S"), r("get", "V"), r("far more pleasure", "O")],
        "steps": [
            choice("s9_side",
                   "빈칸은 훨씬 더 큰 즐거움(far more pleasure)을 얻을 때예요. 표의 어느 줄과 같은 쪽일까요?",
                   [("o0", "너무 멂 — 건너편에 닿지 못함", False),
                    ("o1", "너무 가까움 — 그냥 걸어 건넘", False),
                    ("o2", "그 사이 — 짜릿한 도약", True)],
                   "pleasure(즐거움)는 좋은 말(+)이에요. 표에서 재미없다고 한 줄은 빼 봐요.",
                   why="너무 멀면 못 건너고, 너무 가까우면 도약이 없어요. 즐거움은 청중이 직접 뛰어 건너는 짜릿한 도약 쪽이에요.",
                   highlight=["far more pleasure", "________"], panel=gap_table(), tips=[SIDE_TIP],
                   point="빈칸 = far more pleasure(+) = 너무 멀지도 가깝지도 않아 청중이 직접 뛰어 건너는 도약 = 같은 쪽"),
            choice("s9_fill",
                   "그럼 빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "모든 것이 예상한 대로 흘러갈 때", False),
                    ("o1", "끝까지 무슨 말인지 모를 때", False),
                    ("o2", "청중이 스스로 조금 생각해서 뛰어 건너야 할 때", True)],
                   "표의 가운데, 너무 가깝지도 너무 멀지도 않은 자리를 떠올려 봐요.",
                   why="다 예상되면 너무 가까운 쪽이고, 끝까지 모르면 너무 먼 쪽이에요. 청중이 조금 애써서 틈을 뛰어 건널 때 가장 즐거워요.",
                   highlight=["far more pleasure", "________"]),
            show("s9_go", "빈칸은 짜릿한 도약 쪽이에요. 청중이 틈을 직접 뛰어 건너는 것을 다른 말로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — 짧은 1·6문장. 덩어리는 문장에 그대로 있는 구절
add_match(sentences, 1, [m("Surprise", "놀라움은"), " ", m("the fundamental joke mechanism", "농담의 기본적인 작동 원리"),
                         m("is", "이다"), "."])
add_match(sentences, 6, [m("The setup to the joke", "농담의 설정은"), " ", m("the near-side cliff", "가까운 쪽 절벽"), "이고, ",
                         m("the punch line", "결정적 구절은"), " ", m("the far side", "건너편 절벽"), "이다."])
# 가리키는 말
add_refers(sentences, 2, {"they’re not funny": "they = punch lines(농담의 결정적 구절)"})
add_refers(sentences, 4, {"He": "the joke-teller(농담하는 사람)"})
add_refers(sentences, 7, {"they’re": "they = the setup and the punch line(설정과 결정적 구절, 두 절벽)"})
add_refers(sentences, 8, {"they are": "they = the setup and the punch line(설정과 결정적 구절, 두 절벽)"})

SENSES = {
    2: [sense("for", "for their effect", "~을 위해", "전치사 for (목적)"),
        sense("that", "that’s why", "그것이 (~하는 이유다)", "지시대명사 that — 앞 내용 전체")],
    3: [sense("to", "prepared to take", "~할 (준비가 된)", "be prepared to + 동사원형")],
    4: [sense("to", "appear to be", "~인 것처럼 (보이다)", "appear to + 동사원형")],
    5: [sense("to", "to attempting", "~에 (비유하다)", "compare A to B = A를 B에 비유하다"),
        sense("to", "attempting to leap", "~하려고 (시도하다)", "attempt to + 동사원형")],
    6: [sense("to", "The setup to the joke", "~의 (농담의 설정)", "전치사 to (소속·관련)")],
    7: [sense("if", "If they’re too far apart", "만약 ~라면", "접속사 if (조건)"),
        sense("to", "to the other side", "~에 (닿다)", "make it to + 장소 = ~에 도달하다")],
    8: [sense("if", "And if they are", "만약 ~라면", "접속사 if (조건)")],
}

WORDS = {"surprise": "놀라움", "fundamental": "기본적인", "joke": "농담", "mechanism": "작동 원리", "punch": "펀치",
         "lines": "구절", "rely": "의존하다", "element": "요소", "effect": "효과", "funny": "재미있는", "third": "세 번째의",
         "hear": "듣다", "they’re": "그것들은 ~이다", "joke-teller’s": "농담하는 사람의", "skill": "기술", "lies": "있다",
         "judging": "판단하는 것", "exactly": "정확히", "audience": "청중", "prepared": "준비가 된", "series": "일련",
         "assumptions": "가정", "understand": "이해하다", "reference": "기준", "points": "점", "relaxed": "편안한",
         "appear": "~처럼 보이다", "jerry": "제리", "seinfeld": "사인펠드", "once": "한때", "compared": "비유했다",
         "telling": "말하는 것", "attempting": "시도하는 것", "leap": "뛰어넘다", "metaphorical": "은유적인", "canyon": "협곡",
         "taking": "데리고 가는", "setup": "설정", "near-side": "가까운 쪽의", "cliff": "절벽", "far": "먼", "side": "쪽",
         "apart": "떨어져", "listeners": "듣는 사람들", "close": "가까운", "together": "서로", "steps": "걸어가다",
         "gap": "틈", "experience": "경험하다", "thrilling": "짜릿한", "kind": "종류", "joke-hearers": "농담을 듣는 사람들",
         "pleasure": "즐거움", "cliff,": "절벽", "line": "구절"}

STORIES = [
    (3, [sc("문장 1~2", "😲", "Surprise = joke mechanism", "놀라움이 농담의 기본 — 세 번째 들으면 재미없어요"),
         sc("문장 3", "⚖️", "how much of a surprise", "농담하는 사람은 청중이 받아들일 놀라움이 얼마인지 판단해요")]),
    (5, [sc("문장 4", "🤔", "a series of assumptions", "청중이 무엇을 이해할지 짐작해야 해요"),
         sc("문장 5", "🏞️", "leap a canyon with the audience", "농담하기 = 청중을 데리고 협곡을 뛰어넘기")]),
]

OPTIONS = [
    ("1", "if they feel relaxed enough to laugh", ["relaxed"], "웃을 수 있을 만큼 충분히 편안하다고 느낄 때", False),
    ("2", "when it matches their expectations", ["matches", "expectations"], "그것이 자신의 예상과 일치할 때", False),
    ("3", "if it is about someone else", ["someone else"], "그것이 다른 사람에 관한 것일 때", False),
    ("4", "if they have to do a little work", ["a little work"], "약간의 노력을 해야 할 때", True),
    ("5", "when they fail to fully understand it", ["fail", "fully understand"], "그것을 완전히 이해하지 못할 때", False),
]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오. [3점]",
    "underline": "________", "sentence": 9, "analysis_first": True, "wrong_rate": 73.0, "wrong_rank": 1,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("feel relaxed", "편안하다고 느끼다"), g("enough to laugh", "웃을 수 있을 만큼"), g("matches", "일치하다, 맞다"),
                g("expectations", "예상, 기대"), g("someone else", "다른 사람"), g("have to", "~해야 하다"),
                g("do a little work", "약간의 노력을 하다"), g("fail to", "~하지 못하다"), g("fully understand", "완전히 이해하다")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "표의 가운데, 짜릿한 도약을 떠올리며 골라 봐요.",
        "정답이에요! 너무 가까우면 그냥 걸어 건너고, 너무 멀면 못 건너요. 청중이 약간 애써서 틈을 뛰어 건널 때 가장 즐거워요.",
        "정답은 ④예요. 두 절벽이 너무 가까우면 도약이 없고, 너무 멀면 건너지 못해요. 청중이 조금 노력해서 뛰어 건널 때 즐거움이 커요.",
        {"1": "relaxed는 4문장에서 농담하는 사람이 짐작하는 것 중 하나예요. 즐거움은 편안함이 아니라 짜릿한 도약에서 와요.",
         "2": "예상과 맞으면 놀라움이 없어요. 두 절벽이 너무 가까워 그냥 걸어 건너는 쪽이에요.",
         "3": "누구에 관한 농담인지는 글에 없어요. 글은 놀라움의 크기 이야기예요.",
         "5": "끝까지 이해하지 못하면 두 절벽이 너무 먼 쪽이에요. 건너편에 닿지 못하면 즐거움도 없어요."},
        {"2": review(25,
                     "②는 '예상과 맞으면 즐겁다'는 상식처럼 들려서 끌려요. 하지만 글은 놀라움(surprise)이 농담의 기본이라고 했어요.\n예상과 딱 맞으면 두 절벽이 너무 가까워 그냥 걸어 건널 뿐, 짜릿한 도약이 없어요.",
                     panel=rows(("1·2문장", "Surprise is the fundamental joke mechanism", "놀라움이 농담의 기본", "hl"),
                                ("8문장", "too close together → just steps across the gap", "다 예상됨 — 도약 없음", "hl2"),
                                ("②", "matches their expectations", "예상과 일치 — 너무 가까운 쪽", "hl2")),
                     rank_word="가장 많이 고른"),
         "1": review(24,
                     "①은 4문장에 relaxed(편안한)가 나와서 끌려요. 하지만 그건 농담하는 사람이 청중에 대해 짐작하는 것 중 하나예요.\n빈칸은 청중이 언제 더 즐거운지예요 — 7·8문장 협곡 비유가 답을 줘요.",
                     panel=rows(("4문장", "how relaxed they appear to be", "농담하는 사람이 짐작하는 것", "hl2"),
                                ("7·8문장", "not too far, not too close → a thrilling leap", "짜릿한 도약 — 즐거움", "hl")))}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(1·3·8)만 ──
EMPHASIS = {
    1: ["Surprise", "fundamental"],
    3: ["how much of a surprise"],
    7: ["too far apart"],
    8: ["too close together", "a thrilling leap"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
    if not _s.get("modifiers"):
        _s.pop("modifiers", None)
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 34번 (빈칸 추론, 3점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 같은 말 모으기 → 빈칸이 어느 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-joke-canyon.svg", ("Joke", "농담"), "+", ("Surprise", "놀라움"),
                                       "농담은 언제 가장 재미있을까?", "2026년 9월 모의평가 34번 도입 칠판"),
                      "alt": "칠판: Joke(농담) + Surprise(놀라움)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "같은 농담을 세 번 들으면 어떤가요? 이번 글은 농담과 놀라움 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 위치를 살펴보고 가면 좋아요. 빈칸은 글쓴이 의견과 동일할 수도 있고, 반대일 수도 있어요."}}],
    exam=exam,
    key_words={"passage": [g("fundamental", "기본적인"), g("mechanism", "작동 원리"), g("punch line", "농담의 결정적인 구절"),
                           g("rely on", "~에 의존하다"), g("element", "요소"), g("lie in", "~에 있다"),
                           g("be prepared to", "~할 준비가 되어 있다"), g("assumption", "가정"), g("reference point", "기준점"),
                           g("relaxed", "편안한"), g("compare A to B", "A를 B에 비유하다"), g("leap", "뛰어넘다; 도약"),
                           g("metaphorical", "은유적인"), g("cliff", "절벽"), g("make it", "도달하다"), g("gap", "틈"),
                           g("thrilling", "짜릿한")],
               "options": [g("match", "일치하다"), g("expectation", "예상"), g("fail to", "~하지 못하다")]},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법")
