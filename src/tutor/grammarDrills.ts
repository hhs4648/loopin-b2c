/**
 * 문법 drill — 보충학습실에서 푸는 10문제. 자료는 `content/tutor/grammar-drills/<id>.json`.
 *
 * 객관식(`choice`)은 보기를 고르고, 주관식(`input`)은 빈칸에 들어갈 영어를 직접 쓴다.
 * 채점은 모델 없이 — 주관식은 소문자·공백·아포스트로피를 맞춘 뒤 `answers` 중 하나와 같으면 맞다.
 */

export type DrillItem =
  | {
      type: "choice";
      /** 빈칸이 든 문장 (___) */
      sentence: string;
      /** 한국어 뜻 — 문장 아래 작게 */
      ko?: string;
      options: string[];
      /** 정답 보기 (options 안의 글) */
      answer: string;
      /** 틀렸을 때 「아쉽게도 틀렸어요.」 뒤 이유 */
      why: string;
    }
  | {
      type: "input";
      sentence: string;
      ko?: string;
      /** 맞다고 볼 답들 — 빈칸 전체에 들어갈 말 */
      answers: string[];
      why: string;
    };

export type GrammarDrill = {
  id: string;
  /** 「nor 도치」 */
  title: string;
  /** drill 위에 접어 둔 한 줄 정리들 */
  rules: string[];
  items: DrillItem[];
};

const FILES = import.meta.glob("../../content/tutor/grammar-drills/*.json", { eager: true, import: "default" }) as Record<
  string,
  GrammarDrill
>;

const DRILLS: Record<string, GrammarDrill> = Object.fromEntries(Object.values(FILES).map((d) => [d.id, d]));

export function getGrammarDrill(id: string): GrammarDrill | null {
  return DRILLS[id] ?? null;
}

export function allGrammarDrills(): GrammarDrill[] {
  return Object.values(DRILLS);
}

/** 주관식 답 맞추기 — 대소문자·띄어쓰기·’/' 차이는 보지 않는다 */
export function normalizeAnswer(s: string): string {
  return s
    .toLowerCase()
    .replace(/[’‘`]/g, "'")
    .replace(/[.,!?]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function isRightInput(item: Extract<DrillItem, { type: "input" }>, typed: string): boolean {
  const t = normalizeAnswer(typed);
  return item.answers.some((a) => normalizeAnswer(a) === t);
}
