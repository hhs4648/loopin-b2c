"""2026학년도 6월 모의평가 34번 레슨 + 대사를 만든다 (빈칸 추론, 3점).

레슨 JSON(content/tutor/policy-lessons/…)과 대사(content/tutor/policy-copy/dajung/…)는 이 스크립트의
생성물이다. 고칠 때는 여기를 고치고 다시 돌린 뒤 도장을 찍는다:

    python3 scripts/lessons/gen_mopyeong_2026_06_34.py
    npm run policy:copy stamp mopyeong-2026-06-34-geography-where

빈칸 푸는 법(33번과 같다): ① 빈칸 문장부터 보고 무엇을 찾을지 정하기 ② 문장마다 주어·동사(+목적어·보어)
찾고 핵심어 잡기 ③ 빈칸이 주장과 같은 쪽인지 반대 쪽인지 ④ 같은 말을 바꿔 쓴 보기 찾기.
이 글은 「공간(어디에, 어떻게 배치돼 있나)」이 계속 다른 말로 반복된다 — 단어 지도에 모은다.
정답 ② how phenomena are arranged on Earth’s surface (해설지로 확인 전). 오답률 자료 없음.
inextricably, premise는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니다.
"""
import sys
import copy
import json
import os

ID = "mopyeong-2026-06-34-geography-where"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def g(en, ko):
    return {"en": en, "ko": ko}


def choice(id, ask, options, hint, praise="맞아요!", method=0, why=None, **extra):
    """why: 틀렸을 때 「아쉽게도 틀렸어요.」 뒤의 이유 (없으면 힌트)"""
    feedback = {o[0]: why or hint for o in options if not o[2]}
    brief = {"ask": ask, "reask": "그럼 하나 골라 봐요.", "hints": [hint, hint], "explain": hint, "praise": praise, "feedback": feedback}
    if id in POINTS:
        brief["point"] = POINTS[id]
    return {
        "id": id, "type": "choice", "interaction": "meaning_choice", "one_try": True,
        "brief": brief,
        "options": [{"id": o[0], "label": o[1], **({"correct": True} if o[2] else {})} for o in options],
        "method": method, **extra,
    }


def show(id, say, method=0, button="다음", point=None, **extra):
    brief = {"say": say, **({"point": point} if point else {})}
    return {"id": id, "type": "show", "interaction": "note", "brief": brief, "method": method, "button": button, **extra}


def sv_pick(id, candidates, roles, ask, wrong_by, explain, wrong="그건 주어나 동사가 아니에요."):
    """읽기 끝나면 덩어리째 주어·동사(+목적어·보어) 찾기 — 찾은 건 표시로 남는다"""
    return {
        "id": id, "type": "pick", "interaction": "word_pick", "shade": True, "no_unknown": True,
        "candidates": candidates, "answers": list(roles), "roles": roles,
        "brief": {"ask": ask, "wrong": wrong, "wrong_by": wrong_by, "more": "좋아요! {n}개 남았어요.",
                  "praise": "다 찾았어요!", "explain": explain, **({"point": POINTS[id]} if id in POINTS else {})},
        "method": 0,
    }


def same_pick(id, candidates, answer, ask, wrong_by, praise):
    """단어 지도에 학생이 직접 넣는다 — 이 문장에서 앞의 말(where)과 같은 쪽 말을 찾아 누른다"""
    return {
        "id": id, "type": "pick", "interaction": "word_pick", "shade": True,
        "candidates": candidates, "answers": [answer],
        "brief": {"ask": ask, "wrong": "그건 '어디에, 어떻게 놓여 있나'와 같은 쪽 말이 아니에요.", "wrong_by": wrong_by,
                  "more": "좋아요! {n}개 남았어요.", "praise": praise,
                  "explain": f"{answer}가 where와 같은 쪽이에요. 어디에, 어떻게 놓여 있나를 말해요."},
        # 칠판은 찾은 다음에 — 찾는 동안 칠판이 문장을 가리면 안 된다
        "method": 0,
    }


POINTS = {
    "s1_where": "빈칸은 여섯째 문장 — without some awareness of ____, it is difficult to … = ____을 모르면 판단하기 어렵다",
    "s6_fill": "빈칸 = 앞에서 계속 나온 말(where, spatial arrangements, spatial circumstances) = 어디에 어떻게 놓여 있나",
    "s1_word": "지리학과 떼려야 뗄 수 없는 단어 = where(어디)",
    "s2_matters": "it matters where … = 어디에서 일어나는지가 중요하다 (it은 가주어)",
    "s3_key": "not simply A; B — 세미콜론 뒤 B(why there, so what)가 글쓴이 생각",
    "s4_what": "spatial arrangements = 공간 배치 (어디에 어떻게 놓여 있나)",
    "s5_appreciation": "appreciation = 감사가 아니라 '이해, 인식' · spatial circumstances = 공간적 상황",
    "s6_side": "without(없으면) → difficult(−) · 빈칸 = 꼭 알아야 하는 것 = 글쓴이 주장과 같은 쪽",
    "s7_examples": "가게 위치를 정할 때 인구 분포·도로 위치를 고려 = 모두 '어디에 어떻게 배치돼 있나'",
    "s8_gist": "글 전체 = 지리학은 '어디'에서 출발해, 공간 배치를 알아야 판단하고 이해할 수 있다",
}

BLANK_TEXT = ("Moving up in scale, without some awareness of ________, it is difficult to make reasoned business "
              "or policy judgments, make sense of events, or grasp some of the basic forces shaping life on the planet.")
S = [
    "One word is inextricably associated with geography: where.",
    "That is because geography starts from the premise that it matters where something takes place on Earth’s surface.",
    "The key questions are not simply “where” questions, though; they are “why there” and “so what” questions.",
    "Getting to such questions means taking spatial arrangements, variations, and interconnections seriously.",
    "Engaging in even the simplest day-to-day activity requires some appreciation of spatial circumstances ― where to find food and services, how to get to work places, and the like.",
    BLANK_TEXT,
    "Locating a new store or public service requires taking into consideration population distributions, the location of roads and utilities, socio-economic patterns, and more.",
    "Understanding why and where migration happens requires consideration of the political organization of territory, the spatial consequences of discrimination, socio-economic patterns, and the layout of the physical environment.",
]
# 해설지 없이 쓴 해석 — 해설을 받으면 맞춰 본다
KO = [
    "한 단어가 지리학과 떼려야 뗄 수 없이 연관되어 있는데, 그것은 '어디'이다.",
    "그것은 지리학이 지구 표면 위 어디에서 어떤 일이 일어나는지가 중요하다는 전제에서 출발하기 때문이다.",
    "그러나 핵심 질문은 단순히 '어디' 질문이 아니라, '왜 거기에'와 '그래서 무엇이' 질문이다.",
    "그러한 질문에 이르는 것은 공간적 배치, 차이, 상호 연결을 진지하게 받아들이는 것을 의미한다.",
    "가장 단순한 일상 활동에 참여하는 것조차도 공간적 상황에 대한 어느 정도의 이해를 필요로 하는데, 음식과 서비스를 어디에서 찾을지, 직장에 어떻게 갈지 등이 그렇다.",
    "규모를 키워 보면, ________에 대한 어느 정도의 인식 없이는 합리적인 사업적 또는 정책적 판단을 내리거나, 사건을 이해하거나, 지구상의 삶을 형성하는 기본적인 힘의 일부를 파악하기 어렵다.",
    "새 가게나 공공 서비스의 위치를 정하는 것은 인구 분포, 도로와 공공 설비의 위치, 사회 경제적 양식 등을 고려하는 것을 필요로 한다.",
    "이주가 왜 그리고 어디에서 일어나는지를 이해하는 것은 영토의 정치적 조직, 차별의 공간적 결과, 사회 경제적 양식, 물리적 환경의 배치를 고려하는 것을 필요로 한다.",
]

# 단어 지도 — 「공간(어디에, 어떻게 배치돼 있나)」이 다른 말로 계속 반복된다
SPACE = [("where", "어디"), ("spatial arrangements", "공간 배치"), ("spatial circumstances", "공간적 상황"),
         ("the location of roads", "도로의 위치"), ("the layout", "배치")]


def space_board(n, fresh=()):
    # 묶음 이름·아래 한 줄은 안 단다 — 단어만으로 충분하고, '어떻게 배치'는 정답 보기와 같은 말이라 미리 주면 안 된다 (2026-10-14 선생님)
    return {"kind": "groups", "title": "단어 지도",
            "left": {"label": "",
                     "words": [{"text": en, "ko": ko, **({"fresh": True} if en in fresh else {})} for en, ko in SPACE[:n]]}}


sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("One word", "한 단어"), g("is inextricably associated with", "~와 떼려야 뗄 수 없이 연관되어 있다"),
                    g("is associated with", "~와 연관되어 있다"), g("geography", "지리학"), g("where", "어디"),
                    g("Moving up in scale", "규모를 키워 보면"), g("without", "~ 없이는"), g("awareness", "인식, 앎"),
                    g("it is difficult to", "~하기 어렵다"), g("reasoned", "합리적인"), g("judgments", "판단"),
                    g("make sense of", "~을 이해하다"), g("grasp", "파악하다"), g("forces", "힘")],
        "steps": [
            # ① 지문 전체에서 빈칸 문장 위치만 — 「잠깐 볼까요」 정도로 (2026-10-14 선생님: 처음부터 설명은 어색)
            show("s1_passage", "빈칸은 여기, 여섯째 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK_TEXT]),
            # ② 빈칸 문장 — 핵심어만 칠하고 뜻을 고민하게
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "____을 알면 사업에 성공할 수 있다", False),
                    ("o1", "____을 모르면 판단하고 이해하기 어렵다", True),
                    ("o2", "____이 없어도 사건을 이해할 수 있다", False)],
                   "without은 '~ 없이', difficult는 '어려운'이에요.",
                   why="without(~ 없이)과 difficult(어려운)를 봐요. ____이 없으면 어렵다는 말이에요.",
                   before_read=True, display=BLANK_TEXT, tag="빈칸 문장",
                   highlight=["without", "awareness", "________"],
                   highlight_alt=["difficult", "judgments", "make sense of", "grasp"],
                   tips=[{"label": "grasp", "mark": "grasp",
                          "text": "grasp는 '(손으로) 잡다'와 '(뜻을) 이해하다, 파악하다' 두 뜻이 있어요. 여기서는 이해하다예요."}]),
            # ③ 중·초 — 세 덩어리가 같은 말(이해하다)이라는 것
            show("s1_where_map",
                 "judgments, make sense of, grasp는 모두 '이해하다'라는 같은 말을 반복한 거예요.",
                 button="다음", before_read=True, levels=["중", "초"],
                 display=BLANK_TEXT, tag="빈칸 문장",
                 highlight_alt=["judgments", "make sense of", "grasp"],
                 panel_below=True,
                 panel={"kind": "structure", "rows": [
                     {"label": "모르면", "text": "without some awareness of ____", "tone": "hl"},
                     {"label": "이해하기 어렵다", "text": "make judgments = make sense of = grasp", "ko": "세 덩어리 모두 '이해하다'", "tone": "hl2"},
                 ]}),
            # ④ 이걸 생각하며 처음부터
            show("s1_where",
                 "그럼 잘 판단하려면 무엇을 알아야 하는지 생각하면서 문장 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True,
                 # 첫 문장은 버튼을 누른 뒤에 — 이 말은 빈칸 문장을 띄운 채로
                 display=BLANK_TEXT, tag="빈칸 문장"),
            sv_pick("s1_sv", ["One word", "is inextricably associated", "geography", "where"],
                    {"One word": "S", "is inextricably associated": "V", "geography": "전목"},
                    "첫 문장의 주어(S), 동사(V), 그리고 with 뒤의 목적어(전목)를 찾아볼까요?",
                    {"where": "콜론(:) 뒤에서 그 단어가 무엇인지 알려 주는 말이에요."},
                    "주어는 One word, 동사는 is inextricably associated, with 뒤 목적어는 geography예요.",
                    wrong="그건 주어·동사·목적어가 아니에요."),
            # One word가 가리키는 것 — 콜론 뒤
            {
                "id": "s1_word", "type": "pick", "interaction": "word_pick", "shade": True,
                "candidates": ["word", "geography", "where"],
                "answers": ["where"],
                "brief": {
                    "ask": "One word(한 단어)가 가리키는 건 무엇일까요? 문장에서 찾아 눌러 봐요.",
                    "wrong": "그건 One word가 가리키는 단어가 아니에요.",
                    "wrong_by": {
                        "word": "word는 '단어'라는 말 자체예요. 어떤 단어인지는 콜론(:) 뒤를 봐요.",
                        "geography": "geography는 그 단어와 연관된 대상이에요. 콜론(:) 뒤를 봐요.",
                    },
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "맞아요! 콜론(:) 뒤의 where가 그 한 단어예요.",
                    "explain": "콜론(:) 뒤가 앞의 One word가 무엇인지 알려 줘요. 그 단어는 where(어디)예요.",
                    "point": "One word … : where — 콜론 뒤가 앞말을 풀어 준다 · 그 한 단어 = where(어디)",
                },
                "method": 0,
            },
            # 이 문장의 뜻 — 해석 맞추기 (2026-10-14 선생님): 중·초는 짧은 문장이면 모두 돌려 낸다. 고는 미정
            # 같은 자리(slot)의 객관식과 돌려 가며 — 최근에 덜 한 방식이 나온다
            {
                "id": "s1_match", "levels": ["중", "초"], "slot": "s1_meaning", "type": "pick", "interaction": "word_pick", "no_unknown": False,
                "candidates": ["One word", "is inextricably associated with", "geography", "where"],
                "answers": ["One word", "is inextricably associated with", "geography", "where"],
                "match": {"ko": [
                    {"en": "One word", "ko": "한 단어는"}, " ",
                    {"en": "geography", "ko": "지리학과"}, " ",
                    {"en": "is inextricably associated with", "ko": "떼려야 뗄 수 없이 연관되어 있다"}, ": 바로 ",
                    {"en": "where", "ko": "'어디'"}, "다.",
                ]},
                "brief": {
                    "ask": "이번엔 해석을 맞춰 봐요. 영어 덩어리를 끌어다 맞는 한국어 칸에 놓아 볼까요?",
                    "wrong": "그 칸은 '{ko}'예요. 다른 덩어리를 놓아 봐요.",
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "다 맞췄어요! '어디'라는 한 단어가 지리학과 떼려야 뗄 수 없대요.",
                    "explain": "One word = 한 단어, geography = 지리학, is inextricably associated with = 떼려야 뗄 수 없이 연관되어 있다, where = 어디예요.",
                    "point": "One word is inextricably associated with geography: where — 한 단어(where)가 지리학과 떼려야 뗄 수 없다",
                },
                "method": 0,
            },
            # 이 문장의 뜻 — 객관식 (같은 자리 s1_meaning: 맞추기와 돌려 가며)
            choice("s1_meaning",
                   "그럼 이 문장의 뜻은 무엇일까요?",
                   [("o0", "지리학은 단 한 단어로 설명할 수 있다", False),
                    ("o1", "'어디(where)'라는 단어는 지리학과 떼려야 뗄 수 없다", True),
                    ("o2", "지리학에서는 단어를 정확하게 써야 한다", False)],
                   "주어 One word = where, 동사 is inextricably associated with = 떼려야 뗄 수 없이 연관되어 있다, 목적어 geography예요.",
                   why="One word는 where이고, is inextricably associated with geography는 '지리학과 떼려야 뗄 수 없이 연관되어 있다'예요.",
                   slot="s1_meaning"),
            show("s1_map", "where(어디)가 이 글의 첫 열쇠예요. 단어 지도에 넣어 둘게요.",
                 button="다음 문장", panel=space_board(1, fresh=("where",))),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("That is because", "그것은 ~이기 때문이다"), g("geography", "지리학"), g("starts", "출발하다"),
                    g("the premise", "전제"), g("it matters", "중요하다"), g("takes place", "일어나다"),
                    g("Earth’s surface", "지구 표면")],
        "steps": [
            sv_pick("s2_sv", ["is", "geography", "starts", "the premise", "something", "takes place"],
                    {"geography": "S", "starts": "V"},
                    "because 뒤에서 주어(S)와 동사(V)를 찾아볼까요?",
                    {"is": "That is는 because 앞이에요. because 뒤에서 찾아봐요.",
                     "the premise": "from 뒤 덩어리예요. 전치사 뒤 덩어리는 주어·동사가 될 수 없어요.",
                     "something": "그건 that 뒤 덩어리(전제의 내용) 안의 말이에요.",
                     "takes place": "그건 that 뒤 덩어리(전제의 내용) 안의 동사예요."},
                    "because 뒤는 S geography, V starts예요."),
            choice("s2_matters",
                   "'it matters where something takes place'는 무슨 뜻일까요?",
                   [("o0", "무엇이 일어나는지가 중요하다", False), ("o1", "어디에서 일어나는지가 중요하다", True),
                    ("o2", "언제 일어나는지는 중요하지 않다", False)],
                   "matter는 동사로 '중요하다'예요. it은 뒤의 where 덩어리를 대신하는 가주어예요.",
                   why="it은 뒤의 'where something takes place'를 대신하는 가주어예요. matter는 '중요하다', where는 '어디'예요.",
                   highlight=["matters where"],
                   tips=[{"label": "it matters + 의문사", "mark": "it matters",
                          "text": "matter는 동사로 '중요하다'예요. it matters where …는 '어디에서 …하는지가 중요하다'예요. it은 뒤의 where 덩어리를 대신하는 가주어예요."}]),
            # 문장 1·2를 이어서 — 지리학은 '어디'와 떼려야 뗄 수 없다, 왜냐하면 '어디'가 중요하다는 데서 출발하니까
            show("s2_both",
                 "두 문장을 이어 보면, 지리학은 '어디'와 떼려야 뗄 수 없어요. 지리학은 어디에서 일어나는지가 중요하다는 데서 출발하기 때문이에요.",
                 button="다음 문장", display=f"{S[0]} {S[1]}", tag="문장 1·2",
                 highlight=["geography", "where"], highlight_alt=["That is because", "matters where"],
                 panel_below=True,
                 panel={"kind": "structure", "rows": [
                     {"label": "문장 1", "text": "geography ↔ where", "ko": "지리학은 '어디'와 떼려야 뗄 수 없다", "tone": "hl"},
                     {"label": "문장 2 (이유)", "text": "That is because … it matters where", "ko": "어디에서 일어나는지가 중요하니까", "tone": "hl2"},
                 ]}),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("The key questions", "핵심 질문"), g("are not simply", "단순히 ~인 것은 아니다"), g("though", "그렇지만"),
                    g("they are", "그것들은 ~이다"), g("why there", "왜 거기에"), g("so what", "그래서 뭐, 그래서 어떻다는 건가")],
        "steps": [
            choice("s3_key",
                   "글쓴이가 말하는 핵심 질문은 어느 쪽일까요?",
                   [("o0", "'어디' 질문만", False), ("o1", "'왜 거기에', '그래서 뭐' 질문", True),
                    ("o2", "'언제' 질문", False)],
                   "not simply A; B예요. 세미콜론 뒤 B가 글쓴이 생각이에요.",
                   why="'not simply where questions'는 '단순히 어디 질문만은 아니다'예요. 세미콜론 뒤 'why there', 'so what'이 글쓴이가 말하는 핵심 질문이에요.",
                   highlight=["“why there”", "“so what”"],
                   tips=[{"label": "not simply A; B", "mark": "not simply",
                          "text": "'단순히 A가 아니라 B'예요. 뒤의 B가 글쓴이가 말하고 싶은 쪽이에요. 끝의 though는 '그렇지만'이에요."}]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Getting to such questions", "그런 질문에 이르는 것"), g("means", "의미하다"),
                    g("taking … seriously", "~을 진지하게 받아들이는 것"), g("spatial arrangements", "공간 배치"),
                    g("variations", "차이, 변화"), g("interconnections", "상호 연결"), g("seriously", "진지하게")],
        "steps": [
            sv_pick("s4_sv", ["Getting to such questions", "means", "spatial arrangements", "variations", "interconnections", "seriously"],
                    {"Getting to such questions": "S", "means": "V"},
                    "이번엔 주어(S)와 동사(V)를 찾아볼까요? 주어가 꽤 길 수도 있어요.",
                    {"spatial arrangements": "그건 taking 뒤 덩어리 안의 말이에요. 문장 맨 앞부터 봐요.",
                     "variations": "그건 taking 뒤 덩어리 안의 말이에요. 문장 맨 앞부터 봐요.",
                     "interconnections": "그건 taking 뒤 덩어리 안의 말이에요. 문장 맨 앞부터 봐요.",
                     "seriously": "seriously는 '진지하게'라서 주어나 동사가 아니에요."},
                    "주어는 Getting to such questions(그런 질문에 이르는 것), 동사는 means예요.",
                    wrong="그건 주어나 동사가 아니에요."),
            choice("s4_what",
                   "그런 질문에 답하려면 무엇을 진지하게 봐야 한대요?",
                   [("o0", "공간 배치, 차이, 연결", True), ("o1", "역사적 사건의 순서", False),
                    ("o2", "사람들의 감정", False)],
                   "means taking 뒤 'spatial arrangements, variations, and interconnections'를 봐요.",
                   highlight=["spatial arrangements", "seriously"],
                   tips=[{"label": "-ing 주어", "mark": "Getting",
                          "text": "Getting to such questions처럼 -ing로 시작하는 덩어리가 주어일 수 있어요. '~하는 것'으로 읽어요."}]),
            # 단어 지도 — 첫 단어(where)는 선생님이 넣었고, 중요한 다음 말은 학생이 찾아 넣는다
            same_pick("s4_same", ["such questions", "spatial arrangements", "seriously"], "spatial arrangements",
                      "이 문장에서 where와 같은 쪽 말, 즉 '어디에 어떻게 놓여 있나'를 말하는 걸 찾아 눌러 볼까요?",
                      {"such questions": "such questions는 앞의 '왜 거기에, 그래서 뭐' 질문을 가리켜요.",
                       "seriously": "seriously는 '진지하게'라서 어디에 놓여 있는지와는 상관없어요."},
                      "맞아요! spatial arrangements(공간 배치)도 where와 같은 쪽이에요."),
            show("s4_map", "단어 지도에 넣었어요.",
                 button="다음 문장", panel=space_board(2, fresh=("spatial arrangements",))),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("Engaging in even the simplest day-to-day activity", "가장 단순한 일상 활동을 하는 것조차"),
                    g("requires", "필요로 하다"), g("some appreciation", "어느 정도의 이해"),
                    g("spatial circumstances", "공간적 상황"), g("where to find food and services", "음식과 서비스를 어디서 찾을지"),
                    g("how to get to work places", "직장에 어떻게 갈지"), g("and the like", "~ 등"),
                    g("Engaging in", "~에 참여하는 것"), g("day-to-day", "일상의"), g("appreciation", "이해, 인식 · 감사")],
        "steps": [
            sv_pick("s5_sv", ["Engaging in even the simplest day-to-day activity", "requires", "some appreciation",
                              "spatial circumstances", "where to find food and services", "how to get to work places"],
                    {"Engaging in even the simplest day-to-day activity": "S", "requires": "V", "some appreciation": "O"},
                    "이번엔 주어(S), 동사(V), 목적어(O)를 찾아볼까요?",
                    {"spatial circumstances": "of 뒤에서 appreciation을 꾸며 주는 말이에요.",
                     "where to find food and services": "대시(―) 뒤의 예예요. 문장의 주어·동사·목적어가 아니에요.",
                     "how to get to work places": "대시(―) 뒤의 예예요. 문장의 주어·동사·목적어가 아니에요."},
                    "주어는 Engaging in even the simplest day-to-day activity, 동사는 requires, 목적어는 some appreciation이에요.",
                    wrong="그건 주어·동사·목적어가 아니에요."),
            # 함정 단어 — appreciation은 '감사'가 아니라 '이해, 인식'
            choice("s5_appreciation",
                   "여기서 appreciation은 무슨 뜻일까요?",
                   [("o0", "감사", False), ("o1", "이해, 인식", True), ("o2", "감상", False)],
                   "of spatial circumstances(공간적 상황)를 '감사'할 수는 없어요.",
                   why="appreciation은 '감사'로 많이 알지만, 공간적 상황을 '감사'할 수는 없어요. 여기서는 '알고 있음'에 가까운 뜻이에요.",
                   highlight=["appreciation"]),
            show("s5_dash",
                 "대시(―) 뒤는 spatial circumstances의 예예요. 음식을 어디서 찾을지, 직장에 어떻게 갈지처럼 일상도 '어디'를 알아야 해요.",
                 highlight=["where to find", "how to get"],
                 highlight_alt=["spatial circumstances"]),
            same_pick("s5_same", ["some appreciation", "spatial circumstances", "food and services"], "spatial circumstances",
                      "이번에도 where와 같은 쪽 말을 찾아 눌러 볼까요?",
                      {"some appreciation": "appreciation은 '이해, 인식'이에요. 무엇에 대한 이해인지 뒤를 봐요.",
                       "food and services": "음식과 서비스는 예로 든 것이에요. 어디서 찾을지, 그 앞의 말을 봐요."},
                      "맞아요! spatial circumstances(공간적 상황)도 같은 쪽이에요."),
            show("s5_map", "단어 지도에 넣었어요.",
                 button="다음 문장", panel=space_board(3, fresh=("spatial circumstances",))),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Moving up in scale", "규모를 키워 보면"), g("without", "~ 없이는"), g("some awareness of", "~에 대한 어느 정도의 인식"),
                    g("it is difficult to", "~하기 어렵다"), g("make reasoned business or policy judgments", "합리적인 사업·정책 판단을 내리다"),
                    g("make sense of events", "사건을 이해하다"), g("grasp", "파악하다"),
                    g("the basic forces shaping life on the planet", "지구상의 삶을 만드는 기본적인 힘"),
                    g("reasoned", "합리적인"), g("judgments", "판단"), g("shaping", "형성하는")],
        "steps": [
            choice("s6_scale",
                   "Moving up in scale은 무슨 뜻일까요?",
                   [("o0", "규모를 키워 보면", True), ("o1", "저울에 올려 보면", False), ("o2", "위층으로 올라가면", False)],
                   "scale은 여기서 '규모'예요. 일상(앞 문장)에서 사업·정책(이 문장)으로 크기를 키운다는 말이에요.",
                   why="scale은 '저울'로 많이 알지만 여기서는 '규모'예요. 앞 문장의 일상 활동에서 사업·정책 판단으로 규모를 키운다는 말이에요.",
                   highlight=["Moving up in scale"]),
            choice("s6_fill",
                   "드디어 빈칸 문장이에요. 앞에서 모은 말을 떠올리면, 빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "어디에, 어떻게 놓여 있는지 (공간 배치)", True), ("o1", "사업에 성공하는 방법", False),
                    ("o2", "사람들의 감정 변화", False)],
                   "단어 지도를 봐요. where, spatial arrangements, spatial circumstances가 계속 나왔어요.",
                   why="앞 문장들은 계속 where(어디), spatial arrangements(공간 배치), spatial circumstances(공간적 상황)를 말했어요. 빈칸도 그쪽 말이어야 해요.",
                   highlight=["without some awareness of ________"], panel=space_board(3)),
            choice("s6_side",
                   "빈칸은 글쓴이 주장과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 (꼭 알아야 하는 것)", True), ("o1", "반대 쪽 (몰라도 되는 것)", False)],
                   "without(~이 없으면) 뒤가 difficult(어렵다, −)예요. 그러니 빈칸은 꼭 있어야 하는 것이에요.",
                   why="'~이 없으면 판단하기 어렵다'는 빈칸이 꼭 필요하다는 말이에요. 반전 단서도 없으니 글쓴이 주장과 같은 쪽이에요.",
                   signs=[{"text": "difficult", "sign": "−"}],
                   tips=[{"label": "without ~, it is difficult",
                          "text": "'~이 없으면 …하기 어렵다' = '~이 꼭 필요하다'예요. 빈칸에는 글에서 계속 강조한 것이 들어가요."}]),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("Locating a new store or public service", "새 가게나 공공 서비스의 위치를 정하는 것"), g("requires", "필요로 하다"),
                    g("taking into consideration", "~을 고려하는 것"), g("population distributions", "인구 분포"),
                    g("the location of roads", "도로의 위치"), g("utilities", "공공 설비(전기·수도 등)"),
                    g("socio-economic patterns", "사회 경제적 양식"), g("and more", "등등"), g("Locating", "위치를 정하는 것")],
        "steps": [
            sv_pick("s7_sv", ["Locating a new store or public service", "requires", "population distributions",
                              "the location of roads", "socio-economic patterns"],
                    {"Locating a new store or public service": "S", "requires": "V"},
                    "이번엔 주어(S)와 동사(V)를 찾아볼까요?",
                    {"population distributions": "그건 고려할 것들의 예예요. 문장 맨 앞부터 봐요.",
                     "the location of roads": "그건 고려할 것들의 예예요. 문장 맨 앞부터 봐요.",
                     "socio-economic patterns": "그건 고려할 것들의 예예요. 문장 맨 앞부터 봐요."},
                    "주어는 Locating a new store or public service(새 가게나 공공 서비스의 위치를 정하는 것), 동사는 requires예요."),
            show("s7_examples",
                 "빈칸 문장 뒤는 예시예요. 가게 위치를 정하려면 인구 분포, 도로 위치를 따져야 하는데, 모두 '어디에 어떻게 놓여 있나'예요.",
                 highlight=["population distributions", "location of roads"],
                 panel=space_board(4, fresh=("the location of roads",)), point=POINTS["s7_examples"]),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("Understanding why and where migration happens", "이주가 왜, 어디서 일어나는지 이해하는 것"),
                    g("requires", "필요로 하다"), g("consideration", "고려"), g("migration", "이주"),
                    g("the political organization of territory", "영토의 정치적 조직"),
                    g("the spatial consequences of discrimination", "차별의 공간적 결과"),
                    g("the layout of the physical environment", "물리적 환경의 배치"), g("layout", "배치")],
        "steps": [
            sv_pick("s8_sv", ["Understanding why and where migration happens", "requires", "consideration",
                              "the political organization", "the layout"],
                    {"Understanding why and where migration happens": "S", "requires": "V", "consideration": "O"},
                    "마지막 문장이에요. 주어(S), 동사(V), 목적어(O)를 찾아볼까요?",
                    {"the political organization": "of 뒤에서 고려할 것들의 예예요.",
                     "the layout": "of 뒤에서 고려할 것들의 예예요."},
                    "주어는 Understanding why and where migration happens, 동사는 requires, 목적어는 consideration이에요.",
                    wrong="그건 주어·동사·목적어가 아니에요."),
            show("s8_map",
                 "the layout(배치)까지, 이 글은 '공간이 어떻게 배치돼 있나'를 계속 다른 말로 말해요.",
                 panel=space_board(5, fresh=("the layout",))),
            show("s8_go",
                 "빈칸은 주장과 같은 쪽이에요. '어디에, 어떻게 배치돼 있나'를 다른 말로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요", panel=space_board(5)),
        ],
    },
]

OPTIONS = [
    ("1", "why cross-cultural conflicts will increase", ["cross-cultural conflicts", "increase"],
     "문화 간 갈등이 왜 늘어날지", False),
    ("2", "how phenomena are arranged on Earth’s surface", ["phenomena", "arranged", "Earth’s surface"],
     "현상이 지구 표면에 어떻게 배치되어 있는지", True),
    ("3", "when the Earth’s natural resources will be exhausted", ["natural resources", "exhausted"],
     "지구의 천연자원이 언제 고갈될지", False),
    ("4", "which places on Earth are damaged by climate change", ["damaged", "climate change"],
     "지구의 어느 곳이 기후 변화로 피해를 입는지", False),
    ("5", "who has the authority to make decisions about territories", ["authority", "territories"],
     "누가 영토에 대한 결정 권한을 가지는지", False),
]

exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오. [3점]",
    "underline": "________",
    "sentence": 6,
    "analysis_first": True,
    "glosses": [g("cross-cultural", "문화 간의"), g("conflicts", "갈등"), g("phenomena", "현상"), g("arranged", "배치된"),
                g("natural resources", "천연자원"), g("exhausted", "고갈된"), g("damaged", "피해를 입은"),
                g("climate change", "기후 변화"), g("authority", "권한"), g("territories", "영토")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": {
        "ask": "단어 지도에 모은 말을 떠올리며 골라 봐요.",
        "first_correct": "맞았어요!",
        "first_wrong": "아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.",
        "final_correct": "정답이에요!",
        "answer_explain": "정답이에요! 지리학은 '어디'에서 출발해, 공간 배치를 진지하게 봐요. 그래서 현상이 지구 표면에 어떻게 배치돼 있는지 알아야 판단하고 이해할 수 있어요.",
        "final_wrong": "정답은 ②예요.",
        "option_feedback": {
            "1": "문화 간 갈등이 늘어난다는 이야기는 글에 없어요. 글은 '어디에, 어떻게 놓여 있나'를 계속 말해요.",
            "3": "자원이 언제 고갈될지는 '언제' 질문이에요. 이 글은 '어디' 질문에서 출발해요.",
            "4": "기후 변화로 피해를 입는 곳 이야기는 글에 없어요. place(장소)가 나와서 헷갈렸죠.",
            "5": "territory(영토)가 마지막 문장에 나와서 헷갈렸죠. 하지만 글은 결정 권한이 아니라 공간 배치 이야기예요.",
        },
        "ask_first": "실제 시험처럼 풀어 봐요. 위 보기에서 답을 골라요.",
    },
}

lesson = {
    "id": ID, "kind": "policy", "version": "0.1",
    "source": "2026학년도 6월 모의평가(한국교육과정평가원) 영어 34번 (빈칸 추론, 3점)",
    "brief": {"topic": "빈칸 푸는 법: 빈칸 문장부터 → 주어·동사와 핵심어 → 빈칸이 주장과 같은 쪽인지 → 같은 말을 바꿔 쓴 보기", "closing": "수고 인사"},
    "method": {"type": "blank", "labels": ["빈칸 문장 먼저 보기", "같은 말 모으기"], "intro_times": 3},
    "read_button": "분석하러 갈게요",
    "read_first": True,
    "images": {"topic": {"src": "/assets/topic-geography-where.svg", "alt": "칠판: Geography(지리학) — Where(어디). 지리학은 '어디'를 어떻게 바라볼까?", "kind": "drawing"}},
    "intro": [
        {"id": "topic", "type": "say", "button": "네", "image": "topic",
         "brief": {"say": "새 가게를 어디에 낼지 정하려면 무엇부터 알아야 할까요? 이번 글은 지리학이 '어디'를 어떻게 바라보는지 다뤄요."}},
        {"id": "method1", "type": "say", "button": "좋아요",
         "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 같은 말이 다른 말로 반복되는 걸 모으면 빈칸이 보여요."}},
    ],
    "exam": exam,
    "key_words": {
        # inextricably, premise는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
        "passage": [g("geography", "지리학"), g("matter", "중요하다"), g("spatial", "공간의"), g("arrangement", "배치"),
                    g("variation", "차이, 변화"), g("interconnection", "상호 연결"), g("appreciation", "이해, 인식"),
                    g("circumstance", "상황"), g("scale", "규모"), g("awareness", "인식"), g("reasoned", "합리적인"),
                    g("distribution", "분포"), g("migration", "이주"), g("territory", "영토"), g("layout", "배치")],
        "options": [g("phenomena", "현상"), g("arranged", "배치된"), g("exhausted", "고갈된"), g("authority", "권한")],
    },
    "context": {"mode": "paper_review", "exam_relevance": "high", "time_budget": "normal"},
    "item": {"english_difficulty": "high", "conceptual_difficulty": "high", "background_knowledge_required": "low",
             "exam_importance": "high", "teaching_value": "high", "intervention_density": "normal"},
    "sentences": sentences,
    "passage_on_try": True,
}

# 학생 단계(고 1~2 · 중 3~5 · 초 6~8등급) — 영어를 돕는 화면만 나눈다. 내용 파악 화면은 모두에게
# 주어·동사 찾기: 짧은 문장(20단어 미만)은 중·초만, 긴 문장은 고도 / 가리키는 말·헷갈리는 단어 뜻: 중·초
HELP_ONLY = {"s1_word", "s5_appreciation", "s6_scale"}
for s_ in sentences:
    long_sentence = len(s_["text"].split()) >= 20
    for st in s_["steps"]:
        if (st["id"].endswith("_sv") and not long_sentence) or st["id"] in HELP_ONLY:
            st["levels"] = ["중", "초"]

# 찾기 후보 덩어리는 화면에서 따로 누를 수 있어야 한다 — 덩어리 뜻이 없으면 채운다
CHUNKS = {
    "is inextricably associated": "떼려야 뗄 수 없이 연관되어 있다", "is": "~이다", "something": "어떤 일", "word": "단어",
    "such questions": "그러한 질문", "food and services": "음식과 서비스",
    "the political organization": "정치적 조직", "the layout": "배치",
}
for s_ in sentences:
    have = {x["en"] for x in s_["glosses"]}
    for st in s_["steps"]:
        for c_ in st.get("candidates", []):
            if c_ not in have:
                s_["glosses"].insert(0, g(c_, CHUNKS[c_]))
                have.add(c_)

# 초급 기본 — 문장마다 「주어·동사 + 뜻」 또는 「해석 맞추기」 하나 (2026-10-15 선생님).
# 문장 1은 s1_meaning 자리(맞추기/뜻 객관식)가 이미 있다. 빈칸 문장(6)은 수업 처음에 뜻을 짚어서 넣지 않는다
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beginner import add_basic, add_that_sv, fill_chunk_glosses, m, sv_step  # noqa: E402

add_basic(sentences, 2, [m("That is because", "그건 ~ 때문이다:"), " ", m("geography", "지리학은"), " ",
                         m("where something takes place", "어떤 일이 어디서 일어나는지"), "가 ", m("it matters", "중요하다"), "는 ",
                         m("the premise", "전제"), "에서 ", m("starts", "출발한다"), "."],
          sv_id="s2_sv", meaning_ids=["s2_matters"])
add_basic(sentences, 3, [m("The key questions", "핵심 질문은"), " 단순히 ", m("where", "'어디'"), " 질문이 ", m("are not simply", "아니다"), "; ",
                         m("they are", "그것들은"), " ", m("why there", "'왜 거기'"), "와 ", m("so what", "'그래서 뭐'"), " 질문이다."],
          sv_new=sv_step("s3_basic_sv", ["The key questions", "are not simply", "though", "they are"],
                         {"The key questions": "S", "are not simply": "V"},
                         {"they are": "그건 세미콜론(;) 뒤 문장이에요. 앞에서 찾아봐요.", "though": "그건 '그렇지만'이라는 연결 말이에요."},
                         "주어는 The key questions(핵심 질문), 동사는 are not simply(단순히 ~이 아니다)예요."),
          meaning_ids=["s3_key"],
          meaning="핵심 질문은 그냥 '어디'가 아니라, '왜 거기'와 '그래서 뭐'라는 질문이래요.")
add_basic(sentences, 4, [m("Getting to such questions", "그런 질문에 이르는 것은"), " ", m("spatial arrangements", "공간 배치"), ", ",
                         m("variations", "차이"), ", ", m("interconnections", "상호 연결"), "을 ", m("seriously", "진지하게"), " 받아들임을 ",
                         m("means", "의미한다"), "."],
          sv_id="s4_sv", meaning_ids=["s4_what"],
          meaning="그런 질문에 답하려면 공간 배치, 차이, 상호 연결을 진지하게 봐야 한대요.")
add_basic(sentences, 5, [m("Engaging in even the simplest day-to-day activity", "가장 단순한 일상 활동을 하는 것도"), " ",
                         m("spatial circumstances", "공간적 상황"), "에 대한 ", m("some appreciation", "어느 정도의 이해"), "를 ",
                         m("requires", "필요로 한다"), "."],
          match_display="Engaging in even the simplest day-to-day activity requires some appreciation of spatial circumstances.",
          sv_id="s5_sv", meaning_ids=["s5_appreciation"],
          meaning="가장 단순한 일상 활동을 하는 데에도 공간적 상황을 어느 정도 이해해야 한대요.")
add_basic(sentences, 7, [m("Locating a new store", "새 가게의 위치를 정하는 것은"), " ", m("population distributions", "인구 분포"), "와 ",
                         m("the location of roads", "도로의 위치"), "를 ", m("taking into consideration", "고려하는 것"), "을 ",
                         m("requires", "필요로 한다"), "."],
          match_display="Locating a new store requires taking into consideration population distributions and the location of roads.",
          sv_id="s7_sv", meaning_ids=["s7_examples"])
add_basic(sentences, 8, [m("Understanding why and where migration happens", "이주가 왜, 어디서 일어나는지 이해하는 것은"), " ",
                         m("the layout of the physical environment", "물리적 환경의 배치"), "에 대한 ", m("consideration", "고려"), "를 ",
                         m("requires", "필요로 한다"), "."],
          match_display="Understanding why and where migration happens requires consideration of the layout of the physical environment.",
          sv_id="s8_sv",
          meaning="이주가 왜, 어디서 일어나는지 이해하려면 영토의 정치 조직, 차별의 공간적 결과, 물리적 환경의 배치 등을 고려해야 한대요.")
# the premise that ~ 안이 핵심 (2026-10-16 선생님, 공통)
add_that_sv(sentences, 2, "s2_sv", "s2_that_sv", ["it", "matters", "where something takes place"],
            {"it": "S", "matters": "V"},
            {"where something takes place": "그건 진짜 주어예요. 자리에는 it이 대신 와 있어요."},
            "that 안의 주어는 it(가짜 주어 — 진짜는 where something takes place), 동사는 matters(중요하다)예요. 어디서 일어나는지가 중요하다는 거예요.",
            ask="the premise that ~: that 뒤가 그 전제의 내용이에요. 그 안에서 주어(S)와 동사(V)를 찾아볼까요?")
fill_chunk_glosses(sentences, {
    "where something takes place": "어떤 일이 어디서 일어나는지", "The key questions": "핵심 질문", "are not simply": "단순히 ~이 아니다",
    "though": "그렇지만", "they are": "그것들은 ~이다", "where": "어디", "why there": "왜 거기", "so what": "그래서 뭐",
    "seriously": "진지하게", "variations": "차이", "interconnections": "상호 연결", "means": "의미하다",
    "Locating a new store": "새 가게의 위치를 정하는 것", "population distributions": "인구 분포",
    "the location of roads": "도로의 위치", "taking into consideration": "고려하는 것", "consideration": "고려",
    "the layout of the physical environment": "물리적 환경의 배치", "That is because": "그건 ~ 때문이다",
    "it matters": "중요하다", "the premise": "전제", "starts": "출발하다", "geography": "지리학",
    "matters": "중요하다", "it": "그것(가짜 주어)",
})

# 칠판 정리 — 2~3문장마다 지금까지 상황을 칠판에 (공통 틀)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_boards import add_story_boards  # noqa: E402
add_story_boards(ID, lesson["sentences"])

json.dump(lesson, open(f"{ROOT}/content/tutor/policy-lessons/{ID}.json", "w"), ensure_ascii=False, indent=2)

ref = json.load(open(f"{ROOT}/content/tutor/policy-copy/dajung/moeui-2026-03-21-music-researchers.json"))
steps = {st["id"]: copy.deepcopy(st["brief"]) for s in sentences for st in s["steps"]}
c = {
    "lesson": ID, "character": "dajung", "note": "생성물",
    "topic_intro": "빈칸 푸는 법",
    "closing": ref["closing"],
    "helps": {},
    "steps": steps,
    "exam": {k: v for k, v in exam["brief"].items()},
    "intro": {i["id"]: dict(i["brief"]) for i in lesson["intro"]},
    "ending": {**ref["ending"], "wrong": "이번엔 한 번 헷갈렸으니 {weeks} 뒤에 다시 한번 볼 거예요."},
}
json.dump(c, open(f"{ROOT}/content/tutor/policy-copy/dajung/{ID}.json", "w"), ensure_ascii=False, indent=2)
print("ok", ID)
