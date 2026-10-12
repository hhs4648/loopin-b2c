"""2026년 3월 33번 레슨 + 대사를 만든다 (빈칸 추론, 3점).

레슨 JSON(content/tutor/policy-lessons/…)과 대사(content/tutor/policy-copy/dajung/…)는 이 스크립트의
생성물이다. 고칠 때는 여기를 고치고 다시 돌린 뒤 도장을 찍는다:

    python3 scripts/lessons/gen_moeui_2026_03_33.py
    npm run policy:copy stamp moeui-2026-03-33-profound-building

빈칸 푸는 법: ① 빈칸 문장부터 보고 무엇을 찾을지 정하기 ② 핵심어로 글쓴이 주장 잡기
③ 빈칸이 주장과 같은 쪽인지 반대 의견인지 파악하기(선생님 보충, 2026-10-12) ④ 그걸 다른 말로 바꿔 쓴 보기 찾기.
정답 ③ an extension of human bodily and mental actions and capabilities.
많이 고른 오답 ④(설계자의 미적 취향) 22.1% — 글에 designer가 많이 나와서. ② 18.0%.
"""
import copy
import json
import os

ID = "moeui-2026-03-33-profound-building"
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


POINTS = {
    "s1_blank": "빈칸 문제는 빈칸 문장부터 — 'A profound building is ____' → 좋은 건물이 어떤 건물인지 찾는다",
    "s1_what": "architectural structures = spatial choreography that guides action (행동을 이끄는 공간 연출)",
    "s2_body": "movement and behavior(움직임·행동) = 몸 쪽",
    "s2_mind": "perceptions, emotions and feelings(지각·감정·느낌) = 마음 쪽",
    "s3_designer": "좋은 설계자는 자기 취향이 아니라 사용자의 행동과 욕구(human behavior and desire)를 알아챈다",
    "s4_behalf": "on behalf of the future dweller = 미래에 살 사람을 대신해서",
    "s5_where": "올바른 창문 = 사는 사람이 내다보고 싶은 바로 그곳",
    "s6_same": "계단도 사는 사람이 오르내리고 싶은 곳 — 창문과 같은 원리",
    "s7_why": "as = ~이기 때문에 · 성공적인 건축은 말없이도 쓰임새를 드러낸다",
    "s8_side": "빈칸이 주장과 같은 쪽인지 반대 쪽인지 먼저 — profound(+) 건물을 설명하고 반전 단서가 없으니 주장과 같은 쪽",
    "s8_gist": "글 전체 = 좋은 건물은 사는 사람의 몸(행동)과 마음(느낌)에 꼭 맞는다",
}

BLANK = "A profound building is ________."
S = [
    "All architectural structures are forms of spatial choreography that guides action; space facilitates or prohibits, encourages or prevents, invites or inhibits.",
    "This choreography predetermines patterns of movement and behavior, but it also guides experiential characteristics, perceptions, imageries, emotions and feelings.",
    "A sensitive and empathic designer intuits human behavior and desire, and this intuitive architectural scripting resonates with the actual user/occupant’s natural and instinctual needs and intentions.",
    "While designing a house, the designer lives, uses and feels the non-existent house in his imagination on behalf of the future dweller.",
    "A correctly placed window is located exactly where the occupant wishes to look out into the garden, or where daylight is needed.",
    "The stairway is located where the dweller wishes to enter the floor above or below.",
    "Successful architecture does not need manuals or signage for its use, as it reveals its very structure and use in a wordless manner.",
    BLANK,
]
KO = [
    "모든 건축 구조물은 행동을 유도하는 공간적 연출의 형태인데, 공간은 촉진하거나 금지하고, 권장하거나 막고, 초대하거나 억제한다.",
    "이러한 연출은 움직임과 행동 양식을 미리 결정하지만, 그것은 또한 경험적 특성, 지각, 심상, 감정과 느낌을 유도한다.",
    "세심하고 공감할 수 있는 설계자는 인간의 행동과 욕망을 직관으로 알며, 이러한 직관적인 건축적 대본 쓰기는 실제 사용자 또는 입주자의 자연스럽고 본능적인 욕구 및 의도와 공명한다.",
    "주택을 설계하는 동안, 설계자는 자신의 상상 속에서 미래 거주자를 대신하여 존재하지 않는 집을 경험하고, 사용하고, 느낀다.",
    "올바르게 배치된 창문은 입주자가 정원을 내다보고 싶어 하는, 또는 햇빛이 필요한 바로 그곳에 설치된다.",
    "계단은 거주자가 위층이나 아래층으로 들어가고 싶어 하는 곳에 설치된다.",
    "성공적인 건축에는 그것의 사용을 위한 설명서나 표지판이 필요하지 않은데, 성공적인 건축은 무언의 방식으로 바로 그 구조와 용도를 드러내기 때문이다.",
    "심오한 건물은 ________이다.",
]

BODY = "왼쪽 · 몸 (행동)"
MIND = "오른쪽 · 마음 (느낌)"


def board(left, right, caption=None):
    p = {"kind": "groups", "title": "공간이 이끄는 것", "between": "+",
         "left": {"label": "몸 · 움직임과 행동", "words": [{"text": w, "fresh": True} for w in left]},
         "right": {"label": "마음 · 지각과 느낌", "words": [{"text": w, "fresh": True} for w in right]}}
    if caption:
        p["caption"] = caption
    return p


sentences = [
    {
        "id": 1, "text": S[0], "model_translation": KO[0], "teaching_value": "high",
        # choreography는 시험지 아래 *로 풀어 준 단어 — 뜻만 단다
        "glosses": [g("architectural structures", "건축 구조물"), g("forms of", "~의 형태"), g("spatial", "공간의"),
                    g("choreography", "연출"), g("guides action", "행동을 이끌다"), g("space", "공간"),
                    g("facilitates", "촉진하다, 쉽게 하다"), g("prohibits", "금지하다"), g("encourages", "권장하다"),
                    g("prevents", "막다"), g("invites", "초대하다"), g("inhibits", "억제하다"),
                    g("A profound building", "심오한(훌륭한) 건물")],
        "steps": [
            # 빈칸 문장부터 — 앞 문장들에서 무엇을 찾을지 정한다
            choice("s1_blank",
                   "빈칸 문제는 빈칸 문장부터 봐요. 그럼 글에서 무엇을 찾아야 할까요?",
                   [("o0", "건축의 역사", False), ("o1", "훌륭한 건물이 어떤 건물인지", True), ("o2", "설계자의 이름", False)],
                   "'A profound building is ____'예요. 빈칸이 설명하는 건 building이에요.",
                   display=BLANK, tag="빈칸 문장", flip={},
                   tips=[{"label": "빈칸 문제 요령",
                          "text": "빈칸 문장을 먼저 읽고 무엇을 찾을지 정해요. 빈칸에는 글쓴이 주장과 같은 말이 올 때도, 반대 의견이 올 때도 있어요. 빈칸 앞뒤의 단서(But, However, not, 좋은 말·나쁜 말)로 어느 쪽인지 먼저 파악해요."}],
                   method=0),
            choice("s1_what",
                   "그럼 첫 문장부터 봐요. 건축 구조물은 무엇의 한 형태래요?",
                   [("o0", "설계자의 개인 취향", False), ("o1", "아름다운 그림", False), ("o2", "행동을 이끄는 공간 연출", True)],
                   "'spatial choreography that guides action'을 봐요. choreography는 '연출'이에요.",
                   why="'spatial choreography'는 공간의 연출, 'that guides action'은 행동을 이끈다는 말이에요. 취향이나 그림 이야기가 아니에요.",
                   highlight=["spatial choreography that guides action"], method=1),
            show("s1_pairs",
                 "세미콜론(;) 뒤는 짝으로 읽어요. 공간은 행동을 돕기도(+) 하고 막기도(−) 해요.",
                 signs=[{"text": "facilitates", "sign": "+"}, {"text": "prohibits", "sign": "−"},
                        {"text": "encourages", "sign": "+"}, {"text": "prevents", "sign": "−"},
                        {"text": "invites", "sign": "+"}, {"text": "inhibits", "sign": "−"}],
                 method=1),
        ],
    },
    {
        "id": 2, "text": S[1], "model_translation": KO[1], "teaching_value": "high",
        "glosses": [g("This choreography", "이 연출"), g("predetermines", "미리 결정하다"),
                    g("patterns of movement and behavior", "움직임과 행동 양식"), g("but it also", "그러나 그것은 또한"),
                    g("guides", "이끌다"), g("experiential characteristics", "경험적 특성"), g("perceptions", "지각, 인식"),
                    g("imageries", "심상, 이미지"), g("emotions and feelings", "감정과 느낌")],
        "steps": [
            choice("s2_body",
                   "공간이 이끄는 것을 두 그룹으로 나눠 봐요. 'movement and behavior(움직임과 행동)'는 어느 그룹일까요?",
                   [("o0", BODY, True), ("o1", MIND, False)],
                   "움직임과 행동은 몸으로 하는 거예요.",
                   panel={**board([], []), "sort": {"words": ["movement and behavior"], "left": BODY, "right": MIND}},
                   highlight=["patterns of movement and behavior"], method=1),
            choice("s2_mind",
                   "'but it also' 뒤의 'emotions and feelings(감정과 느낌)'는 어느 그룹일까요?",
                   [("o0", BODY, False), ("o1", MIND, True)],
                   "감정과 느낌은 마음으로 하는 거예요. but it also는 '그뿐 아니라 또'예요.",
                   panel={**board(["movement and behavior"], []), "sort": {"words": ["emotions and feelings"], "left": BODY, "right": MIND}},
                   highlight=["experiential characteristics, perceptions, imageries, emotions and feelings"], method=1),
            show("s2_both",
                 "공간은 몸의 움직임뿐 아니라 마음의 느낌까지 이끌어요. 이 두 그룹을 기억해 둬요.",
                 panel=board(["movement and behavior"], ["emotions and feelings"], "공간 = 몸과 마음을 함께 이끈다"),
                 method=1),
        ],
    },
    {
        "id": 3, "text": S[2], "model_translation": KO[2], "teaching_value": "high",
        # intuit, resonate는 시험지 아래 *로 풀어 준 단어
        "glosses": [g("A sensitive and empathic designer", "세심하고 공감할 줄 아는 설계자"), g("intuits", "직관으로 알다"),
                    g("human behavior and desire", "인간의 행동과 욕구"), g("intuitive", "직관적인"),
                    g("architectural scripting", "건축적 대본 쓰기"), g("resonates with", "~와 공명하다, 꼭 맞아떨어지다"),
                    g("user/occupant’s", "사용자·입주자의"), g("natural and instinctual", "자연스럽고 본능적인"),
                    g("needs and intentions", "욕구와 의도")],
        "steps": [
            choice("s3_designer",
                   "좋은 설계자는 누구의 무엇을 알아챈다고 할까요?",
                   [("o0", "자기 자신의 취향", False), ("o1", "사람들의 행동과 욕구", True), ("o2", "다른 건축가들의 유행", False)],
                   "intuits 뒤 'human behavior and desire'를 봐요.",
                   why="intuits 뒤 'human behavior and desire', 인간의 행동과 욕구를 알아챈대요. 설계자 자신의 취향이 아니에요.",
                   highlight=["intuits human behavior and desire"], method=1),
            show("s3_fit",
                 "그래서 설계자가 짠 대본이 실제 사는 사람의 욕구와 꼭 맞아떨어져요. 설계자의 취향이 아니라 사는 사람이 기준이에요.",
                 highlight=["resonates with the actual user/occupant’s natural and instinctual needs and intentions"],
                 method=1),
        ],
    },
    {
        "id": 4, "text": S[3], "model_translation": KO[3], "teaching_value": "medium",
        "glosses": [g("While designing a house", "집을 설계하는 동안"), g("the designer", "설계자"),
                    g("lives, uses and feels", "살아 보고, 써 보고, 느껴 보다"), g("non-existent", "존재하지 않는"),
                    g("in his imagination", "상상 속에서"), g("on behalf of", "~을 대신해서"), g("the future dweller", "미래의 거주자")],
        "steps": [
            choice("s4_behalf",
                   "설계자는 누구를 대신해서 상상 속 집을 살아 보나요?",
                   [("o0", "자기 가족", False), ("o1", "다른 설계자", False), ("o2", "미래에 그 집에 살 사람", True)],
                   "'on behalf of'는 '~을 대신해서'예요. 그 뒤를 봐요.",
                   why="'on behalf of the future dweller', 미래의 거주자를 대신해서래요. 설계자는 사는 사람이 되어 미리 살아 봐요.",
                   highlight=["on behalf of the future dweller"],
                   faded=["While designing a house,"],
                   tips=[{"label": "on behalf of", "mark": "on behalf of", "text": "'~을 대신해서, ~을 위해'예요."}],
                   method=1),
        ],
    },
    {
        "id": 5, "text": S[4], "model_translation": KO[4], "teaching_value": "medium",
        "glosses": [g("A correctly placed window", "올바르게 놓인 창문"), g("is located", "놓여 있다"), g("exactly where", "바로 ~하는 곳에"),
                    g("the occupant", "입주자, 사는 사람"), g("wishes to", "~하고 싶어 하다"), g("look out into the garden", "정원을 내다보다"),
                    g("daylight", "햇빛"), g("is needed", "필요하다")],
        "steps": [
            choice("s5_where",
                   "창문은 어디에 있어야 '올바르게' 놓인 걸까요?",
                   [("o0", "사는 사람이 정원을 내다보고 싶은 곳", True), ("o1", "설계자가 보기에 예쁜 곳", False),
                    ("o2", "공사비가 가장 싼 곳", False)],
                   "'where the occupant wishes to look out into the garden'을 봐요. occupant는 사는 사람이에요.",
                   highlight=["exactly where the occupant wishes to look out into the garden"], method=1),
        ],
    },
    {
        "id": 6, "text": S[5], "model_translation": KO[5], "teaching_value": "low",
        "glosses": [g("The stairway", "계단"), g("is located", "놓여 있다"), g("the dweller", "거주자, 사는 사람"),
                    g("wishes to", "~하고 싶어 하다"), g("enter the floor above or below", "위층이나 아래층으로 가다")],
        "steps": [
            choice("s6_same",
                   "계단도 같은 원리예요. 계단은 어디에 놓일까요?",
                   [("o0", "건물 한가운데 아무 곳", False), ("o1", "사는 사람이 오르내리고 싶은 곳", True),
                    ("o2", "설계 규칙에 정해진 곳", False)],
                   "창문처럼 'where the dweller wishes to …'예요. dweller도 사는 사람이에요.",
                   highlight=["where the dweller wishes to enter the floor above or below"], method=1),
        ],
    },
    {
        "id": 7, "text": S[6], "model_translation": KO[6], "teaching_value": "high",
        "glosses": [g("Successful architecture", "성공적인 건축"), g("does not need", "필요하지 않다"),
                    g("manuals or signage", "설명서나 표지판"), g("as", "~이기 때문에"), g("reveals", "드러내다"),
                    g("its very structure and use", "바로 그 구조와 쓰임새"), g("in a wordless manner", "말없이")],
        "steps": [
            choice("s7_why",
                   "성공적인 건축에는 왜 설명서나 표지판이 필요 없을까요?",
                   [("o0", "사람들이 설명서를 안 읽어서", False), ("o1", "건물이 아주 단순해서", False),
                    ("o2", "말없이도 쓰임새를 드러내서", True)],
                   "여기서 as는 '~이기 때문에'예요. as 뒤를 봐요.",
                   why="as는 여기서 '~이기 때문에'예요. 'it reveals its very structure and use in a wordless manner', 말없이 쓰임새를 드러내서래요.",
                   highlight=["as it reveals its very structure and use in a wordless manner"],
                   tips=[{"label": "as", "mark": "as",
                          "text": "as는 '~처럼, ~할 때, ~이기 때문에' 등 뜻이 많아요. 콤마 뒤에서 이유를 덧붙이면 '~이기 때문에'예요."}],
                   method=1),
        ],
    },
    {
        "id": 8, "text": BLANK, "model_translation": KO[7], "teaching_value": "high",
        "glosses": [g("A profound building", "심오한(훌륭한) 건물")],
        "steps": [
            # 빈칸이 주장과 같은 쪽인지 반대 쪽인지 — 이걸 먼저 파악해야 보기를 고른다
            choice("s8_side",
                   "이 빈칸 문장은 글쓴이 주장과 같은 쪽일까요, 반대 쪽일까요?",
                   [("o0", "같은 쪽 (주장 그대로)", True), ("o1", "반대 쪽 (반대 의견)", False)],
                   "profound(심오한, 훌륭한)는 좋은 말(+)이에요. But이나 not 같은 반전 단서도 없어요.",
                   why="profound(훌륭한)는 좋은 말(+)이고, But이나 not 같은 반전 단서가 없어요. 훌륭한 건물을 설명하니 주장 그대로예요.",
                   signs=[{"text": "A profound building", "sign": "+"}],
                   tips=[{"label": "같은 쪽? 반대 쪽?",
                          "text": "빈칸 문장에 But, However, not 같은 반전 단서가 있거나 나쁜 말(−)을 설명하면 반대 의견이 들어가요. 좋은 말(+)을 그대로 설명하면 주장과 같은 말이 들어가요."}],
                   method=1),
            choice("s8_gist",
                   "지금까지를 한 줄로 모으면, 훌륭한 건물은 어떤 건물일까요?",
                   [("o0", "설계자의 취향을 잘 보여 주는 건물", False), ("o1", "그 시대의 문화를 전하는 건물", False),
                    ("o2", "사는 사람의 몸과 마음의 움직임에 꼭 맞는 건물", True)],
                   "공간은 몸과 마음을 함께 이끌고, 설계자는 사는 사람이 기준이었어요.",
                   why="공간은 몸(행동)과 마음(느낌)을 함께 이끌고, 좋은 설계자는 자기 취향이 아니라 사는 사람의 행동과 욕구에 맞춰요.",
                   panel=board(["movement and behavior"], ["emotions and feelings"], "훌륭한 건물 = 사는 사람의 몸과 마음에 꼭 맞는다"),
                   underline=None, method=1),
            show("s8_go",
                 "빈칸은 주장과 같은 쪽이니, 이 주장을 다른 말로 바꿔 쓴 보기를 찾아봐요.",
                 button="문제 풀러 갈게요",
                 panel=board(["movement and behavior"], ["emotions and feelings"], "훌륭한 건물 = 사는 사람의 몸과 마음에 꼭 맞는다"),
                 method=1),
        ],
    },
]
# underline=None 같은 빈 값은 지운다
for s_ in sentences:
    for st in s_["steps"]:
        for k in [k for k, v in st.items() if v is None]:
            st.pop(k)

OPTIONS = [
    ("1", "an instrument to pass down cultural mindsets of its time", ["pass down", "cultural mindsets"],
     "그 시대의 문화적 사고방식을 전하는 도구", False),
    ("2", "a spatial logic made independent from nonprofessional opinions", ["independent from", "nonprofessional opinions"],
     "비전문가의 의견과 떨어져서 만든 공간 논리", False),
    ("3", "an extension of human bodily and mental actions and capabilities", ["extension", "bodily and mental"],
     "인간의 신체적·정신적 행동과 능력의 연장", True),
    ("4", "an architectural expression of the designer’s aesthetic preference", ["designer’s", "aesthetic preference"],
     "설계자의 미적 취향을 건축으로 표현한 것", False),
    ("5", "a structure whose outward appearance masks its function", ["outward appearance", "masks its function"],
     "겉모습이 기능을 가리는 구조물", False),
]

exam = {
    "question": "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오. [3점]",
    "underline": "________",
    "sentence": 8,
    "analysis_first": True,
    "glosses": [g("instrument", "도구"), g("pass down", "물려주다, 전하다"), g("cultural mindsets", "문화적 사고방식"),
                g("independent from", "~와 떨어진"), g("nonprofessional", "비전문가의"), g("extension", "연장, 확장"),
                g("bodily", "신체의"), g("mental", "정신의"), g("capabilities", "능력"), g("aesthetic preference", "미적 취향"),
                g("outward appearance", "겉모습"), g("masks", "가리다")],
    "options": [{"id": o[0], "label": o[1], "keywords": o[2], "ko": o[3], **({"correct": True} if o[4] else {})} for o in OPTIONS],
    "brief": {
        "ask": "훌륭한 건물은 사는 사람의 몸과 마음에 꼭 맞는다는 생각을 떠올리며 골라 봐요.",
        "first_correct": "맞았어요!",
        "first_wrong": "아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.",
        "final_correct": "정답이에요!",
        "answer_explain": "정답이에요! 훌륭한 건물은 사는 사람의 행동(몸)과 느낌(마음)에 꼭 맞아서, 그 몸과 마음이 하는 일을 이어서 넓혀 주는 연장이에요.",
        "final_wrong": "정답은 ③이에요.",
        "option_feedback": {
            "1": "시대의 문화를 전하는 이야기는 글에 없어요. 글은 사는 사람의 행동과 느낌에 맞추는 건축 이야기예요.",
            "2": "비전문가, 즉 사는 사람의 의견과 떨어진다면 사는 사람에게 맞춘다는 글과 반대예요.",
            "4": "글에 designer가 여러 번 나와서 헷갈렸죠. 하지만 설계자는 자기 취향이 아니라 사는 사람의 행동과 욕구에 맞춰요.",
            "5": "겉모습이 기능을 가린다면, 말없이도 쓰임새를 드러낸다는 7문장과 반대예요.",
        },
        "ask_first": "실제 시험처럼 풀어 봐요. 위 보기에서 답을 골라요.",
    },
}

lesson = {
    "id": ID, "kind": "policy", "version": "0.1",
    "source": "2026년 3월 고3 전국연합학력평가 영어 33번 (빈칸 추론, 3점)",
    "brief": {"topic": "빈칸 푸는 법: 빈칸 문장부터 → 주장 잡기 → 빈칸이 주장과 같은 쪽인지 반대 쪽인지 → 바꿔 쓴 보기 찾기", "closing": "수고 인사"},
    "method": {"type": "blank", "labels": ["빈칸 문장 먼저 보기", "요지 잡기"], "intro_times": 3},
    "read_button": "분석하러 갈게요",
    "read_first": True,
    "intro": [
        {"id": "topic", "type": "say", "button": "네",
         "brief": {"say": "좋은 집은 왜 설명서 없이도 쓰기 편할까요? 이번 글은 건축과 사람의 몸과 마음을 다뤄요."}},
        {"id": "method1", "type": "say", "button": "좋아요",
         "brief": {"say": "빈칸 문제는 빈칸 문장부터 보고 글쓴이의 주장을 잡아요. 빈칸이 주장과 같은 말인지, 반대 의견인지 파악해서 보기를 골라요."}},
    ],
    "exam": exam,
    "key_words": {
        # choreography, intuit, resonate는 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
        "passage": [g("architectural", "건축의"), g("spatial", "공간의"), g("facilitate", "촉진하다"), g("prohibit", "금지하다"),
                    g("inhibit", "억제하다"), g("predetermine", "미리 결정하다"), g("perception", "지각, 인식"),
                    g("empathic", "공감할 수 있는"), g("occupant", "입주자"), g("instinctual", "본능적인"),
                    g("on behalf of", "~을 대신해서"), g("dweller", "거주자"), g("reveal", "드러내다"), g("profound", "심오한")],
        "options": [g("extension", "연장, 확장"), g("bodily", "신체의"), g("aesthetic", "미적인")],
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
    "topic_intro": "빈칸 푸는 법",
    "closing": ref["closing"],
    "helps": {},
    "steps": steps,
    "exam": {k: v for k, v in exam["brief"].items()},
    "intro": {i["id"]: dict(i["brief"]) for i in lesson["intro"]},
    "ending": {**ref["ending"], "wrong": "이번엔 한 번 헷갈렸으니 {weeks} 뒤에 다시 한번 볼 거예요."},
}
json.dump(c, open(f"{ROOT}/content/tutor/policy-copy/dajung/{ID}.json", "w"), ensure_ascii=False, indent=2)
print("ok", ID)
