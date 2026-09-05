/// <reference types="vite/client" />

interface ImportMetaEnv {
  /**
   * **개발 전용** Anthropic API 키. `VITE_`로 시작하는 값은 브라우저 번들에
   * 그대로 실리므로, 이 상태로 배포하면 키가 공개된다. 배포 전에는 프록시
   * 서버로 옮긴다. 비워 두면 앱은 지금처럼 코드만으로 돈다.
   */
  readonly VITE_ANTHROPIC_API_KEY?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
