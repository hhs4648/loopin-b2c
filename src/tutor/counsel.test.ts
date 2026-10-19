import { describe, expect, it } from "vitest";
import type { LessonSet } from "../../content/tutor/types";
import { buildPlan, gradeOfScore, levelOfGrade, nextSetOf, todayOf, weakFromMini, type CounselAnswers } from "./counsel";
import { allSets } from "./sets";

const base: CounselAnswers = { grade: 4, goal: 2, exam: "수능", weak: [], timeShort: false, minutes: 30 };

const set = (id: string, kind: string, rate?: number): LessonSet => ({
  id,
  collection: "c",
  title: id,
  subtitle: `${kind} — 테스트`,
  wrong_rate: rate,
  lessons: [id],
});

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
});

describe("상담실 — 커리큘럼", () => {
  const sets = [
    set("a", "빈칸", 60),
    set("b", "빈칸", 80),
    set("c", "순서", 70),
    set("d", "제목", 90),
    set("e", "듣기 응답", 95),
    set("b-v1", "빈칸", 80),
  ];

  it("아쉬운 유형부터, 유형끼리 번갈아, 나머지는 오답률 순, 듣기는 맨 끝", () => {
    const plan = buildPlan({ ...base, weak: ["빈칸", "순서"] }, sets, {});
    expect(plan.days.flatMap((d) => d.sets)).toEqual(["b", "c", "a", "d", "e"]);
  });

  it("6등급 아래는 같은 유형 안에서 쉬운 것(오답률 낮은 것)부터", () => {
    const plan = buildPlan({ ...base, grade: 7, weak: ["빈칸"] }, sets, {});
    expect(plan.days.flatMap((d) => d.sets).slice(0, 2)).toEqual(["a", "b"]);
  });

  it("끝낸 문제는 맨 뒤, 비교용 사본(-v1)은 빼고, 하루 분량은 공부 시간대로", () => {
    const plan = buildPlan({ ...base, minutes: 15, weak: ["빈칸"] }, sets, { b: "이해" });
    expect(plan.days.map((d) => d.sets)).toEqual([["a"], ["d"], ["c"], ["e"], ["b"]]);
    expect(nextSetOf(plan, { b: "이해" })).toBe("a");
    expect(todayOf(plan, { b: "이해", a: "이해" })?.day).toBe(2);
  });

  it("미니 모의고사에서 절반 넘게 틀린 유형도 집중 유형에 들어간다", () => {
    const fromRecords = weakFromMini([
      { kind: "빈칸", right: 1, total: 4 },
      { kind: "순서", right: 2, total: 3 },
      { kind: "어휘", right: 0, total: 1 },
      { kind: "어법", right: 1, total: 1 },
    ]);
    expect(fromRecords).toEqual(["빈칸"]);
    expect(buildPlan(base, sets, {}, fromRecords).focus).toEqual(["빈칸"]);
  });

  it("시간이 모자라면 마지막 날에 미니 모의고사", () => {
    const plan = buildPlan({ ...base, timeShort: true }, sets, {});
    expect(plan.days.at(-1)?.mini).toBe(true);
    expect(plan.days.slice(0, -1).some((d) => d.mini)).toBe(false);
  });

  it("실제 세트로 짜도 일주일 · 중복 없이 나온다", () => {
    const plan = buildPlan({ ...base, minutes: 60, weak: ["빈칸", "문장 넣기"] }, allSets(), {});
    const ids = plan.days.flatMap((d) => d.sets);
    expect(plan.days.length).toBe(7);
    expect(new Set(ids).size).toBe(ids.length);
    expect(ids.some((id) => id.endsWith("-v1"))).toBe(false);
  });
});
