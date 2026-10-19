---
name: order-paragraph-view
description: 순서 문제는 「문장 N」 대신 (A)(B)(C)로 표시하고, 단락이 여러 문장이면 단락 전체를 보인다(지금 문장 진하게, 나머지 연하게)
metadata:
  type: project
---

순서 문제 공통 규칙(2026-10-15 선생님): 화면 태그는 (A)·(B)·(C), 단락이 여러 문장이면 다 보여 준다. 구현: lesson `method.type = "order"`면 세션 `paragraphOf`가 (A)로 시작하는 문장부터 다음 단락 전까지 묶어 `view.paragraph`(before/after)로 내보내고, SentenceStudy가 연하게 그린다. 말은 「(A) 단락」, 「(A) 단락의 두 번째 문장」. 안내(paper_order)는 주어진 글 마지막 화면에. docs/tutor/templates/order.md. [[type-templates]]
