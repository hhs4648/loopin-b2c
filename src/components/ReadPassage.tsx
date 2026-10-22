import { useEffect, useRef, useState } from "react";
import type { ReactNode } from "react";
import type { TutorView } from "../tutor/view";
import { MODE_TRY_BTN, READ_NEXT_CMD } from "../tutor/policy/session";
import { clock, type MiniItem } from "../tutor/mini";
import { getPolicyLesson } from "../tutor/policy/lessons";
import { getSet } from "../tutor/sets";
import { cleanWord, meaningOf } from "../tutor/miniWords";
import { addVocab } from "../tutor/vocab";
import { applySpeakBlanks } from "../tutor/spoken";
import { TeacherFigure, TeacherReaction } from "./TeacherFigure";
import { PassageFull } from "./PassageFull";
import { MarkArea, NO_MARKS, type Marks, type Overlay, type Pen } from "./MiniMarks";

type Props = {
  view: TutorView;
  onSend: (text: string) => void;
  onClose: () => void;
  /**
   * 코스의 문제(2026-10-20 선생님): 이 미리보기 화면 그대로 **시간을 재서** 푼다. 큰 버튼이 「시간 재서 풀어 볼게요 · N분」,
   * 분석은 밑줄 글자. `left`는 남은 초(시작 전엔 null, 넘기면 음수 — 계속 풀 수 있다)
   */
  course?: {
    minutes: number;
    left: number | null;
    analyzeBtn: string;
    /** 이 문제의 10분 모의고사 문항 — 시험 밑줄·펜 표시용 */
    item: MiniItem;
    /** 보라펜으로 표시한 모르는 단어가 바뀌면 (풀이 기록에 같이 남긴다) */
    onUnknown?: (words: { en: string; ko: string }[]) => void;
  };
  /**
   * 핵심어로 한 번에 풀기 (온보딩 예시 문제, 2026-10-22 선생님): 지문에 핵심어를 칠하고, 다정쌤이 「이 핵심어로 푸는 법」을
   * 말한 뒤 바로 보기를 고른다. 분석을 원하는 학생은 아래 「분석부터 할게요」로
   */
  quick?: { keys: string[]; howto: string; image?: { src: string; alt: string }; onAnalyze: () => void };
};

/**
 * 지문 읽기 — 분석에 들어가기 전에 글 전체를 한 번 쭉 본다.
 *
 * 문장이 하나씩 드러나며 소리로 읽히고, 화면은 읽는 문장을 따라 내려간다.
 * 학생은 언제든 「계속」으로 넘어갈 수 있고, ▶를 눌러 한 문장을 다시 들을 수 있다.
 * 글자는 학습 화면보다 작다 — 여기서는 뜻을 따지는 게 아니라 흐름을 본다.
 */
export function ReadPassage({ view, onSend, onClose, course, quick }: Props) {
  const p = view.passage!;
  // 핵심어로 풀기 — 아직 답을 안 골랐으면 다정쌤 풀이법 + 「분석부터 할게요」
  const quickSolving = !!quick && !!p.pickable && !p.picked;
  const modeScreen = p.auto === false && view.buttons.length === 2 && view.buttons[1] === MODE_TRY_BTN;
  // 처음 고르는 화면 — 「바로 풀어 볼게요」는 큰 버튼에서 빼서 위에 밑줄 글자로
  const tryLink = !course && modeScreen;
  // 코스(2026-10-20 선생님): 들어가자마자 시계가 가고 보기를 고를 수 있다. 분홍 버튼은 「분석하기」 하나
  const courseSolving = !!course && p.pickable;
  const dockButtons = tryLink ? view.buttons.slice(0, 1) : courseSolving || quickSolving ? [] : view.buttons;
  const left = course?.left ?? null;
  /* ── 코스 풀기: 펜 줄 — 모르는 단어(보라펜) · 형광펜 · 끊어읽기 (미니 모의고사와 같은 `MiniMarks`), 2026-10-20 선생님 ── */
  const [pen, setPen] = useState<Pen>("none");
  const [showSlash, setShowSlash] = useState(false);
  const [marks, setMarks] = useState<Marks>(NO_MARKS);
  const [toast, setToast] = useState<string | null>(null);
  // item.lesson은 세트 id — 끊어읽기·뜻은 그 세트의 분석 레슨에서
  const set = course?.item.lesson ? getSet(course.item.lesson) : null;
  const lesson = set ? getPolicyLesson(set.lessons[0]!) : null;
  const hasSlash = !!lesson?.sentences.some((x) => x.slashes?.length);
  const overlay: Overlay = { slashes: showSlash ? (lesson?.sentences.flatMap((x) => x.slashes ?? []) ?? []) : [], keys: [] };
  useEffect(() => {
    if (!toast) return;
    const id = window.setTimeout(() => setToast(null), 2600);
    return () => window.clearTimeout(id);
  }, [toast]);
  const putMarks = (m: Marks) => {
    setMarks(m);
    course?.onUnknown?.(m.unk.map((u) => ({ en: u.en, ko: u.ko })));
  };
  const onUnknown = (i: number, token: string, el: HTMLElement) => {
    const en = cleanWord(token);
    if (!en) return;
    if (marks.unk.some((u) => u.i === i)) {
      putMarks({ ...marks, unk: marks.unk.filter((u) => u.i !== i) });
      setToast(`「${en}」 모르는 단어에서 뺐어요`);
      return;
    }
    const ko = meaningOf(en, set?.lessons ?? []);
    putMarks({ ...marks, unk: [...marks.unk, { i, en, ko }] });
    if (ko) {
      const block = el.closest("p")?.textContent ?? "";
      const sentence = block.split(/(?<=[.!?”])\s+/).find((x) => x.includes(token)) ?? block;
      addVocab([{ en, ko, sentence: sentence.trim(), source: lesson?.id ?? "", kind: "word" }]);
    }
    setToast(ko ? `${en} — ${ko.split(" · ")[0]}` : `「${en}」 모르는 단어로 담았어요`);
  };
  const onTapUnknown = (i: number) => {
    const u = marks.unk.find((x) => x.i === i);
    if (u) setToast(u.ko ? `${u.en} — ${u.ko.split(" · ")[0]}` : `「${u.en}」 뜻을 아직 못 찾았어요`);
  };
  const sendRef = useRef(onSend);
  sendRef.current = onSend;
  const rows = useRef<(HTMLDivElement | null)[]>([]);
  /*
    읽는 중인 utterance를 붙들고 있는다. 크롬은 이 객체가 가비지 컬렉션되면
    `onend`를 부르지 않고 읽기가 멈춘 채로 남는다 — 그러면 다음 문장이 영영 안 온다.
  */
  const utter = useRef<SpeechSynthesisUtterance | null>(null);

  function speak(text: string, onEnd?: () => void) {
    if (!("speechSynthesis" in window)) return false;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(applySpeakBlanks(text, view.speakBlanks));
    u.lang = "en-US";
    u.rate = 0.95;
    if (onEnd) u.onend = onEnd;
    utter.current = u;
    // 방금 끊은 소리와 겹치지 않게 한 박자 뒤에 시작한다
    window.setTimeout(() => {
      if (utter.current === u) window.speechSynthesis.speak(u);
    }, 80);
    return true;
  }

  /*
    지금 문장을 읽고, 다 읽으면 잠시 뒤 다음 문장을 드러내 달라고 세션에 알린다.
    학생이 「계속」으로 나가면 정리(cleanup)에서 소리를 끊고, 끊긴 소리로는
    다음 문장을 부르지 않는다.
  */
  useEffect(() => {
    // 전체를 한 번에 보여 주는 지문(바로 풀기)은 혼자 읽어 나가지 않는다
    if (p.auto === false) return;
    let live = true;
    let timer = 0;
    let done = false;
    rows.current[p.current]?.scrollIntoView({ behavior: "smooth", block: "center" });
    const text = applySpeakBlanks(p.sentences[p.current]!, view.speakBlanks);
    const last = p.current >= p.sentences.length - 1;
    const advance = () => {
      if (!live || done) return;
      done = true;
      if (last) return;
      timer = window.setTimeout(() => {
        if (live) sendRef.current(READ_NEXT_CMD);
      }, 500);
    };
    const spoke = speak(text, advance);
    /*
      소리가 끝나는 신호를 못 받아도 멈추지 않는다. 브라우저 음성이 가끔 「읽는 중」인
      채로 굳고(크롬), 소리를 아예 못 내는 기기도 있다. 읽는 데 걸릴 만한 시간이
      지나면 다음 문장으로 간다.
    */
    const words = text.trim().split(/\s+/).length;
    const watchdog = window.setTimeout(advance, spoke ? words * 520 + 2500 : words * 380 + 800);
    return () => {
      live = false;
      window.clearTimeout(timer);
      window.clearTimeout(watchdog);
      if ("speechSynthesis" in window) window.speechSynthesis.cancel();
    };
    // 읽는 문장이 바뀔 때만
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [p.current]);

  // 바로 풀기를 누르면 화면은 그대로, 지문 아래 보기가 보이게 내려 준다
  useEffect(() => {
    if (!p.pickable) return;
    document.querySelector(".passage-options")?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [p.pickable]);

  return (
    <div className={`stage-fill read${p.auto === false ? " preview" : ""}`}>
      <header className="read-top">
        {p.auto === false ? null : (
          <button type="button" className="close-soft" title="학습 종료" aria-label="학습 종료" onClick={onClose}>
            <CloseIcon />
          </button>
        )}
        {p.auto === false ? (
          left != null ? (
            <span className={`read-label mini-clock${left < 0 ? " over" : left < 30 ? " low" : ""}`} aria-label={left < 0 ? "초과한 시간" : "남은 시간"}>
              ⏱ {left < 0 ? `+${clock(-left)} 초과` : clock(left)}
            </span>
          ) : (
            <span className="read-label">지문 한눈에 미리보기</span>
          )
        ) : (
          <div className="read-bar">
            {p.sentences.map((_, i) => (
              <i key={i} className={i < p.revealed ? "on" : ""} />
            ))}
          </div>
        )}
        {p.auto === false ? (
          <button type="button" className="close-soft" title="학습 종료" aria-label="학습 종료" onClick={onClose}>
            <CloseIcon />
          </button>
        ) : null}
      </header>

      <div className="read-scroll">
        {/* 문제 보기에서는 시험 이름을 빼둔다 — 문제 글과 겹친다 */}
        {p.auto !== false ? <p className="read-heading">{p.heading}</p> : null}
        <h1 className="read-title">{p.title}</h1>
        {view.message && p.auto !== false ? <p className="read-note">{view.message}</p> : null}

        {/* 코스 풀기 — 펜 줄. 미니 모의고사와 같은 보라펜·형광펜·끊어읽기 */}
        {course ? (
          <>
            <div className="mini-pens" role="toolbar" aria-label="펜">
              <button type="button" className={`pen-btn unk${pen === "unk" ? " on" : ""}`} aria-pressed={pen === "unk"} onClick={() => setPen(pen === "unk" ? "none" : "unk")}>
                <i /> 모르는 단어
              </button>
              <button type="button" className={`pen-btn hi${pen === "hi" ? " on" : ""}`} aria-pressed={pen === "hi"} onClick={() => setPen(pen === "hi" ? "none" : "hi")}>
                <i /> 형광펜
              </button>
              {hasSlash ? (
                <button type="button" className={`pen-btn slash${showSlash ? " on" : ""}`} aria-pressed={showSlash} onClick={() => setShowSlash(!showSlash)}>
                  / 끊어읽기
                </button>
              ) : null}
            </div>
            {toast ? <div className="mini-toast" role="status">{toast}</div> : null}
          </>
        ) : null}

        {/* 시험지처럼 — 문제 제목 아래 (주어진 문장) · 지문 전체 · 보기. 꼼꼼히 읽히려는 게 아니다 */}
        {p.auto === false && course ? (
          <MarkArea pen={pen} marks={marks} onHighlight={(hi) => putMarks({ ...marks, hi })} onUnknown={onUnknown} onTapUnknown={onTapUnknown}>
            <PassageFull
              given={p.given}
              sentences={p.sentences}
              underline={p.underline}
              options={p.options}
              numbersOnly={p.numbersOnly}
              onPick={p.pickable ? onSend : null}
              picked={p.picked}
              right={p.right}
              // 시간 재서 푸는 화면엔 문장 듣기(▶)를 두지 않는다 (2026-10-21 선생님)
              mark={{ item: course.item, marks, overlay }}
            />
          </MarkArea>
        ) : p.auto === false ? (
          <>
          {/* 한 번에 풀기 그림 (데카르트의 나무) — 글로만 읽으면 어려운 비유를 그림으로 먼저 */}
          {quick?.image ? <img className="quick-picture" src={quick.image.src} alt={quick.image.alt} /> : null}
          <PassageFull
            given={p.given}
            sentences={p.sentences}
            underline={p.underline}
            options={p.options}
            numbersOnly={p.numbersOnly}
            onPick={p.pickable ? onSend : null}
            picked={p.picked}
            right={p.right}
            highlight={quick?.keys}
            // 지문 한눈에 미리보기에도 문장 듣기(▶)를 두지 않는다 (2026-10-21 선생님)
          />
          </>
        ) : null}

        {/* (.read-list는 display:flex라 hidden 속성이 안 먹는다 — 아예 그리지 않는다) */}
        {p.auto !== false ? (
        <div className="read-list">
          {p.sentences.slice(0, p.revealed).map((text, i) => (
            <div
              key={i}
              ref={(el) => {
                rows.current[i] = el;
              }}
              className={`read-row${i === p.current ? " now" : ""}`}
            >
              <button
                type="button"
                className="read-play"
                aria-label={`${i + 1}번째 문장 듣기`}
                onClick={() => speak(text)}
              >
                <PlayIcon />
              </button>
              <p className="read-text">{underlined(text, p.underline)}</p>
            </div>
          ))}
        </div>
        ) : null}
      </div>

      {/* 지문 미리보기에서는 버튼을 한 줄로 — 지문 자리를 넓힌다 */}
      <div className={`read-dock${p.auto === false && dockButtons.length >= 2 ? " row" : ""}`}>
        {/* 미리보기 화면에서 선생님 말(바로 풀기 안내, 채점)은 버튼 바로 위에 — 보기를 고르는 손 가까이 */}
        {/* 풀기 안내(「실제 시험처럼 풀어 봐요 …」)는 뺐다 — 풀 때는 말하지 않는다 (2026-10-21 선생님) */}
        {courseSolving ? null : quickSolving ? (
          <p className="read-say">{quick!.howto}</p>
        ) : view.message && p.auto === false ? (
          // 채점 말 — 고른 쌤 얼굴(표정)과 한마디를 같이
          <div className="read-say with-face">
            <span className="read-face" aria-hidden="true">
              <TeacherFigure mood={view.mood} />
            </span>
            <p>
              {view.message}
              <TeacherReaction reaction={view.reaction} />
            </p>
          </div>
        ) : null}
        {quickSolving ? (
          <button type="button" className="read-try-link" onClick={quick!.onAnalyze}>
            분석부터 할게요
          </button>
        ) : null}
        {courseSolving ? (
          <button type="button" className="read-continue" onClick={() => onSend(course!.analyzeBtn)}>
            분석하기
          </button>
        ) : dockButtons.map((label, i) => (
          <button
            key={label}
            type="button"
            className={`read-continue${i > 0 ? " second" : ""}`}
            onClick={() => onSend(label)}
          >
            {label}
          </button>
        ))}

        {/* 「바로 풀어 볼게요」는 큰 버튼 아래에 밑줄 글자로 — 큰 버튼은 「분석하러 갈게요」 하나 */}
        {tryLink ? (
          <button type="button" className="read-try-link" onClick={() => onSend(MODE_TRY_BTN)}>
            {MODE_TRY_BTN}
          </button>
        ) : null}
      </div>
    </div>
  );
}

/** 시험에서 밑줄 친 구절은 여기서도 밑줄 */
function underlined(text: string, phrases: string[]) {
  const hits = phrases
    .map((p) => [text.indexOf(p), p] as const)
    .filter(([at]) => at >= 0)
    .sort((a, b) => a[0] - b[0]);
  if (!hits.length) return text;
  const out: ReactNode[] = [];
  let pos = 0;
  for (const [at, p] of hits) {
    if (at < pos) continue;
    out.push(text.slice(pos, at), <u key={at} className="read-underline">{p}</u>);
    pos = at + p.length;
  }
  out.push(text.slice(pos));
  return <>{out}</>;
}

function PlayIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M7 4.5v15l12-7.5z" />
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
