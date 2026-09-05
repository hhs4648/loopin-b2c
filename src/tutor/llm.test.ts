import { describe, expect, it } from "vitest";
import { validateLlmOutput } from "./llm";

/**
 * 가드레일은 **모델이 무슨 말을 하든 마지막으로 걸러 주는 그물**이다.
 * 여기서 새는 게 있으면 프롬프트를 아무리 잘 써도 언젠가 정답이 새어 나간다.
 */
const banned = [
  "지난 4년 동안 이 회사에서 근무할 수 있었던 것은 영광이었다",
  "근무하다",
];

describe("validateLlmOutput", () => {
  it("정상 발화는 통과한다", () => {
    const v = validateLlmOutput(
      { message: "지금 막힌 곳은 문장 뒷부분이에요. 그 부분만 다시 볼까요?" },
      { bannedStrings: banned },
    );
    expect(v.ok).toBe(true);
  });

  it("모범 해석을 그대로 말하면 버린다", () => {
    const v = validateLlmOutput(
      { message: "정답은 지난 4년 동안 이 회사에서 근무할 수 있었던 것은 영광이었다 예요." },
      { bannedStrings: banned },
    );
    expect(v.ok).toBe(false);
  });

  it("채점 포인트를 읊어도 버린다 — 모범 해석을 피해 가는 유출 경로다", () => {
    const v = validateLlmOutput(
      { message: "여기서는 serve → 근무하다 로 보면 돼요." },
      { bannedStrings: banned },
    );
    expect(v.ok).toBe(false);
  });

  it("정답이 버튼에 있어도 버린다", () => {
    const v = validateLlmOutput(
      { message: "어느 쪽일까요?", buttons: ["근무하다", "봉사하다"] },
      { bannedStrings: banned },
    );
    expect(v.ok).toBe(false);
  });

  it("문장이 4개를 넘으면 버린다", () => {
    const v = validateLlmOutput(
      { message: "하나예요. 둘이에요. 셋이에요. 넷이에요. 다섯이에요." },
      { bannedStrings: banned },
    );
    expect(v.ok).toBe(false);
  });

  it("한 턴에 질문이 두 개면 버린다", () => {
    const v = validateLlmOutput(
      { message: "여기 볼까요? 저기도 볼까요?" },
      { bannedStrings: banned },
    );
    expect(v.ok).toBe(false);
  });

  it.each(["여기 동사부터 봐.", "다시 한번 해.", "그 정도면 좋아."])(
    "반말이면 버린다: %s",
    (message) => {
      expect(validateLlmOutput({ message }, { bannedStrings: banned }).ok).toBe(false);
    },
  );

  it.each([
    "좋아요. 앞부분은 맞았어요. 뒤쪽만 다시 볼게요. 어느 부분이 걸리나요?",
    "잘했어요! 이번엔 뒷부분만 볼까요?",
    "지금 볼 곳은 문장 뒤쪽이에요. 거기만 다시 적어 주세요.",
  ])("해요체 정상 발화는 오탐하지 않는다: %s", (message) => {
    expect(validateLlmOutput({ message }, { bannedStrings: banned }).ok).toBe(true);
  });
});
