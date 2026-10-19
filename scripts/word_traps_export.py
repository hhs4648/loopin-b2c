"""헷갈리는 단어 엑셀 → 앱이 읽는 JSON (content/tutor/word-traps/traps.json).

    npm run traps:export          ← 엑셀을 고친 뒤

사용(O/X)이 **O인 줄만** 레슨 id별로 모은다 — 비어 있으면 아직 선생님이 안 본 후보라 뺀다(2026-10-16 선생님: 후보 Tip이 다 떠서 불필요). 앱은 그 단어가 나오는 문장에서
💡 Tip으로 띄운다(src/tutor/policy/traps.ts). 「문제」 칸(3월 36번 · 6월 37번)은 sets.json의 중분류로 레슨 id를 찾는다.
"""
import json
import os
import re

import openpyxl

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
XLSX = f"{ROOT}/content/tutor/word-traps/함정단어.xlsx"
OUT = f"{ROOT}/content/tutor/word-traps/traps.json"

sets = json.load(open(f"{ROOT}/content/tutor/sets.json"))
# 「3월」 → moeui-2026-03, 「6월」 → mopyeong-2026-06 (지금 있는 중분류 기준 — 같은 달이 둘 생기면 문제 칸을 더 자세히)
# 「2024년 3월」처럼 해가 있으면 그 해의 중분류 (2026-10-18 — 3월이 2024·2026 둘이 됨)
month_to_collection = {}
for g in sets["groups"]:
    for c in g["collections"]:
        m = re.search(r"(\d+)월", c["title"])
        if m:
            month_to_collection.setdefault(f"{m.group(1)}월", c["id"])
            y = re.search(r"(\d{4})(?:년|학년도)", c["title"])
            if y:
                month_to_collection.setdefault(f"{y.group(1)}년 {m.group(1)}월", c["id"])
lessons_of = {}
for s in sets["sets"]:
    lessons_of.setdefault((s["collection"], s["id"].rsplit("-", 1)[-1]), []).extend(
        l for l in s["lessons"] if not l.endswith("-v1"))

out, missing = {}, set()
ws = openpyxl.load_workbook(XLSX)["함정 단어"]
for row in ws.iter_rows(min_row=2, values_only=True):
    q, word, kind, mis, ko, who, use, *_ = list(row) + [None] * 8
    if not q or not word or str(use or "").strip().upper() != "O":
        continue
    m = re.match(r"((?:\d{4}년\s*)?\d+월)\s*(\d+)번", str(q))
    col = m and month_to_collection.get(re.sub(r"\s+", " ", m.group(1)))
    ids = lessons_of.get((col, m.group(2)), []) if m else []
    if not ids:
        missing.add(str(q))
        continue
    item = {"word": str(word).strip(), "kind": kind or "", "mis": (mis or "").strip(), "ko": (ko or "").strip(),
            "who": (who or "").strip()}
    for lid in ids:
        out.setdefault(lid, []).append(item)

json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=2)
print("ok", {k: len(v) for k, v in out.items()}, "레슨을 못 찾은 문제:", sorted(missing) or "없음")
