/**
 * LLM을 붙일 자리.
 *
 * 엔진이 액션을 고르고, 모델은 **그 액션의 말만** 만든다. 모델이 열 수 있는 문은
 * 두 개뿐이다 — **D(예상 밖 해석)** 과 **B(부분 정답)**.
 *
 * 코드에 남는 것(모델에 절대 넘기지 않는 것):
 * - C 예상 오류(P2/P3) 고정 대사
 * - E 「잘 모르겠어요」 힌트 사다리 1→2→3
 * - miss 카운트와 좌절 방지 임계
 * - 다음 unit으로 넘어갈지
 *
 * 어댑터가 등록돼 있지 않으면 엔진은 **지금 데모와 완전히 같이** 동작한다
 * (D도 힌트 사다리로 접힌다). 그래서 이 파일이 들어와도 화면 동작은 안 바뀐다.
 */

/** 엔진이 고르는 이번 턴 액션. 모델은 이걸 고르지 않는다. */
export type TutorAction =
  | "INTRO"
  | "ASK_TRANSLATION"
  | "PRAISE_AND_ADVANCE"
  | "TREAT_EXPECTED"
  | "TREAT_PARTIAL"
  | "TREAT_UNEXPECTED"
  | "ANSWER_WORD"
  | "HINT_1"
  | "HINT_2"
  | "HINT_3"
  | "FRUSTRATION_EXPLAIN"
  | "DONE";

/**
 * 모델이 말을 만들어도 되는 액션 — 이 셋뿐이다.
 *
 * `ANSWER_WORD`는 **이번 문장에서 가르치지 않는 단어**의 뜻을 묻는 질문에만
 * 열린다. 가르치는 단어(채점 포인트)는 코드가 힌트 사다리로 답한다 — 그 뜻이
 * 곧 이 문장의 정답이라서다.
 */
export type SpokenAction = "TREAT_PARTIAL" | "TREAT_UNEXPECTED" | "ANSWER_WORD";

/**
 * 모델에게 넘기는 **현재 unit만**. 편지 전체를 매 턴 넣지 않는다.
 *
 * `hintLadderVisible`은 지금 허용된 단까지 **잘라서** 넘긴다. "3단은 쓰지 마"라고
 * 지시하는 대신 물리적으로 안 보이게 하는 쪽이 확실하다.
 */
export type UnitBrief = {
  index: number;
  text: string;
  scoringPoints: string[];
  errorPriority: string[];
  hintLadderVisible: string[];
};

export type SessionBrief = {
  unitIndex: number;
  hintRung: number;
  missCountInUnit: number;
  /** 같은 말을 두 번 하지 않게 */
  lastTutorUtterance: string;
};

export type JudgeInput = {
  studentText: string;
  unit: UnitBrief;
};

/**
 * 판정 콜(콜 1). **A와 C는 코드가 이미 정했다** — 모델은 B와 D만 가른다.
 * 그래서 모델이 오답을 정답으로 뒤집을 길이 없다(`never_mark_correct`도 자동으로 안전).
 */
export type JudgeResult = {
  diagnosis: "B" | "D";
  matchedPoints?: string[];
  confidence?: number;
};

export type SpeakInput = {
  action: SpokenAction;
  studentText: string;
  /** `ANSWER_WORD`일 때 학생이 물어본 단어 */
  askedWord?: string;
  unit: UnitBrief;
  state: SessionBrief;
  matchedPoints?: string[];
};

/** 발화 콜(콜 2)의 출력. `effect`는 엔진이 정한다 — 모델이 켜지 못한다. */
export type SpeakResult = {
  message: string;
  buttons?: string[];
};

export type TutorLlm = {
  /** 없으면 전부 D로 본다 (부분 정답 판정을 안 하는 것뿐, 동작은 안전한 쪽) */
  judge?: (input: JudgeInput) => Promise<JudgeResult | null>;
  speak: (input: SpeakInput) => Promise<SpeakResult | null>;
};

let adapter: TutorLlm | null = null;

/** 앱 진입점에서 한 번 꽂는다. 안 꽂으면 엔진은 코드만으로 돈다. */
export function setTutorLlm(next: TutorLlm | null): void {
  adapter = next;
}

export function getTutorLlm(): TutorLlm | null {
  return adapter;
}

/**
 * 모델 호출은 **실패해도 수업이 멈추면 안 된다.**
 * 던지거나 늦으면 `null`을 주고, 엔진은 힌트 사다리로 폴백한다.
 */
export async function safeCall<T>(
  run: () => Promise<T | null>,
  timeoutMs = 6000,
): Promise<T | null> {
  try {
    return await Promise.race([
      run(),
      new Promise<null>((resolve) => setTimeout(() => resolve(null), timeoutMs)),
    ]);
  } catch (error) {
    console.warn("[tutor] LLM 호출 실패", error);
    return null;
  }
}

export type GuardContext = {
  /** 모범 해석, 정답 선택지 라벨, 아직 못 쓰는 힌트 단 */
  bannedStrings: string[];
  maxSentences?: number;
  maxQuestions?: number;
};

export type GuardVerdict = { ok: true } | { ok: false; reason: string };

function compact(s: string): string {
  return s.toLowerCase().replace(/[“”"'’.,!?~\-·…\s]/g, "");
}

function sentencesOf(message: string): string[] {
  return message
    .split(/(?<=[.!?？！…])\s+|\n+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

/**
 * 반말 감지 — **보수적으로** 본다.
 *
 * 오탐이 나면 정상 발화가 버려지고 힌트로 폴백해서 수업이 딱딱해진다. 그래서
 * 해요체·합쇼체 어미로 끝나면 무조건 통과시키고, 명백한 반말 어미만 잡는다.
 */
function looksBanmal(sentence: string): boolean {
  const body = sentence.replace(/[.!?？！…~\s]+$/, "");
  if (!body) return false;
  if (/(요|죠|까|용|니다|습니다)$/.test(body)) return false;
  /*
    해요체는 예외 없이 `요`(또는 죠·용)로, 합쇼체는 `니다`·`습니까`로 끝난다.
    그래서 위를 통과한 뒤 아래 어미로 끝나면 반말로 본다. 명사로 끝나는 문장까지
    잡지 않으려고 `지`·`데`·`가`처럼 명사 끝에도 흔한 글자는 일부러 뺐다.
  */
  return /(야|해|봐|와|줘|자|니|냐|래|거든|잖아|었어|았어|겠어|이야|이지|구나|어|아)$/.test(
    body,
  );
}

/**
 * 모든 발화 콜의 출력에 **예외 없이** 통과시킨다.
 * 액션별로 골라 검사하면 빠뜨리는 자리가 생긴다.
 */
export function validateLlmOutput(
  output: SpeakResult,
  ctx: GuardContext,
): GuardVerdict {
  const message = output.message?.trim() ?? "";
  if (!message) return { ok: false, reason: "빈 발화" };

  const haystack = compact(message);
  for (const banned of ctx.bannedStrings) {
    const needle = compact(banned);
    if (needle.length >= 4 && haystack.includes(needle)) {
      return { ok: false, reason: `정답 선공개: "${banned}"` };
    }
  }

  // 정답을 빠른 대답 버튼에 미리 띄우는 것도 선공개다
  for (const button of output.buttons ?? []) {
    const label = compact(button);
    for (const banned of ctx.bannedStrings) {
      const needle = compact(banned);
      if (needle.length >= 4 && label.includes(needle)) {
        return { ok: false, reason: `정답이 버튼에 노출: "${button}"` };
      }
    }
  }

  const sentences = sentencesOf(message);
  const maxSentences = ctx.maxSentences ?? 4;
  if (sentences.length > maxSentences) {
    return { ok: false, reason: `문장 ${sentences.length}개 (최대 ${maxSentences})` };
  }

  const questions = (message.match(/[?？]/g) ?? []).length;
  const maxQuestions = ctx.maxQuestions ?? 1;
  if (questions > maxQuestions) {
    return { ok: false, reason: `한 턴에 질문 ${questions}개` };
  }

  const banmal = sentences.find(looksBanmal);
  if (banmal) return { ok: false, reason: `반말: "${banmal}"` };

  return { ok: true };
}
