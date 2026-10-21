"""2026년 6월 모의평가(2027학년도) 32번 레슨 + 대사를 만든다 (빈칸 추론, 2점). 오답률 52%(메가스터디) · Top 9.

    PYTHONUTF8=1 py scripts/lessons/gen_mopyeong_2027_06_32.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: docs/tutor/templates/blank.md — 빈칸이 마지막 문장. 정답 ② conceal what they mean and feel(자신이 의미하고 느끼는 것을 숨기는).
선택률(메가스터디 풀서비스 채점): ① 7 ② 48 ③ 30 ④ 9 ⑤ 5 — 많이 고른 오답 ③ interpret one’s nonverbal behavior.
③ 짐작: 3문장 「it is easy to misinterpret nonverbal behavior」(오해하기 쉽다)와 빈칸 문장의 difficult가 이어 보여서.
   하지만 3문장은 듣는 사람(listeners)의 일이고, 빈칸은 No wonder(당연하다)로 바로 앞 Freud의 말(아무도 비밀을 지킬 수 없다)을 받는다.
열쇠: 두 쪽 — words 쪽(into words · verbally confirm · lips are silent) ↔ nonverbal 쪽(nonverbal behaviors · conveyed nonverbally ·
chatters with his fingertips · betrayal oozes out). 빈칸 = 말을 안 해도 몸이 속마음을 드러낸다 → 숨기기 어렵다(같은 쪽).
시험지 아래 *풀이 단어: mortal(인간), ooze(스며 나오다), pore(모공) — 핵심어·단어 체크에서 뺐다(뜻만 둠).
해설지(2027-06-평가원/해설.txt 32번) 해석·Words and Phrases와 대조함 — betrayal은 해설대로 「누설, (속마음을) 드러냄」.
규칙 반영: 2026-10-21까지 — S·V 찾기 스텝 없음(svo-finding), 핵심어 나열형 translate 없음, 끊어읽기(slashes·roles·modifiers),
화면 중계 말 없음, 칭찬과 질문 분리(엔진), option_review는 review()(되묻기 없음). Claude 초안 — 선생님 검토 전.

선생님이 확인할 점
1. 「같은 쪽? 반대 쪽?」(s8_side)의 기준을 글쓴이 주장 「말을 안 해도 몸이 속마음을 드러낸다」로 잡았다. No wonder(당연하다)가 결론 표시라서 같은 쪽.
2. ③을 많이 고른 이유(3문장 misinterpret ↔ 빈칸 difficult)는 추측이다. s3_note에서 「이건 듣는 사람의 일」을 미리 짚고, s8_link에서 No wonder가 어느 말을 받는지 3지로 물었다.
3. Freud 인용이 두 문장이라 문장 6·7로 나눴다(6문장 끝에 닫는 따옴표가 없다 — 시험지 그대로).
4. 헷갈리는 단어(trap)는 betrayal(배신 ✕ → 누설, 속마음을 드러냄) 하나만 — 엑셀(함정단어.xlsx)에는 안 넣었다.
   후보: volume(크기, 음량 — 「책의 권」 아님), wavelength(같은 이해 — 「파장」).
5. 해석 맞추기는 넣지 않았다 — 짧은 문장(1·4)은 뜻 질문이나 예시 한 줄과 겹친다. 넣을지 정해 주세요.
6. 4문장 문장 안에 시험지의 물음표(“Do your nods indicate a yes vote?”)가 그대로 있다.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, r, choice, show, pick, tip, groups, rows, sense, sc, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)
from beginner import add_refers  # noqa: E402

ID = "mopyeong-2027-06-32-nonverbal-secret"

BLANK = "No wonder it is difficult for most people to ________ in a face-to-face group discussion."
S = [
    "Speakers don’t always put everything that’s important to them into words.",
    "Very often you can understand a speaker’s meaning by observing their nonverbal behaviors such as a change in a vocal tone "
    "or volume, eye contact, facial expressions and gestures.",
    "As it is easy to misinterpret nonverbal behavior, effective listeners verbally confirm their interpretations of someone’s "
    "nonverbal communication.",
    "A question as simple as “Do your nods indicate a yes vote?” can make sure that everyone is on the same wavelength.",
    "If, as nonverbal research indicates, more than half of a speaker’s meaning is conveyed nonverbally, we are missing a lot of "
    "important information if we fail to “listen” to nonverbal behavior.",
    "Even Freud suggested that “he that has eyes to see and ears to hear may convince himself that no mortal can keep a secret.",
    "If his lips are silent, he chatters with his fingertips; betrayal oozes out of him at every pore.”",
    BLANK,
]
# 해설지 해석 (2027-06-평가원/해설.txt 32번)
KO = [
    "화자가 항상 자신에게 중요한 모든 것을 말로 표현하는 것은 아니다.",
    "매우 흔하게, 목소리 어조나 크기의 변화, 시선 교환, 얼굴 표정, 몸짓과 같은 비언어적 행동을 관찰함으로써 화자가 전달하려는 의미를 이해할 수 있다.",
    "비언어적 행동은 오해하기 쉽기 때문에, 효과적인 청자는 누군가의 비언어적 소통에 대한 자신의 해석을 말로 확인한다.",
    "“고개를 끄덕이신 것이 찬성을 의미하나요?”와 같은 간단한 질문으로 모두가 같은 이해를 공유하고 있다는 것을 분명히 할 수 있다.",
    "비언어적 (소통에 대한) 연구가 가리키듯이, 화자가 의미하고자 하는 것의 절반 이상이 비언어적으로 전달된다면, "
    "우리가 비언어적 행동을 ‘귀담아 듣지’ 않을 때, 많은 중요한 정보를 놓치게 되는 것이다.",
    "심지어 Freud는 “볼 눈과 들을 귀가 있는 사람은 어떤 인간도 비밀을 지킬 수 없다는 것을 스스로 확신하게 될 수 있다.",
    "만약 입술이 침묵하더라도 그는 손가락 끝으로 재잘거리며, 누설(속마음)이 그의 모든 모공에서 스며 나온다.”라고 시사했다.",
    "대면 집단 토론에서 대부분의 사람들이 ________ 것은 당연하다.",
]


def board(left, right, fresh=()):
    """단어 지도 — 묶음 이름은 글에 나온 말(words / nonverbal)까지만. 빈칸 말(숨기다)은 쓰지 않는다"""
    return groups("words와 nonverbal", "words 쪽 (말)", left, "nonverbal 쪽 (말 아닌 것)", right, fresh=fresh, between="↔")


L1 = [("into words", "말로")]
R2 = [("nonverbal behaviors", "비언어적 행동")]
L3 = L1 + [("verbally confirm", "말로 확인")]
R5 = R2 + [("conveyed nonverbally", "비언어적으로 전달")]
L7 = L3 + [("lips are silent", "입은 침묵")]
R7 = R5 + [("chatters with his fingertips", "손끝으로 재잘거림"), ("betrayal oozes out", "속마음이 새어 나옴")]

SIDE_TIP = tip("같은 쪽? 반대 쪽?", "빈칸 문장에 But, However, not 같은 반전 단서가 있으면 반대 의견이 들어가요. "
               "No wonder(당연하다)처럼 앞 내용을 받아 결론을 내면 앞과 같은 쪽 말이 들어가요.")

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("Speakers", "화자 · 말하는 사람"), g("don’t always put", "늘 ~하는 것은 아니다"), g("put", "넣다, 표현하다"),
                    g("everything that’s important to them", "자신에게 중요한 모든 것"), g("important", "중요한"),
                    g("into words", "말로"), g("words", "말"),
                    # 빈칸 문장 (s1 화면에서 띄운다)
                    g("No wonder", "~은 당연하다"), g("wonder", "놀라움, 이상한 일"), g("it is difficult", "어렵다"),
                    g("difficult", "어려운"), g("for most people", "대부분의 사람들이"), g("most people", "대부분의 사람들"),
                    g("in a face-to-face group discussion", "대면 집단 토론에서"), g("face-to-face", "대면의, 얼굴을 마주한"),
                    g("group", "집단"), g("discussion", "토론")],
        "slashes": ["put everything", "important to them"],
        "roles": [r("Speakers", "S"), r("don’t always put", "V"), r("everything", "O")],
        "modifiers": ["that’s important to them"],
        "steps": [
            show("s1_passage", "빈칸은 마지막 문장에 있어요. 이 문장을 잠깐 볼까요?",
                 button="네", before_read=True, show_passage=[BLANK], method=0),
            choice("s1_blank_meaning",
                   "핵심어만 칠해 뒀어요. 이 문장은 무슨 뜻일까요?",
                   [("o0", "대면 토론에서 대부분의 사람들이 ____하기 어려운 것은 당연하다", True),
                    ("o1", "대면 토론에서 대부분의 사람들은 ____하기가 의외로 쉽다", False),
                    ("o2", "대면 토론에서 ____하는 사람이 많다니 놀랍다", False)],
                   "No wonder는 '~은 당연하다'예요. it is difficult for 사람 to ~는 '사람이 ~하기 어렵다'예요.",
                   why="'No wonder', 당연하대요. 'it is difficult for most people to ____', 대부분의 사람들이 ____하기 어렵대요.",
                   before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                   highlight=["No wonder", "difficult", "________", "face-to-face"],
                   tips=[tip("No wonder ~", "'~은 당연하다, 놀랄 일이 아니다'예요. 앞 내용을 받아 결론을 말해요.", "No wonder"),
                         tip("it is difficult for A to B", "'A가 B하기는 어렵다'예요. it은 뒤의 to 덩어리를 가리켜요.", "it is difficult")]),
            show("s1_where", "No wonder(당연하다)는 앞 내용을 받아요. 사람들이 대면 토론에서 무엇을 하기 어려운지 생각하며 처음부터 읽어 봐요.",
                 button="처음부터 읽어 볼게요", before_read=True, display=BLANK, tag="빈칸 문장", method=0,
                 highlight=["No wonder", "difficult"]),
            choice("s1_meaning",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "화자는 중요한 것을 늘 다 말로 하지는 않는다", True),
                    ("o1", "화자는 중요한 것을 절대 말로 하지 않는다", False),
                    ("o2", "화자는 중요한 것을 늘 빠짐없이 말로 한다", False)],
                   "not always는 '늘 ~인 것은 아니다'예요. put A into words는 'A를 말로 표현하다'예요.",
                   why="'don’t always put … into words', 늘 말로 다 하는 것은 아니래요. not always는 '절대 아니다'가 아니에요.",
                   highlight=["don’t always put", "into words"],
                   tips=[tip("not always", "'늘 ~인 것은 아니다'예요. 일부만 부정해요 — '절대 ~ 않다'가 아니에요.", "always"),
                         tip("put A into words", "'A를 말로 표현하다'예요.", "into words")]),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("Very often", "매우 흔하게"), g("can understand", "이해할 수 있다"), g("understand", "이해하다"),
                    g("a speaker’s meaning", "화자가 전달하려는 의미"), g("speaker’s", "화자의"), g("meaning", "의미"),
                    g("by observing", "~을 관찰함으로써"), g("observing", "관찰하는 것"),
                    g("their nonverbal behaviors", "그들의 비언어적 행동"), g("nonverbal behaviors", "비언어적 행동"),
                    g("nonverbal", "비언어적인 · 말이 아닌"), g("behaviors", "행동"), g("such as", "~와 같은"),
                    g("a change in a vocal tone or volume", "목소리 어조나 크기의 변화"), g("change", "변화"),
                    g("vocal", "목소리의"), g("tone", "어조"), g("volume", "(목소리) 크기"), g("eye contact", "시선 교환, 눈 맞춤"),
                    g("contact", "접촉"), g("facial expressions", "얼굴 표정"), g("facial", "얼굴의"), g("expressions", "표정"),
                    g("gestures", "몸짓")],
        "slashes": ["Very often", "a speaker’s meaning", "nonverbal behaviors", "tone or volume,", "eye contact,"],
        "roles": [r("you", "S"), r("can understand", "V"), r("a speaker’s meaning", "O")],
        "steps": [
            choice("s2_how",
                   "화자가 전달하려는 뜻을 무엇으로 이해할 수 있대요?",
                   [("o0", "비언어적 행동을 관찰해서", True),
                    ("o1", "화자에게 다시 물어봐서", False),
                    ("o2", "화자가 쓴 글을 읽어서", False)],
                   "by + -ing는 '~함으로써'예요. by 뒤를 봐요.",
                   why="'by observing their nonverbal behaviors', 말 아닌 행동을 지켜보면 뜻을 알 수 있대요. such as 뒤는 그 예시예요.",
                   highlight=["by observing", "nonverbal behaviors"],
                   tips=[tip("such as ~", "'~와 같은'이에요. 뒤에 예시가 이어져요 — 어조·크기의 변화, 시선, 표정, 몸짓.", "such as")]),
            show("s2_board", "말로 다 하지 않아도(into words), 말 아닌 행동(nonverbal behaviors)으로 뜻을 알 수 있대요.",
                 panel=board(L1, R2, fresh=("into words", "nonverbal behaviors")), highlight=["nonverbal behaviors"], button="다음 문장"),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("As", "~ 때문에"), g("it is easy to misinterpret", "오해하기 쉽다"), g("easy", "쉬운"),
                    g("misinterpret", "오해하다, 잘못 해석하다"), g("nonverbal behavior", "비언어적 행동"), g("nonverbal", "비언어적인"),
                    g("behavior", "행동"), g("effective listeners", "효과적인 청자"), g("effective", "효과적인"),
                    g("listeners", "청자 · 듣는 사람"), g("verbally confirm", "말로 확인하다"), g("verbally", "말로"),
                    g("confirm", "확인하다"), g("their interpretations", "자신의 해석"), g("interpretations", "해석"),
                    g("someone’s nonverbal communication", "누군가의 비언어적 소통"), g("someone’s", "누군가의"),
                    g("communication", "소통")],
        "slashes": ["nonverbal behavior,", "effective listeners", "verbally confirm", "their interpretations"],
        "roles": [r("it", "S"), r("is", "V"), r("easy", "C"), r("effective listeners", "S"), r("verbally confirm", "V"),
                  r("their interpretations", "O")],
        "steps": [
            choice("s3_why",
                   "효과적인 청자는 왜 자기 해석을 말로 확인한대요?",
                   [("o0", "비언어적 행동은 오해하기 쉬워서", True),
                    ("o1", "말로 확인해야 예의라서", False),
                    ("o2", "비언어적 행동은 늘 정확해서", False)],
                   "문장 앞 As는 '~ 때문에'예요. As 뒤를 봐요.",
                   why="'As it is easy to misinterpret nonverbal behavior', 비언어적 행동은 오해하기 쉽기 때문이래요.",
                   highlight=["As", "misinterpret", "verbally confirm"],
                   tips=[tip("As + 문장", "문장 앞 As가 주어·동사를 이끌면 '~ 때문에'일 때가 많아요. As it is easy … = 쉽기 때문에.", "As")]),
            show("s3_note", "몸짓은 오해하기 쉬워서(misinterpret), 듣는 사람(listeners)이 자기 해석을 말로 확인한대요.\n해석하는 건 듣는 사람의 일이에요.",
                 panel=board(L3, R2, fresh=("verbally confirm",)), highlight=["listeners", "verbally confirm"], button="다음 문장"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "low",
        "glosses": [g("A question", "질문"), g("question", "질문"), g("as simple as", "~만큼 간단한"), g("simple", "간단한"),
                    g("Do your nods indicate a yes vote", "고개를 끄덕이신 것이 찬성을 의미하나요"), g("nods", "(고개) 끄덕임"),
                    g("indicate", "나타내다, 의미하다"), g("a yes vote", "찬성 표"), g("vote", "표, 투표"),
                    g("can make sure", "분명히 할 수 있다"), g("make sure", "분명히 하다, 확인하다"), g("everyone", "모두"),
                    g("on the same wavelength", "같은 이해를 공유하는"), g("wavelength", "파장")],
        "slashes": ["A question", "a yes vote?”", "can make sure"],
        "roles": [r("A question", "S"), r("can make sure", "V"), r("everyone", "S"), r("is", "V")],
        "steps": [
            show("s4_note", "예시예요. '고개를 끄덕인 게 찬성이라는 뜻인가요?'처럼 간단한 질문으로 모두 같은 이해를 하고 있는지 확인해요.",
                 highlight=["make sure", "on the same wavelength"], button="다음 문장",
                 tips=[tip("on the same wavelength", "'같은 이해를 공유하는, 생각이 통하는'이에요. 같은 주파수에 맞춰져 있다는 비유예요.",
                           "wavelength")]),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("as nonverbal research indicates", "비언어적 연구가 가리키듯이"), g("nonverbal research", "비언어적 (소통) 연구"),
                    g("research", "연구"), g("indicates", "가리키다"), g("more than half", "절반 이상"), g("half", "절반"),
                    g("of a speaker’s meaning", "화자가 의미하고자 하는 것의"), g("speaker’s", "화자의"), g("meaning", "의미"),
                    g("is conveyed nonverbally", "비언어적으로 전달되다"), g("conveyed nonverbally", "비언어적으로 전달되는"),
                    g("conveyed", "전달된"), g("nonverbally", "비언어적으로"), g("we are missing", "우리는 놓치고 있다"),
                    g("missing", "놓치는"), g("a lot of important information", "많은 중요한 정보"),
                    g("important information", "중요한 정보"), g("important", "중요한"), g("information", "정보"),
                    g("fail to", "~하지 못하다"), g("fail", "실패하다"), g("listen", "귀담아듣다"),
                    g("nonverbal behavior", "비언어적 행동"), g("nonverbal", "비언어적인"), g("behavior", "행동")],
        "slashes": ["If,", "research indicates,", "more than half", "conveyed nonverbally,", "are missing", "important information",
                    "fail to “listen”"],
        "roles": [r("more than half of a speaker’s meaning", "S"), r("is conveyed", "V"), r("we … we", "S"), r("are missing", "V"),
                  r("a lot of important information", "O"), r("fail to “listen”", "V")],
        "steps": [
            choice("s5_meaning",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "뜻의 절반 넘게 말 아닌 것으로 전달되니, 그걸 '듣지' 않으면 중요한 정보를 많이 놓친다", True),
                    ("o1", "몸짓은 뜻을 거의 전달하지 않으니, 말만 잘 들으면 된다", False),
                    ("o2", "말로 확인하면 중요한 정보를 많이 놓친다", False)],
                   "more than half는 '절반 넘게', conveyed nonverbally는 '비언어적으로 전달되는'이에요.",
                   why="'more than half of a speaker’s meaning is conveyed nonverbally', 뜻의 절반 넘게 말 아닌 것으로 전달된대요. 그걸 안 들으면 많이 놓쳐요.",
                   highlight=["more than half", "conveyed nonverbally", "missing"], faded=["as nonverbal research indicates,"],
                   tips=[tip("“listen” (따옴표)", "몸짓은 소리가 아니라서 따옴표를 쳤어요. 몸짓을 '귀담아듣는다'는 비유예요.", "listen")]),
            pick("s5_same", "nonverbal 쪽 말을 이 문장에서 하나 찾아 눌러 볼까요?",
                 ["nonverbal research", "more than half", "conveyed nonverbally", "important information"], ["conveyed nonverbally"],
                 "그건 nonverbal 쪽 말이 아니에요.",
                 "conveyed nonverbally(비언어적으로 전달되는)예요. 뜻의 절반 넘게 말 아닌 것으로 전해져요.",
                 wrong_by={"nonverbal research": "그건 '비언어적 연구', 연구 이름이에요. 뜻이 어떻게 전달되는지 봐요.",
                           "more than half": "more than half는 '절반 넘게', 얼마나인지예요. 어떻게 전달되는지 봐요.",
                           "important information": "important information은 놓치게 되는 '중요한 정보'예요."},
                 faded=["as nonverbal research indicates,"]),
            show("s5_board", "말 아닌 것으로 전달되는 뜻이 절반 넘게 있어요.",
                 panel=board(L3, R5, fresh=("conveyed nonverbally",)), highlight=["conveyed nonverbally"], button="다음 문장",
                 faded=["as nonverbal research indicates,"]),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "high",
        "glosses": [g("Even", "심지어"), g("Freud", "프로이트 · 정신분석학자예요"), g("suggested", "시사했다, 말했다"),
                    g("he that has eyes to see and ears to hear", "볼 눈과 들을 귀가 있는 사람"), g("eyes", "눈"), g("see", "보다"),
                    g("ears", "귀"), g("hear", "듣다"), g("may convince himself", "스스로 확신하게 될 수 있다"),
                    g("convince", "확신시키다, 납득시키다"), g("himself", "그 자신"),
                    g("no mortal can keep a secret", "어떤 인간도 비밀을 지킬 수 없다"), g("no mortal", "어떤 인간도 ~ 않다"),
                    g("mortal", "인간"), g("keep a secret", "비밀을 지키다"), g("secret", "비밀")],
        "slashes": ["suggested that", "ears to hear", "convince himself"],
        "roles": [r("Freud", "S"), r("suggested", "V"), r("he", "S"), r("may convince", "V"), r("himself", "O"), r("no mortal", "S"),
                  r("can keep", "V"), r("a secret", "O")],
        "modifiers": ["that has eyes to see and ears to hear"],
        "steps": [
            choice("s6_secret",
                   "Freud는 볼 눈과 들을 귀가 있는 사람이 무엇을 확신하게 된다고 했대요?",
                   [("o0", "어떤 인간도 비밀을 지킬 수 없다", True),
                    ("o1", "누구나 비밀을 잘 지킬 수 있다", False),
                    ("o2", "눈과 귀가 좋으면 거짓말을 잘한다", False)],
                   "convince himself that 뒤를 봐요. no + 명사는 '어떤 ~도 ~ 않다'예요.",
                   why="'that no mortal can keep a secret', 어떤 인간(mortal)도 비밀을 지킬 수 없대요.",
                   highlight=["convince himself", "no mortal", "keep a secret"],
                   tips=[tip("he that ~", "'~하는 사람'이에요. he that has eyes to see = 볼 눈이 있는 사람.", "he that"),
                         tip("convince oneself that ~", "'~라고 스스로 확신하다'예요.", "convince")]),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("his lips", "그의 입술"), g("lips", "입술"), g("are silent", "침묵하다"), g("silent", "조용한, 말이 없는"),
                    g("he chatters", "그는 재잘거린다"), g("chatters", "재잘거리다"), g("with his fingertips", "손가락 끝으로"),
                    g("fingertips", "손가락 끝"), g("betrayal", "누설 · (속마음을) 드러냄"), g("oozes out of him", "그에게서 스며 나온다"),
                    g("oozes", "스며 나오다"), g("at every pore", "모든 모공에서"), g("every", "모든"), g("pore", "모공")],
        "slashes": ["are silent,", "his fingertips;", "out of him"],
        "roles": [r("his lips", "S"), r("are", "V"), r("silent", "C"), r("he", "S"), r("chatters", "V"), r("betrayal", "S"),
                  r("oozes out of", "V")],
        "steps": [
            choice("s7_meaning",
                   "이 문장은 무슨 뜻일까요?",
                   [("o0", "입을 다물어도 손끝이 말하고, 온몸에서 속마음이 새어 나온다", True),
                    ("o1", "입을 다물면 아무것도 드러나지 않는다", False),
                    ("o2", "말을 많이 하면 비밀이 새어 나간다", False)],
                   "chatters with his fingertips는 '손가락 끝으로 재잘거린다'예요. If는 여기서 '~하더라도'로 읽어요.",
                   why="'If his lips are silent, he chatters with his fingertips', 입이 침묵해도 손끝으로 재잘거린대요. 'betrayal oozes out', 속마음이 새어 나와요.",
                   highlight=["silent", "fingertips", "betrayal", "oozes out"],
                   tips=[tip("세미콜론(;)", "세미콜론(;) 뒤는 앞말을 이어서 더 말해요. 손끝으로 재잘거린다 → 모든 모공에서 새어 나온다.")]),
            show("s7_board", "입(lips)은 말이 없어도 손끝과 온몸이 속마음을 드러내요. 그래서 아무도 비밀을 지킬 수 없대요.",
                 panel=board(L7, R7, fresh=("lips are silent", "chatters with his fingertips", "betrayal oozes out")),
                 highlight=["lips", "fingertips", "betrayal"], button="다음 문장"),
        ],
    },
    {
        "id": 8, "text": BLANK, "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("No wonder", "~은 당연하다"), g("wonder", "놀라움, 이상한 일"), g("it is difficult", "어렵다"),
                    g("difficult", "어려운"), g("for most people", "대부분의 사람들이"), g("most people", "대부분의 사람들"),
                    g("in a face-to-face group discussion", "대면 집단 토론에서"), g("face-to-face", "대면의, 얼굴을 마주한"),
                    g("group", "집단"), g("discussion", "토론")],
        "roles": [r("it", "S"), r("is", "V"), r("difficult", "C")],
        "steps": [
            choice("s8_link",
                   "No wonder(당연하다)는 바로 앞 말을 받아요. 사람들이 하기 어려운 일은 앞의 어느 말과 이어질까요?",
                   [("o0", "no mortal can keep a secret (어떤 인간도 비밀을 지킬 수 없다)", True),
                    ("o1", "it is easy to misinterpret nonverbal behavior (비언어적 행동은 오해하기 쉽다)", False),
                    ("o2", "you can understand a speaker’s meaning (화자의 뜻을 이해할 수 있다)", False)],
                   "No wonder 바로 앞은 Freud의 말이에요. 그 말이 무엇을 할 수 없다고 했는지 떠올려 봐요.",
                   why="No wonder는 바로 앞 Freud의 말을 받아요. 오해하기 쉽다는 건 3문장, 듣는 사람 이야기예요.",
                   highlight=["No wonder", "difficult"], panel=board(L7, R7),
                   point="No wonder = 바로 앞 Freud의 말(no mortal can keep a secret)을 받는 결론"),
            choice("s8_side",
                   "글쓴이 주장은 '말을 안 해도 몸이 속마음을 드러낸다'예요. 빈칸 문장은 이 주장과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 — 몸이 드러내서 하기 어렵다", True), ("o1", "반대 쪽 — 마음먹으면 쉽게 할 수 있다", False)],
                   "No wonder는 앞 내용을 받아 결론을 내요. But이나 not 같은 반전 단서도 없어요.",
                   why="No wonder는 '당연하다', 앞 말의 결론이에요. 반전 단서가 없으니 주장과 같은 쪽이에요.",
                   highlight=["No wonder"], tips=[SIDE_TIP],
                   point="빈칸 = No wonder로 Freud 말(비밀을 못 지킨다)의 결론 = 주장과 같은 쪽"),
            choice("s8_fill",
                   "빈칸에는 어떤 말이 와야 할까요?",
                   [("o0", "남의 몸짓을 정확히 해석하는", False),
                    ("o1", "남의 말에 귀 기울이는 척하는", False),
                    ("o2", "자기 속마음을 감추는", True)],
                   "입을 다물어도 몸이 속마음을 드러내요. 그렇다면 사람들이 하기 어려운 일은 무엇일지 생각해 봐요.",
                   why="아무도 비밀을 지킬 수 없으니, 사람들이 하기 어려운 건 속마음을 감추는 일이에요. 해석은 듣는 사람(3문장)의 일이에요.",
                   highlight=["difficult", "________"]),
            show("s8_go", "빈칸은 주장과 같은 쪽, 몸이 다 드러내서 하기 어려운 일이에요. 이 말을 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요"),
        ],
    },
]

# 가리키는 말
add_refers(sentences, 2, {"their nonverbal behaviors": "a speaker(화자)의 비언어적 행동"})
add_refers(sentences, 3, {"their interpretations": "effective listeners(효과적인 청자)의 해석"})

SENSES = {
    1: [sense("that", "that’s important", "~한 (모든 것)", "관계대명사 that — everything을 꾸민다 (that’s = that is)"),
        sense("to", "important to them", "~에게", "전치사 to (important to ~ = ~에게 중요한)")],
    2: [sense("as", "such as", "~와 같은", "such as = ~와 같은 (예시)")],
    3: [sense("as", "As it is easy", "~ 때문에", "접속사 as (이유)"),
        sense("to", "to misinterpret", "~하는 것은", "가주어 it … to부정사(진주어)")],
    4: [sense("as", "as simple", "~만큼", "as 형용사 as ~ = ~만큼 …한 (앞 as)"),
        sense("as", "simple as “Do your nods …”", "~만큼", "as ~ as의 뒤 as — 비교 대상 앞"),
        sense("that", "make sure that", "~라는 것을", "접속사 that — make sure의 목적어 절")],
    5: [sense("if", "If, as …", "만약 ~라면", "조건 if"),
        sense("as", "as nonverbal research indicates", "~하듯이", "접속사 as — 연구가 가리키듯이"),
        sense("if", "if we fail", "만약 ~라면", "조건 if"),
        sense("to", "fail to “listen”", "~하지 (못하다)", "fail to + 동사원형 = ~하지 못하다"),
        sense("to", "“listen” to nonverbal behavior", "~을 (귀담아듣다)", "listen to ~ = ~을 귀담아듣다")],
    6: [sense("that", "suggested that", "~라고", "접속사 that — suggested의 목적어 절"),
        sense("that", "he that has", "~하는 (사람)", "관계대명사 that — he that ~ = ~하는 사람"),
        sense("to", "eyes to see", "~할 (눈)", "명사 + to부정사 (eyes to see = 볼 눈)"),
        sense("to", "ears to hear", "~할 (귀)", "명사 + to부정사 (ears to hear = 들을 귀)"),
        sense("that", "himself that", "~라고", "접속사 that — convince oneself that ~ = ~라고 확신하다")],
    7: [sense("if", "If his lips are silent", "~하더라도", "if — 해설은 '침묵하더라도'로 옮김")],
    8: [sense("for", "for most people", "~가 (하기)", "가주어 it … for 사람 to ~ — for 뒤가 to의 행동을 하는 사람"),
        sense("to", "to ________", "~하는 것은", "가주어 it … to부정사(진주어)"),
        sense("to", "face-to-face", "(얼굴을) 마주", "face-to-face = 대면의 (한 덩어리 형용사)")],
}

WORDS = {"speakers": "화자", "don’t": "~하지 않다", "always": "늘", "put": "넣다, 표현하다", "everything": "모든 것",
         "that’s": "그것은 ~이다", "important": "중요한", "words": "말", "wonder": "놀라움", "difficult": "어려운",
         "most": "대부분의", "face-to-face": "대면의", "group": "집단", "discussion": "토론", "often": "흔히",
         "understand": "이해하다", "speaker’s": "화자의", "meaning": "의미", "observing": "관찰하는 것", "nonverbal": "비언어적인",
         "behaviors": "행동", "behavior": "행동", "change": "변화", "vocal": "목소리의", "tone": "어조", "volume": "(목소리) 크기",
         "eye": "눈", "contact": "접촉", "facial": "얼굴의", "expressions": "표정", "easy": "쉬운", "misinterpret": "오해하다",
         "effective": "효과적인", "listeners": "청자", "verbally": "말로", "confirm": "확인하다", "interpretations": "해석",
         "someone’s": "누군가의", "communication": "소통", "question": "질문", "simple": "간단한", "nods": "끄덕임",
         "indicate": "의미하다", "yes": "찬성", "vote": "표", "sure": "확실한 · make sure = 분명히 하다", "everyone": "모두",
         "wavelength": "파장", "research": "연구", "indicates": "가리키다", "half": "절반", "conveyed": "전달된",
         "nonverbally": "비언어적으로", "missing": "놓치는", "lot": "많음 · a lot of = 많은", "information": "정보", "fail": "실패하다",
         "listen": "귀담아듣다", "eyes": "눈", "see": "보다", "ears": "귀", "hear": "듣다", "convince": "확신시키다",
         "himself": "그 자신", "mortal": "인간", "secret": "비밀", "lips": "입술", "silent": "조용한", "chatters": "재잘거리다",
         "fingertips": "손가락 끝", "oozes": "스며 나오다", "pore": "모공", "every": "모든", "him": "그"}

STORIES = [
    (4, [sc("문장 1~2", "🗣️", "not always into words → nonverbal behaviors", "말로 다 하지 않아도 몸짓·표정으로 뜻을 알 수 있어요"),
         sc("문장 3~4", "❓", "easy to misinterpret → verbally confirm", "몸짓은 오해하기 쉬워서 듣는 사람이 말로 확인해요")]),
    (6, [sc("문장 5", "📊", "more than half … conveyed nonverbally", "뜻의 절반 넘게 말 아닌 것으로 전달돼요"),
         sc("문장 6", "🤫", "no mortal can keep a secret", "Freud — 어떤 인간도 비밀을 지킬 수 없다")]),
]

OPTIONS = [("1", "pretend to pay attention to others", "다른 사람에게 주의를 기울이는 척하는", False, ["pretend", "pay attention"]),
           ("2", "conceal what they mean and feel", "자신이 의미하고 느끼는 것을 숨기는", True, ["conceal", "mean and feel"]),
           ("3", "interpret one’s nonverbal behavior", "누군가의 비언어적 행동을 해석하는", False, ["interpret", "nonverbal behavior"]),
           ("4", "maintain the nonverbal communication", "비언어적 의사소통을 유지하는", False, ["maintain"]),
           ("5", "encounter a chance to understand others", "다른 사람을 이해할 기회를 접하는", False, ["encounter", "chance"])]
exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오.",
    "underline": "________", "sentence": 8, "analysis_first": True, "wrong_rate": 52, "wrong_rank": 9,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("pretend", "~인 척하다"), g("pay attention to", "~에 주의를 기울이다"), g("conceal", "숨기다"),
                g("what they mean and feel", "자신이 의미하고 느끼는 것"), g("interpret", "해석하다"),
                g("one’s nonverbal behavior", "누군가의 비언어적 행동"), g("maintain", "유지하다"),
                g("encounter", "접하다, 마주치다"), g("chance", "기회")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[4], "ko": o[2], **({"correct": True} if o[3] else {})} for o in OPTIONS],
    "brief": exam_brief(
        "몸이 속마음을 다 드러내서 사람들이 하기 어려운 일, 그 말을 바꿔 쓴 보기를 골라 봐요.",
        "정답이에요! 입을 다물어도 손끝과 온몸이 속마음을 드러내요. 그러니 대면 토론에서 자신이 의미하고 느끼는 것을 숨기기(conceal) 어려운 건 당연해요.",
        "정답은 ② conceal what they mean and feel(자신이 의미하고 느끼는 것을 숨기는)이에요. 아무도 비밀을 지킬 수 없으니, 속마음을 숨기기 어려워요.",
        {"1": "pretend to pay attention(주의를 기울이는 척하기)은 글에 없는 이야기예요. 글은 속마음이 몸으로 드러난다는 이야기예요.",
         "3": "interpret(해석하다)은 3문장, 듣는 사람 이야기예요. 빈칸은 No wonder로 Freud의 말(비밀을 못 지킨다)을 받아요.",
         "4": "maintain(유지하다)은 글에 없는 말이에요. 비언어적 소통은 일부러 유지하는 게 아니라 저절로 드러나요.",
         "5": "encounter a chance(기회를 접하다)는 글과 상관없어요. 빈칸은 사람들이 하기 어려운 일이에요."},
        {"3": review(30,
                     "interpret(해석하다)은 3문장 'easy to misinterpret'(오해하기 쉽다)에서 떠오르는 말이에요. 하지만 그건 듣는 사람(listeners)의 일이에요.\n"
                     "No wonder(당연하다)는 바로 앞 Freud의 말을 받아요. 아무도 비밀을 지킬 수 없으니, 어려운 일은 속마음을 숨기는 거예요.",
                     panel=rows(("3문장", "effective listeners verbally confirm", "해석은 듣는 사람이 말로 확인", "hl2"),
                                ("6문장", "no mortal can keep a secret", "어떤 인간도 비밀을 지킬 수 없다", "hl"),
                                ("빈칸 문장", "No wonder it is difficult …", "그러니 ____하기 어려운 건 당연하다", "hl")),
                     rank_word="가장 많이 고른")}),
}

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 지문당 10개 안팎, 주장이 서는 문장(5·6·8)만 ──
EMPHASIS = {
    5: ["more than half", "conveyed nonverbally", "missing"],
    6: ["no mortal", "keep a secret"],
    7: ["silent", "fingertips", "betrayal"],
    8: ["No wonder", "difficult"],
}
for _s in sentences:
    for _c in _s.get("slashes", []):
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

lesson = base_lesson(
    ID, source="2026년 6월 모의평가(2027학년도, 한국교육과정평가원) 영어 32번 (빈칸 추론, 2점)",
    topic="빈칸 푸는 법: 빈칸 문장부터 → 처음부터 읽으며 같은 말 모으기 → 빈칸이 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기",
    method={"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-nonverbal-secret.svg", ("Words", "말"), "+", ("Nonverbal", "말 아닌 행동"),
                                       "말하지 않아도 뜻이 전해질까?", "2026년 6월 모의평가 32번 도입 칠판"),
                      "alt": "칠판: Words(말) + Nonverbal(말 아닌 행동)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "말하지 않아도 뜻이 전해질까요? 이번 글은 말(words)과 말 아닌 행동(nonverbal behavior) 이야기예요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}}],
    exam=exam,
    key_words={"passage": [g("put A into words", "A를 말로 표현하다"), g("observe", "관찰하다"), g("nonverbal", "비언어적인"),
                           g("vocal", "목소리의"), g("tone", "어조"), g("eye contact", "시선 교환"), g("facial expression", "얼굴 표정"),
                           g("gesture", "몸짓"), g("misinterpret", "오해하다"), g("verbally", "말로"), g("confirm", "확인하다"),
                           g("interpretation", "해석"), g("indicate", "가리키다, 의미하다"),
                           g("be on the same wavelength", "같은 이해를 공유하다"), g("convey", "전달하다"),
                           g("fail to", "~하지 못하다"), g("convince", "확신시키다, 납득시키다"), g("chatter", "재잘거리다"),
                           g("fingertip", "손가락 끝"), g("betrayal", "누설, (속마음을) 드러냄"), g("no wonder", "~은 당연하다"),
                           g("face-to-face", "대면의")],
               "options": [g("pretend", "~인 척하다"), g("pay attention to", "~에 주의를 기울이다"), g("conceal", "숨기다"),
                           g("interpret", "해석하다"), g("maintain", "유지하다"), g("encounter", "접하다, 마주치다")]},
    sentences=sentences)

# 헷갈리는 단어(trap) — 평소 아는 뜻과 이 글의 뜻이 다른 단어. 해설 번역과 대조함: betrayal 누설, (속마음을) 드러냄.
TRAPS = {
    7: [tip("betrayal", "이 글에서는 → 누설, (속마음을) 드러냄  ('배신' 아님)", "betrayal", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

finish(ID, lesson, senses=SENSES, words=WORDS, stories=STORIES, topic_intro="빈칸 푸는 법")
