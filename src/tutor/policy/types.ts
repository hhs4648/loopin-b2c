import type { ProperNoun, WordGloss } from "../../../content/tutor/types";

/**
 * Teaching Policy v0.1 — 타입.
 *
 * 명세: `docs/tutor/policy/Loopin_Teaching_Policy_Spec_v0.1.md`.
 * 예전 해석 엔진(`src/tutor/engine.ts`)과 **나란히** 선다. 예전 레슨은 그대로
 * 예전 엔진이 돌리고, `content/tutor/policy-lessons/*.json`만 여기로 온다.
 *
 * 나눔은 명세 §2 그대로다.
 *   - 정책(`decide.ts`)은 **무엇을·언제·어느 깊이로**만 정해 `TeachingAction`을 낸다.
 *   - 레슨 JSON에는 **가르치는 내용**만 있다 (`brief` — 말투 없는 메모).
 *   - 대사는 그 brief에서 캐릭터 말투로 **미리 뽑아 둔** JSON이다
 *     (`content/tutor/policy-copy/<캐릭터>/`, `scripts/policy_copy.mjs`). LLM은 뽑을 때만
 *     쓰고, 수업 중에는 부르지 않는다.
 *   - 세션(`session.ts`)이 행동에 맞는 대사를 골라 기존 화면(`TutorView`)에 싣는다.
 */

export type Level3 = "low" | "medium" | "high";

/** 명세 §5 */
export type LearningContext = {
  mode:
    | "first_attempt"
    | "paper_review"
    | "regular_learning"
    | "exam_review"
    | "weakness_review"
    | "spaced_review";
  exam_relevance: Level3;
  student_level?: "low" | "mid" | "high";
  time_budget: "short" | "normal" | "deep";
};

/** 명세 §6 */
export type ItemProperty = {
  english_difficulty: Level3;
  conceptual_difficulty: Level3;
  background_knowledge_required: Level3;
  exam_importance: Level3;
  teaching_value: Level3;
  intervention_density: "minimal" | "normal" | "deep";
};

/** 명세 §9 — 모를 법한 단어라고 다 가르치는 단어가 아니다 */
export type VocabularySupport = "lookup_only" | "teaching_target" | "concept_support";

/* ── 화면에 같이 띄우는 그림 (문장 아래 패널) ───────────────────────── */

export type StructurePanel = {
  kind: "structure";
  /** `ko`가 있으면 영어 아래에 작은 글씨로 뜻을 단다 */
  rows: { label: string; text: string; ko?: string }[];
};

/** 한 줄 정리 카드 */
export type NotePanel = {
  kind: "note";
  label: string;
  text: string;
};

/** `right`가 null이면 아직 안 채운 칸이다 (`?`로 보인다) */
export type MappingPanel = {
  kind: "mapping";
  title?: string;
  rows: { left: string; right: string | null; note?: string }[];
};

export type ContrastPanel = {
  kind: "contrast";
  left: { title: string; text: string };
  right: { title: string; text: string };
};

export type StudyPanel = StructurePanel | MappingPanel | ContrastPanel | NotePanel;
export type PanelRef = StudyPanel | string;

/* ── 스텝 ─────────────────────────────────────────────────────────── */

/**
 * 스텝을 **보여 줄지**는 정책이 정한다 (`decide.ts`).
 *
 * - `always` — 기본
 * - `unless_stable` — 그 skill이 stable이고 이 문장의 질문을 혼자 맞혔으면 건너뛴다
 *   (§6 "이미 충분히 이해한 학생에게 장황한 설명을 반복하지 않는다")
 * - `if_struggled` — 이 문장의 질문에서 틀렸거나 힌트를 썼을 때만 (§18 "필요하면")
 */
export type StepWhen = "always" | "unless_stable" | "if_struggled";

type StepBase = {
  id: string;
  when?: StepWhen;
  /** 이 스텝이 건드리는 skill. 상태 갱신과 `unless_stable` 판단에 쓴다 */
  skill?: string;
  /** 점진 공개(§13) — 이 스텝 동안 문장을 이렇게 보여 준다. 없으면 원문 */
  display?: string;
  /** 문장 안에서 강조할 구절 */
  highlight?: string[];
  /** 그림 자체이거나, 레슨 `panels`에 적어 둔 이름 */
  panel?: PanelRef;
  /** 앞 문장에서 만든 표상을 다시 꺼내 쓰는 스텝인가 (§15) */
  retrieve?: boolean;
};

export type ChoiceOption = {
  id: string;
  label: string;
  correct?: boolean;
};

/** meaning_choice / translation_choice / structure_choice(주어 범위 등) / visual_mapping의 한 칸 / prediction */
export type ChoiceStep = StepBase & {
  type: "choice";
  interaction:
    | "meaning_choice"
    | "translation_choice"
    | "structure_choice"
    | "visual_mapping"
    | "prediction";
  options: ChoiceOption[];
  /** 무엇을 말할지 (말투 없음). 대사는 여기서 뽑는다 */
  brief: ChoiceCopy;
  /** 맞힌 뒤 패널을 이렇게 바꿔 보여 준다 (대응표의 칸이 채워진다) */
  panel_after?: PanelRef;
};

/** contrast_reasoning 등 — 채점하지 않는다. 생각할 틈을 주고, 그다음 정리한다 */
export type ThinkStep = StepBase & {
  type: "think";
  interaction: "contrast_reasoning" | "clickable_question" | "prediction";
  brief: ThinkCopy;
  panel_after?: PanelRef;
};

/** 보여 주고 기다린다 — 구조 분석, 맥락 의미, 이전 표상 회상, 다음 문장 다리 */
export type ShowStep = StepBase & {
  type: "show";
  interaction:
    | "structure_highlight"
    | "note"
    | "retrieve"
    | "bridge"
    | "read_and_continue";
  brief: ShowCopy;
  /** 누르면 넘어가는 버튼 — 학생의 말이라 캐릭터 말투와 상관없다. 없으면 「다음으로」 */
  button?: string;
};

export type PolicyStep = ChoiceStep | ThinkStep | ShowStep;

/*
  ── 대사 ──────────────────────────────────────────────────────────────
  레슨의 `brief`와 뽑아 둔 대사는 **같은 모양**이다. brief는 「무엇을 말할지」,
  대사는 그걸 캐릭터가 말한 것.
*/

export type ChoiceCopy = {
  ask: string;
  /** 도움말을 본 뒤 질문으로 돌아올 때 붙이는 짧은 한마디 */
  reask?: string;
  /** [가벼운 힌트, 더 센 힌트] — §10 */
  hints: [string, string];
  /** 정답 공개 + 설명. 사다리 끝 */
  explain: string;
  praise: string;
  /** 오답 보기 id → 그 오개념을 겨냥한 첫 힌트. 없으면 `hints[0]` */
  feedback?: Record<string, string>;
};

export type ThinkCopy = {
  ask: string;
  reask?: string;
  hint: string;
  /** 학생이 생각한 뒤에 주는 정리 */
  summary: string;
};

export type ShowCopy = { say: string };

/** 뽑은 대사에는 도장이 붙는다 — 어느 brief에서 뽑았는지 (brief의 해시) */
type Stamped<T> = T & { from?: string };

export type PolicyCopy = {
  lesson: string;
  character: string;
  from?: string;
  /** 「오늘은 {topic_intro} 볼 거예요.」에 들어갈 구절 */
  topic_intro: string;
  closing: string;
  helps: Record<string, Stamped<{ answer: string }>>;
  steps: Record<string, Stamped<Partial<ChoiceCopy & ThinkCopy & ShowCopy>>>;
};

/** 눌러야 열리는 배경 설명 (§18 optional_help). 지문 이해에 필요한 만큼만 */
export type OptionalHelp = {
  id: string;
  /** 칩에 적는 말 — 학생의 말이다 */
  label: string;
  brief: string;
};

export type PolicySentence = {
  id: number;
  text: string;
  model_translation: string;
  teaching_value: Level3;
  /** 문장 내내 색으로 눈에 띄게 할 단어 — 누르면 뜻이 나온다. 스텝의 `highlight`와 다르다 */
  emphasis?: string[];
  glosses: WordGloss[];
  vocabulary?: Record<string, VocabularySupport>;
  helps?: OptionalHelp[];
  steps: PolicyStep[];
};

export type PolicyLesson = {
  id: string;
  kind: "policy";
  version: string;
  source: string;
  brief: { topic: string; closing: string };
  context: LearningContext;
  item: ItemProperty;
  proper_nouns?: ProperNoun[];
  /** 여러 스텝이 같이 쓰는 그림. 스텝에서는 이름으로 부른다 */
  panels?: Record<string, StudyPanel>;
  sentences: PolicySentence[];
};

/* ── 관찰 · 행동 ──────────────────────────────────────────────────── */

/** 명세 §7 — **앱이 실제로 본 것만.** 속마음은 여기 없다 */
export type Observation =
  | { kind: "start" }
  | { kind: "answer"; correct: boolean; optionId: string; latencyMs: number }
  | { kind: "dont_know"; latencyMs: number }
  | { kind: "thought"; latencyMs: number }
  | { kind: "continue" };

/** 화면에서 바로 올라오는 관찰 — 턴을 만들지 않는다 */
export type UiObservation = { kind: "vocab_click"; word: string };

/** 명세 §21 */
export type TeachingActionName =
  | "CONTINUE"
  | "ALLOW_LOOKUP"
  | "ASK_MEANING_CHOICE"
  | "ASK_TRANSLATION_CHOICE"
  | "ASK_STRUCTURE"
  | "SHOW_STRUCTURE"
  | "SHOW_VISUAL_MAPPING"
  | "ASK_PREDICTION"
  | "ASK_CONTRAST"
  | "GIVE_SELF_CORRECTION_OPPORTUNITY"
  | "GIVE_LIGHT_HINT"
  | "GIVE_STRONG_HINT"
  | "EXPLAIN"
  | "SUMMARIZE"
  | "SHOW_NOTE"
  | "ASK_BRIDGE"
  | "PRAISE"
  | "RETRIEVE_PREVIOUS_REPRESENTATION"
  | "FINISH";

export type TeachingAction = {
  action: TeachingActionName;
  target?: string;
  intensity?: "minimal" | "brief" | "normal" | "deep";
  interactionId?: string;
  reason?: string[];
};

/** 한 문제(choice 스텝)가 어떻게 끝났나 — §11 힌트로 맞힌 건 혼자 맞힌 게 아니다 */
export type PerformanceStatus =
  | "independent_success"
  | "hint_assisted_success"
  | "explained";
