type Props = {
  buttons: string[];
  hidden?: boolean;
  /** 보기가 길면 세로로 쌓는다 (Teaching Policy 레슨의 뜻 고르기) */
  layout?: "row" | "stack";
  /** 보기가 아닌 버튼 — 옅은 색으로 구분한다 */
  aux?: string[];
  /** 보기에 ①②③을 단다 */
  numbered?: boolean;
  onPick: (label: string) => void;
};

const NUMERALS = ["①", "②", "③", "④", "⑤"];

export function QuickReplies({ buttons, hidden, layout = "row", aux, numbered, onPick }: Props) {
  if (hidden || buttons.length === 0) return null;
  // 보기에는 ①②③을 단다. 보조 버튼(`aux`)과 「다음으로」 같은 단독 버튼에는 안 단다
  let n = 0;
  return (
    <div className={`quick-row${layout === "stack" ? " stack" : ""}`}>
      {buttons.map((label) => {
        const isAux = aux?.includes(label) ?? false;
        const numeral = numbered && !isAux ? NUMERALS[n++] : null;
        return (
          <button
            key={label}
            type="button"
            className={`pill${isAux ? " aux" : ""}${numeral ? " numbered" : ""}`}
            onClick={() => onPick(label)}
          >
            {numeral ? <span className="pill-num">{numeral}</span> : null}
            {label}
          </button>
        );
      })}
    </div>
  );
}
