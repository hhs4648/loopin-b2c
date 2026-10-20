---
name: slash-reading-toggle
description: "끊어읽기 버튼 — 전체 규칙(2026-10-20 확정). 더 잘게, 켜면 S·V·O·C + [ ] 수식어. 관계대명사절 안 S·V는 안 침, there is는 be동사만 V. 2024-03 23개·2026-03 36번·2022-03 29번 모두 적용됨"
metadata:
  node_type: memory
  type: project
  originSessionId: f4cf0afa-03f4-4f2b-b5ef-960e6f14a2a3
  modified: 2026-10-19T19:29:42.725Z
---

2026-10-16 선생님: 학생들은 끊어읽기 법 자체를 모르니 보조도구로. 문장 필드 `slashes`(이 말 뒤에 /), 「/ 끊어읽기」 버튼, 기본 꺼짐·문장 바뀌면 꺼짐, / 양옆은 아주 좁은 간격(hair space).

**2026-10-20 선생님이 전체 규칙으로 못 박음 → 같은 날 2024-03 23개·2026-03 36번에 다 넣음(커밋은 선생님 몫)**:
- **더 잘게** 끊는다 — 구두점 뒤 · 긴 주어 뒤(짧은 주어 2~3단어는 동사와 안 끊음, 꾸밈말 달린 주어는 꾸밈말 앞) · 접속사·관계사·that절 앞 · be동사 뒤 보어절 앞 · 뒤 전치사구·to부정사 앞, 대략 4~8단어. of-구는 4~5단어 넘으면 끊음, 나열은 2~3개씩 묶음, 7단어 이하 짧은 문장은 안 끊음. **S·V 덩어리 안에도 끊는 자리를 둘 수 있다**(화면이 / 를 건너뛰고 찾음) — 끊는 자리를 빼면 읽기 어렵다(선생님)
- 켜면 문장 필드 `roles`(`{text, role: S|V|O|C}`)가 단어 위에 **같이 보인다** — 메인 문장 S·V·O·C + because·if·when 같은 **부사절 안의 S·V**, 모두 같은 진하기, 찾기 전에도.
  **관계대명사절(who·which·that·whose·in which·접촉절)·분사 수식어 안의 S·V는 안 친다** → 대신 문장 필드 `modifiers`로 적어 켜면 **[ ]로 묶어** 수식어라는 것만 보인다
- 명사절(what/how/whether) 주어·목적어는 **통째로 S/O** (determines for us [how much of what we have should be given away]=O). that절 목적어는 안의 S·V만(기존 that_sv 스텝과 같게)
- **there is/was는 be동사만 V**, there는 표시 안 함 (31번 초급 sv 스텝도 "is"로)
- 같은 낱말이 같은 역할로 여러 번이면 「we … we」로 차례로(차지한 자리는 건너뜀); 다른 역할로 또 나오면 앞쪽을 더 긴 덩어리로 먼저 잡는다
- sv 스텝의 roles 텍스트와 문장 roles 텍스트는 똑같이(다르면 표시가 둘 붙는다)

**How to apply:** 생성기에 `slashes` + `roles`(exam_kit `r()`) + `modifiers`. 화면 placeWords는 / 와 [ ] 를 건너뛰어 찾는다(SentenceStudy wordRe). 검사: exam_kit check·policy.test.ts(문장에 그대로 있나). 2024-03 작업 메모·애매한 자리 목록은 side-session-notes/…/slash-roles-2024-03.md. [[svo-finding]] [[trap-words-to-tips]]

**저절로 켜기 (2026-10-20 선생님):** 주어·동사·목적어 찾기와 관련된 설명 화면은 학생이 안 눌렀어도 끊어읽기를 켠다. 엔진: show 스텝 말에 「주어」·「목적어」가 있고 문장에 roles가 있으면 자동(slashAuto), 아니면 스텝에 `slash_on: true`. 고르는 화면(choice·pick)은 답이 보이니 안 켠다. 2026-10-20 기준 8개 레슨 15개 화면이 자동으로 켜짐.
**O 안에 꾸밈이 든 경우:** 목적어는 꾸밈까지 길게 한 덩어리 O(music in which … song), 꾸밈은 modifiers로 [ ]. 화면 wordRe가 [ ]도 건너뛰어 찾는다. 29번 문장 3(who 절)·5(in which 절)를 이 규칙대로 고침 — 처음 29번 만들 때 관계사절 S·V를 쳤던 실수.
