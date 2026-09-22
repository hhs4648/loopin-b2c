type Props = {
  buttons: string[];
  hidden?: boolean;
  /** 보기가 길면 세로로 쌓는다 (Teaching Policy 레슨의 뜻 고르기) */
  layout?: "row" | "stack";
  /** 보기가 아닌 버튼 — 옅은 색으로 구분한다 */
  aux?: string[];
  onPick: (label: string) => void;
};

export function QuickReplies({ buttons, hidden, layout = "row", aux = [], onPick }: Props) {
  if (hidden || buttons.length === 0) return null;
  return (
    <div className={`quick-row${layout === "stack" ? " stack" : ""}`}>
      {buttons.map((label) => (
        <button
          key={label}
          type="button"
          className={`pill${aux.includes(label) ? " aux" : ""}`}
          onClick={() => onPick(label)}
        >
          {label}
        </button>
      ))}
    </div>
  );
}
