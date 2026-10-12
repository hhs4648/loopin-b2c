import { useMemo, useState } from "react";
import { loadVocab, type VocabEntry } from "../tutor/vocab";
import {
  buildQuestions,
  distractorPool,
  loadWordStats,
  pickWords,
  recordAnswer,
  type Question,
} from "../tutor/vocabTest";

type Props = {
  /** 이 단어들로만 본다 (틀린 단어 다시). 없으면 단어장에서 고른다 */
  only?: VocabEntry[];
  onRetry: (words: VocabEntry[]) => void;
  onClose: () => void;
};

/**
 * 단어장 테스트 화면 — 짝 맞추기 · 뜻 고르기 · 문장 빈칸이 번갈아 나온다.
 * 틀리면 첫마디는 「아쉽게도 틀렸어요.」, 정답을 보여 주고 [다음]으로 넘긴다.
 * 끝나면 맞힌 수와 틀린 단어를 보여 주고, 틀린 단어만 다시 볼 수 있다.
 */
export function VocabTest({ only, onRetry, onClose }: Props) {
  const vocab = useMemo(() => loadVocab(), []);
  const questions = useMemo(() => {
    const words = only ?? pickWords(vocab, loadWordStats());
    return buildQuestions(words, distractorPool(vocab));
    // 처음 한 번만 만든다
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const [qi, setQi] = useState(0);
  /** 단어별 이번 테스트 결과 — 한 번이라도 틀리면 틀린 단어 */
  const [result, setResult] = useState<Record<string, boolean>>({});

  function finishQuestion(marks: Record<string, boolean>) {
    for (const [en, ok] of Object.entries(marks)) recordAnswer(en, ok);
    setResult((r) => ({ ...r, ...marks }));
    setQi((i) => i + 1);
  }

  const q = questions[qi];
  const total = Object.keys(result).length;
  const wrongWords = vocab.filter((w) => result[w.en] === false);

  return (
    <div className="stage-fill words vtest">
      <header className="words-top">
        <span className="words-step">
          단어 테스트{q ? ` · ${qi + 1} / ${questions.length}` : ""}
        </span>
        <button type="button" className="close-soft" title="그만하기" aria-label="그만하기" onClick={onClose}>
          ✕
        </button>
      </header>

      {!questions.length ? (
        <>
          <p className="words-title">테스트할 단어가 없어요. 수업 중에 단어를 저장해 보세요.</p>
          <div className="words-dock">
            <button type="button" className="read-continue" onClick={onClose}>단어장으로</button>
          </div>
        </>
      ) : q ? (
        q.kind === "match" ? (
          <MatchRound key={qi} q={q} onDone={finishQuestion} />
        ) : (
          <ChoiceRound key={qi} q={q} onDone={finishQuestion} />
        )
      ) : (
        <>
          <p className="words-title">
            {total}개 중에 {total - wrongWords.length}개 맞혔어요.
            {wrongWords.length ? " 틀린 단어만 한 번 더 볼까요?" : " 다 맞혔어요, 잘했어요!"}
          </p>
          <ul className="words-list">
            {wrongWords.map((w) => (
              <li key={w.en} className="word-row">
                <span className="word-en">{w.en}</span>
                <span className="word-ko">{w.ko.split(" · ")[0]}</span>
              </li>
            ))}
          </ul>
          <div className="words-dock">
            {wrongWords.length ? (
              <button type="button" className="read-continue" onClick={() => onRetry(wrongWords)}>
                틀린 단어 다시 보기
              </button>
            ) : null}
            <button type="button" className={`read-continue${wrongWords.length ? " second" : ""}`} onClick={onClose}>
              단어장으로
            </button>
          </div>
        </>
      )}
    </div>
  );
}

/** 짝 맞추기 한 판. 한 번이라도 잘못 짝지은 단어는 틀린 걸로 센다 */
function MatchRound({
  q,
  onDone,
}: {
  q: Extract<Question, { kind: "match" }>;
  onDone: (marks: Record<string, boolean>) => void;
}) {
  const right = useMemo(() => [...q.pairs].sort(() => Math.random() - 0.5), [q]);
  const [pick, setPick] = useState<string | null>(null);
  const [done, setDone] = useState<string[]>([]);
  const [missed, setMissed] = useState<string[]>([]);
  const [shake, setShake] = useState<string | null>(null);

  function choose(en: string) {
    if (!pick) return;
    if (pick === en) {
      const next = [...done, en];
      setDone(next);
      setPick(null);
      if (next.length === q.pairs.length) {
        const marks = Object.fromEntries(q.pairs.map((p) => [p.en, !missed.includes(p.en)]));
        window.setTimeout(() => onDone(marks), 600);
      }
    } else {
      if (!missed.includes(pick)) setMissed([...missed, pick]);
      setShake(en);
      window.setTimeout(() => setShake(null), 450);
    }
  }

  return (
    <>
      <p className="words-title">영어와 뜻을 짝지어 보세요.</p>
      <div className="match-grid">
        <div className="match-col">
          {q.pairs.map((p) => (
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
          {right.map((p) => (
            <button
              key={p.en}
              type="button"
              disabled={done.includes(p.en)}
              className={`match-card ko${done.includes(p.en) ? " done" : ""}${shake === p.en ? " miss" : ""}`}
              onClick={() => choose(p.en)}
            >
              {p.ko}
            </button>
          ))}
        </div>
      </div>
    </>
  );
}

/** 뜻 고르기 · 문장 빈칸 — 보기 넷 중 하나 */
function ChoiceRound({
  q,
  onDone,
}: {
  q: Exclude<Question, { kind: "match" }>;
  onDone: (marks: Record<string, boolean>) => void;
}) {
  const [chosen, setChosen] = useState<string | null>(null);
  const correct = chosen === q.answer;

  function choose(option: string) {
    if (chosen) return;
    setChosen(option);
    // 맞히면 칭찬만 잠깐 보이고 다음 문제로
    if (option === q.answer) window.setTimeout(() => onDone({ [q.en]: true }), 900);
  }

  return (
    <>
      {q.kind === "meaning" ? (
        <>
          <p className="words-title">이 단어의 뜻은 뭘까요?</p>
          <p className="vtest-word">{q.en}</p>
        </>
      ) : (
        <>
          <p className="words-title">해석을 보고 빈칸에 들어갈 단어를 골라 보세요.</p>
          <div className="vtest-sentence">
            <p className="vtest-en">
              {q.sentence.slice(0, q.at)}
              <span className={`vtest-blank${chosen ? (correct ? " right" : " wrong") : ""}`}>
                {chosen ? q.answer : " ".repeat(8)}
              </span>
              {q.sentence.slice(q.at + q.form.length)}
            </p>
            <p className="vtest-ko">{q.translation}</p>
          </div>
        </>
      )}

      <ul className="words-list vtest-options">
        {q.options.map((o) => {
          const state = !chosen ? "" : o === q.answer ? " right" : o === chosen ? " wrong" : " dim";
          return (
            <li key={o}>
              <button type="button" className={`vtest-option${state}`} disabled={!!chosen} onClick={() => choose(o)}>
                {o}
              </button>
            </li>
          );
        })}
      </ul>

      <div className="words-dock">
        {chosen ? (
          <p className={`vtest-feedback${correct ? " right" : ""}`}>
            {correct ? "맞았어요!" : "아쉽게도 틀렸어요. 초록색이 정답이에요."}
          </p>
        ) : null}
        {chosen && !correct ? (
          <button type="button" className="read-continue" onClick={() => onDone({ [q.en]: false })}>
            다음
          </button>
        ) : null}
      </div>
    </>
  );
}
