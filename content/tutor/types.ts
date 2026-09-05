/**
 * Loopin B2C — 다정쌤 tutor contracts.
 * Keep in sync with content/tutor/schema/lesson.schema.json and frame.json.
 */

export type TutorResult = "이해" | "오류후이해" | "설명제공" | "취약";

export type Diagnosis = "A" | "B" | "C" | "D" | "E";

/*
  세션 상태 타입은 여기 두지 않는다.
  **`src/tutor/engine.ts`의 `EngineState`가 실물**이고, 규격은
  `docs/tutor/ARCHITECTURE.md` §3이다. 예전에는 이 파일에도 한 벌 있어서
  세 곳(문서 2 + 코드 1)이 서로 다른 이름을 썼다 (`chunkIndex` vs `unitIndex`).
*/

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

/**
 * 이 문장에서 학생이 스스로 내야 하는 것 하나. **체크리스트 한 줄**이다.
 *
 * 배열 순서가 곧 **쉬운 순**이다. 아직 못 한 것 중 첫 번째를 유도한다.
 * (나중에 학생 데이터가 쌓이면 첫 시도 체크율로 이 순서를 덮어쓸 수 있다.)
 */
export type ScoringPoint = {
  id: number;
  text: string;
  /** 학생 답에 이 말이 하나라도 있으면 체크 */
  check?: string[];
  /** 아직 못 한 항목을 유도하는 말. 답을 주지 않는다 */
  nudge?: string;
  /** 같은 항목에서 또 막혔을 때 **그 항목만** 알려 준다 */
  tell?: string;
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
  /**
   * 이 말이 같이 있으면 그 오류가 아니다.
   * (예: '봉사'가 있어도 '근무'가 같이 있으면 serve 오해가 아니다)
   */
  not_signals?: string[];
  treatment?: TreatmentRound;
  rounds?: TreatmentRound[];
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
  /** 정답일 때 하는 구체적 칭찬. 없으면 프레임의 기본 칭찬 */
  praise?: string;
  scoring_points: ScoringPoint[];
  error_priority?: string[];
  expected_errors?: ExpectedError[];
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
