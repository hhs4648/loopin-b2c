# Loopin B2C — Agent instructions

This repo is **Loopin B2C**, the real Loopin product. Apps named haksup are a different product line — do not port haksup UX, copy, or architecture here unless a human explicitly asks.

**The rules live in [`CLAUDE.md`](CLAUDE.md) (Korean). Read it first; it wins over anything here.**

## What the app is

**Loopin** (this B2C repo) is a Korean-language tutor for **수능/모의고사 English reading**. **다정쌤** is the teacher character, not the product name. Each lesson is one high-wrong-rate exam question, taught with that question type's solving method. Students answer with buttons; free text only appears in `translate` steps, graded by rules (regex `need`/`wrong`), never by an LLM.

**No LLM is called during a lesson.** Teacher lines are generated ahead of time from each step's `brief` and stored as JSON (`npm run policy:copy check|prompt|stamp`).

## Read in this order

1. `CLAUDE.md` — product rules, lesson flow, code map
2. `docs/tutor/policy/AUTHORING_RULES.md` — dated feedback at the top first
3. `docs/tutor/templates/README.md` — shared lesson template + per-type templates
4. `content/tutor/policy-copy/dajung/VOICE.md` — lesson copy voice (write 해요체; 반말 teachers get it converted by `speak()` in `src/tutor/teacher.ts`)
5. `src/tutor/policy/types.ts` — step types (choice · show · think · pick · translate)

`docs/tutor/policy/Loopin_Teaching_Policy_Spec_v0.1.md` is the original engine design; its worked example (2025 Q21, Descartes) was deleted. Use it for background only.

## Hard rules (summary)

- Never reveal the answer before the student tries. A wrong answer starts with 「아쉽게도 틀렸어요.」
- At most **three sentences** of teacher speech per screen, and one question mark
- Every screen teaches English needed to solve *this* question, or it is cut. No background-knowledge lectures
- Lessons made by a generator (`scripts/lessons/gen_*.py`) are edited in the generator, never in the JSON
- After changing rules or shared generator code: `npm run lessons:regen` then `npm run build`
- Do not commit or push unless a human asks
