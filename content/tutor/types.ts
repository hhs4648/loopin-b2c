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

/** 문장 학습에서 단어를 눌렀을 때 보여줄, 이 문맥의 짧은 뜻 */
export type WordGloss = {
  en: string;
  ko: string;
};

export type LessonChunk = {
  id: number;
  text: string;
  model_translation: string;
  /** 정답일 때 하는 구체적 칭찬. 없으면 프레임의 기본 칭찬 */
  praise?: string;
  /**
   * 단어/구 → 한국어 뜻. 문장 전체 해석이 아니다.
   * 긴 구가 있으면 그 구를 통째로 누른다.
   */
  glosses?: WordGloss[];
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
  chunks: LessonChunk[];
};

/**
 * 수업 세트 — **학생이 한 번에 앉는 분량**이자 목록에 뜨는 카드 하나.
 *
 * 레슨(지문)과 따로 두는 이유는 셈이 다르기 때문이다. 「수능 18번 문제」는
 * 학생이 고르는 단위이고, 레슨은 그 안에 들어가는 지문이다. 지금은 세트마다
 * 지문이 하나지만, 같은 유형의 지문을 여러 개 묶는 게 원래 목적이다.
 */
export type LessonSet = {
  id: string;
  /** 어느 중분류에 들어가는지 (`LessonCollection.id`) */
  collection: string;
  title: string;
  subtitle: string;
  /** `lessons.ts`의 레슨 id. 순서대로 푼다 */
  lessons: string[];
  /**
   * 한 문제를 **작은 학습 단위**로 쪼갠 것 (단어 → 핵심 문장 → … → 실전 풀기).
   * 있으면 세트를 눌렀을 때 수업이 바로 열리지 않고 단위 목록이 먼저 나온다.
   * `lessons`에는 이 중 만들어진 단위의 레슨만, 같은 순서로 적는다.
   */
  units?: LessonUnit[];
};

/** `lesson`이 없으면 아직 안 만든 단위다 — 목록에 「준비 중」으로 뜬다 */
export type LessonUnit = {
  title: string;
  subtitle: string;
  lesson?: string;
};

/**
 * 중분류 — **한 시험지 한 벌.** 「2024 수능」 안에 18~45번이 들어간다.
 *
 * 세트를 여기에 담지 않고 세트가 `collection` id로 붙는다. 그래야 지문을
 * 추가할 때 고칠 곳이 한 줄이다.
 */
export type LessonCollection = {
  id: string;
  title: string;
  subtitle: string;
  /** 카드 왼쪽 위 라벨 (기출 · 모의 …) */
  tag: string;
};

/** 대분류 — 수능 · 모의고사 · 교과서처럼 가장 큰 갈래 */
export type LessonGroup = {
  id: string;
  title: string;
  subtitle: string;
  collections: LessonCollection[];
};
