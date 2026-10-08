import { useEffect, useLayoutEffect, useMemo, useRef, useState, type ReactNode } from "react";
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
import { PassageFull } from "./PassageFull";
import { NEXT_SENTENCE_CMD, PICK_CMD, PREV_SENTENCE_CMD } from "../tutor/policy/session";

type Props = {
  view: TutorView;
  typing: boolean;
  onSend: (text: string) => void;
  onBack: () => void;
  onClose: () => void;
  /** 턴이 아닌 관찰(단어를 눌러 봄)을 세션에 알린다. 예전 레슨에는 없다 */
  onObserve?: (observation: UiObservation) => void;
};

const NO_CONCEPTS: NonNullable<TutorView["concepts"]> = [];

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
  /*
    문장 먼저 읽기 — 「다 읽었어요」는 문장 길이만큼(2~6초) 지나서 나타난다.
    바로 눌러 넘기지 못하게, 영어를 한 번은 보게 한다
  */
  const [readWait, setReadWait] = useState(false);
  /*
    읽기가 끝나 문장이 가운데에서 위로 갈 때 「툭」 옮겨 가지 않게 — 옮기기 전 자리를
    기억해 두었다가, 새 자리에서 그만큼 끌어내린 뒤 부드럽게 올려 보낸다 (FLIP)
  */
  // 「듣기 · 단어를 누르면 …」 줄은 처음 몇 화면만 — 칠판 분석이 한 번 나오면 그 뒤로는 치운다
  const [sawBoard, setSawBoard] = useState(false);
  useEffect(() => {
    if (view.panel) setSawBoard(true);
  }, [view.panel]);
  const sentenceTips = useMemo(() => (view.tips ?? []).filter((t) => !t.hint), [view.tips]);
  const hintTips = useMemo(() => (view.tips ?? []).filter((t) => t.hint), [view.tips]);
  const lastTop = useRef<{ top: number; sentence: string } | null>(null);
  const hasPanel = !!view.panel;
  useLayoutEffect(() => {
    const el = sentenceBox.current?.querySelector<HTMLElement>(".english");
    if (!el) return;
    const top = el.getBoundingClientRect().top;
    const prev = lastTop.current;
    lastTop.current = { top, sentence: view.sentence };
    // 같은 문장이 자리만 옮길 때만 (가운데 ↔ 칠판 때문에 위로). 새 문장은 그냥 그 자리에
    if (!prev || prev.sentence !== view.sentence) return;
    const from = prev.top;
    if (Math.abs(from - top) < 4) return;
    if (window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) return;
    el.animate([{ transform: `translateY(${from - top}px)` }, { transform: "translateY(0)" }], {
      duration: 450,
      easing: "cubic-bezier(.2,.8,.2,1)",
    });
  }, [view.readingFirst, hasPanel, view.sentence]);
  useEffect(() => {
    if (!view.readingFirst || !view.readDelayMs) {
      setReadWait(false);
      return;
    }
    setReadWait(true);
    const id = window.setTimeout(() => setReadWait(false), view.readDelayMs);
    return () => window.clearTimeout(id);
  }, [view.readingFirst, view.readDelayMs, view.sentence]);
  // 어휘 문제: 보기의 「문장 보기」로 잠깐 띄운 문장 (보기 id)
  const [peek, setPeek] = useState<string | null>(null);
  // 💡 Tip을 연 동안 문장에서 표시할 단어 (Tip의 `mark`)
  const [tipMark, setTipMark] = useState<string | null>(null);
  const peeked = peek ? view.examSentences?.[peek] : undefined;
  useEffect(() => setPeek(null), [view.sentence, view.progressLabel]);
  /*
    칠판이 크면 긴 문장은 칸 안에서 스크롤된다. 노랗게 칠한 구절이 칸 밖에 숨지 않게
    스텝이 바뀔 때마다 그 구절로 칸만 내려 준다 (화면 전체는 움직이지 않는다)
  */
  const sentenceBox = useRef<HTMLDivElement>(null);
  const highlightKey = (view.highlight ?? []).join("|");
  useEffect(() => {
    const box = sentenceBox.current;
    if (!box) return;
    box.scrollTop = 0;
    const marks = [...box.querySelectorAll<HTMLElement>(tipMark ? ".hl-tip" : ".hl, .hl2, .ul")];
    if (!marks.length) return;
    // 칠한 구절이 처음부터 다 보이면 그대로 둔다. 칸 아래로 숨으면 첫 구절이 위에 오게 내린다
    const boxTop = box.getBoundingClientRect().top;
    const bottom = Math.max(...marks.map((m) => m.getBoundingClientRect().bottom - boxTop));
    if (bottom <= box.clientHeight) return;
    const top = Math.min(...marks.map((m) => m.getBoundingClientRect().top - boxTop));
    box.scrollTop = Math.max(0, top - 12);
  }, [highlightKey, view.sentence, peek, tipMark]);
  // 덩어리를 나누는 슬래시(/)는 단어가 아니다
  const words = view.sentence.trim().split(/\s+/).filter((w) => w !== "/").length;
  const dots = Array.from({ length: view.progressTotal }, (_, i) => i);

  return (
    <div className={`stage-fill study${view.celebrate ? " celebrate" : ""}${view.panel ? " has-panel" : ""}${view.readingFirst ? " reading-first" : ""}`}>
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
            {/* 위쪽은 한 줄로 — 풀이법 단계(①②③)도 따로 줄을 두지 않고 여기 적는다 */}
            {view.progressLabel ??
              (view.methodSteps?.active != null
                ? `${"①②③④"[view.methodSteps.active]} ${view.methodSteps.labels[view.methodSteps.active]}`
                : "문장 학습")}{" "}
            · {view.progressIndex}/{view.progressTotal}
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
        <button type="button" className="close-soft" title="학습 종료" aria-label="학습 종료" onClick={onClose}>
          <CloseIcon />
        </button>
      </header>


      <div className="study-sentence" ref={sentenceBox}>
        {view.sentenceTag && !peeked ? <span className="sentence-no">{view.sentenceTag}</span> : null}
        <GlossSentence
          sentence={peeked?.sentence ?? view.sentence}
          nouns={view.properNouns}
          glosses={peeked?.glosses ?? view.glosses}
          highlight={peeked ? [] : (view.highlight ?? [])}
          underline={peeked ? [peeked.underline] : (view.underline ?? [])}
          highlightAlt={peeked ? [] : (view.highlightAlt ?? [])}
          tipMark={peeked ? null : tipMark}
          pick={peeked ? null : (view.pick ?? null)}
          onPickWord={(w) => !typing && onSend(`${PICK_CMD}${w}`)}
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
        {sawBoard ? null : <div className="listen-row">
          <button type="button" className="listen" onClick={listen}>
            <SpeakerIcon /> 듣기
          </button>
          <span>단어를 누르면 뜻이 나와요 · {words} words</span>
        </div>}
      </div>

      {sentenceTips.length || view.concepts?.length ? (
        <TipChips
          tips={sentenceTips}
          concepts={view.concepts ?? []}
          onMark={setTipMark}
          onHint={() => onObserve?.({ kind: "hint_open" })}
        />
      ) : null}

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
            {/* 힌트는 선생님 말풍선 바로 위 — 질문을 읽다가 바로 누를 수 있게 */}
            {hintTips.length && !typing ? (
              <TipChips
                tips={hintTips}
                concepts={NO_CONCEPTS}
                onMark={setTipMark}
                onHint={() => onObserve?.({ kind: "hint_open" })}
              />
            ) : null}
            <div className={`bubble-card${view.effect === "light" ? " lit" : ""}${view.celebrate ? " cheer" : ""}`}>
              {typing ? (
                <div className="dots"><i /><i /><i /></div>
              ) : (
                <span>
                  {view.message}
                  {view.bubbleNote ? <small className="bubble-note">{view.bubbleNote}</small> : null}
                </span>
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
              <button type="button" className="close-soft" title="닫기" aria-label="닫기" onClick={() => setShowPassage(false)}>
                <CloseIcon />
              </button>
            </div>
            <PassageFull
              given={view.fullPassage.given}
              sentences={view.fullPassage.sentences}
              underline={view.fullPassage.underline}
            />
          </div>
        </div>
      ) : null}

      <div className="study-dock">
        {view.examOptions ? (
          <ExamOptions
            options={view.examOptions}
            glosses={view.examGlosses ?? []}
            peekable={view.examSentences ?? null}
            explain={view.examExplain ?? null}
            peek={peek}
            onPeek={(id) => setPeek(peek === id ? null : id)}
            disabled={typing}
            onPick={onSend}
          />
        ) : null}
        <QuickReplies
          buttons={view.buttons}
          hidden={typing || readWait}
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
  underline,
  highlightAlt,
  tipMark,
  pick,
  onPickWord,
  emphasis,
  faded,
  shaded,
  onLookup,
}: {
  sentence: string;
  nouns: TutorView["properNouns"];
  glosses: TutorView["glosses"];
  highlight: string[];
  underline: string[];
  highlightAlt: string[];
  tipMark: string | null;
  /** 「찾기」 스텝 — 후보 구절을 누르면 고른다 (뜻 대신) */
  pick: TutorView["pick"];
  onPickWord: (word: string) => void;
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
  const markedAlt = highlightRanges(sentence, highlightAlt);
  const markedUl = highlightRanges(sentence, underline);
  const markedTip = tipMark ? wordRanges(sentence, tipMark) : [];
  const candAt = (pick?.candidates ?? []).flatMap((c) => wordRanges(sentence, c).map(([a, b]) => ({ c, a, b })));
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
    const hl2 = !hl && hit(markedAlt);
    const tip = hit(markedTip);
    /*
      흐림 = 빼도 되는 삽입, 음영 = 건너뛰어도 되는 부분. 공백까지 같은 칸으로 감싸야
      음영이 단어마다 끊기지 않고 한 줄로 이어진다.
    */
    const marks = `${hit(fadedAt) ? " faded" : ""}${hit(shadedAt) ? " shaded" : ""}${hit(markedUl) ? " ul" : ""}`;
    if (!span.gloss) {
      if (tip) parts.push(<mark key={i} className={`hl-tip${marks}`}>{span.text}</mark>);
      else if (hl || hl2) parts.push(<mark key={i} className={`${hl ? "hl" : "hl2"}${marks}`}>{span.text}</mark>);
      else if (marks) parts.push(<span key={i} className={marks.trim()}>{span.text}</span>);
      else parts.push(span.text);
      return;
    }
    // 「찾기」 후보 — 점선 상자로, 누르면 고른다
    const cand = candAt.find((x) => start < x.b && at > x.a);
    if (cand && pick) {
      const state = pick.found.includes(cand.c) ? " found" : pick.missed.includes(cand.c) ? " missed" : "";
      parts.push(
        <span key={i} className={`english-token${marks}`}>
          {OPENING.test(spans[i - 1]?.text ?? "") ? spans[i - 1]!.text : null}
          <button
            type="button"
            className={`english-word cand${state}`}
            disabled={!pick.open || !!state}
            onClick={(e) => {
              e.stopPropagation();
              onPickWord(cand.c);
            }}
          >
            {span.text}
          </button>
          {CLOSING.test(spans[i + 1]?.text ?? "") ? spans[i + 1]!.text : null}
        </span>,
      );
      return;
    }
    const noun = nouns.some(
      (n) => n.en === span.gloss!.en || n.en.replace(/\.$/, "") === span.text.replace(/\.$/, ""),
    );
    const selected = open === i;
    parts.push(
      <span
        key={i}
        className={`english-token${selected ? " open" : ""}${hl ? " hl" : ""}${hl2 ? " hl2" : ""}${tip ? " hl-tip" : ""}${marks}`}
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
  onMark,
  onHint,
}: {
  tips: NonNullable<TutorView["tips"]>;
  concepts: NonNullable<TutorView["concepts"]>;
  /** 연 Tip이 문장에서 가리키는 단어 — 닫으면 null */
  onMark: (mark: string | null) => void;
  /** 「힌트」 칩을 열었다 — 세션에 알린다 */
  onHint: () => void;
}) {
  const tips = [
    ...concepts.map((c) => ({ icon: "❓", label: c.en, text: `${c.title} ${c.text}` })),
    ...tipList.map((t) => ({ icon: "💡", ...t })),
  ] as { icon: string; label: string; text: string; mark?: string; hint?: boolean }[];
  const [open, setOpen] = useState<number | null>(null);
  useEffect(() => {
    setOpen(null);
    onMark(null);
  }, [tipList, concepts]); // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div className="tip-chips">
      <div className="tip-row">
        {tips.map((tip, i) => (
          <button
            key={tip.label}
            type="button"
            className={`tip-chip${open === i ? " on" : ""}${tip.hint ? " hint" : ""}`}
            aria-expanded={open === i}
            onClick={() => {
              const next = open === i ? null : i;
              setOpen(next);
              onMark(next == null ? null : (tips[next]!.mark ?? null));
              if (next != null && tips[next]!.hint) onHint();
            }}
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
  peekable,
  peek,
  onPeek,
  explain,
  disabled,
  onPick,
}: {
  options: NonNullable<TutorView["examOptions"]>;
  glosses: WordGloss[];
  /** 어휘 문제 — 보기마다 「문장 보기」를 단다 */
  peekable: TutorView["examSentences"];
  peek: string | null;
  onPeek: (id: string) => void;
  /** 해설만 보는 화면 — 보기를 누르면 해설이 열린다 */
  explain: TutorView["examExplain"];
  disabled: boolean;
  onPick: (label: string) => void;
}) {
  const [ko, setKo] = useState<string[]>([]);
  const [opened, setOpened] = useState<string[]>([]);
  const pick = (o: { id: string; label: string }) => {
    if (disabled) return;
    if (explain) setOpened(opened.includes(o.id) ? opened.filter((x) => x !== o.id) : [...opened, o.id]);
    else onPick(o.label);
  };
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
              className={`exam-option${explain?.[o.id]?.correct ? " is-answer" : ""}`}
              onClick={() => pick(o)}
              onKeyDown={(e) => e.key === "Enter" && pick(o)}
            >
              <span className="exam-num">{NUM[n] ?? o.id}</span>
              <span className="exam-text">{parts}</span>
              {peekable?.[o.id] ? (
                <button
                  type="button"
                  className={`exam-peek${peek === o.id ? " on" : ""}`}
                  aria-pressed={peek === o.id}
                  onClick={(e) => {
                    e.stopPropagation();
                    onPeek(o.id);
                  }}
                >
                  문장 보기
                </button>
              ) : null}
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
            {explain && opened.includes(o.id) ? (
              <div className={`exam-explain${explain[o.id]?.correct ? " right" : ""}`}>
                <b>{explain[o.id]?.correct ? "정답" : "오답"}</b> {explain[o.id]?.text}
              </div>
            ) : null}
          </li>
        );
      })}
    </ol>
  );
}

/** 단어 바로 뒤에 붙는 문장부호 */
const CLOSING = /^[,.;:!?)”’"']$/;
/** 단어 바로 앞에 붙는 문장부호 */
const OPENING = /^[(“‘①②③④⑤]$/;

/** 강조할 구절이 문장의 몇 번째 글자부터 몇 번째까지인지 */
function highlightRanges(sentence: string, phrases: string[]): [number, number][] {
  const ranges: [number, number][] = [];
  for (const phrase of phrases) {
    const from = sentence.indexOf(phrase);
    if (from >= 0) ranges.push([from, from + phrase.length]);
  }
  return ranges;
}

/** 단어 단위로 찾는다 — Tip이 가리키는 「one」이 Nonetheless 안에서 잡히지 않게 */
function wordRanges(sentence: string, word: string): [number, number][] {
  const esc = word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const m = new RegExp(`(?<![A-Za-z])${esc}(?![A-Za-z])`).exec(sentence);
  return m ? [[m.index, m.index + word.length]] : [];
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
