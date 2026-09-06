import { beforeEach, describe, expect, it } from "vitest";
import { isDone, loadProgress, markDone } from "./progress";

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

  it("저장된 게 망가져 있어도 빈 값으로 돌려준다", () => {
    store.set("dajung.done", "{망가진 값");
    expect(loadProgress()).toEqual({});
  });
});
