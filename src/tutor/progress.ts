/**
 * 어느 문제를 끝냈는지.
 *
 * **이 브라우저에만 남는다.** 서버(`sessions`)에도 수업 기록이 남지만 그건
 * 난이도를 재려고 모으는 것이고, 목록에 「완료」를 칠하는 데는 지금 당장
 * 손에 있는 값이 필요하다. 계정을 붙일 때 서버 기록으로 갈아타면 된다.
 *
 * 저장이 안 되는 브라우저(사파리 프라이빗 등)에서는 그냥 완료 표시가 안 뜬다.
 * 수업은 그대로 돌아간다.
 */

const KEY = "dajung.done";

/**
 * 세트 id → 마지막으로 받은 결과 (이해·오류후이해·취약·설명제공).
 * 단위로 쪼갠 세트는 **단위의 레슨 id**로도 같은 자리에 적는다 — 세트 id와 겹치지 않는다.
 */
export type Progress = Record<string, string>;

export function loadProgress(): Progress {
  try {
    const raw = window.localStorage.getItem(KEY);
    const parsed: unknown = raw ? JSON.parse(raw) : null;
    if (!parsed || typeof parsed !== "object") return {};
    return parsed as Progress;
  } catch {
    return {};
  }
}

/**
 * 끝낸 것으로 표시한다.
 *
 * 다시 풀면 **마지막 결과로 덮어쓴다** — 「취약」이었다가 「이해」가 되면 그게
 * 지금의 실력이다. 완료 여부 자체는 한 번 켜지면 꺼지지 않는다.
 */
export function markDone(setId: string, result: string): void {
  try {
    const next = { ...loadProgress(), [setId]: result };
    window.localStorage.setItem(KEY, JSON.stringify(next));
  } catch {
    /* 저장 못 해도 수업은 끝났다 */
  }
}

export function isDone(progress: Progress, setId: string): boolean {
  return setId in progress;
}

/**
 * 단위 하나를 끝냈다. 만들어진 단위를 다 끝냈으면 세트도 「완료」가 된다 —
 * 세트의 결과는 마지막 단위(실전 풀기)의 것이다.
 */
export function markUnitDone(setId: string, unitLessons: string[], lessonId: string, result: string): void {
  markDone(lessonId, result);
  const progress = loadProgress();
  if (unitLessons.every((id) => isDone(progress, id))) {
    markDone(setId, progress[unitLessons[unitLessons.length - 1]!] ?? result);
  }
}
