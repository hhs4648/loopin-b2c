import { useEffect, useState, type FormEvent } from "react";
import { AuthFailure, linkedEmail, sendCode, verifyCode, type OtpKind } from "../tutor/auth";

/**
 * 「기록 지키기」 — 익명 학습자에 이메일을 붙인다.
 *
 * 비밀번호가 없다. 이메일 → 메일로 온 숫자 여섯 자리 → 끝. 그러면 폰을 바꿔도
 * 진행 기록·내 노트·단어장이 같은 이메일로 따라온다 (`src/tutor/auth.ts`).
 * 강제하지 않는다 — 돌아가기만 눌러도 지금처럼 익명으로 돈다.
 */

type Props = {
  onBack: () => void;
  /** 로그인해서 서버 기록과 합쳤다. 로컬이 바뀌었으면 true — 부모가 홈·목록을 다시 그린다 */
  onSynced: (changed: boolean) => void;
};

type Step = { at: "email" } | { at: "code"; email: string; kind: OtpKind } | { at: "done"; email: string };

const EMAIL_SHAPE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/** 다정쌤이 학생에게 하는 말 — 원인마다 한 문장 */
function explain(e: unknown): string {
  const kind = e instanceof AuthFailure ? e.kind : "unknown";
  switch (kind) {
    case "rate_limit":
      return "메일을 너무 자주 보냈어요. 잠시 뒤에 다시 해 봐요.";
    case "bad_code":
      return "코드가 맞지 않아요. 메일을 다시 확인해 주세요.";
    case "expired":
      return "코드 시간이 지났어요. 코드를 다시 받아 주세요.";
    case "invalid_email":
      return "이메일 모양이 맞지 않아요. 다시 확인해 주세요.";
    default:
      return "지금은 연결이 안 되네요. 잠시 뒤에 다시 해 봐요.";
  }
}

export function AccountLink({ onBack, onSynced }: Props) {
  const [step, setStep] = useState<Step>({ at: "email" });
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 이미 붙여 둔 이메일이 있으면 그 상태를 보여 준다
  useEffect(() => {
    let alive = true;
    void linkedEmail().then((e) => alive && e && setStep({ at: "done", email: e }));
    return () => {
      alive = false;
    };
  }, []);

  async function submitEmail(e: FormEvent) {
    e.preventDefault();
    const addr = email.trim().toLowerCase();
    if (!EMAIL_SHAPE.test(addr) || busy) return;
    setBusy(true);
    setError(null);
    try {
      const kind = await sendCode(addr);
      setCode("");
      setStep({ at: "code", email: addr, kind });
    } catch (err) {
      setError(explain(err));
    } finally {
      setBusy(false);
    }
  }

  async function submitCode(e: FormEvent) {
    e.preventDefault();
    if (step.at !== "code" || code.length !== 6 || busy) return;
    setBusy(true);
    setError(null);
    try {
      const changed = await verifyCode(step.email, code, step.kind);
      onSynced(changed);
      setStep({ at: "done", email: step.email });
    } catch (err) {
      setError(explain(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="stage-fill saved account">
      <header className="saved-top">
        <button type="button" className="icon-btn light" title="홈으로" onClick={onBack}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
            <path d="M15 6l-6 6 6 6" />
          </svg>
        </button>
      </header>
      <div className="saved-body-scroll">
        <h1 className="saved-title">기록 지키기</h1>

        {step.at === "email" ? (
          <form className="account-form" onSubmit={submitEmail}>
            <p className="account-say">
              이메일을 붙여 두면 폰을 바꿔도 진행 기록·노트·단어장이 따라와요.
              <br />
              비밀번호는 없어요. 메일로 온 숫자 여섯 자리만 넣으면 돼요.
            </p>
            <input
              type="email"
              inputMode="email"
              autoComplete="email"
              placeholder="이메일"
              value={email}
              autoFocus
              disabled={busy}
              onChange={(e) => setEmail(e.target.value)}
            />
            {error ? <p className="account-error">{error}</p> : null}
            <button type="submit" className="pill" disabled={busy || !EMAIL_SHAPE.test(email.trim())}>
              {busy ? "보내는 중…" : "코드 받기"}
            </button>
            <p className="account-note">다른 기기에서 이미 붙여 둔 이메일이면, 그 기록으로 이어서 해요.</p>
          </form>
        ) : step.at === "code" ? (
          <form className="account-form" onSubmit={submitCode}>
            <p className="account-say">
              <b>{step.email}</b>로 숫자 여섯 자리를 보냈어요.
              <br />
              메일함을 확인해 주세요.
            </p>
            <input
              inputMode="numeric"
              pattern="[0-9]*"
              autoComplete="one-time-code"
              maxLength={6}
              placeholder="000000"
              className="account-code"
              value={code}
              autoFocus
              disabled={busy}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
            />
            {error ? <p className="account-error">{error}</p> : null}
            <button type="submit" className="pill" disabled={busy || code.length !== 6}>
              {busy ? "확인하는 중…" : "확인"}
            </button>
            <button type="button" className="account-link" disabled={busy} onClick={() => setStep({ at: "email" })}>
              이메일 다시 적기
            </button>
          </form>
        ) : (
          <div className="account-form">
            <p className="account-say">
              <b>{step.email}</b>로 이어 두었어요.
              <br />
              이제 어느 기기에서든 이 이메일로 기록을 이어 할 수 있어요.
            </p>
            <button type="button" className="pill" onClick={onBack}>
              홈으로
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
