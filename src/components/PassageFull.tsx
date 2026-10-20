import type { ReactNode } from "react";

type Props = {
  /** 시험 문제 글 (「다음 글의 밑줄 친 부분 중, 어법상 틀린 것은?」) — 있으면 맨 위에 */
  question?: string | null;
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
  /** 노랗게 칠할 핵심어 — 답을 고를 때 읽기 편하게 */
  highlight?: string[];
  /** 문장마다 따로 칠할 핵심어 (문장 글 → 핵심어). 같은 단어가 다른 문장에 또 나와도 그 문장에서만 칠한다 */
  highlightBy?: Record<string, string[]>;
};

/**
 * 문제지처럼 지문을 한 덩어리로 쭉 보여 준다. 문장 번호도, 장 넘기기도 없다 —
 * 학생이 처음 보는 건 실제 시험지 모양이어야 「무슨 문제인지」 바로 안다.
 */
export function PassageFull({ question, given, sentences, underline, options, onPick, picked, right, numbersOnly, highlight = [], highlightBy = {} }: Props) {
  const NUM = "①②③④⑤";
  // 핵심어를 칠하는 화면(답 고르기) — 핵심어가 없는 문장의 ①~⑤도 굵게
  const keyMode = highlight.length > 0 || Object.keys(highlightBy).length > 0;
  return (
    <div className="passage-full">
      {question ? <p className="passage-question">{question}</p> : null}
      {given ? <p className="passage-given">{underlined(given, [], [...highlight, ...(highlightBy[given] ?? [])], keyMode)}</p> : null}
      {/* 순서 문제처럼 (A)·(B)·(C)로 시작하는 문장에서 단락을 나눈다 — 시험지 모양 그대로 */}
      {paragraphs(sentences).map((para, k) => (
        <p key={k} className="passage-text">
          {para.map((text, i) => (
            <span key={i}>
              {underlined(text, underline, [...highlight, ...(highlightBy[text] ?? [])], keyMode)}
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
    if (!out.length || /^\([A-E]\)/.test(text)) out.push([]);
    out[out.length - 1]!.push(text);
  }
  return out;
}

function underlined(text: string, phrases: string[], marks: string[] = [], boldNums = marks.length > 0) {
  type Hit = { a: number; b: number; kind: "u" | "mark" | "num" };
  const find = (p: string, kind: Hit["kind"]): Hit | null => {
    const at = p ? text.indexOf(p) : -1;
    return at < 0 ? null : { a: at, b: at + p.length, kind };
  };
  // 칠한 핵심어끼리 겹치면(the information … / one simply cannot … the information) 한 덩어리로 합친다
  const marked = marks
    .map((p) => find(p, "mark"))
    .filter((h): h is Hit => !!h)
    .sort((x, y) => x.a - y.a)
    .reduce<Hit[]>((acc, h) => {
      const last = acc[acc.length - 1];
      if (last && h.a <= last.b) last.b = Math.max(last.b, h.b);
      else acc.push({ ...h });
      return acc;
    }, []);
  const hits = [
    ...phrases.map((p) => find(p, "u")).filter((h): h is Hit => !!h),
    ...marked,
    // 핵심어를 칠하는 화면(답 고르기)에서는 ①~⑤ 자리도 굵게 — 어디에 넣을지 눈에 띄게
    ...(boldNums ? [...text.matchAll(/\([①②③④⑤]\)/g)].map((m) => ({ a: m.index!, b: m.index! + m[0].length, kind: "num" as const })) : []),
  ].sort((x, y) => x.a - y.a);
  if (!hits.length) return text;
  const out: ReactNode[] = [];
  let pos = 0;
  for (const { a, b, kind } of hits) {
    if (a < pos) continue;
    const p = text.slice(a, b);
    out.push(
      text.slice(pos, a),
      kind === "u" ? (
        <u key={a} className="read-underline">{p}</u>
      ) : kind === "num" ? (
        <b key={a} className="passage-num">{p}</b>
      ) : (
        <mark key={a} className="passage-key">{p}</mark>
      ),
    );
    pos = b;
  }
  out.push(text.slice(pos));
  return <>{out}</>;
}
