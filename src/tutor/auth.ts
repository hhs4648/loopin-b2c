/**
 * 기록 지키기 — 익명 학습자에 **이메일을 붙인다**.
 *
 * 학습자는 익명 uid로 시작한다(`records.ts`). 브라우저 저장소가 지워지거나 기기를
 * 바꾸면 익명 사용자가 새로 생겨 기록이 끊기므로, 이메일을 붙여 두면 어느 기기에서든
 * 같은 uid로 들어온다. 비밀번호는 없다 — 메일로 온 **숫자 여섯 자리**(OTP)로만 확인한다.
 *
 * 두 갈래다:
 * - 이 기기에 익명 세션이 있고 그 이메일이 처음이면 `updateUser({ email })` —
 *   **새 계정을 만들지 않고** 지금 uid에 이메일을 붙여 기록이 그대로 따라온다.
 *   확인은 `verifyOtp({ type: "email_change" })`.
 * - 그 이메일이 이미 다른 uid에 붙어 있으면(다른 기기에서 먼저 붙였다) `signInWithOtp` —
 *   그 uid로 들어온다. 이 기기에 있던 익명 기록은 `cloud.ts`가 합집합으로 올려 준다.
 *
 * 강제하지 않는다 — 안 해도 지금처럼 익명으로 돈다. 대시보드 설정은 `.env.example` 참고.
 */

import { note } from "./journey";
import { isNativeApp, openNativeLogin } from "./nativeAuth";
import { adoptLearner, ensureLearner, supabaseClient, supabaseConfig } from "./records";
import { dropPending, flushNow, pullAll, resetPull } from "./cloud";

export type OtpKind = "email_change" | "email";

export type AuthError = "rate_limit" | "bad_code" | "expired" | "invalid_email" | "unknown";

export class AuthFailure extends Error {
  constructor(
    readonly kind: AuthError,
    detail: string,
  ) {
    super(detail);
  }
}

/** 지금 붙어 있는 이메일. 없으면 null (익명이거나 서버 없음) */
export async function linkedEmail(): Promise<string | null> {
  const db = supabaseClient();
  if (!db) return null;
  const { data } = await db.auth.getSession();
  const user = data.session?.user;
  if (!user || user.is_anonymous) return null;
  return user.email ?? null;
}

/** 익명이 아닌 계정으로 들어와 있나. 카카오는 이메일이 없을 수 있어서 이메일만 보면 안 된다 */
export async function hasAccount(): Promise<boolean> {
  const db = supabaseClient();
  if (!db) return false;
  const { data } = await db.auth.getSession();
  const user = data.session?.user;
  return Boolean(user && !user.is_anonymous);
}

export type SocialProvider = "google" | "kakao" | "apple";

const SOCIAL_LABEL: Record<SocialProvider, string> = {
  google: "Google",
  kakao: "카카오",
  apple: "Apple",
};

/** 계정 화면에 보일 이름 — 이메일, 없으면 「카카오 계정」처럼. 익명이면 null */
export async function accountLabel(): Promise<string | null> {
  const db = supabaseClient();
  if (!db) return null;
  const { data } = await db.auth.getSession();
  const user = data.session?.user;
  if (!user || user.is_anonymous) return null;
  if (user.email) return user.email;
  const provider = user.app_metadata?.provider as string | undefined;
  return provider && provider in SOCIAL_LABEL ? `${SOCIAL_LABEL[provider as SocialProvider]} 계정` : "내 계정";
}

/** 소셜 로그인을 마치고 돌아올 주소. Supabase 대시보드 Redirect URLs 에도 같은 주소를 넣는다 */
export function socialRedirectUrl(): string {
  // 아이폰 앱의 주소는 capacitor://localhost 라 허용 목록에 없다. 앱은 loopin:// 로 돌아온다.
  if (isNativeApp()) return "loopin://auth/callback";
  return `${window.location.origin}/auth/callback`;
}

const AFTER_LOGIN = "loopin.afterLogin";

/** 로그인 뒤에 관리자 화면으로 돌아올 때. 허용한 주소만 기억한다 */
export function rememberAfterLogin(path: "/admin"): void {
  try {
    window.sessionStorage.setItem(AFTER_LOGIN, path);
  } catch {
    /* 기억 못 하면 로그인 뒤 홈으로 간다 */
  }
}

export function takeAfterLogin(): "/admin" | null {
  try {
    const value = window.sessionStorage.getItem(AFTER_LOGIN);
    window.sessionStorage.removeItem(AFTER_LOGIN);
    return value === "/admin" ? "/admin" : null;
  } catch {
    return null;
  }
}

/** 붙어 있는 소셜 계정. 익명이면 null */
export async function accountProvider(): Promise<SocialProvider | "guest" | null> {
  const db = supabaseClient();
  if (!db) return null;
  const { data } = await db.auth.getSession();
  const user = data.session?.user;
  if (!user || user.is_anonymous) return null;
  const provider = user.app_metadata?.provider;
  if (provider === "google" || provider === "kakao" || provider === "apple") return provider;
  return "guest";
}

/*
  `signInWithOAuth()`는 provider가 대시보드에 꺼져 있어도 에러를 주지 않고
  authorize URL로 보내 버린다. 그러면 학생은 날것의 JSON만 보고 돌아올 버튼이 없다.
  켜진 provider만 시도한다. 확인 자체가 실패하면 그냥 진행한다.
*/
let enabledProviders: Set<string> | null = null;

async function isSocialProviderEnabled(provider: SocialProvider): Promise<boolean | null> {
  if (enabledProviders) return enabledProviders.has(provider);
  const env = supabaseConfig();
  if (!env) return null;
  try {
    const res = await fetch(`${env.url}/auth/v1/settings`, { headers: { apikey: env.anonKey } });
    if (!res.ok) return null;
    const json = (await res.json()) as { external?: Record<string, boolean> };
    if (!json.external) return null;
    enabledProviders = new Set(
      Object.entries(json.external)
        .filter(([, on]) => on === true)
        .map(([name]) => name),
    );
    return enabledProviders.has(provider);
  } catch {
    return null;
  }
}

/**
 * OAuth를 시작한다. 성공하면 브라우저가 그 사이트로 떠나므로 이 함수 뒤는 실행되지 않는다.
 */
export async function startSocialLogin(provider: SocialProvider): Promise<void> {
  const db = supabaseClient();
  if (!db) throw new AuthFailure("unknown", "서버 설정이 없다");
  if ((await isSocialProviderEnabled(provider)) === false) {
    throw new AuthFailure("unknown", `${SOCIAL_LABEL[provider]} 로그인이 아직 준비되지 않았어요.`);
  }
  const redirectTo = socialRedirectUrl();
  const { data, error } = await db.auth.signInWithOAuth({
    provider,
    options: { redirectTo, skipBrowserRedirect: isNativeApp() },
  });
  if (error) throw new AuthFailure(classify(error.message, error.status), error.message);
  if (isNativeApp()) {
    if (!data.url) throw new AuthFailure("unknown", "로그인 주소를 받지 못했어요.");
    await openNativeLogin(data.url);
  }
}

/**
 * `/auth/callback`에서 세션이 생긴 뒤. 그 학습자로 바꾸고 서버 기록을 로컬과 합친다.
 * 로컬이 바뀌었으면 true.
 */
export async function finishSocialLogin(): Promise<boolean> {
  const db = supabaseClient();
  if (!db) throw new AuthFailure("unknown", "서버 설정이 없다");
  const { data } = await db.auth.getSession();
  const user = data.session?.user;
  if (!user || user.is_anonymous) throw new AuthFailure("unknown", "세션을 만들지 못했어요.");
  adoptLearner(user.id);
  resetPull();
  const provider = user.app_metadata?.provider;
  if (provider === "google" || provider === "kakao" || provider === "apple") void note({ account: provider });
  return pullAll();
}

function classify(message: string, status?: number): AuthError {
  const m = message.toLowerCase();
  if (status === 429 || m.includes("rate limit") || m.includes("security purposes")) return "rate_limit";
  if (m.includes("expired")) return "expired";
  if (m.includes("invalid") && (m.includes("otp") || m.includes("token") || m.includes("code"))) return "bad_code";
  if (m.includes("invalid") && m.includes("email")) return "invalid_email";
  return "unknown";
}

function alreadyRegistered(code: string | undefined, message: string): boolean {
  return code === "email_exists" || /already (been )?registered|already exists/i.test(message);
}

/**
 * 코드를 보낸다. 돌려주는 값은 확인할 때 어떤 종류로 확인하는지(`verifyCode`에 그대로 준다).
 */
export async function sendCode(email: string): Promise<OtpKind> {
  const db = supabaseClient();
  if (!db) throw new AuthFailure("unknown", "서버 설정이 없다");
  const learner = await ensureLearner();
  const { data } = await db.auth.getSession();
  const user = data.session?.user;

  if (learner && user?.is_anonymous) {
    // 지금 uid에 이메일을 붙인다 — 기록이 그대로 따라온다
    const { error } = await db.auth.updateUser({ email });
    if (!error) return "email_change";
    if (!alreadyRegistered(error.code, error.message)) throw new AuthFailure(classify(error.message, error.status), error.message);
    // 이미 다른 기기에서 붙인 이메일 → 그 계정으로 들어간다
  }

  const { error } = await db.auth.signInWithOtp({ email, options: { shouldCreateUser: !user } });
  if (error) throw new AuthFailure(classify(error.message, error.status), error.message);
  return "email";
}

/*
  **이 기기의 학습 기록을 지운다.** 남겨 두면 다음 사람이 「로그인 없이 시작하기」로 들어왔을 때
  `pullAll()`이 그 기록을 새 익명 uid에 합쳐 올린다 — 남의 노트·단어장이 따라간다.
*/
const LOCAL_PREFIXES = ["dajung.", "loopin."];
/** 「로그인 없이 시작하기」. 로그아웃·탈퇴의 clearLocalLearner가 loopin. 접두사로 같이 지운다 */
const ENTERED_KEY = "loopin.entered";

/** 한 번 들어와 봤다. 새로고침이나 교무실을 다녀와도 로그인 화면으로 돌아가지 않는다 */
export function hasEntered(): boolean {
  try {
    return window.localStorage.getItem(ENTERED_KEY) === "1";
  } catch {
    return false;
  }
}

export function markEntered(): void {
  try {
    window.localStorage.setItem(ENTERED_KEY, "1");
  } catch {
    /* 저장이 안 되면 이번 화면만 지나간다 */
  }
}

function clearLocalLearner(): void {
  try {
    const keys: string[] = [];
    for (let i = 0; i < window.localStorage.length; i++) {
      const key = window.localStorage.key(i);
      if (key && LOCAL_PREFIXES.some((p) => key.startsWith(p))) keys.push(key);
    }
    for (const key of keys) window.localStorage.removeItem(key);
  } catch {
    /* 저장소를 못 읽으면 지울 것도 없다 */
  }
}

/**
 * 로그아웃. 기록은 서버에 남아 다시 로그인하면 돌아온다.
 * 끝나면 페이지를 새로 연다 — 메모리에 남은 학습자·동기화 상태를 한 번에 버린다.
 */
export async function signOut(): Promise<void> {
  const db = supabaseClient();
  if (db) {
    await flushNow();
    const { error } = await db.auth.signOut();
    if (error) throw new AuthFailure("unknown", error.message);
  }
  clearLocalLearner();
  window.location.replace("/");
}

/**
 * 회원 탈퇴. 서버의 계정과 모든 학습 기록을 지운다 (`003_delete_account.sql`). 되돌릴 수 없다.
 */
export async function deleteAccount(): Promise<void> {
  const db = supabaseClient();
  if (!db) throw new AuthFailure("unknown", "서버 설정이 없다");
  dropPending();
  const { error } = await db.rpc("delete_my_account");
  if (error) throw new AuthFailure(classify(error.message), error.message);
  // 서버의 사용자는 이미 없다 — 이 기기의 세션만 버린다
  await db.auth.signOut({ scope: "local" });
  clearLocalLearner();
  window.location.replace("/");
}

/**
 * 메일로 온 숫자 여섯 자리를 확인한다. 성공하면 서버 기록을 다시 받아 로컬과 합치고,
 * 로컬이 바뀌었으면 true (화면을 다시 그릴 것).
 */
export async function verifyCode(email: string, token: string, kind: OtpKind): Promise<boolean> {
  const db = supabaseClient();
  if (!db) throw new AuthFailure("unknown", "서버 설정이 없다");
  const { data, error } = await db.auth.verifyOtp({ email, token: token.trim(), type: kind });
  if (error) throw new AuthFailure(classify(error.message, error.status), error.message);
  if (!data.session?.user) throw new AuthFailure("unknown", "세션이 없다");
  // 같은 uid면 그대로, 다른 uid(다른 기기에서 먼저 붙인 계정)면 그 기록을 받아 합친다
  adoptLearner(data.session.user.id);
  resetPull();
  return pullAll();
}
