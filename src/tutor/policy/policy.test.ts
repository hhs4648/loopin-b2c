import { describe, expect, it } from "vitest";
import { UNKNOWN_BTN, HINT_BTN } from "../engine";
import { decideOnChoice, shouldShow, type DecideInput } from "./decide";
import { stamps } from "./copy";
import { allPolicyLessons, getPolicyCopy } from "./lessons";
import { createPolicySession } from "./session";
import {
  emptyStudentState,
  recordPerformance,
  skillOf,
  type LearningEvent,
  type StudentState,
} from "./student-state";
import type { ChoiceStep, PolicyStep } from "./types";

const LESSON_ID = "moeui-2025-03-21-descartes-tree";
const lesson = allPolicyLessons().find((l) => l.id === LESSON_ID)!;
const copy = getPolicyCopy(LESSON_ID)!;

function harness(student: StudentState = emptyStudentState()) {
  const events: LearningEvent[] = [];
  let saved = student;
  const session = createPolicySession(LESSON_ID, "민지", {
    loadStudent: () => saved,
    saveStudent: (next) => {
      saved = next;
    },
    logEvents: (batch) => events.push(...batch),
    now: () => 0,
  });
  return { session, events, student: () => saved };
}

function correctLabel(stepId: string): string {
  const step = lesson.sentences.flatMap((s) => s.steps).find((s) => s.id === stepId) as ChoiceStep;
  return step.options.find((o) => o.correct)!.label;
}

function wrongLabels(stepId: string): string[] {
  const step = lesson.sentences.flatMap((s) => s.steps).find((s) => s.id === stepId) as ChoiceStep;
  return step.options.filter((o) => !o.correct).map((o) => o.label);
}

type Session = ReturnType<typeof harness>["session"];

/** 도입을 첫 번째 보기로 끝까지 넘긴다 → 읽기 화면 */
async function passIntro(session: Session) {
  let v = session.view();
  for (let guard = 0; guard < 12 && v.screen === "chat"; guard++) v = await session.submit(v.buttons[0]!);
  return v;
}

/** 도입 → 지문 읽기 → 「분석부터 할게요」 → 1문장 첫 질문 */
async function startAnalysis(session: Session) {
  let v = await passIntro(session);
  if (v.screen === "read") v = await session.submit("계속");
  return session.submit("분석부터 할게요");
}

/** 1문장을 혼자 다 맞히고 2문장 첫 질문까지 간다 */
async function passSentence1(session: Session) {
  let v = await startAnalysis(session);
  v = await session.submit(correctLabel("s1_meaning"));
  v = await session.submit("다음으로");
  v = await session.submit(correctLabel("s1_subject"));
  for (let i = 0; i < 4; i++) v = await session.submit(v.buttons[0]!);
  return v;
}

const input = (student = emptyStudentState()): DecideInput => ({
  student,
  context: lesson.context,
  item: lesson.item,
  sentence: lesson.sentences[0]!,
});

describe("정책 — 개입 사다리 (§10)", () => {
  const step = lesson.sentences[0]!.steps[0] as ChoiceStep;
  const wrong = { kind: "answer", correct: false, optionId: "b", latencyMs: 0 } as const;
  const dontKnow = { kind: "dont_know", latencyMs: 0 } as const;

  it("처음 틀리면 설명이 아니라 가벼운 힌트다", () => {
    expect(decideOnChoice(step, { rung: 0, wrongPicks: [] }, wrong, input()).action).toBe(
      "GIVE_LIGHT_HINT",
    );
  });

  it("바로 「모르겠어요」를 눌러도 힌트가 먼저다", () => {
    const actions = [0, 1, 2].map(
      (rung) => decideOnChoice(step, { rung, wrongPicks: [] }, dontKnow, input()).action,
    );
    expect(actions).toEqual(["GIVE_LIGHT_HINT", "GIVE_STRONG_HINT", "EXPLAIN"]);
  });

  it("보기가 하나만 남으면 더 묻지 않고 설명한다", () => {
    expect(decideOnChoice(step, { rung: 1, wrongPicks: ["c"] }, wrong, input()).action).toBe(
      "EXPLAIN",
    );
  });

  it("stable인 skill에서 뜻밖에 틀리면 스스로 고칠 기회를 준다 (§4)", () => {
    let student = emptyStudentState();
    student = recordPerformance(student, "sentence_meaning", "independent_success", 0);
    student = recordPerformance(student, "sentence_meaning", "independent_success", 0);
    expect(skillOf(student, "sentence_meaning").status).toBe("stable");
    expect(decideOnChoice(step, { rung: 0, wrongPicks: [] }, wrong, input(student)).action).toBe(
      "GIVE_SELF_CORRECTION_OPPORTUNITY",
    );
  });
});

describe("정책 — 무엇을 보여 줄까", () => {
  const structure = lesson.sentences[0]!.steps.find((s) => s.id === "s1_structure") as PolicyStep;

  it("정답이어도 가치가 높은 문장은 뼈대를 짧게 본다 — 3지선다는 찍을 수 있다 (§6)", () => {
    expect(shouldShow(structure, input(), false)).toBe(true);
  });

  it("거듭 혼자 맞혀 온 학생에게는 같은 설명을 되풀이하지 않는다", () => {
    let student = emptyStudentState();
    student = recordPerformance(student, "long_subject", "independent_success", 0);
    student = recordPerformance(student, "long_subject", "independent_success", 0);
    expect(shouldShow(structure, input(student), false)).toBe(false);
    // 그래도 이번에 막혔으면 본다
    expect(shouldShow(structure, input(student), true)).toBe(true);
  });

  it("「필요하면」 주는 도움은 막혔을 때만 나온다", () => {
    const asNote = lesson.sentences[2]!.steps.find((s) => s.id === "s3_as_structure")!;
    expect(shouldShow(asNote, input(), false)).toBe(false);
    expect(shouldShow(asNote, input(), true)).toBe(true);
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

describe("21번 수업 흐름", () => {
  it("첫 화면은 인사 없이 오답률 소개로 연다", () => {
    const named = harness().session.view();
    expect(named.message).toBe("이번 문제는 오답률 57.4%로, 오답률 Top7 문제예요. 자신 있나요~?");
    // 칠판에는 데카르트의 나무가 그려져 있다
    expect(named.boardImage?.kind).toBe("drawing");
    expect(named.buttons).toEqual(["네~", "앗 걱정돼요.."]);

    const anonymous = createPolicySession(LESSON_ID, null, { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 }).view();
    expect(anonymous.message.startsWith("이번 문제는")).toBe(true);
  });

  it("도입: 데카르트를 아는지 → 모르면 사진과 설명 → 17세기 질문 → 지문으로", async () => {
    const { session } = harness();
    let v = await session.submit("앗 걱정돼요..");
    // 글 소개는 칠판 제목이 한다 — 바로 데카르트 질문
    expect(v.message).toBe("괜찮아요, 같이 차근차근 봐요! 수업 들어가기 전에, 배경지식 조금만 살펴봐요. 혹시 데카르트가 누군지 아나요?");
    expect(v.buttons).toEqual(["네, 알아요 😀", "들어는 봤어요 😮", "잘 몰라요 😓"]);
    expect(v.studentLine).toBe("");

    v = await session.submit("잘 몰라요 😓");
    expect(v.message).toContain("17세기 프랑스 철학자");
    expect(v.boardImage?.alt).toBe("데카르트 초상");
    expect(v.buttons).toEqual(["네"]);
    v = await session.submit("네");
    expect(v.boardImage?.kind).toBe("drawing"); // 사진이 내려가면 나무가 돌아온다
    expect(v.message).toBe("데카르트가 살던 17세기에는 과학과 철학의 관계가 어땠을까요?");

    v = await session.submit("흠.. 잘 모르겠어요");
    expect(v.message.startsWith("답은 '과학과 철학이 비슷하게 여겨졌다'예요.")).toBe(true);
    v = await session.submit("네");
    expect(v.message).toBe("그럼 지문을 한번 살펴볼까요?");
    expect(v.buttons).toEqual(["네, 좋아요!"]);
    v = await session.submit("네, 좋아요!");
    expect(v.screen).toBe("read");
  });

  it("도입: 데카르트를 안다고 하면 설명 없이 다음 질문이 한 화면에 붙는다", async () => {
    const { session } = harness();
    await session.submit("네~");
    let v = await session.submit("네, 알아요 😀");
    expect(v.message).toBe("잘 알고 있군요~ 데카르트가 살던 17세기에는 과학과 철학의 관계가 어땠을까요?");
    expect(v.boardImage?.kind).toBe("drawing");
    v = await session.submit("과학과 철학이 비슷하게 여겨졌어요");
    expect(v.message.startsWith("맞아요~~")).toBe(true);
  });

  it("도입의 선생님 말은 한 화면에 세 문장까지", async () => {
    const lines = Object.values(copy.intro ?? {}).flatMap((x) =>
      typeof x === "string" ? [] : Object.values(x),
    );
    const long = lines.filter((line) => (line.match(/[.?!~](\s|$)/g) ?? []).length > 3);
    expect(long).toEqual([]);
  });

  it("첫 문장: 뜻 고르기 → 맞혀도 주어 범위 묻기 → 뼈대 → unity → 다리 질문 → 2문장", async () => {
    const { session } = harness();
    let v = await startAnalysis(session);
    expect(v.screen).toBe("study");
    expect(session.lastAction()?.action).toBe("ASK_MEANING_CHOICE");
    expect(v.buttons).toContain(UNKNOWN_BTN);

    // 칭찬 + 뜻 되짚기가 한 말풍선. 그다음에 구조 질문
    v = await session.submit(correctLabel("s1_meaning"));
    expect(v.message.startsWith("맞았어요!")).toBe(true);
    expect(v.buttons).toEqual(["다음으로"]);

    // 객관식은 찍을 수 있다 — 맞혀도 구조를 한 번 묻는다
    v = await session.submit("다음으로");
    expect(session.lastAction()?.action).toBe("ASK_STRUCTURE");
    expect(v.message).toContain("주어가 어디까지일까요?");
    expect(v.panel).toBeNull();

    v = await session.submit(correctLabel("s1_subject"));
    expect(session.lastAction()?.action).toBe("SHOW_STRUCTURE");
    expect(v.panel?.kind).toBe("structure");

    v = await session.submit(v.buttons[0]!);
    expect(v.highlight).toEqual(["unity"]);
    expect(v.panel).toBeNull();

    // 요약 그림은 다음 화면에
    v = await session.submit(v.buttons[0]!);
    expect(session.lastAction()?.interactionId).toBe("s1_summary");
    expect(v.panel?.kind).toBe("structure");

    v = await session.submit(v.buttons[0]!);
    expect(session.lastAction()?.action).toBe("ASK_BRIDGE");

    v = await session.submit(v.buttons[0]!);
    expect(v.progressIndex).toBe(2);
  });

  it("2문장은 괄호를 뺀 뼈대부터 보여 주고, 끝에 괄호를 되돌린다 (§13)", async () => {
    const { session } = harness();
    let v = await passSentence1(session);

    expect(v.sentence).not.toContain("(");
    v = await session.submit(correctLabel("s2_correspond"));
    expect(v.panel?.kind).toBe("mapping");
    v = await session.submit(correctLabel("s2_map_trunk"));
    v = await session.submit(correctLabel("s2_map_fruit"));
    // 혼자 다 맞혔으니 what 보충은 건너뛴다. 병렬 구조는 본다
    expect(session.lastAction()?.interactionId).toBe("s2_parallel");
    v = await session.submit(v.buttons[0]!);
    expect(session.lastAction()?.interactionId).toBe("s2_restore");
    expect(v.sentence).toContain("(the intelligible principles)");
  });

  it("오답 → 그 오개념을 겨냥한 힌트 → 보기에서 빠진다 → 또 틀리면 설명", async () => {
    const { session, student } = harness();
    await startAnalysis(session);
    const [b, c] = wrongLabels("s1_meaning");

    let v = await session.submit(b!);
    expect(session.lastAction()?.action).toBe("GIVE_LIGHT_HINT");
    expect(v.message).toContain("반대");
    expect(v.buttons).not.toContain(b);
    // 정답을 먼저 말하지 않는다
    expect(v.message).not.toContain("정답은");

    v = await session.submit(c!);
    expect(session.lastAction()?.action).toBe("EXPLAIN");
    expect(v.buttons).toEqual(["다음으로"]);

    await session.submit("다음으로");
    // 문장이 끝나야 저장한다 (설명을 본 뒤라 칭찬 말풍선은 없다)
    await session.submit(correctLabel("s1_subject"));
    for (let i = 0; i < 4; i++) await session.submit("다음으로");
    expect(skillOf(student(), "sentence_meaning").failure).toBe(1);
  });

  it("「이미 알고 있어요」로 주어 질문을 넘기면 뼈대 그림도 같이 건너뛴다", async () => {
    const { session, events, student } = harness();
    await startAnalysis(session);
    await session.submit(correctLabel("s1_meaning"));
    let v = await session.submit("다음으로");
    expect(v.buttons).toContain("넘어갈게요");
    v = await session.submit("넘어갈게요");
    expect(session.lastAction()?.interactionId).toBe("s1_unity");
    // 틀린 뒤에는 넘길 수 없다
    const other = harness().session;
    await startAnalysis(other);
    await other.submit(correctLabel("s1_meaning"));
    await other.submit("다음으로");
    v = await other.submit(wrongLabels("s1_subject")[0]!);
    expect(v.buttons).not.toContain("넘어갈게요");
    // 맞힌 것으로 적지 않는다. 넘겼다는 기록은 남는다 (문장이 끝나야 쌓인다)
    for (let i = 0; i < 3; i++) await session.submit("다음으로");
    expect(skillOf(student(), "long_subject").independent).toBe(0);
    expect(events.some((e) => (e.observation as { kind: string }).kind === "skip")).toBe(true);
  });

  it("틀렸다가 스스로 고친 턴만 반짝인다", async () => {
    const { session } = harness();
    await startAnalysis(session);
    await session.submit(wrongLabels("s1_meaning")[0]!);
    const v = await session.submit(correctLabel("s1_meaning"));
    expect(v.effect).toBe("light");
  });

  it("도움말은 사다리를 건드리지 않고, 「모른다」로 적지도 않는다 (§20)", async () => {
    const { session, events } = harness();
    // 1문장은 도움말 대신 단어 강조를 쓴다. 도움말 칩은 2문장에 있다
    let v = await passSentence1(session);
    expect(v.emphasis).toEqual([]);
    v = await session.submit("형이상학이 뭐예요?");
    expect(v.message).toContain("근본 원리");
    // 도움말을 읽는 동안은 보기를 치운다 — 글이 너무 많다
    expect(v.buttons).toEqual(["이어서 할게요"]);
    v = await session.submit("이어서 할게요");
    expect(v.message).toBe("그럼 'corresponded to'의 뜻을 골라 봐요.");
    expect(v.buttons).toContain(correctLabel("s2_correspond"));
    const after = await session.submit(correctLabel("s2_correspond"));
    expect(after.effect).toBeNull();
    // 첫 스텝이 지나면 칩은 숨는다
    expect(after.helps).toEqual([]);
    for (const id of ["s2_map_trunk", "s2_map_fruit"]) await session.submit(correctLabel(id));
    for (let i = 0; i < 3; i++) await session.submit("다음으로");
    expect(events.some((e) => (e.observation as { kind: string }).kind === "help_click")).toBe(true);
    expect(events.find((e) => e.stepId === "s2_correspond" && e.outcome)?.outcome).toBe(
      "independent_success",
    );
  });

  it("보기 밖의 말은 시도로 세지 않는다", async () => {
    const { session } = harness();
    await startAnalysis(session);
    const v = await session.submit("음 글쎄요");
    expect(v.buttons).toHaveLength(4);
    expect(session.lastAction()?.action).toBe("ASK_MEANING_CHOICE");
  });

  it("생각해 보기는 채점하지 않는다 — 힌트는 한 번, 그다음 정리", async () => {
    const { session } = harness();
    let v = await passSentence1(session);
    for (const id of ["s2_correspond", "s2_map_trunk", "s2_map_fruit"]) {
      v = await session.submit(correctLabel(id));
    }
    for (let i = 0; i < 2; i++) v = await session.submit(v.buttons[0]!);
    v = await session.submit(correctLabel("s3_as"));
    expect(session.lastAction()?.interactionId).toBe("s3_quotes");
    expect(v.buttons).toEqual(["생각해 봤어요", HINT_BTN]);

    v = await session.submit(HINT_BTN);
    expect(v.buttons).toEqual(["생각해 봤어요"]);
    v = await session.submit("비유라서요");
    expect(session.lastAction()?.action).toBe("SUMMARIZE");

    v = await session.submit(v.buttons[0]!);
    // 앞 문장의 나무를 다시 꺼낸다 (§15)
    expect(session.lastAction()?.reason).toContain("retrieve_previous_representation");
    expect(v.panel?.kind).toBe("mapping");
  });

  it("끝까지 혼자 맞히면 결과는 「이해」 — 마지막에 시험 문제를 풀고 끝난다", async () => {
    const { session } = harness();
    let v = await startAnalysis(session);
    for (let guard = 0; guard < 80 && !v.ended && v.progressLabel !== "문제 풀기"; guard++) {
      const id = session.lastAction()?.interactionId ?? "";
      const step = lesson.sentences.flatMap((s) => s.steps).find((s) => s.id === id);
      const resolved = v.buttons.length === 1;
      v = await session.submit(step?.type === "choice" && !resolved ? correctLabel(id) : v.buttons[0]!);
    }
    expect(v.progressLabel).toBe("문제 풀기");
    expect(v.buttons).toHaveLength(5);
    expect(v.highlight).toEqual(["the tree was cut in the middle"]);
    v = await session.submit(lesson.exam!.options.find((o) => o.correct)!.label);
    expect(v.ended).toBe(true);
    expect(v.screen).toBe("chat");
    expect(v.message.startsWith("정답이에요!")).toBe(true);
    expect(v.recordLine).toContain("결과=이해");
    // 마무리에는 물음표를 채운 나무가 칠판에
    expect(v.boardImage?.src).toBe("/assets/descartes-tree-filled.svg");
  });

  it("인트로에 오답률을 말하고, 지문이 한 문장씩 드러나며 읽힌다", async () => {
    const { session } = harness();
    expect(session.view().message).toContain("오답률 57.4%");
    let v = await passIntro(session);
    expect(v.screen).toBe("read");
    expect(v.passage?.revealed).toBe(1);
    expect(v.passage?.sentences).toHaveLength(8);
    expect(v.passage?.underline).toBe("the tree was cut in the middle");
    expect(v.buttons).toEqual(["계속"]);
    // 화면이 한 문장을 다 읽으면 다음 문장이 드러난다
    v = await session.submit("__read_next");
    expect(v.passage?.revealed).toBe(2);
    expect(v.passage?.current).toBe(1);
    for (let i = 0; i < 10; i++) v = await session.submit("__read_next");
    expect(v.passage?.revealed).toBe(8); // 끝에서 더 가지 않는다
    v = await session.submit("계속");
    expect(v.screen).toBe("chat");
    expect(v.buttons).toEqual(["바로 풀어 볼게요", "분석부터 할게요"]);
  });

  it("「계속」은 다 읽기 전에도 넘어간다", async () => {
    const { session } = harness();
    await passIntro(session);
    const v = await session.submit("계속");
    expect(v.screen).toBe("chat");
  });

  it("바로 풀기: 맞혀도 분석으로, 틀려도 답을 말하지 않는다", async () => {
    const { session, events } = harness();
    let v = await passIntro(session);
    v = await session.submit("계속");
    v = await session.submit("바로 풀어 볼게요");
    expect(v.progressLabel).toBe("문제 풀기");
    expect(v.numbered).toBe(true);
    v = await session.submit(lesson.exam!.options[2]!.label); // 오답
    expect(v.message).not.toContain("①");
    expect(v.message).toContain("정답을 말하지 않을게요");
    expect(v.buttons).toEqual(["분석 시작할게요"]);
    v = await session.submit("분석 시작할게요");
    expect(session.lastAction()?.interactionId).toBe("s1_meaning");

    const other = harness().session;
    await passIntro(other);
    await other.submit("계속");
    await other.submit("바로 풀어 볼게요");
    v = await other.submit(lesson.exam!.options[0]!.label); // 정답
    expect(v.message).toContain("맞았어요");
    expect(v.buttons).toEqual(["분석 시작할게요"]);
    void events;
  });
});

describe("21번 글 — 절대 규칙", () => {
  const steps = lesson.sentences.flatMap((s) => s.steps);
  const lines = [
    copy.closing,
    ...Object.values(copy.helps).map((h) => h.answer),
    ...Object.values(copy.steps).flatMap((c) => [
      c.ask, c.reask, ...(c.hints ?? []), c.explain, c.praise, c.say, c.hint, c.summary,
      ...Object.values(c.feedback ?? {}),
    ]),
  ].filter((line): line is string => !!line);

  it("대사가 낡지 않았다 — brief를 고쳤으면 대사도 다시 뽑는다", () => {
    /*
      가르치는 내용(brief)만 고치고 대사를 그대로 두면 학생은 예전 말을 듣는다.
      `node scripts/policy_copy.mjs prompt`로 다시 뽑고 `stamp`로 도장을 찍는다.
    */
    const stale = stamps(lesson, copy).filter(([, now, stamped]) => now !== stamped).map(([slot]) => slot);
    expect(stale).toEqual([]);
  });

  it("brief에 있는 말은 대사에도 다 있다", () => {
    for (const step of steps) {
      const c = copy.steps[step.id] as Record<string, unknown> | undefined;
      expect(c, step.id).toBeTruthy();
      for (const key of Object.keys(step.brief)) expect(c![key], `${step.id}.${key}`).toBeTruthy();
    }
  });

  it("한 턴에 질문 하나", () => {
    const many = lines.filter((line) => (line.match(/\?/g) ?? []).length > 1);
    expect(many).toEqual([]);
  });

  it("해요체 — 반말로 끝나는 문장이 없다", () => {
    const banmal = lines
      .flatMap((line) => line.split(/(?<=[.!?])\s+/))
      .filter((sentence) => /(?:[^요죠]|^)[.!?]$/.test(sentence.replace(/[\s😊^'’"”)]+$/u, "")) && /[가-힣]/.test(sentence))
      .filter((sentence) => !/[요죠][.!?]?$/.test(sentence.replace(/[\s😊^]+$/u, "")));
    expect(banmal).toEqual([]);
  });

  it("질문과 힌트는 정답 보기를 미리 말하지 않는다", () => {
    for (const step of steps) {
      if (step.type !== "choice") continue;
      const answer = step.options.find((o) => o.correct)!.label;
      if (!/[가-힣]/.test(answer)) continue; // 영어 보기는 문장에 그대로 나오는 말이다
      const c = copy.steps[step.id]!;
      for (const line of [c.ask!, ...c.hints!, ...Object.values(c.feedback ?? {})]) {
        expect(line, step.id).not.toContain(answer);
      }
    }
  });

  it("1문장의 강조 단어에는 뜻이 있고, 다음 문장에서 찾을 대응(뿌리→형이상학 …)을 미리 말하지 않는다", () => {
    const s1 = lesson.sentences[0]!;
    for (const word of s1.emphasis ?? []) {
      const gloss = s1.glosses.find((g) => g.en === word);
      expect(gloss, word).toBeTruthy();
      for (const banned of ["형이상학", "물리학", "응용과학"]) expect(gloss!.ko).not.toContain(banned);
    }
  });

  it("보기는 세 개, 정답은 하나 (AUTHORING_RULES §2-4)", () => {
    for (const step of steps) {
      if (step.type !== "choice") continue;
      expect(step.options, step.id).toHaveLength(3);
      expect(step.options.filter((o) => o.correct), step.id).toHaveLength(1);
    }
  });

  it("인트로는 자신 있는지 묻는 두 버튼, 고유명사 칩 없음 (AUTHORING_RULES §1)", () => {
    const v = harness().session.view();
    expect(v.buttons).toEqual(["네~", "앗 걱정돼요.."]);
    expect(v.properNouns).toEqual([]);
  });

  it("강조·점진 공개 구절이 실제 문장 안에 있다", () => {
    for (const sentence of lesson.sentences) {
      for (const step of sentence.steps) {
        const shown = step.display ?? sentence.text;
        for (const phrase of step.highlight ?? []) expect(shown, step.id).toContain(phrase);
      }
    }
  });

  it("이름으로 부른 그림이 레슨에 있다", () => {
    for (const step of steps) {
      for (const ref of [step.panel, "panel_after" in step ? step.panel_after : undefined]) {
        if (typeof ref === "string") expect(lesson.panels?.[ref], step.id).toBeTruthy();
      }
    }
  });
});

/*
  지문마다 지키는 규칙 (AUTHORING_RULES §2) — 모든 Teaching Policy 레슨에 돈다.
  새 지문을 넣으면 여기서 같이 검사된다.
*/
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
      if (L.exam) expect(L.sentences.some((s) => s.text.includes(L.exam!.underline))).toBe(true);
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
    expect(v.message).toBe("아쉽게도 아니에요. 정답은 분석하면서 같이 찾아봐요.");
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

  it("틀리면 「아쉽게도 아니에요.」 + 이유, 다시 고르게 하지 않고 넘어간다", async () => {
    const { session } = await toAnalysis();
    let v = await session.submit("같아요");
    expect(v.message.startsWith("아쉽게도 아니에요. 'without'을 봐요.")).toBe(true);
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
    expect(v.message).toBe("아쉽게도 아니에요. science는 지도에도 있지만, 글에선 과학을 흉내 내요. 구별하는 게 아니에요.");
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
