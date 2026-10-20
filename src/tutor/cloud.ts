/**
 * 진행 기록 · 내 노트 · 단어장을 서버(`learner_state`)에도 둔다.
 *
 * **localStorage가 그대로 원본이다.** 화면은 지금까지처럼 동기로 읽고(`loadProgress()` 등),
 * 서버는 그 값의 사본이다:
 * - 쓸 때 — 로컬에 쓴 뒤 같은 값을 잠깐 모았다가(0.8초) 한 행으로 upsert한다. 값이 늘 전체
 *   상태라서 한 번 못 보내도 다음 쓰기가 메운다.
 * - 열 때 — 서버 값을 받아 로컬과 **합친다**(`MERGES`). 합친 값이 로컬과 다르면 화면을 다시
 *   그리게 true를 돌려주고, 서버와 다르면 서버에 올린다.
 *
 * 합치기는 전부 **합집합**이다. 다른 기기에서 지운 별표가 이 기기에서 되살아날 수 있지만,
 * 한 달 공개 동안 "사라졌다"가 "되살아났다"보다 훨씬 나쁘다.
 *
 * 환경변수(`VITE_SUPABASE_*`)가 없으면 아무것도 하지 않는다 — 지금까지처럼 브라우저만으로 돈다.
 * 익명 학습자 기준이라 **기기를 바꾸면 아직 따라오지 않는다** — 계정(이메일)을 붙이는 게 다음 일이다.
 */

import { ensureLearner, supabaseClient } from "./records";

type Merge = (local: unknown, server: unknown) => unknown;

const isObj = (v: unknown): v is Record<string, unknown> => !!v && typeof v === "object" && !Array.isArray(v);
const asList = <T>(v: unknown): T[] => (Array.isArray(v) ? (v as T[]) : []);

/** 두 목록을 id로 합친다 — 로컬 것이 먼저, 서버에만 있는 것은 뒤에 (저장 순서대로 보이게 시각으로 정렬) */
function unionBy<T>(local: unknown, server: unknown, idOf: (x: T) => string, at: (x: T) => string): T[] {
  const seen = new Set<string>();
  const out: T[] = [];
  for (const x of [...asList<T>(local), ...asList<T>(server)]) {
    const id = idOf(x);
    if (seen.has(id)) continue;
    seen.add(id);
    out.push(x);
  }
  return out.sort((a, b) => at(a).localeCompare(at(b)));
}

type Run = { started_at: string };
type Runs = { current: string | null; sets: Record<string, Run[]> };

/** 어느 키를 어떻게 합치나 — 여기 적힌 키만 서버로 간다 */
export const MERGES: Record<string, Merge> = {
  // 세트 → 마지막 결과. 로컬이 이긴다 (지금 이 기기에서 방금 푼 값이 더 새롭다)
  "dajung.done": (l, s) => ({ ...(isObj(s) ? s : {}), ...(isObj(l) ? l : {}) }),
  // 세트마다 회차 목록 — 시작 시각으로 합친다
  "dajung.runs": (l, s) => {
    const L = isObj(l) ? (l as Partial<Runs>) : {};
    const S = isObj(s) ? (s as Partial<Runs>) : {};
    const sets: Record<string, Run[]> = {};
    for (const id of new Set([...Object.keys(L.sets ?? {}), ...Object.keys(S.sets ?? {})])) {
      sets[id] = unionBy<Run>(L.sets?.[id], S.sets?.[id], (r) => r.started_at, (r) => r.started_at);
    }
    return { current: L.current ?? S.current ?? null, sets };
  },
  "loopin.notes.v1": (l, s) =>
    unionBy<{ lessonId: string; key: string; savedAt: string }>(l, s, (n) => `${n.lessonId}#${n.key}`, (n) => n.savedAt),
  "loopin.vocab.v1": (l, s) =>
    unionBy<{ en: string; savedAt: string }>(l, s, (w) => w.en.trim().toLowerCase(), (w) => w.savedAt),
};

export const SYNCED_KEYS = Object.keys(MERGES);

/*
  테스트(vitest)는 `.env.local`도 읽어서 Supabase 키가 보일 수 있다. 거기서 네트워크를 타면
  안 되므로 테스트에서는 꺼 둔다.
*/
function enabled(): boolean {
  return !import.meta.env.VITEST && typeof window !== "undefined" && supabaseClient() != null;
}

export const cloudEnabled = enabled;

function readLocal(key: string): unknown {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as unknown) : null;
  } catch {
    return null;
  }
}

function writeLocal(key: string, value: unknown): void {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* 못 써도 서버 값은 이번 화면에 못 쓸 뿐 */
  }
}

const timers = new Map<string, number>();
const DEBOUNCE_MS = 800;

/** 로컬에 쓴 직후 부른다 — 잠깐 모았다가 서버에 올린다 */
export function pushKey(key: string): void {
  if (!(key in MERGES) || !enabled()) return;
  const old = timers.get(key);
  if (old != null) window.clearTimeout(old);
  timers.set(key, window.setTimeout(() => void flush(key), DEBOUNCE_MS));
}

async function flush(key: string): Promise<void> {
  timers.delete(key);
  const db = supabaseClient();
  const learner = await ensureLearner();
  if (!db || !learner) return;
  const value = readLocal(key);
  if (value == null) return;
  const { error } = await db
    .from("learner_state")
    .upsert({ learner_id: learner, key, value, updated_at: new Date().toISOString() });
  if (error) console.warn("[cloud] 저장 실패", key, error.message);
}

/** 탭을 닫거나 숨길 때 모아 둔 것을 바로 보낸다 */
function flushAll(): void {
  for (const key of [...timers.keys()]) {
    window.clearTimeout(timers.get(key));
    void flush(key);
  }
}

if (typeof window !== "undefined" && typeof window.addEventListener === "function") {
  window.addEventListener("pagehide", flushAll);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") flushAll();
  });
}

/**
 * 앱을 열 때 한 번 — 서버 값을 받아 로컬과 합친다.
 * 로컬이 바뀌었으면 true (화면을 다시 그릴 것).
 */
export function pullAll(): Promise<boolean> {
  // React StrictMode는 개발에서 effect를 두 번 돌린다 — 한 번만 받는다
  return (pullInFlight ??= pull());
}

let pullInFlight: Promise<boolean> | null = null;

async function pull(): Promise<boolean> {
  if (!enabled()) return false;
  const db = supabaseClient();
  const learner = await ensureLearner();
  if (!db || !learner) return false;
  const { data, error } = await db.from("learner_state").select("key, value").eq("learner_id", learner);
  if (error) {
    console.warn("[cloud] 불러오기 실패", error.message);
    return false;
  }
  const server = new Map((data ?? []).map((r) => [r.key as string, r.value as unknown]));
  let changed = false;
  for (const key of SYNCED_KEYS) {
    const local = readLocal(key);
    const remote = server.get(key) ?? null;
    if (local == null && remote == null) continue;
    const merged = MERGES[key]!(local, remote);
    const mergedJson = JSON.stringify(merged);
    if (mergedJson !== JSON.stringify(local)) {
      writeLocal(key, merged);
      changed = true;
    }
    if (mergedJson !== JSON.stringify(remote)) void flush(key);
  }
  return changed;
}
