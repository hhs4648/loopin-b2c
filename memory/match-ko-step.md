---
name: match-ko-step
description: 해석 맞추기 — 중·초 짧은 문장 모두(고 미정); 같은 자리(slot)에 방식 여러 개 두고 최근에 덜 한 방식을 돌려 냄(듀오링고처럼)
metadata:
  type: project
---

해석 맞추기(2026-10-14 선생님 "너무 괜찮아"): 짧은 문장에서 영어 덩어리를 한국어 해석 칸에 끌어 맞춘다. 긴 문장 절대 X. 전체 문장 아니어도 S·V·O/C+핵심어만으로 OK.
- 단계: **중·초는 짧은 문장이면 모두 돌려 내기 후보**(대체이지 추가가 아니라서, 2026-10-14 선생님 재결정). 고는 미정
- **맞추기를 하는 문장은 주어·동사 찾기, 뜻 다시 풀어 주기, 뜻 객관식을 건너뛴다** — 둘 다 하면 반복적(세션이 자동으로: roles 있는 pick + `meaning_check: True` 스텝)
- **매번 내면 절대 안 됨** — 이것저것 섞어 내야 덜 질린다(듀오링고처럼)

**How to apply:** 뜻 확인 자리에 방식 여러 개(객관식·맞추기·요약·자유 해석)를 적고 같은 `slot`을 단다 → 세션이 단계(`levels`)에 맞는 것 중 학생의 `recentFormats`(최근 6개)에서 가장 오래전/안 한 방식을 하나 고른다. 맞추기는 `levels=["중","초"]`. pick + `match: {ko:[…]}`, `src/components/MatchKo.tsx`. 첫 적용: 6월 34번 s1_match / s1_meaning(slot s1_meaning). [[free-translation-step]] [[svo-finding]]
