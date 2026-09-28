import type { ChoiceCopy, PolicyCopy, PolicyLesson, PolicyStep, ShowCopy, ThinkCopy } from "./types";

/**
 * 뽑아 둔 대사를 꺼낸다.
 *
 * **수업 중에는 모델을 부르지 않는다.** 대사는 `scripts/policy_copy.mjs`로 미리 뽑아
 * `content/tutor/policy-copy/<캐릭터>/<레슨>.json`에 둔 것이고, 여기서는 읽기만 한다.
 * 캐릭터를 바꾸는 건 다른 폴더의 파일을 읽는 일이다 — 레슨(가르치는 내용)은 그대로다.
 */

/** `scripts/policy_copy.mjs`의 `stampOf`와 같은 계산이어야 한다 */
export function stampOf(value: unknown): string {
  const text = JSON.stringify(value);
  let h = 5381;
  for (let i = 0; i < text.length; i++) h = ((h * 33) ^ text.charCodeAt(i)) >>> 0;
  return h.toString(36);
}

/** 이 스텝의 대사가 무엇에서 뽑혔는지 — brief와 보기가 바뀌면 다시 뽑아야 한다 */
export function stepSource(step: PolicyStep) {
  return {
    brief: step.brief,
    options: (step.type === "choice" ? step.options : []).map((o) => [o.id, o.label, !!o.correct]),
  };
}

/** [자리, 지금 brief의 도장, 대사에 찍힌 도장] — 둘이 다르면 대사가 낡은 것이다 */
export function stamps(lesson: PolicyLesson, copy: PolicyCopy): [string, string, string | undefined][] {
  const out: [string, string, string | undefined][] = [["lesson", stampOf(lesson.brief), copy.from]];
  if (lesson.exam) out.push(["exam", stampOf(lesson.exam.brief), copy.exam?.from]);
  if (lesson.intro) out.push(["intro", stampOf(lesson.intro), copy.intro?.from as string | undefined]);
  for (const sentence of lesson.sentences) {
    for (const help of sentence.helps ?? []) {
      out.push([`helps.${help.id}`, stampOf(help.brief), copy.helps[help.id]?.from]);
    }
    for (const step of sentence.steps) {
      out.push([`steps.${step.id}`, stampOf(stepSource(step)), copy.steps[step.id]?.from]);
    }
  }
  return out;
}

export function choiceCopy(copy: PolicyCopy, id: string): ChoiceCopy {
  return copy.steps[id] as ChoiceCopy;
}
export function thinkCopy(copy: PolicyCopy, id: string): ThinkCopy {
  return copy.steps[id] as ThinkCopy;
}
export function showCopy(copy: PolicyCopy, id: string): ShowCopy {
  return copy.steps[id] as ShowCopy;
}
