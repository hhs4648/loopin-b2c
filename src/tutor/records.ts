import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { PointRecord } from "./view";

/**
 * 학습 기록을 서버에 남긴다.
 *
 * **저장이 실패해도 수업은 멈추지 않는다.** 기록은 나중에 난이도를 재기 위한
 * 부산물이지, 학생이 지금 문장을 푸는 데 필요한 게 아니다. 그래서 모든 실패를
 * 삼키고 경고만 남긴다.
 *
 * 환경변수가 없으면 아무것도 하지 않는다 — 지금까지처럼 코드만으로 돈다.
 */

let client: SupabaseClient | null = null;
let learnerId: string | null = null;
let sessionRow: string | null = null;
/*
  **동시에 두 번 불려도 한 번만 한다.**
  React StrictMode는 개발에서 effect를 두 번 돌린다. 가드가 없으면 둘 다
  "세션 없음"을 보고 각자 익명 로그인을 해서 **사용자가 둘 생긴다.** 그러면
  수업 행은 A가 만들고 앱은 B로 로그인된 상태가 되어, 종료 기록이 RLS에 막혀
  조용히 0행을 고친다 (204만 돌아온다). 2026-09-06 실제로 재현했다.
*/
let learnerInFlight: Promise<string | null> | null = null;
let sessionInFlight: Promise<void> | null = null;

function supabase(): SupabaseClient | null {
  const url = import.meta.env.VITE_SUPABASE_URL?.trim();
  const key = import.meta.env.VITE_SUPABASE_ANON_KEY?.trim();
  if (!url || !key) return null;
  if (!client) {
    client = createClient(url, key, {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
        /*
          소셜 로그인에서 돌아올 때 URL의 `?code=`를 세션으로 바꾼다.
          끄면 `/auth/callback`이 세션을 영원히 못 찾는다.
        */
        detectSessionInUrl: true,
        flowType: "pkce",
      },
    });
    /*
      이메일을 붙이거나 다른 기기에서 로그인하면(`auth.ts`) 학습자가 바뀔 수 있다.
      여기서 따라가야 그 뒤의 기록·동기화(`cloud.ts`)가 새 uid로 간다.
    */
    client.auth.onAuthStateChange((_event, session) => {
      if (session?.user && session.user.id !== learnerId) {
        learnerId = session.user.id;
        sessionRow = null; // 수업 행은 예전 학습자 것 — 새 uid로는 못 고친다
      }
    });
  }
  return client;
}

/** 다른 모듈(`cloud.ts`)도 같은 클라이언트·같은 학습자를 쓴다 */
export const supabaseClient = supabase;

/*
  **테스트 브라우저에서는 기록을 남기지 않는다.** 2026-10-21에 보니 사용자 157명 중 136명이
  개발 PC(HeadlessChrome·curl·Claude 앱)와 클라우드 자동 테스트였다 — 진짜 학생 기록이 묻힌다.
  개발 서버(`npm run dev`), 내 컴퓨터 주소(127.0.0.1·localhost), 자동 브라우저(webdriver·HeadlessChrome)면
  익명 학습자를 만들지 않고 수업·동기화·호출 기록을 모두 건너뛴다.
  동기화를 직접 확인해야 할 때만 주소에 `?record=1`을 붙인다 (이 탭에서만 켜진다).
*/
const LOCAL_HOST = /^(localhost|127\.0\.0\.1|\[::1\])$|\.localhost$|\.test$/;
const FORCE_KEY = "loopin.record.force";

function forced(): boolean {
  try {
    if (new URLSearchParams(window.location.search).get("record") === "1") {
      window.sessionStorage.setItem(FORCE_KEY, "1");
    }
    return window.sessionStorage.getItem(FORCE_KEY) === "1";
  } catch {
    return false;
  }
}

export function isTestBrowser(): boolean {
  if (typeof window === "undefined" || typeof navigator === "undefined") return false;
  if (forced()) return false;
  return (
    import.meta.env.DEV ||
    LOCAL_HOST.test(window.location.hostname) ||
    navigator.webdriver === true ||
    /HeadlessChrome/.test(navigator.userAgent)
  );
}

export function recordingEnabled(): boolean {
  return supabase() != null;
}

/** 프록시를 부를 때 필요한 값. 둘 다 공개돼도 되는 값이다 */
export function supabaseConfig(): { url: string; anonKey: string } | null {
  const url = import.meta.env.VITE_SUPABASE_URL?.trim();
  const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY?.trim();
  return url && anonKey ? { url, anonKey } : null;
}

/**
 * 프록시에 보낼 학습자 토큰.
 *
 * 익명 세션이 아직 없으면 여기서 만든다 — 수업 기록과 **같은 사람**이어야
 * 호출 로그가 이어진다.
 */
export async function learnerToken(): Promise<string | null> {
  const db = supabase();
  if (!db) return null;
  await ensureLearner();
  const { data } = await db.auth.getSession();
  return data.session?.access_token ?? null;
}

/**
 * 학습자 신원.
 *
 * **익명으로 시작한다.** 지금 필요한 건 난이도 집계이고 그건 익명으로 충분하다.
 * 계정(이메일)은 `auth.ts`가 `updateUser({ email })`로 **같은 uid에** 붙인다 —
 * 지금까지의 기록이 그대로 따라온다. 새 계정을 만들면 기록이 남의 것이 된다.
 */
export async function ensureLearner(): Promise<string | null> {
  const db = supabase();
  if (!db || isTestBrowser()) return null;
  if (learnerId) return learnerId;
  learnerInFlight ??= (async () => {
    const { data } = await db.auth.getSession();
    if (data.session?.user) return (learnerId = data.session.user.id);
    const { data: signed, error } = await db.auth.signInAnonymously();
    if (error || !signed.user) {
      console.warn("[records] 익명 세션 실패", error?.message);
      learnerInFlight = null; // 다음 기회에 다시 시도한다
      return null;
    }
    return (learnerId = signed.user.id);
  })();
  return learnerInFlight;
}

/** 로그인 직후(`auth.ts`) — 이벤트를 기다리지 않고 바로 새 학습자로 바꾼다 */
export function adoptLearner(id: string): void {
  if (id === learnerId) return;
  learnerId = id;
  learnerInFlight = Promise.resolve(id);
  sessionRow = null;
}

/** 수업 시작. 실패하면 이후 기록도 조용히 건너뛴다 */
export function startSessionRecord(lessonId: string): Promise<void> {
  sessionInFlight ??= (async () => {
    const db = supabase();
    const learner = await ensureLearner();
    if (!db || !learner) return;
    const { data, error } = await db
      .from("sessions")
      .insert({ learner_id: learner, lesson_id: lessonId })
      .select("id")
      .single();
    if (error) {
      console.warn("[records] 수업 시작 기록 실패", error.message);
      return;
    }
    sessionRow = data.id as string;
  })();
  return sessionInFlight;
}

/**
 * 수업 종료. **항목 기록을 한 번에 넣는다** — 문장마다 왕복하면 수업 중에
 * 네트워크를 계속 쓰게 되고, 중간에 끊기면 반쯤 남은 기록이 생긴다.
 */
export async function finishSessionRecord(
  result: string,
  records: PointRecord[],
): Promise<void> {
  // 시작 기록이 아직 날아가는 중일 수 있다
  await sessionInFlight;
  const db = supabase();
  if (!db || !sessionRow || !learnerId || isTestBrowser()) return;

  /*
    `select()`를 붙여 **몇 행이 바뀌었는지 확인한다.** PostgREST는 RLS에 막혀
    0행을 고쳐도 204를 돌려주므로, 안 보면 실패가 성공처럼 보인다.
  */
  const { data: updated, error: sessionError } = await db
    .from("sessions")
    .update({ result, ended_at: new Date().toISOString() })
    .eq("id", sessionRow)
    .select("id");
  if (sessionError) console.warn("[records] 수업 종료 기록 실패", sessionError.message);
  else if (!updated?.length) console.warn("[records] 수업 종료 기록이 0행을 고쳤다");

  if (!records.length) return;
  const { error } = await db.from("point_attempts").insert(
    records.map((r) => ({
      session_id: sessionRow,
      learner_id: learnerId,
      lesson_id: r.lessonId,
      unit: r.unit,
      point: r.point,
      first_try: r.firstTry,
      nudged: r.nudged,
      told: r.told,
      revealed: r.revealed,
    })),
  );
  if (error) console.warn("[records] 항목 기록 실패", error.message);
}

export type LlmCallRecord = {
  call: "judge" | "speak";
  ms: number;
  inputTokens: number;
  cachedTokens: number;
  outputTokens: number;
  droppedReason?: string;
};

/** 모델 호출 한 건. 비용·지연·폐기율을 나중에 보려고 남긴다 */
export async function recordLlmCall(info: LlmCallRecord): Promise<void> {
  const db = supabase();
  if (!db || !learnerId || isTestBrowser()) return;
  const { error } = await db.from("llm_calls").insert({
    session_id: sessionRow,
    learner_id: learnerId,
    call: info.call,
    ms: info.ms,
    input_tokens: info.inputTokens,
    cached_tokens: info.cachedTokens,
    output_tokens: info.outputTokens,
    dropped_reason: info.droppedReason ?? null,
  });
  if (error) console.warn("[records] 호출 기록 실패", error.message);
}
