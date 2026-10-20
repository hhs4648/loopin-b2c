import { pushKey } from "./cloud";
import { getPolicyLesson } from "./policy/lessons";
import type { PickStep } from "./policy/types";
import { loadNotes } from "./notes";
import { seenBySet } from "./seen";
import { allCollections, allSets } from "./sets";

/**
 * 문장 연습 — 영어 덩어리를 한국어 해석 칸에 끌어 맞추는 「해석 맞추기」를 연습실에서 (2026-10-20 선생님: 해석할 때 가장 유용했다).
 *
 * 어떤 문장을 내나: ① 「연습할 문장」으로 노트에 담긴 것(자유 해석을 틀린 문장) ② 최근에 틀린 지문의 문장들 ③ 그 밖에 본 지문의 문장들.
 * 맞추기 자료(`match`)가 있는 문장만 — 레슨 JSON의 pick 스텝 중 `match.ko`가 있는 것.
 *
 * 화면에는 문장을 쭉 나열하지 않는다 — 연도 → 시험(월)별로 **연습할 문장 수와 본 비율**만 보이고, 「연습 시작」이면
 * 추천 순(안 본 것 먼저, 연습할 문장 → 틀린 지문 → 본 지문)으로 낸다 (2026-10-20 선생님).
 */

export type PracticeSentence = {
  key: string;
  lessonId: string;
  setId: string;
  collectionId: string;
  setTitle: string;
  sentenceId: number;
  text: string;
  /** 끌어 놓을 영어 덩어리 */
  chunks: string[];
  /** 한국어 해석 — 칸은 { en, ko } */
  ko: (string | { en: string; ko: string })[];
  reason: "연습할 문장" | "틀린 지문" | "본 지문";
};

const REASON_RANK: Record<PracticeSentence["reason"], number> = { "연습할 문장": 0, "틀린 지문": 1, "본 지문": 2 };

function matchOf(set: { id: string; collection: string; title: string; lessons: string[] }, reason: PracticeSentence["reason"], onlyText?: string): PracticeSentence[] {
  const lessonId = set.lessons[0]!;
  const lesson = getPolicyLesson(lessonId);
  if (!lesson) return [];
  const out: PracticeSentence[] = [];
  for (const sen of lesson.sentences) {
    if (onlyText && sen.text !== onlyText) continue;
    const st = sen.steps.find((x): x is PickStep => x.type === "pick" && !!(x as PickStep).match);
    if (!st?.match) continue;
    out.push({
      key: `${lessonId}#${sen.id}`, lessonId, setId: set.id, collectionId: set.collection, setTitle: set.title,
      sentenceId: sen.id, text: sen.text, chunks: st.candidates, ko: st.match.ko, reason,
    });
  }
  return out;
}

export function practiceSentences(): PracticeSentence[] {
  const out: PracticeSentence[] = [];
  const seenKey = new Set<string>();
  const push = (list: PracticeSentence[]) => {
    for (const p of list) {
      if (seenKey.has(p.key)) continue;
      seenKey.add(p.key);
      out.push(p);
    }
  };
  const sets = allSets();
  // ① 연습할 문장 (자유 해석을 틀린 것) — 노트 키 practice:<영어 문장>
  for (const n of loadNotes()) {
    if (!n.key.startsWith("practice:")) continue;
    const set = sets.find((s) => s.lessons.includes(n.lessonId));
    if (set) push(matchOf(set, "연습할 문장", n.key.slice("practice:".length)));
  }
  // ② 최근에 틀린 지문 ③ 본 지문
  const rows = seenBySet();
  for (const s of sets) if (rows[s.id]?.latest === false) push(matchOf(s, "틀린 지문"));
  for (const s of sets) if (rows[s.id]?.seen && rows[s.id]?.latest !== false) push(matchOf(s, "본 지문"));
  return out;
}

/* ── 연습한 문장 기록 — 이 브라우저가 원본, 서버가 사본 (`cloud.ts`) ── */

const KEY = "loopin.sentence-practice.v1";

export function practicedKeys(): Record<string, string> {
  try {
    const raw = window.localStorage.getItem(KEY);
    const all = raw ? (JSON.parse(raw) as Record<string, string>) : {};
    return all && typeof all === "object" ? all : {};
  } catch {
    return {};
  }
}

/** 한 문장을 끝까지 맞췄다 */
export function markPracticed(key: string): void {
  try {
    window.localStorage.setItem(KEY, JSON.stringify({ ...practicedKeys(), [key]: new Date().toISOString() }));
    pushKey(KEY);
  } catch {
    /* 그대로 */
  }
}

/** 추천 순 — 안 본 것 먼저, 그 안에서 연습할 문장 → 틀린 지문 → 본 지문, 그다음 문장 순서 */
export function recommendedOrder(list: PracticeSentence[], practiced: Record<string, string> = practicedKeys()): PracticeSentence[] {
  return [...list].sort((a, b) =>
    Number(a.key in practiced) - Number(b.key in practiced) ||
    REASON_RANK[a.reason] - REASON_RANK[b.reason] ||
    a.setId.localeCompare(b.setId) ||
    a.sentenceId - b.sentenceId,
  );
}

export type PracticeGroup = {
  collectionId: string;
  title: string;
  year: number;
  held: string;
  sentences: PracticeSentence[];
  /** 연습할 문장 중 끝까지 맞춰 본 수 */
  seen: number;
};

/** 시험(월)별 묶음 — 최근 시험부터. 연도 구분은 화면에서 year로 */
export function practiceGroups(list: PracticeSentence[] = practiceSentences(), practiced: Record<string, string> = practicedKeys()): PracticeGroup[] {
  const groups = new Map<string, PracticeGroup>();
  for (const p of list) {
    let g = groups.get(p.collectionId);
    if (!g) {
      const c = allCollections().find((x) => x.id === p.collectionId);
      const held = c?.exam?.held ?? "0000-00";
      g = { collectionId: p.collectionId, title: c?.title ?? p.collectionId, year: Number(/(\d{4})/.exec(c?.title ?? "")?.[1] ?? held.slice(0, 4)), held, sentences: [], seen: 0 };
      groups.set(p.collectionId, g);
    }
    g.sentences.push(p);
    if (p.key in practiced) g.seen++;
  }
  return [...groups.values()].sort((a, b) => b.held.localeCompare(a.held));
}
