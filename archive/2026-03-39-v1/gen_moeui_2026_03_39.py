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


def sv_pick(id, candidates, roles, ask, wrong_by, explain, point, wrong="그건 주어나 동사가 아니에요."):
    """읽기 끝나면 덩어리째 주어·동사(목적어) 찾기 — 찾은 건 S·V·O 표시로 남는다"""
    return {
        "id": id, "type": "pick", "interaction": "word_pick", "shade": True, "no_unknown": True,
        "candidates": candidates, "answers": list(roles), "roles": roles,
        "brief": {"ask": ask, "wrong": wrong, "wrong_by": wrong_by, "more": "좋아요! {n}개 남았어요.",
                  "praise": "다 찾았어요!", "explain": explain, "point": point},
        "method": 0,
    }


def key_summary(id, model, rules, highlight, feedback, point, **extra):
    """노란 핵심어만 보고 직역 말고 상황 요약 (자유 응답, 규칙 채점)"""
    return {
        "id": id, "type": "translate", "interaction": "free_translation",
        "model": model, "labels": {"mine": "내 요약", "model": "요약 예시"},
        "rules": [{"id": r[0], "need": r[1], "fix": r[2]} for r in rules],
        "highlight": highlight,
        "brief": {
            "ask": "노란 핵심어만 보고, 직역 말고 어떤 상황인지 간단히 요약해서 써 봐요.",
            "praise": "잘 요약했어요! 핵심어만으로도 상황이 보여요.",
            "wrong": "고친 부분을 같이 봐요.",
            "explain": "괜찮아요. 요약 예시를 같이 봐요. 연습할 문장으로 저장해 둘게요.",
            "feedback": feedback, "placeholder": "어떤 상황인지 한 줄로 써 보세요", "point": point,
        },
        "method": 0, **extra,
    }


# 단어 지도 — 이 글은 내부자(전문가) ↔ 외부자(초보자) 대비가 계속 반복된다. 문장마다 그 묶음에 단어가 쌓인다
INSIDE = [("knowledge bearers", "지식 보유자"), ("a member", "구성원"), ("epistemic communities", "지식 공동체"),
          ("experts", "전문가"), ("the members", "구성원들")]
OUTSIDE = [("outsiders", "외부인"), ("a newcomer", "새로 온 사람"), ("a candidate", "후보자")]


def groups_board(n_in, n_out, fresh=(), caption="내부자(전문가) ↔ 외부자(초보자)"):
    """앞에서 n_in·n_out개까지 보인다. fresh에 든 영어는 이번 문장에서 새로 붙은 것"""
    side = lambda words: [{"text": en, "ko": ko, **({"fresh": True} if en in fresh else {})} for en, ko in words]
    return {"kind": "groups", "title": "단어 지도", "between": "↔",
            "left": {"label": "내부자 · 전문가 쪽", "words": side(INSIDE[:n_in])},
            "right": {"label": "외부자 · 초보자 쪽", "words": side(OUTSIDE[:n_out])},
            "caption": caption}


SORT_LEFT = "왼쪽 · 내부자(전문가) 쪽"
SORT_RIGHT = "오른쪽 · 외부자(초보자) 쪽"


def sort_word(id, en, ko, inside, n_in, n_out, why):
    """단어 지도에 학생이 직접 옮긴다 — 첫 단어(knowledge bearers, outsiders)만 미리 넣고 나머지는 끌어 넣기"""
    return choice(id, f"'{en}'({ko}), 어느 쪽일까요? 끌어서 넣어 봐요.",
                  [("o0", SORT_LEFT, inside), ("o1", SORT_RIGHT, not inside)],
                  "집단 안에서 지식을 가진 쪽인지, 바깥이나 막 들어오는 쪽인지 떠올려 봐요.",
                  why=why,
                  panel={**groups_board(n_in, n_out), "sort": {"words": [en], "left": SORT_LEFT, "right": SORT_RIGHT}})


def main_obj_pick(id, candidates, answers, ask, wrong_by, explain, point):
    """동사에 딸린 전치사 + 명사(예: learn from experts, shift to openness) — 전치사의 목적어가 메인 목적어 역할"""
    return {
        "id": id, "type": "pick", "interaction": "word_pick", "shade": True,
        "candidates": candidates, "answers": answers, "roles": {a: "전목" for a in answers},
        "brief": {"ask": ask, "wrong": "그건 동사에 딸린 전치사의 목적어가 아니에요.", "wrong_by": wrong_by,
                  "more": "좋아요! {n}개 남았어요.", "praise": "맞아요!", "explain": explain, "point": point},
        "method": 0,
    }


# 수업 끝 「오늘 헷갈렸던 곳」 한 줄
POINTS = {
    "s2_subject": "To acquire … = ~하기 위해(주어 아님) · S one / V needs / O to become a member · 콤마 사이가 메인 문장",
    "g_veil": "lift the veil = 장막 뒤에 숨겨진 지식(knowledge)을 드러내다 · behind which such forms of knowledge are hidden",
    "g_veil_mean": "lift the veil(비유) = 숨겨진 지식을 드러내 이해하게 하다",
    "g_for": "for most outsiders = 대부분의 외부인에게는 · 주어는 아니지만 이 문장이 해당하는 대상(누구에게)이라 중요한 정보",
    "g_sv": "주어진 문장의 S·V·O 두 쌍 = even completely transparent practices + do not lift + the veil / (대시 뒤) one + cannot make sense of + the information · for most outsiders는 전치사 덩어리라 주어 아님",
    "g_nonetheless_before": "Nonetheless(그럼에도 불구하고) → 바로 앞 문장은 반대 상황 · 주어진 문장 앞에는 '지식이 외부인에게도 열려 있다'가 와야 한다",
    "g_subject": "for most outsiders = 대부분의 외부인에게는(주어 아님) · 주어는 even completely transparent practices",
}

GIVEN = ("Nonetheless, for most outsiders even completely transparent practices do not lift the veil behind which "
         "such forms of knowledge are hidden—without the relevant training and acquisition of skills, which often take "
         "many years, one simply cannot make sense of the information that is being shared.")
# 대시(—) 뒤 「without … shared」는 대시가 하나뿐이라 삽입이 아니다 — 흐리지 않는다 (대시 두 개 사이만 삽입)

S2_SLASH = "To acquire expert knowledge, / one needs to become a member of the relevant group of knowledge bearers, / for which I will use the term “epistemic communities.”"

sentences = [
    {
        "id": 1, "label": "주어진 문장", "text": GIVEN,
        "model_translation": "그럼에도 불구하고, 대부분의 외부인에게는 완전히 투명한 관행조차도 그러한 형태의 지식이 뒤에 감추어져 있는 장막을 들어 올리지 못하는데, 즉 자주 수년이 걸리는 관련 교육과 기술의 습득 없이는 공유되고 있는 정보를 그야말로 이해할 수 없다.",
        "teaching_value": "high",
        "glosses": [
            g("Nonetheless", "그럼에도 불구하고"),
            g("for most outsiders", "대부분의 외부인에게는"),
            g("for", "~에게(는)"),
            # 주어·동사 찾기에서 덩어리째 누르는 칸 (그 밖의 화면에서는 단어마다 나뉜다)
            g("even completely transparent practices", "완전히 투명한 관행조차"),
            g("do not lift", "들어 올리지 못한다"),
            g("the veil", "장막"),
            g("such forms of knowledge", "그러한 형태의 지식"),
            g("are hidden", "숨겨져 있다"),
            g("the relevant training", "관련 교육"),
            g("cannot make sense of", "~을 이해할 수 없다"),
            g("the information", "정보"),
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
        "steps": [
            # 읽기 끝나면 바로 주어·동사 찾기 — 대시(—) 뒤도 새 문장이라 두 쌍을 한꺼번에. 덩어리째 누른다
            {
                "id": "g_sv", "type": "pick", "interaction": "word_pick", "shade": True, "no_unknown": True,
                "candidates": ["for most outsiders", "even completely transparent practices", "do not lift", "the veil",
                               "such forms of knowledge", "are hidden", "the relevant training", "one",
                               "cannot make sense of", "the information"],
                "answers": ["even completely transparent practices", "do not lift", "the veil", "one", "cannot make sense of", "the information"],
                "roles": {"even completely transparent practices": "S", "do not lift": "V", "the veil": "O",
                          "one": "S", "cannot make sense of": "V", "the information": "O"},
                "brief": {
                    "ask": "이 문장에는 주어·동사가 두 쌍 있어요. 주어(S), 동사(V), 목적어(O)를 모두 찾아볼까요?",
                    "wrong": "그건 주어·동사·목적어가 아니에요.",
                    "wrong_by": {
                        "for most outsiders": "for 같은 전치사가 앞에 붙은 덩어리는 주어가 될 수 없어요. 'for most outsiders'는 '대부분의 외부인에게는'이에요.",
                        "such forms of knowledge": "그건 behind which 뒤 덩어리 안의 주어예요. 문장 전체의 주어가 아니에요.",
                        "are hidden": "그건 behind which 뒤 덩어리 안의 동사예요. 문장 전체의 동사가 아니에요.",
                        "the relevant training": "without 같은 전치사 뒤 덩어리는 주어가 될 수 없어요.",
                    },
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "다 찾았어요!",
                    "explain": "대시(—) 앞은 S even completely transparent practices, V do not lift, O the veil이에요. 대시 뒤는 S one, V cannot make sense of, O the information이에요.",
                    "point": POINTS["g_sv"],
                },
                "method": 0,
            },
            # for most outsiders — 주어는 아니지만 이 말이 「누구에게」 해당하는지 알려 주는 중요한 정보 (39번 정답 단서이기도)
            choice("g_for",
                   "그럼 for most outsiders는 어떤 역할일까요?",
                   [("o0", "주어", False), ("o1", "이 문장이 해당하는 대상 (~에게는)", True), ("o2", "목적어", False)],
                   "for most outsiders는 '대부분의 외부인에게는'이에요. 주어는 아니지만, 장막을 못 걷는 게 누구에게 그런지 알려 줘요.",
                   why="for가 붙어서 주어는 될 수 없어요. 대신 '대부분의 외부인에게는', 이 문장이 누구에게 해당하는지 알려 주는 중요한 정보예요.",
                   highlight=["for most outsiders"],
                   mark_roles=[{"text": "for most outsiders", "role": "대상"}],
                   method=0),
            show("g_for_note",
                 "for + 명사는 모의고사에서 '~에게는'이라는 뜻으로 자주 쓰여요. 주어는 아니지만 중요한 정보예요.",
                 button="다음", highlight=["for most outsiders"], method=0),
            show("g_svo_tip", "수능은 주어, 동사, 목적어 + 핵심 내용 위주로 빠르게 해석해 보면 좋아요. 한번 해 볼까요?", button="네", method=0),
            # S·V·O(+대상)만 가지고 간단히 해석 — 두 쌍이라 한 쌍씩
            {
                "id": "g_svo1", "type": "translate", "interaction": "free_translation",
                "model": "대부분의 외부인에게는 완전히 투명한 관행조차 장막을 걷어 내지 못한다.",
                "rules": [
                    {"id": "outsiders", "need": ["외부", "바깥", "밖의", "모르는 사람", "남들", "타인", "비전문가"], "fix": "대부분의 외부인에게는"},
                    {"id": "practices", "need": ["관행", "방식", "관습", "하는 일"], "fix": "완전히 투명한 관행조차"},
                    {"id": "veil", "need": ["장막", "베일", "가림", "덮개"], "fix": "장막을"},
                    {"id": "lift", "need": ["걷", "들어 ?올", "올리", "벗기", "젖히", "드러내", "밝히", "치우", "제거"], "fix": "걷어 내지(들어 올리지)"},
                    {"id": "not", "need": ["못", "않", "없"], "fix": "못한다"},
                ],
                "highlight": ["for most outsiders", "even completely transparent practices", "do not lift the veil"],
                "brief": {
                    "ask": "그럼 노란색으로 표시된 부분만 해석해 봐요.",
                    "praise": "잘 해석했어요! S·V·O만 잡아도 뜻이 보여요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "outsiders": "for most outsiders는 '대부분의 외부인에게는'이에요. 누구에게 해당하는지 빠뜨리면 안 돼요.",
                        "practices": "S even completely transparent practices는 '완전히 투명한 관행조차'예요.",
                        "veil": "O the veil은 '장막'이에요.",
                        "lift": "V do not lift는 '들어 올리지(걷어 내지) 못한다'예요.",
                        "not": "do not이 있으니 '~하지 못한다'예요.",
                    },
                    "placeholder": "S·V·O만 보고 해석해 보세요",
                    "point": "S·V·O ① = 대부분의 외부인에게는 완전히 투명한 관행조차 장막을 걷어 내지 못한다.",
                },
                "method": 0,
            },
            # lift the veil — 무엇을 가린 장막인지 지문에서 찾는다 → knowledge → 뜻 짚기
            {
                "id": "g_veil", "type": "pick", "interaction": "word_pick",
                "candidates": ["outsiders", "practices", "veil", "knowledge", "training"],
                "answers": ["knowledge"],
                "highlight": ["lift the veil"],
                "brief": {
                    "ask": "여기서 lift the veil은 무엇을 가린 장막을 들어 올린다는 걸까요? 지문에서 힌트가 될 수 있는 단어를 골라 봐요.",
                    "wrong": "그건 장막 뒤에 숨겨진 게 아니에요. veil 바로 뒤를 읽어 봐요.",
                    "wrong_by": {
                        "outsiders": "outsiders는 장막을 못 걷는 사람들이에요. 장막 뒤에 숨겨진 걸 찾아봐요.",
                        "practices": "practices(관행)는 장막을 걷으려는 쪽이에요. 장막 뒤에 숨겨진 걸 찾아봐요.",
                        "veil": "veil은 장막 자체예요. 장막 뒤에 무엇이 숨겨져 있는지 찾아봐요.",
                        "training": "training은 대시(—) 뒤에서 장막을 걷는 데 필요한 것이에요. veil 바로 뒤를 읽어 봐요.",
                    },
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "맞아요!",
                    "explain": "'behind which such forms of knowledge are hidden', 장막 뒤에 그런 지식이 숨겨져 있대요. 답은 knowledge예요.",
                    "point": POINTS["g_veil"],
                },
                "method": 1,
            },
            choice("g_veil_mean",
                   "그럼 lift the veil은 무슨 뜻일까요?",
                   [("o0", "얼굴을 가린 천을 벗기다", False), ("o1", "숨겨진 지식을 드러내 이해하게 하다", True),
                    ("o2", "관행을 모두에게 공개하다", False)],
                   "veil 뒤에는 그런 지식(knowledge)이 숨겨져 있어요. 장막을 걷으면 그 지식이 보이게 돼요.",
                   why="여기서 veil은 진짜 천이 아니라 비유예요. 장막 뒤에 지식이 숨겨져 있으니, 걷어 낸다는 건 그 지식을 드러내 이해하게 한다는 뜻이에요.",
                   highlight=["lift the veil", "behind which such forms of knowledge are hidden"],
                   method=1),
            # 그림으로 — ① 집단과 바깥의 외부인 ② 집단 안의 지식, 장막에 막혀 닿기 어려운 외부인
            show("g_veil_pic1",
                 "전문가들이 모인 집단이 있고, 외부인은 그 바깥에 있어요.",
                 button="다음",
                 panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/veil-group.svg",
                        "alt": "전문가 집단의 원 바깥에 외부인이 서 있다"},
                 method=1),
            show("g_veil_pic2",
                 "집단 안에는 전문 지식이 있어요. 관행이 아무리 투명해도, 외부인은 장막에 막혀 그 지식에 닿기 어려워요.",
                 button="다음",
                 panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/veil-knowledge.svg",
                        "alt": "집단 가운데 지식이 있고, 장막 바깥의 외부인이 손을 뻗지만 닿지 않는다"},
                 highlight=["behind which such forms of knowledge are hidden"],
                 method=1),
            {
                "id": "g_svo2", "type": "translate", "interaction": "free_translation",
                "model": "누구든 그 정보를 이해할 수 없다.",
                "rules": [
                    {"id": "one", "need": ["누구", "사람", "아무도", "우리", "외부인"], "fix": "누구든"},
                    {"id": "information", "need": ["정보"], "fix": "그 정보를"},
                    {"id": "understand", "need": ["이해", "알 수", "파악", "의미를 알"], "fix": "이해할"},
                    {"id": "not", "need": ["못", "않", "없"], "fix": "수 없다"},
                ],
                "highlight": ["one simply cannot make sense of the information"],
                "brief": {
                    "ask": "이번에도 노란색으로 표시된 부분만 해석해 봐요.",
                    "praise": "잘 해석했어요! 주어·동사만 잡아도 뜻이 보여요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "one": "S one은 숫자 1이 아니라 '사람'이에요. 여기서는 외부인을 가리켜요.",
                        "information": "O the information은 '그 정보'예요.",
                        "understand": "V make sense of는 '~을 이해하다'예요.",
                        "not": "cannot이 있으니 '~할 수 없다'예요.",
                    },
                    "placeholder": "S·V·O만 보고 해석해 보세요",
                    "point": "S·V·O ② = 누구든 그 정보를 이해할 수 없다.",
                },
                "method": 0,
            },
            # 관계사 수식 — 한 번에 맞힌 학생은 다음부터 이런 수식을 묻지 않는다 (known)
            {
                "id": "g_rel", "type": "translate", "interaction": "free_translation",
                "known": "rel_that_no_subject",
                "model": "공유되고 있는 그 정보",
                "rules": [
                    {"id": "that", "wrong": ["그것", "저것"], "fix": "공유되고 있는 정보"},
                    {"id": "share", "need": ["공유", "나누", "나눠", "나눈", "주고받", "전달"], "fix": "공유되고 있는"},
                    {"id": "modify", "need": ["(공유|나누|나눠|나눈|주고받|전달)[^.]*정보"], "wrong": ["정보(는|가|이|를)\\s*\\S*\\s*(공유|나누|나눠|주고받|전달)"],
                     "fix": "공유되고 있는 정보"},
                    {"id": "information", "need": ["정보"], "fix": "정보"},
                ],
                "highlight": ["the information that is being shared"],
                "brief": {
                    "ask": "이번엔 노란색으로 표시된 부분을 해석해 봐요.",
                    "praise": "잘 해석했어요! that 뒤가 앞 단어를 꾸며 주는 걸 잘 잡았어요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 고친 해석을 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "that": "여기서 that은 '그것'이 아니라 앞의 information을 꾸며 주는 말이에요.",
                        "share": "is being shared는 '공유되고 있는'이에요.",
                        "modify": "'공유되고 있는 정보'처럼 뒤에서부터 꾸며 해석해요.",
                        "information": "information은 '정보'예요.",
                    },
                    "placeholder": "노란 부분을 우리말로 써 보세요",
                    "point": "the information that is being shared = 공유되고 있는 정보 · that + 주어 없는 문장 → 앞 단어를 꾸민다",
                },
                "method": 0,
            },
            # 못 맞힌 학생만 — that + 주어 없는 문장이 앞 단어를 꾸민다
            show("g_rel_note",
                 "that 뒤에 주어 없이 바로 동사가 오면, 그 덩어리가 앞 단어를 꾸며 줘요. 'that is being shared'가 앞의 information을 꾸며서 '공유되고 있는 정보'예요.",
                 button="다음", if_missed="g_rel", skip_with="g_rel",
                 panel={"kind": "structure", "rows": [
                     {"label": "앞 단어", "text": "the information", "ko": "정보", "tone": "hl2"},
                     {"label": "꾸며 줌", "text": "that + (주어 없음) is being shared", "ko": "공유되고 있는", "tone": "hl"},
                 ]},
                 highlight=["that is being shared"], highlight_alt=["the information"]),
            # shared = 집단 안에서 — 대시 뒤도 대시 앞과 같은 말
            show("g_shared",
                 "shared는 앞서 본 집단 안에서, 내부인끼리 공유된다는 뜻이에요. 그래서 대시(—) 뒤도 앞과 같은 말이에요. 외부인은 내부인끼리 공유하는 지식을 이해하기 어렵다는 거예요.",
                 button="다음",
                 panel={"kind": "structure", "rows": [
                     {"label": "대시(—) 앞", "text": "do not lift the veil", "ko": "외부인은 장막을 걷지 못한다 = 숨겨진 지식에 닿지 못한다", "tone": "hl2"},
                     {"label": "대시(—) 뒤", "text": "cannot make sense of the information that is being shared", "ko": "외부인은 집단 안에서 공유되는 정보를 이해할 수 없다", "tone": "hl"},
                 ]},
                 highlight=["one simply cannot make sense of the information that is being shared"],
                 highlight_alt=["do not lift the veil"]),
            show("g_dash_tip",
                 "수능 팁이에요. 대시(—) 앞뒤는 비슷한 뜻인 경우가 많아요. 한쪽을 이해했다면 다른 쪽은 가볍게 넘기며 시간을 아낄 수 있어요.",
                 button="다음"),
            show("g_structure",
                 "",
                 button="다음", panel_below=True,
                 panel={"kind": "structure", "rows": [
                     {"label": "~에게는", "text": "for most outsiders", "ko": "대부분의 외부인에게는", "tone": "hl2"},
                     {"label": "주어", "text": "even completely transparent practices", "ko": "완전히 투명한 관행조차", "tone": "hl"},
                     {"label": "동사", "text": "do not lift the veil", "ko": "장막을 걷어 내지 못한다"},
                     {"label": "대시(—) 뒤", "text": "one + cannot make sense of", "ko": "누구든(= 외부인) + 이해할 수 없다", "tone": "hl"},
                 ]},
                 highlight=["even completely transparent practices"],
                 highlight_alt=["for most outsiders"],
                 tips=[
                     {"label": "one", "mark": "one",
                      "text": "여기서 one은 숫자 '1'이 아니라 '사람'이에요. 이 문장에서는 앞에 나온 outsiders(외부인)를 가리켜요. 'one simply cannot …'은 '외부인은 그야말로 ~할 수 없다'예요."},
                     {"label": "make sense of", "mark": "make sense of",
                      "text": "'~을 이해하다'라는 중요한 표현이에요. 'make sense'만 쓰면 '말이 되다, 이치에 맞다'예요."},
                 ],
                 ),
            # 마지막으로 Nonetheless — 앞 문장은 이 문장과 반대 상황이어야 한다 (넣을 자리를 찾는 열쇠)
            show("g_nonetheless",
                 "마지막으로 Nonetheless를 짚고 가요. '그럼에도 불구하고'라서, 바로 앞 문장은 이 문장과 반대 상황이어야 해요.",
                 button="다음", highlight=["Nonetheless"], method=1),
            choice("g_nonetheless_before",
                   "그럼 이 문장 바로 앞에는 어떤 내용이 와야 할까요?",
                   [("o0", "지식이 외부인에게도 열려 가고 있다", True),
                    ("o1", "외부인은 전문 지식을 이해하기 어렵다", False),
                    ("o2", "전문가가 되려면 오랜 훈련이 필요하다", False)],
                   "이 문장은 '외부인은 지식에 닿기 어렵다'예요. Nonetheless 앞에는 그 반대 상황이 와요.",
                   why="그건 이 문장과 같은 쪽 말이에요. Nonetheless 앞에는 반대 상황, 즉 지식이 외부인에게도 열려 있다는 말이 와야 해요.",
                   highlight=["Nonetheless"], method=1),
            show("g_nonetheless_note",
                 "앞 문장이 '지식이 외부인에게도 열려 있다'라면, 그럼에도 외부인은 지식에 닿기 어렵다는 흐름이 돼요. 지문에서 이런 반대 상황이 나오는 곳 바로 뒤가 이 문장 자리예요.",
                 button="다음",
                 panel={"kind": "contrast", "title": "Nonetheless → 앞뒤가 반대", "between": "↔",
                        "left": {"title": "바로 앞 문장 (찾을 곳)", "text": "지식이 외부인에게도 열려 있다"},
                        "right": {"title": "주어진 문장", "text": "그래도 외부인은 지식에 닿기 어렵다"}},
                 highlight=["Nonetheless"], method=1),
        ],
    },
    {
        "id": 2,
        "text": "To acquire expert knowledge, one needs to become a member of the relevant group of knowledge bearers, for which I will use the term “epistemic communities.”",
        "model_translation": "전문 지식을 습득하기 위해서는 관련 지식 보유자 집단의 구성원이 되어야 하는데, 그것에 나는 '지식 공동체'라는 용어를 사용하겠다.",
        "teaching_value": "medium",
        "glosses": [g("To acquire", "얻기 위해, 습득하기 위해"), g("one", "누구든, 사람"), g("needs", "필요로 하다, ~해야 한다"), g("to become a member", "구성원이 되는 것"),
                    g("a member", "구성원"), g("the relevant group", "관련 집단"), g("I", "나"), g("will use", "사용할 것이다"),
                    g("the term", "용어"),
                    g("acquire", "습득하다"), g("expert knowledge", "전문 지식"), g("member", "구성원"), g("relevant", "관련된"),
                    g("knowledge bearers", "지식 보유자 · 지식을 지닌 사람들"), g("term", "용어"), g("epistemic communities", "지식 공동체")],
        "steps": [
            # 주어진 문장처럼 — 읽기 끝나면 덩어리째 주어·동사·목적어 찾기 (to become a member = needs의 목적어) (for which 뒤는 덧붙임 안의 주어·동사)
            {
                "id": "s2_svc", "type": "pick", "interaction": "word_pick", "shade": True, "no_unknown": True,
                "candidates": ["To acquire", "expert knowledge", "one", "needs", "to become a member",
                               "the relevant group", "I", "will use", "the term"],
                "answers": ["one", "needs", "to become a member"],
                "roles": {"one": "S", "needs": "V", "to become a member": "O"},
                "brief": {
                    "ask": "이번엔 주어(S), 동사(V), 목적어(O)를 찾아볼까요?",
                    "wrong": "그건 주어·동사·목적어가 아니에요.",
                    "wrong_by": {
                        "To acquire": "To + 동사는 '~하기 위해'라서 문장의 동사가 아니에요.",
                        "expert knowledge": "'To acquire expert knowledge'는 '전문 지식을 얻기 위해'라서, 그 안의 expert knowledge는 주어가 아니에요.",
                        "the relevant group": "of 뒤 덩어리는 앞의 a member를 꾸며 줘요. '관련 집단의 구성원'이에요. 목적어는 그 앞에서 찾아봐요.",
                        "I": "그건 for which 뒤 덩어리 안의 주어예요. 문장 전체의 주어가 아니에요.",
                        "will use": "그건 for which 뒤 덩어리 안의 동사예요. 문장 전체의 동사가 아니에요.",
                        "the term": "그건 for which 뒤 덩어리 안의 목적어예요. 문장 전체의 목적어가 아니에요.",
                    },
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "다 찾았어요!",
                    "explain": "주어는 one, 동사는 needs, 목적어는 to become a member(구성원이 되는 것)예요.",
                    "point": POINTS["s2_subject"],
                },
                "method": 0,
            },
            # S·V·O + 핵심어(acquire expert knowledge, group)로 — 직역 말고 어떤 상황인지 요약
            {
                "id": "s2_sum", "type": "translate", "interaction": "free_translation",
                "model": "전문 지식을 습득하려면 집단의 구성원이 되어야 한다.",
                "labels": {"mine": "내 요약", "model": "요약 예시"},
                "rules": [
                    {"id": "knowledge", "need": ["지식"], "fix": "전문 지식을"},
                    {"id": "acquire", "need": ["습득", "얻", "배우", "갖", "가지"], "fix": "습득하려면"},
                    {"id": "group", "need": ["집단", "그룹", "모임", "공동체", "단체"], "fix": "집단의"},
                    {"id": "member", "need": ["구성원", "회원", "일원", "멤버", "들어가", "속해", "가입"], "fix": "구성원이 되어야 한다"},
                ],
                "highlight": ["acquire expert knowledge", "one needs to become a member", "group"],
                "brief": {
                    "ask": "노란 핵심어만 보고, 직역 말고 어떤 상황인지 간단히 요약해서 써 봐요.",
                    "praise": "잘 요약했어요! 핵심어만으로도 상황이 보여요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 요약 예시를 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "knowledge": "expert knowledge는 '전문 지식'이에요.",
                        "acquire": "To acquire는 '얻기 위해, 습득하려면'이에요.",
                        "group": "group은 '집단'이에요. 어떤 집단의 구성원이 되는지가 중요해요.",
                        "member": "to become a member는 '구성원이 되는 것'이에요.",
                    },
                    "placeholder": "어떤 상황인지 한 줄로 써 보세요",
                    "point": "To acquire expert knowledge, one needs to become a member of … group = 전문 지식을 습득하려면 집단의 구성원이 되어야 한다",
                },
                "method": 0,
            },
            # bear는 헷갈리기 쉽다 — 먼저 고르게 하고, 그다음 설명
            choice("s2_bear_q",
                   "knowledge bearers의 bear는 헷갈리기 쉬운 단어예요. 여기서 bear는 무슨 뜻일까요?",
                   [("o0", "낳다", False), ("o1", "참다, 견디다", False), ("o2", "지니다, 가지고 있다", True)],
                   "knowledge(지식)와 붙어 있어요. 지식을 어떻게 하는 사람들일까요?",
                   why="여기서 bear는 그 뜻이 아니에요. 바로 이어서 설명해 줄게요.",
                   highlight=["knowledge bearers"]),
            show("s2_bear",
                 "bear는 '곰', '참다', '낳다' 말고도 '지니다, 가지고 있다'라는 뜻이 있어요. bearer는 '지닌 사람'이라서, knowledge bearers는 '지식을 지닌 사람들', 즉 지식 보유자예요.",
                 button="다음", highlight=["knowledge bearers"]),
            # 이 집단을 가리키는 말 — 글쓴이가 붙인 이름 epistemic communities
            {
                "id": "s2_name", "type": "pick", "interaction": "word_pick", "shade": True,
                "candidates": ["expert knowledge", "a member", "I", "the term", "epistemic communities"],
                "answers": ["epistemic communities"],
                "brief": {
                    "ask": "그럼 이 지식 보유자 집단을 가리키는 말은 무엇일까요? 문장에서 찾아 눌러 봐요.",
                    "wrong": "그건 집단을 가리키는 말이 아니에요.",
                    "wrong_by": {
                        "expert knowledge": "그건 집단이 지닌 '전문 지식'이에요. 집단을 부르는 이름을 찾아봐요.",
                        "a member": "a member는 집단 안의 구성원 한 명이에요. 집단 전체를 부르는 말을 찾아봐요.",
                        "I": "I는 글쓴이예요. 글쓴이가 이 집단을 무엇이라고 부르는지 찾아봐요.",
                        "the term": "the term은 '용어'예요. 어떤 용어인지 바로 뒤를 봐요.",
                    },
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "맞아요! 글쓴이는 이 집단을 epistemic communities(지식 공동체)라고 불러요.",
                    "explain": "for which는 '그 집단에 대해'예요. 글쓴이는 이 집단을 epistemic communities(지식 공동체)라고 불러요.",
                    "point": "the relevant group of knowledge bearers = epistemic communities(지식 공동체) · for which I will use the term …",
                },
                "method": 0,
            },
            # 주어진 문장의 장막 그림과 짝 — 지식을 얻으려면 집단 안으로 들어가 구성원이 되어야 한다
            show("s2_join_pic",
                 "아까 외부인은 장막에 막혀 집단 안의 지식에 닿기 어려웠어요. 이 문장은 그 지식을 얻으려면 집단 안으로 들어가 구성원이 되어야 한다는 말이에요.",
                 button="다음",
                 panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/member-join.svg",
                        "alt": "바깥에 있던 외부인이 지식 보유자 집단 안으로 들어가 구성원이 되어 가운데 지식 곁에 선다"},
                 highlight=["one needs to become a member of the relevant group of knowledge bearers"]),
            # 수능은 같은 쪽 단어 묶음이 중요 — 내부자(전문가) ↔ 외부자(초보자)
            show("s2_groups",
                 "수능에서는 같은 쪽 단어 묶음이 중요해요. 이 글은 내부자(전문가)와 외부자(초보자)의 대비가 계속 반복돼요. 첫 단어는 넣어 뒀으니, 나머지는 직접 옮겨 봐요.",
                 button="다음",
                 panel=groups_board(1, 1, fresh=("knowledge bearers", "outsiders"))),
            sort_word("s2_sort_member", "a member", "구성원", True, 1, 1,
                      "a member는 집단의 구성원이라 집단 안, 내부자 쪽이에요."),
            sort_word("s2_sort_comm", "epistemic communities", "지식 공동체", True, 2, 1,
                      "epistemic communities는 지식 보유자 집단 그 자체라 내부자 쪽이에요."),
            show("s2_groups_done", "구성원(a member)과 지식 공동체(epistemic communities)는 집단 안, 내부자 쪽이에요.",
                 button="다음", panel=groups_board(3, 1, fresh=("a member", "epistemic communities"))),
            # 맞히든 틀리든 슬래시로 덩어리를 나눠 보여 준다. 콤마 사이는 삽입이 아니라 메인 문장 — 흐리지 않는다
            show("s2_slash",
                 "'To acquire …'는 '~하기 위해'라서 주어가 아니에요. 콤마 사이가 주어와 동사가 있는 메인 문장이라 꼭 읽어야 해요.",
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
        "teaching_value": "medium",
        "glosses": [g("A newcomer", "새로 온 사람"), g("learns", "배운다"), g("from experts", "전문가들로부터"),
                    g("and", "그리고"), g("is socialized", "사회화된다, 익숙해진다"),
                    g("into the common practices", "공동 관행 속으로"), g("the common practices", "공동 관행"),
                    g("the relevant epistemic community", "관련 지식 공동체"),
                    g("newcomer", "새로 온 사람"), g("experts", "전문가"), g("is socialized into", "~에 사회화되다, 익숙해지다"),
                    g("common practices", "공동 관행"), g("community", "공동체, 집단")],
        "steps": [
            # 주어·동사 찾기 — and 뒤에 주어 없이 동사가 또 온다 (동사 두 개)
            {
                "id": "s3_sv", "type": "pick", "interaction": "word_pick", "shade": True, "no_unknown": True,
                "candidates": ["A newcomer", "learns", "from experts", "and", "is socialized",
                               "into the common practices", "the relevant epistemic community"],
                "answers": ["A newcomer", "learns", "is socialized"],
                "roles": {"A newcomer": "S", "learns": "V", "is socialized": "V"},
                "brief": {
                    "ask": "이번엔 주어(S)와 동사(V)를 찾아볼까요? 동사가 하나가 아닐 수도 있어요.",
                    "wrong": "그건 주어나 동사가 아니에요.",
                    "wrong_by": {
                        "from experts": "from 같은 전치사가 붙은 덩어리는 주어나 동사가 될 수 없어요.",
                        "into the common practices": "into 같은 전치사가 붙은 덩어리는 주어나 동사가 될 수 없어요.",
                        "and": "and는 앞뒤를 이어 주는 말이에요. and 뒤에 무엇이 오는지 봐요.",
                        "the relevant epistemic community": "of 뒤 덩어리라 주어가 아니에요.",
                    },
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "다 찾았어요!",
                    "explain": "주어는 A newcomer, 동사는 learns와 is socialized 두 개예요.",
                    "point": "A newcomer(S) learns(V) … and is socialized(V) … · and 뒤에 주어 없이 동사가 오면 앞 주어의 동사가 하나 더",
                },
                "method": 0,
            },
            show("s3_and",
                 "and 뒤에 주어 없이 동사가 바로 오면, 앞 주어의 동사가 하나 더 있는 거예요. 그래서 A newcomer가 learns도 하고, is socialized도 돼요.",
                 button="다음", highlight=["and is socialized"], highlight_alt=["A newcomer"]),
            # 전치사의 목적어 — from experts의 experts, into the common practices의 the common practices
            {
                "id": "s3_prep", "type": "pick", "interaction": "word_pick", "shade": True,
                "candidates": ["A newcomer", "experts", "the common practices", "is socialized"],
                "answers": ["experts", "the common practices"],
                "roles": {"experts": "전목", "the common practices": "전목"},
                "brief": {
                    "ask": "from, into 같은 전치사 뒤의 명사는 '전치사의 목적어'예요. 이 문장에서 두 개를 찾아볼까요?",
                    "wrong": "그건 전치사의 목적어가 아니에요.",
                    "wrong_by": {
                        "A newcomer": "A newcomer는 문장의 주어예요. 전치사 from, into 바로 뒤를 봐요.",
                        "is socialized": "is socialized는 동사예요. 전치사 from, into 바로 뒤를 봐요.",
                    },
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "맞아요! experts는 from의, the common practices는 into의 목적어예요.",
                    "explain": "from experts의 experts, into the common practices의 the common practices가 전치사의 목적어예요.",
                    "point": "전치사 + 명사 = 전치사의 목적어 · from experts(전문가들로부터), into the common practices(공동 관행 속으로) · 문장의 목적어(O)와는 달라요",
                },
                "method": 0,
            },
            # 핵심어로 상황 요약 — newcomer, learns, experts, is socialized, community
            {
                "id": "s3_sum", "type": "translate", "interaction": "free_translation",
                "model": "새로 온 사람은 전문가로부터 배우고, 그 집단에 사회화된다.",
                "labels": {"mine": "내 요약", "model": "요약 예시"},
                "rules": [
                    {"id": "newcomer", "need": ["새로", "새 ", "신입", "초보", "신참", "뉴커머"], "fix": "새로 온 사람은"},
                    {"id": "experts", "need": ["전문가"], "fix": "전문가로부터"},
                    {"id": "learns", "need": ["배우", "배운", "학습", "익히", "익힌"], "fix": "배우고"},
                    {"id": "socialized", "need": ["사회화", "익숙", "적응", "녹아", "어울", "물들"], "fix": "사회화된다"},
                    {"id": "community", "need": ["집단", "공동체", "그룹", "모임", "단체"], "fix": "그 집단에"},
                ],
                "highlight": ["newcomer", "learns", "experts", "is socialized", "community"],
                "brief": {
                    "ask": "노란 핵심어만 보고, 직역 말고 어떤 상황인지 간단히 요약해서 써 봐요.",
                    "praise": "잘 요약했어요! 핵심어만으로도 상황이 보여요.",
                    "wrong": "고친 부분을 같이 봐요.",
                    "explain": "괜찮아요. 요약 예시를 같이 봐요. 연습할 문장으로 저장해 둘게요.",
                    "feedback": {
                        "newcomer": "newcomer는 '새로 온 사람'이에요.",
                        "experts": "experts는 '전문가'예요.",
                        "learns": "learns는 '배운다'예요.",
                        "socialized": "is socialized는 '사회화된다, 익숙해진다'예요.",
                        "community": "community는 '공동체, 집단'이에요. 앞 문장의 그 집단이에요.",
                    },
                    "placeholder": "어떤 상황인지 한 줄로 써 보세요",
                    "point": "A newcomer learns from experts and is socialized into … community = 새로 온 사람은 전문가로부터 배우고 그 집단에 사회화된다",
                },
                "method": 0,
            },
            sort_word("s3_sort_experts", "experts", "전문가", True, 3, 1,
                      "experts는 지식을 가진 전문가라 내부자 쪽이에요."),
            sort_word("s3_sort_newcomer", "a newcomer", "새로 온 사람", False, 4, 1,
                      "a newcomer는 이제 막 들어오는 사람이라 초보자 쪽이에요."),
            show("s3_draft", "새로 온 사람은 전문가에게 배우며 그 공동체의 관행에 익숙해져요. 단어 지도에도 붙여 둘게요.",
                 panel=groups_board(4, 2, fresh=("experts", "a newcomer"))),
        ],
    },
    {
        "id": 4,
        "text": "(②) Often there are admittance processes, combined with tests of a candidate’s abilities.",
        "model_translation": "자주 후보자의 능력에 대한 시험과 결합한 입회 절차가 존재한다.",
        "teaching_value": "medium",
        "glosses": [g("Often", "자주"), g("there", "(there are: ~이 있다)"), g("are", "있다"),
                    g("a candidate’s abilities", "후보자의 능력"),
                    g("admittance processes", "입회 절차"), g("combined with", "~와 결합된"), g("tests", "시험"),
                    g("candidate", "후보자"), g("abilities", "능력"), g("admittance", "입회, 들어가는 것")],
        "steps": [
            sv_pick("s4_sv",
                    ["Often", "there", "are", "admittance processes", "combined with", "tests", "a candidate’s abilities"],
                    {"are": "V", "admittance processes": "S"},
                    "이번엔 주어(S)와 동사(V)를 찾아볼까요?",
                    {"Often": "Often은 '자주'라서 주어나 동사가 아니에요.",
                     "there": "there are 문장에서 there는 주어가 아니에요. 주어는 are 뒤에 와요.",
                     "combined with": "combined with는 '~와 결합된'이라 앞 말을 꾸며 줘요. 문장의 동사가 아니에요.",
                     "tests": "tests는 with 뒤 덩어리예요. 전치사 뒤 덩어리는 주어·동사가 될 수 없어요.",
                     "a candidate’s abilities": "of 뒤 덩어리예요. 전치사 뒤 덩어리는 주어·동사가 될 수 없어요."},
                    "동사는 are, 주어는 are 뒤의 admittance processes예요.",
                    "there are + 명사 = 명사가 있다 · 주어는 are 뒤 admittance processes · combined with는 꾸미는 말"),
            show("s4_there",
                 "there are 문장은 are 뒤의 명사가 진짜 주어예요. 그래서 'admittance processes(입회 절차)가 있다'로 읽어요. combined with는 동사가 아니라 '~와 결합된'으로 앞 말을 꾸며 줘요.",
                 button="다음", highlight=["there are admittance processes"], highlight_alt=["combined with"]),
            # 요약 대신 — 핵심어(주어·동사 + tests) 짚고, 상황을 그림으로
            show("s4_key",
                 "핵심어는 주어·동사와 tests예요. 입회 절차(admittance processes)가 있고, 거기에 능력 시험(tests)이 붙어 있다는 말이에요.",
                 button="다음", highlight=["there are admittance processes", "tests"]),
            show("s4_pic",
                 "집단에 들어가는 문이 입회 절차예요. 후보자는 그 문을 지나기 전에 능력 시험을 봐요.",
                 button="다음",
                 panel={"kind": "picture", "title": "칠판 그림", "src": "/assets/admittance-test.svg",
                        "alt": "후보자가 능력 시험을 보고 입회 절차라는 문을 지나 지식 공동체 안으로 들어간다"}),
            sort_word("s4_sort_candidate", "a candidate", "후보자", False, 4, 2,
                      "a candidate는 아직 시험을 보는 후보자라 집단 바깥, 초보자 쪽이에요."),
            show("s4_draft", "",
                 panel=groups_board(4, 3, fresh=("a candidate",))),
        ],
    },
    {
        "id": 5,
        "text": "(③) In the premodern era, epistemic communities were often kept secret, with strict tests of loyalty for new members, not least because of fears that specialized knowledge would fall into the “wrong hands.”",
        "model_translation": "전근대적인 시대에는, 지식 공동체가 자주 비밀에 부쳐졌고, 신입 구성원에게 엄격한 충성심 시험이 있었는데, 특히 전문적인 지식이 '잘못된 손'에 들어갈 것이라는 두려움 때문이었다.",
        "teaching_value": "medium",
        "glosses": [g("In the premodern era", "전근대 시대에는"), g("for", "~에게"), g("the premodern era", "전근대 시대"), g("secret", "비밀인, 비밀"), g("epistemic communities", "지식 공동체"),
                    g("were often kept", "자주 (~하게) 유지되었다"), g("strict tests", "엄격한 시험"), g("new members", "신입 구성원"),
                    g("would fall", "떨어질 것이다, 들어갈 것이다"),
                    g("premodern era", "전근대 시대"), g("kept secret", "비밀에 부쳐진"), g("strict", "엄격한"), g("loyalty", "충성심"),
                    g("not least because of", "특히 ~때문에"), g("fears", "두려움"), g("specialized knowledge", "전문적인 지식"),
                    g("wrong hands", "잘못된 손 · 나쁜 사람")],
        "steps": [
            sv_pick("s5_sv",
                    ["the premodern era", "epistemic communities", "were often kept", "secret", "strict tests", "new members",
                     "fears", "specialized knowledge", "would fall"],
                    {"epistemic communities": "S", "were often kept": "V", "secret": "C"},
                    "이번엔 주어(S), 동사(V), 보어(C)를 찾아볼까요? 보어는 동사 뒤에서 주어가 어떤 상태인지 말해 줘요.",
                    {"the premodern era": "In 뒤 덩어리예요. 전치사 뒤 덩어리는 주어·동사가 될 수 없어요.",
                     "strict tests": "with 뒤 덩어리예요. 전치사 뒤 덩어리는 주어·동사가 될 수 없어요.",
                     "new members": "for 뒤 덩어리예요. 전치사 뒤 덩어리는 주어·동사가 될 수 없어요.",
                     "fears": "because of 뒤 덩어리예요. 전치사 뒤 덩어리는 주어·동사가 될 수 없어요.",
                     "specialized knowledge": "그건 that 뒤 덩어리(두려움의 내용) 안의 주어예요. 문장 전체의 주어가 아니에요.",
                     "would fall": "그건 that 뒤 덩어리 안의 동사예요. 문장 전체의 동사가 아니에요."},
                    "주어는 epistemic communities, 동사는 were often kept, 보어는 secret(비밀인 상태)이에요.",
                    "epistemic communities(S) were often kept(V) secret(C) · 뒤는 with(시험), because of(이유)로 덧붙임",
                    wrong="그건 주어·동사·보어가 아니에요."),
            show("s5_past",
                 "In the premodern era는 '전근대 시대에는', 즉 과거를 말해요. 모의고사에서는 과거와 현대의 대조가 자주 나와요. 뒤에서 지금은 어떤지 나오는지 봐요.",
                 button="다음", highlight=["In the premodern era"],
                 tips=[{"label": "pre-", "mark": "premodern",
                        "text": "pre-는 '~ 이전, 미리'라는 뜻이에요. pre + modern(근대) = 근대 이전, 즉 전근대예요. preview(미리 보기)의 pre-도 같아요."}]),
            key_summary("s5_sum", "옛날에는 지식 공동체가 비밀이었고, 신입에게 엄격한 충성심 시험이 있었다.",
                        [("past", ["옛날", "과거", "전근대", "예전", "옛"], "옛날에는"),
                         ("secret", ["비밀", "숨기", "숨겨", "감추", "감춰", "폐쇄", "닫"], "비밀이었고"),
                         ("test", ["시험", "테스트", "검사", "검증"], "시험"),
                         ("loyalty", ["충성"], "충성심")],
                        ["premodern era", "epistemic communities were often kept secret", "strict tests of loyalty"],
                        {"past": "In the premodern era는 '전근대 시대에는', 즉 옛날이에요.",
                         "secret": "were kept secret은 '비밀로 유지되었다'예요.",
                         "test": "tests는 '시험'이에요.",
                         "loyalty": "loyalty는 '충성심'이에요."},
                        "In the premodern era, epistemic communities were often kept secret … = 옛날엔 지식 공동체가 비밀이었고 충성심 시험이 있었다",
                        tips=[{"label": "not least because of", "mark": "not least because of",
                               "text": "'특히 ~때문에'예요. 비밀로 한 이유가 뒤에 나와요. 전문 지식이 '잘못된 손', 즉 나쁜 사람에게 들어갈까 봐서예요."}]),
            show("s5_draft", "옛날에는 지식 공동체가 비밀이었고, 신입에게 엄격한 충성심 시험이 있었대요."),
        ],
    },
    {
        "id": 6,
        "text": "(④) Some traces of these older practices may still be present today, but on the whole, the ideal has shifted to openness among the members of epistemic communities, and also, to some extent, toward outsiders.",
        "model_translation": "이러한 오래된 관행의 일부 흔적이 오늘날에도 여전히 존재할 수 있지만, 전체적으로 보아, 이상은 지식 공동체 구성원 사이에서 개방성, 그리고 또한, 어느 정도는, 외부인을 향한 것으로 옮겨 갔다.",
        "teaching_value": "high",
        "glosses": [g("Some traces", "일부 흔적"), g("these older practices", "이러한 오래된 관행"), g("may still be", "여전히 ~일 수 있다"),
                    g("but", "하지만"), g("the ideal", "이상, 바람직하다고 여기는 것"), g("has shifted", "옮겨 갔다, 바뀌었다"),
                    g("the members", "구성원들"), g("outsiders", "외부인"),
                    g("traces", "흔적"), g("older practices", "오래된 관행"), g("present", "존재하는"), g("on the whole", "전체적으로 봤을 때에는"),
                    g("ideal", "이상"), g("has shifted to", "~로 옮겨 갔다"), g("openness", "개방성"), g("to some extent", "어느 정도는"),
                    g("toward outsiders", "외부인을 향해")],
        "steps": [
            # 읽기 끝나면 먼저 주어·동사·보어·목적어를 모두 찾는다 (두 쌍)
            {
                "id": "s6_sv", "type": "pick", "interaction": "word_pick", "shade": True, "no_unknown": True,
                "candidates": ["Some traces", "these older practices", "may still be", "present", "but", "the ideal",
                               "has shifted", "openness", "the members", "outsiders"],
                "answers": ["Some traces", "may still be", "present", "the ideal", "has shifted", "openness"],
                "roles": {"Some traces": "S", "may still be": "V", "present": "C",
                          "the ideal": "S", "has shifted": "V", "openness": "전목"},
                "brief": {
                    "ask": "이 문장에는 주어·동사가 두 쌍 있어요. 주어(S), 동사(V), 그리고 보어(C)나 목적어까지 모두 찾아볼까요?",
                    "wrong": "그건 주어·동사·보어·목적어가 아니에요.",
                    "wrong_by": {
                        "these older practices": "of 뒤에서 traces를 꾸며 주는 말이에요. 주어는 그 앞에 있어요.",
                        "but": "but은 두 문장을 이어 주는 말이에요. but 뒤에 새 주어·동사가 와요.",
                        "the members": "among 뒤에서 꾸며 주는 말이에요.",
                        "outsiders": "toward 뒤에서 덧붙인 말이에요.",
                    },
                    "more": "좋아요! {n}개 남았어요.",
                    "praise": "다 찾았어요!",
                    "explain": "but 앞은 S Some traces, V may still be, C present예요. but 뒤는 S the ideal, V has shifted, to 뒤 openness예요.",
                    "point": "Some traces(S) may still be(V) present(C) … but … the ideal(S) has shifted(V) to openness(전목)",
                },
                "method": 0,
            },
            # 앞부분 뜻 — present는 '선물'·'현재의'가 아니라 '존재하는, 남아 있는'
            choice("s6_traces",
                   "노란 부분은 무슨 뜻일까요?",
                   [("o0", "옛 관행이 오늘날 사람들에게 선물이 될 수 있다", False),
                    ("o1", "옛 관행의 흔적이 오늘날에도 조금은 남아 있을 수 있다", True),
                    ("o2", "옛 관행이 오늘날 완전히 사라졌다", False)],
                   "traces는 '흔적', present는 여기서 '존재하는, 남아 있는'이에요.",
                   why="여기서 present는 '선물'이나 '현재의'가 아니라 '존재하는, 남아 있는'이에요. traces(흔적)라서 조금만 남아 있다는 말이에요.",
                   highlight=["Some traces of these older practices may still be present today"]),
            # but 뒤가 중요한 말
            show("s6_but",
                 "but은 앞과 뒤를 뒤집는 말이에요. 그래서 but 뒤가 글쓴이가 하고 싶은 중요한 말이에요.",
                 button="다음", highlight=["but"],
                 tips=[{"label": "on the whole", "mark": "on the whole",
                        "text": "'전체적으로 봤을 때에는'이라는 뜻이에요. whole만 떼어 '전체'로 읽지 말고 한 덩어리로 봐요."}]),
            # 그 밖의 핵심어 — members, outsiders
            show("s6_keys",
                 "핵심어 members(구성원)와 outsiders(외부인)도 봐요. 개방성이 구성원끼리, 그리고 어느 정도는 외부인에게까지 넓어졌다는 거예요.",
                 button="다음", highlight=["the members", "outsiders"]),
            # 칠판 — 과거 secret → 지금 openness (내부자도 외부자도)
            show("s6_board",
                 "내부자도 외부자도, 이상(=추구하는 바)이 secret(비밀)에서 openness(개방성), 즉 공개로 넘어갔어요.",
                 button="다음",
                 panel={"kind": "groups", "title": "칠판", "between": "→",
                        "left": {"label": "과거 · premodern", "words": [{"text": "secret", "ko": "비밀"}]},
                        "right": {"label": "지금 · today", "words": [{"text": "openness", "ko": "개방성 = 공개", "fresh": True}]},
                        "process": {"arrow": "→", "words": [{"text": "the ideal has shifted"}]},
                        "caption": "구성원(members)끼리도, 외부인(outsiders)에게도"}),
            sort_word("s6_sort_members", "the members", "구성원들", True, 4, 3,
                      "the members는 지식 공동체의 구성원들이라 내부자 쪽이에요."),
            show("s6_draft", "",
                 panel=groups_board(5, 3, fresh=("the members",))),
        ],
    },
    {
        "id": 7,
        "text": "(⑤) Other, more active strategies are needed to make certain forms of knowledge as “accessible” as is realistically possible.",
        "model_translation": "특정한 형태의 지식을 현실적으로 가능한 한 '접근 가능하게' 만들기 위해서는, 다른, 보다 더 적극적인 전략이 필요하다.",
        "teaching_value": "high",
        "glosses": [g("Other, more active strategies", "다른, 더 적극적인 전략"), g("to make", "만들기 위해"),
                    g("Other", "다른"), g("more active strategies", "더 적극적인 전략"), g("are needed", "필요하다"),
                    g("certain forms of knowledge", "특정한 형태의 지식"), g("accessible", "접근 가능한"),
                    g("realistically possible", "현실적으로 가능한")],
        "steps": [
            sv_pick("s7_sv",
                    ["Other, more active strategies", "are needed", "to make", "certain forms of knowledge", "accessible",
                     "realistically possible"],
                    {"Other, more active strategies": "S", "are needed": "V"},
                    "이번엔 주어(S)와 동사(V)를 찾아볼까요?",
                    {"to make": "to + 동사는 '~하기 위해'라서 문장의 동사가 아니에요.",
                     "certain forms of knowledge": "그건 make 뒤의 말이에요. 문장 전체의 주어가 아니에요.",
                     "accessible": "accessible은 '접근 가능한'이라 주어나 동사가 아니에요.",
                     "realistically possible": "'현실적으로 가능한'이라 주어나 동사가 아니에요."},
                    "주어는 Other, more active strategies, 동사는 are needed예요.",
                    "Other, more active strategies(S) are needed(V) to make … accessible"),
            key_summary("s7_sum", "지식을 접근 가능하게 만들려면 더 적극적인 전략이 필요하다.",
                        [("strategy", ["전략", "방법", "방안", "대책"], "전략이"),
                         ("active", ["적극"], "더 적극적인"),
                         ("need", ["필요", "해야"], "필요하다"),
                         ("access", ["접근", "다가", "닿", "쉽게", "알 수", "이해"], "접근 가능하게")],
                        ["more active strategies", "are needed", "knowledge", "accessible"],
                        {"strategy": "strategies는 '전략'이에요.",
                         "active": "more active는 '더 적극적인'이에요.",
                         "need": "are needed는 '필요하다'예요.",
                         "access": "accessible은 '접근 가능한'이에요."},
                        "Other, more active strategies are needed to make … knowledge … accessible = 지식을 접근 가능하게 하려면 더 적극적인 전략이 필요하다"),
            show("s7_draft", "지식을 최대한 '접근 가능하게' 하려면 다른, 더 적극적인 전략이 필요하대요.", button="문제 풀러 갈게요"),
        ],
    },
]

exam = {
    "question": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은? [3점]",
    "underline": ["(①)", "(②)", "(③)", "(④)", "(⑤)"],
    # 보기 글이 「… 앞」뿐이라 숫자 ①~⑤만 가로로 보인다
    "numbers_only": True,
    # 답 고르기 화면 — 지문 전체에 칠해 둘 핵심어 (①~⑤ 자리를 찾는 단서)
    "passage_highlight": ["Nonetheless", "for most outsiders", "even completely transparent practices", "kept secret", "the ideal has shifted to openness", "toward outsiders", "Other, more active strategies", "accessible",
                          # 자유 해석 대신 핵심어 짚기로 다룬 문장 3·5
                          "there are admittance processes", "tests", "Some traces", "older practices", "may still be present today", "but", "the members"],
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
        "ask": "핵심어 위주로 읽고 들어갈 곳을 찾아봐요. Nonetheless(그럼에도 불구하고)는 앞 문장과 내용이 달라질 때 써요. 이걸 잘 생각하고 골라 봐요.",
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
