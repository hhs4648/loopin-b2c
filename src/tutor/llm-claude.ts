import Anthropic from "@anthropic-ai/sdk";
import frame from "../../content/tutor/frame.json";
import type { JudgeInput, SpeakInput, TutorLlm, UnitBrief } from "./llm";

/**
 * 진짜 Claude 어댑터.
 *
 * **콜을 둘로 나눈다.**
 * - 콜 1 `judge` — 체크리스트를 의미로 한 번 더 본다. 라벨(숫자)만 낸다
 * - 콜 2 `speak` — 그 액션의 말만 만든다. 캐릭터는 여기에만 있다
 *
 * 채점과 발화를 한 콜에 섞지 않는다. 같은 모델이 "정확히 채점하기"와 "다정하게
 * 말하기"를 동시에 하면 애매한 답에서 채점이 말투에 묻힌다.
 *
 * ⚠️ **개발 전용.** 브라우저에서 직접 부르므로 키가 번들에 실린다.
 * 배포 전에는 프록시 서버로 옮기고, 이 파일은 그 서버를 부르게 고친다.
 */

const MODEL = "claude-opus-5";

/** 프레임은 매 턴 같다 — 캐시가 먹도록 시스템 맨 앞에 고정으로 둔다 */
function characterSystem(): string {
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
    `- 질문은 한 턴에 하나만.`,
    `- 말버릇(${frame.speech.rapport.examples.join(" ")})은 한 턴에 ${speech.rapport.max_per_turn}개까지.`,
    `- 칭찬은 구체적으로. 잘한 지점을 짚어서 말한다.`,
    "",
    "## 절대 규칙",
    "- 학생이 아직 못 낸 항목의 답을 먼저 말하지 않는다.",
    "- 모범 해석 전체를 말하지 않는다.",
    "- 한 턴에 한 가지만 짚는다. 다음 문장으로 혼자 넘어가지 않는다.",
    "- 레슨에 없는 문법·어휘를 새로 가르치지 않는다.",
    "- 직전에 한 말을 그대로 반복하지 않는다.",
    "",
    "## 이렇게 말한다",
    good,
    "",
    "## 이렇게 말하지 않는다",
    bad,
  ].join("\n");
}

/** 이번 턴에만 달라지는 부분 — 캐시 경계 뒤에 온다 */
function unitBlock(unit: UnitBrief): string {
  return [
    "## 지금 문장",
    unit.text,
    "",
    "## 이 문장의 체크리스트 (순서 = 쉬운 순)",
    ...unit.scoringPoints.map((p, i) => {
      const id = i + 1;
      const done = unit.checkedPoints.includes(id) ? "[체크됨]" : "[아직]";
      return `${id}. ${done} ${p}`;
    }),
  ].join("\n");
}

function textOf(message: Anthropic.Message): string {
  return message.content
    .filter((b): b is Anthropic.TextBlock => b.type === "text")
    .map((b) => b.text)
    .join("\n")
    .trim();
}

export type ClaudeAdapterOptions = {
  apiKey: string;
  model?: string;
  /** 호출마다 토큰·지연을 보고 싶을 때 */
  onUsage?: (info: {
    call: "judge" | "speak";
    inputTokens: number;
    outputTokens: number;
    cachedTokens: number;
    ms: number;
  }) => void;
};

export function createClaudeTutorLlm(options: ClaudeAdapterOptions): TutorLlm {
  const client = new Anthropic({
    apiKey: options.apiKey,
    // 개발 전용. 프록시로 옮기면 이 줄이 사라진다
    dangerouslyAllowBrowser: true,
  });
  const model = options.model ?? MODEL;

  async function call(
    which: "judge" | "speak",
    system: Anthropic.TextBlockParam[],
    userText: string,
    maxTokens: number,
    effort: "low" | "medium",
  ): Promise<string | null> {
    const started = Date.now();
    const message = await client.messages.create({
      model,
      max_tokens: maxTokens,
      system,
      output_config: { effort },
      messages: [{ role: "user", content: userText }],
    });
    options.onUsage?.({
      call: which,
      inputTokens: message.usage.input_tokens,
      outputTokens: message.usage.output_tokens,
      cachedTokens: message.usage.cache_read_input_tokens ?? 0,
      ms: Date.now() - started,
    });
    /*
      거절은 예외가 아니라 200으로 온다. `content`를 읽기 전에 확인한다.
      학생 해석 교정에서 나올 일은 거의 없지만, 나오면 조용히 이상한 말을
      하는 대신 없는 셈 치고 코드 유도로 폴백한다.
    */
    if (message.stop_reason === "refusal") return null;
    return textOf(message) || null;
  }

  return {
    /*
      **콜 1 — 채점만.** 자유 문장을 만들지 않는다. 숫자만 받으므로 파싱이
      안정적이고, 틀려도 "항목 하나 더 체크" 이상은 못 한다.
    */
    async judge({ studentText, unit }: JudgeInput) {
      const system: Anthropic.TextBlockParam[] = [
        {
          type: "text",
          text: [
            "너는 영어 해석 채점기다. 말을 만들지 마라.",
            "학생의 한국어 해석이 아래 체크리스트의 어느 항목을 충족했는지만 고른다.",
            "표현이 달라도 뜻이 같으면 충족으로 본다. 어순·조사·오타는 무시한다.",
            "출력은 충족한 항목 번호를 쉼표로 이은 것뿐이다. 없으면 none.",
            "예: 1,2   예: 2   예: none",
          ].join("\n"),
        },
      ];
      const answer = await call(
        "judge",
        system,
        `${unitBlock(unit)}\n\n## 학생의 해석\n${studentText}`,
        64,
        "low",
      );
      if (!answer) return null;
      const ids = (answer.match(/\d+/g) ?? []).map(Number);
      return { checkedPoints: [...new Set(ids)] };
    },

    /*
      **콜 2 — 말만.** 무엇을 할지는 엔진이 이미 정했다. 여기서 단계를 고르거나
      다음 문장으로 넘기지 않는다. 나온 말은 엔진의 가드레일을 한 번 더 통과해야
      학생에게 간다.
    */
    async speak(input: SpeakInput) {
      const { action, studentText, unit, state, askedWord } = input;
      const task =
        action === "ANSWER_WORD"
          ? [
              `학생이 "${askedWord}"의 뜻을 물었다.`,
              "그 단어의 뜻만 한 문장으로 알려 준다.",
              "이 문장의 해석 자체를 알려 주지 않는다.",
            ].join(" ")
          : action === "TREAT_PARTIAL"
            ? [
                "학생이 일부는 맞혔다.",
                "맞은 부분을 먼저 짧게 인정하고,",
                "아직 못 한 항목 **하나만** 스스로 찾도록 유도한다.",
              ].join(" ")
            : [
                "학생의 해석이 체크리스트와 어긋난다.",
                "어디가 걸리는지 위치만 짚고,",
                "아직 못 한 항목 **하나만** 스스로 찾도록 유도한다.",
              ].join(" ");

      const system: Anthropic.TextBlockParam[] = [
        // 프레임은 안 변한다 — 여기까지 캐시한다
        { type: "text", text: characterSystem(), cache_control: { type: "ephemeral" } },
        {
          type: "text",
          text: [
            "## 이번 턴에 할 일",
            task,
            unit.nextNudge
              ? `\n참고로 이 항목의 유도 문구는 이렇다: "${unit.nextNudge}"\n같은 말을 그대로 반복하지 말고, 학생이 쓴 말에 맞춰 다시 말한다.`
              : "",
            state.lastTutorUtterance
              ? `\n직전에 한 말: "${state.lastTutorUtterance}" — 이 말을 되풀이하지 않는다.`
              : "",
          ]
            .filter(Boolean)
            .join("\n"),
        },
      ];

      const answer = await call(
        "speak",
        system,
        `${unitBlock(unit)}\n\n## 학생이 방금 한 말\n${studentText}`,
        512,
        "medium",
      );
      return answer ? { message: answer } : null;
    },
  };
}
