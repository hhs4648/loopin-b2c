import { useEffect, useRef, type ReactNode } from "react";

/**
 * 미니 모의고사 지문에 표시하며 읽기 — 낱말마다 data-i(문항 안 차례)가 붙어 있다.
 *
 * 위의 펜을 고르고 낱말을 **한 번 두드린다** (두 번 두드리기·길게 누르기는 번거로워서 뺐다, 2026-10-20 선생님):
 * - 보라펜(`unk`): 모르는 단어 — 밑줄이 그어지고 뜻이 잠깐 뜬다. 이미 표시된 낱말을 다시 두드리면 뺀다
 * - 형광펜(`hi`): 두드리면 그 낱말, 끌면 지나간 낱말들을 칠한다. 칠해진 낱말에서 시작하면 지우개
 * - 펜 없음: 보라펜으로 표시해 둔 낱말을 두드리면 뜻만 다시 뜬다
 */
export type Marks = { hi: number[]; unk: { i: number; en: string; ko: string }[] };
export const NO_MARKS: Marks = { hi: [], unk: [] };

export type Pen = "none" | "unk" | "hi";

/** 지문 위에 더 보여 주는 것 — 끊어읽기(/)와 핵심어 (분석 레슨의 slashes · emphasis) */
export type Overlay = { slashes: string[]; keys: string[] };
export const NO_OVERLAY: Overlay = { slashes: [], keys: [] };

export function MarkArea({
  pen,
  marks,
  onHighlight,
  onUnknown,
  onTapUnknown,
  children,
}: {
  pen: Pen;
  marks: Marks;
  onHighlight: (hi: number[]) => void;
  /** 보라펜으로 두드림 — i = 낱말 차례, token = 보이는 낱말, el = 그 낱말 (문장 찾기용) */
  onUnknown: (i: number, token: string, el: HTMLElement) => void;
  /** 펜 없이 표시된 낱말을 두드림 — 뜻만 보여 준다 */
  onTapUnknown: (i: number) => void;
  children: ReactNode;
}) {
  const box = useRef<HTMLDivElement>(null);
  const latest = useRef({ pen, marks, onHighlight, onUnknown, onTapUnknown });
  latest.current = { pen, marks, onHighlight, onUnknown, onTapUnknown };
  const press = useRef<{ i: number; x: number; y: number; moved: number; mode: "paint" | "erase" | null; base: number[] } | null>(null);

  const wordAt = (x: number, y: number) =>
    (document.elementFromPoint(x, y) as HTMLElement | null)?.closest<HTMLElement>("[data-i]") ?? null;

  const paint = (to: number) => {
    const p = press.current;
    if (!p?.mode) return;
    const [a, b] = p.i <= to ? [p.i, to] : [to, p.i];
    const range = new Set<number>();
    for (let k = a; k <= b; k++) range.add(k);
    const next = p.mode === "paint" ? [...new Set([...p.base, ...range])] : p.base.filter((k) => !range.has(k));
    latest.current.onHighlight(next.sort((x, y) => x - y));
  };

  // 형광펜으로 칠하는 동안은 화면이 스크롤되지 않게 — passive가 아닌 touchmove라야 막힌다
  useEffect(() => {
    const el = box.current;
    if (!el) return;
    const stop = (e: TouchEvent) => {
      if (press.current?.mode) e.preventDefault();
    };
    el.addEventListener("touchmove", stop, { passive: false });
    return () => el.removeEventListener("touchmove", stop);
  }, []);

  return (
    <div
      ref={box}
      className={`mini-markable pen-${pen}`}
      onContextMenu={(e) => e.preventDefault()}
      onPointerDown={(e) => {
        const w = (e.target as HTMLElement).closest<HTMLElement>("[data-i]");
        if (!w || (e.pointerType === "mouse" && e.button !== 0)) return;
        const i = Number(w.dataset.i);
        press.current = { i, x: e.clientX, y: e.clientY, moved: 0, mode: null, base: [] };
        if (latest.current.pen === "hi") {
          const p = press.current;
          p.mode = latest.current.marks.hi.includes(i) ? "erase" : "paint";
          p.base = latest.current.marks.hi;
          paint(i);
        }
      }}
      onPointerMove={(e) => {
        const p = press.current;
        if (!p) return;
        p.moved = Math.max(p.moved, Math.hypot(e.clientX - p.x, e.clientY - p.y));
        if (!p.mode) return;
        const w = wordAt(e.clientX, e.clientY);
        if (w && box.current?.contains(w)) paint(Number(w.dataset.i));
      }}
      onPointerUp={(e) => {
        const p = press.current;
        press.current = null;
        if (!p || p.mode || p.moved > 10) return;
        const pen = latest.current.pen;
        const w = (e.target as HTMLElement).closest<HTMLElement>("[data-i]") ?? box.current?.querySelector<HTMLElement>(`[data-i="${p.i}"]`);
        if (!w) return;
        if (pen === "unk") latest.current.onUnknown(p.i, w.textContent ?? "", w);
        else if (latest.current.marks.unk.some((u) => u.i === p.i)) latest.current.onTapUnknown(p.i);
      }}
      onPointerCancel={() => {
        press.current = null;
      }}
    >
      {children}
    </div>
  );
}

const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/** 글 안에서 구절들이 차지하는 [시작, 끝) — 구절은 레슨에 적힌 그대로(문장부호 포함). 낱말 경계를 지킨다(「but」이 attributes에 걸리지 않게) */
function ranges(text: string, phrases: string[]): [number, number][] {
  const out: [number, number][] = [];
  for (const p of phrases) {
    if (!p) continue;
    const re = new RegExp(`${/^\w/.test(p) ? "\\b" : ""}${esc(p)}${/\w$/.test(p) ? "\\b" : ""}`, "g");
    for (let m = re.exec(text); m; m = re.exec(text)) out.push([m.index, m.index + m[0].length]);
  }
  return out;
}

/**
 * 지문 글을 낱말 단위로 — counter는 문항 안에서 이어지는 낱말 차례.
 * overlay가 있으면 핵심어 낱말에 `key`를, 끊어읽기 구절 끝 낱말 뒤에 「/」를 넣는다 (「/」는 낱말로 세지 않는다 — 표시 차례가 밀리지 않게)
 */
export function markWords(text: string, keyBase: string, counter: { n: number }, marks: Marks | null, overlay: Overlay = NO_OVERLAY): ReactNode[] {
  if (!marks) return [text];
  const hi = new Set(marks.hi);
  const unk = new Set(marks.unk.map((u) => u.i));
  const keyRanges = ranges(text, overlay.keys);
  const slashEnds = new Set(ranges(text, overlay.slashes).map(([, b]) => b));
  const out: ReactNode[] = [];
  let pos = 0;
  text.split(/(\s+)/).forEach((tok, k) => {
    const start = pos;
    pos += tok.length;
    if (!tok) return;
    if (/^\s+$/.test(tok)) {
      // 칠한 낱말 사이 빈칸도 이어 칠해 한 줄로 보이게
      const on = hi.has(counter.n - 1) && hi.has(counter.n);
      out.push(<span key={`${keyBase}-${k}`} className={on ? "mini-sp on" : "mini-sp"}>{tok}</span>);
      return;
    }
    const i = counter.n++;
    const isKey = keyRanges.some(([a, b]) => a < pos && b > start);
    const cls = `mini-w${hi.has(i) ? " on" : ""}${unk.has(i) ? " unk" : ""}${isKey ? " key" : ""}`;
    out.push(<span key={`${keyBase}-${k}`} data-i={i} className={cls}>{tok}</span>);
    // 구절이 낱말 중간(문장부호 앞)에서 끝나도 그 낱말 뒤에 긋는다
    if ([...slashEnds].some((e) => e > start && e <= pos)) out.push(<span key={`${keyBase}-${k}s`} className="mini-slash" aria-hidden="true"> /</span>);
  });
  return out;
}
