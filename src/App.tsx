import { useEffect, useMemo, useState } from "react";
import type { LessonCollection, LessonSet } from "../content/tutor/types";
import { ClassroomChat } from "./components/ClassroomChat";
import { LessonList } from "./components/LessonList";
import { HomeVillage } from "./components/HomeVillage";
import { CounselRoom } from "./components/CounselRoom";
import { SignupWelcome } from "./components/SignupWelcome";
import { ProgressBoard } from "./components/ProgressBoard";
import { PracticeRoom } from "./components/PracticeRoom";
import { WrongBook } from "./components/WrongBook";
import { WrongReview } from "./components/WrongReview";
import type { MiniStage } from "./components/CounselRoom";
import { VocabTest } from "./components/VocabTest";
import { firstMockId, isFirstVisit, isVocabSlot, markVocabSlot, nextProblemOf, onboardingSet, vocabSlotWords, withPlanMinutes } from "./tutor/counsel";
import { singleOf } from "./tutor/tenmin";
import { loadPlan, nextMockOf } from "./tutor/counsel";
import { MiniMockView } from "./components/MiniMockView";
import { getMiniMock, saveAttempt } from "./tutor/mini";
import { finishAnalysis } from "./tutor/miniLog";
import { SavedBook, type SavedKind } from "./components/SavedBook";
import { AccountLink } from "./components/AccountLink";
import { LoginScreen } from "./components/LoginScreen";
import { AuthCallback } from "./components/AuthCallback";
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
import { hasAccount } from "./tutor/auth";
import { policyLessonIds } from "./tutor/policy/lessons";
import { AUTO_NEXT_CMD, MODE_TRY_BTN, READ_DONE_BTN, createPolicySession, type PolicySession, type ResumeSnapshot } from "./tutor/policy/session";
import type { UiObservation } from "./tutor/policy/types";
import { clearResume, loadResume, markDone, noteReachedEnd, noteSmallScore, noteStudyTime, resumeRun, saveResume, startRun } from "./tutor/progress";
import { finishSessionRecord, startSessionRecord } from "./tutor/records";
import { pullAll } from "./tutor/cloud";
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
  const [miniView, setMiniView] = useState<{ id: string; showLast: boolean; n: number; stage?: MiniStage; lead?: boolean } | null>(() =>
    onlyMini ? { id: onlyMini, showLast: false, n: 0 } : null,
  );
  /** 홈(마을)에 있나 — 「오늘의 학습 시작하기」를 누르면 수업 목록으로 */
  const [home, setHome] = useState(true);
  /** 상담실에 있나 */
  const [counsel, setCounsel] = useState(false);
  /** 온보딩 — 처음 가입한 학생(코스가 없는 학생)에게 다정쌤 소개 + 학년·등급·기출 묻기 (2026-10-21 선생님) */
  const [welcome, setWelcome] = useState(false);
  /** 「기록 지키기」(이메일 붙이기) 화면에 있나 */
  const [account, setAccount] = useState(false);
  /** 로그인. 지문·세트·미니 링크로 들어온 경우는 건너뛴다 */
  const [passedLogin, setPassedLogin] = useState(
    () => Boolean(directLesson || directSet || shareLesson || onlyMini),
  );
  /** 소셜 로그인에서 돌아온 주소 (`/auth/callback`) */
  const [authCallback, setAuthCallback] = useState(() => window.location.pathname === "/auth/callback");
  /** 진도표(본 문제·안 본 문제·자주 틀리는 유형)에 있나 */
  const [board, setBoard] = useState(false);
  /** 코스의 단어 칸 — 그 회차 주요 단어 테스트 (id = vocab-<10분 모의고사 id>) */
  const [vocabSlot, setVocabSlot] = useState<string | null>(null);
  /** 틀린 문제 모아보기에 있나 */
  const [wrongBook, setWrongBook] = useState(false);
  /** 첫 방문 체험 분석 중 — 끝나면 코스 첫 회 10분 모의고사 시작 화면으로 (2026-10-20 선생님) */
  const [onboarding, setOnboarding] = useState(false);
  /** 코스의 문제 흐름(단어 → 풀기 → 분석 → 다음 문제) 안에 있나 — 그 시험 묶음 id */
  const [flow, setFlow] = useState<string | null>(null);
  /**
   * 코스 문제를 미리보기 화면에서 시간 재서 푸는 중 (2026-10-20 선생님) — 등급별 제한시간(`withPlanMinutes`),
   * 「시간 재서 풀어 볼게요」를 누르면 시작, 답을 고르면 그 문제의 10분 모의고사 기록(`ten-<시험>-q<번호>`)으로 남긴다
   */
  const [courseExam, setCourseExam] = useState<{ mockId: string; no: number; limit: number; startedAt: number | null; endedAt: number | null; analyzeBtn: string; unknown: { en: string; ko: string }[] } | null>(null);
  const [typing, setTyping] = useState(false);
  const [seconds, setSeconds] = useState(0);
  /*
    진행 기록·노트·단어장은 localStorage에서 동기로 읽는다. 앱을 열 때 서버 값과 합쳐
    로컬이 바뀌면 이 수가 올라가고, 그 값을 읽는 화면(홈·목록·단어장·상담실)을 다시 그린다.
    수업 화면은 건드리지 않는다 — 진행 중인 세션을 잃으면 안 된다.
  */
  const [cloudGen, setCloudGen] = useState(0);
  /** 서버 값을 한 번 받아 합쳤나 — 그 뒤에야 「계획이 없다」고 볼 수 있다 */
  const [pulled, setPulled] = useState(false);
  useEffect(() => {
    if (passedLogin || authCallback) return;
    void hasAccount().then((on) => on && setPassedLogin(true));
  }, [passedLogin, authCallback]);
  useEffect(() => {
    if (authCallback) return;
    void pullAll().then((changed) => {
      if (changed) setCloudGen((n) => n + 1);
      setPulled(true);
    });
  }, [authCallback]);
  /*
    가입하고 들어오면 온보딩 — 코스가 없는 학생은 다정쌤 소개를 듣고 학년·등급·기출을 골라 코스를 짠 뒤
    그 자리에서 첫 문제를 예시로 본다 (2026-10-20·21 선생님). 상담실은 홈에서 따로 들어간다.
    지문·미니 링크로 들어온 경우는 그대로 둔다.
  */
  const [autoCounsel, setAutoCounsel] = useState(false);
  useEffect(() => {
    if (autoCounsel || !passedLogin || !pulled || started) return;
    if (directLesson || directSet || shareLesson || onlyMini) return;
    setAutoCounsel(true);
    if (!loadPlan()) setWelcome(true);
  }, [autoCounsel, passedLogin, pulled, started, directLesson, directSet, shareLesson, onlyMini]);

  const session = started?.session ?? null;

  // 시계는 수업 중에만 간다. 목록을 보는 시간은 공부한 시간이 아니다
  useEffect(() => {
    if (!session) return;
    const id = window.setInterval(() => setSeconds((n) => n + 1), 1000);
    return () => window.clearInterval(id);
  }, [session]);
  // 목록에 「⏱ 10m」 — 10초마다, 그리고 목록으로 나갈 때 이 회차의 공부 시간을 남긴다
  useEffect(() => {
    if (started?.set && seconds > 0 && seconds % 10 === 0) noteStudyTime(started.set.id, seconds);
  }, [seconds, started]);

  /*
    수업 하나가 기록의 단위다. 시작할 때 행을 하나 열고, 끝날 때 결과와
    항목 기록을 한 번에 채운다. 실패해도 수업은 그대로 진행된다.
  */
  useEffect(() => {
    if (!session) return;
    void startSessionRecord(session.lessonId());
  }, [session]);

  /*
    이어 하기 — 화면이 바뀔 때마다 지금 자리를 남긴다. 끝난 수업은 지운다(다음엔 처음부터).
    마지막 문장까지 왔으면 답을 안 냈어도 「봤다」 (2026-10-20 선생님)
  */
  useEffect(() => {
    const id = started?.set?.id;
    if (!id || !session || shareLesson) return;
    if (view?.ended) {
      clearResume(id);
      return;
    }
    saveResume(id, session.lessonId(), session.snapshot());
    if (session.reachedEnd()) noteReachedEnd(id);
  }, [view, started, session]);

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
    if (setId && view?.smallScore) noteSmallScore(setId, view.smallScore.right, view.smallScore.total);
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

  // 미리보기에서 답을 골랐다 — 걸린 시간과 답을 코스 기록으로 (맞음/틀림·예상 점수·틀린 문제 복습이 여기서 나온다)
  useEffect(() => {
    if (!courseExam?.startedAt || courseExam.endedAt || !view?.passage) return;
    const picked = view.passage.right ?? view.passage.picked;
    if (view.passage.pickable || !picked) return;
    const secs = Math.round((Date.now() - courseExam.startedAt) / 1000);
    saveAttempt(courseExam.mockId, {
      at: new Date().toISOString(),
      answers: { [courseExam.no]: Number(picked) },
      seconds: secs,
      timeUp: secs > courseExam.limit,
      times: { [courseExam.no]: secs },
      unknown: courseExam.unknown.map((u) => ({ no: courseExam.no, ...u })),
    });
    setCourseExam({ ...courseExam, endedAt: Date.now() });
  }, [view, courseExam]);

  function send(text: string) {
    if (typing || !session) return;
    // 코스 문제 — 「시간 재서 풀어 볼게요」부터 시계가 간다
    if (courseExam && !courseExam.startedAt && text === MODE_TRY_BTN) setCourseExam({ ...courseExam, startedAt: Date.now() });
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

  /**
   * analyze — 미니 모의고사에서 분석하러 넘어왔다: 지문 한눈에 미리보기는 그대로 보여 주되(2026-10-20 선생님: 분석 전에
   * 전체 지문을 한 번 본다) 이미 푼 문제라 「바로 풀어 볼게요」만 뺀다. 이어 하기 없이 처음부터.
   */
  function startSet(set: LessonSet, analyze = false, course = false) {
    setCollection(getCollection(set.collection));
    const lessonId = firstLessonId(set);
    const next = open(lessonId);
    // 중간에 나갔던 수업이면 멈춘 자리부터 — 그 회차를 잇고 시계도 이어 간다 (미니 모의고사에서 분석하러 온 건 처음부터)
    const snap = analyze ? null : loadResume(set.id, lessonId);
    if (snap && next.session.restore(snap as ResumeSnapshot)) {
      setSeconds(resumeRun(set.id, lessonId));
    } else {
      clearResume(set.id);
      startRun(set.id, lessonId);
      setSeconds(0);
    }
    setStarted(next);
    const first = next.session.view();
    // 코스 문제는 미리보기에서 시간 재서 푸니 「바로 풀어 볼게요」도 그대로 (화면이 「시간 재서 풀어 볼게요」로 그린다)
    setView(analyze && !course ? { ...first, buttons: first.buttons.filter((b) => b !== MODE_TRY_BTN) } : first);
    // 코스 문제는 들어가자마자 보기를 고를 수 있게 (시계는 `courseExam.startedAt`부터) — 2026-10-20 선생님
    if (course && first.buttons.includes(MODE_TRY_BTN)) {
      // 「분석하기」 버튼이 보낼 말은 이 레슨의 읽기 버튼(첫 버튼) — 레슨마다 다를 수 있다
      const analyzeBtn = first.buttons[0] ?? READ_DONE_BTN;
      setCourseExam((c) => (c ? { ...c, analyzeBtn } : c));
      void next.session.submit(MODE_TRY_BTN).then(setView);
    }
    setChatOverride(false);
  }

  /**
   * 「학습 종료」와 「다시 시작」이 같은 자리로 간다 — **그 문제가 있던 목록**.
   * 맨 앞으로 돌려보내면 방금 있던 자리를 다시 찾아 들어가야 한다.
   */
  function backToList() {
    finishAnalysis("나감");
    if (started?.set) noteStudyTime(started.set.id, seconds);
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
    setCourseExam(null);
    // 코스 문제 흐름 — 분석이 끝났으면 다음 문제의 단어 화면으로, 다 끝났으면 코스 카드로
    if (flow) {
      const no = nextProblemOf(flow);
      setMiniView(no == null ? null : { id: `${flow}-q${no}`, showLast: false, n: 0, stage: "words" });
      if (no == null) setFlow(null);
      return;
    }
    // 첫 방문 체험이 끝났다 — 안내 한 줄과 함께 코스 첫 회로
    if (onboarding) {
      setOnboarding(false);
      const first = firstMockId(loadPlan());
      setHome(false);
      if (first) setMiniView({ id: first, showLast: false, n: 0, lead: true });
    }
  }

  if (authCallback && !started) {
    return (
      <div className="viewport">
        <div className="phone">
          <AuthCallback
            onDone={() => {
              window.history.replaceState({}, "", "/");
              setAuthCallback(false);
              setPassedLogin(true);
              setCloudGen((n) => n + 1);
            }}
            onBack={() => {
              window.history.replaceState({}, "", "/");
              setAuthCallback(false);
            }}
          />
        </div>
      </div>
    );
  }

  if (!passedLogin && !started) {
    return (
      <div className="viewport">
        <div className="phone">
          <LoginScreen onSkip={() => setPassedLogin(true)} />
        </div>
      </div>
    );
  }

  const mini = miniView ? withPlanMinutes(getMiniMock(miniView.id)) : null;
  if ((!started || !view) && mini && miniView && miniView.stage === "review") {
    return (
      <div className="viewport">
        <div className="phone">
          <WrongReview
            key={`${mini.id}-review-${miniView.n}`}
            mockId={mini.id}
            onBack={() => setMiniView(null)}
            onAnalyze={(set) => {
              // 분석을 보고 돌아오면 같은 복습 화면으로
              setMiniView({ ...miniView, n: miniView.n + 1 });
              startSet(set, true);
            }}
          />
        </div>
      </div>
    );
  }
  if ((!started || !view) && mini && miniView) {
    return (
      <div className="viewport">
        <div className="phone">
          <MiniMockView
            key={`${mini.id}-${miniView.n}`}
            mock={mini}
            showLast={miniView.showLast}
            flow={!!flow && !!singleOf(mini.id)}
            initialStage={miniView.stage === "review" ? undefined : miniView.stage}
            lead={miniView.lead ? "방금처럼 어려운 문제를 문장 단위로 잡아 드려요. 이제 10분 모의고사로 시작해요!" : undefined}
            standalone={miniView.id === onlyMini}
            onBack={() => {
              setFlow(null);
              setMiniView(null);
            }}
            onAnalyze={(set, fromExam) => {
              setMiniView({ id: mini.id, showLast: !fromExam, n: miniView.n + 1 });
              // 코스 문제 — 단어 화면 다음은 지문 미리보기, 거기서 시간 재서 푼다
              const single = flow ? singleOf(mini.id) : null;
              if (single) setCourseExam({ mockId: mini.id, no: single.no, limit: mini.minutes * 60, startedAt: Date.now(), endedAt: null, analyzeBtn: "", unknown: [] });
              startSet(set, true, !!single);
            }}
          />
        </div>
      </div>
    );
  }

  if ((!started || !view) && wrongBook) {
    return (
      <div className="viewport">
        <div className="phone">
          <WrongBook
            key={cloudGen}
            onBack={() => setWrongBook(false)}
            onOpenSet={(set) => {
              setWrongBook(false);
              setCounsel(false);
              setHome(false);
              startSet(set);
            }}
            onOpenMini={(id) => {
              setWrongBook(false);
              setMiniView({ id, showLast: false, n: 0 });
            }}
          />
        </div>
      </div>
    );
  }

  if ((!started || !view) && vocabSlot) {
    return (
      <div className="viewport">
        <div className="phone">
          <VocabTest
            key={vocabSlot}
            only={vocabSlotWords(vocabSlot)}
            onRetry={() => setVocabSlot(null)}
            onClose={() => {
              markVocabSlot(vocabSlot);
              setVocabSlot(null);
            }}
          />
        </div>
      </div>
    );
  }

  if ((!started || !view) && board) {
    return (
      <div className="viewport">
        <div className="phone">
          <ProgressBoard
            key={cloudGen}
            onBack={() => setBoard(false)}
            onOpenSet={(set) => {
              setBoard(false);
              setCounsel(false);
              setHome(false);
              startSet(set);
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
          {saved === "notes" ? (
            <SavedBook key={cloudGen} kind={saved} onBack={() => setSaved(null)} />
          ) : (
            <PracticeRoom key={cloudGen} tab="vocab" onBack={() => setSaved(null)} />
          )}
        </div>
      </div>
    );
  }

  if ((!started || !view) && account) {
    return (
      <div className="viewport">
        <div className="phone">
          <AccountLink
            onBack={() => setAccount(false)}
            // 로그인해서 서버 기록과 합쳐 로컬이 바뀌었으면 홈·목록·단어장을 다시 그린다
            onSynced={(changed) => changed && setCloudGen((n) => n + 1)}
          />
        </div>
      </div>
    );
  }

  if ((!started || !view) && welcome) {
    return (
      <div className="viewport">
        <div className="phone">
          <SignupWelcome
            learnerName={loadLearnerName()}
            // 예시 문제는 풀기가 아니라 **바로 분석** — 코스 첫 시험의 오답률 1위 (홈의 첫 방문 길과 같다, 2026-10-21 선생님)
            onStartExample={() => {
              setWelcome(false);
              const set = onboardingSet(loadPlan());
              if (!set) return;
              setOnboarding(true);
              setHome(false);
              startSet(set, true);
            }}
          />
        </div>
      </div>
    );
  }

  if ((!started || !view) && counsel) {
    return (
      <div className="viewport">
        <div className="phone">
          <CounselRoom
            key={cloudGen}
            learnerName={loadLearnerName()}
            onClose={() => setCounsel(false)}
            // 코스의 10분 모의고사 — 끝나고 「목록으로」 하면 상담실 코스 화면으로 돌아온다
            onOpenMini={(id, stage) => {
              if (isVocabSlot(id)) return setVocabSlot(id);
              // 낱개 문제를 단어 화면부터 열면 문제 흐름 — 분석이 끝나면 다음 문제로 이어진다
              setFlow(stage === "words" ? (singleOf(id)?.base ?? null) : null);
              setMiniView({ id, showLast: false, n: 0, stage });
            }}
            onOpenBoard={() => setBoard(true)}
            onOpenWrong={() => setWrongBook(true)}
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
            key={cloudGen}
            learnerName={loadLearnerName()}
            onStart={() => {
              // 코스의 다음 10분 모의고사로(상담을 안 했어도 최근 시험부터), 코스를 다 맞혔으면 수업 목록으로
              // 첫 방문 — 코스 첫 회 오답률 1위 문제를 분석 모드로 바로 (10분 시험은 그다음)
              if (isFirstVisit()) {
                const set = onboardingSet(loadPlan());
                if (set) {
                  setOnboarding(true);
                  setHome(false);
                  startSet(set, true);
                  return;
                }
              }
              const next = nextMockOf(loadPlan());
              if (next && isVocabSlot(next)) setVocabSlot(next);
              else if (next) {
                // 다음 문제의 단어 화면부터 — 문제 흐름
                const no = nextProblemOf(next);
                setFlow(no == null ? null : next);
                setMiniView(no == null ? { id: next, showLast: false, n: 0 } : { id: `${next}-q${no}`, showLast: false, n: 0, stage: "words" });
              } else setHome(false);
            }}
            onOpenCounsel={() => setCounsel(true)}
            onOpenMini={() => {
              window.location.assign("/staff/loopin-staff-room-raised.html");
            }}
            onOpenSaved={setSaved}
            onOpenAccount={() => setAccount(true)}
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
            key={cloudGen}
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
          <ReadPassage
            view={view}
            onSend={send}
            onClose={backToList}
            course={
              courseExam
                ? {
                    minutes: courseExam.limit / 60,
                    left: courseExam.startedAt ? Math.round(courseExam.limit - ((courseExam.endedAt ?? Date.now()) - courseExam.startedAt) / 1000) : null,
                    analyzeBtn: courseExam.analyzeBtn || READ_DONE_BTN,
                    item: getMiniMock(courseExam.mockId)!.items[0]!,
                    onUnknown: (unknown) => setCourseExam((c) => (c ? { ...c, unknown } : c)),
                  }
                : undefined
            }
          />
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
