import type { LessonChunk } from "../../content/tutor/types";

/**
 * 데모 판정 — LLM 없이 코드가 할 수 있는 만큼만.
 *
 * **키워드를 코드에 두지 않는다.** 정답(A)은 레슨의 `demo_match.p1`,
 * 오류(C)는 `expected_errors[].signals`와 `error_priority`를 읽는다.
 * 예전에는 이 값들이 `units.ts`에 문장 순서대로 박혀 있어서, 지문을 바꾸려면
 * 레슨 JSON과 코드를 같이 고쳐야 했다.
 */
export type Verdict =
  | { kind: "A" }
  /** 예상 오류 — 그 오류의 고정 대사로 간다 */
  | { kind: "C"; errorId: string }
  /** 정답도 예상 오류도 아님. 「모르겠어요」인지는 호출하는 쪽이 따로 본다 */
  | { kind: "E" };

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

/**
 * 오류를 먼저 본다. 정답 키워드가 섞여 있어도 예상 오류가 걸리면 그쪽이다
 * (예: `태어났다`는 `태어나`를 포함하지만 분사구문 오류다).
 *
 * 동시에 여러 개면 `error_priority` 순서로 **하나만**. 한 턴에 질문 둘을 막는다.
 */
export function classify(text: string, chunk: LessonChunk): Verdict {
  if (isUnknownInput(text)) return { kind: "E" };
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

  const groups = chunk.demo_match?.p1 ?? [];
  if (groups.length && groups.every((group) => has(n, group))) {
    return { kind: "A" };
  }
  return { kind: "E" };
}

export function matchChoice(text: string, labels: string[]): string | null {
  const n = compact(text);
  for (const label of labels) {
    if (n === compact(label) || n.includes(compact(label))) return label;
  }
  return null;
}
