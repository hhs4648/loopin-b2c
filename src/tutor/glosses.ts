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

/** JSON에 빠진 고유명사는 칩과 같은 말로 채운다. 덩어리 밖에 홀로 선 of·it·or 같은 기능어도 기본 뜻으로 누를 수 있게 */
export function glossesFor(chunkGlosses: WordGloss[] | undefined, nouns: ProperNoun[]): WordGloss[] {
  const listed = chunkGlosses ?? [];
  const has = (en: string) => listed.some((g) => g.en.toLowerCase() === en.toLowerCase());
  const extra = nouns.filter((n) => !has(n.en)).map((n) => ({ en: n.en, ko: `${nounKind(n.type)} · 그대로` }));
  const basics = Object.entries(BASIC_SENSE).filter(([en]) => !has(en)).map(([en, ko]) => ({ en, ko }));
  return [...listed, ...extra, ...basics];
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

/**
 * 기능어의 기본 뜻 — 누르면 「~의」「그것」「또는」 정도는 나온다 (2026-10-20 선생님).
 * to·for·as·that·which처럼 자리마다 뜻이 크게 다른 말은 여기 없다 — 레슨의 function-senses에 그 자리 쓰임을 적는다
 * (so·but·since처럼 여기 있는 말도 레슨에 쓰임이 적혀 있으면 그쪽이 먼저). 관사(a, an, the)는 뜻이 없다.
 * 덩어리 안에서는 덩어리 뜻이 아랫줄에 같이 보인다
 */
export const BASIC_SENSE: Record<string, string> = {
  // 전치사
  of: "~의", with: "~와 (함께), ~로", from: "~에서, ~로부터", into: "~ 안으로", about: "~에 대해",
  by: "~에 의해, ~로", in: "~ 안에, ~에서", on: "~ 위에, ~에", at: "~에(서)", over: "~ 위에, ~ 넘게",
  under: "~ 아래에", through: "~을 통해", without: "~ 없이", within: "~ 안에", among: "~ 사이에(셋 이상)",
  between: "~ 사이에", during: "~ 동안", after: "~ 후에", before: "~ 전에", until: "~까지", toward: "~을 향해", towards: "~을 향해",
  like: "~처럼", than: "~보다",
  // 대명사
  it: "그것", its: "그것의", itself: "그것 자체", they: "그들, 그것들", them: "그들을, 그것들을", their: "그들의",
  themselves: "그들 자신", he: "그는", him: "그를", his: "그의", she: "그녀는", her: "그녀를, 그녀의", we: "우리는",
  us: "우리를", our: "우리의", you: "너는, 너를", your: "너의", yourself: "너 자신", i: "나는", me: "나를", my: "나의",
  one: "하나, (앞 명사 대신) 것", ones: "(앞 명사 대신) 것들", this: "이, 이것", these: "이것들, 이러한", those: "저것들, 그",
  something: "어떤 것", anything: "무엇이든, 아무것", everything: "모든 것", everyone: "모든 사람", someone: "어떤 사람",
  who: "누구, ~하는 (사람)", whom: "누구를", whose: "누구의, ~의",
  // 접속사·연결어
  and: "그리고", or: "또는", but: "그러나", so: "그래서, 너무", nor: "~도 아니다", yet: "그러나, 아직",
  if: "만약 ~라면, ~인지", because: "~ 때문에", while: "~하는 동안, ~인 반면", since: "~ 이후로, ~ 때문에",
  although: "비록 ~이지만", though: "비록 ~이지만", whether: "~인지 아닌지", unless: "~하지 않으면",
  when: "~할 때, 언제", where: "~하는 곳, 어디", how: "어떻게, 얼마나", why: "왜", what: "무엇, ~하는 것",
  then: "그다음에, 그때", thus: "따라서", however: "그러나", therefore: "그러므로",
  // 한정사·부사
  all: "모든, 모두", both: "둘 다", each: "각각", every: "모든", either: "둘 중 하나", neither: "둘 다 아닌",
  some: "어떤, 약간의", any: "어떤 ~도, 아무", no: "아무 ~도 없는", such: "그런", own: "자신의", same: "같은",
  other: "다른", else: "그 밖에", another: "또 다른", here: "여기", there: "거기, (there is) ~이 있다",
  just: "그저, 딱", too: "너무, ~도", very: "매우", quite: "꽤", really: "정말", also: "또한", even: "심지어, ~조차",
  much: "많은, 많이", not: "~않다, ~아니다",
  // be·조동사
  be: "~이다, 있다", is: "~이다, 있다", are: "~이다, 있다", was: "~였다, 있었다", were: "~였다, 있었다",
  been: "~였다 (완료)", being: "~인 것, ~되고 있는", has: "가지고 있다, (has + 과거분사) ~했다",
  have: "가지다, (have + 과거분사) ~했다", had: "가졌다, (had + 과거분사) ~했었다", do: "하다, (do not) ~않다",
  does: "하다, (does not) ~않다", did: "했다, (did not) ~않았다", will: "~할 것이다", would: "~할 것이다, ~하곤 했다",
  may: "~일 수 있다, ~해도 된다", might: "~일지도 모른다", can: "~할 수 있다", could: "~할 수 있었다, ~일 수도 있다",
  should: "~해야 한다", must: "~해야 한다, ~임이 틀림없다",
};

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
      // to, for 같은 짧은 기능어는 뜻이 문맥마다 달라서 사전 뜻을 쓰지 않는다 — 덩어리 뜻만 (to make = 만들기 위해).
      // of·it·or 같은 기능어는 「~의」「그것」「또는」 정도의 기본 뜻은 띄운다
      const own = singles.get(key)?.ko ?? (CONTEXT_WORDS.has(key) ? BASIC_SENSE[key] : (WORDS[key] ?? BASIC_SENSE[key]));
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
