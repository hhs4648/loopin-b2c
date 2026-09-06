import { useEffect, useState, type ReactNode } from "react";
import { TeacherFigure } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { InputBar } from "./InputBar";
import type { TutorView } from "../tutor/engine";
import { glossSpans, glossesFor } from "../tutor/glosses";
import { nounKind } from "../tutor/proper-nouns";

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
        <GlossSentence sentence={view.sentence} nouns={view.properNouns} glosses={view.glosses} />
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
          <span>단어를 누르면 뜻이 나와요 · {words} words</span>
        </div>
      </div>

      <div className="study-stage">
        <div className="teacher-bubble study-bubble-over" aria-live="polite">
          <div className={`bubble-card${view.effect === "light" ? " lit" : ""}`}>
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

function GlossSentence({
  sentence,
  nouns,
  glosses,
}: {
  sentence: string;
  nouns: TutorView["properNouns"];
  glosses: TutorView["glosses"];
}) {
  const [open, setOpen] = useState<number | null>(null);
  const spans = glossSpans(sentence, glossesFor(glosses, nouns));

  useEffect(() => {
    setOpen(null);
  }, [sentence]);

  useEffect(() => {
    function close(e: MouseEvent) {
      if (!(e.target instanceof Element) || !e.target.closest(".english")) setOpen(null);
    }
    document.addEventListener("click", close);
    return () => document.removeEventListener("click", close);
  }, []);

  const parts: ReactNode[] = [];
  spans.forEach((span, i) => {
    if (!span.gloss) {
      parts.push(span.text);
      return;
    }
    const noun = nouns.some(
      (n) => n.en === span.gloss!.en || n.en.replace(/\.$/, "") === span.text.replace(/\.$/, ""),
    );
    const selected = open === i;
    parts.push(
      <span key={i} className={`english-token${selected ? " open" : ""}`}>
        <button
          type="button"
          className={`english-word${noun ? " noun-mark" : ""}`}
          aria-expanded={selected}
          aria-label={`${span.text}, ${span.gloss.ko}`}
          onClick={(e) => {
            e.stopPropagation();
            setOpen(selected ? null : i);
          }}
        >
          {span.text}
        </button>
        {selected ? (
          <span className="gloss-tip" role="tooltip">
            {span.gloss.ko}
          </span>
        ) : null}
      </span>,
    );
  });

  return <p className="english">{parts}</p>;
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
