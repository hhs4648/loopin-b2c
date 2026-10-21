"""2026년 3월 고3 41번 레슨 + 대사를 만든다 (41~42 장문 중 41번 — 제목, 2점). 오답률 60.8% · Top 7 (EBS).

    PYTHONUTF8=1 py scripts/lessons/gen_moeui_2026_03_42.py && PYTHONUTF8=1 py scripts/lessons/gen_moeui_2026_03_41.py   (→ stamp → npm run build)

지문은 42번과 같다 — 문장·뜻·끊어읽기·가리키는 말·기능어 쓰임은 42번 생성물에서 가져오고, 스텝만 제목용으로 새로 쓴다.
그래서 42번을 고치면 41번도 다시 돌린다.
틀: 제목(docs/tutor/templates/title.md) — 문장마다 핵심어 → 글쓴이 생각(두 그룹 칠판, +/−) → 글 전체 한 줄 → 바꿔 쓴 제목.
정답 ① The Significance of What Literary Mirrors Fail to Show.

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- 열쇠는 4문장: 비추지 않는 것(exclusions and distortions)도 중요하다(significant). 자유 응답(translate method 1) 하나 +
  평가 뒤집기(보통 나쁜 말인 배제·왜곡을 significant로 좋게 봄, +) — 핵심어이고 글쓴이 입장이 확고해서 넣었다
- 지문에 (d)praising(42번 정답 — 틀린 낱말)이 그대로 있어서 10문장에서는 Eliot의 말(defective)만 짚고 naive realism과의 관계는 말하지 않았다
  (41을 먼저 하면 42 답이 드러남). 그래서 10문장은 화면 하나뿐
- 많이 고른 오답 ④ 24.0% — 2문장의 as it stands가 보기에 그대로 나오지만 앞에 by no means(결코 ~이 아닌)가 있어 방향이 반대.
  ② 21.2% — 11·12문장에 viewpoint(관점)가 나와서. 관점은 오히려 거울 안에 안 보인다는 말이고, 작가가 관점을 전한다는 글이 아니다. 둘 다 option_review
- 보기 우리말 뜻(ko)은 해설지에 없어서 Claude가 옮겼다 — 확인 필요
- 글 전체 한 줄은 3지(2024 방식)로 물었다 — title.md 「아직 정할 것」
- 핵심어 찾기(keyword pick)는 넣지 않았다 — 핵심어는 선생님이 표시판에서 확인한 뒤(keys_checked)
- 칠판 정리(story)는 넣지 않았다 — 두 그룹 칠판이 정리 역할. 해석 맞추기도 데이터 세션 몫
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (ROOT, g, choice, show, tip, groups, topic_svg, base_lesson, exam_brief, review, finish)  # noqa: E402

ID = "moeui-2026-03-41-literary-mirror"
SRC = "moeui-2026-03-42-literary-mirror"

src = json.load(open(f"{ROOT}/content/tutor/policy-lessons/{SRC}.json"))
SENSES = {int(k): v for k, v in json.load(open(f"{ROOT}/content/tutor/function-senses/{SRC}.json")).items()}
KEEP = ("id", "text", "model_translation", "teaching_value", "glosses", "slashes", "roles", "modifiers", "emphasis", "refers")
sentences = [{k: s[k] for k in KEEP if k in s} | {"steps": []} for s in src["sentences"]]

LEFT = "있는 그대로 비춤"
RIGHT = "그대로 비추지 않음"


def board(left, right, fresh=()):
    return groups("문학이라는 거울", LEFT, left, RIGHT, right, fresh=fresh, between="↔")


L2 = [("direct reflection", "직접 비춤")]
R3 = [("complex affair", "복잡한 일"), ("flaws", "결함"), ("blind spots", "사각지대")]
R4 = R3 + [("exclusions", "배제"), ("distortions", "왜곡")]
R7 = R4 + [("what isn’t there", "그곳에 없는 것")]

# 4문장 자유 응답 — 규칙 채점(LLM 없음)
S4_FREE = {
    "id": "s4_free", "type": "translate", "interaction": "free_translation",
    "model": "문학 작품은 비추는 것만큼이나 비추지 않는 것(빼놓고 비튼 것) 때문에도 중요하다.",
    "labels": {"mine": "내 답", "model": "모범 답"},
    "rules": [
        {"id": "not_reflect",
         "need": ["비추지 않", "비추지 못", "안 비추", "안 비치", "비치지 않", "보여 주지 않", "보여주지 않", "보여 주지 못", "보여주지 못",
                  "안 보여", "빠", "배제", "없는", "드러나지 않", "왜곡", "비틀", "비튼", "결함"],
         "fix": "비추지 않는 것 때문에도"},
    ],
    "highlight": ["significant", "don’t reflect"],
    "brief": {
        "ask": "문학 작품은 무엇 때문에도 중요할까요? 자유롭게 써 봐요.",
        "praise": "잘 답했어요! 비추지 않는 것도 똑같이 중요하대요.",
        "wrong": "모범 답과 같이 봐요.",
        "explain": "괜찮아요. 모범 답을 같이 봐요.",
        "feedback": {"not_reflect": "what they don’t reflect는 '그것들이 비추지 않는 것'이에요. 대시(—) 사이 exclusions and distortions(배제와 왜곡)가 같은 말이에요."},
        "placeholder": "문학 작품은 …",
        "point": "as significant for what they don’t reflect … as for what they do = 비추는 것만큼이나 비추지 않는 것 때문에도 중요하다",
    },
    "tips": [tip("as ~ for A as for B", "'B만큼이나 A 때문에도 ~하다'예요. 여기선 비추는 것(what they do)만큼이나 비추지 않는 것(what they don’t reflect) 때문에도 중요하다는 말이에요.")],
    "method": 1,
}

STEPS = {
    1: [show("s1_mirror", "Tolstoy의 작품이 1905년 러시아 혁명을 비추는 거울이라는 주장에 Macherey도 동의한대요. 이 글은 '문학 = 거울'이라는 비유로 이어져요.",
             highlight=["holds up a mirror"], button="다음 문장",
             tips=[tip("Writing of ~, 주어 …", "Writing of ~는 '~에 관해 쓰면서'예요. 콤마(,) 뒤 the critic Pierre Macherey가 이 문장의 주어예요.", "Writing of")])],
    2: [choice("s2_mean",
               "Macherey는 이 거울 비추기(this mirroring)가 세상을 있는 그대로 비춘다고 할까요?",
               [("o0", "있는 그대로 비춘다", False), ("o1", "복잡하고, 결코 그대로 비추지 않는다", True)],
               "by no means를 봐요. not보다 센 부정, '결코 ~이 아닌'이에요.",
               why="'a complex affair, by no means a direct reflection', 복잡한 일이고 결코 직접 비추는 게 아니래요.",
               highlight=["complex affair", "by no means"],
               tips=[tip("by no means", "'결코 ~이 아닌'이에요. not보다 센 부정이에요.")],
               point="요지 시작: 문학이라는 거울은 세상을 결코 있는 그대로 비추지 않는다 (by no means = 결코 ~이 아닌)")],
    3: [show("s3_board", "결함(flaws)과 사각지대(blind spots)가 있는 거울이래요. 2문장의 '결코 그대로 비추지 않는다'와 같은 쪽이에요.",
             highlight=["flaws", "blind spots"], button="다음 문장",
             panel=board(L2, R3, fresh=("direct reflection", "complex affair", "flaws", "blind spots")))],
    4: [S4_FREE,
        choice("s4_sign",
               "exclusions(배제)와 distortions(왜곡)를 글쓴이는 좋게 볼까요, 나쁘게 볼까요?",
               [("o0", "좋게 (+) 본다", True), ("o1", "나쁘게 (−) 본다", False)],
               "문장 앞부분 they are as significant for ~를 봐요. significant는 '중요한'이에요.",
               why="'as significant for what they don’t reflect', 비추지 않는 것 때문에도 중요하대요. 중요하다고 했으니 좋게 봐요.",
               highlight=["significant"],
               point="exclusions·distortions = 보통은 나쁜 말이지만 significant(중요한)와 함께 쓰여 좋은 쪽(+)"),
        show("s4_plus", "배제와 왜곡은 보통 나쁜 말이에요. 그런데 여기선 significant(중요한)와 함께 쓰여서 좋은 쪽(+)이에요.",
             highlight=["significant"], button="다음 문장",
             signs=[{"text": "significant", "sign": "+"}],
             panel=board(L2, R4, fresh=("exclusions", "distortions")))],
    5: [show("s5_figure", "거울에 나타나지 않는(do not … figure) 것들이 있대요. Tolstoy에게는 그가 의식하지 못한 사회의 모순(contradictions)이 그랬대요.",
             highlight=["figure", "contradictions"], button="다음 문장",
             tips=[tip("figure", "이 글에서는 → (동사) 나타나다  ('숫자·인물' 아님)", "figure", trap=True)])],
    6: [choice("s6_aware",
               "그래도 거울은 이런 부재(absences)를 어떻게 한대요?",
               [("o0", "깨닫게 해 준다", True), ("o1", "완전히 감춘다", False)],
               "makes us aware of를 봐요. aware는 '알고 있는, 깨닫는'이에요.",
               why="'makes us aware of these absences', 우리가 그 부재를 깨닫게 해 준대요. 그래서 없는 것이 희미하게나마 존재하게 돼요.",
               highlight=["aware", "absences"],
               tips=[tip("present", "이 글에서는 → 존재하는  ('선물·현재' 아님)", "present", trap=True)],
               point="makes us aware of these absences = 거울은 그 부재를 깨닫게 해 준다 → 없는 것이 희미하게 존재하게 됨")],
    7: [show("s7_there", "거울 덕분에 그곳에 없는 것(what isn’t there)이 더 잘 보인대요. 4문장의 '비추지 않는 것도 중요하다'와 이어져요.",
             highlight=["what isn’t there"], button="다음 문장",
             panel=board(L2, R7, fresh=("what isn’t there",)))],
    9: [show("s9_pieces", "8·9문장: 거울 속 모습이 일관된 전체(coherent whole)일 이유는 없고, 오히려 조각나 있을(in pieces) 수도 있대요.",
             highlight=["On the contrary", "in pieces"], button="다음 문장")],
    10: [show("s10_eliot", "작가 Eliot도 거울은 불완전하고(defective), 윤곽이 흐트러지고, 상이 희미하다고 말해요.",
              highlight=["defective"], button="다음 문장",
              tips=[tip("‘인용’, remarks + 주어", "따옴표 말 뒤에 remarks George Eliot이 왔어요. 'Eliot이 ~라고 말한다'로 읽어요.")])],
    11: [show("s11_view", "거울은 현실의 한 버전(a version of reality)을 보여 주지만, 그 관점(viewpoint)은 거울 안에 담길 수 없대요.",
              highlight=["viewpoint", "cannot be captured"], button="다음 문장",
              tips=[tip("does so", "앞의 offers us a version of reality를 다시 쓰지 않으려고 does so로 받았어요.")])],
    12: [choice("s12_line",
                "마지막 문장까지 읽었어요. 글 전체를 한 줄로 묶으면 무엇일까요?",
                [("o0", "문학은 현실을 있는 그대로 비춰야 한다", False),
                 ("o1", "문학이라는 거울은 비추지 못하는 것 때문에도 중요하다", True),
                 ("o2", "좋은 문학은 모든 요소가 조화를 이룬다", False)],
                "4문장 as significant for what they don’t reflect를 떠올려 봐요.",
                why="2문장은 결코 그대로 비추지 않는다(by no means), 4문장은 비추지 않는 것도 중요하다(significant)고 했어요. 9문장도 조화롭지 않을 수 있대요.",
                point="글 전체 한 줄 = 문학이라는 거울은 비추지 못하는 것 때문에도 중요하다"),
         show("s12_go", "이 한 줄을 다른 말로 바꾼 제목을 골라 봐요.", button="문제 풀러 갈게요")],
}
for s in sentences:
    s["steps"] = STEPS.get(s["id"], [])

OPTIONS = [
    ("1", "The Significance of What Literary Mirrors Fail to Show", ["Significance", "What Literary Mirrors Fail to Show"],
     "문학이라는 거울이 보여 주지 못하는 것의 중요성", True),
    ("2", "Literature: A Tool for Writers to Deliver Their View", ["Deliver Their View"], "문학: 작가가 자기 관점을 전하는 도구", False),
    ("3", "Why Are We Fascinated by Twists in Literature?", ["Twists"], "우리는 왜 문학 속 반전에 끌리는가?", False),
    ("4", "The Power of Literature to Reflect Reality As It Stands", ["Reflect Reality As It Stands"], "현실을 있는 그대로 비추는 문학의 힘", False),
    ("5", "What Makes a Classic: All Elements Working in Harmony", ["Working in Harmony"], "고전을 만드는 것: 조화를 이루는 모든 요소", False),
]

exam = {
    "question": "윗글의 제목으로 가장 적절한 것은?", "sentence": 4, "analysis_first": True,
    "wrong_rate": 60.8, "wrong_rank": 7, "wrong_rate_source": "EBS",
    "glosses": [g("Significance", "중요성"), g("Literary Mirrors", "문학이라는 거울"), g("Fail to Show", "보여 주지 못하다"), g("Tool", "도구"),
                g("Deliver Their View", "자기 관점을 전하다"), g("Fascinated", "매료된, 끌리는"), g("Twists", "반전"), g("Power", "힘"),
                g("Reflect Reality", "현실을 비추다"), g("As It Stands", "있는 그대로"), g("Classic", "고전"), g("Elements", "요소"),
                g("Working in Harmony", "조화를 이루는")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "글 전체 한 줄을 다른 말로 바꾼 제목을 골라 봐요.",
        "정답이에요! What Literary Mirrors Fail to Show는 4문장의 what they don’t reflect를, Significance는 significant를 바꿔 쓴 말이에요.",
        "정답은 ①이에요. 문학이라는 거울이 비추지 못하는 것(what they don’t reflect)도 중요하다(significant)는 글이에요.",
        {"2": "viewpoint(관점)는 나오지만, 거울 안에 담기지 않아 보이지 않는다는 말이에요. 작가가 관점을 전한다는 글이 아니에요.",
         "3": "문학 속 반전(twists) 이야기는 글에 없어요.",
         "4": "2문장은 by no means, 결코 있는 그대로 비추지 않는다고 했어요. 방향이 반대예요.",
         "5": "9문장은 거울 속 모습이 조화롭지 않을(discordant) 수도 있다고 했어요. 방향이 반대예요."},
        {"4": review(24.0,
                     "as it stands가 2문장에 그대로 나와서 고르기 쉬워요. 하지만 그 앞에 by no means(결코 ~이 아닌)가 있어요. "
                     "문학은 세상을 있는 그대로 비추는 게 결코 아니래요.",
                     panel={"kind": "contrast", "title": "단어는 같아도 방향이 반대", "between": "↔",
                            "left": {"title": "2문장 · by no means a direct reflection of the world as it stands", "text": "결코 있는 그대로 비추지 않는다"},
                            "right": {"title": "④ Reflect Reality As It Stands", "text": "있는 그대로 비추는 힘"}},
                     rank_word="가장 많이 고른"),
         "2": review(21.2,
                     "11·12문장에 viewpoint(관점)가 나와서 고르기 쉬워요. 하지만 그 관점은 거울 안에 담기지 않아 우리에게 보이지 않는대요(invisible). "
                     "작가가 관점을 전한다는 글이 아니라, 비추지 못하는 것도 중요하다는 글이에요.",
                     panel={"kind": "contrast", "title": "viewpoint는 어떻게 쓰였나", "between": "↔",
                            "left": {"title": "11·12문장 · a viewpoint which cannot be captured … invisible to us", "text": "관점은 거울 안에 안 보인다"},
                            "right": {"title": "② A Tool for Writers to Deliver Their View", "text": "작가가 관점을 전하는 도구"}})}),
}

lesson = base_lesson(
    ID, source="2026년 3월 고3 전국연합학력평가 영어 41~42번 중 41번 (제목, 2점)",
    topic="제목 푸는 법: 문장마다 핵심어 → 글쓴이 생각(두 그룹, +/−) → 글 전체 한 줄 → 바꿔 쓴 제목",
    method={"type": "title", "labels": ["핵심어 찾기", "글쓴이 생각 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-literary-mirror.svg", ("Literature", "문학"), "=", ("Mirror", "거울"),
                                       "문학이라는 거울에는 무엇이 비칠까?", "2026년 3월 41~42번 도입 칠판"),
                      "alt": "칠판: Literature(문학) = Mirror(거울)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "문학 작품이 세상을 비추는 거울이라면, 그 거울엔 무엇이 비칠까요? 이번 글은 문학이라는 거울을 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "제목 문제는 글 전체를 한 줄로 묶는 말을 찾는 거예요. 문장마다 핵심어를 찾고 글쓴이 생각을 잡아 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("hold up a mirror to", "~을 비추어 보여 주다"), g("by no means", "결코 ~이 아닌"), g("reflection", "(비친) 상"),
                           g("flaw", "결함"), g("blind spot", "사각지대"), g("significant", "중요한"), g("exclusion", "배제"),
                           g("distortion", "왜곡"), g("figure", "나타나다"), g("absence", "부재"), g("viewpoint", "관점")],
               "options": [g("significance", "중요성"), g("fail to", "~하지 못하다"), g("deliver", "전하다"), g("fascinated", "매료된"),
                           g("twist", "반전"), g("as it stands", "있는 그대로"), g("in harmony", "조화를 이루어")]},
    sentences=sentences, concept="high")

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함 (work 작품 · figure 나타나다 · present 존재하는 · holds 믿다).
# 스텝이 없는 문장(8)은 없고, 10문장 holds는 화면 하나뿐이라 거기에 붙인다
TRAPS = {
    1: [tip("work", "이 글에서는 → 작품  ('일' 아님)", "work", trap=True)],
    10: [tip("holds", "이 글에서는 → ~라고 믿다, 주장하다  ('잡다' 아님)", "holds", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES,
       words={"significance": "중요성", "literary": "문학의", "mirrors": "거울", "fail": "~하지 못하다", "show": "보여 주다", "tool": "도구",
              "writers": "작가", "deliver": "전하다", "view": "관점", "fascinated": "매료된", "twists": "반전", "power": "힘",
              "reflect": "비추다", "reality": "현실", "stands": "서 있다 · as it stands = 있는 그대로", "classic": "고전", "elements": "요소",
              "working": "작용하는", "harmony": "조화"},
       topic_intro="제목 푸는 법")
