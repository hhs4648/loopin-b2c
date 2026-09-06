import { describe, expect, it } from "vitest";
import type { Lesson, LessonChunk } from "../../content/tutor/types";
import frame from "../../content/tutor/frame.json";
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

describe("레슨 체크리스트", () => {
  it("유도(nudge)는 정답을 흘리지 않는다", () => {
    const leaks: string[] = [];
    eachChunk((lesson, chunk, i) => {
      for (const p of chunk.scoring_points ?? []) {
        if (!p.nudge) continue;
        const verdict = validateLlmOutput(
          { message: p.nudge },
          { bannedStrings: answersOf(chunk) },
        );
        if (!verdict.ok) leaks.push(`${lesson.id} 문장${i + 1} 항목${p.id} — ${verdict.reason}`);
      }
    });
    expect(leaks).toEqual([]);
  });

  it("항목마다 체크 키워드·유도·알려주기가 다 있다", () => {
    eachChunk((lesson, chunk, i) => {
      for (const p of chunk.scoring_points ?? []) {
        const where = `${lesson.id} 문장${i + 1} 항목${p.id}`;
        expect(p.check?.length, where).toBeGreaterThan(0);
        expect(p.nudge, where).toBeTruthy();
        expect(p.tell, where).toBeTruthy();
      }
    });
  });

  it("알려주기(tell)는 그 항목만 답한다 — 모범 해석 전체가 아니다", () => {
    eachChunk((lesson, chunk, i) => {
      for (const p of chunk.scoring_points ?? []) {
        expect(p.tell, `${lesson.id} 문장${i + 1} 항목${p.id}`).not.toContain(
          chunk.model_translation,
        );
      }
    });
  });
});

/*
  **유도는 못 낸 항목에 나가지, 틀린 항목에 나가는 게 아니다.**

  학생이 어떤 항목을 안 냈다고 해서 그걸 어떻게 오해했다는 뜻은 아니다.
  실제로 틀렸을 때 쓸 대사는 `expected_errors`에 따로 있다. 유도가 미리
  "X는 Y가 아니에요"라고 해버리면, 하지도 않은 실수를 뒤집어씌우면서
  **틀린 답 Y까지 알려 주는** 셈이 된다 (2026-09-06 실제 불평).
*/
const PREEMPTIVE_DENIAL = /아니에요|아니라|아닙니다|아니고|(으)?로\s*(보면|두면|읽으면)/;

describe("유도 문구", () => {
  for (const lesson of LESSONS) {
    it(`${lesson.id} — 안 한 오해를 미리 부정하지 않는다`, () => {
      const offenders: string[] = [];
      lesson.chunks.forEach((chunk, i) => {
        for (const p of chunk.scoring_points ?? []) {
          const hit = p.nudge?.match(PREEMPTIVE_DENIAL);
          if (hit) offenders.push(`문장${i + 1} 항목${p.id}: "${hit[0]}" — ${p.nudge}`);
        }
      });
      expect(offenders).toEqual([]);
    });

    it(`${lesson.id} — 유도가 어느 자리인지 가리킨다`, () => {
      const vague: string[] = [];
      lesson.chunks.forEach((chunk, i) => {
        for (const p of chunk.scoring_points ?? []) {
          if (p.nudge && /(그|이|저)\s*(부분|쪽)/.test(p.nudge)) {
            vague.push(`문장${i + 1} 항목${p.id}: ${p.nudge}`);
          }
        }
      });
      expect(vague).toEqual([]);
    });
  }
});

describe("말투 예시(frame.voice_examples)", () => {
  it("좋은 예시는 가드레일을 통과한다 — 예시가 규칙을 어기면 모델도 어긴다", () => {
    const bad: string[] = [];
    for (const example of frame.voice_examples.good) {
      const verdict = validateLlmOutput(
        { message: example.tutor },
        {
          bannedStrings: [],
          minSentences: frame.speech.min_sentences,
          studentText: example.student,
        },
      );
      if (!verdict.ok) bad.push(`${example.action} — ${verdict.reason}`);
    }
    expect(bad).toEqual([]);
  });

  it("나쁜 예시는 전부 걸린다 — 안 걸리면 가드레일에 구멍이 있다", () => {
    const passed: string[] = [];
    for (const example of frame.voice_examples.bad) {
      const verdict = validateLlmOutput(
        { message: example.tutor },
        {
          bannedStrings: ["근무하다"],
          minSentences: frame.speech.min_sentences,
          // 「학생이 쓰지 않은 말을 부정」은 학생 발화가 있어야 잴 수 있다
          studentText: "student" in example ? example.student : undefined,
        },
      );
      if (verdict.ok) passed.push(`${example.why}: ${example.tutor}`);
    }
    expect(passed).toEqual([]);
  });
});

describe("레슨 데이터 계약", () => {
  it("체크리스트가 모든 문장에 있다 — 없으면 정답을 못 알아본다", () => {
    eachChunk((lesson, chunk, i) => {
      expect(chunk.scoring_points?.length, `${lesson.id} 문장${i + 1}`).toBeGreaterThan(0);
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

  it("단어 뜻이 있고, 문장 전체 해석을 그대로 넣지 않는다", () => {
    eachChunk((lesson, chunk, i) => {
      expect(chunk.glosses?.length, `${lesson.id} 문장${i + 1}`).toBeGreaterThan(0);
      for (const g of chunk.glosses ?? []) {
        expect(g.ko, `${lesson.id} 문장${i + 1} ${g.en}`).not.toBe(chunk.model_translation);
      }
    });
  });
});
