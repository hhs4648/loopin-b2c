import frame from "../../../content/tutor/frame.json";
import policyFrame from "../../../content/tutor/policy-frame.json";
import type { TutorResult } from "../../../content/tutor/types";
import { READY_BTN, UNKNOWN_BTN, HINT_BTN, type PointRecord, type TutorView } from "../engine";
import { lookupGloss } from "../glosses";
import { isUnknownInput, matchChoice } from "../match";
import { askedAboutWord } from "../proper-nouns";
import { decideOnChoice, openingAction, shouldShow, type DecideInput } from "./decide";
import { choiceCopy, showCopy, thinkCopy } from "./copy";
import { getPolicyCopy, getPolicyLesson } from "./lessons";
import {
  appendEvents,
  loadStudentState,
  recordPerformance,
  saveStudentState,
  type LearningEvent,
  type StudentState,
} from "./student-state";
import type {
  ChoiceStep,
  Observation,
  PanelRef,
  PerformanceStatus,
  PolicyLesson,
  PolicySentence,
  PolicyStep,
  StudyPanel,
  TeachingAction,
  UiObservation,
} from "./types";

/**
 * Teaching Policy 레슨의 세션 — **Presentation 쪽 절반**이다 (명세 §2).
 *
 * 정책(`decide.ts`)이 고른 `TeachingAction`을 받아, **미리 뽑아 둔 대사**에서 그 행동에
 * 맞는 것을 꺼내 기존 화면(`TutorView`)에 싣는다. 모델을 부르지 않는다. 예전 엔진의 `createSession`과
 * **같은 모양**을 돌려주므로 `App`·교실 화면·문장 학습 화면은 그대로 쓴다.
 *
 * 예전 엔진에서 그대로 지키는 것: 한 턴에 하나, 매 턴 학생을 기다린다,
 * 정답은 학생이 시도하기 전에 말하지 않는다, 해요체.
 */

const L = policyFrame.lines;
const NEXT_BTN = policyFrame.buttons.next;
const THOUGHT_BTN = policyFrame.buttons.thought;
const BACK_BTN = policyFrame.buttons.back;
const SKIP_BTN = policyFrame.buttons.skip;
const READ_DONE_BTN = policyFrame.buttons.read_done;
/** 읽기 화면이 한 문장을 다 읽었을 때 보내는 신호. 학생의 말이 아니다 */
export const READ_NEXT_CMD = "__read_next";
const MODE_TRY_BTN = policyFrame.buttons.mode_try;
const MODE_ANALYZE_BTN = policyFrame.buttons.mode_analyze;
const ANALYZE_START_BTN = policyFrame.buttons.analyze_start;

/** 기기 저장소·시계를 갈아 끼울 수 있게 — 테스트에서 쓴다 */
export type PolicyDeps = {
  loadStudent: () => StudentState;
  saveStudent: (state: StudentState) => void;
  logEvents: (events: LearningEvent[]) => void;
  now: () => number;
};

const DEFAULT_DEPS: PolicyDeps = {
  loadStudent: loadStudentState,
  saveStudent: saveStudentState,
  logEvents: appendEvents,
  now: () => Date.now(),
};

type State = {
  learnerName: string | null;
  /**
   * 이름은 묻지 않는다 — 가입할 때 넣는 것이다. 알면 부르고, 모르면 그냥
   * "안녕하세요!"로 연다. 예전 엔진의 `greeting` 단계는 여기 없다.
   */
  /**
   *   intro → read(지문을 한 문장씩, 소리와 함께) → mode(바로 풀까, 분석부터 할까)
   *   → exam_first(고르면) → lesson → exam_final → done
   * 시험 문제가 없는 레슨은 read 뒤에 바로 lesson으로 간다.
   */
  stage: "intro" | "read" | "mode" | "exam_first" | "lesson" | "exam_final" | "done";
  /** 읽기 단계에서 보고 있는 문장 */
  ri: number;
  /** 처음에 풀어 봤다면 그 결과 */
  firstAnswer: { optionId: string; correct: boolean } | null;
  si: number;
  pi: number;
  /** choice: 풀이 중 → 끝남(설명을 봤다). think: 생각 중 → 정리를 봤다 */
  resolved: boolean;
  rung: number;
  wrongPicks: string[];
  thinkHinted: boolean;
  /** 이 문장의 질문에서 틀렸거나 도움을 받았나 */
  struggledInSentence: boolean;
  /** 이 문장에서 「이미 알고 있어요」로 넘긴 스텝 */
  skipped: string[];
  anyAssisted: boolean;
  anyExplained: boolean;
  student: StudentState;
  message: string;
  buttons: string[];
  studentLine: string;
  effect: null | "light";
  panel: StudyPanel | null;
  /**
   * 도움말을 읽는 동안 치워 둔 질문. 도움말은 길어서 보기와 같이 두면 화면이
   * 글로 꽉 찬다 — 보기를 잠깐 없애고, 「이어서 할게요」로 돌아온다.
   */
  aside: { message: string; buttons: string[] } | null;
  shownAt: number;
  lastAction: TeachingAction | null;
};

export function createPolicySession(
  lessonId: string,
  learnerName?: string | null,
  deps: Partial<PolicyDeps> = {},
) {
  const found = getPolicyLesson(lessonId);
  if (!found) throw new Error(`policy lesson not found: ${lessonId}`);
  const lesson: PolicyLesson = found;
  const foundCopy = getPolicyCopy(lessonId);
  if (!foundCopy) throw new Error(`policy copy not found: ${lessonId}`);
  const copy = foundCopy;
  const d: PolicyDeps = { ...DEFAULT_DEPS, ...deps };

  let pending: LearningEvent[] = [];
  /*
    **정책은 수업을 시작할 때의 학생을 보고 판단한다.** 오늘 방금 두 번 맞힌 걸로
    stable이 되면, 같은 문장 안에서 두 칸을 채웠다는 이유로 설명을 접게 된다 —
    즉시 수행은 기억이 아니다 (§17). 오늘 쌓인 기록은 다음 수업부터 쓰인다.
  */
  let baseline: StudentState = d.loadStudent();
  let s = initial(learnerName?.trim() || null);

  function initial(name: string | null): State {
    const base: State = {
      learnerName: name,
      stage: "intro",
      ri: 0,
      firstAnswer: null,
      si: 0,
      pi: 0,
      resolved: false,
      rung: 0,
      wrongPicks: [],
      thinkHinted: false,
      struggledInSentence: false,
      skipped: [],
      anyAssisted: false,
      anyExplained: false,
      student: baseline,
      message: introMessage(name),
      // 「준비됐나요?」에 「잘 모르겠어요」는 답이 아니다 — 시작 버튼 하나만
      buttons: [READY_BTN],
      studentLine: "",
      effect: null,
      panel: null,
      aside: null,
      shownAt: d.now(),
      lastAction: null,
    };
    return base;
  }

  function introMessage(name: string | null): string {
    const hello = name
      ? frame.fixed_lines.greet_named.replace("{name}", name)
      : frame.fixed_lines.greet_plain;
    const rate = lesson.exam?.wrong_rate;
    return [
      hello,
      ...(rate != null ? [L.intro_rate.replace("{rate}", String(rate))] : []),
      L.intro_topic.replace("{topic}", copy.topic_intro),
      frame.fixed_lines.ready_question,
    ].join(" ");
  }

  /* ── 지문 읽기 · 문제 풀기 ──────────────────────────────────────── */

  function startReading() {
    s = { ...s, stage: "read", ri: 0, message: L.read_intro, buttons: [READ_DONE_BTN], panel: null };
  }

  /** 읽기 화면이 한 문장을 다 읽었다 — 다음 문장을 드러낸다. 마지막이면 그대로 둔다 */
  function readNext() {
    const last = lesson.sentences.length - 1;
    if (s.ri < last) s = { ...s, ri: s.ri + 1 };
  }

  /** 다 읽었으면: 시험 문제가 있으면 어떻게 할지 고르게, 없으면 바로 분석 */
  function askMode() {
    if (!lesson.exam) return startLesson();
    s = { ...s, stage: "mode", message: L.choose_mode, buttons: [MODE_TRY_BTN, MODE_ANALYZE_BTN] };
  }

  function startLesson() {
    s = { ...s, stage: "lesson", si: 0, pi: 0 };
    open(L.start_known);
  }

  /** 밑줄 친 구절이 든 문장 — 문제 화면에 띄운다 */
  function examSentence(): PolicySentence {
    const u = lesson.exam!.underline;
    return lesson.sentences.find((x) => x.text.includes(u)) ?? lesson.sentences[lesson.sentences.length - 1]!;
  }

  function askExam(when: "first" | "final") {
    const ex = copy.exam!;
    s = {
      ...s,
      stage: when === "first" ? "exam_first" : "exam_final",
      si: lesson.sentences.indexOf(examSentence()),
      message: `${when === "final" ? L.final_lead : ""}${ex.ask}`,
      buttons: lesson.exam!.options.map((o) => o.label),
      panel: null,
      shownAt: d.now(),
    };
  }

  function onExam(text: string) {
    const exam = lesson.exam!;
    const ex = copy.exam!;
    const n = text.match(/^([1-9])\s*번?$/)?.[1];
    const picked = n
      ? exam.options[Number(n) - 1]
      : exam.options.find((o) => o.label === text) ??
        exam.options.find((o) => o.label === matchChoice(text, exam.options.map((x) => x.label)));
    if (!picked) {
      s = { ...s, message: `${L.pick_from_buttons} ${ex.ask}` };
      return;
    }
    const correct = !!picked.correct;
    const when = s.stage === "exam_first" ? "first" : "final";
    pending.push({
      at: new Date(d.now()).toISOString(),
      lessonId: lesson.id,
      sentenceId: examSentence().id,
      stepId: `exam_${when}`,
      observation: { kind: "exam", when, correct, optionId: picked.id },
      action: { action: when === "first" ? "CONTINUE" : "FINISH", reason: [correct ? "exam_correct" : "exam_wrong"] },
    });
    if (when === "first") {
      // 찍어서 맞힐 수 있다 — 맞혀도 분석은 한다. 틀려도 답을 말하지 않는다 (§6)
      s = {
        ...s,
        firstAnswer: { optionId: picked.id, correct },
        message: correct ? ex.first_correct : ex.first_wrong,
        buttons: [ANALYZE_START_BTN],
      };
      return;
    }
    s = { ...s, anyExplained: s.anyExplained || !correct, effect: correct && s.firstAnswer && !s.firstAnswer.correct ? "light" : null };
    finish(`${correct ? ex.final_correct : ex.final_wrong} `);
  }

  const sentence = (): PolicySentence => lesson.sentences[s.si]!;
  const step = (): PolicyStep => sentence().steps[s.pi]!;
  const input = (): DecideInput => ({
    student: baseline,
    context: lesson.context,
    item: lesson.item,
    sentence: sentence(),
  });

  function panelOf(ref?: PanelRef): StudyPanel | null {
    if (!ref) return null;
    return typeof ref === "string" ? (lesson.panels?.[ref] ?? null) : ref;
  }

  function log(observation: Observation | UiObservation | { kind: "help_click"; helpId: string }, action: TeachingAction | null, outcome?: PerformanceStatus) {
    pending.push({
      at: new Date(d.now()).toISOString(),
      lessonId: lesson.id,
      sentenceId: sentence().id,
      stepId: step().id,
      observation,
      action,
      ...(outcome ? { outcome } : {}),
    });
  }

  function flush() {
    d.logEvents(pending);
    pending = [];
    d.saveStudent(s.student);
  }

  /* ── 버튼 ───────────────────────────────────────────────────────── */

  function choiceButtons(st: ChoiceStep): string[] {
    const left = st.options.filter((o) => !s.wrongPicks.includes(o.id)).map((o) => o.label);
    // 넘기기는 혼자 시도하기 전에만. 한 번 틀리고 나서 「이미 안다」는 말이 안 된다
    const skip = st.skippable && s.rung === 0 && !s.wrongPicks.length ? [SKIP_BTN] : [];
    return [...left, UNKNOWN_BTN, ...skip];
  }

  function buttonsFor(st: PolicyStep): string[] {
    if (st.type === "choice") return s.resolved ? [NEXT_BTN] : choiceButtons(st);
    if (st.type === "think") {
      if (s.resolved) return [NEXT_BTN];
      return s.thinkHinted ? [THOUGHT_BTN] : [THOUGHT_BTN, HINT_BTN];
    }
    return [st.button ?? NEXT_BTN];
  }

  /* ── 스텝 열기 · 넘어가기 ───────────────────────────────────────── */

  /** 지금 자리(si, pi)에서 시작해, 정책이 보여 주기로 한 첫 스텝을 연다 */
  function open(lead: string) {
    for (;;) {
      if (s.si >= lesson.sentences.length) {
        // 분석이 끝나면 시험 문제를 (다시) 푼다. 문제가 없는 레슨은 바로 마무리
        if (lesson.exam) return askExam("final");
        return finish(lead);
      }
      if (s.pi >= sentence().steps.length) {
        s = { ...s, si: s.si + 1, pi: 0, struggledInSentence: false, skipped: [] };
        flush();
        continue;
      }
      const withSkipped = step().skip_with && s.skipped.includes(step().skip_with!);
      if (!withSkipped && shouldShow(step(), input(), s.struggledInSentence)) break;
      log({ kind: "continue" }, {
        action: "CONTINUE",
        interactionId: step().id,
        reason: [withSkipped ? "skipped_by_student" : "skipped_by_policy"],
      });
      s = { ...s, pi: s.pi + 1 };
    }
    const st = step();
    const action = openingAction(st, input());
    s = {
      ...s,
      resolved: false,
      rung: 0,
      wrongPicks: [],
      thinkHinted: false,
      panel: panelOf(st.panel),
      lastAction: action,
    };
    const body =
      st.type === "show"
        ? showCopy(copy, st.id).say
        : st.type === "think"
          ? thinkCopy(copy, st.id).ask
          : choiceCopy(copy, st.id).ask;
    s = { ...s, message: `${lead}${body}`.trim(), buttons: buttonsFor(st), shownAt: d.now() };
    log({ kind: "start" }, action);
  }

  function next(lead = "") {
    s = { ...s, pi: s.pi + 1 };
    open(lead);
  }

  function finish(lead: string) {
    s = {
      ...s,
      stage: "done",
      si: lesson.sentences.length - 1,
      pi: 0,
      message: `${lead}${copy.closing}`.trim(),
      buttons: [],
      panel: null,
      lastAction: { action: "FINISH" },
    };
    flush();
  }

  /* ── choice ─────────────────────────────────────────────────────── */

  function settle(st: ChoiceStep, status: PerformanceStatus) {
    if (st.skill) {
      s = { ...s, student: recordPerformance(s.student, st.skill, status, s.wrongPicks.length) };
    }
    s = {
      ...s,
      anyAssisted: s.anyAssisted || status !== "independent_success",
      anyExplained: s.anyExplained || status === "explained",
      struggledInSentence: s.struggledInSentence || status !== "independent_success",
    };
  }

  function onChoice(st: ChoiceStep, text: string) {
    if (s.resolved) return next();

    const lines = choiceCopy(copy, st.id);
    const latencyMs = d.now() - s.shownAt;
    const picked = pickOption(st, text);
    let observation: Extract<Observation, { kind: "answer" | "dont_know" }>;
    if (picked) {
      observation = { kind: "answer", correct: !!picked.correct, optionId: picked.id, latencyMs };
    } else if (isUnknownInput(text)) {
      observation = { kind: "dont_know", latencyMs };
    } else {
      // 보기 밖의 말 — 시도로 세지 않는다. 사다리도 그대로 둔다
      s = { ...s, message: `${L.pick_from_buttons} ${lines.reask ?? ""}`.trim() };
      return;
    }

    const action = decideOnChoice(st, { rung: s.rung, wrongPicks: s.wrongPicks }, observation, input());
    s = { ...s, lastAction: action };

    if (action.action === "PRAISE") {
      const assisted = s.rung > 0 || s.wrongPicks.length > 0;
      const status = assisted ? "hint_assisted_success" : "independent_success";
      log(observation, action, status);
      // 틀렸다가 스스로 고친 턴만 반짝인다
      const light = s.wrongPicks.length > 0;
      settle(st, status);
      if (st.praise_alone) {
        // 칭찬(+뜻 되짚기)만 한 말풍선. 「다음으로」가 오면 `resolved`라 다음 스텝으로 간다
        s = {
          ...s,
          resolved: true,
          message: lines.praise,
          panel: panelOf(st.panel_after) ?? s.panel,
          effect: light ? "light" : null,
        };
        s = { ...s, buttons: buttonsFor(st), shownAt: d.now() };
        return;
      }
      next(`${lines.praise} `);
      s = { ...s, effect: light ? "light" : null };
      return;
    }

    if (observation.kind === "answer") {
      s = { ...s, wrongPicks: [...s.wrongPicks, observation.optionId] };
    }

    if (action.action === "EXPLAIN") {
      log(observation, action, "explained");
      settle(st, "explained");
      s = {
        ...s,
        resolved: true,
        rung: s.rung + 1,
        message: `${L.explain_lead} ${lines.explain}`,
        panel: panelOf(st.panel_after) ?? s.panel,
      };
      s = { ...s, buttons: buttonsFor(st), shownAt: d.now() };
      return;
    }

    log(observation, action);
    let body: string;
    if (action.action === "GIVE_SELF_CORRECTION_OPPORTUNITY") {
      body = L.self_correct;
    } else if (action.action === "GIVE_LIGHT_HINT") {
      const lead = observation.kind === "answer" ? L.wrong_lead : L.dont_know_lead;
      // 고른 오답이 예상 오개념이면 그걸 겨냥한 말이 먼저다
      body = `${lead} ${(picked && lines.feedback?.[picked.id]) ?? lines.hints[0]}`;
    } else {
      const lead = observation.kind === "answer" ? L.wrong_lead : L.dont_know_lead;
      body = `${lead} ${lines.hints[1]}`;
    }
    s = { ...s, rung: s.rung + 1, struggledInSentence: true, message: body };
    s = { ...s, buttons: buttonsFor(st), shownAt: d.now() };
  }

  function pickOption(st: ChoiceStep, text: string) {
    const open = st.options.filter((o) => !s.wrongPicks.includes(o.id));
    const exact = open.find((o) => o.label === text);
    if (exact) return exact;
    const n = text.trim().match(/^([1-9])\s*번?$/)?.[1];
    if (n) return open[Number(n) - 1] ?? null;
    const label = matchChoice(text, open.map((o) => o.label));
    return open.find((o) => o.label === label) ?? null;
  }

  /* ── think ──────────────────────────────────────────────────────── */

  function onThink(st: Extract<PolicyStep, { type: "think" }>, text: string) {
    if (s.resolved) return next();
    const lines = thinkCopy(copy, st.id);
    const latencyMs = d.now() - s.shownAt;

    if (text !== THOUGHT_BTN && isUnknownInput(text) && !s.thinkHinted) {
      const action: TeachingAction = { action: "GIVE_LIGHT_HINT", interactionId: st.id, intensity: "minimal" };
      log({ kind: "dont_know", latencyMs }, action);
      s = { ...s, thinkHinted: true, struggledInSentence: true, lastAction: action, message: lines.hint };
      s = { ...s, buttons: buttonsFor(st), shownAt: d.now() };
      return;
    }

    // 채점하지 않는다 — 생각했다는 것만 관찰이고, 맞았는지는 모른다 (§7)
    const action: TeachingAction = { action: "SUMMARIZE", interactionId: st.id, intensity: "brief" };
    log({ kind: "thought", latencyMs }, action);
    s = {
      ...s,
      resolved: true,
      lastAction: action,
      message: lines.summary,
      panel: panelOf(st.panel_after) ?? s.panel,
    };
    s = { ...s, buttons: buttonsFor(st), shownAt: d.now() };
  }

  /* ── 곁길: 도움말 · 단어 뜻 ─────────────────────────────────────── */

  /** 턴을 쓰지 않는 곁길이면 true. 사다리·시도 횟수를 건드리지 않는다 */
  function sideTrack(text: string): boolean {
    const st = step();
    const reask =
      st.type !== "show" && !s.resolved ? ` ${copy.steps[st.id]?.reask ?? ""}` : "";

    const help = sentence().helps?.find((h) => h.label === text);
    if (help) {
      // 눌렀다는 것만 남긴다. 「모른다」로 바꿔 적지 않는다 (§20)
      log({ kind: "help_click", helpId: help.id }, { action: "ALLOW_LOOKUP", target: help.id, intensity: "minimal" });
      const aside = s.aside ?? {
        message: st.type !== "show" && !s.resolved ? (copy.steps[st.id]?.reask ?? s.message) : s.message,
        buttons: s.buttons,
      };
      s = { ...s, aside, message: copy.helps[help.id]?.answer ?? "", buttons: [BACK_BTN] };
      return true;
    }

    const word = askedAboutWord(text, sentence().text);
    if (word) {
      const gloss = lookupGloss(word, sentence().glosses);
      log({ kind: "vocab_click", word }, { action: "ALLOW_LOOKUP", target: word });
      const answer = gloss
        ? L.word_answer.replace("{word}", gloss.en).replace("{ko}", gloss.ko)
        : L.word_unknown;
      s = { ...s, message: `${answer}${reask}`.trim() };
      return true;
    }
    return false;
  }

  /* ── 화면 ───────────────────────────────────────────────────────── */

  function result(): TutorResult {
    if (s.anyExplained) return "설명제공";
    return s.anyAssisted ? "오류후이해" : "이해";
  }

  function view(): TutorView {
    const reading = s.stage === "read";
    const exam = s.stage === "exam_first" || s.stage === "exam_final";
    const sen = sentence();
    const st = step();
    const inLesson = s.stage === "lesson";
    const onStudy = inLesson || exam;
    const shown = inLesson ? (st.display ?? sen.text) : sen.text;
    // 밑줄 친 구절은 읽을 때도, 문제를 풀 때도 노랗게
    const underline = lesson.exam && shown.includes(lesson.exam.underline) ? [lesson.exam.underline] : [];
    // 한 줄에 못 들어가는 보기가 있으면 세로로 쌓는다
    const stack = s.buttons.some((b) => b.length > 18);
    return {
      screen: reading ? "read" : onStudy ? "study" : "chat",
      message: s.message,
      buttons: s.buttons,
      placeholder: "선생님께 답해 보세요…",
      studentLine: s.studentLine,
      effect: s.effect,
      sentence: shown,
      activeChunk: shown,
      chunkLabel: `${s.si + 1}문장`,
      progressIndex: s.si + 1,
      progressTotal: lesson.sentences.length,
      progressLabel: exam ? "문제 풀기" : undefined,
      passage: reading
        ? {
            heading: lesson.source,
            title: lesson.exam?.question ?? copy.topic_intro,
            sentences: lesson.sentences.map((x) => x.text),
            revealed: s.ri + 1,
            current: s.ri,
            underline: lesson.exam?.underline ?? null,
          }
        : undefined,
      ended: s.stage === "done",
      recordLine:
        s.stage === "done"
          ? `[기록] 유형=teaching-policy / 결과=${result()} / 오류=없음`
          : null,
      properNouns: !inLesson
        ? s.stage === "intro"
          ? (lesson.proper_nouns ?? [])
          : []
        : (lesson.proper_nouns ?? []).filter((n) => shown.includes(n.en)),
      glosses: onStudy ? sen.glosses : [],
      highlight: inLesson ? (st.highlight ?? []) : underline,
      emphasis: inLesson ? (sen.emphasis ?? []) : [],
      panel: inLesson ? s.panel : null,
      // 도움말 칩은 문장의 첫 스텝에서만. 수업이 진행되면 화면에 이미 많다
      helps: inLesson && s.pi === 0 ? (sen.helps ?? []).map((h) => h.label) : [],
      buttonLayout: stack ? "stack" : "row",
      auxButtons: [UNKNOWN_BTN, HINT_BTN, SKIP_BTN],
      numbered: (inLesson && st.type === "choice" && !s.resolved && !s.aside) || (exam && s.buttons.length > 1),
    };
  }

  return {
    view,
    async submit(raw: string): Promise<TutorView> {
      const text = raw.trim();
      if (!text || s.stage === "done") return view();
      s = { ...s, studentLine: text, effect: null };

      if (s.stage === "intro") {
        startReading();
        return view();
      }
      if (s.stage === "read") {
        // 「계속」이면 다 읽지 않았어도 넘어간다. 화면이 보내는 신호면 한 문장 더
        if (text === READ_NEXT_CMD) readNext();
        else askMode();
        return view();
      }
      if (s.stage === "mode") {
        if (text === MODE_TRY_BTN) askExam("first");
        else if (text === MODE_ANALYZE_BTN) startLesson();
        else s = { ...s, message: `${L.pick_from_buttons} ${L.choose_mode}` };
        return view();
      }
      if (s.stage === "exam_first" && s.firstAnswer) {
        startLesson();
        return view();
      }
      if (s.stage === "exam_first" || s.stage === "exam_final") {
        onExam(text);
        return view();
      }

      // 도움말에서 돌아온다. 「이어서 할게요」가 아닌 말이면 돌아온 뒤 그 말을 처리한다
      if (s.aside) {
        const { message, buttons } = s.aside;
        s = { ...s, aside: null, message, buttons, shownAt: d.now() };
        if (text === BACK_BTN) return view();
      }

      if (sideTrack(text)) return view();

      const st = step();
      // 「이미 알고 있어요」 — 학생의 말을 믿고 넘어간다. 맞혔다고 적지는 않는다
      if (st.skippable && text === SKIP_BTN && !s.resolved) {
        log({ kind: "skip" }, { action: "CONTINUE", interactionId: st.id, reason: ["student_claims_known"] });
        s = { ...s, skipped: [...s.skipped, st.id] };
        next();
        return view();
      }
      if (st.type === "choice") onChoice(st, text);
      else if (st.type === "think") onThink(st, text);
      else {
        log({ kind: "continue" }, { action: "CONTINUE", interactionId: st.id });
        next();
      }
      return view();
    },
    /** 단어를 눌러 본 것 — 턴이 아니라 관찰이다 (§7 vocabulary_clicks) */
    observe(o: UiObservation) {
      if (s.stage !== "lesson") return;
      log(o, { action: "ALLOW_LOOKUP", target: o.word });
    },
    /** 예전 엔진의 항목 기록은 이 레슨에 없다. 학습 이벤트는 기기에 따로 쌓는다 */
    records: (): PointRecord[] => [],
    lessonId: () => lesson.id,
    learnerName: () => s.learnerName,
    lastAction: () => s.lastAction,
    reset() {
      pending = [];
      baseline = d.loadStudent();
      s = initial(s.learnerName);
      return view();
    },
  };
}

export type PolicySession = ReturnType<typeof createPolicySession>;
