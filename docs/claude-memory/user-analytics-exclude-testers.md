---
name: user-analytics-exclude-testers
description: "사용자 패턴 분석 때 만드는 사람(헌석·수정) 기록 빼는 법 — 테스터 표시·이름·IP, 2026-10-20부터만 셈"
metadata:
  node_type: memory
  type: project
  originSessionId: 274070ea-439c-4ed3-8c07-17615b00fc57
  modified: 2026-10-22T03:03:40.883Z
---

Supabase loopin-b2c(`npx supabase db query --linked`, 읽기만) 사용자 분석 규칙 (2026-10-21 선생님):

- **2026-10-20(KST)부터 가입한 사용자만 센다.** 9월 기록은 데모 공개 전 — 거의 전부 만드는 사람 테스트.
- 빼는 것: `learner_state` key `loopin.tester`가 있는 학습자(`?tester=이름`, 2026-10-21 배포 후), 온보딩 이름(`dajung.learner_name`) 헌석·수정·서희·예린·정엽(팀원, 2026-10-22),
  이메일 hhs4648@gmail.com(하헌석)·ksooj1203@gmail.com(김수정), 개발 PC IP 59.15.x, 수정 IP 58.151.32.5·118.235.69.49,
  HeadlessChrome·curl·미국 AWS(54.183.149.156·13.57.148.235)·Google(172.253.x).
- 개발 서버·127.0.0.1·자동 브라우저는 2026-10-21부터 아예 기록 안 남음(`records.ts` isTestBrowser, `?record=1`로만 켬).
- 헌석 Mac·iPhone IP는 아직 모름 — 211.206.151.167(Mac)·118.235.68.24(iPhone)가 의심. 휴대폰 데이터 IP는 바뀌므로 테스터 표시를 우선.

**Why:** 157명 중 136명이 테스트였고, 남은 "5명"도 선생님은 그렇게 많이 썼을 리 없다고 함 — 숫자를 부풀리지 말 것.
**How to apply:** 분석 결과를 낼 때 위 기준을 적용하고, 확신 없는 사람은 "불확실"로 따로 적는다. [[product-loopin-b2c]]
