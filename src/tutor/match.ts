import type { LessonChunk, ScoringPoint } from "../../content/tutor/types";

/**
 * 데모 판정 — LLM 없이 코드가 할 수 있는 만큼만.
 *
 * **키워드를 코드에 두지 않는다.** 정답은 레슨의 `scoring_points[].check`,
 * 오류(C)는 `expected_errors[].signals`와 `error_priority`를 읽는다.
 *
 * 정답/오답을 한 덩어리로 보지 않고 **체크리스트로 본다.** 학생이 낸 것에
 * 체크하고, 못 한 것 중 하나만 유도하기 위해서다. 그래서 이 파일은 "맞았다/
 * 틀렸다"가 아니라 **어느 항목이 걸렸는지**를 돌려준다.
 */
export type Verdict =
  /** 예상 오류 — 그 오류의 고정 대사로 간다 (체크보다 먼저 본다) */
  | { kind: "C"; errorId: string }
  /** 이번 답에서 체크된 항목 id들 (없으면 빈 배열) */
  | { kind: "points"; hit: number[] };

function compact(s: string): string {
  return s
    .toLowerCase()
    .replace(/[“”"'’.,!?~\-]/g, "")
    .replace(/\s+/g, "");
}

const UNKNOWN_RE = /잘모르|모르겠어|모르겠어요|몰라요|몰라|힌트|포기|잘모르겠/;

export function isUnknownInput(text: string): boolean {
  const n = compact(text);
  return !n || UNKNOWN_RE.test(n);
}

function has(haystack: string, needles: string[]): boolean {
  return needles.some((n) => haystack.includes(compact(n)));
}

/** 학생 답에서 체크되는 항목들 */
export function checkedPointsIn(text: string, points: ScoringPoint[]): number[] {
  const n = compact(text);
  return points.filter((p) => p.check?.length && has(n, p.check)).map((p) => p.id);
}

/**
 * 오류를 먼저 본다. 체크되는 항목이 섞여 있어도 예상 오류가 걸리면 그쪽이다
 * (예: `태어났다`는 `태어나`를 포함하지만 분사구문 오류다).
 *
 * 동시에 여러 개면 `error_priority` 순서로 **하나만**. 한 턴에 질문 둘을 막는다.
 */
export function classify(text: string, chunk: LessonChunk): Verdict {
  if (isUnknownInput(text)) return { kind: "points", hit: [] };
  const n = compact(text);

  const errors = chunk.expected_errors ?? [];
  const order = chunk.error_priority ?? errors.map((e) => e.id);
  for (const id of order) {
    const error = errors.find((e) => e.id === id);
    if (!error?.signals?.length) continue;
    if (!has(n, error.signals)) continue;
    if (error.not_signals?.length && has(n, error.not_signals)) continue;
    return { kind: "C", errorId: id };
  }

  return { kind: "points", hit: checkedPointsIn(text, chunk.scoring_points ?? []) };
}

export function matchChoice(text: string, labels: string[]): string | null {
  const n = compact(text);
  for (const label of labels) {
    if (n === compact(label) || n.includes(compact(label))) return label;
  }
  return null;
}
