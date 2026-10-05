/**
 * 복습 기록 — 문제를 언제 다시 볼지, 특별 목록에 넣었는지.
 *
 * 분석하고 맞힌 문제는 맞았어도 「분석 후 정답」이다. 분석 없이 맞힐 때까지 정해 둔
 * 주기로 다시 나온다. 지금은 기기에만 남는다 (서버가 생기면 옮긴다).
 */

export type ReviewStatus = "analyzed_correct" | "analyzed_wrong" | "mastered";

export type ReviewRecord = {
  status: ReviewStatus;
  /** 몇 주 뒤에 다시 볼지. null이면 「다시 안 봄」 */
  weeks: number | null;
  dueAt: string | null;
  /** 특별 목록 (시험 대비로 자주 볼 지문) */
  saved: boolean;
  updatedAt: string;
};

const REVIEW_KEY = "loopin.review.v1";
const METHOD_KEY = "loopin.method-intro.v1";

function read<T>(key: string, fallback: T): T {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function write(key: string, value: unknown) {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* 저장 못 해도 수업은 그대로 */
  }
}

export function loadReviews(): Record<string, ReviewRecord> {
  return read(REVIEW_KEY, {});
}

export function saveReview(lessonId: string, rec: Omit<ReviewRecord, "dueAt" | "updatedAt">, now = Date.now()) {
  const all = loadReviews();
  all[lessonId] = {
    ...rec,
    dueAt: rec.weeks == null ? null : new Date(now + rec.weeks * 7 * 86_400_000).toISOString(),
    updatedAt: new Date(now).toISOString(),
  };
  write(REVIEW_KEY, all);
}

/** 이 유형(예: 밑줄 의미)의 풀이법 설명을 몇 번 봤나 */
export function methodIntroCount(type: string): number {
  return read<Record<string, number>>(METHOD_KEY, {})[type] ?? 0;
}

export function bumpMethodIntro(type: string) {
  const all = read<Record<string, number>>(METHOD_KEY, {});
  all[type] = (all[type] ?? 0) + 1;
  write(METHOD_KEY, all);
}
