import { useEffect, useRef } from "react";
import type { TutorView } from "../tutor/view";
import { READ_NEXT_CMD } from "../tutor/policy/session";
import { PassagePager } from "./PassagePager";

type Props = {
  view: TutorView;
  onSend: (text: string) => void;
  onClose: () => void;
};

/**
 * 지문 읽기 — 분석에 들어가기 전에 글 전체를 한 번 쭉 본다.
 *
 * 문장이 하나씩 드러나며 소리로 읽히고, 화면은 읽는 문장을 따라 내려간다.
 * 학생은 언제든 「계속」으로 넘어갈 수 있고, ▶를 눌러 한 문장을 다시 들을 수 있다.
 * 글자는 학습 화면보다 작다 — 여기서는 뜻을 따지는 게 아니라 흐름을 본다.
 */
export function ReadPassage({ view, onSend, onClose }: Props) {
  const p = view.passage!;
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
    const u = new SpeechSynthesisUtterance(text);
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
    const text = p.sentences[p.current]!;
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

  return (
    <div className="stage-fill read">
      <header className="read-top">
        <button type="button" className="icon-btn dark" title="학습 종료" onClick={onClose}>
          <CloseIcon />
        </button>
        {p.auto === false ? (
          <span className="read-label">문제 보기</span>
        ) : (
          <div className="read-bar">
            {p.sentences.map((_, i) => (
              <i key={i} className={i < p.revealed ? "on" : ""} />
            ))}
          </div>
        )}
      </header>

      <div className="read-scroll">
        <p className="read-heading">{p.heading}</p>
        <h1 className="read-title">{p.title}</h1>
        {view.message ? <p className="read-note">{view.message}</p> : null}

        {/* 넘겨 보는 지문 — 문제 제목 아래 지문을 장으로, 마지막 장에 보기 */}
        {p.auto === false ? (
          <PassagePager sentences={p.sentences} underline={p.underline} options={p.options} />
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

      <div className="read-dock">
        {view.buttons.map((label, i) => (
          <button
            key={label}
            type="button"
            className={`read-continue${i > 0 ? " second" : ""}`}
            onClick={() => onSend(label)}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}

/** 시험에서 밑줄 친 구절은 여기서도 밑줄 */
function underlined(text: string, phrase: string | null) {
  if (!phrase) return text;
  const at = text.indexOf(phrase);
  if (at < 0) return text;
  return (
    <>
      {text.slice(0, at)}
      <u className="read-underline">{phrase}</u>
      {text.slice(at + phrase.length)}
    </>
  );
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
