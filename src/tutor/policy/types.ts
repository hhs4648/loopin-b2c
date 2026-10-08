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
  /** `ko`가 있으면 영어 아래에 작은 글씨로 뜻을 단다. `tone`은 문장 강조색(노랑 hl · 민트 hl2)과 맞춘다 */
  rows: { label: string; text: string; ko?: string; tone?: "hl" | "hl2" }[];
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
  title?: string;
  /** 두 칸 사이 기호 (예: ↔ 반대 관계). 없으면 점선만 */
  between?: string;
  left: { title: string; text: string };
  right: { title: string; text: string };
};

/**
 * 단어 지도 — 문장을 따라가며 핵심 단어와 관계(=, ≠, →, ↔)를 한 줄씩 쌓는다.
 * `fresh`는 이번 문장에서 새로 붙은 줄, `quote`는 따옴표 친 말 줄(같은 색으로 잇는다).
 */
export type MapPanel = {
  kind: "map";
  title?: string;
  rows: { text: string; fresh?: boolean; quote?: boolean }[];
};

/**
 * 칠판 위 두 그룹 — 서로 다른 단어 무리를 한눈에. 문장을 지날 때마다 단어가 쌓인다.
 * `fresh`는 이번 문장에서 새로 붙은 단어, `quote`는 따옴표 친 말.
 */
export type BoardGroup = {
  label: string;
  /**
   * 같은 뜻으로 쓰인 단어 묶음 — 그룹 안의 작은 원으로 그린다 (`note`는 원 아래 한 줄).
   * `arrow`를 주면 묶음과 `words` 사이에 그 화살표를 그린다
   */
  cluster?: { words: string[]; note?: string; fresh?: boolean };
  arrow?: string;
  words: { text: string; fresh?: boolean; quote?: boolean }[];
};

export type GroupsPanel = {
  kind: "groups";
  title?: string;
  left: BoardGroup;
  /** 아직 반대쪽이 안 나왔으면 비워 둔다 — 왼쪽 그룹만 그린다 */
  right?: BoardGroup;
  /** 두 그룹 사이 표시 (기본 ≠) */
  between?: string;
  /**
   * 두 그룹 사이를 잇는 과정 — 그룹에 속하는 단어가 아니라 화살표 위에 쓴다
   * (예: 오른쪽 → 왼쪽 「abstract away = leave out」). 있으면 `between` 기호 대신 화살표
   */
  process?: { arrow?: string; words: { text: string; fresh?: boolean }[] };
  /**
   * 학생이 직접 나눌 단어 — 칠판 아래 칩으로 두고, 끌어서 그룹에 넣으면 그 쪽 보기(`left`·`right`,
   * choice 스텝의 보기 글)를 고른 것으로 친다. 아래 버튼으로 골라도 된다
   */
  sort?: { words: string[]; left: string; right: string };
  /** 칠판 아래 한 줄 — 이번 문장이 그룹에 무엇을 더했는지 */
  caption?: string;
};

/** 칠판 그림 — 예시 장면을 그려 보이고, 아래에 그 장면의 단어를 붙인다 */
export type PicturePanel = {
  kind: "picture";
  title?: string;
  src: string;
  alt: string;
  words?: { text: string; fresh?: boolean; quote?: boolean }[];
  /** 있으면 단어들을 원 하나로 묶고 원 아래에 이 말을 쓴다 (예: 그 네 개의 보통 명사) */
  words_label?: string;
  caption?: string;
};

export type StudyPanel = StructurePanel | MappingPanel | ContrastPanel | NotePanel | MapPanel | GroupsPanel | PicturePanel;
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
  /** 두 번째 색(민트)으로 강조할 구절 — 노란 강조와 덩어리를 나눠 보일 때 (예: 「~에게는」 덩어리 ↔ 주어) */
  highlight_alt?: string[];
  /** 그림 자체이거나, 레슨 `panels`에 적어 둔 이름 */
  panel?: PanelRef;
  /** 앞 문장에서 만든 표상을 다시 꺼내 쓰는 스텝인가 (§15) */
  retrieve?: boolean;
  /** 빼도 되는 삽입(콤마·대시 사이) — 흐리게 */
  faded?: string[];
  /** 건너뛰어도 되는 문장·부분 — 음영 */
  shaded?: string[];
  /**
   * 💡 누르면 말풍선으로 열리는 요령 (지문 밖에서도 쓰는 표현·요령).
   * `mark`가 있으면 Tip을 연 동안 문장에서 그 단어를 표시한다 — 긴 문장에서 찾기 힘든 단어 (one 등).
   * 단어 단위로 찾는다 (Nonetheless 안의 one은 안 잡는다)
   */
  tips?: { label: string; text: string; mark?: string; hint?: boolean }[];
  /** 「밑줄 문제 푸는 법」 중 지금 단계 (0 핵심 단어, 1 관계, 2 밑줄 뜻) */
  method?: number;
  /** 이 스텝에 「자세히 볼래요」 같은 버튼을 둔다. 누르면 `optional_of`가 이 스텝인 것들을 연다 */
  detail_button?: string;
  /** 앞 스텝에서 「자세히」를 고른 학생만 보는 스텝 */
  optional_of?: string;
  /** 「이미 알고 있어요, 넘어갈게요」를 둔다. 학생의 말을 믿고 넘어간다 — 기록은 남긴다 */
  skippable?: boolean;
  /** 이 스텝을 건너뛰면 같이 건너뛴다 (예: 주어 질문을 넘기면 뼈대 그림도) */
  skip_with?: string;
};

export type ChoiceOption = {
  id: string;
  label: string;
  correct?: boolean;
  /** 시험 보기에서 색칠할 핵심 단어 */
  keywords?: string[];
  /** ▸를 누르면 보기 아래에 뜨는 짧은 한국어 */
  ko?: string;
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
  /**
   * 칭찬을 **따로 한 말풍선**으로 보여 주고 「다음으로」를 기다린다.
   * 기본은 다음 스텝 말 앞에 붙는다("맞아요! 그럼 …").
   * (`one_try`: 한 번 틀리면 다시 고르게 하지 않고 이유를 말한 뒤 넘어간다) 칭찬에 뜻 되짚기가
   * 들어가 길어지면 이걸 켠다 — 한 말풍선에 한두 문장.
   */
  praise_alone?: boolean;
  /** 한 번만 고르게 한다. 틀리면 "아쉽게도 틀렸어요." + 이유 → 「다음으로」 */
  one_try?: boolean;
  /**
   * 문장 아래 💡 칩 줄 맨 앞에 「힌트」 — 누르면 선생님 말 없이 상자에 `hints[0]`이 바로 열린다.
   * 연 것은 기록한다 (힌트로 맞히면 혼자 맞힌 게 아니다 §11)
   */
  hint_button?: boolean;
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

/**
 * 문장에서 직접 찾기 — 문장 안의 후보 구절(점선 상자)을 눌러 `answers`를 다 찾는다.
 * 틀린 후보를 누르면 그 자리에서 짧게 말하고 계속 찾게 한다. 다 찾으면 칭찬 + 다음 스텝
 */
export type PickStep = StepBase & {
  type: "pick";
  interaction: "word_pick";
  candidates: string[];
  answers: string[];
  brief: PickCopy;
};

export type PickCopy = {
  ask: string;
  /** 틀린 후보를 눌렀을 때 (「아쉽게도 틀렸어요.」 뒤) */
  wrong: string;
  /** 몇 개 찾았는데 아직 남았을 때 — {n}은 남은 개수 */
  more: string;
  praise: string;
  /** 「잘 모르겠어요」 — 답을 다 보여 주며 */
  explain: string;
  point?: string;
};

export type PolicyStep = ChoiceStep | ThinkStep | ShowStep | PickStep;

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
  /** 이 질문에서 헷갈린 학생에게 수업 끝 「헷갈린 포인트」로 보여 줄 한 줄 정리. 없으면 `explain` */
  point?: string;
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
  steps: Record<string, Stamped<Partial<ChoiceCopy & ThinkCopy & ShowCopy & PickCopy>>>;
  exam?: Stamped<ExamCopy>;
  /** 마무리 — 복습 주기 · 단어 체크 · 짝 맞추기 */
  ending?: Record<string, string>;
  /** 도입 단계 id → 대사 키 → 대사 */
  intro?: Stamped<Record<string, Record<string, string>>>;
};

/**
 * 예상 질문 (§18 optional_help) — 문장 첫 질문의 보기 옆 민트 버튼. 누른 학생에게만
 * 선생님이 짧게 답한다. 지문 이해에 필요한 만큼만
 */
export type OptionalHelp = {
  id: string;
  /** 칩에 적는 말 — 학생의 말이다 */
  label: string;
  brief: string;
};

/** ❓ 개념 설명 — 문장 아래 💡 Tip 옆에 칩으로. 누르면 참고 설명이 열린다 (선생님 말 아님) */
export type ConceptNote = { en: string; title: string; text: string };

export type PolicySentence = {
  id: number;
  /** 「3문장」 대신 쓰는 이름 — 문장 넣기 문제의 「주어진 문장」 */
  label?: string;
  concepts?: ConceptNote[];
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

/** 시험 문제 그대로 — 처음에 풀어 볼 수도, 분석 뒤에 풀 수도 있다 */
export type ExamQuestion = {
  question: string;
  /** 분석을 먼저 한다 — 「바로 풀어 볼게요」를 묻지 않고, 시험 문제는 분석 뒤에 한 번 */
  analysis_first?: boolean;
  /** 보기 단어 뜻 (보기 화면에서 단어를 누르면) */
  glosses?: WordGloss[];
  /**
   * 밑줄 친 구절. 이 구절이 든 문장을 문제 화면에 띄우고 노랗게 칠한다.
   * 어휘 문제처럼 밑줄이 여러 개면 배열 — 그때 문제 화면에 띄울 문장은 `sentence`로 정한다
   */
  underline: string | string[];
  /** 문제 화면에 띄울 문장 id (기본: 첫 밑줄이 든 문장) */
  sentence?: number;
  /** EBS가 공개하는 오답률(%). 인트로에서 말한다 */
  wrong_rate?: number;
  /** 그 모의고사에서 오답률 순위 (Top N) — `content/tutor/exam-stats/모의고사_오답률.xlsx` */
  wrong_rank?: number;
  wrong_rate_source?: string;
  options: ChoiceOption[];
  brief: ExamCopy;
};

export type OptionReview = {
  /** 「아쉽게도 틀렸어요.」를 포함한 첫 화면 — 많이 틀렸다는 말과 같이 보자는 제안 */
  intro: string;
  intro_button: string;
  /** 그림과 함께 하는 설명 */
  say: string;
  panel?: StudyPanel;
  /** 어디서 헷갈렸는지 묻는 말 (물음표 하나) */
  ask: string;
  /** 고른 이유 — `skills`에 기록하고 `reply`로 답한다 */
  choices: { label: string; skills: string[]; reply: string }[];
};

export type ExamCopy = {
  ask: string;
  /** 바로 풀기에서 — 색칠·한국어가 없으니 다른 말을 한다 */
  ask_first?: string;
  /**
   * 많이 고른 오답 — 이 보기를 고르면 한 줄 해설 대신 같이 자세히 본다.
   * 「많이 틀렸어요, 같이 볼까요?」 → 그림과 설명 → 「어디서 헷갈렸어요?」(버튼) → 답에 맞춘 말.
   * 고른 이유는 skill로 기록해, 다음 수업에서 비슷한 문장이 나오면 강조하는 데 쓴다
   */
  option_review?: Record<string, OptionReview>;
  /** 마지막 문제에서 고른 오답마다 수업 끝 「헷갈린 포인트」 한 줄. 없으면 `option_feedback` */
  option_points?: Record<string, string>;
  /** 고른 보기마다 "아쉽게도 틀렸어요." 뒤에 붙는 이유 */
  option_feedback?: Record<string, string>;
  first_correct: string;
  first_wrong: string;
  final_correct: string;
  /**
   * 분석 뒤 마지막 문제에서 정답을 골랐을 때, 다시 볼 주기 전에 한 화면 보여 주는 정답 해설.
   * 없으면 바로 다시 볼 주기로 (21번)
   */
  answer_explain?: string;
  final_wrong: string;
};

/**
 * 수업 도입 — 지문을 읽기 전의 짧은 대화. 한 화면에 선생님 말은 세 문장까지.
 *
 * - `say`: 말하고 「다음」을 기다린다. id가 `rate`면 대사 대신 오답률 문구를 쓴다
 * - `ask`: 보기를 고르게 하고, 고른 보기에 맞는 답(`replies`)을 한다.
 *   `inline`이면 그 답을 다음 질문 앞에 붙여 한 화면으로 보인다
 */
export type IntroStep =
  | {
      id: string;
      type: "say";
      button?: string;
      /** first: 풀이법 설명을 아직 `intro_times`번 안 본 학생만 / later: 그 뒤의 학생만 */
      show_when?: "first" | "later";
      /** 버튼 없이 이만큼(ms) 뒤에 저절로 넘어간다 */
      auto_ms?: number;
      /** 이 말 동안 칠판에 띄울 그림 (`images`의 키). 없으면 풀이법 칠판 */
      image?: string;
      brief: Record<string, string>;
    }
  | {
      id: string;
      type: "ask";
      options: { id: string; label: string }[];
      replies: Record<string, { line: string; inline?: boolean; image?: string }>;
      brief: Record<string, string>;
    };

/** `drawing`은 칠판에 그린 그림처럼 테두리 없이, `photo`(기본)는 사진처럼 흰 테두리 */
export type LessonImage = { src: string; alt: string; credit?: string; kind?: "photo" | "drawing" };

export type PolicyLesson = {
  id: string;
  kind: "policy";
  version: string;
  source: string;
  brief: { topic: string; closing: string };
  exam?: ExamQuestion;
  intro?: IntroStep[];
  /** 도입 내내 칠판에 그려 두는 그림 (`images`의 키). 사진을 띄울 때만 잠깐 가린다 */
  intro_board?: string;
  /** 수업이 끝났을 때 칠판에 띄우는 그림 (도입의 물음표를 채운 판) */
  closing_board?: string;
  images?: Record<string, LessonImage>;
  /**
   * 문제 유형별 풀이법 칠판. `intro_times`번째 수업까지는 도입에서 설명하고, 그 뒤로는
   * 칠판만 띄우고 바로 시작한다 (같은 유형 수업을 몇 번 봤는지는 기기에 센다)
   */
  method?: { type: string; labels: string[]; intro_times: number };
  /**
   * 문장마다 처음엔 영어 문장만 가운데 크게 — 질문·보기는 「다 읽었어요」 뒤에.
   * 학생이 한국어 질문·보기만 보고 푸는 걸 막는다 (2026-10-07 지인 테스트)
   */
  read_first?: boolean;
  /** 지문 읽기 화면의 버튼 (기본 「계속」) */
  read_button?: string;
  /**
   * 한 문장씩 읽는 화면을 빼고, 도입 뒤에 「바로 풀기 / 분석」을 고르게 한다.
   * 바로 풀기를 고른 학생만 지문 전체를 한 화면에서 보고 바로 문제를 푼다.
   */
  passage_on_try?: boolean;
  /** 마무리 단어 체크 — 본문 단어와 보기 단어를 따로 */
  key_words?: { passage: WordGloss[]; options: WordGloss[] };
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
  | { kind: "skip" }
  | { kind: "intro"; optionId: string }
  | { kind: "exam"; when: "first" | "final"; correct: boolean; optionId: string }
  | { kind: "continue" }
  /** 마지막 문제에서 많이 고른 오답을 고른 이유 (버튼) */
  | { kind: "wrong_reason"; optionId: string; reason: string; skills: string[] };

/** 화면에서 바로 올라오는 관찰 — 턴을 만들지 않는다 */
export type UiObservation = { kind: "vocab_click"; word: string } | { kind: "hint_open" };

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
