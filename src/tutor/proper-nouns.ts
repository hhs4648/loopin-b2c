import type { ProperNoun } from "../../content/tutor/types";

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
 * 되묻기는 오답이 아니다 — 힌트 사다리를 올리거나 miss로 세면 안 된다
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
