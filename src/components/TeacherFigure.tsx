export function TeacherFigure({ size = "lg" }: { size?: "lg" | "sm" }) {
  const w = size === "lg" ? "100%" : 72;
  return (
    <svg
      viewBox="0 0 200 260"
      width={w}
      height="auto"
      role="img"
      aria-label="다정쌤"
      style={{
        position: "relative",
        width: w,
        height: "auto",
        flex: "none",
      }}
    >
      <ellipse cx="100" cy="248" rx="62" ry="10" fill="rgba(60,30,10,.22)" />
      <path
        d="M46 150c8 52 32 78 54 78s46-26 54-78c-18 10-36 14-54 14s-36-4-54-14z"
        fill="#3a3a3f"
      />
      <path
        d="M58 128c10 46 28 70 42 70s32-24 42-70c-14 8-28 12-42 12s-28-4-42-12z"
        fill="#ef7a93"
      />
      <path d="M78 122c6 28 10 44 22 44s16-16 22-44" fill="#f6e9ec" />
      <circle cx="100" cy="92" r="44" fill="#f3c7b3" />
      <path
        d="M58 88c8-40 28-58 42-58s34 18 42 58c-20-12-64-12-84 0z"
        fill="#2b2430"
      />
      <path d="M70 70c18-22 44-22 60 0-18-8-42-8-60 0z" fill="#3a3a3f" />
      <ellipse cx="86" cy="96" rx="5" ry="6" fill="#2b2430" />
      <ellipse cx="114" cy="96" rx="5" ry="6" fill="#2b2430" />
      <path
        d="M90 114q10 10 20 0"
        fill="none"
        stroke="#e2607d"
        strokeWidth="3"
        strokeLinecap="round"
      />
      <circle cx="78" cy="104" r="6" fill="#f0a3b4" opacity=".7" />
      <circle cx="122" cy="104" r="6" fill="#f0a3b4" opacity=".7" />
    </svg>
  );
}
