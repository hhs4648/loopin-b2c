import { useEffect, useState, type CSSProperties, type ReactNode } from "react";
import { cloudEnabled } from "../tutor/cloud";
import { linkedEmail } from "../tutor/auth";
import { loadVocab } from "../tutor/vocab";
import { loadProgress } from "../tutor/progress";
import { courseProgress, isFirstVisit, isVocabSlot, loadPlan, nextMockOf } from "../tutor/counsel";
import { getMiniMock } from "../tutor/mini";
import type { SavedKind } from "./SavedBook";

/**
 * 홈 — **다정쌤 마을**.
 *
 * 그림은 `public/assets/village/` (배경 광장 + 집 세 채, 2026-10-19 받은 디자인).
 * 집은 따로 잘린 그림이라 하나씩 버튼으로 얹는다 — 누르고 싶게 보이도록
 *  - 지붕 위에 「안에 뭐가 있는지」 말풍선이 엇갈려 둥실 떠 있고,
 *  - 손가락을 대면 집이 살짝 들리며 발밑이 따뜻하게 빛나고, 누르면 꾹 눌린다.
 * 간판 글자는 그림에 굽지 않고 HTML로 얹는다 — 이름을 바꿔도 그림을 다시 안 만든다.
 *
 * 위치는 전부 `.village-map`(배경 그림과 같은 비율의 상자) 안의 %다.
 */

type Props = {
  learnerName: string | null;
  /** 「오늘의 10분」 — 코스에서 다음 10분 모의고사. 코스를 다 맞혔으면 수업 목록 */
  onStart: () => void;
  /** 교무실 — public/staff 의 선생님 고르기 페이지 */
  onOpenMini: () => void;
  /** 상담실 — 점수·목표를 듣고 커리큘럼을 짠다 */
  onOpenCounsel: () => void;
  /** 보충학습실(단어장) */
  onOpenSaved: (kind: SavedKind) => void;
  /** 「기록 지키기」 — 이메일을 붙여 다른 기기에서도 이어 한다 */
  onOpenAccount: () => void;
};

/** 별가루·친밀도 — 데모(학생 테스트)에서는 가린다. 쓰임이 정해지면 true로 (2026-10-19 선생님) */
const SHOW_STATS = false;

export function HomeVillage({ learnerName, onStart, onOpenMini, onOpenCounsel, onOpenSaved, onOpenAccount }: Props) {
  /** 이메일을 붙여 두었나 — 서버가 있을 때만 묻고, 모르는 동안은 「기록 지키기」로 둔다 */
  const [linked, setLinked] = useState<string | null>(null);
  useEffect(() => {
    if (!cloudEnabled()) return;
    let alive = true;
    void linkedEmail().then((e) => alive && setLinked(e));
    return () => {
      alive = false;
    };
  }, []);

  const plan = loadPlan();
  // 코스는 상담을 안 했어도 있다(최근 시험부터) — 「오늘의 10분」은 안 푼 첫 회, 다 돌면 틀린 문제 다시
  const planDone = courseProgress(plan);
  const nextId = nextMockOf(plan);
  // 첫 방문 — 10분 시험보다 다정쌤 분석을 먼저 한 문제 경험하게 (2026-10-20 선생님)
  const firstVisit = isFirstVisit();
  const nextVocab = nextId && isVocabSlot(nextId) ? getMiniMock(nextId.slice("vocab-".length)) : null;
  const nextMock = nextId && !nextVocab ? getMiniMock(nextId) : null;
  const vocabCount = loadVocab().length;
  const doneCount = Object.keys(loadProgress()).length;

  return (
    <div className="stage-fill village">
      <div className="village-map">
        <img className="village-ground" src="/assets/village/ground.webp" alt="" width={1122} height={1402} draggable={false} />

        <House
          img="staff"
          sign="교무실"
          badge={{ icon: "👋", text: "선생님 고르기" }}
          // 가운데 x · 바닥 y · 폭 (지도에 대한 %) · 간판 높이 (집 그림에 대한 %)
          at={{ x: 50, y: 48, w: 24, sign: 37 }}
          delay={0}
          onOpen={onOpenMini}
        />
        <House
          img="counsel"
          sign="상담실"
          badge={{ icon: "💬", text: plan ? `코스 ${planDone.done}/${planDone.total}` : "학습 상담" }}
          at={{ x: 33, y: 68, w: 21, sign: 37 }}
          delay={0.9}
          onOpen={onOpenCounsel}
        />
        <House
          img="extra"
          sign="연습실"
          badge={{ icon: "📒", text: vocabCount > 0 ? `단어 ${vocabCount} · 문장 · 문법` : "단어 · 문장 · 문법" }}
          at={{ x: 67.5, y: 70, w: 22, sign: 37 }}
          delay={1.8}
          onOpen={() => onOpenSaved("vocab")}
        />

        {/* 다정쌤 — 광장 한가운데 */}
        <div className="village-teacher">
          <div className="teacher-bob">
            <img src="/assets/character/dajung.webp" alt="다정쌤" width={650} height={616} draggable={false} />
          </div>
        </div>
      </div>

      <header className="village-top">
        <h1 className="village-home">홈</h1>
        {cloudEnabled() ? (
          <button type="button" className={`village-account${linked ? " linked" : ""}`} onClick={onOpenAccount} title={linked ?? "기록 지키기"}>
            {linked ? "✓ 기록 지킴" : "🔒 기록 지키기"}
          </button>
        ) : null}
        {SHOW_STATS ? (
          <div className="village-stats">
            <span className="village-stat">
              <StarIcon />
              별가루 <b>{(doneCount * 120).toLocaleString()}</b>
            </span>
            <span className="village-stat">
              <HeartIcon />
              친밀도 <b>Lv.{1 + Math.floor(doneCount / 3)}</b>
            </span>
          </div>
        ) : null}
      </header>
      <p className="village-hello">
        {learnerName ? (
          <>
            <small>{learnerName}님,</small>
            오늘도 함께 배워 볼까요?
          </>
        ) : (
          "오늘도 함께 배워 볼까요?"
        )}
      </p>

      <div className="village-dock">
        <button type="button" className="village-cta" onClick={onStart}>
          <span>
            {firstVisit ? "다정쌤과 한 문제 분석해 보기" : nextVocab ? `단어 외우기 · ${nextVocab.title}` : nextMock ? `오늘 · ${nextMock.title} 완전 정복` : "오늘의 학습 시작하기"}
            {firstVisit ? <small>5분 · 어려운 문제를 문장 단위로 같이 읽어요</small> : nextVocab ? <small>방금 푼 시험의 주요 단어 테스트</small> : nextMock ? <small>문제마다 단어 → 풀기 → 분석</small> : null}
          </span>
          <i className="village-cta-go">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 6l6 6-6 6" />
            </svg>
          </i>
        </button>
      </div>
    </div>
  );
}

type HouseProps = {
  img: "staff" | "counsel" | "extra";
  sign: string;
  badge: { icon: string; text: string };
  at: { x: number; y: number; w: number; sign: number };
  /** 말풍선이 한꺼번에 뜨지 않게 엇갈린다 (초) */
  delay: number;
  onOpen: () => void;
};

/* 그림 경로는 글자 그대로 — 공유용 한 장 HTML(build_share)이 이 문자열을 찾아 그림을 파일 안에 넣는다 */
const HOUSE_SRC: Record<HouseProps["img"], string> = {
  staff: "/assets/village/house-staff.webp",
  counsel: "/assets/village/house-counsel.webp",
  extra: "/assets/village/house-extra.webp",
};

function House({ img, sign, badge, at, delay, onOpen }: HouseProps) {
  const style = {
    left: `${at.x}%`,
    bottom: `${100 - at.y}%`,
    width: `${at.w}%`,
    "--sign-y": `${at.sign}%`,
    "--delay": `${delay}s`,
  } as CSSProperties;
  return (
    <button type="button" className={`house house-${img}`} style={style} aria-label={`${sign} — ${badge.text}`} onClick={onOpen}>
      <i className="house-glow" />
      <span className="house-body">
        <img src={HOUSE_SRC[img]} alt="" draggable={false} />
        <span className="house-sign">{sign}</span>
      </span>
      <span className="house-badge">
        <span className="house-badge-icon">{badge.icon}</span>
        {badge.text}
        <i className="house-badge-dot" />
      </span>
    </button>
  );
}

function StarIcon(): ReactNode {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24">
      <path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4L2.8 9.5l6.4-.8z" fill="#e7a93a" />
    </svg>
  );
}

function HeartIcon(): ReactNode {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24">
      <path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z" fill="#ef7a93" />
    </svg>
  );
}
