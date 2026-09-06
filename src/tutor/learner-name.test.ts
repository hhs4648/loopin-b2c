import { describe, expect, it } from "vitest";
import { parseName } from "./learner-name";

describe("이름 알아듣기", () => {
  it("그냥 이름", () => {
    expect(parseName("민준")).toBe("민준");
    expect(parseName("김민준")).toBe("김민준");
    expect(parseName("Jimin")).toBe("Jimin");
  });

  it("조사와 어미를 뗀다", () => {
    expect(parseName("민준이요")).toBe("민준");
    expect(parseName("민준이에요")).toBe("민준");
    expect(parseName("민준입니다")).toBe("민준");
    expect(parseName("민준이야")).toBe("민준");
    expect(parseName("저는 민준이에요")).toBe("민준");
    expect(parseName("제 이름은 김민준입니다")).toBe("김민준");
    expect(parseName("민준이라고 해요")).toBe("민준");
  });

  it("문장부호를 떼고 본다", () => {
    expect(parseName("민준!")).toBe("민준");
    expect(parseName("  민준 ")).toBe("민준");
  });

  it("이름이 아닌 말은 null — 되묻지 않고 그냥 넘어가려는 것이다", () => {
    expect(parseName("그건 말하기 싫어요")).toBe(null);
    expect(parseName("잘 모르겠어요")).toBe(null);
    expect(parseName("")).toBe(null);
    expect(parseName("이름이너무길어서받아주지않는이름")).toBe(null);
    expect(parseName("ㅋㅋㅋ")).toBe(null);
    // 모양만 보면 이름 같지만 이름이 아닌 말
    expect(parseName("안녕하세요")).toBe(null);
    expect(parseName("비밀이요")).toBe(null);
    expect(parseName("네")).toBe(null);
  });
});
