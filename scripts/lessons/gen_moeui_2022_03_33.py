"""2022년 3월 고3 33번 레슨 + 대사를 만든다 (빈칸 추론, 3점). 오답률 47.0% · Top 8.

    py scripts/lessons/gen_moeui_2022_03_33.py   (→ node scripts/policy_copy.mjs stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸 위치 먼저 → 처음부터 읽으며 재진술 모으기 → 빈칸이 같은 쪽/반대 쪽 → 바꿔 쓴 보기.
빈칸이 둘째 문장(앞쪽)이라 빈칸 문장에서는 「같은 쪽/반대 쪽」만 잡고, 뒤 문장에서 같은 말을 모은 뒤 끝에서 「빈칸에 올 말」 3지.
정답 ① alter the course of their lives. 많이 고른 오답 ② possess more than other people 17%
(셋째 문장 people possess a need의 possess가 겹치고, drive를 '욕심'으로 읽기 쉬움) — option_review로.
열쇠: not content with(변화·도전 없는 삶에 만족 못 함) ↔ pulled forward · invent motives and purposes · rise above ·
creators · active shapers of their own destiny · generate their own purposes. 칠판 두 쪽 = 벗어나려는 삶 ↔ 원하는 것.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
transcend는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt) — drive = 욕구, consume = 다 쓰다,
accidental if not random = 마구잡이는 아니더라도 우연한, be driven to = ~하도록 이끌리다. vision은 해설지가 '통찰력'으로 옮김.
반영한 규칙: 2026-10-20 끊어읽기(slashes·roles·modifiers)까지. 초급 기본(add_basic)은 짧은 문장(3)만.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic,  # noqa: E402
                      topic_svg, base_lesson, exam_brief, review, finish)

ID = "moeui-2022-03-33-creators-of-destiny"

BLANK = ("Allport considers it normal to be pulled forward by a vision of the future that awakened within persons "
         "their drive to ________.")
S = [
    "Gordon Allport argued that history records many individuals who were not content with an existence that offered them "
    "little variety, a lack of psychic tension, and minimal challenge.",
    BLANK,
    "He suggests that people possess a need to invent motives and purposes that would consume their inner energies.",
    "Similarly, Erich Fromm proposed a need on the part of humans to rise above the roles of passive creatures in an accidental "
    "if not random world.",
    "To him, humans are driven to transcend the state of merely having been created; instead, humans seek to become the creators, "
    "the active shapers of their own destiny.",
    "Rising above the passive and accidental nature of existence, humans generate their own purposes and thereby provide themselves "
    "with a true basis of freedom.",
]
KO = [
    "Gordon Allport는 다양성이 거의 없고 심적 긴장이 결핍되어 있으며 최소한의 도전만을 제공하는 생활에 만족하지 못한 많은 개개인을 역사가 기록하고 있다고 주장했다.",
    "Allport는 인간의 내면에서 ________ 욕구를 일깨운 미래에 대한 통찰력에 의해 앞으로 나아가게 되는 것이 정상이라고 여긴다.",
    "그는 사람들이 내면의 에너지를 다 쓸 동기와 목적을 만들어 내려는 욕구를 지니고 있다고 말한다.",
    "마찬가지로 Erich Fromm은 인간에게는 마구잡이는 아니더라도 우연한 세계에서 수동적인 피조물의 역할을 넘어서고 싶은 욕구가 있다고 제시했다.",
    "그에게, 인간은 단지 창조된 상태를 넘어서도록 이끌리지만, 대신에, 창조자, 즉 자신의 운명을 만드는 적극적인 행위자가 되려고 노력하는 존재이다.",
    "존재의 수동적이고 우연한 본질을 넘어서서, 인간은 자신만의 목적을 만들어 내고 그렇게 함으로써 자신에게 자유의 진정한 토대를 제공한다.",
]

DULL = "왼쪽 · 만족 못 하는 삶"
WANT = "오른쪽 · 사람들의 욕구"


def board(left, right, fresh=(), sort=None):
    """칠판 — 왼쪽 만족 못 하는 삶(벗어나려는 것), 오른쪽 사람들의 욕구. 묶음 이름은 1·2문장에서 나온 말까지만"""
    return groups("만족 못 하는 삶 ↔ 욕구", "만족 못 하는 삶 (not content with)", left, "사람들의 욕구 (drive)", right,
                  fresh=fresh, between="↔", sort={"words": sort, "left": DULL, "right": WANT} if sort else None)


L1 = [("little variety", "변화가 거의 없음"), ("minimal challenge", "최소한의 도전")]
R2 = [("pulled forward", "앞으로 이끌림")]
R3 = R2 + [("invent motives and purposes", "동기와 목적을 만들어 냄")]
L4 = L1 + [("passive creatures", "수동적인 피조물")]
R4 = R3 + [("rise above", "넘어서다")]
L5 = L4 + [("merely having been created", "그저 창조된 상태")]
R5 = R4 + [("the creators", "창조자"), ("active shapers of their own destiny", "자기 운명을 만드는 적극적인 사람")]
R6 = R5 + [("generate their own purposes", "자기 목적을 만들어 냄")]

BLANK_GLOSSES = [g("Allport", "올포트 · 미국의 심리학자"), g("considers it normal", "~을 정상이라고 여긴다"),
                 g("to be pulled forward", "앞으로 이끌려 가는 것"), g("by a vision of the future", "미래에 대한 비전(그려 보는 모습)에 의해"),
                 g("that awakened", "~을 일깨운"), g("within persons", "사람들 내면에서"), g("their drive to", "~하려는 그들의 욕구")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Gordon Allport", "고든 올포트 · 미국의 심리학자"), g("argued", "주장했다"), g("history", "역사"),
                    g("records", "기록한다 · 여기서는 동사예요"), g("many individuals", "많은 개인들"),
                    g("who were not content with", "~에 만족하지 못했던"), g("an existence", "생활, 삶"),
                    g("that offered them", "그들에게 ~을 준"), g("little variety", "변화(다양성)가 거의 없음"),
                    g("a lack of psychic tension", "마음의 긴장(자극)이 없음"), g("minimal challenge", "최소한의 도전"),
                    *BLANK_GLOSSES],
        "slashes": ["Gordon Allport argued", "many individuals", "with an existence", "little variety,", "psychic tension,"],
        "roles": [r("Gordon Allport", "S"), r("argued", "V"), r("history", "S"), r("records", "V"), r("many individuals", "O")],
        "modifiers": ["who were not content with an existence that offered them little variety, a lack of psychic tension, and minimal challenge"],
        "steps": [
            show("s1_passage", "빈칸은 여기, 둘째 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "미래를 그려 보면 사람은 ____하려는 마음을 잃는다", False),
                    ("o1", "미래에 대한 비전이 ____하려는 욕구를 깨워 사람을 앞으로 이끄는 게 정상이다", True),
                    ("o2", "미래를 걱정하며 ____하려는 마음을 누르는 게 정상이다", False)],
                   "drive는 여기서 '운전'이 아니라 '욕구'예요. pulled forward는 '앞으로 이끌려 가다'예요.",
                   why="considers it normal to be pulled forward는 '앞으로 이끌려 가는 걸 정상이라고 여긴다'예요. 미래에 대한 비전이 마음속 ____하려는 욕구(drive)를 깨운대요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["normal", "pulled forward", "drive", "________"],
                   tips=[tip("consider it + 형용사 + to ~", "'~하는 것을 (형용사)라고 여기다'예요. it은 뒤의 to ~를 대신 받아요.", "considers it normal"),
                         tip("drive", "'운전하다'만 있는 게 아니에요. 명사로 '욕구, 충동'이에요. drive to ~ = ~하려는 욕구.", "drive")]),
            show("s1_where", "그럼 사람들이 어떤 욕구를 가졌다는 건지 생각하며 문장 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0),
            sv("s1_sv", ["Gordon Allport", "argued", "history", "records"],
               {"Gordon Allport": "S", "argued": "V"},
               {"history": "그건 that 뒤, 주장한 내용 안의 주어예요. 먼저 바깥 문장을 봐요.",
                "records": "그건 that 뒤, 주장한 내용 안의 동사예요."},
               "주어는 Gordon Allport, 동사는 argued예요. that 뒤가 주장한 내용이에요.",
               ask="먼저 바깥 문장의 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s1_content",
                   "who 뒤를 봐요. 역사에 기록된 많은 사람들은 어떤 사람들이었대요?",
                   [("o0", "변화도 도전도 거의 없는 삶에 만족하지 못한 사람들", True),
                    ("o1", "조용하고 편안한 삶에 만족한 사람들", False),
                    ("o2", "너무 많은 도전에 지친 사람들", False)],
                   "be content with는 '~에 만족하다'예요. 앞에 not이 있어요.",
                   why="'not content with an existence that offered them little variety … and minimal challenge', 변화(variety)도 도전(challenge)도 거의 없는 삶에 만족하지 못했대요.",
                   highlight=["not content with", "little variety", "minimal challenge"],
                   tips=[tip("be content with", "content는 '내용'만 있는 게 아니에요. be content with ~ = ~에 만족하다. not content with = 만족하지 못하는.", "content", trap=True)]),
            show("s1_board", "변화도 도전도 없는 삶에 만족 못 한 사람이 많았대요.",
                 panel=board(L1, [], fresh=("little variety", "minimal challenge")), button="다음 문장"),
        ],
    },
    {
        "id": 2, "text": BLANK, "model_translation": KO[1], "teaching_value": "high",
        "glosses": list(BLANK_GLOSSES) + [g("considers", "여기다"), g("it", "그것 (뒤의 to ~를 받음)"), g("normal", "정상적인, 보통의"),
                                          g("a vision", "비전, 그려 보는 모습"), g("persons", "사람들")],
        "slashes": ["considers it normal", "pulled forward", "of the future", "within persons"],
        "roles": [r("Allport", "S"), r("considers", "V"), r("it", "O"), r("normal", "C")],
        "modifiers": ["that awakened within persons their drive to ________"],
        "steps": [
            sv("s2_sv", ["Allport", "considers", "it", "normal", "a vision", "persons"],
               {"Allport": "S", "considers": "V", "it": "O", "normal": "C"},
               {"a vision": "그건 by(~에 의해) 뒤 덩어리예요.", "persons": "그건 within(~ 안에서) 뒤 덩어리예요."},
               "주어 Allport, 동사 considers, 목적어 it, 보어 normal이에요. it은 뒤의 to be pulled forward를 받아요.",
               ask="빈칸 문장이에요. 주어(S), 동사(V), 목적어(O), 보어(C)를 찾아볼까요?"),
            choice("s2_side",
                   "빈칸은 Allport가 정상(normal)이라고 본 욕구예요. 칠판 왼쪽 삶과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 — 변화 없는 삶에 머무르려는 욕구", False),
                    ("o1", "반대 쪽 — 그런 삶에서 벗어나 앞으로 나아가려는 욕구", True)],
                   "not content with(만족 못 함)와 pulled forward(앞으로 이끌림)를 나란히 봐요.",
                   why="사람들은 변화 없는 삶에 만족 못 하고, 미래에 이끌려 앞으로 나아간대요. 빈칸 욕구는 왼쪽 삶과 반대 쪽이에요.",
                   highlight=["normal", "pulled forward"], signs=[{"text": "normal", "sign": "+"}],
                   panel=board(L1, [])),
            show("s2_board", "빈칸은 Allport가 좋게 본(+) 욕구예요. 이 욕구를 다른 말로 한 표현을 칠판 오른쪽에 모으며 읽어 봐요.",
                 panel=board(L1, R2, fresh=("pulled forward",)), highlight=["pulled forward"], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("He", "그(Allport)는"), g("suggests", "말한다, 제안한다"), g("people", "사람들"), g("possess", "가지고 있다"),
                    g("a need", "욕구, 필요"), g("to invent", "만들어 내려는"), g("motives and purposes", "동기와 목적"),
                    g("invent motives and purposes", "동기와 목적을 만들어 내다"),
                    g("that would consume", "~을 다 쓰게 할"), g("their inner energies", "그들 내면의 에너지")],
        "slashes": ["He suggests", "possess a need", "motives and purposes"],
        "roles": [r("He", "S"), r("suggests", "V"), r("people", "S"), r("possess", "V"), r("a need", "O")],
        "modifiers": ["that would consume their inner energies"],
        "steps": [
            choice("s3_sort",
                   "'invent motives and purposes(동기와 목적을 만들어 내다)'는 칠판 어느 쪽일까요?",
                   [("o0", DULL, False), ("o1", WANT, True)],
                   "people possess a need to invent ~ — 사람들에게 있는 욕구(need)예요.",
                   why="'people possess a need to invent motives and purposes', 사람에게는 스스로 동기와 목적을 만들어 내려는 욕구가 있대요. 욕구 쪽이에요.",
                   highlight=["need", "invent motives and purposes"],
                   panel=board(L1, R2, sort=["invent motives and purposes"]),
                   tips=[tip("consume", "'먹다, 소비하다'예요. 여기선 내면의 에너지를 '다 쏟게 하는'이에요.", "consume")]),
            show("s3_board", "need(욕구)는 앞 문장의 drive와 같은 말이에요. 스스로 동기와 목적을 만들어 내려는 욕구래요.",
                 highlight=["need"], panel=board(L1, R3, fresh=("invent motives and purposes",)), button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Similarly", "마찬가지로"), g("Erich Fromm", "에리히 프롬 · 독일 출신의 심리학자"), g("proposed", "제시했다"),
                    g("a need", "욕구"), g("on the part of humans", "인간 쪽의, 인간에게"), g("humans", "인간"),
                    g("to rise above", "~을 넘어서려는"), g("rise above", "~을 넘어서다"), g("the roles", "역할"),
                    g("passive creatures", "수동적인 피조물"), g("in an accidental if not random world", "마구잡이는 아니더라도 우연한 세상에서"),
                    g("accidental", "우연한"), g("if not", "~까지는 아니더라도"), g("random", "마구잡이의, 무작위의")],
        "slashes": ["Similarly,", "proposed a need", "on the part of humans", "to rise above", "passive creatures"],
        "roles": [r("Erich Fromm", "S"), r("proposed", "V"), r("a need", "O")],
        "steps": [
            sv("s4_sv", ["Erich Fromm", "proposed", "a need", "humans", "passive creatures"],
               {"Erich Fromm": "S", "proposed": "V", "a need": "O"},
               {"humans": "그건 on the part of(~ 쪽의) 뒤 덩어리예요.", "passive creatures": "그건 the roles of 뒤 덩어리예요."},
               "주어 Erich Fromm, 동사 proposed, 목적어 a need예요. a need는 뒤의 to rise above와 이어져요.",
               ask="주어(S), 동사(V), 목적어(O)를 찾아볼까요?"),
            choice("s4_rise",
                   "Similarly(마찬가지로) — Fromm도 비슷한 말을 해요. 인간에게 어떤 욕구가 있대요?",
                   [("o0", "수동적인 역할을 잘 해내려는 욕구", False),
                    ("o1", "수동적인 피조물의 역할을 넘어서려는 욕구", True),
                    ("o2", "우연한 세상을 피해 숨으려는 욕구", False)],
                   "rise above는 '~을 넘어서다'예요. a need ~ to rise above로 이어서 읽어요.",
                   why="'a need … to rise above the roles of passive creatures', 수동적인 피조물의 역할을 넘어서고 싶어 한대요.",
                   highlight=["Similarly", "rise above", "passive creatures"],
                   tips=[tip("a need … to ~", "need와 to ~ 사이에 on the part of humans가 끼어 있어요. a need to rise above = 넘어서려는 욕구.", "on the part of humans"),
                         tip("A if not B", "'B까지는 아니더라도 A'예요. accidental if not random = 마구잡이는 아니더라도 우연한.", "if not")]),
            show("s4_board", "passive creatures(수동적인 피조물)는 왼쪽, rise above(넘어서다)는 오른쪽이에요.",
                 panel=board(L4, R4, fresh=("passive creatures", "rise above")), button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("To him", "그(Fromm)에게"), g("humans", "인간"), g("are driven", "이끌린다, 내몰린다"),
                    g("to transcend", "넘어서도록"), g("transcend", "초월하다, 넘어서다"), g("the state", "상태"),
                    g("merely having been created", "그저 창조된 것"), g("instead", "대신에"), g("seek", "~하려고 애쓰다"),
                    g("to become the creators", "창조자가 되기를"), g("the creators", "창조자"),
                    g("the active shapers of their own destiny", "자기 운명을 만드는 적극적인 사람"),
                    g("active shapers of their own destiny", "자기 운명을 만드는 적극적인 사람")],
        "slashes": ["To him,", "are driven", "merely having been created;", "instead,", "the creators,"],
        "roles": [r("humans … humans", "S"), r("are driven", "V"), r("seek", "V"), r("to become the creators", "O")],
        "steps": [
            sv("s5_sv", ["To him", "humans", "are driven", "the state"],
               {"humans": "S", "are driven": "V"},
               {"To him": "그건 '그에게는'이라고 앞에 붙은 말이에요.", "the state": "그건 to transcend(넘어서도록) 뒤의 말이에요."},
               "주어 humans, 동사 are driven이에요. 세미콜론(;) 뒤 instead 문장도 주어는 humans, 동사는 seek예요.",
               ask="세미콜론(;) 앞에서 주어(S)와 동사(V)를 찾아볼까요?"),
            choice("s5_become",
                   "instead(대신에) 뒤를 봐요. 인간은 무엇이 되려고 한대요?",
                   [("o0", "창조된 그대로 머무는 존재", False),
                    ("o1", "창조자, 자기 운명을 스스로 만드는 사람", True),
                    ("o2", "남의 운명을 이끄는 지도자", False)],
                   "seek to become은 '~이 되려고 애쓰다'예요. 콤마(,) 뒤가 the creators를 다시 풀어 줘요.",
                   why="'seek to become the creators, the active shapers of their own destiny', 창조자, 즉 자기 운명을 만드는 적극적인 사람이 되려 한대요.",
                   highlight=["instead", "the creators", "active shapers", "own destiny"],
                   tips=[tip("A, B (같은 말 풀어 쓰기)", "콤마(,) 뒤 B가 앞의 A를 다시 풀어 줘요. the creators, the active shapers ~ = 창조자, 즉 ~을 만드는 사람.", "the active shapers"),
                         tip("be driven to ~", "'~하도록 이끌리다, 내몰리다'예요.", "are driven")]),
            show("s5_board", "그저 창조된 상태는 왼쪽, 창조자·자기 운명을 만드는 사람은 오른쪽이에요.",
                 panel=board(L5, R5, fresh=("merely having been created", "the creators", "active shapers of their own destiny")),
                 button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Rising above", "~을 넘어서면서"), g("the passive and accidental nature", "수동적이고 우연한 본질"),
                    g("of existence", "존재의"), g("humans", "인간은"), g("generate", "만들어 낸다"),
                    g("their own purposes", "자기 자신의 목적"), g("generate their own purposes", "자기 목적을 만들어 내다"),
                    g("and thereby", "그리고 그렇게 함으로써"), g("provide", "준다"), g("themselves", "자신에게"),
                    g("with a true basis of freedom", "자유의 진정한 토대를"), g("nature", "본질, 성질")],
        "slashes": ["nature of existence,", "humans generate", "their own purposes", "provide themselves"],
        "roles": [r("humans", "S"), r("generate", "V"), r("their own purposes", "O"), r("provide", "V"), r("themselves", "O")],
        "steps": [
            sv("s6_sv", ["the passive and accidental nature", "humans", "generate", "their own purposes", "provide"],
               {"humans": "S", "generate": "V", "their own purposes": "O", "provide": "V"},
               {"the passive and accidental nature": "그건 콤마 앞 Rising above(~을 넘어서면서) 덩어리 안의 말이에요. 주어가 아니에요."},
               "주어 humans, 동사 generate와 provide, generate의 목적어는 their own purposes예요.",
               ask="콤마 뒤에서 주어(S), 동사(V) 둘, 목적어(O)를 찾아볼까요?"),
            show("s6_board", "Rising above는 앞의 rise above를 또 말해요. 자기 목적을 스스로 만들어 내고, 그래서 자유를 얻는대요.",
                 highlight=["Rising above", "generate", "freedom"],
                 panel=board(L5, R6, fresh=("generate their own purposes",)),
                 tips=[tip("thereby", "'그렇게 함으로써'예요. 앞의 일 덕분에 뒤의 일이 생겨요.", "thereby")]),
            choice("s6_what",
                   "빈칸 문장으로 돌아가요. 칠판 오른쪽 말을 보면, 빈칸에는 어떤 욕구가 와야 할까요?",
                   [("o0", "주어진 대로 조용히 살려는 욕구", False),
                    ("o1", "자기 삶을 스스로 만들어 가려는 욕구", True),
                    ("o2", "남에게 인정받으려는 욕구", False)],
                   "칠판 오른쪽의 creators, active shapers of their own destiny를 봐요.",
                   why="사람은 수동적인 삶을 넘어 창조자, 자기 운명을 만드는 사람이 되려 한대요. 빈칸 욕구도 그 말이에요.",
                   display=BLANK, tag="빈칸 문장", highlight=["drive", "________"], panel=board(L5, R6)),
            show("s6_go", "칠판 오른쪽 말(creators, active shapers of their own destiny)을 다른 말로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요", panel=board(L5, R6)),
        ],
    },
]

add_basic(sentences, 3, [m("He suggests", "그는 말한다"), " ", m("people possess a need", "사람들이 욕구를 가지고 있다고"), " — ",
                         m("invent motives and purposes", "동기와 목적을 만들어 내려는"), "."],
          match_display="He suggests that people possess a need to invent motives and purposes.",
          sv_new=sv_step("s3_basic_sv", ["He", "suggests", "people", "possess", "a need"],
                         {"He": "S", "suggests": "V"},
                         {"people": "그건 that 뒤, 말한 내용 안의 주어예요. 먼저 바깥 문장을 봐요.",
                          "possess": "그건 that 뒤, 말한 내용 안의 동사예요.", "a need": "그건 that 뒤, 말한 내용 안의 목적어예요."},
                         "바깥 문장은 주어 He, 동사 suggests예요. that 뒤가 말한 내용이에요."),
          meaning_after="s3_sort")

SENSES = {
    1: [sense("that", "argued that", "~라고", "명사절 that (argue that …)"),
        sense("that", "existence that offered", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    2: [sense("to", "normal to be pulled", "~하는 것 (it이 받는 말)", "가목적어 it … 진목적어 to부정사"),
        sense("that", "the future that awakened", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("to", "drive to", "~하려는 (욕구)", "명사 + to부정사")],
    3: [sense("that", "suggests that", "~라고", "명사절 that (suggest that …)"),
        sense("to", "a need to invent", "~하려는 (욕구)", "명사 + to부정사"),
        sense("that", "purposes that would consume", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    4: [sense("to", "to rise above", "~하려는 (욕구)", "a need … to부정사 (사이에 on the part of humans)"),
        sense("if", "accidental if not random", "~까지는 아니더라도", "A if not B")],
    5: [sense("to", "To him", "~에게는", "전치사 to + 사람"),
        sense("to", "driven to transcend", "~하도록", "be driven + to부정사"),
        sense("to", "seek to become", "~하려고 (애쓰다)", "seek + to부정사")],
}

WORDS = {"gordon": "고든 (이름)", "allport": "올포트 (이름)", "argued": "주장했다", "history": "역사", "records": "기록하다",
         "individuals": "개인들", "content": "만족하는", "existence": "생활, 존재", "offered": "주었다", "variety": "변화, 다양성",
         "lack": "부족, 없음", "psychic": "마음의, 정신적인", "tension": "긴장", "minimal": "최소한의", "challenge": "도전",
         "considers": "여기다", "normal": "정상적인", "pulled": "끌린", "forward": "앞으로", "vision": "비전, 그려 보는 모습",
         "future": "미래", "awakened": "일깨웠다", "persons": "사람들", "drive": "욕구", "suggests": "말한다", "possess": "가지다",
         "need": "욕구", "invent": "만들어 내다", "motives": "동기", "purposes": "목적", "consume": "다 쓰다, 소비하다",
         "inner": "내면의", "energies": "에너지", "similarly": "마찬가지로", "erich": "에리히 (이름)", "fromm": "프롬 (이름)",
         "proposed": "제시했다", "part": "쪽, 부분", "humans": "인간", "rise": "오르다 · rise above = 넘어서다", "above": "~ 위로",
         "roles": "역할", "passive": "수동적인", "creatures": "피조물, 생물", "accidental": "우연한", "random": "마구잡이의",
         "world": "세상", "driven": "이끌린", "transcend": "초월하다", "state": "상태", "merely": "그저, 단지", "created": "창조된",
         "instead": "대신에", "seek": "~하려고 애쓰다", "become": "~이 되다", "creators": "창조자", "active": "적극적인",
         "shapers": "만드는 사람", "destiny": "운명", "rising": "넘어서는", "nature": "본질", "generate": "만들어 내다",
         "thereby": "그렇게 함으로써", "provide": "주다", "themselves": "자신에게", "true": "진정한", "basis": "토대, 기초",
         "freedom": "자유", "own": "자기 자신의", "little": "거의 없는"}

STORIES = [
    (3, [sc("문장 1", "😑", "not content with little variety", "변화도 도전도 없는 삶에 만족 못 한 사람이 많았어요"),
         sc("문장 2~3", "🔭", "drive to ____ · invent motives and purposes", "미래가 ____하려는 욕구를 깨워요 — 사람은 스스로 동기와 목적을 만들어요")]),
    (5, [sc("문장 4~5", "🎨", "rise above passive creatures → the creators", "수동적인 피조물을 넘어 자기 운명을 만드는 창조자가 되려 해요")]),
]

OPTIONS = [
    ("1", "alter the course of their lives", ["alter", "course of their lives"], "자기 삶의 행로를 바꾸려는", True),
    ("2", "possess more than other people", ["possess more", "other people"], "다른 사람들보다 더 많이 소유하려는", False),
    ("3", "suppress their negative emotions", ["suppress", "negative emotions"], "자신의 부정적인 감정을 억누르려는", False),
    ("4", "sacrifice themselves for noble causes", ["sacrifice themselves", "noble causes"], "숭고한 대의명분을 위해 자신을 희생하려는", False),
    ("5", "show admiration for supernatural power", ["admiration", "supernatural power"], "초자연적인 힘에 대해 존경심을 보이려는", False),
]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오. [3점]",
    "underline": "________", "sentence": 2, "analysis_first": True, "wrong_rate": 47.0, "wrong_rank": 8,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("alter", "바꾸다"), g("the course of their lives", "그들 삶의 행로(방향)"), g("possess", "소유하다"),
                g("more than other people", "다른 사람들보다 더 많이"), g("suppress", "억누르다"), g("negative emotions", "부정적인 감정"),
                g("sacrifice themselves", "자신을 희생하다"), g("noble causes", "숭고한 대의"), g("admiration", "존경, 감탄"),
                g("supernatural power", "초자연적인 힘")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "빈칸은 변화 없는 삶과 반대 쪽 욕구예요. 칠판 오른쪽 말을 떠올리며 골라 봐요.",
        "정답이에요! 사람은 수동적인 삶을 넘어 자기 운명을 스스로 만들려 해요. 그걸 '자기 삶의 행로를 바꾸려는'으로 바꿔 썼어요.",
        "정답은 ①이에요. 창조자, 자기 운명을 만드는 사람(active shapers of their own destiny)을 바꿔 쓴 말이에요.",
        {"2": "possess가 셋째 문장에 나와서 헷갈렸죠. 하지만 글에는 남과 비교해 더 갖는다는 말이 없어요.",
         "3": "부정적인 감정 이야기는 글에 없어요. 글은 수동적인 삶을 넘어서는 이야기예요.",
         "4": "남을 위한 희생 이야기는 글에 없어요. 자기 목적(their own purposes)을 만든다고 했어요.",
         "5": "초자연적인 힘 이야기는 없어요. 오히려 인간 스스로 창조자가 되려 한다고 했어요."},
        {"2": review(17,
                     "②의 possess는 셋째 문장(people possess a need)에도 나와서 겹쳐 보여요. 하지만 거기서 possess는 '욕구를 지니고 있다'는 말이에요. 글은 남보다 많이 갖는 게 아니라, 수동적인 삶을 넘어 자기 운명을 만드는 이야기예요.",
                     panel=rows(("글의 말", "the active shapers of their own destiny", "자기 운명을 만드는 사람 — 삶을 바꿈", "hl"),
                                ("②", "possess more than other people", "남보다 더 많이 가지기 — 글에 없는 비교", "hl2")))}),
}

# ── 해석 맞추기(모두에게)·가리키는 말 — 2026-10-20 엔진: S·V 찾기·핵심어 자유 해석은 빠지고 맞추기가 대신 나온다 ──
from beginner import add_match, add_refers, m as _m  # noqa: E402
add_match(sentences, 1, [_m("Gordon Allport", "Gordon Allport는"), " ", _m("argued", "주장했다"), " — 역사가 변화 없는 생활", _m("who were not content with", "에 만족하지 못한"), " ",
                         _m("many individuals", "많은 개개인을"), " ", _m("records", "기록한다고"), "."],
          display="Gordon Allport argued that history records many individuals who were not content with an existence that offered them little variety and minimal challenge.")
add_match(sentences, 2, [_m("Allport", "Allport는"), " ", _m("by a vision of the future", "미래에 대한 통찰력에 의해"), " ", _m("to be pulled forward", "앞으로 나아가게 되는"), " 것을 ",
                         _m("normal", "정상이라고"), " ", _m("considers", "여긴다"), "."])
add_match(sentences, 4, [_m("Erich Fromm", "Erich Fromm은"), " 인간에게 ", _m("passive creatures", "수동적인 피조물"), "의 역할을 ", _m("to rise above", "넘어서고 싶은"), " ",
                         _m("a need", "욕구를"), " 있다고 ", _m("proposed", "제시했다"), "."])
add_match(sentences, 5, [_m("To him", "그에게"), ", ", _m("humans", "인간은"), " 창조된 상태를 ", _m("to transcend", "넘어서도록"), " ", _m("are driven", "이끌린다"),
                         " — 대신 자기 운명의 ", _m("to become the creators", "창조자가 되려고"), " 노력한다."],
          display="To him, humans are driven to transcend the state of merely having been created; instead, humans seek to become the creators of their own destiny.")
add_match(sentences, 6, ["존재의 수동적 본질을 ", _m("Rising above", "넘어서서"), ", ", _m("humans", "인간은"), " ", _m("their own purposes", "자신만의 목적을"), " ",
                         _m("generate", "만들어 내고"), " 자유의 토대를 ", _m("provide", "제공한다"), "."])
add_refers(sentences, 2, {"it": "to be pulled forward by a vision of the future(미래의 통찰에 이끌리는 것 — 가목적어)"})
add_refers(sentences, 3, {"He": "Allport"})
add_refers(sentences, 5, {"To him": "to Erich Fromm(Fromm에게)"})

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 33번 (빈칸 추론, 3점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 두 쪽 말 모으기 → 빈칸이 어느 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-creators-of-destiny.svg", ("Same old life", "변화 없는 삶"), "→",
                                       ("Something more", "그 이상의 무언가"),
                                       "사람은 왜 지루한 삶에 만족하지 못할까?", "2022년 3월 33번 도입 칠판"),
                      "alt": "칠판: Same old life(변화 없는 삶) → Something more(그 이상의 무언가)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "변화도 도전도 없는 하루가 계속되면 어떤 기분일까요? 이번 글은 사람이 가진 욕구에 대한 심리학자들의 생각이에요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 위치를 살펴보고 가면 좋아요. 빈칸은 글쓴이 의견과 동일할 수도 있고, 반대일 수도 있어요."}}],
    exam=exam,
    key_words={"passage": [g("be content with", "~에 만족하다"), g("existence", "생활, 존재"), g("variety", "다양성, 변화"),
                           g("minimal", "최소한의"), g("drive", "욕구, 충동"), g("possess", "가지다"), g("motive", "동기"),
                           g("consume", "다 쓰다, 소비하다"), g("rise above", "~을 넘어서다"), g("passive", "수동적인"),
                           g("creature", "피조물, 생물"), g("accidental", "우연한"), g("be driven to", "~하도록 이끌리다"),
                           g("destiny", "운명"), g("generate", "만들어 내다"), g("thereby", "그렇게 함으로써")],
               "options": [g("alter", "바꾸다"), g("suppress", "억누르다"), g("sacrifice", "희생하다"), g("noble", "숭고한"),
                           g("admiration", "존경, 감탄"), g("supernatural", "초자연적인")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# drive 욕구 · nature 본질.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    2: [tip("drive", "이 글에서는 → 욕구  ('운전하다' 아님)", "drive", trap=True)],
    6: [tip("nature", "이 글에서는 → 본질  ('자연' 아님)", "nature", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법",
       chunks={"Gordon Allport": "고든 올포트", "argued": "주장했다", "history": "역사", "records": "기록한다",
               "Allport": "올포트", "considers": "여기다", "it": "그것", "normal": "정상적인", "a vision": "비전", "persons": "사람들",
               "He": "그는", "suggests": "말한다", "people": "사람들", "possess": "가지고 있다", "a need": "욕구",
               "Erich Fromm": "에리히 프롬", "proposed": "제시했다", "humans": "인간", "passive creatures": "수동적인 피조물",
               "To him": "그에게", "are driven": "이끌린다", "the state": "상태",
               "the passive and accidental nature": "수동적이고 우연한 본질", "generate": "만들어 낸다",
               "their own purposes": "자기 자신의 목적", "provide": "준다",
               "He suggests": "그는 말한다", "people possess a need": "사람들이 욕구를 가지고 있다",
               "invent motives and purposes": "동기와 목적을 만들어 내다"})
