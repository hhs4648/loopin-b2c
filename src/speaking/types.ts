/**
 * 토익 스피킹 시범 레슨의 모양 (`content/speaking/*.json`).
 *
 * 독해 수업(Teaching Policy 엔진)과는 따로 돈다 — 스피킹은 「틀 외우기 → 따라 말하기 →
 * 틀만 보고 말하기 → 실전 타이머」로 흐름이 정해져 있어 정책이 고를 게 없다.
 * 수업 중 LLM은 부르지 않는다. 학생이 말한 걸 음성 인식으로 글자로 받고, 칸마다 `need` 정규식으로 확인한다.
 */

export type SlotKey = string;

/** 답변 틀의 한 칸 — 사진 묘사는 장소 · 가장 눈에 띄는 것 · 주변 · 느낌 */
export type TemplateSlot = {
  key: SlotKey;
  label: string;
  /** 칠판에 쓰는 틀 표현 */
  phrase: string;
  /** 이 칸을 말했다고 볼 표현 (정규식, 대소문자 무시) — 하나라도 맞으면 채운 것 */
  need: string[];
  tip: string;
};

export type ModelLine = { slot: SlotKey; en: string; ko: string };

export type PictureTask = {
  image: string;
  alt: string;
  model: ModelLine[];
  /** 사진 내용 단어 — 몇 개 말했는지 센다 (틀만 외워 말하고 사진 내용이 없으면 점수가 안 나온다) */
  keywords: string[];
  prep_seconds?: number;
  speak_seconds?: number;
};

export type FillItem = {
  id: string;
  slot: SlotKey;
  ask: string;
  sentence: string;
  options: { label: string; correct?: boolean }[];
  praise: string;
  why: string;
};

export type SpeakingLesson = {
  id: string;
  title: string;
  subtitle: string;
  note?: string;
  template: TemplateSlot[];
  practice: PictureTask;
  fill: FillItem[];
  test: PictureTask;
  lines: Record<string, string>;
};
