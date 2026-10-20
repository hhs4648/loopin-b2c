import { beforeEach, describe, expect, it } from "vitest";
import { VOCAB_PREFIX, buildPlan, courseProgress, courseStatus, examTier, gradeOfScore, levelOfGrade, markVocabSlot, nextMockOf, weakFromMini, type CounselAnswers } from "./counsel";
import { getMiniMock, saveAttempt } from "./mini";
import { tenMinMocks } from "./tenmin";

/* 노드에는 localStorage가 없다 — 미니 모의고사 기록이 쓰는 세 함수만 흉내 낸다 */
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

const base: CounselAnswers = { grade: 4, goal: 2, exam: "수능", weak: [], timeShort: false, minutes: 30 };

describe("상담실 — 점수와 등급", () => {
  it("영어 절대평가: 90점부터 1등급, 10점마다 한 등급", () => {
    expect(gradeOfScore(100)).toBe(1);
    expect(gradeOfScore(90)).toBe(1);
    expect(gradeOfScore(89)).toBe(2);
    expect(gradeOfScore(80)).toBe(2);
    expect(gradeOfScore(79)).toBe(3);
    expect(gradeOfScore(0)).toBe(9);
  });

  it("등급 → 수업 단계 (고 1~2 · 중 3~5 · 초 6~, 모르면 중)", () => {
    expect(levelOfGrade(2)).toBe("고");
    expect(levelOfGrade(5)).toBe("중");
    expect(levelOfGrade(6)).toBe("초");
    expect(levelOfGrade(null)).toBe("중");
  });

  it("미니 모의고사에서 절반 넘게 틀린 유형도 집중 유형에 들어간다", () => {
    const fromRecords = weakFromMini([
      { kind: "빈칸", right: 1, total: 4 },
      { kind: "순서", right: 2, total: 3 },
      { kind: "어휘", right: 0, total: 1 },
      { kind: "어법", right: 1, total: 1 },
    ]);
    expect(fromRecords).toEqual(["빈칸"]);
    expect(buildPlan(base, fromRecords).focus).toEqual(["빈칸"]);
  });
});

describe("상담실 — 코스 (10분 모의고사 순서)", () => {
  beforeEach(() => store.clear());

  /** 한 회를 풀었다고 기록 — wrongNos는 틀린 문항 번호 */
  function solve(mockId: string, wrongNos: number[] = []) {
    const mock = getMiniMock(mockId)!;
    const answers: Record<number, number> = {};
    for (const it of mock.items) answers[it.no] = wrongNos.includes(it.no) ? ((it.answer % 5) + 1) : it.answer;
    saveAttempt(mockId, {
      at: new Date().toISOString(), answers, seconds: 300, timeUp: false,
      ...(mockId.startsWith("ten-review-") ? { items: mock.items.map((it) => ({ no: it.no, lesson: it.lesson })) } : {}),
    });
  }

  it("회차마다 실전·분석·단어 연습·복습 단계 — 단어 연습은 테스트를 끝내야 완료, 분석은 틀린 문항 기준", () => {
    const plan = buildPlan(base);
    const [first, second] = plan.course;
    const wrongNo = getMiniMock(first!)!.items[0]!.no;
    solve(first!, [wrongNo]);
    const st = courseStatus(plan)[0]!;
    expect(st.words).toBe(false);
    expect(st.exam?.title).toContain("2026");
    expect(st.analysis).toEqual({ done: 0, total: 1 });
    expect(st.marks?.find((m) => m.no === wrongNo)?.result).toBe("wrong");
    expect(st.marks?.filter((m) => m.result === "right").length).toBe(getMiniMock(first!)!.items.length - 1);
    expect(nextMockOf(plan)).toBe(second);
    markVocabSlot(`${VOCAB_PREFIX}${first}`);
    expect(courseStatus(plan)[0]!.words).toBe(true);
    expect(courseProgress(plan)).toEqual({ done: 1, total: plan.course.length });
  });

  it("시험 순위: 3·6·9월·수능을 합쳐 최근 것부터 → 나머지 달", () => {
    expect(examTier({ held: "2026-03", body: "교육청" })).toBe(0);
    expect(examTier({ held: "2025-09", body: "평가원" })).toBe(0);
    expect(examTier({ held: "2025-11", body: "평가원" })).toBe(0); // 수능도 모의고사와 합쳐 최근 것부터
    expect(examTier({ held: "2025-11", body: "평가원" }, true)).toBe(-1);
    expect(examTier({ held: "2025-10", body: "교육청" })).toBe(2);
    expect(examTier({ held: "2025-05", body: "교육청" })).toBe(2);
  });

  it("코스는 최근 시험부터 (1) 다음 (2) — 상담을 안 했어도 같다", () => {
    const ids = tenMinMocks().map((m) => m.id);
    expect(ids[0]).toBe("ten-moeui-2026-03-1");
    expect(buildPlan(base).course).toEqual(ids);
    expect(courseStatus(null).filter((it) => !it.review).map((it) => it.id)).toEqual(ids);
    expect(nextMockOf(null)).toBe(ids[0]);
  });

  it("푼 회는 점수가 남고, 다음 할 것은 안 푼 첫 회", () => {
    const plan = buildPlan(base);
    const [first, second] = plan.course;
    solve(first!, [getMiniMock(first!)!.items[0]!.no]);
    markVocabSlot(`${VOCAB_PREFIX}${first}`);
    const st = courseStatus(plan);
    expect(st[0]!.done).toBe(true);
    expect(st[0]!.score?.correct).toBe(getMiniMock(first!)!.items.length - 1);
    expect(st[0]!.wrong).toBe(1);
    expect(nextMockOf(plan)).toBe(second);
    expect(courseProgress(plan)).toEqual({ done: 1, total: plan.course.length });
  });

  it("회차의 4단계 — 틀린 문제를 힌트 없이 다시 풀고, 맞히면 틀린 문제에서 빠진다", async () => {
    const { itemsToReview, reviewProgress, saveReviewRecord } = await import("./wrongReview");
    const { wrongItems } = await import("./mini");
    const plan = buildPlan(base);
    const first = plan.course[0]!;
    const it0 = getMiniMock(first)!.items[0]!;
    solve(first, [it0.no]);
    expect(itemsToReview(first).map((x) => x.no)).toEqual([it0.no]);
    expect(reviewProgress(first)).toEqual({ done: 0, total: 1 });
    expect(courseStatus(plan)[0]!.review4).toEqual({ done: 0, total: 1 });
    expect(wrongItems().map((x) => x.lesson)).toContain(it0.lesson);
    // 또 틀림 — 이유를 적어 기록
    saveReviewRecord(first, it0.no, { correct: false, picked: 1, reason: "빈칸 앞 문장을 반대로 읽음" });
    expect(reviewProgress(first)).toEqual({ done: 1, total: 1 });
    expect(wrongItems().map((x) => x.lesson)).toContain(it0.lesson);
    // 다시 풀어 맞힘 — 틀린 문제에서 빠진다
    await new Promise((r) => setTimeout(r, 2));
    saveReviewRecord(first, it0.no, { correct: true, picked: it0.answer });
    expect(wrongItems().map((x) => x.lesson)).not.toContain(it0.lesson);
    // 세 회마다 끼던 복습 칸은 없다
    expect(courseStatus(plan).some((x) => x.review)).toBe(false);
  });
});
