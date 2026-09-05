import { ClassroomBg } from "./ClassroomBg";
import { TeacherFigure } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { InputBar } from "./InputBar";
import type { TutorView } from "../tutor/engine";

type Props = {
  view: TutorView;
  elapsed: string;
  typing: boolean;
  onSend: (text: string) => void;
  onClose: () => void;
};

export function ClassroomChat({ view, elapsed, typing, onSend, onClose }: Props) {
  return (
    <div className="stage-fill">
      <ClassroomBg />
      <header className="top-bar">
        <div className="chip">
          <span className="avatar">다</span>
          <div className="chip-text">
            <strong>다정쌤</strong>
            <small>오늘의 학습 · 1단계</small>
          </div>
        </div>
        <div className="top-right">
          <div className="timer">
            <i className="live-dot" />
            {elapsed}
          </div>
          <button type="button" className="icon-btn dark" title="학습 종료" onClick={onClose}>
            <CloseIcon />
          </button>
        </div>
      </header>

      <div className="teacher-full">
        <div className="teacher-bob">
          <TeacherFigure />
        </div>
      </div>

      <div className="teacher-bubble">
          <div className="bubble-card" aria-live="polite">
          {typing ? <TypingDots /> : <span>{view.message}</span>}
          <i className="bubble-tail" />
        </div>
      </div>

      {view.studentLine ? (
        <div className="student-bubble">{view.studentLine}</div>
      ) : null}

      <div className="dock">
        {view.properNouns.length > 0 && !view.ended ? (
          <div className="noun-chips intro">
            {view.properNouns.map((n) => (
              <span key={n.en} className="noun-chip">
                {n.en} · 회사 이름 · 그대로
              </span>
            ))}
          </div>
        ) : null}
        <QuickReplies buttons={view.buttons} hidden={typing || view.ended} onPick={onSend} />
        {view.ended ? (
          <button type="button" className="pill restart" onClick={onClose}>
            다시 시작
          </button>
        ) : (
          <InputBar placeholder={view.placeholder} disabled={typing} onSend={onSend} />
        )}
      </div>
    </div>
  );
}

function TypingDots() {
  return (
    <div className="dots">
      <i />
      <i />
      <i />
    </div>
  );
}

function CloseIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round">
      <path d="M6 6l12 12M18 6L6 18" />
    </svg>
  );
}
