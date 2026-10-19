import type { ProperNoun, WordGloss } from "../../content/tutor/types";
import { nounKind } from "./proper-nouns";
import wordBook from "../../content/tutor/word-glosses.json";

export type GlossSpan = {
  text: string;
  gloss: WordGloss | null;
};

function glossRegex(en: string): RegExp {
  const escaped = en.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\\s+/g, "\\s+");
  return new RegExp(`^(${escaped})(?![A-Za-z0-9])`, "i");
}

/**
 * 문장을 토큰으로 나누고, 레슨 JSON의 뜻을 붙인다.
 *
 * 긴 구(`the past four years`)가 짧은 단어(`the`)보다 먼저 맞는다.
 * 뜻이 없는 칸(공백·쉼표)은 그대로 둔다.
 */
export function glossSpans(sentence: string, glosses: WordGloss[]): GlossSpan[] {
  const sorted = [...glosses].sort(
    (a, b) => b.en.length - a.en.length || b.en.split(/\s+/).length - a.en.split(/\s+/).length,
  );
  const spans: GlossSpan[] = [];
  let i = 0;
  while (i < sentence.length) {
    const rest = sentence.slice(i);
    const ws = rest.match(/^\s+/);
    if (ws) {
      spans.push({ text: ws[0], gloss: null });
      i += ws[0].length;
      continue;
    }
    let hit: { gloss: WordGloss; len: number } | null = null;
    for (const g of sorted) {
      const m = rest.match(glossRegex(g.en));
      if (m?.[1]) {
        hit = { gloss: g, len: m[1].length };
        break;
      }
    }
    if (hit) {
      spans.push({ text: rest.slice(0, hit.len), gloss: hit.gloss });
      i += hit.len;
      continue;
    }
    const tok = rest.match(/^[A-Za-z0-9]+(?:['.][A-Za-z0-9]+)*/)?.[0] ?? rest[0]!;
    spans.push({ text: tok, gloss: null });
    i += tok.length;
  }
  return spans;
}

/** 「company가 뭐예요?」처럼 단어만 집어 뜻을 찾을 때 */
export function lookupGloss(word: string, glosses: WordGloss[] | undefined): WordGloss | null {
  if (!glosses?.length) return null;
  const needle = word.toLowerCase().replace(/[.,!?;:]+$/g, "");
  const exact = glosses.find((g) => g.en.toLowerCase() === needle);
  if (exact) return exact;
  return (
    glosses.find((g) =>
      g.en
        .toLowerCase()
        .split(/\s+/)
        .some((w) => w.replace(/[.,]+$/g, "") === needle),
    ) ?? null
  );
}

/** JSON에 빠진 고유명사는 칩과 같은 말로 채운다 */
export function glossesFor(chunkGlosses: WordGloss[] | undefined, nouns: ProperNoun[]): WordGloss[] {
  const listed = chunkGlosses ?? [];
  const extra = nouns
    .filter((n) => !listed.some((g) => g.en.toLowerCase() === n.en.toLowerCase()))
    .map((n) => ({ en: n.en, ko: `${nounKind(n.type)} · 그대로` }));
  return [...listed, ...extra];
}

export const WORDS = (wordBook as { words: Record<string, string> }).words;

/**
 * 구절 뜻(「lift the veil」 = 장막을 걷어 내다)을 단어마다 나눈다 — 학생은 단어를 따로 외운다.
 * 단어 뜻은 레슨에 그 단어 뜻이 있으면 그것, 없으면 공용 단어 사전(`word-glosses.json`).
 * 단어 뜻(`ko`)과 그 단어가 들어간 덩어리(`phrase`)를 따로 준다 — 뜻 상자 윗줄·아랫줄, 별도 따로.
 * 관사(a, an, the)는 그냥 글자. to·of 같은 기능어는 단어 뜻 없이 덩어리 뜻만.
 * `keep`에 든 구절(지금 통째로 고르는 후보)은 나누지 않는다.
 */
const ARTICLES = new Set(["a", "an", "the"]);
/**
 * 단어 뜻이 없어도 되는 말 — 관사·접속사·대명사처럼 덩어리 안에서만 뜻이 생기는 말.
 * 이 밖의 단어(내용어)는 덩어리 안에 있어도 단어 뜻이 있어야 한다 (규칙 테스트가 검사)
 */
export const FUNCTION_WORDS = new Set([
  "a", "an", "the", "and", "or", "but", "so", "nor", "yet", "if", "than", "all", "both", "each", "every", "either",
  "neither", "some", "any", "no", "such", "own", "same", "other", "else", "another", "here", "there", "those", "it",
  "its", "itself", "they", "them", "their", "themselves", "he", "him", "his", "she", "her", "we", "us", "our", "you",
  "your", "yourself", "i", "me", "my", "one", "ones", "who", "whom", "whose", "something", "anything", "everything",
  "everyone", "someone", "just", "too", "very", "quite", "really", "also", "even", "much",
]);
/** 사전에 있어도 덩어리 안에서는 그 덩어리 뜻으로만 보이는 기능어 (2026-10-14: to make의 to가 '~로, ~에게'로 떴다) */
export const CONTEXT_WORDS = new Set([
  "to", "of", "for", "in", "on", "with", "from", "into", "at", "by", "as", "about", "toward", "towards",
  "be", "is", "are", "was", "were", "been", "being", "has", "have", "had", "do", "does", "did", "not",
  "will", "would", "may", "might", "can", "could", "should", "must", "which", "that", "it", "this", "these",
]);

export function splitPhraseGlosses(glosses: WordGloss[], keep: string[] = []): WordGloss[] {
  const keepSet = new Set(keep.map((k) => k.toLowerCase()));
  /** 줄임말 조각이 찾을 후보인가 — ’s 그대로, 또는 ’ve been driving처럼 그 조각으로 시작하는 덩어리 */
  const keepsPiece = (piece: string) => [...keepSet].some((k) => k === piece || k.startsWith(`${piece} `));
  const singles = new Map<string, WordGloss>();
  for (const g of glosses) if (!/\s/.test(g.en.trim())) singles.set(g.en.toLowerCase(), g);
  /** 단어 → 그 단어가 처음 들어간 덩어리 (뜻 상자 아랫줄 「덩어리」) */
  const phraseOf = new Map<string, { en: string; ko: string }>();
  const out: WordGloss[] = [];
  const added = new Set<string>();
  for (const g of glosses) {
    const words = g.en.trim().split(/\s+/);
    const cut0 = g.en.indexOf("’");
    // 줄임말 통째 뜻(it’s)은 빼고 조각(it, ’s)으로 누르게 — 두 조각이 다 찾을 후보일 때
    if (words.length === 1 && cut0 > 0 && keepSet.has(g.en.slice(0, cut0).toLowerCase()) && keepsPiece(g.en.slice(cut0).toLowerCase())) continue;
    if (words.length < 2 || keepSet.has(g.en.toLowerCase())) {
      out.push(g);
      continue;
    }
    const phrase = { en: g.en, ko: g.ko.split(" · ")[0] };
    for (const raw of words) {
      const w = raw.replace(/^[“"‘'(]+|[”"’'),.;:!?]+$/g, "");
      const key = w.toLowerCase();
      if (!w) continue;
      // 줄임말을 주어·동사로 나눠 찾을 때(it’s → it + ’s) — 두 조각이 다 찾을 후보면 조각으로 둔다
      const cut = w.indexOf("’");
      if (cut > 0 && keepSet.has(w.slice(0, cut).toLowerCase()) && keepsPiece(w.slice(cut).toLowerCase())) {
        for (const part of [w.slice(0, cut), w.slice(cut)]) {
          const k = part.toLowerCase();
          if (added.has(k)) continue;
          added.add(k);
          if (!singles.has(k)) out.push({ en: part, ko: "", phrase });
        }
        continue;
      }
      if (!phraseOf.has(key)) phraseOf.set(key, phrase);
      if (added.has(key)) continue;
      // to, of, for 같은 짧은 기능어는 뜻이 문맥마다 달라서 사전 뜻을 쓰지 않는다 — 덩어리 뜻만 (to make = 만들기 위해)
      const own = singles.get(key)?.ko ?? (CONTEXT_WORDS.has(key) ? undefined : WORDS[key]);
      if (!own) {
        // 단어 뜻이 없어도 누르면 덩어리 뜻은 보이게 — 관사(a, an, the)만 뺀다
        if (ARTICLES.has(key)) continue;
        added.add(key);
        out.push({ en: w, ko: "", phrase });
        continue;
      }
      added.add(key);
      // 레슨에 그 단어 뜻이 따로 있으면 그걸 쓴다(아래에서 덩어리를 붙인다). 없으면 사전 뜻 + 덩어리
      if (!singles.has(key)) out.push({ en: w, ko: own, phrase });
    }
  }
  // 레슨에 따로 적은 단어 뜻에도, 그 단어가 들어간 덩어리를 아랫줄로 붙인다
  return out.map((g) => {
    if (g.phrase || /\s/.test(g.en.trim())) return g;
    const phrase = phraseOf.get(g.en.toLowerCase());
    return phrase ? { ...g, phrase } : g;
  });
}
