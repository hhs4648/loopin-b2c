import { useRef } from "react";
import type { TutorView } from "../tutor/view";
import { CHECK_ALL_CMD, CHECK_CMD, CHECK_NONE_CMD, CHECK_SET_CMD } from "../tutor/policy/session";

type Props = { view: TutorView; onSend: (text: string) => void; onClose: () => void };

/**
 * 마무리 — 주요 단어 체크. 본문 단어와 보기 단어를 한 화면에 하나씩 나눠 보여 준다.
 * 모르는 단어를 체크하면 단어장으로 간다 (어느 지문에서 나왔는지 같이).
 *
 * 두 줄로 놓고, 손가락으로 쭉 끌면 지나간 단어가 한꺼번에 켜진다(처음 누른 단어가 꺼져 있었으면 켜고,
 * 켜져 있었으면 끈다). 「모두 고르기」로 한 번에 다 켤 수도 있다.
 */
export function WordCheck({ view, onSend, onClose }: Props) {
  const w = view.wordCheck!;
  const drag = useRef<{ on: boolean; seen: Set<string> } | null>(null);
  const allOn = w.words.length > 0 && w.words.every((g) => w.checked.includes(g.en));

  const enAt = (x: number, y: number) =>
    (document.elementFromPoint(x, y)?.closest("[data-en]") as HTMLElement | null)?.dataset.en ?? null;

  const mark = (en: string) => {
    const d = drag.current;
    if (!d || d.seen.has(en)) return;
    d.seen.add(en);
    onSend(`${CHECK_SET_CMD}${d.on ? "on" : "off"}:${en}`);
  };

  return (
    <div className="stage-fill words">
      <header className="words-top">
        <span className="words-step">{w.step}</span>
        <button type="button" className="close-soft" title="학습 종료" aria-label="학습 종료" onClick={onClose}>
          ✕
        </button>
      </header>
      <p className="words-title">{w.title}</p>
      <div className="words-tools">
        <span className="words-hint">쭉 끌어서 여러 개를 한 번에 고를 수 있어요</span>
        <button type="button" className="text-link" onClick={() => onSend(allOn ? CHECK_NONE_CMD : CHECK_ALL_CMD)}>
          {allOn ? "모두 풀기" : "모두 고르기"}
        </button>
      </div>
      <ul
        className="words-list two"
        onPointerMove={(e) => {
          if (!drag.current) return;
          const en = enAt(e.clientX, e.clientY);
          if (en) mark(en);
        }}
        onPointerUp={() => (drag.current = null)}
        onPointerCancel={() => (drag.current = null)}
        onPointerLeave={() => (drag.current = null)}
      >
        {w.words.map((g) => {
          const on = w.checked.includes(g.en);
          return (
            <li key={g.en}>
              <button
                type="button"
                data-en={g.en}
                className={`word-row${on ? " on" : ""}`}
                aria-pressed={on}
                onPointerDown={(e) => {
                  // 손가락을 따라 다른 단어 위로 가도 이 목록이 움직임을 받는다
                  (e.currentTarget.closest("ul") as HTMLElement | null)?.setPointerCapture?.(e.pointerId);
                  drag.current = { on: !on, seen: new Set() };
                  mark(g.en);
                }}
                // 키보드(Enter·Space)로 누를 때만 — 손가락·마우스는 위에서 이미 처리했다
                onClick={(e) => e.detail === 0 && onSend(`${CHECK_CMD}${g.en}`)}
              >
                <span className="word-box" aria-hidden="true">{on ? "✓" : ""}</span>
                <span className="word-text">
                  <span className="word-en">{g.en}</span>
                  <span className="word-ko">{g.ko}</span>
                </span>
              </button>
            </li>
          );
        })}
      </ul>
      <div className="words-dock">
        <span className="words-count">모르는 단어 {w.checked.length}개 체크</span>
        {view.buttons.map((label) => (
          <button key={label} type="button" className="read-continue" onClick={() => onSend(label)}>
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}
