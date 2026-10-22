import { useState } from "react";
import { AuthFailure, startSocialLogin, type SocialProvider } from "../tutor/auth";
import { note } from "../tutor/journey";

/**
 * 로그인 화면. 그림은 `public/assets/login-screen.svg`.
 * 버튼 글자는 그림 안에 있고, 누르는 영역만 그 자리에 겹친다.
 * Google · 카카오 · Apple 은 Supabase OAuth 로 나갔다가 `/auth/callback` 으로 돌아온다.
 */

type Props = {
  onSkip: () => void;
  onOpenPrivacy: () => void;
};

const BUTTONS: { provider: SocialProvider; label: string; className: string }[] = [
  { provider: "apple", label: "Apple로 시작하기", className: "apple" },
  { provider: "kakao", label: "카카오로 시작하기", className: "kakao" },
  { provider: "google", label: "Google로 시작하기", className: "google" },
];

export function LoginScreen({ onSkip, onOpenPrivacy }: Props) {
  const [pending, setPending] = useState<SocialProvider | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function choose(provider: SocialProvider) {
    if (pending) return;
    setError(null);
    setPending(provider);
    try {
      await note({ login_tap: provider }, true);
      await startSocialLogin(provider);
      setPending(null);
    } catch (err) {
      setError(err instanceof AuthFailure ? err.message : "로그인을 시작하지 못했어요. 잠시 뒤에 다시 해 봐요.");
      setPending(null);
    }
  }

  return (
    <div className="stage-fill login login-screen">
      <div className="login-frame">
        <h1 className="login-sr">Loopin</h1>
        <p className="login-sr">효율적인 학습 루프로 공부의 흐름을 바꾸다</p>
        <img className="login-art" src="/assets/login-screen.svg" alt="" draggable={false} />
        {BUTTONS.map((button) => (
          <button
            key={button.provider}
            type="button"
            className={`login-hit ${button.className}${pending === button.provider ? " is-pending" : ""}`}
            aria-label={button.label}
            disabled={pending !== null}
            onClick={() => void choose(button.provider)}
          >
            {pending === button.provider ? "이동 중이에요…" : null}
          </button>
        ))}
        {error ? <p className="login-error">{error}</p> : null}
      </div>
      <p className="login-foot">
        <button
          type="button"
          className="login-skip"
          disabled={pending !== null}
          onClick={() => {
            void note({ login_tap: "guest", account: "guest" }, true).finally(onSkip);
          }}
        >
          로그인 없이 시작하기
        </button>
        <span>
          만 14세 이상 ·{" "}
          <button type="button" className="login-privacy" disabled={pending !== null} onClick={onOpenPrivacy}>
            개인정보 처리방침
          </button>
        </span>
      </p>
    </div>
  );
}
