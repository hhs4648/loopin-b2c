---
name: exam-year-labeling
description: "평가원(6·9월 모평·수능)은 학년도=시행연도+1, 교육청은 시행연도 그대로 — 제목 아래 「YYYY년 M월 시행」; 모의고사·수능 갈래 공통, 일반 영어는 별개"
metadata:
  node_type: memory
  type: project
  originSessionId: 80a912c9-bcc3-4d30-8c7b-381aca5e7d02
  modified: 2026-10-14T06:40:22.084Z
---

시험 제목 연도 규칙(2026-10-14 선생님): 평가원 시행(6월·9월 모의평가, 수능)은 제목이 「YYYY학년도」로 실제 시행연도 +1. 교육청 시행(3·4·7·10월 전국연합학력평가)은 제목 연도 = 시행연도. 헷갈리니 제목 아래 부제 맨 앞에 「YYYY년 M월 시행」(일자 없이)을 작게 단다.

**Why:** 시험마다 표기 연도와 실제 시행연도가 달라 학생이 헷갈린다. 관행이라 제목은 그대로 둔다.

**How to apply:** `content/tutor/sets.json` 중분류에 `exam: {body, held}`를 적고, 대분류 `track: "exam"`. 테스트가 검사. 지금 만드는 건 전부 모의고사·수능 갈래 — 나중에 만들 일반 영어는 다른 플로우로 별개 관리(`track: "general"`). 규칙 문서는 docs/tutor/templates/README.md §0. [[type-templates]]
