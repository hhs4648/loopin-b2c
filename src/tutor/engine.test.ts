import { afterEach, describe, expect, it } from "vitest";
import type { Lesson } from "../../content/tutor/types";
import { createSession, READY_BTN } from "./engine";
import { getLesson } from "./lessons";
import { setTutorLlm, type TutorLlm } from "./llm";

/**
 * 엔진 회귀 테스트.
 *
 * 여기 있는 것은 전부 `docs/tutor/TEST_SCENARIOS.md`에서 **코드만으로 확인할 수
 * 있는 항목**이다. 예상 밖(D) 대응처럼 모델이 있어야 하는 항목은 가짜 어댑터로만
 * 확인한다.
 */

const RESIGNATION = getLesson();
const THALES = getLesson("thales-participial-phrase-front");

/** 퇴사 편지 7문장의 정답 예시 (레슨의 `demo_match.p1`을 만족한다) */
const CORRECT = [
  "지난 4년간 이 회사에서 근무한 것은 큰 영광이었습니다",
  "제가 얻은 경험은 정말 소중했습니다",
  "다른 회사의 자리를 수락하고 떠나게 되었습니다",
  "쉬운 결정은 아니었지만 확신합니다",
  "마지막 근무일은 4월 30일입니다",
  "업무 인수인계를 위해 최선을 다하겠습니다",
  "당신과 회사 모두에게 행운이 있기를 바랍니다",
];

/** 인트로를 지나 첫 문장까지 온 세션 */
async function startedSession(lessonId?: string) {
  const session = createSession(lessonId);
  await session.submit(READY_BTN);
  return session;
}

async function say(
  session: Awaited<ReturnType<typeof startedSession>>,
  ...inputs: string[]
) {
  let view = session.view();
  for (const input of inputs) view = await session.submit(input);
  return view;
}

function hint(lesson: Lesson, unit: number, rung: 1 | 2 | 3): string {
  const found = lesson.chunks[unit]!.hint_ladder?.find((h) => h.rung === rung);
  if (!found) throw new Error(`문장 ${unit + 1}에 힌트 ${rung}단이 없다`);
  return found.message;
}

afterEach(() => setTutorLlm(null));

describe("인트로", () => {
  it("레슨에서 만든다 — 지문을 바꾸면 인트로도 바뀐다", () => {
    expect(createSession().view().message).toContain(RESIGNATION.topic_intro);
    expect(createSession(THALES.id).view().message).toContain(THALES.topic_intro);
  });

  it("고유명사를 미리 보여 준다 — 해석 과제가 아니다", () => {
    const view = createSession().view();
    expect(view.properNouns.map((n) => n.en)).toContain("Lewis Ltd.");
  });
});

describe("진단", () => {
  it("정답(A)이면 칭찬하고 다음 문장으로 간다", async () => {
    const session = await startedSession();
    const view = await say(session, CORRECT[0]!);
    expect(view.message).toContain(RESIGNATION.chunks[0]!.praise);
    expect(view.progressIndex).toBe(2);
  });

  it("예상 오류(C)는 레슨의 고정 대사와 선택지를 그대로 쓴다", async () => {
    const session = await startedSession();
    const view = await say(session, "지난 4년간 이 회사에서 봉사한 것은 영광이었습니다");
    const p2 = RESIGNATION.chunks[0]!.expected_errors!.find((e) => e.id === "P2")!;
    expect(view.message).toBe(p2.treatment!.message);
    for (const choice of p2.treatment!.choices!) {
      expect(view.buttons).toContain(choice.label);
    }
    expect(view.progressIndex).toBe(1);
  });

  it("정답 키워드가 섞여 있어도 예상 오류가 먼저다", async () => {
    // "밀레투스가 소아시아에서 태어났다" — 주어 오인(E2)이 먼저 (TEST_SCENARIOS #1)
    const session = await startedSession(THALES.id);
    const view = await say(session, "밀레투스가 소아시아에서 태어났다");
    const chunk = THALES.chunks[0]!;
    const first = chunk.error_priority!.find((id) =>
      chunk.expected_errors!.some((e) => e.id === id && e.signals?.some((s) => "밀레투스가 소아시아에서 태어났다".includes(s))),
    );
    expect(first).toBe("E2");
    expect(view.message).toBe(
      chunk.expected_errors!.find((e) => e.id === "E2")!.treatment!.message,
    );
  });

  it("never_mark_correct 오류는 절대 정답으로 새지 않는다", async () => {
    // 탈레스 E4 — B.C.를 '기원후'로 (TEST_SCENARIOS #12)
    const session = await startedSession(THALES.id);
    await say(session, "소아시아 밀레투스라는 도시에서 태어난");
    const view = await say(session, "그는 기원후 624년부터 546년까지 살았다");
    const e4 = THALES.chunks[1]!.expected_errors!.find((e) => e.id === "E4")!;
    expect(e4.never_mark_correct).toBe(true);
    expect(view.message).toBe(e4.treatment!.message);
    expect(view.ended).toBe(false);
  });

  it("not_signals가 있으면 그 오류로 보지 않는다", async () => {
    // '봉사'가 있어도 '근무'가 같이 있으면 serve 오해가 아니다
    const session = await startedSession();
    const view = await say(session, "봉사 정신으로 이 회사에서 근무한 것은 영광이었습니다");
    expect(view.progressIndex).toBe(2);
  });
});

describe("역질문", () => {
  it("고유명사를 물으면 답하고 하던 자리로 돌아온다", async () => {
    // TEST_SCENARIOS #11
    const session = await startedSession(THALES.id);
    const view = await say(session, "Asia Minor가 뭐예요?");
    expect(view.message).toContain("Asia Minor");
    expect(view.message).toContain("지역명");
    expect(view.progressIndex).toBe(1);
  });

  it("오답으로 세지 않는다 — 힌트 사다리가 그대로다", async () => {
    const session = await startedSession();
    await say(session, "Lewis Ltd.가 뭐예요?");
    // 되묻기가 miss였다면 이 「모르겠어요」는 2단이 나왔을 것이다
    expect((await say(session, "잘 모르겠어요")).message).toBe(hint(RESIGNATION, 0, 1));
  });

  it("2지선다 중에 물어봐도 선택지를 뺏지 않는다", async () => {
    const session = await startedSession();
    const opened = await say(session, "지난 4년간 이 회사에서 봉사한 것은 영광이었습니다");
    const view = await say(session, "Lewis Ltd.가 뭐예요?");
    expect(view.buttons).toEqual(opened.buttons);
    // 아직 그 자리 — 선택지에 답하면 원래 분기로 이어진다
    const after = await say(session, "근무하다");
    expect(after.message).not.toBe(view.message);
  });

  it("해석 시도를 되묻기로 잘못 보지 않는다", async () => {
    const session = await startedSession();
    const view = await say(session, "지난 4년간 이 회사에서 근무한 것은 큰 영광이었습니다");
    expect(view.progressIndex).toBe(2);
  });

  it("종류 이름이 화면과 같은 말을 쓴다", async () => {
    const session = await startedSession();
    const view = await say(session, "Lewis Ltd.가 뭐예요?");
    expect(view.message).toContain("회사 이름");
  });
});

describe("단어 뜻 질문", () => {
  it("가르치는 단어는 뜻을 그냥 주지 않고 사다리로 답한다", async () => {
    // serve는 이 문장의 채점 포인트다 — 뜻이 곧 정답이다
    const session = await startedSession();
    const view = await say(session, "serve가 뭐예요?");
    expect(view.message).toBe(hint(RESIGNATION, 0, 1));
  });

  it("사다리를 썼으므로 다음에는 2단이 나온다", async () => {
    const session = await startedSession();
    await say(session, "serve가 뭐예요?");
    expect((await say(session, "잘 모르겠어요")).message).toBe(hint(RESIGNATION, 0, 2));
  });

  it("가르치지 않는 단어는 모델이 답하고, 오답으로 세지 않는다", async () => {
    const seen: string[] = [];
    setTutorLlm({
      speak: async (input) => {
        seen.push(`${input.action}:${input.askedWord}`);
        return { message: "company는 회사라는 뜻이에요." };
      },
    });
    const session = await startedSession();
    const view = await say(session, "company가 뭐예요?");
    expect(seen).toEqual(["ANSWER_WORD:company"]);
    expect(view.message).toContain("회사라는 뜻");
    // miss를 안 셌으므로 다음 「모르겠어요」는 1단이어야 한다
    expect((await say(session, "잘 모르겠어요")).message).toBe(hint(RESIGNATION, 0, 1));
  });

  it("어댑터가 없으면 사다리로 폴백한다", async () => {
    const session = await startedSession();
    expect((await say(session, "company가 뭐예요?")).message).toBe(hint(RESIGNATION, 0, 1));
  });

  it("모델이 정답을 흘리면 그 발화를 버린다", async () => {
    setTutorLlm({
      speak: async () => ({ message: "serve는 근무하다라는 뜻이에요." }),
    });
    const session = await startedSession();
    expect((await say(session, "company가 뭐예요?")).message).toBe(hint(RESIGNATION, 0, 1));
  });

  it("해석 시도를 단어 질문으로 잘못 보지 않는다", async () => {
    const session = await startedSession();
    const view = await say(session, CORRECT[0]!);
    expect(view.progressIndex).toBe(2);
  });
});

describe("힌트 사다리", () => {
  it("1→2→3단을 순서대로만 오른다", async () => {
    const session = await startedSession();
    expect((await say(session, "잘 모르겠어요")).message).toBe(hint(RESIGNATION, 0, 1));
    expect((await say(session, "잘 모르겠어요")).message).toBe(hint(RESIGNATION, 0, 2));
    expect((await say(session, "잘 모르겠어요")).message).toBe(hint(RESIGNATION, 0, 3));
  });

  it("3단 전에는 모범 해석이 나오지 않는다", async () => {
    const session = await startedSession();
    const answer = RESIGNATION.chunks[0]!.model_translation;
    expect((await say(session, "잘 모르겠어요")).message).not.toContain(answer);
    expect((await say(session, "잘 모르겠어요")).message).not.toContain(answer);
    expect((await say(session, "잘 모르겠어요")).message).toContain(answer);
  });

  it("문장이 바뀌면 사다리가 처음으로 돌아간다", async () => {
    const session = await startedSession();
    await say(session, "잘 모르겠어요", "잘 모르겠어요");
    await say(session, CORRECT[0]!);
    expect((await say(session, "잘 모르겠어요")).message).toBe(hint(RESIGNATION, 1, 1));
  });
});

describe("좌절 방지", () => {
  it("4번째부터는 시도를 강요하지 않고 설명해 준다", async () => {
    const session = await startedSession();
    const view = await say(
      session,
      "잘 모르겠어요",
      "잘 모르겠어요",
      "잘 모르겠어요",
      "잘 모르겠어요",
    );
    expect(view.message).toContain(RESIGNATION.chunks[0]!.model_translation);
    expect(view.buttons.length).toBeGreaterThan(1);
  });

  it("선택지 밖의 답을 해도 다음 문장으로 넘어간다", async () => {
    /*
      회귀: 예전에는 여기서 힌트로 갔다가 miss가 이미 4라 좌절 방지가 다시 열려
      **같은 문장에 영원히 갇혔다.** 시도를 강요하지 않겠다는 장치가 반대로 굴었다.
    */
    const session = await startedSession();
    await say(session, "잘 모르겠어요", "잘 모르겠어요", "잘 모르겠어요", "잘 모르겠어요");
    const view = await say(session, "네");
    expect(view.progressIndex).toBe(2);
  });
});

describe("기록", () => {
  async function finish(prefix: string[]) {
    const session = await startedSession();
    await say(session, ...prefix, ...CORRECT);
    return session.view().recordLine ?? "(기록 없음)";
  }

  it("오류 없이 통과하면 이해", async () => {
    expect(await finish([])).toContain("결과=이해");
  });

  it("스스로 고쳤으면 오류후이해 — 오류 id가 남는다", async () => {
    const record = await finish([
      "지난 4년간 봉사한 것은 영광이었습니다",
      "근무하다",
    ]);
    expect(record).toContain("결과=오류후이해");
    expect(record).toContain("1:P2");
  });

  it("힌트 3단을 봐야 넘어갔으면 취약", async () => {
    const record = await finish(["잘 모르겠어요", "잘 모르겠어요", "잘 모르겠어요"]);
    expect(record).toContain("결과=취약");
    expect(record).toContain("1:HINT3");
  });

  it("좌절 방지가 발동했으면 설명제공", async () => {
    const record = await finish([
      "잘 모르겠어요",
      "잘 모르겠어요",
      "잘 모르겠어요",
      "잘 모르겠어요",
      "네",
    ]);
    expect(record).toContain("결과=설명제공");
  });

  it("유형은 레슨에서 온다", async () => {
    const session = await startedSession(THALES.id);
    await say(session, "소아시아 밀레투스라는 도시에서 태어난", "그는 기원전 624년부터 546년까지 살았다");
    expect(session.view().recordLine).toContain(`유형=${THALES.grammar_type}`);
  });
});

describe("한 턴에 질문 하나", () => {
  /*
    레슨 글은 `lesson-content.test.ts`가 본다. 여기서 보는 건 **엔진이 조립한
    문장** — 프레임 문구 + 레슨 문구를 이어 붙일 때 물음표가 겹치기 쉽다.
  */
  const paths: Record<string, string[]> = {
    정답: [CORRECT[0]!, CORRECT[1]!],
    예상오류: ["지난 4년간 이 회사에서 봉사한 것은 영광이었습니다", "근무하다"],
    힌트: ["잘 모르겠어요", "잘 모르겠어요", "잘 모르겠어요"],
    좌절방지: ["잘 모르겠어요", "잘 모르겠어요", "잘 모르겠어요", "잘 모르겠어요"],
  };

  it.each(Object.entries(paths))("%s 경로", async (_name, inputs) => {
    const session = await startedSession();
    for (const input of inputs) {
      const view = await session.submit(input);
      const questions = (view.message.match(/[?？]/g) ?? []).length;
      expect(questions, view.message).toBeLessThanOrEqual(1);
    }
  });
});

describe("LLM 자리", () => {
  const spoken = "지금 막힌 곳은 문장 뒷부분이에요. 그 부분만 다시 볼까요?";
  const unexpected = "이 문장은 뭔가 특권 같은 느낌인데 잘 안 잡히네요";

  it("어댑터가 없으면 예상 밖 입력도 힌트 사다리로 접힌다", async () => {
    const session = await startedSession();
    expect((await say(session, unexpected)).message).toBe(hint(RESIGNATION, 0, 1));
  });

  it("어댑터가 있으면 D는 모델 발화로 나간다", async () => {
    const llm: TutorLlm = { speak: async () => ({ message: spoken }) };
    setTutorLlm(llm);
    const session = await startedSession();
    expect((await say(session, unexpected)).message).toBe(spoken);
  });

  it("「잘 모르겠어요」(E)는 모델을 부르지 않는다", async () => {
    let called = 0;
    setTutorLlm({
      speak: async () => {
        called += 1;
        return { message: spoken };
      },
    });
    const session = await startedSession();
    expect((await say(session, "잘 모르겠어요")).message).toBe(hint(RESIGNATION, 0, 1));
    expect(called).toBe(0);
  });

  it("가드레일에 걸린 발화는 버리고 힌트로 폴백한다", async () => {
    setTutorLlm({
      speak: async () => ({
        message: `정답은 ${RESIGNATION.chunks[0]!.model_translation}예요.`,
      }),
    });
    const session = await startedSession();
    expect((await say(session, unexpected)).message).toBe(hint(RESIGNATION, 0, 1));
  });

  it("모델이 죽어도 수업은 이어진다", async () => {
    setTutorLlm({
      speak: async () => {
        throw new Error("네트워크 실패");
      },
    });
    const session = await startedSession();
    expect((await say(session, unexpected)).message).toBe(hint(RESIGNATION, 0, 1));
  });

  it("모델은 정답(A)을 뒤집지 못한다 — A는 코드가 정한다", async () => {
    let called = 0;
    setTutorLlm({
      speak: async () => {
        called += 1;
        return { message: spoken };
      },
    });
    const session = await startedSession();
    const view = await say(session, CORRECT[0]!);
    expect(view.progressIndex).toBe(2);
    expect(called).toBe(0);
  });
});
