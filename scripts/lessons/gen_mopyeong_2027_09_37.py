"""2026년 9월 모의평가(2027학년도, 평가원) 37번 레슨 + 대사를 만든다 (글의 순서, 3점). 오답률 38% · Top 8 (메가스터디 풀서비스 채점 기준).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_37.py   (→ npm run policy:copy stamp <id> → npx vitest run src/tutor/policy)

틀: docs/tutor/templates/order.md — 주어진 글의 끝 → 단락 첫머리(앞에 무엇?) → 단락 끝(다음에 무엇?) → 순서 잇기.
정답 ④ (C)-(A)-(B). 많이 고른 오답 ⑤ (C)-(B)-(A) 23% — (B) 끝 'quite different from the initial wild ancestors(야생 조상과 아주 다른)'와
(A) 첫머리 'whatever the manifestation of difference(차이가 어떤 모습이든)'가 같은 말(different ↔ difference)이라 이었다.
그러나 (A)의 차이는 'difference that occurred in different species of salmon', 곧 (C)의 하천마다 다른 연어 이야기이고,
(A)의 the first salmon farmers(최초의 양식업자들)는 양식이 막 시작될 때다. (B)의 And … once favorable individuals were found는
(A)의 '더 빨리 자라는 연어를 얻는 교배'에 덧붙이는 말이다.
해설지 해석·Words and Phrases와 대조함 (content/tutor/exam-source/2027-09-평가원/해설.txt) — farmed '양식된', take place '이루어지다',
river system '수계', cross '교배시키다', family '계통', race '품종', domestic '사육되는', population '집단', ancestor '조상',
unique '고유한', a set of '일련의', reserve '비축량', extended '길어진', maximize '극대화하다'.
manifestation, offspring은 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다(뜻만 둠).
반영한 규칙: 2026-10-20 끊어읽기(slashes·roles·modifiers), S·V 찾기 없음, 핵심어 나열형 해석 없음, 2026-10-21 제출·보기 해설까지.

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- (C) 첫 문장 Every salmon river에는 앞을 받는 말이 없어서 「앞에 무엇이 와야 할까요?」(_before)를 넣지 않고 해석 맞추기만 두었다.
  하천 이야기로 이어진다는 것은 주어진 글 g_next(40개의 서로 다른 하천 → 하천마다 무엇이 다른지)에서 묻는다
- (C) 끝은 다음을 부르는 말이 없어서 「다음엔?」 대신 한 줄 정리 + 칠판(긴 하천 — 지방 비축 / 북쪽 하천 — 성장 극대화)만 두었다
- (A)는 한 문장 단락이라 a_before(But whatever … difference ← 앞에 연어들 사이의 차이)와 a_next(더 빨리 자라는 연어 → 그 연어로 새 품종)를 둘 다 묻는다
- (B) 끝 b_diff 「여기서 different는 무엇과 무엇이 다른가」 — ⑤ 23%(different ↔ difference를 이은 것)를 미리 짚으려고 넣었다
- 헷갈리는 단어(trap): cross(건너다 ✕ → 교배시키다), families(가족 ✕ → 계통), once(한 번 ✕ → 일단 ~하면), race(경주 ✕ → 품종),
  domestic(국내의 ✕ → 사육되는), reserves(예약 ✕ → 비축량)
- (B) 첫 문장 thousands는 해설지에서 '수천 마리의'에 작은따옴표 — 원문 기울임 글씨로 보인다. 텍스트에는 표시하지 않았다
- 해석 맞추기(add_match): (C) 첫 문장 하나
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from order_tools import card, order_link  # noqa: E402
from beginner import add_match, m  # noqa: E402

ID = "mopyeong-2027-09-37-farmed-salmon"

G = "The initial selection of farmed Atlantic salmon took place from fish drawn from forty different river systems."
A1 = ("(A) But whatever the manifestation of difference that occurred in different species of salmon, the first salmon farmers "
      "realized that crossing and recrossing the specific families from the original forty rivers would result in salmon that "
      "grew faster.")
B1 = ("(B) And because salmon, unlike cattle and sheep, can produce many thousands of offspring in the course of their lives, "
      "once favorable individuals were found, just a few strong males and females could form the basis of a whole new race of "
      "highly productive fish.")
B2 = "A domestic population could be created quickly that would be quite different from the initial wild ancestors."
C1 = "(C) Every salmon river has its own unique set of challenges to which fish must adapt."
C2 = ("Some rivers are very long, like the Yukon, and require animals that can build up massive fat reserves in order to survive "
      "the extended journey.")
C3 = ("Others are very far north, with only a short season of warmer temperatures, and require a fish that can maximize growth, "
      "particularly during its younger phase.")

sentences = [
    {
        "id": 1, "label": "주어진 글", "text": G, "teaching_value": "high",
        "model_translation": "양식 대서양 연어의 초기 선발은 40개의 서로 다른 하천 수계에서 가져온 물고기로부터 이루어졌다.",
        "glosses": [g("The initial selection", "초기 선발"), g("initial", "초기의"), g("selection", "선발, 고르기"),
                    g("farmed Atlantic salmon", "양식 대서양 연어"), g("farmed", "양식된"), g("Atlantic", "대서양의"),
                    g("salmon", "연어"), g("took place", "이루어졌다"), g("fish", "물고기"),
                    g("drawn from", "~에서 가져온"), g("drawn", "가져온, 뽑아 온"),
                    g("forty different river systems", "40개의 서로 다른 하천 수계"), g("forty", "40개의"),
                    g("different", "서로 다른"), g("river systems", "하천 수계 · 본류와 지류를 묶은 강 하나의 물줄기")],
        "slashes": ["of farmed Atlantic salmon", "took place", "from fish"],
        "roles": [r("The initial selection of farmed Atlantic salmon", "S"), r("took place", "V")],
        "modifiers": ["drawn from forty different river systems"],
        "steps": [
            choice("g_main",
                   "양식 연어를 처음 고를 때 물고기를 어디에서 가져왔대요?",
                   [("o0", "한 강에서만", False), ("o1", "바다 양식장에서", False), ("o2", "40개의 서로 다른 하천에서", True)],
                   "took place from fish drawn from … 뒤를 봐요.",
                   why="'fish drawn from forty different river systems', 40개의 서로 다른 하천 수계에서 가져온 물고기래요.",
                   highlight=["initial selection", "forty different river systems"],
                   tips=[tip("take place", "'일어나다, 이루어지다'예요. The initial selection … took place = 초기 선발이 이루어졌다.", "took place"),
                         tip("farmed", "'양식된'이에요. farmed salmon = 양식장에서 기른 연어.", "farmed")]),
            choice("g_next",
                   "주어진 글은 '40개의 서로 다른 하천에서 가져온 물고기'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "하천마다 무엇이 다른지", True), ("o1", "양식 연어를 요리하는 방법", False),
                    ("o2", "소와 양을 기르는 방법", False)],
                   "forty different river systems에서 different(서로 다른)를 봐요.",
                   why="서로 다른 40개 하천이라고 했어요. 다음엔 그 하천들이 어떻게 다른지 풀어 주는 말이 오기 쉬워요.",
                   highlight=["different river systems"],
                   point="주어진 글 끝 '40개의 서로 다른 하천' → 다음은 하천마다 다른 점"),
            show("paper_order", "이제 (A)·(B)·(C)를 시험지 순서대로 읽어요. 단락마다 첫머리와 끝을 잘 봐 두면 좋아요.",
                 button="(A)부터 읽어 볼게요"),
        ],
    },
    {
        "id": 2, "text": A1, "teaching_value": "high",
        "model_translation": "(A) 그러나 서로 다른 연어 종들 사이에서 나타난 차이가 무엇이든, 최초의 연어 양식업자들은 원래의 40개 하천에서 가져온 특정 계통들을 교배하고 재교배하면 더 빨리 자라는 연어를 얻게 될 것임을 깨달았다.",
        "glosses": [g("But whatever the manifestation of difference", "그러나 차이가 어떤 모습으로 나타났든"),
                    g("whatever", "무엇이든"), g("manifestation", "표현, 나타남"), g("difference", "차이"),
                    g("occurred", "생겼다, 나타났다"), g("different species of salmon", "서로 다른 연어 종들"),
                    g("species", "종"), g("the first salmon farmers", "최초의 연어 양식업자들"), g("farmers", "양식업자, 농부"),
                    g("realized", "깨달았다"), g("crossing and recrossing", "교배하고 재교배하는 것"),
                    g("crossing", "교배하는 것"), g("recrossing", "다시 교배하는 것"),
                    g("the specific families", "특정 계통들"), g("specific", "특정한"), g("families", "계통"),
                    g("the original forty rivers", "원래의 40개 하천"), g("original", "원래의"), g("rivers", "하천"),
                    g("would result in", "~을 낳을 것이다, 결과로 ~이 되다"), g("result", "결과"),
                    g("grew faster", "더 빨리 자랐다"), g("grew", "자랐다"), g("faster", "더 빨리")],
        "slashes": ["But whatever the manifestation of difference", "different species of salmon,", "the first salmon farmers realized",
                    "crossing and recrossing", "the specific families", "the original forty rivers", "would result in salmon"],
        "roles": [r("the first salmon farmers", "S"), r("realized", "V"),
                  r("crossing and recrossing the specific families from the original forty rivers", "S"), r("would result in", "V")],
        "modifiers": ["that occurred in different species of salmon", "that grew faster"],
        "steps": [
            choice("a_before",
                   "(A)는 'But whatever the manifestation of difference(그러나 차이가 어떤 모습이든)'로 시작해요. 앞에는 무엇이 와야 할까요?",
                   [("o0", "양식 연어가 야생 조상과 아주 달라졌다는 결과", False),
                    ("o1", "연어들 사이에 어떤 차이가 있는지 설명한 내용", True),
                    ("o2", "연어 양식이 실패한 까닭", False)],
                   "difference that occurred in different species of salmon을 봐요. 어디에서 생긴 차이인지가 단서예요.",
                   why="'difference that occurred in different species of salmon', 서로 다른 연어 종들 사이에서 나타난 차이예요. 그러니 앞에 연어들이 어떻게 다른지 말한 내용이 있어야 해요.\n또 the first salmon farmers(최초의 양식업자들)가 깨달은 일이라 양식이 막 시작될 때 이야기예요.",
                   highlight=["But whatever", "difference", "different species of salmon"],
                   tips=[tip("whatever + 명사", "'~이 무엇이든'이에요. whatever the manifestation of difference = 차이가 어떤 모습으로 나타났든.", "whatever"),
                         tip("cross", "평소엔 '건너다'로 알기 쉬워요. 여기서는 '교배시키다'예요. crossing and recrossing = 교배하고 다시 교배하는 것.", "crossing", trap=True),
                         tip("family", "평소엔 '가족'으로 알기 쉬워요. 여기서는 생물의 '계통'이에요. the specific families = 특정 계통들.", "families", trap=True)],
                   point="(A) But whatever … difference ← 앞에 연어들 사이의 차이"),
            choice("a_next",
                   "(A)는 '특정 계통을 교배하면 더 빨리 자라는 연어가 나온다'는 깨달음으로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "하천마다 다른 난관", False), ("o1", "야생 연어가 강으로 돌아오는 길", False),
                    ("o2", "그렇게 고른 연어로 새 품종을 만드는 이야기", True)],
                   "would result in salmon that grew faster를 봐요. 더 빨리 자라는 연어를 얻을 길을 찾았어요.",
                   why="양식업자들이 더 빨리 자라는 연어를 얻는 교배 방법을 깨달았어요. 다음엔 그 방법으로 연어를 길러 나가는 이야기가 이어지기 쉬워요.",
                   highlight=["result in", "grew faster"],
                   tips=[tip("result in", "'~을 낳다, 결과로 ~이 되다'예요. would result in salmon that grew faster = 더 빨리 자라는 연어를 얻게 될 것이다.", "result")],
                   point="(A) 끝 '더 빨리 자라는 연어를 얻는 교배' → 다음은 그 연어로 기르는 이야기"),
        ],
    },
    {
        "id": 3, "text": B1, "teaching_value": "high",
        "model_translation": "(B) 그리고 연어는 소나 양과 달리 일생 동안 ‘수천 마리의’ 새끼를 낳을 수 있기 때문에, 일단 유리한 개체가 발견되면 소수의 강한 수컷과 암컷만으로도 생산성이 매우 높은 완전히 새로운 품종의 물고기 기반을 형성할 수 있었다.",
        "glosses": [g("And because salmon", "그리고 연어는 ~ 때문에"), g("salmon", "연어"), g("unlike", "~와 달리"),
                    g("cattle and sheep", "소와 양"), g("cattle", "소"), g("sheep", "양"), g("can produce", "낳을 수 있다"),
                    g("produce", "낳다, 만들어 내다"), g("many thousands of offspring", "수천 마리의 새끼"), g("thousands", "수천"),
                    g("offspring", "자손, 새끼"), g("in the course of their lives", "일생 동안"), g("course", "과정, 동안"),
                    g("lives", "삶, 일생"), g("once", "일단 ~하면"), g("favorable individuals", "유리한 개체"),
                    g("favorable", "유리한"), g("individuals", "개체"), g("were found", "발견되었다"),
                    g("just a few strong males and females", "소수의 강한 수컷과 암컷만"), g("few", "적은"), g("strong", "강한"),
                    g("males", "수컷"), g("females", "암컷"), g("could form", "형성할 수 있었다"), g("form", "형성하다"),
                    g("the basis", "기반"), g("basis", "기반"), g("a whole new race", "완전히 새로운 품종"), g("whole", "완전한"),
                    g("race", "품종"), g("highly productive fish", "생산성이 매우 높은 물고기"), g("highly", "매우"),
                    g("productive", "생산성이 높은")],
        "slashes": ["And because salmon,", "cattle and sheep,", "many thousands of offspring", "of their lives,", "were found,",
                    "males and females", "could form the basis", "a whole new race"],
        "roles": [r("salmon", "S"), r("can produce", "V"), r("favorable individuals", "S"), r("were found", "V"),
                  r("just a few strong males and females", "S"), r("could form", "V"),
                  r("the basis of a whole new race of highly productive fish", "O")],
        "steps": [
            choice("b_before",
                   "(B)는 'And(그리고)'로 시작하고, 'once favorable individuals were found(일단 유리한 개체가 발견되면)'라고 해요. 앞에는 무엇이 와야 할까요?",
                   [("o0", "하천마다 필요한 연어가 다르다는 내용", False), ("o1", "소와 양이 새끼를 적게 낳는 까닭", False),
                    ("o2", "어떤 연어를 골라 기르면 좋은지 알아낸 내용", True)],
                   "favorable individuals(유리한 개체)를 봐요. 무엇에 유리한지가 앞에 나와 있어야 해요.",
                   why="And(그리고)는 앞 이야기에 덧붙이는 말이에요. once favorable individuals were found(일단 유리한 개체를 찾으면)라고 했으니, 앞에 어떤 연어를 찾으려는지가 먼저 나와야 해요.",
                   highlight=["And", "once", "favorable individuals"],
                   tips=[tip("once", "평소엔 '한 번'으로 알기 쉬워요. 여기서는 주어·동사 앞에 와서 '일단 ~하면'이에요. once favorable individuals were found = 일단 유리한 개체가 발견되면.", "once", trap=True),
                         tip("race", "평소엔 '경주'로 알기 쉬워요. 여기서는 '품종'이에요. a whole new race of … fish = 완전히 새로운 품종의 물고기.", "race", trap=True),
                         tip("unlike", "'~와 달리'예요. salmon, unlike cattle and sheep = 소나 양과 달리 연어는.", "unlike")],
                   point="(B) And … once favorable individuals ← 앞에 어떤 연어를 고를지"),
        ],
    },
    {
        "id": 4, "text": B2, "teaching_value": "high",
        "model_translation": "최초의 야생 조상들과는 상당히 다른 사육 집단이 빠르게 만들어질 수 있었다.",
        "glosses": [g("A domestic population", "사육 집단"), g("domestic", "사육되는"), g("population", "집단"),
                    g("could be created", "만들어질 수 있었다"), g("created", "만들어진"), g("quickly", "빠르게"),
                    g("quite different from", "~와 상당히 다른"), g("quite", "상당히"), g("different", "다른"),
                    g("the initial wild ancestors", "최초의 야생 조상들"), g("initial", "최초의, 초기의"), g("wild", "야생의"),
                    g("ancestors", "조상")],
        "slashes": ["A domestic population", "created quickly", "quite different"],
        "roles": [r("A domestic population", "S"), r("could be created", "V")],
        "modifiers": ["that would be quite different from the initial wild ancestors"],
        "steps": [
            choice("b_diff",
                   "(B)는 '야생 조상과 상당히 다른 사육 집단이 빠르게 만들어질 수 있었다'로 끝나요. 여기서 different(다른)는 무엇과 무엇이 다르다는 말일까요?",
                   [("o0", "새로 만든 사육 집단과 야생 조상", True), ("o1", "긴 하천의 연어와 북쪽 하천의 연어", False),
                    ("o2", "연어와 소·양", False)],
                   "A domestic population … different from the initial wild ancestors를 이어 봐요.",
                   why="that would be quite different …는 앞의 A domestic population을 꾸며요. 사육 집단이 the initial wild ancestors(최초의 야생 조상)와 다르다는 말이에요.",
                   highlight=["domestic population", "different from", "wild ancestors"],
                   tips=[tip("domestic", "평소엔 '국내의'로 알기 쉬워요. 여기서는 동물이 '사육되는'이에요. A domestic population = 사육 집단.", "domestic", trap=True),
                         tip("떨어진 that", "A domestic population … that would be quite different에서 that 덩어리는 동사 뒤로 밀려났지만 A domestic population을 꾸며요.", "that")]),
        ],
    },
    {
        "id": 5, "text": C1, "teaching_value": "high",
        "model_translation": "(C) 모든 연어 하천은 물고기가 적응해야 하는 고유한 일련의 난관이 있다.",
        "glosses": [g("Every salmon river", "모든 연어 하천은"), g("salmon", "연어"), g("river", "하천"),
                    g("its own unique set of challenges", "고유한 일련의 난관"), g("unique", "고유한"),
                    g("a set of", "일련의"), g("set", "한 벌, 묶음"), g("challenges", "난관, 어려움"),
                    g("to which fish must adapt", "물고기가 적응해야 하는"), g("adapt", "적응하다")],
        "slashes": ["Every salmon river has", "set of challenges"],
        "roles": [r("Every salmon river", "S"), r("has", "V"), r("its own unique set of challenges to which fish must adapt", "O")],
        "modifiers": ["to which fish must adapt"],
        "steps": [],
    },
    {
        "id": 6, "text": C2, "teaching_value": "medium",
        "model_translation": "Yukon강처럼 어떤 하천은 매우 길어서, 길어진 여정에서 살아남기 위해 막대한 지방 비축량을 축적할 수 있는 동물이 필요하다.",
        "glosses": [g("Some rivers", "어떤 하천은"), g("rivers", "하천"), g("very long", "매우 긴"), g("like the Yukon", "Yukon강처럼"),
                    g("Yukon", "유콘강 · 캐나다와 알래스카를 흐르는 긴 강"), g("require", "필요로 하다"), g("animals", "동물"),
                    g("build up", "축적하다, 쌓다"), g("massive fat reserves", "막대한 지방 비축량"), g("massive", "막대한"),
                    g("fat", "지방"), g("reserves", "비축량"), g("in order to survive", "살아남기 위해"), g("survive", "살아남다"),
                    g("the extended journey", "길어진 여정"), g("extended", "길어진"), g("journey", "여정")],
        "slashes": ["are very long,", "like the Yukon,", "and require animals", "massive fat reserves"],
        "roles": [r("Some rivers", "S"), r("are", "V"), r("very long", "C"), r("require", "V"),
                  r("animals that can build up massive fat reserves in order to survive the extended journey", "O")],
        "modifiers": ["that can build up massive fat reserves in order to survive the extended journey"],
        "steps": [
            show("c2_mid", "Yukon강처럼 아주 긴 하천에는 긴 여정을 버티도록 지방을 많이 쌓아 두는 연어가 필요하대요.",
                 highlight=["very long", "massive fat reserves"],
                 tips=[tip("reserve", "평소엔 '예약하다'로 알기 쉬워요. 여기서는 명사로 '비축량, 쌓아 둔 것'이에요. massive fat reserves = 막대한 지방 비축량.", "reserves", trap=True),
                       tip("build up", "'축적하다, 쌓다'예요. build up massive fat reserves = 막대한 지방 비축량을 쌓다.", "build up")]),
        ],
    },
    {
        "id": 7, "text": C3, "teaching_value": "high",
        "model_translation": "다른 하천들은 아주 멀리 북쪽에 있어 기온이 더 따뜻한 시기가 짧아서, 특히 어린 시기 동안 성장을 극대화할 수 있는 물고기가 필요하다.",
        "glosses": [g("Others", "다른 하천들은"), g("very far north", "아주 멀리 북쪽에"), g("far", "멀리"), g("north", "북쪽"),
                    g("with only a short season of warmer temperatures", "더 따뜻한 시기가 짧아서"), g("short", "짧은"),
                    g("season", "시기, 계절"), g("warmer", "더 따뜻한"), g("temperatures", "기온"), g("require", "필요로 하다"),
                    g("maximize growth", "성장을 극대화하다"), g("maximize", "극대화하다"), g("growth", "성장"),
                    g("particularly", "특히"), g("during its younger phase", "어린 시기 동안"), g("younger", "더 어린"),
                    g("phase", "시기, 단계")],
        "slashes": ["very far north,", "warmer temperatures,", "and require a fish", "maximize growth,"],
        "roles": [r("Others", "S"), r("are", "V"), r("very far north", "C"), r("require", "V"),
                  r("a fish that can maximize growth", "O")],
        "modifiers": ["that can maximize growth"],
        "steps": [
            show("c3_end", "아주 먼 북쪽 하천은 따뜻한 시기가 짧아서, 어릴 때 빨리 자라는 물고기가 필요하대요.\n하천마다 필요한 연어가 이렇게 달라요.",
                 highlight=["very far north", "maximize growth"],
                 tips=[tip("Others", "'다른 것들(다른 하천들)'이에요. 앞 문장 Some rivers와 짝을 이뤄요. Some … Others … = 어떤 것은 …, 다른 것은 ….", "Others")],
                 panel=groups("Every salmon river (하천마다 다른 난관)", "very long (아주 긴 하천)",
                              [("massive fat reserves", "막대한 지방 비축량")],
                              "very far north (아주 먼 북쪽 하천)", [("maximize growth", "성장 극대화")],
                              between="/", fresh=("maximize growth",))),
            order_link(
                card("given", "주어진 글", last=("… from fish drawn from forty different river systems.", "40개의 서로 다른 하천 수계에서 가져온 물고기로부터")),
                [card("A", "(A)", first=("But whatever the manifestation of difference that occurred in different species of salmon …", "그러나 서로 다른 연어 종들 사이의 차이가 무엇이든"),
                      last=("… would result in salmon that grew faster.", "더 빨리 자라는 연어를 얻게 될 것이다")),
                 card("B", "(B)", first=("And because salmon … once favorable individuals were found …", "그리고 연어는 … 일단 유리한 개체가 발견되면"),
                      last=("… quite different from the initial wild ancestors.", "최초의 야생 조상들과 상당히 다른")),
                 card("C", "(C)", first=("Every salmon river has its own unique set of challenges …", "모든 연어 하천은 고유한 난관이 있다"),
                      last=("… require a fish that can maximize growth …", "성장을 극대화하는 물고기가 필요하다"))],
                ["C", "A", "B"],
                "주어진 글(40개의 서로 다른 하천에서 가져온 물고기) → (C) 하천마다 난관이 달라 필요한 연어도 다르다 → (A) 그러나 차이가 무엇이든 교배하면 더 빨리 자라는 연어가 나온다 → (B) 그리고 유리한 개체만 찾으면 새 품종을 빠르게 만들 수 있었다, 순서예요."),
            show("c_go", "직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?", button="문제 풀러 갈게요"),
        ],
    },
]

add_match(sentences, 5, [m("Every salmon river", "모든 연어 하천은"), " ", m("to which fish must adapt", "물고기가 적응해야 하는"), " ",
                         m("its own unique set of challenges", "고유한 일련의 난관이"), " ", m("has", "있다"), "."])

SENSES = {
    2: [sense("but", "But whatever", "그러나", "접속사 but (앞 내용과 맞섬)"),
        sense("that", "difference that occurred", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("that", "realized that crossing", "~라는 것을", "명사절 that + 주어·동사"),
        sense("that", "salmon that grew faster", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    4: [sense("that", "that would be quite different", "(앞의 A domestic population을 꾸밈)", "관계대명사 that (꾸미는 명사와 떨어져 있음)")],
    5: [sense("to", "to which fish must adapt", "~에 (적응하다)", "adapt to ~ = ~에 적응하다 (to which = 그 난관에)"),
        sense("which", "to which", "그것(난관)", "관계대명사 which (전치사 to + which)")],
    6: [sense("that", "animals that can", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("to", "in order to survive", "~하기 위해", "in order to + 동사원형 = ~하기 위해")],
    7: [sense("that", "a fish that can", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
}

WORDS = {"initial": "초기의", "selection": "선발", "farmed": "양식된", "atlantic": "대서양의", "salmon": "연어", "took": "가졌다",
         "place": "자리", "fish": "물고기", "drawn": "가져온", "forty": "40", "different": "서로 다른", "river": "하천",
         "systems": "체계, 수계", "whatever": "무엇이든", "manifestation": "표현", "difference": "차이", "species": "종",
         "farmers": "양식업자", "crossing": "교배하는 것", "recrossing": "재교배하는 것", "specific": "특정한",
         "families": "계통", "original": "원래의", "rivers": "하천", "result": "결과", "grew": "자랐다", "faster": "더 빨리",
         "cattle": "소", "sheep": "양", "produce": "낳다", "thousands": "수천", "offspring": "자손", "course": "동안",
         "lives": "일생", "favorable": "유리한", "individuals": "개체", "found": "발견된", "strong": "강한", "males": "수컷",
         "females": "암컷", "form": "형성하다", "basis": "기반", "whole": "완전한", "race": "품종", "highly": "매우",
         "productive": "생산성이 높은", "domestic": "사육되는", "population": "집단", "created": "만들어진", "quite": "상당히",
         "wild": "야생의", "ancestors": "조상", "unique": "고유한", "set": "묶음", "challenges": "난관", "adapt": "적응하다",
         "long": "긴", "yukon": "유콘강", "build": "쌓다", "massive": "막대한", "fat": "지방", "reserves": "비축량",
         "survive": "살아남다", "extended": "길어진", "journey": "여정", "far": "멀리", "north": "북쪽", "short": "짧은",
         "season": "시기", "warmer": "더 따뜻한", "temperatures": "기온", "maximize": "극대화하다", "growth": "성장",
         "younger": "더 어린", "phase": "시기", "realized": "깨달았다", "occurred": "나타났다", "quickly": "빠르게",
         "every": "모든", "its": "그것의"}

OPTIONS = [("1", "(A)-(C)-(B)", False), ("2", "(B)-(A)-(C)", False), ("3", "(B)-(C)-(A)", False), ("4", "(C)-(A)-(B)", True), ("5", "(C)-(B)-(A)", False)]
exam = {
    "question": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은? [3점]",
    "sentence": 1, "analysis_first": True, "wrong_rate": 38.0, "wrong_rank": 8,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], **({"correct": True} if o[2] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "단락 첫머리 단서(But whatever … difference, And … once)를 떠올리며 순서를 골라 봐요.",
        "정답이에요! 40개의 서로 다른 하천 → (C) 하천마다 필요한 연어가 다르다 → (A) 그러나 차이가 무엇이든 교배하면 더 빨리 자라는 연어 → (B) 그리고 유리한 개체만 찾으면 새 품종을 빠르게, 순서예요.",
        "정답은 ④ (C)-(A)-(B)예요.",
        {"1": "(A)의 difference(차이)는 앞에 연어들이 어떻게 다른지 나와 있어야 해요. 그 차이는 (C)의 하천마다 다른 난관이에요.",
         "2": "(B)의 favorable individuals(유리한 개체)는 무엇에 유리한지 앞에 나와 있어야 해요. 주어진 글 바로 뒤에는 그런 말이 없어요.",
         "3": "(B)가 주어진 글 바로 뒤에 오면 favorable individuals가 무엇에 유리한지 알 수 없어요. (A)의 difference도 (C)의 하천별 차이를 받아요.",
         "5": "가장 많이 고른 오답이에요. (A)의 difference는 (B) 끝 '야생 조상과 다르다'가 아니라 (C)의 하천마다 다른 연어를 받아요. (B)의 And … once favorable individuals were found는 (A)의 '더 빨리 자라는 연어'에 덧붙이는 말이에요."},
        {"5": review(23,
                     "(B) 끝의 different(다른)와 (A) 첫머리의 difference(차이)가 같은 말이라 이었을 거예요. 하지만 (A)의 차이는 'difference that occurred in different species of salmon', 연어 종들 사이의 차이로 (C)의 하천마다 다른 연어예요. 또 (A)는 the first salmon farmers(최초의 양식업자들)가 깨달은 일이고, (B)의 favorable individuals(유리한 개체)는 그 깨달음 뒤에 찾은 '더 빨리 자라는 연어'예요.",
                     panel=rows(("(C)", "Every salmon river has its own unique set of challenges …", "하천마다 다른 연어", "hl"),
                                ("(A) 첫머리", "But whatever the manifestation of difference …", "그 차이가 무엇이든", "hl"),
                                ("(B) 끝", "… quite different from the initial wild ancestors", "사육 집단 ≠ 야생 조상 (다른 차이)", "hl2")),
                     rank_word="가장 많이 고른")}),
}

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 37번 (글의 순서, 3점)",
    topic="순서 푸는 법: 주어진 글의 끝 → 단락 첫머리 단서로 앞 내용 예측 → 단락 끝으로 다음 내용 예측 → 순서 잇기",
    method={"type": "order", "labels": ["단락 요지 잡기", "연결 단서 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-farmed-salmon.svg", ("Wild salmon", "야생 연어"), "→", ("Farmed salmon", "양식 연어"),
                                       "양식 연어는 처음에 어떻게 만들어졌을까?", "2026년 9월 모의평가 37번 도입 칠판"),
                      "alt": "칠판: Wild salmon(야생 연어) → Farmed salmon(양식 연어)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "양식장에서 기르는 연어도 처음엔 강에서 데려온 야생 연어였어요. 이번 글은 양식 연어를 처음 어떻게 골라 길렀는지 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "순서 문제는 단락 첫머리의 단서가 앞 내용과 이어지는지 보는 거예요. But, And 같은 말이 무엇을 받는지 찾아볼게요."}}],
    exam=exam,
    key_words={"passage": [g("initial", "초기의"), g("selection", "선발"), g("farmed", "양식된"), g("take place", "이루어지다"),
                           g("river system", "수계"), g("whatever", "무엇이든"), g("species", "종"), g("cross", "교배시키다"),
                           g("specific", "특정한"), g("family", "계통"), g("result in", "~을 낳다"), g("unlike", "~와 달리"),
                           g("cattle", "소"), g("once", "일단 ~하면"), g("favorable", "유리한"), g("individual", "개체"),
                           g("basis", "기반"), g("race", "품종"), g("productive", "생산성이 높은"), g("domestic", "사육되는"),
                           g("population", "집단"), g("ancestor", "조상"), g("unique", "고유한"), g("a set of", "일련의"),
                           g("challenge", "난관"), g("adapt to", "~에 적응하다"), g("require", "필요로 하다"),
                           g("build up", "축적하다"), g("massive", "막대한"), g("reserve", "비축량"), g("extended", "길어진"),
                           g("maximize", "극대화하다"), g("particularly", "특히"), g("phase", "시기")],
               "options": []},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="순서 푸는 법")
