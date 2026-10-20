---
name: svo-finding
description: 주어·동사(S·V·O) 찾기 활동은 2026-10-20에 전부 삭제 — 끊어읽기(/ + S·V·O·C 표시)가 대신함. 세션이 roles pick·_sv 스텝을 건너뜀
metadata:
  node_type: memory
  type: feedback
  originSessionId: 366a5c43-e885-4119-8361-ad866907eab8
  modified: 2026-10-20T06:56:10.035Z
---

2026-10-20 선생님: "주어 동사 찾기 활동은 그냥 없애자, 어차피 끊어읽기가 있잖아. 그동안 만들어둔 주어 동사 활동 모두 삭제." (예전 규칙 — 긴 문장은 고·중·초 모두 S·V 찾기, 꾸밈 구조 표 — 는 폐기.)

**Why:** 끊어읽기 버튼을 켜면 S·V·O·C와 [ ] 수식어가 보이므로 직접 찾게 하는 활동은 되풀이. 고·중엔 해석 맞추기가 더 유용.

**How to apply:** 레슨 JSON·생성기의 S·V 스텝(`roles` 있는 pick, id가 `_sv`/`_svc`/`_basic_sv`로 끝나는 pick)은 그대로 두되 **세션(`session.ts` `isSvStep`)이 항상 건너뜀**(lastAction에도 안 남김). 같은 슬롯의 맞추기·객관식이 대신 나옴. 새 레슨 생성기에 S·V 스텝을 더 만들지 말 것. v1 39번 S·V 테스트는 describe.skip. 관련 [[slash-reading-toggle]] [[match-ko-step]] [[beginner-basic-per-sentence]]
