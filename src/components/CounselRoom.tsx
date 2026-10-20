import { useState, type FormEvent } from "react";
import { ClassroomBg } from "./ClassroomBg";
import { TeacherFigure } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { allMiniMocks, byKind, clock, loadAttempts } from "../tutor/mini";
import { loadStudentState, saveStudentState } from "../tutor/policy/student-state";
import {
  EXAMS,
  MINUTES,
  TIME_SHORT,
  WEAK_TYPES,
  MOCKS_PER_DAY,
  VOCAB_PREFIX,
  buildPlan,
  courseProgress,
  courseStatus,
  gradeOfScore,
  levelOfGrade,
  loadPlan,
  nextMockOf,
  savePlan,
  weakFromMini,
  type CounselAnswers,
  type CounselPlan,
  type CourseItem,
  type Exam,
  type Minutes,
} from "../tutor/counsel";

/**
 * 상담실 — 다정쌤과 이야기하며 커리큘럼을 짠다 (규칙은 `src/tutor/counsel.ts`).
 *
 * 수업 화면처럼 선생님 + 말풍선 + 버튼으로 묻고, 다 들으면 10분 모의고사 코스를 보여 준다.
 * 화면마다 선생님 말은 세 문장까지, 물음표는 하나.
 */

type Step = "resume" | "intro" | "grade" | "score" | "goal" | "three" | "exam" | "weak" | "time" | "confirm" | "plan";

type Props = {
  learnerName: string | null;
  onClose: () => void;
  /** 코스의 10분 모의고사 하나를 연다 — stage로 단어 학습(words)·분석 목록(prep)부터 열 수 있다 */
  onOpenMini: (mockId: string, stage?: MiniStage) => void;
  /** 진도표 — 시험마다 본 문제·안 본 문제, 자주 틀리는 유형 */
  onOpenBoard: () => void;
  /** 틀린 문제 모아보기 */
  onOpenWrong: () => void;
};

export type MiniStage = "words" | "prep" | "review";

const MINUTE_LABEL: Record<Minutes, string> = { 15: "15분", 30: "30분", 60: "1시간 이상" };

/** 미니 모의고사 최근 기록에서 아쉬운 유형 */
function weakFromRecords(): string[] {
  const mock = allMiniMocks()[0];
  const last = mock ? loadAttempts(mock.id)[0] : undefined;
  return mock && last ? weakFromMini(byKind(mock, last.answers)) : [];
}

export function CounselRoom({ learnerName, onClose, onOpenMini, onOpenBoard, onOpenWrong }: Props) {
  const [plan, setPlan] = useState<CounselPlan | null>(() => loadPlan());
  // 코스가 있으면 바로 코스 화면 — 「이어서 볼까요?」를 올 때마다 묻지 않는다
  const [step, setStep] = useState<Step>(() => (loadPlan() ? "plan" : "intro"));
  const records = useState(() => weakFromRecords())[0];

  const [grade, setGrade] = useState<number | null>(null);
  const [score, setScore] = useState<number | undefined>(undefined);
  const [goal, setGoal] = useState(2);
  const [exam, setExam] = useState<Exam>("다음 모의고사");
  const [weak, setWeak] = useState<string[]>(records);
  const [timeShort, setTimeShort] = useState(false);
  const [minutes, setMinutes] = useState<Minutes>(30);
  const [skipThree, setSkipThree] = useState(false);

  // 학생이 고른 답을 오른쪽 말풍선으로 되보여 주던 것은 뺐다 — 버튼처럼 보여서 오류로 보인다 (2026-10-20 선생님)
  const go = (next: Step, _studentLine: string | null = null) => {
    setStep(next);
  };

  function restart() {
    setGrade(null);
    setScore(undefined);
    setWeak(records);
    setTimeShort(false);
    go("grade", "다시 상담할래요");
  }

  function finish() {
    const answers: CounselAnswers = { grade, score, goal, exam, weak, timeShort, minutes, skipThree };
    const next = buildPlan(answers, records);
    savePlan(next);
    // 수업 화면 단계도 같이 맞춘다 (목록의 「내 등급」과 같은 값)
    saveStudentState({ ...loadStudentState(), level: levelOfGrade(grade) });
    setPlan(next);
    go("plan");
  }

  if (step === "plan" && plan) {
    return <CourseView plan={plan} onClose={onClose} onRestart={restart} onOpenMini={onOpenMini} onOpenBoard={onOpenBoard} onOpenWrong={onOpenWrong} />;
  }

  const name = learnerName ? `${learnerName}님, ` : "";
  const goalChoices = grade == null ? [1, 2, 3, 4, 5] : grade === 1 ? [1] : Array.from({ length: grade - 1 }, (_, i) => i + 1);
  const recordLabel = records.join("·");
  const weakSummary = weak.length > 0 ? `${weak.join("·")}부터 같이 잡아 봐요!` : "";

  let line = "";
  let buttons: string[] = [];
  let onPick: (label: string) => void = () => {};

  switch (step) {
    case "resume": {
      line = "어서 와요! 지난번에 같이 짠 계획이 있는데, 이어서 볼까요?";
      buttons = ["계획 볼게요", "다시 상담할래요"];
      onPick = (b) => (b === "계획 볼게요" ? go("plan") : restart());
      break;
    }
    case "intro": {
      line = `${name}어서 와요! 오늘은 어떤 이야기를 해 볼까요?\n지금 실력이랑 목표를 들려주면, 공부 순서를 같이 짜 볼게요.`;
      buttons = ["좋아요"];
      onPick = (b) => go("grade", b);
      break;
    }
    case "grade": {
      line = "먼저 궁금한 게 있어요. 최근 모의고사 영어는 몇 등급이었어요?";
      buttons = [...Array.from({ length: 9 }, (_, i) => `${i + 1}등급`), "점수로 적을게요", "아직 안 봤어요"];
      onPick = (b) => {
        if (b === "점수로 적을게요") return go("score", b);
        if (b === "아직 안 봤어요") {
          setGrade(null);
          setGoal(3);
          return go("goal", b);
        }
        const g = Number.parseInt(b, 10);
        setGrade(g);
        setGoal(Math.max(1, g - 1));
        go("goal", b);
      };
      break;
    }
    case "score": {
      line = "점수를 적어 줄래요? 등급은 제가 계산해 줄게요.";
      break;
    }
    case "goal": {
      line =
        score != null && grade != null
          ? `${score}점이면 ${grade}등급이에요. 좋아요, 그럼 목표는 몇 등급이에요?`
          : grade === 1
            ? "와, 벌써 1등급이네요! 그럼 1등급을 끝까지 지키는 게 우리 목표예요."
            : "좋아요! 그럼 목표는 몇 등급이에요?";
      buttons = grade === 1 ? ["1등급 지키기"] : goalChoices.map((g) => `${g}등급`);
      onPick = (b) => {
        setGoal(grade === 1 ? 1 : Number.parseInt(b, 10));
        // 5등급부터는 3점을 버리고 2점부터 다지는 학생이 많다 — 물어본다
        go(grade == null || grade >= 5 ? "three" : "exam", b);
      };
      break;
    }
    case "three": {
      line = "3점짜리는 어려워서 일단 빼고 2점부터 다지는 친구도 많아요. 3점 문제도 같이 풀까요?";
      buttons = ["3점도 풀래요", "2점부터 할래요"];
      onPick = (b) => {
        setSkipThree(b === "2점부터 할래요");
        go("exam", b);
      };
      break;
    }
    case "exam": {
      line = "응원할게요! 가장 먼저 볼 시험은 뭐예요?";
      buttons = [...EXAMS];
      onPick = (b) => {
        setExam(b as Exam);
        // 「아쉬운 유형」은 묻지 않는다 — 틀리는 이유가 다 비슷하다 (2026-10-20 선생님). 미니 모의고사 기록에서 찾은 것만 쓴다
        go("time", b);
      };
      break;
    }
    case "weak": {
      line = records.length
        ? `기록을 보니 미니 모의고사에서 ${recordLabel} 문제를 절반 넘게 놓쳤더라고요. 그 밖에 요즘 아쉬웠던 것도 편하게 다 골라 줘요.`
        : "요즘 시험에서 아쉬웠던 걸 편하게 다 골라 줘요. 여러 개여도 괜찮아요!";
      break;
    }
    case "time": {
      line = "거의 다 왔어요! 하루에 영어 공부는 얼마나 할 수 있어요?";
      buttons = MINUTES.map((m) => MINUTE_LABEL[m]);
      onPick = (b) => {
        setMinutes(MINUTES.find((m) => MINUTE_LABEL[m] === b) ?? 30);
        // 「최근 모의고사부터 / 수능부터」는 묻지 않는다 — 모의고사·수능을 합쳐 최근 것부터 (2026-10-20 선생님)
        go("confirm", b);
      };
      break;
    }
    case "confirm": {
      const now = grade == null ? "아직 등급은 없고" : `지금 ${grade}등급에서`;
      line = `정리해 볼게요! ${now} ${goal}등급이 목표예요. ${weakSummary}
최근 시험부터 ${skipThree ? "2점 문제 중 " : ""}어려운 5문제씩 하루 ${MOCKS_PER_DAY[minutes]}회, 회차마다 틀린 문제 복습으로 코스를 짤게요.`;
      buttons = ["좋아요, 코스 짜 주세요", "처음부터 다시"];
      onPick = (b) => (b === "처음부터 다시" ? restart() : finish());
      break;
    }
    case "plan":
      break;
  }

  return (
    <div className="stage-fill counsel">
      {/* 상담실 배경 — 캐릭터(`TeacherFigure`)·말풍선은 따로 얹는다. 배경에는 글자를 넣지 않는다 */}
      <img className="counsel-bg" src="/assets/counsel-room.webp" alt="" width={1122} height={1402} draggable={false} />
      <header className="top-bar">
        <div className="chip">
          <span className="avatar">다</span>
          <div className="chip-text">
            <strong>다정쌤</strong>
            <small>상담실</small>
          </div>
        </div>
        <button type="button" className="close-soft" title="홈으로" aria-label="홈으로" onClick={onClose}>
          <CloseIcon />
        </button>
      </header>

      <div className="teacher-full">
        <div className="teacher-bob">
          <TeacherFigure />
        </div>
      </div>
      {/* 책상 앞부분(같은 그림의 아랫부분만, 위는 투명)을 선생님 위에 얹어 선생님이 책상 뒤에 서 있게 */}
      <img className="counsel-bg counsel-desk" src="/assets/counsel-desk.webp" alt="" width={1122} height={1402} draggable={false} />
      {/* 말풍선은 책상 앞, 화면 폭 가득 — 이름표가 왼쪽 위에 걸린다 (시안) */}
      <div className="teacher-bubble" key={step}>
        <div className="bubble-card" aria-live="polite">
          <b className="bubble-name">다정쌤</b>
          <span>{line}</span>
        </div>
      </div>

      <div className="dock">
        {step === "score" ? (
          <ScoreInput
            onSubmit={(n) => {
              const g = gradeOfScore(n);
              setScore(n);
              setGrade(g);
              setGoal(Math.max(1, g - 1));
              go("goal", `${n}점`);
            }}
          />
        ) : step === "weak" ? (
          <div className="quick-row counsel-multi">
            {[...WEAK_TYPES.map((w) => w.label), TIME_SHORT].map((label) => {
              const on = label === TIME_SHORT ? timeShort : weak.includes(label);
              return (
                <button
                  key={label}
                  type="button"
                  className={`pill${on ? " on" : ""}`}
                  aria-pressed={on}
                  onClick={() =>
                    label === TIME_SHORT
                      ? setTimeShort(!timeShort)
                      : setWeak(on ? weak.filter((w) => w !== label) : [...weak, label])
                  }
                >
                  {on ? "✓ " : ""}
                  {label}
                </button>
              );
            })}
            <button
              type="button"
              className="pill counsel-done"
              onClick={() => {
                const picked = [...weak, ...(timeShort ? [TIME_SHORT] : [])];
                go("time", picked.length ? picked.join(" · ") : "잘 모르겠어요");
              }}
            >
              {weak.length || timeShort ? "다 골랐어요" : "잘 모르겠어요"}
            </button>
          </div>
        ) : (
          <QuickReplies buttons={buttons} onPick={onPick} />
        )}
      </div>
    </div>
  );
}

function ScoreInput({ onSubmit }: { onSubmit: (score: number) => void }) {
  const [value, setValue] = useState("");
  const n = Number.parseInt(value, 10);
  const ok = value !== "" && Number.isFinite(n) && n >= 0 && n <= 100;
  const submit = (e: FormEvent) => {
    e.preventDefault();
    if (ok) onSubmit(n);
  };
  return (
    <form className="counsel-score" onSubmit={submit}>
      <input
        inputMode="numeric"
        pattern="[0-9]*"
        maxLength={3}
        placeholder="0 ~ 100"
        value={value}
        autoFocus
        onChange={(e) => setValue(e.target.value.replace(/\D/g, ""))}
      />
      <span>점</span>
      <button type="submit" className="pill" disabled={!ok}>
        확인
      </button>
    </form>
  );
}

/* ── 계획 ───────────────────────────────────────────────────────── */

function CourseView({
  plan,
  onClose,
  onRestart,
  onOpenMini,
  onOpenBoard,
  onOpenWrong,
}: {
  plan: CounselPlan;
  onClose: () => void;
  onRestart: () => void;
  onOpenMini: (mockId: string, stage?: MiniStage) => void;
  onOpenBoard: () => void;
  onOpenWrong: () => void;
}) {
  const items = courseStatus(plan);
  const { done, total } = courseProgress(plan);
  const next = nextMockOf(plan);
  const a = plan.answers;

  /*
    쭉 나열하면 보기 힘들다 (2026-10-20 선생님) — 연도 구분줄 → 「시험 오답률 Top 10 풀기」 → 회차 (1)(2) → 1 단어 학습 · 2 실전 풀기 · 3 분석.
    복습 칸은 코스 순서 그 자리에 그대로 둔다.
  */
  type Block = { kind: "year"; year: number } | { kind: "exam"; title: string; mocks: CourseItem[] } | { kind: "review"; item: CourseItem };
  const blocks: Block[] = [];
  let year = 0;
  let examId = "";
  for (const it of items) {
    if (it.review) {
      blocks.push({ kind: "review", item: it });
      continue;
    }
    if (!it.exam) continue;
    if (it.exam.year !== year) {
      year = it.exam.year;
      examId = "";
      blocks.push({ kind: "year", year });
    }
    if (it.exam.collectionId !== examId) {
      examId = it.exam.collectionId;
      blocks.push({ kind: "exam", title: it.exam.title, mocks: [] });
    }
    const last = blocks[blocks.length - 1];
    if (last?.kind === "exam") last.mocks.push(it);
  }
  let seq = 0;

  return (
    <div className="stage-fill home counsel-plan">
      <ClassroomBg />
      <header className="top-bar">
        <button type="button" className="icon-btn light" title="홈으로" onClick={onClose}>
          <BackIcon />
        </button>
        <span className="plan-head-btns">
          <button type="button" className="plan-redo" onClick={onOpenBoard}>진도표</button>
          <button type="button" className="plan-redo" onClick={onOpenWrong}>틀린 문제</button>
        </span>
      </header>

      <div className="home-body">
        <p className="home-hello">다정쌤이 짠 코스</p>
        <h1 className="home-title">10분 모의고사 코스</h1>

        <div className="plan-summary">
          <div className="plan-goal">
            <span>
              <small>지금</small>
              <b>{a.grade == null ? "—" : `${a.grade}등급`}</b>
            </span>
            <i>→</i>
            <span className="to">
              <small>목표</small>
              <b>{a.goal}등급</b>
            </span>
          </div>
          <div className="plan-tags">
            <span>{a.exam}</span>
            <span>하루 {MOCKS_PER_DAY[a.minutes]}회 · {MINUTE_LABEL[a.minutes]}</span>
            {a.suneungFirst ? <span>수능 먼저</span> : null}
            {a.skipThree ? <span>2점부터</span> : null}
          </div>
          <div className="plan-bar" aria-label={`${total}회 중 ${done}회 풀었어요`}>
            <i style={{ width: `${total ? (done / total) * 100 : 0}%` }} />
          </div>
          <small className="plan-count">
            어려운 5문제씩 10분 · 회차마다 틀린 문제 복습 — {total}회 중 {done}회 풀었어요
          </small>
        </div>

        <div className="course">
          {blocks.map((bl, k) => {
            if (bl.kind === "year") return <div key={`y${bl.year}`} className="course-year"><span>{bl.year}년</span></div>;
            if (bl.kind === "review") {
              const it = bl.item;
              const isNext = it.id === next;
              return (
                <div key={it.id} className={`course-exam review${isNext ? " today" : ""}`}>
                  <button type="button" className="course-mock-head" onClick={() => onOpenMini(it.id)}>
                    <b>↻ {it.title}{isNext ? <span className="plan-today">오늘</span> : null}</b>
                    <small>{it.done ? "복습했어요" : it.subtitle}</small>
                  </button>
                </div>
              );
            }
            return (
              <section key={`${bl.title}${k}`} className="course-exam">
                <h3 className="course-exam-title">
                  {bl.title} 오답률 Top 10 풀기
                  <small>{bl.mocks.filter((m) => m.done).length}/{bl.mocks.length}회</small>
                </h3>
                {bl.mocks.map((m) => {
                  seq++;
                  const isNext = m.id === next;
                  const part = /-(\d)(?:\s|$)/.exec(m.title)?.[1] ?? seq;
                  const analysisDone = !!m.analysis && m.analysis.done >= m.analysis.total && m.done;
                  return (
                    <div key={m.id} className={`course-mock${isNext ? " today" : ""}${m.done ? " done" : ""}`}>
                      <div className="course-mock-head">
                        <b>
                          ({part}) {m.subtitle.split(" · ")[0]} · 10분 모의고사
                          {isNext ? <span className="plan-today">오늘</span> : null}
                        </b>
                        {m.done && m.score ? (
                          <small>{m.score.correct}/{m.score.total} 맞힘 · 예상 약 {m.estimate}점 · {clock(m.seconds ?? 0)}</small>
                        ) : null}
                      </div>
                      <ol className="course-steps four">
                        <li className={m.done ? "fin" : ""}>
                          <button type="button" onClick={() => onOpenMini(m.id)}>
                            <i>{m.done ? "✓" : "1"}</i>
                            <span>실전 풀기<small>{m.done ? "풀기 완료" : "풀기 전에 주요 단어를 한 번 봐요"}</small></span>
                          </button>
                        </li>
                        <li className={analysisDone ? "fin" : ""}>
                          <button type="button" onClick={() => onOpenMini(m.id, "prep")}>
                            <i>{analysisDone ? "✓" : "2"}</i>
                            <span>
                              분석
                              <small>
                                {!m.done
                                  ? "풀고 나서 틀린 문제를"
                                  : analysisDone
                                    ? "분석 완료"
                                    : `틀린 ${m.analysis!.total}문제 중 ${m.analysis!.done}개 분석`}
                              </small>
                            </span>
                          </button>
                        </li>
                        <li className={m.words ? "fin" : ""}>
                          <button type="button" onClick={() => onOpenMini(`${VOCAB_PREFIX}${m.id}`)}>
                            <i>{m.words ? "✓" : "3"}</i>
                            <span>단어 연습<small>{m.words ? "연습 완료" : "별표·모르는 단어 테스트"}</small></span>
                          </button>
                        </li>
                        <li className={m.done && m.review4 && m.review4.done >= m.review4.total ? "fin" : ""}>
                          <button type="button" onClick={() => onOpenMini(m.id, "review")}>
                            <i>{m.done && m.review4 && m.review4.done >= m.review4.total ? "✓" : "4"}</i>
                            <span>
                              틀린 문제 복습
                              <small>
                                {!m.done
                                  ? "풀고 나서"
                                  : m.review4!.total === 0
                                    ? "틀린 문제 없음"
                                    : m.review4!.done >= m.review4!.total
                                      ? "복습 완료"
                                      : `${m.review4!.total}문제 중 ${m.review4!.done}개`}
                              </small>
                            </span>
                          </button>
                        </li>
                      </ol>
                      {m.done && m.marks ? (
                        <ul className="course-marks" aria-label="문항별 결과">
                          {m.marks.map((x) => (
                            <li key={x.no} className={x.result}>
                              <b>{x.no}</b>
                              <span>{x.result === "right" ? "○" : x.result === "wrong" ? "✕" : "—"}</span>
                              {x.peeked ? <em>분석 보고</em> : x.checked ? <em>정답 확인</em> : null}
                              {x.analyzed ? <em className="an">분석 ✓</em> : null}
                            </li>
                          ))}
                        </ul>
                      ) : null}
                    </div>
                  );
                })}
              </section>
            );
          })}
        </div>
        <p className="plan-note">
          {next
            ? "한 회는 실전 풀기 → 분석 → 단어 연습 → 틀린 문제 복습이에요. 실전은 풀기 전에 주요 단어를 한 번 보여 줘요!"
            : "지금까지 전부 맞혔어요! 새 시험이 들어오면 코스에 붙여 둘게요."}
        </p>
        {/* 다시 상담은 맨 아래 — 자주 누르는 버튼이 아니다 (2026-10-20 선생님) */}
        <button type="button" className="plan-redo plan-redo-bottom" onClick={onRestart}>
          다시 상담하기
        </button>
      </div>

      {next ? (
        <div className="village-dock">
          <button type="button" className="village-cta" onClick={() => onOpenMini(next)}>
            <span>바로 시작하기</span>
            <i className="village-cta-go">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 6l6 6-6 6" />
              </svg>
            </i>
          </button>
        </div>
      ) : null}
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

function BackIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 6l-6 6 6 6" />
    </svg>
  );
}
