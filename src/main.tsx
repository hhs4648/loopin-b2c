import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { setTutorLlm } from "./tutor/llm";
import { recordLlmCall, supabaseConfig } from "./tutor/records";
import "./styles.css";

/*
  **개발에서만** 가짜 LLM을 꽂는다 — `?fakellm=normal|leak|bad`.
  아무것도 안 꽂으면 엔진은 코드만으로 돌고, 화면 동작은 지금 데모 그대로다.
  배포 빌드에서는 `import.meta.env.DEV`가 false라 이 블록이 통째로 빠진다.
*/
if (import.meta.env.DEV) {
  const mode = new URLSearchParams(window.location.search).get("fakellm");
  const apiKey = import.meta.env.VITE_ANTHROPIC_API_KEY?.trim();

  if (mode === "normal" || mode === "leak" || mode === "bad") {
    void import("./tutor/llm-fake").then(({ createFakeTutorLlm }) => {
      setTutorLlm(createFakeTutorLlm(mode));
      console.info(`[tutor] 가짜 LLM 어댑터 연결: ${mode}`);
    });
  } else if (apiKey && new URLSearchParams(window.location.search).has("direct")) {
    /*
      **개발 전용 직접 호출.** 브라우저가 Anthropic을 직접 부른다 — 키가 번들에
      실린다. 프록시를 배포하기 전이나, 프록시 없이 프롬프트만 빨리 고쳐 볼 때
      `?direct` 를 붙여서 쓴다. 평소에는 아래 프록시 경로를 탄다.
    */
    void import("./tutor/llm-claude").then(({ createClaudeTutorLlm }) => {
      setTutorLlm(
        createClaudeTutorLlm({
          apiKey,
          // 기본은 low. ?effort=medium 으로 올려서 비교해 볼 수 있다
          speakEffort:
            new URLSearchParams(window.location.search).get("effort") === "medium"
              ? "medium"
              : "low",
          onUsage: (u) => {
            console.info(
              `[tutor] ${u.call} ${u.ms}ms · 입력 ${u.inputTokens}(캐시 ${u.cachedTokens}) · 출력 ${u.outputTokens}`,
            );
            void recordLlmCall({
              call: u.call,
              ms: u.ms,
              inputTokens: u.inputTokens,
              cachedTokens: u.cachedTokens,
              outputTokens: u.outputTokens,
            });
          },
        }),
      );
      console.info("[tutor] Claude 직접 호출 (개발 전용 — 키가 번들에 실린다)");
    });
  } else if (supabaseConfig()) {
    /*
      **평소 경로.** 키는 서버에만 있다. 브라우저는 액션과 문장만 보낸다.
      함수가 아직 배포 전이면 호출이 실패하고, 엔진은 코드 유도로 폴백한다 —
      수업은 그대로 돈다.
    */
    void import("./tutor/llm-proxy").then(({ createProxyTutorLlm }) => {
      setTutorLlm(createProxyTutorLlm());
      console.info("[tutor] 프록시 어댑터 연결됨");
    });
  }
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
