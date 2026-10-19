import eng2024March from "../../content/tutor/mini-mocks/eng-2024-03-full.json";

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

export function allMiniMocks(): MiniMock[] {
  return MOCKS;
}

export function getMiniMock(id: string | null | undefined): MiniMock | null {
  return MOCKS.find((m) => m.id === id) ?? null;
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
};

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

/** 지난 기록 — 이 브라우저에만 (시험마다 최근 것부터) */
export function loadAttempts(mockId: string): MiniAttempt[] {
  try {
    const raw = window.localStorage.getItem(KEY);
    const all = raw ? (JSON.parse(raw) as Record<string, MiniAttempt[]>) : {};
    return Array.isArray(all[mockId]) ? all[mockId]! : [];
  } catch {
    return [];
  }
}

export function saveAttempt(mockId: string, attempt: MiniAttempt): void {
  try {
    const raw = window.localStorage.getItem(KEY);
    const all = raw ? (JSON.parse(raw) as Record<string, MiniAttempt[]>) : {};
    all[mockId] = [attempt, ...(all[mockId] ?? [])].slice(0, 20);
    window.localStorage.setItem(KEY, JSON.stringify(all));
  } catch {
    /* 못 저장해도 이번 결과는 보인다 */
  }
}

export function clock(seconds: number): string {
  const s = Math.max(0, Math.round(seconds));
  return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
}
