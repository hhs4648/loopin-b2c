import type { LessonCollection, LessonSet } from "../../content/tutor/types";
import type { PolicyLesson } from "./policy/types";
import { getPolicyLesson } from "./policy/lessons";
import { allCollections, setsIn } from "./sets";
import type { MiniItem, MiniMock } from "./mini";

/**
 * 10분 모의고사 — **시험마다 오답률 높은 5문제**를 시험지 순서로 묶어 시간을 재고 푼다 (2026-10-20 선생님).
 *
 * 코스의 단위다: 시험마다 오답률 Top 10을 5문제씩 (1)·(2)로 나눈다(2026-10-20 선생님). 코스 순서는 `counsel.ts`가 정한다.
 * 다 풀면 틀린 문제만 모아 다시(`mini.ts`의 복습 모의고사).
 * 문항은 따로 만들지 않고 **분석 레슨 JSON에서 그대로 꺼낸다** — 지문·문제·보기·정답이 거기 다 있다.
 * 그래서 레슨을 추가하면 10분 모의고사도 저절로 늘어난다. 레슨이 다섯 개 안 되는 시험은 있는 만큼, 세 개 미만이면 뺀다.
 */

export const TEN_MIN_PREFIX = "ten-";
export const TEN_MIN_MINUTES = 10;
export const TEN_MIN_COUNT = 5;
/** 시험마다 몇 문제까지 — Top 10을 5문제씩 두 회로 */
export const TEN_MIN_TOP = 10;
/** 두 번째 회는 이만큼은 남아야 만든다 */
const MIN_ITEMS = 3;

/** 세트 제목 「21번 문제」 → 21 */
function numberOf(set: LessonSet): number | null {
  const m = /(\d+)번/.exec(set.title);
  return m ? Number(m[1]) : null;
}

/** 세트 부제 「빈칸 — …」 → 빈칸 */
export function kindOfSet(set: LessonSet): string {
  return set.subtitle.split(" — ")[0]!.trim();
}

/** 레슨 source 「… 21번 (밑줄 의미 추론, 3점)」 → 3 */
function pointsOf(lesson: PolicyLesson): number {
  const m = /(\d)점\)/.exec(lesson.source ?? "");
  return m ? Number(m[1]) : 2;
}

/** 세트의 배점 — 진도표·목록의 「3점」 표시용 */
export function pointsOfSet(set: LessonSet): number {
  const lesson = getPolicyLesson(set.lessons[0]!);
  return lesson ? pointsOf(lesson) : 2;
}

/**
 * 코스 변형 — "all"은 오답률 순 그대로, "2pt"는 **2점 문제만**(등급이 낮은 학생은 3점을 버리고 2점부터 다진다, 2026-10-20 선생님).
 * id가 달라서(`ten-<시험>-2pt-1`) 기록도 따로 남는다
 */
export type TenMinVariant = "all" | "2pt";

/** 번호만 고르는 문항(어법·어휘·무관한 문장·문장 넣기)은 보기 글이 비어 있고, 지문 안의 ①~⑤를 본다 */
const NUMBERS_ONLY_TYPES = new Set(["grammar", "word_in_context", "irrelevant", "sentence_insertion"]);
/** ①brings처럼 번호 뒤 낱말에 밑줄 */
const MARKED_TYPES = new Set(["grammar", "word_in_context"]);

/** 레슨 하나 → 미니 모의고사 문항 하나. 정답이나 번호를 못 찾으면 null */
export function itemOfLesson(set: LessonSet, lesson: PolicyLesson): MiniItem | null {
  const exam = lesson.exam;
  const no = numberOf(set);
  if (!exam || no == null) return null;
  const answer = exam.options.findIndex((o) => o.correct) + 1;
  if (!answer) return null;
  const type = lesson.method?.type ?? "";

  /*
    주어진 글(순서)·주어진 문장(문장 넣기)·요약문은 `label`이 달린 문장이다. 순서 문제의 주어진 글은
    (A)가 나오기 전까지 여러 문장일 수 있다 — 세션(`session.ts`)과 같은 규칙으로 자른다.
  */
  const sentences = lesson.sentences;
  const givenAt = sentences.findIndex((x) => x.label && x.label !== "요약문");
  let givenEnd = givenAt;
  while (type === "order" && givenAt >= 0 && givenEnd + 1 < sentences.length &&
    !sentences[givenEnd + 1]!.label && !/^\([A-E]\)/.test(sentences[givenEnd + 1]!.text)) givenEnd++;
  const given = givenAt < 0 ? undefined : sentences.slice(givenAt, givenEnd + 1).map((x) => x.text).join(" ");
  const after = sentences.find((x) => x.label === "요약문")?.text;
  const body = sentences.filter((x, i) => !x.label && (i < givenAt || i > givenEnd)).map((x) => x.text);

  let passage: string | undefined;
  let paragraphs: string[] | undefined;
  if (type === "order") {
    // (A)(B)(C)로 시작하는 문장에서 새 단락
    paragraphs = [];
    for (const t of body) {
      if (/^\([A-E]\)/.test(t) || paragraphs.length === 0) paragraphs.push(t);
      else paragraphs[paragraphs.length - 1] += ` ${t}`;
    }
  } else {
    passage = body.join(" ");
  }

  const numbersOnly = !!exam.numbers_only || NUMBERS_ONLY_TYPES.has(type);
  const underline = typeof exam.underline === "string" && !/^\(?[①-⑤]/.test(exam.underline) ? exam.underline : undefined;

  return {
    no,
    kind: kindOfSet(set),
    points: pointsOf(lesson),
    answer,
    question: exam.question,
    ...(given ? { given } : {}),
    ...(passage ? { passage } : {}),
    ...(paragraphs ? { paragraphs } : {}),
    ...(after ? { after } : {}),
    ...(underline ? { underline } : {}),
    ...(MARKED_TYPES.has(type) ? { marked: true } : {}),
    options: numbersOnly ? ["", "", "", "", ""] : exam.options.map((o) => o.label),
    ...(set.wrong_rate != null ? { wrong_rate: set.wrong_rate } : {}),
    lesson: set.id,
    ...(exam.options.every((o) => o.ko) && !numbersOnly ? { options_ko: exam.options.map((o) => o.ko!) } : {}),
  };
}

/**
 * 이 시험에서 10분 모의고사에 넣을 세트 — 오답률 높은 순.
 * 비교용 사본(-v1)·듣기는 빼고, 장문(41~45번)도 뺀다 — 지문 하나에 문제 둘셋이 붙어 있어 한 문제만 떼어 내면 어색하다
 */
export function hardestSets(collectionId: string, count = TEN_MIN_COUNT, variant: TenMinVariant = "all"): LessonSet[] {
  return setsIn(collectionId)
    .filter((s) => !/-v\d+$/.test(s.id) && kindOfSet(s) !== "듣기 응답" && (numberOf(s) ?? 0) < 41)
    .filter((s) => variant === "all" || pointsOfSet(s) === 2)
    .sort((a, b) => (b.wrong_rate ?? -1) - (a.wrong_rate ?? -1))
    .slice(0, count);
}

/** 시험 하나 → (1) Top 1~5, (2) Top 6~10. 각 회 안에서는 시험지 순서 */
function mocksOf(c: LessonCollection, variant: TenMinVariant): MiniMock[] {
  const all = hardestSets(c.id, TEN_MIN_TOP, variant)
    .map((s) => {
      const lesson = getPolicyLesson(s.lessons[0]!);
      return lesson ? itemOfLesson(s, lesson) : null;
    })
    .filter((x): x is MiniItem => x != null);
  const out: MiniMock[] = [];
  for (let k = 0; k * TEN_MIN_COUNT < all.length; k++) {
    const items = all.slice(k * TEN_MIN_COUNT, (k + 1) * TEN_MIN_COUNT).sort((a, b) => a.no - b.no);
    if (items.length < MIN_ITEMS) break;
    const part = k + 1;
    out.push({
      id: `${TEN_MIN_PREFIX}${c.id}${variant === "2pt" ? "-2pt" : ""}-${part}`,
      subject: "english",
      // 「2026년 3월 10분 모의고사-1」 (2026-10-20 선생님) — 시험 이름 뒤의 「모의고사/모의평가」는 뺀다
      title: `${c.title.replace(/\s*(모의고사|모의평가)$/, "")} 10분 모의고사-${part}${variant === "2pt" ? " · 2점" : ""}`,
      subtitle: `${variant === "2pt" ? "2점 문제 " : ""}오답률 Top ${k * TEN_MIN_COUNT + 1}~${k * TEN_MIN_COUNT + items.length} · ${c.subtitle}`,
      source: c.subtitle,
      minutes: TEN_MIN_MINUTES,
      items,
    });
  }
  return out;
}

const cache = new Map<TenMinVariant, MiniMock[]>();

/** 시험마다 (1)(2), **최근 시험부터** (코스 순서는 `counsel.ts`가 다시 정한다) */
export function tenMinMocks(variant: TenMinVariant = "all"): MiniMock[] {
  const hit = cache.get(variant);
  if (hit) return hit;
  const exams = allCollections()
    .filter((c) => c.exam)
    .sort((a, b) => b.exam!.held.localeCompare(a.exam!.held));
  const out = exams.flatMap((c) => mocksOf(c, variant));
  cache.set(variant, out);
  return out;
}

/** 이 10분 모의고사가 어느 시험 것인가 (시행 연월·주관) */
export function examOfMock(mockId: string): { held: string; body: "평가원" | "교육청" } | null {
  const cid = mockId.replace(TEN_MIN_PREFIX, "").replace(/(-2pt)?-\d+$/, "");
  return allCollections().find((c) => c.id === cid)?.exam ?? null;
}

export function isTenMin(id: string): boolean {
  return id.startsWith(TEN_MIN_PREFIX);
}
