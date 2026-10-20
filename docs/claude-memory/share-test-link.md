---
name: share-test-link
metadata:
  node_type: memory
  type: reference
  originSessionId: e9d225ae-ee3a-4324-ab57-6629bfa1e3f7
  modified: 2026-10-12T08:47:44.484Z
---

테스트 링크는 앱 전체를 `scripts/build_share.mjs all`로 한 장 HTML로 묶어 claude.ai 아티팩트로 올린 것이다.

- **실제 배포(Vercel, 2026-10-20부터 메인)**: https://loopin-b2c.vercel.app — `npx vercel --prod --yes`(프로젝트 .vercel/project.json에 연결됨, Supabase 공개 키는 Vercel production env에 있음). 로그인·클라우드 저장까지 되는 진짜 앱.
- **영어 아티팩트**: https://claude.ai/artifact/GmX5HgA6MH8ksXgwLCRUrk (「다정쌤 테스트 수업」, 영어 대화가 관리). 2026-10-12에 국어를 한 번 넣었지만(버전 49) 영어 대화가 다음에 올리면 영어만 남아도 된다
- 테스트용은 예전 링크 GmX5HgA6…를 계속 쓴다(2026-10-14 새로 만들었던 ELnV3MH9…는 사용자 뜻을 잘못 이해한 것이라 지움). 작업용 파일 scratchpad/site/index.html. 2026-10-17 버전 208에 2024년 3월 Top15 포함해 갱신(사용자: 다른 사람에게 공개돼도 됨)
- **국어**: https://claude.ai/artifact/RSSfXXy48XYdYZWRXzHqsS (「다정쌤 국어 테스트」, 이 국어 라인이 관리). 국어 폴더에서 `npm run share:korean` → `share/korean-test.html`을 같은 URL에 올린다. 국어만 보임 — 과목 드롭다운 없음(`VITE_ONLY_SUBJECT=korean`, 2026-10-13 사용자 요청: 영어는 이 링크로 안 들어가도 됨). 만들 때는 비공개 — 공유는 사용자가 Share 메뉴에서

**Why:** 국어를 자주 고칠 거라 링크 하나로 합치면 매번 영어 브랜치와 합쳐야 해서, 사용자가 2026-10-12 따로 관리하기로 함.
**How to apply:** 국어를 고치면 국어 링크만 다시 올린다. 엔진 공통 부분은 나중에 [[korean-line]] 브랜치와 영어 브랜치를 한 번에 합친다.
- **검수용 (유일, 2026-10-18 새로, 사용자 「검수용 링크 따로 만들어줘」)**: https://claude.ai/artifact/DdR3hJTtdoycBgViVdjhr2 — 파일 scratchpad/review3/review.html, 그날 테스트 링크와 같은 내용(2024년 3월 23개 + 미니) 고정. 사용자가 갱신을 말할 때만 올린다.
- 예전 검수용(CRow8V6N…, McTpPAU3…)은 사용자 요청으로 모두 삭제(2026-10-18). 검수용은 DdR3hJTt… 하나만 쓴다.
- **검수용 학생 기록 (2026-10-18):** 검수용 DdR3hJTt…에 db 권한(lessonlogs·attempts, 주인만 전체 읽기, 학생은 자기 문서만) + user + downloads. 수업 이벤트(보기 고름·찾기·해석 입력·지연시간)는 `lessonlogs/<학생 id>`.sessions[접속].events, 미니 모의고사는 `attempts/<학생 id>`. 코드 src/tutor/lessonLog.ts(세션 logEvents → 2초 모아 저장, 화면 떠날 때 flush). 학생은 claude.ai 로그인 + Contributor 이상이어야 써짐. 분석은 ArtifactData list lessonlogs. 다시 올릴 때 capabilities 생략하면 유지됨.

- **공개 링크(카톡) 학생은 db에 못 씀 (2026-10-18 확인):** 검수용을 공개로 카톡에 보냈더니 lessonlogs가 비어 있음. 대신 목록 화면 「📤 선생님께 기록 보내기」(db 못 쓸 때만 보임) → 브라우저 기록(수업 이벤트 최대 5000 + 미니 결과 + 문제별 분) JSON 복사 → 카톡으로 받음. 받은 JSON을 주면 분석. db로 받으려면 학생을 claude.ai 계정으로 Contributor 초대.
- **검수용 db 끔 (2026-10-18, v8):** 공개 링크 방문자에게 「이 아티팩트의 데이터를 보려면 로그인하세요」가 계속 떠서 capabilities {} 로 지움. 기록은 「📤 선생님께 기록 보내기」 복사로만 받는다. 다시 db를 켜면 그 안내가 다시 뜬다.
