#!/usr/bin/env node
/**
 * 생성기로 만든 레슨을 **전부** 다시 만들고 대사에 도장을 찍는다.
 *
 *   npm run lessons:regen          ← 그다음 npm run build
 *
 * 규칙(AUTHORING_RULES)이나 생성기 공용 부분(story_boards.py 등)을 바꾼 뒤에 돌린다.
 * 예전 레슨이 새 규칙과 어긋나면 `npm run build`의 테스트가 잡는다.
 * 생성기는 같은 입력이면 같은 JSON을 낸다 — 아무것도 안 바꿨으면 바뀐 파일이 없어야 한다.
 *
 * 손으로 쓴 레슨(21번)은 생성기가 없어 여기서 건너뛴다. 테스트는 똑같이 받는다.
 */
import { execFileSync } from "node:child_process";
import { readdirSync, readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const DIR = join(ROOT, "scripts", "lessons");

const gens = readdirSync(DIR).filter((f) => /^gen_.*\.py$/.test(f)).sort();
for (const f of gens) {
  const id = readFileSync(join(DIR, f), "utf8").match(/^ID = "([^"]+)"/m)?.[1];
  if (!id) {
    console.error(`✗ ${f}: ID = "…" 줄을 못 찾았어요`);
    process.exit(1);
  }
  execFileSync("python3", [join(DIR, f)], { cwd: ROOT, stdio: "pipe" });
  execFileSync("node", [join(ROOT, "scripts", "policy_copy.mjs"), "stamp", id], { cwd: ROOT, stdio: "pipe" });
  console.log(`✓ ${id}`);
}

const changed = execFileSync(
  "git",
  ["status", "--short", "--", "content/tutor/policy-lessons", "content/tutor/policy-copy"],
  { cwd: ROOT, encoding: "utf8" },
).trim();
console.log(changed ? `\n바뀐 레슨·대사:\n${changed}\n\n→ npm run build 로 확인하세요.` : "\n바뀐 레슨 없음.");
