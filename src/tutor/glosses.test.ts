import { describe, expect, it } from "vitest";
import { glossSpans, lookupGloss, splitPhraseGlosses } from "./glosses";

describe("glossSpans", () => {
  it("긴 구가 짧은 단어보다 먼저 맞는다", () => {
    const spans = glossSpans("the past four years.", [
      { en: "the", ko: "그" },
      { en: "the past four years", ko: "지난 4년" },
    ]);
    const hit = spans.find((s) => s.gloss);
    expect(hit?.text).toBe("the past four years");
    expect(hit?.gloss?.ko).toBe("지난 4년");
  });

  it("단어 일부에 달라붙지 않는다", () => {
    const spans = glossSpans("insights", [{ en: "in", ko: "~에서" }]);
    expect(spans[0]!.gloss).toBeNull();
  });
});

describe("lookupGloss", () => {
  const glosses = [
    { en: "company", ko: "회사" },
    { en: "the past four years", ko: "지난 4년" },
  ];

  it("단어 그대로 찾는다", () => {
    expect(lookupGloss("Company", glosses)?.ko).toBe("회사");
  });

  it("구 안의 단어로도 찾는다", () => {
    expect(lookupGloss("past", glosses)?.ko).toBe("지난 4년");
  });
});

describe("구절 뜻을 단어마다 나누기", () => {
  const glosses = [
    { en: "lift the veil", ko: "장막을 걷어 내다 · 숨겨진 것을 드러내다" },
    { en: "completely transparent", ko: "완전히 투명한" },
    { en: "practices", ko: "관행, 하는 방식" },
  ];

  it("구절 안의 단어마다 따로 뜻을 달고, 구절은 아랫줄(phrase)로 따로 준다 (the 같은 말은 그냥 글자)", () => {
    const out = splitPhraseGlosses(glosses);
    expect(out.find((g) => g.en === "lift")?.ko).toBe("들어 올리다");
    expect(out.find((g) => g.en === "lift")?.phrase).toEqual({ en: "lift the veil", ko: "장막을 걷어 내다" });
    expect(out.find((g) => g.en === "veil")?.ko).toContain("장막");
    expect(out.find((g) => g.en === "transparent")?.ko).toBe("투명한");
    expect(out.find((g) => g.en === "transparent")?.phrase?.en).toBe("completely transparent");
    expect(out.some((g) => g.en === "the")).toBe(false);
    const spans = glossSpans("do not lift the veil behind", out).filter((s) => s.gloss).map((s) => s.text);
    expect(spans).toEqual(["lift", "veil"]);
  });

  it("지금 통째로 고르는 후보 구절은 나누지 않는다", () => {
    const out = splitPhraseGlosses(glosses, ["lift the veil"]);
    expect(out.some((g) => g.en === "lift the veil")).toBe(true);
    expect(out.some((g) => g.en === "lift")).toBe(false);
  });
});

describe("덩어리 안의 기능어는 덩어리 뜻으로", () => {
  it("to make의 to는 '~로, ~에게'가 아니라 to make의 뜻", () => {
    const to = splitPhraseGlosses([{ en: "to make", ko: "만들기 위해" }]).find((g) => g.en === "to");
    // 단어 뜻은 비우고 덩어리 뜻만
    expect(to?.ko).toBe("");
    expect(to?.phrase).toEqual({ en: "to make", ko: "만들기 위해" });
  });
  it("of·it·or 같은 기능어는 「~의」「그것」「또는」 정도의 기본 뜻 + 덩어리 뜻 (2026-10-20 선생님)", () => {
    const out = splitPhraseGlosses([{ en: "no examples of it", ko: "그것의 사례가 없다" }, { en: "in written or notated form", ko: "기록되거나 악보에 적힌 형태로" }]);
    const of = out.find((g) => g.en === "of");
    expect(of?.ko).toBe("~의");
    expect(of?.phrase).toEqual({ en: "no examples of it", ko: "그것의 사례가 없다" });
    expect(out.find((g) => g.en === "it")?.ko).toBe("그것");
    expect(out.find((g) => g.en === "or")?.ko).toBe("또는");
  });
  it("레슨에 따로 적은 단어 뜻은 그대로 먼저", () => {
    const fr = splitPhraseGlosses([{ en: "for", ko: "~에게(는)" }, { en: "for most outsiders", ko: "대부분의 외부인에게는" }]).find((g) => g.en === "for");
    expect(fr?.ko).toBe("~에게(는)");
  });
});
