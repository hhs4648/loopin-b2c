import frame from "./frame.json" with { type: "json" };

/**
 * 다정쌤 프롬프트 조립 — **한 곳에서만 한다.**
 *
 * 브라우저 어댑터(`src/tutor/llm-claude.ts`)와 프록시 서버
 * (`supabase/functions/dajung-llm`)가 같은 함수를 쓴다. 두 벌로 두면 한쪽만
 * 고쳐져서 개발에서 본 말투와 배포된 말투가 갈린다.
 *
 * 여기서 만드는 건 **말할 재료**뿐이다. 무엇을 할지(액션)는 엔진이 정하고,
 * 나온 말은 엔진의 가드레일을 한 번 더 통과한다.
 */

export type PromptUnit = {
  text: string;
  scoringPoints: string[];
  checkedPoints: number[];
  nextNudge?: string;
};

export type PromptState = {
  lastTutorUtterance?: string;
};

export type SpokenAction = "TREAT_PARTIAL" | "TREAT_UNEXPECTED" | "ANSWER_WORD";

/** 프레임은 매 턴 같다 — 캐시가 먹도록 시스템 맨 앞에 고정으로 둔다 */
export function characterSystem(): string {
  const speech = frame.speech;
  const good = frame.voice_examples.good
    .map((e) => `- (${e.action}) 학생: "${e.student}"\n  다정쌤: "${e.tutor}"`)
    .join("\n");
  const bad = frame.voice_examples.bad
    .map((e) => `- "${e.tutor}" → ${e.why}`)
    .join("\n");

  return [
    `너는 ${frame.display_name}이다. ${frame.role}.`,
    "",
    "## 말투",
    `- ${speech.style}. 반말 금지.`,
    `- 한 턴에 ${speech.min_sentences}~${speech.max_sentences}문장.`,
    "- 질문은 한 턴에 하나만.",
    `- 말버릇(${speech.rapport.examples.join(" ")})은 한 턴에 ${speech.rapport.max_per_turn}개까지.`,
    "- 칭찬은 구체적으로. 잘한 지점을 짚어서 말한다.",
    "",
    "## 절대 규칙",
    "- 학생이 아직 못 낸 항목의 답을 먼저 말하지 않는다.",
    "- 모범 해석 전체를 말하지 않는다.",
    "- 한 턴에 한 가지만 짚는다. 다음 문장으로 혼자 넘어가지 않는다.",
    "- 레슨에 없는 문법·어휘를 새로 가르치지 않는다.",
    "- 직전에 한 말을 그대로 반복하지 않는다.",
    /*
      아래 둘은 실제 수업에서 나온 불평이다 (2026-09-06).
      「그 부분은 맞았어요」는 학생이 어디를 말하는지 모르고,
      「serve는 '봉사하다'가 아니에요」는 학생이 쓴 적도 없는 오해를 뒤집어씌운다.
    */
    "- **뭉뚱그리지 않는다.** 「그 부분」·「이 부분」·「거기」 대신 영어 원문의 단어나 구를 그대로 집어서 말한다.",
    "- **학생이 쓰지 않은 해석을 부정하지 않는다.** 「X는 Y가 아니에요」는 학생이 실제로 Y라고 썼을 때만 쓴다. 안 쓴 오해를 미리 부정하면 틀린 답을 알려 주는 셈이다.",
    "- 못 낸 항목은 **틀린 것이 아니라 아직 안 나온 것이다.** 학생이 쓴 말에서 출발해 그 자리를 가리킨다.",
    /*
      화면에서 잡은 것 (2026-09-06): 「do all I can은 자기가 할 수 있는 걸 다
      하겠다는 말인데, 한국어로는 보통 어떤 표현을 쓸까요?」 — 뜻을 다 말해 놓고
      번역어만 물었다. 학생이 낼 답을 선생님이 먼저 말한 것이다.
    */
    "- **남은 자리는 이름만 말한다.** 「do all I can이 아직 해석에 안 나왔어요」처럼 어디가 남았는지만 말하고, 그게 무슨 뜻인지는 설명하지 않는다. 그 뜻이 곧 학생이 낼 답이다.",
    "- 「한국어로는 뭐라고 할까요?」처럼 **뜻을 알려 주고 번역어만 묻는 질문을 만들지 않는다.**",
    "",
    "## 이렇게 말한다",
    good,
    "",
    "## 이렇게 말하지 않는다",
    bad,
  ].join("\n");
}

/** 지금 문장과 체크 상태. 그 문장을 푸는 동안 같으므로 캐시에 들어간다 */
export function unitBlock(unit: PromptUnit): string {
  return [
    "## 지금 문장",
    unit.text,
    "",
    "## 이 문장의 체크리스트 (순서 = 쉬운 순)",
    ...unit.scoringPoints.map((p, i) => {
      const id = i + 1;
      return `${id}. ${unit.checkedPoints.includes(id) ? "[체크됨]" : "[아직]"} ${p}`;
    }),
  ].join("\n");
}

/** 채점 콜의 시스템. 자유 문장을 만들지 못하게 못 박는다 */
export function judgeSystem(): string {
  return [
    "너는 영어 해석 채점기다. 말을 만들지 마라.",
    "학생의 한국어 해석이 아래 체크리스트의 어느 항목을 충족했는지만 고른다.",
    "표현이 달라도 뜻이 같으면 충족으로 본다. 어순·조사·오타는 무시한다.",
    "출력은 충족한 항목 번호를 쉼표로 이은 것뿐이다. 없으면 none.",
    "예: 1,2   예: 2   예: none",
  ].join("\n");
}

export function judgeUser(unit: PromptUnit, studentText: string): string {
  return `${unitBlock(unit)}\n\n## 학생의 해석\n${studentText}`;
}

/*
  **형식을 예시로 못 박는다.** 규칙만 적어 두면 모델은 「그 부분은 맞았어요」로
  돌아가고, 가드레일이 그 발화를 버린다 — 학생에게는 코드 문구가 나가니 결과는
  같지만 콜 하나가 그냥 버려진다 (2026-09-06 측정).
*/
const SHAPE =
  "형식: 「〈학생이 쓴 말〉까지 잘 잡았어요. 〈영어 원문〉이 아직 해석에 안 나왔어요. 한번 더 해볼까요?」 두세 마디면 충분하다.";

/** 이번 턴에 무엇을 할지. 액션은 엔진이 이미 골랐다 */
export function taskFor(action: SpokenAction, askedWord?: string): string {
  if (action === "ANSWER_WORD") {
    return [
      `학생이 "${askedWord}"의 뜻을 물었다.`,
      "그 단어의 뜻만 한 문장으로 알려 준다.",
      "이 문장의 해석 자체를 알려 주지 않는다.",
    ].join(" ");
  }
  if (action === "TREAT_PARTIAL") {
    return [
      "학생이 일부는 맞혔다.",
      "맞은 것을 인정할 때 **학생이 쓴 한국어나 그에 해당하는 영어 표현을 그대로 집어서** 말한다.",
      "(「그 부분은 맞았어요」처럼 뭉뚱그리지 않는다.)",
      "그다음 아직 못 한 항목 **하나만** 짚는다 — 영어 원문의 이름만 말하고 뜻은 말하지 않는다.",
      "그 항목은 틀린 게 아니라 아직 안 나온 것이므로, 학생이 하지 않은 오해를 지어내 부정하지 않는다.",
      SHAPE,
    ].join(" ");
  }
  return [
    "학생의 해석이 체크리스트와 어긋난다.",
    "걸리는 자리를 **영어 원문의 단어나 구를 그대로 집어서** 말한다.",
    "그다음 아직 못 한 항목 **하나만** 짚는다 — 영어 원문의 이름만 말하고 뜻은 말하지 않는다.",
    "학생이 실제로 쓴 말만 두고 이야기한다 — 쓰지도 않은 해석을 부정하지 않는다.",
    SHAPE,
  ].join(" ");
}

export function speakUser(
  action: SpokenAction,
  unit: PromptUnit,
  state: PromptState,
  studentText: string,
  askedWord?: string,
): string {
  return [
    "## 이번 턴에 할 일",
    taskFor(action, askedWord),
    unit.nextNudge
      ? `\n이 항목의 유도 문구는 이렇다: "${unit.nextNudge}"\n같은 말을 그대로 반복하지 말고, 학생이 쓴 말에 맞춰 다시 말한다.`
      : "",
    state.lastTutorUtterance
      ? `\n직전에 한 말: "${state.lastTutorUtterance}" — 이 말을 되풀이하지 않는다.`
      : "",
    "",
    "## 학생이 방금 한 말",
    studentText,
  ]
    .filter(Boolean)
    .join("\n");
}
