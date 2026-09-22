import { describe, expect, it } from "vitest";
import data from "../../content/tutor/sets.json";
import type { LessonSet } from "../../content/tutor/types";
import {
  allCollections,
  allGroups,
  allSets,
  firstLessonId,
  getCollection,
  knownLessonIds,
  sentencesIn,
  sentenceCount,
  setOfLesson,
  setsIn,
} from "./sets";

const RAW = data.sets as LessonSet[];

/**
 * 세트는 **학생이 고르는 단위**다. 여기가 어긋나면 목록에 카드가 안 뜨거나,
 * 눌렀을 때 엉뚱한 지문이 열린다 — 둘 다 화면을 봐야만 알 수 있는 종류의 버그다.
 */
describe("수업 세트", () => {
  it("적어 둔 레슨 id가 실제로 있다", () => {
    const missing = RAW.flatMap((set) =>
      set.lessons.filter((id) => !knownLessonIds().includes(id)).map((id) => `${set.id}: ${id}`),
    );
    expect(missing).toEqual([]);
  });

  it("세트 id가 겹치지 않는다", () => {
    const ids = RAW.map((set) => set.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("목록에 올리지 않은 지문은 참고용으로 적어 둔 것만 허용한다", () => {
    /*
      탈레스 원안은 엔진 회귀용으로 JSON을 남긴다. 학생이 고르는 목록에는
      올리지 않는다.
    */
    const allowedUnlisted = new Set(["thales-participial-phrase-front"]);
    const orphans = knownLessonIds().filter((id) => !setOfLesson(id) && !allowedUnlisted.has(id));
    expect(orphans).toEqual([]);
  });

  it("모든 세트가 있는 중분류에 붙어 있다 — 안 그러면 목록에서 못 연다", () => {
    const known = new Set(allCollections().map((c) => c.id));
    const orphans = allSets().filter((s) => !known.has(s.collection));
    expect(orphans.map((s) => s.id)).toEqual([]);
  });

  it("대분류 > 중분류 > 세트 세 켜가 이어진다", () => {
    expect(allGroups().map((g) => g.id)).toEqual(["suneung", "moeui"]);
    expect(allCollections().map((c) => c.id)).toEqual([
      "suneung-2024",
      "moeui-2027-09",
      "moeui-2025-03",
    ]);
    // 모든 세트는 어느 중분류엔가 담긴다 — 흩어진 것이 없어야 한다
    const inCollections = allCollections().reduce((n, c) => n + setsIn(c.id).length, 0);
    expect(inCollections).toBe(allSets().length);
  });

  it("2024 수능에 26문제가 들어 있다", () => {
    const sets = setsIn("suneung-2024");
    expect(getCollection("suneung-2024")?.title).toBe("2024 수능");
    expect(sets).toHaveLength(26);
    expect(sets[0]!.title).toBe("18번 문제");
  });

  it("카드에 띄우는 문장 수가 실제 지문과 같다", () => {
    for (const set of allSets()) {
      const real = set.lessons.reduce((n, id) => n + sentencesIn(id), 0);
      expect(sentenceCount(set), set.id).toBe(real);
    }
  });

  it("세트를 시작하면 그 세트의 첫 지문이 열린다", () => {
    for (const set of allSets()) {
      expect(firstLessonId(set), set.id).toBe(set.lessons[0]);
    }
  });

  it("수능 18번 세트에 퇴사 편지 7문장이 들어 있다", () => {
    const suneung = allSets().find((set) => set.id === "suneung-18");
    expect(suneung?.title).toBe("18번 문제");
    expect(suneung?.lessons).toEqual(["resignation-letter"]);
    expect(sentenceCount(suneung!)).toBe(7);
  });
});
