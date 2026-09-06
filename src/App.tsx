import { useEffect, useMemo, useState } from "react";
import type { LessonCollection, LessonSet } from "../content/tutor/types";
import { ClassroomChat } from "./components/ClassroomChat";
import { LessonList } from "./components/LessonList";
import { SentenceStudy } from "./components/SentenceStudy";
import { createSession, type TutorSession, type TutorView } from "./tutor/engine";
import { loadLearnerName, saveLearnerName } from "./tutor/learner-name";
import { markDone } from "./tutor/progress";
import { finishSessionRecord, startSessionRecord } from "./tutor/records";
import { firstLessonId, getCollection, getSet, setOfLesson } from "./tutor/sets";

/*
  개발에서 지문 하나만 보고 싶을 때가 있다. `?lesson=<id>`나 `?set=<id>`가
  있으면 목록을 건너뛰고 바로 시작한다 (`src/tutor/sets.ts`).
  문장 학습의 단어 뜻은 레슨 JSON `glosses`에서 온다.
*/
const params = new URLSearchParams(window.location.search);
const directLesson = import.meta.env.DEV ? params.get("lesson") : null;
const directSet = import.meta.env.DEV ? getSet(params.get("set")) : null;

type Started = { session: TutorSession; set: LessonSet | null };

/** 수업 하나를 연다. 이름은 아는 사람이면 물어보지 않고 그 이름으로 인사한다 */
function open(lessonId: string | null): Started {
  const session = createSession(
    lessonId,
    import.meta.env.DEV && params.has("newname") ? null : loadLearnerName(),
  );
  return { session, set: setOfLesson(session.lessonId()) };
}

export function App() {
  /*
    **수업은 목록에서 고른 뒤에 만든다.** 예전에는 모듈이 로드될 때 세션을
    하나 만들어 두고 앱을 열자마자 그 지문이 시작됐다. 이제 화면이 둘이라
    (목록 / 수업) 고르기 전에는 세션이 없다.
  */
  const [started, setStarted] = useState<Started | null>(() => {
    if (directLesson) return open(directLesson);
    if (directSet) return open(firstLessonId(directSet));
    return null;
  });
  const [view, setView] = useState<TutorView | null>(
    () => started?.session.view() ?? null,
  );
  /* 목록에서 열어 둔 중분류. null이면 중분류 목록을 본다 */
  const [collection, setCollection] = useState<LessonCollection | null>(() =>
    directSet ? getCollection(directSet.collection) : null,
  );
  const [chatOverride, setChatOverride] = useState(false);
  const [typing, setTyping] = useState(false);
  const [seconds, setSeconds] = useState(0);

  const session = started?.session ?? null;

  // 시계는 수업 중에만 간다. 목록을 보는 시간은 공부한 시간이 아니다
  useEffect(() => {
    if (!session) return;
    const id = window.setInterval(() => setSeconds((n) => n + 1), 1000);
    return () => window.clearInterval(id);
  }, [session]);

  /*
    수업 하나가 기록의 단위다. 시작할 때 행을 하나 열고, 끝날 때 결과와
    항목 기록을 한 번에 채운다. 실패해도 수업은 그대로 진행된다.
  */
  useEffect(() => {
    if (!session) return;
    void startSessionRecord(session.lessonId());
  }, [session]);

  const ended = view?.ended ?? false;
  const recordLine = view?.recordLine ?? null;
  const setId = started?.set?.id;
  useEffect(() => {
    if (!ended || !recordLine || !session) return;
    const result = recordLine.match(/결과=([^\s/]+)/)?.[1];
    if (!result) return;
    void finishSessionRecord(result, session.records());
    // 목록에 「완료」를 칠하려면 지금 손에 있는 값이 필요하다
    if (setId) markDone(setId, result);
  }, [ended, recordLine, session, setId]);

  const elapsed = useMemo(() => {
    const m = String(Math.floor(seconds / 60)).padStart(2, "0");
    const s = String(seconds % 60).padStart(2, "0");
    return `${m}:${s}`;
  }, [seconds]);

  /*
    한 턴이 **비동기**다. D(예상 밖)·B(부분 정답)에서 LLM을 부를 수 있어서다.
    어댑터가 없으면 즉시 끝나므로 체감은 같다. 실패해도 타이핑 표시가 남지
    않도록 `finally`에서 반드시 푼다.
  */
  function send(text: string) {
    if (typing || !session) return;
    setTyping(true);
    window.setTimeout(() => {
      void session
        .submit(text)
        .then((next) => {
          setView(next);
          setChatOverride(false);
          // 인사 턴에서 이름을 받았으면 다음 수업을 위해 남긴다.
          // 못 알아들었을 때(null) 이미 있던 이름을 지우지는 않는다
          const name = session.learnerName();
          if (name) saveLearnerName(name);
        })
        .catch((error: unknown) => {
          console.error("[tutor] 턴 처리 실패", error);
        })
        .finally(() => setTyping(false));
    }, 700);
  }

  function startSet(set: LessonSet) {
    setCollection(getCollection(set.collection));
    const next = open(firstLessonId(set));
    setStarted(next);
    setView(next.session.view());
    setChatOverride(false);
    setSeconds(0);
  }

  /**
   * 「학습 종료」와 「다시 시작」이 같은 자리로 간다 — **그 문제가 있던 목록**.
   * 맨 앞으로 돌려보내면 방금 있던 자리를 다시 찾아 들어가야 한다.
   */
  function backToList() {
    setStarted(null);
    setView(null);
    setChatOverride(false);
    setSeconds(0);
  }

  if (!started || !view) {
    return (
      <div className="viewport">
        <div className="phone">
          <LessonList
            learnerName={loadLearnerName()}
            collection={collection}
            onOpenCollection={setCollection}
            onBack={() => setCollection(null)}
            onPickSet={startSet}
          />
        </div>
      </div>
    );
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
            onClose={backToList}
          />
        ) : (
          <ClassroomChat
            view={view}
            setTitle={started.set?.title}
            elapsed={elapsed}
            typing={typing}
            onSend={send}
            onClose={backToList}
          />
        )}
        {view.recordLine ? <pre className="record">{view.recordLine}</pre> : null}
      </div>
    </div>
  );
}
