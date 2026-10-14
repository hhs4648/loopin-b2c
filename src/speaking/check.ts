import type { PictureTask, SlotKey, TemplateSlot } from "./types";

/**
 * 학생이 말한 것(음성 인식 결과 글자)을 틀에 맞춰 본다 — LLM 없이 규칙으로.
 *
 * 음성 인식은 한국인 억양에서 자주 틀리게 받아 적는다. 그래서 **틀렸다고 하지 않는다** —
 * 빠진 칸만 「이 표현도 넣어 봐요」로 알려 준다. 발음·유창성 점수는 재지 않는다.
 */

export type SpeechCheck = {
  /** 칸마다 채웠는지 */
  slots: { key: SlotKey; label: string; used: boolean }[];
  usedCount: number;
  words: number;
  /** 사진 내용 단어를 몇 개 말했는지 */
  keywordHits: string[];
};

/** 소문자 · 따옴표 정리 · 공백 하나로 */
export function normalize(text: string): string {
  return text
    .toLowerCase()
    .replace(/[’‘`]/g, "'")
    .replace(/[^a-z0-9' ]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function slotUsed(slot: TemplateSlot, text: string): boolean {
  const t = normalize(text);
  return slot.need.some((re) => new RegExp(`\\b(?:${re})\\b`, "i").test(t));
}

export function countWords(text: string): number {
  const t = normalize(text);
  return t ? t.split(" ").length : 0;
}

/** 단어 기본형만 맞으면 센다 (apple → apples, sell → selling) */
export function keywordHits(task: PictureTask, text: string): string[] {
  const words = new Set(normalize(text).split(" "));
  return task.keywords.filter((k) =>
    [...words].some((w) => w === k || w === `${k}s` || w === `${k}es` || w === `${k}ing` || (k.endsWith("e") && w === `${k.slice(0, -1)}ing`)),
  );
}

export function checkSpeech(template: TemplateSlot[], task: PictureTask, text: string): SpeechCheck {
  const slots = template.map((s) => ({ key: s.key, label: s.label, used: slotUsed(s, text) }));
  return {
    slots,
    usedCount: slots.filter((s) => s.used).length,
    words: countWords(text),
    keywordHits: keywordHits(task, text),
  };
}
