"""2022년 3월 고3 30번 레슨 + 대사를 만든다 (문맥상 낱말의 쓰임). 오답률 42.0% · Top 9.

    py scripts/lessons/gen_moeui_2022_03_30.py   (→ node scripts/policy_copy.mjs stamp <id> → npm run build)

틀: 어휘(2024년 3월 30번·42번과 같다) — 요지 → 두 쪽(+ 좋게 / − 나쁘게) → 밑줄 단어가 흐름에 맞는지 하나씩 점검.
정답이 아닌 밑줄은 「문맥에 맞아요」로 짚어 점검표(rows)에 쌓고, 정답 밑줄(④)은 흐름만 잡게 하고 맞다/틀리다는 문제에서 고른다.
정답 ④ right (→ wrong). 해설지: "맞는(right)을 문맥상 틀린(wrong)으로 바꿔야 한다."
열쇠: 대시(—) 사이 「새 기술이 실제로 그가 두려워한 결과를 자주 가져왔다」 → 소크라테스는 틀리지 않았다, but 근시안적이었다.
많이 고른 오답 ③ receive 18% — option_review로 같이 본다 (가르침 없이 정보를 '받기만' 한다는 소크라테스의 걱정과 맞음).
평가 뒤집기(evaluation-flip)는 쓰지 않는다 — 글쓴이가 소크라테스를 반은 맞고 반은 근시안이라 보는, 평소와 반대 평가가 아니다.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
bemoan·conceit는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt). 원문의 ─ 는 대시(—)로 적었다(두 개 = 삽입).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish, METHOD_IMAGES)

ID = "moeui-2022-03-30-socrates-writing"

S = [
    "Just as there’s a tendency to glorify technological progress, there’s a countertendency to expect the worst of every new tool or machine.",
    "In Plato’s Phaedrus, Socrates bemoaned the ①development of writing.",
    "He feared that, as people came to rely on the written word as a ②substitute for the knowledge they used to carry inside their heads, "
    "they would, in the words of one of the dialogue’s characters, “cease to exercise their memory and become forgetful.”",
    "And because they would be able to “③receive a quantity of information without proper instruction,” they would “be thought very "
    "knowledgeable when they are for the most part quite ignorant.”",
    "They would be “filled with the conceit of wisdom instead of real wisdom.”",
    "Socrates wasn’t ④right — the new technology did often have the effects he feared — but he was shortsighted.",
    "He couldn’t ⑤foresee the many ways that writing and reading would serve to spread information, spark fresh ideas, and expand "
    "human knowledge (if not wisdom).",
]
KO = [
    "기술의 발달을 미화하는 경향이 있는 것과 마찬가지로, 모든 새로운 도구나 기계에서 최악의 것을 예상하는 반대 경향도 있다.",
    "플라톤의 『Phaedrus』에서, 소크라테스는 글쓰기의 발전을 한탄했다.",
    "그는 사람들이 머릿속에 지니고 다니던 지식에 대한 대체물로서 글로 쓰인 말에 의존하게 됨에 따라, 대화의 등장인물 중 한 사람의 말처럼, 그들은 '기억력을 발휘하는 것을 멈추고 잘 잊어버리게' 될 것이라고 우려했다.",
    "그리고 그들은 '적절한 가르침 없이 많은 양의 정보를 받을' 수 있을 것이기 때문에, '대체로 상당히 무지할 때도 매우 박식하다고 생각될' 것이었다.",
    "그들은 '진정한 지혜 대신 지혜의 자만심으로 가득 차' 있게 될 것이었다.",
    "소크라테스가 틀리지는 않았지만(새로운 기술은 자주 그가 두려워했던 결과를 실제로 가져왔지만), 그는 근시안적이었다.",
    "그는 쓰기와 읽기가 정보를 전파하고, 신선한 생각을 촉발하며, (지혜는 아닐지라도) 인간의 지식을 확장하는 데 도움이 될 많은 방법을 예견할 수 없었다.",
]
UNDER = ["①development", "②substitute", "③receive", "④right", "⑤foresee"]

PLUS = "(+) 좋은 쪽"
MINUS = "(−) 나쁜 쪽"


def board(left, right, fresh=(), sort=None):
    return groups("새 기술을 보는 눈", PLUS, left, MINUS, right, fresh=fresh, between="vs",
                  sort={"words": sort, "left": PLUS, "right": MINUS} if sort else None)


def check(*done):
    """밑줄 점검표 — 문맥에 맞는다고 확인한 밑줄만 쌓는다 (정답 밑줄 ④는 쓰지 않는다)"""
    names = {"1": ("①", "bemoaned the development of writing", "글쓰기의 발전을 한탄했다"),
             "2": ("②", "a substitute for the knowledge", "머릿속 지식 대신 글에 기댄다"),
             "3": ("③", "receive information without instruction", "가르침 없이 정보만 받는다"),
             "5": ("⑤", "shortsighted → couldn’t foresee", "근시안적 → 내다보지 못했다")}
    return rows(*[(names[d][0] + " 맞음", names[d][1], names[d][2], "hl") for d in done])


L1 = [("glorify progress", "진보를 미화")]
R1 = [("expect the worst", "최악을 예상")]
R2 = R1 + [("bemoaned writing", "글쓰기를 한탄")]
R3 = R2 + [("become forgetful", "잘 잊어버림")]
R4 = R3 + [("quite ignorant", "상당히 무지")]
R5 = R4 + [("conceit of wisdom", "지혜의 자만심")]
L7 = L1 + [("spread information", "정보를 퍼뜨림"), ("spark fresh ideas", "새 생각을 일으킴"), ("expand human knowledge", "지식을 넓힘")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Just as", "~인 것처럼"), g("there’s a tendency", "경향이 있다"), g("to glorify", "미화하는, 좋게만 보는"),
                    g("technological progress", "기술의 발달"), g("there’s a countertendency", "반대 경향이 있다"),
                    g("to expect the worst", "최악을 예상하는"), g("of every new tool or machine", "모든 새 도구나 기계에서")],
        "slashes": ["there’s a tendency", "technological progress,", "a countertendency", "expect the worst"],
        "roles": [r("a tendency", "S"), r("a countertendency", "S"), r("’s … ’s", "V")],
        "steps": [
            choice("s1_counter",
                   "Just as A, B는 'A인 것처럼 B도'예요. 새 도구나 기계를 두고 반대 경향(countertendency)은 무엇을 한대요?",
                   [("o0", "최악을 예상한다", True), ("o1", "더 높이 칭찬한다", False), ("o2", "아무 관심을 두지 않는다", False)],
                   "콤마(,) 뒤 'to expect the worst'를 봐요.",
                   why="'expect the worst of every new tool or machine', 새 도구마다 최악을 예상하는 경향이래요. 기술을 미화하는(glorify) 경향과 반대예요.",
                   highlight=["glorify", "expect the worst"],
                   tips=[tip("Just as A, B", "'A인 것처럼 B도 그렇다'예요. 앞뒤가 짝을 이뤄요.", "Just as")],
                   panel=board(L1, R1, fresh=("expect the worst",)),
                   point="요지 시작: 새 기술을 미화하는 경향(+) ↔ 최악을 예상하는 경향(−)"),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("In Plato’s Phaedrus", "플라톤의 『파이드로스』에서"), g("Plato’s Phaedrus", "플라톤의 『파이드로스』"),
                    g("Socrates", "소크라테스는"), g("bemoaned", "한탄했다"), g("development of writing", "글쓰기의 발전")],
        "slashes": ["In Plato’s Phaedrus,"],
        "roles": [r("Socrates", "S"), r("bemoaned", "V"), r("the ①development", "O")],
        "steps": [
            choice("s2_sort",
                   "소크라테스는 글쓰기의 발전을 bemoan(한탄)했대요. 칠판 어느 쪽일까요?",
                   [("o0", PLUS, False), ("o1", MINUS, True)],
                   "bemoan은 시험지 아래에 '한탄하다'라고 풀어 줬어요.",
                   why="한탄했다는 건 글쓰기를 나쁘게 봤다는 거예요. 1문장의 '최악을 예상하는 경향'의 예예요.",
                   highlight=["bemoaned"],
                   panel=board(L1, R1, sort=["bemoaned writing"])),
            show("s2_check", "새 기술(글쓰기)이 발전하는 걸 한탄했다는 말이라 ①development는 문맥에 맞아요.",
                 panel=check("1"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("He", "그는"), g("feared", "두려워했다"), g("people", "사람들"), g("came to rely on", "~에 의존하게 되었다"),
                    g("the written word", "글로 쓰인 말"), g("as a substitute for", "~의 대체물로"), g("the knowledge", "지식"),
                    g("they used to carry inside their heads", "머릿속에 지니고 다니던"),
                    g("in the words of one of the dialogue’s characters", "대화의 등장인물 중 한 사람의 말로"),
                    g("would", "~할 것이다"), g("cease to exercise their memory", "기억력을 쓰기를 멈추다"),
                    g("become forgetful", "잘 잊어버리게 되다")],
        "slashes": ["He feared that,", "rely on the written word", "the knowledge", "inside their heads,", "they would,",
                    "dialogue’s characters,", "exercise their memory"],
        "roles": [r("He", "S"), r("feared", "V"), r("people", "S"), r("came", "V"), r("would … cease", "V"), r("become", "V")],
        "modifiers": ["they used to carry inside their heads"],
        "steps": [
            sv("s3_sv", ["He", "feared", "people", "came", "the written word"],
               {"He": "S", "feared": "V"},
               {"people": "그건 as(~함에 따라) 덩어리 안의 주어예요.", "came": "그건 as 덩어리 안의 동사예요.",
                "the written word": "그건 rely on 뒤 덩어리예요."},
               "주어는 He, 동사는 feared예요. that 뒤가 소크라테스가 두려워한 내용이에요.",
               ask="아주 긴 문장이에요. 맨 앞 메인 문장의 주어(S)와 동사(V)를 찾아볼까요?",
               faded=["in the words of one of the dialogue’s characters,"]),
            choice("s3_fear",
                   "소크라테스는 사람들이 글에 기대면 어떻게 될까 봐 두려워했대요?",
                   [("o0", "기억력을 안 써서 잘 잊어버리게 된다", True), ("o1", "글을 너무 많이 써서 지친다", False),
                    ("o2", "남의 생각만 따라 하게 된다", False)],
                   "따옴표 안 'cease to exercise their memory and become forgetful'을 봐요.",
                   why="'cease to exercise their memory and become forgetful', 기억력 쓰기를 멈추고 잘 잊어버리게 된대요. 소크라테스의 걱정(−)이에요.",
                   highlight=["cease to exercise their memory", "become forgetful"],
                   faded=["in the words of one of the dialogue’s characters,"],
                   tips=[tip("come to + 동사", "'~하게 되다'예요. came to rely on = 의존하게 되었다.", "came to"),
                         tip("cease to + 동사", "'~하기를 멈추다'예요. cease to exercise = 쓰기를 멈추다.", "cease")],
                   panel=board(L1, R3, fresh=("become forgetful",))),
            show("s3_check", "머릿속 지식을 대신하는 것(substitute)으로 글에 기대니, 기억력을 안 쓰게 된다는 흐름이에요. 그래서 ②substitute는 문맥에 맞아요.",
                 highlight=["substitute", "the knowledge"],
                 tips=[tip("substitute for ~", "'~의 대체물, ~을 대신하는 것'이에요.", "substitute"),
                       tip("used to + 동사", "'(예전에) ~하곤 했다'예요. they used to carry = 지니고 다니던.", "used to")],
                 panel=check("1", "2"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("And because", "그리고 ~ 때문에"), g("they would be able to", "그들은 ~할 수 있을 것이다"),
                    g("receive", "받다"), g("a quantity of information", "많은 양의 정보"),
                    g("without proper instruction", "제대로 된 가르침 없이"), g("they would", "그들은 ~할 것이다"),
                    g("be thought", "~라고 여겨지다"), g("very knowledgeable", "아주 박식한"), g("when they are", "그들이 ~일 때에도"),
                    g("for the most part", "대체로"), g("quite ignorant", "상당히 무지한")],
        "slashes": ["they would be able", "a quantity of information", "proper instruction,”", "very knowledgeable", "when they are"],
        "roles": [r("they … they … they", "S"), r("would be able", "V"), r("be thought", "V"), r("very knowledgeable", "C"),
                  r("are", "V"), r("quite ignorant", "C")],
        "steps": [
            sv("s4_sv", ["receive", "information", "be thought", "very knowledgeable", "are"],
               {"be thought": "V", "very knowledgeable": "C"},
               {"receive": "그건 because 덩어리 안의 동사예요.", "information": "그건 receive 뒤 받는 것이에요.",
                "are": "그건 when 덩어리 안의 동사예요."},
               "메인 문장은 they would be thought very knowledgeable, '아주 박식하다고 여겨질 것이다'예요.",
               ask="because 덩어리가 길어요. 콤마(,) 뒤 메인 문장의 동사(V)와 보어(C)를 찾아볼까요?"),
            choice("s4_seem",
                   "가르침 없이 많은 정보를 받으면, 사람들은 어떻게 보인대요?",
                   [("o0", "실제로는 무지한데 박식하다고 여겨진다", True), ("o1", "정말로 박식해진다", False),
                    ("o2", "정보를 하나도 기억하지 못한다", False)],
                   "when 뒤 'for the most part quite ignorant'를 봐요. ignorant는 '무지한'이에요.",
                   why="'be thought very knowledgeable when they are … quite ignorant', 실제론 무지한데 박식해 보인대요. 이것도 걱정(−)이에요.",
                   highlight=["very knowledgeable", "quite ignorant"],
                   tips=[tip("a quantity of", "'많은 양의'예요. a quantity of information = 많은 양의 정보.", "a quantity of"),
                         tip("for the most part", "'대체로, 대부분'이에요.", "for the most part")],
                   panel=board(L1, R4, fresh=("quite ignorant",))),
            show("s4_check", "가르침 없이 정보만 '받으니(receive)' 아는 척만 하게 된다, 걱정의 흐름에 맞아요. 그래서 ③receive는 문맥에 맞아요.",
                 highlight=["receive", "without proper instruction"],
                 panel=check("1", "2", "3"), panel_below=True, button="다음 문장"),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("They", "그들은"), g("would be", "~일 것이다"), g("filled with", "~으로 가득 찬"),
                    g("the conceit of wisdom", "지혜의 자만심"), g("instead of real wisdom", "진정한 지혜 대신")],
        "slashes": ["They would be", "the conceit of wisdom"],
        "roles": [r("They", "S"), r("would be", "V")],
        "steps": [
            show("s5_conceit", "진짜 지혜 대신 '지혜의 자만심(conceit)'으로 가득 찬대요. 소크라테스의 걱정은 여기까지예요.",
                 highlight=["the conceit of wisdom", "real wisdom"],
                 panel=board(L1, R5, fresh=("conceit of wisdom",)), button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Socrates", "소크라테스는"), g("wasn’t", "~가 아니었다"), g("right", "옳은, 맞는"),
                    g("the new technology", "그 새 기술은"), g("did often have", "실제로 자주 가져왔다"),
                    g("the effects he feared", "그가 두려워한 결과"), g("but he was shortsighted", "하지만 그는 근시안적이었다"),
                    g("shortsighted", "근시안적인, 멀리 못 보는")],
        "slashes": ["wasn’t ④right", "the effects he feared —"],
        "roles": [r("Socrates", "S"), r("wasn’t", "V"), r("the new technology", "S"), r("did often have", "V"), r("the effects", "O")],
        "steps": [
            choice("s6_dash",
                   "대시(—) 두 개 사이를 봐요. 새 기술은 소크라테스가 두려워한 결과를 실제로 가져왔대요, 아니래요?",
                   [("o0", "실제로 자주 가져왔다", True), ("o1", "전혀 가져오지 않았다", False)],
                   "'did often have the effects he feared'를 봐요. 동사 앞 did는 '정말로'라는 강조예요.",
                   why="'the new technology did often have the effects he feared', 새 기술이 그가 걱정한 결과를 정말로 자주 가져왔대요. 그의 걱정에 맞는 부분이 있었던 거예요.",
                   highlight=["did often have", "the effects he feared"],
                   tips=[tip("did + 동사원형 (강조)", "동사 앞 do·does·did는 '정말로, 실제로'라는 강조예요. did have = 실제로 가져왔다.", "did often have")]),
            choice("s6_but",
                   "but 뒤에서 그는 shortsighted(근시안적)였대요. 그럼 대시(—) 내용으로 보아, but 앞은 소크라테스를 어떻게 보는 말일까요?",
                   [("o0", "그의 걱정에도 맞는 부분이 있었다 (+)", True), ("o1", "그의 걱정은 완전히 엉터리였다 (−)", False)],
                   "걱정한 결과가 실제로 일어났다면, 소크라테스의 걱정은 맞은 걸까요, 틀린 걸까요?",
                   why="걱정한 일이 실제로 일어났으니 그의 걱정엔 맞는 부분이 있었어요. but 앞은 이렇게 인정하고, 뒤는 '하지만 멀리는 못 봤다'로 꼬집어요.",
                   highlight=["did often have", "but he was shortsighted"],
                   signs=[{"text": "did often have", "sign": "+"}, {"text": "shortsighted", "sign": "−"}],
                   point="대시 사이: 걱정한 결과가 실제로 일어났다 → but 앞은 그를 인정(+), 뒤는 근시안(−) — 이 흐름에 ④가 맞는지 문제에서 확인"),
            show("s6_hold", "대시(—) 사이 내용과 but 앞뒤 흐름에 밑줄 ④가 맞는지는 마지막 문제에서 같이 확인해 봐요.",
                 signs=[{"text": "did often have", "sign": "+"}, {"text": "shortsighted", "sign": "−"}], button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("He", "그는"), g("couldn’t", "~할 수 없었다"), g("foresee", "내다보다, 예견하다"), g("the many ways", "많은 방식"),
                    g("writing and reading", "쓰기와 읽기"), g("would serve to", "~하는 데 도움이 될 것이다"),
                    g("spread information", "정보를 퍼뜨리다"), g("spark fresh ideas", "새로운 생각을 일으키다"),
                    g("expand human knowledge", "인간의 지식을 넓히다"), g("if not wisdom", "지혜는 아닐지라도")],
        "slashes": ["the many ways", "would serve", "spread information,", "spark fresh ideas,"],
        "roles": [r("He", "S"), r("couldn’t … foresee", "V"), r("the many ways", "O")],
        "modifiers": ["that writing and reading would serve to spread information, spark fresh ideas, and expand human knowledge"],
        "steps": [
            choice("s7_ways",
                   "소크라테스가 내다보지 못한 건 무엇이래요?",
                   [("o0", "글이 정보를 퍼뜨리고 지식을 넓힐 많은 방식", True), ("o1", "글이 기억력을 망치는 방식", False),
                    ("o2", "사람들이 글을 싫어할 이유", False)],
                   "the many ways that 뒤 'spread information, spark fresh ideas, and expand human knowledge'를 봐요.",
                   why="'spread information, spark fresh ideas, and expand human knowledge', 글이 정보를 퍼뜨리고 새 생각을 일으키고 지식을 넓히는 좋은 점(+)을 못 봤대요.",
                   highlight=["spread information", "spark fresh ideas", "expand human knowledge"],
                   tips=[tip("serve to + 동사", "'~하는 데 도움이 되다, 쓰이다'예요.", "serve to"),
                         tip("if not ~", "'~은 아닐지라도'예요. (if not wisdom) = 지혜까지는 아닐지라도.", "if not")],
                   panel=board(L7, R5, fresh=("spread information", "spark fresh ideas", "expand human knowledge"))),
            show("s7_check", "근시안적(shortsighted)이라 글의 좋은 점을 '내다보지 못했다(couldn’t foresee)', 앞 문장과 이어져요. 그래서 ⑤foresee는 문맥에 맞아요.",
                 highlight=["foresee"], panel=check("1", "2", "3", "5"), panel_below=True),
            show("s7_go", "①②③⑤는 흐름에 맞았어요. 남은 하나가 대시(—) 사이 내용과 but 앞뒤 흐름에 맞는지 문제에서 골라 봐요.",
                 panel=check("1", "2", "3", "5"), panel_below=True, button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 2, [m("In Plato’s Phaedrus", "플라톤의 『파이드로스』에서"), " ", m("Socrates", "소크라테스는"), " ",
                         m("the development of writing", "글쓰기의 발전"), "을 ", m("bemoaned", "한탄했다"), "."],
          match_display="In Plato’s Phaedrus, Socrates bemoaned the development of writing.",
          sv_new=sv_step("s2_basic_sv", ["Plato’s Phaedrus", "Socrates", "bemoaned", "writing"], {"Socrates": "S", "bemoaned": "V"},
                         {"Plato’s Phaedrus": "그건 In 뒤, 어디에서인지예요.", "writing": "그건 of 뒤 덩어리예요."},
                         "주어는 Socrates, 동사는 bemoaned예요."),
          meaning_after="s2_sort")
add_basic(sentences, 5, [m("They", "그들은"), " ", m("instead of real wisdom", "진정한 지혜 대신"), " ", m("the conceit of wisdom", "지혜의 자만심"),
                         "으로 ", m("filled with", "가득 찬"), " 상태", m("would be", "일 것이다"), "."],
          sv_new=sv_step("s5_basic_sv", ["They", "would be", "wisdom"], {"They": "S", "would be": "V"},
                         {"wisdom": "그건 of 뒤 덩어리예요."}, "주어는 They, 동사는 would be예요."),
          meaning_ids=["s5_conceit"])

SENSES = {
    1: [sense("as", "Just as there’s", "~인 것처럼", "Just as A, B = A인 것처럼 B도"),
        sense("to", "tendency to glorify", "~하는 (경향)", "to부정사 (앞 명사 tendency를 꾸밈)"),
        sense("to", "countertendency to expect", "~하는 (반대 경향)", "to부정사 (앞 명사 countertendency를 꾸밈)")],
    3: [sense("that", "feared that", "~라는 것을", "명사절 that (feared that …)"),
        sense("as", "as people came", "~함에 따라", "접속사 as + 주어·동사 (변화)"),
        sense("to", "came to rely", "~하게 (되다)", "come to + 동사원형 = ~하게 되다"),
        sense("as", "as a substitute", "~로서", "전치사 as (자격)"),
        sense("for", "substitute for the knowledge", "~의 (대체물)", "substitute for ~ = ~의 대체물"),
        sense("to", "used to carry", "~하곤 (했다)", "used to + 동사원형 = (예전에) ~하곤 했다"),
        sense("to", "cease to exercise", "~하기를 (멈추다)", "cease + to부정사")],
    4: [sense("to", "able to receive", "~할 (수 있는)", "be able to + 동사원형"),
        sense("for", "for the most part", "(for the most part의 일부)", "for the most part = 대체로")],
    6: [sense("but", "but he was shortsighted", "하지만", "접속사 but (대조)")],
    7: [sense("that", "ways that writing", "(앞 명사를 꾸밈)", "관계사 that + 주어·동사 (the many ways를 꾸밈)"),
        sense("to", "serve to spread", "~하는 데 (도움이 되다)", "serve + to부정사"),
        sense("if", "if not wisdom", "~은 아닐지라도", "if not ~ = ~까지는 아니더라도")],
}

WORDS = {"there’s": "~이 있다", "just": "~인 바로 그대로", "tendency": "경향", "glorify": "미화하다", "technological": "기술의", "progress": "발달, 진보",
         "countertendency": "반대 경향", "expect": "예상하다", "worst": "최악", "every": "모든", "new": "새로운", "tool": "도구",
         "machine": "기계", "plato’s": "플라톤의", "phaedrus": "『파이드로스』(플라톤의 대화편)", "socrates": "소크라테스",
         "bemoaned": "한탄했다", "development": "발전", "writing": "글쓰기", "feared": "두려워했다", "people": "사람들", "came": "~하게 되었다",
         "rely": "의존하다", "written": "글로 쓰인", "word": "말", "substitute": "대체물", "knowledge": "지식", "used": "~하곤 했다",
         "carry": "지니고 다니다", "inside": "~ 안에", "heads": "머리", "words": "말", "dialogue’s": "대화편의", "characters": "등장인물",
         "cease": "멈추다", "exercise": "발휘하다, 쓰다", "memory": "기억력", "become": "~해지다", "forgetful": "잘 잊어버리는",
         "able": "~할 수 있는", "receive": "받다", "quantity": "양", "information": "정보", "proper": "제대로 된", "instruction": "가르침",
         "thought": "여겨지는", "knowledgeable": "박식한", "most": "대부분", "part": "부분", "quite": "상당히", "ignorant": "무지한",
         "filled": "가득 찬", "conceit": "자만심", "wisdom": "지혜", "instead": "대신에", "real": "진정한", "wasn’t": "~가 아니었다",
         "right": "옳은, 맞는", "technology": "기술", "often": "자주", "effects": "결과, 효과", "shortsighted": "근시안적인",
         "couldn’t": "~할 수 없었다", "foresee": "내다보다", "ways": "방식", "reading": "읽기", "serve": "도움이 되다", "spread": "퍼뜨리다",
         "spark": "일으키다, 촉발하다", "fresh": "새로운", "ideas": "생각", "expand": "넓히다, 확장하다", "human": "인간의",
         "would": "~할 것이다", "be": "~이다", "did": "실제로 (강조)", "have": "가져오다",
         "be thought": "~라고 여겨지다"}

STORIES = [
    (2, [sc("문장 1~2", "📜", "expect the worst · bemoaned writing", "새 기술마다 최악을 예상하는 경향 — 소크라테스도 글쓰기를 한탄했어요")]),
    (5, [sc("문장 3~5", "🧠", "forgetful · ignorant · conceit", "글에 기대면 잊어버리고, 아는 척만 하고, 자만심만 커질 거라고 걱정했어요")]),
]

exam = {
    "question": "다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?",
    "underline": UNDER, "sentence": 6, "analysis_first": True, "wrong_rate": 42.0, "wrong_rank": 9,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("development", "발전"), g("substitute", "대체물"), g("receive", "받다"), g("right", "옳은, 맞는"), g("foresee", "내다보다")],
    "options": [
        {"id": "1", "label": "development", "keywords": ["development"], "ko": "발전"},
        {"id": "2", "label": "substitute", "keywords": ["substitute"], "ko": "대체물"},
        {"id": "3", "label": "receive", "keywords": ["receive"], "ko": "받다"},
        {"id": "4", "label": "right", "keywords": ["right"], "ko": "옳은, 맞는", "correct": True},
        {"id": "5", "label": "foresee", "keywords": ["foresee"], "ko": "내다보다"},
    ],
    "brief": exam_brief(
        "밑줄 점검표를 떠올려 봐요. 대시(—) 사이 내용과 but 앞뒤 흐름에 맞지 않는 하나를 골라요.",
        "정답이에요! 대시(—) 사이에서 새 기술이 그가 걱정한 결과를 실제로 가져왔다고 했어요. 그러니 '소크라테스가 틀리지는 않았다'가 맞고, but 뒤 '근시안적이었다'와 이어져요. right가 아니라 wrong이어야 해요.",
        "정답은 ④예요. 걱정한 일이 실제로 일어났으니 소크라테스는 틀리지 않았어요(wasn’t wrong). right를 wrong으로 바꿔야 해요.",
        {"1": "소크라테스가 새 기술인 글쓰기의 발전(development)을 한탄했다는 말이라 맞아요.",
         "2": "머릿속 지식을 대신하는 것(substitute)으로 글에 기댄다는 말이라 맞아요.",
         "3": "가르침 없이 정보만 받는다(receive)는 소크라테스의 걱정이라 맞아요.",
         "5": "근시안적이라 글의 좋은 점을 내다보지(foresee) 못했다는 말이라 맞아요."},
        {"3": review(18,
                     "③ 앞뒤를 봐요. 사람들이 가르침 없이(without proper instruction) 많은 정보를 받기만 하면, 실제론 무지한데 박식해 보일 거라는 걱정이에요. receive(받다)는 이 걱정과 딱 맞아요.",
                     panel=rows(("③", "receive information without proper instruction", "가르침 없이 정보만 받는다 → 걱정과 맞음", "hl"),
                                ("④", "wasn’t right — did often have the effects he feared —", "걱정한 일이 실제로 일어남 → '틀리지 않았다'여야", "hl2")),
                     rank_word="가장 많이 고른")}),
}

# ── 해석 맞추기(모두에게)·가리키는 말 — 2026-10-20 엔진: S·V 찾기·핵심어 자유 해석은 빠지고 맞추기가 대신 나온다 ──
from beginner import add_match, add_refers, m as _m  # noqa: E402
add_match(sentences, 3, ["그는 사람들이 ", _m("the written word", "글로 쓰인 말에"), " ", _m("came to rely on", "의존하게 됨에 따라"), " ",
                         _m("cease to exercise their memory", "기억력을 발휘하는 것을 멈추고"), " ", _m("become forgetful", "잘 잊어버리게 될 것이라고"), " ", _m("feared", "우려했다"), "."],
          display="He feared that, as people came to rely on the written word, they would “cease to exercise their memory and become forgetful.”")
add_match(sentences, 4, ["그리고 ", _m("without proper instruction", "적절한 가르침 없이"), " ", _m("a quantity of information", "많은 양의 정보를"), " 받을 수 있을 것이기 때문에, ",
                         _m("quite ignorant", "상당히 무지"), "할 때도 ", _m("very knowledgeable", "매우 박식하다고"), " ", _m("be thought", "생각될 것이었다"), "."],
          display="And because they would be able to “receive a quantity of information without proper instruction,” they would “be thought very knowledgeable when they are quite ignorant.”")
add_refers(sentences, 3, {"He": "Socrates(소크라테스)"})
add_refers(sentences, 5, {"They": "people who rely on writing(글에 의존하게 된 사람들)"})
add_refers(sentences, 6, {"he": "Socrates(소크라테스)"})
add_refers(sentences, 7, {"He": "Socrates(소크라테스)"})

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 30번 (문맥상 낱말의 쓰임)",
    topic="어휘 문제 푸는 법: 요지 → 두 쪽(+ 좋은 쪽 / − 나쁜 쪽) → 밑줄 단어가 흐름에 맞는지 하나씩 점검",
    method={"type": "word_in_context", "labels": ["요지 잡기", "두 그룹으로 나누기", "밑줄 단어 맞춰 보기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-socrates-writing.svg", ("Writing", "글쓰기"), "vs", ("Memory", "기억력"),
                                       "글쓰기는 우리를 더 똑똑하게 할까?", "2022년 3월 30번 도입 칠판"),
                      "alt": "칠판: Writing(글쓰기) vs Memory(기억력)", "kind": "drawing"},
            "method": METHOD_IMAGES["vocab"]},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "새로운 기술이 나오면 걱정부터 하는 사람들이 있어요. 이번 글은 소크라테스가 '글쓰기'라는 새 기술을 걱정한 이야기예요."}},
           {"id": "method1", "type": "say", "button": "네",
            "brief": {"say": "어휘 문제는 단어 뜻만 보면 다 맞아 보여요. 문장마다 흐름을 잡아야 틀린 단어가 보여요."}},
           {"id": "method2", "type": "say", "button": "좋아요",
            "brief": {"say": "요지를 잡고, 좋은 쪽과 나쁜 쪽 두 그룹으로 나눈 뒤, 밑줄 단어가 흐름에 맞는지 하나씩 볼 거예요. 칠판 순서대로 해 볼게요."}}],
    exam=exam,
    key_words={"passage": [g("tendency", "경향"), g("glorify", "미화하다"), g("progress", "발달, 진보"), g("countertendency", "반대 경향"),
                           g("rely on", "~에 의존하다"), g("substitute", "대체물"), g("cease", "멈추다"), g("forgetful", "잘 잊어버리는"),
                           g("a quantity of", "많은 양의"), g("instruction", "가르침"), g("knowledgeable", "박식한"),
                           g("for the most part", "대체로"), g("ignorant", "무지한"), g("shortsighted", "근시안적인"),
                           g("foresee", "예견하다"), g("spark", "촉발하다"), g("expand", "확장하다")],
               "options": [g("right", "옳은, 맞는"), g("wrong", "틀린")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# exercise (기억력을) 발휘하다, 쓰다.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    3: [tip("exercise", "이 글에서는 → (기억력을) 발휘하다, 쓰다  ('운동하다' 아님)", "exercise", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="어휘 문제 푸는 법",
       chunks={"He": "그는", "feared": "두려워했다", "people": "사람들", "came": "~하게 되었다", "the written word": "글로 쓰인 말",
               "receive": "받다", "information": "정보", "be thought": "~라고 여겨지다", "very knowledgeable": "아주 박식한", "are": "~이다",
               "Plato’s Phaedrus": "플라톤의 『파이드로스』", "Socrates": "소크라테스는", "bemoaned": "한탄했다", "writing": "글쓰기",
               "They": "그들은", "would be": "~일 것이다", "wisdom": "지혜", "filled with": "~으로 가득 찬",
               "the conceit of wisdom": "지혜의 자만심", "instead of real wisdom": "진정한 지혜 대신",
               "In Plato’s Phaedrus": "플라톤의 『파이드로스』에서", "the development of writing": "글쓰기의 발전"})
