import { loadTester } from "../tutor/tester";

/** 테스터 기기면 화면 왼쪽 아래에 작게 「테스터: 헌석」 — 표시가 붙었는지 바로 보이게 */
export function TesterBadge() {
  const name = loadTester();
  if (!name) return null;
  return (
    <div className="tester-badge" aria-hidden="true">
      테스터: {name}
    </div>
  );
}
