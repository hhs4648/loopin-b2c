import eng2024March from "../../content/tutor/mini-mocks/eng-2024-03-full.json";
import { pushKey } from "./cloud";
import { reviewedRight } from "./wrongReview";
import { TEN_MIN_COUNT, singleMock, singleOf, tenMinMocks } from "./tenmin";

/**
 * 미니 모의고사 — 전체 모의고사는 너무 오래 걸려서, 쉬운 문항(18~20, 도표·일치 등)은 빼고
 * 고난도만 20분짜리로 묶은 시험. 시간을 재고, 끝나면 점수와 문항별 해설을 보여 준다.
 *
 * 문항은 시험지 그대로(`content/tutor/mini-mocks/*.json`, `scripts/mini/`의 생성기가 만든다).
 * 분석 레슨이 없는 문항도 넣는다 — 틀리면 레슨이 있는 문항은 「분석하러 가기」, 없으면 해설.
 */

export type MiniItem = {
  no: number;
  /** 유형 — 「빈칸」「순서」 */
  kind: string;
  points: number;
  /** 1~5 */
  answer: number;
  question: string;
  /** 묶음 안내 — 장문 「[41~42] 다음 글을 읽고, 물음에 답하시오.」 */
  group?: string;
  /** 순서의 주어진 글, 문장 넣기의 주어진 문장 */
  given?: string;
  passage?: string;
  /** 본문 뒤에 상자로 — 요약문 문제의 요약문 */
  after?: string;
  /** 순서 문제의 (A)(B)(C) */
  paragraphs?: string[];
  /** 함축 의미 문제의 밑줄 */
  underline?: string;
  /** 어법·어휘 — ①~⑤·(a)~(e) 바로 뒤 낱말에 밑줄 */
  marked?: boolean;
  /** 보기 글. 번호만 고르는 문항은 빈 글 */
  options: string[];
  foot?: string;
  /** 전국 오답률(%) */
  wrong_rate?: number;
  /** 분석 레슨이 있는 세트 */
  lesson?: string;
  /** 해설지 [출제의도] */
  intent?: string;
  translation?: string;
  /** 선지 해석 — ①~⑤ 순서 (다정쌤 분석 레슨의 보기 뜻에서). 한국어 선지·번호만 있는 문항은 없다 */
  options_ko?: string[];
  /** 정답 고친 줄 (어법·어휘) — 「④ which → in which」 */
  fix?: string;
};

export type MiniMock = {
  id: string;
  subject: "english" | "korean";
  title: string;
  subtitle: string;
  source: string;
  minutes: number;
  items: MiniItem[];
};

/* 이 폴더(영어 라인)에는 2024년 3월 고3 하나 — 다른 회차는 국어 라인(korean/2025-03-10)에 있다 */
const MOCKS = [eng2024March] as unknown as MiniMock[];

/** 교무실의 긴 미니 모의고사(20분, 시험지 순서). 코스의 10분 모의고사는 `tenMinMocks()` */
export function allMiniMocks(): MiniMock[] {
  return MOCKS;
}

/**
 * 복습 모의고사 — 10분 모의고사에서 틀린 문제만 모은 것. id는 `ten-review-<칸 이름>`(코스의 복습 칸마다 하나,
 * `counsel.ts`). 풀 때마다 **그때 틀려 있는** 문제로 새로 만든다.
 */
export const REVIEW_PREFIX = "ten-review-";
export const isReviewMock = (id: string) => id.startsWith(REVIEW_PREFIX);

export function getMiniMock(id: string | null | undefined): MiniMock | null {
  if (!id) return null;
  if (isReviewMock(id)) return reviewMock(id);
  const single = singleOf(id);
  if (single) {
    const base = getMiniMock(single.base);
    return base ? singleMock(base, single.no) : null;
  }
  return MOCKS.find((m) => m.id === id) ?? tenMinMocks("all").find((m) => m.id === id) ?? tenMinMocks("2pt").find((m) => m.id === id) ?? null;
}

/**
 * 한 묶음의 문항마다 **가장 최근에 낸 답** — 전체(20분) 풀이와 낱개(`-q<번호>`) 풀이를 합친다.
 * 코스 화면의 ○/✕·예상 점수·틀린 문제 복습이 이걸 본다
 */
export function combinedAnswers(mockId: string): { answers: Record<number, number>; at: string | null; peeked: number[]; checked: number[] } {
  const mock = getMiniMock(mockId);
  const out = { answers: {} as Record<number, number>, at: null as string | null, peeked: [] as number[], checked: [] as number[] };
  if (!mock) return out;
  const latest = new Map<number, string>();
  const note = (a: MiniAttempt) => {
    for (const [no, v] of Object.entries(a.answers)) {
      const n = Number(no);
      if ((latest.get(n) ?? "") > a.at) continue;
      latest.set(n, a.at);
      out.answers[n] = v;
      if (a.peeked?.includes(n)) out.peeked.push(n);
      else out.peeked = out.peeked.filter((x) => x !== n);
      if (a.checked?.includes(n)) out.checked.push(n);
      else out.checked = out.checked.filter((x) => x !== n);
    }
    if (!out.at || a.at > out.at) out.at = a.at;
  };
  for (const a of loadAttempts(mockId)) note(a);
  for (const it of mock.items) for (const a of loadAttempts(`${mockId}-q${it.no}`)) note(a);
  return out;
}

/**
 * 10분 모의고사의 문항마다 **가장 최근에 푼 기록**(원래 회차든 복습이든)에서 틀렸거나 안 푼 것.
 * 같은 문제를 그대로 다시 풀면 답을 외우므로 맞힌 것은 뺀다 — 복습에서 맞히면 다음 복습엔 안 나온다.
 * 문항은 레슨(세트) id로 알아본다 — 번호(24번)는 시험이 다르면 겹친다.
 */
export function wrongItems(): MiniItem[] {
  const all = allAttempts();
  /** 레슨 → 마지막으로 푼 시각과 맞았는지 */
  const latest = new Map<string, { at: string; ok: boolean }>();
  const note = (mock: MiniMock, a: MiniAttempt) => {
    for (const it of mock.items) {
      if (!it.lesson) continue;
      const prev = latest.get(it.lesson);
      // 같은 시각이면 뒤에 보는 쪽(복습)이 이긴다
      if (prev && prev.at > a.at) continue;
      latest.set(it.lesson, { at: a.at, ok: a.answers[it.no] === it.answer });
    }
  };
  const tens = [...tenMinMocks("all"), ...tenMinMocks("2pt")];
  for (const m of tens) {
    for (const a of all[m.id] ?? []) note(m, a);
    // 낱개 풀기 기록도
    for (const it of m.items) {
      const single = singleMock(m, it.no);
      if (single) for (const a of all[single.id] ?? []) note(single, a);
    }
  }
  // 복습 기록 — 그때 어떤 문항이었는지는 기록(`items`)에 남겨 둔 것으로 안다
  for (const [id, list] of Object.entries(all)) {
    if (!isReviewMock(id)) continue;
    for (const a of list) {
      if (!a.items) continue;
      const mock = reviewMockOf(id, a.items.map((x) => x.lesson));
      if (mock) note(mock, a);
    }
  }
  // 4단계 「틀린 문제 복습」에서 맞힌 것 — 그 뒤에 다시 틀린 기록이 없으면 틀린 문제가 아니다
  for (const [lesson, at] of Object.entries(reviewedRight())) {
    if (!at) continue;
    const prev = latest.get(lesson);
    if (!prev || prev.at <= at) latest.set(lesson, { at, ok: true });
  }
  const out: MiniItem[] = [];
  const seenLesson = new Set<string>();
  for (const m of tens) {
    for (const it of m.items) {
      if (!it.lesson || seenLesson.has(it.lesson)) continue;
      seenLesson.add(it.lesson);
      const l = latest.get(it.lesson); // 아직 안 푼 문제는 복습이 아니다
      if (l && !l.ok) out.push(it);
    }
  }
  return out;
}

/** 틀린 문제 중 최근 시험 것부터 다섯 개 — 번호는 1부터 새로 (시험이 다른 문항끼리 번호가 겹치지 않게) */
export function reviewMock(id: string): MiniMock | null {
  const wrong = wrongItems().slice(0, TEN_MIN_COUNT);
  return reviewMockOf(id, wrong.map((it) => it.lesson!));
}

function reviewMockOf(id: string, lessons: (string | undefined)[]): MiniMock | null {
  const byLesson = new Map(tenMinMocks("all").flatMap((m) => m.items).map((it) => [it.lesson!, it] as const));
  const items = lessons.map((l) => (l ? byLesson.get(l) : undefined)).filter((x): x is MiniItem => x != null).map((it, k) => ({ ...it, no: k + 1 }));
  if (!items.length) return null;
  return {
    id,
    subject: "english",
    title: "틀린 문제 다시",
    subtitle: `10분 모의고사에서 틀린 ${items.length}문제`,
    source: "최근 기록에서 틀렸거나 안 푼 문항",
    minutes: Math.max(4, items.length * 2),
    items,
  };
}

export type MiniAttempt = {
  at: string;
  /** 문항 번호 → 고른 보기(1~5). 안 푼 문항은 없다 */
  answers: Record<number, number>;
  seconds: number;
  /** 시간이 다 돼서 저절로 냈나 */
  timeUp: boolean;
  /** 푸는 중에 「정답 확인」을 누른 문항 */
  checked?: number[];
  /** 답을 고르기 전에 다정쌤 분석을 먼저 본 문항 — 그 뒤에 고른 답은 「분석 보고 고름」 */
  peeked?: number[];
  /** 두 번 두드려 담은 모르는 단어 — 뜻은 분석 레슨에서 찾은 것(못 찾으면 빈 칸) */
  unknown?: { no: number; en: string; ko: string }[];
  /** 문항마다 그 화면에 머문 시간(초) — 여러 번 오가면 더한다. 분석·일시정지 시간은 뺀다 */
  times?: Record<number, number>;
  /** 복습 모의고사는 풀 때마다 문항이 다르다 — 그때 문항(번호 → 레슨)을 남겨 둔다 */
  items?: { no: number; lesson?: string }[];
};

/**
 * 푸는 중인 시험 — 중간에 나가도 푼 데까지 남겨 두고, 돌아오면 남은 시간부터 이어 푼다 (2026-10-20 선생님).
 * 제출하면 지운다. 이 브라우저가 원본, 서버가 사본 (`cloud.ts`).
 */
export type MiniDoing = {
  answers: Record<number, number>;
  checked: number[];
  peeked: number[];
  marks: Record<number, { hi: number[]; unk: { i: number; en: string; ko: string }[] }>;
  at: number;
  /** 지금까지 쓴 시간(ms) — 분석·일시정지 시간은 뺀 것 */
  usedMs: number;
  /** 문항마다 쓴 시간(초) */
  times?: Record<number, number>;
  savedAt: string;
};

const DOING_KEY = "loopin.mini.doing.v1";

function allDoing(): Record<string, MiniDoing> {
  try {
    const raw = window.localStorage.getItem(DOING_KEY);
    const all = raw ? (JSON.parse(raw) as Record<string, MiniDoing>) : {};
    return all && typeof all === "object" ? all : {};
  } catch {
    return {};
  }
}

export function loadDoing(mockId: string): MiniDoing | null {
  return allDoing()[mockId] ?? null;
}

export function saveDoing(mockId: string, doing: Omit<MiniDoing, "savedAt">): void {
  try {
    const all = allDoing();
    all[mockId] = { ...doing, savedAt: new Date().toISOString() };
    window.localStorage.setItem(DOING_KEY, JSON.stringify(all));
    pushKey(DOING_KEY);
  } catch {
    /* 못 남겨도 이번 풀이는 계속된다 */
  }
}

export function clearDoing(mockId: string): void {
  try {
    const all = allDoing();
    if (!(mockId in all)) return;
    delete all[mockId];
    window.localStorage.setItem(DOING_KEY, JSON.stringify(all));
    pushKey(DOING_KEY);
  } catch {
    /* 그대로 */
  }
}

/** 문항당 평균 시간(초) — 전체 · 2점 · 3점. 화면을 열어 본 문항만 센다 (시간 기록이 없는 예전 풀이는 null) */
export function averageTimes(mock: MiniMock, times: Record<number, number> | undefined): { all: number; byPoints: { points: number; avg: number; n: number }[] } | null {
  if (!times) return null;
  const seen = mock.items.filter((it) => (times[it.no] ?? 0) > 0);
  if (!seen.length) return null;
  const avg = (xs: MiniItem[]) => xs.reduce((n, it) => n + times[it.no]!, 0) / xs.length;
  const points = [...new Set(seen.map((it) => it.points))].sort((a, b) => a - b);
  return { all: avg(seen), byPoints: points.map((p) => { const xs = seen.filter((it) => it.points === p); return { points: p, avg: avg(xs), n: xs.length }; }) };
}

export type MiniScore = { score: number; max: number; correct: number; total: number };

export function scoreOf(mock: MiniMock, answers: Record<number, number>): MiniScore {
  let score = 0;
  let correct = 0;
  for (const it of mock.items) {
    if (answers[it.no] === it.answer) {
      score += it.points;
      correct++;
    }
  }
  return { score, max: mock.items.reduce((n, it) => n + it.points, 0), correct, total: mock.items.length };
}

/**
 * 예상 시험점수 — 10분 모의고사는 그 시험에서 가장 어려운 문제만 푸는 것이라, 나머지(쉬운) 문제는 잘 맞힌다고 보고
 * 100점으로 환산한다 (2026-10-20 선생님: 「예상 시험점수」 정도로 대충).
 *
 * 맞힌 문제의 점수(3점은 3점 그대로 — 가중치)에, 나머지 점수(100 − 이 회 문제 배점 합)를 쉬운 문제 정답률로 곱해 더한다.
 * 쉬운 문제 정답률은 어려운 문제 정답률에 따라 80~95% — 어려운 걸 다 맞힌 학생은 쉬운 것도 거의 다 맞힌다.
 */
export function estimatedExamScore(mock: MiniMock, answers: Record<number, number>): number {
  const s = scoreOf(mock, answers);
  if (!s.total) return 0;
  const hardRate = s.correct / s.total;
  const easyRate = 0.8 + 0.15 * hardRate;
  const rest = Math.max(0, 100 - s.max);
  return Math.round(s.score + rest * easyRate);
}

/** 유형별로 몇 개 맞혔나 — 「빈칸 1/3」 */
export function byKind(mock: MiniMock, answers: Record<number, number>): { kind: string; right: number; total: number }[] {
  const out: { kind: string; right: number; total: number }[] = [];
  for (const it of mock.items) {
    let row = out.find((r) => r.kind === it.kind);
    if (!row) out.push((row = { kind: it.kind, right: 0, total: 0 }));
    row.total++;
    if (answers[it.no] === it.answer) row.right++;
  }
  return out;
}

const KEY = "loopin.mini.v1";

/** 지난 기록 — 시험마다 최근 것부터. 이 브라우저가 원본, 서버(`learner_state`)가 사본 (`cloud.ts`) */
export function loadAttempts(mockId: string): MiniAttempt[] {
  try {
    const all = allAttempts();
    return Array.isArray(all[mockId]) ? all[mockId]! : [];
  } catch {
    return [];
  }
}

/** 시험 id → 풀이 목록 (최근 것부터) */
export function allAttempts(): Record<string, MiniAttempt[]> {
  try {
    const raw = window.localStorage.getItem(KEY);
    const all = raw ? (JSON.parse(raw) as Record<string, MiniAttempt[]>) : {};
    return all && typeof all === "object" ? all : {};
  } catch {
    return {};
  }
}

export function saveAttempt(mockId: string, attempt: MiniAttempt): void {
  try {
    const all = allAttempts();
    all[mockId] = [attempt, ...(all[mockId] ?? [])].slice(0, 20);
    window.localStorage.setItem(KEY, JSON.stringify(all));
    pushKey(KEY);
  } catch {
    /* 못 저장해도 이번 결과는 보인다 */
  }
}

export function clock(seconds: number): string {
  const s = Math.max(0, Math.round(seconds));
  return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
}
