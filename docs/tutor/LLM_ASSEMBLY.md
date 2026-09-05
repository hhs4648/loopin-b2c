# LLM 조립 — 나중에 모델 붙일 때

초기 테스트는 `content/tutor/prompts/dajung-system.v0.1.md`의 `===` 사이 블록을 시스템 프롬프트로 넣고, 사용자를 학생으로 두면 됩니다.

앱에 LLM을 넣을 때는 **프레임과 레슨을 조립**합니다. 문장을 바꿀 때 프레임을 다시 쓰지 않기 위해서입니다.

## 조립 순서

```
[1] frame.json → 캐릭터 / 절대 규칙 / 흐름 / 힌트 / 좌절 방지 / 역질문 / 팁
[2] 현재 레슨 JSON → 【레슨 데이터】 블록으로 직렬화
[3] (나중) UI JSON 출력 규칙
[4] (권장) 현재 SessionState 요약 — 청크 번호, 힌트 단, missCount, pendingBranch
```

`[4]`를 넣지 않으면 모델이 힌트 2단을 건너뛰거나 청크를 혼자 진행합니다. 프로덕션에서는 넣는 쪽을 기본으로 하세요.

## 시스템 vs 유저 메시지

- **system**: 프레임 + 레슨 데이터 + (선택) UI 포맷 + 현재 상태.
- **user**: 학생의 이번 발화만. 가능하면 메타데이터(`chunkId`, `isQuestion`)를 앱이 앞에 붙이지 말고, 학생이 보는 그대로 보냅니다. 진단은 모델/코드가 합니다.
- **assistant**: 다정쌤 한 턴. 2~4문장. 필요 시 `[기록]`은 세션 끝에만.

## 레슨 직렬화 최소 필드

모델이 봐야 하는 것:

- `topic_intro`, `sentence`, `grammar_type`, `split_rule`
- 각 청크의 `text`, `model_translation`, `scoring_points`
- `expected_errors` 전체 (detect, never_mark_correct, script, rounds, priority)
- `scoring_points`의 `nudge`(지금 유도할 것 하나만), `anticipated_responses`, `anticipated_questions`
- `teach_points`, `proper_nouns`

앱 UI만 쓰는 필드(`id`, `authors`)는 프롬프트에서 빼도 됩니다.

## 모델에게 맡기지 말 것 (코드가 강제)

- `hintRung`을 2로 점프
- `missCountInChunk` 리셋 없이 다음 청크
- teach_points 한 번에 출력
- `never_mark_correct` 오류를 A로 채점
- 기록 라인 형식 변경
- 해요체 이외 말투

이 항목은 가드레일로 응답을 거르거나, 도구 호출 없이 상태머신이 다음 액션을 정한 뒤 모델에게 “이 액션만 말로 풀어라”고 시키는 편이 안전합니다.

## 권장 액션 열거 (프로덕션)

상태가 정해지면 모델 입력을 이렇게 줄입니다.

```text
action: TREAT_EXPECTED_ERROR
error_id: E1
script_id: ask_verb_or_participle
do_not_reveal_answer: true
one_question_only: true
```

모델은 `script.message`를 거의 그대로 말하고, 없는 연결만 보완합니다.

테스트 단계에서는 액션 열거 없이 통째 프롬프트로도 충분합니다.

---

## 코드에 난 자리 (2026-09-06)

`src/tutor/llm.ts`가 어댑터 계약이다. **어댑터를 안 꽂으면 엔진은 지금 데모와 똑같이
돈다** — D도 체크리스트 유도로 접힌다. 그래서 이 파일이 들어와도 화면 동작은 안 바뀐다.

```ts
type TutorLlm = {
  judge?: (i: JudgeInput) => Promise<JudgeResult | null>;  // 콜 1: B인지 D인지만
  speak:  (i: SpeakInput) => Promise<SpeakResult | null>;  // 콜 2: 그 액션의 말만
};
setTutorLlm(adapter);   // 앱 진입점에서 한 번
```

**모델이 열리는 문은 셋뿐이다.** D(예상 밖)·B(부분 정답)은
`treatUnexpectedOrPartial()`, 단어 뜻 질문은 `answerWord()`가 부른다.
C(고정 대사)·E(체크리스트 유도)·miss 카운트·다음 unit 이동은 전부 코드에 남아 있다.

`ANSWER_WORD`는 **이번 문장이 가르치지 않는 단어**에만 열린다. 가르치는 단어
(채점 포인트·예상 오류가 겨냥하는 단어)는 뜻이 곧 정답이라 코드가 힌트 사다리로
답한다. 잘못 분류되더라도 가드레일이 정답 문자열을 막는다.

판정을 `"B" | "D"`로만 받는 것이 중요하다. A와 C는 코드가 이미 정했으므로 **모델이
오답을 정답으로 뒤집을 길 자체가 없다** — `never_mark_correct`도 자동으로 지켜진다.

### 모델에게 넘기는 것

현재 unit만 넘긴다(편지 전체 아님). 유도 문구는 **지금 유도해도 되는 항목 하나만**(`nextNudge`)
넘긴다. 다음 항목이나 `tell`까지 보여 주고 "쓰지 마"라고 지시하면 언젠가 쓴다.

### 가드레일 — 모든 발화에 예외 없이

`validateLlmOutput()`을 통과 못 하면 그 발화를 **버리고 코드의 항목 유도로
폴백**한다. 재시도하지 않는다.

| 검사 | 왜 |
|------|-----|
| 금지 문자열 (모범 해석 · 정답 선택지 라벨 · 아직 안 알려 준 항목의 `tell` · **채점 포인트의 정답 쪽**) | 정답 선공개 |
| 버튼 라벨에도 같은 검사 | 정답을 빠른 대답에 띄우는 것도 선공개 |
| 문장 4개 이하 / 물음표 1개 | 한 턴에 하나 |
| 반말 | 해요체 고정 |

**채점 포인트를 금지 목록에 넣은 이유:** 모델에게 `scoring_points`를 주는 건 판정하라고지
읊으라고가 아니다. 안 막으면 모범 해석을 피해 가면서 `serve → 근무하다`를 그대로 흘린다
(2026-09-06 가짜 어댑터로 재현하고 막았다).

### 키 없이 확인하는 법

`npm run dev` 후 쿼리로 가짜 어댑터를 꽂는다 (개발 빌드 전용, `src/tutor/llm-fake.ts`).

| URL | 봐야 하는 것 |
|-----|--------------|
| `?fakellm=normal` | D 처치가 힌트 대신 모델 발화로 나감. 부분 정답이면 다른 대사 |
| `?fakellm=leak` | 정답을 흘리면 **폐기 → 힌트 1단**. 콘솔에 폐기 사유 |
| `?fakellm=bad` | 문장 5개·질문 2개·반말도 같은 폴백 |
| (쿼리 없음) | 지금 데모 그대로 |
