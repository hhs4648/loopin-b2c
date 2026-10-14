import { beforeEach, describe, expect, it } from "vitest";
import { noteTipOpened, takeTipShow } from "./tipExposure";

describe("되풀이 💡 칩 — 눌렀으면 세 번, 안 눌렀으면 다섯 번까지", () => {
  beforeEach(() => {
    const store = new Map<string, string>();
    (globalThis as unknown as { window: unknown }).window = {
      localStorage: { getItem: (k: string) => store.get(k) ?? null, setItem: (k: string, v: string) => void store.set(k, v) },
    };
  });

  it("안 누르면 다섯 화면까지 보이고 여섯째부터 안 보인다 — 같은 화면은 한 번으로 센다", () => {
    const shown = [1, 1, 2, 3, 4, 5, 6, 7].map((n) => takeTipShow("왜 핵심어만 보나요?", `화면${n}`));
    expect(shown).toEqual([true, true, true, true, true, true, false, false]);
  });

  it("한 번 누르면 세 화면까지만", () => {
    expect(takeTipShow("빈칸 문제 요령", "a")).toBe(true);
    noteTipOpened("빈칸 문제 요령");
    expect(takeTipShow("빈칸 문제 요령", "b")).toBe(true);
    expect(takeTipShow("빈칸 문제 요령", "c")).toBe(true);
    expect(takeTipShow("빈칸 문제 요령", "d")).toBe(false);
  });

  it("칩마다 따로 센다", () => {
    for (const n of [1, 2, 3, 4, 5]) takeTipShow("A", `x${n}`);
    expect(takeTipShow("A", "x6")).toBe(false);
    expect(takeTipShow("B", "x6")).toBe(true);
  });
});
