---
name: one-demo-address
description: 로컬 데모는 모든 대화가 http://127.0.0.1:5173 하나만 — 떠 있으면 loopin-attach로 붙고 새 포트 띄우지 않기
metadata:
  type: feedback
---

2026-10-20 선생님: "대화마다 데모 링크 누르면 뜨는 게 조금씩 다른데 통일 가능해?" — 원인은 대화마다 다른 포트(5173·5174·5175·5190)에 서버를 띄운 것.
코드는 같아도 주소가 다르면 브라우저 저장소(진행 기록·등급·이어 하기·풀이법 설명 본 횟수·Tip 노출)가 따로라 화면이 달라진다.
localhost와 127.0.0.1도 서로 다른 주소로 친다.

**Why:** 선생님이 어느 대화에서 열어도 같은 상태를 보게.
**How to apply:** `.claude/launch.json`은 `loopin-dev`(5173, strictPort) 하나만 실제로 띄우고 나머지 이름은 모두 http://127.0.0.1:5173에 붙는다.
이미 떠 있으면 `preview_start {name: "loopin-attach"}`. 다른 포트·localhost 주소로 띄우지 말 것. 링크를 줄 때도 http://127.0.0.1:5173/ (?lesson= 같은 파라미터 없이, 필요할 때만).
공유용 아티팩트 링크([[share-test-link]])는 별개 — 올린 시점의 한 장 HTML이라 로컬과 다를 수 있다.
