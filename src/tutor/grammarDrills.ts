/**
 * 문법 drill — 보충학습실에서 푸는 10문제. 자료는 `content/tutor/grammar-drills/<id>.json`.
 *
 * 객관식(`choice`)은 보기를 고르고, 주관식(`input`)은 빈칸에 들어갈 영어를 직접 쓴다.
 * 채점은 모델 없이 — 주관식은 소문자·공백·아포스트로피·줄임말을 맞춘 뒤 `answers` 중 하나와 같으면 맞다.
 *
 * drill 여럿은 문법 묶음(`categories/<id>.json`, 예: 「nor / so」 = 기본 개념 · nor vs so · nor vs neither · 작문)으로
 * 묶는다. 수업에서 담는 것도 묶음 id다. 묶음에 안 든 drill은 혼자 한 묶음처럼 보인다.
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
  /** 「writing」이면 작문 — 한국어를 보고 빈칸(뒷부분)을 영어로 쓴다 */
  mode?: "writing";
  /** 「nor 도치」 */
  title: string;
  /**
   * 시작 전 규칙 카드 — 한 줄에 [언제, → 어떻게, 보기]. 「부정문일 땐 → nor + 동사 + 주어」처럼 짧게 (2026-10-20 선생님).
   * 푸는 중에도 💡로 다시 연다
   */
  intro: [string, string, string?][];
  items: DrillItem[];
};

const FILES = import.meta.glob("../../content/tutor/grammar-drills/*.json", { eager: true, import: "default" }) as Record<
  string,
  GrammarDrill
>;

const DRILLS: Record<string, GrammarDrill> = Object.fromEntries(Object.values(FILES).map((d) => [d.id, d]));

/** 문법 묶음 — drill 세트를 순서대로 */
export type GrammarGroup = { id: string; title: string; subtitle?: string; drills: string[] };

const GROUP_FILES = import.meta.glob("../../content/tutor/grammar-drills/categories/*.json", { eager: true, import: "default" }) as Record<
  string,
  GrammarGroup
>;
const GROUPS: Record<string, GrammarGroup> = Object.fromEntries(Object.values(GROUP_FILES).map((g) => [g.id, g]));

/** 담은 id(묶음 또는 drill)가 가리키는 묶음 — drill이면 그 drill이 든 묶음, 없으면 drill 하나짜리 묶음 */
export function groupOf(id: string): GrammarGroup | null {
  if (GROUPS[id]) return GROUPS[id]!;
  const inGroup = Object.values(GROUPS).find((g) => g.drills.includes(id));
  if (inGroup) return inGroup;
  const d = DRILLS[id];
  return d ? { id: d.id, title: d.title, drills: [d.id] } : null;
}

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
    // 줄임말은 풀어서 맞춘다 — can't = cannot = can not, won't = will not, I'm = I am
    .replace(/\bwon't\b/g, "will not")
    .replace(/\bcan't\b|\bcannot\b/g, "can not")
    .replace(/n't\b/g, " not")
    .replace(/'m\b/g, " am")
    .replace(/'ll\b/g, " will")
    .replace(/'re\b/g, " are")
    .replace(/'ve\b/g, " have")
    .replace(/\s+/g, " ")
    .trim();
}

export function isRightInput(item: Extract<DrillItem, { type: "input" }>, typed: string): boolean {
  const t = normalizeAnswer(typed);
  return item.answers.some((a) => normalizeAnswer(a) === t);
}
