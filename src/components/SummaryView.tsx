import { useState } from "react";
import type { TutorView } from "../tutor/view";
import { isSaved, loadVocab, toggleVocab, type VocabEntry } from "../tutor/vocab";
import { StudyPanelView } from "./StudyPanel";

type Props = { view: TutorView; lessonId: string; onSend: (text: string) => void; onClose: () => void };

/**
 * 바로 맞힌 학생의 「핵심만 정리」 — 문장 분석 없이, 이 지문에서 챙길 것만 한 화면에.
 * 중요 표현(수업의 💡·❓) → 주요 단어(두 줄, ☆ 누르면 단어장) → 칠판 그림(맨 아래, 눌러서 연다).
 */
export function SummaryView({ view, lessonId, onSend, onClose }: Props) {
  const sum = view.summary!;
  const [vocab, setVocab] = useState<VocabEntry[]>(() => loadVocab());
  // 칠판 그림은 크니까 맨 아래에 접어 두고, 눌러서 연다
  const [showBoard, setShowBoard] = useState(false);
  return (
    <div className="stage-fill words summary">
      <header className="words-top">
        <span className="words-step">핵심 정리</span>
        <button type="button" className="close-soft" title="학습 종료" aria-label="학습 종료" onClick={onClose}>
          ✕
        </button>
      </header>
      <p className="words-title">{sum.title}</p>
      <div className="summary-scroll">
        {sum.expressions.length ? (
          <section className="summary-section">
            <h2>중요 표현</h2>
            <ul className="summary-list">
              {sum.expressions.map((e) => (
                <li key={e.label}>
                  <b>
                    {e.icon} {e.label}
                  </b>
                  <span>{e.text}</span>
                </li>
              ))}
            </ul>
          </section>
        ) : null}
        {sum.words.length ? (
          <section className="summary-section">
            <h2>주요 단어</h2>
            <ul className="summary-words">
              {sum.words.map((w) => {
                const on = isSaved(vocab, w.en);
                return (
                  <li key={w.en}>
                    <button
                      type="button"
                      className={`point-star${on ? " on" : ""}`}
                      aria-pressed={on}
                      aria-label={on ? "단어장에서 빼기" : "단어장에 저장"}
                      onClick={() => setVocab(toggleVocab(vocab, { en: w.en, ko: w.ko, sentence: "", source: lessonId }))}
                    >
                      {on ? "★" : "☆"}
                    </button>
                    <span className="summary-en">{w.en}</span>
                    <span className="summary-ko">{w.ko}</span>
                  </li>
                );
              })}
            </ul>
          </section>
        ) : null}
        {sum.board ? (
          <section className="summary-section">
            <button type="button" className={`summary-board-toggle${showBoard ? " on" : ""}`} aria-expanded={showBoard} onClick={() => setShowBoard(!showBoard)}>
              {showBoard ? "칠판 그림 접기" : "칠판 그림 보기"}
            </button>
            {showBoard ? <StudyPanelView panel={sum.board} /> : null}
          </section>
        ) : null}
      </div>
      <div className="words-dock">
        {view.buttons.map((label) => (
          <button key={label} type="button" className="read-continue" onClick={() => onSend(label)}>
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}
