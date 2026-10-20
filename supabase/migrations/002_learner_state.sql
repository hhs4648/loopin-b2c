-- ---------------------------------------------------------------------------
-- 학생이 손에 들고 다니는 것 — 진행 기록 · 내 노트 · 단어장.
--
-- 지금까지는 브라우저(localStorage)에만 있었다. 무료 공개를 앞두고 서버에도
-- 같은 값을 둔다: 브라우저 저장소가 비워져도(사파리 7일 규칙, 캐시 삭제)
-- 다음에 열면 돌아오고, 나중에 계정을 붙이면 기기를 바꿔도 따라온다.
--
-- **localStorage 키 하나 = 행 하나.** 값은 브라우저에 있던 JSON 그대로다
-- (`src/tutor/cloud.ts`가 어느 키를 어떻게 합치는지 안다). 서버는 모양을
-- 모른다 — 앱이 바뀌어도 마이그레이션이 필요 없게 하려고.
-- ---------------------------------------------------------------------------

create table if not exists public.learner_state (
  learner_id uuid not null references auth.users (id) on delete cascade,
  -- 'dajung.runs' · 'loopin.notes.v1' 같은 localStorage 키
  key text not null,
  value jsonb not null,
  updated_at timestamptz not null default now(),
  primary key (learner_id, key)
);

alter table public.learner_state enable row level security;

drop policy if exists learner_state_own on public.learner_state;
create policy learner_state_own on public.learner_state
  for all using (learner_id = auth.uid()) with check (learner_id = auth.uid());
