/* Play 앱이 이 주소를 앱으로 열게 하는 최소 서비스 워커. 수업 파일은 캐시하지 않는다. */
self.addEventListener("install", (event) => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", () => {});
