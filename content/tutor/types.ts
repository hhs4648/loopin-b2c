/**
 * Loopin B2C — 다정쌤 tutor contracts.
 * Keep in sync with content/tutor/schema/lesson.schema.json and frame.json.
 */

export type TutorResult = "이해" | "오류후이해" | "설명제공" | "취약";

export type SessionStage = "intro" | "chunk" | "wrap_up" | "done";

export type Diagnosis = "A" | "B" | "C" | "D" | "E";

export type SessionState = {
  lessonId: string;
  stage: SessionStage;
  chunkIndex: number;
  hintRung: 0 | 1 | 2 | 3;
  missCountInChunk: number;
  skipFinalRetake: boolean;
  hadAnyError: boolean;
  properNounTipTold: boolean;
  lastTutorUtterance: string;
  taughtPointIndex: number;
  pendingBranch: string | null;
  errorIds: string[];
  result: TutorResult | null;
};

export type TutorUiOutput = {
  message: string;
  buttons: string[];
  effect: null | "light";
};

export type ProperNoun = {
  en: string;
  ko: string;
  type?: string;
};

export type ScoringPoint = {
  id: number;
  text: string;
};

export type Choice = {
  id: string;
  label: string;
  correct?: boolean;
};

export type Branch = {
  message: string;
  reveal_answer?: boolean;
  next?: string;
};

export type TreatmentRound = {
  round?: number;
  style?: string;
  forbid?: string[];
  message?: string;
  choices?: Choice[];
  on_choice?: Record<string, Branch>;
  on_why_question?: Branch;
  next?: string;
};

export type ExpectedError = {
  id: string;
  detect: string;
  never_mark_correct?: boolean;
  signals?: string[];
  treatment?: TreatmentRound;
  rounds?: TreatmentRound[];
};

export type HintRung = {
  rung: 1 | 2 | 3;
  message: string;
};

export type AnticipatedResponse = {
  when: string;
  match: string[];
  do_not_repeat_question?: boolean;
  message: string;
  next?: string;
};

export type TeachPoint = {
  id: number;
  label: string;
  message: string;
  enrichment?: string;
};

export type LessonChunk = {
  id: number;
  text: string;
  model_translation: string;
  scoring_points: ScoringPoint[];
  error_priority?: string[];
  expected_errors?: ExpectedError[];
  hint_ladder?: HintRung[];
  anticipated_responses?: AnticipatedResponse[];
  anticipated_questions?: string[];
  teach_points?: TeachPoint[];
};

export type Lesson = {
  id: string;
  version: string;
  updated?: string;
  authors?: { content?: string; prompt?: string };
  category: string;
  topic_intro: string;
  sentence: string;
  grammar_type: string;
  split_rule: {
    when: string;
    how: string;
    labels: string[];
  };
  proper_nouns: ProperNoun[];
  proper_noun_tip?: {
    tell_once_on_first_appearance: boolean;
    message: string;
  };
  chunks: LessonChunk[];
};
