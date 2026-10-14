import pictureDescription from "../../content/speaking/toeic-sp-picture-01.json";
import type { SpeakingLesson } from "./types";

/** 스피킹 레슨 목록 — 시범은 사진 묘사 하나. `?speaking=<id>`로 연다 */
const SPEAKING_LESSONS = [pictureDescription] as SpeakingLesson[];

export function getSpeakingLesson(id: string | null): SpeakingLesson | null {
  return SPEAKING_LESSONS.find((l) => l.id === id) ?? null;
}
