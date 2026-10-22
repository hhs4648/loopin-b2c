import { describe, expect, it } from "vitest";
import { homeLine, LINES, speak, TEACHERS, teacherOf } from "./teacher";

const prickly = teacherOf("prickly");
const sangnyang = teacherOf("sangnyang");

describe("speak — 반말 쌤", () => {
  it("해요체 끝말을 반말로", () => {
    expect(speak("아쉽게도 틀렸어요.", prickly)).toBe("아쉽게도 틀렸어.");
    expect(speak("여기가 주어예요. 동사는 어디일까요?", prickly)).toBe("여기가 주어야. 동사는 어디일까?");
    expect(speak("시간이에요! 그렇죠?", prickly)).toBe("시간이야! 그렇지?");
    expect(speak("그건 아니에요, 다시 찾아 보세요.", prickly)).toBe("그건 아니야, 다시 찾아 봐.");
  });
  it("「」 안 버튼 이름과 끝말 아닌 「요」는 그대로", () => {
    expect(speak("「네, 좋아요!」를 눌러요.", prickly)).toBe("「네, 좋아요!」를 눌러.");
    expect(speak("이건 중요.", prickly)).toBe("이건 중요.");
    expect(speak("뜻이 필요해요.", prickly)).toBe("뜻이 필요해.");
  });
  it("존댓말 쌤은 그대로", () => {
    expect(speak("아쉽게도 틀렸어요.", sangnyang)).toBe("아쉽게도 틀렸어요.");
    expect(speak("맞아요.", teacherOf("sosim"))).toBe("맞아요.");
  });
});

describe("쌤 목록", () => {
  it("모든 쌤에 표 대사가 다 있다", () => {
    for (const t of TEACHERS) {
      const l = LINES[t.id];
      for (const k of ["greet", "start", "correct", "combo", "best", "wrong", "repeat", "away", "done", "streak", "comeback", "growth", "slump"] as const) {
        expect(l[k], `${t.name} ${k}`).toBeTruthy();
      }
      expect(l.free.length).toBeGreaterThan(0);
      for (const o of TEACHERS) if (o.id !== t.id) expect(l.meet[o.id], `${t.name} → ${o.name}`).toBeTruthy();
    }
  });
  it("모르는 id는 상냥쌤", () => {
    expect(teacherOf("nope").id).toBe("sangnyang");
  });
});

describe("homeLine — 출석", () => {
  const now = new Date(2026, 9, 22, 9);
  it("3일 연속이면 출석 대사, 숫자를 넣는다", () => {
    expect(homeLine(prickly, ["2026-10-20", "2026-10-21", "2026-10-22"], now, () => 1)).toBe("…3일째네. 4일째부터가 진짜니까 내일 봐.");
  });
  it("7일 넘게 쉬었으면 복귀", () => {
    expect(homeLine(sangnyang, ["2026-10-01", "2026-10-22"], now, () => 1)).toBe(LINES.sangnyang.comeback);
  });
  it("그 밖엔 첫 인사", () => {
    expect(homeLine(sangnyang, ["2026-10-21", "2026-10-22"], now, () => 1)).toBe(LINES.sangnyang.greet);
  });
});
