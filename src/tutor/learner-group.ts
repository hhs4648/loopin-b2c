/**
 * 학습자 구분 — 온보딩에서 한 번 고른다 (2026-10-22 선생님: 나중에 지표 볼 때 참고).
 *
 * 브라우저에 두고 서버(`learner_state`의 `loopin.learner_group`)에도 사본이 간다 (`cloud.ts`).
 * 지금은 코스·수업에 영향이 없다 — 중학생·일반인은 모의고사 등급 질문만 건너뛴다.
 */

import { pushKey } from "./cloud";

export const LEARNER_GROUP_KEY = "loopin.learner_group";

export const LEARNER_GROUPS = [
  { id: "suneung", label: "고3·N수생" },
  { id: "high12", label: "고1·2" },
  { id: "middle", label: "중학생" },
  { id: "adult", label: "일반인" },
] as const;

export type LearnerGroup = (typeof LEARNER_GROUPS)[number]["id"];

const IDS = new Set<string>(LEARNER_GROUPS.map((g) => g.id));

export function loadLearnerGroup(): LearnerGroup | null {
  try {
    const saved = window.localStorage.getItem(LEARNER_GROUP_KEY)?.trim();
    return saved && IDS.has(saved) ? (saved as LearnerGroup) : null;
  } catch {
    return null;
  }
}

export function saveLearnerGroup(group: LearnerGroup): void {
  try {
    window.localStorage.setItem(LEARNER_GROUP_KEY, group);
    pushKey(LEARNER_GROUP_KEY);
  } catch {
    /* 저장 못 해도 온보딩은 그대로 간다 */
  }
}
