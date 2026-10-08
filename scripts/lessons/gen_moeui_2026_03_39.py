"""2026년 3월 39번 레슨 + 대사를 만든다 (주어진 문장 넣기, 3점).

레슨 JSON(content/tutor/policy-lessons/…)과 대사(content/tutor/policy-copy/dajung/…)는 이 스크립트의
생성물이다. 고칠 때는 여기를 고치고 다시 돌린 뒤 도장을 찍는다:

    python3 scripts/lessons/gen_moeui_2026_03_39.py
    npm run policy:copy stamp moeui-2026-03-39-epistemic-communities

주어진 문장(첫 화면)의 주어 찾기는 선생님과 정했다. 나머지 문장과 푸는 법 칠판은 아직 초안.
"""
import copy
import json
import os

ID = "moeui-2026-03-39-epistemic-communities"
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


def show(id, say, method=0, button="다음 문장", **extra):
    return {"id": id, "type": "show", "interaction": "note", "brief": {"say": say}, "method": method, "button": button, **extra}


# 수업 끝 「오늘 헷갈렸던 곳」 한 줄
POINTS = {
    "s2_subject": "To acquire … = ~하기 위해(주어 아님) · 주어는 one(누구든) · 콤마 사이가 메인 문장",
    "g_subject": "for most outsiders = 대부분의 외부인에게는(주어 아님) · 주어는 even completely transparent practices",
}

GIVEN = ("Nonetheless, for most outsiders even completely transparent practices do not lift the veil behind which "
         "such forms of knowledge are hidden—without the relevant training and acquisition of skills, which often take "
         "many years, one simply cannot make sense of the information that is being shared.")
DASH = ("—without the relevant training and acquisition of skills, which often take many years, one simply cannot make "
        "sense of the information that is being shared.")

S2_SLASH = "To acquire expert knowledge, / one needs to become a member of the relevant group of knowledge bearers, / for which I will use the term “epistemic communities.”"

sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN,
        "model_translation": "그럼에도 불구하고, 대부분의 외부인에게는 완전히 투명한 관행조차도 그러한 형태의 지식이 뒤에 감추어져 있는 장막을 들어 올리지 못하는데, 즉 자주 수년이 걸리는 관련 교육과 기술의 습득 없이는 공유되고 있는 정보를 그야말로 이해할 수 없다.",
        "teaching_value": "high",
        "glosses": [
            g("Nonetheless", "그럼에도 불구하고"),
            g("for most outsiders", "대부분의 외부인에게는 · 주어가 아니에요"),
            g("outsiders", "외부인"),
            g("even", "~조차"),
            g("completely transparent", "완전히 투명한"),
            g("practices", "관행, 하는 방식"),
            g("lift the veil", "장막을 걷어 내다 · 숨겨진 것을 드러내다"),
            g("behind which", "그 뒤에"),
            g("forms of knowledge", "지식의 형태"),
            g("hidden", "숨겨진"),
            g("without", "~없이는"),
            g("relevant", "관련된"),
            g("training", "교육, 훈련"),
            g("acquisition", "습득"),
            g("skills", "기술"),
            g("often take many years", "자주 수년이 걸리다"),
            g("simply", "그야말로"),
            g("make sense of", "~을 이해하다 · 중요 표현"),
            g("information", "정보"),
            g("being shared", "공유되고 있는"),
        ],
        "emphasis": ["Nonetheless", "for most outsiders", "completely transparent"],
        "helps": [{"id": "g_subject_help", "label": "주어 찾기 헷갈려요",
                   "brief": "'for'처럼 전치사로 시작하는 덩어리는 주어가 아니에요. 'for most outsiders'는 '대부분의 외부인에게는'으로 읽어요. 그걸 빼면 주어가 보여요."}],
        "steps": [
            choice("g_subject",
                   "먼저 주어진 문장이에요. 이 문장의 주어는 무엇일까요?",
                   [("o0", "most outsiders", False), ("o1", "completely transparent practices", True), ("o2", "the veil", False)],
                   "'for most outsiders'는 'for'로 시작하는 덩어리예요. 그다음 덩어리를 봐요.",
                   why="'for most outsiders'는 '대부분의 외부인에게는'이라는 덩어리라 주어가 아니에요. 그다음 덩어리가 주어예요.",
                   highlight=["even completely transparent practices"],
                   highlight_alt=["for most outsiders"],
                   faded=[DASH]),
            show("g_structure",
                 "'for most outsiders'는 '대부분의 외부인에게는'으로 읽어요. 주어는 'even completely transparent practices', 즉 '완전히 투명한 관행조차'예요.",
                 button="다음",
                 panel={"kind": "structure", "rows": [
                     {"label": "~에게는", "text": "for most outsiders", "ko": "대부분의 외부인에게는", "tone": "hl2"},
                     {"label": "주어", "text": "even completely transparent practices", "ko": "완전히 투명한 관행조차", "tone": "hl"},
                     {"label": "동사", "text": "do not lift the veil", "ko": "장막을 걷어 내지 못한다"},
                 ]},
                 highlight=["even completely transparent practices"],
                 highlight_alt=["for most outsiders"],
                 faded=[DASH]),
            # 대시 앞 'lift the veil'은 비유라 한 번에 안 들어온다 — 같은 말을 쉽게 풀어 쓴 대시 뒤로 읽는다
            show("g_dash",
                 "'lift the veil'은 비유라 한 번에 안 들어와요. 대시 뒤를 보면 쉬워요. 교육과 기술 습득 없이는 공유되는 정보를 이해할 수 없대요.",
                 highlight=["without the relevant training and acquisition of skills", "one simply cannot make sense of the information that is being shared"],
                 faded=[", which often take many years,"],
                 tips=[
                     {"label": "one", "mark": "one",
                      "text": "여기서 one은 숫자 '1'이 아니라 특정되지 않은 '사람', 즉 '누구든'이에요. 'one simply cannot …'은 '누구든 그야말로 ~할 수 없다'예요."},
                     {"label": "make sense of", "mark": "make sense of",
                      "text": "'~을 이해하다'라는 중요한 표현이에요. 'make sense'만 쓰면 '말이 되다, 이치에 맞다'예요."},
                 ]),
        ],
    },
    {
        "id": 2,
        "text": "To acquire expert knowledge, one needs to become a member of the relevant group of knowledge bearers, for which I will use the term “epistemic communities.”",
        "model_translation": "전문 지식을 습득하기 위해서는 관련 지식 보유자 집단의 구성원이 되어야 하는데, 그것에 나는 '지식 공동체'라는 용어를 사용하겠다.",
        "teaching_value": "medium",
        "glosses": [g("acquire", "습득하다"), g("expert knowledge", "전문 지식"), g("member", "구성원"), g("relevant", "관련된"),
                    g("knowledge bearers", "지식 보유자"), g("term", "용어"), g("epistemic communities", "지식 공동체")],
        "helps": [{"id": "s2_subject_help", "label": "주어 찾기 헷갈려요",
                   "brief": "'To acquire …'처럼 To로 시작하는 덩어리는 '~하기 위해'라는 뜻이라 주어가 아니에요. 콤마 뒤 첫 단어를 봐요."}],
        "steps": [
            choice("s2_subject",
                   "이 문장의 주어는 무엇일까요?",
                   [("o0", "expert knowledge", False), ("o1", "one", True), ("o2", "a member", False)],
                   "'To acquire expert knowledge'는 '전문 지식을 얻기 위해'예요. 콤마 뒤를 봐요.",
                   why="'To acquire expert knowledge'는 '전문 지식을 얻기 위해'라서 주어가 아니에요. 콤마 뒤 'one needs'에서 주어를 찾아요."),
            # 맞히든 틀리든 슬래시로 덩어리를 나눠 보여 준다. 콤마 사이는 삽입이 아니라 메인 문장 — 흐리지 않는다
            show("s2_slash",
                 "'To acquire …'는 '~하기 위해'라서 주어가 아니에요. 주어는 'one', 여기서도 '누구든'이에요. 콤마 사이가 주어와 동사가 있는 메인 문장이라 꼭 읽어야 해요.",
                 display=S2_SLASH,
                 panel={"kind": "structure", "rows": [
                     {"label": "~하기 위해", "text": "To acquire expert knowledge", "ko": "전문 지식을 얻기 위해", "tone": "hl2"},
                     {"label": "메인 문장", "text": "one needs to become a member of the relevant group of knowledge bearers", "ko": "누구든 관련 지식 보유자 집단의 구성원이 되어야 한다", "tone": "hl"},
                     {"label": "덧붙임", "text": "for which I will use the term “epistemic communities”", "ko": "그 집단을 나는 '지식 공동체'라고 부르겠다"},
                 ]},
                 highlight=["one needs to become a member of the relevant group of knowledge bearers"],
                 highlight_alt=["To acquire expert knowledge"],
                 tips=[{"label": "콤마 사이 = 늘 삽입?", "mark": "one needs",
                        "text": "콤마 두 개 사이가 늘 빼도 되는 삽입은 아니에요. 그 안에 주어와 동사가 있으면 메인 문장이라 꼭 읽어야 해요. 여기서는 'one needs'가 주어와 동사예요."},
                       {"label": "for which", "mark": "for which",
                        "text": "which는 앞의 'the relevant group of knowledge bearers'를 받아요. '그 집단에 대해 나는 ~라는 용어를 쓰겠다'예요."}]),
        ],
    },
    {
        "id": 3,
        "text": "(①) A newcomer learns from experts and is socialized into the common practices of the relevant epistemic community.",
        "model_translation": "새로 온 사람은 전문가들로부터 배우며, 관련 지식 공동체의 공동 관행에 사회화된다.",
        "teaching_value": "low",
        "glosses": [g("newcomer", "새로 온 사람"), g("experts", "전문가"), g("is socialized into", "~에 사회화되다, 익숙해지다"),
                    g("common practices", "공동 관행")],
        "steps": [show("s3_draft", "새로 온 사람은 전문가에게 배우며 그 공동체의 관행에 익숙해져요.")],
    },
    {
        "id": 4,
        "text": "(②) Often there are admittance processes, combined with tests of a candidate’s abilities.",
        "model_translation": "자주 후보자의 능력에 대한 시험과 결합한 입회 절차가 존재한다.",
        "teaching_value": "low",
        "glosses": [g("admittance processes", "입회 절차"), g("combined with", "~와 결합된"), g("tests", "시험"),
                    g("candidate", "후보자"), g("abilities", "능력")],
        "steps": [show("s4_draft", "능력 시험이 붙은 입회 절차가 있는 경우가 많대요.")],
    },
    {
        "id": 5,
        "text": "(③) In the premodern era, epistemic communities were often kept secret, with strict tests of loyalty for new members, not least because of fears that specialized knowledge would fall into the “wrong hands.”",
        "model_translation": "전근대적인 시대에는, 지식 공동체가 자주 비밀에 부쳐졌고, 신입 구성원에게 엄격한 충성심 시험이 있었는데, 특히 전문적인 지식이 '잘못된 손'에 들어갈 것이라는 두려움 때문이었다.",
        "teaching_value": "high",
        "glosses": [g("premodern era", "전근대 시대"), g("kept secret", "비밀에 부쳐진"), g("strict", "엄격한"), g("loyalty", "충성심"),
                    g("not least because of", "특히 ~때문에"), g("fears", "두려움"), g("specialized knowledge", "전문적인 지식"),
                    g("wrong hands", "잘못된 손 · 나쁜 사람")],
        "steps": [show("s5_draft", "옛날에는 지식 공동체가 비밀이었고, 신입에게 엄격한 충성심 시험이 있었대요.")],
    },
    {
        "id": 6,
        "text": "(④) Some traces of these older practices may still be present today, but on the whole, the ideal has shifted to openness among the members of epistemic communities, and also, to some extent, toward outsiders.",
        "model_translation": "이러한 오래된 관행의 일부 흔적이 오늘날에도 여전히 존재할 수 있지만, 전체적으로 보아, 이상은 지식 공동체 구성원 사이에서 개방성, 그리고 또한, 어느 정도는, 외부인을 향한 것으로 옮겨 갔다.",
        "teaching_value": "high",
        "glosses": [g("traces", "흔적"), g("older practices", "오래된 관행"), g("present", "존재하는"), g("on the whole", "전체적으로"),
                    g("ideal", "이상"), g("has shifted to", "~로 옮겨 갔다"), g("openness", "개방성"), g("to some extent", "어느 정도는"),
                    g("toward outsiders", "외부인을 향해")],
        "steps": [show("s6_draft", "지금도 흔적은 있지만, 전체적으로는 개방성, 어느 정도는 외부인에게까지 열린 쪽으로 바뀌었대요.")],
    },
    {
        "id": 7,
        "text": "(⑤) Other, more active strategies are needed to make certain forms of knowledge as “accessible” as is realistically possible.",
        "model_translation": "특정한 형태의 지식을 현실적으로 가능한 한 '접근 가능하게' 만들기 위해서는, 다른, 보다 더 적극적인 전략이 필요하다.",
        "teaching_value": "high",
        "glosses": [g("Other", "다른"), g("more active strategies", "더 적극적인 전략"), g("are needed", "필요하다"),
                    g("certain forms of knowledge", "특정한 형태의 지식"), g("accessible", "접근 가능한"),
                    g("realistically possible", "현실적으로 가능한")],
        "steps": [show("s7_draft", "지식을 최대한 '접근 가능하게' 하려면 다른, 더 적극적인 전략이 필요하대요.", button="문제 풀러 갈게요")],
    },
]

exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은? [3점]",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"],
    "sentence": 1,
    "analysis_first": True,
    "glosses": [],
    "options": [
        {"id": "1", "label": "A newcomer learns … 앞", "keywords": [], "ko": "'지식 공동체' 정의 뒤"},
        {"id": "2", "label": "Often there are … 앞", "keywords": [], "ko": "신입이 배우며 사회화된다 뒤"},
        {"id": "3", "label": "In the premodern era … 앞", "keywords": [], "ko": "입회 절차·능력 시험 뒤"},
        {"id": "4", "label": "Some traces … 앞", "keywords": [], "ko": "옛날엔 비밀이었다 뒤"},
        {"id": "5", "label": "Other, more active strategies … 앞", "keywords": [], "ko": "개방성, 외부인에게까지 뒤", "correct": True},
    ],
    "brief": {
        "ask": "주어진 문장의 단서(Nonetheless, transparent, outsiders)를 떠올리며 들어갈 곳을 골라 봐요.",
        "first_correct": "맞았어요!",
        "first_wrong": "아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.",
        "final_correct": "정답이에요!",
        "answer_explain": "정답이에요! '투명한 관행'과 '외부인'은 바로 앞 문장의 개방성, 외부인을 향한 개방을 받아요. 그런데도(Nonetheless) 외부인은 이해 못 하니, '다른, 더 적극적인 전략'이 필요하다로 이어져요.",
        "final_wrong": "정답은 ⑤예요.",
        "option_feedback": {
            "1": "여기서는 아직 지식 공동체가 무엇인지만 말했어요. '투명한 관행'이 나올 자리가 아니에요.",
            "2": "신입이 배우는 이야기 중이에요. '투명한 관행'이나 '외부인'을 받을 말이 앞에 없어요.",
            "3": "입회 절차 이야기 중이에요. '투명한 관행'을 받을 말이 앞에 없어요.",
            "4": "바로 앞은 '비밀에 부쳤다'예요. 비밀 뒤에 '투명한 관행조차'가 오면 어색해요.",
        },
        "ask_first": "실제 시험처럼 풀어 봐요. 위 보기에서 답을 골라요.",
    },
}

# 학생이 막힐 만한 단어는 다 누를 수 있게
MORE_GLOSSES = {
    1: [("most", "대부분의"), ("such", "그러한"), ("one", "사람, 누구나"), ("cannot", "~할 수 없다")],
    2: [("To", "~하기 위해"), ("needs to become", "~가 되어야 한다"), ("group", "집단"), ("use", "사용하다")],
    3: [("learns", "배우다"), ("community", "공동체")],
    4: [("Often", "자주")],
    5: [("communities", "공동체들"), ("new members", "신입 구성원"), ("would fall into", "~에 들어가게 될")],
    6: [("Some", "일부"), ("still", "여전히"), ("today", "오늘날"), ("among", "~사이에서"), ("members", "구성원")],
    7: [("make", "만들다")],
}
for s_ in sentences:
    have = {x["en"].lower() for x in s_["glosses"]}
    s_["glosses"] += [g(en, ko) for en, ko in MORE_GLOSSES.get(s_["id"], []) if en.lower() not in have]

lesson = {
    "id": ID, "kind": "policy", "version": "0.2",
    "source": "2026년 3월 고3 전국연합학력평가 영어 39번 (주어진 문장 넣기, 3점)",
    "brief": {"topic": "문장 넣기 푸는 법: 주어진 문장의 단서 → 앞 내용 예측 → 흐름이 끊기는 곳", "closing": "수고 인사"},
    "method": {"type": "sentence_insertion", "labels": ["주어진 문장 단서 찾기", "앞에 올 내용 예측하기", "흐름 끊기는 곳 찾기"], "intro_times": 3},
    "read_button": "분석하러 갈게요",
    # 문장마다 영어 문장부터 — 질문·보기는 「다 읽었어요」 뒤에
    "read_first": True,
    "images": {"method": {"src": "/assets/insert-method.svg", "alt": "문장 넣기 푸는 법: ① 주어진 문장의 단서 찾기 ② 앞에 올 내용 예측하기 ③ 흐름이 끊기는 곳 찾기", "kind": "drawing"}},
    "intro_board": "method",
    "intro": [
        {"id": "method1", "type": "say", "button": "네",
         "brief": {"say": "문장 넣기는 주어진 문장부터 꼼꼼히 봐야 해요. 그 안에 앞 문장과 이어지는 단서가 숨어 있거든요."}},
        {"id": "method2", "type": "say", "button": "좋아요",
         "brief": {"say": "단서를 찾고, 앞에 올 내용을 예측한 뒤, 흐름이 끊기는 곳을 찾을 거예요. 칠판 순서대로 해 볼게요."}},
    ],
    "exam": exam,
    "key_words": {
        # transparent, epistemic은 시험지 아래 *로 풀어 준 단어 — 핵심 단어가 아니라 뺐다
        "passage": [g("nonetheless", "그럼에도 불구하고"), g("outsider", "외부인"), g("practice", "관행"),
                    g("lift the veil", "장막을 걷어 내다"), g("acquisition", "습득"), g("make sense of", "~을 이해하다"),
                    g("socialize", "사회화하다"), g("admittance", "입회, 입장 허가"),
                    g("candidate", "후보자"), g("premodern", "전근대적인"), g("loyalty", "충성심"), g("openness", "개방성"),
                    g("strategy", "전략"), g("accessible", "접근 가능한")],
        "options": [],
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
    "topic_intro": "문장 넣기 푸는 법",
    "closing": ref["closing"],
    "helps": {h["id"]: {"answer": h["brief"]} for s_ in sentences for h in s_.get("helps", [])},
    "steps": steps,
    "exam": {k: v for k, v in exam["brief"].items()},
    "intro": {i["id"]: dict(i["brief"]) for i in lesson["intro"]},
    # 정답 해설이 이미 「정답이에요!」로 시작하니, 다시 볼 주기 말에서는 빼 둔다
    "ending": {**ref["ending"], "wrong": "이번엔 한 번 헷갈렸으니 {weeks} 뒤에 다시 한번 볼 거예요."},
}
json.dump(c, open(f"{ROOT}/content/tutor/policy-copy/dajung/{ID}.json", "w"), ensure_ascii=False, indent=2)
print("ok", ID)
