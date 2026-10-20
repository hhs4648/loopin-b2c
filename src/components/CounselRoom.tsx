import { useState, type FormEvent } from "react";
import { ClassroomBg } from "./ClassroomBg";
import { TeacherFigure } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { allSets, getCollection, getSet } from "../tutor/sets";
import { loadProgress } from "../tutor/progress";
import { allMiniMocks, byKind, loadAttempts } from "../tutor/mini";
import { loadStudentState, saveStudentState } from "../tutor/policy/student-state";
import {
  EXAMS,
  MINUTES,
  TIME_SHORT,
  WEAK_TYPES,
  buildPlan,
  gradeOfScore,
  levelOfGrade,
  loadPlan,
  planProgress,
  savePlan,
  todayOf,
  weakFromMini,
  type CounselAnswers,
  type CounselPlan,
  type Exam,
  type Minutes,
} from "../tutor/counsel";

/**
 * 상담실 — 다정쌤과 이야기하며 커리큘럼을 짠다 (규칙은 `src/tutor/counsel.ts`).
 *
 * 수업 화면처럼 선생님 + 말풍선 + 버튼으로 묻고, 다 들으면 일주일 계획을 보여 준다.
 * 화면마다 선생님 말은 세 문장까지, 물음표는 하나.
 */

type Step = "resume" | "intro" | "grade" | "score" | "goal" | "exam" | "weak" | "time" | "confirm" | "plan";

type Props = {
  learnerName: string | null;
  onClose: () => void;
  /** 계획의 문제 하나를 바로 시작 */
  onStartSet: (setId: string) => void;
  /** 미니 모의고사 (시간이 모자란 학생의 마지막 날) */
  onOpenMini: () => void;
};

const MINUTE_LABEL: Record<Minutes, string> = { 15: "15분", 30: "30분", 60: "1시간 이상" };

/** 미니 모의고사 최근 기록에서 아쉬운 유형 */
function weakFromRecords(): string[] {
  const mock = allMiniMocks()[0];
  const last = mock ? loadAttempts(mock.id)[0] : undefined;
  return mock && last ? weakFromMini(byKind(mock, last.answers)) : [];
}

export function CounselRoom({ learnerName, onClose, onStartSet, onOpenMini }: Props) {
  const [plan, setPlan] = useState<CounselPlan | null>(() => loadPlan());
  const [step, setStep] = useState<Step>(() => (loadPlan() ? "resume" : "intro"));
  const records = useState(() => weakFromRecords())[0];

  const [grade, setGrade] = useState<number | null>(null);
  const [score, setScore] = useState<number | undefined>(undefined);
  const [goal, setGoal] = useState(2);
  const [exam, setExam] = useState<Exam>("다음 모의고사");
  const [weak, setWeak] = useState<string[]>(records);
  const [timeShort, setTimeShort] = useState(false);
  const [minutes, setMinutes] = useState<Minutes>(30);

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
    const answers: CounselAnswers = { grade, score, goal, exam, weak, timeShort, minutes };
    const next = buildPlan(answers, allSets(), loadProgress(), records);
    savePlan(next);
    // 수업 화면 단계도 같이 맞춘다 (목록의 「내 등급」과 같은 값)
    saveStudentState({ ...loadStudentState(), level: levelOfGrade(grade) });
    setPlan(next);
    go("plan");
  }

  if (step === "plan" && plan) {
    return <PlanView plan={plan} onClose={onClose} onRestart={restart} onStartSet={onStartSet} onOpenMini={onOpenMini} />;
  }

  const name = learnerName ? `${learnerName}님, ` : "";
  const goalChoices = grade == null ? [1, 2, 3, 4, 5] : grade === 1 ? [1] : Array.from({ length: grade - 1 }, (_, i) => i + 1);
  const recordLabel = records.join("·");
  const weakSummary = weak.length > 0 ? `${weak.join("·")}부터 잡을 거예요.` : "기본 독해부터 고르게 잡을 거예요.";

  let line = "";
  let buttons: string[] = [];
  let onPick: (label: string) => void = () => {};

  switch (step) {
    case "resume": {
      line = "지난번에 같이 짠 계획이 있어요. 이어서 볼까요?";
      buttons = ["계획 볼게요", "다시 상담할래요"];
      onPick = (b) => (b === "계획 볼게요" ? go("plan") : restart());
      break;
    }
    case "intro": {
      line = `${name}상담실에 잘 왔어요. 지금 실력과 목표를 듣고, 공부 순서를 같이 짜 볼게요.`;
      buttons = ["좋아요"];
      onPick = (b) => go("grade", b);
      break;
    }
    case "grade": {
      line = "최근 모의고사 영어는 몇 등급이었어요?";
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
      line = "점수를 적어 주세요. 등급은 제가 계산할게요.";
      break;
    }
    case "goal": {
      line =
        score != null && grade != null
          ? `${score}점이면 ${grade}등급이에요. 목표는 몇 등급이에요?`
          : grade === 1
            ? "벌써 1등급이네요. 그럼 1등급을 놓치지 않는 게 목표예요."
            : "목표는 몇 등급이에요?";
      buttons = grade === 1 ? ["1등급 지키기"] : goalChoices.map((g) => `${g}등급`);
      onPick = (b) => {
        setGoal(grade === 1 ? 1 : Number.parseInt(b, 10));
        go("exam", b);
      };
      break;
    }
    case "exam": {
      line = "가장 먼저 볼 시험은 뭐예요?";
      buttons = [...EXAMS];
      onPick = (b) => {
        setExam(b as Exam);
        go("weak", b);
      };
      break;
    }
    case "weak": {
      line = records.length
        ? `미니 모의고사에서 ${recordLabel} 문제를 절반 넘게 놓쳤어요. 그 밖에 요즘 아쉬웠던 것도 모두 골라 주세요.`
        : "요즘 시험에서 아쉬웠던 것을 모두 골라 주세요. 여러 개 골라도 돼요.";
      break;
    }
    case "time": {
      line = "하루에 영어 공부는 얼마나 할 수 있어요?";
      buttons = MINUTES.map((m) => MINUTE_LABEL[m]);
      onPick = (b) => {
        setMinutes(MINUTES.find((m) => MINUTE_LABEL[m] === b) ?? 30);
        go("confirm", b);
      };
      break;
    }
    case "confirm": {
      const now = grade == null ? "아직 등급은 없고" : `지금 ${grade}등급에서`;
      line = `정리해 볼게요. ${now} ${goal}등급이 목표예요. ${weakSummary}`;
      buttons = ["좋아요, 계획 짜 주세요", "처음부터 다시"];
      onPick = (b) => (b === "처음부터 다시" ? restart() : finish());
      break;
    }
    case "plan":
      break;
  }

  return (
    <div className="stage-fill counsel">
      <ClassroomBg />
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
      <div className="teacher-bubble" key={step}>
        <div className="bubble-card" aria-live="polite">
          <span>{line}</span>
          <i className="bubble-tail" />
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

function PlanView({
  plan,
  onClose,
  onRestart,
  onStartSet,
  onOpenMini,
}: {
  plan: CounselPlan;
  onClose: () => void;
  onRestart: () => void;
  onStartSet: (setId: string) => void;
  onOpenMini: () => void;
}) {
  const progress = loadProgress();
  const today = todayOf(plan, progress);
  const { done, total } = planProgress(plan, progress);
  const a = plan.answers;
  const next = today?.sets.find((id) => !(id in progress)) ?? null;

  return (
    <div className="stage-fill home counsel-plan">
      <ClassroomBg />
      <header className="top-bar">
        <button type="button" className="icon-btn light" title="홈으로" onClick={onClose}>
          <BackIcon />
        </button>
        <button type="button" className="plan-redo" onClick={onRestart}>
          다시 상담하기
        </button>
      </header>

      <div className="home-body">
        <p className="home-hello">다정쌤이 짠 일주일 계획</p>
        <h1 className="home-title">내 커리큘럼</h1>

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
            <span>하루 {MINUTE_LABEL[a.minutes]}</span>
            {plan.focus.map((f) => (
              <span key={f} className="focus">
                {f}
              </span>
            ))}
            {a.timeShort ? <span className="focus">시간 재기</span> : null}
          </div>
          <div className="plan-bar" aria-label={`${total}문제 중 ${done}개 끝냄`}>
            <i style={{ width: `${total ? (done / total) * 100 : 0}%` }} />
          </div>
          <small className="plan-count">
            {total}문제 중 {done}개 끝냈어요
          </small>
        </div>

        <ol className="plan-days">
          {plan.days.map((d) => {
            const isToday = today?.day === d.day;
            const allDone = d.sets.every((id) => id in progress);
            return (
              <li key={d.day} className={`plan-day${isToday ? " today" : ""}${allDone ? " done" : ""}`}>
                <div className="plan-day-head">
                  <b>{d.day}일차</b>
                  {isToday ? <span className="plan-today">오늘</span> : allDone ? <span className="done-mark">완료</span> : null}
                </div>
                <ul>
                  {d.sets.map((id) => {
                    const set = getSet(id);
                    if (!set) return null;
                    const fin = id in progress;
                    return (
                      <li key={id}>
                        <button type="button" className={`plan-item${fin ? " fin" : ""}`} onClick={() => onStartSet(id)}>
                          <span className="plan-check">{fin ? "✓" : ""}</span>
                          <span className="plan-item-text">
                            <strong>
                              {set.title}
                              <em>{getCollection(set.collection)?.title}</em>
                            </strong>
                            <small>{set.subtitle}</small>
                          </span>
                        </button>
                      </li>
                    );
                  })}
                  {d.mini ? (
                    <li>
                      <button type="button" className="plan-item mini" onClick={onOpenMini}>
                        <span className="plan-check">⏱</span>
                        <span className="plan-item-text">
                          <strong>미니 모의고사</strong>
                          <small>시간 재며 풀어 보기</small>
                        </span>
                      </button>
                    </li>
                  ) : null}
                </ul>
              </li>
            );
          })}
        </ol>
        <p className="plan-note">일주일 계획을 다 끝내면 다시 상담하러 와요.</p>
      </div>

      {next ? (
        <div className="village-dock">
          <button type="button" className="village-cta" onClick={() => onStartSet(next)}>
            <span>오늘 공부 시작하기</span>
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
