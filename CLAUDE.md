# CLAUDE.md — Loopin B2C / 다정쌤

이 저장소는 **Loopin 본제품(B2C)** 이다. 기존 앱 **haksup은 다른 라인**이다. haksup UX·카피·채점·튜터 로직을 가져오지 마라.

너는 다정쌤 영어 해석 튜터를 이어서 만든다. 챗봇을 새로 설계하지 마라. 이미 있는 **상태머신 + 레슨 JSON + UI 셸** 위에만 작업한다.

---

## 시작 전 읽을 순서 (이 순서 그대로)

1. `docs/tutor/ARCHITECTURE.md` — 레이어, 턴 파이프라인, LLM 계약
2. `docs/tutor/HANDOFF_CLAUDE_CODE.md` — 지금 할 일 / 하지 말 일
3. `docs/tutor/BEHAVIOR.md` — 진단 A–E, 힌트, 좌절 방지
4. `docs/tutor/UI.md` — 교실 대화 + 문장 학습 화면
5. `content/tutor/frame.json` + `content/tutor/lessons/resignation-letter.json`
6. `src/tutor/engine.ts` — 현재 데모 엔진

실행: `npm install` → `npm run dev` → http://127.0.0.1:5173/

확인: `npm test` (엔진·레슨 글·가드레일 회귀). `npm run build`가 타입검사 → 테스트 →
빌드 순서로 돌므로, 빌드가 통과하면 회귀도 통과한 것이다.
개발 중에는 `?lesson=<id>`로 지문을, `?fakellm=normal|leak|bad`로 가짜 모델을 꽂을 수 있다.

---

## 절대 깨지 말 것

틀은 고정. 모델은 틀 안에서만 자유.

- 정답을 학생이 시도하기 전에 말하지 않는다. 모범 해석 전체는 좌절 방지에서만 나온다.
- 한 턴에 질문·교정·설명 **하나**.
- 매 턴 학생을 기다린다. 혼자 다음 문장으로 가지 않는다.
- 유도는 체크리스트에서 **못 한 것 중 첫 번째 하나만**. 같은 항목에서 또 막히면 그 항목만 알려 준다(`tell`). 한 턴에 둘을 짚지 않는다.
- 한 unit에서 실패+모름 합산 3회 후 4번째부터는 설명제공 (시도 강요 금지).
- 고유명사(Lewis Ltd. 등)는 **미리 제시**, 해석 과제가 아니다. 그대로 두면 된다.
- 짧은 문장은 끊지 않는다. unit 기본값은 문장 하나.
- 말풍선은 선생님 **위**. 메신저형 긴 채팅 로그를 만들지 않는다. 선생님 현재 한 줄, 학생 마지막 한 줄.
- 캐릭터 이름은 **다정쌤**. 해요체. 반말 금지.
- 레슨 문장을 시스템 프롬프트에 하드코딩하지 않는다. 지문 교체는 `content/tutor/lessons/*.json`만.

---

## 역할 분리 (구현할 때)

| 누가 | 무엇을 |
|------|--------|
| 엔진 `src/tutor/engine.ts` | stage, unitIndex, hintRung, missCount, pending, 화면 전환, `[기록]` |
| 레슨 JSON | 문장, 모범 해석, P2/P3 고정 대사, 힌트 문구, 고유명사 |
| LLM (아직 없음) | **D 예상 밖** 대응, B 부분 정답 판정, 가르치지 않는 단어의 뜻, 연결어. 단계는 고르지 않음 |
| UI | `message` / `buttons` / `effect` 렌더, 고유명사 칩 |

지금 데모: A/C는 키워드, D는 E(힌트)로 폴백. LLM을 붙일 때는 **D만** 열고 C·E·카운터는 코드에 남겨라.

LLM 출력 계약:

```json
{ "message": "2~4문장", "buttons": ["잘 모르겠어요"], "effect": null }
```

`effect: "light"`는 학생이 오류를 **스스로** 고친 턴만.

---

## 코드 위치

- 엔진: `src/tutor/engine.ts`, `match.ts`, `lessons.ts`, `llm.ts`
- **지문을 고칠 때는 `scripts/specs/*.json`을 고치고 `npm run lessons`.**
  `content/tutor/lessons/*.json`은 생성물이라 손으로 고치면 덮어써진다 (`scripts/specs/README.md`)
- 수업 목록(메인 화면): `content/tutor/sets.json` + `src/tutor/sets.ts` + `src/components/LessonList.tsx`.
  **세트가 학생이 고르는 단위**다 — 지문을 추가하면 세트에도 넣어야 목록에 뜬다 (`sets.test.ts`가 검사한다)
- 매칭 키워드·칭찬 문구는 **레슨 JSON 안**에 있다 (`demo_match.p1`, `praise`). 예전 `units.ts`는 없어졌다
- UI: `src/components/ClassroomChat.tsx`, `SentenceStudy.tsx`
- 퇴사 편지 7문장 레슨: `content/tutor/lessons/resignation-letter.json`
- 탈레스 원안 레슨(참고): `content/tutor/lessons/thales-participial-phrase-front.json`
- 시스템 프롬프트 원안: `content/tutor/prompts/dajung-system.v0.2.md`

## Teaching Policy 레슨 (앞으로의 공식 policy)

**방향 (2026-09-22 결정).** 새 Teaching Policy가 공식이다. 2025년 3월 모의고사부터 지문을
하나씩 만들며 고쳐 나간다. 예전 해석 엔진과 예전 레슨은 **지금은 그대로 두고 나중에 폐기**
한다 — 거기에 새 작업을 하지 마라. 말투와 가르치는 로직은 계속 분리하고, LLM은 꼭 필요한
곳에만 쓴다(비용). 웬만하면 코드로 한다. UX/UI는 현재 것을 유지한다.

2025년 3월 모의고사 21번부터는 **다른 엔진**이 돈다 — 해석을 적게 하는 대신, 정책이
문장마다 상호작용(뜻 고르기·대응표·대비·예측)을 고른다. 화면과 말투는 그대로.
읽을 것: `docs/tutor/policy/README.md` → 명세 `Loopin_Teaching_Policy_Spec_v0.1.md` →
**`docs/tutor/policy/AUTHORING_RULES.md`** (지문 만드는 규칙. 21번으로 정했고 새 지문은 전부 이대로).

- 코드: `src/tutor/policy/` (`decide.ts` 정책 · `session.ts` 세션 · `student-state.ts`)
- 레슨: `content/tutor/policy-lessons/*.json` — **가르치는 내용만**, 말투 없는 `brief`로 쓴다 (`npm run lessons`와 무관)
- 대사: `content/tutor/policy-copy/dajung/*.json` — brief에서 다정쌤 말투로 **미리 뽑은 생성물**.
  LLM은 이때만 쓴다. **수업 중에는 모델을 부르지 않는다.** brief를 고치면
  `npm run policy:copy check|prompt|stamp` (말투 규칙은 같은 폴더 `VOICE.md`)
- **예전 레슨과 `engine.ts`는 그대로 둔다.** 위 「절대 깨지 말 것」 중 말풍선·해요체·
  한 턴에 하나·학생을 기다린다·정답 선공개 금지는 이쪽에도 그대로 적용된다

커밋은 인간이 요청하기 전에 하지 마라.
