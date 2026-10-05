import descartesTree from "../../../content/tutor/policy-lessons/moeui-2025-03-21-descartes-tree.json";
import u1Words from "../../../content/tutor/policy-lessons/moeui-2025-03-21-u1-words.json";
import u6Exam from "../../../content/tutor/policy-lessons/moeui-2025-03-21-u6-exam.json";
import descartesTreeDajung from "../../../content/tutor/policy-copy/dajung/moeui-2025-03-21-descartes-tree.json";
import u1WordsDajung from "../../../content/tutor/policy-copy/dajung/moeui-2025-03-21-u1-words.json";
import u6ExamDajung from "../../../content/tutor/policy-copy/dajung/moeui-2025-03-21-u6-exam.json";
import type { PolicyCopy, PolicyLesson } from "./types";

/**
 * Teaching Policy 레슨 목록.
 *
 * 예전 레슨(`src/tutor/lessons.ts`)과 **따로** 둔다 — 모양이 다르고, 도는 엔진도
 * 다르다. 지문을 추가하면 여기에 레슨 한 줄과 대사 한 줄,
 * `content/tutor/sets.json`에 세트 하나.
 *
 * 21번은 한 문제를 **작은 단위**(u1 단어 … u6 실전 풀기)로 쪼개 다시 만드는 중이다.
 * 통째로 된 예전 21번(`descartesTree`)은 목록에서 내렸고, 엔진 회귀용으로 남겨 둔다.
 */
const POLICY_LESSONS = [descartesTree, u1Words, u6Exam] as unknown as PolicyLesson[];

/** 캐릭터 → 레슨 → 뽑아 둔 대사. 지금 캐릭터는 다정쌤 하나다 */
const POLICY_COPY: Record<string, PolicyCopy[]> = {
  dajung: [descartesTreeDajung, u1WordsDajung, u6ExamDajung] as unknown as PolicyCopy[],
};

export function getPolicyCopy(lessonId: string, character = "dajung"): PolicyCopy | null {
  return POLICY_COPY[character]?.find((copy) => copy.lesson === lessonId) ?? null;
}

export function policyLessonIds(): string[] {
  return POLICY_LESSONS.map((lesson) => lesson.id);
}

export function isPolicyLesson(id?: string | null): boolean {
  return !!id && policyLessonIds().includes(id);
}

export function getPolicyLesson(id: string): PolicyLesson | null {
  return POLICY_LESSONS.find((lesson) => lesson.id === id) ?? null;
}

export function allPolicyLessons(): PolicyLesson[] {
  return POLICY_LESSONS;
}
