/**
 * 헷갈린 포인트 노트 — 수업 끝에 「오늘 헷갈렸던 곳」에서 별표를 눌러 모아 둔 것.
 *
 * 단어장(`vocab.ts`)과 같은 방식: 지금은 이 브라우저에만 남는다. 서버가 생기면 그대로 흘려보낸다.
 */

export type NoteEntry = {
  /** 레슨 안에서 포인트를 가리키는 키 (스텝 id 또는 exam_<보기>) */
  key: string;
  lessonId: string;
  /** 「7문장」「문제 ③」 */
  title: string;
  text: string;
  savedAt: string;
};

const KEY = "loopin.notes.v1";

const idOf = (e: { lessonId: string; key: string }) => `${e.lessonId}#${e.key}`;

export function loadNotes(): NoteEntry[] {
  try {
    const raw = window.localStorage.getItem(KEY);
    const parsed = raw ? (JSON.parse(raw) as NoteEntry[]) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function save(entries: NoteEntry[]): void {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(entries));
  } catch {
    /* 못 저장해도 수업은 그대로 */
  }
}

export function isNoteSaved(entries: NoteEntry[], e: { lessonId: string; key: string }): boolean {
  return entries.some((x) => idOf(x) === idOf(e));
}

/** 별표를 누른다 — 없으면 넣고, 있으면 뺀다. 새 목록을 돌려준다 */
export function toggleNote(entries: NoteEntry[], e: Omit<NoteEntry, "savedAt">): NoteEntry[] {
  const next = isNoteSaved(entries, e)
    ? entries.filter((x) => idOf(x) !== idOf(e))
    : [...entries, { ...e, savedAt: new Date().toISOString() }];
  save(next);
  return next;
}
