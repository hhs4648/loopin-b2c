import { describe, expect, it } from "vitest";
import { allMiniMocks, getMiniMock } from "./mini";
import { hardestSets, itemOfLesson, tenMinMocks } from "./tenmin";
import { getPolicyLesson } from "./policy/lessons";
import { setsIn } from "./sets";

/*
  10분 모의고사 문항은 분석 레슨 JSON에서 꺼낸다. 2024년 3월은 시험지에서 따로 만든 미니 모의고사
  (`content/tutor/mini-mocks/eng-2024-03-full.json`)가 있으니, 같은 문항끼리 맞춰 본다.
*/
describe("10분 모의고사 — 레슨에서 문항 꺼내기", () => {
  const full = allMiniMocks().find((m) => m.id.includes("2024-03"))!;

  it("2024년 3월 세트 전부: 번호·정답·배점·유형이 시험지 미니와 같다", () => {
    const errs: string[] = [];
    for (const set of setsIn("moeui-2024-03")) {
      const no = Number(/(\d+)번/.exec(set.title)![1]);
      if (/-v\d+$/.test(set.id) || no >= 41) continue; // 장문은 10분 모의고사에 안 넣는다
      const lesson = getPolicyLesson(set.lessons[0]!);
      const mine = lesson ? itemOfLesson(set, lesson) : null;
      const ref = full.items.find((it) => it.no === no);
      if (!ref) continue; // 듣기 등 시험지 미니에 없는 문항
      if (!mine) {
        errs.push(`${set.id}: 문항을 못 만듦`);
        continue;
      }
      if (mine.answer !== ref.answer) errs.push(`${set.id}: 정답 ${mine.answer} ≠ ${ref.answer}`);
      if (mine.points !== ref.points) errs.push(`${set.id}: 배점 ${mine.points} ≠ ${ref.points}`);
      if (mine.kind !== ref.kind) errs.push(`${set.id}: 유형 ${mine.kind} ≠ ${ref.kind}`);
      if (!!mine.marked !== !!ref.marked) errs.push(`${set.id}: marked`);
      if (!!mine.paragraphs !== !!ref.paragraphs) errs.push(`${set.id}: 단락 유무`);
      if ((mine.options[0] === "") !== (ref.options[0] === "")) errs.push(`${set.id}: 번호만 고르는 문항 여부`);
      if (ref.given && !mine.given?.startsWith(ref.given.slice(0, 30))) errs.push(`${set.id}: 주어진 글`);
      if (ref.after && !mine.after?.startsWith(ref.after.slice(0, 30))) errs.push(`${set.id}: 요약문`);
      if (ref.passage && !mine.passage?.startsWith(ref.passage.slice(0, 30))) errs.push(`${set.id}: 지문 시작`);
    }
    expect(errs).toEqual([]);
  });

  it("순서 문제는 주어진 글 + (A)(B)(C) 세 단락", () => {
    const set = setsIn("moeui-2024-03").find((s) => s.id === "moeui-2024-03-36")!;
    const item = itemOfLesson(set, getPolicyLesson(set.lessons[0]!)!)!;
    expect(item.given).toMatch(/^Different creative pursuits/);
    expect(item.paragraphs?.map((p) => p.slice(0, 3))).toEqual(["(A)", "(B)", "(C)"]);
    expect(item.options[1]).toBe("(B)-(A)-(C)");
  });

  it("시험마다 오답률 Top 10 한 묶음(Top1부터), 듣기·비교용 사본·장문은 빼고, 최근 시험부터", () => {
    const hard = hardestSets("moeui-2024-03");
    expect(hard.length).toBe(5);
    expect(hard.every((s) => Number(/(\d+)번/.exec(s.title)![1]) < 41)).toBe(true);
    expect(hard.map((s) => s.wrong_rate)).toEqual([...hard].map((s) => s.wrong_rate).sort((a, b) => b! - a!));
    expect(hard.some((s) => /-v\d+$/.test(s.id) || s.subtitle.startsWith("듣기"))).toBe(false);

    const mocks = tenMinMocks();
    expect(mocks.map((m) => m.id)).toEqual(["ten-moeui-2026-03", "ten-moeui-2024-03", "ten-moeui-2022-03"]);
    expect(mocks[1]!.title).toBe("2024년 3월 오답률 Top 10");
    for (const m of mocks) {
      expect(m.items.length).toBeGreaterThanOrEqual(3);
      expect(m.items.length).toBeLessThanOrEqual(10);
      // 문제마다 2분 — 10문제면 20분 미니 모의고사
      expect(m.minutes).toBe(m.items.length * 2);
      // 오답률 Top1부터
      const rates = m.items.map((it) => it.wrong_rate ?? -1);
      expect(rates).toEqual([...rates].sort((a, b) => b - a));
      for (const it of m.items) expect(it.lesson).toBeTruthy();
    }
    // 문제 하나만 풀기 — 낱개 id
    const single = getMiniMock(`${mocks[0]!.id}-q${mocks[0]!.items[0]!.no}`)!;
    expect(single.items).toHaveLength(1);
    expect(single.items[0]!.no).toBe(mocks[0]!.items[0]!.no);
  });
});
