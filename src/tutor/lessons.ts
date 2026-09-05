import resignation from "../../content/tutor/lessons/resignation-letter.json";
import thales from "../../content/tutor/lessons/thales-participial-phrase-front.json";
import type { Lesson } from "../../content/tutor/types";

/**
 * 레슨 목록.
 *
 * **지문을 추가할 때 고치는 유일한 코드**다 — 한 줄 import + 배열에 넣기.
 * 문장·칭찬·힌트·오류 대사는 전부 JSON 안에 있다.
 */
const LESSONS = [resignation, thales] as unknown as Lesson[];

export const DEFAULT_LESSON_ID = LESSONS[0]!.id;

export function getLesson(id?: string | null): Lesson {
  if (!id) return LESSONS[0]!;
  return LESSONS.find((lesson) => lesson.id === id) ?? LESSONS[0]!;
}

export function lessonIds(): string[] {
  return LESSONS.map((lesson) => lesson.id);
}
