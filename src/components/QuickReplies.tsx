type Props = {
  buttons: string[];
  hidden?: boolean;
  onPick: (label: string) => void;
};

export function QuickReplies({ buttons, hidden, onPick }: Props) {
  if (hidden || buttons.length === 0) return null;
  return (
    <div className="quick-row">
      {buttons.map((label) => (
        <button
          key={label}
          type="button"
          className="pill"
          onClick={() => onPick(label)}
        >
          {label}
        </button>
      ))}
    </div>
  );
}
