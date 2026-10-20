import { useMemo } from "react";
import type { LessonSet } from "../../content/tutor/types";
import { allCollections, setsIn } from "../tutor/sets";
import { kindStats, seenBySet } from "../tutor/seen";
import { kindOfSet, pointsOfSet } from "../tutor/tenmin";

/**
 * 진도표 — 시험(연도)마다 어떤 문제를 봤고 안 봤는지 한눈에 + 자주 틀리는 유형 (2026-10-20 선생님).
 *
 * 문제 하나가 칸 하나: 안 봄(연한 회색) · 맞힘(초록) · 틀림(빨강) · 보기만 함(파랑). 3점은 칸 위 작은 「3」.
 * 기록은 분석 수업·미니 모의고사·10분 모의고사를 모두 합친 것(`seen.ts`).
 */

type Props = {
  onBack: () => void;
  /** 칸을 누르면 그 문제의 분석 수업으로 */
  onOpenSet: (set: LessonSet) => void;
};

const no = (s: LessonSet) => Number(/(\d+)번/.exec(s.title)?.[1] ?? 0);

export function ProgressBoard({ onBack, onOpenSet }: Props) {
  const rows = useMemo(() => seenBySet(), []);
  const kinds = useMemo(() => kindStats(rows), [rows]);
  const exams = allCollections()
    .filter((c) => c.exam)
    .sort((a, b) => b.exam!.held.localeCompare(a.exam!.held));
  const all = exams.flatMap((c) => setsIn(c.id)).filter((s) => !/-v\d+$/.test(s.id));
  const seenCount = all.filter((s) => rows[s.id]?.seen).length;
  const weak = kinds.filter((k) => k.answered >= 2 && k.rate >= 0.5).slice(0, 3);

  return (
    <div className="stage-fill saved board">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="뒤로" aria-label="뒤로" onClick={onBack}>
          <BackIcon />
        </button>
      </header>
      <div className="saved-body-scroll">
        <p className="home-hello">본 문제 · 안 본 문제</p>
        <h1 className="saved-title">진도표</h1>
        <p className="mini-sub">
          {all.length}문제 중 {seenCount}개 봤어요 · 칸을 누르면 그 문제 분석으로
        </p>

        <div className="board-legend">
          <span><i className="ok" />맞힘</span>
          <span><i className="ng" />틀림</span>
          <span><i className="seen" />보기만 함</span>
          <span><i />안 봄</span>
          <span>[3] 3점</span>
        </div>

        {kinds.length ? (
          <section className="board-kinds">
            <h2 className="group-title">자주 틀리는 유형</h2>
            {weak.length ? (
              <p className="board-weak">
                {weak.map((k) => <b key={k.kind}>{k.kind}</b>)} — 이 유형을 자주 틀려요. 코스에서 이 유형이 나오면 「분석 먼저」로 풀어 봐요
              </p>
            ) : (
              <p className="board-weak">아직 뚜렷하게 자주 틀리는 유형은 없어요. 좋아요!</p>
            )}
            <ul className="board-kind-list">
              {kinds.map((k) => (
                <li key={k.kind} className={k.answered >= 2 && k.rate >= 0.5 ? "weak" : ""}>
                  <span className="kind">{k.kind}</span>
                  <span className="bar" aria-hidden="true"><i style={{ width: `${Math.round(k.rate * 100)}%` }} /></span>
                  <span className="num">{k.answered}번 중 {k.wrong}번 틀림</span>
                </li>
              ))}
            </ul>
          </section>
        ) : (
          <p className="board-weak">아직 답을 낸 문제가 없어요. 10분 모의고사를 한 회 풀면 유형별로 보여 드릴게요.</p>
        )}

        {exams.map((c) => {
          const sets = setsIn(c.id).filter((s) => !/-v\d+$/.test(s.id)).sort((a, b) => no(a) - no(b));
          if (!sets.length) return null;
          const seen = sets.filter((s) => rows[s.id]?.seen).length;
          return (
            <section key={c.id} className="board-exam">
              <h2 className="group-title">
                {c.title}
                <small>{seen}/{sets.length} 봄 · {c.subtitle.split(" · ")[0]}</small>
              </h2>
              <div className="board-grid">
                {sets.map((s) => {
                  const r = rows[s.id];
                  const state = !r?.seen ? "" : r.latest == null ? " seen" : r.latest ? " ok" : " ng";
                  const pts = pointsOfSet(s);
                  return (
                    <button
                      key={s.id}
                      type="button"
                      className={`board-cell${state}`}
                      title={`${s.title} · ${kindOfSet(s)} · ${pts}점${r ? (r.latest == null ? " · 보기만 함" : r.latest ? " · 최근 맞힘" : " · 최근 틀림") : " · 안 봄"}`}
                      onClick={() => onOpenSet(s)}
                    >
                      <span>{no(s)}{pts === 3 ? <em>[3]</em> : null}</span>
                      <small>{kindOfSet(s)}</small>
                    </button>
                  );
                })}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}

function BackIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 6l-6 6 6 6" />
    </svg>
  );
}
