import { useMemo, useState } from "react";
import type { TutorView } from "../tutor/view";
import { MATCH_DONE_CMD } from "../tutor/policy/session";

type Props = { view: TutorView; onSend: (text: string) => void; onClose: () => void };

/**
 * 마무리 — 단어 짝 맞추기. 영어 하나를 누르고 뜻 하나를 누르면 짝이 맞는지 본다.
 * 다 맞추면 수업이 끝난다. 뜻은 「·」 앞(원뜻)만 쓴다 — 해설까지 붙이면 너무 길다.
 */
export function MatchGame({ view, onSend, onClose }: Props) {
  const pairs = view.matchPairs ?? [];
  const meaning = (ko: string) => ko.split(" · ")[0]!;
  const right = useMemo(
    () => [...pairs].map((p) => p.en).sort(() => Math.random() - 0.5),
    // 처음 한 번만 섞는다
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );
  const [pick, setPick] = useState<string | null>(null);
  const [done, setDone] = useState<string[]>([]);
  const [miss, setMiss] = useState<string | null>(null);

  function choose(en: string) {
    if (!pick) return;
    if (pick === en) {
      const next = [...done, en];
      setDone(next);
      setPick(null);
      if (next.length === pairs.length) window.setTimeout(() => onSend(MATCH_DONE_CMD), 600);
    } else {
      setMiss(en);
      window.setTimeout(() => setMiss(null), 450);
    }
  }

  return (
    <div className="stage-fill words">
      <header className="words-top">
        <span className="words-step">짝 맞추기 · {done.length} / {pairs.length}</span>
        <button type="button" className="close-soft" title="학습 종료" aria-label="학습 종료" onClick={onClose}>
          ✕
        </button>
      </header>
      <p className="words-title">{view.message}</p>
      <div className="match-grid">
        <div className="match-col">
          {pairs.map((p) => (
            <button
              key={p.en}
              type="button"
              disabled={done.includes(p.en)}
              className={`match-card en${pick === p.en ? " on" : ""}${done.includes(p.en) ? " done" : ""}`}
              onClick={() => setPick(pick === p.en ? null : p.en)}
            >
              {p.en}
            </button>
          ))}
        </div>
        <div className="match-col">
          {right.map((en) => {
            const p = pairs.find((x) => x.en === en)!;
            return (
              <button
                key={en}
                type="button"
                disabled={done.includes(en)}
                className={`match-card ko${done.includes(en) ? " done" : ""}${miss === en ? " miss" : ""}`}
                onClick={() => choose(en)}
              >
                {meaning(p.ko)}
              </button>
            );
          })}
        </div>
      </div>
      <div className="words-dock">
        <button type="button" className="match-skip" onClick={() => onSend(MATCH_DONE_CMD)}>
          그만하고 끝낼게요
        </button>
      </div>
    </div>
  );
}
