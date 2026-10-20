import { describe, expect, it } from "vitest";
import { decideOnChoice, shouldShow, type DecideInput } from "./decide";
import { stamps } from "./copy";
import { allPolicyLessons, getPolicyCopy } from "./lessons";
import { createPolicySession as realCreatePolicySession, gradeTranslation, underlinesOf } from "./session";
import { SENSE_WORDS, sensesOf } from "./senses";
import {
  emptyStudentState,
  recordPerformance,
  skillOf,
} from "./student-state";
import type { ChoiceStep, PolicyStep, TranslateStep } from "./types";
import type { TutorView } from "../view";
import { CONTEXT_WORDS, FUNCTION_WORDS, WORDS, glossSpans, splitPhraseGlosses } from "../glosses";

/**
 * 긴 문장의 초급용 주어·동사 찾기(`*_basic_sv`)는 이제 모든 단계에 나온다(2026-10-16 선생님).
 * 원래 흐름을 보는 테스트가 그 화면에 걸리지 않게 — 그 찾기는 정답으로 저절로 지나간다. 초급 테스트는 `realCreatePolicySession`
 */
function createPolicySession(...args: Parameters<typeof realCreatePolicySession>) {
  const session = realCreatePolicySession(...args);
  const lesson = allPolicyLessons().find((l) => l.id === args[0]);
  const steps = new Map((lesson?.sentences ?? []).flatMap((s) => s.steps).map((st) => [st.id, st]));
  const passBasicSv = async (v: TutorView): Promise<TutorView> => {
    for (let g = 0; g < 6; g++) {
      const id = session.lastAction()?.interactionId ?? "";
      const st = steps.get(id);
      if (v.readingFirst || !v.pick?.open || !(id.endsWith("_basic_sv") || id.endsWith("_that_sv")) || st?.type !== "pick") return v;
      for (const a of st.answers) v = await session.submit(`__pick:${a}`);
      if (v.praiseOnly) v = await session.submit("__auto_next");
    }
    return v;
  };
  return { ...session, submit: async (text: string) => passBasicSv(await session.submit(text)) };
}

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

    it("「찾기」 후보는 화면의 문장에서 따로 누를 수 있다 (뜻이 달린 칸 하나와 딱 맞는다)", () => {
      for (const sen of L.sentences) {
        for (const step of sen.steps) {
          // 순서 잇기는 문장이 아니라 단락 카드를 고른다
          if (step.type !== "pick" || step.order) continue;
          const shown = step.display ?? sen.text;
          // 화면처럼 — 지금 고르는 후보 구절은 그대로, 나머지 구절 뜻은 단어마다 나뉜다
          const spans = glossSpans(shown, splitPhraseGlosses(sen.glosses, step.candidates)).filter((x) => x.gloss).map((x) => x.text.replace(/[.,;:!?]+$/, ""));
          for (const c of step.candidates) expect(spans, `${step.id}: ${c}`).toContain(c);
        }
      }
    });

    it("흐림(삽입)은 대시(—)가 두 개일 때만 — 대시 하나로 시작하는 구절은 생략하지 않는다", () => {
      for (const sen of L.sentences) {
        for (const step of sen.steps) {
          for (const f of step.faded ?? []) {
            if (f.trim().startsWith("—")) expect(f.trim().slice(1), `${step.id}: ${f}`).toContain("—");
          }
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

  it("바로 풀어서 맞히면 「분석하기」「다음 문제로」 둘 중에 고른다. 다음 문제로 가면 다시 볼 주기 없이 종료", async () => {
    const session = make();
    let v = session.view();
    await session.submit("바로 풀어 볼게요");
    v = await session.submit(L.exam!.options[2]!.label);
    expect(v.message.startsWith("맞았어요!")).toBe(true);
    expect(v.passage?.right).toBe("3");
    expect(v.buttons).toEqual(["분석하기", "다음 문제로"]);
    v = await session.submit("다음 문제로");
    expect(v.ended).toBe(true);
  });

  // 「핵심 정리」 버튼은 2026-10-20 화면에서 뺐다 — 세션은 아직 받는다
  it.skip("「핵심만 정리」는 마지막 단어 지도, 수업의 💡·❓ 표현, 주요 단어를 한 화면에", async () => {
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
    v = await session.submit("분석하기");
    for (let g = 0; g < 80 && !v.examOptions && !v.examExplain; g++) {
      const id = session.lastAction()?.interactionId ?? "";
      const step = L.sentences.flatMap((x) => x.steps).find((x) => x.id === id);
      v = await answer(session, v, step);
    }
    expect(v.examExplain?.["3"]?.correct).toBe(true);
    expect(v.examExplain?.["3"]?.text.startsWith("음악가도")).toBe(true);
    expect(v.buttons).toEqual(["다음으로"]);
    v = await session.submit("다음으로");
    // 「다시 볼 주기」 화면은 없다 — 바로 단어 체크
    expect(v.review).toBeFalsy();
    expect(v.screen).toBe("words");
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

  it("자유 해석 — 「잘 모르겠어요」는 밑줄 글자. 누르면 단어를 눌러 보며 써 보자고 하고, 그다음에야 「답 바로 보기」", async () => {
    const { session } = await toAnalysis();
    for (const t of ["대조", "다음", "뛰어난 음악가는 엄밀히 말해 발명가가 아니어도 혁신가일 수 있다", S2_RIGHT[0]!, "inventor"]) await session.submit(t);
    let v = session.view();
    expect(v.buttons).toEqual([]);
    expect(v.linkButtons).toEqual(["잘 모르겠어요"]);
    v = await session.submit("잘 모르겠어요");
    expect(v.message).toContain("모르는 단어를 하나씩 눌러 뜻을 보고");
    expect(v.translation).toBeNull();
    expect(v.linkButtons).toEqual(["답 바로 보기"]);
    v = await session.submit("답 바로 보기");
    expect(v.translation?.model).toBeTruthy();
    expect(v.linkButtons).toEqual([]);
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
    // 「다 읽었어요」는 잠깐 기다렸다가 — 1.2~3.5초
    expect(v.readDelayMs).toBeGreaterThanOrEqual(1200);
    expect(v.readDelayMs).toBeLessThanOrEqual(3500);
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
    // 「잘 모르겠어요」는 큰 버튼이 아니라 밑줄 글자
    expect(v.buttons).toEqual([]);
    expect(v.linkButtons).toEqual(["잘 모르겠어요"]);
    v = await session.submit("__pick:in fact");
    // 핵심어 고르기는 틀렸다고 하지 않는다 — 더 좋은 선택이 있다고만
    expect(v.message.startsWith("더 좋은 선택이 있어요.")).toBe(true);
    expect(v.message).not.toContain("틀렸어요");
    expect(v.pick?.missed).toEqual(["in fact"]);
    expect(v.pick?.soft).toBe(true);
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
      for (const t of ["대조", "다음", "뛰어난 음악가는 엄밀히 말해 발명가가 아니어도 혁신가일 수 있다", ...S2_RIGHT, "다음 문장", "기술(technique)일 뿐", "다음 문장"]) await session.submit(t);
      return session;
    };
    let session = await walkTo4();
    let v = session.view();
    expect(session.lastAction()?.interactionId).toBe("s4_skim");
    expect(v.shaded).toEqual([L.sentences[3]!.text]);
    expect(v.faded?.[0]).toContain("automobile");
    expect(v.buttons).toEqual(["다음 문장", "자세히 볼래요"]);
    v = await session.submit("다음 문장");
    expect(session.lastAction()?.interactionId).toBe("story_4");
    v = await session.submit("다음 문장");
    expect(session.lastAction()?.interactionId).toBe("s5_skim");

    session = await walkTo4();
    v = await session.submit("자세히 볼래요");
    expect(session.lastAction()?.interactionId).toBe("s4_just_as");
    expect(v.tips?.[0]?.label).toBe("콤마(,)·대시(—) 사이 건너뛰기");
  });

  it("6문장의 arms race는 ❓ 개념, last thing은 💡 Tip", async () => {
    const { session } = await toAnalysis();
    for (const t of ["대조", "다음", "뛰어난 음악가는 엄밀히 말해 발명가가 아니어도 혁신가일 수 있다", ...S2_RIGHT, "다음 문장", "기술(technique)일 뿐", "다음 문장", "다음 문장", "다음 문장", "다음 문장"]) await session.submit(t);
    const v = session.view();
    expect(session.lastAction()?.interactionId).toBe("s6_q");
    expect(v.concepts?.[0]?.en).toBe("arms race");
    expect(v.glosses.some((g) => g.en === "arms race")).toBe(true);
    expect(v.tips?.[0]?.label).toBe("last thing");
  });

  it("시험 보기: 다섯 개를 카드로, 한 번 제출하면 정답을 밝히고 보기마다 짧은 해설 → 다시 볼 주기 → 단어 → 짝 맞추기", async () => {
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

    // 틀린 보기를 제출 — 다시 고르게 하지 않고 정답을 밝힌다. 보기마다 짧은 해설이 다 펼쳐진다 (2026-10-20 선생님)
    v = await session.submit(L.exam!.options[4]!.label);
    expect(v.message).toBe("아쉽게도 틀렸어요. 정답은 ③예요.");
    expect(v.examOptions).toHaveLength(5);
    expect(v.examExplainOpen).toBe(true);
    expect(v.examExplain?.["5"]).toMatchObject({ correct: false, picked: true });
    expect(v.examExplain?.["5"]?.text).toBe("science는 지도에도 있지만, 글에선 과학을 흉내 내요. 구별하는 게 아니에요.");
    expect(v.examExplain?.["3"]?.correct).toBe(true);
    v = await session.submit("다음으로");
    // 「다시 볼 주기」 화면 없이 바로 단어 체크
    expect(v.review).toBeFalsy();
    expect(v.screen).toBe("words");
    expect(v.wordCheck?.step).toBe("본문 단어 1/2");
    expect(v.wordCheck?.words.some((w) => w.en === "pastiche")).toBe(false);
    v = await session.submit("__check:outmoded");
    expect(v.wordCheck?.checked).toEqual(["outmoded"]);
    // 끌어서 여러 개 — 켜고 끄기, 모두 고르기·모두 풀기
    const ens = v.wordCheck!.words.map((w) => w.en);
    v = await session.submit(`__check_set:on:${ens[1]}|${ens[2]}`);
    expect(v.wordCheck?.checked).toEqual(["outmoded", ens[1], ens[2]].filter((x, i, a) => a.indexOf(x) === i));
    v = await session.submit(`__check_set:off:${ens[1]}`);
    expect(v.wordCheck?.checked).not.toContain(ens[1]);
    v = await session.submit("__check_all");
    expect(ens.every((e) => v.wordCheck!.checked.includes(e))).toBe(true);
    v = await session.submit("__check_none");
    expect(v.wordCheck?.checked).toEqual([]);
    v = await session.submit("__check:outmoded");
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
    expect(v.review).toBeFalsy();
    expect(["words", "points", "chat"]).toContain(v.screen);
  });
});

describe("2026년 3월 30번 — 어휘 문제", () => {
  const ID = "moeui-2026-03-30-names-and-differences";
  const L = allPolicyLessons().find((l) => l.id === ID)!;

  it("29%가 고른 ③을 제출하면 해설 아래 「같이 자세히 볼래요」 — 고르면 설명 한 화면을 보고(어디서 헷갈렸는지는 안 묻는다) 보기 해설로 돌아온다", async () => {
    const session = autoRead(createPolicySession(ID, null, {
      loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0,
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
    expect(v.message.startsWith("아쉽게도 틀렸어요. 정답은")).toBe(true);
    expect(v.examExplain?.["3"]?.picked).toBe(true);
    expect(v.buttons).toEqual(["다음으로", "같이 자세히 볼래요"]);
    v = await session.submit("같이 자세히 볼래요");
    expect(v.examOptions).toBeNull();
    expect(v.sentence).toContain("③alike");
    expect(v.panel?.kind).toBe("contrast");
    v = await session.submit("다음으로");
    expect(v.message).not.toContain("헷갈렸어요?");
    // 다시 고르지 않는다 — 다섯 보기와 해설이 그대로, 「다음으로」면 마무리로
    expect(v.examOptions).toHaveLength(5);
    expect(v.examExplain?.["3"]?.picked).toBe(true);
    expect(v.buttons).toEqual(["다음으로"]);
  });
});

describe("2026년 3월 24번 — 제목 문제", () => {
  const ID24 = "moeui-2026-03-24-translation-strangeness";
  const L24 = () => allPolicyLessons().find((l) => l.id === ID24)!;
  const raw = () =>
    createPolicySession(ID24, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
  /** 핵심어 자유 해석을 뺀 문장은 읽자마자 해석 맞추기 — 칸마다 맞는 덩어리를 놓고 칭찬 화면을 넘긴다 */
  async function solveMatch(session: ReturnType<typeof raw>, v: Awaited<ReturnType<typeof session.submit>>) {
    if (!v.pick?.match) return v;
    const slots = v.pick.match.ko.filter((x): x is { en: string; ko: string } => typeof x !== "string");
    for (const [i, sl] of slots.entries()) v = await session.submit(`__match:${i}:${sl.en}`);
    if (v.praiseOnly) v = await session.submit("__auto_next");
    return v;
  }

  it("1문장: accessible X / evaporates O → 예술의 역할 자유 응답(힌트 its) → 핵심어 6개 찾기 → 핵심어만으로 해석", async () => {
    const session = raw();
    let v = await session.submit("분석하러 갈게요");
    v = await session.submit("넘어가기");
    expect(v.readingFirst).toBe(true);
    v = await session.submit("다 읽었어요");
    expect(v.concepts?.map((c) => c.en)).toEqual(["domesticated", "take it for granted"]);
    // 핵심어는 마지막에 직접 찾는다 — 미리 색칠하지 않는다
    expect(v.emphasis).toEqual([]);
    // 핵심어 자유 해석을 뺀 문장 — 해석 맞추기가 먼저 (2026-10-20)
    expect(v.pick?.match).toBeTruthy();
    v = await solveMatch(session, v);
    // 뜻 질문(사라져 버린다)은 맞추기가 대신한다 — 바로 대조 칠판
    expect(v.panel?.kind).toBe("contrast");
    v = await session.submit("다음");
    expect(v.message).toBe("그럼 예술(art)의 역할은 뭘까요? 자유롭게 써 봐요.");
    expect(v.allowInput).toBe(true);
    expect(v.tips?.find((t) => t.hint)?.text).toContain("something too domesticated");
    v = await session.submit("예술은 너무 익숙한 것을 다시 보이게 해 준다");
    expect(v.message).toBe("잘 답했어요! 예술은 익숙해서 안 보이던 것을 다시 보이게 해요.");
    expect(v.translation?.labels).toEqual({ mine: "내 답", model: "모범 답" });
    expect(v.tips?.some((t) => t.hint)).toBe(false);
    v = await session.submit("다음으로");
    expect(v.message).toBe("이제 이 문장의 핵심어 6개를 찾아볼까요?");
    for (const w of ["domesticated", "evaporates", "take it for granted", "art", "restores", "visibility"]) v = await session.submit(`__pick:${w}`);
    // 「핵심어만 가지고 해석」(자유 해석)은 뺐다 (2026-10-20) — 칭찬 뒤 바로 문장 마무리
    for (let g = 0; g < 3 && !v.celebrate; g++) v = await session.submit(v.praiseOnly ? "__auto_next" : v.buttons[0] ?? "__auto_next");
    expect(v.allowInput).toBeFalsy();
    expect(v.celebrate).toBe(true);
  });

  it("2문장: this 같은 지시어는 앞 문장에서 — 문장 1을 띄워 음영 구절 중 this task를 고른다(‹ › 로 오감)", async () => {
    const session = raw();
    let v = await session.submit("분석하러 갈게요");
    v = await session.submit("넘어가기");
    v = await session.submit("__next_sentence");
    v = await session.submit("다 읽었어요");
    v = await solveMatch(session, v);
    expect(v.message.startsWith("this처럼 앞에 나온 걸 가리키는 말이 나오면")).toBe(true);
    expect(v.highlight).toEqual(["this task"]);
    v = await session.submit("앞 문장 볼게요");
    expect(v.sentenceTag).toBe("문장 1");
    expect(v.sentence).toBe(L24().sentences[0]!.text);
    expect(v.pick?.shade).toBe(true);
    expect(v.flip).toEqual({ tag: "문장 2", text: L24().sentences[1]!.text, highlight: ["this task"] });
    v = await session.submit("__pick:take it for granted");
    expect(v.message.startsWith("아쉽게도 틀렸어요.")).toBe(true);
    v = await session.submit("__pick:art restores its visibility");
    expect(v.message).toBe("맞아요!");
    v = await session.submit("__auto_next");
    expect(v.sentenceTag).toBe("문장 2");
    expect(v.flip).toBeNull();
    expect(v.message).toBe("this task는 익숙해서 안 보이던 것을 다시 보이게 하는 일이에요.");
    v = await session.submit("다음");
    // 이 일에 잘 맞는 건 — 문장에서 고른다
    expect(v.message).toBe("그럼 this task에 특히 잘 맞는 건 무엇일까요?");
    expect(v.highlight).toEqual(["this task"]);
    v = await session.submit("__pick:art");
    expect(v.message.startsWith("아쉽게도 틀렸어요.")).toBe(true);
    v = await session.submit("__pick:translation");
    v = await session.submit("__auto_next");
    expect(v.message).toBe("이 문장의 핵심어 4개를 찾아볼까요?");
    for (const w of ["translation", "art", "suited", "this task"]) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    // 핵심어만으로 해석(자유 해석)은 뺐다 (2026-10-20) — 바로 문장 마무리
    expect(v.celebrate).toBe(true);
    expect(v.message).toBe("맞아요! 두 번째 문장을 아주 잘 이해했어요!");
  });

  it("3문장: while 두 뜻 → 주어·동사 두 쌍 찾기 → 핵심어 → 해석 보기 → 두 그룹에 끌어 넣기 → 예술에 해당하는 것", async () => {
    const session = raw();
    let v = await session.submit("분석하러 갈게요");
    v = await session.submit("넘어가기");
    v = await session.submit("__next_sentence");
    v = await session.submit("__next_sentence");
    v = await session.submit("다 읽었어요");
    expect(v.buttons).toEqual(["이미 잘 알고 있어요", "다음에 또 알려주세요"]);
    v = await session.submit("다음에 또 알려주세요");
    expect(v.message).toBe("여기서 while은 무슨 뜻일까요?");
    v = await session.submit("~하는 반면에");
    v = await session.submit("__auto_next");
    v = await session.submit("찾아볼게요");
    expect(v.pick?.shade).toBe(true);
    for (const w of ["a great work of literature", "accumulates", "translations of that work", "free"]) {
      v = await session.submit(`__pick:${w}`);
      expect(v.message).toBe("맞아요!");
      v = await session.submit("__auto_next");
    }
    expect(v.panel?.kind).toBe("structure");
    v = await session.submit("다음");
    expect(v.tips?.find((t) => t.hint)?.text).toContain("목적어");
    for (const w of ["a great work of literature", "accumulates", "imitations", "translations of that work", "free", "its stodgy fame"]) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    expect(v.buttons).toHaveLength(4);
    v = await session.submit("위대한 문학 작품은 모방작 같은 것들이 쌓이는 반면, 그 번역본은 작품을 따분한 명성에서 풀어 준다");
    v = await session.submit("__auto_next");
    expect(v.panel?.kind).toBe("groups");
    v = await session.submit("왼쪽 · 익숙해서 안 보임");
    v = await session.submit("__auto_next");
    v = await session.submit("오른쪽 · 다시 보이게 함");
    v = await session.submit("__auto_next");
    expect(v.message.startsWith("아까 예술은")).toBe(true);
    v = await session.submit("__pick:translations of that work");
    if (v.praiseOnly) v = await session.submit("__auto_next");
    // 문장 3 뒤 칠판 정리 — 지금까지 장면이 쌓이고 이번 장면만 노랗게
    expect(v.panel?.kind).toBe("story");
    if (v.panel?.kind === "story") expect(v.panel.scenes.filter((x) => x.fresh)).toHaveLength(2);
    v = await session.submit("다음 문장");
    expect(v.sentenceTag).toBe("문장 4");
  });

  it("4문장: one(앞의 text) → 낯섦이 없는 글 → 좋은 말(+)인지(−·−·+ 표시) → native strangeness는 다시 보이게 하는 쪽 → 아무 일도 안 일어남 → 핵심어 → 해석", async () => {
    const session = raw();
    let v = await session.submit("분석하러 갈게요");
    v = await session.submit("넘어가기");
    for (let i = 0; i < 3; i++) v = await session.submit("__next_sentence");
    v = await session.submit("다 읽었어요");
    v = await solveMatch(session, v);
    expect(v.message).toBe("여기서 one은 무슨 뜻일까요?");
    expect(v.faded).toEqual(["in Berman’s terms"]);
    v = await session.submit("앞의 text를 다시 받는 '것(글)'");
    if (v.praiseOnly) v = await session.submit("__auto_next");
    // 뜻 질문('본래의 낯섦'이 없는 글)은 맞추기를 한 문장에선 건너뛴다
    if (!v.message.startsWith("그럼 native strangeness")) {
      v = await session.submit("'본래의 낯섦'이 없는 글");
      if (v.praiseOnly) v = await session.submit("__auto_next");
    }
    expect(v.message).toBe("그럼 native strangeness(본래의 낯섦)는 좋은 말일까요, 나쁜 말일까요?");
    expect(v.signs).toEqual([]);
    v = await session.submit("나쁜 말 (−)");
    expect(v.message.startsWith("아쉽게도 틀렸어요.")).toBe(true);
    v = await session.submit("다음으로");
    // 설명 화면 — bad text −, lacks −, native strangeness +
    expect(v.signs?.map((x) => `${x.text}${x.sign}`)).toEqual(["A bad text−", "lacks−", "native strangeness+"]);
    v = await session.submit("다음");
    expect(v.panel?.kind).toBe("groups");
    v = await session.submit("오른쪽 · 다시 보이게 함");
    v = await session.submit("__auto_next");
    v = await session.submit("아무 일도 일어나지 않는다");
    v = await session.submit("__auto_next");
    // 뜻 설명(극복할 게 아니라)은 맞추기를 한 문장에선 건너뛴다 — 바로 핵심어 찾기
    if (!v.message.includes("핵심어")) v = await session.submit("다음");
    expect(v.message).toBe("이 문장의 핵심어 4개를 찾아볼까요?");
    for (const w of ["A bad text", "lacks", "native strangeness", "nothing happens"]) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    // 핵심어만으로 해석(자유 해석)은 뺐다 (2026-10-20)
    expect(v.message).toBe("맞아요! 네 번째 문장을 아주 잘 이해했어요!");
  });

  it("5~7문장: 주어·it·이미 내재된 자질 → not A but B·괄호 건너뛰기 → make+목적어+seem → 글 전체 한 줄 → 문제", async () => {
    const session = raw();
    let v = await session.submit("분석하러 갈게요");
    v = await session.submit("넘어가기");
    for (let i = 0; i < 4; i++) v = await session.submit("__next_sentence");
    expect(v.sentenceTag).toBe("문장 5");
    v = await session.submit("다 읽었어요");
    const go = async (t: string) => {
      v = await session.submit(t);
      if (v.praiseOnly) v = await session.submit("__auto_next");
      return v;
    };
    v = await solveMatch(session, v);
    await go("__pick:The translation of a true work of art");
    await go("번역 (The translation)");
    await go("작품 안에 이미 있던 것");
    expect(v.signs?.map((x) => x.sign)).toEqual(["+", "+"]);
    await go("다음");
    for (const w of ["The translation of a true work of art", "significant", "reinforces", "enhances", "qualities", "inherent"]) await go(`__pick:${w}`);
    // 핵심어만으로 해석(자유 해석)은 뺐다 (2026-10-20) — 문장 6으로, 읽고 나면 해석 맞추기부터
    for (let g = 0; g < 4 && v.sentenceTag !== "문장 6"; g++) await go(v.buttons[0] ?? "__auto_next");
    await go("다 읽었어요");
    v = await solveMatch(session, v);
    // 문장 6 — 괄호 속 덧붙임만 흐림, 안내도 괄호로
    expect(v.faded?.[0]).toContain("Heyvaert");
    expect(v.fadedNote).toContain("괄호");
    // 「괄호 건너뛰기」 Tip은 뺀 자유 해석 스텝에 달려 있었다
    await go("A가 아니라 B");
    await go("작품이 우리에게 낯설게 다가오는 방식");
    await go("다음");
    for (const w of ["translation", "makeshift", "the mode of existence", "reaches us", "étrange"]) await go(`__pick:${w}`);
    // 핵심어만으로 해석(자유 해석)은 뺐다 (2026-10-20) — 문장 7로
    for (let g = 0; g < 4 && v.sentenceTag !== "문장 7"; g++) await go(v.buttons[0] ?? "__auto_next");
    // 문장 7 — As Wilson put it은 주어+동사가 있어 흐리지 않는다
    expect(v.faded ?? []).toEqual([]);
    await go("다 읽었어요");
    v = await solveMatch(session, v);
    // 맞추기를 한 문장은 뜻 질문을 건너뛸 수 있다 — 핵심어 찾기까지 넘긴다
    for (let g = 0; g < 6 && !v.pick?.open; g++) await go(v.buttons.find((b) => /낯설게|다시 보이게/.test(b)) ?? v.buttons[0] ?? "__auto_next");
    for (const w of ["translation", "makes", "the work", "more strange", "newly strange"]) await go(`__pick:${w}`);
    // 핵심어만으로 해석(자유 해석)은 뺐다 (2026-10-20)
    for (let g = 0; g < 3 && !v.message.startsWith("다 모으면 이래요."); g++) await go(v.buttons[0] ?? "__auto_next");
    expect(v.message.startsWith("다 모으면 이래요.")).toBe(true);
    await go("문제 풀러 갈게요");
    expect(v.examOptions).toHaveLength(5);
  });

  it("3문장 주어·동사 찾기는 슬래시로 나눠 보이고, 「이미 잘 알고 있어요」면 묻지 않고 이번과 다음 수업에서 건너뛴다", async () => {
    let saved = emptyStudentState();
    const mk = () =>
      createPolicySession(ID24, null, { loadStudent: () => saved, saveStudent(st) { saved = st; }, logEvents() {}, now: () => 0 });
    const toPairs = async (session: ReturnType<typeof mk>) => {
      for (const t of ["분석하러 갈게요", "넘어가기", "__next_sentence", "__next_sentence", "다 읽었어요", "다음에 또 알려주세요", "~하는 반면에"]) {
        await session.submit(t);
      }
      return session.submit("__auto_next");
    };
    let session = mk();
    let v = await toPairs(session);
    expect(v.sentence).toContain("bury it, / translations");
    expect(v.buttons).toEqual(["찾아볼게요", "이미 잘 알고 있어요"]);
    // 묻지 않고 바로 건너뛴다 — 주어·동사 찾기를 건너뛰고 핵심어 찾기로
    v = await session.submit("이미 잘 알고 있어요");
    expect(session.lastAction()?.interactionId).toBe("s3_keys");
    expect(saved.known).toEqual(["clause_pairs"]);
    // 다음 수업 — 설명 자체가 안 뜬다
    session = mk();
    v = await toPairs(session);
    expect(session.lastAction()?.interactionId).toBe("s3_keys");
  });

  it("예술의 역할 — 가리키는 것·보이게 한다가 없으면 짚어 준다", async () => {
    const session = raw();
    let v0 = await session.submit("분석하러 갈게요");
    v0 = await session.submit("넘어가기");
    v0 = await session.submit("다 읽었어요");
    await solveMatch(session, v0);
    await session.submit("다음");
    const v = await session.submit("예술은 사람들을 감동시킨다");
    expect(v.translation?.fixes).toEqual(["너무 익숙해서 당연하게 여기던 것을", "다시 보이게 한다"]);
    expect(v.translation?.save).toBe(true);
  });
});

describe("2026년 3월 36번 — 순서 문제", () => {
  const ID36 = "moeui-2026-03-36-conversation-stoppers";
  it("주어진 글(+로 끝남) → (A) This is a problem → (B) in this manner → (C) The problem → 순서 고르기", async () => {
    const session = createPolicySession(ID36, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    v = await session.submit("넘어가기");
    expect(v.sentenceTag).toBe("주어진 글");
    const go = async (t: string) => {
      v = await session.submit(t);
      // 칠판 정리(2~3문장마다)는 넘긴다 — 따로 검사한다. 해석 맞추기(주어·동사 찾기 대신, 2026-10-20)는 다 채우고 넘긴다
      for (let g = 0; g < 6 && (v.praiseOnly || v.readingFirst || v.celebrate || v.panel?.kind === "story" || v.pick?.match); g++) {
        if (v.pick?.match) {
          const slots = v.pick.match.ko.filter((x): x is { en: string; ko: string } => typeof x !== "string");
          for (const [i, sl] of slots.entries()) v = await session.submit(`__match:${i}:${sl.en}`);
          continue;
        }
        v = await session.submit(v.praiseOnly ? "__auto_next" : v.readingFirst ? "다 읽었어요" : v.buttons[0]!);
      }
      return v;
    };
    await go("다 읽었어요");
    // 주어·동사 찾기는 뺐다 (2026-10-20) — 읽자마자 뜻 질문
    await go("대화를 끝내 주는 역할");
    // 보통은 나쁜 말인데 글은 좋게 본다 — benefit·value로 짚는다
    expect(v.message).toContain("conversation-stoppers(대화를 멈추게 하는 것)");
    // 칠판(story)에 「이점·가치 → +」를 한 줄 더 — go가 넘긴다
    v = await session.submit("좋게 본다 (+)");
    for (let g = 0; g < 2 && v.praiseOnly; g++) v = await session.submit("__auto_next");
    expect(v.panel?.kind).toBe("story");
    expect(v.signs?.[0]).toEqual({ text: "conversation-stoppers", sign: "+" });
    await go("다음");
    // We = 인간 → 앞과 좀 반대인지 묻고 → 칠판 「평소 / 때때로」
    expect(v.message.startsWith("We는 우리 인간이에요.")).toBe(true);
    await go("다음");
    await go("대비되는 내용");
    expect(v.panel?.kind).toBe("groups");
    await go("다음");
    await go("이유를 끝없이 물으면 생기는 문제");
    // (A)를 읽기 전에 한 번 — 시험지 순서라 어색할 수 있다
    for (let g = 0; g < 2 && !v.message.includes("시험지 순서대로"); g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(v.message).toContain("시험지 순서대로");
    expect(v.readingFirst).toBe(false);
    await go("(A)부터 읽어 볼게요");
    expect(v.sentence.startsWith("(A) This")).toBe(true);
    // 「문장 2」가 아니라 (A), 단락의 다른 문장도 함께
    expect(v.sentenceTag).toBe("(A)");
    // (A)는 단락 통째로 — 둘째 문장(부연)도 한 화면에
    expect(v.sentence).toContain("Dennett suggests");
    await go("어떤 '문제'에 대한 설명");
    // 뜻만 짚는다 (질문 없이)
    expect(v.message.startsWith("(A)는 메인 문장 하나와")).toBe(true);
    expect(v.panel?.kind).toBe("structure");
    await go("다음");
    // 메인(problem)과 뒷받침(squelchers)의 관계
    await go("squelchers가 그 문제를 해결해 준다");
    expect(v.signs).toContainEqual({ text: "consideration-generator-squelchers", sign: "+" });
    await go("다음");
    // 단락 끝 — 다음에 올 내용 예측
    await go("그런 말이 실제로 어떻게 쓰이는지 예");
    // (B)는 첫 문장에 집중 — 한 줄 → 받아들이면 어떻게 되나(글에서 직접) → 앞에 올 내용
    expect(v.message.startsWith("첫 문장부터 봐요.")).toBe(true);
    await go("다음");
    await go("더 이상 이유를 찾을 필요가 없다");
    await go("생각을 그 자리에서 멈추게 하는 말이 쓸모 있다");
    await go("이유를 끝없이 물어서 결정을 못 하는 것");
    // (C)는 − 말이 이어진다 (선생님 표시판)
    expect(v.signs?.some((x) => x.sign === "−")).toBe(true);
    await go("다음");
    await go("이유를 늘 물을 수 있고 그게 도움이 됐다는 말");
    // 순서 잇기 — 학생이 카드를 놓는다. 틀리면 처음 어긋난 칸만 짚고 순서는 말하지 않는다
    expect(v.pick?.order?.cards.map((c) => c.id)).toEqual(["A", "B", "C"]);
    v = await session.submit("__order:A,C,B");
    expect(v.message).toBe("아쉽게도 틀렸어요. 주어진 글의 끝을 다시 봐요. 그 바로 뒤에 이어질 첫머리를 찾아봐요.");
    expect(v.message).not.toContain("(C)");
    v = await session.submit("__order:C,B,A");
    expect(v.message).toContain("두 번째 칸");
    await go("__order:C,A,B");
    expect(v.message).toBe("직접 이어 봤어요. 실제 시험 보기에서는 몇 번일지 볼까요?");
    await go("문제 풀러 갈게요");
    // 다시 풀지 않는다 — 맞춘 순서의 보기를 표시하고 해설만 (잇기에서 두 번 틀렸으니 다시 볼 주기는 짧게)
    expect(v.message).toBe("방금 맞춘 순서가 바로 ④ (C)-(A)-(B)예요. 보기를 누르면 해설이 열려요.");
    expect(v.examExplain?.["4"]?.correct).toBe(true);
    expect(v.examOptions?.map((o) => o.label)).toEqual(["(A)-(C)-(B)", "(B)-(A)-(C)", "(B)-(C)-(A)", "(C)-(A)-(B)", "(C)-(B)-(A)"]);
    v = await session.submit("다음으로");
    expect(v.review).toBeFalsy();
  });
});

describe("2026년 3월 33번 — 빈칸 문제", () => {
  const ID33 = "moeui-2026-03-33-profound-building";
  it("빈칸 위치 먼저(질문 없이) → 문장 1 읽기 → 공간=행동 연출(+/−) → 몸·마음 두 그룹 → 사는 사람이 기준 → 한 줄 요지 → 문제", async () => {
    const session = createPolicySession(ID33, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    v = await session.submit("넘어가기");
    const go = async (t: string) => {
      v = await session.submit(t);
      // 칠판 정리(2~3문장마다)는 넘긴다 — 따로 검사한다
      for (let g = 0; g < 4 && (v.praiseOnly || v.readingFirst || v.celebrate || v.panel?.kind === "story"); g++)
        v = await session.submit(v.praiseOnly ? "__auto_next" : v.readingFirst ? "다 읽었어요" : v.buttons[0]!);
      return v;
    };
    // 읽기 전에 빈칸 위치만 짚는다 (질문 없이) — 그다음 문장 1을 읽는다
    expect(v.readingFirst).toBe(false);
    expect(v.sentenceTag).toBe("빈칸 문장");
    expect(v.sentence).toBe("A profound building is ________.");
    expect(v.buttons).toEqual(["처음부터 읽어 볼게요"]);
    v = await session.submit("처음부터 읽어 볼게요");
    expect(v.readingFirst).toBe(true);
    expect(v.sentenceTag).toBe("문장 1");
    await go("다 읽었어요");
    await go("행동을 이끄는 공간 연출");
    expect(v.signs).toHaveLength(6);
    await go("다음 문장");
    expect(v.panel?.kind).toBe("groups");
    await go("왼쪽 · 몸 (행동)");
    await go("오른쪽 · 마음 (느낌)");
    await go("다음 문장");
    await go("사람들의 행동과 욕구");
    await go("다음 문장");
    expect(v.faded).toEqual(["While designing a house,"]);
    await go("미래에 그 집에 살 사람");
    await go("사는 사람이 정원을 내다보고 싶은 곳");
    await go("사는 사람이 오르내리고 싶은 곳");
    await go("말없이도 쓰임새를 드러내서");
    // 빈칸이 주장과 같은 쪽인지 반대 쪽인지 먼저
    expect(v.message).toBe("이 빈칸 문장은 글쓴이 주장과 같은 쪽일까요, 반대 쪽일까요?");
    await go("같은 쪽 (주장 그대로)");
    await go("사는 사람의 몸과 마음의 움직임에 꼭 맞는 건물");
    await go("문제 풀러 갈게요");
    expect(v.examOptions).toHaveLength(5);
  });
});

describe("2026년 3월 38번 — 문장 넣기", () => {
  const ID38 = "moeui-2026-03-38-gesture-glue";
  it("such choices 단서 → 앞뒤 예측 → 언어/제스처 두 그룹 → Instead, it(제스처) 앞엔 제스처 이야기 → 문제", async () => {
    const session = createPolicySession(ID38, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    const go = async (t: string) => {
      v = await session.submit(t);
      // 칠판 정리(2~3문장마다)는 넘긴다 — 따로 검사한다
      for (let g = 0; g < 4 && (v.praiseOnly || v.readingFirst || v.celebrate || v.panel?.kind === "story"); g++)
        v = await session.submit(v.praiseOnly ? "__auto_next" : v.readingFirst ? "다 읽었어요" : v.buttons[0]!);
      return v;
    };
    await go("다 읽었어요");
    expect(v.sentenceTag).toBe("주어진 문장");
    // 중급은 먼저 해석 맞추기 → 상황 표 → 앞을 가리키는 말 찾기
    expect(v.pick?.match).toBeTruthy();
    for (const c of v.pick!.candidates) await go(`__pick:${c}`);
    expect(v.panel?.kind).toBe("structure");
    await go("다음");
    expect(v.message).toContain("앞 내용을 가리키는 말");
    expect(v.pick?.shade).toBe(true);
    // 맞아요 화면에서만 찾은 말을 칠하고, 왜 중요한지 한 줄 덧붙인다
    v = await session.submit("__pick:such choices");
    expect(v.praiseOnly).toBe(true);
    expect(v.highlight).toContain("such choices");
    expect(v.message).toContain("주의 깊게");
    // 칭찬이 길면 저절로 넘어가지 않고 「네」로
    expect(v.buttons).toEqual(["네"]);
    // 「앞을 가리키는 말」 Tip은 맞힌 화면에서만
    expect((v.tips ?? []).map((x) => x.label)).toEqual(["앞을 가리키는 말"]);
    expect(v.autoNextMs).toBeNull();
    v = await session.submit("네");
    expect(v.praiseOnly).toBe(false);
    // choices를 먼저 언어/제스처 그룹에 나눈다
    expect(v.panel?.kind).toBe("groups");
    // 맞히면 그 그룹에 들어간 칠판을 1초 보여 주고 저절로 넘어간다
    v = await session.submit("왼쪽 · 언어");
    expect(v.praiseOnly).toBe(true);
    expect(v.buttons).toEqual([]);
    expect(v.autoNextMs).toBe(1000);
    expect(v.panel?.kind === "groups" && v.panel.left.words.map((w) => w.text)).toEqual(["choice"]);
    await go("__auto_next");
    await go("언어가 화자에게 선택을 하게 한다는 내용");
    await go("제스처가 선택 대신 하는 일");
    // 주어·동사 찾기는 뺐다 (2026-10-20) — 꾸미는 덩어리 설명(그림) 다음 뜻 질문
    expect(v.panel?.kind).toBe("structure");
    await go("다음");
    await go("제스처는 말과 동시에 만들어진다");
    // 5형식 읽는 법 (중·초)
    expect(v.message).toContain("사람이 ~하게 해 준다");
    await go("다음");
    await go("왼쪽 · 언어");
    await go("오른쪽 · 제스처");
    await go("완료인지 진행인지 꼭 고르게 한다");
    await go("다음");
    await go("제스처 (gesture)");
    await go("제스처는 선택을 주지 않는다는 이야기");
    expect(v.panel?.kind).toBe("groups");
    await go("다음 문장");
    await go("서로 중복되지 않고 각자 다른 일을 한다");
    await go("말과 제스처의 결합");
    await go("문제 풀러 갈게요");
    expect(v.examOptions).toHaveLength(5);
  });
});

describe("2026년 3월 39번 — 줄인 판(2026-10-14): 줄기는 모두에게, 아는 건 건너뛴다", () => {
  const ID = "moeui-2026-03-39-epistemic-communities";
  /** 정답만 고르며 보기 화면까지 간다. 지나온 스텝 id를 돌려준다 */
  async function walk(firstSvoWrong = false) {
    let saved = emptyStudentState();
    const lesson = allPolicyLessons().find((l) => l.id === ID)!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    const session = createPolicySession(ID, null, { loadStudent: () => saved, saveStudent(st) { saved = st; }, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const seen: string[] = [];
    let wrongOnce = firstSvoWrong;
    for (let g = 0; g < 300 && !v.examOptions; g++) {
      const id = session.lastAction()?.interactionId ?? "";
      const st = steps.get(id);
      if (st && seen[seen.length - 1] !== id) seen.push(id);
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "pick" && v.pick?.open) {
        if (wrongOnce) {
          wrongOnce = false;
          v = await session.submit(`__pick:${st.candidates.find((c) => !st.answers.includes(c))}`);
        }
        for (const a of st.answers) v = await session.submit(`__pick:${a}`);
      } else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) {
        v = await session.submit(st.options.find((o) => o.correct)!.label);
      } else if (st?.type === "translate" && v.allowInput) v = await session.submit(st.model);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    return { v, seen, saved };
  }

  it("다 맞히면: S·V·O 찾기는 없고(2026-10-20 삭제), 딸린 설명·대시 뒤 해석은 건너뛰고, ①~⑤ 흐름 확인과 Other를 지나 보기 화면에 간다", async () => {
    const { v, seen } = await walk();
    expect(v.examOptions).toHaveLength(5);
    expect(seen.filter((x) => /_svc?$/.test(x))).toEqual([]);
    for (const x of ["g_for_note", "g_svo2", "g_rel_note"]) expect(seen).not.toContain(x);
    for (const x of ["s3_flow", "s4_flow", "s5_flow", "s6_flow", "s7_other", "s7_flow", "s2_sort", "s3_sort_experts"]) expect(seen).toContain(x);
    // 잘하는 학생 기준 — 예전 56스텝에서 크게 줄었다 (칠판 정리 3장 + 주어진 문장의 해석 맞추기 1장 포함)
    expect(seen.length).toBeLessThanOrEqual(39);
  });

  it("S·V·O 찾기는 틀려도 다시 나오지 않는다 — 활동 자체를 뺐다 (2026-10-20)", async () => {
    const { seen } = await walk(true);
    expect(seen.filter((x) => /_svc?$/.test(x))).toEqual([]);
  });

  // 핵심어만 나열하는 자유 해석은 뺐다 (2026-10-20 선생님) — 해석 맞추기가 대신한다
  it.skip("S·V·O 해석 안내 대사 없이 바로 해석하고, 노란 박스 위에 「왜 핵심어만 보나요?」 칩이 뜬다", async () => {
    const { seen } = await walk();
    expect(seen).not.toContain("g_svo_tip");
    const session = createPolicySession(ID, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    v = await session.submit("다 읽었어요");
    for (const w of ["even completely transparent practices", "do not lift", "the veil", "one", "cannot make sense of", "the information"]) v = await session.submit(`__pick:${w}`);
    for (let g = 0; g < 8 && !v.allowInput; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(session.lastAction()?.interactionId).toBe("g_svo1");
    expect(v.translateWhy?.label).toBe("왜 핵심어만 보나요?");
    expect(v.translateWhy?.text).toContain("시간 제한");
    v = await session.submit("대부분의 외부인에게는 완전히 투명한 관행조차 장막을 걷어 내지 못한다");
    expect(v.translateWhy).toBeNull();
  });

  it("문법 설명은 ❓ 칩으로 남는다", () => {
    const lesson = allPolicyLessons().find((l) => l.id === ID)!;
    expect(lesson.sentences.flatMap((s) => (s.concepts ?? []).map((c) => c.en))).toEqual(["knowledge bearers", "from experts", "there are", "present"]);
  });
});

// 주어·동사 찾기 활동은 2026-10-20에 뺐다 — v1 흐름 검사는 건너뛴다
describe.skip("2026년 3월 39번 이전 버전(v1) — 주어진 문장 주어·동사 찾기", () => {
  it("읽기 끝나면 덩어리째 S·V·O 두 쌍을 찾고 S·V·O만으로 해석한다 — for most outsiders는 전치사라서, 찾은 건 S·V 표시로 남는다", async () => {
    const session = createPolicySession("moeui-2026-03-39-epistemic-communities-v1", null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(v.givenBox).toBe(true);
    v = await session.submit("다 읽었어요");
    expect(session.lastAction()?.interactionId).toBe("g_sv");
    expect(v.pick?.shade).toBe(true);
    // 「잘 모르겠어요」 없이 끝까지 직접 찾는다
    expect(v.buttons).toEqual([]);
    v = await session.submit("__pick:for most outsiders");
    expect(v.message).toContain("for 같은 전치사가 앞에 붙은 덩어리는 주어가 될 수 없어요");
    v = await session.submit("__pick:even completely transparent practices");
    expect(v.roles).toEqual([{ text: "even completely transparent practices", role: "S" }]);
    for (const w of ["do not lift", "the veil", "one", "cannot make sense of", "the information"]) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    // 다음 화면에도 S·V·O가 남는다 — for most outsiders는 주어가 아니지만 「대상」
    expect(v.roles?.map((r) => r.role)).toEqual(["S", "V", "O", "S", "V", "O"]);
    expect(v.message).toBe("그럼 for most outsiders는 어떤 역할일까요?");
    v = await session.submit("이 문장이 해당하는 대상 (~에게는)");
    v = await session.submit("__auto_next");
    // 맞힌 다음 바로 넘어가지 않고 for + 명사를 설명한다
    expect(v.message).toBe("for + 명사는 모의고사에서 '~에게는'이라는 뜻으로 자주 쓰여요. 주어는 아니지만 중요한 정보예요.");
    v = await session.submit("다음");
    expect(v.roles?.map((r) => r.role)).toContain("대상");
    // 안내 말과 해석 요청은 따로
    expect(v.message).toBe("수능은 주어, 동사, 목적어 + 핵심 내용 위주로 빠르게 해석해 보면 좋아요. 한번 해 볼까요?");
    v = await session.submit("네");
    expect(v.message).toBe("그럼 노란색으로 표시된 부분만 해석해 봐요.");
    expect(v.allowInput).toBe(true);
    v = await session.submit("대부분의 외부인에게는 완전히 투명한 관행조차 장막을 걷어 내지 못한다");
    expect(v.translation?.fixes).toEqual([]);
    v = await session.submit("다음으로");
    // lift the veil — 장막 뒤에 숨겨진 것 찾기 → 뜻
    expect(v.message.startsWith("여기서 lift the veil은 무엇을 가린 장막을")).toBe(true);
    v = await session.submit("__pick:veil");
    expect(v.message).toContain("veil은 장막 자체예요");
    v = await session.submit("__pick:knowledge");
    v = await session.submit("__auto_next");
    expect(v.message).toBe("그럼 lift the veil은 무슨 뜻일까요?");
    v = await session.submit("숨겨진 지식을 드러내 이해하게 하다");
    v = await session.submit("__auto_next");
    // 그림 ① 집단과 바깥의 외부인 → ② 집단 안의 지식, 닿기 어려운 외부인
    expect(v.panel).toMatchObject({ kind: "picture", src: "/assets/veil-group.svg" });
    v = await session.submit("다음");
    expect(v.panel).toMatchObject({ kind: "picture", src: "/assets/veil-knowledge.svg" });
    v = await session.submit("다음");
    expect(v.message).toBe("이번에도 노란색으로 표시된 부분만 해석해 봐요.");
    v = await session.submit("누구든 그 정보를 이해할 수 없다");
    expect(v.translation?.fixes).toEqual([]);
    expect(v.buttons).not.toContain("주어 찾기 헷갈려요");
    // 관계사 수식 — 못 맞히면 that + 주어 없는 문장 설명 → shared = 집단 안 → 대시 앞뒤 같은 말 → 수능 팁
    v = await session.submit("다음으로");
    expect(v.message).toBe("이번엔 노란색으로 표시된 부분을 해석해 봐요.");
    v = await session.submit("그것은 공유되고 있다");
    expect(v.translation?.fixes.length).toBeGreaterThan(0);
    v = await session.submit("다음으로");
    expect(v.message.startsWith("that 뒤에 주어 없이 바로 동사가 오면")).toBe(true);
    v = await session.submit("다음");
    expect(v.message.startsWith("shared는 앞서 본 집단 안에서")).toBe(true);
    v = await session.submit("다음");
    expect(v.message.startsWith("수능 팁이에요. 대시(—) 앞뒤는")).toBe(true);
    v = await session.submit("다음");
    expect(v.panel?.kind).toBe("structure");
    // 마지막으로 Nonetheless — 앞 문장은 반대 상황
    v = await session.submit("다음");
    expect(v.message.startsWith("마지막으로 Nonetheless를 짚고 가요.")).toBe(true);
    v = await session.submit("다음");
    expect(v.message).toBe("그럼 이 문장 바로 앞에는 어떤 내용이 와야 할까요?");
    v = await session.submit("외부인은 전문 지식을 이해하기 어렵다");
    expect(v.message.startsWith("아쉽게도 틀렸어요.")).toBe(true);
    v = await session.submit(v.buttons[0]);
    expect(v.panel).toMatchObject({ kind: "contrast", title: "Nonetheless → 앞뒤가 반대" });
  });

  it("관계사 수식을 한 번에 맞히면 설명을 건너뛰고, 다음부터는 묻지 않는다", async () => {
    let saved = emptyStudentState();
    const session = createPolicySession("moeui-2026-03-39-epistemic-communities-v1", null, { loadStudent: () => saved, saveStudent(st) { saved = st; }, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    v = await session.submit("다 읽었어요");
    for (let g = 0; g < 60 && v.message !== "이번엔 노란색으로 표시된 부분을 해석해 봐요."; g++) {
      v = await session.submit(v.allowInput ? "답 바로 보기" : v.pick?.open ? "잘 모르겠어요" : (v.buttons[0] ?? "__auto_next"));
    }
    expect(v.message).toBe("이번엔 노란색으로 표시된 부분을 해석해 봐요.");
    v = await session.submit("공유되고 있는 정보");
    expect(v.translation?.fixes).toEqual([]);
    expect(saved.known).toContain("rel_that_no_subject");
    v = await session.submit("다음으로");
    expect(v.message.startsWith("shared는 앞서 본 집단 안에서")).toBe(true);
  });
});

describe.skip("2026년 3월 39번 이전 버전(v1) — 문장 1 주어·동사·목적어 찾기", () => {
  it("읽기 끝나면 덩어리째 S·V·O를 찾고(to become a member = needs의 목적어), for which 뒤 I는 덧붙임 안의 주어라고 알려 준 뒤 S·V·O만 해석한다", async () => {
    const session = createPolicySession("moeui-2026-03-39-epistemic-communities-v1", null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    v = await session.submit("__next_sentence");
    expect(v.readingFirst).toBe(true);
    v = await session.submit("다 읽었어요");
    expect(session.lastAction()?.interactionId).toBe("s2_svc");
    expect(v.pick?.shade).toBe(true);
    v = await session.submit("__pick:I");
    expect(v.message).toContain("for which 뒤 덩어리 안의 주어예요");
    for (const w of ["one", "needs", "to become a member"]) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    expect(v.roles?.map((r) => r.role)).toEqual(["S", "V", "O"]);
    expect(v.allowInput).toBe(true);
    // 핵심어로 상황 요약 (직역 말고)
    expect(v.message.startsWith("노란 핵심어만 보고, 직역 말고")).toBe(true);
    v = await session.submit("전문 지식을 얻으려면 집단의 구성원이 되어야 한다");
    expect(v.translation?.fixes).toEqual([]);
    // bear — 고르게 하고 그다음 설명
    v = await session.submit("다음으로");
    expect(v.message.endsWith("여기서 bear는 무슨 뜻일까요?")).toBe(true);
    v = await session.submit("낳다");
    expect(v.message.startsWith("아쉽게도 틀렸어요.")).toBe(true);
    for (let g = 0; g < 3 && !v.message.startsWith("bear는 '곰', '참다', '낳다' 말고도"); g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(v.message.startsWith("bear는 '곰', '참다', '낳다' 말고도")).toBe(true);
    // 이 집단을 가리키는 말
    v = await session.submit("다음");
    expect(v.message.startsWith("그럼 이 지식 보유자 집단을 가리키는 말은")).toBe(true);
    v = await session.submit("__pick:the term");
    expect(v.message).toContain("어떤 용어인지 바로 뒤를 봐요");
    v = await session.submit("__pick:epistemic communities");
    v = await session.submit("__auto_next");
    expect(v.panel).toMatchObject({ kind: "picture", src: "/assets/member-join.svg" });
    // 내부자(전문가) ↔ 외부자(초보자) 단어 묶음
    v = await session.submit("다음");
    expect(v.message.startsWith("수능에서는 같은 쪽 단어 묶음이 중요해요.")).toBe(true);
    expect(v.panel).toMatchObject({ kind: "groups", left: { label: "내부자 · 전문가 쪽" }, right: { label: "외부자 · 초보자 쪽" } });
    // 첫 단어(knowledge bearers, outsiders)만 미리 넣고, 나머지는 학생이 끌어 넣는다
    expect(v.panel?.kind === "groups" && v.panel.left.words.map((w) => w.text)).toEqual(["knowledge bearers"]);
    v = await session.submit("다음");
    expect(v.panel?.kind === "groups" && v.panel.sort?.words).toEqual(["a member"]);
    v = await session.submit("오른쪽 · 외부자(초보자) 쪽");
    expect(v.message.startsWith("아쉽게도 틀렸어요.")).toBe(true);
  });
});

describe.skip("2026년 3월 39번 이전 버전(v1) — 문장 2 동사 두 개·전치사의 목적어", () => {
  it("and 뒤 동사까지 S·V를 찾고, 전치사의 목적어를 찾은 뒤 핵심어로 요약하고, 단어 지도로 끝난다", async () => {
    const session = createPolicySession("moeui-2026-03-39-epistemic-communities-v1", null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    v = await session.submit("__next_sentence");
    v = await session.submit("__next_sentence");
    expect(v.sentenceTag).toBe("문장 2");
    v = await session.submit("다 읽었어요");
    expect(session.lastAction()?.interactionId).toBe("s3_sv");
    v = await session.submit("__pick:from experts");
    expect(v.message).toContain("전치사가 붙은 덩어리는 주어나 동사가 될 수 없어요");
    for (const w of ["A newcomer", "learns", "is socialized"]) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    expect(v.message.startsWith("and 뒤에 주어 없이 동사가 바로 오면")).toBe(true);
    v = await session.submit("다음");
    expect(v.message.startsWith("from, into 같은 전치사 뒤의 명사는")).toBe(true);
    for (const w of ["experts", "the common practices"]) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    expect(v.roles?.map((r) => r.role)).toEqual(["S", "V", "V", "전목", "전목"]);
    expect(v.allowInput).toBe(true);
    v = await session.submit("새로 온 사람은 전문가에게 배우고 그 집단에 적응한다");
    expect(v.translation?.fixes).toEqual([]);
    v = await session.submit("다음으로");
    expect(v.panel?.kind).toBe("groups");
  });
});

describe.skip("2026년 3월 39번 이전 버전(v1) — 문장 3~6도 주어·동사 찾기 → 핵심어 요약", () => {
  // [주어·동사(보어) 고르기, 그 답, 전치사의 목적어 답, 요약]
  const cases: [string, string[], string[], string][] = [
    ["s5_sv", ["epistemic communities", "were often kept", "secret"], [],
     "옛날엔 지식 공동체가 비밀이었고 충성심 시험이 있었다"],
    ["s7_sv", ["Other, more active strategies", "are needed"], [], "지식에 접근 가능하게 하려면 더 적극적인 전략이 필요하다"],
  ];
  it.each(cases)("%s — 찾은 뒤 요약을 맞히고 다음으로 넘어간다", async (pickId, answers, preps, summary) => {
    const session = createPolicySession("moeui-2026-03-39-epistemic-communities-v1", null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    for (let g = 0; g < 10 && !(v.readingFirst && session.lastAction()?.interactionId === pickId); g++) {
      v = await session.submit("__next_sentence");
    }
    v = await session.submit("다 읽었어요");
    expect(session.lastAction()?.interactionId).toBe(pickId);
    for (const w of answers) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    expect(v.roles).toHaveLength(answers.length);
    // 전치사의 목적어 찾기 → 전목 표시가 더해진다
    if (preps.length) {
      expect(v.message).toContain("전치사의 목적어(전목)");
      for (const w of preps) v = await session.submit(`__pick:${w}`);
      v = await session.submit("__auto_next");
      expect(v.roles?.filter((r) => r.role === "전목")).toHaveLength(preps.length);
    }
    // 문법 설명 화면(but)이 있으면 넘긴다
    for (let g = 0; g < 2 && !v.allowInput; g++) v = await session.submit(v.buttons[0]);
    expect(v.message.startsWith("노란 핵심어만 보고")).toBe(true);
    v = await session.submit(summary);
    expect(v.translation?.fixes).toEqual([]);
  });
});

describe.skip("2026년 3월 39번 이전 버전(v1) — 문장 3은 요약 없이 핵심어(주어·동사 + tests) → 그림", () => {
  it("there are 설명 뒤 핵심어를 짚고 입회 절차 그림을 보여 준다", async () => {
    const session = createPolicySession("moeui-2026-03-39-epistemic-communities-v1", null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    for (let g = 0; g < 10 && !(v.readingFirst && v.sentenceTag === "문장 3"); g++) v = await session.submit("__next_sentence");
    v = await session.submit("다 읽었어요");
    expect(session.lastAction()?.interactionId).toBe("s4_sv");
    for (const w of ["are", "admittance processes"]) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    expect(v.message.startsWith("there are 문장은")).toBe(true);
    v = await session.submit("다음");
    expect(v.message.startsWith("핵심어는 주어·동사와 tests예요.")).toBe(true);
    expect(v.allowInput).toBeFalsy();
    v = await session.submit("다음");
    expect(v.panel).toMatchObject({ kind: "picture", src: "/assets/admittance-test.svg" });
  });
});

describe.skip("2026년 3월 39번 이전 버전(v1) — 문장 5: S·V·C·목적어 모두 → 앞부분 뜻 고르기 → but → 핵심어 → 칠판", () => {
  it("요약 없이 secret → openness 칠판으로 정리한다", async () => {
    const session = createPolicySession("moeui-2026-03-39-epistemic-communities-v1", null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    for (let g = 0; g < 10 && !(v.readingFirst && v.sentenceTag === "문장 5"); g++) v = await session.submit("__next_sentence");
    v = await session.submit("다 읽었어요");
    // 먼저 주어·동사·보어·목적어를 모두 찾는다
    expect(session.lastAction()?.interactionId).toBe("s6_sv");
    v = await session.submit("__pick:these older practices");
    expect(v.message).toContain("traces를 꾸며 주는 말이에요");
    for (const w of ["Some traces", "may still be", "present", "the ideal", "has shifted", "openness"]) v = await session.submit(`__pick:${w}`);
    v = await session.submit("__auto_next");
    expect(v.roles?.map((r) => r.role)).toEqual(["S", "V", "C", "S", "V", "전목"]);
    // 앞부분 뜻 고르기 — present = 남아 있는
    expect(v.message).toBe("노란 부분은 무슨 뜻일까요?");
    v = await session.submit("옛 관행이 오늘날 사람들에게 선물이 될 수 있다");
    expect(v.message).toContain("'선물'이나 '현재의'가 아니라");
    for (let g = 0; g < 3 && !v.message.startsWith("but은 앞과 뒤를"); g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(v.message.startsWith("but은 앞과 뒤를 뒤집는 말이에요.")).toBe(true);
    v = await session.submit("다음");
    expect(v.message.startsWith("핵심어 members(구성원)와 outsiders(외부인)")).toBe(true);
    v = await session.submit("다음");
    expect(v.panel).toMatchObject({ kind: "groups", left: { label: "과거 · premodern" }, right: { label: "지금 · today" } });
    expect(v.allowInput).toBeFalsy();
  });
});

describe("자유 해석 — 한 군데까지는 봐준다", () => {
  const given = () => allPolicyLessons().find((l) => l.id === "moeui-2026-03-39-epistemic-communities")!.sentences[0];
  const svo1 = () => given().steps.find((x) => x.id === "g_svo1") as TranslateStep;
  it("lift를 '들어올리다'로 써도 맞다", () => {
    expect(gradeTranslation(svo1(), "대부분의 외부인에게는 완전히 투명한 관행조차 장막을 들어올리지 못한다").issues).toEqual([]);
  });
  // 핵심어 자유 해석 스텝이 빠져 수업에서는 안 나온다 — 채점 규칙 자체는 위 gradeTranslation 테스트가 본다
  it.skip("한 군데만 다르면 틀렸다고 하지 않고 그 곳만 표시한다", async () => {
    const session = createPolicySession("moeui-2026-03-39-epistemic-communities", null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    v = await session.submit("다 읽었어요");
    for (const w of ["even completely transparent practices", "do not lift", "the veil", "one", "cannot make sense of", "the information"]) v = await session.submit(`__pick:${w}`);
    for (let g = 0; g < 8 && !v.allowInput; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    v = await session.submit("투명한 관행조차 장막을 걷어 내지 못한다");
    expect(v.message.startsWith("아쉽게도 틀렸어요.")).toBe(false);
    expect(v.message).toContain("한 군데만 다르게 썼어요.");
    expect(v.translation?.fixes).toHaveLength(1);
    expect(v.translation?.save).toBe(false);
  });
  it("for most outsiders의 for는 '~에게'만 — '위해'가 뜨지 않는다", () => {
    const fr = splitPhraseGlosses(given().glosses).find((g) => g.en === "for");
    expect(fr?.ko.startsWith("~에게")).toBe(true);
    expect(fr?.ko).not.toContain("위해");
  });
});

describe("2026학년도 6월 모평 34·37번 — 처음부터 끝까지 정답으로 지나가면 보기 화면까지 간다", () => {
  it.each(["mopyeong-2026-06-34-geography-where", "mopyeong-2026-06-37-chaos-pendulum",
    ...allPolicyLessons().map((l) => l.id).filter((id) => id.startsWith("moeui-2024-03-") || id.startsWith("moeui-2022-03-"))])("%s", async (id) => {
    const lesson = allPolicyLessons().find((l) => l.id === id)!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    const session = createPolicySession(id, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const seen = new Set<string>();
    for (let g = 0; g < 200 && !v.examOptions; g++) {
      const st = steps.get(session.lastAction()?.interactionId ?? "");
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "pick" && v.pick?.open) {
        seen.add(st.id);
        for (const a of st.answers) v = await session.submit(`__pick:${a}`);
      } else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) {
        seen.add(st.id);
        v = await session.submit(st.options.find((o) => o.correct)!.label);
      } else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    expect(v.examOptions).toHaveLength(5);
    // 주어·동사 찾기는 수업에서 뺐다 (2026-10-20) — 지나오지 않는다
    expect([...seen].some((x) => /_sv$|_svc$/.test(x))).toBe(false);
  });
});

describe("도입 — 풀이법 설명은 그 유형을 처음 풀 때만", () => {
  it("같은 유형을 두 번째 풀면 method 말을 건너뛴다", async () => {
    // 풀이법 설명을 몇 번 봤는지는 브라우저 저장소에 남는다 — 테스트에서는 흉내 낸 저장소로
    const store = new Map<string, string>();
    const g = globalThis as unknown as { window?: unknown };
    const had = g.window;
    g.window = { localStorage: { getItem: (k: string) => store.get(k) ?? null, setItem: (k: string, v: string) => void store.set(k, v), removeItem: (k: string) => void store.delete(k) } };
    const deps = { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 };
    const intros = async () => {
      const session = createPolicySession("moeui-2026-03-21-music-researchers", null, deps);
      let v = await session.submit("분석하러 갈게요");
      const said: string[] = [];
      for (let g = 0; g < 6 && !v.readingFirst; g++) {
        said.push(v.message);
        v = await session.submit(v.buttons[0] ?? "__auto_next");
      }
      return said;
    };
    const first = await intros();
    expect(first.some((m) => m.includes("시간 싸움"))).toBe(true);
    const second = await intros();
    expect(second.some((m) => m.includes("시간 싸움"))).toBe(false);
    expect(second.length).toBeLessThan(first.length);
    g.window = had;
  });
});

describe("덩어리 안의 내용어는 단어 뜻이 있다 — 단어 카드로 저장하고 연습할 수 있게", () => {
  it.each(allPolicyLessons().map((l) => [l.id, l] as const))("%s", (_id, lesson) => {
    const missing: string[] = [];
    for (const s of lesson.sentences) {
      const singles = new Set(s.glosses.filter((g) => !/\s/.test(g.en.trim())).map((g) => g.en.toLowerCase()));
      for (const g of s.glosses) {
        const words = g.en.trim().split(/\s+/);
        if (words.length < 2) continue;
        for (const raw of words) {
          const k = raw.replace(/^[“"‘'(]+|[”"’'),.;:!?]+$/g, "").toLowerCase();
          if (!k || /^[\W\d_]+$/.test(k) || FUNCTION_WORDS.has(k) || CONTEXT_WORDS.has(k)) continue;
          if (!singles.has(k) && !WORDS[k]) missing.push(`${s.id}:${k}`);
        }
      }
    }
    expect(missing).toEqual([]);
  });
});

describe("6월 34번 — 빈칸 위치 먼저(질문 없이) → 순서대로 읽기 → 빈칸 문장에서 질문", () => {
  it("읽기 전에 빈칸 문장을 짚고, 빈칸 질문은 빈칸 문장에 도착해서 한다", async () => {
    const session = createPolicySession("mopyeong-2026-06-34-geography-where", null, { loadStudent: () => ({ ...emptyStudentState(), recentFormats: ["match"] }), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 4 && !v.message.includes("여섯째 문장"); g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(v.readingFirst).toBe(false);
    // ① 지문 전체에서 빈칸 문장 위치만
    expect(v.message).toContain("빈칸은 여기, 여섯째 문장에 있어요.");
    expect(v.examPassage?.highlight[0]).toContain("________");
    v = await session.submit("네");
    // ② 핵심어만 칠한 빈칸 문장 — 뜻 고르기
    expect(v.examPassage).toBeUndefined();
    expect(v.sentenceTag).toBe("빈칸 문장");
    expect(v.message).toContain("이 문장은 무슨 뜻일까요?");
    v = await session.submit("____을 모르면 판단하고 이해하기 어렵다");
    for (let g = 0; g < 2 && v.praiseOnly; g++) v = await session.submit("__auto_next");
    // ③ 중 — 세 덩어리가 같은 말
    expect(v.message).toContain("모두 '이해하다'라는 같은 말");
    v = await session.submit("다음");
    expect(v.message).toContain("무엇을 알아야 하는지 생각하면서 문장 처음부터 읽어 봐요.");
    v = await session.submit("처음부터 읽어 볼게요");
    expect(v.readingFirst).toBe(true);
    expect(v.sentenceTag).toBe("문장 1");
    v = await session.submit("다 읽었어요");
    // 주어·동사 찾기는 뺐다 (2026-10-20)
    expect(session.lastAction()?.interactionId).not.toBe("s1_sv");
    const lesson = allPolicyLessons().find((l) => l.id === "mopyeong-2026-06-34-geography-where")!;
    const blankSentence = lesson.sentences.find((s) => s.steps.some((st) => st.id === "s6_fill"))!;
    expect(blankSentence.text).toContain("________");
  });
});

describe("학생 단계 — 고·중·초에 따라 영어를 돕는 화면만 달라진다 (6월 34번 시범)", () => {
  const walk = async (level: "고" | "중" | "초", recentFormats: string[] = []) => {
    const id = "mopyeong-2026-06-34-geography-where";
    const lesson = allPolicyLessons().find((l) => l.id === id)!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    const session = createPolicySession(id, null, { loadStudent: () => ({ ...emptyStudentState(), level, recentFormats }), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const seen = new Set<string>();
    for (let g = 0; g < 200 && !v.examOptions; g++) {
      const st = steps.get(session.lastAction()?.interactionId ?? "");
      if (st && !v.readingFirst) seen.add(st.id);
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "pick" && v.pick?.open) for (const a of st.answers) v = await session.submit(`__pick:${a}`);
      else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) v = await session.submit(st.options.find((o) => o.correct)!.label);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    expect(v.examOptions).toHaveLength(5);
    return seen;
  };
  it("고는 짧은 문장의 주어·동사, 가리키는 말, 헷갈리는 단어 뜻을 건너뛰고 내용 파악은 그대로 본다", async () => {
    const high = await walk("고");
    const mid = await walk("중", ["match"]); // 맞추기 차례가 아닐 때
    for (const id of ["s6_scale"]) {
      expect(high.has(id)).toBe(false);
      expect(mid.has(id)).toBe(true);
    }
    expect(high.has("s5_appreciation")).toBe(false);
    // s1_word는 1문장의 맞추기가 자리를 차지해 중도 안 본다
    expect(mid.has("s1_match")).toBe(true);
    // 주어·동사 찾기는 누구에게도 없다 (2026-10-20)
    for (const id of ["s1_sv", "s5_sv"]) {
      expect(high.has(id)).toBe(false);
      expect(mid.has(id)).toBe(false);
    }
    for (const id of ["s6_fill", "s6_side", "s4_same"]) expect(high.has(id)).toBe(true);
    expect(high.size).toBeLessThan(mid.size);
    // 1문장의 주어·동사 찾기(중·초)를 뺀 자리는 해석 맞추기가 대신한다 — 고는 원래 안 봤으니 뜻 객관식 그대로 (2026-10-20)
    expect(high.has("s1_match")).toBe(false);
    expect(high.has("s1_meaning")).toBe(true);
    expect((await walk("중")).has("s1_match")).toBe(true);
  });
  it("해석 맞추기(s1_match): 칸에 맞지 않는 덩어리는 「아쉽게도 틀렸어요」+ 그 칸 뜻, 맞으면 칸이 채워지고 다 채우면 칭찬", async () => {
    const id = "mopyeong-2026-06-34-geography-where";
    const session = createPolicySession(id, null, { loadStudent: () => ({ ...emptyStudentState(), level: "초" }), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const answers: Record<string, string[]> = { s1_sv: ["One word", "is inextricably associated", "geography"], s1_word: ["where"] };
    for (let g = 0; g < 60 && session.lastAction()?.interactionId !== "s1_match"; g++) {
      const now = session.lastAction()?.interactionId ?? "";
      if (!v.readingFirst && v.pick?.open && answers[now]) { for (const a of answers[now]!) v = await session.submit(`__pick:${a}`); continue; }
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (v.buttons.length > 1 && !v.buttons.includes("다음으로")) v = await session.submit(v.buttons.find((b) => b.startsWith("____을 모르면")) ?? v.buttons[0]!);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    if (v.readingFirst) v = await session.submit("다 읽었어요");
    expect(v.pick?.match?.ko.filter((x) => typeof x !== "string")).toHaveLength(4);
    v = await session.submit("__match:0:geography");
    expect(v.message).toBe("아쉽게도 틀렸어요. 그 칸은 '한 단어는'예요. 다른 덩어리를 놓아 봐요.");
    v = await session.submit("__match:0:One word");
    expect(v.pick?.found).toEqual(["One word"]);
    for (const [i, c] of [[1, "geography"], [2, "is inextricably associated with"], [3, "where"]] as const) v = await session.submit(`__match:${i}:${c}`);
    expect(v.message.startsWith("다 맞췄어요!")).toBe(true);
  });

  it("같은 자리(slot)는 방식을 돌려 가며 — 초가 최근에 맞추기를 했으면 이번엔 객관식, 안 했으면 맞추기", async () => {
    const fresh = await walk("초");
    expect(fresh.has("s1_match")).toBe(true);
    expect(fresh.has("s1_meaning")).toBe(false);
    expect(fresh.has("s1_sv")).toBe(false); // 주어·동사 찾기는 뺐다
    // 주어·동사 찾기를 뺀 자리는 돌려 내지 않고 늘 맞추기 (2026-10-20)
    const after = await walk("초", ["match"]);
    expect(after.has("s1_match")).toBe(true);
    expect(after.has("s1_meaning")).toBe(false);
  });

  it("초는 중이 보는 화면을 다 보되, 해석 맞추기를 한 문장에서만 주어·동사 찾기·뜻 확인을 건너뛴다", async () => {
    const lesson = allPolicyLessons().find((l) => l.id === "mopyeong-2026-06-34-geography-where")!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    const low = await walk("초", ["match"]);
    const mid = await walk("중", ["match"]);
    const skipped = [...mid].filter((id) => !low.has(id));
    for (const id of skipped) {
      const st = steps.get(id)!;
      expect(st.type === "pick" && !!st.roles || !!st.meaning_check || !!st.slot, id).toBe(true);
    }
    expect([...low].some((id) => id.endsWith("_match"))).toBe(true);
  });
});

describe("다의 기능어(to, for, that …)는 문장마다 그 자리 쓰임이 적혀 있다", () => {
  const lessons = allPolicyLessons().filter((l) => !l.id.endsWith("-v1"));
  it.each(lessons.map((l) => [l.id, l] as const))("%s", (_id, lesson) => {
    const wrong: string[] = [];
    for (const s of lesson.sentences) {
      const words = (s.text.match(/[A-Za-z]+/g) ?? []).map((w) => w.toLowerCase()).filter((w) => SENSE_WORDS.includes(w));
      const written = sensesOf(lesson.id, s.id).map((x) => x.word.toLowerCase());
      for (const w of SENSE_WORDS) {
        const need = words.filter((x) => x === w).length;
        const have = written.filter((x) => x === w).length;
        if (need !== have) wrong.push(`${s.id}:${w} 문장 ${need}개 / 적은 것 ${have}개`);
      }
    }
    expect(wrong).toEqual([]);
  });
});

describe("초급은 문장마다 「해석 맞추기」 하나 — 주어·동사 찾기는 뺐다 (2026-10-20)", () => {
  it.each([
    ["moeui-2026-03-36-conversation-stoppers", [2, 3, 4]],
    ["mopyeong-2026-06-37-chaos-pendulum", [2, 3, 4, 5, 6, 7, 8, 9]],
    ["mopyeong-2026-06-34-geography-where", [2, 3, 4, 5, 7, 8]],
    ["moeui-2026-03-33-profound-building", [1, 2, 3, 4, 5, 6, 7]],
    ["moeui-2026-03-38-gesture-glue", [1, 3, 4, 5, 6, 7, 8]],
    ["moeui-2026-03-30-names-and-differences", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]],
    ["moeui-2026-03-39-epistemic-communities", [2, 3, 4, 5, 6, 7]],
    ["moeui-2026-03-24-translation-strangeness", [1, 2, 4, 5, 6, 7]],
    ["moeui-2026-03-21-music-researchers", [1, 2, 3, 6, 7]],
    // 2024년 3월 — 초급 기본(s<n>_basic)을 단 레슨의, 단 문장 전부 (41·44·45처럼 짧은 확인 레슨은 기본이 없다)
    ...allPolicyLessons().filter((l) => l.id.startsWith("moeui-2024-03-") && l.sentences.some((s) => s.steps.some((st) => st.slot === `s${s.id}_basic`))).map((l) =>
      [l.id, l.sentences.filter((s) => s.steps.some((st) => st.slot === `s${s.id}_basic`)).map((s) => s.id)] as const),
  ] as const)("%s — 둘 중 하나만, 번갈아", async (id, ids) => {
    const lesson = allPolicyLessons().find((l) => l.id === id)!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    let saved = { ...emptyStudentState(), level: "초" as const };
    const session = realCreatePolicySession(id, null, { loadStudent: () => saved, saveStudent(x) { saved = x as typeof saved; }, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const seen: string[] = [];
    for (let g = 0; g < 400 && !v.examOptions; g++) {
      const st = steps.get(session.lastAction()?.interactionId ?? "");
      if (st && !v.readingFirst && seen.at(-1) !== st.id) seen.push(st.id);
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "pick" && st.order && v.pick?.open) v = await session.submit(`__order:${st.answers.join(",")}`);
      else if (st?.type === "pick" && v.pick?.open) for (const a of st.answers) v = await session.submit(`__pick:${a}`);
      else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) v = await session.submit(st.options.find((o) => o.correct)!.label);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    expect(v.examOptions).toHaveLength(5);
    // 주어·동사 찾기(roles pick)는 어떤 문장에서도 나오지 않는다
    for (const st of lesson.sentences.flatMap((s) => s.steps).filter((x) => x.type === "pick" && x.roles)) expect(seen).not.toContain(st.id);
    for (const n of ids) {
      const sen = lesson.sentences.find((s) => s.id === n)!;
      const slotted = sen.steps.filter((x) => x.slot === `s${n}_basic`).map((x) => x.id);
      const shown = slotted.filter((x) => seen.includes(x));
      // 같은 자리에선 하나만 (맞추기·객관식을 돌려 낸다) — 주어·동사 찾기는 절대 아니다
      expect(shown.length, `문장 ${n}`).toBeLessThanOrEqual(1);
      expect(shown.some((x) => /_sv$|_svc$/.test(x)), `문장 ${n}`).toBe(false);
      // 맞추기를 하면 뜻 풀기·뜻 질문은 건너뛴다
      if (shown[0] === `s${n}_match`) for (const x of sen.steps.filter((x) => x.meaning_check)) expect(seen).not.toContain(x.id);
    }
    expect(seen.some((x) => x.endsWith("_match"))).toBe(true);
  });
});

describe("순서 문제는 시험지 순서대로 (A)→(B)→(C)를 읽고, 주어진 글의 마지막 화면에서 한 번 알린다", () => {
  it.each(["moeui-2026-03-36-conversation-stoppers", "mopyeong-2026-06-37-chaos-pendulum"])("%s", (id) => {
    const lesson = allPolicyLessons().find((l) => l.id === id)!;
    const heads = lesson.sentences.map((s) => s.text.slice(0, 3)).filter((h) => /^\([ABC]\)$/.test(h));
    expect(heads).toEqual(["(A)", "(B)", "(C)"]);
    const given = lesson.sentences[0]!;
    expect(given.steps.at(-1)).toMatchObject({ id: "paper_order", button: "(A)부터 읽어 볼게요" });
  });
});

describe("헷갈리는 단어(선생님 엑셀)는 그 단어가 나오는 문장에서 💡 Tip으로", () => {
  it("6월 37번: 선생님이 O로 확인한 단어만 Tip으로 — 확인 안 한 후보는 안 뜨고, 손으로 쓴 Tip과 겹치지 않는다", async () => {
    const id = "mopyeong-2026-06-37-chaos-pendulum";
    const session = createPolicySession(id, null, { loadStudent: () => ({ ...emptyStudentState(), level: "중" }), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const labels = new Set<string>();
    const lesson = allPolicyLessons().find((l) => l.id === id)!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    for (let g = 0; g < 200 && !v.examOptions; g++) {
      for (const t of [...(v.tips ?? []), ...(v.wordTips ?? [])]) labels.add(t.label);
      const st = steps.get(session.lastAction()?.interactionId ?? "");
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "pick" && st.order && v.pick?.open) v = await session.submit(`__order:${st.answers.join(",")}`);
      else if (st?.type === "pick" && v.pick?.open) for (const a of st.answers) v = await session.submit(`__pick:${a}`);
      else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) v = await session.submit(st.options.find((o) => o.correct)!.label);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    // 아직 안 본 후보(사용 칸이 빈 것)는 안 뜬다
    expect(labels.has("executive")).toBe(false);
    expect(labels.has("fashion")).toBe(true);
    // 손으로 쓴 note Tip과 엑셀 note가 겹치지 않는다 — 같은 이름 하나
    expect([...labels].filter((l) => l.toLowerCase() === "note")).toHaveLength(1);
  });
});

describe("읽는 동안 헷갈리는 단어 Tip을 미리", () => {
  it("3월 36번 (B): 읽기 화면에 표시판 단어 Tip이 뜨고(손으로 쓴 글로), 질문으로 묻는 단어는 빠진다", async () => {
    const id = "moeui-2026-03-36-conversation-stoppers";
    const session = createPolicySession(id, null, { loadStudent: () => ({ ...emptyStudentState(), level: "중" }), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const lesson = allPolicyLessons().find((l) => l.id === id)!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    for (let g = 0; g < 200 && !(v.readingFirst && v.sentence.startsWith("(B)")); g++) {
      const st = steps.get(session.lastAction()?.interactionId ?? "");
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "pick" && v.pick?.open) for (const a of st.answers) v = await session.submit(`__pick:${a}`);
      else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) v = await session.submit(st.options.find((o) => o.correct)!.label);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    expect(v.readingFirst).toBe(true);
    // 단어 Tip은 칩이 아니라 문장 속 색 글자(wordTips)
    const tips = v.wordTips ?? [];
    expect(tips.map((t) => t.label)).toContain("work");
    expect(tips.find((t) => t.label === "work")?.text).toContain("효과가 있다");
  });

  it("3월 38번 주어진 문장: 손으로 쓴 단어 Tip(in that)도 처음 읽는 화면부터", async () => {
    const session = createPolicySession("moeui-2026-03-38-gesture-glue", null, { loadStudent: () => ({ ...emptyStudentState(), level: "중" }), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 6 && !v.readingFirst; g++) v = await session.submit(v.buttons[0] ?? "__auto_next");
    expect(v.readingFirst).toBe(true);
    expect((v.wordTips ?? []).map((t) => t.label)).toContain("in that");
    // 요령 칩(mark 없는 것)은 읽기 화면에 안 뜬다
    expect((v.tips ?? []).map((t) => t.label)).not.toContain("앞을 가리키는 말");
  });

  it("헷갈리는 단어는 trap(평소 뜻과 이 글의 뜻이 다른 단어)만 — 2022년 3월 29번 문장 3: accounts는 O, more A than B Tip은 X", async () => {
    const session = createPolicySession("moeui-2022-03-29-greek-music", null, { loadStudent: () => ({ ...emptyStudentState(), level: "중" }), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const lesson = allPolicyLessons().find((l) => l.id === "moeui-2022-03-29-greek-music")!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    for (let g = 0; g < 200 && !(v.readingFirst && v.sentence.startsWith("So we are forced")); g++) {
      const st = steps.get(session.lastAction()?.interactionId ?? "");
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) v = await session.submit(st.options.find((o) => o.correct)!.label);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    expect(v.readingFirst).toBe(true);
    const labels = (v.wordTips ?? []).map((t) => t.label);
    expect(labels).toEqual(expect.arrayContaining(["accounts", "exercise", "practice"]));
    expect(labels).not.toContain("more A than B");
  });
});

describe("정답 해설 다음 참고(answer_note)", () => {
  it("2022년 3월 29번: 분석 뒤 문제에서 정답 ② → 해설 → 참고(오답률 1위 이유) → 다음 화면", async () => {
    const id = "moeui-2022-03-29-greek-music";
    const session = createPolicySession(id, null, { loadStudent: () => ({ ...emptyStudentState(), level: "중" }), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const lesson = allPolicyLessons().find((l) => l.id === id)!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    for (let g = 0; g < 400 && !v.message.includes("어법상 틀린 것 하나"); g++) {
      const st = steps.get(session.lastAction()?.interactionId ?? "");
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) v = await session.submit(st.options.find((o) => o.correct)!.label);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    const answer = lesson.exam!.options.find((o) => o.correct)!.label;
    v = await session.submit(answer);
    expect(v.message).toBe("정답이에요!");
    expect(v.examExplain?.["2"]?.text).toContain("than");
    v = await session.submit("다음으로");
    expect(v.message).toContain("오답률 1위");
    v = await session.submit("다음으로");
    expect(v.message).not.toContain("오답률 1위");
  });
});

describe("설명 화면 아래 「보충학습실에서 더 공부할게요」", () => {
  it("2022년 3월 29번 ③ 동사·분사 표: 그 버튼을 누르면 「담아 뒀어요」를 다음 말과 줄을 바꿔 말하고 넘어간다", async () => {
    const id = "moeui-2022-03-29-greek-music";
    const session = createPolicySession(id, null, { loadStudent: () => ({ ...emptyStudentState(), level: "중" }), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    const lesson = allPolicyLessons().find((l) => l.id === id)!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    for (let g = 0; g < 300 && session.lastAction()?.interactionId !== "s4_cons_table"; g++) {
      const st = steps.get(session.lastAction()?.interactionId ?? "");
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) v = await session.submit(st.options.find((o) => o.correct)!.label);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
    expect(v.buttons).toEqual(["알겠어요", "나중에 보충학습실에서 더 깊이 공부할게요"]);
    v = await session.submit("나중에 보충학습실에서 더 깊이 공부할게요");
    expect(v.message.startsWith("보충학습실에 담아 뒀어요.\n꼭 외워 둘 것이 있어요.")).toBe(true);
  });
});

describe("끊어읽기", () => {
  it("적어 둔 끊는 자리는 문장에 그대로 있다 (모든 레슨)", () => {
    for (const l of allPolicyLessons()) for (const s of l.sentences) for (const c of s.slashes ?? []) expect(s.text, `${l.id} ${s.id}`).toContain(c);
  });
  it("끊어읽기 때 보이는 S·V·O·C도 문장에 그대로 있다 (모든 레슨)", () => {
    // 「has … survived」처럼 떨어진 두 조각은 조각마다
    for (const l of allPolicyLessons()) for (const s of l.sentences) for (const r of s.roles ?? []) for (const part of r.text.split(" … ")) expect(s.text, `${l.id} ${s.id}`).toContain(part);
  });
  it("[ ]로 묶는 수식어도 문장에 그대로 있다 (모든 레슨)", () => {
    for (const l of allPolicyLessons()) for (const s of l.sentences) for (const m of s.modifiers ?? []) expect(s.text, `${l.id} ${s.id}`).toContain(m);
  });
});

describe("칠판은 정답을 먼저 말하지 않는다 — 질문에 답하기 전엔 이번에 붙을 말(fresh)이 안 보인다", () => {
  it.each(allPolicyLessons().map((l) => l.id))("%s", async (id) => {
    const lesson = allPolicyLessons().find((l) => l.id === id)!;
    const steps = new Map(lesson.sentences.flatMap((s) => s.steps).map((st) => [st.id, st]));
    const session = createPolicySession(id, null, { loadStudent: () => emptyStudentState(), saveStudent() {}, logEvents() {}, now: () => 0 });
    let v = await session.submit("분석하러 갈게요");
    for (let g = 0; g < 600 && !v.examOptions; g++) {
      const st = steps.get(session.lastAction()?.interactionId ?? "");
      if (st?.type === "choice" && !v.readingFirst && v.buttons.length > 1 && !v.buttons.includes("다음으로"))
      {
        expect(JSON.stringify(v.panel ?? {}), st.id).not.toContain('"fresh":true');
        // 빈 칠판(칸만 있고 단어 없음)은 질문 화면에 띄우지 않는다
        if (v.panel && v.panel.kind !== "picture" && !("sort" in v.panel && v.panel.sort))
          expect(/"(words|rows|scenes)":\[\{/.test(JSON.stringify(v.panel)), `${st.id} 빈 칠판`).toBe(true);
      }
      if (v.readingFirst) v = await session.submit("다 읽었어요");
      else if (st?.type === "pick" && st.order && v.pick?.open) v = await session.submit(`__order:${st.answers.join(",")}`);
      else if (st?.type === "pick" && v.pick?.open) for (const a of st.answers) v = await session.submit(`__pick:${a}`);
      else if (st?.type === "choice" && !v.buttons.includes("다음으로") && v.buttons.length > 1) v = await session.submit(st.options.find((o) => o.correct)!.label);
      else v = await session.submit(v.buttons[0] ?? "__auto_next");
    }
  });
});
