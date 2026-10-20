import { useEffect, useMemo, useState } from "react";
import type { LessonCollection, LessonSet } from "../content/tutor/types";
import { ClassroomChat } from "./components/ClassroomChat";
import { LessonList } from "./components/LessonList";
import { HomeVillage } from "./components/HomeVillage";
import { CounselRoom } from "./components/CounselRoom";
import { loadPlan, nextSetOf } from "./tutor/counsel";
import { loadProgress } from "./tutor/progress";
import { MiniMockView } from "./components/MiniMockView";
import { allMiniMocks, getMiniMock } from "./tutor/mini";
import { finishAnalysis } from "./tutor/miniLog";
import { SavedBook, type SavedKind } from "./components/SavedBook";
import { ReadPassage } from "./components/ReadPassage";
import { PointsReview } from "./components/PointsReview";
import { SummaryView } from "./components/SummaryView";
import { MatchGame } from "./components/MatchGame";
import { WordCheck } from "./components/WordCheck";
import { SentenceStudy } from "./components/SentenceStudy";
import { SpeakingLesson } from "./components/SpeakingLesson";
import { getSpeakingLesson } from "./speaking/lessons";
import type { TutorView } from "./tutor/view";
import { loadLearnerName, saveLearnerName } from "./tutor/learner-name";
import { policyLessonIds } from "./tutor/policy/lessons";
import { AUTO_NEXT_CMD, createPolicySession, type PolicySession } from "./tutor/policy/session";
import type { UiObservation } from "./tutor/policy/types";
import { markDone, startRun } from "./tutor/progress";
import { finishSessionRecord, startSessionRecord } from "./tutor/records";
import { firstLessonId, getCollection, getSet, setOfLesson } from "./tutor/sets";

/*
  개발에서 지문 하나만 보고 싶을 때가 있다. `?lesson=<id>`나 `?set=<id>`가
  있으면 목록을 건너뛰고 바로 시작한다 (`src/tutor/sets.ts`).
  문장 학습의 단어 뜻은 레슨 JSON `glosses`에서 온다.
*/
const params = new URLSearchParams(window.location.search);
/*
  공유용 한 장짜리 HTML(`scripts/build_share.mjs`)은 빌드할 때 `VITE_SHARE_LESSON`에 지문을
  박는다. 그 파일에는 목록이 없고, 열면 바로 그 수업이 시작된다.
*/
const shareLesson = (import.meta.env.VITE_SHARE_LESSON as string | undefined) || null;
const directLesson = import.meta.env.DEV ? params.get("lesson") : shareLesson;
const directSet = import.meta.env.DEV ? getSet(params.get("set")) : null;
/* 학생 테스트 링크(`npm run share:mini2403`)는 미니 모의고사 하나만 연다. 개발에선 `?mini=<id>` */
const onlyMini = (import.meta.env.DEV ? params.get("mini") : import.meta.env.VITE_ONLY_MINI) || null;

/* 수업은 전부 Teaching Policy 세션이다 (예전 해석 엔진은 2026-10-05에 지웠다) */
type AnySession = PolicySession & { observe?: (observation: UiObservation) => void };

type Started = { session: AnySession; set: LessonSet | null };

/** 수업 하나를 연다. 이름은 아는 사람이면 물어보지 않고 그 이름으로 인사한다 */
function open(lessonId: string | null): Started {
  const name = import.meta.env.DEV && params.has("newname") ? null : loadLearnerName();
  // 모르는 id면 첫 수업으로
  const id = lessonId && policyLessonIds().includes(lessonId) ? lessonId : policyLessonIds()[0]!;
  const session: AnySession = createPolicySession(id, name);
  return { session, set: setOfLesson(session.lessonId()) };
}

/*
  토익 스피킹 시범(2026-10-15) — `?speaking=<id>`로 연다. 독해 수업과 엔진이 달라 따로 그린다.
  시범이라 개발 빌드가 아니어도 열린다. 공유용 한 장 HTML은 `VITE_SHARE_SPEAKING`에 id를 박는다
*/
const speakingLesson = getSpeakingLesson(
  params.get("speaking") ?? ((import.meta.env.VITE_SHARE_SPEAKING as string | undefined) || null),
);

export function App() {
  if (speakingLesson) {
    return (
      <div className="viewport">
        <div className="phone">
          <SpeakingLesson lesson={speakingLesson} onClose={() => (window.location.search = "")} />
        </div>
      </div>
    );
  }
  return <ReadingApp />;
}

function ReadingApp() {
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
  /** 메인에서 연 단어장 · 내 노트 */
  const [saved, setSaved] = useState<SavedKind | null>(null);
  /** 미니 모의고사 — 분석 레슨을 보고 돌아오면 그 결과로(showLast), 푸는 중에 갔으면 이어 풀기로 */
  const [miniView, setMiniView] = useState<{ id: string; showLast: boolean; n: number } | null>(() =>
    onlyMini ? { id: onlyMini, showLast: false, n: 0 } : null,
  );
  /** 홈(마을)에 있나 — 「오늘의 학습 시작하기」를 누르면 수업 목록으로 */
  const [home, setHome] = useState(true);
  /** 상담실에 있나 */
  const [counsel, setCounsel] = useState(false);
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
    // 미니 모의고사에서 분석하러 왔으면 그 풀이 기록에도 결과를 남긴다
    finishAnalysis(result);
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
  // 버튼 없이 저절로 넘어가는 말 (도입의 「첫 문장의 핵심 단어를 찾아볼까요?」 등)
  useEffect(() => {
    const ms = view?.autoNextMs;
    if (!ms || !session) return;
    const id = window.setTimeout(() => void session.submit(AUTO_NEXT_CMD).then(setView), ms);
    return () => window.clearTimeout(id);
  }, [view, session]);

  function send(text: string) {
    if (typing || !session) return;
    // 화면 조작 신호(__로 시작)는 선생님이 생각할 일이 아니다 — 기다리지 않고 바로
    if (text.startsWith("__")) {
      void session.submit(text).then(setView);
      return;
    }
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
      // 점 세 개는 잠깐만 — 길면 여러 지문을 이어 푸는 학생에게 답답하다
    }, 250);
  }

  /** analyze — 미니 모의고사에서 넘어왔다: 이미 푼 문제라 미리보기·「바로 풀어 볼게요」를 건너뛰고 바로 다정쌤 분석으로 */
  function startSet(set: LessonSet, analyze = false) {
    setCollection(getCollection(set.collection));
    startRun(set.id);
    const next = open(firstLessonId(set));
    setStarted(next);
    setView(next.session.view());
    setChatOverride(false);
    setSeconds(0);
    const go = next.session.view().buttons[0];
    if (analyze && go) void next.session.submit(go).then(setView);
  }

  /**
   * 「학습 종료」와 「다시 시작」이 같은 자리로 간다 — **그 문제가 있던 목록**.
   * 맨 앞으로 돌려보내면 방금 있던 자리를 다시 찾아 들어가야 한다.
   */
  function backToList() {
    finishAnalysis("나감");
    // 공유 파일에는 목록이 없다 — 닫으면 같은 수업을 처음부터
    if (shareLesson) {
      const next = open(shareLesson);
      setStarted(next);
      setView(next.session.view());
      setChatOverride(false);
      setSeconds(0);
      return;
    }
    setStarted(null);
    setView(null);
    setChatOverride(false);
    setSeconds(0);
  }

  const mini = miniView ? getMiniMock(miniView.id) : null;
  if ((!started || !view) && mini && miniView) {
    return (
      <div className="viewport">
        <div className="phone">
          <MiniMockView
            key={`${mini.id}-${miniView.n}`}
            mock={mini}
            showLast={miniView.showLast}
            standalone={miniView.id === onlyMini}
            onBack={() => setMiniView(null)}
            onAnalyze={(set, fromExam) => {
              setMiniView({ id: mini.id, showLast: !fromExam, n: miniView.n + 1 });
              startSet(set, true);
            }}
          />
        </div>
      </div>
    );
  }

  if ((!started || !view) && saved) {
    return (
      <div className="viewport">
        <div className="phone">
          <SavedBook kind={saved} onBack={() => setSaved(null)} />
        </div>
      </div>
    );
  }

  /** 상담실 계획의 문제를 바로 시작한다 (끝나면 다른 수업처럼 그 문제가 있던 목록으로) */
  function startPlanned(setId: string) {
    const set = getSet(setId);
    if (!set) return;
    setCounsel(false);
    setHome(false);
    startSet(set);
  }

  if ((!started || !view) && counsel) {
    return (
      <div className="viewport">
        <div className="phone">
          <CounselRoom
            learnerName={loadLearnerName()}
            onClose={() => setCounsel(false)}
            onStartSet={startPlanned}
            onOpenMini={() => {
              const first = allMiniMocks()[0];
              if (first) setMiniView({ id: first.id, showLast: false, n: 0 });
            }}
          />
        </div>
      </div>
    );
  }

  if ((!started || !view) && home) {
    return (
      <div className="viewport">
        <div className="phone">
          <HomeVillage
            learnerName={loadLearnerName()}
            onStart={() => {
              // 상담실에서 짠 계획이 있으면 그다음 문제로, 없으면 수업 목록으로
              const plan = loadPlan();
              const next = plan ? nextSetOf(plan, loadProgress()) : null;
              if (next) startPlanned(next);
              else setHome(false);
            }}
            onOpenCounsel={() => setCounsel(true)}
            onOpenMini={() => {
              const first = allMiniMocks()[0];
              if (first) setMiniView({ id: first.id, showLast: false, n: 0 });
              else setHome(false);
            }}
            onOpenSaved={setSaved}
          />
        </div>
      </div>
    );
  }

  if (!started || !view) {
    return (
      <div className="viewport">
        <div className="phone">
          <LessonList
            onHome={() => {
              setCollection(null);
              setHome(true);
            }}
            learnerName={loadLearnerName()}
            collection={collection}
            onOpenCollection={setCollection}
            onBack={() => setCollection(null)}
            onPickSet={startSet}
            onOpenMini={(id) => setMiniView({ id, showLast: false, n: 0 })}
            onOpenSaved={setSaved}
          />
        </div>
      </div>
    );
  }

  const screen = chatOverride ? "chat" : view.screen;

  return (
    <div className="viewport">
      <div className="phone">
        {screen === "read" && view.passage ? (
          <ReadPassage view={view} onSend={send} onClose={backToList} />
        ) : screen === "words" && view.wordCheck ? (
          <WordCheck view={view} onSend={send} onClose={backToList} />
        ) : screen === "summary" && view.summary && session ? (
          <SummaryView view={view} lessonId={session.lessonId()} onSend={send} onClose={backToList} />
        ) : screen === "points" && view.pointsReview ? (
          <PointsReview view={view} onSend={send} onClose={backToList} />
        ) : screen === "match" && view.matchPairs ? (
          <MatchGame view={view} onSend={send} onClose={backToList} />
        ) : screen === "study" ? (
          <SentenceStudy
            view={view}
            typing={typing}
            onSend={send}
            onBack={() => setChatOverride(true)}
            onClose={backToList}
            onObserve={session?.observe}
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
