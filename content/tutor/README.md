# content/tutor

다정쌤이 LLM에 실제로 넣는 재료입니다. 사람이 읽는 설명은 `docs/tutor/`에 있습니다.

| 경로 | 역할 |
|------|------|
| `prompts/dajung-system.v0.1.md` | 시스템 프롬프트. `===` 사이를 통째로 사용 |
| `frame.json` | 레슨과 무관한 고정 틀 (말투, 절대 규칙, 힌트, 좌절 방지) |
| `lessons/resignation-letter.json` | 퇴사 편지 7문장 데모. 문장 단위, 예상 1·2·3 |
| `lessons/*.json` | 문장·청크·예상 오류·고정 대사. 문장 교체는 여기만 |
| `ui-shell.json` | 교실 대화 / 문장 학습 화면 토큰. 프로토타입과 동일한 셸 |
| `schema/lesson.schema.json` | 레슨 JSON 검증 |
| `types.ts` | 앱이 나중에 import할 타입 |
