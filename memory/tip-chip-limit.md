---
name: tip-chip-limit
description: 되풀이 💡 참고 칩은 학생 전체에서 3번(안 누르면 5번)까지만 — 전체 정책, tipExposure.ts
metadata:
  type: feedback
---

2026-10-14 사용자 정책: 「왜 핵심어만 보나요?」 같은 참고 칩을 매번 띄우지 말 것. 수능·모의고사 수업에서 앱 설치~삭제까지 같은 칩은 3번만, 학생이 한 번도 안 누르면 5번 띄우고 없앤다. "전체 정책".

**Why:** 같은 설명을 계속 보이면 소음이 된다. 한 번 읽은 학생에겐 몇 번이면 충분하고, 안 누르는 학생에게도 무한히 보일 필요는 없다.

**How to apply:** 새로 만드는 되풀이 칩(같은 label로 여러 레슨에 나오는 💡)은 자동으로 이 제한을 받는다(`takeTipShow`, `noteTipOpened`, 칩 이름=label 기준). 힌트 칩(`hint: true`)은 제외. 레슨마다 한 번 나오는 칩(grasp 등)은 사실상 영향 없음. [[type-templates]]
