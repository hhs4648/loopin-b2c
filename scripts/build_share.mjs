#!/usr/bin/env node
/**
 * Teaching Policy 레슨 하나를 **공유용 HTML 한 장**으로 뽑는다.
 *
 *   node scripts/build_share.mjs <lesson-id> [out.html]
 *
 * 앱을 통째로 싣지 않는다. 레슨 JSON·대사·선생님 그림을 파일 안에 넣고, 세션
 * 로직(`src/tutor/policy/session.ts`)을 바닐라 JS로 **같은 규칙으로** 옮겨 실었다.
 * 학생 상태·기록·단어장 저장은 없다 — 보여 주기용이다. 앱이 바뀌면 다시 뽑는다.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const [id, out] = process.argv.slice(2);
if (!id) {
  console.error("usage: build_share.mjs <lesson-id> [out.html]");
  process.exit(1);
}

const lesson = JSON.parse(readFileSync(join(ROOT, "content/tutor/policy-lessons", `${id}.json`), "utf8"));
const copy = JSON.parse(readFileSync(join(ROOT, "content/tutor/policy-copy/dajung", `${id}.json`), "utf8"));
const frame = JSON.parse(readFileSync(join(ROOT, "content/tutor/frame.json"), "utf8"));
const pframe = JSON.parse(readFileSync(join(ROOT, "content/tutor/policy-frame.json"), "utf8"));
const teacher = readFileSync(join(ROOT, "public/assets/dajung-teacher.webp")).toString("base64");

const DATA = { lesson, copy, lines: { ...frame.fixed_lines, ...pframe.lines }, buttons: pframe.buttons };

const html = `<meta charset="utf-8">
<title>다정쌤 · 21번 데카르트의 나무</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;600;700&display=swap">
<style>
:root {
  --page: #efe6dc; --page-ink: #5b4f57;
  --paper: #f7efe6; --ink: #2b2430; --muted: #8a7f88; --line: #e6d8cc;
  --pink: #ef7a93; --pink-ink: #e2607d; --mint: #8fd0c0; --mint-ink: #3f9a86; --mint-bg: #eefaf6;
  --em: #e2607d; --hl: rgba(255,214,102,.55); --star: #f2c33d;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --page: #1d1719; --page-ink: #cfc3c9; } }
:root[data-theme="dark"] { --page: #1d1719; --page-ink: #cfc3c9; }
html, body { height: 100%; }
body { margin: 0; background: var(--page); color: var(--page-ink); font-family: "Noto Sans KR", -apple-system, sans-serif; }
.wrap { min-height: 100%; display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 16px; box-sizing: border-box; }
.note { font-size: 12px; opacity: .75; text-align: center; max-width: 390px; }
.phone {
  position: relative; width: 390px; max-width: 100%; height: 780px; max-height: calc(100dvh - 60px);
  background: var(--paper); border-radius: 28px; overflow: hidden; box-shadow: 0 20px 60px rgba(60,30,20,.25);
  color: var(--ink); container-type: size;
}
.screen { position: absolute; inset: 0; display: flex; flex-direction: column; }
button { font: inherit; cursor: pointer; }
button:focus-visible { outline: 2px solid var(--pink-ink); outline-offset: 2px; }

/* 교실 (인트로·마무리) */
.chat { background: linear-gradient(#f3ebe1 0 70%, #d7b79a 70% 100%); }
.chat .top { display: flex; align-items: center; gap: 10px; padding: 16px; }
.chat .avatar { width: 34px; height: 34px; border-radius: 50%; background: var(--pink); color: #fff; display: grid; place-items: center; font-weight: 700; }
.chat .name { font-weight: 700; font-size: 14px; } .chat .sub { font-size: 11px; color: var(--muted); }
.chat .stage { position: relative; flex: 1; }
.chat .teacher { position: absolute; left: 50%; bottom: 14%; transform: translateX(-50%); width: 56%; }
.chat .bubble { position: absolute; left: 50%; transform: translateX(-50%); bottom: calc(14% + 56cqw * .95 + 8px); width: max-content; max-width: 86%; }
.chat .dock { padding: 0 14px 18px; display: flex; flex-direction: column; gap: 10px; }

/* 문장 학습 */
.study .top { display: flex; align-items: center; justify-content: space-between; padding: 14px 14px 0; }
.icon { width: 44px; height: 44px; border-radius: 50%; border: none; display: grid; place-items: center; }
.icon.light { background: #fff; color: var(--ink); box-shadow: 0 6px 16px rgba(60,30,20,.1); } .icon.dark { background: #2b2430; color: #fff; }
.progress { display: flex; flex-direction: column; align-items: center; gap: 6px; font-size: 12px; font-weight: 600; color: var(--muted); letter-spacing: .04em; }
.dots { display: flex; gap: 5px; } .dots i { width: 8px; height: 5px; border-radius: 3px; background: var(--line); } .dots i.on { width: 18px; background: var(--pink); }
.sentence { flex: 0 1 auto; min-height: 0; max-height: 34cqh; overflow-y: auto; padding: 18px 24px 8px; }
.study.has-panel .sentence { max-height: 30cqh; }
.english { margin: 0; font-family: "Gowun Dodum", "Noto Sans KR", sans-serif; font-size: clamp(17px, 5.6cqw, 24px); line-height: 1.4; font-weight: 500; letter-spacing: -.01em; overflow-wrap: break-word; }
.tok { position: relative; display: inline-block; }
.word { font: inherit; color: inherit; background: none; border: none; padding: 0 1px; margin: 0; border-radius: 4px; text-decoration: underline dotted rgba(239,122,147,.5); text-underline-offset: 4px; }
.word:hover, .tok.open .word { background: rgba(239,122,147,.16); }
.word.em { color: var(--em); font-weight: 700; text-decoration-color: var(--em); text-decoration-style: solid; }
mark.hl, .tok.hl .word { background: var(--hl); color: inherit; border-radius: 4px; }
.tip { position: absolute; left: 50%; top: calc(100% + 8px); transform: translateX(-50%); z-index: 7; max-width: min(240px, 62cqw); width: max-content; background: #fff; color: var(--ink); font-size: 13px; font-weight: 600; line-height: 1.35; letter-spacing: 0; padding: 7px 11px 7px 8px; border-radius: 12px; box-shadow: 0 8px 20px rgba(60,30,20,.16); border: 1.5px solid #f0d3db; display: flex; gap: 6px; text-align: left; font-family: "Noto Sans KR", sans-serif; }
.tip::after { content: ""; position: absolute; left: 50%; bottom: 100%; transform: translateX(-50%); border: 6px solid transparent; border-bottom-color: #fff; }
.tip .note-txt { color: #9a8f96; font-weight: 500; }
.star { flex: none; width: 22px; height: 22px; margin: -2px 0 0 -1px; padding: 0; border: none; background: none; color: #c9b9c0; display: inline-flex; align-items: center; justify-content: center; border-radius: 50%; }
.star.on { color: var(--star); }
.listen { display: flex; align-items: center; gap: 10px; margin-top: 14px; font-size: 12px; color: #a2969e; }
.listen b { font-weight: 600; color: var(--pink-ink); background: #fff; border-radius: 999px; padding: 10px 14px; box-shadow: 0 6px 16px rgba(60,30,20,.1); }
.helps { flex: none; display: flex; flex-wrap: wrap; gap: 8px; padding: 0 24px 6px; }
.help { height: 30px; padding: 0 12px; border-radius: 999px; border: 1.5px dashed #d9a9b5; background: rgba(255,255,255,.7); color: #b45a70; font-size: 12px; font-weight: 600; }
.panel { flex: none; margin: 2px 18px 0; padding: 10px 14px; border-radius: 16px; background: #fff; box-shadow: 0 6px 16px rgba(60,30,20,.08); font-size: clamp(12px, 3.5cqw, 13.5px); line-height: 1.35; display: flex; flex-direction: column; gap: 6px; }
.panel .title { font-size: 11px; font-weight: 700; color: #a2969e; letter-spacing: .04em; }
.row { display: flex; align-items: baseline; gap: 8px; min-width: 0; }
.lab { flex: none; min-width: 52px; font-size: 11px; font-weight: 700; color: var(--pink-ink); }
.txt { min-width: 0; font-weight: 500; } .txt small { display: block; font-size: 11px; color: var(--muted); font-weight: 500; }
.left { flex: 0 0 38%; font-weight: 600; } .arrow { flex: none; color: #c9b9c0; } .right { color: var(--pink-ink); font-weight: 700; }
.right.blank { color: #c9b9c0; border: 1.5px dashed var(--line); border-radius: 8px; padding: 0 14px; } .right small { display: block; font-size: 11px; font-weight: 500; color: var(--muted); }
.panel.contrast { flex-direction: row; gap: 10px; } .side { flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 3px; } .side + .side { border-left: 1.5px dashed var(--line); padding-left: 10px; } .side strong { font-size: 12px; color: var(--pink-ink); }
.panel.note { background: #fbeef1; box-shadow: none; }
.stage { position: relative; flex: 1 1 auto; min-height: 132px; container-type: size; --mascot: min(42cqw, 52cqh, calc(100cqh - 116px)); }
.study.has-panel .stage { --mascot: min(42cqw, 44cqh, calc(100cqh - 150px)); }
.mascot { position: absolute; left: 50%; bottom: 0; transform: translateX(-50%); width: var(--mascot); z-index: 3; }
.mascot img { display: block; width: 100%; height: auto; animation: bob 3.4s ease-in-out infinite; filter: drop-shadow(0 10px 14px rgba(80,40,30,.18)); }
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
@media (prefers-reduced-motion: reduce) { .mascot img { animation: none; } }
.over { position: absolute; left: 50%; bottom: calc(var(--mascot) * .95 + 10px); transform: translateX(-50%); z-index: 4; width: max-content; max-width: 86cqw; }
.card { position: relative; background: #fff; border-radius: 22px; padding: clamp(12px, 4.1cqw, 16px) clamp(14px, 5.7cqw, 22px); box-shadow: 0 12px 30px rgba(60,30,20,.16), 0 0 0 1px rgba(226,96,125,.18); font-family: "Gowun Dodum", "Noto Sans KR", sans-serif; font-size: clamp(15px, 4.4cqw, 17px); line-height: 1.45; font-weight: 500; text-align: center; min-width: min(200px, 56cqw); box-sizing: border-box; display: flex; flex-direction: column; animation: pop .3s ease-out; }
.card > span { min-height: 0; overflow-y: auto; } .over .card { max-height: calc(100cqh - var(--mascot) * .95 - 16px); }
.tail { position: absolute; left: 50%; bottom: -11px; width: 22px; height: 22px; background: #fff; transform: translateX(-50%) rotate(45deg); border-radius: 4px; }
@keyframes pop { from { opacity: 0; transform: translateY(10px) scale(.96); } to { opacity: 1; transform: none; } }
@container (max-height: 240px) {
  .mascot { display: none; }
  .over { top: 50%; bottom: auto; transform: translate(-50%, -50%); max-width: 92cqw; }
  .over .tail { display: none; } .over .card { max-height: calc(100cqh - 16px); border-radius: 18px; text-align: left; }
}
.dock { flex: none; padding: 0 14px 16px; display: flex; flex-direction: column; gap: 12px; z-index: 6; }
.quick { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px; }
.pill { border: 1.5px solid var(--pink); background: rgba(255,255,255,.94); color: var(--pink-ink); font-weight: 600; font-size: 14px; border-radius: 999px; padding: 0 16px; height: 40px; box-shadow: 0 6px 16px rgba(60,30,20,.12); display: inline-flex; align-items: center; gap: 6px; }
.pill:hover { background: var(--pink); color: #fff; }
.pill.aux { border-color: var(--mint); background: var(--mint-bg); color: var(--mint-ink); box-shadow: none; } .pill.aux:hover { background: var(--mint); color: #fff; }
.num { font-weight: 700; opacity: .85; }
.quick.stack { flex-direction: column; flex-wrap: nowrap; align-items: stretch; gap: 6px; }
.quick.stack .pill { height: auto; min-height: 36px; padding: 7px 14px; border-radius: 16px; font-size: clamp(12.5px, 3.5cqw, 13.5px); line-height: 1.35; text-align: left; word-break: keep-all; align-items: flex-start; }
.quick.stack .pill.aux { align-self: flex-end; min-height: 30px; padding: 4px 12px; border-radius: 999px; }
.input { display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,.95); border-radius: 28px; padding: 6px 6px 6px 18px; box-shadow: 0 8px 24px rgba(60,30,20,.12); }
.input input { flex: 1; border: none; background: none; font: inherit; font-size: 15px; color: var(--ink); outline: none; min-width: 0; }
.input .send { width: 40px; height: 40px; border-radius: 50%; border: none; background: var(--pink); color: #fff; }
</style>

<div class="wrap">
  <div class="phone" id="phone"></div>
  <div class="note">2025년 3월 고3 영어 21번 · Teaching Policy 시연. 단어를 누르면 뜻이 나와요.</div>
</div>

<script>
const DATA = ${JSON.stringify(DATA)};
const TEACHER = "data:image/webp;base64,${teacher}";
const { lesson, copy, lines, buttons: B } = DATA;
const UNKNOWN = "잘 모르겠어요", HINT = "힌트 주세요", READY = "네, 좋아요!";
const NUMERALS = ["①","②","③","④","⑤"];

/* ── 세션 (src/tutor/policy/session.ts와 같은 규칙) ─────────────── */
let s;
function init() {
  s = { stage: "intro", si: 0, pi: 0, resolved: false, rung: 0, wrong: [], thinkHinted: false, struggled: false, skipped: [], aside: null, panel: null, effect: false, saved: {},
    message: [lines.greet_plain, lines.intro_topic.replace("{topic}", copy.topic_intro), lines.ready_question].join(" "), buttons: [READY] };
}
const sen = () => lesson.sentences[s.si];
const step = () => sen().steps[s.pi];
const panelOf = (ref) => !ref ? null : typeof ref === "string" ? (lesson.panels?.[ref] ?? null) : ref;
const linesOf = (st) => copy.steps[st.id];

function shouldShow(st) {
  const when = st.when ?? "always";
  if (when === "if_struggled") return s.struggled;
  return true; // unless_stable: 시연에는 학생 기록이 없으니 늘 보여 준다
}
function buttonsFor(st) {
  if (st.type === "choice") {
    if (s.resolved) return [B.next];
    const left = st.options.filter(o => !s.wrong.includes(o.id)).map(o => o.label);
    const skip = st.skippable && s.rung === 0 && !s.wrong.length ? [B.skip] : [];
    return [...left, UNKNOWN, ...skip];
  }
  if (st.type === "think") return s.resolved ? [B.next] : s.thinkHinted ? [B.thought] : [B.thought, HINT];
  return [st.button ?? B.next];
}
function open(lead) {
  for (;;) {
    if (s.si >= lesson.sentences.length) return finish(lead);
    if (s.pi >= sen().steps.length) { s.si++; s.pi = 0; s.struggled = false; s.skipped = []; continue; }
    const st = step();
    const withSkipped = st.skip_with && s.skipped.includes(st.skip_with);
    if (!withSkipped && shouldShow(st)) break;
    s.pi++;
  }
  const st = step();
  Object.assign(s, { resolved: false, rung: 0, wrong: [], thinkHinted: false, panel: panelOf(st.panel) });
  const body = st.type === "show" ? linesOf(st).say : linesOf(st).ask;
  s.message = (lead + body).trim(); s.buttons = buttonsFor(st);
}
function next(lead = "") { s.pi++; open(lead); }
function finish(lead) { s.stage = "done"; s.message = (lead + copy.closing).trim(); s.buttons = []; s.panel = null; }

function pick(st, text) {
  const open = st.options.filter(o => !s.wrong.includes(o.id));
  const n = text.match(/^([1-9])\\s*번?$/)?.[1];
  if (n) return open[Number(n) - 1] ?? null;
  const t = text.replace(/\\s+/g, "");
  return open.find(o => o.label === text) ?? open.find(o => t.includes(o.label.replace(/\\s+/g, ""))) ?? null;
}
function onChoice(st, text) {
  if (s.resolved) return next();
  const L = linesOf(st);
  const picked = pick(st, text);
  const dontKnow = !picked && /모르|힌트|포기/.test(text);
  if (!picked && !dontKnow) { s.message = (lines.pick_from_buttons + " " + (L.reask ?? "")).trim(); return; }
  if (picked?.correct) {
    const light = s.wrong.length > 0;
    s.struggled = s.struggled || light || s.rung > 0;
    if (st.praise_alone) { s.resolved = true; s.message = L.praise; s.panel = panelOf(st.panel_after) ?? s.panel; s.buttons = buttonsFor(st); s.effect = light; return; }
    next(L.praise + " "); s.effect = light; return;
  }
  if (picked) s.wrong.push(picked.id);
  const remaining = st.options.length - s.wrong.length;
  if (remaining <= 1 || s.rung >= 2) {
    s.resolved = true; s.rung++; s.struggled = true;
    s.message = lines.explain_lead + " " + L.explain; s.panel = panelOf(st.panel_after) ?? s.panel; s.buttons = buttonsFor(st); return;
  }
  const lead = picked ? lines.wrong_lead : lines.dont_know_lead;
  s.message = lead + " " + (s.rung === 0 ? (picked && L.feedback?.[picked.id]) ?? L.hints[0] : L.hints[1]);
  s.rung++; s.struggled = true; s.buttons = buttonsFor(st);
}
function onThink(st, text) {
  if (s.resolved) return next();
  const L = linesOf(st);
  if (text !== B.thought && /모르|힌트/.test(text) && !s.thinkHinted) { s.thinkHinted = true; s.struggled = true; s.message = L.hint; s.buttons = buttonsFor(st); return; }
  s.resolved = true; s.message = L.summary; s.panel = panelOf(st.panel_after) ?? s.panel; s.buttons = buttonsFor(st);
}
function submit(raw) {
  const text = raw.trim();
  if (!text || s.stage === "done") return;
  s.effect = false;
  if (s.stage === "intro") { s.stage = "lesson"; s.si = 0; s.pi = 0; open(lines.start_known); return render(); }
  if (s.aside) { const a = s.aside; s.aside = null; s.message = a.message; s.buttons = a.buttons; if (text === B.back) return render(); }
  const st = step();
  const help = (sen().helps ?? []).find(h => h.label === text);
  if (help) {
    s.aside = s.aside ?? { message: st.type !== "show" && !s.resolved ? (linesOf(st).reask ?? s.message) : s.message, buttons: s.buttons };
    s.message = copy.helps[help.id]?.answer ?? ""; s.buttons = [B.back]; return render();
  }
  if (st.skippable && text === B.skip && !s.resolved) { s.skipped.push(st.id); next(); return render(); }
  if (st.type === "choice") onChoice(st, text); else if (st.type === "think") onThink(st, text); else next();
  render();
}

/* ── 화면 ──────────────────────────────────────────────────────── */
const phone = document.getElementById("phone");
const esc = (t) => t.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
let openTip = null;

function renderPanel(p) {
  if (!p) return "";
  if (p.kind === "structure") return '<div class="panel">' + p.rows.map(r => \`<div class="row"><span class="lab">\${esc(r.label)}</span><span class="txt">\${esc(r.text)}\${r.ko ? "<small>" + esc(r.ko) + "</small>" : ""}</span></div>\`).join("") + "</div>";
  if (p.kind === "mapping") return '<div class="panel">' + (p.title ? \`<div class="title">\${esc(p.title)}</div>\` : "") + p.rows.map(r => \`<div class="row"><span class="left">\${esc(r.left)}</span><span class="arrow">→</span><span class="right\${r.right ? "" : " blank"}">\${esc(r.right ?? "?")}\${r.note ? "<small>" + esc(r.note) + "</small>" : ""}</span></div>\`).join("") + "</div>";
  if (p.kind === "note") return \`<div class="panel note"><span class="lab">\${esc(p.label)}</span><span class="txt">\${esc(p.text)}</span></div>\`;
  return '<div class="panel contrast">' + [p.left, p.right].map(x => \`<div class="side"><strong>\${esc(x.title)}</strong><span>\${esc(x.text)}</span></div>\`).join("") + "</div>";
}

function glossOf(word) {
  const w = word.replace(/[.,;:!?)”’"']+$/g, "").toLowerCase();
  return sen().glosses.find(g => g.en.toLowerCase() === w) ?? null;
}
function renderSentence(text, highlight, emphasis) {
  // 긴 구(what we would call)가 먼저 맞도록 긴 것부터
  const glosses = [...sen().glosses].sort((a, b) => b.en.length - a.en.length);
  const ranges = highlight.map(h => { const i = text.indexOf(h); return i < 0 ? null : [i, i + h.length]; }).filter(Boolean);
  let out = "", i = 0, k = 0;
  while (i < text.length) {
    const rest = text.slice(i);
    const ws = rest.match(/^\\s+/); if (ws) { out += ws[0]; i += ws[0].length; continue; }
    let hit = null;
    for (const g of glosses) { const m = rest.match(new RegExp("^(" + g.en.replace(/[.*+?^\${}()|[\\]\\\\]/g, "\\\\$&") + ")(?![A-Za-z0-9])", "i")); if (m) { hit = { g, len: m[1].length }; break; } }
    const tok = hit ? rest.slice(0, hit.len) : (rest.match(/^[A-Za-z0-9]+(?:['.][A-Za-z0-9]+)*/)?.[0] ?? rest[0]);
    const hl = ranges.some(([a, b]) => i < b && i + tok.length > a);
    if (hit) {
      const em = emphasis.includes(tok.replace(/[.,;:]$/, ""));
      const on = openTip === k;
      const ko = hit.g.ko, at = ko.indexOf(" · ");
      const tip = on ? \`<span class="tip"><button class="star\${s.saved[hit.g.en] ? " on" : ""}" data-star="\${esc(hit.g.en)}" aria-label="단어장"><svg width="16" height="16" viewBox="0 0 24 24" fill="\${s.saved[hit.g.en] ? "currentColor" : "none"}" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1.1 5.9L12 17l-5.3 2.7 1.1-5.9-4.3-4.1 5.9-.8z"/></svg></button><span>\${at < 0 ? esc(ko) : esc(ko.slice(0, at)) + '<span class="note-txt"> · ' + esc(ko.slice(at + 3)) + "</span>"}</span></span>\` : "";
      // 뒤에 붙는 문장부호는 같은 칸에
      const after = text.slice(i + tok.length).match(/^[,.;:!?)”’"']/)?.[0] ?? "";
      out += \`<span class="tok\${on ? " open" : ""}\${hl ? " hl" : ""}"><button class="word\${em ? " em" : ""}" data-tip="\${k}">\${esc(tok)}</button>\${esc(after)}\${tip}</span>\`;
      i += tok.length + after.length; k++; continue;
    }
    out += hl ? \`<mark class="hl">\${esc(tok)}</mark>\` : esc(tok);
    i += tok.length;
  }
  return out;
}

function render() {
  if (s.stage !== "lesson") {
    phone.innerHTML = \`<div class="screen chat">
      <div class="top"><div class="avatar">다</div><div><div class="name">다정쌤</div><div class="sub">21번 문제</div></div></div>
      <div class="stage">
        <div class="bubble"><div class="card"><span>\${esc(s.message)}</span><i class="tail"></i></div></div>
        <div class="teacher"><img src="\${TEACHER}" alt="다정쌤" width="650" height="616" style="width:100%;height:auto;display:block;animation:bob 3.4s ease-in-out infinite;filter:drop-shadow(0 10px 14px rgba(80,40,30,.18))"></div>
      </div>
      <div class="dock"><div class="quick">\${s.stage === "done" ? '<button class="pill" data-send="__restart">다시 보기</button>' : s.buttons.map(b => \`<button class="pill" data-send="\${esc(b)}">\${esc(b)}</button>\`).join("")}</div></div>
    </div>\`;
    return;
  }
  const st = step(), se = sen();
  const shown = st.display ?? se.text;
  const aux = [UNKNOWN, HINT, B.skip];
  const numbered = st.type === "choice" && !s.resolved && !s.aside;
  const stack = s.buttons.some(b => b.length > 18);
  let n = 0;
  const pills = s.buttons.map(b => { const isAux = aux.includes(b); const num = numbered && !isAux ? NUMERALS[n++] : null; return \`<button class="pill\${isAux ? " aux" : ""}" data-send="\${esc(b)}">\${num ? '<span class="num">' + num + "</span>" : ""}\${esc(b)}</button>\`; }).join("");
  const helps = s.pi === 0 ? (se.helps ?? []).map(h => \`<button class="help" data-send="\${esc(h.label)}">\${esc(h.label)}</button>\`).join("") : "";
  phone.innerHTML = \`<div class="screen study\${s.panel ? " has-panel" : ""}">
    <div class="top">
      <button class="icon light" data-send="__restart" title="처음으로">‹</button>
      <div class="progress"><span>문장 학습 · \${s.si + 1} / \${lesson.sentences.length}</span><div class="dots">\${lesson.sentences.map((_, i) => \`<i class="\${i <= s.si ? "on" : ""}"></i>\`).join("")}</div></div>
      <button class="icon dark" data-send="__restart" title="처음으로">×</button>
    </div>
    <div class="sentence"><p class="english">\${renderSentence(shown, st.highlight ?? [], se.emphasis ?? [])}</p>
      <div class="listen"><b>🔊 듣기</b><span>단어를 누르면 뜻이 나와요 · \${shown.trim().split(/\\s+/).length} words</span></div></div>
    \${helps ? \`<div class="helps">\${helps}</div>\` : ""}
    \${renderPanel(s.panel)}
    <div class="stage">
      <div class="over"><div class="card"><span>\${esc(s.message)}</span><i class="tail"></i></div></div>
      <div class="mascot"><img src="\${TEACHER}" alt="다정쌤" width="650" height="616"></div>
    </div>
    <div class="dock"><div class="quick\${stack ? " stack" : ""}">\${pills}</div>
      <form class="input" id="f"><input id="in" placeholder="선생님께 답해 보세요…" autocomplete="off"><button class="send" type="submit" aria-label="보내기">↑</button></form></div>
  </div>\`;
}

phone.addEventListener("click", (e) => {
  const t = e.target.closest("[data-send],[data-tip],[data-star]");
  if (!t) { if (openTip != null) { openTip = null; render(); } return; }
  if (t.dataset.star != null) { e.stopPropagation(); s.saved[t.dataset.star] = !s.saved[t.dataset.star]; render(); return; }
  if (t.dataset.tip != null) { e.stopPropagation(); openTip = openTip === Number(t.dataset.tip) ? null : Number(t.dataset.tip); render(); return; }
  openTip = null;
  if (t.dataset.send === "__restart") { init(); render(); return; }
  submit(t.dataset.send);
});
phone.addEventListener("submit", (e) => { e.preventDefault(); const v = phone.querySelector("#in")?.value ?? ""; openTip = null; submit(v); });
phone.addEventListener("click", () => {}, true);
init(); render();
</script>
`;

const dest = out ?? join(ROOT, "share", `${id}.html`);
writeFileSync(dest, html);
console.log(`${dest} (${Math.round(html.length / 1024)} KB)`);
