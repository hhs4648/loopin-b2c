# 배포 메모

## Vercel

```bash
npx vercel --prod
```

환경변수는 `VITE_SUPABASE_URL` · `VITE_SUPABASE_ANON_KEY` 둘뿐이다.
**Anthropic 키는 앱에 넣지 않는다** — Edge Function의 secret으로만 있다.

### `vercel.json`의 rewrite 정규식을 건드리지 말 것

```json
"source": "/((?!.*\.[a-zA-Z0-9]+$).*)"
```

SPA 라우팅을 위해 모든 경로를 `index.html`로 보내되, **확장자가 붙은 요청은
제외**한다. 이걸 `/(.*)`로 두면 `/assets/dajung-teacher.webp` 같은 정적 파일까지
index.html로 삼킨다. 브라우저는 **200을 받으므로 실패 로그도 안 남기고**, 그림만
조용히 안 보인다 (2026-09-06 실제로 이렇게 캐릭터가 사라졌다).

확인하는 법:

```bash
curl -s https://loopin-b2c.vercel.app/assets/dajung-teacher.webp | head -c 4
# RIFF 가 나와야 한다. <!do 가 나오면 위 규칙이 깨진 것이다
```

Vercel은 `vercel.json`에 `//` 같은 주석 키를 허용하지 않는다. 설명은 이 파일에 쓴다.

## Supabase

- 마이그레이션: SQL Editor에 `supabase/migrations/*.sql`
- 함수: `npm run fn:deploy` (`--no-verify-jwt`로 배포된 상태 — 프리플라이트 때문)
- 시크릿: `ANTHROPIC_API_KEY` 하나
