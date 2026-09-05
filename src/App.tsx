import { useEffect, useMemo, useState } from "react";
import { ClassroomChat } from "./components/ClassroomChat";
import { SentenceStudy } from "./components/SentenceStudy";
import { createSession, type TutorView } from "./tutor/engine";

/*
  지문은 데이터다. 개발에서는 `?lesson=<id>`로 갈아끼워 본다
  (`src/tutor/lessons.ts`). 값이 없거나 못 찾으면 첫 레슨.
*/
const session = createSession(
  import.meta.env.DEV
    ? new URLSearchParams(window.location.search).get("lesson")
    : null,
);

export function App() {
  const [view, setView] = useState<TutorView>(() => session.view());
  const [chatOverride, setChatOverride] = useState(false);
  const [typing, setTyping] = useState(false);
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const id = window.setInterval(() => setSeconds((n) => n + 1), 1000);
    return () => window.clearInterval(id);
  }, []);

  const elapsed = useMemo(() => {
    const m = String(Math.floor(seconds / 60)).padStart(2, "0");
    const s = String(seconds % 60).padStart(2, "0");
    return `${m}:${s}`;
  }, [seconds]);

  /*
    한 턴이 **비동기**가 됐다. D(예상 밖)·B(부분 정답)에서 LLM을 부를 수 있어서다.
    어댑터가 없으면 즉시 끝나므로 체감은 지금과 같다. 실패해도 타이핑 표시가
    남지 않도록 `finally`에서 반드시 푼다.
  */
  function send(text: string) {
    if (typing) return;
    setTyping(true);
    window.setTimeout(() => {
      void session
        .submit(text)
        .then((next) => {
          setView(next);
          setChatOverride(false);
        })
        .catch((error: unknown) => {
          console.error("[tutor] 턴 처리 실패", error);
        })
        .finally(() => setTyping(false));
    }, 700);
  }

  function closeOrReset() {
    setView(session.reset());
    setChatOverride(false);
    setSeconds(0);
  }

  const screen = chatOverride ? "chat" : view.screen;

  return (
    <div className="viewport">
      <div className="phone">
        {screen === "study" ? (
          <SentenceStudy
            view={view}
            typing={typing}
            onSend={send}
            onBack={() => setChatOverride(true)}
            onClose={closeOrReset}
          />
        ) : (
          <ClassroomChat
            view={view}
            elapsed={elapsed}
            typing={typing}
            onSend={send}
            onClose={closeOrReset}
          />
        )}
        {view.recordLine ? <pre className="record">{view.recordLine}</pre> : null}
      </div>
    </div>
  );
}
