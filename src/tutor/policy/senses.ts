/**
 * 다의 기능어(to, for, as, that, which, so, but, yet, if, while, since)의 **그 자리 쓰임과 뜻**.
 * 사전 뜻을 그대로 띄우면 문맥과 다른 뜻이 뜬다(to make의 to가 「~로」로). 레슨을 만들 때 문장마다
 * 나온 순서대로 적어 둔다 — `content/tutor/function-senses/<레슨 id>.json`, 키는 문장 id.
 * 쉬운 쓰임이든 어려운 쓰임이든 다 적는다(누르면 보이는 뜻). 먼저 짚어 줄 어려운 쓰임은 함정 단어 목록에서.
 */
export type FunctionSense = { word: string; phrase: string; sense: string; usage: string };

const FILES = import.meta.glob("../../../content/tutor/function-senses/*.json", { eager: true, import: "default" }) as Record<
  string,
  Record<string, FunctionSense[]>
>;

const BY_LESSON: Record<string, Record<string, FunctionSense[]>> = Object.fromEntries(
  Object.entries(FILES).map(([path, data]) => [path.replace(/^.*\//, "").replace(/\.json$/, ""), data]),
);

/** 다의 기능어 — 레슨 문장에 나오면 쓰임을 적어야 한다 (규칙 테스트) */
export const SENSE_WORDS = ["to", "for", "as", "since", "while", "that", "which", "so", "but", "yet", "if"];

export function sensesOf(lessonId: string, sentenceId: number): FunctionSense[] {
  return BY_LESSON[lessonId]?.[String(sentenceId)] ?? [];
}

export function hasSenses(lessonId: string): boolean {
  return lessonId in BY_LESSON;
}
