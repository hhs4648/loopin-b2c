import { describe, expect, it } from "vitest";
import data from "../../content/tutor/sets.json";
import type { LessonSet } from "../../content/tutor/types";
import { getLesson, lessonIds } from "./lessons";
import { allSets, firstLessonId, sentenceCount, setOfLesson } from "./sets";

const RAW = data.sets as LessonSet[];

/**
 * 세트는 **학생이 고르는 단위**다. 여기가 어긋나면 목록에 카드가 안 뜨거나,
 * 눌렀을 때 엉뚱한 지문이 열린다 — 둘 다 화면을 봐야만 알 수 있는 종류의 버그다.
 */
describe("수업 세트", () => {
  it("적어 둔 레슨 id가 실제로 있다", () => {
    const missing = RAW.flatMap((set) =>
      set.lessons.filter((id) => !lessonIds().includes(id)).map((id) => `${set.id}: ${id}`),
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
    const orphans = lessonIds().filter((id) => !setOfLesson(id) && !allowedUnlisted.has(id));
    expect(orphans).toEqual([]);
  });

  it("수업 목록 순서", () => {
    expect(allSets().map((set) => set.id)).toEqual([
      "suneung-18",
      "suneung-19",
      "suneung-20",
      "suneung-21",
      "suneung-22",
      "suneung-23",
      "suneung-24",
      "suneung-26",
      "suneung-27",
      "suneung-28",
      "suneung-29",
      "suneung-30",
      "suneung-31",
      "suneung-32",
      "suneung-33",
      "suneung-34",
      "suneung-35",
      "suneung-36",
      "suneung-37",
      "suneung-38",
      "suneung-39",
      "suneung-40",
      "suneung-41-1",
      "suneung-41-2",
      "suneung-43-1",
      "suneung-43-2",
    ]);
  });

  it("카드에 띄우는 문장 수가 실제 지문과 같다", () => {
    for (const set of allSets()) {
      const real = set.lessons.reduce((n, id) => n + getLesson(id).chunks.length, 0);
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
    expect(suneung?.title).toBe("수능 18번 문제");
    expect(suneung?.lessons).toEqual(["resignation-letter"]);
    expect(sentenceCount(suneung!)).toBe(7);
  });
});
