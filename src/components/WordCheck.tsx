import type { TutorView } from "../tutor/view";
import { CHECK_CMD } from "../tutor/policy/session";

type Props = { view: TutorView; onSend: (text: string) => void; onClose: () => void };

/**
 * 마무리 — 주요 단어 체크. 본문 단어와 보기 단어를 한 화면에 하나씩 나눠 보여 준다.
 * 모르는 단어를 체크하면 단어장으로 간다 (어느 지문에서 나왔는지 같이).
 */
export function WordCheck({ view, onSend, onClose }: Props) {
  const w = view.wordCheck!;
  return (
    <div className="stage-fill words">
      <header className="words-top">
        <span className="words-step">{w.step}</span>
        <button type="button" className="icon-btn dark" title="학습 종료" onClick={onClose}>
          ✕
        </button>
      </header>
      <p className="words-title">{w.title}</p>
      <ul className="words-list">
        {w.words.map((g) => {
          const on = w.checked.includes(g.en);
          return (
            <li key={g.en}>
              <button
                type="button"
                className={`word-row${on ? " on" : ""}`}
                aria-pressed={on}
                onClick={() => onSend(`${CHECK_CMD}${g.en}`)}
              >
                <span className="word-box" aria-hidden="true">{on ? "✓" : ""}</span>
                <span className="word-en">{g.en}</span>
                <span className="word-ko">{g.ko}</span>
              </button>
            </li>
          );
        })}
      </ul>
      <div className="words-dock">
        <span className="words-count">모르는 단어 {w.checked.length}개 체크</span>
        {view.buttons.map((label) => (
          <button key={label} type="button" className="read-continue" onClick={() => onSend(label)}>
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}
