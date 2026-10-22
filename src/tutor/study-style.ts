/**
 * 공부 성향 — 빠르게 푸는 쪽인지, 꼼꼼히 분석하는 쪽인지 (2026-10-22 선생님).
 *
 * 온보딩에서 묻지 않고 **학생이 실제로 고른 것**을 센다: 핵심어로 바로 푼 뒤 [다음 문제로]면 fast,
 * [분석하기]·「분석부터 할게요」면 deep. 브라우저에 두고 서버(`learner_state`의 `loopin.study_style`)에도 사본이 간다.
 * 지금은 온보딩 예시 문제(핵심어로 한 번에 풀기)에서만 기록한다 — 다음 단계에서 시작 버튼 순서를 이 값에 맞춘다.
 */

import { pushKey } from "./cloud";

export const STUDY_STYLE_KEY = "loopin.study_style";

export type StudyStyle = {
  fast: number;
  deep: number;
  last: "fast" | "deep" | null;
  /** 「핵심어로 한 번에 푸는 법」 설명을 봤다 — 다음부터는 짧게 */
  howtoSeen: boolean;
  at: string;
};

const EMPTY: StudyStyle = { fast: 0, deep: 0, last: null, howtoSeen: false, at: "" };

export function loadStudyStyle(): StudyStyle {
  try {
    const raw = window.localStorage.getItem(STUDY_STYLE_KEY);
    return raw ? { ...EMPTY, ...(JSON.parse(raw) as Partial<StudyStyle>) } : EMPTY;
  } catch {
    return EMPTY;
  }
}

function save(next: StudyStyle): void {
  try {
    window.localStorage.setItem(STUDY_STYLE_KEY, JSON.stringify({ ...next, at: new Date().toISOString() }));
    pushKey(STUDY_STYLE_KEY);
  } catch {
    /* 못 남겨도 수업은 그대로 */
  }
}

export function recordStudyChoice(kind: "fast" | "deep"): void {
  const s = loadStudyStyle();
  save({ ...s, [kind]: s[kind] + 1, last: kind });
}

export function markHowtoSeen(): void {
  const s = loadStudyStyle();
  if (!s.howtoSeen) save({ ...s, howtoSeen: true });
}
