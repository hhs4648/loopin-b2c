#!/usr/bin/env node
/**
 * Teaching Policy 레슨 하나를 **공유용 HTML 한 장**으로 뽑는다.
 *
 *   node scripts/build_share.mjs <lesson-id> [out.html]
 *
 * 실제 앱을 그대로 빌드해서(VITE_SHARE_LESSON=<id>) JS·CSS·그림을 파일 하나에 넣는다.
 * 앱을 고치면 이 명령을 다시 돌리기만 하면 된다 — 따로 흉내 낸 코드가 없다.
 * 받은 사람은 더블클릭으로 연다. 밖에서 받아오는 건 글꼴(Google Fonts)뿐이다.
 */
import { execSync } from "node:child_process";
import { readFileSync, writeFileSync, readdirSync, rmSync, mkdirSync } from "node:fs";
import { join, dirname, extname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const [id, out] = process.argv.slice(2);
if (!id) {
  console.error("usage: build_share.mjs <lesson-id> [out.html]");
  process.exit(1);
}

const tmp = join(ROOT, "share", ".build");
rmSync(tmp, { recursive: true, force: true });
execSync(`npx vite build --outDir "${tmp}" --emptyOutDir --logLevel warn`, {
  cwd: ROOT,
  stdio: "inherit",
  env: { ...process.env, VITE_SHARE_LESSON: id },
});

let html = readFileSync(join(tmp, "index.html"), "utf8");
const MIME = { ".webp": "image/webp", ".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml" };
const dataUri = (file) =>
  `data:${MIME[extname(file)]};base64,${readFileSync(file).toString("base64")}`;

/* public/assets의 그림 — 코드와 레슨 JSON 안에 "/assets/…"로 박혀 있다 */
const pictures = readdirSync(join(ROOT, "public/assets")).filter((f) => MIME[extname(f)]);
const inlinePictures = (text) =>
  pictures.reduce((t, f) => t.split(`/assets/${f}`).join(dataUri(join(ROOT, "public/assets", f))), text);

html = html.replace(/<link rel="stylesheet"[^>]*href="\/(assets\/[^"]+\.css)"[^>]*>/g, (_, p) =>
  `<style>${inlinePictures(readFileSync(join(tmp, p), "utf8"))}</style>`,
);
html = html.replace(/<script type="module"[^>]*src="\/(assets\/[^"]+\.js)"[^>]*><\/script>/g, (_, p) => {
  const js = inlinePictures(readFileSync(join(tmp, p), "utf8")).replace(/<\/script/gi, "<\\/script");
  return `<script type="module">${js}</script>`;
});
html = html.replace(/<link rel="modulepreload"[^>]*>/g, "");
html = html.replace(/<link rel="icon"[^>]*>/, "");

const dest = out ?? join(ROOT, "share", `${id}.html`);
mkdirSync(dirname(dest), { recursive: true });
writeFileSync(dest, html);
rmSync(tmp, { recursive: true, force: true });
console.log(`${dest} (${Math.round(html.length / 1024)} KB)`);
