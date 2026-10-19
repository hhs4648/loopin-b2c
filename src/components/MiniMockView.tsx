import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import type { LessonSet } from "../../content/tutor/types";
import {
  byKind,
  clock,
  loadAttempts,
  saveAttempt,
  scoreOf,
  type MiniAttempt,
  type MiniItem,
  type MiniMock,
} from "../tutor/mini";
import { getSet } from "../tutor/sets";
import { loadLearnerName } from "../tutor/learner-name";
import { getUser, MiniRecorder, startAnalysis } from "../tutor/miniLog";
import { MiniTeacherBoard } from "./MiniTeacherBoard";
import { MarkArea, markWords, NO_MARKS, type Marks } from "./MiniMarks";
import { cleanWord, meaningOf } from "../tutor/miniWords";
import { addVocab } from "../tutor/vocab";

const NUM = "①②③④⑤";

/**
 * 푸는 중에 분석 레슨으로 간 시험 — 돌아오면 같은 문항에서 이어 푼다(분석한 시간은 시험 시간에서 뺀다).
 * 화면이 닫혀도 남아야 해서 모듈에 둔다
 */
type Paused = { mockId: string; answers: Record<number, number>; checked: number[]; peeked: number[]; marks: Record<number, Marks>; at: number; usedMs: number; recorder: MiniRecorder | null };
let paused: Paused | null = null;
export function hasPausedExam(mockId: string): boolean {
  return paused?.mockId === mockId;
}

type Props = {
  mock: MiniMock;
  /** 처음부터 지난 결과를 보일까 (분석 레슨을 보고 돌아왔을 때) */
  showLast: boolean;
  onBack: () => void;
  /** 분석 레슨으로. fromExam이면 푸는 중에 간 것 — 돌아오면 이어 푼다 */
  onAnalyze: (set: LessonSet, fromExam: boolean) => void;
  /** 학생 테스트용 링크 — 목록 없이 이 시험만. 이름을 받고 지표를 남긴다 */
  standalone?: boolean;
};

const NAME_KEY = "loopin.mini.name";
function savedName(): string {
  try {
    return window.localStorage.getItem(NAME_KEY) ?? "";
  } catch {
    return "";
  }
}

/**
 * 미니 모의고사 — 시작 → 시간 재며 풀기(문항마다 바로 정답 확인·분석도 된다) → 제출(또는 시간 끝) → 점수와 문항별 해설.
 * 수업과 달리 선생님 말은 없다. 실제 시험처럼 문제만.
 */
export function MiniMockView({ mock, showLast, onBack, onAnalyze, standalone }: Props) {
  const resume = paused?.mockId === mock.id ? paused : null;
  const [stage, setStage] = useState<"intro" | "exam" | "result">(() =>
    resume ? "exam" : showLast && loadAttempts(mock.id).length ? "result" : "intro",
  );
  const [attempt, setAttempt] = useState<MiniAttempt | null>(() => (showLast ? (loadAttempts(mock.id)[0] ?? null) : null));
  const [name, setName] = useState(() => (standalone ? savedName() : (loadLearnerName() ?? "")));
  /** 선생님(아티팩트 주인)인가 */
  const [owner, setOwner] = useState(false);
  const [board, setBoard] = useState(false);
  const recorder = useRef<MiniRecorder | null>(resume?.recorder ?? null);
  const [initial] = useState(() => {
    paused = null;
    return resume;
  });
  useEffect(() => {
    if (!standalone) return;
    void getUser().then(async (u) => setOwner((await u?.isOwner()) ?? false));
  }, [standalone]);

  const start = () => {
    recorder.current = new MiniRecorder(mock, name.trim());
    setStage("exam");
  };

  if (board) return <MiniTeacherBoard mock={mock} onBack={() => setBoard(false)} />;

  if (stage === "exam") {
    return (
      <MiniExam
        mock={mock}
        initial={initial}
        recorder={recorder.current}
        onQuit={() => setStage("intro")}
        onSubmit={(a) => {
          saveAttempt(mock.id, a);
          setAttempt(a);
          setStage("result");
        }}
        onAnalyze={(set, state) => {
          paused = { ...state, mockId: mock.id, recorder: recorder.current };
          startAnalysis(recorder.current, state.no);
          onAnalyze(set, true);
        }}
      />
    );
  }
  if (stage === "result" && attempt) {
    return (
      <MiniResult
        mock={mock}
        attempt={attempt}
        recorder={recorder.current}
        onBack={standalone ? () => setStage("intro") : onBack}
        onRetry={start}
        onAnalyze={(set, no) => {
          startAnalysis(recorder.current, no);
          onAnalyze(set, false);
        }}
      />
    );
  }
  const last = loadAttempts(mock.id)[0];
  const max = mock.items.reduce((n, it) => n + it.points, 0);
  return (
    <div className="stage-fill saved mini">
      <header className="saved-top">
        {standalone ? null : (
          <button type="button" className="icon-btn light" title="목록으로" aria-label="목록으로" onClick={onBack}>
            <BackIcon />
          </button>
        )}
      </header>
      <div className="saved-body-scroll">
        <p className="home-hello">미니 모의고사</p>
        <h1 className="saved-title">{mock.title}</h1>
        <p className="mini-sub">{mock.subtitle}</p>
        <ul className="mini-facts">
          <li><b>{mock.minutes}분</b><small>제한 시간</small></li>
          <li><b>{mock.items.length}문항</b><small>{mock.items[0]!.no}~{mock.items[mock.items.length - 1]!.no}번 차례대로</small></li>
          <li><b>{max}점</b><small>만점</small></li>
        </ul>
        <p className="pack-help">
          실제 시험처럼 시간을 재며 풀어요. 한 문제를 풀고 바로 「정답 확인」을 눌러 맞혀 볼 수도 있어요.
          틀린 문제나 모르는 문제는 다정쌤과 분석하러 갈 수 있고, 분석하는 동안은 시계가 멈춰요. ⏸ 버튼으로 잠깐 쉴 수도 있어요.
        </p>
        {standalone ? (
          <label className="mini-name">
            <span>이름</span>
            <input
              id="mini-name"
              value={name}
              maxLength={20}
              placeholder="이름을 적어 주세요"
              onChange={(e) => {
                setName(e.target.value);
                try {
                  window.localStorage.setItem(NAME_KEY, e.target.value);
                } catch {
                  /* 다음에 다시 적으면 된다 */
                }
              }}
            />
          </label>
        ) : null}
        <button type="button" className="mini-start" disabled={standalone && !name.trim()} onClick={start}>
          시작하기
        </button>
        {owner ? (
          <button type="button" className="mini-last" onClick={() => setBoard(true)}>
            선생님 · 학생 결과 보기
          </button>
        ) : null}
        {last ? (
          <button
            type="button"
            className="mini-last"
            onClick={() => {
              setAttempt(last);
              setStage("result");
            }}
          >
            지난 결과 보기 · {scoreOf(mock, last.answers).score}/{max}점
          </button>
        ) : null}
      </div>
    </div>
  );
}

type ExamState = { answers: Record<number, number>; checked: number[]; peeked: number[]; marks: Record<number, Marks>; at: number; usedMs: number; no: number };

function MiniExam({
  mock,
  initial,
  recorder,
  onQuit,
  onSubmit,
  onAnalyze,
}: {
  mock: MiniMock;
  initial: Paused | null;
  recorder: MiniRecorder | null;
  onQuit: () => void;
  onSubmit: (a: MiniAttempt) => void;
  onAnalyze: (set: LessonSet, state: ExamState) => void;
}) {
  const limit = mock.minutes * 60;
  const [answers, setAnswers] = useState<Record<number, number>>(initial?.answers ?? {});
  /** 「정답 확인」을 누른 문항 — 그 문항은 답을 바꿀 수 없다 */
  const [checked, setChecked] = useState<number[]>(initial?.checked ?? []);
  /** 답을 고르기 전에 분석을 먼저 본 문항 — 돌아와서 고를 수 있지만 「분석 보고 고름」으로 따로 표시 */
  const [peeked, setPeeked] = useState<number[]>(initial?.peeked ?? []);
  /** 지문에 표시한 것 — 문항마다 형광펜·모르는 단어 */
  const [marks, setMarks] = useState<Record<number, Marks>>(initial?.marks ?? {});
  const [toast, setToast] = useState<string | null>(null);
  useEffect(() => {
    if (!toast) return;
    const id = window.setTimeout(() => setToast(null), 1600);
    return () => window.clearTimeout(id);
  }, [toast]);
  const unknownList = () => mock.items.flatMap((it) => (marks[it.no]?.unk ?? []).map((u) => ({ no: it.no, en: u.en, ko: u.ko })));
  const [at, setAt] = useState(initial?.at ?? 0);
  // 분석하러 갔다 오면 쓴 시간만큼 이어서 — 분석한 시간은 빠진다
  const started = useRef(Date.now() - (initial?.usedMs ?? 0));
  const [left, setLeft] = useState(limit - (initial?.usedMs ?? 0) / 1000);
  const [confirm, setConfirm] = useState<"submit" | "quit" | null>(null);
  /** 「일시정지」를 누른 때 — 그동안 시계가 멈추고 문제는 가려진다 */
  const [breakAt, setBreakAt] = useState<number | null>(null);
  const done = useRef(false);
  const scroll = useRef<HTMLDivElement>(null);

  const submit = (timeUp: boolean) => {
    if (done.current) return;
    done.current = true;
    recorder?.finish(timeUp ? "timeup" : "submitted", answers);
    onSubmit({ at: new Date().toISOString(), answers, seconds: Math.min(limit, (Date.now() - started.current) / 1000), timeUp, checked, peeked, unknown: unknownList() });
  };
  // 남은 시간 — 시계로 잰다 (탭이 잠깐 멈춰도 어긋나지 않게)
  useEffect(() => {
    if (breakAt != null) return;
    const id = window.setInterval(() => {
      const rest = limit - (Date.now() - started.current) / 1000;
      setLeft(rest);
      if (rest <= 0) submit(true);
    }, 500);
    return () => window.clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [answers, checked, breakAt]);
  const pause = () => {
    recorder?.pause();
    setBreakAt(Date.now());
  };
  const resume = () => {
    if (breakAt == null) return;
    started.current += Date.now() - breakAt;
    recorder?.resume();
    setBreakAt(null);
  };
  useEffect(() => {
    scroll.current?.scrollTo({ top: 0 });
    // 위 번호 줄도 지금 문항이 보이게
    document.querySelector(".mini-grid button.now")?.scrollIntoView({ inline: "center", block: "nearest" });
    recorder?.enter(mock.items[at]!.no);
  }, [at, mock, recorder]);

  const item = mock.items[at]!;
  const itemMarks = marks[item.no] ?? NO_MARKS;
  const wordsOf = (idx: number[]) => idx.map((i) => cleanWord(scroll.current?.querySelector(`[data-i="${i}"]`)?.textContent ?? "")).filter(Boolean);
  const putMarks = (m: Marks) => {
    setMarks((all) => ({ ...all, [item.no]: m }));
    recorder?.marks(item.no, wordsOf(m.hi), m.unk.map((u) => u.en));
  };
  const onHighlight = (hi: number[]) => putMarks({ ...itemMarks, hi });
  const onUnknown = (i: number, token: string, el: HTMLElement) => {
    const en = cleanWord(token);
    if (!en) return;
    if (itemMarks.unk.some((u) => u.i === i)) {
      putMarks({ ...itemMarks, unk: itemMarks.unk.filter((u) => u.i !== i) });
      setToast(`「${en}」 모르는 단어에서 뺐어요`);
      return;
    }
    const ko = meaningOf(en, set?.lessons ?? []);
    putMarks({ ...itemMarks, unk: [...itemMarks.unk, { i, en, ko }] });
    if (ko) {
      // 단어장에도 — 그 낱말이 든 문장과 같이
      const block = el.closest("p")?.textContent ?? "";
      const sentence = block.split(/(?<=[.!?”])\s+/).find((x) => x.includes(token)) ?? block;
      addVocab([{ en, ko, sentence: sentence.trim(), source: set?.lessons[0] ?? mock.id, kind: "word" }]);
    }
    setToast(`「${en}」 모르는 단어로 담았어요${ko ? ` · ${ko.split(" · ")[0]}` : ""}`);
  };
  const unanswered = mock.items.filter((it) => !answers[it.no]).length;
  const last = at === mock.items.length - 1;
  const isChecked = checked.includes(item.no);
  const set = item.lesson ? getSet(item.lesson) : null;
  return (
    <div className="stage-fill saved mini mini-exam">
      {toast ? <div className="mini-toast" role="status">{toast}</div> : null}
      <header className="mini-top">
        <button type="button" className="mini-quit" onClick={() => setConfirm("quit")}>그만</button>
        <span className="mini-clock-wrap">
          <span className={`mini-clock${left < 120 ? " low" : ""}`} aria-label="남은 시간">⏱ {clock(left)}</span>
          <button type="button" className="mini-pause" onClick={pause} aria-label="일시정지">⏸</button>
        </span>
        <button type="button" className="mini-submit" onClick={() => setConfirm("submit")}>제출</button>
      </header>
      <nav className="mini-grid" aria-label="문항">
        {mock.items.map((it, i) => {
          const mark = checked.includes(it.no) ? (answers[it.no] === it.answer ? " ok" : " ng") : "";
          return (
            <button key={it.no} type="button" className={`${i === at ? "now" : ""}${answers[it.no] ? " done" : ""}${mark}${peeked.includes(it.no) ? " peek" : ""}`} onClick={() => setAt(i)}>
              {it.no}
            </button>
          );
        })}
      </nav>
      <div className="saved-body-scroll" ref={scroll}>
        <ItemView
          item={item}
          picked={answers[item.no] ?? null}
          review={isChecked}
          marks={itemMarks}
          onHighlight={onHighlight}
          onUnknown={onUnknown}
          onPick={isChecked ? undefined : (n) => {
            recorder?.pick(item.no, n);
            setAnswers({ ...answers, [item.no]: n });
          }}
        />
        {peeked.includes(item.no) && !isChecked ? (
          <p className="mini-peek-note">다정쌤 분석을 보고 고르는 문항이에요. 결과에 「분석 보고 고름」으로 따로 표시돼요.</p>
        ) : null}
        {isChecked ? (
          <CheckPanel
            item={item}
            peeked={peeked.includes(item.no)}
            unknown={itemMarks.unk}
            picked={answers[item.no] ?? null}
            recorder={recorder}
            onAnalyze={set ? () => onAnalyze(set, { answers, checked, peeked, marks, at, usedMs: Date.now() - started.current, no: item.no }) : null}
          />
        ) : (
          <>
          <button
            type="button"
            className="mini-check"
            disabled={!answers[item.no]}
            onClick={() => {
              recorder?.check(item.no, answers[item.no] === item.answer);
              setChecked([...checked, item.no]);
            }}
          >
            {answers[item.no] ? "정답 확인" : "답을 고르면 바로 정답을 확인할 수 있어요"}
          </button>
          {set && !answers[item.no] && !peeked.includes(item.no) ? (
            <button
              type="button"
              className="mini-analyze-first"
              onClick={() => {
                // 돌아와서 답을 고를 수 있다 — 대신 「분석 보고 고름」으로 따로 남긴다
                recorder?.peek(item.no);
                const next = [...peeked, item.no];
                setPeeked(next);
                onAnalyze(set, { answers, checked, peeked: next, marks, at, usedMs: Date.now() - started.current, no: item.no });
              }}
            >
              <b>답 고르지 않고 다정쌤 분석 보기 ›</b>
              <small>돌아와서 답을 고를 수 있어요 · 「분석 보고 고름」으로 따로 표시돼요</small>
            </button>
          ) : null}
          </>
        )}
      </div>
      <footer className="mini-foot">
        <button type="button" disabled={at === 0} onClick={() => setAt(at - 1)}>‹ 이전</button>
        <span>{at + 1} / {mock.items.length}</span>
        {last ? (
          <button type="button" className="primary" onClick={() => setConfirm("submit")}>제출하기</button>
        ) : (
          <button type="button" onClick={() => setAt(at + 1)}>다음 ›</button>
        )}
      </footer>
      {breakAt != null ? (
        <div className="mini-confirm mini-break" role="dialog" aria-label="일시정지">
          <div>
            <p><b>일시정지 중</b><br />시계가 멈췄어요. 문제는 잠시 가려 둘게요.</p>
            <button type="button" className="primary" onClick={resume}>이어 풀기</button>
          </div>
        </div>
      ) : null}
      {confirm ? (
        <div className="mini-confirm" role="dialog">
          <div>
            <p>
              {confirm === "quit"
                ? "그만두면 이번 풀이는 남지 않아요. 그만둘까요?"
                : unanswered
                  ? `아직 안 푼 문항이 ${unanswered}개 있어요. 그래도 제출할까요?`
                  : "제출할까요?"}
            </p>
            <button type="button" className="primary" onClick={() => {
              if (confirm === "quit") {
                recorder?.finish("quit", answers);
                onQuit();
              } else submit(false);
            }}>
              {confirm === "quit" ? "그만두기" : "제출하기"}
            </button>
            <button type="button" onClick={() => setConfirm(null)}>계속 풀기</button>
          </div>
        </div>
      ) : null}
    </div>
  );
}

/** 푸는 중에 「정답 확인」을 누른 문항 — 맞고 틀림, 해설, 분석하러 가기 */
function CheckPanel({
  item,
  peeked,
  unknown,
  picked,
  recorder,
  onAnalyze,
}: {
  item: MiniItem;
  peeked?: boolean;
  unknown?: Marks["unk"];
  picked: number | null;
  recorder: MiniRecorder | null;
  onAnalyze: (() => void) | null;
}) {
  const right = picked === item.answer;
  return (
    <div className={`mini-checked ${right ? "right" : "wrong"}`}>
      <p className="mini-verdict">
        {peeked ? <i className="mini-tag peek">분석 보고 고름</i> : null}
        {right ? "○ 맞았어요!" : `✕ 아쉽게도 틀렸어요. 정답은 ${NUM[item.answer - 1]}예요.`}
        {item.wrong_rate != null ? <small> · 전국 오답률 {item.wrong_rate}%</small> : null}
      </p>
      {onAnalyze ? (
        <button type="button" className="mini-analyze big" onClick={onAnalyze}>
          <b>다정쌤과 이 문제 분석하기 ›</b>
          <small>문장마다 같이 읽으며 왜 답이 되는지 찾아요 · 분석하는 동안 시계가 멈춰요</small>
        </button>
      ) : (
        <p className="mini-no-lesson">이 문제는 아직 다정쌤 분석이 없어요. 아래 해설을 봐요.</p>
      )}
      {item.fix ? <p className="mini-fix">{item.fix}</p> : null}
      {unknown?.length ? <UnknownWords words={unknown} /> : null}
      {item.intent ? <p className="mini-intent">{item.intent}</p> : null}
      <Translation item={item} recorder={recorder} />
    </div>
  );
}

/** 「해석 보기」 — 지문 해석 + 선지 해석(있으면) */
function Translation({ item, recorder }: { item: MiniItem; recorder: MiniRecorder | null }) {
  if (!item.translation && !item.options_ko?.length) return null;
  return (
    <details onToggle={(e) => e.currentTarget.open && recorder?.opened(item.no, "translated")}>
      <summary>해석 보기{item.options_ko?.length ? " (지문 · 선지)" : ""}</summary>
      {item.translation ? <p className="mini-trans">{item.translation}</p> : null}
      {item.options_ko?.length ? (
        <ol className="mini-trans-options">
          {item.options_ko.map((ko, i) => (
            <li key={i} className={i + 1 === item.answer ? "answer" : undefined}>
              <b>{NUM[i]}</b> {ko}
            </li>
          ))}
        </ol>
      ) : null}
    </details>
  );
}

/** 두 번 두드려 담은 모르는 단어 — 뜻은 분석 레슨에서 (없으면 「분석에서 확인」) */
function UnknownWords({ words }: { words: { en: string; ko: string; no?: number }[] }) {
  return (
    <div className="mini-unknown">
      <p className="mini-unknown-title">모르는 단어 {words.length}개{words.some((w) => w.ko) ? " · 뜻이 있는 단어는 단어장에도 담았어요" : ""}</p>
      <ul>
        {words.map((w, k) => (
          <li key={`${w.no ?? ""}-${w.en}-${k}`}>
            <b>{w.en}</b>
            <span>{w.ko ? w.ko : <i>뜻은 분석·해석에서 확인해요</i>}</span>
            {w.no ? <small>{w.no}번</small> : null}
          </li>
        ))}
      </ul>
    </div>
  );
}

function ItemView({
  item,
  picked,
  onPick,
  review,
  marks,
  onHighlight,
  onUnknown,
}: {
  item: MiniItem;
  picked: number | null;
  onPick?: (n: number) => void;
  /** 결과 화면 — 정답·내 답을 칠한다 */
  review?: boolean;
  /** 푸는 중 — 지문에 형광펜·모르는 단어 표시 */
  marks?: Marks;
  onHighlight?: (hi: number[]) => void;
  onUnknown?: (i: number, token: string, el: HTMLElement) => void;
}) {
  const numbersOnly = item.options.every((o) => !o);
  const ctx = marks ? { counter: { n: 0 }, marks } : null;
  const body = (
    <>
      {item.given ? <p className="mini-given">{passageNodes(item.given, item, ctx, "g")}</p> : null}
      {item.passage ? <p className="mini-passage">{passageNodes(item.passage, item, ctx, "p")}</p> : null}
      {item.paragraphs?.map((p, k) => (
        <p key={p.slice(0, 12)} className="mini-passage para">{passageNodes(p, item, ctx, `r${k}`)}</p>
      ))}
      {item.after ? <p className="mini-given after">{passageNodes(item.after, item, ctx, "a")}</p> : null}
    </>
  );
  return (
    <article className="mini-item">
      {item.group ? <p className="mini-group">{item.group}</p> : null}
      <p className="mini-q">
        <b>{item.no}.</b> {item.question}
      </p>
      {marks && onHighlight && onUnknown ? (
        <>
          <p className="mini-mark-hint">두 번 두드리면 <b className="unk">모르는 단어</b> · 길게 누르거나 끌면 <b className="hi">형광펜</b></p>
          <MarkArea marks={marks} onHighlight={onHighlight} onUnknown={onUnknown}>{body}</MarkArea>
        </>
      ) : body}
      {item.foot ? <p className="mini-foot-note">{item.foot}</p> : null}
      <ol className={`mini-options${numbersOnly ? " numbers" : ""}`}>
        {item.options.map((o, i) => {
          const n = i + 1;
          const state = review
            ? n === item.answer
              ? " right"
              : n === picked
                ? " wrong"
                : ""
            : n === picked
              ? " picked"
              : "";
          return (
            <li key={n}>
              <button type="button" className={`mini-opt${state}`} disabled={!onPick} onClick={() => onPick?.(n)}>
                <b>{NUM[i]}</b>
                {o ? <span>{o}</span> : null}
              </button>
            </li>
          );
        })}
      </ol>
    </article>
  );
}

/** 밑줄(함축 의미), ①~⑤·(a)~(e) 뒤 낱말 밑줄(어법·어휘·지칭), 빈칸, 문장 넣기 자리 표시 */
function passageNodes(text: string, item: MiniItem, ctx: { counter: { n: number }; marks: Marks } | null = null, key = ""): ReactNode[] {
  const out: ReactNode[] = [];
  const re = item.underline
    ? new RegExp(`(${item.underline.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}|_{4,}|\\([①②③④⑤]\\))`)
    : item.marked
      ? /((?:[①②③④⑤]|\([a-e]\))[^\s.,;:!?”]+|_{4,})/
      : /(_{4,}|\([①②③④⑤]\))/;
  text.split(re).forEach((part, i) => {
    if (!part) return;
    if (i % 2 === 0) out.push(...markWords(part, `${key}${i}`, ctx?.counter ?? { n: 0 }, ctx?.marks ?? null));
    else if (/^_{4,}$/.test(part)) out.push(<span key={i} className="mini-blank" aria-label="빈칸" />);
    else if (/^\([①②③④⑤]\)$/.test(part)) out.push(<b key={i} className="mini-slot">{part}</b>);
    else if (item.marked) {
      const mark = part.startsWith("(") ? part.slice(0, 3) : part[0]!;
      out.push(<u key={i}><b>{mark}</b>{part.slice(mark.length)}</u>);
    }
    else out.push(<u key={i}>{part}</u>);
  });
  return out;
}

function MiniResult({
  mock,
  attempt,
  recorder,
  onBack,
  onRetry,
  onAnalyze,
}: {
  mock: MiniMock;
  attempt: MiniAttempt;
  recorder: MiniRecorder | null;
  onBack: () => void;
  onRetry: () => void;
  onAnalyze: (set: LessonSet, no: number) => void;
}) {
  const s = useMemo(() => scoreOf(mock, attempt.answers), [mock, attempt]);
  const kinds = useMemo(() => byKind(mock, attempt.answers), [mock, attempt]);
  // 분석을 먼저 보고 고른 문항을 뺀 점수 — 그런 문항이 있을 때만
  const own = useMemo(() => attempt.peeked?.length
    ? scoreOf(mock, Object.fromEntries(Object.entries(attempt.answers).filter(([no]) => !attempt.peeked!.includes(Number(no)))))
    : null, [mock, attempt]);
  const [open, setOpen] = useState<number | null>(null);
  return (
    <div className="stage-fill saved mini">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="목록으로" aria-label="목록으로" onClick={onBack}>
          <BackIcon />
        </button>
      </header>
      <div className="saved-body-scroll">
        <p className="home-hello">{mock.title} · 결과</p>
        <div className="mini-score">
          <b>{s.score}</b>
          <span>/ {s.max}점</span>
        </div>
        <ul className="mini-facts">
          <li><b>{s.correct} / {s.total}</b><small>맞힌 문항</small></li>
          {own ? <li><b>{own.score}점</b><small>분석 안 보고 맞힌 점수 · 분석 보고 고른 문항 {attempt.peeked!.length}개</small></li> : null}
          <li><b>{clock(attempt.seconds)}</b><small>{attempt.timeUp ? "시간 끝" : `걸린 시간 (제한 ${mock.minutes}분)`}</small></li>
        </ul>
        <div className="mini-kinds">
          {kinds.map((k) => (
            <span key={k.kind} className={k.right === k.total ? "all" : k.right === 0 ? "none" : ""}>
              {k.kind} {k.right}/{k.total}
            </span>
          ))}
        </div>

        {attempt.unknown?.length ? <UnknownWords words={attempt.unknown} /> : null}

        <h2 className="group-title">문항별</h2>
        <ul className="mini-review">
          {mock.items.map((it) => {
            const mine = attempt.answers[it.no] ?? null;
            const right = mine === it.answer;
            const set = it.lesson ? getSet(it.lesson) : null;
            const isOpen = open === it.no;
            return (
              <li key={it.no} className={right ? "right" : "wrong"}>
                <button type="button" className="mini-row" onClick={() => {
                  if (!isOpen) recorder?.opened(it.no, "reviewed");
                  setOpen(isOpen ? null : it.no);
                }}>
                  <span className="mini-mark">{right ? "○" : "✕"}</span>
                  <span className="mini-row-text">
                    <b>{it.no}번 · {it.kind}{set ? <i className="mini-tag lesson">다정쌤 분석</i> : null}{attempt.checked?.includes(it.no) ? <i className="mini-tag">바로 확인</i> : null}{attempt.peeked?.includes(it.no) ? <i className="mini-tag peek">분석 보고 고름</i> : null}</b>
                    <small>
                      {mine ? `내 답 ${NUM[mine - 1]}` : "안 풂"} · 정답 {NUM[it.answer - 1]} · {it.points}점
                      {it.wrong_rate != null ? ` · 전국 오답률 ${it.wrong_rate}%` : ""}
                    </small>
                  </span>
                  <span className="mini-chev">{isOpen ? "▴" : "▾"}</span>
                </button>
                {isOpen ? (
                  <div className="mini-explain">
                    {set ? (
                      <button type="button" className="mini-analyze big" onClick={() => onAnalyze(set, it.no)}>
                        <b>다정쌤과 이 문제 분석하기 ›</b>
                        <small>문장마다 같이 읽으며 왜 답이 되는지 찾아요</small>
                      </button>
                    ) : (
                      <p className="mini-no-lesson">이 문제는 아직 다정쌤 분석이 없어요. 아래 해설을 봐요.</p>
                    )}
                    {it.fix ? <p className="mini-fix">{it.fix}</p> : null}
                    {it.intent ? <p className="mini-intent">{it.intent}</p> : null}
                    <details>
                      <summary>문제 다시 보기</summary>
                      <ItemView item={it} picked={mine} review />
                    </details>
                    <Translation item={it} recorder={recorder} />
                  </div>
                ) : null}
              </li>
            );
          })}
        </ul>
        <button type="button" className="mini-start" onClick={onRetry}>
          다시 풀기
        </button>
      </div>
    </div>
  );
}

function BackIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 6l-6 6 6 6" />
    </svg>
  );
}
