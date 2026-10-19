import { describe, expect, it } from "vitest";
import { allMiniMocks, byKind, scoreOf } from "./mini";
import { getSet } from "./sets";

describe("미니 모의고사 — 2024년 3월 고3 21~45번 (시험지 순서, 쉬운 문항 뺌)", () => {
  const mock = allMiniMocks().find((m) => m.id === "eng-2024-03-full")!;
  const by = (no: number) => mock.items.find((i) => i.no === no)!;

  it("21번부터 차례대로 — 도표·일치·안내문(25~28)은 없다, 45번(장문 일치)은 넣는다", () => {
    expect(mock.items.map((i) => i.no)).toEqual([21, 22, 23, 24, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]);
  });

  it("정답은 해설지 정답표 그대로, 만점 49", () => {
    expect(mock.items.map((i) => [i.no, i.answer])).toEqual([
      [21, 5], [22, 3], [23, 1], [24, 5], [29, 4], [30, 3], [31, 1], [32, 1], [33, 3], [34, 1], [35, 4],
      [36, 2], [37, 5], [38, 4], [39, 2], [40, 1], [41, 3], [42, 4], [43, 4], [44, 4], [45, 5],
    ]);
    expect(scoreOf(mock, {}).max).toBe(49);
  });

  it("문항마다 보기 다섯, 글·출제의도·해석이 있고 시험지 찌꺼기가 없다", () => {
    for (const it of mock.items) {
      expect(it.options, String(it.no)).toHaveLength(5);
      const text = `${it.given ?? ""}${it.passage ?? ""}${it.paragraphs?.join("") ?? ""}`;
      expect(text.length, String(it.no)).toBeGreaterThan(300);
      expect(`${it.question}${text}${it.options.join("")}`, String(it.no)).not.toMatch(/=====PAGE|§|øÇ|LegendStudy|[-]|\[\d+~\d+\]/);
      expect(it.intent, String(it.no)).toMatch(/^\[출제의도\]/);
      expect((it.translation ?? "").length, String(it.no)).toBeGreaterThan(150);
    }
  });

  it("빈칸·문장 넣기 자리·요약문·장문이 제자리에 있다", () => {
    for (const no of [31, 32, 33, 34]) expect(by(no).passage, String(no)).toContain("________");
    expect(by(21).passage).toContain(by(21).underline!);
    expect(by(45).paragraphs).toHaveLength(4);
    expect(by(45).options.join("")).not.toMatch(/확인 사항/);
    expect(by(23).passage).toContain("E = mc²");
    for (const no of [38, 39]) expect(by(no).passage, String(no)).toMatch(/\(①\)[\s\S]*\(⑤\)/);
    expect(by(39).given).toMatch(/^This stands in contrast[\s\S]*how they looked\.$/);
    expect(by(40).after).toMatch(/\(A\) ________[\s\S]*\(B\) ________\.$/);
    for (const no of [36, 37]) expect(by(no).paragraphs, String(no)).toHaveLength(3);
    expect(by(41).passage).toBe(by(42).passage);
    expect(by(42).passage).toMatch(/\(a\)anxious[\s\S]*\(d\)relieve[\s\S]*\(e\)cloud/);
    expect(by(43).paragraphs).toHaveLength(3);
    expect(by(44).paragraphs).toHaveLength(4);
  });

  it("분석 레슨이 적힌 문항은 그 세트가 앱에 있다 — 21문항 모두", () => {
    const withLesson = mock.items.filter((it) => it.lesson);
    expect(withLesson.map((i) => i.no)).toEqual(mock.items.map((i) => i.no));
    expect(withLesson).toHaveLength(21);
    for (const it of withLesson) expect(getSet(it.lesson), String(it.no)).toBeTruthy();
  });

  it("채점 — 맞힌 문항 배점의 합, 유형별 맞힌 수", () => {
    const all = Object.fromEntries(mock.items.map((i) => [i.no, i.answer]));
    expect(scoreOf(mock, all)).toEqual({ score: 49, max: 49, correct: 21, total: 21 });
    const some = { 31: 1, 32: 5, 33: 3 };
    expect(byKind(mock, some).find((k) => k.kind === "빈칸")).toEqual({ kind: "빈칸", right: 2, total: 4 });
  });
});
