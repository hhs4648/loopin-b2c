import { useMemo, useState } from "react";
import { MatchKo } from "./MatchKo";
import { markPracticed, practiceGroups, practiceSentences, practicedKeys, recommendedOrder, type PracticeSentence } from "../tutor/sentencePractice";

/**
 * 연습실 · 문장 — 해석 맞추기만 모아서.
 * 문장을 쭉 나열하면 압박감이 든다 (2026-10-20 선생님) — 연도 → 시험(월)별로 **연습할 문장 수와 본 비율**만 보이고,
 * 「연습 시작」을 누르면 추천 순(안 본 것 먼저)으로 한 문장씩. 끝까지 맞추면 본 문장으로 기록된다.
 */
export function SentencePractice() {
  const [gen, setGen] = useState(0);
  const all = useMemo(() => practiceSentences(), []);
  const practiced = useMemo(() => practicedKeys(), [gen]); // eslint-disable-line react-hooks/exhaustive-deps
  const groups = useMemo(() => practiceGroups(all, practiced), [all, practiced]);
  const [queue, setQueue] = useState<{ list: PracticeSentence[]; at: number; label: string } | null>(null);

  if (!all.length) {
    return <p className="saved-empty">아직 연습할 문장이 없어요. 10분 모의고사를 풀고 틀린 문제를 분석하면 그 지문의 문장이 여기 모여요.</p>;
  }
  if (queue && queue.list[queue.at]) {
    const item = queue.list[queue.at]!;
    return (
      <MatchOne
        key={item.key}
        item={item}
        index={queue.at}
        total={queue.list.length}
        label={queue.label}
        onDone={() => {
          markPracticed(item.key);
          setGen((n) => n + 1);
        }}
        onNext={() => setQueue(queue.at + 1 < queue.list.length ? { ...queue, at: queue.at + 1 } : null)}
        onClose={() => setQueue(null)}
      />
    );
  }

  const seenAll = Object.keys(practiced).filter((k) => all.some((p) => p.key === k)).length;
  const start = (list: PracticeSentence[], label: string) => setQueue({ list: recommendedOrder(list, practiced), at: 0, label });

  let year = 0;
  return (
    <>
      <p className="mini-sub">연습할 문장 {all.length}개 중 {seenAll}개 봤어요 · 안 본 문장부터 추천 순으로 나와요</p>
      <button type="button" className="read-continue vtest-start" onClick={() => start(all, "추천 순")}>
        연습 시작 · 추천 순
      </button>
      <div className="course sp-groups">
        {groups.map((g) => {
          const divider = g.year !== year ? ((year = g.year), <div key={`y${g.year}`} className="course-year"><span>{g.year}년</span></div>) : null;
          const pct = g.sentences.length ? Math.round((g.seen / g.sentences.length) * 100) : 0;
          const wrong = g.sentences.filter((p) => p.reason !== "본 지문").length;
          return (
            <div key={g.collectionId} className="sp-group-wrap">
              {divider}
              <div className="course-exam sp-group">
                <div className="sp-group-text">
                  <b>{g.title}</b>
                  <small>
                    연습할 문장 {g.sentences.length}개{wrong ? ` (틀린 지문·연습할 문장 ${wrong})` : ""} · 본 문장 {g.seen}/{g.sentences.length} ({pct}%)
                  </small>
                  <span className="plan-bar sp-bar" aria-hidden="true"><i style={{ width: `${pct}%` }} /></span>
                </div>
                <button type="button" className="pill primary sp-go" onClick={() => start(g.sentences, g.title)}>
                  연습
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </>
  );
}

function MatchOne({ item, index, total, label, onDone, onNext, onClose }: {
  item: PracticeSentence; index: number; total: number; label: string; onDone: () => void; onNext: () => void; onClose: () => void;
}) {
  const [found, setFound] = useState<string[]>([]);
  const [wrong, setWrong] = useState(0);
  const [flash, setFlash] = useState<string | null>(null);
  // 칸 번호는 한국어 해석의 { en, ko } 칸만 센 차례 — `MatchKo`·세션과 같은 규칙
  const slots = item.ko.filter((k): k is { en: string; ko: string } => typeof k === "object");
  const done = found.length >= slots.length;
  return (
    <div className="sp-one">
      <p className="home-hello">{label} · {index + 1}/{total} · {item.setTitle} {item.sentenceId}문장 · {item.reason}</p>
      <p className="pack-help">영어 덩어리를 끌어다 맞는 한국어 칸에 놓아요. 누르고 칸을 눌러도 돼요.</p>
      <MatchKo
        sentence={item.text}
        chunks={item.chunks}
        found={found}
        ko={item.ko}
        open={!done}
        onMatch={(slot, chunk) => {
          const target = slots[slot];
          if (!target || found.includes(chunk)) return;
          if (target.en === chunk) {
            const next = [...found, chunk];
            setFound(next);
            setFlash(null);
            if (next.length >= slots.length) onDone();
          } else {
            setWrong((n) => n + 1);
            setFlash(`그 칸은 '${target.ko}'예요. 다른 덩어리를 놓아 봐요.`);
          }
        }}
      />
      {flash && !done ? <p className="sp-flash">{flash}</p> : null}
      {done ? <p className="sp-done">다 맞췄어요!{wrong ? ` (틀린 횟수 ${wrong})` : " 한 번에!"}</p> : null}
      <div className="sp-btns">
        <button type="button" className="pill" onClick={onClose}>목록으로</button>
        <button type="button" className={`pill${done ? " primary" : ""}`} onClick={onNext}>{index + 1 < total ? "다음 문장" : "끝내기"}</button>
      </div>
    </div>
  );
}
