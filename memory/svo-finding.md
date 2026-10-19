---
name: svo-finding
description: 모든 문장은 읽기 직후 S·V + 있으면 O·C를 덩어리째 찾고(전목은 메인 목적어 역할일 때만), 핵심어로 요약
metadata:
  type: feedback
---

2026-10-13 39번 주어진 문장에서 사용자가 정한 방식:
1. 읽기 끝나면 바로 주어(S)·동사(V)·목적어(O, 있으면) 찾기 — 문장에서 **덩어리째** 누른다(`pick` + `shade` + `roles`). 대시(—) 뒤도 새 문장이면 두 쌍을 한꺼번에.
2. 맞힌 덩어리 위에 S·V·O 표시가 떠서 그 문장이 끝날 때까지 남는다.
3. 예상 오답은 이유를 따로(`wrong_by`): 전치사가 붙은 덩어리(for most outsiders)는 주어가 될 수 없다, which 덩어리 안의 주어·동사는 문장 전체의 것이 아니다.
4. 이어서 「수능 문장은 주어·동사(목적어) 위주로 빠르게 읽으면 좋아요」 → S·V·O만으로 간단히 자유 해석(`translate`).

**2026-10-13 추가 (39번 문장 1~6):**
- 모든 문장에 쓴다(긴 문장만이 아니라). and 뒤 주어 없는 동사 = 동사 여러 개, there are 뒤 명사 = 주어.
- 보어(C)·목적어(O)가 있으면 S·V와 같이 찾는다. needs to become a member → O는 to부정사 덩어리 전체(문법적으로 정확하게).
- 「전목」(전치사의 목적어)은 **문장 전체의 메인 목적어 역할일 때만** 찾게 한다 — 예: learns **from experts**, is socialized **into the common practices**(동사에 딸린 것). with tests, of a candidate's abilities, In the premodern era처럼 꾸미는 전치사구 안의 명사는 찾게 하지 않는다(2026-10-14 사용자 정정: "이건 다 빼야 해").
- 요약할 때 노란 핵심어(「보고 쓸 부분」)에는 **찾은 동사·보어·목적어를 기본으로 넣는다** (2026-10-14: may still be, present가 빠졌다는 지적). 숙어(on the whole 등)는 Tip으로 한 덩어리 뜻을 알려 준다.
- 그다음 핵심어(노란 표시)만 보고 "직역 말고 어떤 상황인지 간단히 요약"(자유 응답, 요약 예시). 짧은 문장은 요약 대신 핵심어 짚기 + 상황 그림.

**Why:** 학생들이 긴 문장에서 주어를 못 찾는 게 가장 큰 어려움. 「주어 찾기 헷갈려요」 버튼은 지웠다.

**How to apply:** 주어가 숨은 긴 문장(전치사구·to부정사·관계절이 앞에 오는 문장)마다 이 순서를 쓴다. [[main-clause-never-faded]] [[dash-rules]]


**긴 문장·꾸밈 구조 (2026-10-16 선생님, 공통):** 20단어 넘는 문장은 고·중·초 모두 S·V를 다 찾는다(초급 번갈아 내기 X). S·V를 꾸미는 덩어리(관계사 생략·분사구·관계절)가 있으면 찾기 다음에 꾸밈 구조 표(S / ↖ 꾸밈 / V, 꾸밈은 초록 highlight_alt), 말은 한 줄. 예: 3월 38번 the gestures ← (that) hearing people produce while they are speaking.

**5형식은 보어까지 (2026-10-16 선생님):** S V O C 문장(enable/allow/make/help O to-V 등)은 SVO에서 멈추지 말고 C까지 찾는다(덩어리째). 예: 3월 38번 enables speakers to conceptualize and formulate → C.

**that 명사절 (2026-10-16 선생님, 공통):** 접속사가 이끄는 완전한 절(명사절·동격절·in that·if/whether)이고 그 안 내용이 핵심이면, 메인 S·V 다음 그 안의 S·V(+O/C)를 한 번 더 찾는다. beginner.py add_that_sv. 적용: 3월 21 문장3, 36 (C), 38 주어진 문장·①, 6월 34 문장2.

**2026-10-18 (24번 문장 5 피드백 「두번째 동사는 neither does 아니야?」):** 도치(neither/nor/never + 조동사 + 주어 + 동사)는 부정어(neither)와 조동사(does)를 따로 후보로 — 조동사 does와 본동사 stop을 둘 다 V, neither는 오답(부정어), 주어 it은 사이에. 앞 절의 does not stop처럼 조동사도 동사에 넣는다. 같은 낱말이 두 번 나오면 화면이 이미 잡힌 자리를 건너뛰고 다음 자리에 칸을 단다(SentenceStudy placeWords).
