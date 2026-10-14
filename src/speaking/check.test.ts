import { describe, expect, it } from "vitest";
import data from "../../content/speaking/toeic-sp-picture-01.json";
import { checkSpeech, countWords, keywordHits, slotUsed } from "./check";
import type { SpeakingLesson } from "./types";

const L = data as SpeakingLesson;
const slot = (k: string) => L.template.find((s) => s.key === k)!;

describe("토익 스피킹 — 말한 것을 틀에 맞춰 보기 (LLM 없이)", () => {
  it("예시 답변은 네 칸을 모두 채운다 — 연습 사진과 실전 사진 둘 다", () => {
    for (const task of [L.practice, L.test]) {
      const text = task.model.map((m) => m.en).join(" ");
      expect(checkSpeech(L.template, task, text).usedCount).toBe(4);
    }
  });

  it("예시 문장 하나는 자기 칸을 채운다 (따라 말하기 확인)", () => {
    for (const task of [L.practice, L.test]) {
      for (const m of task.model) expect(slotUsed(slot(m.slot), m.en), m.en).toBe(true);
    }
  });

  it("음성 인식이 대문자·마침표 없이 받아 적어도 맞게 본다", () => {
    expect(slotUsed(slot("place"), "this picture was taken in a meeting room")).toBe(true);
    expect(slotUsed(slot("main"), "in the center of the picture a man is selling fruit")).toBe(true);
    expect(slotUsed(slot("guess"), "It's seems like a busy day")).toBe(true);
  });

  it("틀 표현이 없으면 그 칸은 비어 있다", () => {
    const r = checkSpeech(L.template, L.test, "A man is selling fruit. A woman has a bag.");
    expect(r.usedCount).toBe(0);
    expect(r.keywordHits).toEqual(expect.arrayContaining(["man", "fruit", "woman", "bag"]));
  });

  it("단어 수와 사진 내용 단어를 센다 (apples → apple, selling → sell 꼴도)", () => {
    expect(countWords("On the right side, a woman is choosing apples.")).toBe(9);
    expect(keywordHits(L.test, "she is choosing apples and buying vegetables")).toEqual(["apple", "buying", "vegetable"]);
  });

  it("다정쌤 말은 세 문장까지, 물음표 하나 (독해 수업과 같은 규칙)", () => {
    const lines = [...Object.values(L.lines), ...L.fill.flatMap((f) => [f.ask, f.praise, f.why]), ...L.template.map((s) => s.tip)];
    for (const line of lines) {
      expect(line.split(/(?<=[.!?])\s+/).filter(Boolean).length, line).toBeLessThanOrEqual(3);
      expect((line.match(/\?/g) ?? []).length, line).toBeLessThanOrEqual(1);
    }
  });

  it("빈칸 문제는 정답이 하나고, 틀렸을 때 설명이 정답 보기만 콕 집어 말하지 않는다", () => {
    for (const f of L.fill) {
      expect(f.options.filter((o) => o.correct)).toHaveLength(1);
      expect(f.ask).not.toContain(f.options.find((o) => o.correct)!.label);
    }
  });
});
