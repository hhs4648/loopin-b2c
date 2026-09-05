import type { TutorLlm } from "./llm";

/**
 * 키 없이 **D·B 자리를 눈으로 확인**하려고 두는 가짜 어댑터. 개발에서만 꽂힌다
 * (`src/main.tsx`, `?fakellm=` 쿼리). 배포 빌드에는 꽂히는 코드가 없다.
 *
 * | 모드 | 무엇을 보나 |
 * |------|-------------|
 * | `normal` | D 처치가 힌트 대신 모델 발화로 나가는지 |
 * | `leak` | 모범 해석·정답 키를 흘리면 **버려지고 힌트로 폴백**하는지 |
 * | `bad` | 문장 5개·질문 2개·반말이 걸러지는지 |
 *
 * 진짜 어댑터를 붙일 때는 이 파일을 지우지 말고 옆에 두면 된다 — 가드레일이
 * 살아 있는지 회귀 확인하는 가장 싼 방법이다.
 */
export type FakeMode = "normal" | "leak" | "bad";

export function createFakeTutorLlm(mode: FakeMode): TutorLlm {
  return {
    async judge({ studentText, unit }) {
      /*
        진짜 콜 1을 흉내만 낸다. 채점 포인트의 한국어 조각이 학생 답에 들어 있으면
        그 항목을 체크로 본다. **판정은 여기서 끝이 아니다** — 전부 체크됐는지,
        그래서 다음 문장으로 갈지는 엔진이 정한다.
      */
      const checkedPoints = unit.scoringPoints.flatMap((point, index) => {
        const tail = point.split("→").pop() ?? "";
        const word = tail.replace(/[^가-힣]/g, "").slice(0, 3);
        return word.length >= 2 && studentText.includes(word) ? [index + 1] : [];
      });
      return { checkedPoints, confidence: 0.5 };
    },

    async speak({ action, unit, askedWord }) {
      if (mode === "leak") {
        // 일부러 정답 키를 흘린다 — 가드레일이 잡아야 정상
        return {
          message: `이 문장은 ${unit.scoringPoints[0] ?? "정답"} 이렇게 보면 돼요.`,
        };
      }
      if (mode === "bad") {
        // 문장 5개 + 질문 2개 + 반말 — 셋 다 걸려야 정상
        return {
          message:
            "자 보자. 여기 동사가 뭐야? 그리고 앞에 있는 건 뭘까? 한번 봐. 다시 해봐.",
        };
      }
      if (action === "ANSWER_WORD") {
        return {
          message: `${askedWord}는 이 문장에서 그렇게 중요한 단어는 아니에요. 뜻만 알고 넘어가도 돼요.`,
        };
      }
      if (action === "TREAT_PARTIAL") {
        return {
          message:
            "앞부분은 잘 잡았어요. 뒤쪽 동사 하나만 다시 보고 적어 볼까요?",
          buttons: [],
        };
      }
      return {
        message: "지금 막힌 곳은 문장 뒷부분이에요. 그 부분만 다시 볼까요?",
        buttons: [],
      };
    },
  };
}
