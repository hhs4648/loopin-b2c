import { useEffect, useRef, type ReactNode } from "react";

/**
 * 미니 모의고사 지문에 표시하며 읽기 — 낱말마다 data-i(문항 안 차례)가 붙어 있다.
 * - 두 번 두드리기: 모르는 단어 (한 번 더 두 번 두드리면 뺀다)
 * - 길게 누르기(터치) · 끌기(마우스): 형광펜. 누른 낱말이 칠해져 있으면 지우개로 끈다
 * 한 번 두드리기는 아무것도 안 한다(스크롤·고르기와 안 겹치게).
 */
export type Marks = { hi: number[]; unk: { i: number; en: string; ko: string }[] };
export const NO_MARKS: Marks = { hi: [], unk: [] };

const LONG_MS = 420;
const DOUBLE_MS = 350;

export function MarkArea({
  marks,
  onHighlight,
  onUnknown,
  children,
}: {
  marks: Marks;
  onHighlight: (hi: number[]) => void;
  /** i = 낱말 차례, token = 보이는 낱말, el = 그 낱말 (문장 찾기용) */
  onUnknown: (i: number, token: string, el: HTMLElement) => void;
  children: ReactNode;
}) {
  const box = useRef<HTMLDivElement>(null);
  const latest = useRef({ marks, onHighlight, onUnknown });
  latest.current = { marks, onHighlight, onUnknown };
  const press = useRef<{
    i: number; x: number; y: number; t: number; mouse: boolean;
    timer: number; mode: "paint" | "erase" | null; base: number[]; moved: number;
  } | null>(null);
  const lastTap = useRef<{ i: number; t: number } | null>(null);

  const wordAt = (x: number, y: number) =>
    (document.elementFromPoint(x, y) as HTMLElement | null)?.closest<HTMLElement>("[data-i]") ?? null;

  const paint = (to: number) => {
    const p = press.current;
    if (!p?.mode) return;
    const [a, b] = p.i <= to ? [p.i, to] : [to, p.i];
    const range = new Set<number>();
    for (let k = a; k <= b; k++) range.add(k);
    const next = p.mode === "paint"
      ? [...new Set([...p.base, ...range])]
      : p.base.filter((k) => !range.has(k));
    latest.current.onHighlight(next.sort((x, y) => x - y));
  };
  const begin = () => {
    const p = press.current;
    if (!p || p.mode) return;
    p.mode = latest.current.marks.hi.includes(p.i) ? "erase" : "paint";
    p.base = latest.current.marks.hi;
    navigator.vibrate?.(8);
    paint(p.i);
  };

  // 칠하는 동안은 화면이 스크롤되지 않게 — passive가 아닌 touchmove라야 막힌다
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
      className="mini-markable"
      onContextMenu={(e) => e.preventDefault()}
      onPointerDown={(e) => {
        const w = (e.target as HTMLElement).closest<HTMLElement>("[data-i]");
        if (!w || (e.pointerType === "mouse" && e.button !== 0)) return;
        if (press.current) window.clearTimeout(press.current.timer);
        press.current = {
          i: Number(w.dataset.i), x: e.clientX, y: e.clientY, t: Date.now(), mouse: e.pointerType === "mouse",
          timer: window.setTimeout(begin, LONG_MS), mode: null, base: [], moved: 0,
        };
      }}
      onPointerMove={(e) => {
        const p = press.current;
        if (!p) return;
        p.moved = Math.max(p.moved, Math.hypot(e.clientX - p.x, e.clientY - p.y));
        if (!p.mode) {
          if (p.mouse && p.moved > 6) begin();
          else if (p.moved > 10) {
            // 손가락으로 스크롤하는 중
            window.clearTimeout(p.timer);
            press.current = null;
          }
          return;
        }
        const w = wordAt(e.clientX, e.clientY);
        if (w && box.current?.contains(w)) paint(Number(w.dataset.i));
      }}
      onPointerUp={(e) => {
        const p = press.current;
        press.current = null;
        if (!p) return;
        window.clearTimeout(p.timer);
        if (p.mode || p.moved > 10 || Date.now() - p.t > LONG_MS) return;
        const now = Date.now();
        const last = lastTap.current;
        if (last && last.i === p.i && now - last.t < DOUBLE_MS) {
          lastTap.current = null;
          const w = (e.target as HTMLElement).closest<HTMLElement>("[data-i]") ?? box.current?.querySelector<HTMLElement>(`[data-i="${p.i}"]`);
          if (w) latest.current.onUnknown(p.i, w.textContent ?? "", w);
        } else lastTap.current = { i: p.i, t: now };
      }}
      onPointerCancel={() => {
        if (press.current) window.clearTimeout(press.current.timer);
        press.current = null;
      }}
    >
      {children}
    </div>
  );
}

/** 지문 글을 낱말 단위로 — counter는 문항 안에서 이어지는 낱말 차례 */
export function markWords(text: string, keyBase: string, counter: { n: number }, marks: Marks | null): ReactNode[] {
  if (!marks) return [text];
  const hi = new Set(marks.hi);
  const unk = new Set(marks.unk.map((u) => u.i));
  const out: ReactNode[] = [];
  text.split(/(\s+)/).forEach((tok, k) => {
    if (!tok) return;
    if (/^\s+$/.test(tok)) {
      // 칠한 낱말 사이 빈칸도 이어 칠해 한 줄로 보이게
      const on = hi.has(counter.n - 1) && hi.has(counter.n);
      out.push(<span key={`${keyBase}-${k}`} className={on ? "mini-sp on" : "mini-sp"}>{tok}</span>);
      return;
    }
    const i = counter.n++;
    const cls = `mini-w${hi.has(i) ? " on" : ""}${unk.has(i) ? " unk" : ""}`;
    out.push(<span key={`${keyBase}-${k}`} data-i={i} className={cls}>{tok}</span>);
  });
  return out;
}
