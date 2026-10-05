import { describe, expect, it } from "vitest";
import { UNKNOWN_BTN } from "../engine";
import { stamps } from "./copy";
import { allPolicyLessons, getPolicyCopy, getPolicyLesson } from "./lessons";
import { createPolicySession } from "./session";
import { emptyStudentState, type LearningEvent } from "./student-state";
import type { ChoiceStep } from "./types";

/**
 * 한 문제를 **작은 단위**로 쪼갠 수업 (21번: 단어 → … → 실전 풀기).
 *
 * 통째로 된 예전 21번의 흐름은 `policy.test.ts`가 본다. 여기는 단위 수업의 흐름과,
 * 단위 레슨 글이 지켜야 하는 규칙을 본다.
 */

const WORDS = "moeui-2025-03-21-u1-words";
const EXAM = "moeui-2025-03-21-u6-exam";
const UNITS = allPolicyLessons().filter((l) => !!l.unit);

function harness(id: string) {
  const events: LearningEvent[] = [];
  let saved = emptyStudentState();
  const session = createPolicySession(id, "민지", {
    loadStudent: () => saved,
    saveStudent: (next) => {
      saved = next;
    },
    logEvents: (batch) => events.push(...batch),
    now: () => 0,
  });
  return { session, events };
}

function choice(id: string, stepId: string): ChoiceStep {
  return getPolicyLesson(id)!.sentences.flatMap((s) => s.steps).find((s) => s.id === stepId) as ChoiceStep;
}
const right = (id: string, stepId: string) => choice(id, stepId).options.find((o) => o.correct)!.label;

describe("단어 (1) — 지문을 읽지 않고 바로 단어로", () => {
  it("도입 한 화면 → 첫 단어 질문. 지문 읽기 화면은 없다", async () => {
    const { session } = harness(WORDS);
    let v = session.view();
    expect(v.screen).toBe("chat");
    expect(v.buttons).toEqual(["네, 좋아요!"]);
    v = await session.submit("네, 좋아요!");
    expect(v.screen).toBe("study");
    expect(session.lastAction()?.interactionId).toBe("w1_trunk");
    expect(v.highlight).toEqual(["the trunk"]);
    // 머리글은 단위 이름, 진행은 스텝으로 센다
    expect(v.progressLabel).toBe("단어 (1)");
    expect([v.progressIndex, v.progressTotal]).toEqual([1, 4]);
  });

  it("묻는 단어는 눌러도 뜻이 안 나온다 — 답을 보고 고르게 하지 않는다", () => {
    const sentence = getPolicyLesson(WORDS)!.sentences[0]!;
    const glossed = sentence.glosses.map((g) => g.en);
    for (const word of ["trunk", "metaphysics", "applied science"]) expect(glossed).not.toContain(word);
  });

  it("셋을 다 혼자 맞히면 버튼 다섯 번에 끝난다 — 마지막은 나무 표", async () => {
    const { session } = harness(WORDS);
    let taps = 0;
    const tap = async (text: string) => {
      taps++;
      return session.submit(text);
    };
    let v = await tap("네, 좋아요!");
    v = await tap(right(WORDS, "w1_trunk"));
    expect(session.lastAction()?.interactionId).toBe("w1_metaphysics");
    v = await tap(right(WORDS, "w1_metaphysics"));
    v = await tap(right(WORDS, "w1_applied"));
    expect(session.lastAction()?.interactionId).toBe("w1_tree");
    expect(v.panel?.kind).toBe("mapping");
    expect([v.progressIndex, v.progressTotal]).toEqual([4, 4]);
    v = await tap(v.buttons[0]!);
    expect(v.ended).toBe(true);
    expect(v.recordLine).toContain("결과=이해");
    expect(v.boardImage?.src).toBe("/assets/descartes-tree-filled.svg");
    expect(taps).toBe(5);
  });

  it("틀리면 그 오독을 겨냥한 말이 먼저 — 답은 말하지 않는다", async () => {
    const { session } = harness(WORDS);
    await session.submit("네, 좋아요!");
    const v = await session.submit("자동차 트렁크");
    expect(v.message).toContain("그 뜻도 있는 단어예요");
    expect(v.message).not.toContain("줄기");
    expect(v.buttons).toEqual(["가지", "줄기", UNKNOWN_BTN]);
  });
});

describe("실전 풀기 — 많이 고른 보기 세 개만 먼저", () => {
  async function toExam(session: ReturnType<typeof harness>["session"]) {
    let v = session.view();
    expect(v.message).toContain("오답률 57.4%");
    v = await session.submit(v.buttons[0]!);
    expect(v.screen).toBe("read");
    return session.submit("계속");
  }
  const lesson = getPolicyLesson(EXAM)!;
  const label = (id: string) => lesson.exam!.options.find((o) => o.id === id)!.label;

  it("지문을 읽으면 「분석부터 할까」를 묻지 않고 바로 문제다", async () => {
    const { session } = harness(EXAM);
    const v = await toExam(session);
    expect(v.screen).toBe("study");
    expect(v.progressLabel).toBe("문제 풀기");
    expect(v.message).not.toContain("다시");
  });

  it("정답과 가장 많이 고른 오답 둘(④ 21.3% · ③ 17.4%)만 보인다. 번호는 시험지 그대로", async () => {
    const { session } = harness(EXAM);
    const v = await toExam(session);
    expect(v.buttons).toEqual([label("1"), label("3"), label("4"), "보기 다 볼래요"]);
    expect(v.numerals).toEqual(["①", "③", "④"]);
    expect(v.auxButtons).toContain("보기 다 볼래요");
  });

  it("「보기 다 볼래요」를 누르면 다섯 개가 다 나오고, 눌렀다는 게 남는다", async () => {
    const { session, events } = harness(EXAM);
    await toExam(session);
    let v = await session.submit("보기 다 볼래요");
    expect(v.buttons).toEqual(lesson.exam!.options.map((o) => o.label));
    expect(v.numerals).toEqual(["①", "②", "③", "④", "⑤"]);
    v = await session.submit(label("1"));
    expect(v.ended).toBe(true);
    expect(events.some((e) => (e.observation as { kind: string }).kind === "exam_show_all")).toBe(true);
  });

  it("안 보이는 보기는 번호로도 고를 수 없다 — 「4번」은 시험지의 ④", async () => {
    const { session } = harness(EXAM);
    await toExam(session);
    let v = await session.submit("2번");
    expect(v.ended).toBe(false);
    expect(v.message).toContain("보기 중에서");
    v = await session.submit("4번");
    expect(v.message).toContain("'both'");
  });

  it("처음 틀리면 그 보기만 치우고 한 번 더 — 답은 말하지 않는다. 고치면 반짝", async () => {
    const { session } = harness(EXAM);
    await toExam(session);
    let v = await session.submit(label("4"));
    expect(v.ended).toBe(false);
    expect(v.message).not.toContain("①");
    expect(v.buttons).toEqual([label("1"), label("3"), "보기 다 볼래요"]);
    expect(v.numerals).toEqual(["①", "③"]);
    v = await session.submit(label("1"));
    expect(v.ended).toBe(true);
    expect(v.effect).toBe("light");
    expect(v.recordLine).toContain("결과=오류후이해");
  });

  it("두 번 틀리면 정답과 이유를 알려 주고 끝난다", async () => {
    const { session } = harness(EXAM);
    await toExam(session);
    await session.submit(label("4"));
    const v = await session.submit(label("3"));
    expect(v.ended).toBe(true);
    expect(v.message).toContain("정답은 ①");
    expect(v.recordLine).toContain("결과=설명제공");
  });

  it("추린 보기는 정답 하나 + 오답 둘", () => {
    const { options, shortlist } = lesson.exam!;
    expect(shortlist).toHaveLength(3);
    expect(options.filter((o) => shortlist!.includes(o.id) && o.correct)).toHaveLength(1);
  });
});

describe("단위 레슨 글 — 절대 규칙", () => {
  it("단위 레슨이 있다", () => {
    expect(UNITS.map((l) => l.id)).toEqual([WORDS, EXAM]);
  });

  for (const lesson of UNITS) {
    const copy = getPolicyCopy(lesson.id)!;
    const steps = lesson.sentences.flatMap((s) => s.steps);
    const lines = [
      copy.closing,
      ...Object.values(copy.intro ?? {}).flatMap((x) => (typeof x === "string" ? [] : Object.values(x))),
      ...(copy.exam
        ? [copy.exam.ask, copy.exam.final_correct, copy.exam.final_wrong, ...Object.values(copy.exam.feedback ?? {})]
        : []),
      ...Object.values(copy.steps).flatMap((c) => [
        c.ask, c.reask, ...(c.hints ?? []), c.explain, c.praise, c.say, c.hint, c.summary,
        ...Object.values(c.feedback ?? {}),
      ]),
    ].filter((line): line is string => !!line);

    describe(lesson.id, () => {
      it("대사가 낡지 않았다", () => {
        const stale = stamps(lesson, copy).filter(([, now, stamped]) => now !== stamped).map(([slot]) => slot);
        expect(stale).toEqual([]);
      });

      it("brief에 있는 말은 대사에도 다 있다", () => {
        for (const step of steps) {
          const c = copy.steps[step.id] as Record<string, unknown> | undefined;
          expect(c, step.id).toBeTruthy();
          for (const key of Object.keys(step.brief)) expect(c![key], `${step.id}.${key}`).toBeTruthy();
        }
        const exam = copy.exam as Record<string, unknown> | undefined;
        for (const key of Object.keys(lesson.exam?.brief ?? {})) expect(exam?.[key], `exam.${key}`).toBeTruthy();
        for (const id of Object.keys(lesson.exam?.brief.feedback ?? {})) {
          expect(copy.exam?.feedback?.[id], `exam.feedback.${id}`).toBeTruthy();
        }
      });

      it("한 말풍선에 물음표 하나, 세 문장까지", () => {
        expect(lines.filter((line) => (line.match(/\?/g) ?? []).length > 1)).toEqual([]);
        expect(lines.filter((line) => line.split(/(?<=[.!?])\s+/).length > 3)).toEqual([]);
      });

      it("해요체 — 반말로 끝나는 문장이 없다", () => {
        const banmal = lines
          .flatMap((line) => line.split(/(?<=[.!?])\s+/))
          .filter((sentence) => /[가-힣]/.test(sentence))
          .filter((sentence) => !/[요죠][.!?]?$/.test(sentence.replace(/[\s😊^'’"”)]+$/u, "")));
        expect(banmal).toEqual([]);
      });

      it("질문·힌트·오답 피드백은 정답을 미리 말하지 않는다", () => {
        for (const step of steps) {
          if (step.type !== "choice") continue;
          const answer = step.options.find((o) => o.correct)!.label;
          const c = copy.steps[step.id]!;
          for (const line of [c.ask!, ...c.hints!, ...Object.values(c.feedback ?? {})]) {
            expect(line, step.id).not.toContain(answer);
          }
        }
        // 시험 문제: 다시 고를 기회를 주는 말에 정답 번호가 없어야 한다
        const correct = lesson.exam?.options.findIndex((o) => o.correct) ?? -1;
        for (const line of Object.values(copy.exam?.feedback ?? {})) {
          expect(line).not.toContain(["①", "②", "③", "④", "⑤"][correct] ?? "\u0000");
        }
      });

      it("보기는 세 개, 정답은 하나. 오답마다 그 오독을 겨냥한 말이 있다", () => {
        for (const step of steps) {
          if (step.type !== "choice") continue;
          expect(step.options, step.id).toHaveLength(3);
          expect(step.options.filter((o) => o.correct), step.id).toHaveLength(1);
          for (const o of step.options.filter((x) => !x.correct)) {
            expect(step.brief.feedback?.[o.id], `${step.id}.${o.id}`).toBeTruthy();
          }
        }
      });

      it("강조 구절이 보여 주는 문장 안에 있고, 이름으로 부른 그림이 레슨에 있다", () => {
        for (const sentence of lesson.sentences) {
          for (const step of sentence.steps) {
            const shown = step.display ?? sentence.text;
            for (const phrase of step.highlight ?? []) expect(shown, step.id).toContain(phrase);
            if (typeof step.panel === "string") expect(lesson.panels?.[step.panel], step.id).toBeTruthy();
          }
        }
      });
    });
  }
});

