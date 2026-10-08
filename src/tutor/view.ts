import type { ProperNoun, WordGloss } from "../../content/tutor/types";
import type { StudyPanel } from "./policy/types";

/**
 * 세션이 화면에 넘기는 모양 (`TutorView`)과 공통 버튼 글.
 *
 * 예전 해석 엔진(`engine.ts`)에 있던 것을 그 엔진을 지우면서 여기로 옮겼다.
 * 지금은 Teaching Policy 세션(`policy/session.ts`)만 이 모양을 채운다.
 */

export const UNKNOWN_BTN = "잘 모르겠어요";
export const HINT_BTN = "힌트 주세요";
export const READY_BTN = "네, 좋아요!";
export const READ_BTN = "다 읽었어요";
export const MORE_BTN = "더 알고 싶어요";
export const NEXT_BTN = "다음으로";

export type UiScreen = "chat" | "study" | "read" | "words" | "match" | "points" | "summary";

/**
 * 항목 하나에 대한 학습 기록.
 *
 * **`firstTry`가 난이도의 근거다.** 유도 후 결과로 난이도를 재면, 우리가 늘
 * 1번 항목을 먼저 유도하기 때문에 1번이 쉬워 보이는 편향이 생긴다.
 * 지금은 세션 안에만 쌓이고, 서버가 생기면 그대로 흘려보낸다.
 */
export type PointRecord = {
  lessonId: string;
  unit: number;
  point: number;
  firstTry: boolean;
  nudged: boolean;
  told: boolean;
  /** 좌절 방지로 모범 해석을 본 뒤였나 */
  revealed: boolean;
};

export type TutorView = {
  screen: UiScreen;
  message: string;
  buttons: string[];
  placeholder: string;
  studentLine: string;
  effect: null | "light";
  sentence: string;
  activeChunk: string;
  chunkLabel: string;
  progressIndex: number;
  progressTotal: number;
  ended: boolean;
  recordLine: string | null;
  properNouns: ProperNoun[];
  /** 지금 문장의 단어 뜻. 문장 학습에서 눌러 본다 */
  glosses: WordGloss[];
  /*
    아래 넷은 Teaching Policy 레슨(`src/tutor/policy/`)만 채운다.
    예전 레슨에서는 비어 있고 화면도 예전 그대로다.
  */
  /** 이번 스텝에서 강조할 구절 (노란 칠) */
  highlight?: string[];
  /** 시험지의 밑줄 친 구절 — 음영이 아니라 밑줄로 그린다 */
  underline?: string[];
  /** 「찾기」 스텝 — 문장 안 후보 구절을 눌러 고른다. found는 맞힌 것, missed는 틀리게 누른 것 */
  pick?: { candidates: string[]; found: string[]; missed: string[]; open: boolean } | null;
  /** 수업 소개(도입 말) 중 — 화면 아무 데나 눌러도 다음 말로 */
  tapToNext?: boolean;
  /** 맞았다는 말만 하는 짧은 화면 (잠깐 뒤 저절로 다음 질문) */
  praiseOnly?: boolean;
  /** 흐린 부분이 왜 흐린지 — 문장 아래 작게 */
  fadedNote?: string | null;
  /** 자유 해석 결과 — 내 해석(틀린 곳 표시) · 고친 해석(고친 곳 표시) · 짚을 말 */
  translation?: TranslationResult | null;
  /** 문장 위 꼬리표 — 「문장 2」, 「주어진 문장」 */
  sentenceTag?: string | null;
  /** 문장 하나를 맞히고 끝낸 칭찬 화면 */
  celebrate?: boolean;
  /** 도입 건너뛰기 — 버튼 아래 밑줄 글자로 */
  skipButton?: string | null;
  /** 이 말은 버튼 없이 이만큼(ms) 뒤 저절로 넘어간다 — 화면이 AUTO_NEXT_CMD를 보낸다 */
  autoNextMs?: number | null;
  /** 말풍선 아래 작은 안내 (문장 먼저 읽기의 「모르는 단어는 ☆로 저장해요」) */
  bubbleNote?: string | null;
  /** 문장 먼저 읽기 — 영어 문장만 가운데 크게. 버튼은 readDelayMs 뒤에 나타난다 */
  readingFirst?: boolean;
  readDelayMs?: number | null;
  /** 두 번째 색(민트) 강조 */
  highlightAlt?: string[];
  /** 문장 내내 색으로 띄우는 단어 (누르면 뜻) */
  emphasis?: string[];
  /** 문장 아래에 띄우는 그림 — 문장 뼈대, 대응표, 대비 */
  panel?: StudyPanel | null;
  /** 보기가 길면 알약을 세로로 쌓는다 */
  buttonLayout?: "row" | "stack";
  /** 보기가 아닌 버튼(「잘 모르겠어요」 등) — 보기와 다른 색으로 그린다 */
  auxButtons?: string[];
  /** 지금 버튼들이 보기라서 ①②③을 단다 (「다음으로」 하나일 때는 안 단다) */
  numbered?: boolean;
  /*
    ── Teaching Policy 문장 화면 표시 ──
  */
  /** 빼도 되는 삽입 — 흐리게 */
  faded?: string[];
  /** 건너뛰어도 되는 부분 — 음영 */
  shaded?: string[];
  /** ❓ 개념 — 문장 아래 칩. 누르면 참고 설명 */
  concepts?: { en: string; title: string; text: string }[];
  /** 💡 요령 말풍선 */
  tips?: { label: string; text: string; mark?: string; hint?: boolean }[];
  /** 「밑줄 문제 푸는 법」 단계 표시. active가 null이면 표시만 */
  methodSteps?: { labels: string[]; active: number | null } | null;
  /** 시험 보기 — 핵심 단어 색칠, ▸ 한국어 */
  examOptions?: { id: string; label: string; keywords: string[]; ko: string }[] | null;
  examGlosses?: WordGloss[];
  /** 해설만 보는 마지막 화면 — 보기 id마다 정답 여부와 해설. 보기를 누르면 고르는 게 아니라 해설이 열린다 */
  examExplain?: Record<string, { correct: boolean; text: string }> | null;
  /**
   * 밑줄이 여러 개인 문제(어휘) — 보기 id마다 그 밑줄이 든 문장. 보기의 「문장 보기」를 누르면
   * 위 문장 칸이 그 문장으로 바뀐다 (보기를 고르는 건 아니다)
   */
  examSentences?: Record<string, { sentence: string; underline: string; glosses: WordGloss[] }> | null;
  /** 마무리 — 다시 볼 주기와 특별 저장 */
  review?: { weeks: number | null; saved: boolean; choices: (number | null)[]; caption: string } | null;
  /** 마무리 — 주요 단어 체크 */
  wordCheck?: { title: string; step: string; words: WordGloss[]; checked: string[] } | null;
  /** 바로 맞힌 뒤 「핵심만 정리」 — 칠판 그림, 중요 표현, 주요 단어 */
  summary?: {
    title: string;
    board: StudyPanel | null;
    expressions: { icon: string; label: string; text: string }[];
    words: WordGloss[];
  } | null;
  /** 마무리 — 오늘 헷갈렸던 곳 (별표로 노트에 저장) */
  pointsReview?: { title: string; lessonId: string; items: { key: string; title: string; text: string }[] } | null;
  /** 마무리 — 짝 맞추기 */
  matchPairs?: WordGloss[] | null;
  /** false면 아래 입력창을 숨긴다 — 버튼으로만 답하는 화면에서 (기본은 보인다) */
  allowInput?: boolean;
  /** 문장 학습 중 위의 「전체 지문」으로 여는 지문 */
  fullPassage?: { given?: string | null; sentences: string[]; underline: string[] } | null;
  /** 이전·다음 문장으로 옮겨 갈 수 있나 */
  canPrevSentence?: boolean;
  canNextSentence?: boolean;
  /** 교실 화면 칠판에 띄우는 그림 (도입에서 데카르트 초상 등) */
  boardImage?: { src: string; alt: string; credit?: string; kind?: "photo" | "drawing" } | null;
  /** 머리글 「문장 학습」 자리에 쓸 말 — 「지문 읽기」「문제 풀기」 */
  progressLabel?: string;
  /**
   * 지문 읽기 화면(`screen: "read"`). 문장이 하나씩 드러나며 소리로 읽히고,
   * 다 드러나면 「계속」으로 넘어간다.
   */
  passage?: {
    heading: string;
    title: string;
    /** 문장 넣기 문제의 「주어진 문장」 — 지문과 따로 */
    given?: string | null;
    sentences: string[];
    /** 지금까지 드러난 문장 수 */
    revealed: number;
    /** 지금 읽고 있는 문장 (0부터) */
    current: number;
    /** 시험에서 밑줄 친 구절 (어휘 문제는 여러 개) */
    underline: string[];
    /** false면 한 문장씩 드러내며 읽지 않는다 — 장으로 넘겨 보는 지문(+ 문제와 보기) */
    auto?: boolean;
    /** 지문 아래에 붙이는 시험 보기 */
    options?: string[] | null;
    /** 바로 풀기 중 — 보기를 누르면 그 보기를 답으로 고른다 */
    pickable?: boolean;
    /** 바로 풀기에서 고른 오답 보기 id ("1"~"5") — 줄이 그어진다 */
    picked?: string | null;
    /** 바로 풀기에서 맞힌 보기 id — 초록으로 */
    right?: string | null;
  };
};

export type TranslationResult = {
  /** 학생이 쓴 해석. 「잘 모르겠어요」면 null */
  mine: string | null;
  /** `mine`에서 틀린 자리 [시작, 끝) */
  marks: [number, number][];
  model: string;
  /** `model`에서 고친 구절 */
  fixes: string[];
  notes: string[];
  /** 연습할 문장으로 저장한다 */
  save: boolean;
  english: string;
  lessonId: string;
  /** 「2문장」 */
  where: string;
};
