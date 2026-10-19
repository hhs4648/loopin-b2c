import type { CSSProperties, ReactNode } from "react";
import { loadVocab } from "../tutor/vocab";
import { loadProgress } from "../tutor/progress";
import { loadPlan, planProgress } from "../tutor/counsel";
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
  /** 「오늘의 학습 시작하기」 — 계획이 있으면 그다음 문제, 없으면 수업 목록 */
  onStart: () => void;
  /** 교무실 — 미니 모의고사 */
  onOpenMini: () => void;
  /** 상담실 — 점수·목표를 듣고 커리큘럼을 짠다 */
  onOpenCounsel: () => void;
  /** 보충학습실(단어장) */
  onOpenSaved: (kind: SavedKind) => void;
};

/** 별가루·친밀도 — 데모(학생 테스트)에서는 가린다. 쓰임이 정해지면 true로 (2026-10-19 선생님) */
const SHOW_STATS = false;

export function HomeVillage({ learnerName, onStart, onOpenMini, onOpenCounsel, onOpenSaved }: Props) {
  const plan = loadPlan();
  const planDone = plan ? planProgress(plan, loadProgress()) : null;
  const vocabCount = loadVocab().length;
  const doneCount = Object.keys(loadProgress()).length;

  return (
    <div className="stage-fill village">
      <div className="village-map">
        <img className="village-ground" src="/assets/village/ground.webp" alt="" width={1122} height={1402} draggable={false} />

        <House
          img="staff"
          sign="교무실"
          badge={{ icon: "⏱", text: "미니 모의고사" }}
          // 가운데 x · 바닥 y · 폭 (지도에 대한 %) · 간판 높이 (집 그림에 대한 %)
          at={{ x: 50, y: 48, w: 24, sign: 37 }}
          delay={0}
          onOpen={onOpenMini}
        />
        <House
          img="counsel"
          sign="상담실"
          badge={{ icon: "💬", text: planDone ? `내 계획 ${planDone.done}/${planDone.total}` : "학습 상담" }}
          at={{ x: 33, y: 68, w: 21, sign: 37 }}
          delay={0.9}
          onOpen={onOpenCounsel}
        />
        <House
          img="extra"
          sign="보충학습실"
          badge={{ icon: "📒", text: vocabCount > 0 ? `단어장 ${vocabCount}` : "단어장" }}
          at={{ x: 67.5, y: 70, w: 22, sign: 37 }}
          delay={1.8}
          onOpen={() => onOpenSaved("vocab")}
        />

        {/* 다정쌤 — 광장 한가운데 */}
        <div className="village-teacher">
          <div className="teacher-bob">
            <img src="/assets/dajung-teacher.webp" alt="다정쌤" width={650} height={616} draggable={false} />
          </div>
        </div>
      </div>

      <header className="village-top">
        <h1 className="village-home">홈</h1>
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
          <span>{plan ? "오늘의 계획 이어 하기" : "오늘의 학습 시작하기"}</span>
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
