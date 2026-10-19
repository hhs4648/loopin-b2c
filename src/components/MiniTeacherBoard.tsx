import { useEffect, useMemo, useState } from "react";
import { clock, type MiniMock } from "../tutor/mini";
import { getDb, getDownloads, watchStudents, type RunLog, type StudentDoc } from "../tutor/miniLog";

const NUM = "①②③④⑤";

/** 학생마다 첫 번째로 끝낸 풀이 — 처음 푼 실력이 지표다 (다시 푼 건 「풀이 수」에만 센다) */
function firstFinished(doc: StudentDoc, mockId: string): RunLog | null {
  const runs = Object.values(doc.runs ?? {})
    .filter((r) => r.mock === mockId && (r.status === "submitted" || r.status === "timeup"))
    .sort((a, b) => a.started_at.localeCompare(b.started_at));
  return runs[0] ?? null;
}

/**
 * 선생님 보기 — 학생 테스트 링크의 지표. 아티팩트 주인에게만 학생 문서가 읽힌다.
 */
export function MiniTeacherBoard({ mock, onBack }: { mock: MiniMock; onBack: () => void }) {
  const [docs, setDocs] = useState<StudentDoc[] | null>(null);
  const [canSave, setCanSave] = useState(false);
  useEffect(() => {
    let stop: (() => void) | null = null;
    let live = true;
    void getDb().then((db) => {
      if (!live) return;
      if (!db) return setDocs([]);
      stop = watchStudents(db, setDocs);
    });
    void getDownloads().then((d) => live && setCanSave(!!d));
    return () => {
      live = false;
      stop?.();
    };
  }, []);

  const rows = useMemo(
    () =>
      (docs ?? [])
        .map((d) => {
          const runs = Object.values(d.runs ?? {}).filter((r) => r.mock === mock.id);
          return { name: d.name || "(이름 없음)", first: firstFinished(d, mock.id), runs };
        })
        .filter((r) => r.runs.length)
        .sort((a, b) => (b.first?.score ?? -1) - (a.first?.score ?? -1)),
    [docs, mock.id],
  );
  const finished = rows.map((r) => r.first).filter((r): r is RunLog => !!r);
  const avg = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0);

  const items = mock.items.map((it) => {
    const logs = finished.map((r) => ({ ans: r.answers[it.no], log: r.items[it.no] }));
    const right = logs.filter((l) => l.ans === it.answer).length;
    const wrongPicks = [1, 2, 3, 4, 5]
      .filter((n) => n !== it.answer)
      .map((n) => ({ n, c: logs.filter((l) => l.ans === n).length }))
      .sort((a, b) => b.c - a.c);
    return {
      it,
      rate: finished.length ? Math.round((right / finished.length) * 100) : null,
      sec: avg(logs.map((l) => l.log?.seconds ?? 0)),
      changed: logs.filter((l) => (l.log?.picks.length ?? 0) > 1).length,
      blank: logs.filter((l) => !l.ans).length,
      // 푸는 중에 정답을 확인한 학생 · 분석 레슨까지 간 학생 (다시 푼 것까지 모든 풀이에서)
      checked: finished.filter((r) => r.checked?.[it.no]).length,
      analyzed: rows.filter((r) => r.runs.some((x) => x.analyzed?.some((a) => a.no === it.no))).length,
      topWrong: wrongPicks[0]?.c ? wrongPicks[0] : null,
    };
  });

  const csv = () => {
    const head = ["이름", "풀이", "상태", "시작", "점수", "맞힌 수", "걸린 초"];
    for (const it of mock.items) head.push(`${it.no}번 답`, `${it.no}번 정오`, `${it.no}번 초`, `${it.no}번 고른 차례`);
    head.push("해설 본 문항", "해석 본 문항", "바로 확인한 문항", "분석 간 문항(초·결과)", "분석 보고 고른 문항", "멈춘 초(분석·일시정지)", "일시정지(시작 후 초·쉰 초)", "모르는 단어(문항:단어)", "형광펜(문항:낱말)");
    const lines = [head];
    for (const r of rows)
      for (const run of r.runs.sort((a, b) => a.started_at.localeCompare(b.started_at))) {
        const line = [r.name, run.run, run.status, run.started_at, String(run.score ?? ""), String(run.correct ?? ""), String(run.seconds)];
        for (const it of mock.items) {
          const a = run.answers[it.no];
          const log = run.items[it.no];
          line.push(a ? String(a) : "", a ? (a === it.answer ? "O" : "X") : "", String(log?.seconds ?? 0), (log?.picks ?? []).join(">"));
        }
        line.push(
          run.reviewed.join(" "),
          run.translated.join(" "),
          Object.entries(run.checked ?? {}).map(([no, c]) => `${no}${c.correct ? "O" : "X"}`).join(" "),
          (run.analyzed ?? []).map((a) => `${a.no}(${a.seconds}초·${a.result})`).join(" "),
          (run.peeked ?? []).map((no) => `${no}${run.answers[no] ? (run.answers[no] === mock.items.find((i) => i.no === no)?.answer ? "O" : "X") : "-"}`).join(" "),
          String(run.paused_seconds ?? 0),
          (run.breaks ?? []).map((b) => `${b.at}(${b.seconds})`).join(" "),
          Object.entries(run.items).flatMap(([no, l]) => (l.unknown ?? []).map((w) => `${no}:${w}`)).join(" "),
          Object.entries(run.items).filter(([, l]) => l.hi?.length).map(([no, l]) => `${no}:${l.hi!.join(" ")}`).join(" / "),
        );
        lines.push(line);
      }
    const text = "﻿" + lines.map((l) => l.map((c) => `"${c.replace(/"/g, '""')}"`).join(",")).join("\n");
    void getDownloads().then((d) =>
      d?.save({ filename: `${mock.id}-결과.csv`, data: new Blob([text], { type: "text/csv" }) }).catch(() => {}),
    );
  };

  return (
    <div className="stage-fill saved mini">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="돌아가기" aria-label="돌아가기" onClick={onBack}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
            <path d="M15 6l-6 6 6 6" />
          </svg>
        </button>
      </header>
      <div className="saved-body-scroll">
        <p className="home-hello">선생님 보기</p>
        <h1 className="saved-title">{mock.title} · 학생 결과</h1>
        {docs == null ? (
          <p className="mini-sub">불러오는 중…</p>
        ) : !rows.length ? (
          <p className="mini-sub">아직 푼 학생이 없어요.</p>
        ) : (
          <>
            <ul className="mini-facts">
              <li><b>{rows.length}명</b><small>시작한 학생 (끝낸 {finished.length}명)</small></li>
              <li><b>{avg(finished.map((r) => r.score ?? 0)).toFixed(1)}</b><small>평균 점수 / {mock.items.reduce((n, it) => n + it.points, 0)}</small></li>
              <li><b>{clock(avg(finished.map((r) => r.seconds)))}</b><small>평균 시간</small></li>
            </ul>
            <p className="mini-sub">문항별·평균은 학생마다 처음 끝낸 풀이로 셉니다.</p>

            <h2 className="group-title">문항별</h2>
            <div className="mini-board-wrap">
              <table className="mini-board">
                <thead>
                  <tr><th>문항</th><th>정답률</th><th>전국 오답률</th><th>평균 시간</th><th>많이 고른 오답</th><th>답 바꿈</th><th>안 풂</th><th>바로 확인</th><th>분석 감</th></tr>
                </thead>
                <tbody>
                  {items.map((x) => (
                    <tr key={x.it.no}>
                      <td><b>{x.it.no}</b> {x.it.kind}</td>
                      <td>{x.rate == null ? "–" : `${x.rate}%`}</td>
                      <td>{x.it.wrong_rate != null ? `${x.it.wrong_rate}%` : "–"}</td>
                      <td>{clock(x.sec)}</td>
                      <td>{x.topWrong ? `${NUM[x.topWrong.n - 1]} ${x.topWrong.c}명` : "–"}</td>
                      <td>{x.changed}명</td>
                      <td>{x.blank}명</td>
                      <td>{x.checked}명</td>
                      <td>{x.analyzed}명</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <h2 className="group-title">학생별</h2>
            <div className="mini-board-wrap">
              <table className="mini-board">
                <thead>
                  <tr><th>이름</th><th>점수</th><th>시간</th><th>문항</th><th>분석</th><th>풀이</th></tr>
                </thead>
                <tbody>
                  {rows.map((r, i) => (
                    <tr key={`${r.name}-${i}`}>
                      <td>{r.name}</td>
                      <td>{r.first ? `${r.first.score}` : "–"}</td>
                      <td>{r.first ? `${clock(r.first.seconds)}${r.first.status === "timeup" ? " ⏱" : ""}` : "–"}</td>
                      <td className="mini-ox">
                        {r.first
                          ? mock.items.map((it) => (r.first!.answers[it.no] === it.answer ? "○" : r.first!.answers[it.no] ? "✕" : "·")).join("")
                          : r.runs.some((x) => x.status === "quit") ? "그만둠" : "푸는 중·닫음"}
                      </td>
                      <td>{r.runs.flatMap((x) => x.analyzed ?? []).map((a) => a.no).join(" ") || "–"}</td>
                      <td>{r.runs.length}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {canSave ? (
              <button type="button" className="mini-start" onClick={csv}>
                CSV로 받기 (풀이마다 한 줄)
              </button>
            ) : null}
          </>
        )}
      </div>
    </div>
  );
}
