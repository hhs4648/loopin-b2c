import type { LessonSet } from "../../content/tutor/types";
import type { StudentLevel } from "./policy/student-state";
import { pushKey } from "./cloud";
import { allAttempts, estimatedExamScore, getMiniMock, loadAttempts, scoreOf, type MiniScore } from "./mini";
import { reviewProgress } from "./wrongReview";
import { getPolicyLesson } from "./policy/lessons";
import { getSet } from "./sets";
import { loadVocab, type VocabEntry } from "./vocab";
import { examOfMock, tenMinMocks, TEN_MIN_PREFIX } from "./tenmin";
import { isDone, loadProgress } from "./progress";
import { allCollections } from "./sets";

/**
 * 상담실 — 점수·목표·아쉬운 유형·공부 시간을 듣고 **코스**를 짠다 (2026-10-19, 2026-10-20 고침).
 *
 * 코스의 단위는 **10분 모의고사**(`tenmin.ts` — 시험마다 오답률 Top 10을 (1)(2) 5문제씩)다. 문제를 유형별로
 * 듬성듬성 고르는 대신, 한 회씩 시간을 재고 풀고, 틀린 것은 다정쌤 분석으로 간다.
 *
 * 순서(2026-10-20 선생님): 3·6·9월 모의고사와 수능을 합쳐 최근 것부터 → 나머지(5·6·10월 등).
 * 회차마다 단어 학습 → 실전 풀기 → 분석 → **틀린 문제 복습**(4단계, `wrongReview.ts`). 틀린 문제 전체는 「틀린 문제」 화면에서 모아 다시 푼다.
 *
 * 수업처럼 LLM을 부르지 않는다. 대사는 상담실 화면에 미리 적어 두고, 코스는 규칙으로 만든다.
 * 상담을 안 했어도 기본 코스(최근 시험부터)는 같다 — 상담은 등급·목표·아쉬운 유형을 기록해 두는 자리다.
 */

/** 학생이 고르는 「아쉬운 유형」 — 세트 부제의 유형(「빈칸 — …」)으로 이어진다 */
export const WEAK_TYPES: { label: string; kinds: string[] }[] = [
  { label: "빈칸", kinds: ["빈칸"] },
  { label: "순서", kinds: ["순서"] },
  { label: "문장 넣기", kinds: ["문장 넣기"] },
  { label: "어휘·어법", kinds: ["어휘", "어법"] },
  { label: "밑줄 의미", kinds: ["밑줄 의미", "지칭"] },
  { label: "제목·주제·요지", kinds: ["제목", "주제", "요지", "요약문", "무관한 문장"] },
  { label: "듣기", kinds: ["듣기 응답"] },
];
export const TIME_SHORT = "시간이 모자라요";

export const EXAMS = ["다음 모의고사", "수능", "내신"] as const;
export type Exam = (typeof EXAMS)[number];

export const MINUTES = [15, 30, 60] as const;
export type Minutes = (typeof MINUTES)[number];

export type CounselAnswers = {
  /** 최근 모의고사 등급 1~9. 안 봤으면 null */
  grade: number | null;
  /** 점수로 입력했으면 그 점수 */
  score?: number;
  goal: number;
  exam: Exam;
  /** WEAK_TYPES의 label들 */
  weak: string[];
  timeShort: boolean;
  minutes: Minutes;
  /** 수능 기출을 모의고사보다 먼저 */
  suneungFirst?: boolean;
  /** 3점 문제는 빼고 2점부터 — 등급이 낮은 학생 */
  skipThree?: boolean;
};

/** 공부 시간 → 하루에 10분 모의고사 몇 회 (분석·단어까지 한 회에 30분쯤 잡는다) */
export const MOCKS_PER_DAY: Record<Minutes, number> = { 15: 1, 30: 1, 60: 2 };

export type CounselPlan = {
  version: 2;
  at: string;
  answers: CounselAnswers;
  /** 집중할 유형 (WEAK_TYPES label) — 학생이 고른 것 + 기록에서 찾은 것 */
  focus: string[];
  /** 10분 모의고사 id들 — 푸는 순서 */
  course: string[];
};

/** 영어 절대평가 — 90점 이상 1등급, 10점마다 한 등급 */
export function gradeOfScore(score: number): number {
  const s = Math.max(0, Math.min(100, Math.round(score)));
  return Math.min(9, Math.max(1, Math.floor((99 - s) / 10) + 1));
}

/** 수업 화면 단계 — 고 1~2 · 중 3~5 · 초 6~ (모르면 중) */
export function levelOfGrade(grade: number | null): StudentLevel {
  if (grade == null) return "중";
  if (grade <= 2) return "고";
  if (grade <= 5) return "중";
  return "초";
}

/** 세트 부제 맨 앞의 유형 — 「빈칸 — 지리학이 묻는 '어디'」 → 빈칸 */
export function kindOf(set: LessonSet): string {
  return set.subtitle.split(" — ")[0]!.trim();
}

export function weakLabelOfKind(kind: string): string | null {
  return WEAK_TYPES.find((w) => w.kinds.includes(kind))?.label ?? null;
}

/** 미니 모의고사에서 절반 넘게 틀린 유형 (WEAK_TYPES label) — 상담에서 「기록을 보니」로 먼저 짚는다 */
export function weakFromMini(rows: { kind: string; right: number; total: number }[]): string[] {
  const agg = new Map<string, { right: number; total: number }>();
  for (const r of rows) {
    const label = weakLabelOfKind(r.kind);
    if (!label) continue;
    const a = agg.get(label) ?? { right: 0, total: 0 };
    a.right += r.right;
    a.total += r.total;
    agg.set(label, a);
  }
  return WEAK_TYPES.map((w) => w.label).filter((l) => {
    const a = agg.get(l);
    return a != null && a.total > 0 && a.right / a.total < 0.5;
  });
}

/**
 * 시험의 순위 — 3·6·9월 모의고사와 수능(0)을 합쳐 최근 것부터, 5·6·10월 등 나머지(2)는 뒤에.
 * 「수능 먼저」(suneungFirst)는 더 묻지 않는다 (2026-10-20 선생님) — 켜 두면 수능이 -1로 앞에 온다
 */
export function examTier(exam: { held: string; body: string } | null, suneungFirst = false): number {
  if (!exam) return 3;
  const month = Number(exam.held.slice(5, 7));
  if (exam.body === "평가원" && month === 11) return suneungFirst ? -1 : 0;
  return [3, 6, 9].includes(month) ? 0 : 2;
}

/** 기본 코스 — 순위대로, 같은 순위 안에서는 최근 시험부터 ((1) 다음 (2)). skipThree면 2점 문제만 */
export function defaultCourse(suneungFirst = false, skipThree = false): string[] {
  return tenMinMocks(skipThree ? "2pt" : "all")
    .map((m, i) => ({ m, i, tier: examTier(examOfMock(m.id), suneungFirst) }))
    .sort((a, b) => a.tier - b.tier || a.i - b.i)
    .map((x) => x.m.id);
}

/** 상담 답을 기록하고 코스를 짠다 */
export function buildPlan(answers: CounselAnswers, fromRecords: string[] = []): CounselPlan {
  const focus = [...new Set([...answers.weak, ...fromRecords])];
  return { version: 2, at: new Date().toISOString(), answers, focus, course: defaultCourse(!!answers.suneungFirst, !!answers.skipThree) };
}

/* ── 첫 방문 — 10분 시험보다 분석을 먼저 경험하게 (2026-10-20 선생님: 앱의 강점은 분석) ── */

/** 기록이 하나도 없다 — 수업도, 10분 모의고사도 */
export function isFirstVisit(): boolean {
  return Object.keys(loadProgress()).length === 0 && Object.values(allAttempts()).every((l) => !l.length);
}

/** 첫 방문에 분석해 볼 문제 — 코스 첫 회의 오답률 1위 (분석 레슨이 있는 것) */
export function onboardingSet(plan: CounselPlan | null): LessonSet | null {
  const ids = plan?.course?.length ? plan.course : defaultCourse();
  const mock = getMiniMock(ids[0] ?? null);
  if (!mock) return null;
  const top = [...mock.items].sort((a, b) => (b.wrong_rate ?? -1) - (a.wrong_rate ?? -1)).find((it) => it.lesson);
  return top?.lesson ? getSet(top.lesson) : null;
}

/** 첫 방문 체험이 끝나면 여는 10분 모의고사 — 코스 첫 회 */
export function firstMockId(plan: CounselPlan | null): string | null {
  const ids = plan?.course?.length ? plan.course : defaultCourse();
  return ids[0] ?? null;
}

/** 틀린 문제 복습은 회차마다 4단계로 한다 (2026-10-20 선생님) — 세 회마다 끼우던 복습 칸은 뺐다 */

/* ── 단어 칸 — 한 회를 풀면 그 회 주요 단어 테스트가 정규 코스로 따라온다 (2026-10-20 선생님: 단어가 너무 중요하다) ── */

export const VOCAB_PREFIX = "vocab-";
export const isVocabSlot = (id: string) => id.startsWith(VOCAB_PREFIX);
const VOCAB_SLOT_KEY = "loopin.vocab-slots.v1";

function loadVocabSlots(): Record<string, string> {
  try {
    const raw = window.localStorage.getItem(VOCAB_SLOT_KEY);
    const all = raw ? (JSON.parse(raw) as Record<string, string>) : {};
    return all && typeof all === "object" ? all : {};
  } catch {
    return {};
  }
}

export function vocabSlotDone(id: string): boolean {
  return id in loadVocabSlots();
}

export function markVocabSlot(id: string): void {
  try {
    window.localStorage.setItem(VOCAB_SLOT_KEY, JSON.stringify({ ...loadVocabSlots(), [id]: new Date().toISOString() }));
    pushKey(VOCAB_SLOT_KEY);
  } catch {
    /* 그대로 */
  }
}

/** 10분 모의고사 한 회의 주요 단어 — 문항마다 분석 레슨의 단어 체크 목록(지문 단어 앞 8개 + 보기 단어 앞 4개) */
export function mockKeyWords(mockId: string): VocabEntry[] {
  const mock = getMiniMock(mockId);
  if (!mock) return [];
  const out: VocabEntry[] = [];
  const seen = new Set<string>();
  for (const it of mock.items) {
    const set = it.lesson ? getSet(it.lesson) : null;
    const lesson = set ? getPolicyLesson(set.lessons[0]!) : null;
    const kw = lesson?.key_words;
    if (!kw) continue;
    for (const w of [...kw.passage.slice(0, 8), ...kw.options.slice(0, 4)]) {
      const k = w.en.trim().toLowerCase();
      if (seen.has(k)) continue;
      seen.add(k);
      out.push({ en: w.en, ko: w.ko, sentence: "", source: lesson!.id, kind: /\s/.test(w.en.trim()) ? "phrase" : "word", savedAt: "" });
    }
  }
  // 교무실의 긴 모의고사(21문항)는 수백 개가 되니 40개까지 — 10분 모의고사(5문항)는 다 들어간다
  return out.slice(0, 40);
}

/** 단어 연습을 하려면 적어도 이만큼 — 별표 단어가 모자라면 주요 단어로 채운다 */
const VOCAB_MIN = 6;

/**
 * 3단계 「단어 연습」에서 볼 단어 — **별표 단어 위주** (2026-10-20 선생님): 이 회 레슨에서 ★로 저장한 단어 + 풀 때 보라펜으로
 * 표시한 단어. 모자라면 그 회 주요 단어로 채운다. 미리 보기(풀기 전 단어 화면)는 단어 학습으로 치지 않는다
 */
export function vocabSlotWords(slotId: string): VocabEntry[] {
  const mockId = slotId.slice(VOCAB_PREFIX.length);
  const mock = getMiniMock(mockId);
  if (!mock) return [];
  const lessons = new Set(mock.items.map((it) => (it.lesson ? getSet(it.lesson)?.lessons[0] : undefined)).filter((x): x is string => !!x));
  const out: VocabEntry[] = [];
  const has = (en: string) => out.some((w) => w.en.toLowerCase() === en.toLowerCase());
  for (const w of loadVocab()) if (w.source && (lessons.has(w.source) || w.source === mockId) && !has(w.en)) out.push(w);
  const last = loadAttempts(mockId)[0];
  for (const u of last?.unknown ?? []) {
    if (!u.ko || has(u.en)) continue;
    out.push({ en: u.en, ko: u.ko, sentence: "", source: mockId, kind: "word", savedAt: "" });
  }
  for (const w of mockKeyWords(mockId)) {
    if (out.length >= VOCAB_MIN) break;
    if (!has(w.en)) out.push(w);
  }
  return out;
}

/** 코스 한 칸 — 10분 모의고사 하나의 상태 */
export type CourseItem = {
  id: string;
  title: string;
  subtitle: string;
  /** 풀어 본 적 있나 (가장 최근 기록 기준) */
  done: boolean;
  score: MiniScore | null;
  /** 예상 시험점수(100점 환산) — 푼 회만 */
  estimate?: number;
  seconds: number | null;
  /** 최근 기록에서 틀리거나 안 푼 문항 수 */
  wrong: number;
  /** 복습 모의고사(틀린 문제 다시) 칸인가 */
  review?: boolean;
  /** 단어 칸(그 회 주요 단어 테스트)인가 */
  vocab?: boolean;
  /** 어느 시험 것인가 — 코스 화면이 연도 → 시험으로 묶는다 */
  exam?: { collectionId: string; title: string; year: number; held: string };
  /** 1단계 단어 학습을 했나 (건너뛰어도 된다) */
  words?: boolean;
  /** 3단계 분석 — 틀린 문항 중 분석한 수 / 틀린 문항 수 (다 맞혔으면 0/0 = 완료) */
  analysis?: { done: number; total: number };
  /** 4단계 틀린 문제 복습 — 복습한 수 / 복습할 수 (다 맞혔으면 0/0 = 완료) */
  review4?: { done: number; total: number };
  /** 문항마다 결과 — 코스 화면의 작은 표시 */
  marks?: { no: number; kind: string; points: number; result: "right" | "wrong" | "none"; peeked: boolean; checked: boolean; analyzed: boolean }[];
};

/** 10분 모의고사가 속한 시험 — 제목 앞 연도(평가원은 학년도)로 묶는다 */
function examInfoOf(mockId: string): CourseItem["exam"] | undefined {
  const cid = mockId.replace(TEN_MIN_PREFIX, "").replace(/(-2pt)?-\d+$/, "");
  const c = allCollections().find((x) => x.id === cid);
  if (!c?.exam) return undefined;
  const year = Number(/(\d{4})/.exec(c.title)?.[1] ?? c.exam.held.slice(0, 4));
  return { collectionId: c.id, title: c.title, year, held: c.exam.held };
}

/** 코스 전체의 상태 — 계획이 없으면 기본 코스. 회차마다 단어 → 실전 → 분석 → 틀린 문제 복습(4단계) */
export function courseStatus(plan: CounselPlan | null): CourseItem[] {
  const ids = plan?.course?.length ? plan.course : defaultCourse();
  const items: CourseItem[] = [];
  const progress = loadProgress();
  ids.forEach((id) => {
    const mock = getMiniMock(id);
    if (!mock) return;
    const last = loadAttempts(id)[0];
    const score = last ? scoreOf(mock, last.answers) : null;
    const marks = mock.items.map((it) => {
      const set = it.lesson ? getSet(it.lesson) : null;
      const mine = last?.answers[it.no];
      return {
        no: it.no,
        kind: it.kind,
        points: it.points,
        result: (mine == null ? "none" : mine === it.answer ? "right" : "wrong") as "right" | "wrong" | "none",
        peeked: !!last?.peeked?.includes(it.no),
        checked: !!last?.checked?.includes(it.no),
        analyzed: !!set && isDone(progress, set.id),
      };
    });
    const toAnalyze = last ? marks.filter((m) => m.result !== "right") : [];
    items.push({
      id,
      title: mock.title,
      subtitle: mock.subtitle,
      done: !!last,
      score,
      ...(last ? { estimate: estimatedExamScore(mock, last.answers) } : {}),
      seconds: last?.seconds ?? null,
      wrong: score ? score.total - score.correct : mock.items.length,
      exam: examInfoOf(id),
      words: vocabSlotDone(`${VOCAB_PREFIX}${id}`),
      analysis: { done: toAnalyze.filter((m) => m.analyzed).length, total: toAnalyze.length },
      review4: reviewProgress(id),
      marks,
    });
  });
  return items;
}

/** 오늘 할 것 — 아직 안 푼 첫 칸(복습 칸 포함), 전부 끝났으면 null(다 맞힘) */
export function nextMockOf(plan: CounselPlan | null): string | null {
  const items = courseStatus(plan);
  return items.find((it) => !it.done)?.id ?? null;
}

export function courseProgress(plan: CounselPlan | null): { done: number; total: number } {
  const items = courseStatus(plan).filter((it) => !it.review && !it.vocab);
  return { done: items.filter((it) => it.done).length, total: items.length };
}

const KEY = "loopin.counsel.v1";

export function loadPlan(): CounselPlan | null {
  try {
    const raw = window.localStorage.getItem(KEY);
    const parsed = raw ? (JSON.parse(raw) as CounselPlan) : null;
    // 예전(v1, 문제 낱개 계획)은 버린다 — 다시 상담하면 코스로 짠다
    if (!parsed || parsed.version !== 2 || !Array.isArray(parsed.course)) return null;
    // 10분 모의고사 id가 바뀌었거나(예: (1)(2)로 나뉨) 시험이 늘었으면 상담 답은 두고 코스만 다시 짠다
    const fresh = defaultCourse(!!parsed.answers?.suneungFirst, !!parsed.answers?.skipThree);
    if (parsed.course.length !== fresh.length || parsed.course.some((id) => !fresh.includes(id))) return { ...parsed, course: fresh };
    return parsed;
  } catch {
    return null;
  }
}

export function savePlan(plan: CounselPlan): void {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(plan));
    pushKey(KEY);
  } catch {
    /* 저장 못 해도 이번 화면에는 보인다 */
  }
}
