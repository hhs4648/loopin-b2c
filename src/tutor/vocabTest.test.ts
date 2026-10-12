import { describe, expect, it } from "vitest";
import { allPolicyLessons } from "./policy/lessons";
import type { VocabEntry } from "./vocab";
import { blankOptions, blankSourceOf, buildQuestions, distractorPool, findForm, inflect, pickWords, posOf } from "./vocabTest";

const word = (en: string, ko: string, savedAt = "2026-10-01T00:00:00Z"): VocabEntry => ({ en, ko, sentence: "", savedAt });

describe("단어 테스트", () => {
  it("문장 속 꼴을 찾는다", () => {
    expect(findForm("He contributed a lot.", "contribute")).toEqual({ form: "contributed", at: 3 });
    expect(findForm("They start now.", "art")).toBeNull();
    expect(findForm("Those nouns leave out their differences.", "leave out")?.form).toBe("leave out");
  });

  it("레슨 문장에서 빈칸 문장과 해석을 찾는다", () => {
    const src = blankSourceOf(word("leave out", "빠뜨리다"));
    expect(src).not.toBeNull();
    expect(src!.sentence.slice(src!.at, src!.at + src!.form.length).toLowerCase()).toBe(src!.form.toLowerCase());
    expect(src!.translation.length).toBeGreaterThan(0);
    expect(src!.sentence).not.toMatch(/[①-⑳]/);
  });

  it("세 유형을 섞고, 단어마다 한 번씩 낸다", () => {
    const glosses = allPolicyLessons().flatMap((l) => l.sentences.flatMap((s) => s.glosses));
    const singles = glosses.filter((g) => !g.en.includes(" ") && blankSourceOf(word(g.en, g.ko)));
    const words = [...new Map(singles.map((g) => [g.en.toLowerCase(), word(g.en, g.ko)])).values()].slice(0, 12);
    const qs = buildQuestions(words, distractorPool(words));
    expect(new Set(qs.map((q) => q.kind))).toEqual(new Set(["match", "meaning", "blank"]));
    const asked = qs.flatMap((q) => (q.kind === "match" ? q.pairs.map((p) => p.en) : [q.en]));
    expect(asked.sort()).toEqual(words.map((w) => w.en).sort());
    for (const q of qs) {
      if (q.kind === "match") continue;
      expect(q.options).toContain(q.answer);
      expect(q.options.length).toBe(4);
      expect(new Set(q.options).size).toBe(4);
    }
  });

  it("덜 본 단어와 많이 틀린 단어를 먼저 고른다", () => {
    const ws = [word("a", "가"), word("b", "나"), word("c", "다")];
    const stats = { a: { seen: 4, right: 4, wrong: 0 }, b: { seen: 2, right: 0, wrong: 2 } };
    expect(pickWords(ws, stats, 2).map((w) => w.en)).toEqual(["c", "b"]);
  });

  it("한국어 뜻으로 품사를 가른다", () => {
    expect(posOf("개념화하다")).toBe("verb");
    expect(posOf("~이 없다")).toBe("verb");
    expect(posOf("실용적인")).toBe("adj");
    expect(posOf("접근 가능한")).toBe("adj");
    expect(posOf("시간의, 일시적인")).toBe("adj");
    expect(posOf("균일하게")).toBe("adv");
    expect(posOf("외부인")).toBe("noun");
    expect(posOf("차이")).toBe("noun");
  });

  it("보기를 정답과 같은 꼴로 바꾼다", () => {
    expect(inflect("restore", "ed", "verb")).toBe("restored");
    expect(inflect("deprive", "ing", "verb")).toBe("depriving");
    expect(inflect("reveal", "s", "verb")).toBe("reveals");
    expect(inflect("strategy", "s", "noun")).toBe("strategies");
    expect(inflect("make sense of", "ed", "verb")).toBe("made sense of");
    expect(inflect("arms race", "s", "noun")).toBe("arms races");
  });

  it("빈칸 보기는 정답과 품사·꼴이 같다", () => {
    const pool = distractorPool([]);
    const w = word("contribute", "기여하다");
    for (let i = 0; i < 20; i++) {
      const opts = blankOptions(w, "contributed", pool);
      expect(opts).toHaveLength(4);
      expect(opts).toContain("contributed");
      for (const o of opts) expect(o).toMatch(/(ed|made|took|left|overcame|gave|got|found|thought|brought|held|kept)\b/);
      const nouns = blankOptions(word("difference", "차이"), "differences", pool);
      for (const o of nouns) expect(o).toMatch(/s$/);
    }
  });
});
