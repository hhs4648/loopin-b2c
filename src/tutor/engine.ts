import lesson from "../../content/tutor/lessons/resignation-letter.json";
import type { Lesson, LessonChunk, ProperNoun, TutorResult } from "../../content/tutor/types";
import { classifyUnit, isUnknownInput, matchChoice } from "./match";
import {
  getTutorLlm,
  safeCall,
  validateLlmOutput,
  type UnitBrief,
} from "./llm";
import { PRAISE, UNIT_MATCH } from "./units";

export const UNKNOWN_BTN = "잘 모르겠어요";
export const HINT_BTN = "힌트 주세요";
export const READY_BTN = "네, 좋아요!";
export const READ_BTN = "다 읽었어요";

const data = lesson as unknown as Lesson;
const units = data.chunks;

export type UiScreen = "chat" | "study";

export type TutorView = {
  screen: UiScreen;
  message: string;
  buttons: string[];
  placeholder: string;
  studentLine: string;
  effect: null | "light";
  sentence: string;
  activeChunk: string;
  chunkLabel: string;
  progressIndex: number;
  progressTotal: number;
  ended: boolean;
  recordLine: string | null;
  properNouns: ProperNoun[];
};

type Branch = {
  errorId: string;
  choices: { id: string; label: string; correct?: boolean }[];
  on_choice: Record<
    string,
    { message: string; reveal_answer?: boolean; next?: string }
  >;
};

type EngineState = {
  stage: "intro" | "chunk" | "done";
  unitIndex: number;
  hintRung: 0 | 1 | 2 | 3;
  missCount: number;
  skipFinalRetake: boolean;
  hadAnyError: boolean;
  properNounTipTold: boolean;
  pending: Branch | null;
  errorIds: string[];
  result: TutorResult | null;
  /** 같은 말을 두 번 하지 않으려고 들고 있는다 (모델에 넘긴다) */
  lastTutorUtterance: string;
  studentLine: string;
  effect: null | "light";
  screen: UiScreen;
  message: string;
  buttons: string[];
  placeholder: string;
  ended: boolean;
};

function current(s: EngineState): LessonChunk {
  return units[s.unitIndex]!;
}

function errorOf(s: EngineState, id: string) {
  return current(s).expected_errors?.find((e) => e.id === id);
}

function hintOf(s: EngineState, rung: 1 | 2 | 3) {
  return current(s).hint_ladder?.find((h) => h.rung === rung)?.message;
}

function uniqueButtons(btns: string[]) {
  return [...new Set(btns.filter(Boolean))];
}

const INTRO =
  "오늘은 퇴사 인사 편지예요. Lewis Ltd.는 회사 이름이라 해석하지 말고 그대로 두면 돼요. 한 문장씩 해석해볼까요?";

function initialState(): EngineState {
  return {
    stage: "intro",
    unitIndex: 0,
    hintRung: 0,
    missCount: 0,
    skipFinalRetake: false,
    hadAnyError: false,
    properNounTipTold: true,
    pending: null,
    errorIds: [],
    result: null,
    lastTutorUtterance: INTRO,
    studentLine: "",
    effect: null,
    screen: "chat",
    message: INTRO,
    buttons: [READY_BTN, UNKNOWN_BTN],
    placeholder: "선생님께 답해 보세요…",
    ended: false,
  };
}

function nounsIn(text: string): ProperNoun[] {
  return (data.proper_nouns ?? []).filter((n) =>
    text.includes(n.en) || text.includes(n.en.replace(/\.$/, "")),
  );
}

function view(s: EngineState): TutorView {
  const u = current(s);
  return {
    screen: s.screen,
    message: s.message,
    buttons: s.buttons,
    placeholder: s.placeholder,
    studentLine: s.studentLine,
    effect: s.effect,
    sentence: u.text,
    activeChunk: u.text,
    chunkLabel: `${s.unitIndex + 1}문장`,
    progressIndex: s.unitIndex + 1,
    progressTotal: units.length,
    ended: s.ended,
    properNouns: s.stage === "intro" ? data.proper_nouns ?? [] : nounsIn(u.text),
    recordLine:
      s.ended && s.result
        ? `[기록] 유형=${data.grammar_type} / 결과=${s.result} / 오류=${s.errorIds.join(",") || "없음"}`
        : null,
  };
}

function say(
  s: EngineState,
  message: string,
  extra: Partial<EngineState> = {},
): EngineState {
  return { ...s, ...extra, message, lastTutorUtterance: message };
}

function startUnit(s: EngineState, index: number, lead: string): EngineState {
  return say(s, `${lead}이 문장을 해석해볼까요?`, {
    stage: "chunk",
    unitIndex: index,
    hintRung: 0,
    missCount: 0,
    pending: null,
    screen: "study",
    placeholder: "해석을 적어 보세요…",
    buttons: [READ_BTN, HINT_BTN, UNKNOWN_BTN],
    effect: null,
  });
}

function finish(s: EngineState, result: TutorResult, closing: string): EngineState {
  return say(s, closing, {
    stage: "done",
    result,
    ended: true,
    screen: "chat",
    buttons: [],
    placeholder: "",
    pending: null,
    effect: null,
  });
}

function advance(s: EngineState, praise: string, light: boolean): EngineState {
  const stepped = { ...s, effect: light ? ("light" as const) : null };
  if (s.unitIndex < units.length - 1) {
    return startUnit(stepped, s.unitIndex + 1, `${praise} 다음 문장이에요. `);
  }
  if (s.skipFinalRetake) {
    return finish(stepped, "설명제공", `${praise} 편지 끝까지 같이 봤어요. 오늘은 여기까지 해요.`);
  }
  if (!s.hadAnyError) {
    return finish(stepped, "이해", `${praise} 일곱 문장 모두 잘 따라왔어요. 오늘 정말 잘했어요.`);
  }
  return finish(
    stepped,
    "오류후이해",
    `${praise} 막히는 지점도 있었는데, 끝까지 왔어요. 오늘 수업은 여기까지예요.`,
  );
}

function openBranch(s: EngineState, errorId: "P2" | "P3"): EngineState {
  const t = errorOf(s, errorId)?.treatment;
  if (!t?.message) return climbHint(s);
  const choices = t.choices ?? [];
  return say(s, t.message, {
    hadAnyError: true,
    missCount: s.missCount + 1,
    errorIds: s.errorIds.includes(`${s.unitIndex + 1}:${errorId}`)
      ? s.errorIds
      : [...s.errorIds, `${s.unitIndex + 1}:${errorId}`],
    pending:
      t.on_choice && choices.length
        ? { errorId, choices, on_choice: t.on_choice }
        : null,
    screen: "study",
    buttons: uniqueButtons([...choices.map((c) => c.label), UNKNOWN_BTN]),
    placeholder: "선생님께 답해 보세요…",
    effect: null,
  });
}

function frustration(s: EngineState): EngineState {
  const u = current(s);
  const wrong = errorOf(s, "P3")?.treatment?.choices?.find((c) => !c.correct)?.label
    ?? errorOf(s, "P2")?.treatment?.choices?.find((c) => !c.correct)?.label
    ?? "잘 모르겠어요";
  const right = u.model_translation;
  return say(
    s,
    `오늘 문장이 좀 까다롭죠? 괜찮아요, 우리 그냥 같이 봐요. 정답은 '${right}'예요. 어느 쪽이 더 가깝나요?`,
    {
      skipFinalRetake: true,
      hadAnyError: true,
      result: "설명제공",
      pending: {
        errorId: "FRUSTRATION",
        choices: [
          { id: "wrong", label: wrong, correct: false },
          { id: "right", label: right, correct: true },
        ],
        on_choice: {
          right: { message: "맞아요. 그 표현이면 충분해요.", next: "advance" },
          wrong: {
            message: `괜찮아요. 정답은 '${right}'예요.`,
            reveal_answer: true,
            next: "advance",
          },
        },
      },
      screen: "study",
      buttons: uniqueButtons([wrong, right, UNKNOWN_BTN]),
      placeholder: "선생님께 답해 보세요…",
      effect: null,
    },
  );
}

function climbHint(s: EngineState): EngineState {
  const miss = s.missCount + 1;
  if (miss >= 4) return frustration({ ...s, missCount: miss, hadAnyError: true });
  const rung = Math.min(3, s.hintRung + 1) as 1 | 2 | 3;
  return say(s, hintOf(s, rung) ?? hintOf(s, 1)!, {
    hintRung: rung,
    missCount: miss,
    hadAnyError: true,
    pending: null,
    screen: "study",
    buttons: [HINT_BTN, UNKNOWN_BTN],
    placeholder: "해석을 적어 보세요…",
    effect: null,
  });
}

/**
 * 모델에게 넘길 **현재 unit만** 추린다.
 *
 * 힌트 사다리는 지금 허용된 단까지만 잘라서 넘긴다 — 다음 단을 보여 주고
 * "쓰지 마"라고 지시하면 언젠가 쓴다.
 */
function briefOf(s: EngineState): UnitBrief {
  const u = current(s);
  const allowedRung = Math.min(3, s.hintRung + 1);
  return {
    index: s.unitIndex,
    text: u.text,
    scoringPoints: (u.scoring_points ?? []).map((p) => p.text),
    errorPriority: u.error_priority ?? [],
    hintLadderVisible: (u.hint_ladder ?? [])
      .filter((h) => h.rung <= allowedRung)
      .map((h) => h.message),
  };
}

/**
 * 이번 턴에 절대 나오면 안 되는 문자열 — 나오면 그 발화를 버린다.
 *
 * **채점 포인트의 한국어 쪽도 넣는다.** 모델에게 `scoring_points`를 주는 이유는
 * 판정하라고지 읊으라고가 아니다. 안 막으면 모범 해석을 피해 가면서
 * `serve → 근무하다` 같은 답을 그대로 흘린다 (2026-09-06 가짜 어댑터로 재현).
 */
function bannedFor(s: EngineState): string[] {
  const u = current(s);
  const allowedRung = Math.min(3, s.hintRung + 1);
  const correctChoices = (u.expected_errors ?? []).flatMap((e) =>
    (e.treatment?.choices ?? []).filter((c) => c.correct).map((c) => c.label),
  );
  const lockedHints = (u.hint_ladder ?? [])
    .filter((h) => h.rung > allowedRung)
    .map((h) => h.message);
  // "It has been a privilege to ~ → '~할 수 있어서 영광이었다'" 에서 화살표 뒤쪽
  const scoringAnswers = (u.scoring_points ?? []).flatMap((point) => {
    const tail = point.text.split("→").slice(1).join("→").trim();
    const cleaned = tail.replace(/^['"“”‘’]|['"“”‘’]$/g, "").trim();
    return cleaned ? [cleaned] : [];
  });
  return [
    u.model_translation,
    ...correctChoices,
    ...lockedHints,
    ...scoringAnswers,
  ];
}

/**
 * **D(예상 밖) · B(부분 정답) — 모델이 열리는 유일한 자리.**
 *
 * 어댑터가 없으면 여기서 하는 일은 `climbHint`와 똑같다. 즉 지금 데모의 동작이
 * 그대로 남는다. 어댑터가 있어도 다음은 코드가 쥔다:
 * - miss 카운트와 좌절 임계(4번째)는 모델을 부르기 **전에** 코드가 판단한다
 * - 가드레일에 걸리면 발화를 버리고 힌트 사다리 한 단으로 폴백한다
 * - `effect: "light"`는 스스로 고친 순간만이므로 여기서는 절대 켜지 않는다
 */
async function treatUnexpectedOrPartial(
  s: EngineState,
  text: string,
): Promise<EngineState> {
  const llm = getTutorLlm();
  if (!llm) return climbHint(s);

  const miss = s.missCount + 1;
  if (miss >= 4) {
    return frustration({ ...s, missCount: miss, hadAnyError: true });
  }

  const unit = briefOf(s);
  const judged = llm.judge
    ? await safeCall(() => llm.judge!({ studentText: text, unit }))
    : null;
  const partial = judged?.diagnosis === "B";

  const spoken = await safeCall(() =>
    llm.speak({
      action: partial ? "TREAT_PARTIAL" : "TREAT_UNEXPECTED",
      studentText: text,
      unit,
      state: {
        unitIndex: s.unitIndex,
        hintRung: s.hintRung,
        missCount: s.missCount,
        lastTutorUtterance: s.lastTutorUtterance,
      },
      matchedPoints: judged?.matchedPoints,
    }),
  );
  if (!spoken) return climbHint(s);

  const verdict = validateLlmOutput(spoken, { bannedStrings: bannedFor(s) });
  if (!verdict.ok) {
    console.warn("[tutor] 발화 폐기 →", verdict.reason);
    return climbHint(s);
  }

  return say(s, spoken.message, {
    missCount: miss,
    hadAnyError: true,
    pending: null,
    screen: "study",
    buttons: uniqueButtons([...(spoken.buttons ?? []), UNKNOWN_BTN]),
    placeholder: "해석을 적어 보세요…",
    effect: null,
  });
}

function compactEq(a: string, b: string) {
  return a.replace(/\s+/g, "") === b.replace(/\s+/g, "");
}

function handlePending(s: EngineState, text: string): EngineState {
  const pending = s.pending!;
  if (isUnknownInput(text)) {
    if (pending.errorId === "FRUSTRATION") {
      return advance({ ...s, pending: null, skipFinalRetake: true }, "괜찮아요, 방금 같이 본 그 문장이에요.", false);
    }
    return climbHint({ ...s, pending: null });
  }
  const byLabel = matchChoice(text, pending.choices.map((c) => c.label));
  const choice =
    pending.choices.find((c) => c.label === byLabel || compactEq(text, c.id)) ??
    pending.choices.find((c) => byLabel === c.label);
  if (!choice) return climbHint({ ...s, pending: null });
  const branch = pending.on_choice[choice.id];
  if (!branch) return climbHint({ ...s, pending: null });
  if (pending.errorId === "FRUSTRATION" || branch.next === "advance") {
    return advance({ ...s, pending: null, skipFinalRetake: true, result: "설명제공" }, branch.message, false);
  }
  const light = !!choice.correct && !branch.reveal_answer;
  return say(s, branch.message, {
    pending: null,
    screen: "study",
    buttons: [HINT_BTN, UNKNOWN_BTN],
    placeholder: "해석을 적어 보세요…",
    effect: light ? "light" : null,
  });
}

export function createSession() {
  let s = initialState();
  return {
    view: () => view(s),
    async submit(raw: string) {
      const text = raw.trim();
      if (!text || s.ended) return view(s);
      s = { ...s, studentLine: text, effect: null };

      if (s.pending) {
        s = handlePending(s, text);
        return view(s);
      }

      if (s.stage === "intro") {
        const lead = isUnknownInput(text) ? "괜찮아요, 같이 보면 돼요. " : "좋아요. ";
        s = startUnit(s, 0, lead);
        return view(s);
      }

      if (text === READ_BTN) {
        s = say(s, "잘 읽었어요. 그럼 이 문장을 한국어로 적어 볼까요?", {
          screen: "study",
          buttons: [HINT_BTN, UNKNOWN_BTN],
        });
        return view(s);
      }

      const path = classifyUnit(text, UNIT_MATCH[s.unitIndex]!);

      if (path === "P1") {
        s = advance(s, PRAISE[s.unitIndex]!, s.hadAnyError);
        return view(s);
      }
      if (path === "P2") {
        s = openBranch(s, "P2");
        return view(s);
      }
      if (path === "P3") {
        s = openBranch(s, "P3");
        return view(s);
      }

      /*
        여기부터 두 갈래다. **E와 D를 섞으면 안 된다.**
        학생이 스스로 「잘 모르겠어요」라고 말한 것(E)은 코드가 힌트 사다리를
        한 단 올린다 — 모델을 부르지 않는다.
      */
      if (isUnknownInput(text)) {
        s = climbHint(s);
        return view(s);
      }

      // 해석을 시도했는데 A(P1)도 C(P2/P3)도 아니다 = D, 판정에 따라 B.
      s = await treatUnexpectedOrPartial(s, text);
      return view(s);
    },
    reset() {
      s = initialState();
      return view(s);
    },
  };
}

export type TutorSession = ReturnType<typeof createSession>;
