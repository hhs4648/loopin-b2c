/// <reference types="vite/client" />

interface ImportMetaEnv {
  /**
   * **개발 전용** Anthropic API 키. `VITE_`로 시작하는 값은 브라우저 번들에
   * 그대로 실리므로, 이 상태로 배포하면 키가 공개된다. 배포 전에는 프록시
   * 서버로 옮긴다. 비워 두면 앱은 지금처럼 코드만으로 돈다.
   */
  readonly VITE_ANTHROPIC_API_KEY?: string;
  /** Supabase 프로젝트 URL. 없으면 기록을 남기지 않는다 */
  readonly VITE_SUPABASE_URL?: string;
  /** anon 키 — 공개돼도 되는 값이다. 보호는 RLS가 한다 */
  readonly VITE_SUPABASE_ANON_KEY?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
