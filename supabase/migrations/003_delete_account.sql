-- ---------------------------------------------------------------------------
-- 회원 탈퇴 — 학생이 앱에서 직접 자기 계정을 지운다.
--
-- 브라우저에는 service_role 키를 둘 수 없으므로 `security definer` 함수로 연다.
-- 지우는 대상은 **부른 사람 자신(auth.uid())뿐**이다 — 인자를 받지 않는다.
--
-- auth.users 한 행만 지우면 나머지는 외래키가 따라 지운다:
--   sessions · point_attempts · learner_state  → on delete cascade
--   llm_calls                                  → session 쪽 cascade, learner_id는 set null
--   auth.identities(카카오·Google·Apple 연결)   → Supabase 기본 cascade
-- ---------------------------------------------------------------------------

create or replace function public.delete_my_account()
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  me uuid := auth.uid();
begin
  if me is null then
    raise exception 'not signed in' using errcode = '28000';
  end if;
  delete from auth.users where id = me;
end;
$$;

revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;
