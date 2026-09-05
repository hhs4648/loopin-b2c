-- ---------------------------------------------------------------------------
-- Loopin B2C — 학습 기록.
--
-- **haksup과 다른 프로젝트다.** 두 제품이 프로필 한 행을 공유해서 역할이 뒤엉킨
-- 적이 있어서, 여기서는 아예 저장소를 분리한다.
--
-- 레슨 콘텐츠(문장·체크리스트·유도 문구)는 **여기 두지 않는다.** 소스는
-- `content/tutor/lessons/*.json`이다 — 버전 관리되고 리뷰가 되기 때문이다.
-- DB에는 "무슨 일이 일어났는지"만 쌓는다.
-- ---------------------------------------------------------------------------

create extension if not exists pgcrypto;

-- ── 한 수업 ────────────────────────────────────────────────────────────────
create table if not exists public.sessions (
  id uuid primary key default gen_random_uuid(),
  learner_id uuid not null references auth.users (id) on delete cascade,
  lesson_id text not null,
  -- 끝났을 때만 채워진다. 값은 engine.ts의 TutorResult와 같다
  result text check (result in ('이해', '오류후이해', '설명제공', '취약')),
  started_at timestamptz not null default now(),
  ended_at timestamptz
);

create index if not exists sessions_learner_idx
  on public.sessions (learner_id, started_at desc);

-- ── 항목별 기록 — 난이도의 근거 ────────────────────────────────────────────
--
-- `first_try`가 핵심이다. **유도를 받기 전에 스스로 냈는지**만이 난이도를 말해
-- 준다. 유도 후 결과로 재면, 우리가 늘 1번 항목을 먼저 유도하기 때문에 1번이
-- 쉬워 보이는 편향이 생긴다.
create table if not exists public.point_attempts (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.sessions (id) on delete cascade,
  learner_id uuid not null references auth.users (id) on delete cascade,
  lesson_id text not null,
  unit int not null,
  point int not null,
  first_try boolean not null,
  nudged boolean not null,
  told boolean not null,
  -- 좌절 방지로 모범 해석을 본 뒤였나
  revealed boolean not null default false,
  created_at timestamptz not null default now()
);

create index if not exists point_attempts_lesson_idx
  on public.point_attempts (lesson_id, unit, point);

-- ── 모델 호출 로그 ─────────────────────────────────────────────────────────
--
-- 비용·지연·폐기율을 나중에 눈으로 보려고 남긴다. 지금은 브라우저 콘솔에만
-- 찍히고 사라진다. 학생 발화는 넣지 않는다 — 개인정보를 늘릴 이유가 없다.
create table if not exists public.llm_calls (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references public.sessions (id) on delete cascade,
  learner_id uuid references auth.users (id) on delete set null,
  call text not null check (call in ('judge', 'speak')),
  ms int not null,
  input_tokens int not null default 0,
  cached_tokens int not null default 0,
  output_tokens int not null default 0,
  -- 가드레일에 걸려 버려졌으면 그 사유
  dropped_reason text,
  created_at timestamptz not null default now()
);

create index if not exists llm_calls_created_idx
  on public.llm_calls (created_at desc);

-- ── RLS — 자기 기록만 ──────────────────────────────────────────────────────
--
-- 익명 세션도 `authenticated` 롤이다. 익명이라도 남의 기록은 못 본다.
alter table public.sessions enable row level security;
alter table public.point_attempts enable row level security;
alter table public.llm_calls enable row level security;

drop policy if exists sessions_own on public.sessions;
create policy sessions_own on public.sessions
  for all using (learner_id = auth.uid()) with check (learner_id = auth.uid());

drop policy if exists point_attempts_own on public.point_attempts;
create policy point_attempts_own on public.point_attempts
  for all using (learner_id = auth.uid()) with check (learner_id = auth.uid());

drop policy if exists llm_calls_own on public.llm_calls;
create policy llm_calls_own on public.llm_calls
  for all using (learner_id = auth.uid()) with check (learner_id = auth.uid());

-- ── 난이도 집계 ────────────────────────────────────────────────────────────
--
-- 항목별 첫 시도 성공률. 표본이 쌓이면 이 값으로 레슨의 항목 순서(쉬운 순)를
-- 덮어쓸 수 있다. **표본이 적을 때는 작성자가 적은 순서가 이긴다** — 앱에서
-- 임계치를 두고 판단한다.
--
-- 뷰는 RLS를 우회하지 않는다(security_invoker). 집계를 보려면 대시보드에서
-- 본다 — 학생 앱은 이걸 읽지 않는다.
create or replace view public.point_difficulty
with (security_invoker = true) as
  select
    lesson_id,
    unit,
    point,
    count(*)                        as attempts,
    avg(first_try::int)             as first_try_rate,
    avg(told::int)                  as told_rate
  from public.point_attempts
  group by lesson_id, unit, point;
