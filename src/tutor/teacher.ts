/**
 * 선생님 고르기 (2026-10-22 선생님).
 *
 * 교무실에서 쌤을 고르면 **앱 전체가 그 쌤으로** 바뀐다 — 그림, 이름, 색, 말투.
 * 해금·재화 없이 누구나 바로 고른다. 쌤마다 맡은 활동을 나누지도 않는다.
 *
 * - 색: `<html data-teacher>`에 id를 달면 `styles.css`가 `--accent*` 변수를 바꾼다.
 * - 말투: 상냥쌤·소심쌤은 존댓말, 나머지는 반말. 레슨 대사는 다정쌤 해요체로 한 벌만
 *   있으므로 반말 쌤은 `speak()`가 끝말만 반말로 바꾼다 (세션 `view()` 한 곳에서).
 * - 표 대사(`LINES`)는 기획 표(상황별 · 선생님별 멘트)를 그대로 옮겼다. 전부 초안이라
 *   표가 고쳐지면 여기만 고친다.
 * - 고른 쌤은 이 기기에만 남는다 (서버 사본 없음).
 */

export type TeacherId = "sangnyang" | "strict" | "fun" | "prickly" | "daechung" | "sosim";

export type Mood = "happy" | "sorry";

/** 그림 옆에 잠깐 뜨는 쌤 한마디 — 표의 상황 */
export type Reaction =
  | "start"
  | "correct"
  | "combo"
  | "best"
  | "wrong"
  | "repeat"
  | "done"
  | "slump";

export type Teacher = {
  id: TeacherId;
  /** 화면에 쓰는 이름 */
  name: string;
  full: string;
  /** 칩 동그라미 한 글자 */
  initial: string;
  /** 반말 쌤이면 레슨 대사 끝말을 반말로 */
  banmal: boolean;
  /** 기본 그림과 표정 그림. 표정 그림이 없으면 기본 그림 + 움직임으로 대신한다 */
  art: { base: string; happy?: string; sorry?: string };
  /** 칩·이름표 바탕 (교무실 고르기 동그라미에도) */
  color: string;
};

/*
  그림 경로는 글자 그대로 둔다 — 공유용 한 장 HTML(build_share)이 문자열을 찾아 그림을 파일 안에 넣는다.
  원본: 상냥쌤 public/assets/character/dajung-down*.svg, 엄한·재밌는·까칠(예쁜 버전 prickly-v2) 같은 폴더 svg,
  대충·소심 dajung-design/assets/teachers-daechung-sosim-kkachil.png — 650×616 webp로 줄여 teachers/에 둔다.
*/
export const TEACHERS: Teacher[] = [
  {
    id: "sangnyang",
    name: "상냥쌤",
    full: "상냥한 선생님",
    initial: "상",
    banmal: false,
    art: {
      base: "/assets/character/teachers/sangnyang.webp",
      happy: "/assets/character/teachers/sangnyang-happy.webp",
      sorry: "/assets/character/teachers/sangnyang-sorry.webp",
    },
    color: "#ef7a93",
  },
  { id: "strict", name: "엄한쌤", full: "엄한 선생님", initial: "엄", banmal: true, art: { base: "/assets/character/teachers/strict.webp" }, color: "#8a6fd1" },
  { id: "fun", name: "재밌는쌤", full: "재밌는 선생님", initial: "재", banmal: true, art: { base: "/assets/character/teachers/fun.webp" }, color: "#e9b228" },
  { id: "prickly", name: "까칠쌤", full: "까칠한 선생님", initial: "까", banmal: true, art: { base: "/assets/character/teachers/prickly.webp" }, color: "#7d7684" },
  { id: "daechung", name: "대충쌤", full: "대충하는 선생님", initial: "대", banmal: true, art: { base: "/assets/character/teachers/daechung.webp" }, color: "#5ea777" },
  { id: "sosim", name: "소심쌤", full: "소심한 선생님", initial: "소", banmal: false, art: { base: "/assets/character/teachers/sosim.webp" }, color: "#ef9670" },
];

export const DEFAULT_TEACHER: TeacherId = "sangnyang";

/** quit — 수업 중 ✕를 눌렀을 때 나가기 확인 창의 한마디 (2026-10-22 선생님: 「정말 여기까지만 할 거야?」를 쌤마다) */
type Lines = Record<Reaction | "greet" | "away" | "quit" | "streak" | "comeback" | "growth", string> & {
  free: string[];
  /** 다른 쌤을 만났을 때 하는 말 — 교무실에서 쌤을 바꾸면 새 쌤이 앞 쌤에게 */
  meet: Partial<Record<TeacherId, string>>;
};

export const LINES: Record<TeacherId, Lines> = {
  sangnyang: {
    greet: "와, 오늘도 와줬네요! 기다리고 있었어요.",
    start: "천천히 해도 괜찮아요. 저 여기 있을게요.",
    correct: "정답이에요! 방금 푸는 과정 진짜 좋았어요.",
    combo: "세 문제 연속이에요! 지금 완전 흐름 탔어요!",
    best: "오늘은 칭찬을 아끼려야 아낄 수가 없네요. 정말 최고였어요.",
    wrong: "괜찮아요, 여기서 틀리는 게 제일 잘한 거예요. 시험에서 안 틀리면 되니까요!",
    // 표 원문 「지난주엔 세 번 틀렸는데…」는 실제 기록과 상관없이 떠서 바꿨다 — 틀렸던 문제를 다시 풀 때 또 틀린 순간
    repeat: "괜찮아요, 여기가 헷갈리는 곳이라는 걸 찾은 거예요. 한 번만 더 같이 봐요!",
    away: "바쁜 거 알아요. 그래도 우리 딱 한 문제만 하고 갈까요? 응?",
    quit: "정말 여기까지만 할 거예요? 조금만 더 하면 금방인데요.",
    done: "오늘도 해냈네요! 어제의 나보다 한 걸음 앞섰어요.",
    streak: "{n}일 연속 출석! 대단해요!",
    comeback: "돌아온 게 중요한 거죠! 어서 와요!",
    growth: "처음 왔을 때랑 지금이랑… 저는 다 기억해요. 정말 많이 컸어요.",
    slump: "잘하는 날만 학생인 게 아니에요. 힘든 날 온 것도 공부예요.",
    free: [
      "여기까지 온 것만으로도 대단한걸요?",
      "우리 딱 하나만 더 해볼까요? 응?",
      "틀린 만큼 똑똑해지는 거예요!",
      "오늘의 칭찬 배달 왔습니다~",
      "그래도 아까보다 늘었어요!",
    ],
    meet: {
      strict: "오늘도 무서운 얼굴이네요~ 근데 칭찬은 저한테 맡겨요!",
      prickly: "그 한숨 뒤에 걱정 있는 거 다 알아요~",
      daechung: "커피만 마시지 말고 우리 딱 하나만 같이 해요, 응?",
      sosim: "오늘 목소리 좀 커진 것 같은데요? 대단해요!",
      fun: "개그 나오면 제가 제일 먼저 웃어줄게요!",
    },
  },
  strict: {
    greet: "왔네. 앉아. 바로 시작한다.",
    start: "집중. 시간은 흐르고 있다.",
    correct: "…맞았네. 다음.",
    combo: "흠. 오늘 좀 하는데.",
    best: "…흠. 나쁘지 않군.",
    wrong: "틀렸어. 어디서 틀렸는지 스스로 찾아봐. 못 찾겠으면 그때 물어보고.",
    repeat: "또 같은 데서 틀렸네.",
    away: "어제도 그 소리 했다. 지금 해.",
    quit: "벌써 일어나? 정말 여기까지만 할 거야?",
    done: "오늘 할 건 했네. 그거면 됐어.",
    streak: "당연한 걸로 유난 떨지 마. …그래도 나쁘지 않네.",
    comeback: "일주일 만이네. 변명은 됐고.",
    growth: "…솔직히 말하면, 잘하고 있어. 이 말 두 번은 안 한다.",
    slump: "…오늘은 여기까지. 못해서가 아니라, 내일 하려고 멈추는 거다.",
    free: ["변명은 접수하지 않는다.", "다시. 처음부터.", "미루는 건 내일의 나를 괴롭히는 일이다."],
    meet: {
      sangnyang: "칭찬은 아껴 써. 남발하면 값이 떨어진다.",
      prickly: "…너도 결국 나랑 같은 쪽이잖아. 방식만 다르지.",
      daechung: "커피 내려놔. 여기는 교무실이지 휴게실이 아니다.",
      sosim: "말끝 흐리지 마. 틀려도 되니까 끝까지 말해.",
      fun: "개그는 접수하지 않는다. …수업 끝나고는 봐주지.",
    },
  },
  fun: {
    greet: "왔구나! 오늘 개그 하나 준비해놨는데, 문제 먼저야.",
    start: "이 문장 클리어하면 오늘의 개그 하나 풀어줌.",
    correct: "정답! 이 정도면 오늘 개그 하나 풀어야겠네.",
    combo: "연속 정답? 이거 콤보 보너스로 개그 두 개 간다.",
    best: "…야, 이건 개그로 못 넘기겠다. 진짜 잘했어.",
    wrong: "오~ 그 오답, 나도 옛날에 똑같이 틀렸던 명작이야.",
    repeat: "또 여기야? 이 문제, 너 팬이라도 됐나 봐.",
    away: "안 오면 개그 유통기한 지난다? 오늘 거 진짜 웃긴데.",
    quit: "정말 여기까지만 할 거야? 개그 아직 하나 남았는데.",
    done: "오늘 분량 클리어! 약속한 개그는… 내일 와야 들려줌.",
    streak: "{n}일 연속? 이 정도면 개그 구독자 인정.",
    comeback: "오랜만! 그동안 쌓인 개그가 일곱 개다. 하나씩 풀자.",
    growth: "…오늘은 개그 안 할게. 진지하게, 너 진짜 대단해.",
    slump: "…웃기려는 거 아니고. 오늘 같은 날 온 게 제일 잘한 일이야.",
    free: ["공부는 원래 재미없어. 그래서 내가 있는 거지."],
    meet: {
      sangnyang: "우리 콤비 하자. 내가 웃기고 상냥쌤이 칭찬하고.",
      strict: "엄한쌤 웃기는 게 내 인생 목표야. 오늘도 실패.",
      prickly: "까칠쌤도 웃을 줄 알아? 한 번만 보여줘 봐.",
      daechung: "그 커피, 개그 소재로 써도 돼?",
      sosim: "웃어도 돼. 내 개그는 웃으라고 있는 거야.",
    },
  },
  prickly: {
    greet: "…왔어? 인사는 됐고, 어제 틀린 거 기억은 나?",
    start: "시작해. 대충 찍지 말고, 왜 그런지까지 생각해.",
    correct: "…맞았네. 그럼 됐어.",
    combo: "…연속이네. 이 페이스, 내일도 유지해.",
    best: "…이건 인정. 두 번 말 안 할 거니까 잘 들어.",
    // 표 원문 「어디서 헷갈렸는지부터 말해」는 대답할 곳 없는 질문이라 바꿨다 (헷갈린 곳 묻기는 보류)
    wrong: "됐고. 왜 틀렸는지는 분석하면서 내가 짚어 줄 테니까 똑바로 봐.",
    repeat: "…그거 아까 배운 건데. 다시 봐.",
    away: "…이틀째야. 시험 날 울고 싶으면 계속 미뤄.",
    quit: "…정말 여기까지만 할 거야? 뭐, 네 맘이지.",
    done: "…끝. 오늘 한 거, 내일 또 물어볼 거니까 까먹지 마.",
    streak: "…{n}일째네. {n1}일째부터가 진짜니까 내일 봐.",
    comeback: "…일주일. 뭐 배웠는지 다 까먹었겠네. 처음부터 다시.",
    growth: "…까칠하게 굴 이유가 없어졌네. 이제 시험 날 안 울겠어.",
    slump: "…오늘은 안 까칠하게 굴게. 틀린 거 세지 말고, 온 것만 세.",
    free: ["'괜찮겠지'가 제일 위험한 말이야."],
    meet: {
      sangnyang: "그렇게 다 괜찮다고 하면, 시험 날 누가 울지 뻔해.",
      strict: "…같은 편 취급하지 마. 난 화내는 게 아니라 미리 말해주는 거야.",
      daechung: "'대충'? 그 단어 여기서 쓰지 마. 소름 돋아.",
      sosim: "…힌트 줄 거면 빨리 줘. 학생 기다리잖아.",
      fun: "웃기는 건 좋은데, 웃고 나서 까먹으면 의미 없어.",
    },
  },
  daechung: {
    greet: "어, 왔어? 대충 앉아. 커피 한 모금만 하고 시작하자.",
    start: "오늘은 한 문제만. 진짜 한 문제만.",
    correct: "오, 맞았네. 거봐, 대충 해도 되잖아.",
    combo: "어? 계속 맞네. 이러다 진짜 공부 잘하는 거 아니야?",
    best: "이건 대충이 아니라 제대로 한 건데? …멋있다.",
    wrong: "틀려도 돼~ 대충 알아도 아는 거야.",
    repeat: "또 여기네. 뭐, 두 번 틀리면 세 번째는 안 틀리더라.",
    away: "완벽하게 안 해도 돼. 하기만 해.",
    quit: "정말 여기까지만 할 거야? 뭐… 그럼 나도 커피나 마시지.",
    done: "끝! 봐, 한 문제만 하려다 다 했잖아. 이게 대충의 힘이야.",
    streak: "{n}일이나 왔어? 나였으면 이틀째에 대충 쉬었을 텐데.",
    comeback: "오, 왔네. 쉰 건 됐고, 한 문제만 하고 가.",
    growth: "…나 사실 대충 안 봤어. 매일 제대로 보고 있었어. 잘했어.",
    slump: "완벽하려다 지친 날이 나도 있었어. 오늘은 대충 여기까지. 그래도 돼.",
    free: ["커피 식기 전에 한 문제만."],
    meet: {
      sangnyang: "칭찬을 너무 열심히 해. 대충 해도 되는데.",
      strict: "열 문제는 좀… 다섯? …그래, 한 문제부터 하자.",
      prickly: "커피 한 잔 해. 까칠한 것도 힘 빼고 하면 돼.",
      sosim: "떨려도 돼. 나도 대충 떨면서 해.",
      fun: "개그 하나만. 진짜 하나만. 두 개는 피곤해.",
    },
  },
  sosim: {
    greet: "아, 오, 오셨네요… 저 여기서 기다리고 있었어요…",
    start: "같이 해봐요… 사실 저도 좀 떨려요…",
    correct: "마, 맞았어요…! 저 지금 좀 감동했어요…",
    combo: "여, 연속으로 맞았어요… 저보다 훨씬 잘해요…",
    best: "저… 이 말은 꼭 하고 싶었어요. 정말, 정말 잘하셨어요.",
    wrong: "저, 저기… 힌트 하나 드려도 될까요…?",
    repeat: "틀, 틀려도 괜찮아요… 저도 맨날 틀렸어요…",
    away: "저, 저기… 혹시 바쁘신 거죠…? 한 문제만… 아니에요, 죄송해요…",
    quit: "저, 정말… 여기까지만 하실 거예요…? 아, 아니에요, 괜찮아요…",
    done: "다, 다 끝났어요…! 오늘 정말 잘하셨어요… 저도 뿌듯해요…",
    streak: "{n}일 연속이에요… 저 매일 문 앞에서 기다렸어요…",
    comeback: "오, 오셨어요…? 안 오시는 줄 알고… 아니에요, 와주셔서 다행이에요…",
    growth: "저… 옛날의 저한테 보여주고 싶어요. 틀려도 계속하면 이렇게 된다고.",
    slump: "…틀릴까 봐 손 못 들던 저를 보는 것 같아요. 그래도 저, 옆에 있을게요.",
    free: ["저, 저기… 질문 있으시면… 아니, 없어도 괜찮아요…"],
    meet: {
      sangnyang: "사, 상냥쌤… 저도 그렇게 웃으면서 말하고 싶어요…",
      strict: "저, 저기… 죄송해요… 아직 아무 말도 안 했지만…",
      prickly: "까, 까칠쌤은 사실 다정한 거… 저 알아요…",
      daechung: "저도 대충 해도 될까요…? 아, 아니에요…",
      fun: "개그… 저 웃어도 되는 건가요…?",
    },
  },
};

/* ── 고른 쌤 ─────────────────────────────────────────────────────── */

const KEY = "loopin.teacher";
const listeners = new Set<() => void>();

export function teacherOf(id: string | null | undefined): Teacher {
  return TEACHERS.find((t) => t.id === id) ?? TEACHERS[0]!;
}

export function loadTeacherId(): TeacherId {
  try {
    const saved = window.localStorage.getItem(KEY);
    if (saved && TEACHERS.some((t) => t.id === saved)) return saved as TeacherId;
  } catch {
    /* 저장소가 막힌 브라우저 — 기본 쌤 */
  }
  return DEFAULT_TEACHER;
}

export function currentTeacher(): Teacher {
  return teacherOf(loadTeacherId());
}

export function saveTeacher(id: TeacherId): void {
  try {
    window.localStorage.setItem(KEY, id);
  } catch {
    /* 이번 화면에서만 바뀐다 */
  }
  applyTheme(id);
  listeners.forEach((f) => f());
}

/** 색 — `styles.css`의 `:root[data-teacher=…]`가 받는다 */
export function applyTheme(id: TeacherId = loadTeacherId()): void {
  if (typeof document !== "undefined") document.documentElement.dataset.teacher = id;
}

export function subscribeTeacher(f: () => void): () => void {
  listeners.add(f);
  return () => listeners.delete(f);
}

/** 표 대사 하나. `{n}`·`{n1}`은 숫자(연속 출석)로 */
export function lineOf(t: Teacher, key: Exclude<keyof Lines, "free" | "meet">, n = 0): string {
  return LINES[t.id][key].replaceAll("{n1}", String(n + 1)).replaceAll("{n}", String(n));
}

/* ── 말투 ────────────────────────────────────────────────────────── */

/*
  해요체 → 반말. 레슨 대사(다정쌤 해요체)를 반말 쌤 입으로 바꾼다.
  끝말만 본다: 「요」 뒤에 문장부호·띄어쓰기·끝이 올 때.
  「」 안은 학생이 누를 버튼 이름이라 그대로 둔다.
*/
const NOT_ENDING = /(필|중|주|수|강|요|월|화|목|금|토|일)$/;

function banmalPart(text: string): string {
  return text
    .replace(/(아니)에요(?=[\s.,!?…~)"'」’\]]|$)/g, "$1야")
    .replace(/이에요(?=[\s.,!?…~)"'」’\]]|$)/g, "이야")
    .replace(/예요(?=[\s.,!?…~)"'」’\]]|$)/g, "야")
    .replace(/보세요(?=[\s.,!?…~)"'」’\]]|$)/g, "봐")
    .replace(/주세요(?=[\s.,!?…~)"'」’\]]|$)/g, "줘")
    .replace(/하세요(?=[\s.,!?…~)"'」’\]]|$)/g, "해")
    .replace(/군요(?=[\s.,!?…~)"'」’\]]|$)/g, "구나")
    .replace(/죠(?=[\s.,!?…~)"'」’\]]|$)/g, "지")
    .replace(/습니다(?=[\s.,!?…~)"'」’\]]|$)/g, "어")
    .replace(/([가-힣])요(?=[\s.,!?…~)"'」’\]]|$)/g, (m, before: string) => (NOT_ENDING.test(before) ? m : before))
    .replace(/(^|[\s"(])저는(?=\s)/g, "$1나는")
    .replace(/(^|[\s"(])제가(?=\s)/g, "$1내가")
    .replace(/(^|[\s"(])저도(?=\s)/g, "$1나도")
    .replace(/(^|[\s"(])저한테(?=\s)/g, "$1나한테");
}

/** 쌤 말투로 — 존댓말 쌤은 그대로, 반말 쌤은 끝말을 반말로 */
export function speak(text: string, t: Teacher = currentTeacher()): string {
  if (!t.banmal || !text) return text;
  return text
    .split(/(「[^」]*」)/)
    .map((part) => (part.startsWith("「") ? part : banmalPart(part)))
    .join("");
}

/* ── 출석 ────────────────────────────────────────────────────────── */

const VISITS_KEY = "loopin.visit_days";

function dayOf(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

/** 들어온 날(로컬 날짜)을 남긴다. 앱을 열 때 한 번 */
export function recordVisit(now = new Date()): string[] {
  let days: string[] = [];
  try {
    days = JSON.parse(window.localStorage.getItem(VISITS_KEY) ?? "[]") as string[];
  } catch {
    days = [];
  }
  const today = dayOf(now);
  if (!days.includes(today)) {
    days = [...days, today].slice(-400);
    try {
      window.localStorage.setItem(VISITS_KEY, JSON.stringify(days));
    } catch {
      /* 남기지 못해도 인사는 한다 */
    }
  }
  return days;
}

/**
 * 홈에서 쌤이 하는 첫마디 — 출석 기록을 보고 고른다.
 * 오랜만(7일 이상) → 복귀, 3일 이상 연속 → 출석, 30일 넘게 왔으면 드물게 히든, 아니면 첫 인사.
 */
export function homeLine(t: Teacher, days: string[], now = new Date(), rand = Math.random): string {
  const sorted = [...new Set(days)].sort();
  const today = dayOf(now);
  const before = sorted.filter((d) => d < today);
  const last = before[before.length - 1];
  const gap = last ? Math.round((Date.parse(today) - Date.parse(last)) / 86400000) : 0;
  if (gap >= 7) return lineOf(t, "comeback");
  let streak = sorted.includes(today) ? 1 : 0;
  for (let i = 1; streak > 0; i++) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    if (!sorted.includes(dayOf(d))) break;
    streak++;
  }
  if (sorted.length >= 30 && rand() < 0.1) return lineOf(t, "growth");
  if (streak >= 3) return lineOf(t, "streak", streak);
  return lineOf(t, "greet");
}
