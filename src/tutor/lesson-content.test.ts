import { describe, expect, it } from "vitest";
import type { Lesson, LessonChunk } from "../../content/tutor/types";
import { getLesson, lessonIds } from "./lessons";
import { validateLlmOutput } from "./llm";

/**
 * **레슨 글도 규칙을 지켜야 한다.**
 *
 * 모델 발화만 가드레일에 태우고 사람이 쓴 대사는 그냥 두면, 정작 학생이 제일
 * 많이 보는 문장(고정 대사·힌트)에서 규칙이 깨진다. 그래서 같은 검사기를
 * 레슨 JSON에도 돌린다.
 */

const LESSONS = lessonIds().map((id) => getLesson(id));

/** 이 문장에서 학생이 스스로 도달해야 하는 말들 */
function answersOf(chunk: LessonChunk): string[] {
  const correctChoices = (chunk.expected_errors ?? []).flatMap((e) =>
    [...(e.treatment?.choices ?? []), ...(e.rounds?.[0]?.choices ?? [])]
      .filter((c) => c.correct)
      .map((c) => c.label),
  );
  const scoringAnswers = (chunk.scoring_points ?? []).flatMap((p) => {
    const tail = p.text.split("→").slice(1).join("→").trim();
    const cleaned = tail.replace(/^['"“”‘’]|['"“”‘’]$/g, "").trim();
    return cleaned ? [cleaned] : [];
  });
  return [chunk.model_translation, ...correctChoices, ...scoringAnswers];
}

function eachChunk(run: (lesson: Lesson, chunk: LessonChunk, index: number) => void) {
  for (const lesson of LESSONS) {
    lesson.chunks.forEach((chunk, index) => run(lesson, chunk, index));
  }
}

describe("레슨 힌트", () => {
  it("1·2단은 정답을 흘리지 않는다", () => {
    const leaks: string[] = [];
    eachChunk((lesson, chunk, i) => {
      for (const rung of [1, 2] as const) {
        const message = chunk.hint_ladder?.find((h) => h.rung === rung)?.message;
        if (!message) continue;
        const verdict = validateLlmOutput({ message }, { bannedStrings: answersOf(chunk) });
        if (!verdict.ok) leaks.push(`${lesson.id} 문장${i + 1} ${rung}단 — ${verdict.reason}`);
      }
    });
    expect(leaks).toEqual([]);
  });

  it("3단은 모범 해석을 알려 준다 — 여기까지 와야 공개다", () => {
    eachChunk((lesson, chunk, i) => {
      const message = chunk.hint_ladder?.find((h) => h.rung === 3)?.message;
      // 사다리가 2칸인 레슨도 있다. 있으면 정답이 들어 있어야 한다
      if (!message) return;
      expect(message, `${lesson.id} 문장${i + 1}`).toContain(chunk.model_translation);
    });
  });

  it("단이 비지 않는다 — 1단 없이 2단만 있는 문장은 사다리가 아니다", () => {
    eachChunk((lesson, chunk, i) => {
      const rungs = (chunk.hint_ladder ?? []).map((h) => h.rung).sort();
      if (!rungs.length) return;
      expect(rungs, `${lesson.id} 문장${i + 1}`).toEqual(
        Array.from({ length: rungs.length }, (_, n) => n + 1),
      );
    });
  });
});

describe("레슨 고정 대사", () => {
  it("한 턴에 질문은 하나다", () => {
    const offenders: string[] = [];
    eachChunk((lesson, chunk, i) => {
      const lines = [
        ...(chunk.hint_ladder ?? []).map((h) => h.message),
        ...(chunk.expected_errors ?? []).flatMap((e) => [
          e.treatment?.message,
          ...Object.values(e.treatment?.on_choice ?? {}).map((b) => b.message),
          ...(e.rounds ?? []).map((r) => r.message),
        ]),
      ].filter((x): x is string => Boolean(x));
      for (const line of lines) {
        const questions = (line.match(/[?？]/g) ?? []).length;
        if (questions > 1) offenders.push(`${lesson.id} 문장${i + 1} — ${line.slice(0, 40)}…`);
      }
    });
    expect(offenders).toEqual([]);
  });

  it("반말이 없다", () => {
    const offenders: string[] = [];
    eachChunk((lesson, chunk, i) => {
      for (const h of chunk.hint_ladder ?? []) {
        const verdict = validateLlmOutput(
          { message: h.message },
          { bannedStrings: [], maxSentences: 99, maxQuestions: 99 },
        );
        if (!verdict.ok) offenders.push(`${lesson.id} 문장${i + 1} ${h.rung}단 — ${verdict.reason}`);
      }
    });
    expect(offenders).toEqual([]);
  });
});

describe("레슨 데이터 계약", () => {
  it("정답 매칭(demo_match)이 모든 문장에 있다 — 없으면 정답을 못 알아본다", () => {
    eachChunk((lesson, chunk, i) => {
      expect(chunk.demo_match?.p1?.length, `${lesson.id} 문장${i + 1}`).toBeGreaterThan(0);
    });
  });

  it("error_priority에 적힌 id가 실제로 있다", () => {
    eachChunk((lesson, chunk, i) => {
      const ids = (chunk.expected_errors ?? []).map((e) => e.id);
      for (const id of chunk.error_priority ?? []) {
        expect(ids, `${lesson.id} 문장${i + 1}`).toContain(id);
      }
    });
  });
});
