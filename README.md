# Loopin B2C

Loopin의 **실제 B2C 제품** 저장소입니다.

기존 haksup 앱들과 혼동하지 마세요. haksup은 학습/학원 쪽 기존 앱이고, **이 저장소가 Loopin 본제품**입니다.

현재 단계는 **다정쌤 튜터 규격 + 퇴사 편지 7문장 데모**입니다. 화면은 상냥쌤 HTML 프로토타입과 같은 형식입니다. 예상 밖 답변은 지금은 힌트 사다리로 두고, 나중에 LLM을 붙입니다.

Claude Code에 맡길 때: 루트 `CLAUDE.md` + [`docs/tutor/HANDOFF_CLAUDE_CODE.md`](docs/tutor/HANDOFF_CLAUDE_CODE.md).

## 지금 있는 것

| 경로 | 역할 |
|------|------|
| `docs/tutor/` | 사람이 읽는 튜터 설계·구현 가이드 |
| `content/tutor/` | LLM에 넣을 프롬프트, 레슨 JSON, 스키마 |
| `.cursor/rules/` | 이 저장소에서 작업하는 AI가 항상 따르는 규칙 |
| `AGENTS.md` | 코딩 에이전트용 빠른 진입점 |

시작점은 [`docs/tutor/README.md`](docs/tutor/README.md)입니다.

데모 실행:

```bash
npm install
npm run dev
```

퇴사 편지 첫 문장 데모: 예상 행동 1·2·3은 스크립트, 그 외 입력은 `잘 모르겠어요`와 같은 힌트 사다리입니다.
