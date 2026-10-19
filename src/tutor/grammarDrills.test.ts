import { describe, expect, it } from "vitest";
import { allGrammarDrills, getGrammarDrill, groupOf, isRightInput, normalizeAnswer } from "./grammarDrills";

describe("문법 drill 자료", () => {
  for (const d of allGrammarDrills()) {
    it(`${d.id} — 10문제, 빈칸 하나, 정답이 보기에 있다, 규칙 카드`, () => {
      expect(d.items).toHaveLength(10);
      expect(d.intro.length).toBeGreaterThan(0);
      for (const it of d.items) {
        expect(it.sentence.split("___")).toHaveLength(2);
        expect(it.why.length).toBeGreaterThan(0);
        if (it.type === "choice") expect(it.options).toContain(it.answer);
        else expect(it.answers.length).toBeGreaterThan(0);
      }
    });
  }

  it("묶음 「nor / so」는 세트 4개를 순서대로, 예전에 담은 nor-inversion도 그 묶음", () => {
    const g = groupOf("nor-so");
    expect(g?.drills).toEqual(["nor-inversion", "nor-vs-so", "nor-vs-neither", "nor-writing"]);
    for (const id of g!.drills) expect(getGrammarDrill(id)).not.toBeNull();
    expect(groupOf("nor-inversion")?.id).toBe("nor-so");
    expect(groupOf("adverb-verb")?.drills).toEqual(["adverb-verb"]);
  });
});

describe("주관식 채점", () => {
  it("대소문자·마침표·줄임말 차이는 같은 답", () => {
    expect(normalizeAnswer("Nor can't they.")).toBe(normalizeAnswer("nor cannot they"));
    expect(normalizeAnswer("I won't")).toBe("i will not");
    expect(normalizeAnswer("I’m")).toBe("i am");
  });

  it("작문 — 맞는 여러 모양을 받는다", () => {
    const item = getGrammarDrill("nor-writing")!.items[0]!;
    if (item.type !== "input") throw new Error("작문은 주관식");
    expect(isRightInput(item, "nor has she.")).toBe(true);
    expect(isRightInput(item, "and neither has she")).toBe(true);
    expect(isRightInput(item, "and she hasn’t either")).toBe(true);
    expect(isRightInput(item, "nor she has")).toBe(false);
  });
});
