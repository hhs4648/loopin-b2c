/**
 * 미니 모의고사에서 두 번 두드린 「모르는 단어」의 뜻 — 그 문항의 분석 레슨이 단 뜻(glosses·핵심어)에서 찾는다.
 * 수업 중 LLM은 부르지 않는다. 못 찾으면 빈 뜻(분석·해설에서 확인).
 */
import { allPolicyLessons } from "./policy/lessons";

let byLesson: Map<string, Map<string, string>> | null = null;
let all: Map<string, string> | null = null;

const norm = (w: string) => w.toLowerCase().replace(/[’']/g, "'").replace(/^[^a-z0-9]+|[^a-z0-9]+$/g, "");

function build() {
  byLesson = new Map();
  all = new Map();
  for (const l of allPolicyLessons()) {
    const m = new Map<string, string>();
    const put = (en: string, ko: string) => {
      const k = norm(en);
      if (!k || /\s/.test(en.trim()) || !ko) return;
      if (!m.has(k)) m.set(k, ko);
      if (!all!.has(k)) all!.set(k, ko);
    };
    for (const s of l.sentences) for (const g of s.glosses ?? []) put(g.en, g.ko);
    for (const g of [...(l.key_words?.passage ?? []), ...(l.key_words?.options ?? [])]) put(g.en, g.ko);
    byLesson.set(l.id, m);
  }
}

/** 낱말 그대로 → 끝(-s, -es, -ed, -d, -ing, -ly)을 뗀 꼴 순으로 찾는다 */
function forms(w: string): string[] {
  const out = [w];
  for (const end of ["s", "es", "ed", "d", "ing", "ly"]) if (w.length > end.length + 2 && w.endsWith(end)) out.push(w.slice(0, -end.length));
  if (w.endsWith("ies")) out.push(`${w.slice(0, -3)}y`);
  if (w.endsWith("ied")) out.push(`${w.slice(0, -3)}y`);
  return out;
}

export function cleanWord(token: string): string {
  return token.replace(/^[^A-Za-z0-9]+|[^A-Za-z0-9]+$/g, "");
}

/** lessonIds = 그 문항의 분석 레슨들 (먼저 찾는다) */
export function meaningOf(token: string, lessonIds: string[] = []): string {
  if (!byLesson) build();
  const w = norm(token);
  for (const f of forms(w)) {
    for (const id of lessonIds) {
      const ko = byLesson!.get(id)?.get(f);
      if (ko) return ko;
    }
  }
  for (const f of forms(w)) {
    const ko = all!.get(f);
    if (ko) return ko;
  }
  return "";
}
