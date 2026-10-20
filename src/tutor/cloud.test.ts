import { describe, expect, it } from "vitest";
import { MERGES, SYNCED_KEYS } from "./cloud";

/* 합치기 규칙만 본다 — 네트워크는 테스트에서 꺼져 있다(`enabled()`) */
describe("서버 사본 합치기", () => {
  it("동기화하는 키는 진행 기록 둘 · 노트 · 단어장 · 미니 모의고사 기록 · 상담 코스", () => {
    expect(SYNCED_KEYS).toEqual(["dajung.done", "dajung.runs", "loopin.notes.v1", "loopin.vocab.v1", "loopin.mini.v1", "loopin.mini.doing.v1", "loopin.wrong-reviews.v1", "loopin.sentence-practice.v1", "loopin.vocab-slots.v1", "loopin.counsel.v1"]);
  });

  it("미니 기록은 시험마다 합쳐 최근 것이 앞, 상담 코스는 더 최근에 짠 쪽", () => {
    const mini = MERGES["loopin.mini.v1"]!(
      { a: [{ at: "2026-10-20T02:00:00Z" }] },
      { a: [{ at: "2026-10-19T00:00:00Z" }], b: [{ at: "2026-10-18T00:00:00Z" }] },
    ) as Record<string, { at: string }[]>;
    expect(mini.a!.map((x) => x.at)).toEqual(["2026-10-20T02:00:00Z", "2026-10-19T00:00:00Z"]);
    expect(mini.b).toHaveLength(1);
    expect(MERGES["loopin.counsel.v1"]!({ at: "2026-10-19", course: ["x"] }, { at: "2026-10-20", course: ["y"] })).toEqual({ at: "2026-10-20", course: ["y"] });
    expect(MERGES["loopin.counsel.v1"]!(null, { at: "2026-10-20" })).toEqual({ at: "2026-10-20" });
  });

  it("완료 표시 — 둘을 합치되 같은 세트는 이 기기 값이 이긴다", () => {
    expect(MERGES["dajung.done"]!({ a: "이해" }, { a: "취약", b: "이해" })).toEqual({ a: "이해", b: "이해" });
    expect(MERGES["dajung.done"]!(null, { b: "이해" })).toEqual({ b: "이해" });
  });

  it("회차 — 세트마다 시작 시각으로 합치고 순서대로", () => {
    const r = (t: string) => ({ started_at: t, last_at: t, done: true, correct: null });
    const merged = MERGES["dajung.runs"]!(
      { current: "a", sets: { a: [r("2026-10-20T02:00:00Z")] } },
      { current: "b", sets: { a: [r("2026-10-20T01:00:00Z"), r("2026-10-20T02:00:00Z")], b: [r("2026-10-19T00:00:00Z")] } },
    ) as { current: string; sets: Record<string, { started_at: string }[]> };
    expect(merged.current).toBe("a");
    expect(merged.sets.a!.map((x) => x.started_at)).toEqual(["2026-10-20T01:00:00Z", "2026-10-20T02:00:00Z"]);
    expect(merged.sets.b).toHaveLength(1);
  });

  it("노트·단어장 — 같은 것은 하나로, 서버에만 있던 것은 살아난다", () => {
    const notes = MERGES["loopin.notes.v1"]!(
      [{ lessonId: "L", key: "s1", savedAt: "2026-10-20T02:00:00Z" }],
      [{ lessonId: "L", key: "s1", savedAt: "2026-10-19T00:00:00Z" }, { lessonId: "L", key: "s2", savedAt: "2026-10-18T00:00:00Z" }],
    ) as { key: string }[];
    expect(notes.map((n) => n.key)).toEqual(["s2", "s1"]);

    const vocab = MERGES["loopin.vocab.v1"]!(
      [{ en: "Innovator", savedAt: "2026-10-20T00:00:00Z" }],
      [{ en: "innovator", savedAt: "2026-10-19T00:00:00Z" }, { en: "without", savedAt: "2026-10-21T00:00:00Z" }],
    ) as { en: string }[];
    expect(vocab.map((w) => w.en)).toEqual(["Innovator", "without"]);
  });
});
