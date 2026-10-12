"""2026년 3월 24번 레슨 + 대사를 만든다 (글의 제목, 3점).

레슨 JSON(content/tutor/policy-lessons/…)과 대사(content/tutor/policy-copy/dajung/…)는 이 스크립트의
생성물이다. 고칠 때는 여기를 고치고 다시 돌린 뒤 도장을 찍는다:

    python3 scripts/lessons/gen_moeui_2026_03_24.py
    npm run policy:copy stamp moeui-2026-03-24-translation-strangeness

1문장은 선생님과 정했다 (domesticated·take it for granted 뜻 → accessible X / evaporates O →
예술의 역할 자유 응답 → 핵심어 찾기). 2~5문장, 도입, 푸는 법 칠판은 아직 초안.
"""
import copy
import json
import os

ID = "moeui-2026-03-24-translation-strangeness"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def g(en, ko):
    return {"en": en, "ko": ko}


def choice(id, ask, options, hint, praise="맞아요!", method=0, why=None, **extra):
    """why: 틀렸을 때 「아쉽게도 틀렸어요.」 뒤의 이유 (없으면 힌트)"""
    feedback = {o[0]: why or hint for o in options if not o[2]}
    brief = {"ask": ask, "reask": "그럼 하나 골라 봐요.", "hints": [hint, hint], "explain": hint, "praise": praise, "feedback": feedback}
    if id in POINTS:
        brief["point"] = POINTS[id]
    return {
        "id": id, "type": "choice", "interaction": "meaning_choice", "one_try": True,
        "brief": brief,
        "options": [{"id": o[0], "label": o[1], **({"correct": True} if o[2] else {})} for o in options],
        "method": method, **extra,
    }


def show(id, say, method=0, button="다음 문장", point=None, **extra):
    brief = {"say": say, **({"point": point} if point else {})}
    return {"id": id, "type": "show", "interaction": "note", "brief": brief, "method": method, "button": button, **extra}


def pick(id, ask, candidates, answers, wrong, explain, praise="맞아요!", shade=False, method=0, **extra):
    brief = {"ask": ask, "wrong": wrong, "more": "좋아요! {n}개 남았어요.", "praise": praise, "explain": explain}
    if id in POINTS:
        brief["point"] = POINTS[id]
    return {"id": id, "type": "pick", "interaction": "word_pick", **({"shade": True} if shade else {}),
            "candidates": candidates, "answers": answers, "brief": brief, "method": method, **extra}


# 수업 끝 「오늘 헷갈렸던 곳」 한 줄
POINTS = {
    "s1_fate": "Something too domesticated = 너무 익숙해진 것 → 다가가기 쉬워지는 게 아니라(isn't accessible) 사라진다(evaporates)",
    "s1_art": "art restores its visibility = 예술이 그것(너무 익숙한 것)을 다시 보이게 한다",
    "s2_task": "this task = 앞 문장의 'art restores its visibility' (익숙해서 안 보이던 것을 다시 보이게 하는 일) · this·that 같은 지시어는 앞 문장에서 찾는다",
    "s2_suited": "this task(다시 보이게 하는 일)에 특히 잘 맞는 것 = translation(번역) · art는 번역이 무엇인지 말하는 말",
    "s2_pick": "2문장 핵심어 = translation · art · suited · this task",
    "s3_subj1": "while 덩어리의 주어 = a great work of literature (동사 accumulates)",
    "s3_subj2": "메인 문장의 주어 = translations of that work (동사 free) · 콤마 뒤 첫 덩어리",
    "s3_verb1": "주어 a great work of literature의 동사 = accumulates (bury는 that 덩어리 안의 동사)",
    "s3_verb2": "주어 translations of that work의 동사 = free (putting은 by ~ing '옮김으로써')",
    "s3_keys": "3문장 핵심어 = 주어·동사 + 목적어: a great work of literature · accumulates · imitations · translations of that work · free · its stodgy fame",
    "s3_while": "while = ~하는 반면에 (앞: 작품이 묻힌다 ↔ 뒤: 번역이 풀어 준다)",
    "s3_trans": "3문장 = 위대한 문학 작품은 모방작 등이 쌓여 묻힐 수 있는 반면, 번역본은 작품을 따분한 명성에서 풀어 준다",
    "s3_art": "3문장에서 예술(다시 보이게 하는 것) = translations of that work (번역본)",
    "s4_one": "A bad text is one that … = one은 앞의 text를 다시 받는 '것(글)' (숫자 1 · '누구든'과 다름)",
    "s4_lacks": "lacks “native strangeness” = '본래의 낯섦'이 없다 · in Berman’s terms(Berman의 용어로)는 빼도 되는 삽입",
    "s4_sign": "native strangeness = 좋은 말(+) · a bad text(−)가 lacks(−, 부족하다) → 부족해서 안 좋으면 있어야 좋은 것",
    "s4_sort": "native strangeness(본래의 낯섦) = 익숙해진 것(domesticated)의 반대 → 번역·예술이 살려 내는 쪽",
    "s4_nothing": "낯섦이 없는 글은 번역해도 nothing happens(아무 일도 일어나지 않는다)",
    "s4_pick": "4문장 핵심어 = A bad text · lacks · native strangeness · nothing happens",
    "s5_subj": "5문장 주어 = The translation of a true work of art (is 앞 덩어리)",
    "s5_it": "because it의 it = 번역(The translation) · 끝의 in it의 it = 작품",
    "s5_inherent": "qualities already inherent in it = 작품 안에 이미 있던 자질 (= native strangeness)",
    "s5_pick": "5문장 핵심어 = The translation of a true work of art · significant · reinforces · enhances · qualities · inherent",
    "s6_notbut": "not A, but B = A가 아니라 B (뒤가 글쓴이의 말)",
    "s6_what": "번역 = 임시방편(makeshift)이 아니라, 작품이 우리에게 낯설게(étrange) 다가오는 방식",
    "s6_pick": "6문장 핵심어 = translation · makeshift · the mode of existence · reaches us · étrange",
    "s7_make": "makes the work seem more strange = 작품을 더 낯설게 보이게 만든다 (make + 목적어 + 동사원형)",
    "s7_sort": "seem more strange(더 낯설게 보인다) = 다시 보이게 하는 쪽 (익숙해서 안 보임의 반대)",
    "s7_pick": "7문장 핵심어 = translation · makes · the work · more strange · newly strange",
    "s1_pick": "1문장 핵심어 = domesticated · evaporates · take it for granted · art · restores · visibility",
}

S1 = ("Something too domesticated isn’t actually more accessible or approachable, it evaporates altogether—"
      "we just take it for granted until art restores its visibility.")

S3 = ("while a great work of literature accumulates imitations and clichés and a body of scholarship and analysis and "
      "study guides that may well bury it, translations of that work free it from its stodgy fame and make the stone "
      "stony again, precisely by putting it in another language.")

S4_FADED = "in Berman’s terms"

S5 = "The translation of a true work of art is significant because it reinforces and enhances qualities already inherent in it:"
S6 = ("“translation is not a makeshift, but the mode of existence by which a work reaches us as étrange” "
      "(translated by Heyvaert as “foreign,” but I’m not sure about that).")
S6_FADED = "(translated by Heyvaert as “foreign,” but I’m not sure about that)"
S6_FADED_NOTE = "흐린 부분은 괄호 속 글쓴이의 덧붙임이라 건너뛰어도 돼요"
S6_FADED_TIP = {"label": "괄호 건너뛰기",
                "text": "괄호 ( ) 안은 글쓴이가 덧붙인 말일 때가 많아요. 급할 때는 건너뛰고 괄호 앞만 읽어도 뜻이 통해요."}
S7 = "As Wilson put it, translation makes the work “seem more strange, and newly strange.”"

# while 덩어리와 메인 문장 사이(콤마 뒤)에 슬래시 — 'while + 주어 + 동사, / 주어 + 동사'가 보이게
S3_SLASH = S3.replace("may well bury it, translations", "may well bury it, / translations")

SORT3_LEFT = "왼쪽 · 익숙해서 안 보임"
SORT3_RIGHT = "오른쪽 · 다시 보이게 함"


def board3(left_extra, right_extra):
    """1문장의 두 그룹 — something too domesticated(익숙해서 안 보임) ↔ art(다시 보이게 함)"""
    return {
        "kind": "groups", "title": "1문장의 두 그룹", "between": "↔",
        "left": {"label": "something too domesticated 쪽 · 익숙해서 안 보임",
                 "words": [{"text": "something too domesticated"}] + [{"text": w, "fresh": True} for w in left_extra]},
        "right": {"label": "art 쪽 · 다시 보이게 함",
                  "words": [{"text": "art"}] + [{"text": w, "fresh": True} for w in right_extra]},
    }


sentences = [
    {
        "id": 1, "text": S1,
        "model_translation": "너무나 길든 것은 실제로 더 다가가기 쉽거나 이해하기 쉬운 것이 아니라, 모두 증발해 버리며, 우리는 예술이 그것의 가시성을 회복할 때까지 그것을 당연하게 여길 뿐이다.",
        "teaching_value": "high",
        "glosses": [
            # 「Something too domesticated」를 한 덩어리 뜻으로 묶으면 핵심어 찾기에서 domesticated를 따로 못 누른다
            g("Something", "어떤 것"),
            g("domesticated", "길든, 익숙해진"),
            g("actually", "실제로"),
            g("accessible", "다가가기 쉬운"),
            g("approachable", "이해하기 쉬운, 가까이하기 쉬운"),
            g("evaporates", "증발하다, 사라지다"),
            g("altogether", "완전히, 모두"),
            g("take it for granted", "그것을 당연하게 여기다"),
            g("until", "~할 때까지"),
            g("art", "예술"),
            g("restores", "회복시키다, 되살리다"),
            g("visibility", "눈에 보임, 가시성"),
        ],
        # 2등급 아래 학생은 이 두 표현에서 막힌다 — 문장 아래 ❓ 칩으로 늘 열어 볼 수 있게
        "concepts": [
            {"en": "domesticated", "title": "domesticated:",
             "text": "원래 '(동물이) 길든'이에요. 여기서는 너무 자주 봐서 '익숙해진'이라는 뜻이에요."},
            {"en": "take it for granted", "title": "take it for granted:",
             "text": "'그것을 당연하게 여기다'예요. 너무 익숙해서 더는 눈여겨보지 않는다는 말이에요."},
        ],
        # 핵심어는 마지막에 학생이 직접 찾는다 — 미리 색칠하지 않는다
        "steps": [
            # 익숙한 것은 어떻게 되나 — accessible(X) / evaporates(O)
            choice("s1_fate",
                   "너무 익숙해진 것(something too domesticated)은 어떻게 된다고 할까요?",
                   [("o0", "더 다가가기 쉬워진다 (accessible)", False), ("o1", "사라져 버린다 (evaporates)", True)],
                   "'isn’t actually more accessible'에 not이 붙어 있어요. 콤마 뒤를 봐요.",
                   why="'isn’t actually more accessible'이라서 다가가기 쉬워지는 게 아니래요. 콤마 뒤 'it evaporates', 사라져 버린대요.",
                   highlight=["Something too domesticated"],
                   method=0),
            show("s1_contrast",
                 "너무 익숙해진 것은 다가가기 쉬워지는 게 아니라 사라져 버려요. 너무 익숙해서 당연하게 여기니까 눈에 안 보이는 거예요.",
                 button="다음",
                 highlight=["isn’t actually more accessible or approachable", "it evaporates altogether"],
                 panel={"kind": "contrast", "title": "너무 익숙해진 것은", "between": "↔",
                        "left": {"title": "✗ accessible", "text": "다가가기 쉬워진다"},
                        "right": {"title": "✓ evaporates", "text": "사라져 버린다"}},
                 method=1),
            # 예술의 역할 — 학생이 직접 쓴다 (규칙으로 채점, 쓴 답은 그대로 기록)
            {
                "id": "s1_art", "type": "translate", "interaction": "free_translation",
                "model": "예술은 너무 익숙해서 당연하게 여기던 것을 다시 보이게 한다.",
                "labels": {"mine": "내 답", "model": "모범 답"},
                "rules": [
                    {"id": "target", "need": ["익숙", "당연", "길든", "길들", "그것", "something"],
                     "fix": "너무 익숙해서 당연하게 여기던 것을"},
                    {"id": "visible", "need": ["보이", "보여", "보게", "가시", "드러", "눈에 띄", "알아차", "인식", "되살", "회복"],
                     "fix": "다시 보이게 한다"},
                ],
                "highlight": ["art restores its visibility"],
                "tips": [{"label": "힌트", "hint": True, "mark": "its",
                          "text": "its가 가리키는 것은 something too domesticated(너무 익숙해진 것)예요."}],
                "brief": {
                    "ask": "그럼 예술(art)의 역할은 뭘까요? 자유롭게 써 봐요.",
                    "praise": "잘 답했어요! 예술은 익숙해서 안 보이던 것을 다시 보이게 해요.",
                    "wrong": "모범 답과 같이 봐요.",
                    "explain": "괜찮아요. 모범 답을 같이 봐요.",
                    "feedback": {
                        "target": "its는 something too domesticated, 즉 너무 익숙해서 당연하게 여기던 것을 가리켜요.",
                        "visible": "restores its visibility는 '그것이 다시 보이게 한다'예요. visibility는 '눈에 보임'이에요.",
                    },
                    "placeholder": "예술은 …",
                    "point": POINTS["s1_art"],
                },
                "method": 1,
            },
            {
                "id": "s1_pick", "type": "pick", "interaction": "word_pick",
                # 함정은 뜻을 덧붙이기만 하는 말 (actually, altogether, we, just) — accessible 같은 내용어는 넣지 않는다
                "candidates": ["domesticated", "actually", "evaporates", "altogether", "we", "just",
                               "take it for granted", "art", "restores", "visibility"],
                "answers": ["domesticated", "evaporates", "take it for granted", "art", "restores", "visibility"],
                "brief": {
                    "ask": "이제 이 문장의 핵심어 6개를 찾아볼까요?",
                    "wrong": "그건 핵심어가 아니에요. 익숙한 것이 어떻게 되고, 무엇이 그것을 되살리는지 찾아봐요.",
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "다 찾았어요!",
                    "explain": "핵심어는 domesticated, evaporates, take it for granted, art, restores, visibility예요. 익숙한 것은 사라지고, 예술이 그것을 다시 보이게 해요.",
                    "point": POINTS["s1_pick"],
                },
                "method": 0,
            },
            # 찾은 핵심어만 이어서 해석 — 모든 단어를 읽지 않아도 뜻이 잡힌다는 걸 직접 해 본다
            {
                "id": "s1_keys", "type": "translate", "interaction": "free_translation",
                "model": "너무 익숙해진 것은 사라져 버리고, 우리는 예술이 다시 보이게 할 때까지 그것을 당연하게 여긴다.",
                "rules": [
                    {"id": "familiar", "need": ["익숙", "길든", "길들"], "fix": "너무 익숙해진 것은"},
                    {"id": "fade", "need": ["사라", "증발", "없어"], "wrong": ["다가가기 쉬", "접근하기 쉬"], "fix": "사라져 버리고"},
                    {"id": "granted", "need": ["당연"], "fix": "당연하게 여긴다"},
                    {"id": "art", "need": ["예술"], "fix": "예술이"},
                    {"id": "visible", "need": ["보이", "보여", "보게", "가시", "드러", "되살", "회복"], "fix": "다시 보이게 할 때까지"},
                ],
                "highlight": ["domesticated", "evaporates", "take it for granted", "art", "restores", "visibility"],
                "brief": {
                    "ask": "그럼 이 핵심어만 가지고 문장을 자유롭게 해석해 봐요.",
                    "praise": "잘 해석했어요! 핵심어만으로도 뜻이 잡혀요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "familiar": "domesticated는 '너무 익숙해진'이에요. 문장의 주인공이에요.",
                        "fade": "evaporates는 '사라져 버린다'예요. 다가가기 쉬워지는 게 아니에요.",
                        "granted": "take it for granted는 '그것을 당연하게 여기다'예요.",
                        "art": "art, 예술이 그것을 되살리는 주인공이에요.",
                        "visible": "restores its visibility는 '다시 보이게 한다'예요.",
                    },
                    "placeholder": "핵심어만 보고 해석해 보세요",
                    "point": "핵심어만으로 해석 = " + "너무 익숙해진 것은 사라져 버리고, 우리는 예술이 다시 보이게 할 때까지 그것을 당연하게 여긴다.",
                },
                "method": 0,
            },
        ],
    },
    {
        "id": 2,
        # 원문은 한 문장이지만 길어서 콜론(:)에서 나눈다 — 콜론 뒤는 문장 3
        "text": "And perhaps translation is an art especially well suited for this task:",
        "model_translation": "그리고 아마도 번역은 이러한 과업에 특히 잘 맞는 예술이다.",
        "teaching_value": "high",
        "glosses": [
                    # 앞 문장(문장 1)을 보여 주고 구절을 고를 때 쓰는 덩어리
                    g("Something too domesticated", "너무 익숙해진 것"), g("it evaporates altogether", "그것은 완전히 사라져 버린다"),
                    g("take it for granted", "그것을 당연하게 여기다"), g("art restores its visibility", "예술이 그것을 다시 보이게 한다"),
                    # well suited for를 한 덩어리로 묶으면 핵심어 찾기에서 suited를 따로 못 누른다
                    g("And", "그리고"), g("translation", "번역"), g("art", "예술"), g("well", "잘"), g("suited", "알맞은 · well suited for = ~에 잘 맞는"),
                    g("this task", "이 일")],
        "steps": [
            # this 같은 지시어 → 앞 문장에서 찾는다
            show("s2_this",
                 "this처럼 앞에 나온 걸 가리키는 말이 나오면, 가리키는 것을 앞 문장에서 찾아야 해요. 'this task'가 무엇인지 앞 문장에서 찾아볼게요.",
                 button="앞 문장 볼게요",
                 highlight=["this task"],
                 tips=[{"label": "this·that·such", "mark": "this",
                        "text": "this, that, such, these 같은 말은 앞에서 말한 것을 다시 가리켜요. 뜻이 안 잡히면 바로 앞 문장으로 돌아가서 찾아요."}],
                 method=1),
            # 앞 문장을 보여 주고 음영 친 구절 중에서 고른다 — ‹ › 로 지금 문장(this task)과 오갈 수 있다
            {
                "id": "s2_task", "type": "pick", "interaction": "word_pick", "shade": True,
                "display": S1, "tag": "문장 1",
                "flip": {"highlight": ["this task"]},
                "candidates": ["Something too domesticated", "it evaporates altogether", "take it for granted",
                               "art restores its visibility"],
                "answers": ["art restores its visibility"],
                "brief": {
                    "ask": "'this task(이 일)'가 가리키는 건 문장 1에서 어느 부분일까요?",
                    "wrong": "그건 '할 일'이 아니에요. 누가 무엇을 해 주는 일인지 찾아봐요.",
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "맞아요!",
                    "explain": "this task는 'art restores its visibility', 익숙해서 안 보이던 것을 예술이 다시 보이게 하는 일이에요.",
                    "point": POINTS["s2_task"],
                },
                "method": 1,
            },
            show("s2_task_back",
                 "this task는 익숙해서 안 보이던 것을 다시 보이게 하는 일이에요.",
                 button="다음",
                 highlight=["this task"],
                 method=1),
            # 이 일에 잘 맞는 건 무엇 — 학생이 문장에서 직접 고른다 (답을 미리 칠하지 않는다)
            pick("s2_suited", "그럼 this task에 특히 잘 맞는 건 무엇일까요?",
                 ["perhaps", "translation", "art", "especially"],
                 ["translation"],
                 "그건 이 일에 잘 맞는 주인공이 아니에요. 문장의 주어를 찾아봐요.",
                 "'translation(번역)'이에요. 번역이 이 일에 특히 잘 맞는 예술(art)이래요.",
                 highlight=["this task"], method=1),
            {
                "id": "s2_pick", "type": "pick", "interaction": "word_pick",
                "candidates": ["And", "perhaps", "translation", "art", "especially", "well", "suited", "this task"],
                "answers": ["translation", "art", "suited", "this task"],
                "brief": {
                    "ask": "이 문장의 핵심어 4개를 찾아볼까요?",
                    "wrong": "그건 뜻을 덧붙이는 말이라 핵심어가 아니에요. 무엇이 어떤 일에 맞는지 찾아봐요.",
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "다 찾았어요!",
                    "explain": "핵심어는 translation, art, suited, this task예요. 번역은 이 일에 잘 맞는 예술이에요.",
                    "point": POINTS["s2_pick"],
                },
                "method": 0,
            },
            {
                "id": "s2_keys", "type": "translate", "interaction": "free_translation",
                "model": "번역은 이 일에 특히 잘 맞는 예술이다.",
                "rules": [
                    {"id": "translation", "need": ["번역"], "fix": "번역은"},
                    {"id": "task", "need": ["이 일", "이러한 일", "그 일", "과업", "과제", "보이게"], "wrong": ["업무", "작업"], "fix": "이 일에"},
                    {"id": "suited", "need": ["맞", "알맞", "적합", "어울", "적절"], "fix": "특히 잘 맞는"},
                    {"id": "art", "need": ["예술"], "fix": "예술이다"},
                ],
                "highlight": ["translation", "art", "suited", "this task"],
                "brief": {
                    "ask": "그럼 이 핵심어만 가지고 문장을 자유롭게 해석해 봐요.",
                    "praise": "잘 해석했어요! 핵심어만으로도 뜻이 잡혀요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "translation": "translation은 '번역'이에요. 문장의 주인공이에요.",
                        "task": "this task는 앞에서 찾은 '이 일', 다시 보이게 하는 일이에요.",
                        "suited": "well suited for는 '~에 잘 맞는'이에요.",
                        "art": "art는 '예술'이에요. 번역도 예술이래요.",
                    },
                    "placeholder": "핵심어만 보고 해석해 보세요",
                    "point": "핵심어만으로 해석 = 번역은 이 일에 특히 잘 맞는 예술이다.",
                },
                "method": 0,
            },
        ],
    },
    {
        "id": 3,
        "text": S3,
        "model_translation": "위대한 문학 작품은 모방작과 상투적인 표현과 많은 양의 학술 연구와 분석과 학습 가이드를 축적하고 이는 그것을 묻어 버릴 수도 있는 반면, 그 작품의 번역본은 정확히는 그것을 다른 언어로 옮김으로써, 그 작품을 자신의 따분한 명성으로부터 해방시키고 그 돌을 다시 돌답게 만든다.",
        "teaching_value": "high",
        # 찾기 후보는 뜻이 달린 칸 하나와 딱 맞아야 누를 수 있다 — 주어는 덩어리, 동사는 한 단어로 나눠 둔다
        "glosses": [g("while", "~하는 반면 / ~하는 동안"), g("a great work of literature", "위대한 문학 작품"),
                    g("accumulates", "쌓다, 축적하다"), g("imitations", "모방작"), g("clichés", "상투적인 표현"),
                    g("a body of scholarship", "많은 양의 학술 연구"), g("analysis", "분석"), g("study guides", "학습 가이드"),
                    g("may well", "~할 수도 있다"), g("bury", "묻다 · may well bury it = 그것을 묻어 버릴 수도 있다"),
                    g("translations of that work", "그 작품의 번역본"),
                    g("free", "해방시키다 · free A from B = A를 B에서 풀어 주다"), g("its stodgy fame", "그것의 따분한 명성"),
                    g("make", "만들다"), g("the stone", "그 돌"), g("stony", "돌다운"), g("again", "다시"),
                    g("precisely", "바로, 정확히"), g("putting", "옮기는 것 · by putting it in = ~에 옮김으로써"),
                    g("another language", "다른 언어")],
        "steps": [
            # while — 두 가지 뜻
            show("s3_while_know",
                 "while은 '~하는 반면에'와 '~하는 동안에', 두 가지 뜻이 있어요.",
                 button="이미 잘 알고 있어요", detail_button="다음에 또 알려주세요", known="while_two_meanings",
                 point="while = ① ~하는 반면에(대조) ② ~하는 동안에(시간) · 앞뒤가 반대면 '반면에'",
                 highlight=["while"], method=1),
            choice("s3_while",
                   "여기서 while은 무슨 뜻일까요?",
                   [("o0", "~하는 반면에", True), ("o1", "~하는 동안에", False)],
                   "앞은 작품이 묻힌다, 뒤는 번역이 작품을 풀어 준다예요. 서로 반대예요.",
                   why="앞은 작품이 묻혀 버린다, 뒤는 번역이 작품을 풀어 준다예요. 시간이 아니라 서로 반대되는 내용이에요.",
                   highlight=["while"], method=1),
            # 주어+동사 두 쌍
            show("s3_two_pairs",
                 "이 문장은 'while(접속사) + 주어 + 동사, 주어 + 동사' 구조예요. 주어와 동사가 두 쌍 있어요. 각각 찾아볼게요.",
                 button="찾아볼게요", known="clause_pairs", display=S3_SLASH,
                 panel={"kind": "structure", "rows": [
                     {"label": "while", "text": "접속사 · ~하는 반면에", "tone": "hl2"},
                     {"label": "주어 ① + 동사 ①", "text": "?"},
                     {"label": "주어 ② + 동사 ②", "text": "?"},
                 ]},
                 method=1),
            pick("s3_subj1", "while 뒤 첫 번째 주어는 무엇일까요?",
                 ["a great work of literature", "imitations", "a body of scholarship", "study guides"],
                 ["a great work of literature"],
                 "그건 동사 뒤에 나오는 말이에요. while 바로 뒤를 봐요.",
                 "while 바로 뒤 'a great work of literature(위대한 문학 작품)'가 첫 번째 주어예요.",
                 shade=True, skip_with="s3_two_pairs", display=S3_SLASH, method=1),
            pick("s3_verb1", "그럼 이 주어의 동사는 무엇일까요?",
                 ["accumulates", "imitations", "analysis", "bury"],
                 ["accumulates"],
                 "그건 동사가 아니거나, 다른 덩어리의 동사예요. 주어 바로 뒤를 봐요.",
                 "주어 바로 뒤 'accumulates(쌓는다)'가 동사예요. bury는 study guides를 꾸미는 that 덩어리 안의 동사예요.",
                 highlight_alt=["a great work of literature"], skip_with="s3_two_pairs", display=S3_SLASH, method=1),
            pick("s3_subj2", "콤마 뒤 두 번째 주어는 무엇일까요?",
                 ["translations of that work", "its stodgy fame", "the stone", "another language"],
                 ["translations of that work"],
                 "그건 동사 뒤에 나오는 말이에요. 콤마 바로 뒤를 봐요.",
                 "콤마 바로 뒤 'translations of that work(그 작품의 번역본)'가 두 번째 주어예요.",
                 shade=True, highlight_alt=["a great work of literature"], skip_with="s3_two_pairs", display=S3_SLASH, method=1),
            pick("s3_verb2", "두 번째 주어의 동사는 무엇일까요?",
                 ["free", "the stone", "precisely", "putting"],
                 ["free"],
                 "그건 동사가 아니에요. 주어 바로 뒤를 봐요.",
                 "주어 바로 뒤 'free(해방시키다)'가 동사예요. putting은 by 뒤에 붙은 '옮김으로써'예요.",
                 highlight_alt=["translations of that work"], skip_with="s3_two_pairs", display=S3_SLASH, method=1),
            show("s3_pairs",
                 "while 덩어리는 'a great work of literature + accumulates', 메인 문장은 'translations of that work + free'예요.",
                 button="다음",
                 highlight=["a great work of literature", "translations of that work"],
                 highlight_alt=["accumulates", "free"],
                 panel={"kind": "structure", "rows": [
                     {"label": "while", "text": "접속사 · ~하는 반면에"},
                     {"label": "주어 ① + 동사 ①", "text": "a great work of literature + accumulates", "ko": "위대한 문학 작품은 + 쌓는다", "tone": "hl"},
                     {"label": "주어 ② + 동사 ②", "text": "translations of that work + free", "ko": "그 작품의 번역본은 + 풀어 준다", "tone": "hl2"},
                 ]},
                 skip_with="s3_two_pairs", display=S3_SLASH, method=1),
            # 주어·동사 + 목적어 = 핵심어
            pick("s3_keys", "주어와 동사는 핵심어예요. 그럼 주어와 동사를 포함해서 핵심어 6개를 찾아볼까요?",
                 ["while", "a great work of literature", "accumulates", "imitations", "may well", "translations of that work",
                  "free", "its stodgy fame", "again", "precisely"],
                 ["a great work of literature", "accumulates", "imitations", "translations of that work", "free", "its stodgy fame"],
                 "그건 뜻을 덧붙이는 말이라 핵심어가 아니에요. 동사 뒤에 오는 말도 찾아봐요.",
                 "핵심어는 a great work of literature, accumulates, imitations, translations of that work, free, its stodgy fame이에요. 주어·동사와 동사 뒤 목적어예요.",
                 praise="다 찾았어요!",
                 tips=[{"label": "힌트", "hint": True,
                        "text": "동사 뒤에 나오는 명사, 즉 목적어도 보통 핵심어예요."}],
                 method=0),
            choice("s3_trans",
                   "그럼 핵심어를 가지고 이 문장을 해석해 봐요. 문장이 기니까 이번엔 보기를 줄게요. 어떤 뜻일까요?",
                   [("o0", "위대한 문학 작품은 모방작 같은 것들이 쌓이는 반면, 그 번역본은 작품을 따분한 명성에서 풀어 준다", True),
                    ("o1", "위대한 문학 작품이 모방작을 쌓는 동안, 그 번역본은 작품을 더 유명하게 만든다", False),
                    ("o2", "그 번역본은 모방작 같은 것들을 쌓는 반면, 위대한 문학 작품은 따분한 명성에서 벗어난다", False)],
                   "주어 ①은 a great work of literature, 주어 ②는 translations of that work예요. free는 '풀어 주다'예요.",
                   why="while은 '반면에', 주어 ②는 translations of that work, free는 '풀어 주다'예요. 번역본이 작품을 따분한 명성에서 풀어 줘요.",
                   highlight=["a great work of literature", "accumulates", "imitations", "translations of that work", "free", "its stodgy fame"],
                   method=0),
            # 1문장의 두 그룹(익숙해서 안 보임 ↔ 다시 보이게 함)에 literature와 translation을 넣는다
            choice("s3_sort_lit",
                   "1문장의 두 그룹을 다시 가져왔어요. literature(문학 작품)는 어느 그룹일까요?",
                   [("o0", SORT3_LEFT, True), ("o1", SORT3_RIGHT, False)],
                   "위대한 작품은 모방작과 연구가 쌓여 묻혀 버린대요. 익숙해져서 안 보이는 쪽이에요.",
                   panel={**board3([], []), "sort": {"words": ["literature"], "left": SORT3_LEFT, "right": SORT3_RIGHT}},
                   method=1),
            choice("s3_sort_trans",
                   "그럼 translation(번역)은 어느 그룹일까요?",
                   [("o0", SORT3_LEFT, False), ("o1", SORT3_RIGHT, True)],
                   "번역은 작품을 따분한 명성에서 풀어 주고 돌을 다시 돌답게 만들어요. 다시 보이게 하는 쪽이에요.",
                   panel={**board3(["literature"], []), "sort": {"words": ["translation"], "left": SORT3_LEFT, "right": SORT3_RIGHT}},
                   method=1),
            pick("s3_art", "아까 예술은 익숙한 걸 다시 보이게 만든다고 했죠. 이 문장에서 예술에 해당하는 걸 찾아볼까요?",
                 ["a great work of literature", "study guides", "translations of that work", "another language"],
                 ["translations of that work"],
                 "그건 작품을 묻어 버리거나, 그냥 옮길 곳이에요. 작품을 풀어 주는 쪽을 찾아봐요.",
                 "'translations of that work', 번역본이 예술 쪽이에요. 작품을 다시 돌답게, 생생하게 보이게 해요.",
                 shade=True,
                 panel=board3(["literature"], ["translation"]),
                 method=1),
        ],
    },
    {
        "id": 4,
        "text": "A bad text is one that, in Berman’s terms, lacks “native strangeness”—and when you translate it, nothing happens.",
        "model_translation": "안 좋은 텍스트란 Berman의 용어로 '본래의 낯섦'이 결여된 것이며, 여러분이 그것을 번역할 때 아무 일도 일어나지 않는다.",
        "teaching_value": "high",
        "glosses": [g("A bad text", "안 좋은 글"), g("one", "것 · 앞의 text를 다시 받는 말"), g("that", "~한 (one을 꾸밈)"),
                    g("in Berman’s terms", "Berman의 용어로"), g("lacks", "~이 없다, 결여되다"),
                    g("native strangeness", "본래의 낯섦 · 작품이 원래 가진 낯선 느낌"), g("when", "~할 때"), g("you", "여러분, 사람"),
                    g("translate", "번역하다"), g("nothing happens", "아무 일도 일어나지 않는다")],
        "steps": [
            # one = 숫자 1이 아니라 앞의 text를 받는 말 (39번의 one '누구든'과도 다르다)
            choice("s4_one",
                   "여기서 one은 무슨 뜻일까요?",
                   [("o0", "숫자 1, 하나", False), ("o1", "앞의 text를 다시 받는 '것(글)'", True), ("o2", "누구든, 사람", False)],
                   "one 앞에 'A bad text'가 있어요. 같은 말을 또 쓰지 않으려고 one으로 받아요.",
                   why="one 앞에 'A bad text'가 있어요. 'a text'를 또 쓰지 않으려고 one으로 받은 거예요.",
                   highlight=["one"], faded=[S4_FADED],
                   tips=[{"label": "one 세 가지", "mark": "one",
                          "text": "one은 ① 숫자 1 ② 앞에 나온 명사를 다시 받는 '것' ③ 일반적인 '사람, 누구든'으로 쓰여요. 앞에 같은 종류의 명사가 있으면 ②예요."}],
                   method=1),
            choice("s4_lacks",
                   "그럼 안 좋은 글(a bad text)은 어떤 글이래요?",
                   [("o0", "'본래의 낯섦'이 없는 글", True), ("o1", "'본래의 낯섦'이 너무 많은 글", False), ("o2", "Berman이 쓴 글", False)],
                   "lacks는 '~이 없다'예요. 콤마 사이 'in Berman’s terms'는 건너뛰고 읽어요.",
                   why="lacks는 '~이 없다'예요. 콤마 사이 'in Berman’s terms(Berman의 용어로)'는 빼도 되는 삽입이에요.",
                   highlight=["A bad text is one that", "lacks “native strangeness”"], faded=[S4_FADED],
                   method=1),
            # native strangeness는 좋은 말일까 — bad text(−)가 lacks(−)하는 것 → +
            choice("s4_sign",
                   "그럼 native strangeness(본래의 낯섦)는 좋은 말일까요, 나쁜 말일까요?",
                   [("o0", "좋은 말 (+)", True), ("o1", "나쁜 말 (−)", False)],
                   "안 좋은 글(a bad text)에 그게 부족하대요(lacks). 부족하면 안 좋은 거라면, 있으면 어떨까요?",
                   why="안 좋은 글(a bad text)은 그게 부족한(lacks) 글이에요. 부족해서 안 좋은 거라면, 있어야 좋은 거예요.",
                   highlight=["A bad text", "lacks", "native strangeness"], faded=[S4_FADED],
                   method=1),
            show("s4_sign_why",
                 "bad text는 −, lacks(부족하다)도 −예요. 안 좋은 글은 이게 부족한 거니까, native strangeness는 좋은 말(+)이에요.",
                 button="다음",
                 signs=[{"text": "A bad text", "sign": "−"}, {"text": "lacks", "sign": "−"},
                        {"text": "native strangeness", "sign": "+"}],
                 faded=[S4_FADED],
                 method=1),
            # native strangeness를 1문장의 두 그룹에 — 익숙해진 것의 반대 → 다시 보이게 하는 쪽
            choice("s4_sort",
                   "native strangeness(본래의 낯섦)는 1문장의 두 그룹 중 어느 쪽일까요?",
                   [("o0", SORT3_LEFT, False), ("o1", SORT3_RIGHT, True)],
                   "domesticated는 '너무 익숙해진'이에요. 낯섦은 그 반대예요.",
                   why="domesticated는 '너무 익숙해진'이에요. 낯섦은 그 반대라, 익숙해서 안 보이는 쪽이 아니에요.",
                   panel={**board3(["literature"], ["translation"]),
                          "sort": {"words": ["native strangeness"], "left": SORT3_LEFT, "right": SORT3_RIGHT}},
                   highlight=["native strangeness"], faded=[S4_FADED],
                   method=1),
            choice("s4_nothing",
                   "그런 글을 번역하면 어떻게 된대요?",
                   [("o0", "더 낯설어진다", False), ("o1", "아무 일도 일어나지 않는다", True), ("o2", "더 유명해진다", False)],
                   "대시 뒤 'when you translate it'의 it은 a bad text예요. 그 뒤를 봐요.",
                   why="낯섦이 없는 글은 번역이 살려 낼 게 없어요. 대시 뒤 'nothing happens'를 봐요.",
                   highlight=["when you translate it, nothing happens"], faded=[S4_FADED],
                   tips=[{"label": "it", "mark": "it",
                          "text": "translate it의 it은 a bad text, 안 좋은 글이에요."}],
                   method=1),
            show("s4_why",
                 "번역은 작품 안의 낯섦을 살려 내는 일이에요. 그래서 낯섦은 없애거나 극복할 게 아니라, 좋은 글에 꼭 있어야 하는 거예요.",
                 button="다음",
                 panel=board3(["literature"], ["translation", "native strangeness"]),
                 faded=[S4_FADED],
                 method=1),
            pick("s4_pick", "이 문장의 핵심어 4개를 찾아볼까요?",
                 ["A bad text", "in Berman’s terms", "lacks", "native strangeness", "when", "you", "nothing happens"],
                 ["A bad text", "lacks", "native strangeness", "nothing happens"],
                 "그건 뜻을 덧붙이는 말이라 핵심어가 아니에요. 어떤 글이 무엇이 없고, 그래서 어떻게 되는지 찾아봐요.",
                 "핵심어는 A bad text, lacks, native strangeness, nothing happens예요. 안 좋은 글은 낯섦이 없어서 번역해도 아무 일도 없어요.",
                 praise="다 찾았어요!", faded=[S4_FADED], method=0),
            {
                "id": "s4_keys", "type": "translate", "interaction": "free_translation",
                "model": "안 좋은 글은 본래의 낯섦이 없어서, 번역해도 아무 일도 일어나지 않는다.",
                "rules": [
                    {"id": "bad", "need": ["안 좋", "나쁜", "좋지 않", "형편없", "별로"], "fix": "안 좋은 글은"},
                    {"id": "strange", "need": ["낯섦", "낯선", "낯설", "이질", "생소", "새로운 느낌"], "fix": "본래의 낯섦이"},
                    {"id": "lacks", "need": ["없", "결여", "부족", "모자"], "wrong": ["많"], "fix": "없어서"},
                    {"id": "nothing", "need": ["아무 일", "아무것도", "일어나지 않", "변화가 없", "변하지 않", "소용없"], "fix": "아무 일도 일어나지 않는다"},
                ],
                "highlight": ["A bad text", "lacks", "native strangeness", "nothing happens"],
                "faded": [S4_FADED],
                "brief": {
                    "ask": "그럼 이 핵심어만 가지고 문장을 자유롭게 해석해 봐요.",
                    "praise": "잘 해석했어요! 핵심어만으로도 뜻이 잡혀요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "bad": "A bad text는 '안 좋은 글'이에요.",
                        "strange": "native strangeness는 '본래의 낯섦', 작품이 원래 가진 낯선 느낌이에요.",
                        "lacks": "lacks는 '~이 없다'예요. 낯섦이 없는 글이에요.",
                        "nothing": "nothing happens는 '아무 일도 일어나지 않는다'예요.",
                    },
                    "placeholder": "핵심어만 보고 해석해 보세요",
                    "point": "핵심어만으로 해석 = 안 좋은 글은 본래의 낯섦이 없어서, 번역해도 아무 일도 일어나지 않는다.",
                },
                "method": 0,
            },
        ],
    },
    {
        "id": 5,
        # 원문은 한 문장이지만 길어서 콜론(:)에서 나눈다 — 콜론 뒤 인용은 문장 6
        "text": S5,
        "model_translation": "진정한 예술 작품의 번역은 그것이 작품 안에 이미 내재된 자질을 강화하고 높이기 때문에 의미 있다.",
        "teaching_value": "high",
        "glosses": [g("The translation of a true work of art", "진정한 예술 작품의 번역"), g("significant", "의미 있는, 중요한"),
                    g("because", "~ 때문에"), g("reinforces", "강화하다"), g("enhances", "높이다, 더 좋게 하다"),
                    g("qualities", "자질, 특성"), g("already", "이미"), g("inherent", "내재된 · inherent in it = 그것 안에 원래 있는")],
        "steps": [
            pick("s5_subj", "이 문장의 주어는 무엇일까요?",
                 ["The translation of a true work of art", "significant", "qualities"],
                 ["The translation of a true work of art"],
                 "그건 동사 뒤에 나오는 말이에요. is 앞 덩어리를 봐요.",
                 "is 앞 덩어리 'The translation of a true work of art(진정한 예술 작품의 번역)'가 주어예요.",
                 shade=True, method=1),
            choice("s5_it",
                   "because 바로 뒤 it은 무엇을 가리킬까요?",
                   [("o0", "번역 (The translation)", True), ("o1", "예술 작품 (a true work of art)", False), ("o2", "자질 (qualities)", False)],
                   "because 뒤 it은 앞 문장의 주어를 다시 받아요.",
                   why="because 뒤 it은 앞 주어, 즉 '번역'이 무언가를 강화한다는 말이에요. 맨 끝 'in it'의 it이 작품이에요.",
                   highlight=["because it"],
                   tips=[{"label": "it 두 개", "mark": "it",
                          "text": "이 문장에는 it이 두 번 나와요. because 뒤 it은 '번역', 맨 끝 in it의 it은 '작품'이에요."}],
                   method=1),
            choice("s5_inherent",
                   "번역이 강화하는 자질(qualities)은 원래 어디에 있던 걸까요?",
                   [("o0", "작품 안에 이미 있던 것", True), ("o1", "번역가가 새로 더한 것", False), ("o2", "다른 언어에 있던 것", False)],
                   "already inherent in it은 '그 안에 이미 내재된'이에요. it은 작품이에요.",
                   why="'already inherent in it'은 '그것(작품) 안에 이미 내재된'이에요. 번역이 새로 만드는 게 아니에요.",
                   highlight=["qualities already inherent in it"],
                   method=1),
            show("s5_link",
                 "작품 안에 이미 있던 자질, 바로 앞 문장의 native strangeness(본래의 낯섦)예요. 번역은 그걸 더 강하게 살려 줘요.",
                 button="다음",
                 signs=[{"text": "reinforces", "sign": "+"}, {"text": "enhances", "sign": "+"}],
                 highlight=["qualities already inherent in it"],
                 method=1),
            pick("s5_pick", "이 문장의 핵심어 6개를 찾아볼까요?",
                 ["The translation of a true work of art", "significant", "because", "reinforces", "enhances", "qualities",
                  "already", "inherent"],
                 ["The translation of a true work of art", "significant", "reinforces", "enhances", "qualities", "inherent"],
                 "그건 뜻을 덧붙이는 말이라 핵심어가 아니에요. 주어·동사와 동사 뒤 목적어를 찾아봐요.",
                 "핵심어는 The translation of a true work of art, significant, reinforces, enhances, qualities, inherent예요.",
                 praise="다 찾았어요!", method=0),
            {
                "id": "s5_keys", "type": "translate", "interaction": "free_translation",
                "model": "진정한 예술 작품의 번역은 작품 안에 이미 있는 자질을 강화하고 높여 주기 때문에 의미 있다.",
                "rules": [
                    {"id": "translation", "need": ["번역"], "fix": "진정한 예술 작품의 번역은"},
                    {"id": "inherent", "need": ["이미", "내재", "원래", "본래", "안에 있", "지닌", "가진"], "fix": "작품 안에 이미 있는"},
                    {"id": "qualities", "need": ["자질", "특성", "성질", "특징", "장점", "가치"], "fix": "자질을"},
                    {"id": "reinforce", "need": ["강화", "높", "키우", "살리", "강하게", "북돋", "향상", "더 좋"], "fix": "강화하고 높여 주기"},
                    {"id": "significant", "need": ["의미", "중요", "가치 있", "뜻깊"], "fix": "의미 있다"},
                ],
                "highlight": ["The translation of a true work of art", "significant", "reinforces", "enhances", "qualities", "inherent"],
                "brief": {
                    "ask": "그럼 이 핵심어만 가지고 문장을 자유롭게 해석해 봐요.",
                    "praise": "잘 해석했어요! 핵심어만으로도 뜻이 잡혀요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "translation": "The translation of a true work of art는 '진정한 예술 작품의 번역'이에요.",
                        "inherent": "already inherent in it은 '작품 안에 이미 있는'이에요.",
                        "qualities": "qualities는 '자질, 특성'이에요.",
                        "reinforce": "reinforces and enhances는 '강화하고 높여 준다'예요.",
                        "significant": "significant는 '의미 있는, 중요한'이에요.",
                    },
                    "placeholder": "핵심어만 보고 해석해 보세요",
                    "point": "핵심어만으로 해석 = 진정한 예술 작품의 번역은 작품 안에 이미 있는 자질을 강화하고 높여 주기 때문에 의미 있다.",
                },
                "method": 0,
            },
        ],
    },
    {
        "id": 6,
        "text": S6,
        "model_translation": "\"번역은 임시방편이 아니라, 한 작품이 우리에게 '낯선 것'으로 다가오는 존재 양식이다.\" (Heyvaert에 의해 '이질적인'으로 번역되었지만, 나는 그것에 대해 확신하지 못한다.)",
        "teaching_value": "high",
        "glosses": [g("translation", "번역"), g("not", "~이 아니라 · not A but B = A가 아니라 B"), g("makeshift", "임시방편"),
                    g("but", "~이다 · not A but B"), g("the mode of existence", "존재 방식"), g("by which", "그것을 통해"),
                    g("a work", "작품"), g("reaches us", "우리에게 다가오다"), g("étrange", "낯선 · 프랑스어, 영어 strange"),
                    g("translated by Heyvaert", "Heyvaert가 번역한"), g("foreign", "이질적인, 외국의"),
                    g("not sure", "확신하지 못하는")],
        "steps": [
            choice("s6_notbut",
                   "'not A, but B'는 무슨 뜻일까요?",
                   [("o0", "A가 아니라 B", True), ("o1", "A도 B도 아니다", False), ("o2", "A이고 또 B이다", False)],
                   "not 뒤가 A, but 뒤가 B예요. 앞은 부정하고 뒤를 말해요.",
                   why="not A, but B는 앞(A)을 부정하고 뒤(B)를 말하는 구조예요. 뒤가 글쓴이가 하고 싶은 말이에요.",
                   highlight=["not a makeshift", "but the mode of existence"],
                   faded=[S6_FADED], faded_note=S6_FADED_NOTE, faded_tip=S6_FADED_TIP,
                   method=1),
            choice("s6_what",
                   "그럼 번역은 임시방편이 아니라 무엇이래요?",
                   [("o0", "작품을 쉽게 바꿔 주는 도구", False), ("o1", "작품이 우리에게 낯설게 다가오는 방식", True),
                    ("o2", "원문을 대신하는 임시 수단", False)],
                   "but 뒤를 봐요. étrange는 프랑스어로 strange예요.",
                   why="but 뒤 'the mode of existence by which a work reaches us as étrange'예요. étrange는 프랑스어로 strange예요.",
                   highlight=["the mode of existence by which a work reaches us as étrange"],
                   faded=[S6_FADED], faded_note=S6_FADED_NOTE,
                   method=1),
            show("s6_link",
                 "étrange는 '낯선'이에요. 번역 덕분에 작품이 다시 낯설게, 즉 생생하게 우리에게 다가온다는 말이에요.",
                 button="다음",
                 signs=[{"text": "makeshift", "sign": "−"}, {"text": "étrange", "sign": "+"}],
                 faded=[S6_FADED], faded_note=S6_FADED_NOTE,
                 method=1),
            pick("s6_pick", "이 문장의 핵심어 5개를 찾아볼까요?",
                 ["translation", "makeshift", "the mode of existence", "by which", "reaches us", "étrange", "foreign"],
                 ["translation", "makeshift", "the mode of existence", "reaches us", "étrange"],
                 "그건 뜻을 덧붙이거나 건너뛰어도 되는 말이에요. not A but B의 A와 B를 찾아봐요.",
                 "핵심어는 translation, makeshift, the mode of existence, reaches us, étrange예요.",
                 praise="다 찾았어요!", faded=[S6_FADED], faded_note=S6_FADED_NOTE, method=0),
            {
                "id": "s6_keys", "type": "translate", "interaction": "free_translation",
                "model": "번역은 임시방편이 아니라, 작품이 우리에게 낯설게 다가오는 방식이다.",
                "rules": [
                    {"id": "translation", "need": ["번역"], "fix": "번역은"},
                    {"id": "makeshift", "need": ["임시", "땜", "대용", "대신", "급조", "임시방편"], "fix": "임시방편이"},
                    {"id": "notbut", "need": ["아니라", "아니고", "아닌"], "wrong": ["이고 또", "도 아니"], "fix": "아니라"},
                    {"id": "strange", "need": ["낯설", "낯선", "낯섦", "이질", "생소", "새롭"], "fix": "낯설게"},
                    {"id": "reach", "need": ["다가", "전해", "도달", "닿", "오는", "만나"], "fix": "다가오는 방식이다"},
                ],
                "highlight": ["translation", "makeshift", "the mode of existence", "reaches us", "étrange"],
                "faded": [S6_FADED], "faded_note": S6_FADED_NOTE,
                "brief": {
                    "ask": "그럼 이 핵심어만 가지고 문장을 자유롭게 해석해 봐요.",
                    "praise": "잘 해석했어요! 핵심어만으로도 뜻이 잡혀요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "translation": "translation은 '번역'이에요.",
                        "makeshift": "makeshift는 '임시방편'이에요.",
                        "notbut": "not A, but B는 'A가 아니라 B'예요.",
                        "strange": "étrange는 '낯선'이에요. 영어 strange와 같아요.",
                        "reach": "reaches us는 '우리에게 다가온다'예요. the mode of existence는 그 '방식'이에요.",
                    },
                    "placeholder": "핵심어만 보고 해석해 보세요",
                    "point": "핵심어만으로 해석 = 번역은 임시방편이 아니라, 작품이 우리에게 낯설게 다가오는 방식이다.",
                },
                "method": 0,
            },
        ],
    },
    {
        "id": 7,
        "text": S7,
        "model_translation": "Wilson이 말했듯, 번역은 작품을 '더 낯설게, 그리고 새롭게 낯설게 보이도록' 한다.",
        "teaching_value": "high",
        "glosses": [g("As Wilson put it", "Wilson이 말했듯 · put = 말하다, 표현하다"), g("translation", "번역"),
                    g("makes", "만들다 · make + 목적어 + 동사원형 = ~가 …하게 만들다"), g("the work", "그 작품"),
                    g("seem", "~처럼 보이다"), g("more strange", "더 낯선"), g("and", "그리고"), g("newly strange", "새롭게 낯선")],
        "steps": [
            choice("s7_make",
                   "번역은 작품(the work)을 어떻게 보이게 만든대요?",
                   [("o0", "더 익숙하고 친근하게", False), ("o1", "더 쉽고 다가가기 쉽게", False), ("o2", "더 낯설게, 새롭게 낯설게", True)],
                   "make + 목적어 + seem은 '~가 …하게 보이게 만들다'예요. seem 뒤를 봐요.",
                   why="'makes the work seem more strange'는 '작품을 더 낯설게 보이게 만든다'예요. 익숙하게 만드는 게 아니에요.",
                   highlight=["makes the work “seem more strange, and newly strange.”"],
                   tips=[{"label": "make + 목적어 + 동사원형", "mark": "makes",
                          "text": "make A do는 'A가 ~하게 만들다'예요. 여기서는 makes the work seem, '작품이 ~하게 보이도록 만든다'예요."},
                         {"label": "As Wilson put it", "mark": "As Wilson put it",
                          "text": "'Wilson이 말했듯'이에요. put은 여기서 '두다'가 아니라 '말하다, 표현하다'예요."}],
                   method=1),
            choice("s7_sort",
                   "'seem more strange(더 낯설게 보인다)'는 1문장의 두 그룹 중 어느 쪽일까요?",
                   [("o0", SORT3_LEFT, False), ("o1", SORT3_RIGHT, True)],
                   "낯설게 보인다는 건 익숙해서 안 보이는 것의 반대예요.",
                   why="낯설게 보인다는 건 다시 눈에 들어온다는 말이에요. 익숙해서 안 보이는 쪽의 반대예요.",
                   panel={**board3(["literature"], ["translation", "native strangeness"]),
                          "sort": {"words": ["seem more strange"], "left": SORT3_LEFT, "right": SORT3_RIGHT}},
                   method=1),
            pick("s7_pick", "이 문장의 핵심어 5개를 찾아볼까요?",
                 ["As Wilson put it", "translation", "makes", "the work", "seem", "more strange", "and", "newly strange"],
                 ["translation", "makes", "the work", "more strange", "newly strange"],
                 "그건 뜻을 덧붙이는 말이라 핵심어가 아니에요. 무엇이 무엇을 어떻게 만드는지 찾아봐요.",
                 "핵심어는 translation, makes, the work, more strange, newly strange예요.",
                 praise="다 찾았어요!", method=0),
            {
                "id": "s7_keys", "type": "translate", "interaction": "free_translation",
                "model": "번역은 작품을 더 낯설게, 그리고 새롭게 낯설게 보이게 만든다.",
                "rules": [
                    {"id": "translation", "need": ["번역"], "fix": "번역은"},
                    {"id": "work", "need": ["작품", "글"], "fix": "작품을"},
                    {"id": "strange", "need": ["낯설", "낯선", "이질", "생소"], "wrong": ["익숙", "친근", "쉽게"], "fix": "더 낯설게"},
                    {"id": "newly", "need": ["새롭", "새로", "다시"], "fix": "새롭게 낯설게"},
                    {"id": "make", "need": ["만든", "만들", "보이게", "하게 한", "보이도록"], "fix": "보이게 만든다"},
                ],
                "highlight": ["translation", "makes", "the work", "more strange", "newly strange"],
                "brief": {
                    "ask": "그럼 이 핵심어만 가지고 문장을 자유롭게 해석해 봐요.",
                    "praise": "잘 해석했어요! 핵심어만으로도 뜻이 잡혀요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "translation": "translation은 '번역'이에요.",
                        "work": "the work는 '그 작품'이에요.",
                        "strange": "more strange는 '더 낯선'이에요. 익숙하게 만드는 게 아니에요.",
                        "newly": "newly strange는 '새롭게 낯선'이에요.",
                        "make": "makes the work seem은 '작품이 ~하게 보이도록 만든다'예요.",
                    },
                    "placeholder": "핵심어만 보고 해석해 보세요",
                    "point": "핵심어만으로 해석 = 번역은 작품을 더 낯설게, 그리고 새롭게 낯설게 보이게 만든다.",
                },
                "method": 0,
            },
            # 글 전체를 한 줄로 — 제목을 고르기 전에 글쓴이의 생각을 묶는다
            show("s7_gist",
                 "다 모으면 이래요. 너무 익숙해진 작품은 안 보이게 되는데, 번역은 작품의 낯섦을 살려 다시 생생하게 보이게 해요.",
                 button="문제 풀러 갈게요",
                 panel={**board3(["literature"], ["translation", "native strangeness", "seem more strange"]),
                        "caption": "번역 = 익숙해진 작품을 다시 낯설게, 생생하게"},
                 method=1),
        ],
    },
]

OPTIONS = [
    ("1", "Translation’s True Calling: Restoring Vitality of the Unfamiliar", ["Translation", "Restoring Vitality", "Unfamiliar"],
     "번역의 진짜 소명: 낯선 것의 생기를 되살리기", True),
    ("2", "Is Refining the Original Tone Always Better for Accessibility?", ["Refining", "Accessibility"],
     "원래 어조를 다듬는 게 늘 접근성에 더 좋을까?", False),
    ("3", "How Literary Guides Deprive Readers of Art’s True Rawness", ["Literary Guides", "Deprive"],
     "학습 가이드는 어떻게 독자에게서 예술의 날것을 빼앗는가", False),
    ("4", "The Role of Translation in Distributing Regional Literature", ["Translation", "Distributing Regional Literature"],
     "지역 문학을 퍼뜨리는 번역의 역할", False),
    ("5", "Overcoming Native Strangeness for Successful Translation", ["Overcoming", "Native Strangeness"],
     "성공적인 번역을 위해 본래의 낯섦 극복하기", False),
]

exam = {
    "question": "다음 글의 제목으로 가장 적절한 것은? [3점]",
    "analysis_first": True,
    "glosses": [g("True Calling", "진짜 소명"), g("Vitality", "생기, 활력"), g("Unfamiliar", "낯선 것"), g("Refining", "다듬기"),
                g("Accessibility", "접근성"), g("Deprive", "빼앗다"), g("Rawness", "날것, 생생함"),
                g("Distributing", "퍼뜨리기"), g("Regional Literature", "지역 문학"), g("Overcoming", "극복하기"),
                g("Native Strangeness", "본래의 낯섦")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": {
        "ask": "핵심어(translation, strange)를 떠올리며 제목을 골라 봐요.",
        "first_correct": "맞았어요!",
        "first_wrong": "아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.",
        "final_correct": "정답이에요!",
        "answer_explain": "정답이에요! 번역은 너무 익숙해진 작품을 다시 낯설게 만들어 살려 내요. 그게 번역의 진짜 소명이에요.",
        "final_wrong": "정답은 ①이에요.",
        "option_feedback": {
            "2": "글은 원래 어조를 다듬는 이야기가 아니에요. 오히려 다가가기 쉬움(accessible)은 아니라고 했어요.",
            "3": "학습 가이드가 작품을 묻어 버릴 수 있다는 말은 잠깐 나와요. 글의 중심은 번역이에요.",
            "4": "translation이 들어가서 헷갈렸죠. 지역 문학을 퍼뜨리는 이야기는 글에 없어요.",
            "5": "글은 '본래의 낯섦'을 극복하는 게 아니라 살려야 한다고 해요. 방향이 반대예요.",
        },
        "ask_first": "실제 시험처럼 풀어 봐요. 위 보기에서 답을 골라요.",
    },
}

# 학생이 막힐 만한 단어는 다 누를 수 있게
MORE_GLOSSES = {
    1: [("just", "그저"), ("we", "우리")],
    2: [("perhaps", "아마도"), ("especially", "특히")],
}
for s_ in sentences:
    have = {x["en"].lower() for x in s_["glosses"]}
    s_["glosses"] += [g(en, ko) for en, ko in MORE_GLOSSES.get(s_["id"], []) if en.lower() not in have]

lesson = {
    "id": ID, "kind": "policy", "version": "0.1",
    "source": "2026년 3월 고3 전국연합학력평가 영어 24번 (글의 제목, 3점)",
    "brief": {"topic": "제목 푸는 법: 핵심어 찾기 → 글쓴이 생각 잡기 → 보기와 맞춰 보기", "closing": "수고 인사"},
    "method": {"type": "title", "labels": ["핵심어 찾기", "글쓴이 생각 잡기"], "intro_times": 3},
    "read_button": "분석하러 갈게요",
    "read_first": True,
    "intro": [
        {"id": "topic", "type": "say", "button": "네",
         "brief": {"say": "너무 익숙한 것은 왜 눈에 안 들어올까요? 이번 글은 번역과 낯섦의 관계를 다뤄요."}},
        {"id": "method1", "type": "say", "button": "좋아요",
         "brief": {"say": "제목 문제는 글 전체를 한 줄로 묶는 말을 찾는 거예요. 문장마다 핵심어를 찾고 글쓴이 생각을 잡아 볼게요."}},
    ],
    "exam": exam,
    "key_words": {
        # clichés, stodgy는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
        "passage": [g("domesticated", "길든, 익숙해진"), g("evaporate", "증발하다, 사라지다"), g("take ~ for granted", "~을 당연하게 여기다"),
                    g("restore", "회복시키다"), g("visibility", "눈에 보임, 가시성"), g("accumulate", "축적하다"),
                    g("imitation", "모방작"), g("scholarship", "학술 연구"), g("lack", "~이 없다"), g("reinforce", "강화하다"),
                    g("enhance", "높이다"), g("inherent", "내재된"), g("makeshift", "임시방편")],
        "options": [g("vitality", "생기, 활력"), g("deprive", "빼앗다"), g("overcome", "극복하다")],
    },
    "context": {"mode": "paper_review", "exam_relevance": "high", "time_budget": "normal"},
    "item": {"english_difficulty": "high", "conceptual_difficulty": "high", "background_knowledge_required": "low",
             "exam_importance": "high", "teaching_value": "high", "intervention_density": "normal"},
    "sentences": sentences,
    "passage_on_try": True,
}

json.dump(lesson, open(f"{ROOT}/content/tutor/policy-lessons/{ID}.json", "w"), ensure_ascii=False, indent=2)

ref = json.load(open(f"{ROOT}/content/tutor/policy-copy/dajung/moeui-2026-03-21-music-researchers.json"))
steps = {st["id"]: copy.deepcopy(st["brief"]) for s in sentences for st in s["steps"]}
c = {
    "lesson": ID, "character": "dajung", "note": "생성물",
    "topic_intro": "제목 푸는 법",
    "closing": ref["closing"],
    "helps": {h["id"]: {"answer": h["brief"]} for s_ in sentences for h in s_.get("helps", [])},
    "steps": steps,
    "exam": {k: v for k, v in exam["brief"].items()},
    "intro": {i["id"]: dict(i["brief"]) for i in lesson["intro"]},
    "ending": {**ref["ending"], "wrong": "이번엔 한 번 헷갈렸으니 {weeks} 뒤에 다시 한번 볼 거예요."},
}
json.dump(c, open(f"{ROOT}/content/tutor/policy-copy/dajung/{ID}.json", "w"), ensure_ascii=False, indent=2)
print("ok", ID)
