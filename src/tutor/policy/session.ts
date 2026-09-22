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
  stage: "intro" | "lesson" | "done";
  si: number;
  pi: number;
  /** choice: 풀이 중 → 끝남(설명을 봤다). think: 생각 중 → 정리를 봤다 */
  resolved: boolean;
  rung: number;
  wrongPicks: string[];
  thinkHinted: boolean;
  /** 이 문장의 질문에서 틀렸거나 도움을 받았나 */
  struggledInSentence: boolean;
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
      si: 0,
      pi: 0,
      resolved: false,
      rung: 0,
      wrongPicks: [],
      thinkHinted: false,
      struggledInSentence: false,
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
    return [
      hello,
      L.intro_topic.replace("{topic}", copy.topic_intro),
      frame.fixed_lines.ready_question,
    ].join(" ");
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
    return [...left, UNKNOWN_BTN];
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
      if (s.si >= lesson.sentences.length) return finish(lead);
      if (s.pi >= sentence().steps.length) {
        s = { ...s, si: s.si + 1, pi: 0, struggledInSentence: false };
        flush();
        continue;
      }
      if (shouldShow(step(), input(), s.struggledInSentence)) break;
      log({ kind: "continue" }, { action: "CONTINUE", interactionId: step().id, reason: ["skipped_by_policy"] });
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
    const sen = sentence();
    const st = step();
    const inLesson = s.stage === "lesson";
    const shown = inLesson ? (st.display ?? sen.text) : sen.text;
    // 한 줄에 못 들어가는 보기가 있으면 세로로 쌓는다
    const stack = s.buttons.some((b) => b.length > 18);
    return {
      screen: inLesson ? "study" : "chat",
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
      glosses: inLesson ? sen.glosses : [],
      highlight: inLesson ? (st.highlight ?? []) : [],
      emphasis: inLesson ? (sen.emphasis ?? []) : [],
      panel: inLesson ? s.panel : null,
      helps: inLesson ? (sen.helps ?? []).map((h) => h.label) : [],
      buttonLayout: stack ? "stack" : "row",
      auxButtons: [UNKNOWN_BTN, HINT_BTN],
    };
  }

  return {
    view,
    async submit(raw: string): Promise<TutorView> {
      const text = raw.trim();
      if (!text || s.stage === "done") return view();
      s = { ...s, studentLine: text, effect: null };

      if (s.stage === "intro") {
        s = { ...s, stage: "lesson", si: 0, pi: 0 };
        open(L.start_known);
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
