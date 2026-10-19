---
name: home-village-counsel
description: "홈(마을) 화면 — 집 = 기능 입구, 상담실 = 점수·목표·약점 듣고 커리큘럼 짜는 곳; 디자인은 사용자가 외부에서 만들어 옴"
metadata:
  node_type: memory
  type: project
  originSessionId: 5e279a3c-23d1-4286-a4c7-aaf0469ea76a
  modified: 2026-10-19T08:58:30.387Z
---

2026-10-19 홈 화면을 「마을」로 추가(HomeVillage.tsx). 집마다 들어가는 곳: 교무실=미니 모의고사(임시), 상담실=학습 상담, 보충학습실=단어장(임시).
상담실 = 내 점수 입력 · 목표 · 최근 부족한 것 얘기하며 **학습 커리큘럼을 짜는 곳** (CounselRoom.tsx, 규칙 src/tutor/counsel.ts, LLM 없이 버튼+규칙).

**Why:** 내가 손으로 그린 SVG 마을은 "너무 이상하다"는 평 → 사용자가 외부에서 만든 그림(광장 배경 + 집 3채 따로, public/assets/village/)으로 교체함(2026-10-19).
**How to apply:** 그림을 손으로 그리지 말고 받은 그림을 조합할 것(간판 글자는 HTML로 얹음). 그림을 바꿀 때도 흐름(App의 home/counsel 상태, 집 onOpen 연결)은 유지. 교무실·보충학습실 용도는 아직 미정 — 사용자가 정하면 갱신. 관련: [[reference-lesson-2026-q21]]
