# 다정쌤 튜터 규격

Loopin B2C의 1:1 영어 해석 교정 튜터입니다. 설계 원칙은 하나입니다.

> **틀은 고정** (단계 · 고정 대사 · 처치). **AI는 틀 안에서만 자유** (예상 밖 응답, 자연스러운 연결어, 부분 정답 판정).

나중에 LLM을 붙일 때도 이 원칙을 깨지 않습니다. 레슨 문장을 바꾸려면 시스템 프롬프트가 아니라 **레슨 JSON만** 교체합니다.

## 파일 지도

| 파일 | 누가 쓰나 | 용도 |
|------|-----------|------|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | 전원 | 레이어 · 턴 파이프라인 · LLM 계약 |
| [`HANDOFF_CLAUDE_CODE.md`](HANDOFF_CLAUDE_CODE.md) | Claude Code | 이어 받을 때 첫 지시 |
| [`BEHAVIOR.md`](BEHAVIOR.md) | 구현 · 프롬프트 검수 | 진단 A–E, 힌트 사다리, 좌절 방지 |
| `content/tutor/prompts/dajung-system.v0.1.md` | LLM | `===` 사이 내용을 통째로 시스템 프롬프트로 사용 |
| `content/tutor/frame.json` | 앱 · LLM 조립기 | 캐릭터/절대규칙 등 레슨과 무관한 고정 틀 |
| `content/tutor/schema/lesson.schema.json` | 검증 | 레슨 JSON 계약 |
| `content/tutor/lessons/*.json` | 콘텐츠 | 문장 · 청크 · 예상 오류 · 고정 대사 |
| `content/tutor/types.ts` | 앱 | 레슨 데이터 타입 (세션 상태는 여기 없다 — `engine.ts`) |
| `src/tutor/lessons.ts` | 앱 | 레슨 목록. 지문 추가는 여기 한 줄 |
| `src/tutor/llm.ts` | 앱 | LLM 어댑터 계약 + 가드레일 ([`LLM_ASSEMBLY.md`](LLM_ASSEMBLY.md)) |
| [`TEST_SCENARIOS.md`](TEST_SCENARIOS.md) | QA | 프롬프트 분기 체크리스트 |
| [`LLM_ASSEMBLY.md`](LLM_ASSEMBLY.md) | 나중에 LLM 붙일 때 | 프롬프트 조립 방법 |
| [`UI.md`](UI.md) | 구현하는 AI | 상냥쌤 HTML 프로토타입과 같은 화면 셸 |
| [`UI_OUTPUT.md`](UI_OUTPUT.md) | 앱 연동 시 | `message` / `buttons` / `effect` |
| [`DEMO_RESIGNATION.md`](DEMO_RESIGNATION.md) | 데모 | 퇴사 편지 첫 문장 · 행동 1·2·3 |
| `docs/tutor/refs/` | 참고 | 프로토타입에서 뽑은 slim HTML |

## 버전

- 튜터 프레임: **v0.1** (2026-08-19)
- 말투: 다정쌤 해요체 확정
- 원안 스크립트: 김수정 / 프롬프트화: Claude 초안
