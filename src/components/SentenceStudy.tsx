import { useEffect, useLayoutEffect, useRef, useState, type ReactNode } from "react";
import { TeacherFigure } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { InputBar } from "./InputBar";
import type { TutorView } from "../tutor/view";
import type { WordGloss } from "../../content/tutor/types";
import { glossSpans, glossesFor } from "../tutor/glosses";
import { nounKind } from "../tutor/proper-nouns";
import { isSaved, loadVocab, toggleVocab, type VocabEntry } from "../tutor/vocab";
import type { UiObservation } from "../tutor/policy/types";
import { StudyPanelView } from "./StudyPanel";
import { PassagePager } from "./PassagePager";
import { NEXT_SENTENCE_CMD, PREV_SENTENCE_CMD } from "../tutor/policy/session";

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


  const [showPassage, setShowPassage] = useState(false);
  const words = view.sentence.trim().split(/\s+/).length;
  const dots = Array.from({ length: view.progressTotal }, (_, i) => i);

  return (
    <div className={`stage-fill study${view.panel ? " has-panel" : ""}`}>
      <header className="study-top">
        {/*
          지문이 따로 있는 수업은 왼쪽 위가 「전체 지문」이다. 예전 ‹(교실로 돌아가기)는
          돌아올 길이 없어서 눌리면 화면이 갑자기 넘어간 것처럼 보였다.
        */}
        {view.fullPassage ? (
          <button type="button" className="passage-btn" onClick={() => setShowPassage(true)}>
            전체 지문
          </button>
        ) : (
          <button type="button" className="icon-btn light" title="이전" onClick={onBack}>
            <BackIcon />
          </button>
        )}
        <div className="study-progress">
          <span className="progress-line">
            {view.canNextSentence != null && view.fullPassage ? (
              <button
                type="button"
                className="sentence-arrow"
                disabled={!view.canPrevSentence || typing}
                aria-label="이전 문장"
                onClick={() => onSend(PREV_SENTENCE_CMD)}
              >
                ‹
              </button>
            ) : null}
            {view.progressLabel ?? "문장 학습"} · {view.progressIndex} / {view.progressTotal}
            {view.canNextSentence != null && view.fullPassage ? (
              <button
                type="button"
                className="sentence-arrow"
                disabled={!view.canNextSentence || typing}
                aria-label="다음 문장"
                onClick={() => onSend(NEXT_SENTENCE_CMD)}
              >
                ›
              </button>
            ) : null}
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

      {/* 「밑줄 문제 푸는 법」 — 지금 어느 단계인지 */}
      {view.methodSteps ? (
        <ol className="method-steps">
          {view.methodSteps.labels.map((label, i) => (
            <li key={label} className={view.methodSteps!.active === i ? "on" : ""}>
              <b>{"①②③④"[i]}</b> {label}
            </li>
          ))}
        </ol>
      ) : null}

      <div className="study-sentence">
        <GlossSentence
          sentence={view.sentence}
          nouns={view.properNouns}
          glosses={view.glosses}
          highlight={view.highlight ?? []}
          emphasis={view.emphasis ?? []}
          faded={view.faded ?? []}
          shaded={view.shaded ?? []}
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

      {view.tips?.length || view.concepts?.length ? <TipChips tips={view.tips ?? []} concepts={view.concepts ?? []} /> : null}

      {view.panel ? (
        <StudyPanelView
          panel={view.panel}
          // 끌어 넣기는 지금 고를 수 있는 보기일 때만 — 답한 뒤의 화면에서는 칩을 치운다
          onPick={
            !typing && view.panel.kind === "groups" && view.panel.sort && view.buttons.includes(view.panel.sort.right)
              ? onSend
              : undefined
          }
        />
      ) : null}

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

      {showPassage && view.fullPassage ? (
        <div className="passage-overlay" role="dialog" aria-label="전체 지문">
          <div className="passage-sheet">
            <div className="passage-sheet-top">
              <b>전체 지문</b>
              <button type="button" className="icon-btn dark" title="닫기" onClick={() => setShowPassage(false)}>
                <CloseIcon />
              </button>
            </div>
            <PassagePager
              sentences={view.fullPassage.sentences}
              underline={view.fullPassage.underline}
              start={0}
            />
          </div>
        </div>
      ) : null}

      <div className="study-dock">
        {view.examOptions ? (
          <ExamOptions
            options={view.examOptions}
            glosses={view.examGlosses ?? []}
            disabled={typing}
            onPick={onSend}
          />
        ) : null}
        <QuickReplies
          buttons={view.buttons}
          hidden={typing}
          layout={view.buttonLayout}
          aux={view.auxButtons}
          numbered={view.numbered}
          onPick={onSend}
        />
        {view.allowInput === false ? null : (
          <InputBar placeholder={view.placeholder} disabled={typing} onSend={onSend} />
        )}
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
  faded,
  shaded,
  onLookup,
}: {
  sentence: string;
  nouns: TutorView["properNouns"];
  glosses: TutorView["glosses"];
  highlight: string[];
  emphasis: string[];
  faded: string[];
  shaded: string[];
  onLookup: (word: string) => void;
}) {
  const [open, setOpen] = useState<number | null>(null);
  const [vocab, setVocab] = useState<VocabEntry[]>(() => loadVocab());
  const tipRef = useRef<HTMLSpanElement>(null);
  const [shift, setShift] = useState(0);
  const spans = glossSpans(sentence, glossesFor(glosses, nouns));
  const marked = highlightRanges(sentence, highlight);
  const fadedAt = highlightRanges(sentence, faded);
  const shadedAt = highlightRanges(sentence, shaded);

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
    const hit = (ranges: [number, number][]) => ranges.some(([from, to]) => start < to && at > from);
    const hl = hit(marked);
    /*
      흐림 = 빼도 되는 삽입, 음영 = 건너뛰어도 되는 부분. 공백까지 같은 칸으로 감싸야
      음영이 단어마다 끊기지 않고 한 줄로 이어진다.
    */
    const marks = `${hit(fadedAt) ? " faded" : ""}${hit(shadedAt) ? " shaded" : ""}`;
    if (!span.gloss) {
      if (hl) parts.push(<mark key={i} className={`hl${marks}`}>{span.text}</mark>);
      else if (marks) parts.push(<span key={i} className={marks.trim()}>{span.text}</span>);
      else parts.push(span.text);
      return;
    }
    const noun = nouns.some(
      (n) => n.en === span.gloss!.en || n.en.replace(/\.$/, "") === span.text.replace(/\.$/, ""),
    );
    const selected = open === i;
    parts.push(
      <span
        key={i}
        className={`english-token${selected ? " open" : ""}${hl ? " hl" : ""}${marks}`}
      >
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

/**
 * 문장 아래 칩 — ❓ 개념(단어 하나로 안 되는 말)과 💡 요령. 누르면 아래에 참고 설명이 열린다.
 * 선생님 말이 아니라 참고 정보. (❓는 예전엔 단어 위에 붙였는데 자리를 너무 차지했다)
 */
function TipChips({
  tips: tipList,
  concepts,
}: {
  tips: NonNullable<TutorView["tips"]>;
  concepts: NonNullable<TutorView["concepts"]>;
}) {
  const tips = [
    ...concepts.map((c) => ({ icon: "❓", label: c.en, text: `${c.title} ${c.text}` })),
    ...tipList.map((t) => ({ icon: "💡", ...t })),
  ];
  const [open, setOpen] = useState<number | null>(null);
  useEffect(() => setOpen(null), [tipList, concepts]);
  return (
    <div className="tip-chips">
      <div className="tip-row">
        {tips.map((tip, i) => (
          <button
            key={tip.label}
            type="button"
            className={`tip-chip${open === i ? " on" : ""}`}
            aria-expanded={open === i}
            onClick={() => setOpen(open === i ? null : i)}
          >
            {tip.icon} {tip.label}
          </button>
        ))}
      </div>
      {open != null ? <div className="info-pop">{tips[open]!.text}</div> : null}
    </div>
  );
}

/**
 * 시험 보기 — 영어만 먼저. 핵심 단어는 색칠하고, 단어를 누르면 뜻, ▸를 누르면
 * 보기 아래에 짧은 한국어. 보기(카드)를 누르면 그걸 답으로 고른 것이다.
 */
function ExamOptions({
  options,
  glosses,
  disabled,
  onPick,
}: {
  options: NonNullable<TutorView["examOptions"]>;
  glosses: WordGloss[];
  disabled: boolean;
  onPick: (label: string) => void;
}) {
  const [ko, setKo] = useState<string[]>([]);
  const [word, setWord] = useState<{ id: string; gloss: WordGloss } | null>(null);
  const NUM = "①②③④⑤";
  return (
    <ol className="exam-options">
      {options.map((o) => {
        const ranges = highlightRanges(o.label, o.keywords);
        let at = 0;
        const parts = glossSpans(o.label, glosses).map((span, i) => {
          const start = at;
          at += span.text.length;
          const kw = ranges.some(([a, b]) => start < b && at > a);
          if (!span.gloss) return kw ? <b key={i} className="kw">{span.text}</b> : span.text;
          const g = span.gloss;
          return (
            <button
              key={i}
              type="button"
              className={`exam-word${kw ? " kw" : ""}`}
              onClick={(e) => {
                e.stopPropagation();
                setWord(word?.id === o.id && word.gloss.en === g.en ? null : { id: o.id, gloss: g });
              }}
            >
              {span.text}
            </button>
          );
        });
        const n = Number(o.id) - 1;
        return (
          <li key={o.id}>
            <div
              role="button"
              tabIndex={0}
              aria-disabled={disabled}
              className="exam-option"
              onClick={() => !disabled && onPick(o.label)}
              onKeyDown={(e) => e.key === "Enter" && !disabled && onPick(o.label)}
            >
              <span className="exam-num">{NUM[n] ?? o.id}</span>
              <span className="exam-text">{parts}</span>
              {o.ko ? (
                <button
                  type="button"
                  className={`exam-ko-toggle${ko.includes(o.id) ? " on" : ""}`}
                  aria-label="한국어로 보기"
                  aria-expanded={ko.includes(o.id)}
                  onClick={(e) => {
                    e.stopPropagation();
                    setKo(ko.includes(o.id) ? ko.filter((x) => x !== o.id) : [...ko, o.id]);
                  }}
                >
                  ▸
                </button>
              ) : null}
            </div>
            {word?.id === o.id ? (
              <div className="exam-gloss">
                <b>{word.gloss.en}</b> <GlossText ko={word.gloss.ko} />
              </div>
            ) : null}
            {ko.includes(o.id) ? <div className="exam-ko">{o.ko}</div> : null}
          </li>
        );
      })}
    </ol>
  );
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
