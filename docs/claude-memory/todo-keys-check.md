---
name: todo-keys-check
description: "할 일 — 선생님이 지문 표시판에서 핵심어를 직접 찍은 뒤, 표시판→생성기 KEYS 가져오기 스크립트 만들고 레슨에 keys_checked 켜기 (2026-10-20)"
metadata:
  node_type: memory
  type: project
  originSessionId: 366a5c43-e885-4119-8361-ad866907eab8
  modified: 2026-10-20T06:51:40.432Z
---

2026-10-20: AI가 고른 핵심어(emphasis/keys)가 엉뚱해서(24번 사례) 10분 모의고사 「핵심어만 읽고 풀기」 버튼은 **`keys_checked: true`인 레슨에서만** 보이게 함. 지금 켜진 레슨: 2026-03-33, 2026-03-24 (선생님이 확인). 나머지 10분 코스 레슨(2026-03 30·36·39, 2024-03 31·32·34·37·39, 2022-03 29·31·32·34·36 + 2회차 10개)은 버튼 숨김.

**할 일 (선생님이 표시판에서 직접 찍은 뒤):**
1. 지문 표시판(아티팩트 8kbfdYKS…, db `passages/<id>`)에서 찍은 핵심어를 읽어 각 생성기 `KEYS`/`EMPHASIS`에 넣는 가져오기 스크립트 (`scripts/lessons/import_keys.py` 같은 것)
2. 가져온 레슨 생성기에 `"keys_checked": True` 켜고 재생성 + `npm run policy:copy -- stamp <id>`
3. 핵심어 찾기 pick 스텝이 있는 문장은 `emphasis` 대신 `keys`(수업에선 안 칠함)

**How to apply:** 새 레슨도 같은 흐름 — 표시판에서 찍기 → 스크립트 → keys_checked. 관련 [[annotation-tool]] [[ten-min-keys-minimal]]
