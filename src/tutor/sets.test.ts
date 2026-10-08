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


  it("목록은 2026년 3월 모의고사 — 21번, 30번, 39번 (2026-10-05에 새로 시작)", () => {
    expect(allGroups().map((g) => g.id)).toEqual(["moeui"]);
    expect(allCollections().map((c) => c.id)).toEqual(["moeui-2026-03"]);
    expect(setsIn("moeui-2026-03").map((s) => s.id)).toEqual(["moeui-2026-03-21", "moeui-2026-03-30", "moeui-2026-03-39"]);
    expect(getCollection("moeui-2026-03")?.title).toBe("2026년 3월 모의고사");
  });
});
