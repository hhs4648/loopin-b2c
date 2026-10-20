import { useEffect, useRef, useState } from "react";
import { finishSocialLogin } from "../tutor/auth";
import { supabaseClient } from "../tutor/records";

/**
 * 소셜 로그인에서 돌아오는 자리 (`/auth/callback`).
 *
 * 개발 모드 StrictMode는 마운트를 두 번 한다. 정리 함수로 첫 시도를 죽이면
 * 두 번째는 이미 시작했다고 보고 아무도 세션을 끝내지 않는다. 그래서 취소하지 않는다.
 */

type Props = {
  onDone: () => void;
  onBack: () => void;
};

export function AuthCallback({ onDone, onBack }: Props) {
  const [failed, setFailed] = useState<string | null>(null);
  const started = useRef(false);

  useEffect(() => {
    if (started.current) return;
    started.current = true;

    void (async () => {
      const db = supabaseClient();
      if (!db) {
        setFailed("서버 설정이 없어요.");
        return;
      }

      const hasSession = async () => {
        try {
          const result = await Promise.race([
            db.auth.getSession(),
            new Promise<null>((resolve) => window.setTimeout(() => resolve(null), 800)),
          ]);
          const user = result?.data.session?.user;
          return Boolean(user && !user.is_anonymous);
        } catch {
          return false;
        }
      };

      let ok = await hasSession();
      for (let tries = 0; !ok && tries < 20; tries += 1) {
        await new Promise((resolve) => window.setTimeout(resolve, 150));
        ok = await hasSession();
      }
      if (!ok) {
        setFailed("세션을 만들지 못했어요.");
        return;
      }

      await finishSocialLogin();
      onDone();
    })().catch((error: unknown) => {
      setFailed(error instanceof Error ? error.message : "로그인을 마치지 못했어요.");
    });
  }, [onDone]);

  return (
    <div className="stage-fill login">
      <div className="login-hero">
        <p className="login-kicker">Loopin</p>
        <h1>{failed ? "로그인을 마치지 못했어요" : "로그인 중이에요"}</h1>
        <p className="login-say">{failed ?? "잠시만 기다려 주세요."}</p>
      </div>
      {failed ? (
        <div className="login-dock">
          <button type="button" className="login-btn apple" onClick={onBack}>
            로그인으로 돌아가기
          </button>
        </div>
      ) : null}
    </div>
  );
}
