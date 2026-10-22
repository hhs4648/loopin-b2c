import { describe, expect, it } from "vitest";
import { examplePatch, mergePatch, resolveSource, summarize, whereNow, type JourneyRow } from "./journey";

function row(over: Partial<JourneyRow> = {}): JourneyRow {
  return {
    src: "direct",
    login_tap: null,
    account: null,
    learner_group: null,
    grade: null,
    onboard_step: null,
    kind: "new",
    example_started: false,
    example_place: null,
    example_index: 0,
    example_total: 0,
    example_done: false,
    visit_days: 1,
    tester: null,
    first_seen: "2026-10-22T00:00:00.000Z",
    last_seen: "2026-10-22T00:00:00.000Z",
    ...over,
  };
}

describe("유입 경로", () => {
  it("주소의 src 가 직전 사이트보다 이긴다", () => {
    expect(resolveSource("?src=insta", "https://orbi.kr/z", "direct")).toBe("insta");
    expect(resolveSource("?utm_source=instagram", "", null)).toBe("insta");
    expect(resolveSource("?src=orbi", "", "insta")).toBe("orbi");
  });

  it("주소에 없으면 저장값, 그것도 없으면 직전 사이트", () => {
    expect(resolveSource("", "https://www.instagram.com/p/1", null)).toBe("insta");
    expect(resolveSource("", "https://orbi.kr/note", null)).toBe("orbi");
    expect(resolveSource("", "android-app://com.loopin.b2capp", null)).toBe("play");
    expect(resolveSource("", "https://orbi.kr/note", "friend")).toBe("friend");
    expect(resolveSource("", "", null)).toBe("direct");
    expect(resolveSource("?src=blog", "", null)).toBe("other");
  });
});

describe("기록 합치기", () => {
  it("뒷 단계가 앞 단계를 지우지 않는다", () => {
    const merged = mergePatch(
      { onboard_step: "order", example_index: 3, example_place: "3문장", example_started: true },
      { onboard_step: "intro", example_index: 1, example_place: "1문장" },
    );
    expect(merged.onboard_step).toBe("order");
    expect(merged.example_index).toBe(3);
    expect(merged.example_place).toBe("3문장");
  });

  it("소셜 로그인이 손님 표시를 덮는다", () => {
    expect(mergePatch({ account: "guest" }, { account: "kakao" }).account).toBe("kakao");
    expect(mergePatch({ account: "google" }, { account: "guest" }).account).toBe("google");
  });
});

describe("예시 분석 자리", () => {
  it("미리보기·문장·끝을 구분한다", () => {
    expect(examplePatch({ screen: "read", ended: false, progressIndex: 1, progressTotal: 8, chunkLabel: "" }).example_place).toBe("지문 미리보기");
    expect(examplePatch({ screen: "study", ended: false, progressIndex: 2, progressTotal: 8, chunkLabel: "2문장" }).example_index).toBe(2);
    const done = examplePatch({ screen: "chat", ended: true, progressIndex: 8, progressTotal: 8, chunkLabel: "8문장" });
    expect(done.example_done).toBe(true);
    expect(done.example_place).toBe("끝");
  });
});

describe("입구 집계", () => {
  it("처음 온 사람만 깔때기에 넣고, 이미 쓰던 사람은 뺀다", () => {
    const summary = summarize([
      row(),
      row({ account: "guest", onboard_step: "grade", learner_group: "suneung", grade: 5 }),
      row({ account: "kakao", login_tap: "kakao", onboard_step: "done", example_started: true, example_place: "3문장" }),
      row({ account: "guest", onboard_step: "done", example_started: true, example_done: true, visit_days: 2, src: "insta" }),
      row({ kind: "returning", account: "google", src: "orbi" }),
      row({ kind: null, login_tap: "apple" }),
    ]);
    expect(summary.fresh).toBe(5);
    expect(summary.returning).toBe(1);
    expect(summary.funnel.map((s) => s.count)).toEqual([5, 3, 3, 2, 2, 1, 1]);
    expect(summary.sources.find((s) => s.id === "insta")?.count).toBe(1);
    expect(summary.sources.find((s) => s.id === "orbi")?.count).toBe(1);
    expect(summary.exampleStops.map((s) => s.label)).toEqual(["3문장"]);
    expect(summary.grades.map((s) => s.label)).toContain("4~5등급");
  });

  it("멈춘 자리를 말로 적는다", () => {
    expect(whereNow(row())).toBe("로그인 화면");
    expect(whereNow(row({ login_tap: "kakao" }))).toBe("카카오만 누르고 나감");
    expect(whereNow(row({ account: "guest", onboard_step: "done" }))).toBe("같이 볼래요");
    expect(whereNow(row({ kind: "returning" }))).toBe("이미 쓰던 사람");
  });
});
