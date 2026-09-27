import { useEffect, useLayoutEffect, useRef, useState, type ReactNode } from "react";
import { TeacherFigure } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { InputBar } from "./InputBar";
import type { TutorView } from "../tutor/engine";
import { glossSpans, glossesFor } from "../tutor/glosses";
import { nounKind } from "../tutor/proper-nouns";
import { isSaved, loadVocab, toggleVocab, type VocabEntry } from "../tutor/vocab";
import type { UiObservation } from "../tutor/policy/types";
import { StudyPanelView } from "./StudyPanel";

type Props = {
  view: TutorView;
  typing: boolean;
  onSend: (text: string) => void;
  onBack: () => void;
  onClose: () => void;
  /** 턴이 아닌 관찰(단어를 눌러 봄)을 세션에 알린다. 예전 레슨에는 없다 */
  onObserve?: (observation: UiObservation) => void;
};

export function SentenceStudy({ view, typing, onSend, onBack, onClose, onObserve }: Props) {
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
    <div className={`stage-fill study${view.panel ? " has-panel" : ""}`}>
      <header className="study-top">
        <button type="button" className="icon-btn light" title="이전" onClick={onBack}>
          <BackIcon />
        </button>
        <div className="study-progress">
          <span>
            {view.progressLabel ?? "문장 학습"} · {view.progressIndex} / {view.progressTotal}
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
        <GlossSentence
          sentence={view.sentence}
          nouns={view.properNouns}
          glosses={view.glosses}
          highlight={view.highlight ?? []}
          emphasis={view.emphasis ?? []}
          onLookup={(word) => onObserve?.({ kind: "vocab_click", word })}
        />
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

      {/*
        눌러야 열리는 배경 설명. 묻지 않은 학생에게 철학 강의를 하지 않는다 —
        궁금한 학생만 누르고, 선생님이 말풍선으로 짧게 답한다.
        지문 칸 밖에 둔다 — 지문 칸은 스크롤이라 그 안에 넣으면 칩이 잘려 안 보인다.
      */}
      {view.helps?.length ? (
        <div className="help-chips">
          {view.helps.map((label) => (
            <button
              key={label}
              type="button"
              className="help-chip"
              disabled={typing}
              onClick={() => onSend(label)}
            >
              {label}
            </button>
          ))}
        </div>
      ) : null}

      {view.panel ? <StudyPanelView panel={view.panel} /> : null}

      <div className="study-stage">
        {/* 지문을 읽는 동안은 할 말이 없다 — 빈 말풍선을 띄우지 않는다 */}
        {typing || view.message ? (
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
        ) : null}
        <div className="study-mascot">
          <div className="teacher-bob">
            <TeacherFigure />
          </div>
        </div>
      </div>

      <div className="study-dock">
        <QuickReplies
          buttons={view.buttons}
          hidden={typing}
          layout={view.buttonLayout}
          aux={view.auxButtons}
          numbered={view.numbered}
          onPick={onSend}
        />
        <InputBar placeholder={view.placeholder} disabled={typing} onSend={onSend} />
      </div>
    </div>
  );
}

function GlossSentence({
  sentence,
  nouns,
  glosses,
  highlight,
  emphasis,
  onLookup,
}: {
  sentence: string;
  nouns: TutorView["properNouns"];
  glosses: TutorView["glosses"];
  highlight: string[];
  emphasis: string[];
  onLookup: (word: string) => void;
}) {
  const [open, setOpen] = useState<number | null>(null);
  const [vocab, setVocab] = useState<VocabEntry[]>(() => loadVocab());
  const tipRef = useRef<HTMLSpanElement>(null);
  const [shift, setShift] = useState(0);
  const spans = glossSpans(sentence, glossesFor(glosses, nouns));
  const marked = highlightRanges(sentence, highlight);

  /*
    뜻 상자는 단어 아래 가운데에 뜬다. 단어가 가장자리에 있으면 상자가 화면 밖으로
    나가 잘리므로, 뜨고 나서 재서 안쪽으로 밀어 넣는다.
  */
  useLayoutEffect(() => {
    setShift(0);
    const tip = tipRef.current;
    const box = tip?.closest(".study-sentence");
    if (!tip || !box) return;
    const t = tip.getBoundingClientRect();
    const b = box.getBoundingClientRect();
    const pad = 12;
    if (t.left < b.left + pad) setShift(b.left + pad - t.left);
    else if (t.right > b.right - pad) setShift(b.right - pad - t.right);
  }, [open]);

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
  let at = 0;
  spans.forEach((span, i) => {
    const start = at;
    at += span.text.length;
    // 옆 단어에 이미 붙여 그린 문장부호
    if (i > 0 && spans[i - 1]!.gloss && CLOSING.test(span.text)) return;
    if (spans[i + 1]?.gloss && OPENING.test(span.text)) return;
    const hl = marked.some(([from, to]) => start < to && at > from);
    if (!span.gloss) {
      parts.push(hl ? <mark key={i} className="hl">{span.text}</mark> : span.text);
      return;
    }
    const noun = nouns.some(
      (n) => n.en === span.gloss!.en || n.en.replace(/\.$/, "") === span.text.replace(/\.$/, ""),
    );
    const selected = open === i;
    parts.push(
      <span key={i} className={`english-token${selected ? " open" : ""}${hl ? " hl" : ""}`}>
        {OPENING.test(spans[i - 1]?.text ?? "") ? spans[i - 1]!.text : null}
        <button
          type="button"
          className={`english-word${noun ? " noun-mark" : ""}${emphasis.includes(span.text.replace(/[.,;:]$/, "")) ? " em" : ""}`}
          aria-expanded={selected}
          aria-label={`${span.text}, ${span.gloss.ko}`}
          onClick={(e) => {
            e.stopPropagation();
            if (!selected) onLookup(span.text);
            setOpen(selected ? null : i);
          }}
        >
          {span.text}
        </button>
        {/*
          단어는 inline-block이라 뒤의 쉼표가 혼자 다음 줄 머리로 떨어질 수 있다.
          바로 뒤 문장부호는 같은 칸에 넣어 단어와 같이 다니게 한다.
        */}
        {CLOSING.test(spans[i + 1]?.text ?? "") ? spans[i + 1]!.text : null}
        {selected ? (
          <span
            ref={tipRef}
            className="gloss-tip"
            role="tooltip"
            style={shift ? { transform: `translateX(calc(-50% + ${shift}px))` } : undefined}
          >
            {/* 별표 = 단어장에 넣기. 뜻 왼쪽, 빈 별에서 누르면 노랗게 찬다 */}
            <button
              type="button"
              className={`vocab-star${isSaved(vocab, span.gloss.en) ? " on" : ""}`}
              aria-pressed={isSaved(vocab, span.gloss.en)}
              aria-label={isSaved(vocab, span.gloss.en) ? "단어장에서 빼기" : "단어장에 저장"}
              onClick={(e) => {
                e.stopPropagation();
                setVocab(toggleVocab(vocab, { en: span.gloss!.en, ko: span.gloss!.ko, sentence }));
              }}
            >
              <StarIcon filled={isSaved(vocab, span.gloss.en)} />
            </button>
            <GlossText ko={span.gloss.ko} />
          </span>
        ) : null}
      </span>,
    );
  });

  return <p className="english">{parts}</p>;
}

/** 단어 바로 뒤에 붙는 문장부호 */
const CLOSING = /^[,.;:!?)”’"']$/;
/** 단어 바로 앞에 붙는 문장부호 */
const OPENING = /^[(“‘]$/;

/** 강조할 구절이 문장의 몇 번째 글자부터 몇 번째까지인지 */
function highlightRanges(sentence: string, phrases: string[]): [number, number][] {
  const ranges: [number, number][] = [];
  for (const phrase of phrases) {
    const from = sentence.indexOf(phrase);
    if (from >= 0) ranges.push([from, from + phrase.length]);
  }
  return ranges;
}

/** 「통합, 통일성 · 여기서는 …」 — 뜻은 진하게, 「·」 뒤의 해설은 연하게 */
function GlossText({ ko }: { ko: string }) {
  const at = ko.indexOf(" · ");
  if (at < 0) return <span className="gloss-ko">{ko}</span>;
  return (
    <span className="gloss-ko">
      {ko.slice(0, at)}
      <span className="gloss-note"> · {ko.slice(at + 3)}</span>
    </span>
  );
}

function StarIcon({ filled }: { filled: boolean }) {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill={filled ? "currentColor" : "none"} stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round">
      <path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1.1 5.9L12 17l-5.3 2.7 1.1-5.9-4.3-4.1 5.9-.8z" />
    </svg>
  );
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
