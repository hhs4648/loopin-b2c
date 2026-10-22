import { useMemo, useState } from "react";
import type { LessonSet } from "../../content/tutor/types";
import { getMiniMock } from "../tutor/mini";
import { getSet } from "../tutor/sets";
import { itemsToReview, reviewRecords, saveReviewRecord } from "../tutor/wrongReview";
import { ItemView, NUM } from "./MiniMockView";
import { currentTeacher } from "../tutor/teacher";

/**
 * 틀린 문제 복습 (회차의 4단계) — 힌트 없이 한 문제씩. 맞히면 「잘했어요!」, 또 틀리면 「두 번 틀렸어요. 왜 틀렸을까요?」를
 * 스스로 적게 하고 기록한 뒤 「분석 다시 보기」로 간다.
 */
type Props = {
  mockId: string;
  onBack: () => void;
  onAnalyze: (set: LessonSet) => void;
};

export function WrongReview({ mockId, onBack, onAnalyze }: Props) {
  const mock = getMiniMock(mockId);
  const items = useMemo(() => itemsToReview(mockId), [mockId]);
  const [recs, setRecs] = useState(() => reviewRecords(mockId));
  // 아직 복습 안 한 문항부터
  const [at, setAt] = useState(() => Math.max(0, items.findIndex((it) => !(it.no in recs))));
  const [picked, setPicked] = useState<number | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [reason, setReason] = useState("");
  const [reasonSaved, setReasonSaved] = useState(false);

  const item = items[at];
  const set = item?.lesson ? getSet(item.lesson) : null;

  const header = (
    <header className="saved-top">
      <button type="button" className="icon-btn light" title="뒤로" aria-label="뒤로" onClick={onBack}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
          <path d="M15 6l-6 6 6 6" />
        </svg>
      </button>
    </header>
  );

  if (!mock || !items.length) {
    return (
      <div className="stage-fill saved mini">
        {header}
        <div className="saved-body-scroll">
          <p className="home-hello">{mock?.title ?? ""}</p>
          <h1 className="home-title">틀린 문제 복습</h1>
          <p className="saved-empty">{mock && !items.length ? "이 회는 틀린 문제가 없어요. 잘했어요!" : "먼저 실전 풀기를 해야 복습할 문제가 생겨요."}</p>
        </div>
      </div>
    );
  }
  if (!item) {
    return (
      <div className="stage-fill saved mini">
        {header}
        <div className="saved-body-scroll">
          <p className="home-hello">{mock.title}</p>
          <h1 className="home-title">틀린 문제 복습 끝!</h1>
          <p className="pack-help">
            {items.length}문제 중 {items.filter((it) => recs[it.no]?.correct).length}개를 이번엔 맞혔어요. 또 틀린 문제는 「틀린 문제」에 남아 있어요.
          </p>
          <button type="button" className="mini-start" onClick={onBack}>코스로 돌아가기</button>
        </div>
      </div>
    );
  }

  const rec = recs[item.no];
  const right = submitted && picked === item.answer;
  const next = () => {
    setPicked(null);
    setSubmitted(false);
    setReason("");
    setReasonSaved(false);
    setAt(at + 1);
  };

  return (
    <div className="stage-fill saved mini mini-exam">
      {header}
      <div className="saved-body-scroll">
        <p className="home-hello">{mock.title} · 틀린 문제 복습 {at + 1}/{items.length}</p>
        {!submitted && !rec ? <p className="pack-help">힌트 없이 한 번 더 풀어 봐요. 지난번엔 틀렸던 문제예요.</p> : null}
        <ItemView item={item} picked={submitted ? picked : picked} review={submitted} onPick={submitted ? undefined : setPicked} />
        {!submitted ? (
          <button type="button" className="mini-check" disabled={!picked} onClick={() => {
            setSubmitted(true);
            if (picked === item.answer) {
              const nextRecs = { ...recs, [item.no]: { correct: true, picked: picked!, at: new Date().toISOString() } };
              setRecs(nextRecs);
              saveReviewRecord(mockId, item.no, { correct: true, picked: picked! });
            }
          }}>
            제출
          </button>
        ) : right ? (
          <div className="mini-checked right">
            <p className="mini-verdict">○ 잘했어요! 이번엔 맞혔어요.</p>
            <button type="button" className="mini-start" onClick={next}>{at + 1 < items.length ? "다음 문제" : "끝내기"}</button>
          </div>
        ) : (
          <div className="mini-checked wrong">
            <p className="mini-verdict">✕ 두 번 틀렸어요. 정답은 {NUM[item.answer - 1]}예요.</p>
            {!reasonSaved ? (
              <>
                <p className="pack-help">왜 틀렸다고 생각해요? 짧게라도 적어 두면 다음에 같은 실수를 덜 해요.</p>
                <textarea
                  className="wr-reason"
                  rows={3}
                  placeholder="예: 빈칸 앞 문장을 반대로 읽었어요 / 단어 뜻을 몰랐어요"
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                />
                <button type="button" className="mini-check" disabled={!reason.trim()} onClick={() => {
                  saveReviewRecord(mockId, item.no, { correct: false, picked: picked!, reason: reason.trim() });
                  setRecs({ ...recs, [item.no]: { correct: false, picked: picked!, reason: reason.trim(), at: new Date().toISOString() } });
                  setReasonSaved(true);
                }}>
                  기록하기
                </button>
              </>
            ) : (
              <>
                <p className="wr-saved">기록했어요: “{reason.trim()}”</p>
                {set ? (
                  <button type="button" className="mini-analyze big" onClick={() => onAnalyze(set)}>
                    <b>{currentTeacher().name} 분석 다시 보기 ›</b>
                    <small>지난번 분석을 처음부터 다시 봐요</small>
                  </button>
                ) : null}
                <button type="button" className="mini-start soft" onClick={next}>{at + 1 < items.length ? "다음 문제" : "끝내기"}</button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
