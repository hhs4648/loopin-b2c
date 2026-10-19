---
name: mini-mock
description: 미니 모의고사 — 쉬운 문항(18~20, 도표·일치·안내문) 빼고 고난도만 20분, 시간 재고 점수화, 레슨 없는 문항도 넣음
metadata:
  type: project
---

요즘 모의고사 공부는 전체를 다 풀면 너무 오래 걸려서 20분짜리 미니 모의고사로 한다 (2026-10-16 선생님).
- 18~20번, 도표 같은 쉬운 문항은 빼고 구성 (영어는 25~28 도표·일치·안내문도 뺌)
- 시간 재기(20분, 0이면 저절로 제출), 끝나면 점수(배점 합)·맞힌 수·걸린 시간·유형별·문항별 + 전국 오답률
- 분석 레슨이 없는 문항도 넣는다 — 틀리면 레슨 있는 문항은 「분석하러 가기」, 없으면 해설(출제의도·고친 줄·해석)
- 영어부터: `eng-2026-03-mini1` (21·24·29·30·31·33·34·36·38·39, 26점), 생성기 `scripts/mini/gen_eng_2026_03_mini1.py`, 원문 `content/tutor/exam-source/2026-03-고3`
- 2회: `eng-2024-suneung-mini` 2024학년도 수능 (21·29·30·31·33·34·36·37·38·39·41·42, 30점, 레슨 없음 → EBSi [풀이]를 intent에), 생성기 `scripts/mini/gen_eng_2024_suneung_mini.py`, 원문 `content/tutor/exam-source/2024-수능` (2026-10-17)
- 미니 코드는 **korean/2025-03-10 브랜치(폴더 loopin-b2c-korean)에만** 있다 — lesson/2026-03-30엔 없음
- 학생 지표용 단독 링크(2024 수능 미니만): https://claude.ai/artifact/9uJ88rQ7rLS1LoLjjYiaq6 (`npm run share:mini24`, VITE_ONLY_MINI) — 이름 받고 db `attempts/<학생id>`에 풀이마다 문항별 시간·고른 차례·해설 열람 기록, 주인만 「선생님 · 학생 결과 보기」·CSV. 학생은 Contributor 이상이어야 기록됨(조직 밖은 view라 못 씀)
- 테스트 링크: https://claude.ai/artifact/LUBbZFtrZ9FswpGHdZKvo5 (`npm run share:mini`, 영어만) — 국어 링크에는 안 보임

- **영어 라인(이 폴더, lesson/2026-03-30)에도 옮김 (2026-10-18):** `eng-2024-03-full` 2024년 3월 고3 21~45번 시험지 순서(25~28 뺌, 21·45는 선생님 요청으로 넣음, 21문항 49점 45분), 생성기 `scripts/mini/gen_eng_2024_03_full.py`. 추가 기능: 푸는 중 문항마다 「정답 확인」, 21문항 모두(2026-10-18) 「다정쌤과 분석하기」(분석 동안 시계 멈춤, 돌아오면 이어 풀기), 기록에 checked·analyzed·paused_seconds, 기록 못 하는 학생은 「결과 복사」. 학생용 단독 링크 https://claude.ai/artifact/R1QpqZ1xtxKPo5aR4rx3RY (`npm run share:mini2403`, db rules attempts owner / attempts/{self} interact)

**How to apply:** 국어 미니 모의고사도 같은 틀(독서 2지문 등). 새 회차는 생성기를 하나 더 두고 `src/tutor/mini.ts`의 MOCKS에 등록. [[korean-line]] [[naesin-packs]]
- **2026-10-18 추가 (사용자 요청):** ⏸ 일시정지(시계 멈춤 + 문제 가림, 기록 `breaks`, paused_seconds에 더함) · 답 안 고른 문항에 「답 고르지 않고 다정쌤 분석 보기」 → 돌아와서 답 고를 수 있음(사용자가 0점 처리 대신 이걸 택함), 번호에 「분석」 배지·결과에 「분석 보고 고름」 태그·「분석 안 보고 맞힌 점수」 따로, 기록 `peeked`.
- **지문 표시 (2026-10-18 사용자 요청):** 두 번 두드리기 = 모르는 단어(보라 물결 밑줄, 뜻은 그 문항 분석 레슨 glosses에서 `src/tutor/miniWords.ts`, 뜻 있으면 단어장에도), 길게 누르기(터치)·끌기(마우스) = 형광펜(칠한 곳에서 시작하면 지우개), 한 번 두드리기는 아무것도 안 함. 정답 확인·결과 화면에 모르는 단어 목록, 기록 items[no].hi/unknown, CSV 칸. 코드 `src/components/MiniMarks.tsx`.

- **선지 해석 (2026-10-18 선생님 요청):** 「해석 보기 (지문 · 선지)」 안에 ①~⑤ 선지 해석, 정답은 굵게. 출처는 분석 레슨 exam.options[].ko (생성기가 LESSON_FILE로 읽음). 영어 선지만 — 21·23·24·31~34·40·41·42번. 29·30번(밑줄 낱말)은 레슨 보기에 ko가 없어 아직 없음.
