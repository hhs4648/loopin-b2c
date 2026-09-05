/**
 * 다정쌤.
 *
 * 원본은 `assets/상냥한 선생님.svg`(282KB, 비트맵이 박힌 Figma 내보내기)이고,
 * 화면에는 표시 크기에 맞춰 뽑은 `public/assets/dajung-teacher.webp`(39KB)를 쓴다.
 * `public/`에 넣는 건 전부 학생 기기로 내려가므로 원본을 그대로 싣지 않는다.
 *
 * 예전에는 여기서 손으로 그린 SVG를 `height="auto"`로 그렸다. SVG 속성에는
 * `auto`가 없어서 브라우저가 오류를 내고, 높이를 못 잡은 그림이 화면 폭만큼
 * 커져 **얼굴이 말풍선 뒤로 들어갔다.** 크기는 CSS(부모 폭)만으로 정한다.
 */
export function TeacherFigure() {
  return (
    <img
      className="teacher-art"
      src="/assets/dajung-teacher.webp"
      alt="다정쌤"
      width={650}
      height={616}
      draggable={false}
    />
  );
}
