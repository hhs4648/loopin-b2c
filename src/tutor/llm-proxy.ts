import type { JudgeInput, SpeakInput, TutorLlm } from "./llm";
import { learnerToken, recordLlmCall, supabaseConfig } from "./records";

/**
 * 프록시 어댑터 — **배포에 쓰는 길.**
 *
 * 브라우저는 "무슨 액션을, 어느 문장에서, 학생이 뭐라고 했는지"만 보낸다.
 * 시스템 프롬프트도 API 키도 서버(`supabase/functions/dajung-llm`)에 있다.
 *
 * 개발용 직접 호출(`llm-claude.ts`)과 **같은 조립기**를 쓰므로 말투가 갈리지
 * 않는다 — 서버가 `content/tutor/prompt.ts`를 그대로 import 한다.
 */

type ProxyReply = {
  text: string | null;
  usage: {
    ms: number;
    inputTokens: number;
    cachedTokens: number;
    outputTokens: number;
  } | null;
  error?: string;
};

async function callProxy(
  kind: "judge" | "speak",
  body: Record<string, unknown>,
): Promise<ProxyReply | null> {
  const config = supabaseConfig();
  const token = await learnerToken();
  if (!config || !token) return null;

  const res = await fetch(`${config.url}/functions/v1/dajung-llm`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      apikey: config.anonKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ kind, ...body }),
  });
  if (!res.ok) {
    console.warn("[tutor] 프록시 응답", res.status, await res.text().catch(() => ""));
    return null;
  }
  const reply = (await res.json()) as ProxyReply;
  if (reply.usage) {
    console.info(
      `[tutor] ${kind} ${reply.usage.ms}ms · 입력 ${reply.usage.inputTokens}(캐시 ${reply.usage.cachedTokens}) · 출력 ${reply.usage.outputTokens}`,
    );
    void recordLlmCall({ call: kind, ...reply.usage });
  }
  return reply;
}

export function createProxyTutorLlm(): TutorLlm {
  return {
    async judge({ studentText, unit }: JudgeInput) {
      const reply = await callProxy("judge", { unit, studentText });
      if (!reply?.text) return null;
      const ids = (reply.text.match(/\d+/g) ?? []).map(Number);
      return { checkedPoints: [...new Set(ids)] };
    },

    async speak({ action, studentText, unit, state, askedWord }: SpeakInput) {
      const reply = await callProxy("speak", {
        action,
        unit,
        studentText,
        askedWord,
        state: { lastTutorUtterance: state.lastTutorUtterance },
      });
      return reply?.text ? { message: reply.text } : null;
    },
  };
}
