import { skillOf, type StudentState } from "./student-state";
import type {
  ChoiceStep,
  ItemProperty,
  LearningContext,
  Observation,
  PolicySentence,
  PolicyStep,
  TeachingAction,
  TeachingActionName,
} from "./types";

/**
 * Teaching Policy Engine (명세 §3, §22).
 *
 *     TeachingDecision = f(StudentState, LearningContext, ItemProperty, Observation)
 *
 * **여기에는 대사가 없다.** 무엇을·언제·어느 깊이로만 정해 `TeachingAction`을 낸다.
 * 상태를 고치지도 않는다 — 순수 함수라서 표로 테스트할 수 있다.
 */

/** 지금 풀고 있는 choice 스텝의 진행 — 세션이 들고 있다 */
export type ChoiceProgress = {
  /** 지금까지 받은 도움의 단수. 0 = 아직 혼자 */
  rung: number;
  wrongPicks: string[];
};

export type DecideInput = {
  student: StudentState;
  context: LearningContext;
  item: ItemProperty;
  sentence: PolicySentence;
};

const ASK_ACTION: Record<ChoiceStep["interaction"], TeachingActionName> = {
  meaning_choice: "ASK_MEANING_CHOICE",
  translation_choice: "ASK_TRANSLATION_CHOICE",
  structure_choice: "ASK_STRUCTURE",
  visual_mapping: "SHOW_VISUAL_MAPPING",
  prediction: "ASK_PREDICTION",
};

/** 스텝을 **여는** 행동 */
export function openingAction(step: PolicyStep, input: DecideInput): TeachingAction {
  const value = input.sentence.teaching_value;
  if (step.type === "choice") {
    return {
      action: ASK_ACTION[step.interaction],
      interactionId: step.id,
      target: step.skill,
      ...(step.retrieve ? { reason: ["retrieve_previous_representation"] } : {}),
    };
  }
  if (step.type === "think") {
    return {
      action: step.interaction === "prediction" ? "ASK_PREDICTION" : "ASK_CONTRAST",
      interactionId: step.id,
      target: step.skill,
    };
  }
  switch (step.interaction) {
    case "structure_highlight":
      return {
        action: "SHOW_STRUCTURE",
        interactionId: step.id,
        target: step.skill,
        intensity: "brief",
        reason: [
          ...(value === "high" ? ["high_teaching_value"] : []),
          "multiple_choice_can_be_guessed",
        ],
      };
    case "retrieve":
      return { action: "RETRIEVE_PREVIOUS_REPRESENTATION", interactionId: step.id };
    case "bridge":
      return { action: "ASK_BRIDGE", interactionId: step.id };
    case "note":
      return { action: "SHOW_NOTE", interactionId: step.id, intensity: "brief", target: step.skill };
    case "read_and_continue":
      return { action: "CONTINUE", interactionId: step.id };
  }
}

/**
 * 이 스텝을 **보여 줄 것인가** (§8 관찰 ≠ 개입, §6 정답이어도 가치가 높으면 짧게).
 *
 * `struggled` — 이 문장의 질문에서 틀렸거나 도움을 받았나.
 */
export function shouldShow(
  step: PolicyStep,
  input: DecideInput,
  struggled: boolean,
): boolean {
  const when = step.when ?? "always";
  // 「필요하면」 주는 도움 — 막혔던 학생, 그리고 하위권이라고 알려진 학생에게
  if (when === "if_struggled") return struggled || input.context.student_level === "low";
  if (when === "unless_stable") {
    // 찍어서 맞힐 수 있으므로 한 번 맞힌 걸로는 건너뛰지 않는다.
    // 거듭 혼자 맞혀 온 skill이고, 이번에도 혼자 맞혔을 때만 설명을 접는다.
    const stable = step.skill ? skillOf(input.student, step.skill).status === "stable" : false;
    return !(stable && !struggled);
  }
  // 시간이 없는 날에는 곁가지(맥락 메모·다리 질문)를 접는다. 핵심 문장은 남긴다
  if (
    step.type === "show" &&
    (step.interaction === "note" || step.interaction === "bridge") &&
    input.context.time_budget === "short" &&
    input.sentence.teaching_value !== "high"
  ) {
    return false;
  }
  return true;
}

/**
 * choice 스텝에서 관찰 하나를 받고 다음 행동을 고른다 (§10 사다리).
 *
 *   혼자 시도 → 가벼운 힌트 → 센 힌트 → 설명
 *
 * 「모르겠어요」를 바로 눌러도 설명이 아니라 **힌트가 먼저**다.
 */
export function decideOnChoice(
  step: ChoiceStep,
  progress: ChoiceProgress,
  observation: Extract<Observation, { kind: "answer" | "dont_know" }>,
  input: DecideInput,
): TeachingAction {
  const base = { interactionId: step.id, target: step.skill };

  if (observation.kind === "answer" && observation.correct) {
    return { ...base, action: "PRAISE" };
  }

  const wrongNow = observation.kind === "answer" ? 1 : 0;
  const remaining = step.options.length - progress.wrongPicks.length - wrongNow;
  // 보기가 하나만 남으면 그건 더 이상 질문이 아니다 — 설명으로 간다
  if (remaining <= 1 || progress.rung >= 2) {
    return { ...base, action: "EXPLAIN", intensity: "normal", reason: ["support_ladder_exhausted"] };
  }

  if (progress.rung === 0) {
    // §4 — 아는 개념에서 뜻밖에 틀렸다면 설명보다 스스로 고칠 기회가 먼저다
    const stable = step.skill ? skillOf(input.student, step.skill).status === "stable" : false;
    if (stable && observation.kind === "answer") {
      return {
        ...base,
        action: "GIVE_SELF_CORRECTION_OPPORTUNITY",
        reason: ["knowledge_stable", "unexpected_error"],
      };
    }
    return { ...base, action: "GIVE_LIGHT_HINT", intensity: "minimal" };
  }
  return { ...base, action: "GIVE_STRONG_HINT", intensity: "brief" };
}
