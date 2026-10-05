import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";

type Props = {
  sentences: string[];
  underline: string[];
  /** 있으면 마지막 장에 시험 보기를 보여 준다 */
  options?: string[] | null;
  /** 처음 펼칠 장 */
  start?: number;
};

/** 한 장에 담을 글자 수 — 폰 화면에서 스크롤 없이 읽힐 만큼 */
const PAGE_BUDGET = 420;

/**
 * 지문을 장으로 나눠 ‹ 1/3 › 로 넘겨 본다. 길게 스크롤하는 것보다 지금 어디쯤인지
 * 보이고, 앞 장으로 돌아가기도 쉽다. 문장 중간에서 끊지 않는다.
 */
export function PassagePager({ sentences, underline, options, start = 0 }: Props) {
  const pages = useMemo(() => {
    const out: { kind: "text"; items: { n: number; text: string }[] }[] = [];
    let cur: { n: number; text: string }[] = [];
    let size = 0;
    sentences.forEach((text, i) => {
      if (cur.length && size + text.length > PAGE_BUDGET) {
        out.push({ kind: "text", items: cur });
        cur = [];
        size = 0;
      }
      cur.push({ n: i + 1, text });
      size += text.length;
    });
    if (cur.length) out.push({ kind: "text", items: cur });
    return out;
  }, [sentences]);
  const total = pages.length + (options?.length ? 1 : 0);
  const [page, setPage] = useState(Math.min(start, total - 1));
  useEffect(() => setPage(Math.min(start, total - 1)), [start, total]);
  const NUM = "①②③④⑤";

  return (
    <div className="pager">
      <div className="pager-body">
        {page < pages.length ? (
          pages[page]!.items.map((it) => (
            <p key={it.n} className="pager-text">
              <span className="pager-n">{it.n}</span>
              {underlined(it.text, underline)}
            </p>
          ))
        ) : (
          <ol className="pager-options">
            {options!.map((o, i) => (
              <li key={o}>
                <b>{NUM[i]}</b> {o}
              </li>
            ))}
          </ol>
        )}
      </div>
      <div className="pager-nav">
        <button type="button" disabled={page === 0} onClick={() => setPage(page - 1)} aria-label="이전 장">
          ‹ 이전
        </button>
        <span>
          {page < pages.length ? "지문" : "보기"} {page + 1} / {total}
        </span>
        <button type="button" disabled={page >= total - 1} onClick={() => setPage(page + 1)} aria-label="다음 장">
          다음 ›
        </button>
      </div>
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
