"""2024년 3월 고3 23번 레슨 + 대사를 만든다 (주제, 3점). 오답률 자료 없음(Top 15 밖).

    python3 scripts/lessons/gen_moeui_2024_03_23.py   (→ npm run policy:copy stamp <id> → npm run build)

주제 유형은 처음 — 요지(22번)·제목(24번) 틀을 따른 Claude 초안(2026-10-18, 미니 모의고사 연결용):
되풀이되는 핵심어(group, tribe, us) 모으기 → 글쓴이가 설명하는 현상 잡기 → 글 전체를 명사구 한 줄로 → 바꿔 쓴 보기.
정답 ① tendency to prefer the group that one identifies with. 해설지 해석과 대조함. 23번 E = mc²는 문제지에서 그림이라 되살렸다.
innate는 시험지 아래 *로 풀어 준 단어(핵심어 아님).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, sv, tip, groups, rows, sense, sc, m, sv_step, add_basic, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, finish)

ID = "moeui-2024-03-23-tribe-thinking"

S = [
    "Sociologist Brooke Harrington said if there was an E = mc² of social science, it would be SD>PD, “social death is more frightening than physical death.”",
    "This is why we feel deeply threatened when a new idea challenges the ones that have become part of our identity.",
    "For some ideas, the ones that identify us as members of a group, we don’t reason as individuals; we reason as a member of a tribe.",
    "We want to seem trustworthy, and reputation management as a trustworthy individual often overrides most other concerns, even our own mortality.",
    "This is not entirely irrational.",
    "A human alone in this world faces a lot of difficulty, but being alone in the world before modern times was almost certainly a death sentence.",
    "So we carry with us an innate drive to form groups, join groups, remain in those groups, and oppose other groups.",
    "But once you can identify them, you start favoring us; so much so that given a choice between an outcome that favors both groups a lot "
    "or one that favors both much less but still favors yours more than theirs, that’s the one you will pick.",
]
KO = [
    "사회학자 Brooke Harrington은 사회 과학의 E = mc²가 있다면, 그것은 SD>PD, 즉 '사회적 죽음이 신체적 죽음보다 더 무섭다.'일 것이라고 말했다.",
    "이것은 새로운 개념이 우리 정체성의 일부가 된 것들에 도전할 때 우리가 매우 위협적으로 느끼는 이유이다.",
    "우리가 한 집단의 구성원으로 우리를 동일시하는 몇몇 견해에 대하여, 우리는 개인으로서 판단하지 않고, 우리는 한 부족의 구성원으로서 판단한다.",
    "우리는 믿음직스럽게 보이고 싶고, 믿음직한 개인으로서의 평판 관리는 흔히 다른 모든 걱정, 심지어 우리 자신의 죽음보다 더 중요하다.",
    "이것은 완전히 비이성적인 것이 아니다.",
    "이 세상에 홀로 있는 인간은 많은 어려움을 직면하지만, 근대 이전의 세상에서 혼자 있는 것은 거의 확실하게 사형 선고였다.",
    "그래서 우리는 집단을 형성하고, 집단에 합류하고, 그 집단에 남아 있고, 다른 집단에 반대하려는 타고난 욕구를 가지고 있다.",
    "하지만 일단 여러분이 '그들'을 인식할 수 있게 되면, 여러분은 '우리'를 편들기 시작하는데, 매우 그러하므로, 양쪽 집단 모두를 크게 유리하게 하는 결과 또는 양측 모두에게 훨씬 덜 유리하게 하지만 여전히 여러분의 집단을 그들보다 더 유리하게 하는 것 사이에 선택이 주어졌을 때, 그것이 바로 여러분이 고르게 될 것이다.",
]


def board(words, fresh=()):
    return groups("되풀이되는 말", "집단 (group)", words, fresh=fresh)


W2 = [("social death", "사회적 죽음"), ("identity", "정체성")]
W3 = W2 + [("a member of a tribe", "부족의 일원")]
W7 = W3 + [("form, join, remain in groups", "집단을 만들고 머묾")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Sociologist Brooke Harrington", "사회학자 브룩 해링턴"), g("said", "말했다"), g("if there was", "만약 ~가 있다면"),
                    g("an E = mc² of social science", "사회 과학의 E = mc²(가장 중요한 공식)"), g("it would be", "그것은 ~일 것이다"),
                    g("SD>PD", "사회적 죽음 > 신체적 죽음"), g("social death", "사회적 죽음(무리에서 밀려남)"),
                    g("is more frightening than", "~보다 더 무섭다"), g("physical death", "신체적 죽음")],
        "slashes": ["Brooke Harrington said", "an E = mc²", "social science,", "SD>PD,", "more frightening"],
        "roles": [r("Sociologist Brooke Harrington", "S"), r("said", "V"), r("was", "V"), r("an E = mc²", "S"), r("it", "S"), r("would be", "V"),
                  r("SD>PD", "C"), r("social death", "S"), r("is", "V"), r("more frightening", "C")],
        "steps": [
            choice("s1_sdpd",
                   "SD>PD, 'social death is more frightening than physical death'는 무슨 뜻일까요?",
                   [("o0", "사람들은 몸이 죽는 것보다 무리에서 밀려나는 것을 더 무서워한다", True),
                    ("o1", "몸이 죽는 것이 가장 무섭다", False), ("o2", "사회 과학은 물리학보다 어렵다", False)],
                   "social death는 '사회적 죽음', 즉 집단에서 밀려나는 거예요. more A than B는 'B보다 더 A'예요.",
                   why="'social death is more frightening than physical death', 무리에서 밀려나는 사회적 죽음이 몸의 죽음보다 더 무섭대요.",
                   highlight=["social death", "physical death"],
                   tips=[tip("E = mc²", "아인슈타인의 유명한 공식이에요. 여기서는 '가장 핵심이 되는 법칙'이라는 뜻으로 빗대어 썼어요.")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "medium",
        "glosses": [g("This is why", "이것이 ~하는 이유이다"), g("we feel deeply threatened", "우리는 크게 위협을 느낀다"), g("when", "~할 때"),
                    g("a new idea", "새로운 생각"), g("challenges", "~에 맞서다, 도전하다"), g("the ones", "그것들(생각들)"),
                    g("that have become part of our identity", "우리 정체성의 일부가 된")],
        "slashes": ["This is why", "deeply threatened", "the ones"],
        "roles": [r("This", "S"), r("is", "V"), r("we", "S"), r("feel", "V"), r("deeply threatened", "C"), r("a new idea", "S"), r("challenges", "V"),
                  r("the ones", "O")],
        "modifiers": ["that have become part of our identity"],
        "steps": [
            show("s2_identity", "새 생각이 맞서는 건 그냥 생각이 아니라 정체성의 일부가 된 생각이에요. 그래서 크게 위협을 느낀대요.",
                 highlight=["challenges", "identity"],
                 panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/new-idea-challenge.svg",
                        "alt": "새 생각(a new idea)이 화살표로 기존 생각(the ones)에 맞선다. 기존 생각은 정체성(identity) 안에, 정체성은 우리 무리(group) 안에 있다. 아래: 크게 위협을 느낀다, 무리에서 밀려날 것 같아서"},  # 아래 단어 칩은 그림 속 글자와 겹쳐 뺀다 (2026-10-19 선생님)
                 tips=[tip("This is why ~", "'이것이 ~하는 이유이다'예요. 앞 문장이 원인, 뒤가 결과예요.", "This is why")], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("For some ideas", "어떤 생각들에 대해서는"), g("the ones that identify us", "우리를 ~로 규정하는 것들"),
                    g("as members of a group", "한 집단의 구성원으로"), g("we don’t reason as individuals", "우리는 개인으로서 판단하지 않는다"),
                    g("we reason", "우리는 판단한다"), g("as a member of a tribe", "한 부족의 일원으로서")],
        "slashes": ["For some ideas,", "identify us", "members of a group,", "as individuals;"],
        "roles": [r("we … we", "S"), r("don’t reason", "V"), r("reason", "V")],
        "modifiers": ["that identify us as members of a group"],
        "steps": [
            choice("s3_tribe",
                   "세미콜론(;) 앞뒤를 봐요. 집단과 관련된 생각에서는 우리가 어떻게 판단한대요?",
                   [("o0", "혼자 따로 생각해서 판단한다", False), ("o1", "부족의 일원으로서 판단한다", True), ("o2", "판단하지 않는다", False)],
                   "앞은 'don't reason as individuals(개인으로서 판단하지 않는다)', 뒤가 그 대신 어떻게 하는지예요.",
                   why="'we don’t reason as individuals; we reason as a member of a tribe', 개인이 아니라 부족의 일원으로서 판단한대요.",
                   highlight=["as individuals", "as a member of a tribe"],
                   point="집단과 관련된 생각 → 개인이 아니라 부족(집단)의 일원으로서 판단한다"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "medium",
        "glosses": [g("We want to seem trustworthy", "우리는 믿음직하게 보이고 싶다"), g("reputation management", "평판 관리"),
                    g("as a trustworthy individual", "믿음직한 개인으로서의"), g("often overrides", "흔히 ~보다 앞선다"),
                    g("most other concerns", "대부분의 다른 걱정"), g("even our own mortality", "심지어 우리 자신의 죽음까지")],
        "slashes": ["seem trustworthy,", "reputation management", "trustworthy individual", "most other concerns,"],
        "roles": [r("We", "S"), r("want", "V"), r("to seem trustworthy", "O"), r("reputation management", "S"), r("overrides", "V"),
                  r("most other concerns", "O")],
        "steps": [
            show("s4_reputation", "무리 안에서 믿음직하게 보이는 평판 관리가 다른 걱정, 심지어 죽음보다 앞선대요. SD>PD와 같은 말이에요.",
                 highlight=["overrides", "even our own mortality"], button="다음 문장",
                 panel=board(W3, fresh=tuple(w for w, _ in W3)),
                 tips=[tip("override", "'~보다 더 중요하다, ~을 무시하고 앞서다'예요.", "overrides")]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "low",
        "glosses": [g("This is not entirely irrational", "이것이 완전히 비이성적인 것은 아니다"), g("irrational", "비이성적인")],
        "roles": [r("This", "S"), r("is", "V"), r("irrational", "C")],
        "steps": [
            show("s5_not", "이게 완전히 말도 안 되는 건 아니래요. 다음 문장에 그 이유가 나와요.", highlight=["not entirely irrational"], button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("A human alone in this world", "이 세상에 홀로인 인간"), g("faces a lot of difficulty", "많은 어려움을 겪는다"),
                    g("being alone in the world", "세상에 혼자 있는 것"), g("before modern times", "근대 이전에는"),
                    g("was almost certainly a death sentence", "거의 확실한 사형 선고였다")],
        "slashes": ["in this world", "a lot of difficulty,", "in the world", "modern times"],
        "roles": [r("A human", "S"), r("faces", "V"), r("a lot of difficulty", "O"), r("being alone in the world", "S"), r("was", "V"),
                  r("a death sentence", "C")],
        "steps": [
            show("s6_alone", "옛날에는 혼자가 되면 거의 죽음이었대요. 그래서 무리에서 밀려나는 걸 그렇게 무서워하는 거예요.",
                 highlight=["a death sentence"], button="다음 문장"),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("So", "그래서"), g("we carry with us", "우리는 지니고 있다"), g("an innate drive", "타고난 욕구"),
                    g("to form groups", "집단을 만들려는"), g("join groups", "집단에 들어가다"), g("remain in those groups", "그 집단에 남다"),
                    g("oppose other groups", "다른 집단에 맞서다")],
        "slashes": ["an innate drive", "join groups,", "those groups,"],
        "roles": [r("we", "S"), r("carry", "V"), r("an innate drive", "O")],
        "steps": [
            sv("s7_sv", ["we", "carry", "an innate drive", "groups"], {"we": "S", "carry": "V", "an innate drive": "O"},
               {"groups": "그건 to form 뒤, 어떤 욕구인지 알려 주는 말이에요."},
               "주어는 we, 동사는 carry, 목적어는 an innate drive(타고난 욕구)예요. with us는 '지니고'예요."),
            show("s7_drive", "그래서 우리에겐 집단을 만들고, 들어가고, 남고, 다른 집단에 맞서려는 타고난 욕구가 있대요.",
                 highlight=["innate drive", "oppose other groups"], panel=board(W7, fresh=("form, join, remain in groups",)), button="다음 문장"),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("But once you can identify them", "하지만 일단 '그들'을 알아볼 수 있게 되면"), g("you start favoring us", "'우리'를 편들기 시작한다"),
                    g("so much so that", "너무 그래서"), g("given a choice between", "~ 사이에서 고르라면"),
                    g("an outcome that favors both groups a lot", "두 집단 모두에게 크게 유리한 결과"),
                    g("one that favors both much less", "둘 다에게 훨씬 덜 유리한 결과"),
                    g("but still favors yours more than theirs", "그래도 그들보다 우리 쪽에 더 유리한"), g("that’s the one you will pick", "바로 그것을 고를 것이다")],
        "slashes": ["identify them,", "favoring us;", "so much so that", "given a choice", "groups a lot", "much less", "than theirs,"],
        "roles": [r("you … you … you", "S"), r("can identify", "V"), r("them", "O"), r("start", "V"), r("favoring us", "O"), r("will pick", "V")],
        "modifiers": ["that favors both groups a lot", "that favors both much less but still favors yours more than theirs"],
        "steps": [
            choice("s8_pick",
                   "두 집단 모두 크게 이득 vs 둘 다 덜 이득이지만 우리 쪽이 더 이득. 사람들은 어느 쪽을 고른대요?",
                   [("o0", "두 집단 모두 크게 이득인 쪽", False), ("o1", "둘 다 덜 이득이어도 우리 쪽이 더 이득인 쪽", True),
                    ("o2", "아무것도 고르지 않는다", False)],
                   "마지막 'that’s the one you will pick'의 that은 바로 앞에 나온 'one that … still favors yours more than theirs'예요.",
                   why="'that’s the one you will pick'은 바로 앞의 '둘 다 덜 이득이지만 우리 쪽이 그들보다 더 이득인 결과'예요. 전체 이득보다 '우리 편'을 고른대요.",
                   highlight=["favoring us", "favors yours more than theirs"],
                   tips=[tip("favor", "동사로 '편들다, ~에게 유리하게 하다'예요. 명사 '호의'만 있는 게 아니에요.", "favoring", trap=True)],
                   point="일단 '그들'이 보이면 '우리'를 편든다 — 다 같이 더 이득보다 우리가 더 이득인 쪽을 고른다"),
            choice("s8_gist",
                   "글 전체가 무엇에 대한 이야기인지 한 줄로 묶으면요?",
                   [("o0", "평판을 쌓으려면 혼자 지내야 한다는 것", False), ("o1", "다른 관심사를 가진 집단을 만들어야 한다는 것", False),
                    ("o2", "사람은 자기가 속한 집단을 편드는 경향이 있다는 것", True)],
                   "칠판에 쌓인 말을 봐요. social death, tribe, form groups, favoring us — 모두 '내 집단'이에요.",
                   why="무리에서 밀려나는 게 가장 무섭고, 부족의 일원으로 판단하고, 집단을 만들고, 결국 '우리 편'을 고른대요. 내 집단을 편드는 경향이 이 글의 주제예요.",
                   panel=board(W7 + [("favoring us", "우리를 편듦")], fresh=("favoring us",)),
                   point="주제 = 자신이 속한 집단을 선호하는(편드는) 경향"),
            show("s8_go", "주제 문제는 이 한 줄을 명사구로 바꿔 쓴 보기를 고르면 돼요.", button="문제 풀러 갈게요"),
        ],
    },
]

add_basic(sentences, 2, [m("This is why", "이것이 ~하는 이유이다"), ": ", m("we feel deeply threatened", "우리는 크게 위협을 느낀다"), " — ",
                         m("a new idea", "새로운 생각이"), " ", m("challenges", "맞설"), " 때."],
          sv_new=sv_step("s2_basic_sv", ["This", "is", "we", "feel"], {"This": "S", "is": "V"},
                         {"we": "그건 why 뒤 덩어리 안의 주어예요.", "feel": "그건 why 뒤 덩어리 안의 동사예요."}, "주어는 This, 동사는 is예요. why 뒤가 그 이유의 내용이에요."),
          meaning_ids=["s2_identity"])
add_basic(sentences, 4, [m("We want to seem trustworthy", "우리는 믿음직하게 보이고 싶다"), ", ", m("reputation management", "평판 관리가"), " ",
                         m("most other concerns", "대부분의 다른 걱정"), "보다 ", m("often overrides", "흔히 앞선다"), "."],
          match_display="We want to seem trustworthy, and reputation management often overrides most other concerns.",
          sv_new=sv_step("s4_basic_sv", ["We", "want", "reputation management", "overrides", "most other concerns"],
                         {"We": "S", "want": "V", "reputation management": "S", "overrides": "V", "most other concerns": "O"}, {},
                         "and 앞은 주어 We, 동사 want예요. and 뒤는 주어 reputation management, 동사 overrides, 목적어 most other concerns예요."),
          meaning_ids=["s4_reputation"])
add_basic(sentences, 6, [m("A human alone in this world", "세상에 홀로인 인간은"), " ", m("faces a lot of difficulty", "많은 어려움을 겪는다"), ", 하지만 ",
                         m("before modern times", "근대 이전에는"), " ", m("being alone in the world", "혼자 있는 것이"), " ",
                         m("was almost certainly a death sentence", "거의 확실한 사형 선고였다"), "."],
          sv_new=sv_step("s6_basic_sv", ["A human", "faces", "being alone in the world", "was"],
                         {"A human": "S", "faces": "V", "being alone in the world": "S", "was": "V"}, {},
                         "but 앞은 주어 A human (alone in this world), 동사 faces예요. but 뒤는 주어 being alone in the world(혼자 있는 것), 동사 was예요."),
          meaning_ids=["s6_alone"])

SENSES = {
    1: [sense("if", "if there was", "만약 ~라면", "가정법 if + 주어 + was")],
    2: [sense("that", "the ones that have become", "(앞 명사를 꾸밈)", "관계대명사 that + 동사")],
    3: [sense("for", "For some ideas", "~에 대해서는", "전치사 for + 명사"),
        sense("that", "the ones that identify", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("as", "as members of a group", "~로서", "전치사 as (자격)"),
        sense("as", "as individuals", "~로서", "전치사 as (자격)"),
        sense("as", "as a member of a tribe", "~로서", "전치사 as (자격)")],
    4: [sense("to", "want to seem", "~하기를", "want + to부정사"), sense("as", "as a trustworthy individual", "~로서", "전치사 as (자격)")],
    6: [sense("but", "but being alone", "하지만", "접속사 but + 주어·동사")],
    7: [sense("so", "So we carry", "그래서", "접속사 so (결과)"), sense("to", "drive to form", "~하려는", "명사 + to부정사")],
    8: [sense("but", "But once you", "하지만", "접속사 but (문장 앞)"),
        sense("so", "so much so", "그렇게 (많이)", "so much so that = 너무 그래서 ~하다"),
        sense("so", "much so that", "그렇게", "so much so that의 둘째 so"),
        sense("that", "so that given", "(so much so that의 일부)", "so much so that + 결과"),
        sense("that", "an outcome that favors", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("that", "one that favors", "(앞 명사를 꾸밈)", "관계대명사 that + 동사"),
        sense("but", "but still favors", "하지만", "접속사 but (대조)"),
        sense("that", "that’s the one", "그것", "지시대명사 that (앞에 말한 결과)")],
}

WORDS = {"sociologist": "사회학자", "said": "말했다", "social": "사회의", "science": "과학", "death": "죽음", "frightening": "무서운",
         "physical": "신체의", "feel": "느끼다", "deeply": "크게, 깊이", "threatened": "위협받은", "idea": "생각", "challenges": "맞서다",
         "ones": "것들", "become": "~이 되다", "part": "일부", "identity": "정체성", "ideas": "생각들", "identify": "규정하다, 알아보다",
         "members": "구성원들", "group": "집단", "reason": "판단하다", "individuals": "개인들", "member": "구성원", "tribe": "부족",
         "want": "원하다", "seem": "~처럼 보이다", "trustworthy": "믿음직한", "reputation": "평판", "management": "관리",
         "individual": "개인", "overrides": "~보다 앞서다", "concerns": "걱정", "mortality": "죽음", "entirely": "완전히",
         "irrational": "비이성적인", "human": "인간", "alone": "혼자인", "faces": "겪다, 마주하다", "lot": "많음", "difficulty": "어려움",
         "modern": "근대의", "times": "시대", "almost": "거의", "certainly": "확실히", "sentence": "선고", "carry": "지니다",
         "innate": "타고난", "drive": "욕구", "form": "만들다", "groups": "집단들", "join": "들어가다", "remain": "남다",
         "oppose": "맞서다", "favoring": "편드는 것", "choice": "선택", "outcome": "결과", "favors": "~에게 유리하다",
         "less": "덜", "yours": "너의 것(집단)", "theirs": "그들의 것(집단)", "pick": "고르다", "given": "~가 주어지면", "once": "일단 ~하면",
         "start": "시작하다", "that’s": "그것은 ~이다", "don’t": "~하지 않다", "brooke": "브룩", "harrington": "해링턴", "e": "E",
         "mc²": "mc²", "sd>pd": "SD>PD"}

STORIES = [
    (4, [sc("문장 1~2", "😨", "SD>PD · identity", "사람은 몸의 죽음보다 무리에서 밀려나는 걸 더 무서워해요"),
         sc("문장 3~4", "👥", "a member of a tribe", "집단과 관련된 생각은 부족의 일원으로 판단하고, 평판을 먼저 챙겨요")]),
    (7, [sc("문장 5~7", "🏕️", "a death sentence · innate drive", "옛날엔 혼자면 죽음이었어요 — 그래서 집단을 만들고 남으려는 욕구를 타고났어요")]),
]

OPTIONS = [
    ("1", "tendency to prefer the group that one identifies with", ["prefer the group", "identifies with"], "자신이 동일시하는 집단을 선호하는 경향", True),
    ("2", "necessity of social isolation to build a reputation", ["social isolation", "reputation"], "평판을 쌓기 위한 사회적 고립의 필요성", False),
    ("3", "ways to ease one’s irrational fear of crowds", ["fear of crowds"], "군중에 대한 비이성적 두려움을 덜어 주는 방법", False),
    ("4", "importance of forming groups with different interests", ["different interests"], "관심사가 다른 집단을 만드는 것의 중요성", False),
    ("5", "tips for staying objective during heated group discussions", ["staying objective"], "열띤 집단 토론 중에 객관성을 지키는 요령", False),
]
exam = {
    "question": "다음 글의 주제로 가장 적절한 것은? [3점]", "sentence": 1, "analysis_first": True,
    "glosses": [g("tendency", "경향"), g("prefer", "선호하다"), g("identifies with", "~와 동일시하다"), g("necessity", "필요성"),
                g("isolation", "고립"), g("ease", "덜어 주다"), g("crowds", "군중"), g("interests", "관심사"), g("objective", "객관적인"),
                g("heated", "열띤")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "칠판에 쌓인 말(social death, tribe, groups, favoring us)을 떠올리며 골라 봐요.",
        "정답이에요! 사람은 무리에서 밀려나는 걸 가장 무서워해서 부족의 일원으로 판단하고, 결국 '우리 편'을 고른대요. 자신이 속한 집단을 선호하는 경향이 주제예요.",
        "정답은 ①이에요. 자신이 속한(동일시하는) 집단을 편드는 경향이 이 글의 주제예요.",
        {"2": "reputation이 나와서 헷갈렸죠. 하지만 글은 고립이 아니라 무리에 남으려는 이야기예요.",
         "3": "군중을 무서워하는 게 아니라 무리에서 밀려나는 걸 무서워해요.",
         "4": "관심사가 다른 집단을 만들자는 이야기는 없어요. 글은 내 집단을 편드는 경향을 설명해요.",
         "5": "토론에서 객관성을 지키는 요령은 글에 없어요."}),
}

lesson = base_lesson(
    ID, source="2024년 3월 고3 전국연합학력평가 영어 23번 (주제, 3점)",
    topic="주제 푸는 법: 되풀이되는 핵심어 모으기 → 글쓴이가 설명하는 현상 잡기 → 글 전체를 한 줄로 → 바꿔 쓴 보기",
    method={"type": "topic", "labels": ["핵심어 모으기", "한 줄로 묶기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-tribe.svg", ("Us", "우리 편"), "↔", ("Them", "그들"),
                                       "사람은 왜 '우리 편'을 고를까?", "2024년 3월 23번 도입 칠판"),
                      "alt": "칠판: Us(우리 편) ↔ Them(그들)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "모두에게 더 좋은 결과보다 '우리 편'에 더 좋은 결과를 고를 때가 있을까요? 이번 글은 사람과 집단의 관계를 다뤄요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "주제 문제는 글에서 되풀이되는 핵심어를 모아 '무엇에 대한 글인지' 한 줄로 묶는 거예요. 칠판에 핵심어를 쌓아 갈게요."}}],
    exam=exam,
    key_words={"passage": [g("sociologist", "사회학자"), g("threatened", "위협받은"), g("identity", "정체성"), g("tribe", "부족"),
                           g("trustworthy", "믿음직한"), g("reputation", "평판"), g("override", "~보다 앞서다"), g("mortality", "죽음"),
                           g("irrational", "비이성적인"), g("death sentence", "사형 선고"), g("drive", "욕구"), g("oppose", "맞서다"),
                           g("favor", "편들다, 유리하게 하다"), g("outcome", "결과")],
               "options": [g("tendency", "경향"), g("identify with", "~와 동일시하다"), g("isolation", "고립"), g("objective", "객관적인")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어 (2026-10-20 선생님). 해설 번역과 대조함:
# reason 판단하다, 따져 생각하다 · sentence (사형) 선고.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. 숙어·문법 요령은 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    3: [tip("reason", "이 글에서는 → 판단하다, 따져 생각하다  ('이유' 아님)", "reason", trap=True)],
    6: [tip("sentence", "이 글에서는 → (사형) 선고  ('문장' 아님)", "death sentence", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="주제 푸는 법",
       chunks={"we": "우리는", "carry": "지니다", "an innate drive": "타고난 욕구", "groups": "집단들", "This": "이것", "is": "~이다",
               "feel": "느끼다", "We": "우리는", "want": "원하다", "reputation management": "평판 관리", "overrides": "~보다 앞서다",
               "most other concerns": "대부분의 다른 걱정", "A human": "인간", "faces": "겪다", "being alone in the world": "세상에 혼자 있는 것",
               "was": "~였다"})
