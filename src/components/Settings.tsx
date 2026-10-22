import { useEffect, useState, type ReactNode } from "react";
import { AuthFailure, accountLabel, deleteAccount, signOut } from "../tutor/auth";
import { supabaseConfig } from "../tutor/records";

/**
 * 설정 — 계정, 로그아웃, 회원 탈퇴.
 *
 * 로그아웃은 서버 기록을 남기고 이 기기만 비운다. 탈퇴는 계정과 기록을 지우고
 * 되돌릴 수 없어서, 한 번 더 묻는 화면을 거친다 (`src/tutor/auth.ts`).
 */

type Props = {
  onBack: () => void;
  /** 이메일을 붙이는 「기록 지키기」 */
  onOpenAccount: () => void;
  onOpenPrivacy: () => void;
};

function explain(e: unknown): string {
  const kind = e instanceof AuthFailure ? e.kind : "unknown";
  if (kind === "rate_limit") return "잠시 뒤에 다시 해 봐요.";
  return "지금은 연결이 안 되네요. 잠시 뒤에 다시 해 봐요.";
}

export function Settings({ onBack, onOpenAccount, onOpenPrivacy }: Props) {
  /** undefined = 아직 확인 중 */
  const [label, setLabel] = useState<string | null | undefined>(undefined);
  const [leaving, setLeaving] = useState(false);
  const [busy, setBusy] = useState<"out" | "leave" | null>(null);
  const [error, setError] = useState<string | null>(null);
  const canLink = supabaseConfig() != null;

  useEffect(() => {
    let alive = true;
    void accountLabel().then((name) => {
      if (alive) setLabel(name);
    });
    return () => {
      alive = false;
    };
  }, []);

  async function logOut() {
    if (busy || !label) return;
    setBusy("out");
    setError(null);
    try {
      await signOut();
    } catch (err) {
      setError(explain(err));
      setBusy(null);
    }
  }

  async function leave() {
    if (busy || !label) return;
    setBusy("leave");
    setError(null);
    try {
      await deleteAccount();
    } catch (err) {
      setError(explain(err));
      setBusy(null);
    }
  }

  function back() {
    if (busy) return;
    if (leaving) {
      setLeaving(false);
      setError(null);
      return;
    }
    onBack();
  }

  return (
    <div className="stage-fill saved settings">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="뒤로" onClick={back} disabled={busy !== null}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M15 6l-6 6 6 6" />
          </svg>
        </button>
      </header>
      <div className="saved-body-scroll">
        <h1 className="saved-title">{leaving ? "회원 탈퇴" : "설정"}</h1>

        {leaving ? (
          <div className="settings-leave">
            <p className="account-say">
              탈퇴하면 이 계정이 사라지고, 진행 기록·노트·단어장이 모두 지워져요.
              <br />
              지운 기록은 되돌릴 수 없어요.
            </p>
            {error ? <p className="account-error">{error}</p> : null}
            <button type="button" className="pill" disabled={busy !== null} onClick={() => setLeaving(false)}>
              그만둘게요
            </button>
            <button type="button" className="pill danger" disabled={busy !== null} onClick={() => void leave()}>
              {busy === "leave" ? "지우는 중…" : "탈퇴하기"}
            </button>
          </div>
        ) : (
          <>
            <p className="settings-kicker">계정</p>
            <section className="settings-card">
              {label === undefined ? (
                <p>계정을 확인하고 있어요.</p>
              ) : label ? (
                <>
                  <b>{label}</b>
                  <p>이 계정으로 기록이 따라와요. 다른 기기에서도 이어서 할 수 있어요.</p>
                </>
              ) : (
                <>
                  <b className="quiet">기록은 이 기기에 있어요</b>
                  <p>이메일을 붙여 두면 폰을 바꿔도 노트와 단어장이 따라와요.</p>
                </>
              )}
            </section>

            {label ? (
              <div className="settings-list">
                <button type="button" className="settings-row" disabled={busy !== null} onClick={() => void logOut()}>
                  <span className="settings-ico" aria-hidden="true">
                    <LogoutIcon />
                  </span>
                  <span className="settings-copy">
                    <span className="settings-name">{busy === "out" ? "로그아웃하는 중…" : "로그아웃"}</span>
                    <small>이 기기의 기록은 지워지고, 다시 로그인하면 돌아와요.</small>
                  </span>
                </button>
                <button
                  type="button"
                  className="settings-row danger"
                  disabled={busy !== null}
                  onClick={() => {
                    setError(null);
                    setLeaving(true);
                  }}
                >
                  <span className="settings-ico" aria-hidden="true">
                    <LeaveIcon />
                  </span>
                  <span className="settings-copy">
                    <span className="settings-name">회원 탈퇴</span>
                    <small>계정과 기록을 모두 지워요. 되돌릴 수 없어요.</small>
                  </span>
                </button>
                {error ? <p className="account-error">{error}</p> : null}
              </div>
            ) : label === null ? (
              <div className="settings-list">
                {canLink ? (
                  <button type="button" className="pill" onClick={onOpenAccount}>
                    기록 지키기
                  </button>
                ) : (
                  <p className="account-note">계정 서버가 연결되면 여기서 로그인할 수 있어요.</p>
                )}
                <p className="account-note">로그아웃과 회원 탈퇴는 로그인한 뒤에 여기 나와요.</p>
              </div>
            ) : null}
            <button type="button" className="account-link" onClick={onOpenPrivacy}>
              개인정보 처리방침
            </button>
          </>
        )}
      </div>
    </div>
  );
}

function LogoutIcon(): ReactNode {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 6H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h3" />
      <path d="M15 16l4-4-4-4" />
      <path d="M19 12H10" />
    </svg>
  );
}

function LeaveIcon(): ReactNode {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 7h14" />
      <path d="M9 7V5h6v2" />
      <path d="M8 7l1 12h6l1-12" />
    </svg>
  );
}
