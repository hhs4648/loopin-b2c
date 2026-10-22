/**
 * 추가 퀘스트(수업 끝 단어 짝 맞추기) 기록 — 성공하면 친밀도 2배 (2026-10-22 선생님).
 * 친밀도 숫자는 아직 홈에서 가려 둔다(`HomeVillage` SHOW_STATS). 쓰임이 정해지면 이 기록으로 센다
 */
export type QuestRun = { cleared: boolean; pairs: number; lives: number; at: string };

const KEY = "loopin.quest.v1";

export function loadQuests(): QuestRun[] {
  try {
    const parsed = JSON.parse(window.localStorage.getItem(KEY) ?? "[]") as unknown;
    return Array.isArray(parsed) ? (parsed as QuestRun[]) : [];
  } catch {
    return [];
  }
}

export function recordQuest(run: QuestRun): void {
  try {
    window.localStorage.setItem(KEY, JSON.stringify([...loadQuests(), run].slice(-200)));
  } catch {
    /* 못 남겨도 퀘스트는 끝난다 */
  }
}
