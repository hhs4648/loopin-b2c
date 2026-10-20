import { describe, expect, it } from "vitest";
import { createPolicySession, type ResumeSnapshot } from "./session";
import { emptyStudentState } from "./student-state";

/*
  이어 하기 (2026-10-20 선생님: 중간에 나가면 멈춘 곳부터) — 자리를 남겼다가 새 세션에 되살리면 같은 화면이 나온다.
*/
const ID = "moeui-2026-03-21-music-researchers";
const deps = { loadStudent: emptyStudentState, saveStudent() {}, logEvents() {}, now: () => 0 };

describe("이어 하기", () => {
  it("남긴 자리를 새 세션에 되살리면 같은 화면 — JSON으로 오가도", async () => {
    const a = createPolicySession(ID, null, deps);
    let v = a.view();
    // 첫 버튼으로 몇 걸음 나아간다 (버튼이 없으면 자동 넘김)
    for (let i = 0; i < 6; i++) v = await a.submit(v.buttons[0] ?? "__auto_next");
    const snap = JSON.parse(JSON.stringify(a.snapshot())) as ResumeSnapshot;

    const b = createPolicySession(ID, null, deps);
    expect(b.restore(snap)).toBe(true);
    const want = a.view();
    const got = b.view();
    expect(got.message).toBe(want.message);
    expect(got.buttons).toEqual(want.buttons);
  });

  it("레슨 모양이 바뀌었거나 끝난 수업이면 되살리지 않는다", () => {
    const a = createPolicySession(ID, null, deps);
    const snap = a.snapshot();
    const b = createPolicySession(ID, null, deps);
    expect(b.restore({ ...snap, shape: "다른 모양" })).toBe(false);
    expect(b.restore({ ...snap, state: { ...(snap.state as object), stage: "done" } })).toBe(false);
    expect(b.restore(null as unknown as ResumeSnapshot)).toBe(false);
  });

  it("처음엔 마지막 문장에 오지 않았다", () => {
    expect(createPolicySession(ID, null, deps).reachedEnd()).toBe(false);
  });
});
