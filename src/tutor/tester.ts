/**
 * 테스터 표시 — 만드는 사람(헌석·수정)의 기기를 학생 기록과 나눈다 (2026-10-21).
 *
 * 기기(브라우저)마다 한 번 주소 끝에 `?tester=헌석`을 붙여 열면 이 브라우저에 남고,
 * 서버(`learner_state`의 `loopin.tester`)에도 사본이 간다. 분석할 때 이 키가 있는 학습자는 뺀다.
 * IP는 집·회사·휴대폰 데이터마다 바뀌어서 못 믿는다 — 표시가 이름을 겸한다.
 *
 * 끄기: `?tester=off`. 시크릿 창·새 브라우저·기록 삭제 뒤에는 다시 붙여야 한다.
 */

import { pushKey } from "./cloud";

export const TESTER_KEY = "loopin.tester";

/** 이름으로 받아 줄 모양 — 한글·영문·숫자 1~20자 */
const SHAPE = /^[가-힣a-zA-Z0-9_-]{1,20}$/;

export function loadTester(): string | null {
  try {
    const saved = window.localStorage.getItem(TESTER_KEY)?.trim();
    return saved && SHAPE.test(saved) ? saved : null;
  } catch {
    return null;
  }
}

/** 앱을 열 때 한 번 — 주소에 `?tester=`가 있으면 저장하거나 지운다 */
export function readTesterFromUrl(): void {
  let value: string | null;
  try {
    value = new URLSearchParams(window.location.search).get("tester");
  } catch {
    return;
  }
  if (value == null) return;
  const name = value.trim();
  try {
    if (name === "off" || name === "") window.localStorage.removeItem(TESTER_KEY);
    else if (SHAPE.test(name)) {
      window.localStorage.setItem(TESTER_KEY, name);
      pushKey(TESTER_KEY);
    }
  } catch {
    /* 저장 못 하면 표시가 안 붙을 뿐 */
  }
}
