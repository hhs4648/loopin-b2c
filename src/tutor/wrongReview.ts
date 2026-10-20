import { pushKey } from "./cloud";
import { combinedAnswers, getMiniMock, type MiniItem } from "./mini";

/**
 * 틀린 문제 복습 — 10분 모의고사 한 회의 4단계 (2026-10-20 선생님).
 * 그 회에서 틀렸거나 안 푼 문제를 **힌트 없이 하나씩** 다시 푼다. 맞히면 「잘했어요」, 또 틀리면 왜 틀렸는지
 * 스스로 생각해 적게 하고(기록), 그다음 분석을 다시 볼 수 있다.
 */
export type WrongReviewRecord = { correct: boolean; picked: number; reason?: string; at: string };

const KEY = "loopin.wrong-reviews.v1";

type Store = Record<string, Record<string, WrongReviewRecord>>;

function load(): Store {
  try {
    const raw = window.localStorage.getItem(KEY);
    const all = raw ? (JSON.parse(raw) as Store) : {};
    return all && typeof all === "object" ? all : {};
  } catch {
    return {};
  }
}

/** 이 묶음에서 복습할 문항 — 전체·낱개 풀이를 합친 가장 최근 답이 틀린 것 (안 푼 문제는 아직 아니다) */
export function itemsToReview(mockId: string): MiniItem[] {
  const mock = getMiniMock(mockId);
  if (!mock) return [];
  const { answers } = combinedAnswers(mockId);
  return mock.items.filter((it) => it.no in answers && answers[it.no] !== it.answer);
}

export function reviewRecords(mockId: string): Record<string, WrongReviewRecord> {
  return load()[mockId] ?? {};
}

export function saveReviewRecord(mockId: string, no: number, rec: Omit<WrongReviewRecord, "at">): void {
  try {
    const all = load();
    all[mockId] = { ...(all[mockId] ?? {}), [no]: { ...rec, at: new Date().toISOString() } };
    window.localStorage.setItem(KEY, JSON.stringify(all));
    pushKey(KEY);
  } catch {
    /* 그대로 */
  }
}

/** 4단계 진행 — 복습할 문항 수와 복습한 수 (그 회를 안 풀었으면 0/0) */
export function reviewProgress(mockId: string): { done: number; total: number } {
  const items = itemsToReview(mockId);
  const recs = reviewRecords(mockId);
  return { done: items.filter((it) => it.no in recs).length, total: items.length };
}

/** 복습에서 맞힌 레슨들 — 「틀린 문제」 목록에서 빼기 위해 (레슨 id → 맞힌 시각) */
export function reviewedRight(): Record<string, string> {
  const out: Record<string, string> = {};
  for (const [mockId, recs] of Object.entries(load())) {
    const mock = getMiniMock(mockId);
    if (!mock) continue;
    for (const [no, r] of Object.entries(recs)) {
      const it = mock.items.find((x) => String(x.no) === no);
      if (it?.lesson && (!(it.lesson in out) || out[it.lesson]! < r.at)) out[it.lesson] = r.correct ? r.at : out[it.lesson] ?? "";
    }
  }
  return out;
}
