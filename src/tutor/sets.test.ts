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

  it("모든 지문이 어느 세트에는 들어 있다 — 목록에서 못 여는 지문을 남기지 않는다", () => {
    const orphans = lessonIds().filter((id) => !setOfLesson(id));
    expect(orphans).toEqual([]);
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
