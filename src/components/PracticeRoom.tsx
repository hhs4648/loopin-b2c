import { useState } from "react";
import { SavedBook } from "./SavedBook";
import { SentencePractice } from "./SentencePractice";

/**
 * 연습실(보충학습실) — 단어 · 문장 · 문법 세 탭 (2026-10-20 선생님).
 * 단어: 단어장 + 단어 테스트(`SavedBook`의 단어 부분). 문장: 해석 맞추기 연습. 문법: 연습할 문법 drill(`SavedBook`의 문법 부분).
 */
export type PracticeTab = "vocab" | "sentence" | "grammar";

const TABS: { id: PracticeTab; label: string }[] = [
  { id: "vocab", label: "단어" },
  { id: "sentence", label: "문장" },
  { id: "grammar", label: "문법" },
];

export function PracticeRoom({ tab: initial = "vocab", onBack }: { tab?: PracticeTab; onBack: () => void }) {
  const [tab, setTab] = useState<PracticeTab>(initial);
  return (
    <div className="stage-fill saved practice">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="홈으로" aria-label="홈으로" onClick={onBack}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
            <path d="M15 6l-6 6 6 6" />
          </svg>
        </button>
        <nav className="practice-tabs" aria-label="연습">
          {TABS.map((t) => (
            <button key={t.id} type="button" className={tab === t.id ? "on" : ""} aria-pressed={tab === t.id} onClick={() => setTab(t.id)}>
              {t.label}
            </button>
          ))}
        </nav>
      </header>
      {tab === "sentence" ? (
        <div className="saved-body-scroll">
          <h1 className="saved-title">문장 연습</h1>
          <SentencePractice />
        </div>
      ) : (
        <SavedBook key={tab} kind="vocab" section={tab} embedded onBack={onBack} />
      )}
    </div>
  );
}
