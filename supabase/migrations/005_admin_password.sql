-- 운영 콘솔은 비밀번호로만 연다. 평문은 두지 않고 bcrypt 로만 비교한다.
-- 예전 함수(Google 계정 확인)는 인자 모양이 달라 지우고 같은 이름으로 다시 만든다.

drop function if exists public.admin_journeys();

create or replace function public.admin_journeys(p_pass text)
returns setof public.journey
language plpgsql
stable
security definer
set search_path = ''
as $$
declare
  hash text := '$2a$08$Oskjsi.1B7afE2mCk0BEJ.gnmtJmLbvlkA3qOyByxAs09eF6COgXW';
begin
  if p_pass is null or extensions.crypt(p_pass, hash) is distinct from hash then
    raise exception 'not admin' using errcode = '42501';
  end if;
  return query
    select * from public.journey
    order by last_seen desc
    limit 2000;
end;
$$;

revoke all on function public.admin_journeys(text) from public, anon, authenticated;
grant execute on function public.admin_journeys(text) to anon, authenticated;
