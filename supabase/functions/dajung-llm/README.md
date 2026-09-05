# dajung-llm — LLM 프록시

**키를 브라우저에서 빼는 것**이 목적이다. 학생 앱은 "무슨 액션을, 어느 문장에서,
학생이 뭐라고 했는지"만 보내고, 시스템 프롬프트와 API 키는 여기에만 있다.

프롬프트는 `content/tutor/prompt.ts`를 **그대로 import** 한다. 브라우저 어댑터와
같은 조립기라 개발에서 본 말투와 배포된 말투가 갈리지 않는다.

## 배포

```bash
npx supabase login                      # 브라우저가 열린다
npx supabase link --project-ref <ref>   # 대시보드 주소의 ref
npx supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
npx supabase functions deploy dajung-llm
```

`SUPABASE_URL` · `SUPABASE_ANON_KEY` · `SUPABASE_SERVICE_ROLE_KEY`는 함수 실행 시
**자동으로 주입**된다. 따로 넣지 않는다.

## 지키는 것

- **로그인한 학습자만** — 익명 세션도 포함이지만, anon 키만으로는 못 부른다
- **1분에 20회** — `llm_calls`를 세서 막는다. 크레딧을 지키는 가장 단순한 장치
- **프롬프트는 서버가 만든다** — 앱이 보낸 문자열을 그대로 모델에 넘기면 우리
  크레딧으로 아무 말이나 시킬 수 있는 열린 프록시가 된다
- **모델·max_tokens 고정** — 앱이 바꿀 수 없다

## 함수가 없을 때

호출이 실패하면 엔진은 코드 유도로 폴백한다. 수업은 그대로 돈다 — 모델이 하던
D·B·단어 뜻만 코드가 대신할 뿐이다.

## 배포 상태 (2026-09-06)

- 함수: `dajung-llm` — `verify_jwt = false` (프리플라이트 때문. 자체 검사가 더 엄격)
- 앱: https://loopin-b2c.vercel.app
- 앱 환경변수는 `VITE_SUPABASE_URL` · `VITE_SUPABASE_ANON_KEY` **둘뿐이다.**
  Anthropic 키는 앱에 들어가지 않는다.
