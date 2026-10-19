import traps from "../../../content/tutor/word-traps/traps.json" with { type: "json" };
import type { StudentLevel } from "./student-state";

/**
 * 헷갈리는 단어(선생님 엑셀 `content/tutor/word-traps/함정단어.xlsx` → `npm run traps:export`)를
 * 그 단어가 나오는 문장에서 💡 Tip으로 띄운다 (2026-10-16 선생님: 「다 Tip으로 연결해줘」).
 *
 * - 엑셀에서 사용이 **O인 단어만**(선생님이 확인한 것) — 비어 있는 후보는 내보내지 않는다
 * - 「누구에게」 칸(중·초 …)에 학생 단계가 없으면 띄우지 않는다. 비어 있으면 모두에게
 * - 레슨에 손으로 쓴 Tip(같은 단어)이 있으면 그걸 쓴다 — 여기서는 겹치지 않는 것만
 * - 「as much A as B」처럼 A·B 자리가 있으면 앞부분(as much)으로 문장에서 찾는다
 */
type Trap = { word: string; kind: string; mis: string; ko: string; who: string };
export type WordTip = { label: string; text: string; mark: string; word: true };

const BY_LESSON = traps as Record<string, Trap[]>;

/** 문장에서 찾을 말 — A·B 자리 앞까지, 끝 문장부호 없이 */
function needle(word: string): string {
  return word.split(/\s+(?:A|B|~)(?:\s|$)/)[0]!.replace(/[.,;:!?]+$/, "").trim();
}

function appears(text: string, word: string): boolean {
  const n = needle(word).replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/['’]/g, "['’]");
  return new RegExp(`(?<![A-Za-z])${n}(?![A-Za-z])`, "i").test(text);
}

function tipText(t: Trap): string {
  const mis = t.mis && t.mis !== "—" && t.mis !== "-" ? t.mis : "";
  // 받침에 따라 「예요/이에요」가 갈리니 서술어 없이 — 이 글에서 뜻 · (착각하기 쉬운 뜻 아님)
  return mis ? `이 글에서는 → ${t.ko}  ('${mis}' 아님)` : `이 글에서는 → ${t.ko}`;
}

export function trapTips(lessonId: string, sentence: string, level: StudentLevel | undefined): WordTip[] {
  const lv = level ?? "중";
  return (BY_LESSON[lessonId] ?? [])
    .filter((t) => !t.who || t.who.includes(lv))
    .filter((t) => appears(sentence, t.word))
    .map((t) => ({ label: t.word, text: tipText(t), mark: needle(t.word), word: true as const }));
}
