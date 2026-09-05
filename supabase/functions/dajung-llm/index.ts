import {
  characterSystem,
  judgeSystem,
  judgeUser,
  speakUser,
  unitBlock,
  type PromptState,
  type PromptUnit,
  type SpokenAction,
} from "../../../content/tutor/prompt.ts";

/**
 * 다정쌤 LLM 프록시.
 *
 * **키를 브라우저에서 뺀다.** 지금까지는 브라우저가 Anthropic을 직접 불러서
 * `sk-ant-` 키가 번들에 실려 있었다 — 개발자 도구를 열면 누구나 가져간다.
 * 이제 학생 앱은 "무슨 액션을, 어느 문장에서" 만 보내고 키는 여기에만 있다.
 *
 * **프롬프트도 여기서 조립한다.** 앱이 보낸 문자열을 그대로 모델에 넘기면
 * 열린 프록시가 된다(우리 크레딧으로 아무 말이나 시킬 수 있다). 앱은 구조화된
 * 값만 보내고, 시스템 프롬프트는 서버가 만든다.
 *
 * 배포:  npx supabase functions deploy dajung-llm
 * 비밀값: npx supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
 */

const MODEL = "claude-opus-5";
const ANTHROPIC_URL = "https://api.anthropic.com/v1/messages";
/** 한 사람이 1분에 부를 수 있는 횟수. 크레딧을 지키는 가장 단순한 장치 */
const RATE_LIMIT_PER_MIN = 20;

type Payload = {
  kind: "judge" | "speak";
  unit: PromptUnit;
  studentText: string;
  action?: SpokenAction;
  state?: PromptState;
  askedWord?: string;
  effort?: "low" | "medium";
};

/*
  `apikey`와 `x-client-info`까지 넣어야 한다. supabase-js와 우리 fetch가 그 헤더를
  같이 보내는데, 허용 목록에 없으면 프리플라이트가 통과해도 브라우저가 본 요청을
  막는다 — 앱에는 `Failed to fetch`만 보이고 이유가 안 보인다 (2026-09-06 재현).
*/
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

/** 이 요청을 보낸 학습자가 누구인지. 익명 세션도 여기서 검증된다 */
async function learnerFrom(req: Request): Promise<string | null> {
  const token = req.headers.get("Authorization")?.replace(/^Bearer\s+/i, "");
  const url = Deno.env.get("SUPABASE_URL");
  const anon = Deno.env.get("SUPABASE_ANON_KEY");
  if (!token || !url || !anon || token === anon) return null;
  const res = await fetch(`${url}/auth/v1/user`, {
    headers: { apikey: anon, Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return null;
  const user = await res.json();
  return typeof user?.id === "string" ? user.id : null;
}

/**
 * 최근 1분 호출 수. `llm_calls`를 그대로 쓴다 — 어차피 기록하고 있으니
 * 제한을 위해 테이블을 하나 더 만들 이유가 없다.
 */
async function tooManyCalls(learnerId: string): Promise<boolean> {
  const url = Deno.env.get("SUPABASE_URL");
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) return false; // 셀 수 없으면 막지 않는다
  const since = new Date(Date.now() - 60_000).toISOString();
  const res = await fetch(
    `${url}/rest/v1/llm_calls?select=id&learner_id=eq.${learnerId}&created_at=gte.${since}`,
    { headers: { apikey: key, Authorization: `Bearer ${key}`, Prefer: "count=exact", Range: "0-0" } },
  );
  const range = res.headers.get("content-range") ?? "";
  const total = Number(range.split("/")[1] ?? "0");
  return total >= RATE_LIMIT_PER_MIN;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "POST만 받는다" }, 405);

  const apiKey = Deno.env.get("ANTHROPIC_API_KEY");
  if (!apiKey) return json({ error: "서버에 키가 설정되지 않았다" }, 500);

  const learnerId = await learnerFrom(req);
  if (!learnerId) return json({ error: "로그인이 필요하다" }, 401);
  if (await tooManyCalls(learnerId)) return json({ error: "잠시 후 다시" }, 429);

  let body: Payload;
  try {
    body = await req.json();
  } catch {
    return json({ error: "잘못된 요청" }, 400);
  }
  if (!body?.unit?.text || typeof body.studentText !== "string") {
    return json({ error: "잘못된 요청" }, 400);
  }

  const judging = body.kind === "judge";
  /*
    시스템은 **서버가 만든다.** 캐시가 먹도록 안 변하는 것(캐릭터·말투)부터
    쌓고, 그 문장을 푸는 동안 같은 블록(체크리스트)을 그다음에 둔다.
  */
  const system = judging
    ? [{ type: "text", text: judgeSystem() }]
    : [
        { type: "text", text: characterSystem(), cache_control: { type: "ephemeral" } },
        { type: "text", text: unitBlock(body.unit), cache_control: { type: "ephemeral" } },
      ];

  const started = Date.now();
  const res = await fetch(ANTHROPIC_URL, {
    method: "POST",
    headers: {
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      /*
        judge는 "1,2" 한 줄이면 되지만 **64로는 부족했다.** Opus 5는 thinking이
        기본으로 켜져 있어서, 상한이 낮으면 생각만 하다 잘리고 text 블록이 빈 채로
        온다 (2026-09-06 프록시에서 재현: output 64 / text null).
      */
      max_tokens: judging ? 256 : 512,
      system,
      output_config: { effort: judging ? "low" : (body.effort ?? "low") },
      messages: [
        {
          role: "user",
          content: judging
            ? judgeUser(body.unit, body.studentText)
            : speakUser(
                body.action ?? "TREAT_UNEXPECTED",
                body.unit,
                body.state ?? {},
                body.studentText,
                body.askedWord,
              ),
        },
      ],
    }),
  });

  if (!res.ok) {
    /*
      본문은 로그로만 남긴다 — 상류 오류 메시지를 그대로 돌려주면 키 설정 같은
      서버 사정이 클라이언트에 새어 나간다. 대신 상태 코드는 준다:
      401은 키 문제, 400은 요청 형태, 429는 한도.
    */
    console.error("anthropic", res.status, await res.text());
    return json({ error: "모델 호출 실패", upstream: res.status }, 502);
  }
  const message = await res.json();

  // 거절은 예외가 아니라 200으로 온다. content를 읽기 전에 본다
  if (message.stop_reason === "refusal") return json({ text: null, usage: null });

  const text = (message.content ?? [])
    .filter((b: { type: string }) => b.type === "text")
    .map((b: { text: string }) => b.text)
    .join("\n")
    .trim();

  return json({
    text: text || null,
    usage: {
      ms: Date.now() - started,
      inputTokens: message.usage?.input_tokens ?? 0,
      cachedTokens: message.usage?.cache_read_input_tokens ?? 0,
      outputTokens: message.usage?.output_tokens ?? 0,
    },
  });
});
