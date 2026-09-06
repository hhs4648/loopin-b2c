import frame from "../../content/tutor/frame.json";
import type {
  Lesson,
  LessonChunk,
  ProperNoun,
  ScoringPoint,
  TutorResult,
} from "../../content/tutor/types";
import { getLesson } from "./lessons";
import {
  getTutorLlm,
  safeCall,
  validateLlmOutput,
  type GuardContext,
  type UnitBrief,
} from "./llm";
import { parseName } from "./learner-name";
import { classify, isUnknownInput, matchChoice } from "./match";
import {
  askedAboutProperNoun,
  askedAboutWord,
  askedWhy,
  isTaughtWord,
  nounKind,
} from "./proper-nouns";

export const UNKNOWN_BTN = "잘 모르겠어요";
export const HINT_BTN = "힌트 주세요";
export const READY_BTN = "네, 좋아요!";
export const READ_BTN = "다 읽었어요";
export const MORE_BTN = "더 알고 싶어요";
export const NEXT_BTN = "다음으로";

export type UiScreen = "chat" | "study";

/**
 * 항목 하나에 대한 학습 기록.
 *
 * **`firstTry`가 난이도의 근거다.** 유도 후 결과로 난이도를 재면, 우리가 늘
 * 1번 항목을 먼저 유도하기 때문에 1번이 쉬워 보이는 편향이 생긴다.
 * 지금은 세션 안에만 쌓이고, 서버가 생기면 그대로 흘려보낸다.
 */
export type PointRecord = {
  lessonId: string;
  unit: number;
  point: number;
  firstTry: boolean;
  nudged: boolean;
  told: boolean;
  /** 좌절 방지로 모범 해석을 본 뒤였나 */
  revealed: boolean;
};

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
  /** 「왜요?」라고 물었을 때만 꺼내는 원리 설명. 묻기 전에는 하지 않는다 */
  onWhy?: string;
};

type EngineState = {
  /** 이 세션이 가르치는 지문. 지문 교체는 이것만 바꾸면 된다 */
  lesson: Lesson;
  /** 부를 이름. 없으면 이름 없이 인사한다 — 받아낼 때까지 되묻지 않는다 */
  learnerName: string | null;
  stage: "greeting" | "intro" | "unit" | "done";
  unitIndex: number;
  missCountInUnit: number;
  skipFinalRetake: boolean;
  hadAnyError: boolean;
  /** 이번 문장에서 학생이 낸 체크리스트 항목 */
  checkedPoints: number[];
  /** 첫 시도에 스스로 낸 항목 — 난이도 데이터의 근거 */
  firstTryPoints: number[];
  /** 이미 한 번 유도한 항목 (두 번째부터는 `tell`) */
  nudgedPoints: number[];
  /** 이번 문장에서 답을 알려 준 항목 */
  toldPoints: number[];
  /**
   * 세션 전체에서 한 번이라도 답을 알려 줬나 → 결과 「취약」.
   * `toldPoints`는 문장이 바뀌면 비워지므로 그것만 보면 마지막 문장만 남는다.
   */
  toldAnyPoint: boolean;
  /** 이번 문장에서 해석을 시도한 횟수 */
  attemptsInUnit: number;
  /**
   * 이 문장에서 각 예상 오류가 몇 번째인지.
   * 같은 실수를 두 번째로 하면 **다른 방식으로** 대응해야 한다 —
   * 같은 대사를 또 하면 학생은 말이 안 통한다고 느낀다.
   */
  errorRounds: Record<string, number>;
  /**
   * 설명 국면 — 지금 보여 주고 있는 `teach_points` 번호. 아니면 null.
   *
   * 좌절 방지로 답을 알려 준 학생에게만 연다. 스스로 푼 학생을 붙잡고 설명하면
   * 그건 상이 아니라 벌이다.
   */
  teaching: number | null;
  /** 이미 심화(enrichment)까지 본 항목 */
  enrichedPoints: number[];
  /** 항목 단위 학습 기록. 서버가 생기면 그대로 흘려보낸다 */
  pointLog: PointRecord[];
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

function uniqueButtons(btns: string[]) {
  return [...new Set(btns.filter(Boolean))];
}

/**
 * 인트로도 **레슨에서 만든다.**
 * 예전에는 "퇴사 인사 편지…Lewis Ltd.…"가 코드에 박혀 있어서, 지문을 바꾸면
 * 다른 지문을 앞에 두고 퇴사 편지를 소개했다.
 */
function introMessage(lesson: Lesson, name: string | null): string {
  const tip = lesson.proper_noun_tip?.message?.trim();
  const hello = name
    ? frame.fixed_lines.greet_named.replace("{name}", name)
    : frame.fixed_lines.greet_plain;
  return [
    hello,
    `오늘은 ${lesson.topic_intro}를 볼 거예요.`,
    tip,
    frame.fixed_lines.ready_question,
  ]
    .filter(Boolean)
    .join(" ");
}

/**
 * 이름을 받고(또는 못 알아듣고) 수업 소개로 넘어간다.
 *
 * 이름은 여기서 한 번만 정해진다. 못 알아들으면 `null`이고, 그러면 그냥
 * "안녕하세요!"로 연다.
 */
function enterIntro(s: EngineState, name: string | null): EngineState {
  return say(s, introMessage(s.lesson, name), {
    learnerName: name,
    stage: "intro",
    screen: "chat",
    buttons: [READY_BTN, UNKNOWN_BTN],
    placeholder: "선생님께 답해 보세요…",
  });
}

/** 레슨에 칭찬 문구가 없으면 프레임의 기본 칭찬 */
function praiseFor(s: EngineState): string {
  return current(s).praise ?? frame.fixed_lines.praise_default;
}

function initialState(lesson: Lesson, learnerName: string | null): EngineState {
  /*
    이름을 아는 학생에게 또 묻지 않는다. 두 번째 수업부터는 곧장 인사로 연다.
  */
  const asking = !learnerName;
  const opening = asking
    ? frame.fixed_lines.ask_name
    : introMessage(lesson, learnerName);
  return {
    lesson,
    learnerName,
    stage: asking ? "greeting" : "intro",
    unitIndex: 0,
    missCountInUnit: 0,
    skipFinalRetake: false,
    hadAnyError: false,
    checkedPoints: [],
    firstTryPoints: [],
    nudgedPoints: [],
    toldPoints: [],
    toldAnyPoint: false,
    attemptsInUnit: 0,
    errorRounds: {},
    teaching: null,
    enrichedPoints: [],
    pointLog: [],
    pending: null,
    errorIds: [],
    result: null,
    lastTutorUtterance: opening,
    studentLine: "",
    effect: null,
    screen: "chat",
    message: opening,
    buttons: asking ? [] : [READY_BTN, UNKNOWN_BTN],
    placeholder: asking ? "이름을 알려 주세요…" : "선생님께 답해 보세요…",
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
      s.stage === "greeting"
        ? [] // 이름을 묻는 자리에 지문 이야기를 같이 띄우지 않는다
        : s.stage === "intro"
          ? s.lesson.proper_nouns ?? []
          : nounsIn(s, u.text),
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
    missCountInUnit: 0,
    checkedPoints: [],
    firstTryPoints: [],
    nudgedPoints: [],
    toldPoints: [],
    attemptsInUnit: 0,
    errorRounds: {},
    teaching: null,
    enrichedPoints: [],
    pending: null,
    screen: "study",
    placeholder: "해석을 적어 보세요…",
    buttons: [READ_BTN, HINT_BTN, UNKNOWN_BTN],
    /*
      **`effect`를 여기서 끄지 않는다.** 스스로 고친 턴은 반짝여야 하는데,
      그 순간이 곧 다음 문장으로 넘어가는 순간이라 여기서 null로 덮으면
      `light`가 화면에 도달한 적이 없다. 다음 입력이 오면 `submit`이 끈다.
    */
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

/**
 * **설명 국면 — 한 번에 하나씩.**
 *
 * 레슨의 `teach_points`를 순서대로 하나씩 내보내고 학생을 기다린다. 한꺼번에
 * 쏟으면 그건 강의고, 학생은 읽지 않는다 (`BEHAVIOR.md` §5).
 *
 * 체크리스트와 내용이 겹치는 항목이 많다 — 겹치는 건 이미 유도에서 다뤘고,
 * 여기서 새로 생기는 건 **`enrichment`**(더 깊은 설명)다. 그래서 「더 알고
 * 싶어요」를 누른 학생에게만 그걸 준다.
 */
function teachStep(s: EngineState, index: number): EngineState {
  const points = current(s).teach_points ?? [];
  const point = points[index];
  if (!point) {
    return advance(
      { ...s, teaching: null },
      "오늘 이 문장은 여기까지 같이 봤어요.",
      false,
    );
  }
  const more = point.enrichment && !s.enrichedPoints.includes(index) ? [MORE_BTN] : [];
  return say(s, point.message, {
    teaching: index,
    screen: "study",
    buttons: uniqueButtons([...more, NEXT_BTN]),
    placeholder: "선생님께 답해 보세요…",
    effect: null,
  });
}

function handleTeaching(s: EngineState, text: string): EngineState {
  const index = s.teaching!;
  const point = (current(s).teach_points ?? [])[index];
  const wantsMore = matchChoice(text, [MORE_BTN]) != null;

  if (wantsMore && point?.enrichment && !s.enrichedPoints.includes(index)) {
    return say(s, point.enrichment, {
      enrichedPoints: [...s.enrichedPoints, index],
      buttons: [NEXT_BTN],
      screen: "study",
      placeholder: "선생님께 답해 보세요…",
      effect: null,
    });
  }
  return teachStep(s, index + 1);
}

/** 이 문장의 항목별 결과. 서버가 생기면 그대로 쌓아 난이도 순서를 덮어쓴다 */
function recordsFor(s: EngineState): PointRecord[] {
  return (current(s).scoring_points ?? []).map((p) => ({
    lessonId: s.lesson.id,
    unit: s.unitIndex + 1,
    point: p.id,
    /** 유도 **전에** 스스로 냈나 — 난이도는 이것만 본다 */
    firstTry: s.firstTryPoints.includes(p.id),
    nudged: s.nudgedPoints.includes(p.id),
    told: s.toldPoints.includes(p.id),
    revealed: s.skipFinalRetake,
  }));
}

function advance(s: EngineState, praise: string, light: boolean): EngineState {
  const logged = { ...s, pointLog: [...s.pointLog, ...recordsFor(s)] };
  const stepped = { ...logged, effect: light ? ("light" as const) : null };
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
  if (s.toldAnyPoint) {
    return finish(
      stepped,
      "취약",
      `${praise} 오늘은 답을 같이 본 곳이 있었어요. 같은 유형을 한 번 더 보면 훨씬 편해질 거예요.`,
    );
  }
  return finish(
    stepped,
    "오류후이해",
    `${praise} 막히는 지점도 있었는데, 끝까지 왔어요. 오늘 수업은 여기까지예요.`,
  );
}

/**
 * 예상 오류(C) 처치.
 *
 * **같은 오류를 두 번째로 하면 라운드가 넘어간다.** 레슨이 `rounds`로 여러 벌을
 * 적어 둔 경우(탈레스 E3), 1회차는 짧은 교정만 하고 2회차에 2지선다로 방식을
 * 바꾼다. 예전에는 항상 첫 라운드만 써서 같은 대사가 반복됐다 —
 * `TEST_SCENARIOS` #10이 「1회차 설명을 다시 하면 실패」라고 정해 둔 그 동작이다.
 *
 * 라운드를 다 쓰면 마지막 라운드를 유지한다. 없는 라운드를 찾다가 침묵하는 것보다
 * 낫다.
 */
function openBranch(s: EngineState, errorId: string): EngineState {
  const error = errorOf(s, errorId);
  const rounds = error?.rounds?.length
    ? error.rounds
    : error?.treatment
      ? [error.treatment]
      : [];
  const round = (s.errorRounds[errorId] ?? 0) + 1;
  const t = rounds[Math.min(round, rounds.length) - 1];
  if (!t?.message) return nudgeNext(s, s.checkedPoints);
  const choices = t.choices ?? [];
  return say(s, t.message, {
    hadAnyError: true,
    missCountInUnit: s.missCountInUnit + 1,
    errorRounds: { ...s.errorRounds, [errorId]: round },
    errorIds: s.errorIds.includes(`${s.unitIndex + 1}:${errorId}`)
      ? s.errorIds
      : [...s.errorIds, `${s.unitIndex + 1}:${errorId}`],
    pending:
      t.on_choice && choices.length
        ? { errorId, choices, on_choice: t.on_choice, onWhy: t.on_why_question?.message }
        : t.on_why_question?.message
          ? { errorId, choices: [], on_choice: {}, onWhy: t.on_why_question.message }
          : null,
    screen: "study",
    buttons: uniqueButtons([...choices.map((c) => c.label), UNKNOWN_BTN]),
    placeholder: "선생님께 답해 보세요…",
    effect: null,
  });
}

/**
 * 좌절 방지에 낼 2지선다 한 쌍.
 *
 * **레슨이 이미 짝지어 둔 보기를 그대로 쓴다.** 예전에는 오답만 레슨에서
 * 가져오고 정답 자리에 **모범 해석 전체**를 넣었다. 방금 알려 준 그 문장이
 * 그대로 보기가 되니 고를 게 없는 문제가 됐다 (2026-09-06 화면).
 *
 * 막힌 항목을 겨냥한 오해부터 찾는다 — 그 오해의 정답 보기가 항목의 `check`에
 * 걸리면 같은 것을 다루고 있다는 뜻이다. 없으면 이 문장의 다른 오해라도 쓴다.
 * 같은 문장 이야기라 어긋나지 않는다.
 */
function frustrationPair(
  s: EngineState,
  target?: ScoringPoint,
): { right: string; wrong: string } | null {
  const pairs = (current(s).expected_errors ?? [])
    /*
      **모든 라운드를 본다.** 탈레스 E3의 2지선다는 2라운드에 있어서, 1라운드만
      보던 예전 코드는 그 문장에서 아무 보기도 못 찾았다.
    */
    .map((e) => [
      ...(e.treatment?.choices ?? []),
      ...(e.rounds ?? []).flatMap((r) => r.choices ?? []),
    ])
    .map((cs) => ({
      right: cs.find((c) => c.correct)?.label ?? "",
      wrong: cs.find((c) => !c.correct)?.label ?? "",
    }))
    .filter((p) => p.right && p.wrong);

  const keys = target?.check ?? [];
  return pairs.find((p) => keys.some((k) => p.right.includes(k))) ?? pairs[0] ?? null;
}

/**
 * 「invaluable → 매우 소중하다」에서 앞쪽만. 물어볼 자리의 이름이 필요하다.
 *
 * 화살표가 없는 형식(탈레스의 「in을 '~에서'로 처리」)은 통째로 설명문이라
 * 이름으로 못 쓴다. 그때는 빈 문자열을 주고 일반 문구로 묻는다.
 */
function englishOf(point?: ScoringPoint): string {
  const text = point?.text ?? "";
  if (!text.includes("→")) return "";
  const head = text.split("→")[0]!.trim();
  return /[a-zA-Z]/.test(head) && head.length <= 30 ? head : "";
}

function frustration(s: EngineState): EngineState {
  const u = current(s);
  const points = u.scoring_points ?? [];
  const target = points.find((p) => !s.checkedPoints.includes(p.id)) ?? points[0];
  const answer = u.model_translation;
  const opening = `${frame.fixed_lines.frustration_tone} 정답은 '${answer}'예요.`;
  const base = {
    skipFinalRetake: true,
    hadAnyError: true,
    result: "설명제공" as const,
    pending: null,
  };

  const pair = frustrationPair(s, target);
  if (!pair) {
    /*
      짝지을 보기가 없으면 **억지로 문제를 만들지 않는다.** 설명하고 넘어간다.
      한쪽만 있는 2지선다는 문제가 아니라 받아쓰기다.
    */
    const next = { ...s, ...base };
    const teach = (u.teach_points ?? [])[0];
    return teach
      ? say(teachStep(next, 0), `${opening} ${teach.message}`)
      : advance(next, opening, false);
  }

  /*
    영어 낱말에 한국어 조사를 붙이면 「invaluable는」처럼 틀린 말이 나온다.
    받침을 알 수 없으므로 조사가 붙지 않는 자리에 놓는다.
  */
  const english = englishOf(target);
  const tail = english
    ? `아래에서 '${english}'의 뜻에 더 가까운 쪽을 골라 주세요.`
    : "아래에서 더 가까운 쪽을 골라 주세요.";
  const correct = english
    ? `맞아요. '${english}'의 뜻은 '${pair.right}'예요.`
    : `맞아요. '${pair.right}'가 맞아요.`;

  return say(
    s,
    /*
      프레임 문구가 이미 「까다롭죠?」로 한 번 묻는다. 여기서 또 물으면
      한 턴에 질문이 둘이 된다 — 버튼이 바로 아래 있으니 청유형으로 끝낸다.
    */
    `${opening} ${tail}`,
    {
      ...base,
      pending: {
        errorId: "FRUSTRATION",
        choices: [
          { id: "wrong", label: pair.wrong, correct: false },
          { id: "right", label: pair.right, correct: true },
        ],
        on_choice: {
          right: { message: correct, next: "advance" },
          wrong: {
            message: `괜찮아요. ${correct.replace(/^맞아요\. /, "")}`,
            reveal_answer: true,
            next: "advance",
          },
        },
      },
      screen: "study",
      /*
        **2지선다에는 보기가 둘이다.** 「잘 모르겠어요」까지 세 개를 띄우면
        2지선다가 아니게 된다. 그래도 적어서 내면 `escapeFrustration`이 받는다.
        정답이 늘 아래에 오지 않도록 문장마다 순서를 뒤집는다.
      */
      buttons:
        s.unitIndex % 2 === 0 ? [pair.wrong, pair.right] : [pair.right, pair.wrong],
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

/**
 * **체크리스트 유도 — 못 한 것 중 하나만.**
 *
 * 예전에는 1·2·3단 고정 사다리였다. 학생이 뭘 썼는지 보지 않아서, 절반을
 * 맞힌 학생에게도 이미 한 걸 또 시켰다. 이제는 낸 것에 체크하고 **아직 못 한
 * 것 중 첫 번째**(= 레슨에 적힌 순서 = 쉬운 순)만 짚는다.
 *
 * 같은 항목에서 또 막히면 그 항목만 `tell`로 알려 준다. 모범 해석 전체는
 * 여전히 좌절 방지(miss 4회)에서만 나온다.
 */
/**
 * 방금 낸 것을 **학생이 쓴 말 그대로** 인정한다.
 *
 * 예전에는 "좋아요, 그 부분은 맞았어요."였다. 학생은 어느 부분인지 모른다
 * (2026-09-06 실제 불평). 항목 설명을 대신 쓰면 아직 안 낸 답이 새어 나가므로,
 * **학생 자신이 쓴 말**을 되짚어 준다 — 이미 쓴 말이라 유출이 아니다.
 */
function acknowledge(
  s: EngineState,
  gained: number[],
  studentText?: string,
): string {
  if (!gained.length) return "";
  if (!studentText) return "좋아요, 지금 쓴 해석은 맞았어요. ";

  const keywords = (current(s).scoring_points ?? [])
    .filter((p) => gained.includes(p.id))
    .flatMap((p) => p.check ?? [])
    .filter((k) => studentText.includes(k))
    .sort((a, b) => b.length - a.length);

  const key = keywords[0];
  if (!key) return "좋아요, 지금 쓴 해석은 맞았어요. ";

  // 「기쁘」가 아니라 「기쁘게」로 되짚는다 — 학생이 쓴 낱말째로 잘라 준다
  const word = studentText.slice(studentText.indexOf(key)).split(/\s/)[0] ?? key;
  const quoted = word.length <= 12 ? word : key;
  return `「${quoted}」까지 잘 잡았어요. `;
}

function nudgeNext(
  s: EngineState,
  checked: number[],
  studentText?: string,
): EngineState {
  const miss = s.missCountInUnit + 1;
  if (miss >= 4) {
    return frustration({ ...s, checkedPoints: checked, missCountInUnit: miss, hadAnyError: true });
  }

  const points = current(s).scoring_points ?? [];
  /*
    **이미 답을 알려 준 항목은 건너뛴다.** 못 낸 것 중 첫 번째만 보면, 한 항목을
    알려 준 뒤에도 계속 그 항목이 걸려서 같은 `tell`이 반복된다 — 학생에게는
    말이 안 통하는 화면이다 (2026-09-06 탈레스 2번 문장에서 재현).
    남은 게 전부 알려 준 것뿐이면 그때는 그 항목을 다시 짚는다.
  */
  const target =
    points.find((p) => !checked.includes(p.id) && !s.toldPoints.includes(p.id)) ??
    points.find((p) => !checked.includes(p.id));
  if (!target) return s; // 전부 체크됐으면 부를 일이 없다

  const gained = checked.filter((id) => !s.checkedPoints.includes(id));
  const already = s.nudgedPoints.includes(target.id);
  const line = (already ? target.tell : target.nudge) ?? target.nudge ?? target.text;
  const lead = acknowledge(s, gained, studentText);

  return say(s, `${lead}${line}`, {
    checkedPoints: checked,
    missCountInUnit: miss,
    hadAnyError: true,
    nudgedPoints: already ? s.nudgedPoints : [...s.nudgedPoints, target.id],
    toldPoints: already && !s.toldPoints.includes(target.id)
      ? [...s.toldPoints, target.id]
      : s.toldPoints,
    toldAnyPoint: s.toldAnyPoint || already,
    errorIds:
      already && !s.errorIds.includes(`${s.unitIndex + 1}:점수${target.id}`)
        ? [...s.errorIds, `${s.unitIndex + 1}:점수${target.id}`]
        : s.errorIds,
    pending: null,
    screen: "study",
    buttons: [HINT_BTN, UNKNOWN_BTN],
    placeholder: "해석을 적어 보세요…",
    effect: null,
  });
}

/**
 * 이번 답을 체크리스트에 반영한다. 첫 시도는 따로 남긴다 — **유도 전에 스스로
 * 낸 것**만이 난이도의 근거가 되기 때문이다. 우리가 늘 1번을 먼저 유도하면
 * 1번 체크율이 올라가서, 유도 후 기록으로 난이도를 재면 편향이 생긴다.
 */
function withAttempt(s: EngineState, hit: number[]) {
  const checked = [...new Set([...s.checkedPoints, ...hit])];
  const first = s.attemptsInUnit === 0;
  return {
    checked,
    next: {
      ...s,
      // checkedPoints는 일부러 안 바꾼다. `nudgeNext`가 **이번 턴에 새로 낸 것**을
      // 알아야 맞힌 말을 되짚어 줄 수 있다
      attemptsInUnit: s.attemptsInUnit + 1,
      firstTryPoints: first ? hit : s.firstTryPoints,
    },
  };
}

function briefOf(s: EngineState): UnitBrief {
  const u = current(s);
  const points = u.scoring_points ?? [];
  const target = points.find((p) => !s.checkedPoints.includes(p.id));
  return {
    index: s.unitIndex,
    text: u.text,
    scoringPoints: points.map((p) => p.text),
    errorPriority: u.error_priority ?? [],
    checkedPoints: s.checkedPoints,
    /*
      **지금 유도해도 되는 것 하나만** 넘긴다. 나머지 항목의 `tell`이나 다음
      항목까지 보여 주고 "쓰지 마"라고 지시하면 언젠가 쓴다.
    */
    nextNudge: target?.nudge,
  };
}

/**
 * 이번 턴에 절대 나오면 안 되는 문자열 — 나오면 그 발화를 버린다.
 *
 * **채점 포인트의 한국어 쪽도 넣는다.** 모델에게 `scoring_points`를 주는 이유는
 * 판정하라고지 읊으라고가 아니다. 안 막으면 모범 해석을 피해 가면서
 * `serve → 근무하다` 같은 답을 그대로 흘린다 (2026-09-06 가짜 어댑터로 재현).
 *
 * **다만 학생이 이미 낸 항목은 뺀다.** 그건 더 이상 비밀이 아니고, 오히려
 * 「맞은 점을 먼저 구체적으로 인정한다」가 프레임의 규칙이다. 안 빼면 학생이
 * 「근무한」이라고 써 놓았는데 그걸 짚어 주는 말이 통째로 폐기된다
 * (2026-09-06 실제 대화에서 재현).
 */
function bannedFor(s: EngineState, checked = s.checkedPoints): string[] {
  const u = current(s);
  const points = u.scoring_points ?? [];
  const done = points.filter((p) => checked.includes(p.id));
  /** 이미 낸 항목의 설명문 — 여기 들어 있는 말은 금지에서 뺀다 */
  const revealed = done.map((p) => p.text).join(" ");

  const correctChoices = (u.expected_errors ?? []).flatMap((e) =>
    [...(e.treatment?.choices ?? []), ...(e.rounds?.[0]?.choices ?? [])]
      .filter((c) => c.correct)
      .map((c) => c.label),
  );
  const lockedTells = points
    .filter((p) => !s.toldPoints.includes(p.id) && !checked.includes(p.id))
    .flatMap((p) => (p.tell ? [p.tell] : []));
  // "It has been a privilege to ~ → '~할 수 있어서 영광이었다'" 에서 화살표 뒤쪽
  const scoringAnswers = points
    .filter((p) => !checked.includes(p.id))
    .flatMap((p) => {
      const tail = p.text.split("→").slice(1).join("→").trim();
      const cleaned = tail.replace(/^['"“”‘’]|['"“”‘’]$/g, "").trim();
      return cleaned ? [cleaned] : [];
    });

  /*
    긴 문장만 막으면 모델이 **짧게 줄여서** 흘린다. 레슨에서 답은 따옴표 안에
    적혀 있으므로(`privilege는 여기서 '영광'이에요`), 아직 못 낸 항목의 따옴표
    안쪽을 따로 뽑아 막는다 (2026-09-06 재현: 「privilege는 '영광'이에요」가
    통과했다).
  */
  const quotedAnswers = points
    .filter((p) => !checked.includes(p.id))
    .flatMap((p) => [...`${p.text} ${p.tell ?? ""}`.matchAll(/['‘’"“”]([^'‘’"“”]{2,})['‘’"“”]/g)])
    .map((m) => m[1]!.trim())
    .filter((word) => word && !word.startsWith("~"));

  return [
    u.model_translation,
    ...correctChoices,
    ...lockedTells,
    ...scoringAnswers,
    ...quotedAnswers,
  ].filter((banned) => banned && !revealed.includes(banned));
}

/**
 * 모델 발화에 거는 검사 기준.
 *
 * 금지 문자열뿐 아니라 **말투 규칙까지** 함께 넘긴다. 기준값은 `frame.json`에서
 * 오고, 직전 대사를 같이 줘서 같은 말을 두 번 하지 못하게 한다.
 */
function voiceGuardFor(
  s: EngineState,
  checked = s.checkedPoints,
  studentText?: string,
): GuardContext {
  return {
    bannedStrings: bannedFor(s, checked),
    minSentences: frame.speech.min_sentences,
    previousUtterance: s.lastTutorUtterance,
    // 학생이 쓰지 않은 해석을 부정하지 못하게 원문을 같이 넘긴다
    studentText,
  };
}

/**
 * **단어 뜻 질문.**
 *
 * 「serve가 뭐예요?」는 무시할 질문이 아니다. 다만 답이 두 갈래다.
 *
 * - **이번 문장에서 가르치는 단어**(채점 포인트·예상 오류가 겨냥하는 단어)면
 *   뜻이 곧 정답이다. 그냥 알려 주면 학생은 다음부터 해석 대신 단어부터
 *   물어보고, 유도에 옆문이 생긴다. 그래서 **그 항목 유도로 답한다** —
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
  if (isTaughtWord(word, current(s))) return nudgeNext(s, s.checkedPoints);

  const llm = getTutorLlm();
  if (!llm) return nudgeNext(s, s.checkedPoints);

  const spoken = await safeCall(() =>
    llm.speak({
      action: "ANSWER_WORD",
      askedWord: word,
      studentText,
      unit: briefOf(s),
      state: {
        unitIndex: s.unitIndex,
        missCountInUnit: s.missCountInUnit,
        lastTutorUtterance: s.lastTutorUtterance,
      },
    }),
  );
  if (!spoken) return nudgeNext(s, s.checkedPoints);

  /*
    **검사는 학생이 실제로 보는 문장에 건다.** 엔진이 복귀 문구를 뒤에 붙이므로,
    모델 발화만 따로 재면 문장 수도 물음표 수도 실제와 다르다.
  */
  const message = `${spoken.message} ${frame.fixed_lines.return_to_lesson}`;
  const verdict = validateLlmOutput(
    { ...spoken, message },
    voiceGuardFor(s, s.checkedPoints, studentText),
  );
  if (!verdict.ok) {
    console.warn("[tutor] 단어 뜻 발화 폐기 →", verdict.reason);
    return nudgeNext(s, s.checkedPoints);
  }

  // 물어본 것은 오답이 아니다 — miss도 유도 단계도 그대로다
  return say(s, message, { effect: null });
}

/**
 * **D(예상 밖) · B(부분 정답) — 모델이 열리는 유일한 자리.**
 *
 * 어댑터가 없으면 여기서 하는 일은 `nudgeNext`와 똑같다. 즉 지금 데모의 동작이
 * 그대로 남는다. 어댑터가 있어도 다음은 코드가 쥔다:
 * - miss 카운트와 좌절 임계(4번째)는 모델을 부르기 **전에** 코드가 판단한다
 * - 가드레일에 걸리면 발화를 버리고 코드의 항목 유도로 폴백한다
 * - `effect: "light"`는 스스로 고친 순간만이므로 여기서는 절대 켜지 않는다
 */
async function treatUnexpectedOrPartial(
  s: EngineState,
  text: string,
  checked: number[] = s.checkedPoints,
): Promise<EngineState> {
  const llm = getTutorLlm();
  if (!llm) return nudgeNext(s, checked, text);

  const miss = s.missCountInUnit + 1;
  if (miss >= 4) {
    return frustration({ ...s, missCountInUnit: miss, hadAnyError: true });
  }

  /*
    **두 콜을 동시에 보낸다.** 직렬로 붙이면 판정(약 3초) + 발화(약 4초) = 7초를
    학생이 기다린다. 발화는 판정 결과가 없어도 만들 수 있다 — 체크리스트와 학생
    답을 같이 주면 맞은 부분은 모델이 알아서 인정한다. 판정은 **체크 상태를
    갱신**하는 데 쓰이므로, 도착한 뒤에 반영해도 늦지 않다.

    판정이 먼저다. 모델이 "전부 채웠다"고 보면 발화는 버리고 다음 문장으로 넘긴다
    (유도할 게 없는데 유도하는 말이 나가면 안 된다).

    키워드가 하나라도 잡았으면 판정 콜을 아예 안 부른다. 그때는 부분 정답이라는
    게 이미 확실해서 다음 할 일이 안 바뀐다 — 콜 하나와 비용 3할이 빠진다.
  */
  const unit = briefOf(s);
  const judging =
    llm.judge && checked.length === 0
      ? safeCall(() => llm.judge!({ studentText: text, unit }))
      : Promise.resolve(null);

  const speaking = safeCall(() =>
    llm.speak({
      action: checked.length > 0 ? "TREAT_PARTIAL" : "TREAT_UNEXPECTED",
      studentText: text,
      unit,
      state: {
        unitIndex: s.unitIndex,
        missCountInUnit: s.missCountInUnit,
        lastTutorUtterance: s.lastTutorUtterance,
      },
    }),
  );

  const [judged, spoken] = await Promise.all([judging, speaking]);

  const known = (current(s).scoring_points ?? []).map((p) => p.id);
  const merged = [
    ...new Set([
      ...checked,
      ...(judged?.checkedPoints ?? []).filter((id) => known.includes(id)),
    ]),
  ];

  // 모델 덕분에 전부 채워졌으면 발화를 버리고 정답으로 넘긴다
  const points = current(s).scoring_points ?? [];
  if (points.length && points.every((p) => merged.includes(p.id))) {
    return advance({ ...s, checkedPoints: merged }, praiseFor(s), s.hadAnyError);
  }

  if (!spoken) return nudgeNext(s, merged, text);

  const verdict = validateLlmOutput(spoken, voiceGuardFor(s, merged, text));
  if (!verdict.ok) {
    console.warn("[tutor] 발화 폐기 →", verdict.reason);
    return nudgeNext(s, merged, text);
  }

  return say(s, spoken.message, {
    checkedPoints: merged,
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

  /*
    **「왜요?」는 오답이 아니다.** 레슨이 원리 설명을 여기 적어 둔 이유가 그것이다 —
    묻기 전에 설명하면 강의가 되고, 물었는데 안 해 주면 답답해진다.
    miss도 안 세고 2지선다도 그대로 둔다.
  */
  if (pending.onWhy && askedWhy(text)) {
    return say(s, pending.onWhy, { effect: null });
  }

  if (isUnknownInput(text)) {
    if (pending.errorId === "FRUSTRATION") {
      return advance(
        { ...s, pending: null, skipFinalRetake: true },
        "괜찮아요, 방금 같이 본 그 문장이에요.",
        false,
      );
    }
    return nudgeNext({ ...s, pending: null }, s.checkedPoints);
  }
  /*
    **좌절 방지 뒤에는 학생을 붙잡아 두지 않는다.**
    선택지 밖의 답이 와도 다음 문장으로 넘긴다. 예전에는 여기서 `climbHint`로
    갔는데, miss가 이미 4라 좌절 방지가 다시 열리고 → 또 못 맞히고 → 무한히
    같은 문장에 갇혔다 (2026-09-06 재현: 「네」라고 답하니 수업이 안 끝났다).
  */
  /*
    좌절 방지를 빠져나갈 때, 이 문장에 `teach_points`가 있으면 **설명 국면**으로
    간다. 답을 알려 준 학생이 바로 다음 문장으로 떠밀리지 않게 하는 자리다.
  */
  const escapeFrustration = (state: EngineState) => {
    const next = { ...state, pending: null, skipFinalRetake: true };
    return (current(state).teach_points ?? []).length
      ? teachStep(next, 0)
      : advance(next, "괜찮아요, 방금 같이 본 그 문장이에요.", false);
  };

  const byLabel = matchChoice(text, pending.choices.map((c) => c.label));
  const choice =
    pending.choices.find((c) => c.label === byLabel || compactEq(text, c.id)) ??
    pending.choices.find((c) => byLabel === c.label);
  if (!choice) {
    /*
      **선택지를 무시하고 고친 답을 바로 적는 학생이 많다.** 버튼을 누르는 대신
      해석을 다시 쓰는 게 자연스럽기 때문이다. 정답이면 정답으로 받는다 —
      예전에는 「선택지 밖」으로 보고 힌트를 올려서, 스스로 고쳐 놓고도 오답
      취급을 받았다.

      `effect: "light"`는 **스스로** 고친 순간만이다. 좌절 방지로 정답을 이미
      알려 준 뒤라면 켜지 않는다.
    */
    const retry = classify(text, current(s));
    if (retry.kind === "points") {
      const checked = [...new Set([...s.checkedPoints, ...retry.hit])];
      const points = current(s).scoring_points ?? [];
      if (points.length && points.every((p) => checked.includes(p.id))) {
        return advance(
          { ...s, pending: null, checkedPoints: checked },
          praiseFor(s),
          !s.skipFinalRetake,
        );
      }
    }
    return pending.errorId === "FRUSTRATION"
      ? escapeFrustration(s)
      : nudgeNext({ ...s, pending: null }, s.checkedPoints);
  }
  const branch = pending.on_choice[choice.id];
  if (!branch) {
    return pending.errorId === "FRUSTRATION"
      ? escapeFrustration(s)
      : nudgeNext({ ...s, pending: null }, s.checkedPoints);
  }
  if (pending.errorId === "FRUSTRATION" || branch.next === "advance") {
    const next = { ...s, pending: null, skipFinalRetake: true, result: "설명제공" as const };
    return (current(s).teach_points ?? []).length
      ? say(teachStep(next, 0), `${branch.message} ${(current(s).teach_points ?? [])[0]!.message}`)
      : advance(next, branch.message, false);
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
export function createSession(lessonId?: string | null, learnerName?: string | null) {
  const lesson = getLesson(lessonId);
  let s = initialState(lesson, learnerName?.trim() || null);
  return {
    view: () => view(s),
    async submit(raw: string) {
      const text = raw.trim();
      if (!text || s.ended) return view(s);
      s = { ...s, studentLine: text, effect: null };

      /*
        **이름이 먼저다.** 아직 인사 중이면 이 말은 해석 시도가 아니라 이름이다.
        아래 어떤 판정에도 넣지 않는다.
      */
      if (s.stage === "greeting") {
        s = enterIntro(s, parseName(text));
        return view(s);
      }

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

      // 설명 국면이 열려 있으면 그 흐름이 먼저다
      if (s.teaching != null) {
        s = handleTeaching(s, text);
        return view(s);
      }

      if (s.pending) {
        /*
          선택지 없이 **설명만 걸려 있는** pending이 있다 (1회차 교정 + 「왜요?」).
          그건 답을 기다리는 게 아니라 물어볼 기회를 열어 둔 것이므로, 「왜요?」가
          아니면 보통 흐름으로 흘려보낸다. 안 그러면 다시 시도한 해석이
          「선택지 밖 답」으로 처리된다.
        */
        if (s.pending.choices.length || askedWhy(text)) {
          s = handlePending(s, text);
          return view(s);
        }
        s = { ...s, pending: null };
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

      if (verdict.kind === "C") {
        s = openBranch(s, verdict.errorId);
        return view(s);
      }

      /*
        **E와 D를 섞으면 안 된다.** 「잘 모르겠어요」는 해석 시도가 아니므로
        체크할 것도 없다. 코드가 다음 항목을 유도한다 — 모델을 부르지 않는다.
      */
      if (isUnknownInput(text)) {
        s = nudgeNext(s, s.checkedPoints);
        return view(s);
      }

      // 해석 시도 — 체크리스트에 반영한다
      const attempt = withAttempt(s, verdict.hit);
      s = attempt.next;
      const points = current(s).scoring_points ?? [];
      if (points.length && points.every((p) => attempt.checked.includes(p.id))) {
        s = advance({ ...s, checkedPoints: attempt.checked }, praiseFor(s), s.hadAnyError);
        return view(s);
      }

      /*
        못 한 항목이 남았다 = 부분 정답(B)이거나 예상 밖(D)이다.
        모델이 있으면 맞은 것을 인정하며 말하게 하고, 없으면 코드가 다음 항목
        하나를 유도한다.
      */
      s = await treatUnexpectedOrPartial(s, text, attempt.checked);
      return view(s);
    },
    /** 항목별 학습 기록. 수업이 끝날 때 서버로 보낸다 */
    records: () => s.pointLog,
    lessonId: () => s.lesson.id,
    /** 이번 수업에서 부르기로 한 이름. 앱이 받아서 저장한다 */
    learnerName: () => s.learnerName,
    reset() {
      // 이름은 들고 간다 — 「다시 시작」마다 이름을 다시 묻지 않는다
      s = initialState(lesson, s.learnerName);
      return view(s);
    },
  };
}

export type TutorSession = ReturnType<typeof createSession>;
