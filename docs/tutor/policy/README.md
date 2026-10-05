# Teaching Policy 레슨

명세: [`Loopin_Teaching_Policy_Spec_v0.1.md`](./Loopin_Teaching_Policy_Spec_v0.1.md)
**지문 만들 때 지키는 규칙: [`AUTHORING_RULES.md`](./AUTHORING_RULES.md)** — 21번으로 정한 것. 새 지문은 전부 이대로.

예전 수업은 **문장을 해석해서 적게 하고 체크리스트로 채점**한다 (`src/tutor/engine.ts`).
Teaching Policy 수업은 **무엇을·언제·어느 깊이로 가르칠지를 정책이 고르고**, 문장마다
다른 상호작용을 쓴다. 화면(교실·문장 학습)과 다정쌤 말투는 그대로다.

예전 레슨은 건드리지 않았다. 두 엔진이 나란히 돌고, **어느 쪽이 돌지는 레슨이 정한다**
(`App.tsx` — `isPolicyLesson(id)`).

## 가르치는 내용과 말투는 다른 파일이다

```
content/tutor/policy-lessons/<id>.json       가르치는 내용. 말투 없는 메모(`brief`)   ← 사람이 고친다
        │  node scripts/policy_copy.mjs prompt   → LLM이 다정쌤 말투로 옮긴다 (만들 때 한 번)
        ▼
content/tutor/policy-copy/dajung/<id>.json   대사. 생성물                              ← 수업 중엔 이것만 읽는다
```

**LLM은 대사를 만들 때만 쓴다.** 학생이 수업을 듣는 동안에는 모델을 한 번도 부르지 않는다 —
비용은 지문당 한 번이고 학생 수와 무관하다. 말투 규칙은 `policy-copy/dajung/VOICE.md`.

대사는 **통째로 다시 뽑지 않는다.** 대사마다 「어느 brief에서 뽑았는지」 도장(`from`)이 찍혀
있고, brief를 고친 자리만 낡은 것으로 잡힌다. 검수한 문장이 다음 빌드에서 바뀌지 않게 하려는 것이다.

```bash
npm run policy:copy check     # brief는 바뀌었는데 대사는 그대로인 자리
npm run policy:copy prompt    # 그 자리들만 LLM에 맡길 지시문 (VOICE.md + brief)
npm run policy:copy stamp     # 대사를 고친 뒤 도장
```

`npm test`도 낡은 대사를 잡는다. 캐릭터를 하나 더 만들려면 `policy-copy/<캐릭터>/`에
`VOICE.md`를 쓰고 `CHARACTER=<캐릭터>`로 같은 명령을 돌린다 — 레슨은 그대로다.

보기(`options`)·도움말 칩·버튼 글은 **학생의 말**이라 레슨에 둔다.

고유명사 칩(「Descartes · 사람 이름 · 그대로」)은 이 수업에서 쓰지 않는다 — 굳이 필요 없는
정보다. 이름은 단어 뜻(`glosses`)에 「데카르트」처럼 넣어 누르면 보이게만 한다.

## 한 문제를 작은 단위로 (2026-09-30)

21번부터는 지문 하나를 통째로 하지 않고 **단위**(단어 → 핵심 문장 → … → 실전 풀기)로 쪼갠다.
규칙은 `AUTHORING_RULES.md` §0. 단위 하나가 레슨 JSON 하나다 (`moeui-2025-03-21-u1-words` …).
통째로 된 예전 21번(`…-descartes-tree`)은 목록에서 내렸고 엔진 회귀용으로 남겼다 —
`?lesson=moeui-2025-03-21-descartes-tree`로는 여전히 열린다.

## 어디에 무엇이 있나

| 무엇 | 어디 |
|------|------|
| 정책 — `TeachingAction`을 고르는 순수 함수. **대사 없음** | `src/tutor/policy/decide.ts` |
| 학생 상태 — 아는 것·실수를 따로 센다. 기기에 저장 | `src/tutor/policy/student-state.ts` |
| 세션 — 행동에 맞는 대사를 레슨에서 꺼내 `TutorView`에 싣는다 | `src/tutor/policy/session.ts` |
| 레슨 (문장·스텝·brief·보기·그림) | `content/tutor/policy-lessons/*.json` |
| 뽑아 둔 대사 · 말투 규칙 | `content/tutor/policy-copy/dajung/` |
| 대사 뽑기 도구 | `scripts/policy_copy.mjs` |
| 지문과 상관없는 고정 대사 | `content/tutor/policy-frame.json` |
| 그림(뼈대·대응표·대비) | `src/components/StudyPanel.tsx` |
| 회귀 테스트 | `src/tutor/policy/policy.test.ts` (예전 21번) · `units.test.ts` (단위 수업) |
| 단위 목록 화면 | `src/components/LessonList.tsx` — `sets.json`의 `units` |

## 스텝 세 가지

- `choice` — 뜻 고르기·해석 고르기·대응표 한 칸. 사다리: 혼자 → 가벼운 힌트 → 센 힌트 → 설명.
  `brief.feedback`에 오답 보기 id를 적어 두면 **그 오개념을 겨냥한 말**이 첫 힌트가 된다.
  틀린 보기는 사라지고, 보기가 하나 남으면 묻지 않고 설명한다.
- `think` — 대비·예측·따옴표 질문. **채점하지 않는다.** 힌트 한 번, 그다음 정리.
- `show` — 뼈대, 맥락 의미, 괄호 되돌리기, 다음 문장 다리. 보여 주고 기다린다.

`when`으로 정책이 스텝을 접는다: `unless_stable`(거듭 혼자 맞혀 온 skill이면 설명을 접는다),
`if_struggled`(막혔을 때만 주는 「필요하면」 도움).

**stable 판단은 수업을 시작할 때의 학생 상태로 한다.** 오늘 두 번 맞힌 걸로 오늘 설명을
접지 않는다 — 즉시 수행은 기억이 아니다 (§17).

## 그대로 지키는 것

한 턴에 하나 · 매 턴 학생을 기다린다 · 정답은 시도 전에 말하지 않는다 · 해요체 ·
말풍선은 선생님 위 · 지문 글은 JSON에만. `policy.test.ts`가 레슨 글을 검사한다.

## 지문을 추가할 때

1. `content/tutor/policy-lessons/<id>.json` — brief까지
2. `npm run policy:copy prompt <id>`로 대사를 뽑아 `policy-copy/dajung/<id>.json`에 넣고 `stamp`
3. `src/tutor/policy/lessons.ts`에 레슨 한 줄, 대사 한 줄
4. `content/tutor/sets.json`에 세트 (중분류가 없으면 그것도)

`scripts/build_lesson.py`는 예전 모양 전용이다. 이쪽 JSON은 손으로 쓴다.

## 아직 없는 것

- 복습 배정·지연 확인 (§16) — 실수 횟수는 세고 있지만 복습 세션은 없다
- 학습 이벤트의 서버 전송 — 지금은 기기(`loopin.policy.events.v1`)에만 쌓인다
- `student_level`·`time_budget`을 학생별로 정하는 곳 — 지금은 레슨 JSON의 값을 쓴다
- `policy_copy.mjs`가 API를 직접 부르는 모드 — 지금은 지시문을 찍어 주고, 뽑는 건 Claude Code 세션 등에서 한다
- 수업 중 LLM — 없다. 자유 입력은 보기·모름·단어 질문만 알아듣는다
