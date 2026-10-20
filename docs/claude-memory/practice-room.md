---
name: practice-room
description: "연습실(보충학습실)은 단어·문장·문법 세 탭 — 문장은 해석 맞추기(틀린 지문·연습할 문장), 단어는 코스 정규 칸 + 10분 전 주요 단어 미리 보기 (2026-10-20)"
metadata:
  node_type: memory
  type: project
  originSessionId: 366a5c43-e885-4119-8361-ad866907eab8
  modified: 2026-10-20T05:25:36.134Z
---

2026-10-20 선생님: 「영어 덩어리 ↔ 한국어 해석 끌어 맞추기」가 해석에 가장 유용 → 연습실에서 틀린 지문·헷갈린 문장으로 연습. 연습실은 **단어 / 문장 / 문법** 세 탭(`PracticeRoom.tsx`; 단어장은 단어 탭으로 들어감, 내 노트는 따로). 문장 탭 = `SentencePractice.tsx`(자료 `sentencePractice.ts`: 노트의 「연습할 문장」 → 최근 틀린 지문 → 본 지문, match 자료 있는 문장만). 단어는 너무 중요 → 코스에 **단어 칸**(`vocab-<10분 id>`, 한 회 풀면 바로 그 회 주요 단어 테스트, `counsel.ts` vocabSlot*) + 10분 풀기 전 **「주요 단어 보고 풀게요」**(뜻 가린 카드, `MiniWords`).

**보류:** 고·중 학생의 주어·동사 찾기 빈도를 줄이고 맞추기로 대체하자는 뜻(「조금 줄여야 할 것 같긴 해」) — 세션에서 맞추기를 고·중에도 열고 우선하게 바꿔 봤더니 기존 흐름 테스트 26개와 부딪혀 되돌림. 어느 문장(짧은 것만? 긴 문장 S·V는 유지?)에 어떻게 줄일지 선생님과 정한 뒤 적용.

**How to apply:** 관련 [[match-ko-step]] [[svo-finding]] [[course-ten-min]]
