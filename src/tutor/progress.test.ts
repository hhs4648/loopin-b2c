import { beforeEach, describe, expect, it } from "vitest";
import { isDone, loadProgress, markDone, noteExamAnswer, setStatuses, startRun, statusLine } from "./progress";

/*
  테스트는 노드에서 돈다 — jsdom을 새로 들이는 대신 필요한 것만 흉내 낸다.
  `progress.ts`가 쓰는 건 localStorage 세 함수뿐이다.
*/
const store = new Map<string, string>();
Object.defineProperty(globalThis, "window", {
  value: {
    localStorage: {
      getItem: (k: string) => store.get(k) ?? null,
      setItem: (k: string, v: string) => void store.set(k, v),
      removeItem: (k: string) => void store.delete(k),
    },
  },
  writable: true,
});

describe("완료 표시", () => {
  beforeEach(() => store.clear());

  it("끝낸 문제를 기억한다", () => {
    markDone("suneung-18", "이해");
    expect(loadProgress()["suneung-18"]).toBe("이해");
    expect(isDone(loadProgress(), "suneung-18")).toBe(true);
    expect(isDone(loadProgress(), "suneung-19")).toBe(false);
  });

  it("다시 풀면 마지막 결과로 덮어쓴다 — 그게 지금의 실력이다", () => {
    markDone("suneung-18", "취약");
    markDone("suneung-18", "이해");
    expect(loadProgress()["suneung-18"]).toBe("이해");
  });

  it("시작하면 진행 중, 끝내면 완료 — 회차마다 처음 고른 보기로 맞힘을 센다", () => {
    startRun("a", new Date("2026-10-20T01:00:00Z"));
    expect(setStatuses().a?.state).toBe("doing");
    noteExamAnswer(false);
    noteExamAnswer(true); // 다시 고른 건 세지 않는다
    markDone("a", "오류후이해");
    expect(setStatuses().a).toMatchObject({ state: "done", doneCount: 1, answered: 1, correct: 0 });
    expect(statusLine(setStatuses().a)).toBe("1번 봄 · 틀림");

    startRun("a");
    noteExamAnswer(true);
    markDone("a", "이해");
    startRun("a");
    noteExamAnswer(true);
    markDone("a", "이해");
    expect(statusLine(setStatuses().a)).toBe("3번 봄 · 3번 중 2번 맞힘");
  });

  it("다른 문제를 시작하면 그 문제의 회차에 기록한다", () => {
    startRun("a", new Date("2026-10-20T01:00:00Z"));
    startRun("b", new Date("2026-10-20T02:00:00Z"));
    noteExamAnswer(true);
    expect(setStatuses().a).toMatchObject({ state: "doing", answered: 0 });
    expect(setStatuses().b).toMatchObject({ state: "doing", answered: 1, correct: 1 });
    markDone("a", "이해"); // 지금 하는 문제가 아니면 회차는 그대로
    expect(setStatuses().a?.state).toBe("doing");
  });

  it("예전 완료 기록만 있어도 완료로 보인다", () => {
    markDone("old", "이해");
    expect(setStatuses().old).toMatchObject({ state: "done", doneCount: 1, answered: 0 });
  });

  it("저장된 게 망가져 있어도 빈 값으로 돌려준다", () => {
    store.set("dajung.done", "{망가진 값");
    expect(loadProgress()).toEqual({});
  });
});
