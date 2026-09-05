import frame from "../../content/tutor/frame.json";
import type { Lesson, LessonChunk, ProperNoun, TutorResult } from "../../content/tutor/types";
import { getLesson } from "./lessons";
import {
  getTutorLlm,
  safeCall,
  validateLlmOutput,
  type UnitBrief,
} from "./llm";
import { classify, isUnknownInput, matchChoice } from "./match";
import {
  askedAboutProperNoun,
  askedAboutWord,
  isTaughtWord,
  nounKind,
} from "./proper-nouns";

export const UNKNOWN_BTN = "잘 모르겠어요";
export const HINT_BTN = "힌트 주세요";
export const READY_BTN = "네, 좋아요!";
export const READ_BTN = "다 읽었어요";

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
  /** 이 세션이 가르치는 지문. 지문 교체는 이것만 바꾸면 된다 */
  lesson: Lesson;
  stage: "intro" | "unit" | "done";
  unitIndex: number;
  hintRung: 0 | 1 | 2 | 3;
  missCountInUnit: number;
  skipFinalRetake: boolean;
  hadAnyError: boolean;
  /** 힌트 3단(=모범 해석 공개)까지 간 문장이 하나라도 있었나 */
  reachedHint3: boolean;
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
  return s.lesson.chunks[s.unitIndex]!;
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

/**
 * 인트로도 **레슨에서 만든다.**
 * 예전에는 "퇴사 인사 편지…Lewis Ltd.…"가 코드에 박혀 있어서, 지문을 바꾸면
 * 다른 지문을 앞에 두고 퇴사 편지를 소개했다.
 */
function introMessage(lesson: Lesson): string {
  const tip = lesson.proper_noun_tip?.message?.trim();
  return [
    `오늘은 ${lesson.topic_intro}를 볼 거예요.`,
    tip,
    "한 문장씩 해석해볼까요?",
  ]
    .filter(Boolean)
    .join(" ");
}

/** 레슨에 칭찬 문구가 없으면 프레임의 기본 칭찬 */
function praiseFor(s: EngineState): string {
  return current(s).praise ?? frame.fixed_lines.praise_default;
}

function initialState(lesson: Lesson): EngineState {
  const intro = introMessage(lesson);
  return {
    lesson,
    stage: "intro",
    unitIndex: 0,
    hintRung: 0,
    missCountInUnit: 0,
    skipFinalRetake: false,
    hadAnyError: false,
    reachedHint3: false,
    pending: null,
    errorIds: [],
    result: null,
    lastTutorUtterance: intro,
    studentLine: "",
    effect: null,
    screen: "chat",
    message: intro,
    buttons: [READY_BTN, UNKNOWN_BTN],
    placeholder: "선생님께 답해 보세요…",
    ended: false,
  };
}

function nounsIn(s: EngineState, text: string): ProperNoun[] {
  return (s.lesson.proper_nouns ?? []).filter((n) =>
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
    progressTotal: s.lesson.chunks.length,
    ended: s.ended,
    properNouns:
      s.stage === "intro" ? s.lesson.proper_nouns ?? [] : nounsIn(s, u.text),
    recordLine:
      s.ended && s.result
        ? `[기록] 유형=${s.lesson.grammar_type} / 결과=${s.result} / 오류=${s.errorIds.join(",") || "없음"}`
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
    stage: "unit",
    unitIndex: index,
    hintRung: 0,
    missCountInUnit: 0,
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
  if (s.unitIndex < s.lesson.chunks.length - 1) {
    return startUnit(stepped, s.unitIndex + 1, `${praise} 다음 문장이에요. `);
  }
  /*
    **결과 네 값이 여기서 갈린다.** `[기록]`은 다음 수업을 고르는 근거라
    "그냥 다 오류후이해"로 뭉치면 쓸모가 없다. 강한 신호부터 본다.

    설명제공 — 좌절 방지가 발동해서 정답을 설명해 줬다 (시도를 더 강요하지 않음)
    취약     — 좌절까지는 아니지만 힌트 3단(정답 공개)을 봐야 넘어간 문장이 있다
    오류후이해 — 틀렸지만 3단 전에 스스로 고쳤다
    이해     — 오류 없이 통과
  */
  if (s.skipFinalRetake) {
    return finish(stepped, "설명제공", `${praise} 끝까지 같이 봤어요. 오늘은 여기까지 해요.`);
  }
  if (!s.hadAnyError) {
    return finish(
      stepped,
      "이해",
      `${praise} ${s.lesson.chunks.length}문장 모두 잘 따라왔어요. 오늘 정말 잘했어요.`,
    );
  }
  if (s.reachedHint3) {
    return finish(
      stepped,
      "취약",
      `${praise} 오늘은 힌트를 끝까지 본 문장이 있었어요. 같은 유형을 한 번 더 보면 훨씬 편해질 거예요.`,
    );
  }
  return finish(
    stepped,
    "오류후이해",
    `${praise} 막히는 지점도 있었는데, 끝까지 왔어요. 오늘 수업은 여기까지예요.`,
  );
}

function openBranch(s: EngineState, errorId: string): EngineState {
  const error = errorOf(s, errorId);
  // `rounds`로 쓴 레슨도 첫 라운드를 고정 대사로 쓴다 (탈레스 E3)
  const t = error?.treatment ?? error?.rounds?.[0];
  if (!t?.message) return climbHint(s);
  const choices = t.choices ?? [];
  return say(s, t.message, {
    hadAnyError: true,
    missCountInUnit: s.missCountInUnit + 1,
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
  /*
    쉬운 2지선다의 오답 쪽은 **레슨이 이미 적어 둔 오해**에서 가져온다.
    예전에는 "P2"/"P3"라는 id를 코드가 알고 있어서, id 체계가 다른 레슨
    (탈레스의 E1~E4)에서는 아무것도 못 찾았다.
  */
  const wrong =
    (u.expected_errors ?? [])
      .flatMap((e) => e.treatment?.choices ?? e.rounds?.[0]?.choices ?? [])
      .find((c) => !c.correct)?.label ?? "잘 모르겠어요";
  const right = u.model_translation;
  return say(
    s,
    /*
      프레임 문구가 이미 「까다롭죠?」로 한 번 묻는다. 여기서 또 물으면
      한 턴에 질문이 둘이 된다 — 버튼이 바로 아래 있으니 청유형으로 끝낸다.
    */
    `${frame.fixed_lines.frustration_tone} 정답은 '${right}'예요. 아래에서 더 가까운 쪽을 골라 주세요.`,
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

/**
 * **역질문 — 오답이 아니다.**
 *
 * 고유명사를 되물으면 짧게 답하고 하던 자리로 돌려보낸다. miss도 힌트 단수도
 * 건드리지 않는다 (`ARCHITECTURE.md` §4-2). 이게 없을 때는 「Asia Minor가
 * 뭐예요?」가 오답(E)으로 세어져서, 궁금해서 물어본 학생이 힌트를 한 단
 * 잃고 좌절 방지에 가까워졌다.
 *
 * 2지선다가 열려 있으면 **그대로 둔다** — 답할 자리를 뺏지 않는다.
 */
function answerProperNoun(s: EngineState, noun: ProperNoun): EngineState {
  const told = frame.fixed_lines.proper_noun_question
    .replace("{name}", noun.en)
    .replace("{type}", nounKind(noun.type));
  return say(s, `${told} ${frame.fixed_lines.return_to_lesson}`, {
    // 화면·버튼·카운터는 건드리지 않는다. 하던 자리 그대로다
    effect: null,
  });
}

function climbHint(s: EngineState): EngineState {
  const miss = s.missCountInUnit + 1;
  if (miss >= 4) return frustration({ ...s, missCountInUnit: miss, hadAnyError: true });
  const rung = Math.min(3, s.hintRung + 1) as 1 | 2 | 3;
  return say(s, hintOf(s, rung) ?? hintOf(s, 1)!, {
    hintRung: rung,
    missCountInUnit: miss,
    hadAnyError: true,
    /*
      3단은 모범 해석을 알려 주는 단이다. 그 문장은 스스로 못 넘은 것으로 남긴다.
      **3단이 없는 레슨에서는 세지 않는다** — 사다리가 2칸뿐이라 학생이 정답을
      본 적이 없는데 「취약」으로 남으면 기록이 거짓말이 된다.
    */
    reachedHint3: s.reachedHint3 || (rung === 3 && hintOf(s, 3) != null),
    /*
      예상 오류(C)만 기록하면 「결과=취약 / 오류=없음」이 나온다. 정답을 보고
      넘어간 문장도 다음 수업을 고르는 근거이므로 같이 남긴다.
    */
    errorIds:
      rung === 3 && hintOf(s, 3) != null && !s.errorIds.includes(`${s.unitIndex + 1}:HINT3`)
        ? [...s.errorIds, `${s.unitIndex + 1}:HINT3`]
        : s.errorIds,
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
 * **단어 뜻 질문.**
 *
 * 「serve가 뭐예요?」는 무시할 질문이 아니다. 다만 답이 두 갈래다.
 *
 * - **이번 문장에서 가르치는 단어**(채점 포인트·예상 오류가 겨냥하는 단어)면
 *   뜻이 곧 정답이다. 그냥 알려 주면 학생은 다음부터 해석 대신 단어부터
 *   물어보고, 힌트 사다리에 옆문이 생긴다. 그래서 **사다리 한 단으로 답한다** —
 *   침묵이 아니라 그 단어를 콕 집은 응답이다(2단이 정확히 그 대사다).
 * - **가르치지 않는 단어**는 그냥 막힌 것이다. 알려 주고 하던 자리로 돌려보낸다.
 *   레슨 JSON에 단어 사전이 없으므로 이건 모델이 답한다. 어댑터가 없으면
 *   사다리로 폴백한다.
 */
async function answerWord(
  s: EngineState,
  word: string,
  studentText: string,
): Promise<EngineState> {
  if (isTaughtWord(word, current(s))) return climbHint(s);

  const llm = getTutorLlm();
  if (!llm) return climbHint(s);

  const spoken = await safeCall(() =>
    llm.speak({
      action: "ANSWER_WORD",
      askedWord: word,
      studentText,
      unit: briefOf(s),
      state: {
        unitIndex: s.unitIndex,
        hintRung: s.hintRung,
        missCountInUnit: s.missCountInUnit,
        lastTutorUtterance: s.lastTutorUtterance,
      },
    }),
  );
  if (!spoken) return climbHint(s);

  const verdict = validateLlmOutput(spoken, { bannedStrings: bannedFor(s) });
  if (!verdict.ok) {
    console.warn("[tutor] 단어 뜻 발화 폐기 →", verdict.reason);
    return climbHint(s);
  }

  // 물어본 것은 오답이 아니다 — miss도 힌트 단수도 그대로다
  return say(s, `${spoken.message} ${frame.fixed_lines.return_to_lesson}`, {
    effect: null,
  });
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

  const miss = s.missCountInUnit + 1;
  if (miss >= 4) {
    return frustration({ ...s, missCountInUnit: miss, hadAnyError: true });
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
        missCountInUnit: s.missCountInUnit,
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
    missCountInUnit: miss,
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
      return advance(
        { ...s, pending: null, skipFinalRetake: true },
        "괜찮아요, 방금 같이 본 그 문장이에요.",
        false,
      );
    }
    return climbHint({ ...s, pending: null });
  }
  /*
    **좌절 방지 뒤에는 학생을 붙잡아 두지 않는다.**
    선택지 밖의 답이 와도 다음 문장으로 넘긴다. 예전에는 여기서 `climbHint`로
    갔는데, miss가 이미 4라 좌절 방지가 다시 열리고 → 또 못 맞히고 → 무한히
    같은 문장에 갇혔다 (2026-09-06 재현: 「네」라고 답하니 수업이 안 끝났다).
  */
  const escapeFrustration = (state: EngineState) =>
    advance(
      { ...state, pending: null, skipFinalRetake: true },
      "괜찮아요, 방금 같이 본 그 문장이에요.",
      false,
    );

  const byLabel = matchChoice(text, pending.choices.map((c) => c.label));
  const choice =
    pending.choices.find((c) => c.label === byLabel || compactEq(text, c.id)) ??
    pending.choices.find((c) => byLabel === c.label);
  if (!choice) {
    return pending.errorId === "FRUSTRATION"
      ? escapeFrustration(s)
      : climbHint({ ...s, pending: null });
  }
  const branch = pending.on_choice[choice.id];
  if (!branch) {
    return pending.errorId === "FRUSTRATION"
      ? escapeFrustration(s)
      : climbHint({ ...s, pending: null });
  }
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

/**
 * 한 수업 세션. `lessonId`를 주면 그 지문으로 시작한다
 * (없거나 못 찾으면 첫 레슨).
 */
export function createSession(lessonId?: string | null) {
  const lesson = getLesson(lessonId);
  let s = initialState(lesson);
  return {
    view: () => view(s),
    async submit(raw: string) {
      const text = raw.trim();
      if (!text || s.ended) return view(s);
      s = { ...s, studentLine: text, effect: null };

      /*
        **순서를 바꾸지 않는다** (ARCHITECTURE §4).
        역질문은 2지선다보다 먼저 본다. 학생이 선택지를 고르다 말고 이름을
        물어봤을 때, 그걸 「선택지 밖 답」으로 처리하면 오답이 된다.
      */
      const asked =
        s.stage !== "intro"
          ? askedAboutProperNoun(text, s.lesson.proper_nouns ?? [])
          : null;
      if (asked) {
        s = answerProperNoun(s, asked);
        return view(s);
      }

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

      /*
        단어 뜻 질문은 해석 시도가 아니다. `classify`에 넘기면 예상 밖(D)으로
        보고 힌트를 올린다 — 물어본 학생이 사다리를 한 단 잃는다.
      */
      const askedWord = askedAboutWord(text, current(s).text);
      if (askedWord) {
        s = await answerWord(s, askedWord, text);
        return view(s);
      }

      const verdict = classify(text, current(s));

      if (verdict.kind === "A") {
        s = advance(s, praiseFor(s), s.hadAnyError);
        return view(s);
      }
      if (verdict.kind === "C") {
        s = openBranch(s, verdict.errorId);
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
      s = initialState(lesson);
      return view(s);
    },
  };
}

export type TutorSession = ReturnType<typeof createSession>;
