import { useState } from "react";
import { setOfLesson } from "../tutor/sets";
import { loadNotes, toggleNote, type NoteEntry } from "../tutor/notes";
import { loadVocab, toggleVocab, type VocabEntry } from "../tutor/vocab";
import { lessonIdOfSentence, loadWordStats, statOf } from "../tutor/vocabTest";
import { VocabTest } from "./VocabTest";
import { GrammarDrill } from "./GrammarDrill";
import { getGrammarDrill, groupOf, type GrammarGroup } from "../tutor/grammarDrills";
import { loadDrillScores, loadGrammarPractice, removeGrammarPractice, type GrammarPracticeEntry } from "../tutor/grammarPractice";

/**
 * 메인에서 여는 내 공부 — **단어장**과 **노트**.
 *
 * 단어장: 문장에서 단어 뜻의 별표를 누르거나, 마무리 단어 체크에서 고른 단어.
 * 노트: 수업 끝 「헷갈린 포인트」에서 별표를 누른 것.
 * 연습할 문법: 수업 중 「이 문법을 나중에 좀 더 연습할까요?」에서 「네」를 누른 것 — 단어장 위에.
 *   묶음(「nor / so」)마다 세트(기본 개념 · nor vs so · …)를 순서대로 — 끝낸 세트는 ✓와 점수. 순서를 잠그지는 않는다.
 * 단어장은 최근에 저장한 단어가 위로 — 단어마다 저장한 날짜, 테스트에서 본 횟수·맞힌 횟수·틀린 횟수.
 * 노트는 어느 문제에서 저장했는지로 묶고, 최근에 공부한 문제가 위로 온다.
 * 별표를 다시 누르면 빠진다 (실수로 눌렀을 때 바로 되돌릴 수 있게, 목록에서 바로 지우지는 않는다).
 */
export type SavedKind = "vocab" | "notes";

type Props = { kind: SavedKind; onBack: () => void };

/** 저장한 지문의 이름 — 「30번 문제」. 목록에 없는 지문은 「다른 수업」 */
function lessonTitle(id?: string): string {
  const set = id ? setOfLesson(id) : null;
  return set ? `${set.title} · ${set.subtitle}` : "다른 수업";
}

/** 「10.12」 — 저장한 날짜 */
function shortDate(iso: string): string {
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? "" : `${d.getMonth() + 1}.${d.getDate()}`;
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
  const [rows, setRows] = useState(() => (kind === "vocab" ? loadVocab() : loadNotes()));
  const [vocab, setVocab] = useState<VocabEntry[]>(() => loadVocab());
  const [notes, setNotes] = useState<NoteEntry[]>(() => loadNotes());
  const [stats, setStats] = useState(() => loadWordStats());
  /** 테스트 중이면 볼 단어 (null = 단어장에서 고름). 테스트를 다시 열 때마다 key를 바꾼다 */
  const [test, setTest] = useState<{ only?: VocabEntry[]; n: number } | null>(null);
  const [grammar, setGrammar] = useState<GrammarPracticeEntry[]>(() => (kind === "vocab" ? loadGrammarPractice() : []));
  const [scores, setScores] = useState(() => loadDrillScores());
  /** 풀고 있는 문법 drill과 그 묶음 */
  const [drill, setDrill] = useState<{ id: string; group: GrammarGroup } | null>(null);

  if (drill) {
    const at = drill.group.drills.indexOf(drill.id);
    const nextId = drill.group.drills[at + 1];
    const nextDrill = nextId ? getGrammarDrill(nextId) : null;
    return (
      <GrammarDrill
        key={drill.id}
        id={drill.id}
        next={nextDrill ? { id: nextDrill.id, title: nextDrill.title } : undefined}
        onOpen={(id) => setDrill({ id, group: drill.group })}
        onClose={() => {
          setDrill(null);
          setGrammar(loadGrammarPractice());
          setScores(loadDrillScores());
        }}
      />
    );
  }

  // 담은 것을 묶음으로 — 예전에 drill 하나(nor-inversion)로 담은 것도 그 묶음으로 보인다
  const groups: { entry: GrammarPracticeEntry; group: GrammarGroup }[] = [];
  for (const entry of [...grammar].sort((a, b) => b.savedAt.localeCompare(a.savedAt))) {
    const group = groupOf(entry.id);
    if (group && !groups.some((x) => x.group.id === group.id)) groups.push({ entry, group });
  }

  if (test) {
    return (
      <VocabTest
        key={test.n}
        only={test.only}
        onRetry={(words) => setTest({ only: words, n: test.n + 1 })}
        onClose={() => {
          setTest(null);
          setStats(loadWordStats());
          setRows(loadVocab());
          setVocab(loadVocab());
        }}
      />
    );
  }

  // 연습할 문법이 있으면 단어장만이 아니니 집 이름(보충학습실)으로
  const title = kind === "vocab" ? (grammar.length ? "보충학습실" : "단어장") : "내 노트";
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
        {rows.length === 0 && !grammar.length ? <p className="saved-empty">{empty}</p> : null}

        {grammar.length ? (
          <section className="saved-group gprac">
            <h2 className="saved-group-title">연습할 문법</h2>
            {groups.map(({ entry, group }) => (
              <div key={group.id} className="gprac-card">
                <div className="gprac-head">
                  <button
                    type="button"
                    className="point-star on"
                    aria-label="연습할 문법에서 빼기"
                    onClick={() => {
                      // 이 묶음으로 보이는 것을 다 뺀다
                      let left = grammar;
                      for (const g of grammar) if (groupOf(g.id)?.id === group.id) left = removeGrammarPractice(g.id);
                      setGrammar(left);
                    }}
                  >
                    ★
                  </button>
                  <span className="saved-body">
                    <b className="saved-en">{group.title}</b>
                    <small className="saved-meta">
                      {group.subtitle ? `${group.subtitle} · ` : ""}
                      {shortDate(entry.savedAt)} 저장 · {setOfLesson(entry.lessonId)?.title ?? "다른 수업"}
                    </small>
                  </span>
                  {group.drills.length === 1 ? (
                    <button type="button" className="gprac-go" onClick={() => setDrill({ id: group.drills[0]!, group })}>
                      {scores[group.drills[0]!] ? `다시 풀기 · ${scores[group.drills[0]!]!.right}/${scores[group.drills[0]!]!.total}` : "10문제 풀기"}
                    </button>
                  ) : null}
                </div>
                {/* 세트가 하나뿐이면 이름이 겹치니 줄을 안 그린다 */}
                {group.drills.length > 1 ? <ol className="gprac-sets">
                  {group.drills.map((id, i) => {
                    const d = getGrammarDrill(id);
                    if (!d) return null;
                    const sc = scores[id];
                    return (
                      <li key={id} className={`gprac-set${sc ? " done" : ""}`}>
                        <span className="gprac-num">{sc ? "✓" : i + 1}</span>
                        <span className="gprac-name">
                          {d.title}
                          {sc ? <small className="gprac-score"> {sc.right}/{sc.total}</small> : null}
                        </span>
                        <button type="button" className="gprac-go" onClick={() => setDrill({ id, group })}>
                          {sc ? "다시 풀기" : `${d.items.length}문제 풀기`}
                        </button>
                      </li>
                    );
                  })}
                </ol> : null}
              </div>
            ))}
            {rows.length ? <h2 className="saved-group-title">단어장</h2> : null}
          </section>
        ) : null}

        {kind === "vocab" && vocab.length ? (
          <button type="button" className="read-continue vtest-start" onClick={() => setTest({ n: 0 })}>
            단어 테스트
          </button>
        ) : null}

        {kind === "vocab"
          ? (
              <ul className="saved-list">
                {[...(rows as VocabEntry[])]
                  .sort((a, b) => b.savedAt.localeCompare(a.savedAt))
                  .map((w) => {
                    const on = vocab.some((x) => x.en.toLowerCase() === w.en.toLowerCase());
                    const st = statOf(stats, w.en);
                    const source = w.source ?? lessonIdOfSentence(w.sentence);
                    return (
                      <li key={w.en} className={`saved-row${on ? "" : " off"}`}>
                        <button
                          type="button"
                          className={`point-star${on ? " on" : ""}`}
                          aria-pressed={on}
                          aria-label={on ? "단어장에서 빼기" : "다시 저장"}
                          onClick={() => setVocab(toggleVocab(vocab, { en: w.en, ko: w.ko, kind: w.kind, sentence: w.sentence, source: w.source }))}
                        >
                          {on ? "★" : "☆"}
                        </button>
                        <span className="saved-body">
                          <b className="saved-en">
                            {w.kind === "phrase" ? <small className="saved-kind">숙어</small> : null}
                            {w.en}
                          </b>
                          <span>{w.ko}</span>
                          <small className="saved-meta">
                            {shortDate(w.savedAt)} 저장 · {(source && setOfLesson(source)?.title) || "다른 수업"}
                          </small>
                          <small className="saved-stat">
                            본 횟수 {st.seen} · <span className="stat-right">맞힘 {st.right}</span> ·{" "}
                            <span className="stat-wrong">틀림 {st.wrong}</span>
                          </small>
                        </span>
                      </li>
                    );
                  })}
              </ul>
            )
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
