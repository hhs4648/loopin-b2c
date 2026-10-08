# CLAUDE.md — Loopin B2C / 다정쌤

이 저장소는 **Loopin 본제품(B2C)** 이다. 기존 앱 **haksup은 다른 라인**이다. haksup UX·카피·채점·튜터 로직을 가져오지 마라.

영어 독해 튜터 앱. 선생님 캐릭터는 **다정쌤**(해요체, 반말 금지).

---

## 기준 (2026-10-05)

**2026년 3월 고3 모의고사 21번이 기준 레슨이다.** 새 문제는 전부 이 레슨처럼 만든다.

- 레슨: `content/tutor/policy-lessons/moeui-2026-03-21-music-researchers.json`
- 대사: `content/tutor/policy-copy/dajung/moeui-2026-03-21-music-researchers.json`
- 규칙: `docs/tutor/policy/AUTHORING_RULES.md` (맨 위 피드백부터)

예전 해석 엔진·예전 지문 50개·2025년 3월 21번(데카르트의 나무)은 지웠다.
데카르트는 `archive/2025-03-21-descartes/`와 브랜치 `archive/2025-03-21-descartes`에 보관.
다른 대화에서 만들던 "단위 6개" 작업은 브랜치 `wip/unit-structure`에 보관 (안 쓰기로 함).

## 수업 흐름 (21번 기준)

지문 한눈에 미리보기(문제 · 지문 전체 · 보기) → [분석하러 갈게요] / [바로 풀어 볼게요]
- 분석: 도입(글 내용 암시 → 칠판 풀이법 설명, 매번, 화면 눌러 넘김) → 분석(문장마다 질문 + 칠판 단어 지도·끌어 넣기·찾기) →
  키워드 색칠한 보기(많이 고른 오답은 「같이 볼까요?」) → 다시 볼 주기 → 단어 체크 → 짝 맞추기 → 헷갈린 포인트
- 바로 풀기: 같은 화면에서 보기를 고름. 틀리면 분석으로. 맞히면 [제대로 분석](끝에 보기마다 해설) / [핵심 정리] / [끝내기]

## 지킬 것

- 정답을 학생이 시도하기 전에 말하지 않는다. 틀리면 첫마디는 "아쉽게도 틀렸어요."
- 한 화면에 선생님 말은 **세 문장까지**, 물음표는 하나
- 모든 화면은 "이 문제를 맞히는 데 필요한 영어"를 가르치거나, 아니면 뺀다. 배경지식 설명 넣지 않기
- **수업 중에는 LLM을 부르지 않는다.** 대사는 brief에서 다정쌤 말투로 미리 뽑아 JSON에 둔다
  (`npm run policy:copy check|prompt|stamp`, 말투 규칙 `content/tutor/policy-copy/dajung/VOICE.md`)
- 버튼으로만 답하는 수업이라 입력창은 없다
- 표시: 흐림 = 빼도 되는 삽입, 음영 = 건너뛰어도 되는 문장, ❓ = 개념 칩, 💡 = 요령 Tip (둘 다 문장 아래 칩, 누르면 참고 설명)

## 코드

- 세션: `src/tutor/policy/session.ts` · 정책: `decide.ts` · 화면 모양: `src/tutor/view.ts`
- 화면: `src/components/` (ClassroomChat, SentenceStudy, ReadPassage, PassagePager, StudyPanel, WordCheck, MatchGame)
- 수업 목록: `content/tutor/sets.json` — 지문을 추가하면 세트에도 넣어야 목록에 뜬다
- 레슨 등록: `src/tutor/policy/lessons.ts` (레슨 한 줄 + 대사 한 줄)
- 30번처럼 스크립트로 만든 레슨은 `scripts/lessons/`의 생성기를 고치고 다시 돌린다 (JSON을 직접 고치지 않는다)
- 오답률: `content/tutor/exam-stats/모의고사_오답률.xlsx`
- 공유용 한 장 HTML: `node scripts/build_share.mjs <lesson-id> share/<이름>.html`

실행: `npm install` → `npm run dev`. 개발 중엔 `?lesson=<id>`로 바로 연다.
확인: `npm run build` (타입검사 → 테스트 → 빌드). 테스트가 지문 규칙(물음표, 세 문장, 보기 수, 강조 구절)을 모든 레슨에 돌린다.

커밋은 인간이 요청하기 전에 하지 마라.
