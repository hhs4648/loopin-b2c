/**
 * 연습실 맛보기 — 온보딩에서 연습실을 처음 보여 줄 때 단어·문장·문법 칸이 비어 있으면 몇 개씩 넣어 둔다 (2026-10-22 선생님).
 * 빈 칸만 보면 무엇을 하는 곳인지 모른다 — 방금 본 예시 문제(2026년 3월 30번)에서 고른 것과 기존 문법 연습 하나.
 * 이미 무언가 있는 칸은 건드리지 않는다.
 */
import { addGrammarPractice, loadGrammarPractice } from "./grammarPractice";
import { addNote, loadNotes } from "./notes";
import { getPolicyLesson } from "./policy/lessons";
import { addVocab, loadVocab } from "./vocab";

const LESSON = "moeui-2026-03-30-names-and-differences";
const WORDS = ["abstract away from", "particularities", "individuality", "uniqueness"];
/** 연습할 문장 — 밑줄 낱말이 없는 짧은 문장 */
const SENTENCE_ID = 6;
/** 2022년 3월 29번(어법)에서 담는 nor·so 도치 묶음 */
const GRAMMAR = { id: "nor-so", lessonId: "moeui-2022-03-29-greek-music" };

export function seedPracticeSamples(): void {
  const lesson = getPolicyLesson(LESSON);
  if (!lesson) return;
  if (!loadVocab().length) {
    const glossary = lesson.key_words?.passage ?? [];
    addVocab(
      WORDS.flatMap((en) => {
        const ko = glossary.find((g) => g.en === en)?.ko;
        const sentence = lesson.sentences.find((s) => s.text.includes(en))?.text ?? "";
        return ko ? [{ en, ko, sentence, source: LESSON, kind: en.includes(" ") ? ("phrase" as const) : ("word" as const) }] : [];
      }),
    );
  }
  if (!loadNotes().some((n) => n.key.startsWith("practice:"))) {
    const sen = lesson.sentences.find((s) => s.id === SENTENCE_ID);
    if (sen) addNote({ key: `practice:${sen.text}`, lessonId: LESSON, title: `${sen.id}문장`, text: sen.text });
  }
  if (!loadGrammarPractice().length) addGrammarPractice(GRAMMAR.id, GRAMMAR.lessonId);
}
