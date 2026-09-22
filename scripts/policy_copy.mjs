#!/usr/bin/env node
/**
 * Teaching Policy 레슨의 **대사 뽑기** 도구.
 *
 *   가르치는 내용 (말투 없음)            대사 (다정쌤 말투)
 *   content/tutor/policy-lessons/*.json → content/tutor/policy-copy/<캐릭터>/*.json
 *        └ brief                              └ 생성물
 *
 * **LLM은 여기서만 쓴다 — 대사를 만들 때 한 번.** 학생이 수업을 들을 때는 뽑아 둔
 * JSON을 읽기만 하므로 모델을 부르지 않는다.
 *
 *   node scripts/policy_copy.mjs check          brief가 바뀌었는데 대사를 안 뽑은 곳
 *   node scripts/policy_copy.mjs prompt [id]    그 자리들을 LLM에게 맡길 지시문을 찍는다
 *   node scripts/policy_copy.mjs stamp [id]     대사를 고친 뒤, 지금 brief에 맞췄다고 도장
 *
 * 대사는 **통째로 다시 뽑지 않는다.** 한 번 검수한 문장이 다음 빌드에서 바뀌면
 * 검수가 무의미해진다. brief가 바뀐 자리만 다시 뽑는다 (도장 = brief의 해시).
 */
import { readFileSync, writeFileSync, readdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const LESSONS = join(ROOT, "content/tutor/policy-lessons");
const CHARACTER = process.env.CHARACTER ?? "dajung";
const COPY = join(ROOT, "content/tutor/policy-copy", CHARACTER);

/** `src/tutor/policy/copy.ts`의 `stampOf`와 같은 계산이어야 한다 (테스트가 맞춰 본다) */
export function stampOf(value) {
  const text = JSON.stringify(value);
  let h = 5381;
  for (let i = 0; i < text.length; i++) h = ((h * 33) ^ text.charCodeAt(i)) >>> 0;
  return h.toString(36);
}

const stepSource = (step) => ({
  brief: step.brief,
  options: (step.options ?? []).map((o) => [o.id, o.label, !!o.correct]),
});

function load(id) {
  const lesson = JSON.parse(readFileSync(join(LESSONS, `${id}.json`), "utf8"));
  const path = join(COPY, `${id}.json`);
  const copy = existsSync(path)
    ? JSON.parse(readFileSync(path, "utf8"))
    : { lesson: id, character: CHARACTER, helps: {}, steps: {} };
  return { lesson, copy, path };
}

/** [자리, 지금 brief의 도장, 재료] */
function slots(lesson) {
  const out = [["lesson", stampOf(lesson.brief), { brief: lesson.brief }]];
  for (const sentence of lesson.sentences) {
    for (const help of sentence.helps ?? []) {
      out.push([`helps.${help.id}`, stampOf(help.brief), { sentence: sentence.text, label: help.label, brief: help.brief }]);
    }
    for (const step of sentence.steps) {
      out.push([
        `steps.${step.id}`,
        stampOf(stepSource(step)),
        { sentence: step.display ?? sentence.text, type: step.type, interaction: step.interaction, options: step.options, brief: step.brief },
      ]);
    }
  }
  return out;
}

function stampIn(copy, slot) {
  if (slot === "lesson") return copy.from;
  const [kind, id] = slot.split(".");
  return copy[kind]?.[id]?.from;
}

function stale({ lesson, copy }) {
  return slots(lesson).filter(([slot, stamp]) => stampIn(copy, slot) !== stamp);
}

const ids = (only) =>
  only ? [only] : readdirSync(LESSONS).filter((f) => f.endsWith(".json")).map((f) => f.slice(0, -5));

const [mode = "check", only] = process.argv.slice(2);

if (mode === "check") {
  let bad = 0;
  for (const id of ids(only)) {
    const list = stale(load(id));
    bad += list.length;
    console.log(`${list.length ? "✗" : "✓"} ${id}${list.length ? "\n  " + list.map(([s]) => s).join("\n  ") : ""}`);
  }
  process.exit(bad ? 1 : 0);
}

if (mode === "stamp") {
  for (const id of ids(only)) {
    const { lesson, copy, path } = load(id);
    for (const [slot, stamp] of slots(lesson)) {
      if (slot === "lesson") copy.from = stamp;
      else {
        const [kind, key] = slot.split(".");
        if (!copy[kind]?.[key]) throw new Error(`${id}: 대사가 없다 — ${slot}`);
        copy[kind][key].from = stamp;
      }
    }
    writeFileSync(path, JSON.stringify(copy, null, 2) + "\n");
    console.log(`stamped ${id}`);
  }
}

if (mode === "prompt") {
  const voice = readFileSync(join(ROOT, "content/tutor/policy-copy", CHARACTER, "VOICE.md"), "utf8");
  for (const id of ids(only)) {
    const list = stale(load(id));
    if (!list.length) continue;
    console.log(voice);
    console.log(`\n---\n레슨: ${id}\n아래 자리마다 brief와 **같은 키**로 대사를 써서 JSON으로 돌려주세요.\n`);
    console.log(JSON.stringify(Object.fromEntries(list.map(([slot, , material]) => [slot, material])), null, 2));
  }
}
