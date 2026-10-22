import { Capacitor } from "@capacitor/core";
import { supabaseClient } from "./records";

/** 아이폰 앱이 소셜 로그인 뒤에 다시 열리는 주소. Supabase Redirect URLs 에도 넣는다. */
export const NATIVE_AUTH_REDIRECT = "loopin://auth/callback";

export function isNativeApp(): boolean {
  try {
    return Capacitor.isNativePlatform();
  } catch {
    return false;
  }
}

/** 시스템 브라우저(사파리 시트)로 로그인 페이지를 연다. 앱 안 웹뷰에서는 구글이 막는다. */
export async function openNativeLogin(url: string): Promise<void> {
  const { Browser } = await import("@capacitor/browser");
  await Browser.open({ url });
}

async function closeNativeLogin(): Promise<void> {
  try {
    const { Browser } = await import("@capacitor/browser");
    await Browser.close();
  } catch {
    /* 이미 닫혀 있다 */
  }
}

/** loopin://auth/callback?code=… 를 세션으로 바꾼다. 그 주소가 아니면 false. */
export async function finishNativeLogin(url: string): Promise<boolean> {
  if (!url.startsWith(NATIVE_AUTH_REDIRECT)) return false;
  const query = url.indexOf("?");
  const params = new URLSearchParams(query >= 0 ? url.slice(query + 1).split("#")[0] : "");
  const code = params.get("code");
  if (!code) return false;
  const db = supabaseClient();
  if (!db) return false;
  const { error } = await db.auth.exchangeCodeForSession(code);
  if (error) return false;
  await closeNativeLogin();
  return true;
}

/** 앱이 딥링크로 다시 열리면 로그인을 마치고 onDone 을 부른다. 브라우저에서는 아무것도 하지 않는다. */
export async function listenNativeLogin(onDone: () => void): Promise<void> {
  if (!isNativeApp()) return;
  const { App } = await import("@capacitor/app");
  const handle = async (url: string) => {
    if (await finishNativeLogin(url)) onDone();
  };
  await App.addListener("appUrlOpen", (event) => {
    void handle(event.url);
  });
  const launch = await App.getLaunchUrl();
  if (launch?.url) void handle(launch.url);
}
