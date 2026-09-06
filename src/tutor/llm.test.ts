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
      { message: "privilege를 잘 봤어요. 이제 serve 자리를 같이 볼까요?" },
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

  it("직전 대사를 그대로 되풀이하면 버린다", () => {
    const line = "privilege를 잘 봤어요. 이제 serve 자리를 같이 볼까요?";
    const v = validateLlmOutput(
      { message: line },
      { bannedStrings: banned, previousUtterance: line },
    );
    expect(v.ok).toBe(false);
  });

  /*
    아래 둘은 실제 수업에서 나온 불평이다 (2026-09-06).
    "좋아요 그 부분은 맞았어요" — 어느 부분인지 학생은 모른다.
    "serve는 봉사하다가 아니에요" — 학생은 그렇게 쓴 적이 없다.
  */
  it("「그 부분」처럼 뭉뚱그리면 버린다 — 학생은 어디인지 모른다", () => {
    for (const message of [
      "좋아요, 그 부분은 맞았어요. 나머지를 볼까요?",
      "이 부분을 다시 볼까요? 조금만 더 보면 돼요.",
      "거기가 맞았어요. 이제 뒤를 볼까요?",
    ]) {
      expect(validateLlmOutput({ message }, { bannedStrings: [] }).ok, message).toBe(
        false,
      );
    }
  });

  it("영어 원문을 집어서 말하면 통과한다", () => {
    const v = validateLlmOutput(
      { message: "in this company를 잘 봤어요. 이제 serve 자리를 같이 볼까요?" },
      { bannedStrings: [], studentText: "이 회사에서 4년 동안" },
    );
    expect(v.ok).toBe(true);
  });

  it("학생이 쓰지 않은 해석을 부정하면 버린다", () => {
    const student = "이 회사에서 4년 동안 일했습니다";
    for (const message of [
      "여기서 serve는 '봉사하다'가 아니에요. 어떤 뜻일까요?",
      "fortune은 재산이 아니에요. 그럼 무엇일까요?",
    ]) {
      expect(
        validateLlmOutput({ message }, { bannedStrings: [], studentText: student }).ok,
        message,
      ).toBe(false);
    }
  });

  it("학생이 실제로 쓴 말을 바로잡는 건 통과한다", () => {
    const v = validateLlmOutput(
      { message: "여기서 serve는 '봉사하다'가 아니에요. 회사 이야기라면 어떨까요?" },
      { bannedStrings: [], studentText: "이 회사에서 4년 동안 봉사했습니다" },
    );
    expect(v.ok).toBe(true);
  });

  it("학생 발화를 모르면 부정 검사를 걸지 않는다 — 레슨 고정 대사까지 막지 않는다", () => {
    const v = validateLlmOutput(
      { message: "여기서 serve는 '봉사하다'가 아니에요. 어떤 뜻일까요?" },
      { bannedStrings: [] },
    );
    expect(v.ok).toBe(true);
  });

  it("말버릇이 한 턴에 둘 이상이면 버린다", () => {
    const v = validateLlmOutput(
      { message: "어머 잘했어요^^ 이번엔 뒷부분만 볼까요?" },
      { bannedStrings: banned },
    );
    expect(v.ok).toBe(false);
  });

  it("말버릇 하나는 통과한다", () => {
    const v = validateLlmOutput(
      { message: "잘했어요^^ 이번엔 뒷부분만 볼까요?" },
      { bannedStrings: banned },
    );
    expect(v.ok).toBe(true);
  });

  it("물결표는 말버릇으로 세지 않는다 — 문법 표기로도 쓰인다", () => {
    const v = validateLlmOutput(
      { message: "from ~ to는 짝을 이루는 표현이에요. 어떻게 이어 줄까요?" },
      { bannedStrings: banned },
    );
    expect(v.ok).toBe(true);
  });

  it("모델 발화가 한 문장뿐이면 버린다 (min_sentences)", () => {
    const v = validateLlmOutput(
      { message: "뒷부분을 다시 볼까요?" },
      { bannedStrings: banned, minSentences: 2 },
    );
    expect(v.ok).toBe(false);
  });

  it.each([
    "좋아요. 앞부분은 맞았어요. 뒤쪽만 다시 볼게요. 어느 부분이 걸리나요?",
    "잘했어요! 이번엔 뒷부분만 볼까요?",
    "지금 볼 곳은 문장 뒤쪽이에요. 거기만 다시 적어 주세요.",
  ])("해요체 정상 발화는 오탐하지 않는다: %s", (message) => {
    expect(validateLlmOutput({ message }, { bannedStrings: banned }).ok).toBe(true);
  });
});
