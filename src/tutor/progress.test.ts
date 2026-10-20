import { beforeEach, describe, expect, it } from "vitest";
import {
  clearResume,
  isDone,
  loadProgress,
  loadResume,
  markDone,
  noteExamAnswer,
  noteReachedEnd,
  noteStudyTime,
  resumeRun,
  saveResume,
  setStatuses,
  startRun,
  statusLine,
  studyTime,
} from "./progress";

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

  it("시작하면 진행 중, 답을 내면 봄 — 목록엔 본 횟수와 최근 정답 여부만", () => {
    startRun("a", undefined, new Date("2026-10-20T01:00:00Z"));
    expect(setStatuses().a?.state).toBe("doing");
    noteExamAnswer(false);
    noteExamAnswer(true); // 같은 회차에 다시 고른 건 세지 않는다
    expect(setStatuses().a).toMatchObject({ state: "done", doneCount: 1, latest: false });
    expect(statusLine(setStatuses().a)).toBe("1번 봄 · 최근 오답");

    startRun("a");
    noteExamAnswer(true);
    markDone("a", "이해");
    startRun("a");
    noteExamAnswer(true);
    markDone("a", "이해");
    expect(statusLine(setStatuses().a)).toBe("3번 봄 · 최근 정답");
  });

  it("맞힘/틀림은 분석한 뒤 고른 보기가 기준 — 분석 없이 끝냈을 때만 바로 풀기로", () => {
    startRun("a");
    noteExamAnswer(false, "first"); // 바로 풀기에서 틀림
    noteExamAnswer(true, "final"); // 분석하고 맞힘
    expect(setStatuses().a?.latest).toBe(true);
    startRun("a");
    noteExamAnswer(true, "first");
    noteExamAnswer(false, "final"); // 분석 뒤 틀렸으면 그게 기준
    expect(setStatuses().a?.latest).toBe(false);
    startRun("a");
    noteExamAnswer(true, "first"); // 바로 맞히고 분석 없이
    expect(statusLine(setStatuses().a)).toBe("3번 봄 · 최근 정답");
  });

  it("다른 문제를 시작하면 그 문제의 회차에 기록한다", () => {
    startRun("a", undefined, new Date("2026-10-20T01:00:00Z"));
    startRun("b", undefined, new Date("2026-10-20T02:00:00Z"));
    noteExamAnswer(true, "first");
    expect(setStatuses().a).toMatchObject({ state: "doing", answered: 0 });
    expect(setStatuses().b).toMatchObject({ state: "done", answered: 1, latest: true });
    markDone("a", "이해"); // 지금 하는 문제가 아니면 회차는 그대로
    expect(setStatuses().a?.state).toBe("doing");
  });

  it("봤다 = 답을 제출했거나(바로 풀기도) 마지막 문장까지 왔거나", () => {
    startRun("a", "lesson-a");
    noteExamAnswer(false, "first", "lesson-a");
    expect(setStatuses().a?.state).toBe("done");
    expect(isDone(loadProgress(), "a")).toBe(true);

    startRun("b", "lesson-b");
    noteReachedEnd("a"); // 지금 하는 문제가 아니면 무시
    expect(setStatuses().b?.state).toBe("doing");
    noteReachedEnd("b"); // 답을 안 냈어도 마지막 문장까지 왔다
    expect(setStatuses().b).toMatchObject({ state: "done", doneCount: 1, latest: null });
    expect(statusLine(setStatuses().b)).toBe("1번 봄");
  });

  it("다른 지문의 답은 지금 회차에 붙이지 않는다 (공유 링크 등 회차 없이 연 수업)", () => {
    startRun("a", "lesson-a");
    noteExamAnswer(true, "final", "lesson-b");
    expect(setStatuses().a).toMatchObject({ state: "doing", answered: 0 });
  });

  it("멈춘 자리를 남기고, 돌아오면 같은 회차를 잇는다", () => {
    startRun("a", "lesson-a");
    noteStudyTime("a", 120);
    saveResume("a", "lesson-a", { shape: "x", state: { si: 3 } });
    expect(setStatuses().a?.resumable).toBe(true);
    expect(loadResume("a", "lesson-b")).toBeNull(); // 다른 지문이면 없다
    startRun("b", "lesson-b");
    expect(resumeRun("a", "lesson-a")).toBe(120); // 새 회차 없이 이어서, 시계도
    noteExamAnswer(true, "final", "lesson-a");
    expect(setStatuses().a).toMatchObject({ doneCount: 1, latest: true });
    expect(loadResume("a", "lesson-a")).toEqual({ shape: "x", state: { si: 3 } });
    clearResume("a");
    expect(setStatuses().a?.resumable).toBe(false);
  });

  it("공부 시간을 회차마다 남기고 더해서 보여 준다", () => {
    startRun("a");
    noteStudyTime("a", 300);
    noteStudyTime("a", 200); // 줄지 않는다
    noteStudyTime("b", 999); // 지금 하는 문제가 아니면 무시
    markDone("a", "이해");
    startRun("a");
    noteStudyTime("a", 330);
    markDone("a", "이해");
    expect(setStatuses().a?.seconds).toBe(630);
    expect(statusLine(setStatuses().a)).toBe("2번 봄 · ⏱ 10m");
    expect(studyTime(40)).toBe("1m 미만");
    expect(studyTime(3900)).toBe("1h 5m");
    expect(studyTime(0)).toBeNull();
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
