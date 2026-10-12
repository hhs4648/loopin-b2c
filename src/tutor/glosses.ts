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

const WORDS = (wordBook as { words: Record<string, string> }).words;

/**
 * 구절 뜻(「lift the veil」 = 장막을 걷어 내다)을 단어마다 나눈다 — 학생은 단어를 따로 외운다.
 * 단어 뜻은 레슨에 그 단어 뜻이 있으면 그것, 없으면 공용 단어 사전(`word-glosses.json`).
 * 뜻 옆에 「· lift the veil = 장막을 걷어 내다」처럼 구절 뜻을 붙인다. 뜻을 모르는 단어(the, of, 이름)는 그냥 글자.
 * `keep`에 든 구절(지금 통째로 고르는 후보)은 나누지 않는다.
 */
export function splitPhraseGlosses(glosses: WordGloss[], keep: string[] = []): WordGloss[] {
  const keepSet = new Set(keep.map((k) => k.toLowerCase()));
  const singles = new Map<string, WordGloss>();
  for (const g of glosses) if (!/\s/.test(g.en.trim())) singles.set(g.en.toLowerCase(), g);
  const out: WordGloss[] = [];
  const added = new Set<string>();
  for (const g of glosses) {
    const words = g.en.trim().split(/\s+/);
    if (words.length < 2 || keepSet.has(g.en.toLowerCase())) {
      out.push(g);
      continue;
    }
    const phraseKo = g.ko.split(" · ")[0];
    for (const raw of words) {
      const w = raw.replace(/^[“"‘'(]+|[”"’'),.;:!?]+$/g, "");
      const key = w.toLowerCase();
      if (!w || added.has(key)) continue;
      const own = singles.get(key)?.ko ?? WORDS[key];
      if (!own) continue;
      added.add(key);
      // 레슨에 이미 그 단어 뜻이 있으면 그대로 두고(따로 들어가 있다), 사전 뜻이면 구절 뜻을 붙여 넣는다
      if (!singles.has(key)) out.push({ ...g, en: w, ko: `${own.split(" · ")[0]} · ${g.en} = ${phraseKo}` });
    }
  }
  return out;
}
