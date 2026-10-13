import { useEffect, useLayoutEffect, useRef, useState } from "react";
import type { StudyPanel } from "../tutor/policy/types";
import { StudyPanelView } from "./StudyPanel";

/** 칠판으로 크게 띄우는 그림 — 단어 지도·그림·지도. 작은 표·메모는 그대로 문장 아래에 둔다 */
export function isBoardPanel(panel: StudyPanel | undefined | null): panel is StudyPanel {
  return !!panel && (panel.kind === "groups" || panel.kind === "picture" || panel.kind === "map");
}

/**
 * 칠판 서랍 — 문장 자리를 덮는 흰 칠판. 오른쪽 가장자리의 손잡이로 언제든 열고 닫는다
 * (누르거나 옆으로 끌어서). 새 칠판이 뜨면 저절로 펼쳐진다.
 *
 * 문장 자리는 머리줄 아래부터 선생님 무대 위까지 — 말풍선과 버튼은 늘 보인다.
 */
export function BoardDrawer({
  panel,
  fresh,
  onPick,
}: {
  panel: StudyPanel;
  /** 지금 스텝의 칠판인지 (아니면 이 문장에서 앞서 본 칠판을 다시 여는 것) */
  fresh: boolean;
  onPick?: (label: string) => void;
}) {
  const [open, setOpen] = useState(true);
  const key = JSON.stringify(panel);
  // 새 칠판(내용이 바뀐 칠판)이 뜨면 펼치고, 칠판 스텝이 끝나면 접어서 문장을 보여 준다
  useEffect(() => {
    setOpen(fresh);
  }, [key, fresh]);

  const self = useRef<HTMLDivElement>(null);
  const [box, setBox] = useState<{ top: number; bottom: number } | null>(null);
  useLayoutEffect(() => {
    const el = self.current;
    const root = el?.closest<HTMLElement>(".study");
    if (!el || !root) return;
    const measure = () => {
      const head = root.querySelector<HTMLElement>(".study-top");
      const stage = root.querySelector<HTMLElement>(".study-stage");
      if (!head || !stage) return;
      const top = head.offsetTop + head.offsetHeight + 8;
      const bottom = root.clientHeight - stage.offsetTop + 6;
      setBox((b) => (b && b.top === top && b.bottom === bottom ? b : { top, bottom }));
    };
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(root);
    const stage = root.querySelector(".study-stage");
    if (stage) ro.observe(stage);
    return () => ro.disconnect();
  }, []);

  // 손잡이 끌기 — 손을 뗐을 때 60px 넘게 끌었으면 그쪽으로, 거의 안 움직였으면 누른 것
  const drag = useRef<{ x: number; moved: number } | null>(null);
  const [dx, setDx] = useState(0);
  const width = self.current?.offsetWidth ?? 360;
  const shift = open ? Math.max(0, dx) : Math.min(width + 8, Math.max(0, width + 8 + dx));

  return (
    <div
      ref={self}
      className={`board-drawer${open ? " open" : ""}${drag.current ? " dragging" : ""}`}
      style={{
        top: box?.top ?? 64,
        bottom: box?.bottom ?? 240,
        transform: drag.current ? `translateX(${shift}px)` : undefined,
      }}
    >
      <button
        type="button"
        className="board-handle"
        aria-label={open ? "칠판 닫기" : "칠판 열기"}
        aria-expanded={open}
        onPointerDown={(e) => {
          drag.current = { x: e.clientX, moved: 0 };
          e.currentTarget.setPointerCapture(e.pointerId);
        }}
        onPointerMove={(e) => {
          if (!drag.current) return;
          const d = e.clientX - drag.current.x;
          drag.current.moved = Math.max(drag.current.moved, Math.abs(d));
          setDx(d);
        }}
        onPointerUp={(e) => {
          const g = drag.current;
          drag.current = null;
          const d = e.clientX - (g?.x ?? e.clientX);
          setDx(0);
          if (!g || g.moved < 8) setOpen(!open);
          else if (open && d > 60) setOpen(false);
          else if (!open && d < -60) setOpen(true);
        }}
        onPointerCancel={() => {
          drag.current = null;
          setDx(0);
        }}
      >
        <span aria-hidden="true">{open ? "›" : "‹"}</span>
        <b>칠판</b>
      </button>
      <div className="board-sheet">
        <button type="button" className="board-close text-link" onClick={() => setOpen(false)}>
          칠판 닫고 문장 보기
        </button>
        <StudyPanelView panel={panel} onPick={onPick} />
      </div>
    </div>
  );
}
