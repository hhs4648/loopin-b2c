/**
 * 연습할 문법 — 수업 중 「이 문법을 나중에 좀 더 연습할까요?」에서 「네」를 누른 것.
 * 보충학습실에서 그 문법의 drill(10문제, 처음엔 객관식 → 나중엔 주관식 섞어서)을 푼다.
 *
 * 단어장(`vocab.ts`)·노트(`notes.ts`)와 같은 방식: 지금은 이 브라우저에만 남는다.
 */

export type GrammarPracticeEntry = {
  /** drill id — `content/tutor/grammar-drills/<id>.json` */
  id: string;
  /** 어느 수업에서 담았나 */
  lessonId: string;
  savedAt: string;
  /** drill을 몇 번 풀었나, 마지막 점수 */
  tries?: number;
  last?: { right: number; total: number; at: string };
};

const KEY = "loopin.grammar-practice.v1";

export function loadGrammarPractice(): GrammarPracticeEntry[] {
  try {
    const raw = window.localStorage.getItem(KEY);
    const parsed = raw ? (JSON.parse(raw) as GrammarPracticeEntry[]) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function save(entries: GrammarPracticeEntry[]): void {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(entries));
  } catch {
    /* 못 저장해도 수업은 그대로 */
  }
}

/** 담는다 — 이미 있으면 그대로 */
export function addGrammarPractice(id: string, lessonId: string, now = Date.now()): void {
  const entries = loadGrammarPractice();
  if (entries.some((x) => x.id === id)) return;
  save([...entries, { id, lessonId, savedAt: new Date(now).toISOString() }]);
}

export function removeGrammarPractice(id: string): GrammarPracticeEntry[] {
  const next = loadGrammarPractice().filter((x) => x.id !== id);
  save(next);
  return next;
}

/** drill을 다 풀었다 — 점수를 남긴다 */
export function recordGrammarDrill(id: string, right: number, total: number, now = Date.now()): void {
  save(
    loadGrammarPractice().map((x) =>
      x.id === id ? { ...x, tries: (x.tries ?? 0) + 1, last: { right, total, at: new Date(now).toISOString() } } : x,
    ),
  );
}
