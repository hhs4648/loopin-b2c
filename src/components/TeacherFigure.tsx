import { useSyncExternalStore } from "react";
import { LINES, loadTeacherId, subscribeTeacher, teacherOf, type Mood, type Reaction, type Teacher } from "../tutor/teacher";

/**
 * 고른 쌤 그림 (교무실에서 고른 쌤 — `tutor/teacher.ts`).
 *
 * 그림은 `public/assets/character/teachers/*.webp`(650×616, 장당 30KB 안팎)이다.
 * 원본 svg는 장당 1MB가 넘어 학생 기기로 그대로 내려보내지 않는다.
 *
 * 표정: 맞히면 `happy`, 틀리면 `sorry`. 표정 그림이 있는 쌤(상냥쌤)은 그림을 바꾸고,
 * 없는 쌤은 같은 그림을 통통 튀기거나(맞힘) 고개를 떨군다(틀림) + 작은 표시(✨/💧).
 *
 * 예전에는 여기서 손으로 그린 SVG를 `height="auto"`로 그렸다. SVG 속성에는
 * `auto`가 없어서 브라우저가 오류를 내고, 높이를 못 잡은 그림이 화면 폭만큼
 * 커져 **얼굴이 말풍선 뒤로 들어갔다.** 크기는 CSS(부모 폭)만으로 정한다.
 */
export function useTeacher(): Teacher {
  const id = useSyncExternalStore(subscribeTeacher, loadTeacherId, loadTeacherId);
  return teacherOf(id);
}

export function TeacherFigure({ mood, teacher }: { mood?: Mood | null; teacher?: Teacher }) {
  const current = useTeacher();
  const t = teacher ?? current;
  const src = (mood === "happy" ? t.art.happy : mood === "sorry" ? t.art.sorry : undefined) ?? t.art.base;
  // 표정 그림이 없으면 움직임으로 — 같은 답에 두 번 튀지 않게 key로 다시 그린다
  const moved = mood && !(mood === "happy" ? t.art.happy : t.art.sorry);
  return (
    <span className={`teacher-figure${moved ? ` mood-${mood}` : ""}`} key={`${t.id}-${mood ?? ""}`}>
      <img className="teacher-art" src={src} alt={t.name} width={650} height={616} draggable={false} />
      {moved ? <i className="teacher-mark" aria-hidden="true">{mood === "happy" ? "✨" : "💧"}</i> : null}
    </span>
  );
}

/** 말풍선 위에 붙는 쌤 한마디 (표 대사). 이름표 + 한 줄 */
export function TeacherReaction({ reaction, beside = false }: { reaction?: Reaction | null; beside?: boolean }) {
  const t = useTeacher();
  if (!reaction) return null;
  return (
    <p className={`teacher-react${beside ? " beside" : ""}`} key={reaction}>
      <b>{t.name}</b>
      {LINES[t.id][reaction]}
    </p>
  );
}
