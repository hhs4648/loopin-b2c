"""칠판 정리 — 2~3문장마다 「지금까지 어떤 상황인지」 칠판에 그림(아이콘)·한 줄로 쌓아 보여 준다.

공통 틀(docs/tutor/templates/README.md §1 「칠판 정리」). 생성기는 lesson을 쓰기 직전에
`add_story_boards(ID, sentences)`를 부른다. 손으로 쓴 레슨(21번)은
`python3 scripts/lessons/story_boards.py <id>`로 JSON과 대사에 바로 넣는다(다시 돌려도 같다).

장면 쓰는 법
- `after`: 이 문장 공부가 끝난 뒤에 칠판을 띄운다. 그 문장의 마지막 스텝이 「문제 풀러」면 그 앞에
- 장면 한 줄 = 영어 핵심어 + (한국어 상황 한 줄). 그림은 이모지 하나
- **순서 문제에는 넣지 않는다** — 시험지 순서라 이야기가 안 맞는다 (2026-10-15 선생님)
- **답을 말하지 않는다** — 밑줄 의미·제목처럼 요약이 곧 답인 문제는 마지막 문장 앞에서 멈춘다.
  빈칸은 ____로 둔다. 문장 넣기·순서는 내용만, 순서나 자리를 암시하는 말은 쓰지 않는다
"""
import copy
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def sc(label, icon, en, ko):
    return {"label": label, "icon": icon, "en": en, "ko": ko}


# 레슨 → [(after 문장 id, [이번에 붙는 장면…])]
STORIES = {
    "mopyeong-2026-06-34-geography-where": [
        (3, [sc("문장 1~2", "🌍", "Geography ↔ Where", "지리학은 '어디'가 중요하다는 데서 출발해요"),
             sc("문장 3", "❓", "why there? · so what?", "그냥 어디가 아니라 — 왜 거기? 그래서 어떤데?")]),
        (5, [sc("문장 4~5", "🛒", "spatial arrangements", "밥 먹을 곳·출근길처럼 일상에도 공간 감각이 필요해요")]),
        (8, [sc("문장 6", "⚖️", "without ____ → difficult", "____을 모르면 판단하고 이해하기 어려워요"),
             sc("문장 7~8", "🏪", "new store · migration", "가게 자리, 사람들이 옮겨 가는 곳도 배치를 따져야 알아요")]),
    ],
    "moeui-2026-03-21-music-researchers": [
        (2, [sc("문장 1~2", "🎻", "innovator ≠ inventor", "뛰어난 음악가는 혁신가지만 꼭 발명가는 아니에요"),
             sc("", "😞", "“great discoveries”", "대발견을 기대하면 실망해요")]),
        (4, [sc("문장 3", "⚙️", "music = technique", "새것에 대한 집착은 음악을 기술로만 봐요"),
             sc("문장 4", "🚗", "new and improved", "자동차·가전처럼 해마다 더 나아져야 한다고 봐요")]),
        (6, [sc("문장 5~6", "🏁", "arms race · patent", "앞 음악의 기록을 깨고, 내가 발명했다고 주장해요")]),
    ],
    "moeui-2026-03-24-translation-strangeness": [
        (3, [sc("문장 1", "💨", "too domesticated → evaporates", "너무 익숙한 것은 당연해져서 안 보여요 — 예술이 다시 보이게 해요"),
             sc("문장 2~3", "🪨", "translation → stony again", "번역은 다른 언어로 옮겨 작품의 낯섦을 되살려요")]),
        (6, [sc("문장 4", "📄", "bad text → nothing happens", "원래 낯섦이 없는 글은 번역해도 아무 일도 없어요"),
             sc("문장 5~6", "✨", "true art → étrange (낯선)", "진짜 작품은 번역이 이미 있던 낯섦을 더 키워요")]),
    ],
    "moeui-2026-03-30-names-and-differences": [
        (3, [sc("문장 1", "🏷️", "name → abstract away", "이름을 붙이면 하나하나의 특징이 지워져요"),
             sc("문장 2~3", "🌼", "daisies · clover · flowers · lawn", "이 네 이름에는 서로 다른 점이 안 담겨요")]),
        (5, [sc("문장 4~5", "🌸", "Flower · Lawn", "여러 색 꽃, 여러 풀과 풀 아닌 식물이 이름 하나에 다 들어가요")]),
        (9, [sc("문장 6~7", "🔍", "zoom in → all different", "가까이 보면 다 다르지만, 얼핏 보면 한 카펫 같아요"),
             sc("문장 8~9", "⚽", "daily life ↔ groundskeeper", "보통은 차이를 신경 안 써도 되지만, 경기장 관리인에겐 중요해요")]),
        (11, [sc("문장 10~11", "♾️", "infinite mind → its own name", "끝없는 기억이 있다면 풀잎마다 이름을 붙일 수 있어요")]),
    ],
    "moeui-2026-03-33-profound-building": [
        (3, [sc("문장 1~2", "🩰", "spatial choreography", "건물은 춤 안무처럼 사람의 움직임과 느낌을 이끌어요"),
             sc("문장 3", "💭", "designer intuits", "좋은 설계자는 사람이 원하는 걸 미리 느껴요")]),
        (6, [sc("문장 4", "🏠", "lives in imagination", "아직 없는 집에 상상으로 살아 봐요"),
             sc("문장 5~6", "🪟", "window · stairway", "창과 계단이 사는 사람이 원하는 바로 그 자리에 있어요")]),
    ],
    "moeui-2026-03-38-gesture-glue": [
        (3, [sc("주어진 문장", "🙌", "gesture ≠ language · no choices", "몸짓은 말과 달리 선택을 강요하지 않아요"),
             sc("문장 1~2", "🗣️", "co-expressive · both", "말과 몸짓은 동시에 나오고, 둘 다로 생각을 표현해요")]),
        (5, [sc("①~②", "⏳", "language → must choose", "말은 끝났는지, 진행 중인지 하나를 골라야 해요")]),
        (8, [sc("③~⑤", "🧩", "glue · combination of the two", "몸짓은 풀처럼 말을 묶고, 생각의 단위는 둘의 조합이에요")]),
    ],
    "moeui-2026-03-39-epistemic-communities": [
        (3, [sc("주어진 문장", "🫥", "Nonetheless · outsiders", "그래도 외부인은 훈련 없이는 지식을 이해할 수 없어요"),
             sc("첫 문장·①", "👥", "become a member · learns from experts", "전문 지식을 얻으려면 그 집단의 일원이 되어 배워야 해요")]),
        (5, [sc("②~③", "🔒", "tests · kept secret", "입회 시험이 있고, 옛날엔 집단을 비밀로 지켰어요")]),
        (7, [sc("④~⑤", "🔓", "openness · more active strategies", "지금은 개방이 이상이고, 더 적극적인 방법도 필요해요")]),
    ],
}

SAY_FIRST = "여기까지 어떤 상황인지 칠판에 정리해 볼게요."
SAY_NEXT = "칠판에 이어서 정리해 볼게요."
SAY_LAST = "글 전체가 어떤 이야기인지 칠판으로 한 번 볼게요."


def _is_go(step):
    return (step.get("button") or "").startswith("문제 풀러")


def add_story_boards(lesson_id, sentences):
    """문장 공부 끝에 칠판 정리 스텝을 끼운다 — 장면은 쌓이고, 이번에 붙은 장면만 노랗게"""
    plan = STORIES.get(lesson_id)
    if not plan:
        return []
    by_id = {s["id"]: s for s in sentences}
    shown, added = [], []
    for n, (after, scenes) in enumerate(plan):
        s = by_id[after]
        s["steps"] = [st for st in s["steps"] if not st["id"].startswith("story_")]
        steps = s["steps"]
        # 「문제 풀러」·순서 잇기 앞에 — 칠판으로 정리한 뒤에 잇는다
        at = len(steps) - 1 if steps and _is_go(steps[-1]) else len(steps)
        while at > 0 and steps[at - 1]["id"] == "order_link":
            at -= 1
        last_in_lesson = after == sentences[-1]["id"]
        say = SAY_FIRST if n == 0 else SAY_LAST if last_in_lesson and len(plan) > 2 else SAY_NEXT
        board = {
            "kind": "story", "title": "지금까지 이야기",
            "scenes": [{**x, "fresh": False} for x in shown] + [{**x, "fresh": True} for x in scenes],
        }
        shown += scenes
        # 「다음 문장」은 칠판 쪽으로 옮긴다 — 바로 앞 화면은 「다음」
        prev = steps[at - 1] if at > 0 else None
        button = "다음"
        if at == len(steps):
            if prev and prev.get("button") == "다음 문장":
                prev["button"] = "다음"
            button = "다음 문장"
        step = {"id": f"story_{after}", "type": "show", "interaction": "note",
                "brief": {"say": say}, "method": 0, "button": button, "panel": board}
        steps.insert(at, step)
        added.append(step)
    return added


def _apply_to_json(lesson_id):
    """손으로 쓴 레슨 — JSON과 대사 파일에 바로 넣는다"""
    lp = f"{ROOT}/content/tutor/policy-lessons/{lesson_id}.json"
    cp = f"{ROOT}/content/tutor/policy-copy/dajung/{lesson_id}.json"
    lesson = json.load(open(lp))
    # 이전에 넣은 칠판을 빼면서 버튼을 되돌린다
    for s in lesson["sentences"]:
        old = [i for i, st in enumerate(s["steps"]) if st["id"].startswith("story_")]
        for i in old:
            if s["steps"][i]["button"] == "다음 문장" and i > 0 and s["steps"][i - 1].get("button") == "다음":
                s["steps"][i - 1]["button"] = "다음 문장"
    added = add_story_boards(lesson_id, lesson["sentences"])
    json.dump(lesson, open(lp, "w"), ensure_ascii=False, indent=2)
    c = json.load(open(cp))
    c["steps"] = {k: v for k, v in c["steps"].items() if not k.startswith("story_")}
    for st in added:
        c["steps"][st["id"]] = copy.deepcopy(st["brief"])
    json.dump(c, open(cp, "w"), ensure_ascii=False, indent=2)
    print("ok", lesson_id, [st["id"] for st in added])


if __name__ == "__main__":
    _apply_to_json(sys.argv[1])
