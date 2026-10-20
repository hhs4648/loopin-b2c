import { useState } from "react";
import { loadStudentState, saveStudentState, type StudentLevel } from "../tutor/policy/student-state";
import type { LessonCollection, LessonSet } from "../../content/tutor/types";
import { isDone, loadProgress, setStatuses, statusLine, type SetStatus } from "../tutor/progress";
import { loadNotes } from "../tutor/notes";
import { loadVocab } from "../tutor/vocab";
import type { SavedKind } from "./SavedBook";
import { allGroups, sentenceCount, setsIn } from "../tutor/sets";
import { allMiniMocks, loadAttempts, scoreOf } from "../tutor/mini";
import { ClassroomBg } from "./ClassroomBg";
import { TeacherFigure } from "./TeacherFigure";

/**
 * 메인 화면 — **수업 목록.**
 *
 * 두 켜다. 처음에는 중분류(2024 수능)를 보여 주고, 하나를 고르면 그 안의
 * 문제들이 나온다. 대분류(수능)는 카드가 아니라 **묶음 제목**으로 둔다 —
 * 26개를 한 줄로 늘어놓는 것도, 하나뿐인 대분류를 누르게 하는 것도 낭비다.
 *
 * 목록 내용은 `content/tutor/sets.json`에 있다. 여기 코드는 그리기만 한다.
 */

/** 오답률 높은 순 — 많이 틀리는 문제가 위로. 오답률이 없는 세트는 맨 뒤 */
function byWrongRate(sets: LessonSet[]): LessonSet[] {
  return [...sets].sort((a, b) => (b.wrong_rate ?? -1) - (a.wrong_rate ?? -1));
}

/** Top 몇까지 앞에 붙이나 — 회차마다 오답률 Top 15를 만든다 */
const TOP_N = 15;

/** 세트 id → 이 묶음 안 오답률 순위 (1부터, Top 15까지만) */
function topRanks(sets: LessonSet[]): Record<string, number> {
  const out: Record<string, number> = {};
  byWrongRate(sets)
    .filter((s) => s.wrong_rate != null)
    .slice(0, TOP_N)
    .forEach((s, i) => (out[s.id] = i + 1));
  return out;
}

/**
 * **하던 문제는 위로, 끝낸 문제는 맨 밑으로** (2026-10-20 선생님).
 *
 * 1. 진행 중 — 가장 최근에 만진 것이 맨 위
 * 2. 아직 안 한 것 — 오답률 높은 순 (Top1, Top2 …)
 * 3. 끝낸 것 — 역시 최근 것이 위
 */
function ordered(all: LessonSet[], status: Record<string, SetStatus>): LessonSet[] {
  const sets = byWrongRate(all);
  const recent = (a: LessonSet, b: LessonSet) => (status[b.id]?.lastAt ?? "").localeCompare(status[a.id]?.lastAt ?? "");
  const state = (s: LessonSet) => status[s.id]?.state ?? "new";
  return [
    ...sets.filter((s) => state(s) === "doing").sort(recent),
    ...sets.filter((s) => state(s) === "new"),
    ...sets.filter((s) => state(s) === "done").sort(recent),
  ];
}

/** 학생 단계 — 고 1~2등급 · 중 3~5등급 · 초 6~8등급 */
const LEVELS: [StudentLevel, string][] = [["고", "1~2등급"], ["중", "3~5등급"], ["초", "6~8등급"]];

type Props = {
  learnerName: string | null;
  /** 열어 둔 중분류. null이면 중분류 목록 */
  collection: LessonCollection | null;
  onOpenCollection: (collection: LessonCollection) => void;
  onBack: () => void;
  onPickSet: (set: LessonSet) => void;
  /** 단어장 · 내 노트 열기 */
  onOpenSaved: (kind: SavedKind) => void;
  /** 미니 모의고사 열기 */
  onOpenMini: (mockId: string) => void;
  /** 홈(마을)으로 */
  onHome?: () => void;
};

export function LessonList({
  learnerName,
  collection,
  onOpenCollection,
  onBack,
  onPickSet,
  onOpenSaved,
  onOpenMini,
  onHome,
}: Props) {
  const progress = loadProgress();
  const status = setStatuses(progress);
  const vocabCount = loadVocab().length;
  // 학생 단계 — 수업에서 보일 화면이 달라진다 (영어를 돕는 화면만). 정하지 않았으면 중으로 수업한다
  const [level, setLevel] = useState<StudentLevel | undefined>(() => loadStudentState().level);
  const pickLevel = (next: StudentLevel) => {
    saveStudentState({ ...loadStudentState(), level: next });
    setLevel(next);
  };
  const noteCount = loadNotes().length;
  const ranks = collection ? topRanks(setsIn(collection.id)) : {};

  return (
    <div className="stage-fill home">
      <ClassroomBg />

      <header className="top-bar">
        {collection ? (
          <button type="button" className="icon-btn light" title="목록으로" onClick={onBack}>
            <BackIcon />
          </button>
        ) : onHome ? (
          <button type="button" className="icon-btn light" title="홈으로" onClick={onHome}>
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
        {collection ? (
          <>
            <p className="home-hello">{collection.subtitle}</p>
            <h1 className="home-title">{collection.title}</h1>
            <ul className="set-list">
              {ordered(setsIn(collection.id), status).map((set) => {
                const st = status[set.id];
                const done = st?.state === "done";
                const doing = st?.state === "doing";
                const record = statusLine(st);
                return (
                  <li key={set.id}>
                    <button
                      type="button"
                      className={`set-card${done ? " done" : ""}${doing ? " doing" : ""}`}
                      onClick={() => onPickSet(set)}
                    >
                      <strong className="set-title">
                        {ranks[set.id] ? <span className="set-top">Top{ranks[set.id]}</span> : null}
                        {set.title}
                        {set.wrong_rate != null ? <span className="set-rate">(오답률 {set.wrong_rate}%)</span> : null}
                        {done ? <span className="done-mark">완료</span> : null}
                        {doing ? <span className="done-mark doing">진행 중</span> : null}
                      </strong>
                      <span className="set-subtitle">{set.subtitle}</span>
                      {record ? <span className="set-record">{record}</span> : null}
                      <span className="set-meta">
                        <span className="set-count">{sentenceCount(set)}문장</span>
                        <span className="set-go">
                          {st?.resumable ? "이어서 하기" : done ? "다시 풀기" : "시작하기"}
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
            <div className={`level-row${level ? "" : " unset"}`}>
              <span className="level-label">{level ? "내 등급" : "최근 모의고사 영어 등급을 골라 주세요"}</span>
              <div className="level-chips" role="group" aria-label="내 영어 등급">
                {LEVELS.map(([lv, label]) => (
                  <button
                    key={lv}
                    type="button"
                    className={`level-chip${level === lv ? " on" : ""}`}
                    aria-pressed={level === lv}
                    onClick={() => pickLevel(lv)}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>
            <div className="my-shelf">
              <button type="button" className="shelf-btn" onClick={() => onOpenSaved("vocab")}>
                <b>📒 단어장</b>
                <small>저장한 단어 {vocabCount}개</small>
              </button>
              <button type="button" className="shelf-btn" onClick={() => onOpenSaved("notes")}>
                <b>⭐ 내 노트</b>
                <small>헷갈린 포인트 {noteCount}개</small>
              </button>
            </div>
            <section className="group">
              <h2 className="group-title">
                미니 모의고사
                <small>시간 재며 풀고 · 바로 채점 · 분석까지</small>
              </h2>
              <ul className="set-list">
                {allMiniMocks().map((m) => {
                  const last = loadAttempts(m.id)[0];
                  const s = last ? scoreOf(m, last.answers) : null;
                  return (
                    <li key={m.id}>
                      <button type="button" className="set-card" onClick={() => onOpenMini(m.id)}>
                        <span className="set-tag">⏱ {m.minutes}분</span>
                        <strong className="set-title">{m.title}</strong>
                        <span className="set-subtitle">{m.subtitle}</span>
                        <span className="set-meta">
                          <span className="set-count">{s ? `지난 점수 ${s.score}/${s.max}점` : `${m.items.length}문항`}</span>
                          <span className="set-go">
                            {s ? "다시 풀기" : "풀어 보기"}
                            <ArrowIcon />
                          </span>
                        </span>
                      </button>
                    </li>
                  );
                })}
              </ul>
            </section>
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


