import type { ExamQuestion } from "./policy/types";

/** 빈칸 표기 → 듣기에서 그 자리에 넣을 말 */
export type SpeakBlank = { mark: string; say: string };

function underlineMarks(exam: ExamQuestion): string[] {
  if (!exam.underline) return [];
  return Array.isArray(exam.underline) ? exam.underline : [exam.underline];
}

/**
 * 시험 빈칸을 정답 말로 짝짓는다.
 * 빈칸이 하나면 정답 보기 전체(Compassion, 긴 구, 듣기 응답 문장).
 * (A)·(B)처럼 빈칸이 둘이면 정답 보기의 `······` 양쪽.
 */
export function speakBlanksOf(exam: ExamQuestion | undefined): SpeakBlank[] {
  if (!exam) return [];
  const marks = underlineMarks(exam).filter((u) => /_{2,}/.test(u));
  if (!marks.length) return [];
  const label = exam.options.find((o) => o.correct)?.label?.trim() ?? "";
  if (!label) return [];
  const parts = label.split(/\s*[·•…]{2,}\s*|\s+\/\s+/).map((s) => s.trim()).filter(Boolean);
  const says =
    marks.length >= 2 && parts.length >= marks.length
      ? parts.slice(0, marks.length)
      : marks.length === 1
        ? [label]
        : parts.length
          ? parts
          : [label];
  return marks.flatMap((mark, i) => {
    const say = says[i];
    return say ? [{ mark, say }] : [];
  });
}

/**
 * 음성으로 읽을 문장.
 * `________`을 그대로 넘기면 엔진이 "underscore"라고 읽는다.
 * 정답 말이 있으면 그 자리에 넣고, 없으면 빈칸만 빼서 읽는다.
 * 화면에 보이는 문장은 바꾸지 않는다.
 */
export function applySpeakBlanks(text: string, blanks: SpeakBlank[] | undefined): string {
  if (!text || !/_{2,}/.test(text)) return text;
  let out = text;
  const usable = (blanks ?? []).filter((b) => b.mark && b.say && out.includes(b.mark));
  const ordered = [...usable].sort((a, b) => b.mark.length - a.mark.length);
  for (const b of ordered) out = out.split(b.mark).join(b.say);
  out = out.replace(/_{2,}/g, " ");
  return out.replace(/[ \t]{2,}/g, " ").replace(/\s+([,.;!?])/g, "$1").trim();
}
