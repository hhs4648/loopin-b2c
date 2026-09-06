import { describe, expect, it } from "vitest";
import { lessonIds, getLesson } from "./lessons";
import { glossSpans, lookupGloss } from "./glosses";

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

describe("레슨 단어 뜻 커버", () => {
  it("문장 속 단어마다 뜻이 있다 — 누르면 빈칸이 나오면 안 된다", () => {
    const missing: string[] = [];
    for (const id of lessonIds()) {
      const lesson = getLesson(id);
      lesson.chunks.forEach((chunk, i) => {
        const spans = glossSpans(chunk.text, chunk.glosses ?? []);
        for (const span of spans) {
          if (!/[A-Za-z0-9]/.test(span.text)) continue;
          if (!span.gloss) missing.push(`${lesson.id} 문장${i + 1}: ${span.text}`);
        }
      });
    }
    expect(missing).toEqual([]);
  });
});
