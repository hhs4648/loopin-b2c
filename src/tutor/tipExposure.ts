/**
 * 되풀이되는 💡 참고 칩(「왜 핵심어만 보나요?」, 「빈칸 문제 요령」…)을 몇 번까지 보일지 — 학생(이 기기) 전체 기준.
 *
 * 2026-10-14 선생님 정책: 수능·모의고사 수업에서 같은 칩은 **세 번**까지. 학생이 한 번도 안 눌렀으면 **다섯 번**까지
 * 보이고 그 뒤로는 띄우지 않는다. 같은 화면에 다시 그려지는 건 한 번으로 센다(화면마다 `appearance` 키).
 */
const KEY = "loopin.tip-exposure.v1";
const OPENED_LIMIT = 3;
const UNOPENED_LIMIT = 5;

type Record_ = { shown: number; opened: boolean; seen: string[] };

function load(): Record<string, Record_> {
  try {
    return JSON.parse(window.localStorage.getItem(KEY) ?? "{}") as Record<string, Record_>;
  } catch {
    return {};
  }
}

function save(all: Record<string, Record_>) {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(all));
  } catch {
    /* 저장 못 하면 이번엔 그냥 보인다 */
  }
}

/** 이 칩을 이 화면에서 보여도 되는가 — 보여 주기로 하면 그 자리에서 한 번 센다 */
export function takeTipShow(label: string, appearance: string): boolean {
  const all = load();
  const r = all[label] ?? { shown: 0, opened: false, seen: [] };
  if (r.seen.includes(appearance)) return true;
  if (r.shown >= (r.opened ? OPENED_LIMIT : UNOPENED_LIMIT)) return false;
  all[label] = { shown: r.shown + 1, opened: r.opened, seen: [...r.seen, appearance].slice(-20) };
  save(all);
  return true;
}

/** 학생이 칩을 눌러 열었다 — 그 뒤로는 세 번까지만 */
export function noteTipOpened(label: string) {
  const all = load();
  const r = all[label] ?? { shown: 1, opened: false, seen: [] };
  all[label] = { ...r, opened: true };
  save(all);
}
