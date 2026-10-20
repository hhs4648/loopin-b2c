/**
 * 어느 문제를 끝냈는지 · 몇 번 풀었고 몇 번 맞혔는지.
 *
 * **이 브라우저에만 남는다.** 서버(`sessions`)에도 수업 기록이 남지만 그건
 * 난이도를 재려고 모으는 것이고, 목록에 「완료」를 칠하는 데는 지금 당장
 * 손에 있는 값이 필요하다. 계정을 붙일 때 서버 기록으로 갈아타면 된다.
 *
 * 저장이 안 되는 브라우저(사파리 프라이빗 등)에서는 그냥 완료 표시가 안 뜬다.
 * 수업은 그대로 돌아간다.
 */

const KEY = "dajung.done";
const RUNS_KEY = "dajung.runs";

/** 세트 id → 마지막으로 받은 결과 (이해·오류후이해·취약·설명제공) */
export type Progress = Record<string, string>;

/** 한 번 시작한 수업 — correct는 그 회차에 문제(보기)를 처음 고른 것이 맞았는지, 아직 안 골랐으면 null */
export type Run = { started_at: string; last_at: string; done: boolean; correct: boolean | null };
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

/** 그 세트의 지금 회차 (마지막으로 시작한 것) — 지금 하는 세트가 아니면 null */
function currentRun(runs: Runs): Run | null {
  if (!runs.current) return null;
  return runs.sets[runs.current]?.at(-1) ?? null;
}

/** 수업을 시작했다 — 새 회차를 연다. 목록에 「진행 중」이 뜨고 맨 위로 온다 */
export function startRun(setId: string, now = new Date()): void {
  const runs = loadRuns();
  const at = now.toISOString();
  runs.sets[setId] = [...(runs.sets[setId] ?? []), { started_at: at, last_at: at, done: false, correct: null }];
  runs.current = setId;
  write(RUNS_KEY, runs);
}

/** 이번 회차에서 문제(보기)를 골랐다 — 처음 고른 것만 맞힘/틀림으로 센다 */
export function noteExamAnswer(correct: boolean, now = new Date()): void {
  const runs = loadRuns();
  const run = currentRun(runs);
  if (!run) return;
  run.last_at = now.toISOString();
  if (run.correct == null) run.correct = correct;
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
  /** 보기를 고른 회차 수 · 그중 처음 고른 게 맞은 수 */
  answered: number;
  correct: number;
  /** 마지막으로 만진 시각 (없으면 null) — 최근 것이 위로 */
  lastAt: string | null;
};

export function setStatuses(progress: Progress = loadProgress()): Record<string, SetStatus> {
  const runs = loadRuns();
  const out: Record<string, SetStatus> = {};
  const ids = new Set([...Object.keys(progress), ...Object.keys(runs.sets)]);
  for (const id of ids) {
    const list = runs.sets[id] ?? [];
    const last = list.at(-1);
    const doneCount = list.filter((r) => r.done).length || (isDone(progress, id) ? 1 : 0);
    const answered = list.filter((r) => r.correct != null);
    out[id] = {
      state: last && !last.done ? "doing" : doneCount > 0 ? "done" : "new",
      doneCount,
      answered: answered.length,
      correct: answered.filter((r) => r.correct).length,
      lastAt: last?.last_at ?? null,
    };
  }
  return out;
}

/** 카드 한 줄 — 「완료 · 3번 봄 · 3번 중 2번 맞힘」 */
export function statusLine(s: SetStatus | undefined): string | null {
  if (!s || s.state === "new") return null;
  const parts: string[] = [];
  if (s.doneCount > 0) parts.push(`${s.doneCount}번 봄`);
  if (s.answered === 1) parts.push(s.correct ? "맞힘" : "틀림");
  else if (s.answered > 1) parts.push(`${s.answered}번 중 ${s.correct}번 맞힘`);
  return parts.length ? parts.join(" · ") : null;
}
