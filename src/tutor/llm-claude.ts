import Anthropic from "@anthropic-ai/sdk";
import {
  characterSystem,
  judgeSystem,
  judgeUser,
  speakUser,
  unitBlock,
} from "../../content/tutor/prompt";
import type { JudgeInput, SpeakInput, TutorLlm } from "./llm";

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
  /**
   * 발화 콜의 깊이.
   *
   * **기본이 `low`인 건 재 보고 정한 것이다** (2026-09-06, 같은 대화 2턴 비교).
   * `medium`은 느리고(6.7초 vs 3.7초) 비싸고, 레슨의 유도 문구를 그대로
   * 베끼는 일이 있었다. `low`는 학생이 쓴 말에 맞춰 다시 말했다.
   * 표본이 작으므로 대화가 쌓이면 다시 잰다.
   */
  speakEffort?: "low" | "medium";
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
  const effort = options.speakEffort ?? "low";

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
      const answer = await call(
        "judge",
        [{ type: "text", text: judgeSystem() }],
        judgeUser(unit, studentText),
        // 64로는 thinking에 다 쓰이고 빈 응답이 온다 (프록시에서 재현)
        256,
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

      /*
        **캐시가 먹도록 안 변하는 것부터 쌓는다.**
        프레임(캐릭터·말투)은 수업 내내 같고, 문장 블록은 그 문장을 푸는 동안
        같다. 매 턴 달라지는 것(이번 할 일·학생 발화)은 캐시 경계 뒤로 보낸다.
      */
      const system: Anthropic.TextBlockParam[] = [
        { type: "text", text: characterSystem(), cache_control: { type: "ephemeral" } },
        { type: "text", text: unitBlock(unit), cache_control: { type: "ephemeral" } },
      ];
      const userText = speakUser(action, unit, state, studentText, askedWord);

      const answer = await call("speak", system, userText, 512, effort);
      return answer ? { message: answer } : null;
    },
  };
}
