import data from "../../content/tutor/sets.json" with { type: "json" };
import type { Lesson, LessonSet } from "../../content/tutor/types";
import { getLesson, lessonIds } from "./lessons";

/**
 * 수업 목록.
 *
 * **세트를 추가할 때 고치는 곳은 `content/tutor/sets.json` 하나다.** 여기 코드는
 * 그걸 읽어서 레슨과 이어 주기만 한다.
 */

const SETS = (data.sets as LessonSet[]).filter((set) =>
  /*
    없는 레슨 id를 적어 두면 카드는 뜨는데 눌러도 엉뚱한 지문이 열린다
    (`getLesson`이 첫 레슨으로 폴백한다). 그런 세트는 아예 목록에서 뺀다.
  */
  set.lessons.some((id) => lessonIds().includes(id)),
);

export function allSets(): LessonSet[] {
  return SETS;
}

export function getSet(id?: string | null): LessonSet | null {
  return SETS.find((set) => set.id === id) ?? null;
}

/** 세트에 실제로 들어 있는 지문들 */
export function lessonsOf(set: LessonSet): Lesson[] {
  return set.lessons.filter((id) => lessonIds().includes(id)).map((id) => getLesson(id));
}

/** 카드에 띄우는 분량. 지문이 여럿이면 다 더한다 */
export function sentenceCount(set: LessonSet): number {
  return lessonsOf(set).reduce((n, lesson) => n + lesson.chunks.length, 0);
}

/** 이 세트를 시작하면 열리는 지문 */
export function firstLessonId(set: LessonSet): string {
  return lessonsOf(set)[0]!.id;
}

/** 지문이 속한 세트 — 수업 화면 머리글에 세트 이름을 띄우려고 */
export function setOfLesson(lessonId: string): LessonSet | null {
  return SETS.find((set) => set.lessons.includes(lessonId)) ?? null;
}
