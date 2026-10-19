---
name: naesin-packs
description: "내신 대비 묶음 — 학교 프린트엔 출처 없이 지문만 있어서 한 문장(일부)으로 찾아 담는다, 요청 기능은 안 함"
metadata:
  node_type: memory
  type: project
  originSessionId: e9d225ae-ee3a-4324-ab57-6629bfa1e3f7
  modified: 2026-10-16T04:25:40.987Z
---

내신은 여러 모의고사에서 지문을 한두 개씩 뽑아 낸다. 학교는 연도·번호 없이 **지문만** 준다 (2026-10-16 사용자).
그래서 「📚 내신 대비」 묶음을 만들었다 (국어 브랜치, 커밋 2026-10-16).

- 찾기는 출처가 아니라 **지문 속 한 문장이나 그 일부** — 글자 3개 조각 겹침(띄어쓰기·문장부호·오타 무시), 모델 안 씀. 비슷한 지문이 여럿이면 다 보여 주고 학생이 고른다
- 지문 전체를 붙여 넣을 필요 없다 (사용자: 한 문장이면 충분)
- 없는 지문 **요청 기능은 만들지 않는다** (사용자: 필요 없음)
- 묶음은 브라우저에 저장(`loopin.packs.v1`), 세트 id만 든다. 수업·완료 기록은 원래 세트 그대로
- 코드: `src/tutor/passage-search.ts`, `src/tutor/packs.ts`, `src/components/PackBook.tsx`

**How to apply:** 다음 후보는 묶음 공유 링크(한 반이 같은 범위). 앱에 지문이 늘수록 쓸모가 커지니 지문 추가할 때 검색에 걸리는지(passage 텍스트) 확인. [[korean-line]]
