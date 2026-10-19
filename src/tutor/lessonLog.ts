/**
 * 수업 응답 기록 — 공유 링크(아티팩트)에서 학생이 수업을 하면 세션 이벤트(고른 보기·찾기·해석 입력·건너뛰기…)를
 * 아티팩트 db `lessonlogs/<학생 id>`에 쌓는다. 나중에 Claude(ArtifactData)나 선생님이 읽어 분석한다.
 *
 * 아티팩트 밖(개발 서버·테스트)이거나 쓰기 권한이 없으면(조직 밖·보기 전용) 아무것도 안 한다 — 브라우저 기록(appendEvents)은 그대로.
 * 실명은 올리지 않는다. 미니 모의고사에서 학생이 직접 적은 이름이 있으면 그것만 같이 둔다.
 */
import type { LearningEvent } from "./policy/student-state";
import { canRecord, getDb, getUser } from "./miniLog";

type Snap = { exists: boolean; data(): Record<string, unknown> | undefined };
type DocRef = { get(): Promise<Snap>; set(d: Record<string, unknown>): Promise<void> };

export type LessonLogDoc = {
  name?: string;
  updated_at: string;
  /** 접속(탭)마다 하나 — 키는 시작 시각 */
  sessions: Record<string, { started_at: string; events: LearningEvent[] }>;
  /**
   * 문제(레슨)별 걸린 시간 — 처음·마지막 이벤트 시각, 실제로 한 시간(이벤트 사이가 5분 넘게 비면 쉰 것으로 빼고 셈),
   * 분으로도. 같은 문제를 다시 하면 이어서 더한다
   */
  lessons?: Record<string, { first_at: string; last_at: string; seconds: number; minutes: number; events: number }>;
};

const IDLE_MS = 5 * 60 * 1000;

const MAX_PER_SESSION = 4000;
const session = `${new Date().toISOString().replace(/[^0-9]/g, "").slice(0, 14)}-${Math.random().toString(36).slice(2, 6)}`;
const startedAt = new Date().toISOString();
let ref: Promise<{ doc: DocRef; base: LessonLogDoc } | null> | null = null;
let buffer: LearningEvent[] = [];
let timer: number | null = null;
let queue: Promise<void> = Promise.resolve();

function miniName(): string | undefined {
  try {
    return window.localStorage.getItem("loopin.mini.name")?.trim() || undefined;
  } catch {
    return undefined;
  }
}

function open() {
  ref ??= (async () => {
    if (!(await canRecord())) return null;
    const [db, user] = await Promise.all([getDb(), getUser()]);
    const id = await user?.id();
    if (!db || !id) return null;
    const doc = db.doc(`lessonlogs/${id}`) as unknown as DocRef;
    let base: LessonLogDoc = { updated_at: startedAt, sessions: {} };
    try {
      const snap = await doc.get();
      if (snap.exists) {
        const d = snap.data() as unknown as LessonLogDoc;
        base = { ...d, sessions: d.sessions ?? {} };
      }
    } catch {
      /* 처음이면 빈 문서 */
    }
    return { doc, base };
  })();
  return ref;
}

function flush() {
  if (timer != null) window.clearTimeout(timer);
  timer = null;
  if (!buffer.length) return;
  const batch = buffer;
  buffer = [];
  queue = queue.then(async () => {
    const r = await open();
    if (!r) return;
    const s = (r.base.sessions[session] ??= { started_at: startedAt, events: [] });
    s.events = [...s.events, ...batch].slice(-MAX_PER_SESSION);
    const lessons = (r.base.lessons ??= {});
    for (const e of batch) {
      const t = Date.parse(e.at);
      const l = lessons[e.lessonId];
      if (!l) {
        lessons[e.lessonId] = { first_at: e.at, last_at: e.at, seconds: 0, minutes: 0, events: 1 };
        continue;
      }
      const gap = t - Date.parse(l.last_at);
      if (gap > 0 && gap <= IDLE_MS) l.seconds = Math.round(l.seconds + gap / 1000);
      if (gap > 0) l.last_at = e.at;
      l.minutes = Math.round((l.seconds / 60) * 10) / 10;
      l.events++;
    }
    r.base.updated_at = new Date().toISOString();
    const name = miniName();
    if (name) r.base.name = name;
    try {
      await r.doc.set(JSON.parse(JSON.stringify(r.base)) as Record<string, unknown>);
    } catch {
      /* 기록이 안 돼도 수업은 그대로 */
    }
  });
}

/** 세션이 이벤트를 낼 때마다 — 모아 두었다가 잠깐 뒤(또는 화면을 떠날 때) 한 번에 저장 */
export function recordLessonEvents(events: LearningEvent[]): void {
  if (!events.length || typeof window === "undefined" || !(window as unknown as { claude?: unknown }).claude) return;
  buffer.push(...events);
  void open();
  if (timer == null) timer = window.setTimeout(flush, 2000);
}

if (typeof window !== "undefined") {
  window.addEventListener("pagehide", flush);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") flush();
  });
}

/**
 * db에 못 쓰는 학생(공개 링크·로그인 안 함)이 선생님께 보낼 기록 — 이 브라우저에 남은 수업 이벤트 + 미니 모의고사 결과.
 * 문제별 걸린 시간(분)도 같이 계산해 붙인다
 */
export function exportLocalLog(): string {
  const read = (k: string) => {
    try {
      return JSON.parse(window.localStorage.getItem(k) ?? "null") as unknown;
    } catch {
      return null;
    }
  };
  const events = (read("loopin.policy.events.v1") as LearningEvent[] | null) ?? [];
  const lessons: Record<string, { first_at: string; last_at: string; minutes: number; events: number }> = {};
  const secs: Record<string, number> = {};
  for (const e of events) {
    const l = lessons[e.lessonId];
    if (!l) {
      lessons[e.lessonId] = { first_at: e.at, last_at: e.at, minutes: 0, events: 1 };
      secs[e.lessonId] = 0;
      continue;
    }
    const gap = Date.parse(e.at) - Date.parse(l.last_at);
    if (gap > 0 && gap <= IDLE_MS) secs[e.lessonId]! += gap / 1000;
    if (gap > 0) l.last_at = e.at;
    l.minutes = Math.round((secs[e.lessonId]! / 60) * 10) / 10;
    l.events++;
  }
  return JSON.stringify({ kind: "loopin-log", at: new Date().toISOString(), name: miniName(), lessons, mini: read("loopin.mini.v1"), events });
}
