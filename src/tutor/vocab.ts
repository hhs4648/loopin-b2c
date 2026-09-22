/**
 * 단어장 — 학생이 뜻을 보다가 별표를 눌러 모아 둔 단어.
 *
 * 지금은 이 브라우저에만 남는다. 서버가 생기면 그대로 흘려보낸다.
 * 별표는 **저장 여부 하나**만 뜻한다. 외웠는지·복습할지는 여기서 판단하지 않는다.
 */

export type VocabEntry = {
  en: string;
  ko: string;
  /** 어느 문장에서 저장했나 — 나중에 문맥과 같이 보여 주려고 */
  sentence: string;
  savedAt: string;
};

const KEY = "loopin.vocab.v1";

function keyOf(en: string): string {
  return en.trim().toLowerCase();
}

export function loadVocab(): VocabEntry[] {
  try {
    const raw = window.localStorage.getItem(KEY);
    const parsed = raw ? (JSON.parse(raw) as VocabEntry[]) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    // 저장소가 없으면(프라이빗 모드 등) 빈 단어장. 별표는 눌러도 이번 세션만 산다
    return [];
  }
}

function save(entries: VocabEntry[]): void {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(entries));
  } catch {
    /* 못 저장해도 수업은 그대로 */
  }
}

export function isSaved(entries: VocabEntry[], en: string): boolean {
  return entries.some((e) => keyOf(e.en) === keyOf(en));
}

/** 별표를 누른다 — 없으면 넣고, 있으면 뺀다. 새 목록을 돌려준다 */
export function toggleVocab(
  entries: VocabEntry[],
  entry: Omit<VocabEntry, "savedAt">,
): VocabEntry[] {
  const next = isSaved(entries, entry.en)
    ? entries.filter((e) => keyOf(e.en) !== keyOf(entry.en))
    : [...entries, { ...entry, savedAt: new Date().toISOString() }];
  save(next);
  return next;
}
