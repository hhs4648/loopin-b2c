"""2024년 3월 고3 41번 레슨 + 대사를 만든다 (41~42 장문 중 41번 — 제목, 2점). 오답률 자료 없음(Top 15 밖).

    python3 scripts/lessons/gen_moeui_2024_03_42.py && python3 scripts/lessons/gen_moeui_2024_03_41.py   (→ stamp → npm run build)

지문은 42번과 같다 — 문장·뜻·기능어는 42번 생성물(policy-lessons/function-senses)에서 가져오고, 스텝만 제목용으로 새로 쓴다.
그래서 42번을 고치면 41번도 다시 돌린다. Claude 초안(2026-10-18, 미니 모의고사 연결용).
틀: 제목(24번) — 글쓴이가 하라는 말(It's time to restructure the way you think) 잡기 → 무엇을 바꾸나(자동적 사고 = self-talk)
→ 두 핵심어를 다 담은 보기. 정답 ③ Reshaping Thoughts: Manage Your Self-talk. 해설지 해석과 대조함.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (ROOT, g, choice, show, rows, topic_svg, base_lesson, exam_brief, finish)  # noqa: E402

ID = "moeui-2024-03-41-reshaping-thoughts"
SRC = "moeui-2024-03-42-automatic-thoughts"

src = json.load(open(f"{ROOT}/content/tutor/policy-lessons/{SRC}.json"))
SENSES = {int(k): v for k, v in json.load(open(f"{ROOT}/content/tutor/function-senses/{SRC}.json")).items()}
sentences = [{k: s[k] for k in ("id", "text", "model_translation", "teaching_value", "glosses", "slashes", "roles", "modifiers") if k in s} | {"steps": []}
             for s in src["sentences"]]


def board(*done):
    r = {"1": ("문장 1~3", "negative narration → anxious feelings", "부정적으로 말하면 불안해진다"),
         "4": ("문장 4", "restructure the way you think", "생각하는 방식을 다시 짜라", "hl"),
         "9": ("문장 9", "automatic thoughts = self-talk", "자동적 사고 = 혼잣말", "hl"),
         "13": ("문장 13", "bad habits", "자동적 사고는 나쁜 습관")}
    return rows(*[r[d] for d in done])


STEPS = {
    1: [show("s1_how", "42번과 같은 글이에요. 이번엔 제목을 찾으려고 글쓴이가 하라는 말과 핵심어만 골라 볼게요.", button="다음 문장")],
    2: [choice("s2_feel", "말하는 어조와 관점이 무엇을 만들어 낸대요?",
               [("o0", "감정 (feelings)", True), ("o1", "기억 (memories)", False)],
               "generates 뒤를 봐요. '그 이야기와 관련된 ~'을 만들어 낸대요.", highlight=["generates feelings"])],
    3: [show("s3_ex", "'어려워', '안 좋게 될 거야'처럼 말하면 불안한 감정이 생긴대요. 내가 나에게 하는 말이 감정을 바꾼다는 거예요.",
             highlight=["anxious feelings"], panel=board("1"), button="다음 문장")],
    4: [choice("s4_main", "글쓴이가 이제 무엇을 하라고 하나요?",
               [("o0", "생각하는 방식을 다시 짜기", True), ("o1", "불안한 감정을 꾹 참기", False)],
               "It’s time to 뒤가 글쓴이가 하라는 말이에요. restructure는 '다시 짜다'예요.", highlight=["restructure the way you think"]),
        show("s4_key", "제목의 첫 번째 핵심어예요. 생각을 바꾸자. 이제 어떤 생각을 바꾸는지 찾아봐요.",
             panel=board("1", "4"), button="다음 문장")],
    9: [show("s9_talk", "자동적 사고를 '혼잣말(self-talk)'이라고 부르재요. 두 번째 핵심어예요.",
             highlight=["self-talk"], panel=board("1", "4", "9"), button="다음 문장")],
    13: [choice("s13_bad", "글쓴이는 자동적 사고를 좋게 보나요, 나쁘게 보나요?",
                [("o0", "나쁘게 (bad habits)", True), ("o1", "좋게 (fresh experiences)", False)],
                "주어 Automatic thoughts 바로 뒤 are 다음 말을 봐요.", highlight=["bad habits"])],
    15: [show("s15_go", "나쁜 혼잣말을 바꿔 생각을 다시 짜자는 글이에요. 두 핵심어를 다 담은 제목을 골라 봐요.",
              panel=board("1", "4", "9", "13"), button="문제 풀러 갈게요")],
}
for s in sentences:
    s["steps"] = STEPS.get(s["id"], [])

OPTIONS = [
    ("1", "The Role of Automatic Thoughts in Language Learning", ["Language Learning"], "언어 학습에서 자동적 사고의 역할", False),
    ("2", "Self-talk: The Best Way to Improve Your Speech", ["Improve Your Speech"], "혼잣말: 말하기 실력을 높이는 최고의 방법", False),
    ("3", "Reshaping Thoughts: Manage Your Self-talk", ["Reshaping Thoughts", "Self-talk"], "생각 바꾸기: 혼잣말을 관리하라", True),
    ("4", "Heightened Anxiety Leads to Productivity", ["Productivity"], "높아진 불안이 생산성으로 이어진다", False),
    ("5", "Ways to Read Others’ Inner Thoughts", ["Others’ Inner Thoughts"], "다른 사람의 속마음을 읽는 방법", False),
]

exam = {
    "question": "윗글의 제목으로 가장 적절한 것은?", "sentence": 4, "analysis_first": True,
    "glosses": [g("Role", "역할"), g("Language Learning", "언어 학습"), g("Improve Your Speech", "말하기 실력을 높이다"),
                g("Reshaping", "다시 만들기, 바꾸기"), g("Manage", "관리하다"), g("Heightened", "높아진"), g("Productivity", "생산성"),
                g("Inner Thoughts", "속마음")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "칠판의 두 핵심어(생각을 다시 짜기, 혼잣말)를 떠올리며 골라 봐요.",
        "정답이에요! Reshaping Thoughts는 restructure the way you think를, Self-talk는 자동적 사고를 바꿔 쓴 말이에요.",
        "정답은 ③이에요. 생각을 다시 짜자(Reshaping Thoughts)는 말과 혼잣말(Self-talk)을 둘 다 담았어요.",
        {"1": "Automatic Thoughts는 맞지만 언어 학습 이야기는 글에 없어요.",
         "2": "Self-talk는 나오지만 말하기 실력을 높이는 글이 아니에요. 혼잣말이 감정을 바꾼다는 글이에요.",
         "4": "불안은 나쁜 경험을 만든대요. 생산성으로 이어진다는 말은 반대예요.",
         "5": "남의 속마음이 아니라 내가 나에게 하는 말 이야기예요."}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 41~42번 중 41번 (제목, 2점)",
    topic="제목 푸는 법: 글쓴이가 하라는 말 잡기 → 무엇을 바꾸는지 찾기 → 두 핵심어를 다 담은 보기",
    method={"type": "title", "labels": ["하라는 말 잡기", "핵심어 둘 담기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-self-talk.svg", ("Self-talk", "혼잣말"), "→", ("Feelings", "감정"),
                                       "내가 나에게 하는 말이 감정을 바꿀까?", "2024년 3월 42번 도입 칠판"),
                      "alt": "칠판: Self-talk(혼잣말) → Feelings(감정)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "새로운 자리에 갈 때 속으로 어떤 말을 하나요? 이번 글은 혼잣말이 감정을 어떻게 바꾸는지 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "제목 문제는 글쓴이가 하라는 말과, 무엇에 대한 말인지를 같이 잡아요. 핵심어 둘을 다 담은 제목이 정답이에요."}}],
    exam=exam,
    key_words={"passage": [g("narrator", "이야기하는 사람"), g("generate", "만들어 내다"), g("restructure", "재구성하다"),
                           g("automatic", "자동적인"), g("self-talk", "혼잣말"), g("navigate", "헤쳐 나가다"), g("habit", "습관")],
               "options": [g("reshape", "다시 만들다"), g("manage", "관리하다"), g("heightened", "높아진"), g("productivity", "생산성")]},
    sentences=sentences, concept="medium")

finish(ID, lesson, senses=SENSES, words={"role": "역할", "learning": "학습", "improve": "높이다", "speech": "말하기", "reshaping": "다시 만들기",
                                          "manage": "관리하다", "heightened": "높아진", "leads": "이끌다", "productivity": "생산성",
                                          "ways": "방법", "read": "읽다", "others’": "다른 사람들의", "inner": "속의"},
       topic_intro="제목 푸는 법")
