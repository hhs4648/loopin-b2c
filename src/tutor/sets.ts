import data from "../../content/tutor/sets.json" with { type: "json" };
import type {
  LessonCollection,
  LessonGroup,
  LessonSet,
} from "../../content/tutor/types";
import { getPolicyLesson, policyLessonIds } from "./policy/lessons";

/**
 * 수업 목록 — **대분류 → 중분류 → 세트** 세 켜다.
 *
 *     수능 (대분류)
 *       └ 2024 수능 (중분류)
 *           ├ 18번 문제
 *           └ 19번 문제 …
 *
 * 목록을 바꿀 때 고치는 곳은 `content/tutor/sets.json` 하나다. 여기 코드는
 * 그걸 읽어서 레슨과 이어 주기만 한다.
 */

const GROUPS = data.groups as LessonGroup[];

/**
 * 목록에 올릴 수 있는 지문 전부 — 예전 레슨과 Teaching Policy 레슨.
 * 모양과 엔진은 달라도 학생이 고르는 자리는 같다.
 */
export function knownLessonIds(): string[] {
  return policyLessonIds();
}

/** 지문 하나의 문장 수 — 어느 쪽 레슨이든 */
export function sentencesIn(lessonId: string): number {
  return getPolicyLesson(lessonId)?.sentences.length ?? 0;
}

const SETS = (data.sets as LessonSet[]).filter((set) =>
  /*
    없는 레슨 id를 적어 두면 카드는 뜨는데 눌러도 엉뚱한 지문이 열린다
    (`getLesson`이 첫 레슨으로 폴백한다). 그런 세트는 아예 목록에서 뺀다.
  */
  set.lessons.some((id) => knownLessonIds().includes(id)),
);

export function allGroups(): LessonGroup[] {
  return GROUPS;
}

/** 중분류 전체 — 대분류 순서 그대로 펼친 것 */
export function allCollections(): LessonCollection[] {
  return GROUPS.flatMap((group) => group.collections);
}

export function getCollection(id?: string | null): LessonCollection | null {
  return allCollections().find((c) => c.id === id) ?? null;
}

/** 이 중분류에 든 세트들. 목록에 뜨는 순서다 */
export function setsIn(collectionId: string): LessonSet[] {
  return SETS.filter((set) => set.collection === collectionId);
}

export function allSets(): LessonSet[] {
  return SETS;
}

export function getSet(id?: string | null): LessonSet | null {
  return SETS.find((set) => set.id === id) ?? null;
}

/** 세트에 실제로 들어 있는 지문 id들 */
function lessonIdsOf(set: LessonSet): string[] {
  return set.lessons.filter((id) => knownLessonIds().includes(id));
}

/** 카드에 띄우는 분량. 지문이 여럿이면 다 더한다 */
export function sentenceCount(set: LessonSet): number {
  return lessonIdsOf(set).reduce((n, id) => n + sentencesIn(id), 0);
}

/** 이 세트를 시작하면 열리는 지문 */
export function firstLessonId(set: LessonSet): string {
  return lessonIdsOf(set)[0]!;
}

/** 지문이 속한 세트 — 수업 화면 머리글에 이름을 띄우려고 */
export function setOfLesson(lessonId: string): LessonSet | null {
  return SETS.find((set) => set.lessons.includes(lessonId)) ?? null;
}
