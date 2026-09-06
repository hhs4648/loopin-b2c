/**
 * 학생 이름.
 *
 * 수업을 "안녕하세요, 민준님!"으로 열려면 이름이 필요하다. 물어보는 건 한
 * 번뿐이고, 그다음부터는 이 브라우저에 남은 걸 쓴다.
 *
 * **서버에 올리지 않는다.** 이름은 수업 진행에 쓰는 호칭일 뿐이고, 난이도
 * 집계(`sessions`·`point_attempts`)는 익명 uid로 이미 이어진다. 실명을 굳이
 * 서버에 두면 지켜야 할 것만 늘어난다.
 */

const KEY = "dajung.learner_name";

/** 이름으로 받아 줄 모양 — 한글·영문 1~10자 */
const SHAPE = /^[가-힣a-zA-Z]{1,10}$/;

/*
  이름 자리에 흔히 오는 **이름 아닌 말**. 모양만 보면 다 통과해서
  ("안녕하세요"도 한글 5자다) 따로 막는다.
*/
const NOT_A_NAME = new Set([
  "안녕",
  "안녕하세요",
  "네",
  "응",
  "예",
  "아니",
  "아니요",
  "몰라",
  "비밀",
  "없어",
  "그냥",
  "싫어",
  "학생",
  "나",
  "저",
]);

const PREFIX = /^(제\s*이름은|내\s*이름은|이름은|저는|나는|난)\s*/;
/*
  꼬리를 떼는 순서가 중요하다. "민준이요"에서 "요"부터 떼면 "민준이"가 남는다.
  긴 것부터 본다.
*/
const SUFFIXES = [
  /(이|라)라고\s*(해요|합니다|불러요|불러주세요)$/,
  /(이라고|라고)\s*(해요|합니다|불러요|불러주세요)$/,
  /입니다$/,
  /이에요$/,
  /이예요$/,
  /예요$/,
  /이야$/,
  /이요$/,
  /요$/,
  /임$/,
];

/**
 * 학생이 적은 말에서 이름만 꺼낸다.
 *
 * 이름을 못 알아보면 **null을 준다.** 그러면 수업은 이름 없이 그냥 시작한다 —
 * 이름을 받아내겠다고 두 번, 세 번 되묻는 건 수업이 아니다.
 */
export function parseName(raw: string): string | null {
  let text = raw.trim().replace(/[.!?~,·^]+$/u, "").trim();
  text = text.replace(PREFIX, "").trim();
  // 꼬리를 떼기 전에 본다 — "안녕하세요"에서 "예요"를 떼면 "안녕하세"가 남는다
  if (NOT_A_NAME.has(text)) return null;
  for (const suffix of SUFFIXES) {
    // 안 걸린 꼬리를 떼면 원문이 그대로 나온다 — 먼저 걸리는지부터 본다
    if (!suffix.test(text)) continue;
    const stripped = text.replace(suffix, "").trim();
    /*
      **먼저 걸린 꼬리가 결정한다.** "비밀이요"에서 "이요"를 떼면 "비밀"이고,
      그건 이름이 아니다. 여기서 그냥 넘기면 다음 꼬리("요")가 "비밀이"를
      이름으로 만들어 낸다.
    */
    if (stripped && SHAPE.test(stripped)) {
      return NOT_A_NAME.has(stripped) ? null : stripped;
    }
  }
  return SHAPE.test(text) && !NOT_A_NAME.has(text) ? text : null;
}

export function loadLearnerName(): string | null {
  try {
    const saved = window.localStorage.getItem(KEY)?.trim();
    return saved && SHAPE.test(saved) ? saved : null;
  } catch {
    // 사파리 프라이빗 모드 등. 이름이 없을 뿐이고 수업은 그대로 돈다
    return null;
  }
}

export function saveLearnerName(name: string | null): void {
  try {
    if (name) window.localStorage.setItem(KEY, name);
    else window.localStorage.removeItem(KEY);
  } catch {
    /* 저장 못 해도 이번 수업에는 이름이 있다 */
  }
}
