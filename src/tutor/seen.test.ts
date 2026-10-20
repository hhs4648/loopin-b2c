import { beforeEach, describe, expect, it } from "vitest";
import { getMiniMock, saveAttempt } from "./mini";
import { kindStats, seenBySet } from "./seen";
import { getSet } from "./sets";
import { hardestSets, tenMinMocks } from "./tenmin";

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

describe("진도표 — 본 문제·안 본 문제·자주 틀리는 유형", () => {
  beforeEach(() => store.clear());

  it("10분 모의고사를 풀면 그 문항들이 봄으로, 틀린 건 최근 틀림으로", () => {
    const mock = tenMinMocks("all")[0]!;
    const [a, b] = mock.items;
    saveAttempt(mock.id, {
      at: "2026-10-20T01:00:00Z", seconds: 300, timeUp: false,
      answers: { [a!.no]: a!.answer, [b!.no]: (b!.answer % 5) + 1 },
    });
    const rows = seenBySet();
    expect(rows[a!.lesson!]).toMatchObject({ seen: true, latest: true, answered: 1, wrong: 0 });
    expect(rows[b!.lesson!]).toMatchObject({ seen: true, latest: false, answered: 1, wrong: 1 });
    // 답을 안 낸 문항은 봤지만 결과가 없다
    expect(rows[mock.items[2]!.lesson!]).toMatchObject({ seen: true, latest: null, answered: 0 });
    const kinds = kindStats(rows);
    const kb = kinds.find((k) => k.kind === getSet(b!.lesson!)!.subtitle.split(" — ")[0]);
    expect(kb?.wrong).toBe(1);
    expect(kinds[0]!.rate).toBeGreaterThanOrEqual(kinds.at(-1)!.rate);
  });

  it("2점 변형 코스는 3점 문제를 빼고, id·제목에 2점이 붙는다", () => {
    const two = hardestSets("moeui-2024-03", 10, "2pt");
    expect(two.length).toBeGreaterThan(0);
    const mocks = tenMinMocks("2pt");
    expect(mocks[0]!.id).toMatch(/-2pt-1$/);
    expect(mocks[0]!.title).toContain("2점");
    for (const m of mocks) for (const it of m.items) expect(it.points).toBe(2);
    expect(getMiniMock(mocks[0]!.id)).toBe(mocks[0]);
  });
});

describe("예상 시험점수 — 어려운 5문제 결과를 100점으로 환산", () => {
  it("다 맞히면 거의 만점, 다 틀리면 나머지 쉬운 문제의 80%", async () => {
    const { estimatedExamScore } = await import("./mini");
    const mock = tenMinMocks("all")[0]!;
    const all: Record<number, number> = {};
    for (const it of mock.items) all[it.no] = it.answer;
    const max = mock.items.reduce((n, it) => n + it.points, 0);
    expect(estimatedExamScore(mock, all)).toBe(Math.round(max + (100 - max) * 0.95));
    expect(estimatedExamScore(mock, {})).toBe(Math.round((100 - max) * 0.8));
  });
});

describe("문장 연습 — 추천 순·시험별 묶음", () => {
  it("틀린 지문의 문장이 모이고, 안 본 것·틀린 지문 먼저, 시험별로 본 비율", async () => {
    const { practiceSentences, practiceGroups, recommendedOrder, markPracticed, practicedKeys } = await import("./sentencePractice");
    store.clear();
    const mock = tenMinMocks("all")[0]!;
    const [a] = mock.items;
    saveAttempt(mock.id, { at: "2026-10-20T01:00:00Z", seconds: 300, timeUp: false, answers: { [a!.no]: (a!.answer % 5) + 1 } });
    const list = practiceSentences();
    expect(list.length).toBeGreaterThan(0);
    expect(list[0]!.reason).toBe("틀린 지문");
    expect(list[0]!.setId).toBe(a!.lesson);
    // 한국어 칸은 { en, ko }만 센다 — 덩어리는 전부 어느 칸의 답이다
    const slots = list[0]!.ko.filter((k) => typeof k === "object") as { en: string }[];
    for (const s of slots) expect(list[0]!.chunks).toContain(s.en);
    markPracticed(list[0]!.key);
    const order = recommendedOrder(list, practicedKeys());
    expect(order.at(-1)!.key).toBe(list[0]!.key); // 본 문장은 뒤로
    const g = practiceGroups(list, practicedKeys());
    expect(g[0]!.seen).toBe(1);
    expect(g[0]!.title).toContain("2026");
  });
});
