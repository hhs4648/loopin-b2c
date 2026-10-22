import { useEffect, useRef, useState } from "react";
import type { OrderCard } from "../tutor/policy/types";
import { phoneScale } from "./phoneScale";

/**
 * 순서 잇기 — 주어진 글 카드 아래 빈칸 세 개에 단락 카드(A·B·C)를 끌어 순서대로 놓는다.
 * 카드마다 단락의 **첫머리**와 **끝**을 적어 두어, 앞 카드의 끝과 다음 카드의 첫머리를 이어 보게 한다.
 * 카드를 누르면 맨 위 빈칸부터 차례로 들어간다(끌어서 원하는 칸에 놓아도 된다). 놓은 카드를 누르면 다시 빠진다.
 * 세 칸이 다 차면 바로 낸다. 틀리면(`tries`가 늘면) 칸을 비운다. `solved`면 정답 순서로 채워 보인다.
 */
export function OrderBoard({
  given,
  cards,
  solved,
  tries,
  open,
  onSubmit,
}: {
  given: OrderCard;
  cards: OrderCard[];
  solved: string[] | null;
  tries: number;
  open: boolean;
  onSubmit: (order: string[]) => void;
}) {
  const [slots, setSlots] = useState<(string | null)[]>(() => cards.map(() => null));
  const [drag, setDrag] = useState<{ id: string; x: number; y: number; dx: number; dy: number } | null>(null);
  const moved = useRef(false);

  useEffect(() => {
    setSlots(cards.map(() => null));
  }, [tries, cards.length]);

  const shown = solved ?? slots;
  const place = (slot: number, id: string) => {
    if (!open) return;
    const next = slots.map((x) => (x === id ? null : x));
    next[slot] = id;
    setSlots(next);
    if (next.every(Boolean)) onSubmit(next as string[]);
  };

  const slotAt = (x: number, y: number) => {
    const el = document.elementsFromPoint(x, y).find((e) => e instanceof HTMLElement && e.dataset.orderSlot) as HTMLElement | undefined;
    return el ? Number(el.dataset.orderSlot) : null;
  };
  const mark = (slot: number | null) => {
    document.querySelectorAll(".order-slot.drop-over").forEach((e) => e.classList.remove("drop-over"));
    if (slot !== null) document.querySelector(`.order-slot[data-order-slot="${slot}"]`)?.classList.add("drop-over");
  };

  const cardView = (c: OrderCard, extra = "") => (
    <div className={`order-card${extra}`}>
      <b className="order-label">{c.label}</b>
      {c.first ? (
        <span className="order-clue">
          <small>첫머리</small> {c.first.en}
          <em>{c.first.ko}</em>
        </span>
      ) : null}
      {c.last ? (
        <span className="order-clue">
          <small>끝</small> {c.last.en}
          <em>{c.last.ko}</em>
        </span>
      ) : null}
    </div>
  );

  const byId = new Map(cards.map((c) => [c.id, c]));
  const tray = cards.filter((c) => !shown.includes(c.id));

  return (
    <div className="order-board">
      {cardView(given, " given")}
      {shown.map((id, i) => (
        <div
          key={i}
          data-order-slot={i}
          className={`order-slot${id ? " filled" : ""}${solved ? " solved" : ""}`}
          onClick={() => {
            if (solved || !id) return;
            setSlots(slots.map((x, j) => (j === i ? null : x)));
          }}
        >
          <span className="order-arrow" aria-hidden="true">↓</span>
          {id ? cardView(byId.get(id)!) : <span className="order-empty">여기에 놓아요</span>}
        </div>
      ))}
      {tray.length && !solved ? (
        <div className="order-tray">
          <p className="match-hint">카드를 누르면 위 빈칸에 차례로 들어가요 (놓은 카드를 누르면 빠져요)</p>
          {tray.map((c) => (
            <div
              key={c.id}
              role="button"
              tabIndex={0}
              className={`order-drag${drag?.id === c.id ? " dragging" : ""}`}
              style={drag?.id === c.id ? { transform: `translate(${drag.dx}px, ${drag.dy}px)` } : undefined}
              onPointerDown={(e) => {
                if (!open) return;
                (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
                moved.current = false;
                setDrag({ id: c.id, x: e.clientX, y: e.clientY, dx: 0, dy: 0 });
              }}
              onPointerMove={(e) => {
                if (!drag || drag.id !== c.id) return;
                const s = phoneScale(e.currentTarget);
                const dx = (e.clientX - drag.x) / s;
                const dy = (e.clientY - drag.y) / s;
                if (Math.abs(dx) + Math.abs(dy) > 6) moved.current = true;
                setDrag({ ...drag, dx, dy });
                mark(slotAt(e.clientX, e.clientY));
              }}
              onPointerUp={(e) => {
                if (!drag || drag.id !== c.id) return;
                const slot = slotAt(e.clientX, e.clientY);
                mark(null);
                setDrag(null);
                if (moved.current) {
                  if (slot !== null) place(slot, c.id);
                } else place(slots.indexOf(null), c.id);
              }}
              onPointerCancel={() => {
                mark(null);
                setDrag(null);
              }}
            >
              {cardView(c)}
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}
