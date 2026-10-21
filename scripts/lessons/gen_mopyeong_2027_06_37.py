"""2026년 6월 모의평가(2027학년도, 평가원) 37번 레슨 + 대사를 만든다 (글의 순서, 3점). 오답률 68% · Top 3 (메가스터디 풀서비스 채점 기준).

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_37.py   (→ npm run policy:copy stamp <id> → npx vitest run src/tutor/policy)

틀: docs/tutor/templates/order.md — 주어진 글의 끝 → 단락 첫머리(앞에 무엇?) → 단락 끝(다음에 무엇?) → 순서 잇기.
정답 ④ (C)-(A)-(B). 많이 고른 오답 ② (B)-(A)-(C) 30% · ③ (B)-(C)-(A) 19% — 둘 다 (B) Spectacle must also be spectacular를
주어진 글 바로 뒤에 놓았다. also를 '하나 더'로만 보고 주어진 글(문화의 틀)에 붙였다. 그러나 must also는 '~해야 한다'는 조건을
하나 더 붙이는 말이라, 앞에 조건 — (A) 끝 'imitation is not enough(모방만으로는 부족하다)' — 이 있어야 한다.
(C) In saying that의 that은 주어진 글의 '문화의 틀' 이야기를 받고, (C) 끝 문학 비유(규칙 + 독창성)를 (A) By extension이 넓힌다.
해설지 해석·Words and Phrases와 대조함 (content/tutor/exam-source/2027-06-평가원/해설.txt) — spectacle '구경거리', be subject to '~에 영향을 받는다',
bring to bear '적용하다', by extension '더 나아가', grain '결', established '기존의', in saying that '그렇게 말함에 있어', address '해결하다',
bound '얽매인', spectacular '장관인', outdo '능가하다', if it is to become '~이 되려면'.
prevailing, deploy는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다(뜻만 둠).
반영한 규칙: 2026-10-20 끊어읽기(slashes·roles·modifiers), S·V 찾기 없음, 핵심어 나열형 해석 없음, 2026-10-21 제출·보기 해설까지.

선생님이 확인할 점 (Claude 초안, 2026-10-21):
- (B) b_before 「must also → 앞에도 '~해야 한다'는 조건」: (A) 끝은 must가 아니라 'imitation is not enough(모방만으론 부족)'라서
  「조건」이라고 묶었다. 이 설명이 학생에게 충분히 납득되는지 확인 부탁드려요 (② 30%의 핵심)
- 주어진 글 g_next 「문화의 틀 이야기를 더 풀어 주는 내용」 — o1 「구경거리가 갖춰야 할 조건」을 오답으로 둔 근거가 (C) In saying that만큼
  단단하지 않다. 억지면 g_next를 빼고 (C) c_before만 남겨도 된다
- 칠판 「구경거리를 만드는 두 가지」: old(기존) — the established · rules and traditions / new(새로움) — the innovative · outdoing previous efforts ·
  sufficient originality. (A)·(B)·(C) 어느 단락에서 읽어도 같은 칸에 쌓이는 말이라 순서를 알려 주지는 않는다고 봤다
- 헷갈리는 단어(trap): spectacle(안경 ✕ → 구경거리), grain(곡물 ✕ → 결), address(주소 ✕ → 해결하다), works(일하다 ✕ → 작품, (C) 둘째 문장)
- (C) 첫 문장 commonly는 해설지에서 '흔히'에 작은따옴표 — 원문 기울임 글씨로 보인다. 텍스트에는 표시하지 않았다
- 해석 맞추기(add_match): (A) 첫 문장 하나
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, tip, groups, rows, sense, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from order_tools import card, order_link  # noqa: E402
from beginner import add_match, m  # noqa: E402

ID = "mopyeong-2027-06-37-spectacle-culture"

G = ("Although there may be elements that trigger instinctive response, spectacle works primarily within a cultural frame and "
     "is subject to prevailing modes of perception that observers bring to bear.")
A1 = ("(A) By extension, spectacle is produced by working with the grain of a particular culture, blending the innovative with "
      "the established.")
A2 = ("Thus anyone deploying spectacle may draw on a repertoire of techniques and conventions developed from previous festivals "
      "or related activities, but imitation is not enough.")
B1 = "(B) Spectacle must also be spectacular."
B2 = ("A spectacle has to amaze spectators, outdoing previous efforts if it is to become part of the collective memory of those "
      "who witnessed and participated in it.")
C1 = ("(C) In saying that, we stress that creation of spectacle is neither a universal nor even an inevitable expression of "
      "culture, but is a strategy commonly used by people from many different cultures to address specific needs.")
C2 = ("The task of creating spectacle has been likened to creating new works of literature, where writers normally feel bound by "
      "the rules and traditions of their genre yet need to show sufficient originality to impress their audiences.")

OLD = "old (기존)"
NEW = "new (새로움)"


def board(left, right, fresh=()):
    return groups("구경거리를 만드는 두 가지", OLD, left, NEW, right, fresh=fresh, between="+")


L_A = [("the established", "기존의 것")]
R_A = [("the innovative", "혁신적인 것")]

sentences = [
    {
        "id": 1, "label": "주어진 글", "text": G, "teaching_value": "high",
        "model_translation": "비록 본능적인 반응을 유발하는 요소들이 있을 수 있지만, 구경거리는 주로 문화적인 틀 안에서 작용하며 관찰자들이 적용하는 주요한 지각 방식에 영향을 받는다.",
        "glosses": [g("Although there may be elements", "~하는 요소들이 있을 수 있지만"), g("elements", "요소"),
                    g("trigger", "유발하다"), g("instinctive response", "본능적인 반응"), g("instinctive", "본능적인"),
                    g("response", "반응"), g("spectacle", "구경거리, 볼거리"), g("works", "작용하다"), g("primarily", "주로"),
                    g("within a cultural frame", "문화적인 틀 안에서"), g("cultural", "문화적인"), g("frame", "틀"),
                    g("is subject to", "~에 영향을 받는다"), g("prevailing modes of perception", "주요한 지각 방식"),
                    g("prevailing", "주요한, 지배적인"), g("modes", "방식"), g("perception", "지각, 인식"),
                    g("observers", "관찰자"), g("bring to bear", "적용하다")],
        "slashes": ["Although there may be elements", "instinctive response,", "spectacle works primarily", "a cultural frame",
                    "is subject to", "modes of perception"],
        "roles": [r("may be", "V"), r("elements", "S"), r("spectacle", "S"), r("works", "V"), r("is", "V"),
                  r("subject to prevailing modes of perception that observers bring to bear", "C")],
        "modifiers": ["that trigger instinctive response", "that observers bring to bear"],
        "steps": [
            choice("g_main",
                   "Although(비록 ~이지만)는 한발 물러서는 말이에요. 글쓴이가 정말 하고 싶은 말은 무엇일까요?",
                   [("o0", "구경거리는 본능적인 반응에서 나온다", False), ("o1", "구경거리는 주로 문화의 틀 안에서 작용한다", True),
                    ("o2", "관찰자는 구경거리에 관심이 없다", False)],
                   "콤마(,) 뒤 메인 문장 spectacle works primarily within …을 봐요.",
                   why="Although 덩어리는 '본능적 반응을 일으키는 요소도 있을 수 있지만'이라고 물러서는 말이에요. 콤마(,) 뒤 'works primarily within a cultural frame'이 글쓴이의 말이에요.",
                   highlight=["spectacle", "cultural frame"],
                   tips=[tip("spectacle", "평소 spectacles(안경)로 알던 학생이 많아요. 여기서는 '구경거리, 볼거리'예요.", "spectacle", trap=True),
                         tip("be subject to", "'~에 영향을 받다'예요. is subject to prevailing modes of perception = 주요한 지각 방식에 영향을 받는다.", "subject"),
                         tip("bring to bear", "'적용하다'예요. modes of perception that observers bring to bear = 관찰자들이 적용하는 지각 방식.", "bring")]),
            choice("g_next",
                   "주어진 글은 '구경거리는 문화의 틀 안에서 작용하고 관찰자의 지각 방식에 영향을 받는다'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "구경거리와 문화의 관계를 더 풀어 말하는 내용", True), ("o1", "구경거리가 갖춰야 할 조건", False),
                    ("o2", "본능적인 반응의 예", False)],
                   "주어진 글의 중심은 a cultural frame(문화의 틀)이에요.",
                   why="주어진 글은 구경거리가 문화의 틀 안에서 작용한다는 주장이에요. 이 주장을 이어 받아 더 풀어 주는 내용이 오기 쉬워요.",
                   highlight=["cultural frame"],
                   point="주어진 글 끝 '문화의 틀 안에서 작용' → 다음은 그 주장을 더 풀어 주는 내용"),
            show("paper_order", "이제 (A)·(B)·(C)를 시험지 순서대로 읽어요. 단락마다 첫머리와 끝을 잘 봐 두면 좋아요.",
                 button="(A)부터 읽어 볼게요"),
        ],
    },
    {
        "id": 2, "text": A1, "teaching_value": "high",
        "model_translation": "(A) 더 나아가, 구경거리는 특정 문화의 결에 맞추어 작업함으로써, 즉 혁신적인 요소와 기존의 요소를 혼합함으로써 만들어진다.",
        "glosses": [g("By extension", "더 나아가"), g("extension", "확장"), g("spectacle", "구경거리"), g("is produced", "만들어진다"),
                    g("produced", "만들어진"), g("by working with", "~에 맞추어 작업함으로써"), g("working", "작업하는 것"),
                    g("grain", "결 · 나뭇결처럼 타고난 방향"), g("particular", "특정한"), g("culture", "문화"),
                    g("blending", "혼합하는"), g("the innovative", "혁신적인 것"), g("innovative", "혁신적인"),
                    g("the established", "기존의 것"), g("established", "기존의, 확립된")],
        "slashes": ["By extension,", "spectacle is produced", "by working", "a particular culture,"],
        "roles": [r("spectacle", "S"), r("is produced", "V")],
        "steps": [
            choice("a_before",
                   "(A)는 'By extension(더 나아가), 구경거리는 새것과 기존의 것을 섞어 만들어진다'로 시작해요. 앞에는 무엇이 와야 할까요?",
                   [("o0", "구경거리는 관객을 놀라게 해야 한다는 조건", False), ("o1", "본능적인 반응을 일으키는 요소의 예", False),
                    ("o2", "규칙을 따르면서도 새로움을 보여야 하는 비슷한 예", True)],
                   "By extension은 '같은 원리를 넓혀서'예요. blending the innovative with the established와 같은 원리가 앞에 있어야 해요.",
                   why="By extension(더 나아가)은 앞에서 말한 원리를 구경거리로 넓힐 때 써요. 그러니 앞에도 '기존의 것 + 새것'과 같은 원리가 먼저 나와야 해요.",
                   highlight=["By extension", "the innovative", "the established"],
                   tips=[tip("by extension", "'더 나아가, 같은 원리를 넓혀서'예요. 앞의 이야기를 다른 것에 넓혀 적용할 때 써요.", "By extension"),
                         tip("grain", "평소엔 '곡물, 낟알'로 알기 쉬워요. 여기서는 나뭇결처럼 '결'이에요. work with the grain = 결에 맞춰 작업하다.", "grain", trap=True),
                         tip("the + 형용사", "'~한 것'이에요. the innovative = 혁신적인 것, the established = 기존의 것.", "innovative"),
                         tip("blend A with B", "'A를 B와 섞다'예요. blending the innovative with the established = 혁신적인 것과 기존의 것을 섞으면서.", "blending")],
                   panel=board(L_A, R_A, fresh=("the established", "the innovative")),
                   point="(A) By extension ← 앞에 '기존 + 새로움'과 같은 원리(비슷한 예)"),
        ],
    },
    {
        "id": 3, "text": A2, "teaching_value": "high",
        "model_translation": "따라서 구경거리를 전개하는 누구든 이전의 축제나 관련 활동들로부터 발전된 기법과 관습의 레퍼토리를 활용할 수 있지만, 모방만으로는 충분하지 않다.",
        "glosses": [g("Thus", "따라서"), g("anyone deploying spectacle", "구경거리를 전개하는 누구든"), g("anyone", "누구든"),
                    g("deploying", "전개하는"), g("may draw on", "~을 활용할 수 있다"), g("draw on", "활용하다, 끌어 쓰다"),
                    g("repertoire", "레퍼토리, (쓸 수 있는) 목록"), g("techniques and conventions", "기법과 관습"),
                    g("techniques", "기법"), g("conventions", "관습"), g("developed", "발전된"),
                    g("previous festivals", "이전의 축제"), g("previous", "이전의"), g("festivals", "축제"),
                    g("related activities", "관련 활동"), g("related", "관련된"), g("activities", "활동"),
                    g("imitation", "모방"), g("is not enough", "충분하지 않다"), g("enough", "충분한")],
        "slashes": ["deploying spectacle", "a repertoire", "techniques and conventions", "related activities,"],
        "roles": [r("anyone deploying spectacle", "S"), r("may draw on", "V"),
                  r("a repertoire of techniques and conventions developed from previous festivals or related activities", "O"),
                  r("imitation", "S"), r("is", "V"), r("not enough", "C")],
        "modifiers": ["deploying spectacle", "developed from previous festivals or related activities"],
        "steps": [
            choice("a_next",
                   "(A)는 'but imitation is not enough(하지만 모방만으로는 충분하지 않다)'로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "모방 말고 더 갖춰야 할 것", True), ("o1", "이전 축제를 모방하는 방법", False),
                    ("o2", "구경거리가 어느 문화에나 있다는 내용", False)],
                   "not enough(충분하지 않다)라고 했어요. 그럼 무엇이 더 필요한지가 궁금해지죠.",
                   why="모방만으로는 부족하다고 했으니, 다음엔 그 밖에 무엇이 더 필요한지가 이어지기 쉬워요.",
                   highlight=["imitation", "not enough"],
                   tips=[tip("draw on", "'~을 활용하다, 끌어 쓰다'예요. draw on a repertoire = 레퍼토리를 활용하다.", "draw"),
                         tip("repertoire", "'(쓸 수 있는) 목록, 레퍼토리'예요. 이전 축제에서 발전된 기법과 관습을 모아 둔 것이에요.", "repertoire")],
                   point="(A) 끝 '모방만으로는 충분하지 않다' → 다음은 더 필요한 것"),
        ],
    },
    {
        "id": 4, "text": B1, "teaching_value": "high",
        "model_translation": "(B) 구경거리는 또한 장관이어야 한다.",
        "glosses": [g("Spectacle", "구경거리는"), g("must also be", "또한 ~이어야 한다"), g("spectacular", "장관인, 볼 만한")],
        "slashes": [],
        "roles": [r("Spectacle", "S"), r("must … be", "V"), r("spectacular", "C")],
        "steps": [
            choice("b_before",
                   "(B)는 'Spectacle must also be spectacular(구경거리는 또한 장관이어야 한다)'로 시작해요. also(또한)를 보면 앞에는 무엇이 와야 할까요?",
                   [("o0", "구경거리가 문화의 틀 안에서 작용한다는 설명", False), ("o1", "구경거리가 갖춰야 할 또 다른 조건", True),
                    ("o2", "문학 작품을 쓰는 방법", False)],
                   "must(~해야 한다)와 also(또한)를 같이 봐요. '~해야 한다'를 하나 더 붙이는 말이에요.",
                   why="must also는 '~해야 한다'는 조건을 하나 더 붙이는 말이에요. 그러니 앞에도 구경거리가 무엇을 해야 하는지가 먼저 있어야 해요. 문화의 틀 이야기는 어떻게 작용하는지 설명이지 조건이 아니에요.",
                   highlight=["must also be"],
                   tips=[tip("spectacular", "'장관인, 볼 만한'이에요. spectacle(구경거리)의 형용사예요.", "spectacular")],
                   point="(B) must also ← 앞에 구경거리가 '~해야 한다'는 다른 조건"),
        ],
    },
    {
        "id": 5, "text": B2, "teaching_value": "high",
        "model_translation": "구경거리가 그것을 목격하고 참여한 사람들의 집단 기억의 일부가 되려면, 관객을 놀라게 하고 이전의 시도들을 능가해야만 한다.",
        "glosses": [g("A spectacle", "구경거리는"), g("has to amaze", "놀라게 해야 한다"), g("amaze", "놀라게 하다"),
                    g("spectators", "관객"), g("outdoing previous efforts", "이전의 시도들을 능가하며"), g("outdoing", "능가하는"),
                    g("previous", "이전의"), g("efforts", "시도, 노력"), g("if it is to become", "~이 되려면"),
                    g("part of the collective memory", "집단 기억의 일부"), g("collective memory", "집단 기억"),
                    g("collective", "집단의"), g("those who witnessed and participated in it", "그것을 목격하고 참여한 사람들"),
                    g("witnessed", "목격했다"), g("participated in", "~에 참여했다")],
        "slashes": ["has to amaze spectators,", "previous efforts", "if it is to become part", "the collective memory"],
        "roles": [r("A spectacle", "S"), r("has to amaze", "V"), r("spectators", "O"), r("it", "S"), r("is to become", "V"),
                  r("part of the collective memory", "C")],
        "modifiers": ["who witnessed and participated in it"],
        "steps": [
            choice("b_amaze",
                   "구경거리가 사람들의 집단 기억에 남으려면 어떻게 해야 한대요?",
                   [("o0", "이전 축제를 그대로 따라 해야 한다", False), ("o1", "관객이 직접 만들어야 한다", False),
                    ("o2", "관객을 놀라게 하고 이전 시도를 넘어서야 한다", True)],
                   "has to amaze spectators, outdoing previous efforts를 봐요. outdo는 '능가하다'예요.",
                   why="'has to amaze spectators, outdoing previous efforts', 관객을 놀라게 하고 이전의 시도들을 능가해야 한대요. if it is to become …는 '~이 되려면'이에요.",
                   highlight=["amaze", "outdoing previous efforts"],
                   tips=[tip("if + be to ~", "if 안의 be to ~는 '~하려면'이에요. if it is to become part of … = …의 일부가 되려면.", "is to become"),
                         tip("outdo", "'능가하다, 넘어서다'예요. outdoing previous efforts = 이전의 시도들을 능가하면서.", "outdoing")],
                   panel=board(L_A, R_A + [("outdoing previous efforts", "이전 시도를 능가함")], fresh=("outdoing previous efforts",))),
        ],
    },
    {
        "id": 6, "text": C1, "teaching_value": "high",
        "model_translation": "(C) 그렇게 말함에 있어, 우리는 구경거리의 창조가 문화의 보편적이거나 심지어 필연적인 표현이 아니라, 오히려 특정한 요구를 해결하기 위해 여러 다양한 문화권의 사람들이 '흔히' 사용하는 전략임을 강조한다.",
        "glosses": [g("In saying that", "그렇게 말함에 있어, 그렇게 말하면서"), g("saying", "말하는 것"), g("we stress", "우리는 강조한다"),
                    g("stress", "강조하다"), g("creation of spectacle", "구경거리의 창조"), g("creation", "창조"),
                    g("neither", "~도 아니다 (neither A nor B)"), g("universal", "보편적인"), g("inevitable", "필연적인"),
                    g("expression of culture", "문화의 표현"), g("expression", "표현"), g("culture", "문화"),
                    g("a strategy", "전략"), g("strategy", "전략"), g("commonly used", "흔히 사용되는"), g("commonly", "흔히"),
                    g("many different cultures", "여러 다양한 문화(권)"), g("cultures", "문화(권)"),
                    g("to address specific needs", "특정한 요구를 해결하기 위해"), g("address", "해결하다, 다루다"),
                    g("specific needs", "특정한 요구"), g("specific", "특정한"), g("needs", "요구")],
        "slashes": ["In saying that,", "we stress", "creation of spectacle", "expression of culture,", "but is a strategy", "by people",
                    "many different cultures"],
        "roles": [r("we", "S"), r("stress", "V"), r("creation of spectacle", "S"), r("is … is", "V"),
                  r("neither a universal nor even an inevitable expression of culture", "C"),
                  r("a strategy commonly used by people from many different cultures to address specific needs", "C")],
        "modifiers": ["commonly used by people from many different cultures to address specific needs"],
        "steps": [
            choice("c_before",
                   "(C)는 'In saying that(그렇게 말하면서)'으로 시작해요. 앞에는 어떤 말이 와야 할까요?",
                   [("o0", "구경거리는 관객을 놀라게 해야 한다는 내용", False), ("o1", "구경거리와 문화의 관계를 말한 내용", True),
                    ("o2", "모방만으로는 충분하지 않다는 내용", False)],
                   "(C)가 that을 받아 무엇에 대해 덧붙이는지 봐요. expression of culture(문화의 표현)가 나와요.",
                   why="(C)는 that을 받아 '구경거리의 창조는 문화의 보편적 표현이 아니라 여러 문화가 쓰는 전략'이라고 덧붙여요. 그러니 that은 구경거리와 문화를 이어 말한 내용이어야 해요.",
                   highlight=["In saying that", "expression of culture"],
                   tips=[tip("neither A nor B", "'A도 B도 아닌'이에요. neither a universal nor even an inevitable expression = 보편적인 표현도, 심지어 필연적인 표현도 아닌.", "neither"),
                         tip("address", "평소엔 '주소'로 알기 쉬워요. 여기서는 '(문제를) 해결하다, 다루다'예요.", "address", trap=True)],
                   point="(C) In saying that ← 앞에 구경거리와 문화를 이어 말한 내용"),
        ],
    },
    {
        "id": 7, "text": C2, "teaching_value": "high",
        "model_translation": "구경거리를 창조하는 과업은 새로운 문학 작품을 창작하는 것에 비유되어 왔는데, 문학에서 작가들은 보통 자신들 장르의 규칙과 전통에 얽매인다고 느끼면서도 독자들에게 깊은 인상을 주기 위해 충분한 독창성을 보여야 한다.",
        "glosses": [g("The task of creating spectacle", "구경거리를 창조하는 과업"), g("task", "과업, 일"), g("creating", "창조하는 것"),
                    g("has been likened to", "~에 비유되어 왔다"), g("likened", "비유된"),
                    g("new works of literature", "새로운 문학 작품"), g("works", "작품"), g("literature", "문학"),
                    g("writers", "작가들"), g("normally", "보통"), g("feel bound", "얽매인다고 느끼다"), g("bound", "얽매인"),
                    g("rules and traditions", "규칙과 전통"), g("traditions", "전통"), g("genre", "장르"),
                    g("sufficient originality", "충분한 독창성"), g("sufficient", "충분한"), g("originality", "독창성"),
                    g("to impress their audiences", "독자들에게 깊은 인상을 주기 위해"), g("impress", "깊은 인상을 주다"),
                    g("audiences", "독자, 청중")],
        "slashes": ["The task of creating spectacle", "has been likened", "works of literature,", "feel bound", "of their genre",
                    "sufficient originality"],
        "roles": [r("The task of creating spectacle", "S"), r("has been likened", "V")],
        "modifiers": ["where writers normally feel bound by the rules and traditions of their genre yet need to show sufficient originality "
                      "to impress their audiences"],
        "steps": [
            choice("c_next",
                   "(C)는 '작가는 장르의 규칙에 얽매이면서도 충분한 독창성을 보여야 한다'는 비유로 끝나요. 다음엔 어떤 내용이 오기 쉬울까요?",
                   [("o0", "문학 장르의 규칙을 하나씩 소개하는 내용", False), ("o1", "그 원리를 구경거리에 넓혀 적용하는 내용", True),
                    ("o2", "구경거리가 본능적인 반응에서 나온다는 내용", False)],
                   "The task of creating spectacle has been likened to …, 구경거리 만들기를 문학 창작에 비유했어요.",
                   why="구경거리 만들기를 문학 창작에 비유했으니, 다음엔 그 원리(규칙 + 독창성)를 다시 구경거리에 적용하는 말이 오기 쉬워요.",
                   highlight=["rules and traditions", "yet", "sufficient originality"],
                   tips=[tip("liken A to B", "'A를 B에 비유하다'예요. has been likened to creating new works of literature = 새 문학 작품을 쓰는 것에 비유되어 왔다.", "likened"),
                         tip("works", "평소엔 '일하다'로 알기 쉬워요. 여기서는 '작품'이에요. new works of literature = 새로운 문학 작품.", "works", trap=True),
                         tip("yet", "여기서는 '그런데도, 하지만'이에요. 규칙에 얽매이면서도 독창성을 보여야 한다는 말이에요.", "yet")],
                   panel=board(L_A + [("rules and traditions", "규칙과 전통")],
                               R_A + [("outdoing previous efforts", "이전 시도를 능가함"), ("sufficient originality", "충분한 독창성")],
                               fresh=("rules and traditions", "sufficient originality")),
                   point="(C) 끝 문학 비유(규칙 + 독창성) → 다음은 그 원리를 구경거리에 넓힘"),
            order_link(
                card("given", "주어진 글", last=("… spectacle works primarily within a cultural frame …", "구경거리는 주로 문화의 틀 안에서 작용한다")),
                [card("A", "(A)", first=("By extension, spectacle is produced by working with the grain of a particular culture …", "더 나아가, 구경거리는 특정 문화의 결에 맞춰 만들어진다"),
                      last=("… but imitation is not enough.", "하지만 모방만으로는 충분하지 않다")),
                 card("B", "(B)", first=("Spectacle must also be spectacular.", "구경거리는 또한 장관이어야 한다"),
                      last=("… outdoing previous efforts if it is to become part of the collective memory …", "집단 기억에 남으려면 이전 시도를 능가해야 한다")),
                 card("C", "(C)", first=("In saying that, we stress that creation of spectacle is neither a universal nor … expression of culture …", "그렇게 말하며, 구경거리의 창조는 문화의 보편적 표현이 아니라고 강조한다"),
                      last=("… writers … feel bound by the rules … yet need to show sufficient originality …", "작가는 규칙에 얽매이면서도 독창성을 보여야 한다"))],
                ["C", "A", "B"],
                "주어진 글(구경거리는 문화의 틀 안에서 작용) → (C) 그렇게 말하며, 문화의 보편적 표현이 아니라 전략이고 문학 창작에 비유된다 → (A) 더 나아가 기존의 것과 새것을 섞어 만들고, 모방만으론 부족하다 → (B) 또한 장관이어야 한다, 순서예요."),
            show("c_go", "직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?", button="문제 풀러 갈게요"),
        ],
    },
]

add_match(sentences, 2, [m("By extension", "더 나아가"), ", ", m("spectacle", "구경거리는"), " ",
                         m("the grain of a particular culture", "특정 문화의 결에"), " 맞추어 작업함으로써, 즉 ",
                         m("the innovative", "혁신적인 요소와"), " ", m("the established", "기존의 요소를"), " 혼합함으로써 ",
                         m("is produced", "만들어진다"), "."])

SENSES = {
    1: [sense("that", "elements that trigger", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("to", "is subject to", "~에 (영향을 받는)", "be subject to ~ = ~에 영향을 받다"),
        sense("that", "perception that observers", "(앞 명사를 꾸밈)", "관계대명사 that + 주어·동사 (목적어 빠짐)"),
        sense("to", "bring to bear", "(숙어의 일부)", "bring to bear = 적용하다")],
    3: [sense("but", "but imitation is", "하지만", "접속사 but (두 문장을 이음)")],
    5: [sense("to", "has to amaze", "~해야 (한다)", "have to + 동사원형 = ~해야 한다"),
        sense("if", "if it is to become", "~한다면 (~하려면)", "조건 if + 주어·동사"),
        sense("to", "is to become", "~하려면", "if 안의 be to + 동사원형 = ~하려면")],
    6: [sense("that", "In saying that", "그것 (앞에서 한 말)", "지시대명사 that"),
        sense("that", "stress that creation", "~라는 것을", "명사절 that + 주어·동사"),
        sense("but", "but is a strategy", "(A가 아니라) 오히려", "neither A nor B, but C = A도 B도 아니라 C"),
        sense("to", "to address specific needs", "~하기 위해", "to부정사 (목적)")],
    7: [sense("to", "likened to creating", "~에 (비유하다)", "liken A to B = A를 B에 비유하다"),
        sense("yet", "yet need to show", "그런데도, 하지만", "접속사 yet"),
        sense("to", "need to show", "~하는 것 (필요하다)", "need to + 동사원형 = ~해야 한다"),
        sense("to", "to impress their audiences", "~하기 위해", "to부정사 (목적)")],
}

WORDS = {"although": "비록 ~이지만", "elements": "요소", "trigger": "유발하다", "instinctive": "본능적인", "response": "반응",
         "spectacle": "구경거리", "works": "작용하다", "primarily": "주로", "cultural": "문화적인", "frame": "틀",
         "subject": "영향을 받는", "prevailing": "주요한", "modes": "방식", "perception": "지각", "observers": "관찰자",
         "bring": "가져오다", "bear": "작용하다 (bring to bear)", "extension": "확장", "produced": "만들어진",
         "working": "작업하는 것", "grain": "결", "particular": "특정한", "culture": "문화", "blending": "혼합하는",
         "innovative": "혁신적인", "established": "기존의", "thus": "따라서", "anyone": "누구든", "deploying": "전개하는",
         "draw": "끌어 쓰다", "repertoire": "레퍼토리", "techniques": "기법", "conventions": "관습", "developed": "발전된",
         "previous": "이전의", "festivals": "축제", "related": "관련된", "activities": "활동", "imitation": "모방",
         "enough": "충분한", "spectacular": "장관인", "amaze": "놀라게 하다", "spectators": "관객", "outdoing": "능가하는",
         "efforts": "시도", "become": "~이 되다", "part": "일부", "collective": "집단의", "memory": "기억",
         "witnessed": "목격했다", "participated": "참여했다", "saying": "말하는 것", "stress": "강조하다", "creation": "창조",
         "universal": "보편적인", "inevitable": "필연적인", "expression": "표현", "strategy": "전략", "commonly": "흔히",
         "used": "사용되는", "different": "다른, 다양한", "cultures": "문화(권)", "address": "해결하다", "specific": "특정한",
         "needs": "요구", "task": "과업", "creating": "창조하는 것", "likened": "비유된", "literature": "문학",
         "writers": "작가들", "normally": "보통", "bound": "얽매인", "rules": "규칙", "traditions": "전통", "genre": "장르",
         "show": "보여 주다", "sufficient": "충분한", "originality": "독창성", "impress": "깊은 인상을 주다",
         "audiences": "독자, 청중", "must": "~해야 한다", "be": "~이다", "has": "가지다",
         "spectacles": "구경거리들"}

OPTIONS = [("1", "(A)-(C)-(B)", False), ("2", "(B)-(A)-(C)", False), ("3", "(B)-(C)-(A)", False), ("4", "(C)-(A)-(B)", True), ("5", "(C)-(B)-(A)", False)]
exam = {
    "question": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은? [3점]",
    "sentence": 1, "analysis_first": True, "wrong_rate": 68.0, "wrong_rank": 3,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [],
    "options": [{"id": o[0], "label": o[1], "keywords": [], **({"correct": True} if o[2] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "단락 첫머리 단서(In saying that, By extension, must also)를 떠올리며 순서를 골라 봐요.",
        "정답이에요! 문화의 틀 → (C) 그렇게 말하며, 문화의 표현이 아니라 전략이고 문학에 비유된다 → (A) 더 나아가 기존의 것 + 새것, 모방만으론 부족 → (B) 또한 장관이어야 한다, 순서예요.",
        "정답은 ④ (C)-(A)-(B)예요.",
        {"1": "(A)의 By extension(더 나아가)은 앞의 원리를 넓히는 말이에요. 주어진 글 바로 뒤에는 넓힐 원리(문학 비유)가 아직 없어요.",
         "2": "가장 많이 고른 오답이에요. (B)의 must also(또한 ~해야 한다)는 앞에 구경거리가 해야 할 조건이 있어야 해요. 그 조건은 (A) 끝 '모방만으로는 부족하다'예요.",
         "3": "많이 고른 오답이에요. (B)가 주어진 글 바로 뒤에 오면 must also가 받을 조건이 없어요. (C)의 In saying that도 문화의 틀 이야기를 받아요.",
         "5": "(B)의 must also는 (A) 끝 '모방만으로는 부족하다'를 받아요. (A)의 By extension은 (C)의 문학 비유를 넓히는 말이에요."},
        {"2": review(30,
                     "(B)의 also(또한)를 보고 주어진 글에 하나를 더 붙이는 말로 읽었을 거예요. 하지만 must also는 '~해야 한다'는 조건을 하나 더 붙이는 말이고, 주어진 글은 조건이 아니라 구경거리가 어떻게 작용하는지 설명이에요. 앞의 조건은 (A) 끝 'imitation is not enough(모방만으로는 부족하다)'이고, (B)의 outdoing previous efforts도 (A)의 previous festivals와 이어져요.",
                     panel=rows(("주어진 글", "spectacle works primarily within a cultural frame", "어떻게 작용하는지 (조건 아님)", "hl"),
                                ("(A) 끝", "… but imitation is not enough", "모방만으론 부족 → 무엇이 더?", "hl2"),
                                ("(B)", "Spectacle must also be spectacular … outdoing previous efforts", "또한 장관이어야, 이전 시도를 능가", "hl2")),
                     rank_word="가장 많이 고른"),
         "3": review(19,
                     "(B)를 주어진 글 바로 뒤에 놓고, (C)의 In saying that이 (B)를 받는다고 본 거예요. 하지만 (C)는 that을 받아 '구경거리의 창조는 문화의 보편적 표현이 아니다'라고 덧붙여요. 그러니 that은 '장관이어야 한다'가 아니라 주어진 글의 '문화의 틀' 이야기예요.",
                     panel=rows(("주어진 글", "… works primarily within a cultural frame", "문화의 틀", "hl"),
                                ("(C)", "In saying that, … neither a universal nor … expression of culture", "그 말(문화 이야기)을 받음", "hl2")))}),
}

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 37번 (글의 순서, 3점)",
    topic="순서 푸는 법: 주어진 글의 끝 → 단락 첫머리 단서로 앞 내용 예측 → 단락 끝으로 다음 내용 예측 → 순서 잇기",
    method={"type": "order", "labels": ["단락 요지 잡기", "연결 단서 찾기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-spectacle-culture.svg", ("Spectacle", "구경거리"), "+", ("Culture", "문화"),
                                       "축제의 볼거리는 어떻게 만들어질까?", "2026년 6월 모의평가 37번 도입 칠판"),
                      "alt": "칠판: Spectacle(구경거리) + Culture(문화)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "축제의 퍼레이드나 불꽃놀이 같은 볼거리를 spectacle(구경거리)이라고 해요. 이번 글은 구경거리와 문화 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "순서 문제는 단락 첫머리의 단서가 앞 내용과 이어지는지 보는 거예요. In saying that, By extension, also 같은 말이 무엇을 받는지 찾아볼게요."}}],
    exam=exam,
    key_words={"passage": [g("trigger", "유발하다"), g("instinctive", "본능적인"), g("spectacle", "구경거리"), g("primarily", "주로"),
                           g("be subject to", "~에 영향을 받다"), g("perception", "지각, 인식"), g("bring to bear", "적용하다"),
                           g("by extension", "더 나아가"), g("grain", "결"), g("blend A with B", "A를 B와 혼합하다"),
                           g("innovative", "혁신적인"), g("established", "기존의"), g("draw on", "활용하다"),
                           g("repertoire", "레퍼토리"), g("convention", "관습"), g("imitation", "모방"),
                           g("spectacular", "장관인"), g("amaze", "놀라게 하다"), g("outdo", "능가하다"),
                           g("collective", "집단의"), g("witness", "목격하다"), g("stress", "강조하다"), g("universal", "보편적인"),
                           g("inevitable", "필연적인"), g("strategy", "전략"), g("address", "해결하다"),
                           g("liken A to B", "A를 B에 비유하다"), g("literature", "문학"), g("bound", "얽매인"),
                           g("sufficient", "충분한"), g("originality", "독창성"), g("impress", "깊은 인상을 주다")],
               "options": []},
    sentences=sentences)

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="순서 푸는 법")
