import { describe, expect, it } from "vitest";
import { decideOnChoice, shouldShow, type DecideInput } from "./decide";
import { stamps } from "./copy";
import { allPolicyLessons, getPolicyCopy } from "./lessons";
import { createPolicySession, underlinesOf } from "./session";
import {
  emptyStudentState,
  recordPerformance,
  skillOf,
} from "./student-state";
import type { ChoiceStep, PolicyStep } from "./types";

/*
  정책 단위 테스트는 레슨에 기대지 않는다 — 지문을 갈아 끼워도 그대로 돈다.
  아래 스텝들은 이 테스트만을 위한 가짜다.
*/
const L0 = allPolicyLessons()[0]!;
const input = (student = emptyStudentState()): DecideInput => ({
  student,
  context: L0.context,
  item: L0.item,
  sentence: L0.sentences[0]!,
});
const choiceStep = {
  id: "t_choice",
  type: "choice",
  interaction: "meaning_choice",
  skill: "sentence_meaning",
  options: [
    { id: "a", label: "정답", correct: true },
    { id: "b", label: "오답 1" },
    { id: "c", label: "오답 2" },
  ],
  brief: { ask: "", hints: ["", ""], explain: "", praise: "" },
} as ChoiceStep;
const showStep = (when: PolicyStep["when"], skill?: string) =>
  ({ id: "t_show", type: "show", interaction: "note", when, skill, brief: { say: "" } }) as PolicyStep;

describe("정책 — 개입 사다리 (§10)", () => {
  const wrong = { kind: "answer", correct: false, optionId: "b", latencyMs: 0 } as const;
  const dontKnow = { kind: "dont_know", latencyMs: 0 } as const;

  it("처음 틀리면 설명이 아니라 가벼운 힌트다", () => {
    expect(decideOnChoice(choiceStep, { rung: 0, wrongPicks: [] }, wrong, input()).action).toBe("GIVE_LIGHT_HINT");
  });

  it("바로 「모르겠어요」를 눌러도 힌트가 먼저다", () => {
    const actions = [0, 1, 2].map((rung) => decideOnChoice(choiceStep, { rung, wrongPicks: [] }, dontKnow, input()).action);
    expect(actions).toEqual(["GIVE_LIGHT_HINT", "GIVE_STRONG_HINT", "EXPLAIN"]);
  });

  it("보기가 하나만 남으면 더 묻지 않고 설명한다", () => {
    expect(decideOnChoice(choiceStep, { rung: 1, wrongPicks: ["c"] }, wrong, input()).action).toBe("EXPLAIN");
  });

  it("stable인 skill에서 뜻밖에 틀리면 스스로 고칠 기회를 준다 (§4)", () => {
    let student = emptyStudentState();
    student = recordPerformance(student, "sentence_meaning", "independent_success", 0);
    student = recordPerformance(student, "sentence_meaning", "independent_success", 0);
    expect(decideOnChoice(choiceStep, { rung: 0, wrongPicks: [] }, wrong, input(student)).action).toBe(
      "GIVE_SELF_CORRECTION_OPPORTUNITY",
    );
  });
});

describe("정책 — 무엇을 보여 줄까", () => {
  it("정답이어도 가치가 높은 설명은 보여 준다 — 객관식은 찍을 수 있다 (§6)", () => {
    expect(shouldShow(showStep("unless_stable", "long_subject"), input(), false)).toBe(true);
  });

  it("거듭 혼자 맞혀 온 학생에게는 같은 설명을 되풀이하지 않는다. 이번에 막혔으면 본다", () => {
    let student = emptyStudentState();
    student = recordPerformance(student, "long_subject", "independent_success", 0);
    student = recordPerformance(student, "long_subject", "independent_success", 0);
    expect(shouldShow(showStep("unless_stable", "long_subject"), input(student), false)).toBe(false);
    expect(shouldShow(showStep("unless_stable", "long_subject"), input(student), true)).toBe(true);
  });

  it("「필요하면」 주는 도움은 막혔을 때만 나온다", () => {
    expect(shouldShow(showStep("if_struggled"), input(), false)).toBe(false);
    expect(shouldShow(showStep("if_struggled"), input(), true)).toBe(true);
  });
});

describe("학생 상태 (§4, §11, §17)", () => {
  it("한 번 맞힌 건 stable이 아니다", () => {
    const s = recordPerformance(emptyStudentState(), "x", "independent_success", 0);
    expect(skillOf(s, "x").status).toBe("uncertain");
  });

  it("힌트로 맞힌 건 혼자 맞힌 것과 따로 센다", () => {
    let s = recordPerformance(emptyStudentState(), "x", "hint_assisted_success", 1);
    s = recordPerformance(s, "x", "hint_assisted_success", 1);
    const r = skillOf(s, "x");
    expect(r.hintAssisted).toBe(2);
    expect(r.independent).toBe(0);
    expect(r.status).toBe("uncertain");
    expect(r.mistakes).toBe(2);
  });

  it("실패가 거듭되면 weak", () => {
    let s = recordPerformance(emptyStudentState(), "x", "explained", 2);
    s = recordPerformance(s, "x", "explained", 2);
    expect(skillOf(s, "x").status).toBe("weak");
  });
});

for (const L of allPolicyLessons()) {
  const C = getPolicyCopy(L.id)!;
  const all = L.sentences.flatMap((s) => s.steps);
  const linesOf = (id: string) => {
    const c = C.steps[id] ?? {};
    return [c.ask, c.reask, ...(c.hints ?? []), c.explain, c.praise, c.say, c.hint, c.summary, ...Object.values(c.feedback ?? {})].filter(
      (x): x is string => !!x,
    );
  };

  describe(`지문 규칙 — ${L.id}`, () => {
    it("대사가 있고 낡지 않았다", () => {
      expect(C).toBeTruthy();
      expect(stamps(L, C).filter(([, now, was]) => now !== was).map(([slot]) => slot)).toEqual([]);
    });

    it("한 말풍선에 물음표 하나, 세 문장까지", () => {
      for (const step of all) {
        for (const line of linesOf(step.id)) {
          expect((line.match(/\?/g) ?? []).length, `${step.id}: ${line}`).toBeLessThanOrEqual(1);
          expect((line.match(/[.?!~](\s|$)/g) ?? []).length, `${step.id}: ${line}`).toBeLessThanOrEqual(3);
        }
      }
    });

    it("보기는 두세 개, 정답 하나, 질문·힌트는 정답 보기를 말하지 않는다", () => {
      for (const step of all) {
        if (step.type !== "choice") continue;
        expect(step.options.length, step.id).toBeGreaterThanOrEqual(2);
        expect(step.options.length, step.id).toBeLessThanOrEqual(3);
        const right = step.options.filter((o) => o.correct);
        expect(right, step.id).toHaveLength(1);
        if (!/[가-힣]/.test(right[0]!.label)) continue;
        const c = C.steps[step.id]!;
        for (const line of [c.ask!, ...c.hints!, ...Object.values(c.feedback ?? {})]) {
          expect(line, step.id).not.toContain(right[0]!.label);
        }
      }
    });

    it("강조 구절이 화면의 문장 안에 있다", () => {
      for (const sen of L.sentences) {
        for (const step of sen.steps) {
          const shown = step.display ?? sen.text;
          for (const phrase of step.highlight ?? []) expect(shown, step.id).toContain(phrase);
        }
        for (const word of sen.emphasis ?? []) {
          const known = [...sen.glosses.map((g) => g.en), ...(sen.concepts ?? []).map((c) => c.en)];
          expect(known.includes(word), `${sen.id}: ${word}`).toBe(true);
        }
        for (const step of sen.steps) {
          const shown = step.display ?? sen.text;
          for (const phrase of [...(step.faded ?? []), ...(step.shaded ?? [])]) expect(shown, step.id).toContain(phrase);
        }
      }
      for (const u of L.exam ? underlinesOf(L.exam) : []) expect(L.sentences.some((s) => s.text.includes(u)), u).toBe(true);
    });

    it.skipIf(!!L.passage_on_try)("처음부터 끝까지 혼자 맞히면 시험 문제를 풀고 「이해」로 끝난다", async () => {
      const session = createPolicySession(L.id, null, {
        loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0,
      });
      let v = session.view();
      for (let g = 0; g < 12 && v.screen === "chat"; g++) v = await session.submit(v.buttons[0]!);
      if (v.screen === "read") v = await session.submit("계속");
      if (L.exam) v = await session.submit("분석부터 할게요");
      for (let g = 0; g < 80 && !v.ended && v.progressLabel !== "문제 풀기"; g++) {
        const id = session.lastAction()?.interactionId ?? "";
        const step = all.find((s) => s.id === id);
        const open = step?.type === "choice" && !(v.buttons.length === 1);
        v = await session.submit(open ? step.options.find((o) => o.correct)!.label : v.buttons[0]!);
      }
      if (L.exam) v = await session.submit(L.exam.options.find((o) => o.correct)!.label);
      // 마무리 단계(다시 볼 주기 · 단어 체크 · 짝 맞추기)가 있는 레슨은 끝까지 넘긴다
      for (let g = 0; g < 10 && !v.ended; g++) {
        v = await session.submit(v.screen === "match" ? "__match_done" : v.buttons[0]!);
      }
      expect(v.ended).toBe(true);
      expect(v.recordLine).toContain("결과=이해");
    });
  });
}

describe("2026년 3월 21번 — 밑줄 문제 푸는 법", () => {
  const ID = "moeui-2026-03-21-music-researchers";
  const L = allPolicyLessons().find((l) => l.id === ID)!;
  const make = () =>
    createPolicySession(ID, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
  /** 도입 → 읽기 → 「분석하러 갈게요」 */
  async function toAnalysis() {
    const session = make();
    let v = session.view();
    for (let g = 0; g < 5 && !v.buttons.includes("분석하러 갈게요"); g++) v = await session.submit(v.buttons[0]!);
    expect(v.buttons).toEqual(["바로 풀어 볼게요", "분석하러 갈게요"]);
    v = await session.submit("분석하러 갈게요");
    return { session, v };
  }

  it("한 문장씩 읽는 화면은 없다. 바로 풀기는 지문 전체 → 문제, 지문으로 돌아갈 수 있다", async () => {
    const session = make();
    let v = session.view();
    for (let g = 0; g < 5 && !v.buttons.includes("바로 풀어 볼게요"); g++) v = await session.submit(v.buttons[0]!);
    // 처음 고르는 화면이 곧 「문제 보기」 — 문제, 넘겨 보는 지문, 보기 다섯 개
    expect(v.screen).toBe("read");
    expect(v.passage?.auto).toBe(false);
    expect(v.passage?.title).toContain("밑줄 친");
    expect(v.passage?.options).toHaveLength(5);
    v = await session.submit("바로 풀어 볼게요");
    expect(v.examOptions).toHaveLength(5);
    expect(v.message.startsWith("실제 시험처럼")).toBe(true);
    // 실제 시험처럼 — 색칠도 한국어도 없다
    expect(v.examOptions!.every((o) => !o.keywords.length && !o.ko)).toBe(true);
    expect(v.buttons).toEqual(["지문 다시 볼래요"]);
    v = await session.submit("지문 다시 볼래요");
    expect(v.screen).toBe("read");
    v = await session.submit("문제 풀기");
    expect(v.examOptions).toHaveLength(5);

    // 틀리면 답을 말하지 않고 분석으로
    v = await session.submit(L.exam!.options[0]!.label);
    expect(v.message).toBe("아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.");
    expect(v.examOptions).toBeNull();
    v = await session.submit("분석하러 갈게요");
    expect(session.lastAction()?.interactionId).toBe("s1_q");
  });

  it("바로 풀어서 맞히면 「분석 없이 정답」 — 기본은 다시 안 봄, 그다음 단어 체크", async () => {
    const session = make();
    let v = session.view();
    for (let g = 0; g < 5 && !v.buttons.includes("바로 풀어 볼게요"); g++) v = await session.submit(v.buttons[0]!);
    await session.submit("바로 풀어 볼게요");
    v = await session.submit(L.exam!.options[2]!.label);
    expect(v.message.startsWith("분석 없이 맞혔어요!")).toBe(true);
    expect(v.review?.weeks).toBeNull();
    v = await session.submit("__weeks:5");
    expect(v.message).toContain("5주 뒤에");
    v = await session.submit("다음으로");
    expect(v.screen).toBe("words");
  });

  it("도입은 칠판의 풀이법 + 말풍선 둘, 그다음 바로 지문 (바로 풀기는 묻지 않는다)", async () => {
    const session = make();
    let v = session.view();
    expect(v.boardImage?.src).toBe("/assets/underline-method.svg");
    expect(v.message).toBe("밑줄 문제는 시간 싸움이에요. 단어를 다 알 필요는 없어요.");
    v = await session.submit("네");
    expect(v.message).toContain("칠판 순서대로");
    const { v: first } = await toAnalysis();
    expect(first.screen).toBe("study");
    expect(first.methodSteps).toEqual({ labels: ["핵심 단어 찾기", "관계 잡기", "밑줄 뜻 고르기"], active: 0 });
  });

  it("문장 학습 위의 ‹ › 로 이전 문장으로 돌아가거나 다음 문장으로 넘긴다. 「전체 지문」도 있다", async () => {
    const { session } = await toAnalysis();
    let v = session.view();
    expect(v.fullPassage?.sentences).toHaveLength(7);
    expect(v.canPrevSentence).toBe(false);
    v = await session.submit("__next_sentence");
    expect(v.progressIndex).toBe(2);
    expect(session.lastAction()?.interactionId).toBe("s2_q");
    v = await session.submit("__prev_sentence");
    expect(v.progressIndex).toBe(1);
    expect(session.lastAction()?.interactionId).toBe("s1_q");
    for (let i = 0; i < 7; i++) v = await session.submit("__next_sentence");
    expect(v.examOptions).toHaveLength(5);
  });

  it("틀리면 「아쉽게도 틀렸어요.」 + 이유, 다시 고르게 하지 않고 넘어간다", async () => {
    const { session } = await toAnalysis();
    let v = await session.submit("같아요");
    expect(v.message.startsWith("아쉽게도 틀렸어요. 'without'을 봐요.")).toBe(true);
    expect(v.buttons).toEqual(["다음으로"]);
    v = await session.submit("다음으로");
    expect(v.message.startsWith("둘은 달라요.")).toBe(true);
    expect(v.panel?.kind).toBe("groups");
  });

  it("맞히면 칭찬이 지도 설명 앞에 붙는다", async () => {
    const { session } = await toAnalysis();
    const v = await session.submit("달라요");
    expect(v.message.startsWith("맞아요! 둘은 달라요.")).toBe(true);
    expect(v.methodSteps?.active).toBe(1);
  });

  it("4문장은 음영 + 대시 흐림. 「다음 문장」이면 자세한 스텝을 건너뛰고, 「자세히 볼래요」면 연다", async () => {
    const walkTo4 = async () => {
      const { session } = await toAnalysis();
      for (const t of ["달라요", "다음 문장", "inventor", "다음 문장", "기술(technique)일 뿐", "다음 문장"]) await session.submit(t);
      return session;
    };
    let session = await walkTo4();
    let v = session.view();
    expect(session.lastAction()?.interactionId).toBe("s4_skim");
    expect(v.shaded).toEqual([L.sentences[3]!.text]);
    expect(v.faded?.[0]).toContain("automobile");
    expect(v.buttons).toEqual(["다음 문장", "자세히 볼래요"]);
    v = await session.submit("다음 문장");
    expect(session.lastAction()?.interactionId).toBe("s5_skim");

    session = await walkTo4();
    v = await session.submit("자세히 볼래요");
    expect(session.lastAction()?.interactionId).toBe("s4_just_as");
    expect(v.tips?.[0]?.label).toBe("대시 사이 건너뛰기");
  });

  it("6문장의 arms race는 ❓ 개념, last thing은 💡 Tip", async () => {
    const { session } = await toAnalysis();
    for (const t of ["달라요", "다음 문장", "inventor", "다음 문장", "기술(technique)일 뿐", "다음 문장", "다음 문장", "다음 문장"]) await session.submit(t);
    const v = session.view();
    expect(session.lastAction()?.interactionId).toBe("s6_q");
    expect(v.concepts?.[0]?.en).toBe("arms race");
    expect(v.glosses.some((g) => g.en === "arms race")).toBe(true);
    expect(v.tips?.[0]?.label).toBe("last thing");
  });

  it("시험 보기: 다섯 개를 카드로, 틀리면 이유와 함께 지우고, 맞히면 다시 볼 주기 → 단어 → 짝 맞추기", async () => {
    const { session } = await toAnalysis();
    let v = session.view();
    for (let g = 0; g < 40 && !v.examOptions; g++) {
      const id = session.lastAction()?.interactionId ?? "";
      const step = L.sentences.flatMap((x) => x.steps).find((x) => x.id === id);
      v = await session.submit(step?.type === "choice" && v.buttons.length > 1 ? step.options.find((o) => o.correct)!.label : v.buttons[0]!);
    }
    expect(v.examOptions).toHaveLength(5);
    expect(v.buttons).toEqual([]);
    expect(v.examOptions![2]!.keywords).toEqual(["embrace", "novelty", "progress"]);
    expect(v.methodSteps?.active).toBe(2);

    v = await session.submit(L.exam!.options[4]!.label);
    expect(v.message).toBe("아쉽게도 틀렸어요. science는 지도에도 있지만, 글에선 과학을 흉내 내요. 구별하는 게 아니에요.");
    expect(v.examOptions).toHaveLength(4);

    v = await session.submit(L.exam!.options[2]!.label);
    expect(v.screen).toBe("chat");
    // 한 번 틀렸으니 기본 1주
    expect(v.review?.weeks).toBe(1);
    expect(v.message).toContain("1주 뒤에");
    v = await session.submit("__weeks:4");
    expect(v.message).toContain("4주 뒤에");
    v = await session.submit("__weeks:none");
    expect(v.review?.weeks).toBeNull();
    expect(v.message).toBe("알겠어요, 이 지문은 복습 목록에서 뺄게요.");
    v = await session.submit("__save");
    expect(v.review?.saved).toBe(true);

    v = await session.submit("다음으로");
    expect(v.screen).toBe("words");
    expect(v.wordCheck?.step).toBe("본문 단어 1/2");
    expect(v.wordCheck?.words.some((w) => w.en === "pastiche")).toBe(false);
    v = await session.submit("__check:outmoded");
    expect(v.wordCheck?.checked).toEqual(["outmoded"]);
    v = await session.submit("다음으로");
    expect(v.wordCheck?.step).toBe("보기 단어 2/2");
    v = await session.submit("__check:embrace");
    v = await session.submit("다 했어요");
    expect(v.screen).toBe("match");
    // 체크한 단어가 먼저, 나머지는 본문 단어로 8개까지
    expect(v.matchPairs?.slice(0, 2).map((w) => w.en)).toEqual(["outmoded", "embrace"]);
    expect(v.matchPairs).toHaveLength(8);
    v = await session.submit("__match_done");
    expect(v.ended).toBe(true);
  });

  it("한 번에 맞히면 기본 3주, 「잘했어요」로 시작", async () => {
    const { session } = await toAnalysis();
    let v = session.view();
    for (let g = 0; g < 40 && !v.examOptions; g++) {
      const id = session.lastAction()?.interactionId ?? "";
      const step = L.sentences.flatMap((x) => x.steps).find((x) => x.id === id);
      v = await session.submit(step?.type === "choice" && v.buttons.length > 1 ? step.options.find((o) => o.correct)!.label : v.buttons[0]!);
    }
    v = await session.submit(L.exam!.options[2]!.label);
    expect(v.review?.weeks).toBe(3);
    expect(v.message.startsWith("잘했어요.")).toBe(true);
    expect(v.message).toContain("3주 뒤에");
  });
});

describe("2026년 3월 30번 — 어휘 문제", () => {
  const ID = "moeui-2026-03-30-names-and-differences";
  const L = allPolicyLessons().find((l) => l.id === ID)!;

  it("29%가 고른 ③을 고르면 같이 자세히 보고, 어디서 헷갈렸는지 기록한 뒤 문제로 돌아온다", async () => {
    let saved = emptyStudentState();
    const session = createPolicySession(ID, null, {
      loadStudent: emptyStudentState, saveStudent: (st) => { saved = st; }, logEvents() {}, now: () => 0,
    });
    let v = session.view();
    for (let g = 0; g < 5 && !v.buttons.includes("분석하러 갈게요"); g++) v = await session.submit(v.buttons[0]!);
    v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 80 && !v.examOptions; g++) {
      const id = session.lastAction()?.interactionId ?? "";
      const step = L.sentences.flatMap((x) => x.steps).find((x) => x.id === id);
      v = await session.submit(step?.type === "choice" && v.buttons.length > 1 ? step.options.find((o) => o.correct)!.label : v.buttons[0]!);
    }
    expect(v.examOptions).toHaveLength(5);

    v = await session.submit("alike");
    expect(v.message.startsWith("아쉽게도 틀렸어요. ③은 29%나")).toBe(true);
    expect(v.examOptions).toBeNull();
    expect(v.sentence).toContain("③alike");
    v = await session.submit("같이 볼게요");
    expect(v.panel?.kind).toBe("contrast");
    v = await session.submit("다음으로");
    expect(v.buttons).toEqual(["No를 못 봤어요", "yet 앞뒤가 반대인 게 헷갈렸어요", "둘 다요"]);
    v = await session.submit("No를 못 봤어요");
    expect(v.message).toContain("No를 강조해서");
    expect(saved.skills.no_negation).toBeTruthy();
    v = await session.submit("다음으로");
    expect(v.examOptions).toHaveLength(4);
    expect(v.sentence).toBe(L.sentences[0]!.text);
  });
});
