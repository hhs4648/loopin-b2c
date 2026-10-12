import type { ReactNode } from "react";

type Props = {
  /** 문장 넣기 문제의 「주어진 문장」 — 지문 위에 따로 상자로 */
  given?: string | null;
  sentences: string[];
  underline: string[];
  /** 있으면 지문 아래 시험 보기 */
  options?: string[] | null;
  /** 있으면 보기를 눌러 답을 고른다 (바로 풀기) */
  onPick?: ((label: string) => void) | null;
  /** 고른 보기 번호 ("1"~"5") — 틀렸으면 표시가 남는다 */
  picked?: string | null;
  /** 맞힌 보기 번호 — 초록으로 */
  right?: string | null;
  /** 보기 글 없이 숫자 ①~⑤만 가로로 (문장 넣기) */
  numbersOnly?: boolean;
};

/**
 * 문제지처럼 지문을 한 덩어리로 쭉 보여 준다. 문장 번호도, 장 넘기기도 없다 —
 * 학생이 처음 보는 건 실제 시험지 모양이어야 「무슨 문제인지」 바로 안다.
 */
export function PassageFull({ given, sentences, underline, options, onPick, picked, right, numbersOnly }: Props) {
  const NUM = "①②③④⑤";
  return (
    <div className="passage-full">
      {given ? <p className="passage-given">{given}</p> : null}
      {/* 순서 문제처럼 (A)·(B)·(C)로 시작하는 문장에서 단락을 나눈다 — 시험지 모양 그대로 */}
      {paragraphs(sentences).map((para, k) => (
        <p key={k} className="passage-text">
          {para.map((text, i) => (
            <span key={i}>
              {underlined(text, underline)}
              {i < para.length - 1 ? " " : ""}
            </span>
          ))}
        </p>
      ))}
      {options?.length ? (
        <ol className={`passage-options${onPick ? " pickable" : ""}${numbersOnly ? " numbers" : ""}`}>
          {options.map((o, i) => (
            <li key={o} className={picked === String(i + 1) ? "picked" : right === String(i + 1) ? "right" : undefined}>
              {onPick ? (
                <button type="button" className="passage-pick" aria-label={numbersOnly ? `${NUM[i]} ${o}` : undefined} onClick={() => onPick(o)}>
                  <b>{NUM[i]}</b> {numbersOnly ? null : o}
                </button>
              ) : (
                <>
                  <b>{NUM[i]}</b> {numbersOnly ? null : o}
                </>
              )}
            </li>
          ))}
        </ol>
      ) : null}
    </div>
  );
}

function paragraphs(sentences: string[]): string[][] {
  const out: string[][] = [];
  for (const text of sentences) {
    if (!out.length || /^\([A-C]\)/.test(text)) out.push([]);
    out[out.length - 1]!.push(text);
  }
  return out;
}

function underlined(text: string, phrases: string[]) {
  const hits = phrases
    .map((p) => [text.indexOf(p), p] as const)
    .filter(([at]) => at >= 0)
    .sort((a, b) => a[0] - b[0]);
  if (!hits.length) return text;
  const out: ReactNode[] = [];
  let pos = 0;
  for (const [at, p] of hits) {
    if (at < pos) continue;
    out.push(text.slice(pos, at), <u key={at} className="read-underline">{p}</u>);
    pos = at + p.length;
  }
  out.push(text.slice(pos));
  return <>{out}</>;
}
