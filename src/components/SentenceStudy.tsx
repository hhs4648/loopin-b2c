import { useEffect, useLayoutEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { TeacherFigure, TeacherReaction } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { InputBar } from "./InputBar";
import type { TranslationResult, TutorView } from "../tutor/view";
import { addNote } from "../tutor/notes";
import type { WordGloss } from "../../content/tutor/types";
import { glossSpans, glossesFor, splitPhraseGlosses } from "../tutor/glosses";
import { nounKind } from "../tutor/proper-nouns";
import { isSaved, loadVocab, toggleVocab, type VocabEntry } from "../tutor/vocab";
import { lessonIdOfSentence } from "../tutor/vocabTest";
import type { UiObservation } from "../tutor/policy/types";
import { StudyPanelView } from "./StudyPanel";
import { noteTipOpened, takeTipShow } from "../tutor/tipExposure";
import { BoardDrawer, isBoardPanel } from "./BoardDrawer";
import { PassageFull } from "./PassageFull";
import { MATCH_CMD, NEXT_SENTENCE_CMD, ORDER_CMD, PICK_CMD, PREV_SENTENCE_CMD } from "../tutor/policy/session";
import { MatchKo } from "./MatchKo";
import { OrderBoard } from "./OrderBoard";

type Props = {
  view: TutorView;
  typing: boolean;
  onSend: (text: string) => void;
  onBack: () => void;
  onClose: () => void;
  /** 턴이 아닌 관찰(단어를 눌러 봄)을 세션에 알린다. 예전 레슨에는 없다 */
  onObserve?: (observation: UiObservation) => void;
  /** 온보딩(가입 직후 첫 분석)인가 — 지금은 쓰지 않는다(칠판 안내도 OnboardingCoach가 한다) */
  onboarding?: boolean;
};

const NO_CONCEPTS: NonNullable<TutorView["concepts"]> = [];

export function SentenceStudy({ view, typing, onSend, onBack, onClose, onObserve }: Props) {
  function listen() {
    // 화면에 보이는 빈칸(________)을 그대로 읽으면 "underscore"가 된다. 정답 단어로 읽는다.
    const text = view.speakSentence ?? view.sentence;
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
  // 덩어리 고르기(음영) 화면은 듣기 줄을 빼고, 3초 동안 반응이 없으면 「회색 부분을 눌러 보세요!」
  const shadePick = !!view.pick?.shade && !view.readingFirst;
  const pickUntouched = !!view.pick?.open && !view.pick.match && !view.pick.order && !view.pick.found.length && !view.pick.missed.length;
  const [pickNudge, setPickNudge] = useState(false);
  useEffect(() => {
    setPickNudge(false);
    if (!pickUntouched || typing) return;
    const id = window.setTimeout(() => setPickNudge(true), 3000);
    return () => window.clearTimeout(id);
  }, [pickUntouched, typing, view.sentence, view.message]);
  useEffect(() => {
    if (view.panel) setSawBoard(true);
  }, [view.panel]);
  const sentenceTips = useMemo(() => (view.tips ?? []).filter((t) => !t.hint), [view.tips]);
  const hintTips = useMemo(() => (view.tips ?? []).filter((t) => t.hint), [view.tips]);
  const lastTop = useRef<{ top: number; sentence: string } | null>(null);
  /*
    단어 지도·그림은 칠판 서랍으로 크게 — 문장 자리를 덮고, 오른쪽 손잡이로 열고 닫는다.
    칠판 스텝이 지나도 같은 문장 안에서는 손잡이가 남아 다시 볼 수 있다
  */
  const boardNow = !view.panelBelow && isBoardPanel(view.panel) ? view.panel : null;
  const [lastBoard, setLastBoard] = useState<{ sentence: string; panel: NonNullable<TutorView["panel"]> } | null>(null);
  useEffect(() => {
    if (boardNow) setLastBoard({ sentence: view.sentence, panel: boardNow });
  }, [boardNow, view.sentence]);
  const board = boardNow ?? (lastBoard?.sentence === view.sentence && !view.readingFirst ? lastBoard.panel : null);
  const inlinePanel = view.panel && !view.panelBelow && !boardNow ? view.panel : null;
  const hasPanel = !!inlinePanel;
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
  // 끊어읽기 — 누르면 의미 덩어리마다 「/」를 넣어 보인다. 문장이 바뀌면 끈다
  const [slashOn, setSlashOn] = useState(false);
  useEffect(() => setSlashOn(false), [view.sentence]);
  // 화면이 저절로 켜 달라고 하면(스텝의 slash_on) 학생이 안 눌렀어도 켠다
  useEffect(() => {
    if (view.slashAuto) setSlashOn(true);
  }, [view.slashAuto]);
  // 자주 헷갈리는 단어 — 누르면 문장 속 그 단어에 밑줄, 단어를 누르면 뜻 아래 💡 (모아보기 목록은 길어서 안 읽는다, 2026-10-16 선생님)
  const [trapOn, setTrapOn] = useState(false);
  useEffect(() => setTrapOn(false), [view.sentence]);
  // 「밑줄 친 단어를 눌러 보세요」는 처음 켰을 때 한 번만 (선생님 말풍선 아래 작은 안내로)
  const [trapHint, setTrapHint] = useState(false);
  useEffect(() => setTrapHint(false), [view.sentence]);
  const toggleTraps = () => {
    const on = !trapOn;
    setTrapOn(on);
    let seen = true;
    try { seen = localStorage.getItem("trapHintSeen") === "1"; localStorage.setItem("trapHintSeen", "1"); } catch { /* 저장 못 해도 그냥 한 번 보인다 */ }
    setTrapHint(on && !seen);
  };
  const withSlashes = (text: string) => {
    if (!slashOn || !(view.slashes?.length || view.slashModifiers?.length)) return text;
    // 수식어(관계대명사절·분사 덩어리)는 [ ]로 묶는다 — 끊는 자리보다 먼저, 뒤에서부터 (2026-10-20 선생님: 수식어라는 걸 괄호로)
    let out = text;
    const mods = [...new Set(view.slashModifiers ?? [])].map((m) => [text.indexOf(m), m.length] as const).filter(([a]) => a >= 0)
      .sort((x, y) => y[0] - x[0]);
    for (const [a, len] of mods) out = `${out.slice(0, a)}[${out.slice(a, a + len)}]${out.slice(a + len)}`;
    // 끊는 자리는 원래 문장에서 먼저 다 찾고 뒤에서부터 넣는다 — 「repertoire」와 「repertoire is」처럼 겹쳐도 둘 다 들어가게
    const cuts = [...new Set((view.slashes ?? []).map((after) => {
      const at = out.indexOf(after);
      if (at < 0) return -1;
      // 수식어 끝에서 끊으면 「]」 뒤에서 — 「danger / ]」가 되지 않게
      return out[at + after.length] === "]" ? at + after.length + 1 : at + after.length;
    }).filter((x) => x > 0))].sort((a, b) => b - a);
    for (const cut of cuts) {
      // 「/」 양옆은 아주 좁은 띄어쓰기(hair space)로 — 보통 띄어쓰기는 너무 벌어져 보인다
      const rest = out.slice(cut).replace(/^ /, "");
      out = `${out.slice(0, cut)}\u200A/\u200A${rest}`;
    }
    return out;
  };

  const [tipMark, setTipMark] = useState<string | null>(null);
  // 💡 칩을 눌러 칠한 표시는 그 화면에서만 — 다음 화면으로 넘어가면 지운다 (안 그러면 엉뚱한 화면에 분홍 표시가 남는다)
  useEffect(() => setTipMark(null), [view.message, view.sentence]);
  const peeked = peek ? view.examSentences?.[peek] : undefined;
  // 자유 해석 입력창에 손이 가 있는 동안 (자판이 올라온 동안)
  const [kbOpen, setKbOpen] = useState(false);
  // 앞 문장을 보는 스텝에서 › 를 눌러 지금 문장을 보는 중
  const [flipped, setFlipped] = useState(false);
  useEffect(() => setFlipped(false), [view.sentence]);
  // 순서 문제 — 단락 안의 다른 문장을 ‹ › 로 잠깐 본다 (null이면 지금 문장)
  const [paraAt, setParaAt] = useState<number | null>(null);
  useEffect(() => setParaAt(null), [view.sentence]);
  const para = view.paragraph && view.paragraph.sentences.length > 1 && !view.flip ? view.paragraph : null;
  const paraAlt = para && paraAt != null && paraAt !== para.at ? { text: para.sentences[paraAt]!, highlight: [] as string[] } : null;
  const alt = flipped && view.flip ? view.flip : paraAlt;
  useEffect(() => setPeek(null), [view.sentence, view.progressLabel]);
  /*
    칠판이 크면 긴 문장은 칸 안에서 스크롤된다. 노랗게 칠한 구절이 칸 밖에 숨지 않게
    스텝이 바뀔 때마다 그 구절로 칸만 내려 준다 (화면 전체는 움직이지 않는다)
  */
  const sentenceBox = useRef<HTMLDivElement>(null);
  /*
    문장 위 여백 — 문장마다 한 번 잰다. 짧은 문장은 화면 위에서 15% 내려오고, 긴 문장은
    문장 자리(화면 절반) 안에 다 들어오도록 여백을 줄인다. 같은 문장 안에서는 바뀌지 않는다
  */
  const [lead, setLead] = useState<number | null>(null);
  useLayoutEffect(() => {
    const box = sentenceBox.current;
    const root = box?.closest<HTMLElement>(".study");
    const en = box?.querySelector<HTMLElement>(".english");
    if (!box || !root || !en) return;
    const h = root.clientHeight;
    // 문장 + 꼬리표 + 아래 줄(듣기·흐림 설명)까지 문장 자리 안에 들어오게
    const pad = parseFloat(getComputedStyle(box).paddingTop) || 0;
    const room = h * 0.5 - (box.scrollHeight - pad) - 8;
    setLead(Math.round(Math.max(12, Math.min(h * 0.15, room))));
  }, [view.sentence]);
  const highlightKey = (view.highlight ?? []).join("|");
  useEffect(() => {
    const box = sentenceBox.current;
    if (!box) return;
    box.scrollTop = 0;
    const marks = [...box.querySelectorAll<HTMLElement>(tipMark ? ".hl-tip" : ".hl, .hl2, .hl3, .ul")];
    if (!marks.length) return;
    // 칠한 구절이 처음부터 다 보이면 그대로 둔다. 칸 아래로 숨으면 첫 구절이 위에 오게 내린다
    const boxTop = box.getBoundingClientRect().top;
    const bottom = Math.max(...marks.map((m) => m.getBoundingClientRect().bottom - boxTop));
    if (bottom <= box.clientHeight) return;
    const top = Math.min(...marks.map((m) => m.getBoundingClientRect().top - boxTop));
    box.scrollTop = Math.max(0, top - 12);
  }, [highlightKey, view.sentence, peek, tipMark]);
  // 지문 전체를 띄운 화면(빈칸 위치 보기 등)에서는 끊어읽기를 안 띄운다 — 한 문장을 읽는 화면이 아니다 (2026-10-21 선생님)
  const showSlash = !!view.slashes?.length && !peeked && !view.pick?.match && !view.pick?.order && !view.examPassage;
  // 고르는 문제 중에는 밑줄이 답을 알려 줄 수 있어 띄우지 않는다
  // 지금 문장에 밑줄 칠 단어가 실제로 있을 때만 — 없으면 버튼도 없다 (2026-10-19 선생님)
  const norm = (t: string) => t.toLowerCase().replace(/[’']/g, "'");
  const hasTraps = (view.wordTips ?? []).some((w) => norm(view.sentence).includes(norm(w.mark || w.label)));
  const showTraps = hasTraps && !peeked && !alt && !view.pick;
  const toggleChips = showSlash || showTraps ? (
    <>
      {showSlash ? (
        <button type="button" className={`slash-toggle${slashOn ? " on" : ""}`} aria-pressed={slashOn} onClick={() => setSlashOn(!slashOn)}>
          / 끊어읽기
        </button>
      ) : null}
      {showTraps ? (
        <button type="button" className={`slash-toggle trap-toggle${trapOn ? " on" : ""}`} aria-pressed={trapOn} onClick={toggleTraps}>
          〰 헷갈리는 단어
        </button>
      ) : null}
    </>
  ) : null;
  const dots = Array.from({ length: view.progressTotal }, (_, i) => i);
  // 단어를 눌러 뜻을 볼 수 있는 화면인가 — 지문 전체(시험지 모양)·순서 카드·해석 맞추기는 못 누른다.
  // 못 누르는 화면에 「단어를 누르면 뜻이 나와요」를 띄우지 않는다 (2026-10-21 선생님)
  const wordsTappable = !view.examPassage && !((view.pick?.order || view.pick?.match) && !peeked && !alt);

  return (
    <div className={`stage-fill study${kbOpen && view.allowInput ? " kb-open" : ""}${view.allowInput || view.translation ? " input-mode" : ""}${view.celebrate ? " celebrate" : ""}${inlinePanel ? " has-panel" : ""}${boardNow ? " board-on" : ""}${view.panelBelow ? " input-mode" : ""}${view.readingFirst ? " reading-first" : ""}${view.examPassage ? " exam-passage-mode" : ""}`}>
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
            <span className="progress-label">{(() => {
              const label =
                view.progressLabel ??
                (view.methodSteps?.active != null
                  ? `${"①②③④"[view.methodSteps.active]} ${view.methodSteps.labels[view.methodSteps.active]}`
                  : "문장 학습");
              // 순서 문제는 「3/6」 대신 자리(주어진 글 · (A)) — 앞 이름과 같으면 한 번만
              if (view.progressPlace) return view.progressPlace === label ? label : `${label} · ${view.progressPlace}`;
              return `${label} · ${view.progressIndex}/${view.progressTotal}`;
            })()}</span>
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


      <div
        className="study-sentence"
        ref={sentenceBox}
        style={lead == null ? undefined : ({ "--lead": `${lead}px` } as React.CSSProperties)}
      >
        {view.flip && !peeked ? (
          // 앞 문장을 보는 스텝 — ‹ › 로 앞 문장과 지금 문장을 오간다
          <div className="sentence-flip">
            <button type="button" className="flip-arrow" disabled={!flipped} aria-label="앞 문장" onClick={() => setFlipped(false)}>‹</button>
            <span className="sentence-no">{flipped ? view.flip.tag : view.sentenceTag}</span>
            <button type="button" className="flip-arrow" disabled={flipped} aria-label="다음 문장" onClick={() => setFlipped(true)}>›</button>
          </div>
        ) : para && !peeked ? (
          // 순서 문제 — 단락 안을 ‹ › 로 오간다 (점은 단락 안 자리, 진한 점이 지금 공부하는 문장)
          <div className="sentence-flip">
            <button type="button" className="flip-arrow" disabled={(paraAt ?? para.at) === 0} aria-label="단락의 앞 문장"
              onClick={() => setParaAt((paraAt ?? para.at) - 1)}>‹</button>
            <span className="sentence-no">
              {view.sentenceTag}{" "}
              {para.sentences.map((_, i) => (
                <i key={i} className={`para-dot${i === (paraAt ?? para.at) ? " on" : ""}${i === para.at ? " now" : ""}`} />
              ))}
            </span>
            <button type="button" className="flip-arrow" disabled={(paraAt ?? para.at) === para.sentences.length - 1} aria-label="단락의 다음 문장"
              onClick={() => setParaAt((paraAt ?? para.at) + 1)}>›</button>
          </div>
        ) : view.sentenceTag && !peeked ? (
          // 듣기는 꼬리표 옆 아이콘만 — 아래 칩 줄에 버튼이 셋이나 되어 많아 보였다 (2026-10-20 선생님)
          <div className="sentence-tag-row">
            <span className="sentence-no">{view.sentenceTag}</span>
            {/* 듣기 아이콘은 늘 — 칠판이 한 번 나오면 치웠더니, 첫 문장부터 칠판이 있는 레슨(31번)은 아예 안 보였다 (2026-10-21 선생님) */}
            <button type="button" className="listen-icon" aria-label="듣기" title="듣기" onClick={listen}>
              <SpeakerIcon />
            </button>
          </div>
        ) : null}
        <div className={view.givenBox && !peeked && !alt ? "given-box" : undefined}>
        {view.pick?.order && !peeked && !alt ? (
          <OrderBoard
            given={view.pick.order.given}
            cards={view.pick.order.cards}
            solved={view.pick.open ? null : view.pick.order.answers}
            tries={view.pick.missed.length}
            open={view.pick.open && !typing}
            onSubmit={(seq) => onSend(`${ORDER_CMD}${seq.join(",")}`)}
          />
        ) : view.pick?.match && !peeked && !alt ? (
          <>
          <MatchKo
            sentence={view.sentence}
            chunks={view.pick.candidates}
            found={view.pick.found}
            ko={view.pick.match.ko}
            open={view.pick.open && !typing}
            onMatch={(slot, chunk) => onSend(`${MATCH_CMD}${slot}:${chunk}`)}
          />
          </>
        ) : (
        <>
        <GlossSentence
          sentence={peeked?.sentence ?? (alt ? alt.text : withSlashes(view.sentence))}
          nouns={view.properNouns}
          glosses={peeked?.glosses ?? view.glosses}
          highlight={peeked || alt ? (alt?.highlight ?? []) : (view.highlight ?? [])}
          underline={peeked ? [peeked.underline] : (view.underline ?? [])}
          highlightAlt={peeked || alt ? [] : (view.highlightAlt ?? [])}
          highlightSame={peeked || alt ? [] : (view.highlightSame ?? [])}
          tipMark={peeked || alt ? null : tipMark}
          pick={peeked || alt ? null : (view.pick ?? null)}
          signs={peeked || alt ? [] : (view.signs ?? [])}
          roles={peeked || alt ? [] : slashOn
            // 끊어읽기를 켜면 문장에 적어 둔 S·V·O·C도 같이 — 찾기로 이미 붙은 말은 그대로 두고 나머지만 보탠다
            ? [...(view.roles ?? []), ...(view.slashRoles ?? []).filter((r) => !(view.roles ?? []).some((x) => x.text === r.text))]
            : (view.roles ?? [])}
          onPickWord={(w) => !typing && onSend(`${PICK_CMD}${w}`)}
          emphasis={view.emphasis ?? []}
          faded={view.faded ?? []}
          shaded={view.shaded ?? []}
          senses={peeked || alt ? [] : (view.senses ?? [])}
          bracketed={peeked || alt ? null : (view.bracket ?? null)}
          resetKey={view.message}
          wordTips={peeked || alt ? [] : (view.wordTips ?? [])}
          showTraps={trapOn && !peeked && !alt}
          onLookup={(word) => onObserve?.({ kind: "vocab_click", word })}
        />
        </>
        )}
        </div>
        {view.fadedNote && !peeked ? <p className="faded-note"><span className="faded-swatch">흐림</span>{view.fadedNote}</p> : null}
        {view.properNouns.length > 0 ? (
          <div className="noun-chips">
            {view.properNouns.map((n) => (
              <span key={n.en} className="noun-chip">
                {n.en} · {nounKind(n.type)} · 그대로
              </span>
            ))}
          </div>
        ) : null}
      </div>

      {/* 문장 넣기 — 답을 고를 때는 지문 전체를 시험지처럼, 핵심어를 칠해서 (①~⑤가 어디인지 보이게) */}
      {view.examPassage ? (
        <div className="exam-passage">
          <PassageFull
            given={view.examPassage.given}
            sentences={view.examPassage.sentences}
            underline={[]}
            highlight={view.examPassage.highlight}
            highlightBy={view.examPassage.highlightBy}
          />
        </div>
      ) : null}

      {/* 끊어읽기 · 헷갈리는 단어 — 문장 칸 밖에 작은 칩 한 줄 (2026-10-16 선생님: 버튼이 너무 많아 보인다).
          듣기는 문장 꼬리표 옆 아이콘으로 옮겼다 (2026-10-20). 안내문은 칠판이 한 번 나오기 전까지만 */}
      {!(sawBoard || shadePick) || toggleChips ? (
        <div className="sentence-toggles">
          {toggleChips}
          {/* 지시문은 말풍선 말고 칩 아래에 (2026-10-16 선생님) — 듣기가 보이는 처음 화면들, 밑줄 켰을 땐 그 안내 */}
          {trapHint ? (
            <span className="toggles-hint">밑줄 친 단어를 눌러 보세요</span>
          ) : sawBoard || shadePick || !wordsTappable ? null : (
            <span className="toggles-hint">단어를 누르면 뜻이 나와요 · 모르는 단어는 ☆로 저장해요</span>
          )}
        </div>
      ) : null}
      {sentenceTips.length || view.concepts?.length ? (
        <TipChips
          tips={[
            ...sentenceTips,
            // 단어 Tip은 칩으로 모으지 않는다 — 「자주 헷갈리는 단어 표시하기」로 문장 속에 밑줄
          ]}
          concepts={view.concepts ?? []}
          onMark={setTipMark}
          onHint={() => onObserve?.({ kind: "hint_open" })}
          appearance={`${view.sentence}|${(view.highlight ?? []).join()}|${(view.highlightAlt ?? []).join()}`}
        />
      ) : null}


      {inlinePanel ? (
        <StudyPanelView
          panel={inlinePanel}
          // 끌어 넣기는 지금 고를 수 있는 보기일 때만 — 답한 뒤의 화면에서는 칩을 치운다
          onPick={
            !typing && inlinePanel.kind === "groups" && inlinePanel.sort && view.buttons.includes(inlinePanel.sort.right)
              ? onSend
              : undefined
          }
        />
      ) : null}
      {board ? (
        <BoardDrawer
          panel={board}
          fresh={board === boardNow}
          onPick={
            !typing && board === boardNow && board.kind === "groups" && board.sort && view.buttons.includes(board.sort.right)
              ? onSend
              : undefined
          }
        />
      ) : null}

      <div className="study-stage">
        {/* 지문을 읽는 동안은 할 말이 없다 — 빈 말풍선을 띄우지 않는다 */}
        {typing || view.message ? (
          <div className="teacher-bubble study-bubble-over" aria-live="polite">
            {/*
              덩어리 고르기에서 3초 동안 아무것도 안 누르면 — 무엇을 할지 말풍선 위에서 알려 준다.
              (문장 칸 안에 두면 긴 문장에서는 스크롤 아래로 숨는다)
            */}
            {/* 틀린 뒤 — 문제가 무엇이었는지 반짝이며 다시 (2026-10-21 선생님) */}
            {view.askAgain && !typing ? (
              <p className="ask-again" role="status" key={view.message}>
                <span className="ask-again-star" aria-hidden="true">✨</span>
                {view.askAgain}
              </p>
            ) : pickNudge ? (
              <p className="pick-nudge" role="status">
                <span className="nudge-arrow" aria-hidden="true">👆</span>
                {view.pick?.shade ? "회색 부분을 눌러 보세요!" : "상자 친 부분을 눌러 보세요!"}
              </p>
            ) : null}
            {/* 힌트는 선생님 말풍선 바로 위 — 질문을 읽다가 바로 누를 수 있게 */}
            {hintTips.length && !typing ? (
              <TipChips
                tips={hintTips}
                concepts={NO_CONCEPTS}
                onMark={setTipMark}
                onHint={() => onObserve?.({ kind: "hint_open" })}
                appearance={`${view.sentence}|${view.message}`}
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
            <TeacherFigure mood={view.mood} />
          </div>
          {/* 쌤 한마디는 말풍선 밖, 쌤 옆 — 말풍선(설명)을 길게 만들지 않고, 틀렸을 때 첫마디도 그대로 */}
          {typing ? null : <TeacherReaction reaction={view.reaction} beside />}
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
              question={view.fullPassage.question}
              given={view.fullPassage.given}
              sentences={view.fullPassage.sentences}
              underline={view.fullPassage.underline}
            />
          </div>
        </div>
      ) : null}

      <div
        className="study-dock"
        onFocusCapture={(e) => (e.target as HTMLElement).tagName === "TEXTAREA" && setKbOpen(true)}
        onBlurCapture={(e) => (e.target as HTMLElement).tagName === "TEXTAREA" && setKbOpen(false)}
      >
        {view.examOptions ? (
          <ExamOptions
            options={view.examOptions}
            glosses={view.examGlosses ?? []}
            peekable={view.examSentences ?? null}
            explain={view.examExplain ?? null}
            explainOpen={!!view.examExplainOpen}
            numbersOnly={!!view.examNumbersOnly}
            peek={peek}
            onPeek={(id) => setPeek(peek === id ? null : id)}
            disabled={typing}
            onPick={onSend}
          />
        ) : null}
        {view.panel && view.panelBelow ? <StudyPanelView panel={view.panel} /> : null}
        {/* 자유 해석 결과 — 답을 쓴 자리(아래)에 그대로 */}
        {view.translation ? <TranslationCard result={view.translation} /> : null}
        <QuickReplies
          buttons={view.buttons}
          hidden={typing || readWait}
          layout={view.buttonLayout}
          aux={view.auxButtons}
          numbered={view.numbered}
          onPick={onSend}
        />
        {view.linkButtons?.length && !typing ? (
          <div className="link-row">
            {view.linkButtons.map((label) => (
              <button key={label} type="button" className="text-link" onClick={() => onSend(label)}>
                {label}
              </button>
            ))}
          </div>
        ) : null}
        {view.allowInput !== false && view.translateWhy ? (
          <WhyChip
            key={view.translateWhy.label + (view.highlight ?? []).join()}
            why={view.translateWhy}
            appearance={`${view.sentence}|${(view.highlight ?? []).join()}`}
          />
        ) : null}
        {view.allowInput === false ? null : (
          // 키보드가 올라오면 위 문장이 밀려나므로, 해석할 영어를 입력창 바로 위에 다시 보여 준다
          // 이 영어도 단어를 눌러 뜻을 볼 수 있다 — 자판이 올라와 위 문장이 밀려나도 여기서 보며 쓴다
          <div className="translate-ref">
            <small>보고 쓸 부분 · 단어를 누르면 뜻이 나와요</small>
            <GlossSentence
              sentence={view.highlight?.length ? view.highlight.join(" … ") : view.sentence}
              nouns={view.properNouns}
              glosses={view.glosses}
              highlight={[]}
              underline={[]}
              highlightAlt={[]}
              tipMark={null}
              pick={null}
              signs={[]}
              roles={[]}
              onPickWord={() => {}}
              emphasis={[]}
              faded={[]}
              shaded={[]}
              onLookup={(word) => onObserve?.({ kind: "vocab_click", word })}
            />
          </div>
        )}
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
  highlightSame = [],
  tipMark,
  pick,
  signs,
  roles,
  onPickWord,
  emphasis,
  faded,
  shaded,
  onLookup,
  senses = [],
  bracketed = null,
  resetKey = "",
  wordTips = [],
  showTraps = false,
}: {
  /** 바뀌면 열린 단어 뜻을 닫는다 (화면이 바뀔 때) */
  resetKey?: string;
  /** 문장 속 색 글자로 보일 단어 Tip — 누르면 뜻 아래 Tip 글 */
  wordTips?: { label: string; text: string; mark?: string }[];
  /** 헷갈리는 단어 표시 버튼을 켰을 때 — 그 단어에 밑줄 */
  showTraps?: boolean;
  /** 다의 기능어의 그 자리 쓰임 — 문장에 나온 순서대로 */
  senses?: NonNullable<TutorView["senses"]>;
  /** [ ]로 묶어 가리키는 한 문장 — 괄호는 색으로, 그 문장은 옅은 바탕으로 */
  bracketed?: string | null;
  sentence: string;
  nouns: TutorView["properNouns"];
  glosses: TutorView["glosses"];
  highlight: string[];
  underline: string[];
  highlightAlt: string[];
  /** 세 번째 색(보라) — 같은 것을 가리키는 말끼리 (빈칸 ↔ it) */
  highlightSame?: string[];
  tipMark: string | null;
  /** 「찾기」 스텝 — 후보 구절을 누르면 고른다 (뜻 대신) */
  pick: TutorView["pick"];
  signs: NonNullable<TutorView["signs"]>;
  roles: NonNullable<TutorView["roles"]>;
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
  // 구절 뜻은 단어마다 나눠 보인다 — 지금 통째로 고르는 후보 구절만 그대로
  // 찾은 S·V 표시가 줄임말 조각(it + ’s)에 붙어 있으면 그 조각도 따로 둔다 — 한 칸에 표시가 하나만 붙으니까
  const rolePieces = roles.map((r) => r.text).filter((t) => !/\s/.test(t) || t.startsWith("’"));
  const spans = withSenses(glossSpans(sentence, glossesFor(splitPhraseGlosses(glosses, [...(pick?.candidates ?? []), ...rolePieces]), nouns)), senses);
  /*
    뜻 상자 아랫줄 「덩어리」는 누른 자리를 실제로 감싸는 덩어리로 — 같은 낱말(in)이 문장 앞 「In many cases」에도
    있으면 맨 앞 덩어리를 붙이던 것을 고친다 (2026-10-18, 24번 「both are in play」의 in)
  */
  const phraseRanges = glosses
    .filter((g) => /\s/.test(g.en.trim()))
    .flatMap((g) => allWordRanges(sentence, g.en).map(([a, b]) => ({ a, b, en: g.en, ko: g.ko.split(" · ")[0]! })));
  const phraseAt = (a: number, b: number) =>
    phraseRanges.filter((r) => r.a <= a && b <= r.b).sort((x, y) => x.b - x.a - (y.b - y.a))[0] ?? null;
  const marked = highlightRanges(sentence, highlight);
  const markedAlt = highlightRanges(sentence, highlightAlt);
  const markedSame = highlightRanges(sentence, highlightSame);
  const markedUl = highlightRanges(sentence, underline);
  const markedTip = tipMark ? wordRanges(sentence, tipMark) : [];
  // 같은 낱말이 두 번 나오면(does not stop … it stop) 이미 다른 후보가 차지한 자리는 건너뛴다
  const candPlaced = placeWords(sentence, pick?.candidates ?? []);
  const candAt = (pick?.candidates ?? []).flatMap((c) => (candPlaced.get(c) ?? []).map(([a, b]) => ({ c, a, b })));
  const fadedAt = highlightRanges(sentence, faded);
  const shadedAt = highlightRanges(sentence, shaded);
  // 단어 경계로 찾는다 — 「one」이 Nonetheless 안에서 잡히지 않게
  const rolePlaced = placeWords(sentence, roles.map((r) => r.text));
  const roleAt = roles.flatMap((r) => (rolePlaced.get(r.text) ?? []).map(([a, b]) => ({ a, b, role: r.role })));

  /*
    뜻 상자는 단어 아래 가운데에 뜬다. 단어가 가장자리에 있으면 상자가 화면 밖으로
    나가 잘리므로, 뜨고 나서 재서 안쪽으로 밀어 넣는다.
  */
  useLayoutEffect(() => {
    setShift(0);
    const tip = tipRef.current;
    // 입력창 위 「보고 쓸 부분」 안에서도 그 상자 안으로 밀어 넣는다
    const box = tip?.closest(".study-sentence, .translate-ref");
    if (!tip || !box) return;
    // 앞에서 연 단어의 밀어 넣기(shift)가 아직 붙어 있으면 잘못 잰다 — 원래 자리로 되돌리고 잰다
    tip.style.transform = "";
    const t = tip.getBoundingClientRect();
    const b = box.getBoundingClientRect();
    const pad = 12;
    const next = t.left < b.left + pad ? b.left + pad - t.left : t.right > b.right - pad ? b.right - pad - t.right : 0;
    // 값이 그대로면 React가 다시 그리지 않으니 여기서 바로 붙인다
    if (next) tip.style.transform = `translateX(calc(-50% + ${next}px))`;
    setShift(next);
    // 아래로 길게 뜬 상자(💡 붙은 뜻)는 문장 칸 밖으로 잘린다 — 칸을 굴려 다 보이게
    if (t.bottom > b.bottom) box.scrollTop += t.bottom - b.bottom + 8;
  }, [open]);

  // 화면(선생님 말)이 바뀌면 열어 둔 단어 뜻도 닫는다 — 안 그러면 누른 단어가 다음 화면까지 분홍으로 남는다
  useEffect(() => {
    setOpen(null);
  }, [sentence, resetKey]);

  useEffect(() => {
    function close(e: MouseEvent) {
      if (!(e.target instanceof Element) || !e.target.closest(".english")) setOpen(null);
    }
    document.addEventListener("click", close);
    return () => document.removeEventListener("click", close);
  }, []);

  // 단어 Tip 자리 — 문장에서 mark(없으면 label)를 찾는다 (따옴표 모양은 가리지 않는다)
  // 단어 단위로 찾는다 — 글자로만 찾으면 as가 contrast 안에 붙는다 (2026-10-17). 「as … as」면 두 자리 모두
  const tipAt = wordTips.flatMap((w) => wordRanges(sentence, w.mark || w.label).map(([a, b]) => ({ a, b, tip: w })));
  const bracketFrom = bracketed ? sentence.indexOf(bracketed) : -1;
  const bracketAt: [number, number] | null = bracketFrom >= 0 ? [bracketFrom, bracketFrom + bracketed!.length] : null;
  const parts: ReactNode[] = [];
  let at = 0;
  spans.forEach((span, i) => {
    const start = at;
    at += span.text.length;
    // 옆 단어에 이미 붙여 그린 문장부호
    if (i > 0 && spans[i - 1]!.gloss && CLOSING.test(span.text)) return;
    if (spans[i + 1]?.gloss && OPENING.test(span.text)) return;
    const hit = (ranges: [number, number][]) => ranges.some(([from, to]) => start < to && at > from);
    const hl3 = hit(markedSame);
    const hl = !hl3 && hit(marked);
    const hl2 = !hl && !hl3 && hit(markedAlt);
    // 칠한 말이 not·never 같은 부정어면 아주 크게, 움직여서 — 시험에서 큰 힌트다 (2026-10-23 선생님)
    const neg = (hl || hl2 || hl3) && NEGATION.test(span.text.trim());
    const tip = hit(markedTip);
    /*
      흐림 = 빼도 되는 삽입, 음영 = 건너뛰어도 되는 부분. 공백까지 같은 칸으로 감싸야
      음영이 단어마다 끊기지 않고 한 줄로 이어진다.
    */
    const inRole = roleAt.find((r) => start < r.b && at > r.a);
    // S·V 표시 — 덩어리 첫 칸 위에 글자, 덩어리 전체에 밑줄 색
    const roleHead = roleAt.find((r) => r.a >= start && r.a < at && span.text.trim());
    const inBracket = bracketAt && start < bracketAt[1] && at > bracketAt[0];
    const tipHit = span.text.trim() ? tipAt.find((x) => start < x.b && at > x.a) : undefined;
    const wordTip = tipHit?.tip;
    // 문장 속 표시는 버튼을 켰을 때만(늘 띄우면 * 처럼 지저분하다, 2026-10-16 선생님) — 누르면 뜻 아래 💡
    const marks = `${showTraps && wordTip ? " trap" : ""}${inBracket ? " bracketed" : ""}${hit(fadedAt) ? " faded" : ""}${hit(shadedAt) ? " shaded" : ""}${hit(markedUl) ? " ul" : ""}${inRole ? ` role-${inRole.role}` : ""}${roleHead ? " role-head" : ""}`;
    const roleAttr = roleHead ? { "data-role": roleHead.role } : {};
    if (!span.gloss) {
      // 덩어리 나누기 슬래시(/)는 굵고 진하게 — 문장 구조가 한눈에 보이게
      // [ ] 괄호도 색으로 — 어느 문장을 가리키는지 보이게
      const text: ReactNode = /[\/\[\]]/.test(span.text)
        ? span.text.split(/([\/\[\]])/).map((t, k) =>
            t === "/" ? <b key={k} className="slash">/</b> : t === "[" || t === "]" ? <b key={k} className="bracket-mark">{t}</b> : t,
          )
        : span.text;
      if (tip) parts.push(<mark key={i} {...roleAttr} className={`hl-tip${marks}`}>{text}</mark>);
      else if (hl || hl2 || hl3) parts.push(<mark key={i} {...roleAttr} className={`${hl3 ? "hl3" : hl ? "hl" : "hl2"}${neg ? " neg-pop" : ""}${marks}`}>{text}</mark>);
      else if (marks) parts.push(<span key={i} {...roleAttr} className={marks.trim()}>{text}</span>);
      else parts.push(<span key={i}>{text}</span>);
      return;
    }
    // 「찾기」 후보 — 점선 상자로, 누르면 고른다
    const cand = candAt.find((x) => start < x.b && at > x.a);
    if (cand && pick) {
      // 핵심어 고르기에서 덜 좋은 선택은 줄을 긋지 않고 흐리게만 (틀렸다는 표시가 아니다)
      const state = pick.found.includes(cand.c)
        ? ` found${pick.foundTone === "hl" ? " tone-hl" : ""}`
        : pick.missed.includes(cand.c) ? (pick.soft ? " missed soft" : " missed") : "";
      parts.push(
        <span key={i} {...roleAttr} className={`english-token${longPhrase(span.text) ? " long" : ""}${marks}`}>
          {OPENING.test(spans[i - 1]?.text ?? "") ? spans[i - 1]!.text : null}
          <Tap
            // 후보라도 강조(highlight)할 말이면 노랑 그대로 — 앞에서 고른 비슷한 말이 계속 노랗게 보이게 (2026-10-21)
            className={`english-word cand${pick.shade ? " shade" : ""}${state}${!state && hl ? " hl-cand" : ""}`}
            disabled={!pick.open || !!state}
            onTap={() => onPickWord(cand.c)}
          >
            {span.text}
          </Tap>
          {CLOSING.test(spans[i + 1]?.text ?? "") ? spans[i + 1]!.text : null}
        </span>,
      );
      return;
    }
    const noun = nouns.some(
      (n) => n.en === span.gloss!.en || n.en.replace(/\.$/, "") === span.text.replace(/\.$/, ""),
    );
    const selected = open === i;
    const sign = signs.find((x) => x.text === span.text.replace(/[.,;:!?]+$/, ""))?.sign;
    parts.push(
      <span
        key={i}
        {...(sign ? { "data-sign": sign } : {})}
        {...roleAttr}
        className={`english-token${longPhrase(span.text) ? " long" : ""}${sign ? (sign === "+" ? " sign-plus" : " sign-minus") : ""}${selected ? " open" : ""}${hl ? " hl" : ""}${hl2 ? " hl2" : ""}${hl3 ? " hl3" : ""}${neg ? " neg-pop" : ""}${tip ? " hl-tip" : ""}${marks}`}
      >
        {OPENING.test(spans[i - 1]?.text ?? "") ? spans[i - 1]!.text : null}
        <Tap
          className={`english-word${noun ? " noun-mark" : ""}${emphasis.includes(span.text.replace(/[.,;:]$/, "")) ? " em" : ""}`}
          expanded={selected}
          label={`${span.text}, ${span.gloss.ko}`}
          onTap={() => {
            if (!selected) onLookup(span.text);
            setOpen(selected ? null : i);
          }}
        >
          {span.text}
        </Tap>
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
            {/*
              한 줄로 — 단어 뜻(진하게) 옆에 그 단어가 들어간 덩어리 뜻(연하게). 별은 단어 카드로 저장한다.
              단어 뜻이 없는 말(to, of …)은 덩어리 뜻이 본문이고, 별은 덩어리(숙어) 카드로
            */}
            {(() => {
              const g0 = span.gloss!;
              const here = g0.phrase ? phraseAt(start, at) : null;
              const g = here && here.en !== g0.phrase!.en ? { ...g0, phrase: { en: here.en, ko: here.ko } } : g0;
              const asPhrase = !g.ko && !!g.phrase;
              // 단어 뜻에 이미 붙어 있는 같은 덩어리 풀이(「자리 · in its tracks = …」)는 빼고 레슨의 덩어리 뜻 하나만 — 중복 방지
              const wordKo = g.phrase && g.ko ? g.ko.split(" · ").filter((part) => !part.startsWith(`${g.phrase!.en} =`)).join(" · ") : g.ko;
              const entry = asPhrase
                ? { en: g.phrase!.en, ko: g.phrase!.ko, kind: "phrase" as const }
                : { en: g.en, ko: wordKo, kind: "word" as const };
              const note = !asPhrase && g.phrase && g.phrase.ko !== wordKo ? `${g.phrase.en} = ${g.phrase.ko}` : null;
              return (
                <>
                  <VocabStar
                    vocab={vocab}
                    en={entry.en}
                    onToggle={() => setVocab(toggleVocab(vocab, { ...entry, sentence, source: lessonIdOfSentence(sentence) }))}
                  />
                  <GlossText ko={asPhrase ? `${g.phrase!.en} = ${g.phrase!.ko}` : note ? `${wordKo} · ${note}` : wordKo} />
                  {wordTip ? <span className="gloss-tip-note">💡 {wordTip.text}</span> : null}
                </>
              );
            })()}
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
  appearance,
}: {
  /** 이 화면을 가리키는 키 — 같은 화면에서 다시 그려져도 한 번으로 센다 */
  appearance: string;
  tips: NonNullable<TutorView["tips"]>;
  concepts: NonNullable<TutorView["concepts"]>;
  /** 연 Tip이 문장에서 가리키는 단어 — 닫으면 null */
  onMark: (mark: string | null) => void;
  /** 「힌트」 칩을 열었다 — 세션에 알린다 */
  onHint: () => void;
}) {
  // 💡 참고 칩은 같은 칩을 세 번(안 누르면 다섯 번)까지만 — 힌트 칩은 그대로
  const shownTips = useMemo(
    () => tipList.filter((t) => t.hint || ("word" in t && t.word) || takeTipShow(t.label, appearance)),
    [tipList, appearance],
  );
  const tips = [
    ...concepts.map((c) => ({ icon: "❓", label: c.en, text: `${c.title} ${c.text}` })),
    ...shownTips.map((t) => ({ icon: "💡", ...t })),
  ] as { icon: string; label: string; text: string; mark?: string; hint?: boolean }[];
  const [open, setOpen] = useState<number | null>(null);
  // 칩 목록이 실제로 바뀔 때만 닫는다 — 배열이 새로 만들어질 때마다 닫으면 연 창이 저절로 꺼진다
  const tipKey = `${tipList.map((x) => `${x.label}|${x.text}`).join("§")}#${concepts.map((c) => c.en).join("§")}`;
  useEffect(() => {
    setOpen(null);
    onMark(null);
  }, [tipKey]); // eslint-disable-line react-hooks/exhaustive-deps
  if (!tips.length) return null;
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
              if (next != null && tips[next]!.icon === "💡" && !tips[next]!.hint) noteTipOpened(tips[next]!.label);
            }}
          >
            {tip.icon} {tip.label}
          </button>
        ))}
      </div>
      {open != null ? (
        <div className="info-pop">
          {/* 모아보기 — 줄마다 「단어 — 설명」, 단어는 굵게 */}
          {tips[open]!.text.includes("\n")
            ? tips[open]!.text.split("\n").map((line, k) => {
                const [w, ...rest] = line.split(" — ");
                return (
                  <span key={k} className="info-line">
                    <b>{w}</b> {rest.join(" — ")}
                  </span>
                );
              })
            : tips[open]!.text}
        </div>
      ) : null}
    </div>
  );
}

/** 「보고 쓸 부분」 위 💡 칩 — 누르면 참고 설명이 열린다 (예: 왜 핵심어만 보나요?) */
function WhyChip({ why, appearance }: { why: { label: string; text: string }; appearance: string }) {
  const [open, setOpen] = useState(false);
  // 같은 칩은 세 번(안 누르면 다섯 번)까지만
  const [show] = useState(() => takeTipShow(why.label, appearance));
  if (!show) return null;
  return (
    <div className="why-chip">
      <button
        type="button"
        className={`tip-chip${open ? " on" : ""}`}
        aria-expanded={open}
        onClick={() => {
          if (!open) noteTipOpened(why.label);
          setOpen(!open);
        }}
      >
        💡 {why.label}
      </button>
      {open ? <div className="info-pop">{why.text}</div> : null}
    </div>
  );
}

/**
 * 시험 보기 — 영어만 먼저. 핵심 단어는 색칠하고, 단어를 누르면 뜻, ▸를 누르면
 * 보기 아래에 짧은 한국어. 보기(카드)를 누르면 **고르기만** 하고, 아래 [제출]을 눌러야 답이 된다 —
 * 「문장 보기」·▸·단어 뜻을 누르다 잘못 고르는 일이 잦아서 (2026-10-20 선생님).
 * 해설 화면(`explain`)에서는 보기를 누르면 해설이 열린다. `explainOpen`이면 처음부터 다 펼쳐 둔다
 */
function ExamOptions({
  options,
  glosses,
  peekable,
  peek,
  onPeek,
  explain,
  explainOpen,
  numbersOnly,
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
  /** 해설을 처음부터 다 펼쳐 둔다 (분석 뒤 문제를 제출한 뒤) */
  explainOpen: boolean;
  /** 보기 글 없이 숫자만 가로로 (문장 넣기) */
  numbersOnly: boolean;
  disabled: boolean;
  onPick: (label: string) => void;
}) {
  const [ko, setKo] = useState<string[]>([]);
  const [opened, setOpened] = useState<string[]>([]);
  /** 고른 보기 — [제출]을 눌러야 답이 된다 */
  const [selected, setSelected] = useState<string | null>(null);
  const ids = options.map((o) => o.id).join(",");
  // 보기가 바뀌면(다른 화면) 고른 것을 지운다. 해설을 다 펼치는 화면이면 처음부터 다 연다
  useEffect(() => {
    setSelected(null);
    setOpened(explainOpen ? ids.split(",") : []);
  }, [ids, explainOpen]);
  const pick = (o: { id: string; label: string }) => {
    if (disabled) return;
    if (explain) setOpened(opened.includes(o.id) ? opened.filter((x) => x !== o.id) : [...opened, o.id]);
    else setSelected(selected === o.id ? null : o.id);
  };
  const submit = () => {
    const o = options.find((x) => x.id === selected);
    if (o && !disabled) onPick(o.label);
  };
  const submitButton = explain ? null : (
    <button type="button" className="read-continue exam-submit" disabled={!selected || disabled} onClick={submit}>
      제출
    </button>
  );
  const tag = (id: string) => {
    const e = explain?.[id];
    if (!e) return "";
    return e.picked ? (e.correct ? "내 답 · 정답" : "내 답 · 오답") : e.correct ? "정답" : "오답";
  };
  const [word, setWord] = useState<{ id: string; gloss: WordGloss } | null>(null);
  const NUM = "①②③④⑤";
  if (numbersOnly) {
    // 문장 넣기 — 「… 앞」 같은 자리 표시는 빼고 숫자만 가로로. 해설은 줄 아래에
    return (
      <div className="exam-numbers-wrap">
        <div className="exam-numbers">
          {options.map((o) => (
            <div
              key={o.id}
              role="button"
              tabIndex={0}
              aria-disabled={disabled}
              aria-label={`${NUM[Number(o.id) - 1] ?? o.id} ${o.label}`}
              className={`exam-num-btn${explain?.[o.id]?.correct ? " is-answer" : ""}${opened.includes(o.id) || selected === o.id ? " on" : ""}${explain?.[o.id]?.picked && !explain[o.id]?.correct ? " picked-wrong" : ""}`}
              onClick={() => pick(o)}
              onKeyDown={(e) => e.key === "Enter" && pick(o)}
            >
              {NUM[Number(o.id) - 1] ?? o.id}
            </div>
          ))}
        </div>
        {explain
          ? options
              .filter((o) => opened.includes(o.id))
              .map((o) => (
                <div key={o.id} className={`exam-explain${explain[o.id]?.correct ? " right" : ""}`}>
                  <b>{NUM[Number(o.id) - 1]} {tag(o.id)}</b> {explain[o.id]?.text}
                </div>
              ))
          : null}
        {submitButton}
      </div>
    );
  }
  return (
    <>
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
              className={`exam-option${explain?.[o.id]?.correct ? " is-answer" : ""}${selected === o.id ? " selected" : ""}${explain?.[o.id]?.picked && !explain[o.id]?.correct ? " picked-wrong" : ""}`}
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
                <b>{tag(o.id)}</b> {explain[o.id]?.text}
              </div>
            ) : null}
          </li>
        );
      })}
    </ol>
    {/* [제출]은 목록 밖 — 보기 다섯 개는 스크롤 없이 다 보이고, 그 아래 붙는다 */}
    {submitButton}
    </>
  );
}

/** 단어 바로 뒤에 붙는 문장부호 */
const CLOSING = /^[,.;:!?)”’"']$/;
/** 단어 바로 앞에 붙는 문장부호 */
const OPENING = /^[(“‘①②③④⑤]$/;

/** 강조할 구절이 문장의 몇 번째 글자부터 몇 번째까지인지 */
/** 부정어 — 칠하면 크게 움직이는 강조 (not, never, isn't …) */
const NEGATION = /^(?:not|never|no|nor|neither|none|nothing|hardly|scarcely|barely|seldom|rarely|cannot|[a-z]+n['’]t)[.,;:!?]?$/i;

function highlightRanges(sentence: string, phrases: string[]): [number, number][] {
  const ranges: [number, number][] = [];
  for (const phrase of phrases) {
    // 칠하기는 핵심 단어 하나만 적을 때가 많다 — 단어 안(has 속 as)에서 잡히지 않게 단어 경계로
    const esc = phrase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const m = new RegExp(`(?<![A-Za-z])${esc}(?![A-Za-z])`).exec(sentence);
    const from = m ? m.index : sentence.indexOf(phrase);
    if (from >= 0) ranges.push([from, from + phrase.length]);
  }
  return ranges;
}

/** 단어 단위로 찾는다 — Tip이 가리키는 「one」이 Nonetheless 안에서 잡히지 않게 */
/**
 * 문장에서 단어 자리를 단어 단위로 찾는다 (as가 contrast 안에 잡히지 않게).
 * 「as … as」처럼 「 … 」로 이으면 앞 말 뒤에서 다음 말을 차례로 찾아 여러 자리를 표시한다 (as A as B, not only … but)
 */
/**
 * 여러 낱말·덩어리의 자리를 한꺼번에 — 긴 것부터 자리를 잡고, 짧은 것은 아직 안 잡힌 자리 중 첫 번째로.
 * 「stop」이 「does not stop」 안과 「it stop」에 다 있으면 뒤의 stop을 준다
 */
function placeWords(sentence: string, words: string[]): Map<string, [number, number][]> {
  const out = new Map<string, [number, number][]>();
  const taken: [number, number][] = [];
  const free = ([a, b]: [number, number]) => !taken.some(([x, y]) => a < y && x < b);
  for (const w of [...new Set(words)].sort((x, y) => y.length - x.length)) {
    if (w.includes(" … ")) {
      // 「we … we」처럼 차례로 잡는 낱말도 이미 긴 덩어리가 차지한 자리(what we have 안의 we)는 건너뛴다 (2026-10-20 선생님: we are adults의 we도 S)
      const r = wordRanges(sentence, w, taken);
      out.set(w, r);
      taken.push(...r);
      continue;
    }
    const all = allWordRanges(sentence, w);
    const hit = all.find(free) ?? all[0];
    const r = hit ? [hit] : [];
    out.set(w, r);
    taken.push(...r);
  }
  return out;
}

/**
 * 찾는 말의 정규식. 끊어읽기를 켜면 문장 안 띄어쓰기 자리에 「 / 」(hair space + / + hair space)가 끼는데,
 * S·V·O 덩어리가 끊는 자리를 가로질러도 찾도록 띄어쓰기마다 그 모양도 허용한다 (2026-10-20 선생님: 끊는 자리는 그대로 두고 표시도 보이게).
 * 수식어 [ ]도 건너뛴다 — 목적어 「music [in which … song]」처럼 O 안에 꾸밈이 든 경우
 */
function wordRe(part: string): RegExp {
  const esc = part.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/ /g, "\\]?(?: |\\u200A\\/\\u200A)\\[?");
  return new RegExp(`${/^[a-z0-9]/.test(part) ? "(?<![a-z0-9])" : ""}${esc}(?![a-z0-9])`, "g");
}

function allWordRanges(sentence: string, word: string): [number, number][] {
  const text = sentence.toLowerCase().replace(/[’']/g, "'");
  const re = wordRe(word.toLowerCase().replace(/[’']/g, "'"));
  const out: [number, number][] = [];
  for (let m = re.exec(text); m; m = re.exec(text)) out.push([m.index, m.index + m[0].length]);
  return out;
}

function wordRanges(sentence: string, word: string, taken: [number, number][] = []): [number, number][] {
  const text = sentence.toLowerCase().replace(/[’']/g, "'");
  const out: [number, number][] = [];
  let from = 0;
  for (const part of word.toLowerCase().replace(/[’']/g, "'").split(" … ")) {
    // ’s처럼 기호로 시작하는 조각은 앞 글자(it)에 붙어 있다 — 앞쪽 경계는 보지 않는다
    const re = wordRe(part);
    re.lastIndex = from;
    let m = re.exec(text);
    // 이미 다른 표시가 차지한 자리는 건너뛰고 다음 자리로
    while (m && taken.some(([x, y]) => m!.index < y && x < m!.index + m![0].length)) m = re.exec(text);
    if (!m) break;
    out.push([m.index, m.index + m[0].length]);
    from = m.index + m[0].length;
  }
  return out;
}

/** 「통합, 통일성 · 여기서는 …」 — 뜻은 진하게, 「·」 뒤의 해설은 연하게 */
function VocabStar({ vocab, en, onToggle }: { vocab: VocabEntry[]; en: string; onToggle: () => void }) {
  const on = isSaved(vocab, en);
  return (
    <button
      type="button"
      className={`vocab-star${on ? " on" : ""}`}
      aria-pressed={on}
      aria-label={on ? `${en} 단어장에서 빼기` : `${en} 단어장에 저장`}
      onClick={(e) => {
        e.stopPropagation();
        onToggle();
      }}
    >
      <StarIcon filled={on} />
    </button>
  );
}

/**
 * 다의 기능어(to, for, that …)에 그 자리 쓰임을 붙인다. 문장에 나온 순서대로 짝짓는다 —
 * 덩어리 칸(찾기 후보) 안에 든 것도 세어야 뒤의 순서가 맞는다. 뜻이 없던 칸도 누를 수 있게 된다
 */
function withSenses(spans: ReturnType<typeof glossSpans>, senses: NonNullable<TutorView["senses"]>) {
  if (!senses.length) return spans;
  const queue = new Map<string, typeof senses>();
  for (const x of senses) queue.set(x.word.toLowerCase(), [...(queue.get(x.word.toLowerCase()) ?? []), x]);
  const seen = new Map<string, number>();
  return spans.map((span) => {
    const words = span.text.match(/[A-Za-z]+/g) ?? [];
    if (words.length === 1) {
      const key = words[0]!.toLowerCase();
      const list = queue.get(key);
      if (list) {
        const n = seen.get(key) ?? 0;
        seen.set(key, n + 1);
        const x = list[n];
        return x ? { ...span, gloss: { en: words[0]!, ko: `${x.sense} · ${x.usage}`, sense: true } } : span;
      }
      return span;
    }
    // 여러 단어 칸 — 안에 든 기능어도 세기만 한다
    for (const w of words) {
      const key = w.toLowerCase();
      if (queue.has(key)) seen.set(key, (seen.get(key) ?? 0) + 1);
    }
    return span;
  });
}

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

/**
 * 자유 해석 결과 — 내 해석(틀린 곳 빨강 밑줄)과 고친 해석(고친 곳 초록), 짚을 말.
 * 틀렸으면 「연습할 문장」으로 내 노트에 저장한다.
 */
function TranslationCard({ result }: { result: TranslationResult }) {
  useEffect(() => {
    if (!result.save) return;
    addNote({
      key: `practice:${result.english}`,
      lessonId: result.lessonId,
      title: `연습할 문장 · ${result.where}`,
      text: `${result.english}\n→ ${result.model}${result.mine ? `\n(내 해석: ${result.mine})` : ""}`,
    });
  }, [result]);
  const mine = result.mine;
  const mineParts: ReactNode[] = [];
  if (mine) {
    let at = 0;
    result.marks.forEach(([a, b], i) => {
      if (a < at) return;
      if (a > at) mineParts.push(mine.slice(at, a));
      mineParts.push(<mark key={i} className="tr-wrong">{mine.slice(a, b)}</mark>);
      at = b;
    });
    mineParts.push(mine.slice(at));
  }
  const modelParts: ReactNode[] = [];
  {
    const spans = result.fixes
      .map((f) => [result.model.indexOf(f), f.length] as const)
      .filter(([i]) => i >= 0)
      .sort((x, y) => x[0] - y[0]);
    let at = 0;
    spans.forEach(([i, n], k) => {
      if (i < at) return;
      if (i > at) modelParts.push(result.model.slice(at, i));
      modelParts.push(<mark key={k} className="tr-fix">{result.model.slice(i, i + n)}</mark>);
      at = i + n;
    });
    modelParts.push(result.model.slice(at));
  }
  return (
    <div className="study-panel translation-card">
      {mine ? (
        <div className="tr-row">
          <span className="tr-label">{result.labels?.mine ?? "내 해석"}</span>
          <p className="tr-mine">{mineParts}</p>
        </div>
      ) : null}
      <div className="tr-row">
        <span className="tr-label fix">{result.labels?.model ?? (mine && result.fixes.length ? "고친 해석" : "해석")}</span>
        <p className="tr-model">{modelParts}</p>
      </div>
      {result.notes.length ? (
        <ul className="tr-notes">
          {result.notes.map((n) => (
            <li key={n}>{n}</li>
          ))}
        </ul>
      ) : null}
      {result.save ? <p className="tr-saved">★ 연습할 문장으로 내 노트에 저장했어요</p> : null}
    </div>
  );
}

/** 네 단어 넘는 구절 — 한 덩어리 상자로 그리면 줄 끝에서 통째로 접혀서, 글처럼 줄을 바꾸게 둔다 */
function longPhrase(text: string): boolean {
  return text.trim().split(/\s+/).length >= 4;
}

/**
 * 문장 속 단어 칸. <button>은 한 덩어리(inline-block)로만 그려져 긴 구절이 줄을 못 바꾼다 —
 * 글자처럼 흐르는 span에 버튼 역할(키보드 Enter·Space)을 준다
 */
function Tap({
  className,
  disabled,
  expanded,
  label,
  onTap,
  children,
}: {
  className: string;
  disabled?: boolean;
  expanded?: boolean;
  label?: string;
  onTap: () => void;
  children: ReactNode;
}) {
  return (
    <span
      role="button"
      tabIndex={disabled ? -1 : 0}
      aria-disabled={disabled || undefined}
      aria-expanded={expanded}
      aria-label={label}
      className={className}
      onClick={(e) => {
        e.stopPropagation();
        if (!disabled) onTap();
      }}
      onKeyDown={(e) => {
        if (disabled || (e.key !== "Enter" && e.key !== " ")) return;
        e.preventDefault();
        e.stopPropagation();
        onTap();
      }}
    >
      {children}
    </span>
  );
}
