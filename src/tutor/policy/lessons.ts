import musicResearchers from "../../../content/tutor/policy-lessons/moeui-2026-03-21-music-researchers.json";
import musicResearchersDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-21-music-researchers.json";
import namesAndDifferences from "../../../content/tutor/policy-lessons/moeui-2026-03-30-names-and-differences.json";
import namesAndDifferencesDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-30-names-and-differences.json";
import epistemicCommunities from "../../../content/tutor/policy-lessons/moeui-2026-03-39-epistemic-communities.json";
import epistemicCommunitiesDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-39-epistemic-communities.json";
// 39번 줄이기 전 그대로 (2026-10-14) — 비교용. 생성기는 archive/2026-03-39-v1/
import epistemicCommunitiesV1 from "../../../content/tutor/policy-lessons/moeui-2026-03-39-epistemic-communities-v1.json";
import epistemicCommunitiesV1Dajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-39-epistemic-communities-v1.json";
import translationStrangeness from "../../../content/tutor/policy-lessons/moeui-2026-03-24-translation-strangeness.json";
import translationStrangenessDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-24-translation-strangeness.json";
import conversationStoppers from "../../../content/tutor/policy-lessons/moeui-2026-03-36-conversation-stoppers.json";
import conversationStoppersDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-36-conversation-stoppers.json";
import profoundBuilding from "../../../content/tutor/policy-lessons/moeui-2026-03-33-profound-building.json";
import profoundBuildingDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-33-profound-building.json";
import gestureGlue from "../../../content/tutor/policy-lessons/moeui-2026-03-38-gesture-glue.json";
import gestureGlueDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-38-gesture-glue.json";
import artAndCommerce from "../../../content/tutor/policy-lessons/moeui-2026-03-31-art-and-commerce.json";
import artAndCommerceDajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-31-art-and-commerce.json";
import literaryMirror41 from "../../../content/tutor/policy-lessons/moeui-2026-03-41-literary-mirror.json";
import literaryMirror41Dajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-41-literary-mirror.json";
import literaryMirror42 from "../../../content/tutor/policy-lessons/moeui-2026-03-42-literary-mirror.json";
import literaryMirror42Dajung from "../../../content/tutor/policy-copy/dajung/moeui-2026-03-42-literary-mirror.json";
import geographyWhere from "../../../content/tutor/policy-lessons/mopyeong-2026-06-34-geography-where.json";
import geographyWhereDajung from "../../../content/tutor/policy-copy/dajung/mopyeong-2026-06-34-geography-where.json";
import chaosPendulum from "../../../content/tutor/policy-lessons/mopyeong-2026-06-37-chaos-pendulum.json";
import chaosPendulumDajung from "../../../content/tutor/policy-copy/dajung/mopyeong-2026-06-37-chaos-pendulum.json";
// 2025년 3월 21번 데카르트의 나무 — 보관(archive/2025-03-21-descartes/)에서 되살렸다. 온보딩 예시 문제 (2026-10-22 선생님: 그림으로 이해되는 지문)
import descartesTree from "../../../content/tutor/policy-lessons/moeui-2025-03-21-descartes-tree.json";
import descartesTreeDajung from "../../../content/tutor/policy-copy/dajung/moeui-2025-03-21-descartes-tree.json";
import type { PolicyCopy, PolicyLesson } from "./types";

/** 2024년 3월 고3 — 생성기(scripts/lessons/gen_moeui_2024_03_*.py)로 만든 레슨은 파일 이름으로 모은다 (레슨 순서 = 문항 번호) */
const byName = (files: Record<string, unknown>) =>
  Object.keys(files).sort((a, b) => Number(a.match(/-(\d+)-[a-z]/)?.[1]) - Number(b.match(/-(\d+)-[a-z]/)?.[1])).map((k) => files[k]);
const LESSONS_2024_03 = byName(import.meta.glob("../../../content/tutor/policy-lessons/moeui-2024-03-*.json", { eager: true, import: "default" }));
const COPY_2024_03 = byName(import.meta.glob("../../../content/tutor/policy-copy/dajung/moeui-2024-03-*.json", { eager: true, import: "default" }));
/** 2022년 3월 고3 — 같은 방식(생성기 + 파일 이름) */
/** 2026년 6월 모의평가(2027학년도) — 같은 방식. id는 예전 관행대로 학년도 */
const LESSONS_2027_06 = byName(import.meta.glob("../../../content/tutor/policy-lessons/mopyeong-2027-06-*.json", { eager: true, import: "default" }));
const COPY_2027_06 = byName(import.meta.glob("../../../content/tutor/policy-copy/dajung/mopyeong-2027-06-*.json", { eager: true, import: "default" }));
/** 2026년 9월 모의평가(2027학년도) — 같은 방식 */
const LESSONS_2027_09 = byName(import.meta.glob("../../../content/tutor/policy-lessons/mopyeong-2027-09-*.json", { eager: true, import: "default" }));
const COPY_2027_09 = byName(import.meta.glob("../../../content/tutor/policy-copy/dajung/mopyeong-2027-09-*.json", { eager: true, import: "default" }));
const LESSONS_2022_03 = byName(import.meta.glob("../../../content/tutor/policy-lessons/moeui-2022-03-*.json", { eager: true, import: "default" }));
const COPY_2022_03 = byName(import.meta.glob("../../../content/tutor/policy-copy/dajung/moeui-2022-03-*.json", { eager: true, import: "default" }));

/**
 * Teaching Policy 레슨 목록.
 *
 * 예전 레슨(`src/tutor/lessons.ts`)과 **따로** 둔다 — 모양이 다르고, 도는 엔진도
 * 다르다. 지문을 추가하면 여기에 레슨 한 줄과 대사 한 줄,
 * `content/tutor/sets.json`에 세트 하나.
 */
const POLICY_LESSONS = [musicResearchers, namesAndDifferences, epistemicCommunities, epistemicCommunitiesV1, translationStrangeness, conversationStoppers, profoundBuilding, gestureGlue, artAndCommerce, literaryMirror41, literaryMirror42, geographyWhere, chaosPendulum, descartesTree, ...LESSONS_2024_03, ...LESSONS_2022_03, ...LESSONS_2027_06, ...LESSONS_2027_09] as unknown as PolicyLesson[];

/** 캐릭터 → 레슨 → 뽑아 둔 대사. 지금 캐릭터는 다정쌤 하나다 */
const POLICY_COPY: Record<string, PolicyCopy[]> = {
  dajung: [musicResearchersDajung, namesAndDifferencesDajung, epistemicCommunitiesDajung, epistemicCommunitiesV1Dajung, translationStrangenessDajung, conversationStoppersDajung, profoundBuildingDajung, gestureGlueDajung, artAndCommerceDajung, literaryMirror41Dajung, literaryMirror42Dajung, geographyWhereDajung, chaosPendulumDajung, descartesTreeDajung, ...COPY_2024_03, ...COPY_2022_03, ...COPY_2027_06, ...COPY_2027_09] as unknown as PolicyCopy[],
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
