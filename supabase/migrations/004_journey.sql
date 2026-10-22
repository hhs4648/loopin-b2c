-- ---------------------------------------------------------------------------
-- 어디서 들어왔고, 어디서 멈췄는지.
--
-- 학생 앱은 자기 행만 고친다 (`touch_journey`). 이름·이메일·해석은 넣지 않는다.
-- 관리자 화면(`/admin`)만 전체를 읽는다 (`admin_journeys`).
-- 회원 탈퇴(`delete_my_account`)는 auth.users 를 지우므로 이 행도 따라 지워진다.
-- ---------------------------------------------------------------------------

create table if not exists public.admin_emails (
  email text primary key
);

insert into public.admin_emails (email) values
  ('hhs4648@gmail.com'),
  ('ksooj1203@gmail.com')
on conflict do nothing;

alter table public.admin_emails enable row level security;
revoke all on table public.admin_emails from public, anon, authenticated;

create table if not exists public.journey (
  learner_id uuid primary key references auth.users (id) on delete cascade,
  -- insta · orbi · kakao · friend · play · direct · other. 처음 들어온 경로만 유지
  src text not null default 'direct',
  -- 로그인 버튼만 누르고 나갔는지. guest · kakao · google · apple
  login_tap text,
  -- 실제로 들어온 방법. 소셜이 손님보다 이긴다
  account text,
  learner_group text,
  grade int,
  -- name · intro · group · grade · order · done. 더 앞선 단계만 덮어쓴다
  onboard_step text,
  -- new · returning · link
  kind text,
  example_started boolean not null default false,
  example_place text,
  example_index int not null default 0,
  example_total int not null default 0,
  example_done boolean not null default false,
  visit_days int not null default 1,
  last_visit_day date not null default (timezone('Asia/Seoul', now()))::date,
  tester text,
  first_seen timestamptz not null default now(),
  last_seen timestamptz not null default now()
);

create index if not exists journey_last_seen_idx on public.journey (last_seen desc);

alter table public.journey enable row level security;
revoke all on table public.journey from public, anon, authenticated;

create or replace function public.is_admin()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.admin_emails
    where lower(email) = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;

revoke all on function public.is_admin() from public, anon, authenticated;
grant execute on function public.is_admin() to authenticated;

create or replace function public.onboard_rank(step text)
returns int
language sql
immutable
as $$
  select case step
    when 'name' then 1
    when 'intro' then 2
    when 'group' then 3
    when 'grade' then 4
    when 'order' then 5
    when 'done' then 6
    else 0
  end;
$$;

revoke all on function public.onboard_rank(text) from public, anon, authenticated;

create or replace function public.touch_journey(patch jsonb)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  me uuid := auth.uid();
  today date := (timezone('Asia/Seoul', now()))::date;
  cur public.journey%rowtype;
  v_src text;
  v_tap text;
  v_account text;
  v_group text;
  v_grade int;
  v_onboard text;
  v_kind text;
  v_place text;
  v_tester text;
  v_index int;
  v_total int;
  v_started boolean;
  v_done boolean;
begin
  if me is null then
    raise exception 'not signed in' using errcode = '28000';
  end if;

  v_src := case lower(trim(coalesce(patch->>'src', '')))
    when 'insta' then 'insta' when 'instagram' then 'insta' when 'ig' then 'insta'
    when 'orbi' then 'orbi'
    when 'kakao' then 'kakao' when 'kakaotalk' then 'kakao'
    when 'friend' then 'friend'
    when 'play' then 'play' when 'playstore' then 'play'
    when 'direct' then 'direct'
    when '' then null
    else 'other'
  end;
  v_tap := case patch->>'login_tap'
    when 'guest' then 'guest' when 'kakao' then 'kakao' when 'google' then 'google' when 'apple' then 'apple'
    else null
  end;
  v_account := case patch->>'account'
    when 'guest' then 'guest' when 'kakao' then 'kakao' when 'google' then 'google' when 'apple' then 'apple'
    else null
  end;
  v_group := case patch->>'learner_group'
    when 'suneung' then 'suneung' when 'high12' then 'high12' when 'middle' then 'middle' when 'adult' then 'adult'
    else null
  end;
  v_onboard := case patch->>'onboard_step'
    when 'name' then 'name' when 'intro' then 'intro' when 'group' then 'group'
    when 'grade' then 'grade' when 'order' then 'order' when 'done' then 'done'
    else null
  end;
  v_kind := case patch->>'kind' when 'new' then 'new' when 'returning' then 'returning' when 'link' then 'link' else null end;
  v_place := nullif(left(regexp_replace(trim(coalesce(patch->>'example_place', '')), '[[:cntrl:]]', '', 'g'), 40), '');
  v_tester := case when coalesce(patch->>'tester', '') ~ '^[가-힣a-zA-Z0-9_-]{1,20}$' then patch->>'tester' else null end;
  v_grade := case
    when coalesce(patch->>'grade', '') ~ '^[0-9]+$' then least(9, greatest(1, (patch->>'grade')::int))
    else null
  end;
  v_index := case when coalesce(patch->>'example_index', '') ~ '^[0-9]+$' then least(99, (patch->>'example_index')::int) else null end;
  v_total := case when coalesce(patch->>'example_total', '') ~ '^[0-9]+$' then least(99, (patch->>'example_total')::int) else null end;
  v_started := case patch->>'example_started' when 'true' then true when 'false' then false else null end;
  v_done := case patch->>'example_done' when 'true' then true when 'false' then false else null end;

  select * into cur from public.journey where learner_id = me;
  if not found then
    begin
      insert into public.journey (
        learner_id, src, login_tap, account, learner_group, grade, onboard_step, kind,
        example_started, example_place, example_index, example_total, example_done, tester,
        visit_days, last_visit_day
      ) values (
        me,
        coalesce(v_src, 'direct'),
        v_tap,
        v_account,
        v_group,
        v_grade,
        v_onboard,
        v_kind,
        coalesce(v_started, false),
        case when v_done then '끝' else v_place end,
        coalesce(v_index, 0),
        coalesce(v_total, 0),
        coalesce(v_done, false),
        v_tester,
        1,
        today
      );
      return;
    exception when unique_violation then
      select * into cur from public.journey where learner_id = me;
    end;
  end if;

  update public.journey set
    login_tap = coalesce(cur.login_tap, v_tap),
    account = case
      when v_account in ('kakao', 'google', 'apple') then v_account
      when cur.account is null then coalesce(v_account, cur.account)
      else cur.account
    end,
    learner_group = coalesce(cur.learner_group, v_group),
    grade = coalesce(cur.grade, v_grade),
    onboard_step = case
      when public.onboard_rank(v_onboard) > public.onboard_rank(cur.onboard_step) then v_onboard
      else cur.onboard_step
    end,
    kind = coalesce(cur.kind, v_kind),
    example_started = cur.example_started or coalesce(v_started, false),
    example_place = case
      when cur.example_done or coalesce(v_done, false) then '끝'
      when v_index is not null and v_index >= cur.example_index then coalesce(v_place, cur.example_place)
      else cur.example_place
    end,
    example_index = greatest(cur.example_index, coalesce(v_index, 0)),
    example_total = greatest(cur.example_total, coalesce(v_total, 0)),
    example_done = cur.example_done or coalesce(v_done, false),
    visit_days = cur.visit_days + case when cur.last_visit_day < today then 1 else 0 end,
    last_visit_day = greatest(cur.last_visit_day, today),
    tester = coalesce(cur.tester, v_tester),
    last_seen = now()
  where learner_id = me;
end;
$$;

revoke all on function public.touch_journey(jsonb) from public, anon, authenticated;
grant execute on function public.touch_journey(jsonb) to authenticated;

create or replace function public.admin_journeys()
returns setof public.journey
language plpgsql
stable
security definer
set search_path = ''
as $$
begin
  if not public.is_admin() then
    raise exception 'not admin' using errcode = '42501';
  end if;
  return query
    select * from public.journey
    order by last_seen desc
    limit 2000;
end;
$$;

revoke all on function public.admin_journeys() from public, anon, authenticated;
grant execute on function public.admin_journeys() to authenticated;
