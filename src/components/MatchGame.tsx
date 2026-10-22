import { useEffect, useMemo, useState } from "react";
import type { TutorView } from "../tutor/view";
import { MATCH_DONE_CMD } from "../tutor/policy/session";
import { recordQuest } from "../tutor/quest";
import { speak } from "../tutor/teacher";

type Props = { view: TutorView; onSend: (text: string) => void; onClose: () => void };

/** 짝 하나에 1초 — 8쌍이면 8초 (2026-10-22 선생님 「각 짝마다 1초」) */
const SECONDS_PER_PAIR = 1;
/** 잘못 누른 것을 봐주는 횟수 (목숨 하트) */
const LIVES = 3;

type Phase = "offer" | "bye" | "study" | "play" | "won" | "lost";

/** 진짜로 섞는다 — sort(() => random)은 브라우저에 따라 거의 안 섞인다(아이폰에서 순서 그대로였다). 원래 순서면 한 칸 돌린다 */
function shuffle(list: string[]): string[] {
  const out = [...list];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j]!, out[i]!];
  }
  if (out.length > 1 && out.every((x, i) => x === list[i])) out.push(out.shift()!);
  return out;
}

/**
 * 마무리 — 추가 퀘스트: 단어 짝 맞추기 (2026-10-22 선생님).
 * 그냥 「짝을 맞춰 봐」가 아니라 하고 갈지 고르게 한다. 안 하면 수고 인사 → 끝.
 * 하면 단어를 먼저 외우게 하고 [준비됐어요] → 카드를 섞고, 제한 시간(짝마다 1초) 안에 다 맞추면 성공(친밀도 2배).
 * 잘못 누르면 하트가 하나 줄고, 셋 다 잃거나 시간이 다 되면 실패 — 다시 도전하거나 끝낸다.
 * 뜻은 「·」 앞(원뜻)만 쓴다 — 해설까지 붙이면 너무 길다.
 */
export function MatchGame({ view, onSend, onClose }: Props) {
  const pairs = view.matchPairs ?? [];
  const meaning = (ko: string) => ko.split(" · ")[0]!;
  const limit = pairs.length * SECONDS_PER_PAIR;
  const pairKey = pairs.map((p) => p.en).join("|");

  const [phase, setPhase] = useState<Phase>("offer");
  /** 판마다 새로 섞는다 */
  const [round, setRound] = useState(0);
  const left = useMemo(() => shuffle(pairs.map((p) => p.en)), [pairKey, round]); // eslint-disable-line react-hooks/exhaustive-deps
  const right = useMemo(() => shuffle(pairs.map((p) => p.en)), [pairKey, round]); // eslint-disable-line react-hooks/exhaustive-deps
  const [pick, setPick] = useState<string | null>(null);
  const [done, setDone] = useState<string[]>([]);
  const [miss, setMiss] = useState<string | null>(null);
  const [lives, setLives] = useState(LIVES);
  const [left_ms, setLeftMs] = useState(limit * 1000);
  const [why, setWhy] = useState<"time" | "lives" | null>(null);

  // 시계 — 판이 도는 동안만
  useEffect(() => {
    if (phase !== "play") return;
    const end = Date.now() + limit * 1000;
    const id = window.setInterval(() => {
      const ms = Math.max(0, end - Date.now());
      setLeftMs(ms);
      if (ms === 0) {
        setWhy("time");
        setPhase("lost");
      }
    }, 100);
    return () => window.clearInterval(id);
  }, [phase, round, limit]);

  useEffect(() => {
    if (phase === "won" || phase === "lost") recordQuest({ cleared: phase === "won", pairs: pairs.length, lives, at: new Date().toISOString() });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase]);

  function start() {
    setRound((r) => r + 1);
    setPick(null);
    setDone([]);
    setMiss(null);
    setLives(LIVES);
    setLeftMs(limit * 1000);
    setWhy(null);
    setPhase("play");
  }

  function choose(en: string) {
    if (!pick || phase !== "play") return;
    if (pick === en) {
      const next = [...done, en];
      setDone(next);
      setPick(null);
      if (next.length === pairs.length) setPhase("won");
    } else {
      setMiss(en);
      window.setTimeout(() => setMiss(null), 450);
      const n = lives - 1;
      setLives(n);
      setPick(null);
      if (n <= 0) {
        setWhy("lives");
        setPhase("lost");
      }
    }
  }

  const finish = () => onSend(MATCH_DONE_CMD);
  const say = (text: string) => <p className="words-title">{speak(text)}</p>;

  const header = (
    <header className="words-top">
      <span className="words-step">
        {phase === "play" ? `짝 맞추기 · ${done.length} / ${pairs.length}` : "추가 퀘스트"}
      </span>
      <button type="button" className="close-soft" title="학습 종료" aria-label="학습 종료" onClick={onClose}>
        ✕
      </button>
    </header>
  );

  if (phase === "offer" || phase === "bye") {
    return (
      <div className="stage-fill words">
        {header}
        {phase === "offer" ? say("마지막으로 추가 퀘스트가 있어요. 하고 갈래요?") : say("오늘도 수고했어요! 다음에 또 봐요.")}
        <div className="quest-card">
          <span className="quest-badge">⭐ 추가 퀘스트</span>
          <b className="quest-name">단어 짝 맞추기</b>
          <p className="quest-rule">
            제한 시간 {limit}초 안에 {pairs.length}쌍을 모두 맞추면 <strong>친밀도 2배</strong>!
            <br />
            {speak(`잘못 누르는 건 ${LIVES}번까지 봐줘요.`)}
          </p>
        </div>
        <div className="words-dock">
          {phase === "offer" ? (
            <>
              <button type="button" className="read-continue" onClick={() => setPhase("study")}>
                하고 갈게요
              </button>
              <button type="button" className="match-skip" onClick={() => setPhase("bye")}>
                오늘은 그만할게요
              </button>
            </>
          ) : (
            <button type="button" className="read-continue" onClick={finish}>
              끝내기
            </button>
          )}
        </div>
      </div>
    );
  }

  if (phase === "study") {
    return (
      <div className="stage-fill words">
        {header}
        {say("카드를 섞기 전에 이 단어들을 외워 봐요. 준비됐으면 눌러요~")}
        <ul className="quest-study">
          {pairs.map((p) => (
            <li key={p.en}>
              <b>{p.en}</b>
              <span>{meaning(p.ko)}</span>
            </li>
          ))}
        </ul>
        <div className="words-dock">
          <button type="button" className="read-continue" onClick={start}>
            준비됐어요
          </button>
        </div>
      </div>
    );
  }

  if (phase === "won" || phase === "lost") {
    return (
      <div className="stage-fill words">
        {header}
        {phase === "won"
          ? say("성공! 친밀도 2배예요. 단어 진짜 잘 외웠네요!")
          : say(why === "time" ? "아쉽게도 시간이 다 됐어요. 한 번 더 해 볼까요?" : "아쉽게도 하트를 다 썼어요. 한 번 더 해 볼까요?")}
        <div className={`quest-card${phase === "won" ? " won" : ""}`}>
          <span className="quest-badge">{phase === "won" ? "🎉 퀘스트 성공" : "퀘스트 실패"}</span>
          <b className="quest-name">
            {done.length} / {pairs.length}쌍
          </b>
          {phase === "won" ? <p className="quest-rule">친밀도 2배 획득!</p> : null}
        </div>
        <div className="words-dock">
          {phase === "lost" ? (
            <button type="button" className="read-continue" onClick={() => setPhase("study")}>
              다시 도전할게요
            </button>
          ) : null}
          <button type="button" className={phase === "won" ? "read-continue" : "match-skip"} onClick={finish}>
            끝내기
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="stage-fill words">
      {header}
      <div className="quest-status">
        <span className="quest-lives" aria-label={`남은 하트 ${lives}개`}>
          {Array.from({ length: LIVES }, (_, i) => (i < lives ? "❤️" : "🤍")).join("")}
        </span>
        <span className={`quest-time${left_ms <= 3000 ? " low" : ""}`}>⏱ {(left_ms / 1000).toFixed(1)}초</span>
      </div>
      <div className="quest-bar">
        <i style={{ width: `${(left_ms / (limit * 1000)) * 100}%` }} />
      </div>
      <div className="match-grid" key={round}>
        <div className="match-col">
          {left.map((en) => (
            <button
              key={en}
              type="button"
              disabled={done.includes(en)}
              className={`match-card en shuffle-in${pick === en ? " on" : ""}${done.includes(en) ? " done" : ""}`}
              onClick={() => setPick(pick === en ? null : en)}
            >
              {en}
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
                className={`match-card ko shuffle-in${done.includes(en) ? " done" : ""}${miss === en ? " miss" : ""}`}
                onClick={() => choose(en)}
              >
                {meaning(p.ko)}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
