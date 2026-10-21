"""2026년 9월 모의평가(2027학년도) 31번 레슨 + 대사를 만든다 (빈칸 추론, 2점). 오답률 29%(메가스터디) · Top 10.

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_09_31.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸이 끝에서 둘째 문장(아홉째), 빈칸이 문장의 주어. 정답 ① Belonging(소속감).
선택률(메가스터디 풀서비스 채점): ① 71 ② 16 ③ 6 ④ 3 ⑤ 4 — 많이 고른 오답 ② Confidence(자신감).
② 짐작: 글이 「사람들 앞에서 말하기(speaking in front of others)·발표(presentation)」로 시작해서 자신감을 떠올렸다.
   하지만 글은 자신감이 아니라 집단에서 밀려나는 것(excluded · alienated · exclusion · on your own) 이야기다.
열쇠: 같은 말 — not to be excluded from the group(4) → alienated from the group(5) → exclusion from the group(8) → on your own(10).
   빈칸 문장은 「배제(exclusion)가 생사의 문제였다」(8)를 받아 「____은 생존의 문제였다」 — 배제의 반대 = 집단에 속하기.
   not merely A but also B는 반전이 아니라 A에 B를 더하는 말 → 주장과 같은 쪽.
시험지 아래 *풀이 단어: starve(굶주리다) — 핵심어·단어 체크에서 뺐다(뜻만 둠).
해설지(2027-09-평가원/해설.txt 31번) 해석·Words and Phrases와 대조함 — fire up 작동시키다, alienate 소외시키다, make it 살아남다.
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음). Claude 초안 — 선생님 검토 전.

선생님이 확인할 점
1. 단어 지도는 한 묶음(「집단에서 밀려남」)만 쓴다 — 글에 반대쪽 말이 따로 없어서. 4문장 뒤가 아니라 5문장(같은 말이 두 번째 나온 뒤)에서 처음 연다.
   5·8문장은 학생이 같은 말을 찾아 누른다(찾는 동안 칠판 없음).
2. 빈칸이 「배제」의 반대말이라 s9_fill 힌트·s10_go·문제 안내에 「밀려나는 것의 반대」를 썼다 — 답에 너무 가까운지 봐 주세요.
3. ② Confidence를 고른 이유(말하기·발표 → 자신감)는 추측이다. option_review는 ② 하나만 달았다.
4. 헷갈리는 단어(trap): 5문장 fires up(작동시키다), 10문장 make it(살아남다) — 엑셀(함정단어.xlsx)에는 안 넣었다.
5. 4문장 끊어읽기 roles는 메인 S·V(The explanation / is)만. that절 안 it’s been은 앞 「for why it’s uncomfortable」에도 it’s가 있어
   자리가 어긋날 수 있어 뺐다. 9문장은 주어가 빈칸이라 V(was)만 표시했다.
6. 해석 맞추기는 2문장(짧은 문장)에만.
7. 1문장(질문)·2문장은 가볍게 지나간다. 시험지의 대시(―) 두 개는 「—」로 바꿨고, 그 사이(and thus alienated from the group)는
   재진술 열쇠라 흐리지 않았다.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, tip, groups, rows, sense, sc, m, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_match, add_refers  # noqa: E402

ID = "mopyeong-2027-09-31-public-speaking"

BLANK = "________ was not merely a matter of safety but also of survival."
S = [
    "What stresses you out more than anything?",
    "Perhaps it’s speaking in front of others.",
    "For many, this is so stressful it even has a name: glossophobia.",
    "The explanation for why it’s uncomfortable to have everyone’s eyes on you is probably that, for almost all of our evolution, "
    "it’s been extremely important not to be excluded from the group.",
    "To prepare for what might happen if you are evaluated and socially shamed — and thus alienated from the group — "
    "your brain fires up the stress system and your heart begins to beat harder.",
    "Our natural sensitivity to being evaluated by other people is another example of our brain not being adapted to the modern world.",
    "If we give a bad presentation at work, we are unlikely to lose our job and thus risk starving to death.",
    "But in the world we long ago evolved for, exclusion from the group could be a matter of life and death.",
    BLANK,
    "You simply couldn’t make it on your own.",
]
# 해설지 해석 (2027-09-평가원/해설.txt 31번)
KO = [
    "무엇이 여러분에게 어떤 것보다 더 많은 스트레스를 주는가?",
    "아마도 그것은 사람들 앞에서 말하는 것일 것이다.",
    "많은 사람에게, 이것은 매우 스트레스를 주는 일이어서 심지어 ‘말하기 공포증’이라는 이름을 갖고 있다.",
    "모든 사람의 시선이 여러분에게 놓이게 하는 것이 불편한 이유에 대한 설명은 아마도 우리가 진화해 온 거의 전 기간 동안, "
    "집단으로부터 배제되지 않는 것이 매우 중요했기 때문일 것이다.",
    "여러분이 평가받고 사회적으로 망신을 당하고 그로 인해 집단으로부터 소외되는 경우에 일어날 ‘수도’ 있을 것에 대비하기 위해, "
    "뇌는 스트레스 체계를 작동시키고 심장은 더 세게 뛰기 시작한다.",
    "다른 사람에게 평가받는 것에 대한 우리의 타고난 민감성은 우리의 뇌가 현대 세계에 적응되어 있지 않은 것의 또 다른 예이다.",
    "직장에서 발표를 망친다고 하더라도, 우리가 직장을 잃고 따라서 굶주려 죽을 위험에 처할 것 같지는 않다.",
    "하지만 오래전 우리가 진화했던 세계에서 집단으로부터의 배제는 생사의 문제일 수 있었다.",
    "________은 단순히 안전의 문제만이 아니라 생존의 문제이기도 했다.",
    "여러분은 결코 혼자서는 살아남을 수 없었다.",
]


def board(words, fresh=()):
    """단어 지도 — 한 묶음. 묶음 이름은 읽은 말까지만(집단에서 밀려남), 빈칸 말(소속)은 쓰지 않는다"""
    return groups("같은 말", "집단에서 밀려남", words, fresh=fresh)


W4 = [("excluded from the group", "집단에서 배제됨")]
W5 = W4 + [("alienated from the group", "집단에서 소외됨")]
W8 = W5 + [("exclusion from the group", "집단에서 배제")]
W10 = W8 + [("on your own", "혼자서")]

SIDE_TIP = tip("같은 쪽? 반대 쪽?", "빈칸 문장에 But, However 같은 반전 단서가 있으면 반대 의견이 들어가요. "
               "not merely A but also B는 반전이 아니라 A에 B를 더하는 말이에요.")

BLANK_GLOSSES = [g("not merely", "단순히 ~만이 아니라"), g("merely", "단순히, 그저"),
                 g("a matter of safety", "안전의 문제"), g("matter", "문제"), g("safety", "안전"),
                 g("but also", "~이기도 하다"), g("of survival", "생존의"), g("survival", "생존")]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "low",
        "glosses": [g("What", "무엇"), g("stresses you out", "너에게 스트레스를 주다"), g("stresses", "스트레스를 주다"),
                    g("more than anything", "어떤 것보다 더"), g("anything", "어떤 것"),
                    # 빈칸 문장 (s1 화면에서 띄운다)
                    *BLANK_GLOSSES],
        "roles": [r("What", "S"), r("stresses … out", "V"), r("you", "O")],
        "steps": [
            show("s1_passage", "빈칸은 여기, 아홉째 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "____은 안전의 문제였을 뿐 아니라 생존의 문제이기도 했다", True),
                    ("o1", "____은 안전의 문제였을 뿐, 생존과는 상관없었다", False),
                    ("o2", "____은 안전의 문제도 생존의 문제도 아니었다", False)],
                   "not merely A but also B는 'A일 뿐만 아니라 B이기도 하다'예요. not이 있어도 A를 지우는 말이 아니에요.",
                   why="'not merely a matter of safety but also of survival', 안전의 문제일 뿐만 아니라 생존의 문제이기도 했대요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["________", "not merely", "but also", "survival"],
                   tips=[tip("not merely A but also B", "'A일 뿐만 아니라 B이기도 하다'예요. not only A but also B와 같아요.", "not merely")]),
            show("s1_where", "빈칸은 생존이 걸린 무언가예요. 옛날 사람들에게 무엇이 생존의 문제였는지 생각하며 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                 highlight=["________", "survival"]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("Perhaps", "아마도"), g("it’s", "그것은 ~이다"), g("speaking in front of others", "다른 사람들 앞에서 말하는 것"),
                    g("speaking", "말하는 것"), g("in front of", "~ 앞에서"), g("front", "앞"), g("others", "다른 사람들")],
        "roles": [r("it", "S"), r("’s", "V"), r("speaking in front of others", "C")],
        "steps": [],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "low",
        "glosses": [g("For many", "많은 사람에게"), g("many", "많은 사람"), g("this", "이것"), g("so stressful", "너무 스트레스를 주는"),
                    g("stressful", "스트레스를 주는"), g("even", "심지어"), g("has a name", "이름을 갖고 있다"), g("name", "이름"),
                    g("glossophobia", "말하기 공포증 · 사람들 앞에서 말하는 것을 몹시 두려워하는 것")],
        "slashes": ["For many,", "so stressful"],
        "roles": [r("this", "S"), r("is", "V"), r("so stressful", "C"), r("it", "S"), r("has", "V"), r("a name", "O")],
        "steps": [
            show("s3_note", "사람들 앞에서 말하기는 너무 스트레스라서, glossophobia(말하기 공포증)라는 이름까지 있대요.",
                 highlight=["this", "stressful", "glossophobia"], button="다음 문장",
                 tips=[tip("so ~ (that)", "'너무 ~해서 …하다'예요. so stressful (that) it even has a name에서 that이 빠졌어요.", "so stressful")]),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("The explanation", "설명"), g("explanation", "설명"),
                    g("for why it’s uncomfortable", "왜 불편한지에 대한"), g("uncomfortable", "불편한"),
                    g("to have everyone’s eyes on you", "모든 사람의 시선이 나에게 놓이게 하는 것"),
                    g("everyone’s eyes", "모든 사람의 시선"), g("everyone’s", "모든 사람의"), g("eyes", "눈, 시선"),
                    g("is probably that", "아마 ~이기 때문일 것이다"), g("probably", "아마"),
                    g("for almost all of our evolution", "우리가 진화해 온 거의 전 기간 동안"), g("almost", "거의"),
                    g("evolution", "진화"), g("it’s been extremely important", "매우 중요했다"), g("extremely", "매우"),
                    g("important", "중요한"), g("not to be excluded from the group", "집단으로부터 배제되지 않는 것"),
                    g("excluded", "배제된"), g("group", "집단")],
        "slashes": ["The explanation", "uncomfortable", "on you", "probably that,", "evolution,", "extremely important"],
        "roles": [r("The explanation", "S"), r("is", "V")],
        "modifiers": ["for why it’s uncomfortable to have everyone’s eyes on you"],
        "steps": [
            choice("s4_why",
                   "모든 사람의 시선이 나에게 쏠리면 왜 불편하대요?",
                   [("o0", "진화하는 내내 집단에서 배제되지 않는 것이 매우 중요했기 때문", True),
                    ("o1", "진화하는 내내 집단을 떠나 혼자 서는 것이 매우 중요했기 때문", False),
                    ("o2", "진화하는 내내 남들과 겨뤄 이기는 것이 매우 중요했기 때문", False)],
                   "is probably that 뒤가 이유예요. 'not to be excluded'의 not을 놓치지 말아요.",
                   why="'it’s been extremely important not to be excluded from the group', 집단에서 배제되지 않는 것이 매우 중요했대요.",
                   highlight=["explanation", "important", "not", "excluded"],
                   tips=[tip("not to ~", "to부정사 앞에 not이 오면 '~하지 않는 것'이에요. not to be excluded = 배제되지 않는 것.", "not to be"),
                         tip("it’s been", "it has been을 줄인 말이에요. 여기 it은 뒤의 not to be excluded …를 대신하는 가짜 주어예요.")]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("To prepare for", "~에 대비하기 위해"), g("prepare", "대비하다"), g("what might happen", "일어날 수도 있는 것"),
                    g("happen", "일어나다"), g("if you are evaluated", "평가받는다면"), g("evaluated", "평가받는"),
                    g("socially shamed", "사회적으로 망신을 당한"), g("socially", "사회적으로"), g("shamed", "망신을 당한"),
                    g("thus", "그로 인해, 따라서"), g("alienated from the group", "집단으로부터 소외된"), g("alienated", "소외된"),
                    g("group", "집단"), g("your brain", "너의 뇌"), g("brain", "뇌"), g("fires up", "작동시키다"),
                    g("the stress system", "스트레스 체계"), g("stress", "스트레스"), g("system", "체계"),
                    g("your heart", "너의 심장"), g("heart", "심장"), g("begins to beat harder", "더 세게 뛰기 시작한다"),
                    g("begins", "시작하다"), g("beat", "뛰다"), g("harder", "더 세게")],
        "slashes": ["To prepare", "might happen", "socially shamed", "the group —", "stress system"],
        "roles": [r("you", "S"), r("are evaluated", "V"), r("your brain", "S"), r("fires up", "V"), r("the stress system", "O"),
                  r("your heart", "S"), r("begins to beat", "V")],
        "steps": [
            pick("s5_same", "4문장의 'excluded from the group(집단에서 배제됨)'과 같은 말을 이 문장에서 찾아 눌러 볼까요?",
                 ["evaluated", "socially shamed", "alienated from the group", "the stress system"], ["alienated from the group"],
                 "그건 집단에서 밀려나는 말이 아니에요.",
                 "alienated from the group(집단으로부터 소외된)이에요. 평가받고 망신당하면, 그 결과(and thus) 집단에서 밀려나요.",
                 wrong_by={"evaluated": "평가받는 건 맨 처음 일이에요. 그 뒤 and thus(그로 인해) 어떻게 되는지 봐요.",
                           "socially shamed": "망신당하는 건 그 앞 단계예요. and thus(그로 인해) 뒤를 봐요.",
                           "the stress system": "스트레스 체계는 뇌가 작동시키는 것이에요. 대시(—) 사이를 봐요."},
                 tips=[tip("To ~, 주어 + 동사", "문장 맨 앞 To ~는 '~하기 위해'예요. 진짜 주어는 대시(—) 뒤 your brain이에요.", "To prepare")]),
            show("s5_board", "평가받고 망신당하면 집단에서 소외될까 봐, 뇌가 스트레스 체계를 켜요.",
                 panel=board(W5, fresh=("alienated from the group",)), highlight=["alienated", "fires up"], button="다음 문장"),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("Our natural sensitivity", "우리의 타고난 민감성"), g("natural", "타고난"), g("sensitivity", "민감성"),
                    g("to being evaluated by other people", "다른 사람에게 평가받는 것에 대한"), g("being evaluated", "평가받는 것"),
                    g("evaluated", "평가받는"), g("other people", "다른 사람"), g("is another example", "또 다른 예이다"),
                    g("another example", "또 다른 예"), g("example", "예"), g("our brain", "우리의 뇌"), g("brain", "뇌"),
                    g("not being adapted", "적응되어 있지 않은 것"), g("adapted", "적응된"),
                    g("to the modern world", "현대 세계에"), g("modern", "현대의"), g("world", "세계")],
        "slashes": ["natural sensitivity", "other people", "another example", "not being adapted"],
        "roles": [r("Our natural sensitivity", "S"), r("is", "V"), r("another example", "C")],
        "modifiers": ["to being evaluated by other people"],
        "steps": [
            choice("s6_meaning",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "남의 평가에 예민한 건, 뇌가 아직 현대 세계에 맞춰지지 않았다는 예이다", True),
                    ("o1", "남의 평가에 예민한 건, 뇌가 현대 세계에 잘 맞춰졌다는 예이다", False),
                    ("o2", "남을 평가하는 버릇은 현대 세계가 만든 것이다", False)],
                   "'our brain not being adapted'에서 not을 봐요. 우리 뇌가 현대 세계에 어떻다는 걸까요?",
                   why="'our brain not being adapted to the modern world', 뇌가 현대 세계에 적응되어 있지 않은 것의 예래요.",
                   highlight=["sensitivity", "not being adapted", "modern world"],
                   tips=[tip("our brain not being adapted", "our brain이 뒤 not being adapted의 주어 역할이에요. '뇌가 적응되어 있지 않은 것'으로 읽어요.",
                             "not being adapted")]),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "medium",
        "glosses": [g("give a bad presentation", "발표를 망치다"), g("bad", "나쁜"), g("presentation", "발표"), g("at work", "직장에서"),
                    g("work", "직장"), g("are unlikely to lose our job", "직장을 잃을 것 같지 않다"), g("unlikely", "~할 것 같지 않은"),
                    g("lose", "잃다"), g("job", "직장"), g("thus", "따라서"), g("risk starving to death", "굶주려 죽을 위험에 처하다"),
                    g("risk", "~의 위험에 처하다"), g("starving", "굶주리는 것"), g("death", "죽음")],
        "slashes": ["at work,", "are unlikely", "our job"],
        "roles": [r("we … we", "S"), r("give", "V"), r("a bad presentation", "O"), r("are", "V"), r("unlikely", "C")],
        "steps": [
            show("s7_note", "요즘은 발표를 망쳐도 직장을 잃고 굶어 죽을 일은 거의 없어요.",
                 highlight=["bad presentation", "unlikely", "starving"], button="다음 문장",
                 tips=[tip("be unlikely to ~", "'~할 것 같지 않다'예요. we are unlikely to lose our job = 직장을 잃을 것 같지 않다.", "unlikely")]),
        ],
    },
    {
        "id": 8, "text": S[7], "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("But", "하지만"), g("in the world", "세계에서"), g("the world", "세계"), g("world", "세계"),
                    g("we long ago evolved for", "우리가 오래전 진화했던"), g("long ago", "오래전"), g("evolved", "진화했다"),
                    g("exclusion from the group", "집단으로부터의 배제"), g("exclusion", "배제"), g("group", "집단"),
                    g("could be", "~일 수 있었다"), g("a matter of life and death", "생사의 문제"), g("matter", "문제"),
                    g("life", "삶, 생명"), g("death", "죽음")],
        "slashes": ["the world", "evolved for,", "the group", "could be"],
        "roles": [r("exclusion from the group", "S"), r("could be", "V"), r("a matter of life and death", "C")],
        "modifiers": ["we long ago evolved for"],
        "steps": [
            pick("s8_same", "칠판의 말과 같은 말을 이 문장에서 찾아 눌러 볼까요?",
                 ["the world", "long ago", "exclusion from the group", "a matter of life and death"], ["exclusion from the group"],
                 "그건 집단에서 밀려나는 말이 아니에요.",
                 "exclusion from the group(집단으로부터의 배제)이에요. excluded(배제된)의 명사 꼴이에요.",
                 wrong_by={"the world": "the world는 '세계', 우리가 오래전 진화한 곳이에요.",
                           "long ago": "long ago는 '오래전', 때를 말해요.",
                           "a matter of life and death": "그건 배제가 어떤 문제였는지예요. 무엇이 생사의 문제였는지 봐요."},
                 tips=[tip("the world we evolved for", "world 뒤에 that이 빠지고 꾸밈말이 붙었어요. '우리가 오래전 진화했던 세계'로 읽어요.",
                           "evolved for")]),
            show("s8_board", "요즘과 달리(But), 오래전에는 집단에서 배제되면(exclusion) 생사가 걸렸어요.",
                 panel=board(W8, fresh=("exclusion from the group",)), highlight=["But", "exclusion", "life and death"],
                 button="다음 문장"),
        ],
    },
    {
        "id": 9, "text": BLANK, "model_translation": KO[8], "teaching_value": "high",
        "glosses": [*BLANK_GLOSSES],
        "roles": [r("was", "V")],
        "steps": [
            choice("s9_side",
                   "글쓴이 주장은 '옛날엔 집단에서 밀려나면 생사가 걸렸다'예요. 빈칸 문장은 이 주장과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 — 집단이 생존에 중요했다는 말", True), ("o1", "반대 쪽 — 집단은 생존과 상관없었다는 말", False)],
                   "not merely A but also B는 A에 B를 더하는 말이에요. But이나 However 같은 반전 단서는 없어요.",
                   why="'not merely … but also of survival', 생존의 문제이기도 했대요. 반전 없이 앞 문장의 생사 이야기를 이어 가요.",
                   highlight=["not merely", "but also", "survival"], tips=[SIDE_TIP],
                   point="빈칸 문장 = 앞 문장(배제는 생사의 문제)을 이어 가는 말 = 주장과 같은 쪽"),
            choice("s9_fill",
                   "빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "집단에 속해 있는 것", True), ("o1", "자기 자신을 믿는 것", False), ("o2", "남들과 겨뤄 이기는 것", False)],
                   "칠판의 말은 모두 집단에서 밀려나는 거예요. 밀려나면 생사가 걸렸다면, 생존의 문제였던 건 그 반대예요.",
                   why="집단에서 밀려나면(exclusion) 생사가 걸렸어요. 그러니 생존이 걸린 건 그 반대, 집단 안에 있는 거예요.",
                   highlight=["________", "survival"], panel=board(W8),
                   point="빈칸 = 배제(exclusion)의 반대 = 집단에 속하기"),
        ],
    },
    {
        "id": 10, "text": S[9], "model_translation": KO[9], "teaching_value": "medium",
        "glosses": [g("You", "여러분"), g("simply couldn’t make it", "결코 살아남을 수 없었다"), g("simply", "결코 (부정과 함께)"),
                    g("couldn’t", "~할 수 없었다"), g("make it", "살아남다, 해내다"), g("on your own", "혼자서")],
        "roles": [r("You", "S"), r("couldn’t make it", "V")],
        "steps": [
            show("s10_board", "혼자서는(on your own) 결코 살아남을 수 없었대요. 이것도 집단에서 밀려난 모습이에요.",
                 panel=board(W10, fresh=("on your own",)), highlight=["make it", "on your own"],
                 tips=[tip("simply + not", "부정어와 함께 쓴 simply는 '결코'예요. simply couldn’t = 결코 ~할 수 없었다.", "simply")]),
            show("s10_go", "빈칸은 집단에서 밀려나는 것의 반대, 생존이 걸린 것이에요. 이 말을 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 해석 맞추기 — 짧은 2문장만 (모두에게)
add_match(sentences, 2, [m("Perhaps", "아마도"), " ", m("it’s", "그것은 ~이다"), " ",
                         m("speaking in front of others", "다른 사람들 앞에서 말하는 것"), "."])
# 가리키는 말
add_refers(sentences, 2, {"it’s": "What stresses you out(가장 스트레스를 주는 것)"})
add_refers(sentences, 3, {"this": "speaking in front of others(사람들 앞에서 말하기)"})

SENSES = {
    3: [sense("for", "For many", "~에게", "전치사 for (대상)"),
        sense("so", "so stressful (that) it …", "너무 (~해서)", "so 형용사 (that) ~ = 너무 …해서 ~하다 (that 생략)")],
    4: [sense("for", "for why it’s uncomfortable", "~에 대한", "전치사 for — The explanation for ~ = ~에 대한 설명"),
        sense("to", "to have everyone’s eyes on you", "~하는 것", "가주어 it … to부정사(진주어)"),
        sense("that", "is probably that", "~라는 것", "접속사 that — is의 보어 절"),
        sense("for", "for almost all of our evolution", "~ 동안", "전치사 for (기간)"),
        sense("to", "not to be excluded", "~하는 것", "가주어 it … to부정사(진주어), not to = ~하지 않는 것")],
    5: [sense("to", "To prepare for", "~하기 위해", "to부정사 (목적)"),
        sense("for", "prepare for what might happen", "~에 (대비하다)", "prepare for ~ = ~에 대비하다"),
        sense("if", "if you are evaluated", "만약 ~라면", "조건 if"),
        sense("to", "begins to beat", "~하기 (시작하다)", "begin to + 동사원형 = ~하기 시작하다")],
    6: [sense("to", "sensitivity to being evaluated", "~에 대한", "전치사 to — sensitivity to ~ = ~에 대한 민감성"),
        sense("to", "adapted to the modern world", "~에", "be adapted to ~ = ~에 적응되다")],
    7: [sense("if", "If we give a bad presentation", "~하더라도", "if — 해설은 '망친다고 하더라도'로 옮김"),
        sense("to", "unlikely to lose", "~할 (것 같지 않다)", "be unlikely to + 동사원형 = ~할 것 같지 않다"),
        sense("to", "starving to death", "~에 이르도록", "starve to death = 굶어 죽다")],
    8: [sense("but", "But in the world", "하지만", "접속사 but — 요즘(7문장)과 옛날을 대조"),
        sense("for", "evolved for", "~에 맞춰", "전치사 for — 목적어는 앞의 the world (that 생략)")],
    9: [sense("but", "not merely … but also", "~뿐만 아니라 …도", "not merely A but also B = A일 뿐만 아니라 B이기도")],
}

WORDS = {"what": "무엇", "stresses": "스트레스를 주다", "anything": "어떤 것", "merely": "단순히", "matter": "문제", "safety": "안전",
         "survival": "생존", "perhaps": "아마도", "speaking": "말하는 것", "front": "앞", "others": "다른 사람들", "many": "많은 사람",
         "stressful": "스트레스를 주는", "name": "이름", "explanation": "설명", "uncomfortable": "불편한", "everyone’s": "모든 사람의",
         "eyes": "눈, 시선", "probably": "아마", "almost": "거의", "evolution": "진화", "extremely": "매우", "important": "중요한",
         "excluded": "배제된", "group": "집단", "prepare": "대비하다", "might": "~할 수도 있다", "happen": "일어나다",
         "evaluated": "평가받는", "socially": "사회적으로", "shamed": "망신을 당한", "thus": "따라서", "alienated": "소외된",
         "brain": "뇌", "fires": "작동시키다 · fire up", "stress": "스트레스", "system": "체계", "heart": "심장",
         "begins": "시작하다", "beat": "뛰다", "harder": "더 세게", "natural": "타고난", "sensitivity": "민감성",
         "being": "~인 것", "example": "예", "adapted": "적응된", "modern": "현대의", "world": "세계", "bad": "나쁜",
         "presentation": "발표", "work": "직장", "unlikely": "~할 것 같지 않은", "lose": "잃다", "job": "직장",
         "risk": "~의 위험에 처하다", "starving": "굶주리는 것", "death": "죽음", "long": "오래", "ago": "전에",
         "evolved": "진화했다", "exclusion": "배제", "life": "삶, 생명", "simply": "결코 (부정과 함께)", "couldn’t": "~할 수 없었다",
         "glossophobia": "말하기 공포증", "give": "하다 · give a presentation = 발표하다"}

STORIES = [
    (3, [sc("문장 1~3", "🎤", "speaking in front of others → glossophobia", "사람들 앞에서 말하기는 이름이 붙을 만큼 스트레스예요")]),
    (6, [sc("문장 4", "👀", "everyone’s eyes on you → uncomfortable", "모든 시선이 쏠리면 불편한 건, 진화 내내 집단에서 배제되지 않는 게 중요해서예요"),
         sc("문장 5~6", "💓", "brain fires up the stress system", "평가받고 소외될까 봐 뇌가 스트레스 체계를 켜요 — 뇌가 현대 세계에 맞춰지지 않았어요")]),
]

OPTIONS = [("1", "Belonging", "소속감", True), ("2", "Confidence", "자신감", False), ("3", "Endurance", "인내", False),
           ("4", "Learning", "학습", False), ("5", "Competition", "경쟁", False)]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 9, "analysis_first": True, "wrong_rate": 29, "wrong_rank": 10,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("Belonging", "소속감, 소속"), g("Confidence", "자신감"), g("Endurance", "인내"), g("Learning", "학습"),
                g("Competition", "경쟁")],
    "options": [{"id": o[0], "label": o[1], "keywords": [o[1]], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "빈칸은 집단에서 밀려나는 것의 반대, 생존이 걸린 것이에요. 이 말을 바꿔 쓴 보기를 골라 봐요.",
        "정답이에요! 오래전에는 집단에서 밀려나면(exclusion) 생사가 걸렸어요. 혼자서는 살아남을 수 없었으니, 집단에 속하는 것(Belonging)이 생존의 문제였어요.",
        "정답은 ① Belonging(소속감)이에요. 집단에서 배제되면 생사가 걸렸으니, 집단에 속하는 것이 생존의 문제였어요.",
        {"2": "Confidence(자신감)는 '사람들 앞에서 말하기'에서 떠올리기 쉬워요. 하지만 글은 자신감이 아니라 집단에서 밀려나는 이야기예요.",
         "3": "Endurance(인내)는 글에 없는 이야기예요. 무엇을 참고 견딘다는 말은 나오지 않아요.",
         "4": "Learning(학습)은 글에 없는 이야기예요. 빈칸은 집단과 생존에 관한 말이에요.",
         "5": "Competition(경쟁)은 남과 겨루는 말이에요. 글은 겨루기가 아니라 집단에서 배제되지 않는 게 중요했다는 이야기예요."},
        {"2": review(16,
                     "Confidence(자신감)는 글 첫머리의 '사람들 앞에서 말하기'에서 떠올리기 쉬워요. 하지만 글은 왜 그게 불편한지, 그 이유를 말해요.\n"
                     "이유는 집단에서 밀려나는 것(excluded, alienated, exclusion)이에요. 혼자서는 살아남을 수 없었으니, 생존이 걸린 건 집단에 속하는 거예요.",
                     panel=rows(("4문장", "not to be excluded from the group", "집단에서 배제되지 않는 것이 중요했다", "hl"),
                                ("8문장", "exclusion from the group … life and death", "집단에서 배제되면 생사가 걸렸다", "hl"),
                                ("10문장", "couldn’t make it on your own", "혼자서는 살아남을 수 없었다", "hl")),
                     rank_word="가장 많이 고른")}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(4·8)과 빈칸 뒤(10)만 ──
EMPHASIS = {
    4: ["important", "excluded", "group"],
    8: ["exclusion from the group", "a matter of life and death"],
    10: ["make it", "on your own"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = base_lesson(
    ID, source="2026년 9월 모의평가(2027학년도, 한국교육과정평가원) 영어 31번 (빈칸 추론, 2점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 같은 말 모으기 → 빈칸이 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-public-speaking.svg", ("Speaking", "사람들 앞에서 말하기"), "→", ("Stress", "스트레스"),
                                       "남들 앞에 서면 왜 심장이 뛸까?", "2026년 9월 모의평가 31번 도입 칠판"),
                      "alt": "칠판: Speaking(사람들 앞에서 말하기) → Stress(스트레스)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "사람들 앞에서 말할 때 왜 심장이 빨리 뛸까요? 이번 글은 그 이유를 진화(evolution)에서 찾아요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("stress out", "스트레스를 주다"), g("in front of", "~ 앞에서"), g("glossophobia", "말하기 공포증"),
                           g("uncomfortable", "불편한"), g("evolution", "진화"), g("exclude", "배제하다"), g("prepare for", "~에 대비하다"),
                           g("evaluate", "평가하다"), g("shame", "망신시키다"), g("alienate", "소외시키다"), g("fire up", "작동시키다"),
                           g("sensitivity", "민감성"), g("adapt", "적응시키다"), g("presentation", "발표"),
                           g("be unlikely to", "~할 것 같지 않다"), g("risk", "~의 위험에 처하다"), g("evolve", "진화하다"),
                           g("exclusion", "배제"), g("a matter of life and death", "생사의 문제"),
                           g("not merely A but also B", "A일 뿐만 아니라 B이기도"), g("survival", "생존"),
                           g("make it", "살아남다, 해내다"), g("on one’s own", "혼자서")],
               "options": [g("belonging", "소속감"), g("confidence", "자신감"), g("endurance", "인내"), g("learning", "학습"),
                           g("competition", "경쟁")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함: fire up 작동시키다 · make it 살아남다.
TRAPS = {
    5: [tip("fires up", "이 글에서는 → 작동시키다, 켜다  ('불을 지르다·해고하다' 아님)", "fires up", trap=True)],
    10: [tip("make it", "이 글에서는 → 살아남다, 해내다  ('그것을 만들다' 아님)", "make it", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법")
