import { useState } from "react";
import type { TutorView } from "../tutor/view";
import { isNoteSaved, loadNotes, toggleNote, type NoteEntry } from "../tutor/notes";
import { speak } from "../tutor/teacher";

type Props = { view: TutorView; onSend: (text: string) => void; onClose: () => void };

/**
 * 마무리 — 오늘 헷갈렸던 곳. 틀렸거나 힌트·설명을 본 질문만 모아 한 줄씩 정리한다.
 * 별표를 누르면 노트에 저장된다 (단어장 별표와 같은 모양).
 */
export function PointsReview({ view, onSend, onClose }: Props) {
  const p = view.pointsReview!;
  const [notes, setNotes] = useState<NoteEntry[]>(() => loadNotes());
  return (
    <div className="stage-fill words points">
      <header className="words-top">
        <span className="words-step">헷갈린 포인트</span>
        <button type="button" className="close-soft" title="학습 종료" aria-label="학습 종료" onClick={onClose}>
          ✕
        </button>
      </header>
      {view.smallScore ? (
        <div className="small-score">
          <b>작은 문제 {view.smallScore.total}개 중 {view.smallScore.right}개</b> 맞혔어요
          {view.smallScore.right === view.smallScore.total ? " 🎉" : ""}
        </div>
      ) : null}
      <p className="words-title">{p.items.length ? p.title : speak("헷갈린 곳 없이 다 맞혔어요!")}</p>
      <ul className="words-list">
        {p.items.map((item) => {
          const on = isNoteSaved(notes, { lessonId: p.lessonId, key: item.key });
          return (
            <li key={item.key} className="point-row">
              <button
                type="button"
                className={`point-star${on ? " on" : ""}`}
                aria-pressed={on}
                aria-label={on ? "노트에서 빼기" : "노트에 저장"}
                onClick={() => setNotes(toggleNote(notes, { lessonId: p.lessonId, ...item }))}
              >
                {on ? "★" : "☆"}
              </button>
              <span className="point-body">
                <b>{item.title}</b>
                <span>{item.text}</span>
              </span>
            </li>
          );
        })}
      </ul>
      <div className="words-dock">
        {p.items.length ? <span className="words-count">☆를 누르면 노트에 저장돼요</span> : null}
        {view.buttons.map((label, i) => (
          <button key={label} type="button" className={`read-continue${i < view.buttons.length - 1 ? "" : " second"}`} onClick={() => onSend(label)}>
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}
