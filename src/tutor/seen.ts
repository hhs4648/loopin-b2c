import type { LessonSet } from "../../content/tutor/types";
import { allMiniMocks, allAttempts, isReviewMock, type MiniAttempt, type MiniMock } from "./mini";
import { setStatuses } from "./progress";
import { allSets } from "./sets";
import { kindOfSet, tenMinMocks } from "./tenmin";

/**
 * 어떤 문제를 봤고 안 봤나 — 진도표와 「자주 틀리는 유형」의 바탕 (2026-10-20 선생님).
 *
 * 기록은 세 군데에 흩어져 있다: 분석 수업(`progress.ts`의 회차), 교무실 미니 모의고사, 10분 모의고사(복습 포함).
 * 전부 **세트 id**로 모아 가장 최근에 답을 낸 결과를 그 문제의 지금 상태로 본다.
 */

export type SeenRow = {
  setId: string;
  /** 어디서든 한 번이라도 봤나 (답을 안 냈어도 수업에 들어갔으면 본 것) */
  seen: boolean;
  /** 가장 최근에 낸 답이 맞았나 — 낸 적 없으면 null */
  latest: boolean | null;
  /** 답을 낸 횟수 · 틀린 횟수 */
  answered: number;
  wrong: number;
};

type Event = { setId: string; at: string; correct: boolean | null };

function eventsOfMock(mock: MiniMock, a: MiniAttempt): Event[] {
  return mock.items
    .filter((it) => it.lesson)
    .map((it) => ({ setId: it.lesson!, at: a.at, correct: it.no in a.answers ? a.answers[it.no] === it.answer : null }));
}

export function seenBySet(): Record<string, SeenRow> {
  const events: Event[] = [];
  // 분석 수업
  for (const [setId, st] of Object.entries(setStatuses())) {
    if (st.state === "new" && st.answered === 0) continue;
    events.push({ setId, at: st.lastAt ?? "", correct: st.latest });
    // 회차별 상세는 없으니 맞힌/틀린 횟수는 합계로
    for (let k = 0; k < st.answered; k++) events.push({ setId, at: "", correct: k < st.correct });
  }
  // 미니 모의고사 — 교무실 긴 것, 10분, 복습
  const attempts = allAttempts();
  const byId = new Map<string, MiniMock>([...allMiniMocks(), ...tenMinMocks("all"), ...tenMinMocks("2pt")].map((m) => [m.id, m]));
  for (const [id, list] of Object.entries(attempts)) {
    for (const a of list) {
      let mock = byId.get(id);
      if (!mock && isReviewMock(id) && a.items) {
        // 복습은 그때 문항을 기록에 남겨 뒀다
        const items = tenMinMocks("all").flatMap((m) => m.items);
        mock = { id, subject: "english", title: "", subtitle: "", source: "", minutes: 0,
          items: a.items.map((x) => ({ ...items.find((it) => it.lesson === x.lesson)!, no: x.no })).filter((it) => it && it.lesson) };
      }
      if (mock) events.push(...eventsOfMock(mock, a));
    }
  }
  const out: Record<string, SeenRow> = {};
  for (const e of events) {
    const row = (out[e.setId] ??= { setId: e.setId, seen: true, latest: null, answered: 0, wrong: 0 });
    if (e.correct == null) continue;
    row.answered++;
    if (!e.correct) row.wrong++;
  }
  // 가장 최근 답
  const latestAt = new Map<string, string>();
  for (const e of events) {
    if (e.correct == null) continue;
    if ((latestAt.get(e.setId) ?? "") <= e.at) {
      latestAt.set(e.setId, e.at);
      out[e.setId]!.latest = e.correct;
    }
  }
  return out;
}

export type KindStat = { kind: string; answered: number; wrong: number; rate: number };

/** 유형별 — 답을 낸 횟수와 틀린 횟수. 틀린 비율 높은 순, 답을 낸 적 없는 유형은 뺀다 */
export function kindStats(rows: Record<string, SeenRow> = seenBySet(), sets: LessonSet[] = allSets()): KindStat[] {
  const agg = new Map<string, { answered: number; wrong: number }>();
  for (const s of sets) {
    const r = rows[s.id];
    if (!r || r.answered === 0) continue;
    const kind = kindOfSet(s);
    const a = agg.get(kind) ?? { answered: 0, wrong: 0 };
    a.answered += r.answered;
    a.wrong += r.wrong;
    agg.set(kind, a);
  }
  return [...agg.entries()]
    .map(([kind, a]) => ({ kind, ...a, rate: a.answered ? a.wrong / a.answered : 0 }))
    .sort((x, y) => y.rate - x.rate || y.answered - x.answered);
}
