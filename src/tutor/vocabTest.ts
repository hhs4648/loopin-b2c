import { allPolicyLessons } from "./policy/lessons";
import type { PolicyLesson } from "./policy/types";
import type { VocabEntry } from "./vocab";

/**
 * 단어장 테스트 — 저장한 단어로 세 가지 문제를 섞어 낸다.
 *
 * - 짝 맞추기: 영어 카드와 뜻 카드를 잇는다 (한 판에 4쌍까지)
 * - 뜻 고르기: 영어를 보고 뜻 네 개 중 하나
 * - 문장 빈칸: 단어가 나온 지문 문장을 빈칸으로 비우고, 한국어 해석을 보고 들어갈 단어를 고른다
 *
 * 문제는 수업 데이터(레슨 JSON)에서만 만든다. LLM을 부르지 않는다.
 * 단어마다 본 횟수·맞힌 횟수·틀린 횟수를 이 브라우저에 센다.
 */

/* ── 단어별 기록 ──────────────────────────────────────────────────── */

export type WordStat = { seen: number; right: number; wrong: number; lastAt?: string };

const STATS_KEY = "loopin.vocab-stats.v1";

const keyOf = (en: string) => en.trim().toLowerCase();

export function loadWordStats(): Record<string, WordStat> {
  try {
    const raw = window.localStorage.getItem(STATS_KEY);
    const parsed = raw ? (JSON.parse(raw) as Record<string, WordStat>) : {};
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

export function statOf(stats: Record<string, WordStat>, en: string): WordStat {
  return stats[keyOf(en)] ?? { seen: 0, right: 0, wrong: 0 };
}

/** 한 문제를 풀 때마다 부른다 — 본 횟수 +1, 맞힘이나 틀림 +1 */
export function recordAnswer(en: string, correct: boolean): Record<string, WordStat> {
  const stats = loadWordStats();
  const prev = statOf(stats, en);
  stats[keyOf(en)] = {
    seen: prev.seen + 1,
    right: prev.right + (correct ? 1 : 0),
    wrong: prev.wrong + (correct ? 0 : 1),
    lastAt: new Date().toISOString(),
  };
  try {
    window.localStorage.setItem(STATS_KEY, JSON.stringify(stats));
  } catch {
    /* 못 저장해도 테스트는 그대로 */
  }
  return stats;
}

/* ── 문제 재료 ────────────────────────────────────────────────────── */

/** 뜻에서 「·」 뒤 해설은 뺀다 — 보기로 쓰기엔 너무 길다 */
export const meaningOf = (ko: string) => ko.split(" · ")[0]!.trim();

/** 시험지 표시(①, ② …)는 빈칸 문제에서 지운다 */
const cleanSentence = (text: string) => text.replace(/[①-⑳]/g, "").replace(/\s{2,}/g, " ").trim();

const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/** 문장 안에서 단어가 쓰인 꼴을 찾는다 — contribute → contributes, contributed 까지 */
export function findForm(sentence: string, en: string): { form: string; at: number } | null {
  const w = en.trim();
  if (!w) return null;
  const forms = [`${esc(w)}(?:s|es|d|ed|ing)?`];
  if (!w.includes(" ")) {
    if (w.endsWith("e")) forms.push(`${esc(w.slice(0, -1))}(?:es|ed|ing)`);
    if (w.endsWith("y")) forms.push(`${esc(w.slice(0, -1))}(?:ies|ied)`);
  }
  const m = new RegExp(`\\b(?:${forms.join("|")})\\b`, "i").exec(sentence);
  return m ? { form: m[0], at: m.index } : null;
}

/** 저장할 때 지문을 안 적어 둔 단어 — 문장으로 지문을 찾는다 */
export function lessonIdOfSentence(sentence: string, lessons: PolicyLesson[] = allPolicyLessons()): string | undefined {
  const s = sentence.trim();
  if (!s) return undefined;
  return lessons.find((l) => l.sentences.some((x) => x.text.trim() === s))?.id;
}

/** `at` = 문장 속 빈칸 자리 (글자 위치) */
export type BlankSource = { sentence: string; form: string; at: number; translation: string };

/**
 * 빈칸 문제에 쓸 문장. 저장한 문장 → 저장한 지문 → 다른 지문 순으로 찾는다.
 * 해석이 있는 문장만 쓴다.
 */
export function blankSourceOf(word: VocabEntry, lessons: PolicyLesson[] = allPolicyLessons()): BlankSource | null {
  const source = word.source ?? lessonIdOfSentence(word.sentence, lessons);
  const ordered = [
    ...lessons.filter((l) => l.id === source),
    ...lessons.filter((l) => l.id !== source),
  ];
  const candidates = ordered.flatMap((l) => l.sentences).filter((s) => s.model_translation?.trim());
  const saved = candidates.find((s) => s.text.trim() === word.sentence.trim());
  for (const s of saved ? [saved, ...candidates] : candidates) {
    const sentence = cleanSentence(s.text);
    const found = findForm(sentence, word.en);
    if (found) return { sentence, ...found, translation: s.model_translation.trim() };
  }
  return null;
}

/* ── 품사 · 꼴 맞추기 (빈칸 보기용) ──────────────────────────────── */

export type Pos = "verb" | "adj" | "adv" | "noun";

/**
 * 품사는 데이터에 없어서 한국어 뜻의 끝으로 가른다 (첫 뜻만 본다).
 * 「…다」 동사 · 「…한/…인/…의/…는/…든」 형용사 · 「…게/…히/…으로/…고」 부사 · 나머지 명사.
 * 「~하는 사람들」 같은 명사구는 끝이 명사라 명사로 떨어진다
 */
export function posOf(ko: string): Pos {
  const first = meaningOf(ko).split(",")[0]!.trim();
  if (/다$/.test(first)) return "verb";
  if (/(게|히|으로|하고|하여)$/.test(first) || /^그럼에도/.test(first)) return "adv";
  if (/(한|적인|중인|의|는|든|운|된|은|던)$/.test(first)) return "adj";
  return "noun";
}

type Ending = "" | "s" | "ed" | "ing";

/** 문장에 쓰인 꼴이 원형에서 어떻게 바뀌었나 — contribute → contributed 면 "ed" */
export function endingOf(base: string, form: string): Ending {
  const b = base.toLowerCase();
  const f = form.toLowerCase();
  if (f === b) return "";
  if (f.endsWith("ing")) return "ing";
  if (f.endsWith("ed")) return "ed";
  if (f.endsWith("s")) return "s";
  return "";
}

const IRREGULAR_ED: Record<string, string> = {
  overcome: "overcame", make: "made", take: "took", leave: "left", lift: "lifted", give: "gave",
  get: "got", find: "found", think: "thought", bring: "brought", hold: "held", keep: "kept",
};

/** 보기 단어를 정답과 같은 꼴로 — 여러 단어면 동사는 첫 단어, 명사는 끝 단어만 바꾼다 */
export function inflect(word: string, ending: Ending, pos: Pos): string {
  if (!ending) return word;
  const parts = word.split(" ");
  if (pos !== "verb" && parts.length > 1) {
    if (ending !== "s") return word;
    return [...parts.slice(0, -1), inflect(parts.at(-1)!, ending, pos)].join(" ");
  }
  const [head, ...rest] = parts;
  const h = head!;
  const cons = (c: string | undefined) => !!c && !/[aeiou]/i.test(c);
  let out = h;
  if (ending === "s") {
    if (/(s|x|z|ch|sh)$/i.test(h)) out = `${h}es`;
    else if (/y$/i.test(h) && cons(h.at(-2))) out = `${h.slice(0, -1)}ies`;
    else out = `${h}s`;
  } else if (pos === "verb" && ending === "ed") {
    if (IRREGULAR_ED[h.toLowerCase()]) out = IRREGULAR_ED[h.toLowerCase()]!;
    else if (/e$/i.test(h)) out = `${h}d`;
    else if (/y$/i.test(h) && cons(h.at(-2))) out = `${h.slice(0, -1)}ied`;
    else out = `${h}ed`;
  } else if (pos === "verb" && ending === "ing") {
    if (/[^e]e$/i.test(h)) out = `${h.slice(0, -1)}ing`;
    else out = `${h}ing`;
  }
  return [out, ...rest].join(" ");
}

/** 정답이 문장 첫머리라 대문자면 보기도 대문자로 */
const caseLike = (answer: string, word: string) =>
  /^[A-Z]/.test(answer) ? word.charAt(0).toUpperCase() + word.slice(1) : word;

/**
 * 빈칸 보기 — 정답과 같은 품사, 같은 단어 수, 같은 꼴(-s/-ed/-ing).
 * 같은 품사가 셋이 안 되면 단어 수만 맞춘 것으로 채운다
 */
export function blankOptions(
  word: VocabEntry,
  answer: string,
  pool: { en: string; ko: string }[],
  rand: () => number = Math.random,
): string[] {
  const pos = posOf(word.ko);
  const ending = endingOf(word.en, answer);
  const size = answer.split(/\s+/).length;
  const others = pool.filter((p) => p.en.toLowerCase() !== word.en.toLowerCase());
  const sameSize = others.filter((p) => p.en.split(/\s+/).length === size);
  const samePos = sameSize.filter((p) => posOf(p.ko) === pos);
  const chosen = shuffle(samePos, rand).slice(0, 3);
  if (chosen.length < 3) {
    const fill = shuffle(sameSize.length >= 3 ? sameSize : others, rand).filter((p) => !chosen.includes(p));
    chosen.push(...fill.slice(0, 3 - chosen.length));
  }
  const shaped = chosen.map((p) => caseLike(answer, inflect(p.en, ending, posOf(p.ko))));
  return shuffle([answer, ...new Set(shaped.filter((o) => o.toLowerCase() !== answer.toLowerCase()))], rand);
}

/**
 * 오답 보기 재료 — 단어장 + 모든 레슨의 마무리 단어(key_words).
 * 문장 뜻풀이(glosses)는 「그것들의」 같은 조각이 많아 보기로 어색해서 쓰지 않는다
 */
export function distractorPool(vocab: VocabEntry[], lessons: PolicyLesson[] = allPolicyLessons()): { en: string; ko: string }[] {
  const all = [
    ...vocab,
    ...lessons.flatMap((l) => [
      ...(l.key_words?.passage ?? []),
      ...(l.key_words?.options ?? []),
    ]),
  ];
  const seen = new Set<string>();
  const pool: { en: string; ko: string }[] = [];
  for (const g of all) {
    const en = g.en.trim();
    const ko = meaningOf(g.ko);
    // 긴 구절은 보기로 어색하다 — 세 단어까지
    if (!en || !ko || en.split(/\s+/).length > 3 || seen.has(keyOf(en))) continue;
    seen.add(keyOf(en));
    pool.push({ en, ko });
  }
  return pool;
}

/* ── 문제 만들기 ──────────────────────────────────────────────────── */

export type Question =
  | { kind: "match"; pairs: { en: string; ko: string }[] }
  | { kind: "meaning"; en: string; answer: string; options: string[] }
  | ({ kind: "blank"; en: string; answer: string; options: string[] } & BlankSource);

/** 한 번에 보는 단어 수. 많이 저장했으면 아직 덜 본 · 많이 틀린 단어부터 */
export const TEST_SIZE = 12;
const MATCH_SIZE = 4;

function shuffle<T>(xs: T[], rand: () => number): T[] {
  const a = [...xs];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [a[i], a[j]] = [a[j]!, a[i]!];
  }
  return a;
}

function optionsWith(answer: string, others: string[], rand: () => number): string[] {
  const picked = shuffle(
    [...new Set(others.filter((o) => o.toLowerCase() !== answer.toLowerCase()))],
    rand,
  ).slice(0, 3);
  return shuffle([answer, ...picked], rand);
}

/** 테스트에 넣을 단어 — 덜 본 단어, 틀린 비율이 높은 단어, 최근 저장한 단어 순 */
export function pickWords(
  vocab: VocabEntry[],
  stats: Record<string, WordStat>,
  size = TEST_SIZE,
): VocabEntry[] {
  const weak = (w: VocabEntry) => {
    const s = statOf(stats, w.en);
    return s.seen === 0 ? 2 : s.wrong / s.seen;
  };
  return [...vocab]
    .sort((a, b) => weak(b) - weak(a) || b.savedAt.localeCompare(a.savedAt))
    .slice(0, size);
}

/**
 * 단어마다 문제 유형을 돌아가며 정하고(짝 → 뜻 → 빈칸), 유형이 번갈아 나오게 늘어놓는다.
 * 빈칸 문장이 없는 단어는 뜻 고르기로, 짝이 하나뿐이면 그 단어도 뜻 고르기로.
 */
export function buildQuestions(
  words: VocabEntry[],
  pool: { en: string; ko: string }[],
  lessons: PolicyLesson[] = allPolicyLessons(),
  rand: () => number = Math.random,
): Question[] {
  const matchWords: VocabEntry[] = [];
  const meaning: Question[] = [];
  const blank: Question[] = [];

  const meaningQ = (w: VocabEntry): Question => {
    const answer = meaningOf(w.ko);
    return { kind: "meaning", en: w.en, answer, options: optionsWith(answer, pool.map((p) => p.ko), rand) };
  };

  shuffle(words, rand).forEach((w, i) => {
    const type = i % 3;
    if (type === 0) return void matchWords.push(w);
    if (type === 2) {
      const src = blankSourceOf(w, lessons);
      if (src) {
        // 보기는 단어 꼴 그대로 — 문장에 쓰인 꼴이 정답
        const answer = src.form;
        const options = blankOptions(w, answer, pool, rand);
        return void blank.push({ kind: "blank", en: w.en, ...src, answer, options });
      }
    }
    meaning.push(meaningQ(w));
  });

  const rounds: Question[] = [];
  for (let i = 0; i < matchWords.length; i += MATCH_SIZE) {
    const group = matchWords.slice(i, i + MATCH_SIZE);
    if (group.length < 2) {
      group.forEach((w) => meaning.push(meaningQ(w)));
      continue;
    }
    rounds.push({ kind: "match", pairs: group.map((w) => ({ en: w.en, ko: meaningOf(w.ko) })) });
  }

  // 유형이 고루 섞이게 하나씩 번갈아 꺼낸다
  const queues = [rounds, meaning, blank];
  const out: Question[] = [];
  while (queues.some((q) => q.length)) {
    for (const q of queues) {
      const next = q.shift();
      if (next) out.push(next);
    }
  }
  return out;
}

/** 이 문제에서 기록을 남길 단어들 */
export function wordsOf(q: Question): string[] {
  return q.kind === "match" ? q.pairs.map((p) => p.en) : [q.en];
}
