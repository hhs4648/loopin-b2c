import type { LessonSet } from "../../content/tutor/types";
import { allSets, sentenceCount } from "../tutor/sets";
import { ClassroomBg } from "./ClassroomBg";
import { TeacherFigure } from "./TeacherFigure";

/**
 * 메인 화면 — **수업 목록.**
 *
 * 예전에는 앱을 열면 곧장 한 지문이 시작됐다. 지문이 늘면 고를 데가 있어야 한다.
 * 카드 하나가 세트 하나이고, 세트가 학생이 한 번에 앉는 분량이다.
 *
 * 세트 내용은 `content/tutor/sets.json`에 있다. 여기 코드는 그리기만 한다.
 */

type Props = {
  learnerName: string | null;
  onPick: (set: LessonSet) => void;
};

export function LessonList({ learnerName, onPick }: Props) {
  const sets = allSets();

  return (
    <div className="stage-fill home">
      <ClassroomBg />

      <header className="top-bar">
        <div className="chip">
          <span className="avatar">다</span>
          <div className="chip-text">
            <strong>다정쌤</strong>
            <small>{learnerName ? `${learnerName}님과 함께` : "영어 해석 수업"}</small>
          </div>
        </div>
      </header>

      <div className="home-body">
        <p className="home-hello">
          {learnerName ? `${learnerName}님, 오늘은 어떤 걸 볼까요?` : "오늘은 어떤 걸 볼까요?"}
        </p>
        <h1 className="home-title">수업 목록</h1>

        <ul className="set-list">
          {sets.map((set) => (
            <li key={set.id}>
              <button type="button" className="set-card" onClick={() => onPick(set)}>
                <span className="set-tag">{set.tag}</span>
                <strong className="set-title">{set.title}</strong>
                <span className="set-subtitle">{set.subtitle}</span>
                <span className="set-meta">
                  <span className="set-count">{sentenceCount(set)}문장</span>
                  <span className="set-go">
                    시작하기
                    <ArrowIcon />
                  </span>
                </span>
              </button>
            </li>
          ))}
        </ul>
      </div>

      <div className="home-mascot">
        <div className="teacher-bob">
          <TeacherFigure />
        </div>
      </div>
    </div>
  );
}

function ArrowIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 6l6 6-6 6" />
    </svg>
  );
}
