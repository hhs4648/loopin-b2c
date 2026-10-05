import { ClassroomBg } from "./ClassroomBg";
import { TeacherFigure } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { InputBar } from "./InputBar";
import type { TutorView } from "../tutor/engine";
import { nounKind } from "../tutor/proper-nouns";

type Props = {
  view: TutorView;
  /** 지금 푸는 세트 이름. 목록에서 고른 게 뭔지 화면에 남겨 둔다 */
  setTitle?: string;
  elapsed: string;
  typing: boolean;
  onSend: (text: string) => void;
  onClose: () => void;
  /**
   * 단위로 쪼갠 문제에서, 이 단위 다음에 할 단위. 끝났을 때 「다음」과 「쉬기」를
   * 나란히 둔다 — 끊어도 되는 자리라는 걸 학생이 알 수 있게.
   */
  next?: { title: string; onGo: () => void } | null;
};

export function ClassroomChat({ view, setTitle, elapsed, typing, onSend, onClose, next }: Props) {
  // 칩이 뜨면 아래 도크가 그만큼 높아진다. 학생 말풍선을 같이 올리지 않으면 가린다
  const showNouns = view.properNouns.length > 0 && !view.ended;

  return (
    <div className="stage-fill">
      <ClassroomBg />
      <header className="top-bar">
        <div className="chip">
          <span className="avatar">다</span>
          <div className="chip-text">
            <strong>다정쌤</strong>
            <small>{setTitle ?? "오늘의 학습"}</small>
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

      {/* 칠판에 띄우는 그림 (도입의 데카르트 초상 등). 파일이 없으면 조용히 숨는다 */}
      {view.boardImage ? (
        <figure className={`board-image ${view.boardImage.kind ?? "photo"}`} key={view.boardImage.src}>
          <img
            src={view.boardImage.src}
            alt={view.boardImage.alt}
            onError={(e) => {
              (e.currentTarget.parentElement as HTMLElement).hidden = true;
            }}
          />
          {view.boardImage.credit ? <figcaption>{view.boardImage.credit}</figcaption> : null}
        </figure>
      ) : null}

      <div className="teacher-full">
        <div className="teacher-bob">
          <TeacherFigure />
        </div>
      </div>

      <div className="teacher-bubble">
          <div
            className={`bubble-card${view.effect === "light" ? " lit" : ""}`}
            aria-live="polite"
          >
          {typing ? <TypingDots /> : <span>{view.message}</span>}
          <i className="bubble-tail" />
        </div>
      </div>

      {view.studentLine ? (
        <div className={`student-bubble${showNouns ? " raised" : ""}`}>
          {view.studentLine}
        </div>
      ) : null}

      <div className="dock">
        {/*
          **고유명사는 말로 설명하지 않고 여기서 보여 준다.** 예전에는 인트로
          대사에 "Lewis Ltd.는 회사 이름이라 …"가 끼어 있었다. 문장을 보지도 않은
          학생에게 문장 이야기를 먼저 하는 셈이라 뺐다.

          문장 학습 화면의 칩은 안내문 없이 혼자 서야 해서 「· 그대로」를 달고
          있다. 여기는 위에 한 줄이 있으니 붙이지 않는다.
        */}
        {showNouns ? (
          <div className="noun-intro">
            <span className="noun-intro-label">그대로 쓰면 되는 이름이에요</span>
            <div className="noun-chips intro">
              {view.properNouns.map((n) => (
                <span key={n.en} className="noun-chip">
                  {n.en} · {nounKind(n.type)}
                </span>
              ))}
            </div>
          </div>
        ) : null}
        <QuickReplies buttons={view.buttons} hidden={typing || view.ended} onPick={onSend} />
        {view.ended ? (
          next ? (
            <div className="quick-row end-row">
              <button type="button" className="pill aux" onClick={onClose}>
                여기서 쉴게요
              </button>
              <button type="button" className="pill" onClick={next.onGo}>
                다음: {next.title}
              </button>
            </div>
          ) : (
            <button type="button" className="pill restart" onClick={onClose}>
              수업 목록으로
            </button>
          )
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
