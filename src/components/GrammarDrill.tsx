import { useState } from "react";
import { getGrammarDrill, isRightInput, type DrillItem } from "../tutor/grammarDrills";
import { recordDrillInput, recordGrammarDrill } from "../tutor/grammarPractice";

type Props = {
  id: string;
  onClose: () => void;
  /** 같은 묶음의 다음 세트 — 끝 화면에 「다음 세트」 버튼 */
  next?: { id: string; title: string };
  onOpen?: (id: string) => void;
};

/**
 * 문법 drill — 보충학습실의 「연습할 문법」에서 연다. 10문제, 처음엔 객관식 → 나중엔 주관식이 섞인다 (자료 순서 그대로).
 * 틀리면 첫마디는 「아쉽게도 틀렸어요.」 + 이유, [다음]으로 넘긴다. 끝나면 점수와 틀린 문제의 정답을 보여 준다.
 */
export function GrammarDrill({ id, onClose, next, onOpen }: Props) {
  const drill = getGrammarDrill(id);
  const [qi, setQi] = useState(0);
  const [marks, setMarks] = useState<boolean[]>([]);
  const [rulesOpen, setRulesOpen] = useState(false);
  /** 시작 전 규칙 카드를 보고 있나 */
  const [ready, setReady] = useState(false);

  if (!drill) {
    return (
      <div className="stage-fill words vtest">
        <p className="words-title">이 문법의 연습 문제가 아직 없어요.</p>
        <div className="words-dock">
          <button type="button" className="read-continue" onClick={onClose}>보충학습실로</button>
        </div>
      </div>
    );
  }

  const items = drill.items;
  const item = items[qi];
  const right = marks.filter(Boolean).length;

  function done(ok: boolean) {
    const all = [...marks, ok];
    setMarks(all);
    setQi(qi + 1);
    if (all.length === items.length) recordGrammarDrill(id, all.filter(Boolean).length, items.length);
  }

  return (
    <div className="stage-fill words vtest gdrill">
      <header className="words-top">
        <span className="words-step">
          {drill.title}{ready && item ? ` · ${qi + 1} / ${items.length}` : ""}
        </span>
        <button type="button" className="close-soft" title="그만하기" aria-label="그만하기" onClick={onClose}>
          ✕
        </button>
      </header>

      {!ready ? (
        <>
          <p className="words-title">시작 전에 규칙부터 짧게 볼게요.</p>
          <RuleCard drill={drill} />
          <div className="words-dock">
            <button type="button" className="read-continue" onClick={() => setReady(true)}>
              시작하기
            </button>
          </div>
        </>
      ) : item ? (
        <>
          <button type="button" className="gdrill-rules-toggle" onClick={() => setRulesOpen(!rulesOpen)}>
            💡 {rulesOpen ? "정리 접기" : "정리 보기"}
          </button>
          {rulesOpen ? <RuleCard drill={drill} /> : null}
          {item.type === "choice" ? (
            <ChoiceItem key={qi} item={item} onDone={done} />
          ) : (
            <InputItem
              key={qi}
              item={item}
              writing={drill.mode === "writing"}
              onTyped={(typed, ok) => recordDrillInput(id, qi, typed, ok)}
              onDone={done}
            />
          )}
        </>
      ) : (
        <>
          <p className="words-title">
            {items.length}문제 중에 {right}개 맞혔어요.
            {right === items.length ? " 다 맞혔어요, 잘했어요!" : " 틀린 문제는 정답을 한 번 더 봐요."}
          </p>
          <ul className="words-list">
            {items.map((it, i) =>
              marks[i] ? null : (
                <li key={i} className="word-row">
                  <span className="word-en">{fill(it.sentence, answerOf(it))}</span>
                </li>
              ),
            )}
          </ul>
          <div className="words-dock">
            {next && onOpen ? (
              <button type="button" className="read-continue" onClick={() => onOpen(next.id)}>
                다음 세트: {next.title}
              </button>
            ) : null}
            {right < items.length ? (
              <button
                type="button"
                className={`read-continue${next ? " second" : ""}`}
                onClick={() => {
                  setMarks([]);
                  setQi(0);
                }}
              >
                처음부터 다시
              </button>
            ) : null}
            <button type="button" className={`read-continue${right < items.length || next ? " second" : ""}`} onClick={onClose}>
              보충학습실로
            </button>
          </div>
        </>
      )}
    </div>
  );
}

/** 규칙 카드 — 「부정문일 땐 → nor + 동사 + 주어」 */
function RuleCard({ drill }: { drill: NonNullable<ReturnType<typeof getGrammarDrill>> }) {
  return (
    <ul className="gdrill-card">
      {drill.intro.map(([when, then, ex]) => (
        <li key={when + then}>
          <span className="gdrill-when">{when}</span>
          <span className="gdrill-arrow">→</span>
          <b className="gdrill-then">{then}</b>
          {ex ? <small className="gdrill-ex">{ex}</small> : null}
        </li>
      ))}
    </ul>
  );
}

function answerOf(it: DrillItem): string {
  return it.type === "choice" ? it.answer : it.answers[0]!;
}

function fill(sentence: string, answer: string): string {
  return sentence.replace("___", answer);
}

/** 빈칸이 든 문장 — 답을 고르거나 쓰면 빈칸에 정답이 들어간다 */
function Sentence({ item, shown, ok }: { item: DrillItem; shown: boolean; ok: boolean }) {
  const [before, after] = item.sentence.split("___");
  return (
    <div className="vtest-sentence">
      <p className="vtest-en">
        {before}
        <span className={`vtest-blank${shown ? (ok ? " right" : " wrong") : ""}`}>{shown ? answerOf(item) : " ".repeat(10)}</span>
        {after}
      </p>
      {item.ko ? <p className="vtest-ko">{item.ko}</p> : null}
    </div>
  );
}

function Feedback({ ok, why, onNext }: { ok: boolean; why: string; onNext: () => void }) {
  return (
    <div className="words-dock">
      <p className={`vtest-feedback${ok ? " right" : ""}`}>{ok ? "맞았어요!" : `아쉽게도 틀렸어요. ${why}`}</p>
      {ok ? null : (
        <button type="button" className="read-continue" onClick={onNext}>
          다음
        </button>
      )}
    </div>
  );
}

function ChoiceItem({ item, onDone }: { item: Extract<DrillItem, { type: "choice" }>; onDone: (ok: boolean) => void }) {
  const [chosen, setChosen] = useState<string | null>(null);
  const ok = chosen === item.answer;

  function choose(o: string) {
    if (chosen) return;
    setChosen(o);
    // 맞히면 칭찬만 잠깐 보이고 다음 문제로
    if (o === item.answer) window.setTimeout(() => onDone(true), 900);
  }

  return (
    <>
      <p className="words-title">빈칸에 알맞은 것을 골라 보세요.</p>
      <Sentence item={item} shown={!!chosen} ok={ok} />
      <ul className="words-list vtest-options">
        {item.options.map((o) => {
          const state = !chosen ? "" : o === item.answer ? " right" : o === chosen ? " wrong" : " dim";
          return (
            <li key={o}>
              <button type="button" className={`vtest-option${state}`} disabled={!!chosen} onClick={() => choose(o)}>
                {o}
              </button>
            </li>
          );
        })}
      </ul>
      {chosen ? <Feedback ok={ok} why={item.why} onNext={() => onDone(false)} /> : null}
    </>
  );
}

function InputItem({
  item,
  writing,
  onTyped,
  onDone,
}: {
  item: Extract<DrillItem, { type: "input" }>;
  /** 작문 — 빈칸이 뒷부분 전체라 길게 쓴다 */
  writing?: boolean;
  /** 학생이 쓴 답을 그대로 남긴다 */
  onTyped: (typed: string, ok: boolean) => void;
  onDone: (ok: boolean) => void;
}) {
  const [typed, setTyped] = useState("");
  const [checked, setChecked] = useState<boolean | null>(null);

  function check() {
    if (checked !== null || !typed.trim()) return;
    const ok = isRightInput(item, typed);
    onTyped(typed, ok);
    setChecked(ok);
    if (ok) window.setTimeout(() => onDone(true), 900);
  }

  return (
    <>
      <p className="words-title">{writing ? "한국어를 보고 빈칸 부분을 영어로 써 보세요." : "빈칸에 들어갈 말을 직접 써 보세요."}</p>
      <Sentence item={item} shown={checked !== null} ok={!!checked} />
      <form
        className="gdrill-input-row"
        onSubmit={(e) => {
          e.preventDefault();
          check();
        }}
      >
        <input
          className={`gdrill-input${checked === null ? "" : checked ? " right" : " wrong"}`}
          value={typed}
          onChange={(e) => setTyped(e.target.value)}
          placeholder={writing ? "빈칸 부분을 영어로" : "영어로 쓰세요"}
          autoCapitalize="off"
          autoComplete="off"
          spellCheck={false}
          disabled={checked !== null}
          autoFocus
        />
        {checked === null ? (
          <button type="submit" className="read-continue gdrill-check" disabled={!typed.trim()}>
            확인
          </button>
        ) : null}
      </form>
      {checked !== null ? <Feedback ok={checked} why={item.why} onNext={() => onDone(false)} /> : null}
    </>
  );
}
