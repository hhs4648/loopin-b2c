import type { LessonChunk, ProperNoun } from "../../content/tutor/types";

/**
 * 고유명사 종류를 학생이 보는 말로.
 *
 * 레슨 JSON의 `type`은 `company`·`place` 같은 영어 키다. 화면 칩과 다정쌤 대사가
 * **같은 말**을 쓰도록 여기 한 곳에서만 옮긴다. 예전에는 문장 학습 화면에만
 * 이 표가 있고 교실 화면은 `회사 이름`이 박혀 있어서, 탈레스 레슨에서는
 * `Miletus · 회사 이름`이 나왔다.
 */
export function nounKind(type?: string): string {
  if (type === "company") return "회사 이름";
  if (type === "place") return "지명";
  if (type === "region") return "지역명";
  if (type === "person") return "사람 이름";
  return "고유명사";
}

/**
 * 학생이 고유명사를 **되물었는지**.
 *
 * 되묻기는 오답이 아니다 — 유도를 올리거나 miss로 세면 안 된다
 * (`ARCHITECTURE.md` §4-2). 해석 시도를 되묻기로 잘못 보면 수업이 헛돌므로,
 * **묻는 티가 나는 문장에서만** 잡는다.
 */
const ASKING =
  /(뭐예요|뭐에요|뭔가요|무슨\s*뜻|뜻이\s*뭐|어떤\s*뜻|누구예요|어디예요|무슨\s*말|뭐야|뭐죠|모르겠는데\s*뭐)/;

export function askedAboutProperNoun(
  text: string,
  nouns: ProperNoun[],
): ProperNoun | null {
  const asking = ASKING.test(text) || /[?？]\s*$/.test(text.trim());
  if (!asking) return null;
  const hit = nouns.find((n) => {
    const bare = n.en.replace(/\.$/, "");
    return text.includes(n.en) || text.includes(bare) || text.includes(n.ko);
  });
  return hit ?? null;
}

/**
 * 학생이 **문장 속 단어의 뜻**을 물었는지. 물었으면 그 단어를 준다.
 *
 * 영어 토큰이 지금 문장 안에 있어야 한다 — 아무 영어나 잡으면 해석 시도를
 * 질문으로 오해한다.
 */
export function askedAboutWord(text: string, sentence: string): string | null {
  if (!ASKING.test(text)) return null;
  const inSentence = new Set(
    (sentence.match(/[A-Za-z][A-Za-z'-]+/g) ?? []).map((w) => w.toLowerCase()),
  );
  const asked = (text.match(/[A-Za-z][A-Za-z'-]+/g) ?? []).find((w) =>
    inSentence.has(w.toLowerCase()),
  );
  return asked ?? null;
}

/**
 * 그 단어가 **이번 문장에서 가르치는 것**인가.
 *
 * 가르치는 단어면 뜻을 그냥 주면 안 된다 — 그게 이 문장의 정답이다. 힌트
 * 사다리로 답한다. 가르치는 대상이 아닌 단어(그냥 막힌 것)는 알려 준다.
 */
export function isTaughtWord(word: string, chunk: LessonChunk): boolean {
  const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const needle = new RegExp(`\\b${escaped}\\b`, "i");
  const haystacks = [
    ...(chunk.scoring_points ?? []).map((p) => p.text),
    ...(chunk.expected_errors ?? []).flatMap((e) => [e.detect, ...(e.signals ?? [])]),
  ];
  return haystacks.some((h) => needle.test(h));
}

/**
 * 「왜요?」 — 이유를 묻는 말인지.
 *
 * 레슨은 원리 설명을 **학생이 물었을 때만** 꺼내도록 적어 둔다
 * (`on_why_question`). 묻기 전에 설명하면 그건 강의다.
 */
const ASKING_WHY = /(왜|어째서|이유가|왠지|왜요|왜 그런|어떻게 그렇)/;

export function askedWhy(text: string): boolean {
  return ASKING_WHY.test(text);
}
