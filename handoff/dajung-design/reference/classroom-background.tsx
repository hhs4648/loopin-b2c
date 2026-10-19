export function ClassroomBg() {
  return (
    <>
      <div
        style={{
          position: "absolute",
          inset: "0 0 26% 0",
          background: "linear-gradient(180deg,#f9f1e7 0%,#f3e6d8 100%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 0,
          height: "74%",
          background:
            "repeating-linear-gradient(90deg,rgba(255,255,255,.35) 0 2px,transparent 2px 34px)",
          opacity: 0.6,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: "calc(74% - 12px)",
          height: 12,
          background: "linear-gradient(180deg,#e8d9c7,#d9c6b0)",
          boxShadow: "0 2px 6px rgba(0,0,0,.08)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 0,
          height: "26%",
          background:
            "repeating-linear-gradient(90deg,#c99a6c 0 70px,#bf8f62 70px 72px,#c99a6c 72px 140px,#b98757 140px 142px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 0,
          height: "26%",
          background:
            "linear-gradient(180deg,rgba(80,40,10,.28),rgba(80,40,10,0) 45%,rgba(255,240,220,.18))",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "15%",
          transform: "translateX(-50%)",
          width: "84cqw",
          height: "30%",
          background: "linear-gradient(135deg,#ffffff 0%,#f6f7f8 60%,#eef0f2 100%)",
          border: "7px solid #d6d9dd",
          borderRadius: 6,
          boxShadow:
            "inset 0 0 30px rgba(0,0,0,.04),0 10px 24px rgba(60,40,20,.12)",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: 12,
            right: 14,
            display: "flex",
            gap: 7,
          }}
        >
          <span className="magnet" style={{ background: "#ef7a93" }} />
          <span className="magnet" style={{ background: "#5c9cf5" }} />
          <span className="magnet" style={{ background: "#f6c948" }} />
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "calc(15% + 30% + 7px)",
          transform: "translateX(-50%)",
          width: "84cqw",
          height: 10,
          background: "linear-gradient(180deg,#cfd3d8,#aab0b7)",
          borderRadius: "0 0 5px 5px",
          boxShadow: "0 5px 8px rgba(0,0,0,.15)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: "calc(50% - 52px)",
          top: "calc(15% + 30% + 1px)",
          display: "flex",
          gap: 5,
        }}
      >
        <span className="marker" style={{ background: "#3a3a3a" }} />
        <span className="marker" style={{ background: "#e2607d" }} />
        <span className="marker" style={{ background: "#3d7ff0" }} />
      </div>
      <div className="clock">
        <i className="hand hour" />
        <i className="hand minute" />
        <i className="hub" />
      </div>
      <div className="plant">
        <i className="stem" />
        <i className="leaf a" />
        <i className="leaf b" />
        <i className="leaf c" />
        <i className="pot" />
        <i className="rim" />
      </div>
    </>
  );
}
