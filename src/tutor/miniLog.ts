import { scoreOf, type MiniMock } from "./mini";

/**
 * 미니 모의고사 지표 — 학생 테스트용 링크(claude.ai 아티팩트)에서만 켜진다.
 *
 * 아티팩트의 db에 학생마다 문서 하나(`attempts/<학생 id>`)를 두고, 그 안에 풀이(run)를 쌓는다.
 * 학생은 자기 문서만 쓰고, 모든 문서는 선생님(아티팩트 주인)만 읽는다 — 규칙은 publish 때 정한다:
 *   { path: "attempts", read: "owner", write: "owner" }, { path: "attempts/{self}", read: "interact", write: "interact" }
 *
 * 개발 서버·다른 링크에는 `window.claude`가 없으니 아무것도 하지 않는다. 저장이 실패해도 시험은 그대로 간다.
 */

export type ItemLog = {
  /** 이 문항 화면에 머문 시간(초) */
  seconds: number;
  /** 이 문항을 연 횟수 */
  visits: number;
  /** 고른 차례 — [3, 5]면 ③을 골랐다가 ⑤로 바꿈 */
  picks: number[];
  /** 시작부터 처음 고를 때까지(초) */
  first_pick_at?: number;
  /** 형광펜으로 칠한 낱말 · 두 번 두드려 담은 모르는 단어 */
  hi?: string[];
  unknown?: string[];
};

export type RunLog = {
  run: string;
  mock: string;
  name: string;
  started_at: string;
  updated_at: string;
  /** doing = 푸는 중(또는 중간에 닫음) */
  status: "doing" | "submitted" | "timeup" | "quit";
  seconds: number;
  answers: Record<string, number>;
  score?: number;
  max?: number;
  correct?: number;
  items: Record<string, ItemLog>;
  /** 결과 화면에서 해설을 펼쳐 본 문항 */
  reviewed: number[];
  /** 해석을 펼쳐 본 문항 */
  translated: number[];
  /** 푸는 중에 「정답 확인」을 누른 문항 — 시작부터 몇 초에, 맞았나 */
  checked?: Record<string, { at: number; correct: boolean }>;
  /** 답을 고르기 전에 분석을 먼저 본 문항 — 그 뒤 고른 답은 「분석 보고 고름」 */
  peeked?: number[];
  /** 다정쌤 분석 레슨으로 간 문항 — 레슨에 머문 초, 결과(이해·헷갈림…, 끝까지 안 하면 「나감」) */
  analyzed?: { no: number; started_at: string; seconds: number; result: string }[];
  /** 분석 레슨에 가 있던 동안·일시정지한 동안은 시험 시간에서 뺀다 — 그 합(초) */
  paused_seconds?: number;
  /** 「일시정지」 — 시작부터 몇 초에 멈췄고 몇 초 쉬었나 */
  breaks?: { at: number; seconds: number }[];
};

export type StudentDoc = { name: string; updated_at: string; runs: Record<string, RunLog> };

type Snap = { id: string; exists: boolean; data(): Record<string, unknown> | undefined };
type DocRef = { get(): Promise<Snap>; set(d: Record<string, unknown>): Promise<void> };
type Db = {
  doc(path: string): DocRef;
  collection(path: string): {
    onSnapshot(next: (s: { docs: Snap[] }) => void, error?: (e: { code: string }) => void): () => void;
  };
};
type User = { id(): Promise<string | null>; isOwner(): Promise<boolean>; can(name: string): Promise<boolean | null> };
type Downloads = { save(f: { filename: string; data: string | Blob }): Promise<unknown> };
type ClaudeHost = { use(name: string): Promise<unknown> };

function host(): ClaudeHost | null {
  return (window as unknown as { claude?: ClaudeHost }).claude ?? null;
}

async function use<T>(name: string): Promise<T | null> {
  try {
    return ((await host()?.use(name)) as T | null) ?? null;
  } catch {
    return null;
  }
}

export const getDb = () => use<Db>("db");
export const getUser = () => use<User>("user");
export const getDownloads = () => use<Downloads>("downloads");

/**
 * 기록을 남길 수 있나 — 아티팩트 안 + 로그인 + 학생 id + 쓰기 권한(공유 메뉴의 Contributor 이상).
 * 보기 전용(Viewer·Commenter, 조직 밖 방문자)은 db에 쓰지 못한다.
 */
export async function canRecord(): Promise<boolean> {
  if (!host()) return false;
  const [db, user] = await Promise.all([getDb(), getUser()]);
  if (!db || !user || !(await user.id())) return false;
  return (await user.can("data.write")) !== false;
}

/**
 * 풀이 하나의 기록. 문항을 옮길 때·고를 때 시간을 재고, 문항을 옮길 때·끝낼 때만 저장한다
 * (한 문서에 한 번에 한 번씩 — 앞 저장이 끝나야 다음 저장).
 */
export class MiniRecorder {
  private log: RunLog;
  private t0 = Date.now();
  private current: number | null = null;
  private enteredAt = Date.now();
  private queue: Promise<void> = Promise.resolve();
  private pausedAt: number | null = null;
  private breakAt: number | null = null;
  private analysisNo: number | null = null;
  private ref: Promise<{ doc: DocRef; base: StudentDoc } | null>;

  constructor(
    private mock: MiniMock,
    name: string,
  ) {
    const now = new Date().toISOString();
    this.log = {
      run: `${now.replace(/[^0-9]/g, "").slice(0, 14)}-${Math.random().toString(36).slice(2, 6)}`,
      mock: mock.id,
      name,
      started_at: now,
      updated_at: now,
      status: "doing",
      seconds: 0,
      answers: {},
      items: {},
      reviewed: [],
      translated: [],
      checked: {},
      analyzed: [],
      paused_seconds: 0,
    };
    this.ref = this.open();
  }

  private async open() {
    if (!host()) return null;
    const [db, user] = await Promise.all([getDb(), getUser()]);
    const id = await user?.id();
    if (!db || !id) return null;
    try {
      const doc = db.doc(`attempts/${id}`);
      const snap = await doc.get();
      const prev = snap.exists ? (snap.data() as Partial<StudentDoc>) : {};
      return { doc, base: { name: prev.name ?? "", updated_at: "", runs: prev.runs ?? {} } };
    } catch {
      return null;
    }
  }

  private item(no: number): ItemLog {
    return (this.log.items[no] ??= { seconds: 0, visits: 0, picks: [] });
  }

  /** 지금 보는 문항이 바뀜 */
  enter(no: number) {
    this.leave();
    this.current = no;
    this.enteredAt = Date.now();
    this.item(no).visits++;
    this.save();
  }

  private leave() {
    if (this.current == null) return;
    const it = this.item(this.current);
    it.seconds = Math.round((it.seconds + (Date.now() - this.enteredAt) / 1000) * 10) / 10;
    this.enteredAt = Date.now();
  }

  pick(no: number, n: number) {
    const it = this.item(no);
    if (it.picks[it.picks.length - 1] === n) return;
    it.picks.push(n);
    it.first_pick_at ??= Math.round((Date.now() - this.t0) / 100) / 10 - (this.log.paused_seconds ?? 0);
    this.log.answers[no] = n;
  }

  /** 지문에 표시한 것 — 형광펜 낱말, 모르는 단어 (바뀔 때마다 통째로) */
  marks(no: number, hi: string[], unknown: string[]) {
    const it = this.item(no);
    it.hi = hi;
    it.unknown = unknown;
  }

  /** 답을 고르기 전에 분석부터 보러 감 */
  peek(no: number) {
    const p = (this.log.peeked ??= []);
    if (!p.includes(no)) p.push(no);
  }

  /** 푸는 중에 정답을 확인함 (문항마다 한 번) */
  check(no: number, correct: boolean) {
    const checked = (this.log.checked ??= {});
    if (checked[no]) return;
    checked[no] = { at: Math.round((Date.now() - this.t0) / 100) / 10 - (this.log.paused_seconds ?? 0), correct };
    this.save();
  }

  /** 분석 레슨으로 감 — 시험 시간을 멈춘다 */
  beginAnalysis(no: number) {
    this.leave();
    this.pausedAt = Date.now();
    this.analysisNo = no;
    this.save();
  }

  /** 분석 레슨에서 돌아옴 — 결과를 남기고 시간을 다시 잰다 */
  endAnalysis(result: string) {
    if (this.pausedAt == null || this.analysisNo == null) return;
    const seconds = Math.round((Date.now() - this.pausedAt) / 1000);
    (this.log.analyzed ??= []).push({ no: this.analysisNo, started_at: new Date(this.pausedAt).toISOString(), seconds, result });
    this.log.paused_seconds = (this.log.paused_seconds ?? 0) + seconds;
    this.pausedAt = null;
    this.analysisNo = null;
    this.enteredAt = Date.now();
    this.save();
  }

  /** 「일시정지」 — 시험 시간을 멈춘다 */
  pause() {
    if (this.breakAt != null) return;
    this.leave();
    this.breakAt = Date.now();
  }

  /** 일시정지를 풀고 이어 풂 */
  resume() {
    if (this.breakAt == null) return;
    const seconds = Math.round((Date.now() - this.breakAt) / 1000);
    const at = Math.round((this.breakAt - this.t0) / 1000 - (this.log.paused_seconds ?? 0));
    (this.log.breaks ??= []).push({ at, seconds });
    this.log.paused_seconds = (this.log.paused_seconds ?? 0) + seconds;
    this.breakAt = null;
    this.enteredAt = Date.now();
    this.save();
  }

  /** 기록이 db에 안 남는 학생이 결과를 선생님께 보낼 수 있게 — 이번 풀이 기록 그대로 */
  snapshot(): RunLog {
    return JSON.parse(JSON.stringify(this.log)) as RunLog;
  }

  finish(status: "submitted" | "timeup" | "quit", answers: Record<number, number>) {
    this.resume();
    this.leave();
    this.current = null;
    this.log.status = status;
    this.log.seconds = Math.round(Math.min(this.mock.minutes * 60, (Date.now() - this.t0) / 1000 - (this.log.paused_seconds ?? 0)));
    this.log.answers = Object.fromEntries(Object.entries(answers).map(([k, v]) => [k, v]));
    const s = scoreOf(this.mock, answers);
    Object.assign(this.log, { score: s.score, max: s.max, correct: s.correct });
    this.save();
  }

  /** 결과 화면에서 해설·해석을 펼침 (처음 한 번만 저장) */
  opened(no: number, what: "reviewed" | "translated") {
    if (this.log[what].includes(no)) return;
    this.log[what].push(no);
    this.save();
  }

  private save() {
    const snapshot: RunLog = JSON.parse(JSON.stringify({ ...this.log, updated_at: new Date().toISOString() }));
    this.queue = this.queue.then(async () => {
      const r = await this.ref;
      if (!r) return;
      r.base.runs[snapshot.run] = snapshot;
      r.base.name = snapshot.name;
      r.base.updated_at = snapshot.updated_at;
      try {
        await r.doc.set(r.base as unknown as Record<string, unknown>);
      } catch {
        /* 기록이 안 돼도 시험은 그대로 */
      }
    });
  }
}

/**
 * 지금 분석 레슨에 가 있는 풀이 — 앱(App.tsx)이 레슨을 끝내거나 닫을 때 결과를 넘겨준다.
 * 시험 화면이 닫혀 있는 동안에도 기록이 이어지게 모듈에 둔다
 */
let analyzing: MiniRecorder | null = null;
export function startAnalysis(rec: MiniRecorder | null, no: number) {
  analyzing = rec;
  rec?.beginAnalysis(no);
}
export function finishAnalysis(result: string) {
  analyzing?.endAnalysis(result);
  analyzing = null;
}

/** 선생님 보기 — 학생 문서를 모두 받아 온다 (주인만 읽힌다) */
export function watchStudents(db: Db, next: (docs: StudentDoc[]) => void): () => void {
  return db.collection("attempts").onSnapshot(
    (s) => next(s.docs.filter((d) => d.exists).map((d) => d.data() as unknown as StudentDoc)),
    () => next([]),
  );
}
