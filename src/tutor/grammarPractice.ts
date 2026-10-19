/**
 * 연습할 문법 — 수업 중 「이 문법을 나중에 좀 더 연습할까요?」에서 「네」를 누른 것.
 * 보충학습실에서 그 문법의 drill(10문제, 처음엔 객관식 → 나중엔 주관식 섞어서)을 푼다.
 * 담는 것은 문법 묶음(「nor / so」처럼 세트 여럿) 또는 drill 하나의 id다 (`grammarDrills.ts`의 groupOf).
 *
 * 단어장(`vocab.ts`)·노트(`notes.ts`)와 같은 방식: 지금은 이 브라우저에만 남는다.
 */

export type GrammarPracticeEntry = {
  /** 묶음 id 또는 drill id */
  id: string;
  /** 어느 수업에서 담았나 */
  lessonId: string;
  savedAt: string;
};

/** drill(세트)마다 — 몇 번 풀었나, 마지막 점수 */
export type DrillScore = { tries: number; right: number; total: number; at: string };

/** 주관식에 학생이 쓴 답 — 그대로 남긴다 (나중에 연구용) */
export type DrillInput = { drill: string; item: number; typed: string; ok: boolean; at: string };

const KEY = "loopin.grammar-practice.v1";
const SCORE_KEY = "loopin.grammar-drill-scores.v1";
const INPUT_KEY = "loopin.grammar-drill-inputs.v1";

function read<T>(key: string, empty: T): T {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : empty;
  } catch {
    return empty;
  }
}

function write(key: string, value: unknown): void {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* 못 저장해도 수업은 그대로 */
  }
}

export function loadGrammarPractice(): GrammarPracticeEntry[] {
  const parsed = read<GrammarPracticeEntry[]>(KEY, []);
  return Array.isArray(parsed) ? parsed : [];
}

/** 담는다 — 이미 있으면 그대로 */
export function addGrammarPractice(id: string, lessonId: string, now = Date.now()): void {
  const entries = loadGrammarPractice();
  if (entries.some((x) => x.id === id)) return;
  write(KEY, [...entries, { id, lessonId, savedAt: new Date(now).toISOString() }]);
}

export function removeGrammarPractice(id: string): GrammarPracticeEntry[] {
  const next = loadGrammarPractice().filter((x) => x.id !== id);
  write(KEY, next);
  return next;
}

export function loadDrillScores(): Record<string, DrillScore> {
  return read<Record<string, DrillScore>>(SCORE_KEY, {});
}

/** drill을 다 풀었다 — 점수를 남긴다 */
export function recordGrammarDrill(id: string, right: number, total: number, now = Date.now()): void {
  const all = loadDrillScores();
  all[id] = { tries: (all[id]?.tries ?? 0) + 1, right, total, at: new Date(now).toISOString() };
  write(SCORE_KEY, all);
}

/** 주관식 답을 남긴다 (최근 1000개) */
export function recordDrillInput(drill: string, item: number, typed: string, ok: boolean, now = Date.now()): void {
  const all = read<DrillInput[]>(INPUT_KEY, []);
  write(INPUT_KEY, [{ drill, item, typed, ok, at: new Date(now).toISOString() }, ...(Array.isArray(all) ? all : [])].slice(0, 1000));
}
