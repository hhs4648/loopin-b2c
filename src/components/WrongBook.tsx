import { useMemo } from "react";
import type { LessonSet } from "../../content/tutor/types";
import { wrongItems, type MiniItem } from "../tutor/mini";
import { getCollection, getSet } from "../tutor/sets";

/**
 * 틀린 문제 모아보기 — 10분 모의고사(복습 포함)에서 **가장 최근에 틀렸거나 안 푼** 문제만 시험별로.
 * 분석으로 가거나, 전부 모아 다시 풀 수 있다(복습 모의고사 `ten-review-book`).
 */
type Props = {
  onBack: () => void;
  onOpenSet: (set: LessonSet) => void;
  onOpenMini: (mockId: string) => void;
};

export const WRONG_BOOK_MOCK = "ten-review-book";

export function WrongBook({ onBack, onOpenSet, onOpenMini }: Props) {
  const items = useMemo(() => wrongItems(), []);
  const groups = useMemo(() => {
    const out = new Map<string, { title: string; rows: { it: MiniItem; set: LessonSet }[] }>();
    for (const it of items) {
      const set = it.lesson ? getSet(it.lesson) : null;
      if (!set) continue;
      const c = getCollection(set.collection);
      const g = out.get(set.collection) ?? { title: c?.title ?? set.collection, rows: [] };
      g.rows.push({ it, set });
      out.set(set.collection, g);
    }
    return [...out.values()];
  }, [items]);

  return (
    <div className="stage-fill saved">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="뒤로" aria-label="뒤로" onClick={onBack}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
            <path d="M15 6l-6 6 6 6" />
          </svg>
        </button>
      </header>
      <div className="saved-body-scroll">
        <p className="home-hello">10분 모의고사에서</p>
        <h1 className="saved-title">틀린 문제</h1>
        {items.length === 0 ? (
          <p className="saved-empty">지금 틀려 있는 문제가 없어요. 10분 모의고사를 풀면 틀린 문제가 여기 모여요.</p>
        ) : (
          <>
            <p className="mini-sub">{items.length}문제 · 다시 풀어서 맞히면 여기서 빠져요</p>
            <button type="button" className="read-continue vtest-start" onClick={() => onOpenMini(WRONG_BOOK_MOCK)}>
              틀린 문제만 다시 풀기 · {Math.min(5, items.length)}문제
            </button>
            {groups.map((g) => (
              <section key={g.title} className="saved-group">
                <h2 className="saved-group-title">{g.title}</h2>
                <ul className="mini-review prep">
                  {g.rows.map(({ it, set }) => (
                    <li key={set.id} className="wrong">
                      <button type="button" className="mini-row" onClick={() => onOpenSet(set)}>
                        <span className="mini-mark">✕</span>
                        <span className="mini-row-text">
                          <b>{it.no}번 · {it.kind}{it.points === 3 ? " [3점]" : ""}</b>
                          <small>{set.subtitle}{it.wrong_rate != null ? ` · 전국 오답률 ${it.wrong_rate}%` : ""} · 다정쌤과 분석하기</small>
                        </span>
                        <span className="mini-chev">›</span>
                      </button>
                    </li>
                  ))}
                </ul>
              </section>
            ))}
          </>
        )}
      </div>
    </div>
  );
}
