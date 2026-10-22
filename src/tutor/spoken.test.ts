import { describe, expect, it } from "vitest";
import { getPolicyLesson } from "./policy/lessons";
import { applySpeakBlanks, speakBlanksOf } from "./spoken";

describe("빈칸 듣기 — underscore라고 읽지 않고 정답 말을 넣는다", () => {
  it("2022년 3월 31번은 Compassion으로 읽는다", () => {
    const lesson = getPolicyLesson("moeui-2022-03-31-metta-meditation")!;
    const text = "________ is a learnable skill, and we need to direct it as much towards those we are tempted to dismiss and detest as to those we love.";
    const spoken = applySpeakBlanks(text, speakBlanksOf(lesson.exam));
    expect(spoken.startsWith("Compassion is a learnable skill")).toBe(true);
    expect(spoken).not.toMatch(/_/);
    expect(spoken).not.toMatch(/underscore/i);
  });

  it("빈칸이 긴 구여도 그 구를 넣어 읽는다", () => {
    const lesson = getPolicyLesson("moeui-2026-03-33-profound-building")!;
    const spoken = applySpeakBlanks("A profound building is ________.", speakBlanksOf(lesson.exam));
    expect(spoken).toBe("A profound building is an extension of human bodily and mental actions and capabilities.");
  });

  it("요약 (A)(B)는 정답 두 단어를 넣어 읽는다", () => {
    const lesson = getPolicyLesson("moeui-2024-03-40-brain-plasticity")!;
    const text = lesson.sentences.find((s) => s.text.includes("(B) ________"))!.text;
    const spoken = applySpeakBlanks(text, speakBlanksOf(lesson.exam));
    expect(spoken).toContain("permanence");
    expect(spoken).toContain("transformation");
    expect(spoken).not.toMatch(/_/);
    expect(spoken).not.toContain("(A)");
    expect(spoken).not.toContain("(B)");
  });

  it("듣기 응답 빈칸은 정답 문장으로 읽는다", () => {
    const lesson = getPolicyLesson("moeui-2024-03-11-student-id-photo")!;
    expect(applySpeakBlanks("________", speakBlanksOf(lesson.exam))).toBe(
      "No need. You can have your photo taken on the spot.",
    );
  });

  it("밑줄 의미 문제와 빈칸 없는 문장은 그대로 읽는다", () => {
    const lesson = getPolicyLesson("moeui-2026-03-21-music-researchers")!;
    expect(speakBlanksOf(lesson.exam)).toEqual([]);
    expect(applySpeakBlanks("Mettā means kindness.", speakBlanksOf(lesson.exam))).toBe("Mettā means kindness.");
  });

  it("정답을 못 찾아도 underscore라고 읽지 않는다", () => {
    expect(applySpeakBlanks("A profound building is ________.", [])).toBe("A profound building is.");
  });
});
