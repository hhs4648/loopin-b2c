"""2022년 3월 고3 29번 레슨 + 대사를 만든다 (어법, 3점). 오답률 67.0% · Top 1.

    python3 scripts/lessons/gen_moeui_2022_03_29.py   (→ npm run policy:copy stamp <id> → npm run build)

틀: 어법 유형(틀 문서 없음 — 2024년 3월 29번 선례를 따름, 둘 다 Claude 초안).
푸는 법: 어법은 문법만 보면 된다 — S·V 찾기 없이 밑줄 문법 위주로 자세히 (2026-10-20 선생님).
①nor는 뜻 → 도치 → 동사 둘이면 맨 앞만 → 앞은 부정문 → 바로 연습(객관식) → 「더 연습할까요?」(보충학습실 drill).
정답이 아닌 밑줄은 「맞아요」로 짚어 밑줄 점검표(rows)에 쌓고, 정답 밑줄(②)은 **구조만** 확인하고
맞다/틀리다는 문제에서 고르게 한다 (2024년 3월 29번·어휘 30번과 같게).

정답 ② as → than (more … than 비교 구문). 해설지: "more가 사용된 비교 구문이므로 as를 than으로 바꿔야 한다."
많이 고른 오답 ③ 24%(동사가 둘로 보인다) · ④ 23%(considered에서 to be가 멀다) — 둘 다 option_review로.
오답률·선택률은 메가스터디 풀서비스 채점 기준이라 EBS 공개 오답률과 다를 수 있다(wrong_rate_source).
primer·lyre·coarse는 시험지 아래 *로 풀어 준 말이라 핵심어·단어 체크에서 뺐다.
해설지 해석과 대조함 (content/tutor/exam-source/2022-03-고3/해설.txt).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_kit import (g, choice, show, sv, tip, rows, sense, topic_svg,  # noqa: E402
                      base_lesson, exam_brief, review, finish)

ID = "moeui-2022-03-29-greek-music"

S = [
    "We don’t know what ancient Greek music sounded like, because there are no examples of it in written or notated form, "
    "nor ①has it survived in oral tradition.",
    "Much of it was probably improvised anyway, within certain rules and conventions.",
    "So we are forced largely to guess at its basis from the accounts of writers such as Plato and Aristotle, who were generally "
    "more concerned with writing about music as a philosophical and ethical exercise ②as with providing a technical primer on its practice.",
    "It seems Greek music was predominantly a vocal form, ③consisting of sung verse accompanied by instruments such as the lyre "
    "or the plucked kithara (the root of ‘guitar’).",
    "In fact, Plato considered music in which the lyre and flute played alone and not as the accompaniment of dance or song "
    "④to be ‘exceedingly coarse and tasteless’.",
    "The melodies seem to have had a very limited pitch range, since the instruments ⑤generally span only an octave, "
    "from one E (as we’d now define it) to the next.",
]
KO = [
    "우리는 고대 그리스 음악이 어떤 소리를 냈는지 알지 못하는데, 그 이유는 그것이 기록되거나 악보에 적힌 형태로 되어 있는 사례가 없고, 구전으로도 살아남지 못했기 때문이다.",
    "어쨌든 그것의 대부분은 아마도 특정 규칙과 관례 내에서 즉흥적으로 연주되었을 것이다.",
    "그래서 우리는 주로 플라톤과 아리스토텔레스와 같은 작가들의 설명으로부터 그것의 토대를 추측할 수밖에 없는데, 그들은 실제에 대한 기술적인 입문서를 "
    "제공하는 것보다 철학적이고 윤리적인 실천으로서의 음악에 대해 글을 쓰는 것에 대체로 더 관심이 있었다.",
    "그리스 음악은 대개 성악 형식이었고, 수금이나 퉁기는 키타라('기타'의 뿌리)와 같은 악기의 반주에 의해 노래되는 운문으로 구성되었던 것으로 보인다.",
    "사실, 플라톤은 춤이나 노래의 반주로서가 아닌 수금과 피리만 연주되는 음악을 '매우 조잡하고 무미건조하다'고 여겼다.",
    "그 선율은 매우 제한된 음역을 가지고 있었던 것으로 보이는데, 왜냐하면 그 악기들은 (우리가 그것을 현재 정의하는 대로) 한 E에서 다음 E까지 단지 한 옥타브에만 걸쳐 있기 때문이다.",
]
UNDER = ["①has", "②as", "③consisting", "④to be", "⑤generally"]

# 밑줄 점검표 — 맞다고 확인한 밑줄만 쌓는다 (정답 밑줄 ②는 끝까지 넣지 않는다)
NAMES = {
    "1": ("① 맞음", "nor has it survived", "부정어 nor가 앞에 와서 조동사 + 주어 순서"),
    "3": ("③ 맞음", "a vocal form, consisting of", "접속사 없이 이어 붙이는 분사(-ing)"),
    "4": ("④ 맞음", "considered music … to be", "consider + 목적어 + to be + 보어"),
    "5": ("⑤ 맞음", "generally span", "동사 span을 꾸미는 부사 generally"),
}


def check(*done):
    return rows(*[(NAMES[d][0], NAMES[d][1], NAMES[d][2], "hl") for d in done])


# ① nor 칠판 — 설명이 한 줄씩 쌓인다
NOR_ROWS = [
    ("뜻", "nor", "~도 아니다"),
    ("도치", "완성된 문장, nor + 동사 + 주어", "주어·동사 순서를 바꾼다"),
    ("동사 둘", "has survived → nor has it survived", "맨 앞 동사 하나만 앞으로"),
    ("앞 문장", "nor 앞은 늘 부정문", "there are no examples …"),
]


def nor_board(n):
    return rows(*[(a, b, c, "hl" if i == n - 1 else None) for i, (a, b, c) in enumerate(NOR_ROWS[:n])])


# ① 바로 연습 — 두 문장을 nor로 합치기 (객관식). 보기마다 틀린 이유가 다르다
nor_try = choice(
    "s1_nor_try", "두 문장을 nor로 합쳐 봐요. 빈칸에 알맞은 것은 무엇일까요?",
    [("o0", "has she read", True), ("o1", "she has read", False), ("o2", "has read she", False)],
    "nor 뒤에는 동사가 주어 앞으로 가요. 동사가 둘이면 맨 앞 하나만요.",
    praise="맞아요! has만 she 앞으로 나와서 nor has she read예요.",
    praise_alone=True,
    panel=rows(("문장 1", "I haven’t read the book.", "나는 그 책을 읽지 않았다"),
               ("문장 2", "She hasn’t read the book.", "그녀도 그 책을 읽지 않았다"),
               ("합치기", "I haven’t read the book, nor ___ ___ ___ the book.", None, "hl")),
    panel_below=True,
    point="nor + 동사 + 주어(도치), 동사가 둘이면 맨 앞만 → nor has she read",
)
# 「네」면 「nor / so」 묶음(기본 개념 · nor vs so · nor vs neither · 작문, 각 10문제)을 보충학습실에 담는다
nor_more = show("s1_nor_more", "이 문법을 나중에 좀 더 연습할까요?", practice="nor-so", button="네")
nor_more["brief"]["saved"] = "보충학습실에 담아 뒀어요."

nor_try["brief"]["feedback"] = {
    "o1": "nor 뒤에는 주어와 동사 순서가 바뀌어요(도치). she has가 아니라 has she예요.",
    "o2": "맨 앞 동사 has 하나만 주어 앞으로 가요. read는 she 뒤에 남아서 has she read예요.",
}


def r(text, role):
    """끊어읽기를 켜면 같이 보이는 S·V·O·C — 절 안의 것도 같은 진하기로"""
    return {"text": text, "role": role}


def board(table, n):
    """칠판 표 — 설명이 한 줄씩 쌓이고, 방금 쌓인 줄을 칠한다"""
    return rows(*[(a, b, c, "hl" if i == n - 1 else None) for i, (a, b, c) in enumerate(table[:n])])


def explain(id, say, table, n, highlight, button="네", **extra):
    return show(id, say, highlight=highlight, panel=board(table, n), panel_below=True, button=button, **extra)


def practice_try(id, ask, panel_rows, options, hint, praise, point, feedback):
    """바로 연습 — 객관식, 보기마다 틀린 이유가 다르다"""
    st = choice(id, ask, options, hint, praise=praise, praise_alone=True, panel=rows(*panel_rows), panel_below=True, point=point)
    st["brief"]["feedback"] = feedback
    return st


def practice_offer(id, drill):
    """「네」면 연습할 문법으로 남겨 보충학습실에서 drill 10문제 (content/tutor/grammar-drills/<drill>.json)"""
    st = show(id, "이 문법을 나중에 좀 더 연습할까요?", practice=drill, button="네")
    st["brief"]["saved"] = "보충학습실에 담아 뒀어요."
    return st


def judge(id, label, why, board_panel, done):
    """설명·연습 끝에 「그럼 보기 ①은 어법상 맞을까요, 틀릴까요?」 — 알려 주지 않고 고르게 한다 (2026-10-20 선생님).
    맞히면 칭찬만 한 화면, 그 뒤에 「더 연습할까요?」. 고른 뒤 밑줄 점검표(맞은 밑줄)가 칠판에 남는다"""
    num, word, eun = label  # eun: 번호에 붙는 조사 (①은 · ④는)
    return choice(
        id, f"그럼 보기 {num}{eun} 어법상 맞을까요, 틀릴까요?",
        [("o0", "맞는 표현", True), ("o1", "틀린 표현", False)],
        why, praise=f"맞아요! 보기 {num}{eun} 어법상 문제가 없어요.",
        why=f"{why} 그래서 보기 {num}{eun} 어법상 맞아요.",
        praise_alone=True, panel=board_panel, panel_below=True, panel_after=check(*done),
        point=f"보기 {num}{word} 어법상 맞음")


# ③ consisting — 이 문제가 묻는 것(동사냐 분사냐) → 동사·분사 표 → 암기(한 문장에 동사 하나) → 「맞을까요?」
#   → 해설(주어·동사 두 쌍, 접속사 없음 → 분사) → 분사구문 이름 → [심화] consisted가 안 되는 이유 (2026-10-20 선생님).
#   보기에 없는 consisted를 먼저 꺼내지 않는다 — 학생은 「consisted가 왜 나오지?」 한다
VERB_PART = rows(("동사", "~하다", "현재 learn · 과거 learned / wrote · 미래 will learn · 진행 is learning"),
                 ("분사", "~하는 · ~된", "현재분사 learning · 과거분사(p.p.) learned / written"))
CONS_RULE = ("암기", "한 문장에 동사는 하나", "and · or · when 같은 접속사가 있어야만 동사를 더 쓸 수 있다")
CONS_WHY = rows(("주어·동사 1", "It seems", None), ("주어·동사 2", "Greek music was", "(사이의 that은 생략)"),
                ("접속사", "없음 → 동사 ✕", None), ("③", "consisting (분사)", None, "hl"))
cons_steps = [
    show("s4_cons_ask", "보기 ③consisting부터 볼게요. 이번 밑줄은 '동사'가 와야 하는지 '분사'가 와야 하는지 고르는 문제예요.",
         highlight=["consisting"], button="네"),
    {**show("s4_cons_table", "동사와 분사의 차이는 표와 같아요.", panel=VERB_PART, panel_below=True,
            button="알겠어요", practice="participle-ing", practice_button="나중에 보충학습실에서 더 깊이 공부할게요"),
     "brief": {"say": "동사와 분사의 차이는 표와 같아요.", "saved": "보충학습실에 담아 뒀어요."}},
    show("s4_cons_rule", "꼭 외워 둘 것이 있어요. 한 문장에 동사는 하나예요. and, or, when 같은 접속사가 있어야만 동사를 더 쓸 수 있어요.",
         panel=rows(CONS_RULE + ("hl",)), panel_below=True, button="알겠어요"),
    judge("s4_cons_judge", ("③", "consisting", "은"), "접속사 없이 동사가 또 올 수는 없어서, 분사가 와야 하는 자리예요.",
          rows(CONS_RULE), ("1", "3")),
    show("s4_cons_why", "여기서는 이미 It seems, Greek music was라는 주어·동사가 있고, 그 뒤로 접속사가 없어요. "
         "그래서 동사는 또 못 오고, 분사인 consisting이 와야 해요.",
         highlight=["It seems", "was", "consisting"], panel=CONS_WHY, panel_below=True, button="다음",
         slash_on=True),  # 「주어·동사가 이미 있어요」 — 끊어읽기(S·V)를 저절로 켜서 보인다
    show("s4_cons_phrase", "이 문장처럼 '완성된 문장 + 콤마(,) + 분사'일 때, 콤마 뒷부분을 '분사구문'이라고 불러요.",
         highlight=["consisting of sung verse"], button="알겠어요", detail_button="심화: consisted는 왜 안 될까요?",
         # 공식 한 줄 + 지문 속 예 — 콤마 뒷부분에 밑줄, 아래에 「분사구문」 (2026-10-20 선생님)
         panel={"kind": "formula", "lines": [
             {"parts": [{"text": "S + V …"}, {"text": ","}, {"text": "-ing 또는 p.p. …", "under": "분사구문"}]},
             {"example": True, "parts": [{"text": "Greek music was a vocal form"}, {"text": ","},
                                         {"text": "consisting of sung verse …", "under": "분사구문"}]}]},
         panel_below=True),
    {**show("s4_cons_deep", "consisted는 동사로도, 과거분사(p.p.)로도 볼 수 있어요. 동사라면 한 문장에 동사가 또 오는 거라 안 되고, "
            "p.p.라면 '~된'이라는 수동인데 consist of는 수동으로 쓰지 않는 말이라 안 돼요. 그래서 능동인 consisting이에요.",
            highlight=["consisting"], button="알겠어요"), "optional_of": "s4_cons_phrase"},
    practice_offer("s4_cons_more", "participle-ing"),
]

# ④ to be — 이 밑줄이 묻는 것(consider와 짝이 맞나) → 짝 표 → 암기(목적어가 길어도 짝은 그대로) → 「맞을까요?」
#   → 해설(목적어 music + 긴 꾸밈 → to be) → 이름(5형식·목적격 보어) → [심화] being·is는 왜 안 될까 (2026-10-20 선생님, ③과 같은 틀)
TOBE_TABLE = rows(("to be와 짝", "consider · believe · find + A + to be + B", "A를 B라고 여기다 (to be는 빼도 된다)"),
                  ("as와 짝", "regard · see · think of + A + as + B", "A를 B로 여기다"))
TOBE_RULE = ("헷갈리는 이유", "목적어가 길다", "music을 꾸미는 in which 절이 중간에 들어와서")
TOBE_WHY = rows(("동사", "considered", None), ("A (목적어)", "music [in which … song]", "[ ]는 music을 꾸미는 긴 설명"),
                ("to be + B", "to be ‘exceedingly coarse and tasteless’", "A를 B라고 여겼다", "hl"))
tobe_steps = [
    show("s5_tobe_ask", "보기 ④to be를 볼게요. 이번 밑줄은 앞의 considered와 짝이 맞는 모양인지 고르는 문제예요.",
         highlight=["considered", "to be"], button="네"),
    {**show("s5_tobe_table", "'A를 B라고 여기다'라는 동사는 짝이 정해져 있어요. 표처럼 to be와 짝인 것, as와 짝인 것이 있어요.",
            panel=TOBE_TABLE, panel_below=True, button="알겠어요", practice="consider-to-be",
            practice_button="나중에 보충학습실에서 더 깊이 공부할게요"),
     "brief": {"say": "'A를 B라고 여기다'라는 동사는 짝이 정해져 있어요. 표처럼 to be와 짝인 것, as와 짝인 것이 있어요.",
               "saved": "보충학습실에 담아 뒀어요."}},
    # 「꼭 외워 둘 것이 있어요」 대신 왜 헷갈리는지부터 (2026-10-20 선생님) — 끊어읽기를 켜서 O와 [ ]를 보여 준다
    show("s5_tobe_rule", "이 문제는 목적어가 많이 길어서 헷갈려요. 목적어가 길어진 이유는 중간에 music을 꾸며 주는 in which 절이 들어왔기 때문이에요. "
         "[ ]를 빼고 보면 considered 뒤의 짝이 보여요.",
         highlight=["considered"], panel=rows(TOBE_RULE + ("hl",)), panel_below=True, button="알겠어요", slash_on=True),
    judge("s5_tobe_judge", ("④", "to be", "는"), "considered의 목적어가 끝나는 곳을 찾아보면 짝이 보여요.",
          rows(TOBE_RULE), ("1", "3", "4")),
    show("s5_tobe_why", "[ ]를 빼고 보면 considered music to be ‘coarse’예요. consider A to be B 모양 그대로라 to be가 맞아요.",
         highlight=["considered", "music", "to be ‘exceedingly coarse and tasteless’"], panel=TOBE_WHY, panel_below=True, button="다음", slash_on=True),
    show("s5_tobe_name", "이렇게 '동사 + 목적어 + 목적어를 설명하는 말'로 된 문장을 '5형식'이라고 해요. 목적어를 설명하는 to be ~ 부분은 '목적격 보어'라고 불러요.",
         highlight=["to be ‘exceedingly coarse and tasteless’"], button="알겠어요", detail_button="심화: being이나 is는 왜 안 될까요?"),
    {**show("s5_tobe_deep", "consider A 뒤 보어 자리에는 to be를 쓰고 being은 쓰지 않아요. is를 쓰면 한 문장에 동사가 또 오는 거라 안 돼요.",
            highlight=["to be"], button="알겠어요"), "optional_of": "s5_tobe_name"},
    practice_offer("s5_tobe_more", "consider-to-be"),
]

# ⑤ generally — 이 밑줄이 묻는 것(형용사냐 부사냐) → 형용사·부사 표 → 암기 → 「맞을까요?」
#   → 해설(바로 뒤 span이 동사 → 부사) → [심화] -ly인데 형용사인 말 (2026-10-20 선생님, ③과 같은 틀)
ADV_TABLE = rows(("형용사", "~한 — 명사를 꾸미거나 be동사 뒤", "a general rule · It is general."),
                 ("부사", "~하게 — 동사·형용사·문장을 꾸밈", "generally span · surprisingly easy"))
ADV_RULE = ("암기", "명사를 꾸미면 형용사, 동사를 꾸미면 부사", "부사는 보통 형용사 + -ly")
ADV_WHY = rows(("주어", "the instruments", None), ("부사", "generally", "일반적으로", "hl"), ("동사", "span", "걸쳐 있다"))
adv_steps = [
    show("s6_adv_ask", "보기 ⑤generally를 볼게요. 이번 밑줄은 '형용사'가 와야 하는지 '부사'가 와야 하는지 고르는 문제예요.",
         highlight=["generally"], button="네"),
    {**show("s6_adv_table", "형용사와 부사의 차이는 표와 같아요.", panel=ADV_TABLE, panel_below=True, button="알겠어요",
            practice="adverb-verb", practice_button="나중에 보충학습실에서 더 깊이 공부할게요"),
     "brief": {"say": "형용사와 부사의 차이는 표와 같아요.", "saved": "보충학습실에 담아 뒀어요."}},
    show("s6_adv_rule", "꼭 외워 둘 것이 있어요. 명사를 꾸미면 형용사, 동사를 꾸미면 부사예요. 부사는 보통 형용사에 -ly가 붙은 모양이에요.",
         panel=rows(ADV_RULE + ("hl",)), panel_below=True, button="알겠어요"),
    judge("s6_adv_judge", ("⑤", "generally", "는"), "generally가 무엇을 꾸미는지 바로 뒤를 보면 알 수 있어요.",
          rows(ADV_RULE), ("1", "3", "4", "5")),
    show("s6_adv_why", "여기서 generally 바로 뒤의 span은 '걸쳐 있다'라는 동사예요. 동사를 꾸미니 부사 generally가 와야 해요. "
         "부사는 이렇게 주어와 동사 사이에 와도 돼요.",
         highlight=["the instruments", "generally span"], panel=ADV_WHY, panel_below=True, button="알겠어요",
         detail_button="심화: -ly로 끝나는데 형용사인 말도 있어요?"),
    {**show("s6_adv_deep", "friendly(친절한), lovely(사랑스러운), costly(비싼)는 -ly로 끝나도 형용사예요.",
            highlight=["generally"], button="알겠어요"), "optional_of": "s6_adv_why"},
    practice_offer("s6_adv_more", "adverb-verb"),
]

sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        "glosses": [g("We", "우리는"), g("don’t know", "알지 못한다"),
                    g("what ancient Greek music sounded like", "고대 그리스 음악이 어떤 소리였는지"), g("because", "~ 때문에"),
                    g("there are no examples of it", "그것의 사례가 없다"), g("in written or notated form", "기록되거나 악보에 적힌 형태로"),
                    g("nor", "~도 아니다"), g("has it survived", "그것이 살아남았다"), g("in oral tradition", "구전으로")],
        "slashes": ["We don’t know", "sounded like,", "no examples of it", "notated form,", "has it survived"],
        "roles": [r("We", "S"), r("don’t know", "V"), r("what ancient Greek music sounded like", "O"),
                  # because 절·nor 절의 주어·동사도 (2026-10-20 선생님). there are의 주어는 뒤의 no examples of it
                  r("are", "V"), r("no examples of it", "S"), r("has … survived", "V"), r("it", "S")],
        "steps": [
            # ① nor — 뜻 → 「, nor + 동사 + 주어」(도치) → 동사 둘이면 맨 앞만 → nor 앞은 부정문 (2026-10-20 선생님).
            # 설명이 넷 이어지니 칠판(표)에 한 줄씩 쌓는다 [[three-lines-then-board]]
            show("s1_nor_mean", "보기 ①이 있는 nor부터 볼게요. nor는 '~도 아니다'라는 뜻이에요.",
                 highlight=["nor"], panel=nor_board(1), panel_below=True, button="네"),
            show("s1_nor_form", "nor는 완성된 문장 뒤에 「, nor + 동사 + 주어」 순서로 붙어요. 주어와 동사 순서를 바꾸는 것을 '도치'라고 해요.",
                 highlight=["nor", "has it survived"], panel=nor_board(2), panel_below=True, button="네",
                 tips=[tip("반대말 so", "긍정문 뒤에서 '~도 그렇다'는 so를 써요. 순서는 똑같이 so + 동사 + 주어예요. I like jazz, and so does she. = 나는 재즈를 좋아하고, 그녀도 그렇다.")]),
            show("s1_nor_aux", "동사가 두 개 이상이면 맨 앞 동사 하나만 주어 앞으로 가요. has survived에서 has만 it 앞으로 나와 nor has it survived가 됐어요.",
                 highlight=["has it survived"], panel=nor_board(3), panel_below=True, button="네"),
            show("s1_nor_neg", "그리고 nor 앞에는 늘 부정문이 와요. 여기도 앞에 no examples가 있어요.",
                 highlight=["there are no examples of it", "nor"], panel=nor_board(4), panel_below=True, button="알겠어요"),
            nor_try,
            judge("s1_nor_judge", ("①", "has", "은"), "nor 뒤라서 has가 주어 it 앞으로 나온 도치예요.", nor_board(4), ("1",)),
            nor_more,
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "low",
        "glosses": [g("Much of it", "그것의 많은 부분이"), g("was probably improvised", "아마 즉흥 연주였다"), g("anyway", "어쨌든"),
                    g("within certain rules and conventions", "특정 규칙과 관례 안에서")],
        "slashes": ["improvised anyway,"],
        "roles": [r("Much of it", "S"), r("was probably improvised", "V")],
        "steps": [
            show("s2_improvised", "악보가 없던 이유가 하나 더 있어요. 대부분 정해진 규칙 안에서 즉흥 연주였대요.",
                 highlight=["improvised"], button="다음 문장",
                 tips=[tip("improvise", "악보 없이 그 자리에서 즉흥으로 연주하는 거예요.", "improvised")]),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        "glosses": [g("So", "그래서"), g("we", "우리는"), g("are forced", "~할 수밖에 없다"), g("largely", "주로"),
                    g("to guess at its basis", "그 토대를 추측하도록"), g("from the accounts of writers", "작가들의 설명으로부터"),
                    g("such as Plato and Aristotle", "플라톤과 아리스토텔레스 같은"), g("who", "(그 작가들을 가리킴)"),
                    g("were generally more concerned with", "대체로 ~에 더 관심이 있었다"), g("writing about music", "음악에 대해 글 쓰는 것"),
                    g("as a philosophical and ethical exercise", "철학적이고 윤리적인 실천으로서"), g("as with", "~와 (비교해)"),
                    g("providing a technical primer on its practice", "실제에 대한 기술적인 입문서를 제공하는 것")],
        "slashes": ["forced largely", "guess at its basis", "accounts of writers", "and Aristotle,", "concerned with",
                    "writing about music", "ethical exercise", "technical primer"],
        # 콤마 뒤 who 절은 앞(작가들)을 꾸미는 관계대명사절 — 안의 S·V는 안 치고 [ ]로만 (끊어읽기 전체 규칙)
        "roles": [r("we", "S"), r("are forced", "V"), r("to guess at its basis", "O")],
        "modifiers": ["who were generally more concerned with writing about music as a philosophical and ethical exercise ②as with providing a technical primer on its practice"],
        "steps": [
            choice("s3_more",
                   "who 뒤를 봐요. 'more concerned with A ②as with B'로 두 가지를 비교하는데, 작가들이 더 관심 있던 쪽은 어디일까요?",
                   [("o0", "음악에 대해 철학적·윤리적으로 글 쓰는 것", True),
                    ("o1", "음악을 실제로 연주하는 기술적인 입문서를 제공하는 것", False),
                    ("o2", "두 쪽에 똑같이 관심이 있었다", False)],
                   "more concerned with 바로 뒤에 오는 쪽이 '더' 관심 있던 쪽이에요.",
                   why="'more concerned with writing about music …', 음악을 철학·윤리의 실천으로 보고 글 쓰는 쪽에 더 관심이 있었대요. 연주 기술 입문서 쪽이 아니고요.",
                   highlight=["more concerned with", "writing about music"],
                   point="작가들은 음악을 철학·윤리로 다루는 글쓰기에 더 관심 — 연주 기술 입문서 쪽이 아니다"),
            show("s3_hold",
                 "여기서 more는 두 가지를 비교하는 말이에요. more와 짝을 이루는 말이 무엇인지 떠올려 봐요. ②가 그 짝으로 맞는지는 문제에서 골라 봐요.",
                 highlight=["more concerned with", "as with"], button="다음 문장",
                 tips=[tip("more A than B", "두 가지를 비교할 때 '더'는 more, 비교하는 대상은 than으로 이어요. more concerned with A than with B = B보다 A에 더 관심이 있다.", "more")],
                 point="② more가 비교하는 짝 — 비교 구문의 짝이 맞는지 문제에서 확인"),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "high",
        "glosses": [g("It seems", "~인 것 같다"), g("Greek music was predominantly a vocal form", "그리스 음악은 대개 성악 형식이었다"),
                    g("consisting of sung verse", "노래되는 운문으로 구성된"), g("accompanied by instruments", "악기의 반주를 받는"),
                    g("such as the lyre", "수금 같은"), g("or the plucked kithara", "또는 퉁기는 키타라"),
                    g("(the root of ‘guitar’)", "('기타'의 뿌리)")],
        "slashes": ["It seems", "vocal form,", "sung verse", "accompanied by instruments", "plucked kithara"],
        "roles": [r("It", "S"), r("seems", "V"), r("Greek music", "S"), r("was", "V"), r("a vocal form", "C")],
        "steps": [
            *cons_steps,
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "high",
        "glosses": [g("In fact", "사실"), g("Plato", "플라톤은"), g("considered", "여겼다"), g("music", "음악을"),
                    g("in which", "그 안에서"), g("the lyre and flute", "수금과 피리가"), g("played alone", "홀로 연주되는"),
                    g("and not as the accompaniment of dance or song", "춤이나 노래의 반주로서가 아니라"),
                    g("to be ‘exceedingly coarse and tasteless’", "'매우 조잡하고 무미건조하다'고")],
        "slashes": ["In fact,", "considered music", "played alone", "dance or song"],
        # in which 절은 music을 꾸미는 관계사절 — 안의 S·V는 안 치고, 목적어는 music부터 song까지 길게, 꾸밈은 [ ] (2026-10-20 선생님)
        "roles": [r("Plato", "S"), r("considered", "V"),
                  r("music in which the lyre and flute played alone and not as the accompaniment of dance or song", "O"),
                  r("to be ‘exceedingly coarse and tasteless’", "C")],
        "modifiers": ["in which the lyre and flute played alone and not as the accompaniment of dance or song"],
        "steps": [
            *tobe_steps,
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "medium",
        "glosses": [g("The melodies", "그 선율은"), g("seem to have had", "가지고 있었던 것 같다"),
                    g("a very limited pitch range", "매우 제한된 음역을"), g("since", "~ 때문에"), g("the instruments", "그 악기들은"),
                    g("generally span", "일반적으로 걸쳐 있다"), g("only an octave", "단지 한 옥타브에만"), g("from one E", "한 E에서"),
                    g("(as we’d now define it)", "(우리가 지금 정의하는 대로)"), g("to the next", "다음 E까지")],
        "slashes": ["seem to have had", "pitch range,", "since the instruments", "an octave,", "from one E", "define it)"],
        "roles": [r("The melodies", "S"), r("seem to have had", "V"), r("a very limited pitch range", "O"), r("the instruments", "S"), r("span", "V")],
        "steps": [
            *adv_steps,
            show("s6_go",
                 "①③④⑤는 모두 맞았어요. 남은 하나, ②를 다시 떠올리며 문제를 골라 봐요.",
                 panel=check("1", "3", "4", "5"), panel_below=True, button="문제 풀러 갈게요"),
        ],
    },
]

SENSES = {
    3: [sense("so", "So we are forced", "그래서", "접속사 so (문장 앞, 결과)"),
        sense("to", "to guess", "~하도록", "be forced + to부정사"),
        sense("as", "such as Plato", "~ 같은", "such as + 예시"),
        sense("as", "as a philosophical and ethical exercise", "~로서", "전치사 as (자격·역할)"),
        sense("as", "as with providing", "~와 (비교해)", "비교 대상을 잇는 자리 — more와 짝이 맞는지 보기")],
    4: [sense("as", "such as the lyre", "~ 같은", "such as + 예시")],
    5: [sense("which", "in which the lyre and flute played", "그 안에서 (앞 명사를 꾸밈)", "전치사 + 관계대명사 (뒤 문장이 완전하다)"),
        sense("as", "as the accompaniment", "~로서", "전치사 as (자격·역할)"),
        sense("to", "to be", "~라고 (여기다)", "consider + 목적어 + to be + 보어")],
    6: [sense("to", "seem to have had", "~한 (것 같다)", "seem + to부정사 (완료형 to have + p.p.)"),
        sense("since", "since the instruments", "~ 때문에", "접속사 since (이유)"),
        sense("as", "as we’d now define it", "~하는 대로", "접속사 as (방식)"),
        sense("to", "to the next", "~까지", "from A to B")],
}

WORDS = {
    "ancient": "고대의", "greek": "그리스의", "music": "음악", "sounded": "소리가 났다", "like": "~처럼", "examples": "사례",
    "written": "기록된", "notated": "악보에 적힌", "form": "형태", "survived": "살아남았다", "oral": "입으로 전하는",
    "tradition": "전통 · oral tradition = 구전", "much": "많은 부분", "probably": "아마", "improvised": "즉흥 연주되었다",
    "anyway": "어쨌든", "certain": "특정한", "rules": "규칙", "conventions": "관례", "forced": "강요받는", "largely": "주로",
    "guess": "추측하다", "basis": "토대", "accounts": "설명", "writers": "작가들", "plato": "플라톤", "aristotle": "아리스토텔레스",
    "generally": "일반적으로, 대체로", "concerned": "관심이 있는 · be concerned with = ~에 관심이 있다", "writing": "글 쓰는 것",
    "philosophical": "철학적인", "ethical": "윤리적인", "exercise": "실천, 활동", "providing": "제공하는 것", "technical": "기술적인",
    "primer": "입문서", "practice": "실제, 실천", "seems": "~인 것 같다", "predominantly": "대개", "vocal": "목소리의, 성악의",
    "consisting": "구성된 · consist of = ~로 구성되다", "sung": "노래되는", "verse": "운문", "accompanied": "반주를 받는",
    "instruments": "악기", "lyre": "수금(현악기)", "plucked": "퉁기는", "kithara": "키타라(옛 현악기)", "root": "뿌리",
    "guitar": "기타", "fact": "사실 · in fact = 사실", "considered": "여겼다", "flute": "피리", "played": "연주되었다",
    "alone": "홀로", "accompaniment": "반주", "dance": "춤", "song": "노래", "exceedingly": "매우", "coarse": "조잡한",
    "tasteless": "무미건조한, 멋없는", "melodies": "선율", "seem": "~인 것 같다", "limited": "제한된", "pitch": "음(높이)",
    "range": "범위 · pitch range = 음역", "span": "걸쳐 있다", "octave": "옥타브", "define": "정의하다", "next": "다음 것",
    "e": "E (음 이름 '미')", "we’d": "우리가 ~하는 (we would)",
}

exam = {
    "question": "다음 글의 밑줄 친 부분 중, 어법상 틀린 것은? [3점]",
    "underline": UNDER, "sentence": 3, "analysis_first": True,
    "wrong_rate": 67.0, "wrong_rank": 1,
    "wrong_rate_source": "메가스터디 풀서비스 채점 기준 — 전체 응시자 공개 오답률과 다를 수 있다",
    "glosses": [g("has", "(현재완료의 조동사)"), g("as", "~와 (비교해)"), g("consisting", "구성된"), g("to be", "~라고 (여기다)"),
                g("generally", "일반적으로")],
    "options": [{"id": str(i + 1), "label": u[1:], "keywords": [u[1:]], **({"correct": True} if i == 1 else {})}
                for i, u in enumerate(UNDER)],
    "brief": exam_brief(
        "밑줄 점검표를 떠올리며 어법상 틀린 것 하나를 골라 봐요.",
        "정답이에요! more로 두 가지를 비교했으니 짝이 되는 말은 than이어야 해요. ②as with → than with로 고쳐요.",
        "정답은 ②예요. 'more concerned with A … as with B'에서 more와 짝을 이루는 말은 than이에요. as with를 than with로 고쳐요.",
        {"1": "부정어 nor가 앞에 와서 '조동사 + 주어' 순서가 된 거라 ①has it survived는 맞아요.",
         "3": "앞에 이미 동사 was가 있어서 접속사 없이 이어 붙이려면 -ing가 와야 해요. ③consisting은 맞아요.",
         "4": "consider + 목적어 + to be + 보어예요. 목적어 music이 길어서 멀어 보일 뿐 ④to be는 맞아요.",
         "5": "동사 span을 꾸미는 자리라 부사 ⑤generally가 맞아요."},
        {"3": review(24,
                     "③ 앞에는 이미 동사 was가 있어서 '동사가 둘'로 보여요. 하지만 접속사 없이 문장을 이어 붙일 때는 동사를 -ing(분사)로 바꿔요. 그래서 consisting이 맞아요.",
                     panel=rows(("앞", "It seems Greek music was …", "콤마 앞 — 이미 주어·동사가 있다", "hl"),
                                ("뒤", "consisting of sung verse", "접속사가 없으니 -ing로 이어 붙인다", "hl2"))),
         "4": review(23,
                     "④to be는 considered와 멀리 떨어져 있어서 어색해 보여요. 목적어 music 뒤에 in which 덩어리가 길게 붙어서 그래요. consider + 목적어 + to be + 보어 모양이라 ④는 맞아요.",
                     panel=rows(("여긴 사람", "Plato considered", "주어 + 동사", "hl"),
                                ("여긴 대상", "music in which … dance or song", "목적어 — in which 덩어리가 길게 꾸민다", "hl2"),
                                ("여긴 어떻다", "to be ‘exceedingly coarse and tasteless’", "그 목적어가 어떻다는 보어", "hl")))}),
}
# 정답 해설 다음 참고 한 화면 (2026-10-20 선생님): more·as 짝은 모의고사 어법에 거의 안 나와서 많이 틀렸다 — 보통은 분사 구분 등을 묻는다
exam["brief"]["answer_note"] = ("참고로 more와 as의 짝을 묻는 어법 문제는 모의고사에 거의 나온 적이 없어요. "
                                "낯선 유형이라 이 문제가 이 회차 오답률 1위였어요. 보통은 동사냐 분사냐 같은 것을 주로 물어봐요.")

# ── 10분 모의고사·분석 화면의 「핵심어」(emphasis) — 2026-10-20 ──
# 핵심어 = S·V·O·C + 이해에 필요한 말, 최소한(덩어리 말고 핵심 단어). 모두 glosses에 뜻이 있는 말로 (exam_kit check)

EMPHASIS = {
    # 선생님 기준(2026-10-20, 33번): 지문당 10개 안팎 — 주장이 서는 1~2문장의 S·V·O·C와 연결어만, 나머지 문장은 없음
    1: ["don’t know", "nor", "has it survived"],
    3: ["were generally more concerned with", "as with"],
    5: ["considered", "to be ‘exceedingly coarse and tasteless’"],
}

for _s in sentences:
    for _c in SLASHES.get(_s["id"], []) if "SLASHES" in globals() else []:
        assert _s["text"].count(_c) == 1, (_s["id"], _c)  # 한 번만 나오는 말로 — 끊을 자리가 하나로 정해지게
    if "SLASHES" in globals() and SLASHES.get(_s["id"]):
        _s["slashes"] = SLASHES[_s["id"]]
    if "ROLES" in globals() and ROLES.get(_s["id"]):
        _s["roles"] = ROLES[_s["id"]]
    if "MODIFIERS" in globals() and MODIFIERS.get(_s["id"]):
        _s["modifiers"] = MODIFIERS[_s["id"]]
    if EMPHASIS.get(_s["id"]):
        _s["emphasis"] = EMPHASIS[_s["id"]]
assert set(EMPHASIS) <= {_s["id"] for _s in sentences}, "EMPHASIS에 없는 문장 번호"

# ── 해석 맞추기(모두에게)·가리키는 말 — 2026-10-20 엔진: S·V 찾기·핵심어 자유 해석은 빠지고 맞추기가 대신 나온다 ──
from beginner import add_match, add_refers, m as _m  # noqa: E402
add_refers(sentences, 2, {"Much of it": "much of ancient Greek music(고대 그리스 음악의 대부분)"})

lesson = base_lesson(
    ID, source="2022년 3월 고3 전국연합학력평가 영어 29번 (어법, 3점)",
    topic="어법 푸는 법: 밑줄마다 무슨 문법을 묻는지 이름 붙이기 → 그 문장 뼈대(주어·동사·빈자리)로 확인",
    method={"type": "grammar", "labels": ["밑줄 문법 확인", "틀린 것 고르기"], "intro_times": 3},
    images={"topic": {"src": topic_svg("topic-greek-music.svg", ("Greek music", "고대 그리스 음악"), "?",
                                       ("No notation", "악보도 기록도 없음"),
                                       "그러면 어떤 소리였는지 어떻게 짐작할까?", "2022년 3월 29번 도입 칠판"),
                      "alt": "칠판: Greek music(고대 그리스 음악) ? No notation(악보도 기록도 없음)", "kind": "drawing"}},
    intro=[{"id": "topic", "type": "say", "button": "네", "image": "topic",
            "brief": {"say": "고대 그리스 음악은 어떤 소리였을까요? 악보도 녹음도 남아 있지 않아서, 글로 남은 설명으로 짐작할 수밖에 없대요."}},
           {"id": "method1", "type": "say", "button": "좋아요",
            "brief": {"say": "어법 문제는 다른 문제들과 달리 문법만 보면 돼요. 그래서 이번 유형은 문법 설명 위주로 갈게요."}}],
    exam=exam,
    key_words={"passage": [g("notate", "악보에 적다"), g("oral tradition", "구전"), g("improvise", "즉흥 연주하다"),
                           g("convention", "관례, 관행"), g("account", "설명"), g("be concerned with", "~에 관심이 있다"),
                           g("philosophical", "철학적인"), g("predominantly", "대개"), g("consist of", "~로 구성되다"),
                           g("verse", "운문"), g("accompany", "반주하다"), g("accompaniment", "반주"), g("exceedingly", "매우"),
                           g("tasteless", "무미건조한"), g("pitch range", "음역"), g("span", "걸쳐 있다")],
               "options": []},
    sentences=sentences, concept="medium")

# 헷갈리는 단어 — 학생이 평소 아는 뜻과 이 글의 뜻이 다른 단어만 (2026-10-20 선생님: bear = 곰 ✕).
# 해설 번역과 대조함: accounts 설명 · exercise 실천 · practice 실제 · conventions 관례 · pitch (range) 음역.
# 그 문장의 첫 스텝에 붙이면 처음 읽는 화면부터 물결 밑줄로 보인다. more·improvise는 헷갈리는 단어가 아니라 Tip이다
TRAPS = {
    2: [tip("conventions", "이 글에서는 → 관례  ('대회, 회의' 아님)", "conventions", trap=True)],
    3: [tip("accounts", "이 글에서는 → 설명  ('계좌' 아님)", "accounts", trap=True),
        tip("exercise", "이 글에서는 → 실천, 행위  ('운동' 아님)", "exercise", trap=True),
        tip("practice", "이 글에서는 → 실제(로 하는 것)  ('연습' 아님)", "practice", trap=True)],
    6: [tip("pitch range", "이 글에서는 → pitch = 음높이, pitch range = 음역  ('던지다, 투구' 아님)", "pitch range", trap=True)],
}
for _s in lesson["sentences"]:
    if _s["id"] in TRAPS:
        _first = _s["steps"][0]
        _first["tips"] = [*_first.get("tips", []), *TRAPS[_s["id"]]]

# 어법은 S·V 찾기 없이 밑줄 문법만 — 분석 스텝은 모두 ① 밑줄 문법 확인, 문제는 ② 틀린 것 고르기
for _s in lesson["sentences"]:
    for _st in _s["steps"]:
        _st["method"] = 0

finish(ID, lesson, senses=SENSES, words=WORDS, topic_intro="어법 푸는 법",
       chunks={"We": "우리는", "don’t know": "알지 못한다",
               "what ancient Greek music sounded like": "고대 그리스 음악이 어떤 소리였는지",
               "there are no examples of it": "그것의 사례가 없다", "has it survived": "그것이 살아남았다",
               "we": "우리는", "are forced": "~할 수밖에 없다", "to guess at its basis": "그 토대를 추측하도록",
               "who": "(앞의 작가들을 가리킴)", "were generally more concerned with": "대체로 ~에 더 관심이 있었다",
               "Plato": "플라톤은", "considered": "여겼다", "music": "음악을", "the lyre and flute": "수금과 피리가",
               "played alone": "홀로 연주되는"})
