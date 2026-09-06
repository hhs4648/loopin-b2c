import type { ProperNoun, WordGloss } from "../../content/tutor/types";
import { nounKind } from "./proper-nouns";

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
