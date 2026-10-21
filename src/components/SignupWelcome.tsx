import { useState, type FormEvent } from "react";
import { loadLearnerName, parseName, saveLearnerName } from "../tutor/learner-name";
import { TeacherFigure } from "./TeacherFigure";
import { QuickReplies } from "./QuickReplies";
import { loadStudentState, saveStudentState } from "../tutor/policy/student-state";
import {
  buildPlan,
  defaultCourse,
  examTitleOfMock,
  examYearRange,
  levelOfGrade,
  savePlan,
  type CounselAnswers,
} from "../tutor/counsel";

/**
 * 온보딩 — 처음 가입했을 때 다정쌤이 앱을 소개하고, 코스를 짤 것만 묻는다 (2026-10-21 선생님이 짠 흐름).
 *
 * **다섯 번 누르면 첫 문제** (2026-10-21 선생님: 줄여 줘):
 * 이름(이미 있으면 건너뜀) → 소개 한 화면(Top 10 · 같이 분석하며 1등급 사고방식 · 필수 단어)
 * → 최근 등급 → 최근 기출부터/이전 기출부터 → 「좋아요! 다 됐어요」 → 코스 첫 시험의 오답률 1위 문제를 **바로 분석**
 * (풀기·시간 재기가 아니다). 5등급 이하는 묻지 않고 2점짜리부터.
 * 학년·기출 범위(평가원만/교육청까지)는 지금 코스에 영향이 없어 뺐다 — 쓸 곳이 생기면(평가원 기출이 들어오면) 다시 넣는다.
 * 상담실(목표·공부 시간 등)은 따로 있다.
 *
 * 선생님은 반말로 적어 줬지만 다정쌤은 해요체다 (CLAUDE.md). 한 화면에 세 문장까지, 물음표 하나, 이모지 하나.
 */

type Step = "name" | "intro" | "grade" | "order" | "done";

type Props = {
  learnerName: string | null;
  /** 코스를 저장한 뒤 — 코스 첫 시험의 오답률 1위 문제를 분석으로 연다 (App의 첫 방문 길) */
  onStartExample: () => void;
};

export function SignupWelcome({ learnerName, onStartExample }: Props) {
  // 이름을 먼저 묻는다 — 이미 알고 있으면(다른 곳에서 적었으면) 건너뛴다 (2026-10-21 선생님)
  const [step, setStep] = useState<Step>(() => (learnerName ?? loadLearnerName() ? "intro" : "name"));
  const [myName, setMyName] = useState<string | null>(() => learnerName ?? loadLearnerName());
  const [grade, setGrade] = useState<number | null>(null);
  const [order, setOrder] = useState<"recent" | "old">("recent");
  // 5등급 이하는 2점짜리부터 (묻지 않는다)
  const skipThree = grade != null && grade >= 5;

  function answers(): CounselAnswers {
    return {
      grade,
      goal: grade == null ? 3 : Math.max(1, grade - 1),
      exam: "다음 모의고사",
      weak: [],
      timeShort: false,
      minutes: 30,
      skipThree,
      order,
      scope: "all",
    };
  }

  function finish() {
    savePlan(buildPlan(answers()));
    // 수업 화면 단계도 같이 맞춘다 (상담실과 같다)
    saveStudentState({ ...loadStudentState(), level: levelOfGrade(grade), grade: grade ?? undefined });
    onStartExample();
  }

  const name = myName ? `${myName}님, ` : "";
  const years = examYearRange();
  const recentLabel = `최근 기출${years ? `(${years.newest})` : ""}부터`;
  const oldLabel = `이전 기출${years ? `(${years.oldest})` : ""}부터`;

  let line = "";
  let buttons: string[] = [];
  let onPick: (label: string) => void = () => {};

  switch (step) {
    case "name":
      line = "안녕하세요! 저는 영어 선생님 다정쌤이에요.\n이름을 알려 줄래요?";
      buttons = ["이름 없이 할게요"];
      onPick = () => setStep("intro");
      break;
    case "intro":
      // 소개 세 화면을 한 화면으로 — 줄마다 다른 이야기라 줄을 바꾼다
      line = `${name}수능 전에 꼭 필요한 기출 오답률 Top 10 문제들만 모았어요💛\n저랑 같이 분석하면서 1등급 사고방식을 똑같이 배울 수 있어요.\n풀었던 지문의 필수 단어도 수능 전까지 계속 볼 수 있게 도와줄게요.`;
      buttons = ["좋아요"];
      onPick = () => setStep("grade");
      break;
    case "grade":
      line = "최근 모의고사 영어는 몇 등급이었어요?";
      buttons = Array.from({ length: 9 }, (_, i) => `${i + 1}등급`);
      onPick = (b) => {
        setGrade(Number.parseInt(b, 10));
        setStep("order");
      };
      break;
    case "order":
      line = "어떤 기출부터 풀어 볼까요?";
      buttons = [recentLabel, oldLabel];
      onPick = (b) => {
        setOrder(b === oldLabel ? "old" : "recent");
        setStep("done");
      };
      break;
    case "done": {
      // 학생이 고른 순서로 짠 코스의 첫 시험 — 5등급 이하면 2점 문제 중에서
      const firstExam = examTitleOfMock(defaultCourse(answers())[0]);
      const which = `${firstExam ?? "첫 시험"}${skipThree ? " 2점 문제" : ""}`;
      const note = skipThree ? "\n처음엔 2점짜리부터 차근차근 풀어 볼게요." : "";
      line = `좋아요! 다 됐어요💛${note}\n아직 낯설 테니까, ${which} 중 오답률이 가장 높았던 문제부터 예시로 함께 봐요.`;
      buttons = ["같이 볼래요"];
      onPick = () => finish();
      break;
    }
  }

  return (
    <div className="stage-fill counsel welcome">
      {/* 상담실과 같은 방 — 캐릭터·말풍선은 따로 얹는다 */}
      <img className="counsel-bg" src="/assets/counsel-room.webp" alt="" width={1122} height={1402} draggable={false} />
      <header className="top-bar">
        <div className="chip">
          <span className="avatar">다</span>
          <div className="chip-text">
            <strong>다정쌤</strong>
            <small>처음 만났어요</small>
          </div>
        </div>
      </header>

      <div className="teacher-full">
        <div className="teacher-bob">
          <TeacherFigure />
        </div>
      </div>
      <img className="counsel-bg counsel-desk" src="/assets/counsel-desk.webp" alt="" width={1122} height={1402} draggable={false} />
      <div className="teacher-bubble" key={step}>
        <div className="bubble-card" aria-live="polite">
          <b className="bubble-name">다정쌤</b>
          <span>{line}</span>
        </div>
      </div>

      <div className="dock">
        {step === "name" ? (
          <NameInput
            onSubmit={(n) => {
              // 「민준이요」처럼 적어도 이름만 꺼낸다. 못 알아보면 이름 없이 간다 — 되묻지 않는다
              const parsed = parseName(n);
              if (parsed) saveLearnerName(parsed);
              setMyName(parsed);
              setStep("intro");
            }}
          />
        ) : null}
        <QuickReplies buttons={buttons} onPick={onPick} />
      </div>
    </div>
  );
}

function NameInput({ onSubmit }: { onSubmit: (name: string) => void }) {
  const [value, setValue] = useState("");
  const ok = value.trim().length > 0;
  const submit = (e: FormEvent) => {
    e.preventDefault();
    if (ok) onSubmit(value.trim());
  };
  return (
    <form className="counsel-score welcome-name" onSubmit={submit}>
      <input placeholder="이름" maxLength={10} value={value} autoFocus autoComplete="given-name" onChange={(e) => setValue(e.target.value)} />
      <button type="submit" className="pill" disabled={!ok}>
        확인
      </button>
    </form>
  );
}
