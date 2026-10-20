---
name: teaching-policy-direction
description: "Loopin B2C 전체 방향 — 새 Teaching Policy가 공식, 예전 해석 엔진은 나중에 폐기, LLM 최소화, UX/UI·말투 유지"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0cda2980-5eb8-42c5-af91-7c5e8a5f7f17
  modified: 2026-09-21T23:51:59.745Z
---

2026-09-22에 사용자가 정한 방향:

- **새 Teaching Policy(`src/tutor/policy/`, `content/tutor/policy-lessons/`)가 앞으로의 공식 policy.** 2025년 3월 고3 모의고사 21번부터 지문을 하나씩 만들며 정책을 고쳐 나간다.
- 예전 해석 엔진(`src/tutor/engine.ts`)과 예전 레슨 50개는 **지금은 그대로 두고 나중에 폐기**한다. 거기에 공을 들이지 않는다.
- **말투(캐릭터)와 가르치는 로직은 계속 분리**해서 운영한다.
- **LLM은 꼭 필요한 곳에만** (비용 통제). 웬만하면 코드·규칙으로 한다. 기준은 **학생에게 호출될 때 도는가**다 — 콘텐츠를 만들 때 한 번 쓰는 LLM은 비용으로 치지 않는다. 그래서 대사는 brief(말투 없는 내용)에서 다정쌤 말투로 미리 뽑아 JSON으로 두고(`content/tutor/policy-copy/`, `scripts/policy_copy.mjs`), 수업 중에는 읽기만 한다.
- 캐릭터 이름은 **다정쌤**으로 확정 (사용자가 말하는 "상냥쌤"은 같은 캐릭터).
- **UX/UI는 현재 것을 유지**한다.

**Why:** teaching policy를 대대적으로 바꾸는 중이고, 비용과 일관성 때문에 규칙 기반을 선호한다.

**How to apply:** 새 기능·지문은 policy 쪽에만 만든다. 예전 엔진을 고치자고 제안하지 않는다. LLM을 쓰자고 할 때는 코드로 안 되는 이유를 먼저 댄다. 화면을 새로 설계하지 않고 기존 화면에 선택 필드를 더하는 식으로 확장한다.
