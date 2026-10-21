---
name: word-meaning-grade-5-9
description: 단어·짧은 구절 뜻 묻는 3지는 5~9등급만, 1~4등급은 엔진이 건너뜀 (2026-10-21)
metadata:
  type: feedback
---
「to foster this attitude는 무슨 뜻일까요?」처럼 단어·짧은 구절 하나의 뜻을 세세하게 묻는 객관식은 5~9등급에만 남기고 1~4등급은 하지 않는다.

**Why:** 선생님 — 윗 등급에겐 불필요한 세부 질문이라 수업만 길어진다.
**How to apply:** 엔진 `session.ts` `isWordMeaningStep`이 질문 모양(영어 네 단어까지 + 「은/는 무슨 뜻일까요?」)으로 자동 판단, 예외는 스텝 `word_meaning: true/false`. 학생 등급은 StudentState.grade(가입·상담실), 모르면 단계 「고」만 건너뜀. 문장·절 뜻·도치 구조·문맥 다의어는 모두에게. 새 레슨도 이 질문 모양을 지키면 자동 적용. 틀: docs/tutor/templates/README.md §0-1. 관련 [[type-templates]] [[user-test-low-grade]]
