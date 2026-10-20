"""2024년 3월 고3 45번 레슨 + 대사를 만든다 (43~45 장문 중 45번 — 내용 불일치, 2점). 오답률 자료 없음(Top 15 밖).

    python3 scripts/lessons/gen_moeui_2024_03_43.py && python3 scripts/lessons/gen_moeui_2024_03_45.py   (→ stamp → npm run build)

지문은 43번과 같다 — 문장·뜻·기능어는 43번 생성물에서 가져오고, 스텝만 내용 일치용으로 새로 쓴다(43번을 고치면 다시 돌린다).
내용 일치 유형은 처음 — Claude 초안(2026-10-18, 미니 모의고사 연결용). 푸는 법: 보기는 글 순서대로 나온다 → 보기의 열쇠말
(차고·젊은 시절·공 치기·유니폼·집 밖)이 나오는 문장에서 하나씩 맞춰 본다. 정답 ⑤ (글은 inside the house = 집 안으로).
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (ROOT, choice, show, tip, rows, base_lesson, exam_brief, finish)  # noqa: E402

ID = "moeui-2024-03-45-story-details"
SRC = "moeui-2024-03-43-baseball-card"

src = json.load(open(f"{ROOT}/content/tutor/policy-lessons/{SRC}.json"))
SENSES = {int(k): v for k, v in json.load(open(f"{ROOT}/content/tutor/function-senses/{SRC}.json")).items()}
sentences = [{k: s[k] for k in ("id", "text", "model_translation", "glosses", "slashes", "roles", "modifiers") if k in s} | {"steps": [], "teaching_value": "low"}
             for s in src["sentences"]]

OPTS = ["Tommy는 차고에서 오래되고 잊혀진 상자를 발견했다.",
        "Grandpa Joe는 야구장에서 보낸 그의 젊은 시절 이야기를 했다.",
        "그들은 함께 공 치기, 잡기를 연습했다.",
        "야구 카드 속에서 Grandpa Joe는 야구 유니폼을 입고 있었다.",
        "Tommy는 Grandpa Joe를 찾기 위해 집 밖으로 서둘러 나왔다."]
SAME, DIFF = "글과 같아요", "글과 달라요"


def board(*done):
    return rows(*[(f"{'①②③④⑤'[n]}", OPTS[n], "같음" if n != 4 else "다름", "hl" if n != 4 else "hl2") for n in done])


def check(id, n, same, hint, why, hl):
    return choice(id, f"보기 {'①②③④⑤'[n]} 「{OPTS[n]}」 이 문장과 비교해 볼까요?",
                  [("o0", SAME, same), ("o1", DIFF, not same)], hint, why=why, highlight=hl, panel=board(*range(n)) if n else None)


STEPS = {
    1: [show("d_how", "내용 일치 문제는 보기를 먼저 훑어요. 보기는 글 순서대로 나오니까, 읽다가 보기 속 열쇠말이 나오면 그 자리에서 맞춰 봐요.",
             button="다음 문장",
             tips=[tip("내용 일치 요령", "보기 ①~⑤는 글 순서대로 나와요. 장소, 사람, 행동처럼 바꾸기 쉬운 말을 하나씩 대조해요.")])],
    4: [check("d_1", 0, True, "while searching the garage, found an old, forgotten box를 봐요.",
              "차고(the garage)를 뒤지다 오래되고 잊혀진 상자를 찾았대요. 보기와 같아요.", ["searching the garage", "an old, forgotten box"])],
    7: [check("d_2", 1, True, "stories of his youthful days on the baseball field를 봐요.",
              "야구장(baseball field)에서 보낸 젊은 시절(youthful days) 이야기를 했대요. 보기와 같아요.", ["his youthful days on the baseball field"])],
    12: [check("d_3", 2, True, "they practiced hitting, catching을 봐요.",
               "함께 치기(hitting), 잡기(catching)를 연습했대요. 보기와 같아요.", ["practiced hitting, catching"])],
    16: [check("d_4", 3, True, "in a baseball uniform을 봐요.", "카드 속 할아버지는 야구 유니폼(baseball uniform)을 입고 서 있었대요. 보기와 같아요.",
               ["in a baseball uniform"])],
    18: [check("d_5", 4, False, "rushed 뒤 방향을 나타내는 말을 봐요. inside는 '안으로'예요.",
               "rushed inside the house, 집 '안으로' 서둘러 들어갔대요. 보기는 '집 밖으로'라서 달라요.", ["rushed inside the house"],),
         show("d_go", "장소 하나만 살짝 바꿔도 틀린 보기가 돼요. 문제에서 골라 봐요.", panel=board(0, 1, 2, 3, 4), button="문제 풀러 갈게요",
              tips=[tip("inside / outside", "inside the house = 집 안으로, outside the house = 집 밖으로예요.", "inside")])],
}
for s in sentences:
    if s["id"] in STEPS:
        s["steps"], s["teaching_value"] = STEPS[s["id"]], "high"

exam = {
    "question": "윗글에 관한 내용으로 적절하지 않은 것은?", "sentence": 18, "analysis_first": True, "glosses": [],
    "options": [{"id": str(i + 1), "label": OPTS[i], "keywords": [], **({"correct": True} if i == 4 else {})} for i in range(5)],
    "brief": exam_brief(
        "칠판에서 '다름'으로 표시한 보기를 골라 봐요.",
        "정답이에요! 글은 rushed inside the house, 집 안으로 서둘러 들어갔대요. 보기 ⑤는 '집 밖으로'라서 글과 달라요.",
        "정답은 ⑤예요. 글은 inside the house(집 안으로)예요.",
        {"1": "while searching the garage, found an old, forgotten box, 글과 같아요.",
         "2": "stories of his youthful days on the baseball field, 글과 같아요.",
         "3": "they practiced hitting, catching, 글과 같아요.",
         "4": "stood proudly in a baseball uniform, 글과 같아요."}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 43~45번 중 45번 (내용 불일치, 2점)",
    topic="내용 일치 푸는 법: 보기를 먼저 훑기 → 글 순서대로 읽다가 열쇠말 자리에서 대조 → 다른 하나",
    method={"type": "detail", "labels": ["보기 먼저 훑기", "자리에서 대조"], "intro_times": 3},
    images={"topic": src["images"]["topic"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "43번에서 본 할아버지와 손자 이야기예요. 이번엔 보기 다섯 개를 글과 하나씩 맞춰 볼게요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "보기는 글 순서대로 나와요. 읽다가 보기 속 장면이 나오면 그 자리에서 같은지 다른지 볼 거예요."}}],
    exam=exam, key_words=src["key_words"], sentences=sentences, english="medium", concept="low")

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# lazy 나른한, 한가한.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    4: [tip("lazy", "이 글에서는 → 나른한, 한가한  ('게으른' 아님)", "lazy", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words={}, topic_intro="내용 일치 푸는 법")
