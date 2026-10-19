---
name: board-drawer-and-pictures
description: "칠판(단어 지도·그림)은 문장 자리를 덮는 큰 서랍, 오른쪽 손잡이로 여닫기; 그림은 지문마다 지시받지 않고 그림 틀로"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 80a912c9-bcc3-4d30-8c7b-381aca5e7d02
  modified: 2026-10-13T06:05:21.553Z
---

2026-10-13 사용자: 칠판·그림을 한 화면에 우겨넣으면 너무 작다 → 흰 칠판이 크게 뜨고, 오른쪽 손잡이로 열고 닫고(누르거나 끌기), 필요할 때 자동으로 펼쳐지게.
구현: `src/components/BoardDrawer.tsx` — groups·picture·map 패널만 서랍, 작은 표(structure·mapping·note·contrast)는 문장 아래 그대로.
또 사용자는 "매번 지문마다 그림을 지시해야 하나?"라고 물었다 — 지문마다 직접 지시하지 않기를 원한다.

**Why:** 폰에서 그림이 작아 안 보였다. 대량 적용이 목표라 그림도 사람이 매번 지시하면 안 된다.

**How to apply:** 그림이 필요한 장면은 Claude가 판단해 그리고 확인만 받는다. 틀 만들 때 그림 틀(집단 안/밖, 대조, 원인→결과, 예전→지금, 비유)을 라벨 바꿔 쓰게 만든다. 넘겨받기 정리는 `handoff/틀-만들기.md`. [[reference-lesson-2026-q21]]

**2026-10-18 (23번 2문장 피드백):** 문장이 관계(A가 B에 맞선다, B는 C의 일부)를 말하면 단어를 칩으로 늘어놓지 말고 관계를 도식으로 그린다 — 「새 생각 →challenges→ 기존 생각 ⊂ 정체성 ⊂ 우리 무리(group)」 + 결과(위협). 파일 public/assets/new-idea-challenge.svg.

**2026-10-18 (31번 피드백 「학생이 이해를 못하더라 — 빵빵이 예시」):** 추상적인 대비(conventional ↔ originality)는 학생 생활 예시 그림으로 — 어릴 때 자동차를 '빵빵이'(내가 지어낸 말) → 자라면서 '자동차'(남들이 다 쓰는 말). public/assets/ppangppang-car.svg, 31번 s7_example. 그림 화면 말은 두 문장까지(폰에서 말풍선 잘림).
