import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { setTutorLlm } from "./tutor/llm";
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
  } else if (apiKey) {
    /*
      **개발 전용.** 브라우저가 Anthropic API를 직접 부른다 — 키가 번들에 실린다.
      배포 전에는 프록시 서버로 옮긴다. 키가 없으면 지금처럼 코드만으로 돈다.
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
          onUsage: (u) =>
            console.info(
              `[tutor] ${u.call} ${u.ms}ms · 입력 ${u.inputTokens}(캐시 ${u.cachedTokens}) · 출력 ${u.outputTokens}`,
            ),
        }),
      );
      console.info("[tutor] Claude 어댑터 연결됨 (개발 전용)");
    });
  }
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
