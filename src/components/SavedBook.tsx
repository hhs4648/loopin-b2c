import { useState } from "react";
import { setOfLesson } from "../tutor/sets";
import { loadNotes, toggleNote, type NoteEntry } from "../tutor/notes";
import { loadVocab, toggleVocab, type VocabEntry } from "../tutor/vocab";

/**
 * 메인에서 여는 내 공부 — **단어장**과 **노트**.
 *
 * 단어장: 문장에서 단어 뜻의 별표를 누르거나, 마무리 단어 체크에서 고른 단어.
 * 노트: 수업 끝 「헷갈린 포인트」에서 별표를 누른 것.
 * 둘 다 어느 문제에서 저장했는지로 묶고, 최근에 공부한 문제가 위로 온다.
 * 별표를 다시 누르면 빠진다 (실수로 눌렀을 때 바로 되돌릴 수 있게, 목록에서 바로 지우지는 않는다).
 */
export type SavedKind = "vocab" | "notes";

type Props = { kind: SavedKind; onBack: () => void };

/** 저장한 지문의 이름 — 「30번 문제」. 목록에 없는 지문은 「다른 수업」 */
function lessonTitle(id?: string): string {
  const set = id ? setOfLesson(id) : null;
  return set ? `${set.title} · ${set.subtitle}` : "다른 수업";
}

function groupBy<T extends { savedAt: string }>(items: T[], keyOf: (x: T) => string) {
  const groups = new Map<string, T[]>();
  for (const x of [...items].sort((a, b) => b.savedAt.localeCompare(a.savedAt))) {
    const k = keyOf(x);
    groups.set(k, [...(groups.get(k) ?? []), x]);
  }
  return [...groups.entries()];
}

export function SavedBook({ kind, onBack }: Props) {
  // 처음 연 순간의 목록을 줄 순서로 쓴다 — 별표를 빼도 줄이 바로 사라지지 않게
  const [rows] = useState(() => (kind === "vocab" ? loadVocab() : loadNotes()));
  const [vocab, setVocab] = useState<VocabEntry[]>(() => loadVocab());
  const [notes, setNotes] = useState<NoteEntry[]>(() => loadNotes());

  const title = kind === "vocab" ? "단어장" : "내 노트";
  const empty =
    kind === "vocab"
      ? "아직 저장한 단어가 없어요. 수업 중에 단어를 누르고 ☆를 눌러 보세요."
      : "아직 저장한 노트가 없어요. 수업 끝 「헷갈린 포인트」에서 ☆를 눌러 보세요.";

  return (
    <div className="stage-fill saved">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="목록으로" onClick={onBack}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
            <path d="M15 6l-6 6 6 6" />
          </svg>
        </button>
      </header>
      <div className="saved-body-scroll">
        <h1 className="saved-title">{title}</h1>
        {rows.length === 0 ? <p className="saved-empty">{empty}</p> : null}

        {kind === "vocab"
          ? groupBy(rows as VocabEntry[], (w) => w.source ?? "").map(([source, words]) => (
              <section key={source} className="saved-group">
                <h2 className="saved-group-title">{lessonTitle(source)}</h2>
                <ul className="saved-list">
                  {words.map((w) => {
                    const on = vocab.some((x) => x.en.toLowerCase() === w.en.toLowerCase());
                    return (
                      <li key={w.en} className={`saved-row${on ? "" : " off"}`}>
                        <button
                          type="button"
                          className={`point-star${on ? " on" : ""}`}
                          aria-pressed={on}
                          aria-label={on ? "단어장에서 빼기" : "다시 저장"}
                          onClick={() => setVocab(toggleVocab(vocab, { en: w.en, ko: w.ko, sentence: w.sentence, source: w.source }))}
                        >
                          {on ? "★" : "☆"}
                        </button>
                        <span className="saved-body">
                          <b className="saved-en">{w.en}</b>
                          <span>{w.ko}</span>
                        </span>
                      </li>
                    );
                  })}
                </ul>
              </section>
            ))
          : groupBy(rows as NoteEntry[], (n) => n.lessonId).map(([lessonId, items]) => (
              <section key={lessonId} className="saved-group">
                <h2 className="saved-group-title">{lessonTitle(lessonId)}</h2>
                <ul className="saved-list">
                  {items.map((n) => {
                    const on = notes.some((x) => x.lessonId === n.lessonId && x.key === n.key);
                    return (
                      <li key={n.key} className={`saved-row${on ? "" : " off"}`}>
                        <button
                          type="button"
                          className={`point-star${on ? " on" : ""}`}
                          aria-pressed={on}
                          aria-label={on ? "노트에서 빼기" : "다시 저장"}
                          onClick={() => setNotes(toggleNote(notes, { key: n.key, lessonId: n.lessonId, title: n.title, text: n.text }))}
                        >
                          {on ? "★" : "☆"}
                        </button>
                        <span className="saved-body">
                          <b className="saved-tag">{n.title}</b>
                          <span>{n.text}</span>
                        </span>
                      </li>
                    );
                  })}
                </ul>
              </section>
            ))}
      </div>
    </div>
  );
}
