import { useEffect, useState, type FormEvent } from "react";
import {
  gradeLabel,
  groupLabel,
  sourceLabel,
  summarize,
  whereNow,
  type JourneyRow,
  type JourneySummary,
} from "../tutor/journey";
import { supabaseClient } from "../tutor/records";

/**
 * 운영 콘솔. `/admin`.
 * 비밀번호는 서버(`admin_journeys`)가 확인한다. 맞는 값을 이 브라우저 탭에만 기억한다.
 */

type Props = {
  onClose: () => void;
};

type Phase = "lock" | "loading" | "ready" | "error" | "no-server";
type Page = "home" | "door" | "src" | "people";

const PASS_KEY = "loopin.admin.pass";

const PAGES: { id: Page; label: string }[] = [
  { id: "home", label: "한눈에" },
  { id: "door", label: "입구" },
  { id: "src", label: "경로" },
  { id: "people", label: "사람" },
];

const LINKS: { src: string; label: string }[] = [
  { src: "insta", label: "인스타" },
  { src: "orbi", label: "오르비" },
  { src: "kakao", label: "카톡" },
  { src: "friend", label: "지인" },
];

const PAGE_COPY: Record<Page, { title: string; sub: string }> = {
  home: { title: "한눈에", sub: "들어온 사람, 경로, 멈춘 자리를 한 화면에서 봅니다." },
  door: { title: "입구", sub: "앱을 연 사람 가운데 어디까지 갔는지입니다." },
  src: { title: "경로", sub: "어느 링크로 들어왔는지입니다." },
  people: { title: "사람", sub: "최근 접속 순입니다. 이름과 이메일은 없습니다." },
};

function when(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "";
  return new Intl.DateTimeFormat("ko-KR", {
    timeZone: "Asia/Seoul",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  }).format(date);
}

function asRow(raw: Record<string, unknown>): JourneyRow {
  return {
    src: String(raw.src ?? "direct"),
    login_tap: raw.login_tap == null ? null : String(raw.login_tap),
    account: raw.account == null ? null : String(raw.account),
    learner_group: raw.learner_group == null ? null : String(raw.learner_group),
    grade: raw.grade == null ? null : Number(raw.grade),
    onboard_step: raw.onboard_step == null ? null : String(raw.onboard_step),
    kind: raw.kind == null ? null : String(raw.kind),
    example_started: Boolean(raw.example_started),
    example_place: raw.example_place == null ? null : String(raw.example_place),
    example_index: Number(raw.example_index ?? 0),
    example_total: Number(raw.example_total ?? 0),
    example_done: Boolean(raw.example_done),
    visit_days: Number(raw.visit_days ?? 1),
    tester: raw.tester == null ? null : String(raw.tester),
    first_seen: String(raw.first_seen ?? ""),
    last_seen: String(raw.last_seen ?? ""),
  };
}

function accountName(row: JourneyRow): string {
  if (row.account === "kakao") return "카카오";
  if (row.account === "google") return "구글";
  if (row.account === "apple") return "Apple";
  if (row.account === "guest") return "손님";
  return "";
}

function stepCount(summary: JourneySummary, id: string): number {
  return summary.funnel.find((step) => step.id === id)?.count ?? 0;
}

async function fetchRows(pass: string): Promise<{ rows: JourneyRow[] } | { error: "bad" | "fail" | "no-server"; message?: string }> {
  const db = supabaseClient();
  if (!db) return { error: "no-server" };
  const { data, error } = await db.rpc("admin_journeys", { p_pass: pass });
  if (error) {
    if (error.code === "42501" || /not admin/i.test(error.message)) return { error: "bad" };
    return { error: "fail", message: error.message };
  }
  const list = Array.isArray(data) ? data : [];
  return { rows: list.map((item) => asRow(item as Record<string, unknown>)) };
}

export function AdminBoard({ onClose }: Props) {
  const [phase, setPhase] = useState<Phase>("loading");
  const [message, setMessage] = useState("");
  const [pass, setPass] = useState("");
  const [pending, setPending] = useState(false);
  const [rows, setRows] = useState<JourneyRow[]>([]);
  const [hideTesters, setHideTesters] = useState(true);
  const [page, setPage] = useState<Page>("home");

  useEffect(() => {
    let saved = "";
    try {
      saved = window.sessionStorage.getItem(PASS_KEY) ?? "";
    } catch {
      saved = "";
    }
    if (!saved) {
      setPhase("lock");
      return;
    }
    let gone = false;
    void fetchRows(saved).then((result) => {
      if (gone) return;
      if ("rows" in result) {
        setRows(result.rows);
        setPhase("ready");
        return;
      }
      try {
        window.sessionStorage.removeItem(PASS_KEY);
      } catch {
        /* 탭을 닫으면 같이 사라진다 */
      }
      setPhase(result.error === "no-server" ? "no-server" : "lock");
      if (result.error === "fail") setMessage(result.message ?? "기록을 불러오지 못했어요.");
    });
    return () => {
      gone = true;
    };
  }, []);

  async function enter(event: FormEvent) {
    event.preventDefault();
    if (pending) return;
    setPending(true);
    setMessage("");
    const result = await fetchRows(pass);
    setPending(false);
    if ("rows" in result) {
      try {
        window.sessionStorage.setItem(PASS_KEY, pass);
      } catch {
        /* 기억 못 해도 이번 화면은 연다 */
      }
      setRows(result.rows);
      setPass("");
      setPhase("ready");
      return;
    }
    if (result.error === "no-server") setPhase("no-server");
    else if (result.error === "bad") setMessage("비밀번호가 맞지 않아요.");
    else setMessage(result.message ?? "기록을 불러오지 못했어요.");
  }

  function leave() {
    try {
      window.sessionStorage.removeItem(PASS_KEY);
    } catch {
      /* 없어도 잠근다 */
    }
    setRows([]);
    setPhase("lock");
    setPage("home");
  }

  if (phase !== "ready") {
    return (
      <div className="ops ops-lock">
        <form className="ops-login" onSubmit={(event) => void enter(event)}>
          <p className="ops-brand">
            LOOPIN
            <small>운영 콘솔</small>
          </p>
          <h1>비밀번호</h1>
          {phase === "no-server" ? <p className="ops-muted">서버 설정이 없어 열 수 없어요.</p> : null}
          {phase === "loading" ? <p className="ops-muted">불러오는 중이에요.</p> : null}
          {phase === "lock" || phase === "error" ? (
            <>
              <input
                type="password"
                autoFocus
                autoComplete="current-password"
                value={pass}
                onChange={(event) => setPass(event.target.value)}
              />
              <button type="submit" disabled={pending || pass.length === 0}>
                {pending ? "확인 중" : "들어가기"}
              </button>
            </>
          ) : null}
          {message ? <p className="ops-warn">{message}</p> : null}
        </form>
      </div>
    );
  }

  const shown = hideTesters ? rows.filter((row) => !row.tester) : rows;
  const hidden = rows.length - shown.length;
  const summary = summarize(shown);
  const week = Date.now() - 7 * 24 * 60 * 60 * 1000;
  const recentWeek = shown.filter((row) => Date.parse(row.last_seen) >= week).length;
  const copy = PAGE_COPY[page];
  const stops = [
    ...summary.stops.map((row) => ({ id: `s:${row.id}`, label: row.label, count: row.count })),
    ...summary.exampleStops.map((row) => ({ id: `e:${row.id}`, label: `분석 · ${row.label}`, count: row.count })),
  ];

  return (
    <div className="ops">
      <aside className="ops-side">
        <p className="ops-brand">
          LOOPIN
          <small>운영 콘솔</small>
        </p>
        <nav className="ops-nav">
          {PAGES.map((item) => (
            <button key={item.id} type="button" aria-current={page === item.id ? "page" : undefined} onClick={() => setPage(item.id)}>
              {item.label}
            </button>
          ))}
        </nav>
        <div className="ops-side-foot">
          <label>
            <input type="checkbox" checked={hideTesters} onChange={(event) => setHideTesters(event.target.checked)} />
            만드는 사람 빼기{hidden ? ` ${hidden}` : ""}
          </label>
          <button type="button" onClick={leave}>
            나가기
          </button>
          <button type="button" onClick={onClose}>
            앱으로
          </button>
        </div>
      </aside>

      <main className="ops-main">
        <header className="ops-head">
          <h1>{copy.title}</h1>
          <p>{copy.sub}</p>
        </header>

        {page === "home" ? (
          <>
            <section className="ops-stats">
              <Stat label="들어온 사람" value={summary.fresh} />
              <Stat label="로그인 넘김" value={stepCount(summary, "login")} />
              <Stat label="예시 시작" value={stepCount(summary, "example")} />
              <Stat label="예시 끝" value={stepCount(summary, "done")} />
              <Stat label="다시 방문" value={stepCount(summary, "return")} note="분석을 끝내고 다른 날" />
              <Stat label="최근 7일" value={recentWeek} note="마지막 접속 기준" />
            </section>
            <section className="ops-split">
              <div>
                <h2>최근 사람</h2>
                <PeopleTable rows={shown.slice(0, 8)} />
              </div>
              <div>
                <h2>멈춘 곳</h2>
                {stops.length === 0 ? (
                  <p className="ops-empty">아직 기록이 없습니다.</p>
                ) : (
                  <ul className="ops-list">
                    {stops.map((row) => (
                      <li key={row.id}>
                        <span>{row.label}</span>
                        <b>{row.count}</b>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </section>
          </>
        ) : null}

        {page === "door" ? (
          <section className="ops-panel">
            {summary.fresh === 0 ? (
              <p className="ops-empty">아직 처음 온 사람 기록이 없습니다.</p>
            ) : (
              <ol className="ops-funnel">
                {summary.funnel.map((step) => {
                  const width = summary.fresh ? Math.max(4, Math.round((step.count / summary.fresh) * 100)) : 0;
                  return (
                    <li key={step.id}>
                      <div>
                        <span>{step.label}</span>
                        <b>
                          {step.count}
                          {step.left > 0 ? <small> · {step.left}명 나감</small> : null}
                        </b>
                      </div>
                      <i style={{ width: `${step.count === 0 ? 0 : width}%` }} />
                    </li>
                  );
                })}
              </ol>
            )}
            <p className="ops-note">
              이미 쓰던 사람 {summary.returning}명, 수업 링크로 바로 연 사람 {summary.link}명은 이 숫자에 넣지 않습니다.
            </p>
          </section>
        ) : null}

        {page === "src" ? (
          <div className="ops-split">
            <div>
              <h2>들어온 경로</h2>
              <CountList rows={summary.sources} empty="아직 기록이 없습니다." />
              <h2 className="ops-next">들어온 방법</h2>
              <CountList rows={summary.accounts} empty="로그인 화면을 넘긴 사람이 없습니다." />
            </div>
            <div>
              <h2>링크</h2>
              <ul className="ops-list">
                {LINKS.map((link) => (
                  <li key={link.src}>
                    <span>{link.label}</span>
                    <code>{`${window.location.origin}/?src=${link.src}`}</code>
                  </li>
                ))}
              </ul>
              <p className="ops-note">플레이로 설치한 사람은 플레이로 잡힙니다. 인스타에 플레이 링크를 걸면 인스타로 안 잡힙니다.</p>
            </div>
          </div>
        ) : null}

        {page === "people" ? (
          <section className="ops-panel">
            <div className="ops-split ops-split-tight">
              <div>
                <h2>누구인지</h2>
                <CountList rows={summary.groups} empty="구분을 고른 사람이 없습니다." />
              </div>
              <div>
                <h2>등급</h2>
                <CountList rows={summary.grades} empty="등급을 고른 사람이 없습니다." />
              </div>
            </div>
            <h2 className="ops-next">전체</h2>
            <PeopleTable rows={shown.slice(0, 100)} wide />
            {shown.length > 100 ? <p className="ops-note">최근 100명만 표에 나열했습니다. 위 숫자는 전체입니다.</p> : null}
          </section>
        ) : null}
      </main>
    </div>
  );
}

function Stat({ label, value, note }: { label: string; value: number; note?: string }) {
  return (
    <article className="ops-stat">
      <span>{label}</span>
      <strong>{value}</strong>
      {note ? <small>{note}</small> : null}
    </article>
  );
}

function CountList({ rows, empty }: { rows: { id: string; label: string; count: number }[]; empty: string }) {
  if (!rows.length) return <p className="ops-empty">{empty}</p>;
  const total = rows.reduce((sum, row) => sum + row.count, 0);
  return (
    <ul className="ops-list">
      {rows.map((row) => (
        <li key={row.id}>
          <span>{row.label}</span>
          <b>
            {row.count}
            {total ? <small> · {Math.round((row.count / total) * 100)}%</small> : null}
          </b>
        </li>
      ))}
    </ul>
  );
}

function PeopleTable({ rows, wide = false }: { rows: JourneyRow[]; wide?: boolean }) {
  if (!rows.length) return <p className="ops-empty">최근 기록이 없습니다.</p>;
  return (
    <div className="ops-table-wrap">
      <table className="ops-table">
        <thead>
          <tr>
            <th>경로</th>
            <th>계정</th>
            {wide ? <th>구분</th> : null}
            <th>지금</th>
            <th>최근</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.last_seen}-${index}`}>
              <td>{sourceLabel(row.src)}</td>
              <td>{accountName(row)}</td>
              {wide ? <td>{groupLabel(row.learner_group)}{row.grade != null ? ` · ${gradeLabel(row.grade)}` : ""}</td> : null}
              <td>{whereNow(row)}</td>
              <td className="ops-when">{when(row.last_seen)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
