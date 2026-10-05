import type { LessonCollection, LessonSet } from "../../content/tutor/types";
import { isDone, loadProgress, type Progress } from "../tutor/progress";
import { allGroups, sentenceCount, setsIn, unitsOf } from "../tutor/sets";
import { ClassroomBg } from "./ClassroomBg";
import { TeacherFigure } from "./TeacherFigure";

/**
 * 메인 화면 — **수업 목록.**
 *
 * 두 켜다. 처음에는 중분류(2024 수능)를 보여 주고, 하나를 고르면 그 안의
 * 문제들이 나온다. 한 문제를 작은 단위로 쪼갠 세트는 한 켜가 더 있다 —
 * 문제를 누르면 **단위 목록**(단어 → … → 실전 풀기)이 나온다. 대분류(수능)는 카드가 아니라 **묶음 제목**으로 둔다 —
 * 26개를 한 줄로 늘어놓는 것도, 하나뿐인 대분류를 누르게 하는 것도 낭비다.
 *
 * 목록 내용은 `content/tutor/sets.json`에 있다. 여기 코드는 그리기만 한다.
 */

/**
 * **끝낸 문제는 맨 밑으로.**
 *
 * 26개가 늘어선 목록에서 학생이 찾는 건 늘 「아직 안 한 것」이다. 끝낸 것을
 * 원래 자리에 두면 매번 그것들을 지나쳐 내려가야 한다. 끼리끼리 순서는
 * 그대로 둔다 — 문제 번호가 곧 순서라 뒤섞으면 오히려 못 찾는다.
 */
function doneLast(sets: LessonSet[], progress: Progress): LessonSet[] {
  const todo = sets.filter((s) => !isDone(progress, s.id));
  const done = sets.filter((s) => isDone(progress, s.id));
  return [...todo, ...done];
}

type Props = {
  learnerName: string | null;
  /** 열어 둔 중분류. null이면 중분류 목록 */
  collection: LessonCollection | null;
  /** 단위 목록을 열어 둔 세트. 있으면 이게 먼저 보인다 */
  unitSet: LessonSet | null;
  onOpenCollection: (collection: LessonCollection) => void;
  onBack: () => void;
  onPickSet: (set: LessonSet) => void;
  onPickUnit: (lessonId: string) => void;
};

export function LessonList({
  learnerName,
  collection,
  unitSet,
  onOpenCollection,
  onBack,
  onPickSet,
  onPickUnit,
}: Props) {
  const progress = loadProgress();
  const units = unitSet ? unitsOf(unitSet) : [];
  /*
    순서대로 하기를 권하지만 잠그지는 않는다 — 자신 있으면 바로 실전 풀기로 가도 된다.
    「여기부터」는 아직 안 한 것 중 첫 단위에만 단다.
  */
  const upNext = units.find((u) => u.lesson && !isDone(progress, u.lesson));

  return (
    <div className="stage-fill home">
      <ClassroomBg />

      <header className="top-bar">
        {collection || unitSet ? (
          <button type="button" className="icon-btn light" title="목록으로" onClick={onBack}>
            <BackIcon />
          </button>
        ) : (
          <div className="chip">
            <span className="avatar">다</span>
            <div className="chip-text">
              <strong>다정쌤</strong>
              <small>{learnerName ? `${learnerName}님과 함께` : "영어 해석 수업"}</small>
            </div>
          </div>
        )}
      </header>

      <div className="home-body">
        {unitSet ? (
          <>
            <p className="home-hello">{unitSet.subtitle}</p>
            <h1 className="home-title">{unitSet.title}</h1>
            <ol className="set-list">
              {units.map((unit, i) => {
                const done = !!unit.lesson && isDone(progress, unit.lesson);
                const soon = !unit.lesson;
                return (
                  <li key={unit.title}>
                    <button
                      type="button"
                      className={`set-card unit-card${done ? " done" : ""}${soon ? " soon" : ""}`}
                      disabled={soon}
                      onClick={() => unit.lesson && onPickUnit(unit.lesson)}
                    >
                      <span className="unit-num">{i + 1}</span>
                      <span className="unit-text">
                        <strong className="set-title">
                          {unit.title}
                          {done ? <span className="done-mark">완료</span> : null}
                        </strong>
                        <span className="set-subtitle">{unit.subtitle}</span>
                      </span>
                      <span className="set-go">
                        {soon ? "준비 중" : done ? "다시 하기" : unit === upNext ? "여기부터" : "시작하기"}
                        {soon ? null : <ArrowIcon />}
                      </span>
                    </button>
                  </li>
                );
              })}
            </ol>
          </>
        ) : collection ? (
          <>
            <p className="home-hello">{collection.subtitle}</p>
            <h1 className="home-title">{collection.title}</h1>
            <ul className="set-list">
              {doneLast(setsIn(collection.id), progress).map((set) => {
                const done = isDone(progress, set.id);
                return (
                  <li key={set.id}>
                    <button
                      type="button"
                      className={`set-card${done ? " done" : ""}`}
                      onClick={() => onPickSet(set)}
                    >
                      <strong className="set-title">
                        {set.title}
                        {done ? <span className="done-mark">완료</span> : null}
                      </strong>
                      <span className="set-subtitle">{set.subtitle}</span>
                      <span className="set-meta">
                        <span className="set-count">
                          {unitsOf(set).length ? `${unitsOf(set).length}단계` : `${sentenceCount(set)}문장`}
                        </span>
                        <span className="set-go">
                          {done ? "다시 풀기" : unitsOf(set).length ? "열기" : "시작하기"}
                          <ArrowIcon />
                        </span>
                      </span>
                    </button>
                  </li>
                );
              })}
            </ul>
          </>
        ) : (
          <>
            <p className="home-hello">
              {learnerName ? `${learnerName}님, 오늘은 어떤 걸 볼까요?` : "오늘은 어떤 걸 볼까요?"}
            </p>
            <h1 className="home-title">수업 목록</h1>
            {allGroups().map((group) => (
              <section key={group.id} className="group">
                <h2 className="group-title">
                  {group.title}
                  <small>{group.subtitle}</small>
                </h2>
                <ul className="set-list">
                  {group.collections.map((c) => {
                    const sets = setsIn(c.id);
                    const sentences = sets.reduce((n, s) => n + sentenceCount(s), 0);
                    const done = sets.filter((s) => isDone(progress, s.id)).length;
                    return (
                      <li key={c.id}>
                        <button
                          type="button"
                          className="set-card"
                          onClick={() => onOpenCollection(c)}
                        >
                          <span className="set-tag">{c.tag}</span>
                          <strong className="set-title">{c.title}</strong>
                          <span className="set-subtitle">{c.subtitle}</span>
                          <span className="set-meta">
                            <span className="set-count">
                              {done > 0
                                ? `${sets.length}문제 중 ${done} 완료`
                                : `${sets.length}문제 · ${sentences}문장`}
                            </span>
                            <span className="set-go">
                              열기
                              <ArrowIcon />
                            </span>
                          </span>
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </section>
            ))}
          </>
        )}
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

function BackIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 6l-6 6 6 6" />
    </svg>
  );
}
