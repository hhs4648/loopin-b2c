import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import type { LessonSet } from "../../content/tutor/types";
import {
  averageTimes,
  byKind,
  clock,
  clearDoing,
  estimatedExamScore,
  isReviewMock,
  loadAttempts,
  loadDoing,
  saveAttempt,
  saveDoing,
  scoreOf,
  type MiniAttempt,
  type MiniItem,
  type MiniMock,
} from "../tutor/mini";
import { getSet } from "../tutor/sets";
import { isDone, loadProgress } from "../tutor/progress";
import { mockKeyWords } from "../tutor/counsel";
import { loadLearnerName } from "../tutor/learner-name";
import { getUser, MiniRecorder, startAnalysis } from "../tutor/miniLog";
import { MiniTeacherBoard } from "./MiniTeacherBoard";
import { MarkArea, markWords, NO_MARKS, NO_OVERLAY, type Marks, type Overlay, type Pen } from "./MiniMarks";
import { getPolicyLesson } from "../tutor/policy/lessons";
import { cleanWord, meaningOf } from "../tutor/miniWords";
import { addVocab, isSaved, loadVocab, toggleVocab, type VocabEntry } from "../tutor/vocab";

export const NUM = "①②③④⑤";

/**
 * 푸는 중에 분석 레슨으로 간 시험 — 돌아오면 같은 문항에서 이어 푼다(분석한 시간은 시험 시간에서 뺀다).
 * 화면이 닫혀도 남아야 해서 모듈에 둔다
 */
/** 「분석 먼저 하고 풀게요」에서 레슨으로 간 모의고사 — 돌아오면 분석 목록으로 (`paused`와 같은 방식) */
let prepFor: string | null = null;

type Paused = { mockId: string; answers: Record<number, number>; checked: number[]; peeked: number[]; marks: Record<number, Marks>; at: number; usedMs: number; times?: Record<number, number>; recorder: MiniRecorder | null };
let paused: Paused | null = null;
export function hasPausedExam(mockId: string): boolean {
  return paused?.mockId === mockId;
}

type Props = {
  mock: MiniMock;
  /** 처음부터 지난 결과를 보일까 (분석 레슨을 보고 돌아왔을 때) */
  showLast: boolean;
  onBack: () => void;
  /** 분석 레슨으로. fromExam이면 푸는 중에 간 것 — 돌아오면 이어 푼다 */
  onAnalyze: (set: LessonSet, fromExam: boolean) => void;
  /** 학생 테스트용 링크 — 목록 없이 이 시험만. 이름을 받고 지표를 남긴다 */
  standalone?: boolean;
  /** 코스에서 단계별로 열 때 — 단어 학습(words) · 분석 목록(prep) */
  initialStage?: "words" | "prep";
  /** 시작 화면 맨 위 다정쌤 한 줄 — 첫 방문 체험 분석을 마치고 왔을 때 */
  lead?: string;
  /** 코스의 문제 흐름(단어 → 풀기 → 분석) 안에서 열렸다 — 단어 화면에서 풀기를 건너뛸 수 있고, 결과 화면 맨 위에 분석 버튼 */
  flow?: boolean;
};

const NAME_KEY = "loopin.mini.name";
function savedName(): string {
  try {
    return window.localStorage.getItem(NAME_KEY) ?? "";
  } catch {
    return "";
  }
}

/**
 * 미니 모의고사 — 시작 → 시간 재며 풀기(문항마다 바로 정답 확인·분석도 된다) → 제출(또는 시간 끝) → 점수와 문항별 해설.
 * 수업과 달리 선생님 말은 없다. 실제 시험처럼 문제만.
 */
export function MiniMockView({ mock, showLast, onBack, onAnalyze, standalone, initialStage, lead, flow }: Props) {
  /** 흐름 모드의 문제(한 문항)의 분석 레슨 세트 */
  const flowSet = flow && mock.items.length === 1 && mock.items[0]!.lesson ? getSet(mock.items[0]!.lesson) : null;
  const resume = paused?.mockId === mock.id ? paused : null;
  // 「분석 먼저」에서 레슨에 갔다 돌아오면 다시 그 목록으로
  const backToPrep = prepFor === mock.id;
  const [stage, setStage] = useState<"intro" | "words" | "prep" | "exam" | "result">(() =>
    resume ? "exam" : backToPrep ? "prep" : initialStage ?? (showLast && loadAttempts(mock.id).length ? "result" : "intro"),
  );
  const [attempt, setAttempt] = useState<MiniAttempt | null>(() => (showLast ? (loadAttempts(mock.id)[0] ?? null) : null));
  const [name, setName] = useState(() => (standalone ? savedName() : (loadLearnerName() ?? "")));
  /** 선생님(아티팩트 주인)인가 */
  const [owner, setOwner] = useState(false);
  const [board, setBoard] = useState(false);
  const recorder = useRef<MiniRecorder | null>(resume?.recorder ?? null);
  const [initial, setInitial] = useState<Paused | null>(() => {
    paused = null;
    return resume;
  });
  /** 중간에 나갔던 풀이 — 있으면 「이어서 풀기」 */
  const doing = loadDoing(mock.id);
  useEffect(() => {
    if (!standalone) return;
    void getUser().then(async (u) => setOwner((await u?.isOwner()) ?? false));
  }, [standalone]);

  const start = () => {
    recorder.current = new MiniRecorder(mock, name.trim());
    setStage("exam");
  };

  if (board) return <MiniTeacherBoard mock={mock} onBack={() => setBoard(false)} />;

  if (stage === "words") {
    return (
      <MiniWords
        mock={mock}
        onBack={flow ? onBack : () => setStage("intro")}
        // 코스 문제는 지문 미리보기로 — 거기서 시간 재서 풀고 바로 분석 (2026-10-20 선생님)
        onStart={flowSet ? () => onAnalyze(flowSet, false) : start}
      />
    );
  }

  if (stage === "prep") {
    return (
      <MiniPrep
        mock={mock}
        onBack={() => {
          prepFor = null;
          setStage("intro");
        }}
        onStart={() => {
          prepFor = null;
          start();
        }}
        onAnalyze={(set, no) => {
          prepFor = mock.id;
          startAnalysis(recorder.current, no);
          onAnalyze(set, false);
        }}
      />
    );
  }

  if (stage === "exam") {
    return (
      <MiniExam
        mock={mock}
        initial={initial}
        recorder={recorder.current}
        onQuit={() => setStage("intro")}
        onSubmit={(a) => {
          // 복습 모의고사는 풀 때마다 문항이 달라서 그때 문항을 같이 남긴다
          saveAttempt(mock.id, isReviewMock(mock.id) ? { ...a, items: mock.items.map((it) => ({ no: it.no, lesson: it.lesson })) } : a);
          clearDoing(mock.id);
          setAttempt(a);
          setStage("result");
        }}
        onAnalyze={(set, state) => {
          paused = { ...state, mockId: mock.id, recorder: recorder.current };
          startAnalysis(recorder.current, state.no);
          onAnalyze(set, true);
        }}
      />
    );
  }
  if (stage === "result" && attempt) {
    return (
      <MiniResult
        mock={mock}
        attempt={attempt}
        recorder={recorder.current}
        onBack={standalone ? () => setStage("intro") : onBack}
        flowSet={flowSet}
        onRetry={start}
        onAnalyze={(set, no) => {
          startAnalysis(recorder.current, no);
          onAnalyze(set, false);
        }}
      />
    );
  }
  const last = loadAttempts(mock.id)[0];
  const max = mock.items.reduce((n, it) => n + it.points, 0);
  return (
    <div className="stage-fill saved mini">
      <header className="saved-top">
        {standalone ? null : (
          <button type="button" className="icon-btn light" title="목록으로" aria-label="목록으로" onClick={onBack}>
            <BackIcon />
          </button>
        )}
      </header>
      <div className="saved-body-scroll">
        {lead ? <p className="mini-lead">{lead}</p> : null}
        <p className="home-hello">미니 모의고사</p>
        <h1 className="saved-title">{mock.title}</h1>
        <p className="mini-sub">{mock.subtitle}</p>
        <ul className="mini-facts">
          <li><b>{mock.minutes}분</b><small>제한 시간</small></li>
          <li><b>{mock.items.length}문항</b><small>{mock.items[0]!.no}~{mock.items[mock.items.length - 1]!.no}번 차례대로</small></li>
          <li><b>{max}점</b><small>만점</small></li>
        </ul>
        <p className="pack-help">
          실제 시험처럼 시간을 재며 풀어요. 한 문제를 풀고 바로 「정답 확인」을 눌러 맞혀 볼 수도 있어요.
          틀린 문제나 모르는 문제는 다정쌤과 분석하러 갈 수 있고, 분석하는 동안은 시계가 멈춰요. ⏸ 버튼으로 잠깐 쉴 수도 있어요.
        </p>
        {standalone ? (
          <label className="mini-name">
            <span>이름</span>
            <input
              id="mini-name"
              value={name}
              maxLength={20}
              placeholder="이름을 적어 주세요"
              onChange={(e) => {
                setName(e.target.value);
                try {
                  window.localStorage.setItem(NAME_KEY, e.target.value);
                } catch {
                  /* 다음에 다시 적으면 된다 */
                }
              }}
            />
          </label>
        ) : null}
        {doing ? (
          // 풀던 게 있으면 무조건 이어서 — 「처음부터 다시」는 두지 않는다 (2026-10-20 선생님: 선택지가 너무 많다)
          <button
            type="button"
            className="mini-start"
            disabled={standalone && !name.trim()}
            onClick={() => {
              setInitial({ ...doing, mockId: mock.id, recorder: null });
              start();
            }}
          >
            이어서 풀게요 · {Object.keys(doing.answers).length}/{mock.items.length}문항 · 남은 {clock(Math.max(0, mock.minutes * 60 - doing.usedMs / 1000))}
          </button>
        ) : (
          <button
            type="button"
            className="mini-start"
            disabled={standalone && !name.trim()}
            onClick={() => {
              setInitial(null);
              // 풀기 전에 주요 단어를 한 번 보여 준다 — 따로 메뉴로 두지 않는다 (2026-10-20 선생님). 단어가 없는 시험은 바로
              if (mockKeyWords(mock.id).length) setStage("words");
              else start();
            }}
          >
            바로 풀어 볼게요
          </button>
        )}

        {owner ? (
          <button type="button" className="mini-last" onClick={() => setBoard(true)}>
            선생님 · 학생 결과 보기
          </button>
        ) : null}
        {last ? (
          <button
            type="button"
            className="mini-last"
            onClick={() => {
              setAttempt(last);
              setStage("result");
            }}
          >
            지난 결과 보기 · {scoreOf(mock, last.answers).score}/{max}점
          </button>
        ) : null}
      </div>
    </div>
  );
}

/** 지문 단어 미리 보기 —풀기 전에 그 회 지문·보기의 주요 단어를 훑는다. 뜻은 가려 두고 누르면 보인다 (외웠나 스스로 확인) */
/** 단어 발음 — 브라우저 음성(en-US). 소리를 못 내는 기기면 조용히 넘어간다 */
export function sayWord(text: string): void {
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-US";
  u.rate = 0.9;
  window.speechSynthesis.speak(u);
}

function MiniWords({ mock, onBack, onStart }: { mock: MiniMock; onBack: () => void; onStart: () => void }) {
  const words = useMemo(() => mockKeyWords(mock.id), [mock.id]);
  const [shown, setShown] = useState<Set<string>>(() => new Set());
  const [allShown, setAllShown] = useState(false);
  /** 별표 — 단어장에 저장 (수업의 단어 별표와 같은 단어장) */
  const [vocab, setVocab] = useState<VocabEntry[]>(() => loadVocab());
  const toggle = (en: string) => setShown((s) => {
    const n = new Set(s);
    if (n.has(en)) n.delete(en);
    else n.add(en);
    return n;
  });
  return (
    <div className="stage-fill saved mini">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="뒤로" aria-label="뒤로" onClick={onBack}>
          <BackIcon />
        </button>
      </header>
      <div className="saved-body-scroll">
        <p className="home-hello">{mock.title}</p>
        <h1 className="home-title">지문 단어 미리 보기</h1>
        {/* 단어 수·「이번 회 지문과 보기에 나오는」은 뺐다 — 할 일만 한 줄 (2026-10-21 선생님) */}
        <p className="pack-help">모르는 단어는 별표를 누르면 단어장에 저장돼요.</p>
        <div className="mini-words-sub">
          <button type="button" className="mini-words-all" onClick={() => setAllShown((v) => !v)}>{allShown ? "뜻 가리기" : "뜻 모두 보기"}</button>
        </div>
        <ul className="mini-words">
          {words.map((w) => {
            const on = allShown || shown.has(w.en);
            return (
              <li key={w.en} className="mini-word-row">
                <button type="button" className="mini-word-say" aria-label={`${w.en} 발음 듣기`} onClick={() => sayWord(w.en)}>
                  {/* 이모지 🔊 대신 분홍 선 스피커 (2026-10-20 선생님: 안 예쁘다) */}
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <path d="M11 5L6 9H3v6h3l5 4z" fill="currentColor" fillOpacity=".18" />
                    <path d="M15.5 8.5a5 5 0 0 1 0 7" />
                    <path d="M18.5 5.5a9 9 0 0 1 0 13" />
                  </svg>
                </button>
                <button type="button" className={`mini-word${on ? " on" : ""}`} onClick={() => toggle(w.en)}>
                  <b>{w.en}</b>
                  <span>{on ? w.ko : "뜻 보기"}</span>
                </button>
                <button
                  type="button"
                  className={`point-star mini-word-star${isSaved(vocab, w.en) ? " on" : ""}`}
                  aria-label={isSaved(vocab, w.en) ? "단어장에서 빼기" : "단어장에 저장"}
                  onClick={() => setVocab(toggleVocab(vocab, { en: w.en, ko: w.ko, sentence: "", source: w.source, kind: w.kind }))}
                >
                  {isSaved(vocab, w.en) ? "★" : "☆"}
                </button>
              </li>
            );
          })}
        </ul>
        {/* 단어를 다 본 뒤에 — 버튼은 아래 (2026-10-20 선생님) */}
        <button type="button" className="mini-start mini-words-go" onClick={onStart}>
          문제 풀러 갈게요
        </button>
      </div>
    </div>
  );
}

/** 분석 먼저 — 문항마다 다정쌤 분석 레슨으로. 다 보고(또는 보고 싶은 만큼 보고) 시간을 재며 푼다 */
function MiniPrep({ mock, onBack, onStart, onAnalyze }: { mock: MiniMock; onBack: () => void; onStart: () => void; onAnalyze: (set: LessonSet, no: number) => void }) {
  const progress = loadProgress();
  const rows = mock.items.map((it) => ({ it, set: it.lesson ? getSet(it.lesson) : null }));
  const seen = rows.filter((r) => r.set && isDone(progress, r.set.id)).length;
  return (
    <div className="stage-fill saved mini">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="뒤로" aria-label="뒤로" onClick={onBack}>
          <BackIcon />
        </button>
      </header>
      <div className="saved-body-scroll">
        <p className="home-hello">{mock.title}</p>
        <h1 className="home-title">분석 먼저 하고 풀기</h1>
        <p className="pack-help">문제마다 다정쌤과 한 문장씩 읽고 나서 시간을 재며 풀어요. 다 안 봐도 돼요 — 보고 싶은 것만 보고 풀어도 괜찮아요.</p>
        <ul className="mini-review prep">
          {rows.map(({ it, set }) => {
            const done = !!set && isDone(progress, set.id);
            return (
              <li key={it.no} className={done ? "right" : ""}>
                <button type="button" className="mini-row" disabled={!set} onClick={() => set && onAnalyze(set, it.no)}>
                  <span className="mini-mark">{done ? "✓" : ""}</span>
                  <span className="mini-row-text">
                    <b>{it.no}번 · {it.kind}{it.points === 3 ? " [3점]" : ""}</b>
                    <small>{set ? (done ? "분석 봤어요 · 다시 보기" : "다정쌤과 분석하기") : "분석 레슨이 아직 없어요"}{it.wrong_rate != null ? ` · 전국 오답률 ${it.wrong_rate}%` : ""}</small>
                  </span>
                  <span className="mini-chev">›</span>
                </button>
              </li>
            );
          })}
        </ul>
        <button type="button" className="mini-start" onClick={onStart}>
          {seen ? `이제 풀어 볼게요 (${seen}/${rows.length} 분석함)` : "분석 없이 바로 풀게요"}
        </button>
      </div>
    </div>
  );
}

type ExamState = { answers: Record<number, number>; checked: number[]; peeked: number[]; marks: Record<number, Marks>; at: number; usedMs: number; times: Record<number, number>; no: number };

function MiniExam({
  mock,
  initial,
  recorder,
  onQuit,
  onSubmit,
  onAnalyze,
}: {
  mock: MiniMock;
  initial: Paused | null;
  recorder: MiniRecorder | null;
  onQuit: () => void;
  onSubmit: (a: MiniAttempt) => void;
  onAnalyze: (set: LessonSet, state: ExamState) => void;
}) {
  const limit = mock.minutes * 60;
  const [answers, setAnswers] = useState<Record<number, number>>(initial?.answers ?? {});
  /** 「정답 확인」을 누른 문항 — 그 문항은 답을 바꿀 수 없다 */
  const [checked, setChecked] = useState<number[]>(initial?.checked ?? []);
  /** 답을 고르기 전에 분석을 먼저 본 문항 — 돌아와서 고를 수 있지만 「분석 보고 고름」으로 따로 표시 */
  const [peeked, setPeeked] = useState<number[]>(initial?.peeked ?? []);
  /** 지문에 표시한 것 — 문항마다 형광펜·모르는 단어 */
  const [marks, setMarks] = useState<Record<number, Marks>>(initial?.marks ?? {});
  /** 고른 펜 · 끊어읽기 · 핵심어 보기 — 문항을 넘겨도 그대로 */
  const [pen, setPen] = useState<Pen>("none");
  const [showSlash, setShowSlash] = useState(false);
  const [showKeys, setShowKeys] = useState(false);
  // 뜻을 보여 주는 토스트는 조금 더 오래(ms) — 읽을 시간이 필요하다
  const [toastState, setToastState] = useState<{ text: string; ms: number } | null>(null);
  const toast = toastState?.text ?? null;
  const setToast = (text: string | null, ms = 1600) => setToastState(text ? { text, ms } : null);
  useEffect(() => {
    if (!toastState) return;
    const id = window.setTimeout(() => setToastState(null), toastState.ms);
    return () => window.clearTimeout(id);
  }, [toastState]);
  const unknownList = () => mock.items.flatMap((it) => (marks[it.no]?.unk ?? []).map((u) => ({ no: it.no, en: u.en, ko: u.ko })));
  const [at, setAt] = useState(initial?.at ?? 0);
  // 분석하러 갔다 오면 쓴 시간만큼 이어서 — 분석한 시간은 빠진다
  const started = useRef(Date.now() - (initial?.usedMs ?? 0));
  const [left, setLeft] = useState(limit - (initial?.usedMs ?? 0) / 1000);
  const [confirm, setConfirm] = useState<"submit" | "quit" | null>(null);
  /** 「일시정지」를 누른 때 — 그동안 시계가 멈추고 문제는 가려진다 */
  const [breakAt, setBreakAt] = useState<number | null>(null);
  const done = useRef(false);
  const scroll = useRef<HTMLDivElement>(null);
  /** 문항마다 쓴 시간(초) — 지금 문항은 들어온 때부터 더해 간다 (일시정지 동안은 안 셈) */
  const times = useRef<Record<number, number>>({ ...(initial?.times ?? {}) });
  const timing = useRef<{ no: number; since: number } | null>(null);
  const tally = () => {
    const t = timing.current;
    if (!t) return times.current;
    const now = Date.now();
    times.current[t.no] = Math.round(((times.current[t.no] ?? 0) + (now - t.since) / 1000) * 10) / 10;
    t.since = now;
    return times.current;
  };

  const submit = (timeUp: boolean) => {
    if (done.current) return;
    done.current = true;
    recorder?.finish(timeUp ? "timeup" : "submitted", answers);
    const spent = { ...tally() };
    timing.current = null;
    onSubmit({ at: new Date().toISOString(), answers, seconds: (Date.now() - started.current) / 1000, timeUp, checked, peeked, unknown: unknownList(), times: spent });
  };
  // 남은 시간 — 시계로 잰다 (탭이 잠깐 멈춰도 어긋나지 않게)
  useEffect(() => {
    if (breakAt != null) return;
    const id = window.setInterval(() => {
      // 시간이 다 돼도 내지 않는다 — 「초과」만 보여 주고 계속 풀게 (2026-10-20 선생님)
      setLeft(limit - (Date.now() - started.current) / 1000);
    }, 500);
    return () => window.clearInterval(id);
  }, [limit, breakAt]);
  /*
    푸는 중 상태를 남긴다 — 답을 고르거나 표시할 때마다, 그리고 10초마다(쓴 시간). 중간에 나가도 돌아오면
    거기서부터, 남은 시간부터 이어 푼다. 제출하면 지운다 (`clearDoing`).
  */
  const snapshot = () => {
    if (done.current) return;
    const usedMs = (breakAt ?? Date.now()) - started.current;
    if (breakAt == null) tally();
    saveDoing(mock.id, { answers, checked, peeked, marks, at, usedMs, times: { ...times.current } });
  };
  const snapshotRef = useRef(snapshot);
  snapshotRef.current = snapshot;
  useEffect(() => {
    snapshotRef.current();
  }, [answers, checked, peeked, marks, at]);
  useEffect(() => {
    const id = window.setInterval(() => snapshotRef.current(), 10_000);
    const hide = () => snapshotRef.current();
    window.addEventListener("pagehide", hide);
    return () => {
      window.clearInterval(id);
      window.removeEventListener("pagehide", hide);
    };
  }, []);
  const pause = () => {
    recorder?.pause();
    tally();
    timing.current = null;
    setBreakAt(Date.now());
  };
  const resume = () => {
    if (breakAt == null) return;
    started.current += Date.now() - breakAt;
    timing.current = { no: mock.items[at]!.no, since: Date.now() };
    recorder?.resume();
    setBreakAt(null);
  };
  useEffect(() => {
    scroll.current?.scrollTo({ top: 0 });
    // 위 번호 줄도 지금 문항이 보이게
    document.querySelector(".mini-grid button.now")?.scrollIntoView({ inline: "center", block: "nearest" });
    recorder?.enter(mock.items[at]!.no);
    tally();
    timing.current = { no: mock.items[at]!.no, since: Date.now() };
  }, [at, mock, recorder]);

  const item = mock.items[at]!;
  const itemMarks = marks[item.no] ?? NO_MARKS;
  const wordsOf = (idx: number[]) => idx.map((i) => cleanWord(scroll.current?.querySelector(`[data-i="${i}"]`)?.textContent ?? "")).filter(Boolean);
  const putMarks = (m: Marks) => {
    setMarks((all) => ({ ...all, [item.no]: m }));
    recorder?.marks(item.no, wordsOf(m.hi), m.unk.map((u) => u.en));
  };
  const onHighlight = (hi: number[]) => putMarks({ ...itemMarks, hi });
  const onUnknown = (i: number, token: string, el: HTMLElement) => {
    const en = cleanWord(token);
    if (!en) return;
    if (itemMarks.unk.some((u) => u.i === i)) {
      putMarks({ ...itemMarks, unk: itemMarks.unk.filter((u) => u.i !== i) });
      setToast(`「${en}」 모르는 단어에서 뺐어요`);
      return;
    }
    const ko = meaningOf(en, set?.lessons ?? []);
    putMarks({ ...itemMarks, unk: [...itemMarks.unk, { i, en, ko }] });
    if (ko) {
      // 단어장에도 — 그 낱말이 든 문장과 같이
      const block = el.closest("p")?.textContent ?? "";
      const sentence = block.split(/(?<=[.!?”])\s+/).find((x) => x.includes(token)) ?? block;
      addVocab([{ en, ko, sentence: sentence.trim(), source: set?.lessons[0] ?? mock.id, kind: "word" }]);
    }
    setToast(ko ? `${en} — ${ko.split(" · ")[0]}` : `「${en}」 모르는 단어로 담았어요`, 2600);
  };
  const onTapUnknown = (i: number) => {
    const u = itemMarks.unk.find((x) => x.i === i);
    if (u) setToast(u.ko ? `${u.en} — ${u.ko.split(" · ")[0]}` : `「${u.en}」 뜻을 아직 못 찾았어요`, 2600);
  };
  const unanswered = mock.items.filter((it) => !answers[it.no]).length;
  const last = at === mock.items.length - 1;
  const isChecked = checked.includes(item.no);
  const set = item.lesson ? getSet(item.lesson) : null;
  // 끊어읽기·핵심어는 분석 레슨에 적힌 것(slashes · emphasis)을 그대로 지문 위에
  const lesson = set ? getPolicyLesson(set.lessons[0]!) : null;
  const overlay: Overlay = {
    slashes: showSlash ? (lesson?.sentences.flatMap((x) => x.slashes ?? []) ?? []) : [],
    keys: showKeys ? (lesson?.sentences.flatMap((x) => x.keys ?? x.emphasis ?? []) ?? []) : [],
  };
  return (
    <div className="stage-fill saved mini mini-exam">
      {toast ? <div className="mini-toast" role="status">{toast}</div> : null}
      <header className="mini-top">
        <button type="button" className="mini-quit" onClick={() => setConfirm("quit")}>그만</button>
        <span className="mini-clock-wrap">
          <span className={`mini-clock${left < 0 ? " over" : left < 120 ? " low" : ""}`} aria-label={left < 0 ? "초과한 시간" : "남은 시간"}>
            ⏱ {left < 0 ? `+${clock(-left)} 초과` : clock(left)}
          </span>
          <button type="button" className="mini-pause" onClick={pause} aria-label="일시정지">⏸</button>
        </span>
        <span className="mini-top-spacer" aria-hidden="true" />
      </header>
      <nav className="mini-grid" aria-label="문항">
        {mock.items.map((it, i) => {
          const mark = checked.includes(it.no) ? (answers[it.no] === it.answer ? " ok" : " ng") : "";
          return (
            <button key={it.no} type="button" className={`${i === at ? "now" : ""}${answers[it.no] ? " done" : ""}${mark}${peeked.includes(it.no) ? " peek" : ""}`} onClick={() => setAt(i)}>
              {it.no}
            </button>
          );
        })}
      </nav>
      <div className="saved-body-scroll" ref={scroll}>
        <ItemView
          item={item}
          picked={answers[item.no] ?? null}
          review={isChecked}
          marks={itemMarks}
          onHighlight={onHighlight}
          onUnknown={onUnknown}
          onTapUnknown={onTapUnknown}
          tools={{ pen, setPen, slash: showSlash, setSlash: setShowSlash, keys: showKeys, setKeys: setShowKeys, has: { slash: !!lesson?.sentences.some((x) => x.slashes?.length), keys: !!lesson?.keys_checked && !!lesson.sentences.some((x) => x.keys?.length || x.emphasis?.length) } }}
          overlay={overlay}
          onPick={isChecked ? undefined : (n) => {
            recorder?.pick(item.no, n);
            setAnswers({ ...answers, [item.no]: n });
          }}
        />
        {peeked.includes(item.no) && !isChecked ? (
          <p className="mini-peek-note">다정쌤 분석을 보고 고르는 문항이에요. 결과에 「분석 보고 고름」으로 따로 표시돼요.</p>
        ) : null}
        {isChecked ? (
          <CheckPanel
            item={item}
            peeked={peeked.includes(item.no)}
            unknown={itemMarks.unk}
            picked={answers[item.no] ?? null}
            recorder={recorder}
            onAnalyze={set ? () => onAnalyze(set, { answers, checked, peeked, marks, at, usedMs: Date.now() - started.current, times: { ...tally() }, no: item.no }) : null}
          />
        ) : (
          <>
          <button
            type="button"
            className="mini-check"
            disabled={!answers[item.no]}
            onClick={() => {
              recorder?.check(item.no, answers[item.no] === item.answer);
              setChecked([...checked, item.no]);
            }}
          >
            {answers[item.no] ? "정답 확인" : "답을 고르면 바로 정답을 확인할 수 있어요"}
          </button>
          {set && !answers[item.no] && !peeked.includes(item.no) ? (
            <button
              type="button"
              className="mini-analyze-first"
              onClick={() => {
                // 돌아와서 답을 고를 수 있다 — 대신 「분석 보고 고름」으로 따로 남긴다
                recorder?.peek(item.no);
                const next = [...peeked, item.no];
                setPeeked(next);
                onAnalyze(set, { answers, checked, peeked: next, marks, at, usedMs: Date.now() - started.current, times: { ...tally() }, no: item.no });
              }}
            >
              <b>답 고르지 않고 다정쌤 분석 보기 ›</b>
              <small>돌아와서 답을 고를 수 있어요 · 「분석 보고 고름」으로 따로 표시돼요</small>
            </button>
          ) : null}
          </>
        )}
      </div>
      <footer className="mini-foot">
        <button type="button" disabled={at === 0} onClick={() => setAt(at - 1)}>‹ 이전</button>
        <span>{at + 1} / {mock.items.length}</span>
        {last ? (
          <button type="button" className="primary" onClick={() => (unanswered ? setConfirm("submit") : submit(left < 0))}>다음 ›</button>
        ) : (
          <button type="button" onClick={() => setAt(at + 1)}>다음 ›</button>
        )}
      </footer>
      {breakAt != null ? (
        <div className="mini-confirm mini-break" role="dialog" aria-label="일시정지">
          <div>
            <p><b>일시정지 중</b><br />시계가 멈췄어요. 문제는 잠시 가려 둘게요.</p>
            <button type="button" className="primary" onClick={resume}>이어 풀기</button>
          </div>
        </div>
      ) : null}
      {confirm ? (
        <div className="mini-confirm" role="dialog">
          <div>
            <p>
              {confirm === "quit"
                ? "지금까지 푼 것은 남아요. 돌아오면 남은 시간부터 이어 풀 수 있어요."
                : unanswered
                  ? `아직 안 푼 문항이 ${unanswered}개 있어요. 그래도 제출할까요?`
                  : "제출할까요?"}
            </p>
            <button type="button" className="primary" onClick={() => {
              if (confirm === "quit") {
                recorder?.finish("quit", answers);
                snapshot();
                onQuit();
              } else submit(left < 0);
            }}>
              {confirm === "quit" ? "그만두기" : "제출하기"}
            </button>
            <button type="button" onClick={() => setConfirm(null)}>계속 풀기</button>
          </div>
        </div>
      ) : null}
    </div>
  );
}

/** 푸는 중에 「정답 확인」을 누른 문항 — 맞고 틀림, 해설, 분석하러 가기 */
function CheckPanel({
  item,
  peeked,
  unknown,
  picked,
  recorder,
  onAnalyze,
}: {
  item: MiniItem;
  peeked?: boolean;
  unknown?: Marks["unk"];
  picked: number | null;
  recorder: MiniRecorder | null;
  onAnalyze: (() => void) | null;
}) {
  const right = picked === item.answer;
  return (
    <div className={`mini-checked ${right ? "right" : "wrong"}`}>
      <p className="mini-verdict">
        {peeked ? <i className="mini-tag peek">분석 보고 고름</i> : null}
        {right ? "○ 맞았어요!" : `✕ 아쉽게도 틀렸어요. 정답은 ${NUM[item.answer - 1]}예요.`}
        {item.wrong_rate != null ? <small> · 전국 오답률 {item.wrong_rate}%</small> : null}
      </p>
      {onAnalyze ? (
        <button type="button" className="mini-analyze big" onClick={onAnalyze}>
          <b>다정쌤과 이 문제 분석하기 ›</b>
        </button>
      ) : (
        <p className="mini-no-lesson">이 문제는 아직 다정쌤 분석이 없어요. 아래 해설을 봐요.</p>
      )}
      {item.fix ? <p className="mini-fix">{item.fix}</p> : null}
      {unknown?.length ? <UnknownWords words={unknown} /> : null}
      {item.intent ? <p className="mini-intent">{item.intent}</p> : null}
      <Translation item={item} recorder={recorder} />
    </div>
  );
}

/** 「해석 보기」 — 지문 해석 + 선지 해석(있으면) */
function Translation({ item, recorder }: { item: MiniItem; recorder: MiniRecorder | null }) {
  if (!item.translation && !item.options_ko?.length) return null;
  return (
    <details onToggle={(e) => e.currentTarget.open && recorder?.opened(item.no, "translated")}>
      <summary>해석 보기{item.options_ko?.length ? " (지문 · 선지)" : ""}</summary>
      {item.translation ? <p className="mini-trans">{item.translation}</p> : null}
      {item.options_ko?.length ? (
        <ol className="mini-trans-options">
          {item.options_ko.map((ko, i) => (
            <li key={i} className={i + 1 === item.answer ? "answer" : undefined}>
              <b>{NUM[i]}</b> {ko}
            </li>
          ))}
        </ol>
      ) : null}
    </details>
  );
}

/** 두 번 두드려 담은 모르는 단어 — 뜻은 분석 레슨에서 (없으면 「분석에서 확인」) */
function UnknownWords({ words }: { words: { en: string; ko: string; no?: number }[] }) {
  return (
    <div className="mini-unknown">
      <p className="mini-unknown-title">모르는 단어 {words.length}개{words.some((w) => w.ko) ? " · 뜻이 있는 단어는 단어장에도 담았어요" : ""}</p>
      <ul>
        {words.map((w, k) => (
          <li key={`${w.no ?? ""}-${w.en}-${k}`}>
            <b>{w.en}</b>
            <span>{w.ko ? w.ko : <i>뜻은 분석·해석에서 확인해요</i>}</span>
            {w.no ? <small>{w.no}번</small> : null}
          </li>
        ))}
      </ul>
    </div>
  );
}

export function ItemView({
  item,
  picked,
  onPick,
  review,
  marks,
  onHighlight,
  onUnknown,
  onTapUnknown,
  tools,
  overlay = NO_OVERLAY,
}: {
  item: MiniItem;
  picked: number | null;
  onPick?: (n: number) => void;
  /** 결과 화면 — 정답·내 답을 칠한다 */
  review?: boolean;
  /** 푸는 중 — 지문에 형광펜·모르는 단어 표시 */
  marks?: Marks;
  onHighlight?: (hi: number[]) => void;
  onUnknown?: (i: number, token: string, el: HTMLElement) => void;
  onTapUnknown?: (i: number) => void;
  /** 펜 줄 — 보라펜(모르는 단어) · 형광펜 · 끊어읽기 · 핵심어. has: 이 문항의 레슨에 그 표시가 있나 */
  tools?: {
    pen: Pen; setPen: (p: Pen) => void;
    slash: boolean; setSlash: (v: boolean) => void;
    keys: boolean; setKeys: (v: boolean) => void;
    has: { slash: boolean; keys: boolean };
  };
  overlay?: Overlay;
}) {
  const numbersOnly = item.options.every((o) => !o);
  const ctx = marks ? { counter: { n: 0 }, marks, overlay } : null;
  const body = (
    <>
      {item.given ? <p className="mini-given">{passageNodes(item.given, item, ctx, "g")}</p> : null}
      {item.passage ? <p className="mini-passage">{passageNodes(item.passage, item, ctx, "p")}</p> : null}
      {item.paragraphs?.map((p, k) => (
        <p key={p.slice(0, 12)} className="mini-passage para">{passageNodes(p, item, ctx, `r${k}`)}</p>
      ))}
      {item.after ? <p className="mini-given after">{passageNodes(item.after, item, ctx, "a")}</p> : null}
    </>
  );
  return (
    <article className="mini-item">
      {item.group ? <p className="mini-group">{item.group}</p> : null}
      <p className="mini-q">
        <b>{item.no}.</b> {item.question}
        {item.points === 3 && !item.question.includes("3점") ? " [3점]" : null}
      </p>
      {marks && onHighlight && onUnknown && onTapUnknown && tools ? (
        <>
          <div className="mini-pens" role="toolbar" aria-label="펜">
            <button type="button" className={`pen-btn unk${tools.pen === "unk" ? " on" : ""}`} aria-pressed={tools.pen === "unk"} onClick={() => tools.setPen(tools.pen === "unk" ? "none" : "unk")}>
              <i /> 모르는 단어
            </button>
            <button type="button" className={`pen-btn hi${tools.pen === "hi" ? " on" : ""}`} aria-pressed={tools.pen === "hi"} onClick={() => tools.setPen(tools.pen === "hi" ? "none" : "hi")}>
              <i /> 형광펜
            </button>
            {tools.has.slash ? (
              <button type="button" className={`pen-btn slash${tools.slash ? " on" : ""}`} aria-pressed={tools.slash} onClick={() => tools.setSlash(!tools.slash)}>
                / 끊어읽기
              </button>
            ) : null}
            {tools.has.keys ? (
              <button type="button" className={`pen-btn keys${tools.keys ? " on" : ""}`} aria-pressed={tools.keys} onClick={() => tools.setKeys(!tools.keys)}>
                핵심어만 읽고 풀기
              </button>
            ) : null}
          </div>
          <p className="mini-mark-hint">
            {tools.pen === "unk" ? "모르는 낱말을 두드리면 밑줄이 그어지고 뜻이 떠요. 다시 두드리면 빼요" : tools.pen === "hi" ? "낱말을 두드리거나 끌어서 칠해요. 칠한 곳에서 시작하면 지워요" : "펜을 고르고 낱말을 두드려요. 밑줄 친 낱말은 그냥 두드리면 뜻이 떠요"}
          </p>
          <MarkArea pen={tools.pen} marks={marks} onHighlight={onHighlight} onUnknown={onUnknown} onTapUnknown={onTapUnknown}>{body}</MarkArea>
        </>
      ) : body}
      {item.foot ? <p className="mini-foot-note">{item.foot}</p> : null}
      <ol className={`mini-options${numbersOnly ? " numbers" : ""}`}>
        {item.options.map((o, i) => {
          const n = i + 1;
          const state = review
            ? n === item.answer
              ? " right"
              : n === picked
                ? " wrong"
                : ""
            : n === picked
              ? " picked"
              : "";
          return (
            <li key={n}>
              <button type="button" className={`mini-opt${state}`} disabled={!onPick} onClick={() => onPick?.(n)}>
                <b>{NUM[i]}</b>
                {o ? <span>{o}</span> : null}
              </button>
            </li>
          );
        })}
      </ol>
    </article>
  );
}

/** 밑줄(함축 의미), ①~⑤·(a)~(e) 뒤 낱말 밑줄(어법·어휘·지칭), 빈칸, 문장 넣기 자리 표시 */
export function passageNodes(text: string, item: MiniItem, ctx: { counter: { n: number }; marks: Marks; overlay?: Overlay } | null = null, key = ""): ReactNode[] {
  const out: ReactNode[] = [];
  const re = item.underline
    ? new RegExp(`(${item.underline.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}|_{4,}|\\([①②③④⑤]\\))`)
    : item.marked
      ? /((?:[①②③④⑤]|\([a-e]\))[^\s.,;:!?”]+|_{4,})/
      : /(_{4,}|\([①②③④⑤]\))/;
  text.split(re).forEach((part, i) => {
    if (!part) return;
    if (i % 2 === 0) out.push(...markWords(part, `${key}${i}`, ctx?.counter ?? { n: 0 }, ctx?.marks ?? null, ctx?.overlay));
    else if (/^_{4,}$/.test(part)) out.push(<span key={i} className="mini-blank" aria-label="빈칸" />);
    else if (/^\([①②③④⑤]\)$/.test(part)) out.push(<b key={i} className="mini-slot">{part}</b>);
    else if (item.marked) {
      const mark = part.startsWith("(") ? part.slice(0, 3) : part[0]!;
      out.push(<u key={i}><b>{mark}</b>{part.slice(mark.length)}</u>);
    }
    else out.push(<u key={i}>{part}</u>);
  });
  return out;
}

function MiniResult({
  mock,
  attempt,
  recorder,
  onBack,
  flowSet,
  onRetry,
  onAnalyze,
}: {
  mock: MiniMock;
  attempt: MiniAttempt;
  recorder: MiniRecorder | null;
  onBack: () => void;
  /** 코스 흐름 — 결과 바로 아래 「다정쌤과 분석하기」 (맞았어도 분석한다) */
  flowSet?: LessonSet | null;
  onRetry: () => void;
  onAnalyze: (set: LessonSet, no: number) => void;
}) {
  const s = useMemo(() => scoreOf(mock, attempt.answers), [mock, attempt]);
  const kinds = useMemo(() => byKind(mock, attempt.answers), [mock, attempt]);
  // 분석을 먼저 보고 고른 문항을 뺀 점수 — 그런 문항이 있을 때만
  const own = useMemo(() => attempt.peeked?.length
    ? scoreOf(mock, Object.fromEntries(Object.entries(attempt.answers).filter(([no]) => !attempt.peeked!.includes(Number(no)))))
    : null, [mock, attempt]);
  const [open, setOpen] = useState<number | null>(null);
  const avgTimes = useMemo(() => averageTimes(mock, attempt.times), [mock, attempt]);
  return (
    <div className="stage-fill saved mini">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="목록으로" aria-label="목록으로" onClick={onBack}>
          <BackIcon />
        </button>
      </header>
      <div className="saved-body-scroll">
        <p className="home-hello">{mock.title} · 결과</p>
        {flowSet ? (
          <button type="button" className="mini-analyze big flow" onClick={() => onAnalyze(flowSet, mock.items[0]!.no)}>
            <b>다정쌤과 이 문제 분석하기 ›</b>
          </button>
        ) : null}
        <div className="mini-score">
          <b>{s.score}</b>
          <span>/ {s.max}점</span>
        </div>
        {mock.id.startsWith("ten-") ? (
          <p className="mini-estimate">
            예상 시험점수 <b>약 {estimatedExamScore(mock, attempt.answers)}점</b> / 100
            <small>어려운 문제만 푼 결과라, 나머지 쉬운 문제는 잘 맞힌다고 보고 환산한 값이에요</small>
          </p>
        ) : null}
        <ul className="mini-facts">
          <li><b>{s.correct} / {s.total}</b><small>맞힌 문항</small></li>
          {own ? <li><b>{own.score}점</b><small>분석 안 보고 맞힌 점수 · 분석 보고 고른 문항 {attempt.peeked!.length}개</small></li> : null}
          <li><b>{clock(attempt.seconds)}</b><small>{attempt.timeUp ? `걸린 시간 · ${mock.minutes}분 초과` : `걸린 시간 (제한 ${mock.minutes}분)`}</small></li>
        </ul>
        {avgTimes ? (
          <ul className="mini-facts">
            <li><b>{dur(avgTimes.all)}</b><small>문항당 평균</small></li>
            {avgTimes.byPoints.map((g) => (
              <li key={g.points}><b>{dur(g.avg)}</b><small>{g.points}점 문항 평균 · {g.n}개</small></li>
            ))}
          </ul>
        ) : null}
        <div className="mini-kinds">
          {kinds.map((k) => (
            <span key={k.kind} className={k.right === k.total ? "all" : k.right === 0 ? "none" : ""}>
              {k.kind} {k.right}/{k.total}
            </span>
          ))}
        </div>

        {attempt.unknown?.length ? <UnknownWords words={attempt.unknown} /> : null}

        <h2 className="group-title">문항별</h2>
        <ul className="mini-review">
          {mock.items.map((it) => {
            const mine = attempt.answers[it.no] ?? null;
            const right = mine === it.answer;
            const set = it.lesson ? getSet(it.lesson) : null;
            const isOpen = open === it.no;
            return (
              <li key={it.no} className={right ? "right" : "wrong"}>
                <button type="button" className="mini-row" onClick={() => {
                  if (!isOpen) recorder?.opened(it.no, "reviewed");
                  setOpen(isOpen ? null : it.no);
                }}>
                  <span className="mini-mark">{right ? "○" : "✕"}</span>
                  <span className="mini-row-text">
                    <b>{it.no}번 · {it.kind}{set ? <i className="mini-tag lesson">다정쌤 분석</i> : null}{attempt.checked?.includes(it.no) ? <i className="mini-tag">바로 확인</i> : null}{attempt.peeked?.includes(it.no) ? <i className="mini-tag peek">분석 보고 고름</i> : null}</b>
                    <small>
                      {mine ? `내 답 ${NUM[mine - 1]}` : "안 풂"} · 정답 {NUM[it.answer - 1]} · {it.points}점
                      {attempt.times?.[it.no] ? ` · ${dur(attempt.times[it.no]!)}` : ""}
                      {it.wrong_rate != null ? ` · 전국 오답률 ${it.wrong_rate}%` : ""}
                    </small>
                  </span>
                  <span className="mini-chev">{isOpen ? "▴" : "▾"}</span>
                </button>
                {isOpen ? (
                  <div className="mini-explain">
                    {set ? (
                      <button type="button" className="mini-analyze big" onClick={() => onAnalyze(set, it.no)}>
                        <b>다정쌤과 이 문제 분석하기 ›</b>
                      </button>
                    ) : (
                      <p className="mini-no-lesson">이 문제는 아직 다정쌤 분석이 없어요. 아래 해설을 봐요.</p>
                    )}
                    {it.fix ? <p className="mini-fix">{it.fix}</p> : null}
                    {it.intent ? <p className="mini-intent">{it.intent}</p> : null}
                    <details>
                      <summary>문제 다시 보기</summary>
                      <ItemView item={it} picked={mine} review />
                    </details>
                    <Translation item={it} recorder={recorder} />
                  </div>
                ) : null}
              </li>
            );
          })}
        </ul>
        <button type="button" className="mini-start" onClick={onRetry}>
          다시 풀기
        </button>
      </div>
    </div>
  );
}

/** 걸린 시간 — 「1분 12초」 · 「48초」 */
function dur(seconds: number): string {
  const s = Math.round(seconds);
  return s >= 60 ? `${Math.floor(s / 60)}분${s % 60 ? ` ${s % 60}초` : ""}` : `${s}초`;
}

function BackIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 6l-6 6 6 6" />
    </svg>
  );
}
