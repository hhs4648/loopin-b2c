import type { LessonSet } from "../../content/tutor/types";
import type { StudentLevel } from "./policy/student-state";
import type { Progress } from "./progress";

/**
 * 상담실 — 점수·목표·아쉬운 유형·공부 시간을 듣고 **학습 커리큘럼**을 짠다 (2026-10-19).
 *
 * 수업처럼 LLM을 부르지 않는다. 대사는 여기 미리 적어 두고, 계획은 규칙으로 만든다:
 *  1. 아쉬운 유형(학생이 고른 것 + 미니 모의고사에서 절반 넘게 틀린 것)부터
 *  2. 같은 유형 안에서는 등급에 맞춰 — 1~2등급은 어려운(오답률 높은) 것부터, 6등급~은 쉬운 것부터
 *  3. 나머지 유형은 오답률 높은 순으로 뒤에 붙인다
 *  4. 끝낸 문제는 맨 뒤 (다시 보기)
 * 하루 분량은 공부 시간으로 정한다 (15분 1문제 · 30분 2문제 · 1시간 3문제).
 */

/** 학생이 고르는 「아쉬운 유형」 — 세트 부제의 유형(「빈칸 — …」)으로 이어진다 */
export const WEAK_TYPES: { label: string; kinds: string[] }[] = [
  { label: "빈칸", kinds: ["빈칸"] },
  { label: "순서", kinds: ["순서"] },
  { label: "문장 넣기", kinds: ["문장 넣기"] },
  { label: "어휘·어법", kinds: ["어휘", "어법"] },
  { label: "밑줄 의미", kinds: ["밑줄 의미", "지칭"] },
  { label: "제목·주제·요지", kinds: ["제목", "주제", "요지", "요약문", "무관한 문장"] },
  { label: "듣기", kinds: ["듣기 응답"] },
];
export const TIME_SHORT = "시간이 모자라요";

export const EXAMS = ["다음 모의고사", "수능", "내신"] as const;
export type Exam = (typeof EXAMS)[number];

export const MINUTES = [15, 30, 60] as const;
export type Minutes = (typeof MINUTES)[number];

export type CounselAnswers = {
  /** 최근 모의고사 등급 1~9. 안 봤으면 null */
  grade: number | null;
  /** 점수로 입력했으면 그 점수 */
  score?: number;
  goal: number;
  exam: Exam;
  /** WEAK_TYPES의 label들 */
  weak: string[];
  timeShort: boolean;
  minutes: Minutes;
};

export type PlanDay = { day: number; sets: string[]; mini?: boolean };

export type CounselPlan = {
  version: 1;
  at: string;
  answers: CounselAnswers;
  /** 집중할 유형 (WEAK_TYPES label) — 학생이 고른 것 + 기록에서 찾은 것 */
  focus: string[];
  days: PlanDay[];
};

/** 영어 절대평가 — 90점 이상 1등급, 10점마다 한 등급 */
export function gradeOfScore(score: number): number {
  const s = Math.max(0, Math.min(100, Math.round(score)));
  return Math.min(9, Math.max(1, Math.floor((99 - s) / 10) + 1));
}

/** 수업 화면 단계 — 고 1~2 · 중 3~5 · 초 6~ (모르면 중) */
export function levelOfGrade(grade: number | null): StudentLevel {
  if (grade == null) return "중";
  if (grade <= 2) return "고";
  if (grade <= 5) return "중";
  return "초";
}

/** 세트 부제 맨 앞의 유형 — 「빈칸 — 지리학이 묻는 '어디'」 → 빈칸 */
export function kindOf(set: LessonSet): string {
  return set.subtitle.split(" — ")[0]!.trim();
}

export function weakLabelOfKind(kind: string): string | null {
  return WEAK_TYPES.find((w) => w.kinds.includes(kind))?.label ?? null;
}

/** 미니 모의고사에서 절반 넘게 틀린 유형 (WEAK_TYPES label) — 상담에서 「기록을 보니」로 먼저 짚는다 */
export function weakFromMini(rows: { kind: string; right: number; total: number }[]): string[] {
  const agg = new Map<string, { right: number; total: number }>();
  for (const r of rows) {
    const label = weakLabelOfKind(r.kind);
    if (!label) continue;
    const a = agg.get(label) ?? { right: 0, total: 0 };
    a.right += r.right;
    a.total += r.total;
    agg.set(label, a);
  }
  return WEAK_TYPES.map((w) => w.label).filter((l) => {
    const a = agg.get(l);
    return a != null && a.total > 0 && a.right / a.total < 0.5;
  });
}

const PER_DAY: Record<Minutes, number> = { 15: 1, 30: 2, 60: 3 };

export function buildPlan(
  answers: CounselAnswers,
  sets: LessonSet[],
  progress: Progress,
  fromRecords: string[] = [],
): CounselPlan {
  const focus = [...new Set([...answers.weak, ...fromRecords])];
  const focusKinds = new Set(focus.flatMap((l) => WEAK_TYPES.find((w) => w.label === l)?.kinds ?? []));
  const level = levelOfGrade(answers.grade);
  const rate = (s: LessonSet) => s.wrong_rate ?? 50;
  // 같은 유형 안에서 — 상위권은 어려운 것부터, 하위권은 쉬운 것부터
  const within = (a: LessonSet, b: LessonSet) => (level === "초" ? rate(a) - rate(b) : rate(b) - rate(a));

  // 비교용 사본(-v1 등 「줄이기 전」)은 계획에 넣지 않는다
  const usable = sets.filter((s) => !/-v\d+$/.test(s.id));
  const todo = usable.filter((s) => !(s.id in progress));
  const done = usable.filter((s) => s.id in progress);

  // 집중 유형은 번갈아 — 빈칸만 사흘 내리 하지 않게 유형마다 한 줄씩 돌려 담는다
  const queues = focus
    .map((label) => {
      const kinds = WEAK_TYPES.find((w) => w.label === label)?.kinds ?? [];
      return todo.filter((s) => kinds.includes(kindOf(s))).sort(within);
    })
    .filter((q) => q.length > 0);
  const focused: LessonSet[] = [];
  while (queues.some((q) => q.length > 0)) {
    for (const q of queues) {
      const next = q.shift();
      if (next) focused.push(next);
    }
  }
  const rest = todo
    .filter((s) => !focusKinds.has(kindOf(s)))
    // 듣기는 독해 수업 뒤로 — 고르지 않았으면 맨 끝
    .sort((a, b) => Number(kindOf(a) === "듣기 응답") - Number(kindOf(b) === "듣기 응답") || rate(b) - rate(a));
  const order = [...focused, ...rest, ...done].map((s) => s.id);

  const per = PER_DAY[answers.minutes];
  const days: PlanDay[] = [];
  // 7일치만 — 일주일 뒤에 다시 상담하러 오게
  for (let d = 0; d < 7 && d * per < order.length; d++) {
    days.push({ day: d + 1, sets: order.slice(d * per, d * per + per) });
  }
  // 시간이 모자란 학생은 마지막 날에 미니 모의고사로 시간 재기
  if (answers.timeShort && days.length > 0) days[days.length - 1] = { ...days[days.length - 1]!, mini: true };

  return { version: 1, at: new Date().toISOString(), answers, focus, days };
}

/** 오늘 할 것 — 아직 안 끝낸 문제가 남은 첫날 */
export function todayOf(plan: CounselPlan, progress: Progress): PlanDay | null {
  return plan.days.find((d) => d.sets.some((id) => !(id in progress))) ?? null;
}

/** 계획에서 다음으로 풀 문제 */
export function nextSetOf(plan: CounselPlan, progress: Progress): string | null {
  for (const d of plan.days) for (const id of d.sets) if (!(id in progress)) return id;
  return null;
}

export function planProgress(plan: CounselPlan, progress: Progress): { done: number; total: number } {
  const all = plan.days.flatMap((d) => d.sets);
  return { done: all.filter((id) => id in progress).length, total: all.length };
}

const KEY = "loopin.counsel.v1";

export function loadPlan(): CounselPlan | null {
  try {
    const raw = window.localStorage.getItem(KEY);
    const parsed = raw ? (JSON.parse(raw) as CounselPlan) : null;
    return parsed && parsed.version === 1 && Array.isArray(parsed.days) ? parsed : null;
  } catch {
    return null;
  }
}

export function savePlan(plan: CounselPlan): void {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(plan));
  } catch {
    /* 저장 못 해도 이번 화면에는 보인다 */
  }
}
