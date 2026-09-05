import type { ReactNode } from "react";
import { TeacherFigure } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { InputBar } from "./InputBar";
import type { TutorView } from "../tutor/engine";

type Props = {
  view: TutorView;
  typing: boolean;
  onSend: (text: string) => void;
  onBack: () => void;
  onClose: () => void;
};

export function SentenceStudy({ view, typing, onSend, onBack, onClose }: Props) {
  function listen() {
    const text = view.sentence;
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US";
    window.speechSynthesis.speak(u);
  }

  const words = view.sentence.trim().split(/\s+/).length;
  const dots = Array.from({ length: view.progressTotal }, (_, i) => i);

  return (
    <div className="stage-fill study">
      <header className="study-top">
        <button type="button" className="icon-btn light" title="이전" onClick={onBack}>
          <BackIcon />
        </button>
        <div className="study-progress">
          <span>
            문장 학습 · {view.progressIndex} / {view.progressTotal}
          </span>
          <div className="dots-bar">
            {dots.map((i) => (
              <i key={i} className={i < view.progressIndex ? "on" : ""} />
            ))}
          </div>
        </div>
        <button type="button" className="icon-btn dark" title="학습 종료" onClick={onClose}>
          <CloseIcon />
        </button>
      </header>

      <div className="study-sentence">
        <p className="english">{highlightNouns(view.sentence, view.properNouns)}</p>
        {view.properNouns.length > 0 ? (
          <div className="noun-chips">
            {view.properNouns.map((n) => (
              <span key={n.en} className="noun-chip">
                {n.en} · {nounKind(n.type)} · 그대로
              </span>
            ))}
          </div>
        ) : null}
        <div className="listen-row">
          <button type="button" className="listen" onClick={listen}>
            <SpeakerIcon /> 듣기
          </button>
          <span>{words} words</span>
        </div>
      </div>

      <div className="study-stage">
        <div className="teacher-bubble study-bubble-over" aria-live="polite">
          <div className="bubble-card">
            {typing ? (
              <div className="dots"><i /><i /><i /></div>
            ) : (
              <span>{view.message}</span>
            )}
            <i className="bubble-tail" />
          </div>
        </div>
        <div className="study-mascot">
          <TeacherFigure />
        </div>
      </div>

      <div className="study-dock">
        <QuickReplies buttons={view.buttons} hidden={typing} onPick={onSend} />
        <InputBar placeholder={view.placeholder} disabled={typing} onSend={onSend} />
      </div>
    </div>
  );
}

function nounKind(type?: string) {
  if (type === "company") return "회사 이름";
  if (type === "place") return "지명";
  if (type === "person") return "사람 이름";
  return "고유명사";
}

function highlightNouns(sentence: string, nouns: TutorView["properNouns"]) {
  if (!nouns.length) return sentence;
  const parts: ReactNode[] = [];
  let rest = sentence;
  let key = 0;
  while (rest.length) {
    let hit: { at: number; len: number; en: string } | null = null;
    for (const n of nouns) {
      const forms = [n.en, n.en.replace(/\.$/, "")].filter(Boolean);
      for (const form of forms) {
        const at = rest.indexOf(form);
                if (at >= 0 && (!hit || at < hit.at || (at === hit.at && form.length > hit.len))) {
                  hit = { at, len: form.length, en: n.en };
                }
      }
    }
    if (!hit) {
      parts.push(rest);
      break;
    }
    if (hit.at > 0) parts.push(rest.slice(0, hit.at));
    parts.push(
      <mark key={key++} className="noun-mark">
        {rest.slice(hit.at, hit.at + hit.len)}
      </mark>,
    );
    rest = rest.slice(hit.at + hit.len);
  }
  return parts;
}

function BackIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 18l-6-6 6-6" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round">
      <path d="M6 6l12 12M18 6L6 18" />
    </svg>
  );
}

function SpeakerIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 5L6 9H3v6h3l5 4z" />
      <path d="M15.5 8.5a5 5 0 0 1 0 7" />
      <path d="M18.5 5.5a9 9 0 0 1 0 13" />
    </svg>
  );
}
