# Loopin B2C — Agent instructions

This repo is **Loopin B2C**, the real Loopin product. Existing apps named haksup are a different product line. Do not port haksup UX, copy, or architecture here unless a human explicitly asks.

## Tutor work

Loopin’s first AI feature is **다정쌤**: a 1:1 English-sentence interpretation tutor.

Design rule: **the frame is fixed** (stages, fixed lines, treatments). **The model is free only inside that frame** — unexpected answers, natural connectors, partial-credit judgment.

When you change or implement the tutor, read in this order:

1. `docs/tutor/ARCHITECTURE.md` — layers, turn pipeline, LLM contract
2. `docs/tutor/README.md` — map of files
3. `docs/tutor/IMPLEMENTATION.md` — what code must do vs what the LLM may do
4. `content/tutor/prompts/dajung-system.v0.2.md` — paste-ready system prompt
5. `content/tutor/lessons/` + `content/tutor/schema/lesson.schema.json` — swappable lesson data

Do not invent new pedagogy. If a student path is not in the spec, follow the unexpected-error ladder in the spec. Do not reveal the answer before the hint ladder (or the frustration exception) allows it.

## File ownership

- Lesson content lives in JSON under `content/tutor/lessons/`. Changing a sentence should not require rewriting the system prompt.
- Character, absolute rules, session flow, hint ladder, and frustration rules live in the system prompt + `content/tutor/frame.json`. Keep those in sync.
- UI shell is the KakaoTalk HTML prototypes (classroom chat + sentence study). Spec: `docs/tutor/UI.md`. Do not invent a messenger-style transcript.
- UI JSON (`message` / `buttons` / `effect`) maps onto that shell: bubble, pill replies, optional light effect. Wire JSON when the app is built; chat-only prompt tests stay plain text.
