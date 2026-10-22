import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { currentTeacher } from "../tutor/teacher";

/**
 * 온보딩(가입 직후 첫 분석) 길잡이 — 처음 해 보는 학생은 「단어를 누르면 뜻이 나온다」 같은 작은 기능을
 * 알아채기 어려웠다 (2026-10-21 선생님, 사용자 테스트). 화면에 그 기능이 처음 보일 때 하나씩 짚어 준다.
 *
 * - 한 번에 하나만. 기능이 화면에 보일 때(다른 것에 가려지지 않았을 때) 순서대로
 * - 그 기능을 직접 누르거나 [알겠어요]를 누르면 끝 — 다시 안 나온다 (기기에 기억)
 * - 칠판 손잡이 안내는 칠판 서랍(`BoardDrawer`)이 따로 한다. 그게 떠 있는 동안은 쉰다
 */

type Coach = {
  id: string;
  text: string;
  /** 짚을 것 — 화면에 보이는 첫 번째 */
  find: (root: HTMLElement) => HTMLElement[];
  /** 이것을 짚은 뒤에만 — 첫 화면부터 여러 개가 줄줄이 뜨지 않게, 문장 화면 기본(단어 누르기)부터 */
  after?: string;
  /** 화면 밖(스크롤 아래)에 있으면 한 번 굴려서 보이게 — 상담실 맨 아래 「다시 상담하기」 */
  reveal?: boolean;
};

const all = (sel: string) => (root: HTMLElement) => [...root.querySelectorAll<HTMLElement>(sel)];

const button = (label: string) => (root: HTMLElement) =>
  [...root.querySelectorAll<HTMLElement>("button")].filter((b) => b.textContent?.trim() === label);

const COACHES: Coach[] = [
  {
    id: "preview",
    get text() {
      return `여기를 누르면 ${currentTeacher().name}과 문장마다 같이 분석해요.`;
    },
    find: button("분석하러 갈게요"),
  },
  {
    id: "word",
    text: "단어를 누르면 뜻이 나와요. 아무 단어나 눌러 볼까요?",
    find: (root) => all(".english-word:not(.cand)")(root).filter((el) => /[A-Za-z]{4,}/.test(el.textContent ?? "")),
  },
  { id: "star", text: "☆를 누르면 모르는 단어가 단어장에 저장돼요.", find: all(".vocab-star") },
  { id: "listen", text: "누르면 문장을 소리 내어 읽어 줘요.", find: all(".listen-icon") },
  { id: "slash", text: "끊어읽기를 누르면 문장을 의미 덩어리로 나눠 보여 줘요.", find: all(".slash-toggle:not(.trap-toggle)") },
  { id: "tip", text: "💡를 누르면 이 문장에 필요한 요령이 나와요.", find: all(".tip-chip") },
  {
    id: "unknown",
    text: "답을 모르겠으면 「잘 모르겠어요」를 눌러요. 힌트를 줘요.",
    find: button("잘 모르겠어요"),
    after: "word",
  },
  { id: "passage", text: "「전체 지문」을 누르면 언제든 지문 전체를 다시 볼 수 있어요.", find: all(".passage-btn"), after: "word" },
  { id: "arrows", text: "‹ › 로 앞뒤 문장을 오갈 수 있어요.", find: all(".sentence-arrow:not(:disabled)"), after: "passage" },
];

/*
  체험 분석 뒤 마을 둘러보기 (2026-10-22 선생님) — 교무실 → 연습실(탭마다) → 상담실.
  단계마다 `only`로 그 단계 것만 켠다 (`App.tsx`의 tour)
*/
const TOUR: Coach[] = [
  { id: "house-staff", text: "교무실에서 함께 공부할 선생님을 고를 수 있어요. 눌러 볼까요?", find: all(".house-staff") },
  { id: "house-practice", text: "연습실에서는 단어·문장·문법을 따로 연습해요. 들어가 볼까요?", find: all(".house-extra") },
  { id: "practice-vocab", text: "수업에서 ☆로 저장한 단어가 여기 모여요. 단어 테스트로 외워요.", find: button("단어") },
  { id: "practice-sentence", text: "문장 탭을 눌러 볼까요? 지문 문장을 해석 맞추기로 연습해요.", find: button("문장"), after: "practice-vocab" },
  { id: "practice-grammar", text: "문법 탭도 눌러 볼까요? 수업에서 담은 문법을 문제로 더 풀어요.", find: button("문법"), after: "practice-sentence" },
  { id: "house-counsel", text: "상담실에서 내 등급과 목표에 맞춰 코스를 짜요. 들어가 볼까요?", find: all(".house-counsel") },
  { id: "counsel-plan", text: "지금 등급과 목표를 알려 주면 나에게 맞는 코스를 짜 줘요. 눌러 볼까요?", find: button("다시 상담하기"), reveal: true },
];

export const PRACTICE_COACHES = ["practice-vocab", "practice-sentence", "practice-grammar"];

const KEY = "loopin.coach.v1";
function loadDone(): string[] {
  try {
    return JSON.parse(window.localStorage.getItem(KEY) ?? "[]") as string[];
  } catch {
    return [];
  }
}
function saveDone(done: string[]) {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(done));
  } catch {
    /* 저장이 안 돼도 이번 판에서는 기억한다 */
  }
}
/** 개발용 `?onboarding` — 길잡이를 처음부터 다시 */
export function resetCoach() {
  saveDone([]);
}

/** 가려지지 않고 화면에 보이는가 — 가운데 점을 눌렀을 때 그 요소가 맞는지 */
function visible(el: HTMLElement): boolean {
  const r = el.getBoundingClientRect();
  if (r.width < 2 || r.height < 2) return false;
  const x = r.left + r.width / 2;
  const y = r.top + r.height / 2;
  if (y < 0 || y > window.innerHeight || x < 0 || x > window.innerWidth) return false;
  // 길잡이 말풍선 자신에 가려진 건 가려진 게 아니다
  const hit = document.elementsFromPoint(x, y).find((h) => !h.closest(".coach-layer"));
  return !!hit && (hit === el || el.contains(hit) || hit.contains(el));
}

export function OnboardingCoach({ only }: { only?: string[] } = {}) {
  const coaches = only ? TOUR.filter((c) => only.includes(c.id)) : COACHES;
  const revealed = useRef(new Set<string>());
  const self = useRef<HTMLDivElement>(null);
  const [done, setDone] = useState<string[]>(loadDone);
  const [now, setNow] = useState<{ coach: Coach; el: HTMLElement } | null>(null);
  const [box, setBox] = useState<{ top: number; left: number; width: number; height: number; below: boolean } | null>(null);

  // 지금 짚을 것 — 화면이 바뀌는 걸 따로 듣지 않고 자주 둘러본다 (가볍다)
  useEffect(() => {
    const look = () => {
      const phone = self.current?.closest<HTMLElement>(".phone");
      if (!phone) return;
      // 칠판 손잡이 안내·확인 창이 떠 있거나 칠판이 곧 펼쳐질 참이면 쉰다 (펼쳐질 때 떴다가 바로 사라지지 않게)
      if (phone.querySelector(".board-coach, .exit-confirm, .board-drawer.open, .board-drawer.pending")) {
        setNow(null);
        return;
      }
      for (const coach of coaches) {
        if (done.includes(coach.id) || (coach.after && !done.includes(coach.after))) continue;
        const found = coach.find(phone);
        const el = found.find(visible);
        if (el) {
          setNow((n) => (n?.coach.id === coach.id && n.el === el ? n : { coach, el }));
          return;
        }
        if (coach.reveal && found[0] && !revealed.current.has(coach.id)) {
          revealed.current.add(coach.id);
          found[0].scrollIntoView({ block: "center" });
          return;
        }
      }
      setNow(null);
    };
    look();
    const id = window.setInterval(look, 400);
    return () => window.clearInterval(id);
  }, [done, only?.join(",")]); // eslint-disable-line react-hooks/exhaustive-deps

  // 자리 — .phone은 화면 크기에 맞춰 줄여 그리므로(scale) 줄인 비율로 나눠 phone 안 좌표로
  useLayoutEffect(() => {
    if (!now) {
      setBox(null);
      return;
    }
    const measure = () => {
      const phone = self.current?.closest<HTMLElement>(".phone");
      if (!phone) return;
      const p = phone.getBoundingClientRect();
      const scale = p.width / phone.offsetWidth || 1;
      const r = now.el.getBoundingClientRect();
      const top = (r.top - p.top) / scale;
      const height = r.height / scale;
      setBox({
        top,
        left: (r.left - p.left) / scale,
        width: r.width / scale,
        height,
        // 아래쪽 절반에 있는 것은 말풍선을 위에
        below: top + height / 2 < phone.offsetHeight / 2,
      });
    };
    measure();
    const id = window.setInterval(measure, 250);
    return () => window.clearInterval(id);
  }, [now]);

  const finish = (id: string) => {
    setDone((d) => {
      if (d.includes(id)) return d;
      const next = [...d, id];
      saveDone(next);
      return next;
    });
    setNow(null);
  };

  // 짚은 것을 직접 누르면 끝 — 단어는 아무 단어나
  useEffect(() => {
    if (!now) return;
    const onDown = (e: MouseEvent) => {
      const t = e.target as HTMLElement | null;
      if (!t) return;
      if (now.el.contains(t) || (now.coach.id === "word" && t.closest(".english-word"))) finish(now.coach.id);
    };
    document.addEventListener("click", onDown, true);
    return () => document.removeEventListener("click", onDown, true);
  }, [now]);

  const phoneW = self.current?.closest<HTMLElement>(".phone")?.offsetWidth ?? 390;
  const cardW = 240;
  const cardLeft = box ? Math.min(Math.max(10, box.left + box.width / 2 - cardW / 2), phoneW - cardW - 10) : 0;
  const arrowLeft = box ? Math.min(Math.max(14, box.left + box.width / 2 - cardLeft - 7), cardW - 28) : 0;

  return (
    <div ref={self} className="coach-layer" aria-live="polite">
      {now && box ? (
        <>
          <div
            className="coach-ring"
            style={{ top: box.top - 4, left: box.left - 4, width: box.width + 8, height: box.height + 8 }}
          />
          <div
            className={`coach-card${box.below ? " below" : " above"}`}
            style={{
              left: cardLeft,
              width: cardW,
              ...(box.below ? { top: box.top + box.height + 12 } : { bottom: `calc(100% - ${box.top - 12}px)` }),
            }}
            role="status"
          >
            <i className="coach-arrow" style={{ left: arrowLeft }} />
            <p>{now.coach.text}</p>
            <button type="button" onClick={() => finish(now.coach.id)}>
              알겠어요
            </button>
          </div>
        </>
      ) : null}
    </div>
  );
}
