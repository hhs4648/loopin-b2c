"""미니 모의고사 — 2024년 3월 고3 영어 · 21~45번 시험지 순서대로 (쉬운 문항 빼고)를 만든다.

선생님 요청(2026-10-18): 학생이 22번부터 차례로 시간을 재며 풀고, 답을 맞혀 보고, 해설을 보고, 분석 레슨으로 넘어간다.
오답률 순이 아니라 시험지 순서. 쉬운 문항은 뺀다 — 25(도표)·26(내용 일치)·27·28(안내문). 21·45번은 선생님 요청으로 넣었다(2026-10-18).
분석 레슨이 있는 문항(Top 15 중 22번 이후)은 「다정쌤과 분석하기」, 없으면 해설(출제의도·고친 줄·해석).

원문: content/tutor/exam-source/2024-03-고3/문제.txt(영어) · 해설.txt(해석·출제의도).
문제지 PDF에서 빈칸(____)과 23번 E = mc²(그림)가 빠져서 뽑혔다 — 아래 FIXES로 되돌린다.

    python3 scripts/mini/gen_eng_2024_03_full.py
"""
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = f"{ROOT}/content/tutor/exam-source/2024-03-고3"
OUT = f"{ROOT}/content/tutor/mini-mocks/eng-2024-03-full.json"

ANSWERS = {21: 5, 22: 3, 23: 1, 24: 5, 29: 4, 30: 3, 31: 1, 32: 1, 33: 3, 34: 1, 35: 4, 36: 2, 37: 5, 38: 4, 39: 2,
           40: 1, 41: 3, 42: 4, 43: 4, 44: 4, 45: 5}
KINDS = {21: "밑줄 의미", 22: "요지", 23: "주제", 24: "제목", 29: "어법", 30: "어휘", 31: "빈칸", 32: "빈칸", 33: "빈칸", 34: "빈칸",
         35: "무관한 문장", 36: "순서", 37: "순서", 38: "문장 넣기", 39: "문장 넣기", 40: "요약문", 41: "제목",
         42: "어휘", 43: "순서", 44: "지칭", 45: "내용 일치"}
# 오답률 Top 15 (content/tutor/exam-stats 2024-03 고3) — 그 밖의 문항은 공개 자료가 없다
WRONG = {21: 49.9, 24: 50.3, 30: 45.9, 31: 71.0, 32: 66.3, 33: 56.1, 34: 71.9, 36: 38.9, 37: 67.3, 38: 57.2, 39: 78.1,
         40: 48.3, 42: 40.2}
LESSON = {n: f"moeui-2024-03-{n}" for n in ANSWERS}
_sets = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "content", "tutor", "sets.json")))
LESSON_FILE = {n: next(x["lessons"][0] for x in _sets["sets"] if x["id"] == sid) for n, sid in LESSON.items()}  # 21문항 모두 다정쌤 분석이 있다
FIX = {29: "④ which → into which (in which도 어법은 맞지만, be born into ~(~에 태어나다)라서 into which가 더 자연스러움)", 30: "③ invalid → privileged", 42: "(d) relieve → fuel"}
QUESTION = {
    **{n: "다음 빈칸에 들어갈 말로 가장 적절한 것을 고르시오." for n in (31, 32, 33, 34)},
    35: "다음 글에서 전체 흐름과 관계 없는 문장은?",
    36: "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것을 고르시오.",
    37: "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것을 고르시오.",
    38: "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳을 고르시오.",
    39: "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳을 고르시오.",
}
# 주어진 문장이 끝나는 말 (문장 넣기)
GIVEN_END = {38: "“at-risk” groups.", 39: "how they looked."}
FIXES = [
    (r"there was an[\s\ue000-\uf8ff]+of social science", "there was an E = mc² of social science"),  # 수식 그림 글자
    (r"with an accompanying\s+of the spontaneity", "with an accompanying ________ of the spontaneity"),
    (r"They insist that they\s*\.", "They insist that they ________."),
    (r"the Stoics warned against\s*\.", "the Stoics warned against ________."),
    (r"announced in 1973 that\s*:", "announced in 1973 that ________:"),
    (r"to mean \(A\)\s+upon molding", "to mean (A) ________ upon molding"),
    (r"capable of \(B\)\s*\.", "capable of (B) ________."),
    (r"\(\s*([①②③④⑤])\s*\)", r"(\1)"),
    (r"\(([A-D])\)(?=[A-Z])", r"(\1) "),
    (r"가장 적절 한", "가장 적절한"),
    (r"\s*\* 확인 사항.*$", ""),  # 시험지 끝 안내
]

raw = open(f"{SRC}/문제.txt", encoding="utf-8").read()
raw = re.sub(r"\S*øÇx.*?c\x00?o\x00?m", " ", raw, flags=re.S)       # 쪽 아래 깨진 글자
raw = re.sub(r"=====PAGE[^\n]*", " ", raw)
raw = raw.replace("\xad", "-").replace("\x00", "")
raw = re.sub(r"\[\d\d[~∼]\d\d\][^\[]*?(?:답하시오|고르시오)\.", " § ", raw)  # 묶음 안내 → 경계
Q = re.sub(r"\s+", " ", raw)
for a, b in FIXES:
    Q = re.sub(a, b, Q)
Q = re.sub(r"\s*[\ue000-\uf8ff]+", "", Q)  # 남은 그림 글자
H = open(f"{SRC}/해설.txt", encoding="utf-8").read()
NUM = r"(?<![\d(]){}\.\s?(?=[다밑주글윗A-Z“])"


def block(n):
    """문제지에서 n번 덩어리 — 다음 번호나 묶음 경계(§) 앞까지"""
    m = re.search(NUM.format(n), Q)
    rest = Q[m.end():]
    ends = [x.start() for x in [re.search(NUM.format(n + 1), rest), re.search("§", rest)] if x]
    return rest[: min(ends)].strip() if ends else rest.strip()


def long_part(n):
    """장문 본문 — 묶음 경계(§) 뒤부터 첫 문항 번호 앞까지"""
    j = re.search(NUM.format(n), Q).start()
    return Q[Q.rfind("§", 0, j) + 1: j].strip()


def take_foot(text):
    """끝의 *각주를 떼어 낸다"""
    m = re.search(r"\s?(\*\s?[a-z].*)$", text)
    return (text[: m.start()].strip(), m.group(1).strip()) if m else (text.strip(), "")


def options_of(text):
    parts = re.split(r"\s*[①②③④⑤]\s*", text)
    return parts[0].strip(), [p.strip() for p in parts[1:6]]


def clean_ko(s):
    s = re.sub(r"\s*=====PAGE \d+\s*\d*\s*", "", s).strip()
    return re.sub(r"[\ue000-\uf8ff]+", "E = mc²", s)  # 23번 수식 그림 글자


def ko(n):
    """해설지 — [출제의도] 한 줄과 해석(끝에 붙은 단어 목록 앞까지)"""
    blk = H[H.find(f"{n}.[출제의도]"): H.find(f"{n + 1}.[출제의도]")]
    head = re.match(r"\d\d\.\[출제의도\]\s*([^.]*\.)", blk)
    text = blk[head.end():]
    m = re.search(r"(?:\.(?=[a-zA-Z①②③④⑤(])|[”’)](?=[a-z]{3,}))", text[10:])
    trans = text[: 10 + m.start() + 1] if m else text
    return f"[출제의도] {head.group(1)}", clean_ko(trans)


def ko_long(tag, end):
    i = H.find(tag) + len(tag)
    text = H[i: H.find(end, i)]
    m = re.search(r"[.”’)](?=[a-z]{3,})", text)
    return clean_ko(text[: m.start() + 1] if m else text)


items = []
for n in ANSWERS:
    it = {"no": n, "kind": KINDS[n], "answer": ANSWERS[n]}
    if n in (41, 42):
        passage, foot = take_foot(long_part(41))
        q, opts = options_of(block(n))
        if n == 41:
            it.update(question=q, options=opts)
        else:
            it.update(question=q, options=["(a)", "(b)", "(c)", "(d)", "(e)"], marked=True)
        it.update(group="[41~42] 다음 글을 읽고, 물음에 답하시오.", passage=passage, foot=foot)
        it["intent"] = "[출제의도] " + ("글의 제목을 추론한다." if n == 41 else "문맥상 부적절한 어휘를 찾는다.")
        it["translation"] = ko_long("[41~42]", "41.[출제의도]")
    elif n in (43, 44, 45):
        body, foot = take_foot(long_part(43).replace("*twinkle: 반짝임", " "))  # 각주가 (C)와 (D) 사이에 있다
        paras = [take_foot(p.strip())[0] for p in re.split(r"(?=\([A-D]\) )", body) if p.strip()]
        q, opts = options_of(block(n))
        if n == 43:
            it.update(question=q, options=opts, given=paras[0], paragraphs=paras[1:])
        elif n == 44:
            it.update(question=q, options=["(a)", "(b)", "(c)", "(d)", "(e)"], marked=True, paragraphs=paras)
        else:
            it.update(question=q, options=opts, paragraphs=paras)
        it.update(group="[43~45] 다음 글을 읽고, 물음에 답하시오.", foot="*twinkle: 반짝임")
        it["intent"] = "[출제의도] " + {43: "글의 순서를 파악한다.", 44: "가리키는 대상이 다른 것을 찾는다.", 45: "글의 세부 내용을 파악한다."}[n]
        it["translation"] = ko_long("[43~45]", "43.[출제의도]")
    else:
        b = block(n)
        three = "[3점]" in b
        b = re.sub(r"\s*\[3점\]\s*", " ", b).strip()
        if n in QUESTION:
            q = QUESTION[n]
            b = b.replace(q, "").strip()
        else:
            m = re.match(r"(.*?것은\??)\s*(.*)", b)
            q, b = m.group(1), m.group(2)
        if n in (29, 30, 35, 38, 39):
            body, opts = b, ["", "", "", "", ""]        # 번호는 본문 안에 있다
        else:
            body, opts = options_of(b)
        if n == 40:
            body, summ = body.split("While some understand")
            it["after"] = ("While some understand" + summ.replace("(A) (B)", "")).strip()
        body, foot = take_foot(body)
        it["question"] = q + (" [3점]" if three else "")
        if n in (36, 37):
            given, rest = body.split("(A) ", 1)
            parts = re.split(r"\s*\((B|C)\)\s*", "(A) " + rest)
            paras = [parts[0]] + [f"({parts[k]}) {parts[k + 1]}" for k in range(1, len(parts) - 1, 2)]
            last_foot = take_foot(paras[-1])[1]
            it["given"] = given.strip()
            it["paragraphs"] = [take_foot(p)[0] for p in paras]
            foot = foot or last_foot
        elif n in (38, 39):
            end = body.index(GIVEN_END[n]) + len(GIVEN_END[n])
            it.update(given=body[:end].strip(), passage=body[end:].strip())
        else:
            it["passage"] = body.strip()
        it["options"] = opts
        if foot:
            it["foot"] = foot
        if n in (29, 30):
            it["marked"] = True
        if n == 21:
            it["underline"] = "you taste its price"
        it["intent"], it["translation"] = ko(n)
    it["points"] = 3 if "[3점]" in it["question"] else 2
    if n in WRONG:
        it["wrong_rate"] = WRONG[n]
    if n in LESSON:
        it["lesson"] = LESSON[n]
        # 선지 해석 — 분석 레슨 보기의 뜻(ko). 영어 선지만 (한국어 선지·번호만인 문항은 뺀다)
        les = json.load(open(f"{ROOT}/content/tutor/policy-lessons/{LESSON_FILE[n]}.json"))
        ops = les.get("exam", {}).get("options", [])
        if any(it["options"]) and len(ops) == len(it["options"]) and all(o.get("ko") for o in ops) \
                and not re.search(r"[가-힣]", " ".join(it["options"])):
            it["options_ko"] = [o["ko"] if o["label"].strip() == (txt or "").strip() else f"{o['label']} — {o['ko']}"
                                for o, txt in zip(ops, it["options"])]
    if n in FIX:
        it["fix"] = FIX[n]
    items.append(it)

for it in items:
    for k in ("question", "given", "passage", "after", "foot", "translation"):
        assert "§" not in it.get(k, "") and "øÇ" not in it.get(k, ""), (it["no"], k)
        assert not re.search(r"[\ue000-\uf8ff]", it.get(k, "")), (it["no"], k)
    assert all("§" not in o and len(o) < 140 for o in it["options"]), it["no"]

mock = {
    "id": "eng-2024-03-full", "subject": "english",
    "title": "2024년 3월 고3 · 21~45번",
    "subtitle": "2024년 3월 시행 · 고3 전국연합학력평가 · 시험지 순서대로 (쉬운 문항 뺌)",
    "source": "2024년 3월 고3 전국연합학력평가 영어",
    "minutes": 45,
    "items": items,
}
json.dump(mock, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", OUT, len(items), "문항", sum(i["points"] for i in items), "점")
