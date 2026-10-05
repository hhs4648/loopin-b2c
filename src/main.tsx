import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import "./styles.css";

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

/* 수업 중에는 모델을 부르지 않는다 — 대사는 미리 뽑아 둔 JSON이다 (예전 LLM 어댑터는 지웠다) */
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
