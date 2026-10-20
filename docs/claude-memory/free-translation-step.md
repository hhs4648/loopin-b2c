---
name: free-translation-step
description: 핵심어 나열형 자유 해석(translate method 0)은 2026-10-20 삭제 — 학생이 뭘 하라는지 모름. 문장 전체 자유 해석·자유 응답(method 1)만 남김. 빠진 자리는 해석 맞추기
metadata:
  node_type: memory
  type: feedback
  originSessionId: 366a5c43-e885-4119-8361-ad866907eab8
  modified: 2026-10-20T07:06:09.892Z
---

2026-10-20 선생님: "핵심어를 문장이 아닌 상태로 나열하니까 학생들이 뭘 하라는 건지 모르겠대. 문장이 성립하는 경우를 제외하고는 모두 삭제." → `translate` 스텝 중 **method 0**(핵심어만/노란 부분만 보고 해석·요약)은 세션이 항상 건너뜀(`isKeywordTranslate`). method 1(문장 전체 자유 해석 s2_free, 자유 응답 s1_art 같은 것)은 그대로.

주어·동사 찾기와 이 자유 해석을 뺀 문장에서는 **해석 맞추기(match)가 단계와 상관없이 그 자리를 대신**하고 돌려 내지 않음(`matchReplaces`). 맞추기를 한 문장은 뜻 질문(meaning_check)도 건너뜀. 맞추기 자료가 없는 문장은 데이터 세션이 채우는 중.

예전 규칙(짧고 중요한 문장은 가이드 뒤 직접 해석, 규칙 채점, ML용 기록, 틀리면 연습할 문장 저장)은 method 1 스텝에서만 살아 있음.

**How to apply:** 새 레슨에 핵심어 나열형 translate를 만들지 말 것. 관련 [[svo-finding]] [[match-ko-step]] [[practice-room]]
