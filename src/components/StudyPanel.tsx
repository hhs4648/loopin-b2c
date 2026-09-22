import type { StudyPanel } from "../tutor/policy/types";

/**
 * 문장 아래에 띄우는 그림 — Teaching Policy 레슨만 쓴다.
 *
 * 말풍선은 한 번에 한 가지만 말한다. 문장 뼈대나 대응표처럼 **한눈에 봐야 하는
 * 것**은 말로 풀지 않고 여기 그린다.
 */
export function StudyPanelView({ panel }: { panel: StudyPanel }) {
  if (panel.kind === "structure") {
    return (
      <div className="study-panel structure">
        {panel.rows.map((row) => (
          <div key={row.label + row.text} className="panel-row">
            <span className="panel-label">{row.label}</span>
            <span className="panel-text">
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

  return (
    <div className="study-panel contrast">
      {[panel.left, panel.right].map((side) => (
        <div key={side.title} className="panel-side">
          <strong>{side.title}</strong>
          <span>{side.text}</span>
        </div>
      ))}
    </div>
  );
}
