---
name: recommend-and-explain
description: "사용자는 git·개발 관례를 잘 모른다 — 선택지가 생기면 가장 적절한 것을 내가 추천하고, 용어는 쉽게 풀어 설명한다"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f4cf0afa-03f4-4f2b-b5ef-960e6f14a2a3
  modified: 2026-10-19T17:15:43.456Z
---

사용자(선생님)는 git·빌드·개발 관례를 잘 모르는 편이다. 2026-10-20에 "앞으로도 네가 가장 적절한 걸 추천해줘, 난 잘 모르는 게 많거든"라고 했다.

**Why:** 선택지만 나열하면 결정을 못 한다. "추적이 안 된다"처럼 용어를 그대로 쓰면 다시 물어본다.

**How to apply:**
- 선택지가 생기면 추천 하나를 먼저, 이유를 한두 줄로 — 그다음에 대안
- git 용어(추적, 스테이지, 푸시 …)는 쓸 때 쉬운 말로 한 번 풀어 준다
- 큰 파일·되돌리기 어려운 일(수백 MB PDF 커밋, 푸시, 강제 덮어쓰기)은 먼저 멈추고 추천과 함께 묻는다 — 2026-10-20 모의고사 PDF 418MB는 .gitignore로 컴퓨터에만 두기로 함
- `__pycache__` 같은 자동 생성물은 올리지 않고 .gitignore에 넣는다
- 사용자의 Claude 기억 폴더 복사본 `memory/`는 저장소에 넣기로 했다(8221b26) — 새 기억을 쓰면 원본(~/.claude/projects/…/memory)에 쓰고, 저장소 쪽은 사용자가 요청할 때 맞춘다

[[reply-in-korean]]
