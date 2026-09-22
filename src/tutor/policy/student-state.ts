import type { PerformanceStatus } from "./types";

/**
 * 학생 상태 (명세 §4).
 *
 * **아는 것(knowledge)과 실수(mistake)를 따로 센다.** 개념은 아는데 같은 자리에서
 * 자꾸 틀리는 학생에게 필요한 건 재설명이 아니라 스스로 고칠 기회다.
 *
 * 여기 담는 건 **관찰에서 곧바로 셀 수 있는 것**뿐이다. 「헷갈려한다」「집중을
 * 안 한다」 같은 속마음은 저장하지 않는다 (§7).
 */

export type KnowledgeStatus = "stable" | "uncertain" | "weak" | "unknown";

export type SkillRecord = {
  status: KnowledgeStatus;
  independent: number;
  hintAssisted: number;
  failure: number;
  /** 틀린 선택 횟수. 결국 맞혔어도 센다 */
  mistakes: number;
};

export type StudentState = {
  version: 1;
  skills: Record<string, SkillRecord>;
};

export function emptyStudentState(): StudentState {
  return { version: 1, skills: {} };
}

export function skillOf(state: StudentState, skill: string): SkillRecord {
  return (
    state.skills[skill] ?? {
      status: "unknown",
      independent: 0,
      hintAssisted: 0,
      failure: 0,
      mistakes: 0,
    }
  );
}

/**
 * §17 — 한 번 맞힌 건 stable이 아니다.
 *
 *   혼자 맞힌 게 거듭되고 실패가 없다   → stable
 *   실패가 거듭되고 혼자 맞힌 적이 없다 → weak
 *   그 밖에 (섞였거나, 힌트로만 맞혔거나, 한 번뿐) → uncertain
 */
function statusOf(r: SkillRecord): KnowledgeStatus {
  const seen = r.independent + r.hintAssisted + r.failure;
  if (seen === 0) return "unknown";
  if (r.independent >= 2 && r.failure === 0) return "stable";
  if (r.failure >= 2 && r.independent === 0) return "weak";
  return "uncertain";
}

export function recordPerformance(
  state: StudentState,
  skill: string,
  status: PerformanceStatus,
  wrongPicks: number,
): StudentState {
  const prev = skillOf(state, skill);
  const next: SkillRecord = {
    ...prev,
    independent: prev.independent + (status === "independent_success" ? 1 : 0),
    hintAssisted: prev.hintAssisted + (status === "hint_assisted_success" ? 1 : 0),
    failure: prev.failure + (status === "explained" ? 1 : 0),
    mistakes: prev.mistakes + wrongPicks,
  };
  next.status = statusOf(next);
  return { ...state, skills: { ...state.skills, [skill]: next } };
}

/** §16 — 같은 실수가 되풀이되나. 지금은 표시만 하고 복습 배정은 아직 없다 */
export function isRepeatedMistake(state: StudentState, skill: string): boolean {
  return skillOf(state, skill).mistakes >= 2;
}

/* ── 저장 ─────────────────────────────────────────────────────────── */

const STATE_KEY = "loopin.policy.student.v1";
const EVENTS_KEY = "loopin.policy.events.v1";
const MAX_EVENTS = 500;

export function loadStudentState(): StudentState {
  try {
    const raw = window.localStorage.getItem(STATE_KEY);
    const parsed = raw ? (JSON.parse(raw) as StudentState) : null;
    return parsed?.version === 1 && parsed.skills ? parsed : emptyStudentState();
  } catch {
    // 저장소가 없으면(테스트·프라이빗 모드) 처음 보는 학생으로 시작한다
    return emptyStudentState();
  }
}

export function saveStudentState(state: StudentState): void {
  try {
    window.localStorage.setItem(STATE_KEY, JSON.stringify(state));
  } catch {
    /* 저장 못 해도 이번 수업은 그대로 돈다 */
  }
}

/**
 * 명세 §25 — `State + Context + Item → Action → Outcome`.
 * 서버가 생기기 전까지 기기에 쌓아 둔다. 오래된 것부터 버린다.
 */
export type LearningEvent = {
  at: string;
  lessonId: string;
  sentenceId: number;
  stepId: string;
  observation: unknown;
  action: unknown;
  outcome?: PerformanceStatus;
};

export function appendEvents(events: LearningEvent[]): void {
  if (!events.length) return;
  try {
    const raw = window.localStorage.getItem(EVENTS_KEY);
    const prev = raw ? (JSON.parse(raw) as LearningEvent[]) : [];
    window.localStorage.setItem(
      EVENTS_KEY,
      JSON.stringify([...prev, ...events].slice(-MAX_EVENTS)),
    );
  } catch {
    /* 로그는 없어도 된다 */
  }
}
