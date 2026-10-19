"""3월 21번(손으로 쓴 기준 레슨)에 초급 기본을 넣는다 — 다시 돌려도 같다.

    python3 scripts/lessons/beginner_21.py
    npm run policy:copy stamp moeui-2026-03-21-music-researchers

문장마다 「주어·동사 찾기 + 뜻」 또는 「해석 맞추기」 하나 (2026-10-15 선생님). 훑고 넘기는 문장(4·5)은 넣지 않는다.
밑줄 문제라 7문장 맞추기는 글자 그대로의 해석만 — 밑줄의 속뜻은 말하지 않는다.
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beginner import add_basic, add_that_sv, fill_chunk_glosses, m, sv_step  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ID = "moeui-2026-03-21-music-researchers"
LP = f"{ROOT}/content/tutor/policy-lessons/{ID}.json"
CP = f"{ROOT}/content/tutor/policy-copy/dajung/{ID}.json"
ADDED = ("_basic_sv", "_match", "_basic_meaning", "_that_sv")

lesson = json.load(open(LP))
sentences = lesson["sentences"]
# 이전에 넣은 것을 걷어 낸다
for s_ in sentences:
    s_["steps"] = [st for st in s_["steps"] if not st["id"].endswith(ADDED)]
    for st in s_["steps"]:
        st.pop("slot", None)
        st.pop("meaning_check", None)

add_basic(sentences, 1, [m("A brilliant musician", "뛰어난 음악가는"), " ", m("in fact", "사실"), " 엄밀히 말해 ", m("an inventor", "발명가"), "가 ",
                         m("without", "아니면서도"), " ", m("an innovator", "혁신가"), "일 수 있다."],
          sv_new=sv_step("s1_basic_sv", ["A brilliant musician", "can in fact be", "an innovator", "an inventor"],
                         {"A brilliant musician": "S", "can in fact be": "V", "an innovator": "C"},
                         {"an inventor": "그건 without(~ 없이) 뒤의 말이에요."},
                         "주어는 A brilliant musician, 동사는 can in fact be, 보어는 an innovator(혁신가)예요."),
          meaning_ids=["s1_trans"])
add_basic(sentences, 2, [m("In such cases", "그런 경우에"), " ", m("great discoveries", "'위대한 발견'"), "을 ", m("expect", "기대하는"), " ",
                         m("those", "사람들은"), " ", m("will be disappointed", "실망할 것이다"), "."],
          sv_new=sv_step("s2_basic_sv", ["those", "expect", "will be disappointed"],
                         {"those": "S", "will be disappointed": "V"},
                         {"expect": "그건 who 뒤 덩어리 안의 동사예요. 문장 끝 쪽을 봐요."},
                         "주어는 those (who expect …)(~를 기대하는 사람들), 동사는 will be disappointed(실망할 것이다)예요."))
add_basic(sentences, 3, [m("the eager need for novelty", "새로움에 대한 간절한 욕구는"), " ", m("music", "음악"), "이 ",
                         m("no more than technique", "기술에 불과하다"), "는 ", m("the idea", "생각"), "을 ", m("involves", "담고 있다"), "."],
          match_display="the eager need for novelty involves the idea that music is no more than technique.",
          sv_new=sv_step("s3_basic_sv", ["the eager need for novelty", "involves", "the idea"],
                         {"the eager need for novelty": "S", "involves": "V", "the idea": "O"}, {},
                         "콜론 뒤 주어는 the eager need for novelty, 동사는 involves(담고 있다), 목적어는 the idea예요.",
                         ask="콜론(:) 뒤에서 주어(S)·동사(V)·목적어(O)를 찾아볼까요?"),
          meaning_ids=["s3_q"])
add_basic(sentences, 6, [m("each new music", "새 음악은 저마다"), " 자신을 ", m("the last thing in modernity", "현대성의 최신품"), "으로 ",
                         m("offers", "내놓고"), ", ", m("each musician", "음악가는 저마다"), " ", m("the patent", "특허"), "를 ", m("claims", "주장한다"), "."],
          match_display="In this arms race, each new music offers itself as the last thing in modernity; and each musician claims the patent on the invention.",
          sv_new=sv_step("s6_basic_sv", ["each new music", "offers", "itself", "each musician", "claims", "the patent"],
                         {"each new music": "S", "offers": "V", "itself": "O", "each musician": "S", "claims": "V", "the patent": "O"}, {},
                         "세미콜론 앞은 주어 each new music, 동사 offers, 목적어 itself예요. 뒤는 주어 each musician, 동사 claims, 목적어 the patent예요."),
          meaning_ids=["s6_q"])
add_basic(sentences, 7, [m("musicians", "음악가들은"), " ", m("just like everyone else", "다른 모두처럼"), " ", m("researchers", "'연구자'"),
                         "가 되는 것을 ", m("owe it to themselves", "스스로에게 해야 할 일로 여긴다"), "."],
          match_display="musicians owe it to themselves to become “researchers” just like everyone else.",
          sv_new=sv_step("s7_basic_sv", ["pastiches", "have become", "musicians", "owe it to themselves"],
                         {"musicians": "S", "owe it to themselves": "V"},
                         {"pastiches": "그건 where 뒤 덩어리 안의 주어예요. 콤마 뒤에서 찾아봐요.",
                          "have become": "그건 where 뒤 덩어리 안의 동사예요. 콤마 뒤에서 찾아봐요."},
                         "주어는 musicians, 동사는 owe it to themselves(스스로에게 ~할 의무가 있다)예요."))
# the idea that ~ 안이 핵심 (2026-10-16 선생님, 공통)
add_that_sv(sentences, 3, "s3_basic_sv", "s3_that_sv", ["a musical act", "is", "a thing"],
            {"a musical act": "S", "is": "V", "a thing": "C"}, {},
            "that 안의 주어는 a musical act(음악 행위), 동사는 is, 보어는 a thing(하나의 물건)이에요. 음악을 '물건'처럼 본다는 생각이에요.",
            ask="the idea that ~: that 뒤가 그 생각의 내용이에요. 그 안에서 주어(S)·동사(V)·보어(C)를 찾아볼까요?")
fill_chunk_glosses(sentences, {
    "A brilliant musician": "뛰어난 음악가", "can in fact be": "사실 ~일 수 있다", "an innovator": "혁신가", "an inventor": "발명가",
    "those": "사람들", "will be disappointed": "실망할 것이다", "the eager need for novelty": "새로움에 대한 간절한 욕구",
    "the idea": "생각", "music": "음악", "no more than technique": "기술에 불과한", "each new music": "새 음악 하나하나",
    "offers": "내놓다", "itself": "그 자신", "each musician": "음악가 하나하나", "the patent": "특허",
    "the last thing in modernity": "현대성의 최신품", "musicians": "음악가들", "have become": "~이 되었다",
    "owe it to themselves": "스스로에게 ~할 의무가 있다", "great discoveries": "위대한 발견들",
    "a musical act": "음악 행위", "a thing": "하나의 물건", "is": "~이다",
})

# 덩어리 안의 내용어도 단어 뜻이 있어야 한다
for sid, en, ko in [(3, "idea", "생각"), (6, "music", "음악")]:
    s_ = next(x for x in sentences if x["id"] == sid)
    if en not in {x["en"] for x in s_["glosses"]}:
        s_["glosses"].append({"en": en, "ko": ko})

json.dump(lesson, open(LP, "w"), ensure_ascii=False, indent=2)
c = json.load(open(CP))
c["steps"] = {k: v for k, v in c["steps"].items() if not k.endswith(ADDED)}
for s_ in sentences:
    for st in s_["steps"]:
        if st["id"].endswith(ADDED):
            c["steps"][st["id"]] = copy.deepcopy(st["brief"])
json.dump(c, open(CP, "w"), ensure_ascii=False, indent=2)
print("ok", ID)
