import { useRef, useState } from "react";
import { phoneScale } from "./phoneScale";

type Part = string | { en: string; ko: string };

/**
 * 해석 맞추기 — 위는 영어 문장(덩어리마다 끌 수 있는 칩), 아래는 한국어 해석(칸마다 점선).
 * 영어 덩어리를 끌어 맞는 한국어 칸에 놓는다. 끌기 어려우면 덩어리를 누르고 칸을 눌러도 된다.
 * 맞으면 칸 위에 영어가 붙고 덩어리는 초록으로 남는다. 짧은 문장에만 쓴다 (2026-10-14 선생님)
 */
export function MatchKo({
  sentence,
  chunks,
  found,
  ko,
  open,
  onMatch,
}: {
  sentence: string;
  chunks: string[];
  found: string[];
  ko: Part[];
  open: boolean;
  onMatch: (slot: number, chunk: string) => void;
}) {
  const [picked, setPicked] = useState<string | null>(null);
  const [drag, setDrag] = useState<{ chunk: string; x: number; y: number; dx: number; dy: number } | null>(null);
  const moved = useRef(false);

  // 영어 문장을 덩어리와 나머지 글자로 나눈다 (문장 순서대로)
  const pieces: { text: string; chunk: boolean }[] = [];
  let rest = sentence;
  for (const c of chunks) {
    const at = rest.indexOf(c);
    if (at < 0) continue;
    if (at > 0) pieces.push({ text: rest.slice(0, at), chunk: false });
    pieces.push({ text: c, chunk: true });
    rest = rest.slice(at + c.length);
  }
  if (rest) pieces.push({ text: rest, chunk: false });

  const slotAt = (x: number, y: number) => {
    const el = document.elementsFromPoint(x, y).find((e) => e instanceof HTMLElement && e.dataset.slot) as HTMLElement | undefined;
    return el ? Number(el.dataset.slot) : null;
  };
  const mark = (slot: number | null) => {
    document.querySelectorAll(".match-slot.drop-over").forEach((e) => e.classList.remove("drop-over"));
    if (slot !== null) document.querySelector(`.match-slot[data-slot="${slot}"]`)?.classList.add("drop-over");
  };

  let slotNo = -1;
  return (
    <div className="match-ko">
      <p className="match-en">
        {pieces.map((p, i) =>
          !p.chunk ? (
            <span key={i}>{p.text}</span>
          ) : (
            <span
              key={i}
              role="button"
              tabIndex={0}
              className={`match-chunk${found.includes(p.text) ? " done" : ""}${picked === p.text ? " picked" : ""}${drag?.chunk === p.text ? " dragging" : ""}`}
              style={drag?.chunk === p.text ? { transform: `translate(${drag.dx}px, ${drag.dy}px)` } : undefined}
              onPointerDown={(e) => {
                if (!open || found.includes(p.text)) return;
                (e.target as HTMLElement).setPointerCapture(e.pointerId);
                moved.current = false;
                setDrag({ chunk: p.text, x: e.clientX, y: e.clientY, dx: 0, dy: 0 });
              }}
              onPointerMove={(e) => {
                if (!drag || drag.chunk !== p.text) return;
                const s = phoneScale(e.currentTarget);
                const dx = (e.clientX - drag.x) / s;
                const dy = (e.clientY - drag.y) / s;
                if (Math.abs(dx) + Math.abs(dy) > 6) moved.current = true;
                setDrag({ ...drag, dx, dy });
                mark(slotAt(e.clientX, e.clientY));
              }}
              onPointerUp={(e) => {
                if (!drag || drag.chunk !== p.text) return;
                const slot = slotAt(e.clientX, e.clientY);
                mark(null);
                setDrag(null);
                if (moved.current) {
                  if (slot !== null) onMatch(slot, p.text);
                  setPicked(null);
                } else setPicked(picked === p.text ? null : p.text);
              }}
              onPointerCancel={() => {
                mark(null);
                setDrag(null);
              }}
            >
              {p.text}
            </span>
          ),
        )}
      </p>
      <p className="match-hint">{picked ? "이제 맞는 한국어 칸을 눌러요" : "영어를 끌어서 맞는 한국어 칸에 놓아요"}</p>
      <p className="match-line">
        {ko.map((part, i) => {
          if (typeof part === "string") return <span key={i}>{part}</span>;
          slotNo += 1;
          const n = slotNo;
          const done = found.includes(part.en);
          return (
            <span
              key={i}
              data-slot={n}
              className={`match-slot${done ? " done" : ""}`}
              onClick={() => {
                if (!picked || done) return;
                onMatch(n, picked);
                setPicked(null);
              }}
            >
              <small className="match-slot-en">{done ? part.en : " "}</small>
              <span className="match-slot-ko">{part.ko}</span>
            </span>
          );
        })}
      </p>
    </div>
  );
}
