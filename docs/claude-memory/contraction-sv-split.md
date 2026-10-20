---
name: contraction-sv-split
description: S·V 찾기에서 주어+동사 줄임말(it’s, That’s, you’ve)은 조각으로 나눠 it=S, ’s=V — 통째 V/S 표시 금지
metadata:
  type: feedback
---

it’s를 통째로 V로 표시한 것을 선생님이 "어색하다"고 함 (2026-10-18, 2024년 3월 24번 문장 4).
주어+동사 줄임말은 후보를 조각으로: `["it", "’s", "easy"]`, roles `{"it": "S", "’s": "V", "easy": "C"}`; you’ve been driving → `"you"` S + `"’ve been driving"` V (조각 뜻 g("’s", "~이다 (= is)") 등 추가). 질문은 "it’s는 it is를 줄인 말이에요. 주어(S)·동사(V)·보어(C)를 찾아볼까요?"
부정 줄임말(don’t, wasn’t, isn’t, can’t)은 동사 덩어리라 그대로 V.

**Why:** it’s에 V만 붙이면 주어 it이 사라지고 가주어 구조가 안 보인다.

**How to apply:** glosses.ts splitPhraseGlosses·exam_kit split_phrase_glosses가 두 조각이 다 후보면 줄임말을 조각으로 나눈다(’ve been driving처럼 조각으로 시작하는 덩어리도). 12·21·24·40·42번 고침. [[svo-finding]]

**2026-10-18 추가 (선생님 「it이 가주어라서 논란이 될 수 있을 거 같아」):** 가주어 it(it’s easy/better to ~)은 S·V·C를 붙이지 않고 「진짜 주어 찾기」 pick으로 — 후보 it’s(오답: 자리만 채우는 가주어) / to 덩어리(정답) / 다른 덩어리, 표시 없음. 24번 문장 4(to mistake …, to treat … 둘), 12번 문장 3(to take a rest). 비인칭 It’s time to(42번 문장 4)는 S·V 찾기 빼고 해석 맞추기만(add_basic sv_new 없이).
