import { useRef, useState } from "react";
import type { StudyPanel } from "../tutor/policy/types";

/**
 * 문장 아래에 띄우는 그림 — Teaching Policy 레슨만 쓴다.
 *
 * 말풍선은 한 번에 한 가지만 말한다. 문장 뼈대나 대응표처럼 **한눈에 봐야 하는
 * 것**은 말로 풀지 않고 여기 그린다.
 */
export function StudyPanelView({ panel, onPick }: { panel: StudyPanel; onPick?: (label: string) => void }) {
  if (panel.kind === "structure") {
    return (
      <div className="study-panel structure">
        {panel.rows.map((row) => (
          <div key={row.label + row.text} className="panel-row">
            <span className="panel-label">{row.label}</span>
            <span className={`panel-text${row.tone ? ` tone-${row.tone}` : ""}`}>
              {row.text}
              {row.ko ? <small>{row.ko}</small> : null}
            </span>
          </div>
        ))}
      </div>
    );
  }

  if (panel.kind === "mapping") {
    return (
      <div className="study-panel mapping">
        {panel.title ? <div className="panel-title">{panel.title}</div> : null}
        {panel.rows.map((row) => (
          <div key={row.left} className="panel-row">
            <span className="panel-left">{row.left}</span>
            <span className="panel-arrow">→</span>
            <span className={`panel-right${row.right ? "" : " blank"}`}>
              {row.right ?? "?"}
              {row.note ? <small>{row.note}</small> : null}
            </span>
          </div>
        ))}
      </div>
    );
  }

  if (panel.kind === "note") {
    return (
      <div className="study-panel note">
        <span className="panel-label">{panel.label}</span>
        <span className="panel-text">{panel.text}</span>
      </div>
    );
  }

  if (panel.kind === "groups") {
    const group = (g: typeof panel.left, side: string) => (
      <div className={`board-group ${side}`} data-side={side.split(" ")[0]}>
        <span className="board-group-label">{g.label}</span>
        {g.cluster ? (
          <div className={`board-cluster${g.cluster.fresh ? " fresh" : ""}`}>
            <div className="board-words">
              {g.cluster.words.map((w) => (
                <span key={w} className="board-word">{w}</span>
              ))}
            </div>
            {g.cluster.note ? <small>{g.cluster.note}</small> : null}
          </div>
        ) : null}
        {g.cluster && g.arrow && g.words.length ? <b className="board-arrow">{g.arrow}</b> : null}
        <div className="board-words">
          {g.words.map((w) => (
            <span key={w.text} className={`board-word${w.fresh ? " fresh" : ""}${w.quote ? " quote" : ""}`}>
              {w.text}
            </span>
          ))}
        </div>
      </div>
    );
    return (
      <div
        className="study-panel board"
        ref={(el) => {
          // 새로 붙은 단어는 그룹 맨 아래에 쌓인다 — 보이게 내려 둔다
          if (el) el.scrollTop = el.scrollHeight;
        }}
      >
        <i className="board-magnets" aria-hidden="true" />
        {panel.title ? <div className="panel-title">{panel.title}</div> : null}
        <div className="board-groups">
          {group(panel.left, panel.right ? "left" : "left solo")}
          {panel.right && panel.process ? (
            <div className="board-process">
              <b>{panel.process.arrow ?? "←"}</b>
              {panel.process.words.map((w) => (
                <small key={w.text} className={w.fresh ? "fresh" : undefined}>{w.text}</small>
              ))}
            </div>
          ) : panel.right ? (
            <b className="board-between">{panel.between ?? "≠"}</b>
          ) : null}
          {panel.right ? group(panel.right, "right") : null}
        </div>
        {panel.sort && onPick ? (
          <SortChip
            words={panel.sort.words}
            onDrop={(side) => onPick(side === "left" ? panel.sort!.left : panel.sort!.right)}
          />
        ) : panel.caption ? (
          <p className="board-caption">{panel.caption}</p>
        ) : null}
      </div>
    );
  }

  if (panel.kind === "picture") {
    return (
      <div className="study-panel board picture">
        <i className="board-magnets" aria-hidden="true" />
        {panel.title ? <div className="panel-title">{panel.title}</div> : null}
        <img className="board-picture" src={panel.src} alt={panel.alt} />
        {panel.words?.length ? (
          <div className={panel.words_label ? "board-cluster fresh" : undefined}>
            <div className="board-words">
              {panel.words.map((w) => (
                <span key={w.text} className={`board-word${w.fresh ? " fresh" : ""}${w.quote ? " quote" : ""}`}>
                  {w.text}
                </span>
              ))}
            </div>
            {panel.words_label ? <small>{panel.words_label}</small> : null}
          </div>
        ) : null}
        {panel.caption ? <p className="board-caption">{panel.caption}</p> : null}
      </div>
    );
  }

  if (panel.kind === "map") {
    return (
      <div
        className="study-panel map"
        ref={(el) => {
          // 지도가 길어지면 새로 붙은 줄(맨 아래)이 보이게 내려 둔다
          if (el) el.scrollTop = el.scrollHeight;
        }}
      >
        {panel.title ? <div className="panel-title">{panel.title}</div> : null}
        {panel.rows.map((row, i) => (
          <div key={i} className={`map-row${row.fresh ? " fresh" : ""}${row.quote ? " quote" : ""}`}>
            {row.text}
          </div>
        ))}
      </div>
    );
  }

  const side = (s: typeof panel.left) => (
    <div className="panel-side">
      <strong>{s.title}</strong>
      <span>{s.text}</span>
    </div>
  );
  return (
    <div className={`study-panel contrast${panel.between ? " with-between" : ""}`}>
      {panel.title ? <div className="panel-title">{panel.title}</div> : null}
      <div className="contrast-row">
        {side(panel.left)}
        {panel.between ? <b className="contrast-between">{panel.between}</b> : null}
        {side(panel.right)}
      </div>
    </div>
  );
}

/**
 * 학생이 그룹에 끌어 넣는 단어 칩. 손가락·마우스 모두 pointer 이벤트로 받는다.
 * 그룹 위에서 놓으면 그 쪽을 고른 것이다. 엉뚱한 곳에 놓으면 제자리로 돌아온다.
 */
function SortChip({ words, onDrop }: { words: string[]; onDrop: (side: "left" | "right") => void }) {
  const start = useRef<{ x: number; y: number } | null>(null);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [over, setOver] = useState<"left" | "right" | null>(null);

  const sideAt = (x: number, y: number) => {
    const el = document
      .elementsFromPoint(x, y)
      .find((e) => e instanceof HTMLElement && e.dataset.side) as HTMLElement | undefined;
    const side = el?.dataset.side;
    return side === "left" || side === "right" ? side : null;
  };

  const mark = (side: "left" | "right" | null) => {
    document.querySelectorAll(".board-group.drop-over").forEach((e) => e.classList.remove("drop-over"));
    if (side) document.querySelector(`.board-group[data-side="${side}"]`)?.classList.add("drop-over");
    setOver(side);
  };

  return (
    <div className="board-sort">
      <span className="board-sort-hint">끌어서 그룹에 넣어 봐요</span>
      <span
        className={`board-sort-chip${start.current ? " dragging" : ""}`}
        style={{ transform: `translate(${offset.x}px, ${offset.y}px)` }}
        onPointerDown={(e) => {
          start.current = { x: e.clientX, y: e.clientY };
          e.currentTarget.setPointerCapture(e.pointerId);
        }}
        onPointerMove={(e) => {
          if (!start.current) return;
          setOffset({ x: e.clientX - start.current.x, y: e.clientY - start.current.y });
          mark(sideAt(e.clientX, e.clientY));
        }}
        onPointerUp={() => {
          const side = over;
          start.current = null;
          setOffset({ x: 0, y: 0 });
          mark(null);
          if (side) onDrop(side);
        }}
        onPointerCancel={() => {
          start.current = null;
          setOffset({ x: 0, y: 0 });
          mark(null);
        }}
      >
        {words.map((w) => (
          <span key={w} className="board-word">{w}</span>
        ))}
      </span>
    </div>
  );
}
