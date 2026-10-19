"""2024년 3월 고3 44번 레슨 + 대사를 만든다 (43~45 장문 중 44번 — 지칭 추론, 2점). 오답률 자료 없음(Top 15 밖).

    python3 scripts/lessons/gen_moeui_2024_03_43.py && python3 scripts/lessons/gen_moeui_2024_03_44.py   (→ stamp → npm run build)

지문은 43번과 같다 — 문장·뜻·기능어는 43번 생성물에서 가져오고, 스텝만 지칭용으로 새로 쓴다(43번을 고치면 다시 돌린다).
지칭 유형은 처음 — Claude 초안(2026-10-18, 미니 모의고사 연결용). 푸는 법: 등장인물 둘(Tommy · Grandpa Joe)을 칠판에 두고,
밑줄 대명사마다 그 문장에서 '누가 무엇을 하는지'로 정한다. (a)(b)(c)(e) = Tommy, (d) = Grandpa Joe. 정답 ④.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (ROOT, choice, show, tip, groups, topic_svg, base_lesson, exam_brief, finish)  # noqa: E402

ID = "moeui-2024-03-44-who-is-he"
SRC = "moeui-2024-03-43-baseball-card"

src = json.load(open(f"{ROOT}/content/tutor/policy-lessons/{SRC}.json"))
SENSES = {int(k): v for k, v in json.load(open(f"{ROOT}/content/tutor/function-senses/{SRC}.json")).items()}
sentences = [{k: s[k] for k in ("id", "text", "model_translation", "glosses", "slashes") if k in s} | {"steps": [], "teaching_value": "low"}
             for s in src["sentences"]]

TOMMY = "Tommy (손자)"
JOE = "Grandpa Joe (할아버지)"


def board(t=(), j=(), fresh=()):
    return groups("밑줄 친 그는 누구?", "Tommy (손자)", list(t), "Grandpa Joe (할아버지)", list(j), fresh=fresh, between="·")


def who(id, mark, tommy, hint, why, hl, t, j):
    return choice(id, f"밑줄 친 {mark}, 누구일까요?", [("o0", TOMMY, tommy), ("o1", JOE, not tommy)], hint, why=why, highlight=hl,
                  panel=board(t, j))


STEPS = {
    1: [show("w_two", "등장인물은 둘, 손자 Tommy와 할아버지 Grandpa Joe예요. 밑줄 친 him·he가 나올 때마다 둘 중 누구인지 칠판에 놓아 볼게요.",
             panel=board(), button="다음 문장",
             tips=[tip("지칭 요령", "대명사가 나오면 그 문장에서 누가 무엇을 하는지 봐요. 바로 앞에 나온 이름이 늘 답은 아니에요.")])],
    2: [who("w_a", "(a)him", True, "Tommy의 할아버지가 '누구에게' 신비로운 인물이었는지 봐요.",
            "Tommy’s grandfather가 주어예요. 할아버지가 신비로운 인물이었던 대상이니 (a)는 손자 쪽이에요.", ["to (a)him"], [], [])],
    5: [who("w_b", "(b)he", True, "바로 앞 문장에서 상자를 찾은 사람이 상자를 열어요.",
            "앞 문장에서 상자를 찾은 사람이 그것(it)을 열어요. 그래서 (b)는 상자를 찾은 손자예요.", ["As (b)he opened it"], ["(a)"], [])],
    10: [who("w_c", "(c)he", True, "(c)he가 '할아버지에게' 가르쳐 달라고 부탁해요.",
             "(c)he asked Grandpa Joe to teach him, 할아버지에게 부탁하는 사람이니 손자예요.", ["(c)he", "asked Grandpa Joe"], ["(a)", "(b)"], [])],
    11: [who("w_d", "(d)he", False, "(d)he가 '그의 손자(his grandson)'에게 지혜를 나눠 줘요.",
             "with his grandson, 자기 손자에게 야구의 지혜를 나눠 주는 사람이에요. 그래서 (d)는 할아버지예요.", ["as (d)he shared", "with his grandson"],
             ["(a)", "(b)", "(c)"], []),
         show("w_d_note", "(d)만 다른 쪽에 놓였어요. his grandson이라는 말이 열쇠였어요.",
              panel=board(["(a)", "(b)", "(c)"], ["(d)"], fresh=("(d)",)), button="다음 문장")],
    19: [who("w_e", "(e)he", True, "할아버지에게 '야구 선수셨어요?'라고 묻는 사람이에요.",
             "Hey, Grandpa! 하고 할아버지께 묻는 사람이니 손자예요.", ["(e)he asked"], ["(a)", "(b)", "(c)"], ["(d)"]),
         show("w_go", "(a)(b)(c)(e)는 한쪽, (d)만 다른 쪽이에요. 문제에서 골라 봐요.",
              panel=board(["(a)", "(b)", "(c)", "(e)"], ["(d)"], fresh=("(e)",)), button="문제 풀러 갈게요")],
}
for s in sentences:
    if s["id"] in STEPS:
        s["steps"], s["teaching_value"] = STEPS[s["id"]], "high"

UNDER = ["(a)him", "(b)he", "(c)he", "(d)he", "(e)he"]
exam = {
    "question": "밑줄 친 (a)~(e) 중에서 가리키는 대상이 나머지 넷과 다른 것은?",
    "underline": UNDER, "sentence": 11, "analysis_first": True, "glosses": [],
    "options": [{"id": str(i + 1), "label": f"({'abcde'[i]})", "keywords": [], **({"correct": True} if i == 3 else {})} for i in range(5)],
    "brief": exam_brief(
        "칠판에서 혼자 다른 쪽에 놓인 밑줄을 골라 봐요.",
        "정답이에요! (a)(b)(c)(e)는 모두 Tommy예요. (d)만 손자에게 야구를 가르쳐 주는 Grandpa Joe예요.",
        "정답은 ④ (d)예요. (d)는 his grandson에게 지혜를 나눠 주는 할아버지예요.",
        {"1": "(a)는 할아버지가 신비로운 인물이었던 대상, Tommy예요.",
         "2": "(b)는 상자를 찾아 연 Tommy예요.",
         "3": "(c)는 할아버지에게 가르쳐 달라고 부탁한 Tommy예요.",
         "5": "(e)는 할아버지께 야구 선수였냐고 묻는 Tommy예요."}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 43~45번 중 44번 (지칭 추론, 2점)",
    topic="지칭 푸는 법: 등장인물 둘을 칠판에 두기 → 밑줄마다 그 문장에서 누가 무엇을 하는지로 정하기 → 혼자 다른 하나",
    method={"type": "reference", "labels": ["인물 정하기", "밑줄마다 놓기"], "intro_times": 3},
    images={"topic": src["images"]["topic"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "43번에서 본 할아버지와 손자 이야기예요. 이번엔 he, him이 누구인지 가려 볼게요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "지칭 문제는 밑줄 대명사마다 그 문장에서 누가 무엇을 하는지 봐요. 칠판 두 칸에 하나씩 놓아 볼게요."}}],
    exam=exam, key_words=src["key_words"], sentences=sentences, english="medium", concept="low")

finish(ID, lesson, senses=SENSES, words={}, topic_intro="지칭 푸는 법")
