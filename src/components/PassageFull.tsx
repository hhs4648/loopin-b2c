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
};

/**
 * 문제지처럼 지문을 한 덩어리로 쭉 보여 준다. 문장 번호도, 장 넘기기도 없다 —
 * 학생이 처음 보는 건 실제 시험지 모양이어야 「무슨 문제인지」 바로 안다.
 */
export function PassageFull({ given, sentences, underline, options, onPick, picked, right }: Props) {
  const NUM = "①②③④⑤";
  return (
    <div className="passage-full">
      {given ? <p className="passage-given">{given}</p> : null}
      <p className="passage-text">
        {sentences.map((text, i) => (
          <span key={i}>
            {underlined(text, underline)}
            {i < sentences.length - 1 ? " " : ""}
          </span>
        ))}
      </p>
      {options?.length ? (
        <ol className={`passage-options${onPick ? " pickable" : ""}`}>
          {options.map((o, i) => (
            <li key={o} className={picked === String(i + 1) ? "picked" : right === String(i + 1) ? "right" : undefined}>
              {onPick ? (
                <button type="button" className="passage-pick" onClick={() => onPick(o)}>
                  <b>{NUM[i]}</b> {o}
                </button>
              ) : (
                <>
                  <b>{NUM[i]}</b> {o}
                </>
              )}
            </li>
          ))}
        </ol>
      ) : null}
    </div>
  );
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
