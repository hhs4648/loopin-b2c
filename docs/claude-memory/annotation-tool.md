---
name: annotation-tool
description: "선생님 지문 표시판(아티팩트 8kbfdYKSRM1e3F1PASz3G6) — 핵심어·+/−·헷갈릴 곳·문장 역할을 선생님이 눌러 표시, db passages/<lesson-id>에 저장, 레슨 만들 때 먼저 읽기"
metadata:
  node_type: memory
  type: reference
  originSessionId: 80a912c9-bcc3-4d30-8c7b-381aca5e7d02
  modified: 2026-10-15T07:22:15.862Z
---

2026-10-15 만든 「다정쌤 지문 표시판」: https://claude.ai/artifact/8kbfdYKSRM1e3F1PASz3G6 (비공개, db 캡). 선생님이 흐름표를 처음부터 쓰긴 어렵다 → 지문에서 직접 눌러 표시.

- 저장: db 컬렉션 `passages`, 문서 id = 레슨 id. 필드 `marks[{s(문장 id), a, b(띄어쓰기 단위 토큰 위치), kind: key|plus|minus|trap, text, note}]`, `roles{문장id: 메인|뒷받침|예시|전환·반전|덜 중요}`, `memo`(전체 메모).
- 읽기: ArtifactData `list`/`get` collection "passages".
- 레슨을 새로 만들거나 고칠 때 **이 표시를 먼저 읽고** 핵심어 칠하기·+/− 표시·함정 Tip·메인/뒷받침 구조에 그대로 쓴다. 지문 목록은 페이지에 박아 넣은 것이라 새 지문을 넣으면 다시 만들어 올린다(scratchpad annot/index.src.html + passages.json).

[[key-words-definition]] [[evaluation-flip]] [[beginner-basic-per-sentence]]
