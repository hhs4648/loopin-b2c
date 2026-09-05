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
  if (mode === "normal" || mode === "leak" || mode === "bad") {
    void import("./tutor/llm-fake").then(({ createFakeTutorLlm }) => {
      setTutorLlm(createFakeTutorLlm(mode));
      console.info(`[tutor] 가짜 LLM 어댑터 연결: ${mode}`);
    });
  }
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
