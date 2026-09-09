import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { setTutorLlm } from "./tutor/llm";
import { recordLlmCall, supabaseConfig } from "./tutor/records";
import "./styles.css";

/*
  어떤 어댑터를 꽂을지.

  **프록시가 기본이고 프로덕션에서도 돈다.** 예전에는 이 블록 전체가
  `import.meta.env.DEV` 안에 있어서 배포본에 어댑터가 아예 안 붙었다 — 모델이
  말할 자리에서 코드 유도만 나갔다 (2026-09-06 배포 후 재현).

  개발 전용은 둘뿐이다: 가짜 어댑터(`?fakellm=`)와 브라우저 직접 호출(`?direct`).
  직접 호출은 키가 번들에 실리므로 프로덕션 빌드에서 통째로 빠진다.
*/
/*
  **보이는 높이를 직접 재서 CSS에 넘긴다** (`--app-h`, `styles.css`의 `.viewport`).

  `100dvh`면 될 것 같지만, 카톡 인앱 브라우저처럼 위아래 막대를 **포함해서**
  재는 웹뷰가 있다. 그러면 액자가 보이는 자리보다 커지고, 가운데 정렬이라
  위아래가 똑같이 잘려 나간다 (2026-09-06 카톡에서 실제로 이렇게 잘렸다).

  `window.innerHeight`는 그 웹뷰에서도 **실제로 그릴 수 있는 높이**다.
  `visualViewport.height`를 쓰지 않는 이유는 키보드가 올라오면 같이 줄어들어서
  — 글자 칠 때마다 화면이 통째로 쪼그라든다.
*/
function syncAppHeight() {
  document.documentElement.style.setProperty("--app-h", `${window.innerHeight}px`);
}
syncAppHeight();
window.addEventListener("resize", syncAppHeight);
// 회전 직후에는 아직 옛 높이가 나온다 — 다음 프레임에 한 번 더 잰다
window.addEventListener("orientationchange", () => {
  requestAnimationFrame(syncAppHeight);
});

const params = new URLSearchParams(window.location.search);
const fakeMode = params.get("fakellm");

if (import.meta.env.DEV && (fakeMode === "normal" || fakeMode === "leak" || fakeMode === "bad")) {
  void import("./tutor/llm-fake").then(({ createFakeTutorLlm }) => {
    setTutorLlm(createFakeTutorLlm(fakeMode));
    console.info(`[tutor] 가짜 LLM 어댑터 연결: ${fakeMode}`);
  });
} else if (
  import.meta.env.DEV &&
  params.has("direct") &&
  import.meta.env.VITE_ANTHROPIC_API_KEY?.trim()
) {
  void import("./tutor/llm-claude").then(({ createClaudeTutorLlm }) => {
    setTutorLlm(
      createClaudeTutorLlm({
        apiKey: import.meta.env.VITE_ANTHROPIC_API_KEY!.trim(),
        speakEffort: params.get("effort") === "medium" ? "medium" : "low",
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
  void import("./tutor/llm-proxy").then(({ createProxyTutorLlm }) => {
    setTutorLlm(createProxyTutorLlm());
    console.info("[tutor] 프록시 어댑터 연결됨");
  });
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
