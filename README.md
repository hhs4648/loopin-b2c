# Loopin B2C

**Loopin** 본제품(B2C) 저장소입니다. 기존 haksup 앱들과는 다른 라인입니다.

수능·모의고사 영어 **독해 튜터** 앱입니다. 오답률 높은 3점 문제를 한 문제씩, 선생님 캐릭터 **다정쌤**(해요체)이
유형별 푸는 법으로 가르칩니다. 다정쌤은 캐릭터 이름이고, 앱·제품 이름은 Loopin입니다.
버튼으로 답하는 수업이고, 짧고 중요한 문장만 직접 해석해 봅니다.
**수업 중에는 LLM을 부르지 않습니다** — 대사는 만들 때 미리 뽑아 JSON에 둡니다.

## 먼저 읽을 것

| 무엇 | 어디 |
|------|------|
| 프로젝트 규칙 (가장 먼저) | [`CLAUDE.md`](CLAUDE.md) |
| 지문 만들기 규칙 — 맨 위 날짜별 피드백부터 | [`docs/tutor/policy/AUTHORING_RULES.md`](docs/tutor/policy/AUTHORING_RULES.md) |
| 유형별 수업 틀 (공통 틀 + 빈칸·순서 …) | [`docs/tutor/templates/README.md`](docs/tutor/templates/README.md) |
| 레슨 데이터와 대사의 관계 | [`docs/tutor/policy/README.md`](docs/tutor/policy/README.md) |
| 다정쌤 말투 | [`content/tutor/policy-copy/dajung/VOICE.md`](content/tutor/policy-copy/dajung/VOICE.md) |
| 틀 작업 넘겨받기 | [`handoff/틀-만들기.md`](handoff/틀-만들기.md) |

[`Loopin_Teaching_Policy_Spec_v0.1.md`](docs/tutor/policy/Loopin_Teaching_Policy_Spec_v0.1.md)는 엔진의 처음 설계입니다.
생각의 바탕으로만 읽고, 예시와 규칙은 위 문서들이 이깁니다.

## 실행

```bash
npm install
npm run dev            # 개발 중엔 ?lesson=<레슨 id> 로 바로 연다
npm run build          # 타입검사 → 테스트(모든 레슨에 지문 규칙) → 빌드
```

## 레슨 만들기·고치기

| 할 일 | 명령 |
|------|------|
| 생성기로 레슨 하나 만들기 | `python3 scripts/lessons/gen_<id>.py` → `npm run policy:copy stamp <id>` |
| 규칙을 바꾼 뒤 레슨 전부 다시 만들기 | `npm run lessons:regen` → `npm run build` |
| 낡은 대사 찾기 / LLM 지시문 / 도장 | `npm run policy:copy check \| prompt \| stamp` |
| 공유용 한 장 HTML (앱 전체) | `node scripts/build_share.mjs all <out.html>` |

새 레슨은 `src/tutor/policy/lessons.ts`(레슨·대사 한 줄씩)와 `content/tutor/sets.json`(목록)에 등록합니다.

## 폴더

| 경로 | 역할 |
|------|------|
| `content/tutor/policy-lessons/` | 레슨 (가르칠 내용, 말투 없는 `brief`) |
| `content/tutor/policy-copy/dajung/` | 다정쌤 대사 (생성물, 수업 중엔 이것만 읽는다) |
| `content/tutor/exam-source/` · `exam-stats/` | 문제·해설 원문, 오답률 |
| `scripts/lessons/` | 레슨 생성기, 칠판 정리 장면(`story_boards.py`) |
| `src/tutor/policy/` | 수업 엔진 (`session.ts` 세션, `decide.ts` 정책, `types.ts` 스텝 모양) |
| `src/components/` | 화면 |
| `supabase/` | 학습 기록 서버 (아직 수업 시작·끝만 — 상용화 전 정리 필요) |
| `archive/` | 지운 레슨 보관 (데카르트, 39번 이전 버전 생성기) |
