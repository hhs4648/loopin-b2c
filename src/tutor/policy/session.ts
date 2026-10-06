import policyFrame from "../../../content/tutor/policy-frame.json";
import type { TutorResult } from "../../../content/tutor/types";
import { UNKNOWN_BTN, HINT_BTN, type PointRecord, type TutorView } from "../view";
import { lookupGloss } from "../glosses";
import { isUnknownInput, matchChoice } from "../match";
import { askedAboutWord } from "../proper-nouns";
import { addVocab } from "../vocab";
import { bumpMethodIntro, methodIntroCount, saveReview, type ReviewStatus } from "./review";
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
  ExamQuestion,
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

/** 밑줄 친 구절들 — 밑줄 의미 문제는 하나, 어휘 문제는 여러 개 */
export function underlinesOf(exam: ExamQuestion): string[] {
  return Array.isArray(exam.underline) ? exam.underline : [exam.underline];
}

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
const INTRO_NEXT_BTN = policyFrame.buttons.intro_next;
/** 읽기 화면이 한 문장을 다 읽었을 때 보내는 신호. 학생의 말이 아니다 */
export const READ_NEXT_CMD = "__read_next";
/* 마무리 화면이 보내는 신호 — 학생의 말이 아니라 화면 조작이다 */
export const WEEKS_CMD = "__weeks:";
export const SAVE_CMD = "__save";
export const CHECK_CMD = "__check:";
export const MATCH_DONE_CMD = "__match_done";
export const PREV_SENTENCE_CMD = "__prev_sentence";
export const NEXT_SENTENCE_CMD = "__next_sentence";
const MODE_TRY_BTN = policyFrame.buttons.mode_try;
const MODE_ANALYZE_BTN = policyFrame.buttons.mode_analyze;
const ANALYZE_START_BTN = policyFrame.buttons.analyze_start;
const SOLVE_BTN = policyFrame.buttons.solve;
const POINTS_DONE_BTN = policyFrame.buttons.points_done;
const PASSAGE_AGAIN_BTN = policyFrame.buttons.passage_again;

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
  stage:
    | "intro"
    | "read"
    | "mode"
    | "exam_first"
    | "lesson"
    | "exam_final"
  | "points"
    | "review"
    | "words"
    | "match"
    | "done";
  /** 「자세히 볼래요」를 누른 스텝 — `optional_of`가 이것인 스텝만 연다 */
  detailOpen: string | null;
  /** 마지막 시험 문제에서 틀리고 지운 보기 */
  finalWrong: string[];
  reviewWeeks: number | null;
  reviewSaved: boolean;
  reviewStatus: ReviewStatus | null;
  /** 단어 체크 — 0 본문 단어, 1 보기 단어 */
  wordPart: number;
  checked: string[];
  /** 도입 단계에서 지금 보고 있는 스텝 */
  ii: number;
  /** 도입 ask에 답한 뒤, 「다음」을 누르면 갈 곳 (답을 보여 주는 중) */
  introReplied: boolean;
  boardImage: string | null;
  /** 읽기 단계에서 보고 있는 문장 */
  ri: number;
  /** 처음에 풀어 봤다면 그 결과 */
  firstAnswer: { optionId: string; correct: boolean } | null;
  /** 헷갈린 질문 — 수업 끝 「헷갈린 포인트」에 모은다 (같은 키는 한 번) */
  points: { key: string; title: string; text: string }[];
  /** 마지막 문제에서 정답을 골라 해설(`answer_explain`)을 보는 중 — 「다음으로」면 다시 볼 주기로 */
  examSolved: boolean;
  /** 많이 고른 오답을 같이 자세히 보는 중 — 보기 id와 몇 번째 화면인지 (0 제안 · 1 설명 · 2 질문 · 3 답) */
  examReview: { optionId: string; step: number } | null;
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
  /* 이 유형의 풀이법 설명을 몇 번 봤나 — `intro_times`번까지는 도입에서 설명한다 */
  const methodSeen = lesson.method ? methodIntroCount(lesson.method.type) : 0;
  const methodFresh = !lesson.method || methodSeen < lesson.method.intro_times;
  let methodBumped = false;
  const readButton = lesson.read_button ?? READ_DONE_BTN;
  const ending = copy.ending ?? {};

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
      detailOpen: null,
      finalWrong: [],
      reviewWeeks: null,
      reviewSaved: false,
      reviewStatus: null,
      wordPart: 0,
      checked: [],
      ii: 0,
      introReplied: false,
      boardImage: null,
      ri: 0,
      firstAnswer: null,
      examSolved: false,
      examReview: null,
      points: [],
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
      message: "",
      buttons: [],
      studentLine: "",
      effect: null,
      panel: null,
      aside: null,
      shownAt: d.now(),
      lastAction: null,
    };
    return showIntro(base, 0, "");
  }

  /* ── 도입 ───────────────────────────────────────────────────────── */

  /** 도입 스텝 i를 연다. 도입이 없거나 끝났으면 읽기로. `lead`는 앞 답을 이어 붙일 때 */
  function showIntro(st0: State, i: number, lead: string): State {
    const step = lesson.intro?.[i];
    // 도입이 없거나 끝났으면 읽기로 (초기화 중에도 불리므로 `s`를 건드리지 않는다)
    if (!step) {
      if (lesson.method && !methodBumped) {
        methodBumped = true;
        bumpMethodIntro(lesson.method.type);
      }
      // 한 문장씩 읽기를 뺀 레슨은 여기서 「바로 풀기 / 분석」을 고른다
      if (lesson.passage_on_try) {
        return { ...st0, stage: "mode", message: "", buttons: [MODE_TRY_BTN, readButton], panel: null };
      }
      return { ...st0, stage: "read", ri: 0, message: L.read_intro, buttons: [readButton], panel: null };
    }
    // 풀이법 설명은 처음 몇 번만, 그 뒤엔 짧은 시작 화면만
    if (step.type === "say" && step.show_when === (methodFresh ? "later" : "first")) {
      return showIntro(st0, i + 1, lead);
    }
    const lines = copy.intro?.[step.id] ?? {};
    let text: string;
    if (step.id === "rate") {
      const ex = lesson.exam;
      const rate =
        ex?.wrong_rate == null
          ? ""
          : (ex.wrong_rank != null ? L.intro_rate : L.intro_rate_only)
              .replace("{rate}", String(ex.wrong_rate))
              .replace("{rank}", String(ex.wrong_rank ?? ""));
      // 인사 없이 바로 문제 소개로 연다
      text = [rate, lines.ask ?? ""].filter(Boolean).join(" ");
    } else {
      text = step.type === "say" ? (lines.say ?? "") : (lines.ask ?? "");
    }
    const buttons =
      step.type === "ask" ? step.options.map((o) => o.label) : [step.button ?? INTRO_NEXT_BTN];
    return { ...st0, stage: "intro", ii: i, introReplied: false, message: `${lead}${text}`.trim(), buttons };
  }

  function onIntro(text: string) {
    const step = lesson.intro?.[s.ii];
    if (!step) return startReading();
    // 답을 보여 주던 중이면 「다음」으로 다음 스텝
    if (step.type === "say" || s.introReplied) {
      s = showIntro({ ...s, boardImage: null }, s.ii + 1, "");
      return;
    }
    const picked = step.options.find((o) => o.label === text) ??
      step.options.find((o) => o.label === matchChoice(text, step.options.map((x) => x.label)));
    if (!picked) {
      s = { ...s, message: `${L.pick_from_buttons} ${copy.intro?.[step.id]?.ask ?? ""}`.trim() };
      return;
    }
    pending.push({
      at: new Date(d.now()).toISOString(),
      lessonId: lesson.id,
      sentenceId: 0,
      stepId: `intro_${step.id}`,
      observation: { kind: "intro", optionId: picked.id },
      action: { action: "CONTINUE" },
    });
    const reply = step.replies[picked.id];
    const line = reply ? (copy.intro?.[step.id]?.[reply.line] ?? "") : "";
    if (!reply || reply.inline) {
      s = showIntro({ ...s, boardImage: null }, s.ii + 1, line ? `${line} ` : "");
      return;
    }
    s = {
      ...s,
      introReplied: true,
      message: line,
      buttons: [INTRO_NEXT_BTN],
      boardImage: reply.image ?? null,
    };
  }

  /* ── 지문 읽기 · 문제 풀기 ──────────────────────────────────────── */

  function startReading() {
    s = { ...s, stage: "read", ri: 0, message: L.read_intro, buttons: [readButton], panel: null };
  }

  /** 읽기 화면이 한 문장을 다 읽었다 — 다음 문장을 드러낸다. 마지막이면 그대로 둔다 */
  function readNext() {
    const last = lesson.sentences.length - 1;
    if (s.ri < last) s = { ...s, ri: s.ri + 1 };
  }

  /** 다 읽었으면: 시험 문제가 있으면 어떻게 할지 고르게, 없으면 바로 분석 */
  function askMode() {
    if (!lesson.exam || lesson.exam.analysis_first) return startLesson();
    s = { ...s, stage: "mode", message: L.choose_mode, buttons: [MODE_TRY_BTN, MODE_ANALYZE_BTN] };
  }

  function startLesson() {
    s = { ...s, stage: "lesson", si: 0, pi: 0 };
    open(L.start_known);
  }

  /** 밑줄 친 구절이 든 문장 — 문제 화면에 띄운다 */
  function examSentence(): PolicySentence {
    const ex = lesson.exam!;
    const [u] = underlinesOf(ex);
    return (
      lesson.sentences.find((x) => (ex.sentence != null ? x.id === ex.sentence : x.text.includes(u!))) ??
      lesson.sentences[lesson.sentences.length - 1]!
    );
  }

  function askExam(when: "first" | "final") {
    const ex = copy.exam!;
    s = {
      ...s,
      stage: when === "first" ? "exam_first" : "exam_final",
      si: lesson.sentences.indexOf(examSentence()),
      message:
        when === "first" && lesson.passage_on_try
          ? (ex.ask_first ?? ex.ask)
          : `${when === "final" && !lesson.exam!.analysis_first ? L.final_lead : ""}${ex.ask}`,
      // 분석 먼저인 문제는 보기를 카드로 그린다 (핵심 단어 색칠, ▸ 한국어) — 버튼은 없다.
      // 바로 풀기에서는 실제 시험처럼 색칠·한국어 없이, 지문으로 돌아가는 버튼만
      buttons: lesson.exam!.analysis_first
        ? when === "first" && lesson.passage_on_try
          ? [PASSAGE_AGAIN_BTN]
          : []
        : lesson.exam!.options.map((o) => o.label),
      finalWrong: [],
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
    if (when === "first" && lesson.passage_on_try) {
      // 분석 없이 맞혔다 — 이 문제는 소화했다. 틀렸으면 답을 말하지 않고 분석으로
      if (correct) {
        s = {
          ...s,
          firstAnswer: { optionId: picked.id, correct },
          stage: "review",
          reviewStatus: "mastered",
          reviewWeeks: null,
          buttons: [NEXT_BTN],
        };
        s = { ...s, message: ending.mastered ?? ex.first_correct };
        return;
      }
      s = {
        ...s,
        firstAnswer: { optionId: picked.id, correct },
        message: ex.first_wrong,
        buttons: [readButton],
      };
      return;
    }
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
    if (exam.analysis_first) {
      // 틀리면 그 보기를 지우고 다시 고르게 한다. 맞히면 마무리(복습 주기 · 단어)로
      if (!correct) {
        const review = ex.option_review?.[picked.id];
        s = {
          ...s,
          finalWrong: [...s.finalWrong, picked.id],
          anyExplained: true,
          message: `${L.wrong_lead} ${ex.option_feedback?.[picked.id] ?? ""}`.trim(),
        };
        addPoint(
          `exam_${picked.id}`,
          `문제 ${"①②③④⑤"[Number(picked.id) - 1] ?? picked.id}`,
          ex.option_points?.[picked.id] ?? ex.option_feedback?.[picked.id] ?? "",
        );
        if (review) {
          // 많이 고른 오답 — 그 밑줄이 든 문장으로 가서 같이 자세히 본다
          const u = underlinesOf(exam)[exam.options.findIndex((o) => o.id === picked.id)];
          const at = u ? lesson.sentences.findIndex((x) => x.text.includes(u)) : -1;
          s = {
            ...s,
            examReview: { optionId: picked.id, step: 0 },
            si: at >= 0 ? at : s.si,
            message: review.intro,
            buttons: [review.intro_button],
          };
        }
        return;
      }
      if (ex.answer_explain) {
        s = { ...s, examSolved: true, message: ex.answer_explain, buttons: [NEXT_BTN] };
        return;
      }
      startReview();
      return;
    }
    s = { ...s, anyExplained: s.anyExplained || !correct, effect: correct && s.firstAnswer && !s.firstAnswer.correct ? "light" : null };
    finish(`${correct ? ex.final_correct : ex.final_wrong} `);
  }

  /** 많이 고른 오답을 같이 자세히 본다 — 제안 → 그림·설명 → 어디서 헷갈렸나 → 답 → 문제로 */
  function onExamReview(text: string) {
    const r = s.examReview!;
    const review = copy.exam!.option_review![r.optionId]!;
    if (r.step === 0) {
      s = { ...s, examReview: { ...r, step: 1 }, message: review.say, panel: review.panel ?? null, buttons: [NEXT_BTN] };
      return;
    }
    if (r.step === 1) {
      s = { ...s, examReview: { ...r, step: 2 }, message: review.ask, buttons: review.choices.map((c) => c.label) };
      return;
    }
    if (r.step === 2) {
      const pick = review.choices.find((c) => c.label === text);
      if (!pick) return;
      // 헷갈린 곳을 기록한다 — 다음 수업에서 비슷한 문장이 나오면 이 skill을 보고 강조한다
      let student = s.student;
      for (const skill of pick.skills) student = recordPerformance(student, skill, "explained", 1);
      s = { ...s, student };
      log({ kind: "wrong_reason", optionId: r.optionId, reason: pick.label, skills: pick.skills }, { action: "SUMMARIZE", reason: ["wrong_reason"] });
      flush();
      s = { ...s, examReview: { ...r, step: 3 }, message: pick.reply, buttons: [NEXT_BTN] };
      return;
    }
    // 문제로 돌아온다 — 고른 보기는 지워진 채로
    s = {
      ...s,
      examReview: null,
      si: lesson.sentences.indexOf(examSentence()),
      panel: null,
      message: L.review_back,
      buttons: [],
    };
  }

  /* ── 마무리: 다시 볼 주기 · 단어 체크 · 짝 맞추기 ───────────────── */

  /** 분석 뒤 마지막 문제를 맞혔다 — 다시 볼 주기로. 한 번이라도 틀렸으면 1주, 아니면 3주 */
  function startReview() {
    const missed = s.finalWrong.length > 0;
    s = {
      ...s,
      stage: "review",
      examSolved: false,
      reviewStatus: missed ? "analyzed_wrong" : "analyzed_correct",
      reviewWeeks: missed ? 1 : 3,
      buttons: [NEXT_BTN],
      effect: missed ? "light" : null,
    };
    s = { ...s, message: reviewMessage() };
  }

  function weeksLabel(w: number | null) {
    return w == null ? "다시 안 봄" : `${w}주`;
  }

  function reviewMessage(): string {
    if (s.reviewStatus === "mastered") {
      return s.reviewWeeks == null
        ? (ending.mastered ?? "")
        : (ending.mastered_later ?? "").replace("{weeks}", weeksLabel(s.reviewWeeks));
    }
    if (s.reviewWeeks == null) return ending.never ?? "";
    const base = s.finalWrong.length ? ending.wrong : ending.correct;
    return (base ?? "").replace("{weeks}", weeksLabel(s.reviewWeeks));
  }

  const keyWords = () => lesson.key_words ?? { passage: [], options: [] };

  function startWords(part: number) {
    const title = part === 0 ? ending.words_passage : ending.words_options;
    s = {
      ...s,
      stage: "words",
      wordPart: part,
      message: title ?? "",
      buttons: [part === 0 && keyWords().options.length ? NEXT_BTN : (ending.words_done ?? NEXT_BTN)],
    };
  }

  /** 짝 맞추기 — 체크한 단어 먼저, 모자라면 본문 단어로 채워 8개까지 */
  function matchPairs() {
    const all = [...keyWords().passage, ...keyWords().options];
    const picked = all.filter((w) => s.checked.includes(w.en));
    for (const w of keyWords().passage) {
      if (picked.length >= 8) break;
      if (!picked.includes(w)) picked.push(w);
    }
    return picked.slice(0, 8);
  }

  function onEnding(text: string) {
    if (s.stage === "review") {
      if (text.startsWith(WEEKS_CMD)) {
        const v = text.slice(WEEKS_CMD.length);
        s = { ...s, reviewWeeks: v === "none" ? null : Number(v) };
        s = { ...s, message: reviewMessage() };
        return;
      }
      if (text === SAVE_CMD) {
        s = { ...s, reviewSaved: !s.reviewSaved };
        return;
      }
      saveReview(lesson.id, {
        status: s.reviewStatus ?? "analyzed_correct",
        weeks: s.reviewWeeks,
        saved: s.reviewSaved,
      });
      if (lesson.key_words) return startWords(0);
      return toPoints();
    }
    if (s.stage === "words") {
      if (text.startsWith(CHECK_CMD)) {
        const en = text.slice(CHECK_CMD.length);
        s = { ...s, checked: s.checked.includes(en) ? s.checked.filter((x) => x !== en) : [...s.checked, en] };
        return;
      }
      if (s.wordPart === 0 && keyWords().options.length) return startWords(1);
      // 체크한 단어는 단어장으로 — 어느 지문에서 나왔는지 같이
      const all = [...keyWords().passage, ...keyWords().options];
      addVocab(
        all
          .filter((w) => s.checked.includes(w.en))
          .map((w) => ({ en: w.en, ko: w.ko, sentence: "", source: lesson.id })),
      );
      s = { ...s, stage: "match", message: ending.match_title ?? "", buttons: [] };
      return;
    }
    if (s.stage === "match" && text === MATCH_DONE_CMD) return toPoints();
    if (s.stage === "points" && text === POINTS_DONE_BTN) finish("");
  }

  /** 헷갈린 곳이 있으면 정리 화면, 없으면 끝 */
  function toPoints() {
    if (!s.points.length) return finish("");
    s = { ...s, stage: "points", message: L.points_title, buttons: [POINTS_DONE_BTN] };
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
    return st.detail_button ? [st.button ?? NEXT_BTN, st.detail_button] : [st.button ?? NEXT_BTN];
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
      // 「자세히 볼래요」를 안 누른 학생에게는 그 뒤의 자세한 스텝을 보여 주지 않는다
      if (step().optional_of && s.detailOpen !== step().optional_of) {
        s = { ...s, pi: s.pi + 1 };
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
      message: `${lead}${ending.closing ?? copy.closing}`.trim(),
      buttons: [],
      panel: null,
      lastAction: { action: "FINISH" },
    };
    flush();
  }

  /* ── choice ─────────────────────────────────────────────────────── */

  /** 수업 끝 「헷갈린 포인트」에 하나 더한다 — 같은 키면 한 번만 */
  function addPoint(key: string, title: string, text: string) {
    if (!text || s.points.some((p) => p.key === key)) return;
    s = { ...s, points: [...s.points, { key, title, text }] };
  }

  function settle(st: ChoiceStep, status: PerformanceStatus) {
    if (status !== "independent_success") {
      const c = copy.steps[st.id];
      addPoint(st.id, `${sentence().id}문장`, c?.point ?? c?.explain ?? "");
    }
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

    /*
      한 번만 고르는 질문 — 틀리면 "아쉽게도 틀렸어요." + 이유를 말하고 넘어간다.
      학생이 틀렸다는 걸 분명히 알게 하되, 같은 질문에 붙잡아 두지 않는다.
    */
    if (st.one_try && !(observation.kind === "answer" && observation.correct)) {
      if (picked) s = { ...s, wrongPicks: [...s.wrongPicks, picked.id] };
      const why = (picked && lines.feedback?.[picked.id]) ?? lines.hints[0];
      log(observation, { action: "EXPLAIN", interactionId: st.id, intensity: "brief" }, "explained");
      settle(st, "explained");
      s = {
        ...s,
        resolved: true,
        message: `${picked ? L.wrong_lead : L.dont_know_lead} ${why}`,
        panel: panelOf(st.panel_after) ?? s.panel,
      };
      s = { ...s, buttons: [NEXT_BTN], shownAt: d.now() };
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
      // 돌아오면 원래 질문을 그대로 다시 보인다 — 질문이 무엇이었는지 잊지 않게
      const aside = s.aside ?? { message: s.message, buttons: s.buttons };
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
    // 처음 고르는 화면(문제·지문·보기)도 지문 화면을 쓴다
    const reading = s.stage === "read" || (s.stage === "mode" && !!lesson.passage_on_try);
    const exam = s.stage === "exam_first" || s.stage === "exam_final";
    const sen = sentence();
    const st = step();
    const inLesson = s.stage === "lesson";
    const onStudy = inLesson || exam;
    const shown = inLesson ? (st.display ?? sen.text) : sen.text;
    // 밑줄 친 구절은 읽을 때도, 문제를 풀 때도 노랗게
    const underline = lesson.exam ? underlinesOf(lesson.exam).filter((u) => shown.includes(u)) : [];
    /*
      예상 질문(「주어 찾기 헷갈려요」 등) — 학생의 말이라 보기 옆에 민트 버튼으로 둔다.
      문장의 첫 질문에서, 아직 답하기 전에만. 누르면 곁길로 답하고 「이어서 할게요」로 돌아온다
    */
    const helpButtons =
      inLesson && s.pi === 0 && st.type === "choice" && !s.resolved && !s.aside
        ? (sen.helps ?? []).map((h) => h.label)
        : [];
    // 한 줄에 못 들어가는 보기가 있으면 세로로 쌓는다
    const stack = s.buttons.some((b) => b.length > 18);
    return {
      screen: reading
        ? "read"
        : s.stage === "words"
          ? "words"
          : s.stage === "match"
            ? "match"
            : s.stage === "points"
              ? "points"
            : onStudy
              ? "study"
              : "chat",
      message: s.message,
      boardImage: (() => {
        const key =
          s.boardImage ??
          (s.stage === "intro" ? lesson.intro_board : s.stage === "done" ? lesson.closing_board : null);
        return key ? (lesson.images?.[key] ?? null) : null;
      })(),
      buttons: [...s.buttons, ...helpButtons],
      // 학생이 방금 고른 답은 화면에 다시 띄우지 않는다 — 다음 질문과 섞여 헷갈린다
      studentLine: "",
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
            underline: lesson.exam ? underlinesOf(lesson.exam) : [],
            auto: !lesson.passage_on_try,
            options: lesson.passage_on_try ? (lesson.exam?.options.map((o) => o.label) ?? null) : null,
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
      // ❓ 개념 구절도 한 덩어리로 잡히게 뜻 목록에 넣는다
      glosses: onStudy
        ? [
            ...sen.glosses,
            ...(sen.concepts ?? [])
              .filter((c) => !sen.glosses.some((g) => g.en.toLowerCase() === c.en.toLowerCase()))
              .map((c) => ({ en: c.en, ko: c.title.replace(/:\s*$/, "") })),
          ]
        : [],
      faded: inLesson ? (st.faded ?? []) : [],
      shaded: inLesson ? (st.shaded ?? []) : [],
      concepts: inLesson ? (sen.concepts ?? []) : [],
      tips: inLesson ? (st.tips ?? []) : [],
      methodSteps:
        lesson.method && (inLesson || s.stage === "exam_final")
          ? { labels: lesson.method.labels, active: exam ? lesson.method.labels.length - 1 : (st.method ?? null) }
          : null,
      examOptions:
        exam && lesson.exam?.analysis_first && !(s.stage === "exam_first" && s.firstAnswer) && !s.examSolved && !s.examReview
          ? lesson.exam.options
              .filter((o) => !s.finalWrong.includes(o.id))
              .map((o) =>
                // 바로 풀기는 실제 시험처럼 — 색칠도 한국어도 없이
                s.stage === "exam_first"
                  ? { id: o.id, label: o.label, keywords: [], ko: "" }
                  : { id: o.id, label: o.label, keywords: o.keywords ?? [], ko: o.ko ?? "" },
              )
          : null,
      examGlosses: lesson.exam?.glosses ?? [],
      examSentences: (() => {
        const ex = lesson.exam;
        const lines = ex ? underlinesOf(ex) : [];
        if (!exam || !ex || lines.length < 2) return null;
        // 보기 순서 = 밑줄 순서 (①~⑤)
        const out: Record<string, { sentence: string; underline: string; glosses: typeof sen.glosses }> = {};
        ex.options.forEach((o, i) => {
          const u = lines[i];
          const hit = u ? lesson.sentences.find((x) => x.text.includes(u)) : undefined;
          if (u && hit) out[o.id] = { sentence: hit.text, underline: u, glosses: hit.glosses };
        });
        return out;
      })(),
      // 이 수업은 버튼으로만 답한다 — 자유 응답이 없으니 입력창도 없다
      allowInput: false,
      placeholder: "선생님께 답해 보세요…",
      fullPassage:
        lesson.passage_on_try && (inLesson || exam)
          ? { sentences: lesson.sentences.map((x) => x.text), underline: lesson.exam ? underlinesOf(lesson.exam) : [] }
          : null,
      canPrevSentence: inLesson && s.si > 0,
      canNextSentence: inLesson,
      review:
        s.stage === "review"
          ? { weeks: s.reviewWeeks, saved: s.reviewSaved, choices: [1, 2, 3, 4, 5, null], caption: ending.save_caption ?? "" }
          : null,
      wordCheck:
        s.stage === "words"
          ? {
              title: s.message,
              step: `${s.wordPart === 0 ? "본문 단어" : "보기 단어"} ${s.wordPart + 1}/${keyWords().options.length ? 2 : 1}`,
              words: s.wordPart === 0 ? keyWords().passage : keyWords().options,
              checked: s.checked,
            }
          : null,
      matchPairs: s.stage === "match" ? matchPairs() : null,
      pointsReview: s.stage === "points" ? { title: s.message, lessonId: lesson.id, items: s.points } : null,
      highlight: inLesson ? (st.highlight ?? []) : underline,
      emphasis: inLesson ? (sen.emphasis ?? []) : [],
      panel: inLesson || s.examReview ? s.panel : null,
      buttonLayout: stack ? "stack" : "row",
      auxButtons: [
        UNKNOWN_BTN, HINT_BTN, SKIP_BTN, PASSAGE_AGAIN_BTN,
        ...(inLesson && st.detail_button ? [st.detail_button] : []),
        ...helpButtons,
      ],
      numbered: (inLesson && st.type === "choice" && !s.resolved && !s.aside) || (exam && s.buttons.length > 1),
    };
  }

  return {
    view,
    async submit(raw: string): Promise<TutorView> {
      const text = raw.trim();
      if (!text || s.stage === "done") return view();
      s = { ...s, studentLine: text.startsWith("__") ? s.studentLine : text, effect: null };

      if (s.stage === "intro") {
        onIntro(text);
        return view();
      }
      if (s.stage === "read") {
        // 바로 풀기: 지문 전체를 본 뒤 문제로 (답을 고른 적이 있으면 그 문제로 돌아간다)
        if (lesson.passage_on_try) {
          if (text !== READ_NEXT_CMD) askExam("first");
          return view();
        }
        // 「계속」이면 다 읽지 않았어도 넘어간다. 화면이 보내는 신호면 한 문장 더
        if (text === READ_NEXT_CMD) readNext();
        else askMode();
        return view();
      }
      if (s.stage === "mode" && lesson.passage_on_try) {
        // 처음에 문제·지문·보기를 한 번 다 보여 준 화면에서 고른다
        if (text === MODE_TRY_BTN) askExam("first");
        else if (text === readButton) startLesson();
        return view();
      }
      // 바로 풀다가 지문을 다시 본다 — 고른 답은 없으니 그대로 돌아오면 된다
      if (s.stage === "exam_first" && !s.firstAnswer && text === PASSAGE_AGAIN_BTN) {
        s = { ...s, stage: "read", message: "", buttons: [SOLVE_BTN] };
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
      if (s.stage === "exam_first" && text === PASSAGE_AGAIN_BTN) {
        s = { ...s, stage: "read", message: "", buttons: [SOLVE_BTN] };
        return view();
      }
      if (s.stage === "exam_final" && s.examReview) {
        onExamReview(text);
        return view();
      }
      if (s.stage === "exam_final" && s.examSolved) {
        // 정답 해설을 봤다 — 「다음으로」면 다시 볼 주기로
        if (text === NEXT_BTN) startReview();
        return view();
      }
      if (s.stage === "exam_first" || s.stage === "exam_final") {
        onExam(text);
        return view();
      }
      if (s.stage === "review" || s.stage === "words" || s.stage === "match" || s.stage === "points") {
        onEnding(text);
        return view();
      }

      // 위의 ‹ › — 이전 문장으로 돌아가거나, 이 문장을 넘기고 다음 문장으로
      if (s.stage === "lesson" && (text === PREV_SENTENCE_CMD || text === NEXT_SENTENCE_CMD)) {
        const to = s.si + (text === PREV_SENTENCE_CMD ? -1 : 1);
        if (to < 0) return view();
        log({ kind: "continue" }, { action: "CONTINUE", interactionId: step().id, reason: [text === PREV_SENTENCE_CMD ? "student_went_back" : "student_skipped_sentence"] });
        s = { ...s, si: to, pi: 0, detailOpen: null, aside: null, struggledInSentence: false, skipped: [] };
        open("");
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
      // 「자세히 볼래요」 — 이 스텝에 딸린 자세한 스텝들을 연다
      if (st.type === "show" && st.detail_button && text === st.detail_button) {
        log({ kind: "continue" }, { action: "CONTINUE", interactionId: st.id, reason: ["student_wants_detail"] });
        s = { ...s, detailOpen: st.id };
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
