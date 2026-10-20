/**
 * 어느 문제를 끝냈는지 · 몇 번 풀었고 몇 번 맞혔는지.
 *
 * **이 브라우저가 원본이고 서버(`learner_state`)는 사본이다.** 목록에 「완료」를
 * 칠하는 데는 지금 당장 손에 있는 값이 필요해서 동기로 읽고, 쓸 때마다 같은 값을
 * `cloud.ts`가 서버에 올린다. 앱을 열 때 서버 값과 합친다.
 *
 * 저장이 안 되는 브라우저(사파리 프라이빗 등)에서는 그냥 완료 표시가 안 뜬다.
 * 수업은 그대로 돌아간다.
 */

import { pushKey } from "./cloud";

const KEY = "dajung.done";
const RUNS_KEY = "dajung.runs";
const RESUME_KEY = "dajung.resume";

/** 세트 id → 마지막으로 받은 결과 (이해·오류후이해·취약·설명제공) */
export type Progress = Record<string, string>;

/**
 * 한 번 시작한 수업. 맞힘/틀림은 **분석한 뒤 고른 보기**가 기준이다 (2026-10-20 선생님: 이 앱은 분석하는 앱).
 * - analyzed — 분석을 마치고 문제에서 처음 고른 보기가 맞았는지 (같은 회차에 다시 고른 건 세지 않는다)
 * - correct — 분석 전 「바로 풀기」에서 처음 고른 것. 분석 없이 끝냈을 때만 대신 쓴다
 * 아직 안 골랐으면 null
 * - seconds — 이 회차에 수업 화면에 있던 시간 (수업 머리글 시계와 같은 값)
 */
export type Run = {
  started_at: string;
  last_at: string;
  done: boolean;
  correct: boolean | null;
  analyzed?: boolean | null;
  seconds?: number;
  /** 이 회차에 연 지문 — 공유 링크·개발용 ?set= 처럼 회차 없이 연 수업의 기록이 엉뚱한 회차에 붙지 않게 */
  lesson_id?: string;
};

/** 그 회차의 맞힘/틀림 — 분석 뒤 고른 게 있으면 그것, 없으면 바로 풀기 */
function verdict(run: Run): boolean | null {
  return run.analyzed ?? run.correct;
}
type Runs = { current: string | null; sets: Record<string, Run[]> };

function read<T>(key: string, empty: T): T {
  try {
    const raw = window.localStorage.getItem(key);
    const parsed: unknown = raw ? JSON.parse(raw) : null;
    if (!parsed || typeof parsed !== "object") return empty;
    return parsed as T;
  } catch {
    return empty;
  }
}

function write(key: string, value: unknown): void {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
    pushKey(key);
  } catch {
    /* 저장 못 해도 수업은 그대로 */
  }
}

export function loadProgress(): Progress {
  return read<Progress>(KEY, {});
}

function loadRuns(): Runs {
  const r = read<Runs>(RUNS_KEY, { current: null, sets: {} });
  return { current: r.current ?? null, sets: r.sets ?? {} };
}

/** 그 세트의 지금 회차 (마지막으로 시작한 것). lessonId를 주면 그 지문을 연 회차일 때만 */
function currentRun(runs: Runs, lessonId?: string): Run | null {
  if (!runs.current) return null;
  const run = runs.sets[runs.current]?.at(-1) ?? null;
  if (run && lessonId && run.lesson_id && run.lesson_id !== lessonId) return null;
  return run;
}

/** 수업을 시작했다 — 새 회차를 연다. 목록에 「진행 중」이 뜨고 맨 위로 온다 */
export function startRun(setId: string, lessonId?: string, now = new Date()): void {
  const runs = loadRuns();
  const at = now.toISOString();
  const run: Run = { started_at: at, last_at: at, done: false, correct: null, analyzed: null, ...(lessonId ? { lesson_id: lessonId } : {}) };
  runs.sets[setId] = [...(runs.sets[setId] ?? []), run];
  runs.current = setId;
  write(RUNS_KEY, runs);
}

/**
 * **「봤다」(완료)의 기준 — 답을 제출했거나 마지막 문장까지 왔으면** (2026-10-20 선생님).
 * 답을 안 냈어도, 중간 문장을 건너뛰었어도 마지막 문장까지 눌러 왔으면 본 것이다. 뒤의 복습·단어 체크는 안 해도 된다
 */
function markSeen(runs: Runs, run: Run, now: Date): void {
  run.done = true;
  run.last_at = now.toISOString();
  const progress = loadProgress();
  if (runs.current && !isDone(progress, runs.current)) write(KEY, { ...progress, [runs.current]: "봄" });
}

/**
 * 이번 회차에서 문제(보기)를 골라 제출했다 — 바로 풀기든 분석 뒤든 제출하면 본 것이다.
 * when — "first"는 분석 전 바로 풀기, "final"은 분석을 마치고 고른 것. 둘 다 그 단계에서 처음 제출한 것만 센다
 */
export function noteExamAnswer(correct: boolean, when: "first" | "final" = "final", lessonId?: string, now = new Date()): void {
  const runs = loadRuns();
  const run = currentRun(runs, lessonId);
  if (!run || !runs.current) return;
  if (when === "first") run.correct ??= correct;
  else run.analyzed ??= correct;
  markSeen(runs, run, now);
  write(RUNS_KEY, runs);
}

/** 마지막 문장까지 왔다 — 답을 안 냈어도 본 것이다 */
export function noteReachedEnd(setId: string, now = new Date()): void {
  const runs = loadRuns();
  const run = runs.current === setId ? currentRun(runs) : null;
  if (!run || run.done) return;
  markSeen(runs, run, now);
  write(RUNS_KEY, runs);
}

/* ── 이어 하기 ─────────────────────────────────────────────────────
   중간에 나가면 멈춘 자리부터 (2026-10-20 선생님). 자리는 세트마다 하나 — 수업이 끝나면(마지막 화면) 지운다.
   이 기기에만 둔다 (서버로는 안 보낸다) */

type Resume = { lesson_id: string; at: string; snap: unknown };

function loadResumes(): Record<string, Resume> {
  return read<Record<string, Resume>>(RESUME_KEY, {});
}

export function saveResume(setId: string, lessonId: string, snap: unknown, now = new Date()): void {
  try {
    window.localStorage.setItem(RESUME_KEY, JSON.stringify({ ...loadResumes(), [setId]: { lesson_id: lessonId, at: now.toISOString(), snap } }));
  } catch {
    /* 저장 못 하면 다음에 처음부터 */
  }
}

/** 이 세트를 멈춘 자리 — 그 지문의 것일 때만 */
export function loadResume(setId: string, lessonId: string): unknown | null {
  const r = loadResumes()[setId];
  return r && r.lesson_id === lessonId ? r.snap : null;
}

export function clearResume(setId: string): void {
  const all = loadResumes();
  if (!(setId in all)) return;
  delete all[setId];
  try {
    window.localStorage.setItem(RESUME_KEY, JSON.stringify(all));
  } catch {
    /* 무시 */
  }
}

/**
 * 멈춘 자리로 돌아왔다 — 새 회차를 열지 않고 그 세트의 마지막 회차를 잇는다. 그 회차에 이미 공부한 시간(초)을 돌려준다.
 * 회차 기록이 없으면(다른 기기에서 지웠다 등) 새로 연다
 */
export function resumeRun(setId: string, lessonId?: string, now = new Date()): number {
  const runs = loadRuns();
  const run = runs.sets[setId]?.at(-1);
  if (!run) {
    startRun(setId, lessonId, now);
    return 0;
  }
  runs.current = setId;
  run.last_at = now.toISOString();
  write(RUNS_KEY, runs);
  return run.seconds ?? 0;
}

/** 이번 회차에 공부한 시간(초) — 수업 화면 시계 값을 그대로 받는다. 줄지 않는다 */
export function noteStudyTime(setId: string, seconds: number): void {
  const runs = loadRuns();
  const run = runs.current === setId ? currentRun(runs) : null;
  if (!run || seconds <= (run.seconds ?? 0)) return;
  run.seconds = Math.round(seconds);
  write(RUNS_KEY, runs);
}

/**
 * 끝낸 것으로 표시한다.
 *
 * 다시 풀면 **마지막 결과로 덮어쓴다** — 「취약」이었다가 「이해」가 되면 그게
 * 지금의 실력이다. 완료 여부 자체는 한 번 켜지면 꺼지지 않는다.
 */
export function markDone(setId: string, result: string, now = new Date()): void {
  write(KEY, { ...loadProgress(), [setId]: result });
  const runs = loadRuns();
  const run = runs.current === setId ? currentRun(runs) : null;
  if (run) {
    run.done = true;
    run.last_at = now.toISOString();
    write(RUNS_KEY, runs);
  }
}

export function isDone(progress: Progress, setId: string): boolean {
  return setId in progress;
}

/** 목록 카드에 띄울 것 */
export type SetStatus = {
  state: "new" | "doing" | "done";
  /** 끝까지 본 횟수 */
  doneCount: number;
  /** 보기를 고른 회차 수 · 그중 맞은 수 (분석 뒤 고른 것 기준) */
  answered: number;
  correct: number;
  /** 가장 최근에 답을 낸 회차가 맞았나 (낸 적 없으면 null) — 목록에는 이것만 보인다 */
  latest: boolean | null;
  /** 멈춘 자리가 있다 — 누르면 이어서 */
  resumable: boolean;
  /** 마지막으로 만진 시각 (없으면 null) — 최근 것이 위로 */
  lastAt: string | null;
  /** 모든 회차에 공부한 시간을 더한 것(초) */
  seconds: number;
};

export function setStatuses(progress: Progress = loadProgress()): Record<string, SetStatus> {
  const runs = loadRuns();
  const resumes = loadResumes();
  const out: Record<string, SetStatus> = {};
  const ids = new Set([...Object.keys(progress), ...Object.keys(runs.sets)]);
  for (const id of ids) {
    const list = runs.sets[id] ?? [];
    const last = list.at(-1);
    const doneCount = list.filter((r) => r.done).length || (isDone(progress, id) ? 1 : 0);
    const answered = list.map(verdict).filter((v) => v != null);
    out[id] = {
      state: last && !last.done ? "doing" : doneCount > 0 ? "done" : "new",
      doneCount,
      answered: answered.length,
      correct: answered.filter(Boolean).length,
      latest: answered.at(-1) ?? null,
      resumable: id in resumes,
      lastAt: last?.last_at ?? null,
      seconds: list.reduce((n, r) => n + (r.seconds ?? 0), 0),
    };
  }
  return out;
}

/** 공부 시간 — 「10m」, 한 시간이 넘으면 「1h 5m」, 1분이 안 되면 「1m 미만」 */
export function studyTime(seconds: number): string | null {
  if (seconds <= 0) return null;
  const m = Math.floor(seconds / 60);
  if (m < 1) return "1m 미만";
  return m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m}m`;
}

/**
 * 카드 한 줄 — 「3번 봄 · 최근 정답 · ⏱ 25m」.
 * 「3번 중 1번 맞힘」은 기분이 상한다 — 수험생은 같은 지문을 여러 번 보는 게 당연하니 **본 횟수와 최근 정답 여부만** (2026-10-20 선생님)
 */
export function statusLine(s: SetStatus | undefined): string | null {
  if (!s || s.state === "new") return null;
  const parts: string[] = [];
  if (s.doneCount > 0) parts.push(`${s.doneCount}번 봄`);
  if (s.latest != null) parts.push(s.latest ? "최근 정답" : "최근 오답");
  const time = studyTime(s.seconds);
  if (time) parts.push(`⏱ ${time}`);
  return parts.length ? parts.join(" · ") : null;
}
