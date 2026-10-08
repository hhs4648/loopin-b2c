import musicResearchers from "../../../content/tutor/policy-lessons/moeui-2026-03-21-music-researchers.json";
import musicResearchersDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-21-music-researchers.json";
import namesAndDifferences from "../../../content/tutor/policy-lessons/moeui-2026-03-30-names-and-differences.json";
import namesAndDifferencesDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-30-names-and-differences.json";
import epistemicCommunities from "../../../content/tutor/policy-lessons/moeui-2026-03-39-epistemic-communities.json";
import epistemicCommunitiesDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-39-epistemic-communities.json";
import type { PolicyCopy, PolicyLesson } from "./types";

/**
 * Teaching Policy 레슨 목록.
 *
 * 예전 레슨(`src/tutor/lessons.ts`)과 **따로** 둔다 — 모양이 다르고, 도는 엔진도
 * 다르다. 지문을 추가하면 여기에 레슨 한 줄과 대사 한 줄,
 * `content/tutor/sets.json`에 세트 하나.
 */
const POLICY_LESSONS = [musicResearchers, namesAndDifferences, epistemicCommunities] as unknown as PolicyLesson[];

/** 캐릭터 → 레슨 → 뽑아 둔 대사. 지금 캐릭터는 다정쌤 하나다 */
const POLICY_COPY: Record<string, PolicyCopy[]> = {
  dajung: [musicResearchersDajung, namesAndDifferencesDajung, epistemicCommunitiesDajung] as unknown as PolicyCopy[],
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
