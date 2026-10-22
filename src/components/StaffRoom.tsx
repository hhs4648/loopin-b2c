import { useState, type CSSProperties } from "react";
import { LINES, saveTeacher, speak, TEACHERS, type Teacher } from "../tutor/teacher";
import { TeacherFigure, useTeacher } from "./TeacherFigure";

const INTRO_LINE = "여기서 함께 공부할 선생님을 고를 수 있어요.\n선생님과 함께 공부한 시간이 늘어날수록 친밀도가 올라가요.";

/**
 * 교무실 — 선생님 고르기 (2026-10-22 선생님).
 *
 * 쌤을 누르는 순간 **앱 전체가** 그 쌤으로 바뀐다(그림·이름·색·말투). 확인 버튼은 없다.
 * 쌤을 바꾸면 새 쌤이 앞 쌤에게 한마디(표의 「선생님 간 상호작용」), 말풍선을 누르면
 * 첫 인사 → 자유 멘트를 돌아가며 말한다.
 *
 * 예전 `public/staff/loopin-staff-room-raised.html`(그림이 박힌 5.9MB 한 장)은 이 화면으로 바꿨다.
 * 배경은 그 파일에서 꺼낸 `public/assets/staff/room.webp`.
 */
export function StaffRoom({ onClose, intro = false }: { onClose: () => void; intro?: boolean }) {
  const teacher = useTeacher();
  // 지금 말풍선 — 처음엔 첫 인사, 쌤을 바꾸면 앞 쌤에게 하는 말.
  // 체험 분석 직후 처음 들어왔으면(intro) 쌤 고르기·친밀도 안내부터 (2026-10-22 선생님)
  const [say, setSay] = useState<{ text: string; i: number }>(() => ({
    text: intro ? speak(INTRO_LINE, teacher) : LINES[teacher.id].greet,
    i: 0,
  }));

  const pick = (t: Teacher) => {
    if (t.id === teacher.id) return;
    const prev = teacher;
    saveTeacher(t.id);
    setSay({ text: LINES[t.id].meet[prev.id] ?? LINES[t.id].greet, i: 0 });
  };

  const nextLine = () => {
    const pool = [LINES[teacher.id].greet, ...LINES[teacher.id].free];
    const i = (say.i + 1) % pool.length;
    setSay({ text: pool[i]!, i });
  };

  return (
    <div className="stage-fill staff">
      <header className="staff-top">
        <button type="button" className="staff-back" onClick={onClose}>
          ← 마을
        </button>
        <h1 className="staff-title">교무실</h1>
      </header>

      <section className="staff-room" aria-label="교무실">
        <img className="staff-bg" src="/assets/staff/room.webp" alt="" width={900} height={1125} draggable={false} />
        <div className="staff-teacher" key={teacher.id}>
          <TeacherFigure />
        </div>
        {/* 같은 그림의 책상 앞부분만 쌤 앞에 — 쌤이 책상 뒤에 선다 */}
        <img className="staff-bg staff-desk" src="/assets/staff/room.webp" alt="" width={900} height={1125} draggable={false} />
        <button type="button" className="staff-dialogue" onClick={nextLine} aria-label="다음 말 보기">
          <span className="staff-name">{teacher.name}</span>
          <span className="staff-message" aria-live="polite">
            {say.text}
          </span>
          <span className="staff-next" aria-hidden="true">
            ▼
          </span>
        </button>
      </section>

      <section className="staff-picker" aria-label="선생님 선택">
        <p className="staff-heading">함께할 선생님을 골라요</p>
        <div className="staff-list">
          {TEACHERS.map((t) => (
            <button
              key={t.id}
              type="button"
              className="staff-choice"
              aria-pressed={t.id === teacher.id}
              style={{ "--tc": t.color } as CSSProperties}
              onClick={() => pick(t)}
            >
              <span className="staff-portrait">
                <img src={t.art.base} alt="" width={650} height={616} draggable={false} />
              </span>
              {t.name}
              <small>{t.banmal ? "반말" : "존댓말"}</small>
            </button>
          ))}
        </div>
        <p className="staff-hint">고른 선생님이 모든 수업에 함께해요.</p>
      </section>
    </div>
  );
}
