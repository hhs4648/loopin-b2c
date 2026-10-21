"""2026년 9월 모의평가(2027학년도) 38번 레슨 + 대사를 만든다 (주어진 문장 넣기, 2점). 오답률 49% · Top 4 (메가스터디).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_38.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/insertion.md — 주어진 문장 상황 → 단서(rather than scientists) → 앞에 올 내용 → ①~⑤ 흐름 확인 → 정답 열쇠.
정답 ⑤. 주어진 문장: Citizen engagement involves people helping governments, rather than scientists, to improve public services …
열쇠 — ① rather than scientists(과학자가 아니라): 앞에는 사람들이 과학자를 돕는 이야기(시민 과학)가 와야 한다.
② ⑤ 뒤 Examples(재난 대비 웹사이트·비상 대응팀)는 과학 활동이 아니다 → 정부를 돕는 일(주어진 문장)의 예.
선택률(메가스터디): ① 2 · ② 7 · ③ 16 · ④ 24 · ⑤ 51 — 많이 고른 오답 ④(They do so 앞), ③(such projects 앞) 둘 다 option_review.
주어진 문장 정석(insertion-given-sentence-order): 「앞에 무엇?」은 rather than이라는 대조 근거가 있어서 묻고, 「뒤에 무엇?」은 묻지 않는다.
단어 지도(누구를 돕나: 과학자 / 정부)에 citizen engagement → citizen science → emergency response team을 차례로 넣는다.
시험지 아래 * 풀이 단어는 이 문항에 없다.
해설지(content/tutor/exam-source/2027-09-평가원/해설.txt) 해석과 대조함 — engagement 참여, instrumental 중요한, at scale 대규모,
whereby 그로 인해, do so 그렇게 한다(= help out), encouraging and coordinating 이는 … 장려하고 조정한다, Examples 예시로는.
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음), 「앞을 가리키는 말」 Tip은 맞힌 뒤에만(praise_tips).
Claude 초안(2026-10-21) — 선생님 검토 전.

선생님이 확인할 점
1. 단서를 rather than scientists 하나로 찾게 했다(g_clue). 해설지 풀이도 「과학자를 도와 … 시민 과학에 관한 내용에 이어」라고 한다.
   ②~③ 사이 Citizen science involves local people helping scientists …와 주어진 문장이 같은 모양(X involves people helping Y)이라는 점은
   짚지 않았다 — 필요하면 s4_sort 설명에 한 줄 넣을 수 있다.
2. 칠판은 단어 지도(누구를 돕나 — 과학자 / 정부) 하나로 정리하고, 칠판 정리(story)는 넣지 않았다 — 칠판이 너무 많아질까 봐.
3. 헷갈리는 단어(trap): engagement(참여, 약혼 X) · instrumental(중요한 역할을 하는, 악기의 X) · at scale(대규모로, 저울 X). 엑셀에는 안 넣었다.
4. 해석 맞추기는 ②~③ 사이 문장(Citizen science involves …)에만 넣었다.
5. 많이 고른 오답 ④는 「They do so가 주어진 문장의 people을 받는다고 읽어서」, ③은 「Citizen science 정의 바로 뒤에 짝 정의를 붙여서」로 봤다(추측).
6. 2점 문제라 39번보다 화면을 줄였다(16스텝 안팎).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, tip, rows, sense, groups, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)
from beginner import add_match, add_refers, m  # noqa: E402

ID = "mopyeong-2027-09-38-citizen-science"

GIVEN = ("Citizen engagement involves people helping governments, rather than scientists, to improve public services and policies "
         "in their communities.")
S = [
    "The growth and success of citizen science and citizen engagement has been made possible by the Internet and mobile technology, "
    "encouraging and coordinating the efforts of millions of people throughout the world.",
    "(①) Websites, smartphone apps, and social media have been instrumental in expanding the reach and impact of a diversity of "
    "citizen science projects across time and geographical zones.",
    "(②) Citizen science involves local people helping scientists carry out a scientific project at scale.",
    "(③) Currently, thousands of such projects have been set up all over the world, whereby volunteers help out in a number of "
    "research areas, including biodiversity, air quality, astronomy, and environmental issues.",
    "(④) They do so by participating in scientific activities such as monitoring plants and wildlife, collecting air and water "
    "samples, categorizing galaxies, and analyzing DNA sequences.",
    "(⑤) Examples include setting up and managing a website that offers local services for community disasters and creating an "
    "emergency response team when a disaster occurs.",
]
# 해설지 해석 (2027-09-평가원/해설.txt 38번)
KO_GIVEN = "시민 참여는 지역 사회의 공공 서비스와 정책을 개선하기 위해, 사람들이 과학자가 아니라 정부를 돕는 것을 포함한다."
KO = [
    "시민 과학 및 시민 참여의 성장과 성공은 인터넷과 모바일 기술에 의해 가능해졌으며, 이는 전 세계 수백만 명의 노력을 장려하고 조정한다.",
    "웹사이트, 스마트폰 앱, 소셜 미디어는 시간과 지리적 구역을 넘어 다양한 시민 과학 프로젝트의 범위와 영향력을 확장하는 데 중요한 역할을 해왔다.",
    "시민 과학은 과학자가 대규모 과학 프로젝트를 수행하는 것을 지역 사람들이 돕는 것을 포함한다.",
    "현재 수천 개의 그러한 프로젝트가 전 세계적으로 창설되어 있으며, 그로 인해 자원봉사자들은 생물 다양성, 대기의 질, 천문학, 환경 문제를 "
    "포함한 수많은 연구 분야에서 도움을 준다.",
    "그들은 식물과 야생 동물을 관찰하고, 공기와 물 표본을 수집하며, 은하를 분류하고, DNA 서열을 분석하는 것과 같은 과학 활동에 참여함으로써 "
    "그렇게 한다.",
    "예시로는 공동체의 재난에 대비한 지역 서비스를 제공하는 웹사이트를 만들고 관리하는 것과 재난 발생 시 비상 대응팀을 만드는 것을 포함한다.",
]

LEFT = "왼쪽 · 과학자 돕기"
RIGHT = "오른쪽 · 정부 돕기"


def board(left, right, fresh=()):
    return groups("누구를 돕나", "scientists (과학자)", left, "governments (정부)", right, fresh=fresh, between="≠")


def flow(id, place, before, after, ok, why, praise="맞아요!"):
    """①~⑤ 자리마다 — 앞 문장과 뒤 문장이 그대로 이어지나. 끊김은 정답 자리 하나뿐"""
    return choice(id, f"{place} 자리예요. '{before}' → '{after}', 자연스럽게 이어지나요?",
                  [("o0", "네, 이어져요", ok), ("o1", "아니요, 끊겨요", not ok)], why, why=why, praise=praise,
                  highlight=[f"({place})"], method=2)


sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN, "model_translation": KO_GIVEN, "teaching_value": "high",
        "glosses": [g("Citizen engagement", "시민 참여"), g("Citizen", "시민"), g("engagement", "참여"),
                    g("involves", "포함하다, ~하는 것이다"), g("people", "사람들"), g("helping governments", "정부를 돕는"),
                    g("helping", "돕는"), g("governments", "정부"), g("rather than scientists", "과학자가 아니라"),
                    g("rather than", "~가 아니라"), g("scientists", "과학자"), g("to improve", "개선하기 위해"), g("improve", "개선하다"),
                    g("public services and policies", "공공 서비스와 정책"), g("public", "공공의"), g("services", "서비스"),
                    g("policies", "정책"), g("in their communities", "그들의 지역 사회에서"), g("communities", "지역 사회")],
        "emphasis": ["Citizen engagement", "rather than scientists"],
        "slashes": ["helping governments,", "rather than scientists,", "public services and policies"],
        "roles": [r("Citizen engagement", "S"), r("involves", "V"), r("people helping governments", "O")],
        "steps": [
            choice("g_situation",
                   "주어진 문장은 무슨 말일까요?",
                   [("o0", "시민 참여는 사람들이 과학자가 아니라 정부를 돕는 것이다", True),
                    ("o1", "시민 참여는 사람들이 정부가 아니라 과학자를 돕는 것이다", False),
                    ("o2", "과학자들이 정부를 도와 공공 서비스를 개선한다", False)],
                   "A, rather than B는 'B가 아니라 A'예요. helping 바로 뒤에 누가 오는지 봐요.",
                   why="'people helping governments, rather than scientists', 사람들이 과학자가 아니라 정부를 돕는 거래요. 지역 사회의 공공 서비스와 정책을 개선하려고요.",
                   highlight=["helping governments", "rather than scientists"],
                   tips=[tip("A, rather than B", "'B가 아니라 A'예요. 콤마(,) 두 개 사이에 끼어 있어도 앞의 governments와 짝이에요.", "rather than")],
                   point="주어진 문장 = 시민 참여는 사람들이 (과학자가 아니라) 정부를 도와 공공 서비스·정책을 개선하는 것"),
            pick("g_clue", "주어진 문장에서 앞에 어떤 이야기가 있었는지 알려 주는 말을 찾아 눌러 볼까요?",
                 ["Citizen engagement", "helping governments", "rather than scientists", "public services and policies"],
                 ["rather than scientists"],
                 "그건 이 문장 안에서 뜻이 끝나는 말이에요. 무엇과 비교하고 있는지 알려 주는 말을 찾아봐요.",
                 "'rather than scientists(과학자가 아니라)'예요. 과학자를 돕는 이야기와 다르다고 말하고 있어요.",
                 wrong_by={"helping governments": "helping governments는 이 문장이 새로 하는 말이에요. 무엇과 다르다고 하는지 찾아봐요.",
                           "Citizen engagement": "Citizen engagement는 이 문장의 주어예요. 앞 이야기와 비교하는 말을 찾아봐요."},
                 praise_tips=[{"label": "대조하는 말", "text": "rather than, instead, unlike처럼 무엇과 다르다고 말하는 표현이 있으면, 비교 대상이 앞에 나와 있을 때가 많아요."}],
                 point="단서 = rather than scientists (과학자를 돕는 이야기와 대비)"),
            choice("g_before",
                   "그럼 이 문장 바로 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "사람들이 과학자를 도와 과학 활동을 하는 이야기", True),
                    ("o1", "정부가 공공 서비스를 개선하는 방법", False),
                    ("o2", "인터넷이 사람들의 노력을 모아 준다는 이야기", False)],
                   "rather than scientists(과학자가 아니라)를 떠올려 봐요. 무엇과 다르다고 말하려면 그 대상이 앞에 있어야 해요.",
                   why="'rather than scientists'라고 했으니 앞에는 과학자를 돕는 이야기가 와야 해요. 그 이야기와 달리 시민 참여는 정부를 돕는다는 흐름이에요.",
                   highlight=["rather than scientists"],
                   point="주어진 문장 앞 = 사람들이 과학자를 돕는 이야기 (rather than scientists)"),
            show("g_before_note",
                 "지문을 읽으며 사람들이 과학자를 돕는 이야기가 어디서 끝나는지 찾아봐요.",
                 panel=board([], ["citizen engagement"]), button="지문 읽어 볼게요"),
        ],
    },
    {
        "id": 2, "text": S[0], "model_translation": KO[0], "teaching_value": "medium",
        "glosses": [g("The growth and success", "성장과 성공"), g("growth", "성장"), g("success", "성공"),
                    g("citizen science", "시민 과학"), g("citizen", "시민"), g("science", "과학"),
                    g("citizen engagement", "시민 참여"), g("engagement", "참여"),
                    g("has been made possible", "가능해졌다"), g("possible", "가능한"),
                    g("by the Internet and mobile technology", "인터넷과 모바일 기술에 의해"), g("Internet", "인터넷"),
                    g("mobile technology", "모바일 기술"), g("mobile", "모바일, 이동하는"), g("technology", "기술"),
                    g("encouraging and coordinating", "(이는) 장려하고 조정한다"), g("encouraging", "장려하는"),
                    g("coordinating", "조정하는, 한데 맞추는"), g("the efforts", "노력"), g("efforts", "노력"),
                    g("millions of people", "수백만 명"), g("millions", "수백만"), g("throughout the world", "전 세계의"),
                    g("throughout", "~ 전체에 걸쳐")],
        "slashes": ["The growth and success", "and citizen engagement", "has been made possible", "mobile technology,",
                    "coordinating the efforts", "millions of people"],
        "roles": [r("The growth and success of citizen science and citizen engagement", "S"), r("has been made", "V"),
                  r("possible", "C")],
        "steps": [
            choice("s2_mean",
                   "시민 과학과 시민 참여가 커지고 성공할 수 있었던 것은 무엇 덕분이래요?",
                   [("o0", "인터넷과 모바일 기술", True), ("o1", "전 세계 과학자들의 연구", False), ("o2", "정부의 새 정책", False)],
                   "'has been made possible by ~'는 '~에 의해 가능해졌다'예요. by 뒤를 봐요.",
                   why="'has been made possible by ~'는 '~에 의해 가능해졌다'예요. by 뒤의 the Internet and mobile technology를 봐요.",
                   highlight=["has been made possible", "Internet", "mobile technology"],
                   tips=[tip("콤마(,) 뒤 -ing", "앞 내용이 하는 일을 덧붙여요. encouraging and coordinating ~ = (이는) ~을 장려하고 조정한다.",
                             "encouraging and coordinating")]),
        ],
    },
    {
        "id": 3, "text": S[1], "model_translation": KO[1], "teaching_value": "medium",
        "glosses": [g("Websites", "웹사이트"), g("smartphone apps", "스마트폰 앱"), g("smartphone", "스마트폰"), g("apps", "앱"),
                    g("social media", "소셜 미디어"), g("social", "사회의"), g("media", "미디어"),
                    g("have been instrumental", "중요한 역할을 해 왔다"), g("instrumental", "중요한 역할을 하는"),
                    g("in expanding", "확장하는 데"), g("expanding", "확장하는, 넓히는"),
                    g("the reach and impact", "범위와 영향력"), g("reach", "미치는 범위"), g("impact", "영향력"),
                    g("a diversity of", "다양한"), g("diversity", "다양성"),
                    g("citizen science projects", "시민 과학 프로젝트"), g("projects", "프로젝트"),
                    g("across time and geographical zones", "시간과 지리적 구역을 넘어"), g("across", "~을 넘어, ~에 걸쳐"),
                    g("geographical", "지리적인"), g("zones", "구역")],
        "slashes": ["and social media", "have been instrumental", "the reach and impact", "citizen science projects"],
        "roles": [r("Websites, smartphone apps, and social media", "S"), r("have been", "V"), r("instrumental", "C")],
        "steps": [
            flow("s3_flow", "①", "인터넷과 모바일 기술이 시민 과학·시민 참여를 가능하게 했다",
                 "웹사이트·앱·소셜 미디어가 시민 과학 프로젝트를 넓혔다", True,
                 "앞의 인터넷과 모바일 기술을 웹사이트·앱·소셜 미디어로 구체적으로 이어 가요. 흐름이 끊기지 않아요."),
        ],
    },
    {
        "id": 4, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("Citizen science", "시민 과학"), g("involves", "포함하다, ~하는 것이다"), g("local people", "지역 사람들이"),
                    g("local", "지역의"), g("helping scientists", "과학자를 도와"), g("helping", "돕는"), g("scientists", "과학자"),
                    g("carry out", "수행하다"), g("carry out a scientific project", "과학 프로젝트를 수행하는 것을"),
                    g("scientific", "과학의"), g("project", "프로젝트"), g("at scale", "대규모로"), g("scale", "규모")],
        "slashes": ["local people", "helping scientists", "a scientific project"],
        "roles": [r("Citizen science", "S"), r("involves", "V"), r("local people helping scientists", "O")],
        "steps": [
            choice("s4_sort",
                   "Citizen science(시민 과학)는 어느 쪽에 들어갈까요?",
                   [("o0", LEFT, True), ("o1", RIGHT, False)],
                   "'local people helping ~' 뒤에 누가 오는지 봐요.",
                   why="'local people helping scientists', 시민 과학은 지역 사람들이 과학자를 돕는 거예요.",
                   highlight=["helping scientists"],
                   panel={**board([], ["citizen engagement"]), "sort": {"words": ["citizen science"], "left": LEFT, "right": RIGHT}},
                   point="citizen science = 사람들이 과학자를 돕는다 (주어진 문장의 citizen engagement와 반대쪽)"),
            flow("s4_flow", "②", "웹사이트·앱·소셜 미디어가 시민 과학 프로젝트를 넓혔다", "시민 과학은 사람들이 과학자를 돕는 것이다", True,
                 "앞 문장의 citizen science projects에서 시민 과학이 무엇인지 풀어 줘요. 그대로 이어져요."),
        ],
    },
    {
        "id": 5, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("Currently", "현재"), g("thousands of such projects", "수천 개의 그러한 프로젝트"), g("thousands", "수천"),
                    g("such projects", "그러한 프로젝트"), g("projects", "프로젝트"),
                    g("have been set up", "만들어져 있다"), g("set up", "세우다, 만들다"),
                    g("all over the world", "전 세계적으로"), g("whereby", "그로 인해, 그것에 의해"),
                    g("volunteers", "자원봉사자들"), g("help out", "돕다, 거들다"), g("a number of", "많은, 수많은"),
                    g("research areas", "연구 분야"), g("research", "연구"), g("areas", "분야"), g("including", "~을 포함한"),
                    g("biodiversity", "생물 다양성"), g("air quality", "대기의 질"), g("quality", "질"), g("astronomy", "천문학"),
                    g("environmental issues", "환경 문제"), g("environmental", "환경의"), g("issues", "문제")],
        "slashes": ["Currently,", "such projects", "all over the world,", "whereby volunteers help out", "research areas,",
                    "air quality,"],
        "roles": [r("thousands of such projects", "S"), r("have been set up", "V")],
        "modifiers": ["whereby volunteers help out in a number of research areas"],
        "steps": [
            choice("s5_such",
                   "'such projects(그러한 프로젝트)'는 어떤 프로젝트일까요?",
                   [("o0", "사람들이 과학자를 돕는 과학 프로젝트", True), ("o1", "사람들이 정부를 돕는 프로젝트", False),
                    ("o2", "웹사이트를 새로 만드는 프로젝트", False)],
                   "such(그러한)는 바로 앞 문장에서 말한 것을 가리켜요. 앞 문장의 a scientific project를 봐요.",
                   why="such projects는 바로 앞 문장의 a scientific project, 곧 사람들이 과학자를 돕는 시민 과학 프로젝트예요.",
                   highlight=["such projects"],
                   tips=[tip("whereby", "'그로 인해, 그것에 의해'예요. 앞 내용(프로젝트가 생긴 것)을 받아 자원봉사자들이 돕는다는 말로 이어 가요.",
                             "whereby")]),
            flow("s5_flow", "③", "시민 과학은 사람들이 과학자를 돕는 것이다", "지금 전 세계에 그러한 프로젝트가 수천 개 있다", True,
                 "such projects(그러한 프로젝트)가 바로 앞의 a scientific project를 받아요. 그대로 이어져요."),
        ],
    },
    {
        "id": 6, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("They", "그들(자원봉사자들)"), g("do so", "그렇게 하다 (= 앞의 help out)"),
                    g("by participating in", "~에 참여함으로써"), g("participating", "참여하는"),
                    g("scientific activities", "과학 활동"), g("scientific", "과학의"), g("activities", "활동"),
                    g("such as", "~와 같은"), g("monitoring plants and wildlife", "식물과 야생 동물을 관찰하는 것"),
                    g("monitoring", "관찰하는, 감시하는"), g("plants", "식물"), g("wildlife", "야생 동물"),
                    g("collecting air and water samples", "공기와 물 표본을 모으는 것"), g("collecting", "모으는"), g("air", "공기"),
                    g("water", "물"), g("samples", "표본"), g("categorizing galaxies", "은하를 분류하는 것"),
                    g("categorizing", "분류하는"), g("galaxies", "은하"), g("analyzing DNA sequences", "DNA 서열을 분석하는 것"),
                    g("analyzing", "분석하는"), g("DNA", "디엔에이"), g("sequences", "서열")],
        "slashes": ["They do so", "scientific activities", "plants and wildlife,", "water samples,", "categorizing galaxies,"],
        "roles": [r("They", "S"), r("do so", "V")],
        "steps": [
            choice("s6_doso",
                   "'They do so'는 누가 무엇을 한다는 말일까요?",
                   [("o0", "자원봉사자들이 연구 분야에서 돕는다", True), ("o1", "과학자들이 새 프로젝트를 만든다", False),
                    ("o2", "정부가 공공 서비스를 개선한다", False)],
                   "They는 바로 앞 문장의 사람들, do so는 앞 문장의 동사를 다시 받는 말이에요.",
                   why="They는 앞 문장의 volunteers(자원봉사자들), do so는 help out(돕다)을 다시 받아요. 과학 활동에 참여해서 돕는대요.",
                   highlight=["They do so"]),
            flow("s6_flow", "④", "자원봉사자들이 여러 연구 분야에서 돕는다", "그들은 과학 활동에 참여해서 그렇게 한다", True,
                 "They(자원봉사자들)와 do so(돕는다)가 바로 앞 문장을 받아요. 그대로 이어져요."),
        ],
    },
    {
        "id": 7, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Examples", "예시"), g("include", "포함하다"), g("setting up and managing", "만들고 관리하는 것"),
                    g("setting up", "만드는 것, 세우는 것"), g("managing", "관리하는 것"), g("a website", "웹사이트"),
                    g("website", "웹사이트"), g("offers", "제공하다"), g("local services", "지역 서비스"), g("local", "지역의"),
                    g("services", "서비스"), g("for community disasters", "공동체의 재난에 대비한"),
                    g("community disasters", "공동체의 재난"), g("community", "공동체, 지역 사회"), g("disasters", "재난"),
                    g("creating", "만드는 것"), g("an emergency response team", "비상 대응팀"),
                    g("emergency response team", "비상 대응팀"), g("emergency", "비상, 긴급"), g("response", "대응"),
                    g("team", "팀"), g("when a disaster occurs", "재난이 일어날 때"), g("a disaster", "재난"),
                    g("disaster", "재난"), g("occurs", "일어나다")],
        "slashes": ["Examples include", "a website", "local services", "community disasters", "response team"],
        "roles": [r("Examples", "S"), r("include", "V"), r("setting up and managing a website", "O"),
                  r("creating an emergency response team", "O"), r("a disaster", "S"), r("occurs", "V")],
        "modifiers": ["that offers local services for community disasters"],
        "steps": [
            flow("s7_flow", "⑤", "식물 관찰·DNA 분석 같은 과학 활동에 참여한다",
                 "예로는 재난 대비 웹사이트와 비상 대응팀 만들기가 있다", False,
                 "재난 대비 웹사이트와 비상 대응팀은 과학 활동이 아니에요. Examples가 무엇의 예인지 앞에 없어서 흐름이 끊겨요.",
                 praise="맞아요! 여기서 흐름이 끊겨요."),
            choice("s7_sort",
                   "재난 대비 웹사이트와 비상 대응팀(emergency response team)은 어느 쪽에 들어갈까요?",
                   [("o0", LEFT, False), ("o1", RIGHT, True)],
                   "과학 연구를 돕는 일인지, 지역 사회의 공공 서비스인지 생각해 봐요.",
                   why="재난에 대비한 지역 서비스는 과학 연구가 아니라 지역 사회의 공공 서비스예요. 주어진 문장의 citizen engagement 쪽이에요.",
                   highlight=["local services", "emergency response team"],
                   panel={**board(["citizen science"], ["citizen engagement"]),
                          "sort": {"words": ["emergency response team"], "left": LEFT, "right": RIGHT}},
                   point="⑤ 뒤 Examples(재난 대비 웹사이트·비상 대응팀) = 정부를 돕는 일의 예 ← 주어진 문장이 먼저 와야"),
            show("s7_go", "①~⑤ 중 흐름이 끊긴 곳은 하나였어요. 주어진 문장의 rather than scientists를 떠올리며 골라 봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — ②~③ 사이 문장(짧은 문장, 모두에게). 덩어리는 문장에 그대로 있는 구절
add_match(sentences, 4, [m("Citizen science", "시민 과학은"), " ", m("local people", "지역 사람들이"), " ",
                         m("helping scientists", "과학자를 도와"), " ", m("at scale", "대규모로"), " ",
                         m("carry out a scientific project", "과학 프로젝트를 수행하는 것을"), " ", m("involves", "포함한다"), "."])
# 가리키는 말
add_refers(sentences, 6, {"They": "volunteers(자원봉사자들)"})

SENSES = {
    1: [sense("to", "to improve", "~하기 위해", "to부정사 (목적)")],
    6: [sense("so", "do so", "그렇게", "do so = 앞의 동사(help out)를 다시 받는 말"),
        sense("as", "such as monitoring", "~와 같은", "such as = ~ 같은, 예를 들어")],
    7: [sense("that", "a website that offers", "~하는 (웹사이트)", "관계대명사 that — a website를 꾸밈"),
        sense("for", "for community disasters", "~에 대비한", "전치사 for (대비·목적)")],
}

WORDS = {"citizen": "시민", "engagement": "참여", "involves": "포함하다", "people": "사람들", "helping": "돕는", "governments": "정부",
         "scientists": "과학자", "improve": "개선하다", "public": "공공의", "services": "서비스", "policies": "정책",
         "communities": "지역 사회", "growth": "성장", "success": "성공", "science": "과학", "possible": "가능한", "made": "만들어진 · be made possible = 가능해지다",
         "internet": "인터넷", "mobile": "모바일", "technology": "기술", "encouraging": "장려하는", "coordinating": "조정하는",
         "efforts": "노력", "millions": "수백만", "throughout": "~ 전체에 걸쳐", "world": "세계", "websites": "웹사이트",
         "smartphone": "스마트폰", "apps": "앱", "social": "사회의", "media": "미디어", "instrumental": "중요한 역할을 하는",
         "expanding": "확장하는", "reach": "범위", "impact": "영향력", "diversity": "다양성", "projects": "프로젝트",
         "geographical": "지리적인", "zones": "구역", "local": "지역의", "carry": "수행하다 · carry out", "scientific": "과학의",
         "project": "프로젝트", "scale": "규모", "currently": "현재", "thousands": "수천", "set": "세우다 · set up",
         "whereby": "그로 인해", "volunteers": "자원봉사자들", "help": "돕다", "number": "수", "research": "연구", "areas": "분야",
         "including": "~을 포함한", "biodiversity": "생물 다양성", "air": "공기", "quality": "질", "astronomy": "천문학",
         "environmental": "환경의", "issues": "문제", "participating": "참여하는", "activities": "활동", "monitoring": "관찰하는",
         "plants": "식물", "wildlife": "야생 동물", "collecting": "모으는", "water": "물", "samples": "표본",
         "categorizing": "분류하는", "galaxies": "은하", "analyzing": "분석하는", "dna": "디엔에이", "sequences": "서열",
         "examples": "예시", "include": "포함하다", "setting": "세우는 · setting up", "managing": "관리하는", "website": "웹사이트",
         "offers": "제공하다", "community": "공동체", "disasters": "재난", "creating": "만드는", "emergency": "비상",
         "response": "대응", "team": "팀", "disaster": "재난", "occurs": "일어나다", "rather": "오히려 · rather than = ~가 아니라"}

OPTIONS = [
    ("1", "Websites, smartphone apps … 앞", "인터넷과 모바일 기술이 시민 과학·시민 참여를 가능하게 했다 뒤", False),
    ("2", "Citizen science involves … 앞", "웹사이트·앱·소셜 미디어가 시민 과학 프로젝트를 넓혔다 뒤", False),
    ("3", "Currently, thousands of such projects … 앞", "시민 과학은 사람들이 과학자를 돕는 것이다 뒤", False),
    ("4", "They do so by … 앞", "자원봉사자들이 여러 연구 분야에서 돕는다 뒤", False),
    ("5", "Examples include … 앞", "식물 관찰·DNA 분석 같은 과학 활동에 참여한다 뒤", True),
]
exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳을 고르시오.",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"], "numbers_only": True,
    "passage_keywords": ["governments", "scientists", "such", "Examples"],
    "sentence": 1, "analysis_first": True, "wrong_rate": 49, "wrong_rank": 4,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "주어진 문장의 rather than scientists와 ⑤ 뒤 Examples를 떠올리며 들어갈 곳을 골라 봐요.",
        "정답이에요! 시민 과학은 사람들이 과학자를 돕는 일(⑤ 앞까지 과학 활동 이야기) → 시민 참여는 과학자가 아니라 정부를 돕는 일(주어진 문장) → "
        "그 예시(Examples): 재난 대비 웹사이트·비상 대응팀, 순서예요.",
        "정답은 ⑤예요. ⑤ 뒤 Examples(재난 대비 웹사이트·비상 대응팀)는 과학 활동이 아니라 정부를 돕는 일의 예라서, 그 앞에 주어진 문장이 와야 해요.",
        {"1": "① 뒤 문장은 앞의 인터넷과 모바일 기술을 웹사이트·앱·소셜 미디어로 이어 가요. 아직 과학자를 돕는 이야기도 나오지 않았어요.",
         "2": "② 뒤에서 시민 과학(과학자를 돕는 일)이 처음 풀이돼요. 그 앞에 넣으면 rather than scientists가 비교할 이야기가 아직 없어요.",
         "3": "③ 뒤 such projects(그러한 프로젝트)는 바로 앞 a scientific project를 받아요. 사이에 넣으면 이 연결이 끊겨요.",
         "4": "④ 뒤 They do so는 앞 문장의 volunteers(자원봉사자들)와 help out(돕다)을 받아요. 사이에 넣으면 이 연결이 끊겨요."},
        {"4": review(24,
                     "④에 넣으면 They do so가 주어진 문장의 people을 받는 것처럼 보여서 끌려요. 그런데 그러면 정부를 돕는 사람들이 '과학 활동'에 "
                     "참여해서 돕는다는 말이 돼서 맞지 않아요.\nThey do so(자원봉사자들이 돕는다)는 바로 앞 문장을 받고, 주어진 문장은 과학 활동 이야기가 끝난 ⑤에 와야 해요.",
                     panel=rows(("③ 뒤", "whereby volunteers help out …", "자원봉사자들이 연구 분야에서 돕는다", "hl2"),
                                ("④ 뒤", "They do so by … scientific activities", "그들은 과학 활동에 참여해서 그렇게 한다", "hl2"),
                                ("⑤ 뒤", "Examples include … community disasters", "재난 대비 웹사이트·비상 대응팀", "hl")),
                     rank_word="가장 많이 고른"),
         "3": review(16,
                     "③에 넣으면 시민 과학 풀이 바로 뒤에 시민 참여 풀이가 와서 그럴듯해 보여요. 그런데 ③ 뒤 such projects(그러한 프로젝트)는 "
                     "과학 프로젝트를 받아야 해서, 그 사이에 정부 이야기가 끼면 연결이 끊겨요.\n과학 이야기는 ④ 뒤 문장까지 이어지고, ⑤에서 끝나요.",
                     panel=rows(("② 뒤", "Citizen science … helping scientists … a scientific project", "과학자를 돕는 과학 프로젝트", "hl2"),
                                ("③ 뒤", "thousands of such projects", "그러한(과학) 프로젝트 수천 개", "hl2")))}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 주어진 문장(위에서 넣음)과 열쇠 문장(4·7)만 ──
EMPHASIS = {
    4: ["Citizen science", "helping scientists"],
    7: ["Examples", "local services"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 38번 (주어진 문장 넣기, 2점)",
    topic="문장 넣기 푸는 법: 주어진 문장의 단서 → 앞에 올 내용 예측 → ①~⑤ 흐름이 끊기는 곳",
    method={"type": "sentence_insertion", "labels": ["주어진 문장 단서 찾기", "앞에 올 내용 예측하기", "흐름 끊기는 곳 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-citizen-science.svg", ("Citizen science", "시민 과학"), "&",
                                       ("Citizen engagement", "시민 참여"), "평범한 시민은 무엇을 도울 수 있을까?",
                                       "2026년 9월 모의평가 38번 도입 칠판"),
                      "alt": "칠판: Citizen science(시민 과학) & Citizen engagement(시민 참여)", "kind": "drawing"},
            "method": METHOD_IMAGES["insert"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "과학자가 아닌 평범한 시민도 무언가를 도울 수 있을까요? 이번 글은 시민 과학과 시민 참여를 다뤄요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "문장 넣기는 주어진 문장부터 꼼꼼히 봐야 해요. 그 안에 앞 문장과 이어지는 단서가 숨어 있어요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "단서를 찾고, 앞에 올 내용을 예측한 뒤, 흐름이 끊기는 곳을 찾아요."}}],
    exam=exam,
    key_words={"passage": [g("engagement", "참여"), g("involve", "포함하다"), g("rather than", "~가 아니라"), g("policy", "정책"),
                           g("coordinate", "조정하다"), g("instrumental", "중요한 역할을 하는"), g("expand", "확장하다"),
                           g("impact", "영향력"), g("geographical", "지리적인"), g("carry out", "수행하다"), g("at scale", "대규모로"),
                           g("whereby", "그로 인해"), g("volunteer", "자원봉사자"), g("biodiversity", "생물 다양성"),
                           g("astronomy", "천문학"), g("sample", "표본"), g("sequence", "서열"), g("disaster", "재난"),
                           g("emergency", "비상")],
               "options": []},
    sentences=sentences, english="medium", concept="medium")

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함:
# engagement 참여 · instrumental 중요한 · at scale 대규모.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다
TRAPS = {
    1: [tip("engagement", "이 글에서는 → 참여  ('약혼' 아님)", "engagement", trap=True)],
    3: [tip("instrumental", "이 글에서는 → 중요한 역할을 하는  ('악기의' 아님) · be instrumental in ~ing = ~하는 데 중요한 역할을 하다",
            "instrumental", trap=True)],
    4: [tip("scale", "이 글에서는 → 규모  ('저울' 아님) · at scale = 대규모로", "at scale", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="문장 넣기 푸는 법")
