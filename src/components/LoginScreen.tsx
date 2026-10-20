import { useState, type ReactNode } from "react";
import { AuthFailure, startSocialLogin, type SocialProvider } from "../tutor/auth";

/**
 * 로그인 화면. Google · 카카오 · Apple 은 Supabase OAuth 로 나갔다가
 * `/auth/callback` 으로 돌아온다. 「로그인 없이 시작하기」는 익명으로 홈에 들어간다.
 */

type Props = {
  onSkip: () => void;
};

const BUTTONS: { provider: SocialProvider; label: string; className: string; mark: () => ReactNode }[] = [
  { provider: "kakao", label: "카카오로 계속하기", className: "kakao", mark: KakaoMark },
  { provider: "google", label: "Google로 계속하기", className: "google", mark: GoogleMark },
  { provider: "apple", label: "Apple로 계속하기", className: "apple", mark: AppleMark },
];

export function LoginScreen({ onSkip }: Props) {
  const [pending, setPending] = useState<SocialProvider | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function choose(provider: SocialProvider) {
    if (pending) return;
    setError(null);
    setPending(provider);
    try {
      await startSocialLogin(provider);
    } catch (err) {
      setError(err instanceof AuthFailure ? err.message : "로그인을 시작하지 못했어요. 잠시 뒤에 다시 해 봐요.");
      setPending(null);
    }
  }

  return (
    <div className="stage-fill login">
      <div className="login-hero">
        <p className="login-kicker">Loopin</p>
        <h1>안녕하세요</h1>
        <p className="login-say">기록을 남기려면 로그인하면 돼요.</p>
        <div className="login-mascot">
          <div className="teacher-bob">
            <img src="/assets/character/dajung.webp" alt="다정쌤" width={650} height={616} draggable={false} />
          </div>
        </div>
      </div>

      <div className="login-dock">
        {BUTTONS.map((button) => (
          <button
            key={button.provider}
            type="button"
            className={`login-btn ${button.className}`}
            disabled={pending !== null}
            onClick={() => void choose(button.provider)}
          >
            <button.mark />
            {pending === button.provider ? "이동 중이에요…" : button.label}
          </button>
        ))}
        {error ? <p className="login-error">{error}</p> : null}
        <button type="button" className="login-skip" disabled={pending !== null} onClick={onSkip}>
          로그인 없이 시작하기
        </button>
      </div>
    </div>
  );
}

function GoogleMark() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">
      <path fill="#4285F4" d="M17.6 9.2c0-.6-.1-1.2-.2-1.8H9v3.4h4.8a4.1 4.1 0 0 1-1.8 2.7v2.2h2.9c1.7-1.6 2.7-3.9 2.7-6.5z" />
      <path fill="#34A853" d="M9 18c2.4 0 4.5-.8 6-2.2l-2.9-2.2c-.8.6-1.9.9-3.1.9-2.4 0-4.4-1.6-5.1-3.8H.9v2.3A9 9 0 0 0 9 18z" />
      <path fill="#FBBC05" d="M3.9 10.7a5.4 5.4 0 0 1 0-3.4V5H.9a9 9 0 0 0 0 8l3-2.3z" />
      <path fill="#EA4335" d="M9 3.6c1.3 0 2.5.5 3.4 1.3l2.6-2.6A9 9 0 0 0 .9 5l3 2.3C4.6 5.2 6.6 3.6 9 3.6z" />
    </svg>
  );
}

function KakaoMark() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">
      <path fill="#191919" d="M9 2.2c-4 0-7.2 2.5-7.2 5.6 0 2 1.3 3.7 3.3 4.7l-.8 3 3.4-2.2c.4.1.9.1 1.3.1 4 0 7.2-2.5 7.2-5.6S13 2.2 9 2.2z" />
    </svg>
  );
}

function AppleMark() {
  return (
    <svg width="16" height="18" viewBox="0 0 16 18" aria-hidden="true">
      <path fill="currentColor" d="M13.2 9.5c0-2.2 1.8-3.3 1.9-3.4-1-1.5-2.6-1.7-3.2-1.7-1.3-.1-2.6.8-3.3.8s-1.7-.8-2.8-.7c-1.5.1-2.8.9-3.5 2.2-1.5 2.6-.4 6.5 1.1 8.6.7 1 1.6 2.2 2.7 2.1 1.1 0 1.5-.7 2.8-.7s1.6.7 2.8.7 1.9-1.1 2.6-2.1c.8-1.2 1.1-2.3 1.2-2.4-.1 0-2.2-.9-2.3-3.4zM11 3.2c.6-.7 1-1.7.9-2.7-.9 0-1.9.6-2.5 1.3-.6.6-1.1 1.7-.9 2.6 1 .1 1.9-.5 2.5-1.2z" />
    </svg>
  );
}
