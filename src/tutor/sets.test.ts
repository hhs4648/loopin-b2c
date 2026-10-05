import { describe, expect, it } from "vitest";
import data from "../../content/tutor/sets.json";
import type { LessonSet } from "../../content/tutor/types";
import {
  allCollections,
  allGroups,
  allSets,
  firstLessonId,
  getCollection,
  getSet,
  knownLessonIds,
  nextUnit,
  sentencesIn,
  sentenceCount,
  setOfLesson,
  setsIn,
  unitsOf,
} from "./sets";
import { getPolicyLesson } from "./policy/lessons";

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
      올리지 않는다. 통째로 된 예전 21번도 같다 — 21번은 작은 단위로 다시 만드는
      중이고, 예전 것은 Teaching Policy 엔진 회귀용으로만 남겼다.
    */
    const allowedUnlisted = new Set([
      "thales-participial-phrase-front",
      "moeui-2025-03-21-descartes-tree",
    ]);
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

  it("단위로 쪼갠 세트: 만들어진 단위의 레슨이 `lessons`와 같은 순서로 같다", () => {
    for (const set of RAW) {
      if (!set.units) continue;
      const built = set.units.flatMap((u) => (u.lesson ? [u.lesson] : []));
      expect(built, set.id).toEqual(set.lessons);
      // 단위 이름은 그 레슨이 머리글에 띄우는 이름과 같아야 한다
      for (const u of set.units) {
        if (u.lesson) expect(getPolicyLesson(u.lesson)?.unit, u.lesson).toBe(u.title);
      }
      const titles = set.units.map((u) => u.title);
      expect(new Set(titles).size, set.id).toBe(titles.length);
    }
  });

  it("다음 단위는 만들어진 것 중에서 고른다 — 「준비 중」은 건너뛴다", () => {
    const set = getSet("moeui-2025-03-21")!;
    expect(unitsOf(set)).toHaveLength(6);
    expect(nextUnit(set, "moeui-2025-03-21-u1-words")?.title).toBe("실전 풀기");
    expect(nextUnit(set, "moeui-2025-03-21-u6-exam")).toBeNull();
  });

  it("수능 18번 세트에 퇴사 편지 7문장이 들어 있다", () => {
    const suneung = allSets().find((set) => set.id === "suneung-18");
    expect(suneung?.title).toBe("18번 문제");
    expect(suneung?.lessons).toEqual(["resignation-letter"]);
    expect(sentenceCount(suneung!)).toBe(7);
  });
});
