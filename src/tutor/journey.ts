/**
 * 유입 경로와 입구에서 멈춘 자리.
 *
 * 이름·이메일·해석은 올리지 않는다. 행은 학습자당 하나고, 관리자 화면만 전체를 본다.
 * 개발 서버·자동 브라우저는 남기지 않는다 (`records.ts` 의 isTestBrowser).
 */

import { ensureLearner, isTestBrowser, supabaseClient } from "./records";
import { loadTester } from "./tester";

export const SRC_KEY = "loopin.src";

export const SOURCES = ["insta", "orbi", "kakao", "friend", "play", "direct", "other"] as const;
export type SourceId = (typeof SOURCES)[number];

const SOURCE_LABEL: Record<SourceId, string> = {
  insta: "인스타",
  orbi: "오르비",
  kakao: "카톡",
  friend: "지인",
  play: "플레이",
  direct: "주소 직접",
  other: "그 밖",
};

const QUERY_SRC: Record<string, SourceId> = {
  insta: "insta",
  instagram: "insta",
  ig: "insta",
  orbi: "orbi",
  kakao: "kakao",
  kakaotalk: "kakao",
  friend: "friend",
  share: "friend",
  play: "play",
  playstore: "play",
  direct: "direct",
};

const REFERRER_SRC: [RegExp, SourceId][] = [
  [/instagram\.com|instagr\.am/i, "insta"],
  [/orbi\.kr|orbi\.ai/i, "orbi"],
  [/kakao\.com|kakao\.talk/i, "kakao"],
];

export const ONBOARD_STEPS = ["name", "intro", "group", "grade", "order", "done"] as const;
export type OnboardStep = (typeof ONBOARD_STEPS)[number];

const ONBOARD_LABEL: Record<OnboardStep, string> = {
  name: "이름",
  intro: "소개",
  group: "구분",
  grade: "등급",
  order: "기출 순서",
  done: "같이 볼래요",
};

const TAP_LABEL: Record<string, string> = {
  guest: "로그인 없이",
  kakao: "카카오",
  google: "Google",
  apple: "Apple",
};

const GROUP_LABEL: Record<string, string> = {
  suneung: "고3·N수생",
  high12: "고1·2",
  middle: "중학생",
  adult: "일반인",
};

const GRADE_LABEL: Record<number, string> = {
  1: "1등급",
  3: "2~3등급",
  5: "4~5등급",
  7: "6~7등급",
  9: "8~9등급",
};

export type JourneyPatch = {
  src?: string;
  login_tap?: "guest" | "kakao" | "google" | "apple";
  account?: "guest" | "kakao" | "google" | "apple";
  learner_group?: string;
  grade?: number | null;
  onboard_step?: OnboardStep;
  kind?: "new" | "returning" | "link";
  example_started?: boolean;
  example_place?: string;
  example_index?: number;
  example_total?: number;
  example_done?: boolean;
  tester?: string | null;
};

export type JourneyRow = {
  src: string;
  login_tap: string | null;
  account: string | null;
  learner_group: string | null;
  grade: number | null;
  onboard_step: string | null;
  kind: string | null;
  example_started: boolean;
  example_place: string | null;
  example_index: number;
  example_total: number;
  example_done: boolean;
  visit_days: number;
  tester: string | null;
  first_seen: string;
  last_seen: string;
};

export type FunnelStep = { id: string; label: string; count: number; left: number };

export type CountRow = { id: string; label: string; count: number };

export type JourneySummary = {
  fresh: number;
  returning: number;
  link: number;
  funnel: FunnelStep[];
  sources: CountRow[];
  accounts: CountRow[];
  groups: CountRow[];
  grades: CountRow[];
  stops: CountRow[];
  exampleStops: CountRow[];
};

function knownSource(value: string | null | undefined): SourceId | null {
  const key = value?.trim().toLowerCase() ?? "";
  if (!key) return null;
  return QUERY_SRC[key] ?? (SOURCES.includes(key as SourceId) ? (key as SourceId) : null);
}

/** 주소의 src 가 있으면 그것, 없으면 저장해 둔 값, 없으면 직전 사이트, 없으면 직접 */
export function resolveSource(search: string, referrer: string, stored: string | null): SourceId {
  const params = new URLSearchParams(search.startsWith("?") ? search.slice(1) : search);
  const explicit = knownSource(params.get("src")) ?? knownSource(params.get("utm_source"));
  if (explicit) return explicit;
  if (params.get("src") || params.get("utm_source")) return "other";
  const kept = knownSource(stored);
  if (kept) return kept;
  if (/^android-app:\/\//i.test(referrer)) return "play";
  for (const [pattern, src] of REFERRER_SRC) {
    if (pattern.test(referrer)) return src;
  }
  return "direct";
}

export function sourceLabel(id: string): string {
  return SOURCE_LABEL[id as SourceId] ?? "그 밖";
}

export function onboardLabel(step: string | null): string {
  if (!step) return "";
  return ONBOARD_LABEL[step as OnboardStep] ?? step;
}

export function groupLabel(id: string | null): string {
  if (!id) return "";
  return GROUP_LABEL[id] ?? id;
}

export function gradeLabel(grade: number | null): string {
  if (grade == null) return "";
  return GRADE_LABEL[grade] ?? `${grade}등급`;
}

function onboardRank(step: string | null | undefined): number {
  const i = ONBOARD_STEPS.indexOf(step as OnboardStep);
  return i < 0 ? 0 : i + 1;
}

/** 잠깐 모았다가 한 번에 보낼 때, 앞선 단계가 뒷 단계에 덮이지 않게 */
export function mergePatch(a: JourneyPatch, b: JourneyPatch): JourneyPatch {
  const onboard = onboardRank(b.onboard_step) > onboardRank(a.onboard_step) ? b.onboard_step : a.onboard_step;
  const indexA = a.example_index ?? -1;
  const indexB = b.example_index ?? -1;
  const place = indexB >= indexA ? (b.example_place ?? a.example_place) : a.example_place;
  const account = b.account && b.account !== "guest" ? b.account : (a.account ?? b.account);
  return {
    ...a,
    ...b,
    ...(onboard ? { onboard_step: onboard } : {}),
    ...(account ? { account } : {}),
    ...(a.example_started || b.example_started ? { example_started: true } : {}),
    ...(a.example_done || b.example_done ? { example_done: true } : {}),
    ...(Math.max(indexA, indexB) >= 0 ? { example_index: Math.max(indexA, indexB) } : {}),
    ...(place ? { example_place: place } : {}),
  };
}

type ExampleView = {
  screen: string;
  ended: boolean;
  progressIndex: number;
  progressTotal: number;
  chunkLabel: string;
};

/** 예시 분석 중 지금 화면. 관리자는 마지막 자리만 본다 */
export function examplePatch(view: ExampleView): JourneyPatch {
  if (view.ended) {
    return {
      example_started: true,
      example_done: true,
      example_place: "끝",
      example_index: view.progressTotal + 1,
      example_total: view.progressTotal,
    };
  }
  if (view.screen === "read") {
    return { example_started: true, example_place: "지문 미리보기", example_index: 0, example_total: view.progressTotal };
  }
  const place = view.chunkLabel.trim() || `${view.progressIndex}/${view.progressTotal}`;
  return {
    example_started: true,
    example_place: place,
    example_index: Math.max(1, view.progressIndex),
    example_total: view.progressTotal,
  };
}

function counts(map: Map<string, { label: string; count: number }>): CountRow[] {
  return [...map.entries()]
    .map(([id, row]) => ({ id, label: row.label, count: row.count }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label, "ko"));
}

function add(map: Map<string, { label: string; count: number }>, id: string, label: string) {
  const row = map.get(id) ?? { label, count: 0 };
  row.count += 1;
  map.set(id, row);
}

/** 처음 온 사람(아직 로그인 전 포함)이 어디까지 갔나 */
export function summarize(rows: JourneyRow[]): JourneySummary {
  const fresh = rows.filter((r) => r.kind === "new" || r.kind == null);
  const steps: { id: string; label: string; count: number }[] = [
    { id: "open", label: "앱을 열었다", count: fresh.length },
    { id: "login", label: "로그인 화면을 넘겼다", count: fresh.filter((r) => r.account).length },
    { id: "ask", label: "첫 질문을 시작했다", count: fresh.filter((r) => onboardRank(r.onboard_step) >= 1).length },
    { id: "ready", label: "같이 볼래요까지 왔다", count: fresh.filter((r) => onboardRank(r.onboard_step) >= 6).length },
    { id: "example", label: "예시 분석을 시작했다", count: fresh.filter((r) => r.example_started).length },
    { id: "done", label: "예시 분석을 끝냈다", count: fresh.filter((r) => r.example_done).length },
    { id: "return", label: "분석을 끝내고 다른 날 다시 왔다", count: fresh.filter((r) => r.example_done && r.visit_days >= 2).length },
  ];
  const funnel: FunnelStep[] = steps.map((step, i) => ({
    ...step,
    left: i === 0 ? 0 : Math.max(0, steps[i - 1]!.count - step.count),
  }));

  const sources = new Map<string, { label: string; count: number }>();
  const accounts = new Map<string, { label: string; count: number }>();
  const groups = new Map<string, { label: string; count: number }>();
  const grades = new Map<string, { label: string; count: number }>();
  const stops = new Map<string, { label: string; count: number }>();
  const exampleStops = new Map<string, { label: string; count: number }>();

  for (const row of rows) add(sources, row.src || "direct", sourceLabel(row.src));

  for (const row of fresh) {
    if (row.account) add(accounts, row.account, TAP_LABEL[row.account] ?? row.account);
    else if (row.login_tap) add(accounts, `tap:${row.login_tap}`, `${TAP_LABEL[row.login_tap] ?? row.login_tap}만 누르고 나감`);
    if (row.learner_group) add(groups, row.learner_group, groupLabel(row.learner_group));
    if (row.grade != null) add(grades, String(row.grade), gradeLabel(row.grade));
    else if (onboardRank(row.onboard_step) >= 5 && (row.learner_group === "suneung" || row.learner_group === "high12")) {
      add(grades, "unknown", "모름");
    }
    if (row.example_done) continue;
    if (row.example_started) {
      add(exampleStops, row.example_place || "start", row.example_place || "시작 직후");
      continue;
    }
    const where = whereNow(row);
    add(stops, where, where);
  }

  return {
    fresh: fresh.length,
    returning: rows.filter((r) => r.kind === "returning").length,
    link: rows.filter((r) => r.kind === "link").length,
    funnel,
    sources: counts(sources),
    accounts: counts(accounts),
    groups: counts(groups),
    grades: counts(grades),
    stops: counts(stops),
    exampleStops: counts(exampleStops),
  };
}

export function whereNow(row: JourneyRow): string {
  if (row.kind === "link") return "수업 링크";
  if (row.kind === "returning" && !row.example_started) return "이미 쓰던 사람";
  if (row.example_done) return "예시 분석을 끝냄";
  if (row.example_started) return row.example_place ? `분석 · ${row.example_place}` : "분석 시작";
  if (row.onboard_step === "done") return "같이 볼래요";
  if (row.onboard_step) return `질문 · ${onboardLabel(row.onboard_step)}`;
  if (!row.account && row.login_tap) return `${TAP_LABEL[row.login_tap] ?? row.login_tap}만 누르고 나감`;
  if (!row.account) return "로그인 화면";
  return "들어온 직후";
}

/** 주소에 경로가 있으면 저장하고, 주소창에서는 지운다. 로그인으로 나갔다 와도 남는다 */
export function rememberSource(): SourceId {
  let stored: string | null = null;
  try {
    stored = window.localStorage.getItem(SRC_KEY);
  } catch {
    stored = null;
  }
  const src = resolveSource(window.location.search, document.referrer, stored);
  try {
    window.localStorage.setItem(SRC_KEY, src);
    const params = new URLSearchParams(window.location.search);
    if (params.has("src") || params.has("utm_source") || params.has("utm_medium")) {
      params.delete("src");
      params.delete("utm_source");
      params.delete("utm_medium");
      const query = params.toString();
      window.history.replaceState({}, "", window.location.pathname + (query ? `?${query}` : "") + window.location.hash);
    }
  } catch {
    /* 저장이 안 되면 이번 접속만 그 경로로 올린다 */
  }
  return src;
}

let pending: JourneyPatch = {};
let timer: number | null = null;
let chain: Promise<void> = Promise.resolve();

async function send(patch: JourneyPatch): Promise<void> {
  const db = supabaseClient();
  if (!db) return;
  const learner = await ensureLearner();
  if (!learner) return;
  const tester = loadTester();
  const body: JourneyPatch = { ...patch, src: rememberSource(), ...(tester ? { tester } : {}) };
  const { error } = await db.rpc("touch_journey", { patch: body });
  if (error) console.warn("[journey] 기록 실패", error.message);
}

function enqueue(): Promise<void> {
  const patch = pending;
  pending = {};
  const run = chain.then(() => send(patch));
  chain = run.then(
    () => undefined,
    () => undefined,
  );
  return run;
}

/** 입구 기록. 수업이 멈추면 안 되므로 실패는 삼킨다. immediate 는 화면을 떠나기 직전 */
export function note(patch: JourneyPatch = {}, immediate = false): Promise<void> {
  if (typeof window === "undefined") return Promise.resolve();
  if (isTestBrowser()) return Promise.resolve();
  pending = mergePatch(pending, patch);
  if (timer != null) window.clearTimeout(timer);
  timer = null;
  if (immediate) {
    return Promise.race([enqueue(), new Promise<void>((resolve) => window.setTimeout(resolve, 1500))]);
  }
  return new Promise((resolve) => {
    timer = window.setTimeout(() => {
      timer = null;
      void enqueue().then(resolve, resolve);
    }, 400);
  });
}
