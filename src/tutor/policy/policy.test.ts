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
import type { TutorView } from "../view";

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



/**
 * 「문장 먼저 읽기」를 자동으로 넘기는 세션 — 수업 흐름을 따라가는 테스트용.
 * 읽기 화면 자체는 따로 확인한다 (rawSession)
 */
function autoRead<T extends { submit: (t: string) => Promise<TutorView> }>(session: T): T {
  const submit = session.submit.bind(session);
  session.submit = async (t: string) => {
    let v = await submit(t);
    // 문장을 맞히고 끝낸 칭찬 화면 → 「다음」, 새 문장 읽기 → 「다 읽었어요」
    for (let g = 0; g < 6 && (v.readingFirst || v.celebrate || v.praiseOnly); g++)
      v = await submit(v.praiseOnly ? "__auto_next" : v.celebrate ? v.buttons[0]! : "다 읽었어요");
    return v;
  };
  return session;
}

/** 21번 2문장을 다 맞히는 답 — such cases → discoveries → 자유 해석 → 1·2문장 요지 */
const S2_RIGHT = [
  "앞 문장의 경우, 즉 발명하지 않아도 훌륭한 음악가인 경우",
  "inventor",
  "그런 경우, '위대한 발견'을 기대하는 사람들은 실망하게 될 것이다.",
  "다음으로",
  "좋은 음악은 꼭 새로울 필요는 없다. 음악이 새로워야 한다고 믿는 사람들은 실망하게 될 것이다.",
];

/** 수업을 한 걸음 — 「찾기」는 답을 다 누르고, 고르기는 정답, 그 밖은 첫 버튼(없으면 자동 넘김) */
async function answer(
  session: { submit: (t: string) => Promise<TutorView> },
  v: TutorView,
  step: PolicyStep | undefined,
): Promise<TutorView> {
  if (step?.type === "pick" && v.pick?.open) {
    let x = v;
    for (const a of step.answers.filter((w) => !v.pick!.found.includes(w))) x = await session.submit(`__pick:${a}`);
    return x;
  }
  if (step?.type === "choice" && v.buttons.length > 1) return session.submit(step.options.find((o) => o.correct)!.label);
  if (step?.type === "translate" && v.allowInput) return session.submit(step.model);
  return session.submit(v.buttons[0] ?? "__auto_next");
}

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
          for (const phrase of [...(step.highlight ?? []), ...(step.highlight_alt ?? [])]) expect(shown, step.id).toContain(phrase);
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
      const session = autoRead(createPolicySession(L.id, null, {
        loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0,
      }));
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
    autoRead(createPolicySession(ID, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 }));
  const rawSession = () =>
    createPolicySession(ID, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
  /** 문제 보기 → 「분석하러 갈게요」 → 칠판 풀이법(도입) → 분석 */
  async function toAnalysis() {
    const session = make();
    let v = session.view();
    expect(v.buttons).toEqual(["분석하러 갈게요", "바로 풀어 볼게요"]);
    v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 5 && v.screen !== "study"; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    // 첫 문장은 핵심 단어 4개 찾기부터 — 다 찾으면 s1_q(같은 사람일까요?)
    expect(v.pick?.candidates).toContain("in fact");
    for (const w of ["brilliant musician", "innovator", "without", "inventor"]) v = await session.submit(`__pick:${w}`);
    return { session, v };
  }

  it("한 문장씩 읽는 화면은 없다. 바로 풀기는 지문 미리보기 화면 그대로, 지문 아래 보기를 눌러 고른다", async () => {
    const session = make();
    let v = session.view();
    for (let g = 0; g < 5 && !v.buttons.includes("바로 풀어 볼게요"); g++) v = await session.submit(v.buttons[0]!);
    // 처음 고르는 화면이 곧 「문제 보기」 — 문제, 넘겨 보는 지문, 보기 다섯 개
    expect(v.screen).toBe("read");
    expect(v.passage?.auto).toBe(false);
    expect(v.passage?.title).toContain("밑줄 친");
    expect(v.passage?.options).toHaveLength(5);
    v = await session.submit("바로 풀어 볼게요");
    // 화면은 그대로(지문 미리보기), 보기만 누를 수 있게 된다
    expect(v.screen).toBe("read");
    expect(v.passage?.pickable).toBe(true);
    expect(v.message.startsWith("실제 시험처럼")).toBe(true);
    expect(v.buttons).toEqual([]);

    // 틀리면 답을 말하지 않고 분석으로
    v = await session.submit(L.exam!.options[0]!.label);
    expect(v.message).toBe("아쉽게도 틀렸어요. 정답은 분석하면서 같이 찾아봐요.");
    expect(v.screen).toBe("read");
    expect(v.passage?.pickable).toBe(false);
    expect(v.passage?.picked).toBe("1");
    v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 5 && v.screen !== "study"; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(session.lastAction()?.interactionId).toBe("s1_pick");
  });

  it("바로 풀어서 맞히면 꼼꼼히 분석 · 핵심만 정리 · 여기서 끝 중에 고른다. 끝내면 다시 볼 주기 없이 종료", async () => {
    const session = make();
    let v = session.view();
    await session.submit("바로 풀어 볼게요");
    v = await session.submit(L.exam!.options[2]!.label);
    expect(v.message.startsWith("맞았어요!")).toBe(true);
    expect(v.passage?.right).toBe("3");
    expect(v.buttons).toEqual(["제대로 분석", "핵심 정리", "끝내기"]);
    v = await session.submit("끝내기");
    expect(v.ended).toBe(true);
  });

  it("「핵심만 정리」는 마지막 단어 지도, 수업의 💡·❓ 표현, 주요 단어를 한 화면에", async () => {
    const session = make();
    let v = session.view();
    await session.submit("바로 풀어 볼게요");
    await session.submit(L.exam!.options[2]!.label);
    v = await session.submit("핵심 정리");
    expect(v.screen).toBe("summary");
    expect(v.summary?.board?.kind).toBe("groups");
    expect(v.summary?.expressions.some((e) => e.label === "arms race")).toBe(true);
    expect(v.summary?.expressions.some((e) => e.label === "last thing")).toBe(true);
    expect(v.summary?.words.length).toBeGreaterThan(0);
    v = await session.submit("다 봤어요");
    expect(v.ended).toBe(true);
  });

  it("바로 맞히고 「꼼꼼히 분석할게요」면 분석 뒤 마지막 문제는 다시 풀지 않고 보기마다 해설만", async () => {
    const session = make();
    let v = session.view();
    await session.submit("바로 풀어 볼게요");
    await session.submit(L.exam!.options[2]!.label);
    v = await session.submit("제대로 분석");
    for (let g = 0; g < 80 && !v.examOptions && !v.examExplain; g++) {
      const id = session.lastAction()?.interactionId ?? "";
      const step = L.sentences.flatMap((x) => x.steps).find((x) => x.id === id);
      v = await answer(session, v, step);
    }
    expect(v.examExplain?.["3"]?.correct).toBe(true);
    expect(v.examExplain?.["3"]?.text.startsWith("음악가도")).toBe(true);
    expect(v.buttons).toEqual(["다음으로"]);
    v = await session.submit("다음으로");
    expect(v.review?.weeks).toBeNull();
  });

  it("처음엔 문제 보기(문제·지문 전체·보기), 「분석하러 갈게요」 뒤에 칠판 풀이법 + 말풍선, 그다음 분석", async () => {
    const session = make();
    let v = session.view();
    expect(v.screen).toBe("read");
    expect(v.passage?.title).toContain("밑줄 친");
    v = await session.submit("분석하러 갈게요");
    // 먼저 글 내용을 한 줄로 암시한다 — 칠판엔 「음악 ? 새로움」
    expect(v.boardImage?.src).toBe("/assets/music-novelty.svg");
    expect(v.message).toBe("좋은 음악은 새로워야 할까요? 이번 글은 음악과 새로움의 관계를 다뤄요.");
    expect(v.tapToNext).toBe(true);
    v = await session.submit("네");
    expect(v.message).toBe("수능 문제는 시간 싸움이에요.");
    expect(v.boardImage?.src).toBe("/assets/underline-method.svg");
    v = await session.submit("네");
    expect(v.message).toContain("핵심 단어 위주로");
    expect(v.skipButton).toBe("넘어가기");
    v = await session.submit("좋아요");
    // 도입이 끝나면 바로 첫 문장 읽기로
    expect(v.screen).toBe("study");
    expect(v.message).toContain("핵심 단어 4개를 찾아볼까요?");
    const { v: first } = await toAnalysis();
    expect(first.screen).toBe("study");
    expect(first.methodSteps).toEqual({ labels: ["핵심 단어 찾기", "관계 잡기"], active: 0 });
  });

  it("문장을 맞히고 끝내면 칭찬만 한 화면(「다음」), 그다음 「이제 두 번째 문장을 읽어 봐요.」 — 문장 위엔 「문장 N」", async () => {
    const session = rawSession();
    let v = await session.submit("분석하러 갈게요");
    v = await session.submit("넘어가기");
    expect(v.sentenceTag).toBe("문장 1");
    expect(v.message).toContain("먼저 문장을 읽어 봐요.");
    v = await session.submit("다 읽었어요");
    for (const w of ["brilliant musician", "innovator", "without", "inventor"]) v = await session.submit(`__pick:${w}`);
    expect(v.praiseOnly).toBe(true);
    v = await session.submit("__auto_next");
    v = await session.submit("대조");
    v = await session.submit("__auto_next");
    v = await session.submit("다음");
    v = await session.submit("뛰어난 음악가는 엄밀히 말해 발명가가 아니어도 혁신가일 수 있다");
    expect(v.celebrate).toBe(true);
    expect(v.message).toBe("맞아요! 첫 번째 문장을 아주 잘 이해했어요!");
    expect(v.sentenceTag).toBe("문장 1");
    expect(v.buttons).toEqual(["다음으로"]);
    v = await session.submit("다음으로");
    expect(v.celebrate).toBe(false);
    expect(v.readingFirst).toBe(true);
    expect(v.sentenceTag).toBe("문장 2");
    expect(v.message).toBe("이제 두 번째 문장을 읽어 봐요.");
  });

  it("2문장: such cases → discoveries → 자유 해석(규칙으로 채점, 틀린 곳·고친 곳 표시) → 1·2문장 요지", async () => {
    const { session } = await toAnalysis();
    for (const t of ["대조", "다음", "뛰어난 음악가는 엄밀히 말해 발명가가 아니어도 혁신가일 수 있다"]) await session.submit(t);
    let v = session.view();
    expect(session.lastAction()?.interactionId).toBe("s2_cases");
    expect(v.message).toBe("'In such cases'가 의미하는 건 뭘까요?");
    expect(v.highlight).toEqual(["In such cases"]);
    v = await session.submit("앞 문장의 경우, 즉 발명하지 않아도 훌륭한 음악가인 경우");
    expect(v.message).toContain("discoveries는");
    v = await session.submit("inventor");
    expect(v.message).toBe("그럼 이 문장을 자유롭게 해석해 봐요.");
    expect(v.allowInput).toBe(true);
    v = await session.submit("이런 케이스에서 위대한 발견을 기대하는 그것들은 실망한다");
    expect(v.allowInput).toBe(false);
    expect(v.message.startsWith("아쉽게도 틀렸어요.")).toBe(true);
    const t = v.translation!;
    expect(t.save).toBe(true);
    expect(t.marks.map(([a, b]) => t.mine!.slice(a, b))).toEqual(["케이스", "그것들은", "실망한다"]);
    expect(t.fixes).toEqual(["사람들은", "실망하게 될 것이다", "그런 경우"]);
    expect(t.notes).toHaveLength(3);
    v = await session.submit("다음으로");
    expect(v.sentenceTag).toBe("문장 1·2");
    expect(v.message).toBe("자, 그럼 문장 1과 2를 모두 읽고 저자가 하고자 하는 말을 골라 볼까요?");
    expect(v.sentence).toContain("A brilliant musician");
    expect(v.sentence).toContain("will be disappointed");
  });

  it("자유 해석 — 고칠 곳이 없으면 칭찬하고 저장하지 않는다", async () => {
    const { session } = await toAnalysis();
    for (const t of ["대조", "다음", "뛰어난 음악가는 엄밀히 말해 발명가가 아니어도 혁신가일 수 있다", S2_RIGHT[0]!, "inventor"]) await session.submit(t);
    const v = await session.submit("그런 경우에 위대한 발견을 기대하는 사람들은 실망할 것이다");
    expect(v.message).toBe("잘 해석했어요! 고칠 곳이 없어요.");
    expect(v.translation?.save).toBe(false);
    expect(v.translation?.marks).toEqual([]);
  });

  it("도입 중 「넘어가기」를 누르면 남은 도입을 건너뛰고 첫 문장으로", async () => {
    const session = rawSession();
    let v = await session.submit("분석하러 갈게요");
    expect(v.message).toContain("음악과 새로움");
    v = await session.submit("넘어가기");
    expect(v.screen).toBe("study");
    expect(v.readingFirst).toBe(true);
  });

  it("문장 학습 위의 ‹ › 로 이전 문장으로 돌아가거나 다음 문장으로 넘긴다. 「전체 지문」도 있다", async () => {
    const { session } = await toAnalysis();
    let v = session.view();
    expect(v.fullPassage?.sentences).toHaveLength(7);
    expect(v.canPrevSentence).toBe(false);
    v = await session.submit("__next_sentence");
    expect(v.progressIndex).toBe(2);
    expect(session.lastAction()?.interactionId).toBe("s2_cases");
    v = await session.submit("__prev_sentence");
    expect(v.progressIndex).toBe(1);
    expect(session.lastAction()?.interactionId).toBe("s1_pick");
    for (let i = 0; i < 7; i++) v = await session.submit("__next_sentence");
    expect(v.examOptions).toHaveLength(5);
  });

  it("문장마다 처음엔 영어 문장만 — 질문·보기·강조는 「다 읽었어요」 뒤에. 읽은 문장은 다시 묻지 않는다", async () => {
    const session = rawSession();
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 6 && v.screen !== "study"; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(v.readingFirst).toBe(true);
    expect(v.message.endsWith("먼저 문장을 읽어 봐요.")).toBe(true);
    expect(v.buttons).toEqual(["다 읽었어요"]);
    expect(v.pick).toBeNull();
    expect(v.emphasis).toEqual([]);
    expect(v.readDelayMs).toBeGreaterThanOrEqual(2000);
    v = await session.submit("다 읽었어요");
    expect(v.readingFirst).toBe(false);
    expect(v.pick?.open).toBe(true);
    // 다음 문장으로 갔다가 돌아오면 다시 읽기를 묻지 않는다
    v = await session.submit("__next_sentence");
    expect(v.readingFirst).toBe(true);
    v = await session.submit("__prev_sentence");
    expect(v.readingFirst).toBe(false);
  });

  it("첫 문장은 후보 구절 중 핵심 단어 4개를 직접 찾는다. 틀린 후보는 이유를 말하고 계속 찾게 한다", async () => {
    const session = make();
    let v = session.view();
    v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 5 && v.screen !== "study"; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(v.pick?.open).toBe(true);
    expect(v.buttons).toEqual(["잘 모르겠어요"]);
    v = await session.submit("__pick:in fact");
    expect(v.message.startsWith("아쉽게도 틀렸어요.")).toBe(true);
    expect(v.pick?.missed).toEqual(["in fact"]);
    v = await session.submit("__pick:innovator");
    expect(v.message).toBe("좋아요! 3개 남았어요.");
    v = await session.submit("__pick:without");
    v = await session.submit("__pick:inventor");
    v = await session.submit("__pick:brilliant musician");
    expect(session.lastAction()?.interactionId).toBe("s1_q");
    expect(v.message).toBe("innovator와 inventor의 관계는 어떨까요?");
    expect(v.tips?.[0]?.label).toBe("힌트");
  });

  it("첫 문장 — innovator·inventor 관계(유의어/대조). 💡 힌트는 위 칩에서 바로 열리고(기록됨), 지도 뒤에 문장 해석", async () => {
    const { session, v: first } = await toAnalysis();
    expect(first.buttons).not.toContain("힌트 주세요");
    const hint = first.tips?.find((t) => t.hint);
    expect(hint?.label).toBe("힌트");
    expect(hint?.text).toBe("innovator와 inventor가 without(~없이)으로 이어져 있어요.");
    session.observe({ kind: "hint_open" });
    let v = await session.submit("대조");
    expect(session.lastAction()?.interactionId).toBe("s1_map");
    // 힌트를 봤으니 혼자 맞힌 게 아니다 — 수업 끝 헷갈린 포인트에 남는다
    v = await session.submit("다음");
    expect(v.message).toBe("이제 문장을 해석해 봐요. 어떤 뜻일까요?");
  });

  it("틀리면 「아쉽게도 틀렸어요.」 + 이유, 다시 고르게 하지 않고 넘어간다", async () => {
    const { session } = await toAnalysis();
    let v = await session.submit("유의어(비슷)");
    expect(v.message).toBe("아쉽게도 틀렸어요. without을 봐요. inventor가 '아니면서도' innovator일 수 있대요. 둘은 반대되는 관계예요.");
    expect(v.buttons).toEqual(["다음으로"]);
    v = await session.submit("다음으로");
    expect(v.message.startsWith("둘은 달라요.")).toBe(true);
    expect(v.panel?.kind).toBe("groups");
  });

  it("맞았다는 말과 다음 말은 따로 — 칭찬만 한 화면(버튼 없이 잠깐) 뒤에 다음 말", async () => {
    const session = rawSession();
    let v = await session.submit("분석하러 갈게요");
    v = await session.submit("넘어가기");
    v = await session.submit("다 읽었어요");
    for (const w of ["brilliant musician", "innovator", "without", "inventor"]) v = await session.submit(`__pick:${w}`);
    expect(v.message).toBe("다 찾았어요!");
    expect(v.buttons).toEqual([]);
    expect(v.autoNextMs).toBeGreaterThan(0);
    v = await session.submit("__auto_next");
    expect(v.message).toBe("innovator와 inventor의 관계는 어떨까요?");
    v = await session.submit("대조");
    expect(v.message).toBe("맞아요!");
    expect(v.praiseOnly).toBe(true);
    v = await session.submit("__auto_next");
    expect(v.message.startsWith("둘은 달라요.")).toBe(true);
    expect(v.methodSteps?.active).toBe(1);
  });

  it("4문장은 음영 + 대시 흐림. 「다음 문장」이면 자세한 스텝을 건너뛰고, 「자세히 볼래요」면 연다", async () => {
    const walkTo4 = async () => {
      const { session } = await toAnalysis();
      for (const t of ["대조", "다음", "뛰어난 음악가는 엄밀히 말해 발명가가 아니어도 혁신가일 수 있다", ...S2_RIGHT, "기술(technique)일 뿐", "다음 문장"]) await session.submit(t);
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
    expect(v.tips?.[0]?.label).toBe("콤마·대시 사이 건너뛰기");
  });

  it("6문장의 arms race는 ❓ 개념, last thing은 💡 Tip", async () => {
    const { session } = await toAnalysis();
    for (const t of ["대조", "다음", "뛰어난 음악가는 엄밀히 말해 발명가가 아니어도 혁신가일 수 있다", ...S2_RIGHT, "기술(technique)일 뿐", "다음 문장", "다음 문장", "다음 문장"]) await session.submit(t);
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
      v = await answer(session, v, step);
    }
    expect(v.examOptions).toHaveLength(5);
    expect(v.buttons).toEqual([]);
    expect(v.examOptions![2]!.keywords).toEqual(["embrace", "novelty", "progress"]);
    expect(v.methodSteps?.active).toBe(1);

    v = await session.submit(L.exam!.options[4]!.label);
    expect(v.message).toBe("아쉽게도 틀렸어요. science는 지도에도 있지만, 글에선 과학을 흉내 내요. 구별하는 게 아니에요.");
    expect(v.examOptions).toHaveLength(4);

    v = await session.submit(L.exam!.options[2]!.label);
    // 정답 해설 한 화면 → 「다음으로」면 다시 볼 주기
    expect(v.message.startsWith("정답이에요!")).toBe(true);
    v = await session.submit("다음으로");
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
    // 헷갈린 곳(⑤를 골랐다)을 한 줄로 정리하고, 별표로 노트에 저장할 수 있다
    expect(v.screen).toBe("points");
    expect(v.pointsReview?.items.map((p) => p.title)).toEqual(["문제 ⑤"]);
    v = await session.submit("다 봤어요");
    expect(v.ended).toBe(true);
  });

  it("한 번에 맞히면 기본 3주, 「잘했어요」로 시작", async () => {
    const { session } = await toAnalysis();
    let v = session.view();
    for (let g = 0; g < 40 && !v.examOptions; g++) {
      const id = session.lastAction()?.interactionId ?? "";
      const step = L.sentences.flatMap((x) => x.steps).find((x) => x.id === id);
      v = await answer(session, v, step);
    }
    v = await session.submit(L.exam!.options[2]!.label);
    // 정답 해설 한 화면 → 「다음으로」면 다시 볼 주기
    expect(v.message.startsWith("정답이에요!")).toBe(true);
    v = await session.submit("다음으로");
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
    const session = autoRead(createPolicySession(ID, null, {
      loadStudent: emptyStudentState, saveStudent: (st) => { saved = st; }, logEvents() {}, now: () => 0,
    }));
    let v = session.view();
    for (let g = 0; g < 5 && !v.buttons.includes("분석하러 갈게요"); g++) v = await session.submit(v.buttons[0]!);
    v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 80 && !v.examOptions; g++) {
      const id = session.lastAction()?.interactionId ?? "";
      const step = L.sentences.flatMap((x) => x.steps).find((x) => x.id === id);
      v = await answer(session, v, step);
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
