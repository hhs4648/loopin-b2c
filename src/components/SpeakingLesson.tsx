import { useEffect, useRef, useState } from "react";
import { checkSpeech, slotUsed, type SpeechCheck } from "../speaking/check";
import { canRecognize, listen, record, say, stopSaying, type Listener, type Recorder } from "../speaking/speech";
import type { ModelLine, SpeakingLesson as Lesson, TemplateSlot } from "../speaking/types";
import "../speaking/speaking.css";

/**
 * 토익 스피킹 시범 수업 — 사진 묘사(Q3~4).
 *
 * 틀 보기 → 예시 듣기 → 빈칸 → 한 문장씩 따라 말하기 → 틀만 보고 전부 말하기 → 새 사진으로 실전(준비·말하기 타이머) → 결과.
 * 수업 중 LLM 없음 — 음성 인식 결과를 `check.ts` 규칙으로만 본다. 학생이 말한 글자는 그대로 남긴다(localStorage, 나중에 서버로).
 */

type Phase = "intro" | "picture" | "listen" | "fill" | "shadow" | "recall" | "testIntro" | "prep" | "speak" | "result";

const STEPS: { label: string; phases: Phase[] }[] = [
  { label: "틀", phases: ["intro"] },
  { label: "듣기", phases: ["picture", "listen"] },
  { label: "빈칸", phases: ["fill"] },
  { label: "따라 말하기", phases: ["shadow"] },
  { label: "틀만 보고", phases: ["recall"] },
  { label: "실전", phases: ["testIntro", "prep", "speak", "result"] },
];

const ATTEMPTS_KEY = "loopin.speaking.attempts";

function saveAttempt(entry: Record<string, unknown>) {
  try {
    const prev = JSON.parse(window.localStorage.getItem(ATTEMPTS_KEY) ?? "[]") as unknown[];
    window.localStorage.setItem(ATTEMPTS_KEY, JSON.stringify([...prev, { ...entry, at: new Date().toISOString() }].slice(-200)));
  } catch {
    /* 기록은 없어도 수업은 간다 */
  }
}

export function SpeakingLesson({ lesson, onClose }: { lesson: Lesson; onClose: () => void }) {
  const L = lesson.lines;
  const [phase, setPhase] = useState<Phase>("intro");
  const [fillIdx, setFillIdx] = useState(0);
  const [fillPicked, setFillPicked] = useState<string | null>(null);
  const [shadowIdx, setShadowIdx] = useState(0);
  const [shadowText, setShadowText] = useState<string | null>(null);
  const [recall, setRecall] = useState<SpeechCheck | null>(null);
  const [left, setLeft] = useState(0);
  const [result, setResult] = useState<{ check: SpeechCheck; text: string; audio: string | null; seconds: number } | null>(null);

  const slotOf = (key: string) => lesson.template.find((s) => s.key === key)!;
  const slotIndex = (key: string) => lesson.template.findIndex((s) => s.key === key);
  const stepNow = STEPS.findIndex((s) => s.phases.includes(phase));

  useEffect(() => () => stopSaying(), []);

  // 실전 준비 타이머 — 0이 되면 바로 말하기
  useEffect(() => {
    if (phase !== "prep") return;
    setLeft(lesson.test.prep_seconds ?? 45);
    const id = window.setInterval(() => {
      setLeft((n) => {
        if (n <= 1) {
          window.clearInterval(id);
          setPhase("speak");
          return 0;
        }
        return n - 1;
      });
    }, 1000);
    return () => window.clearInterval(id);
  }, [phase, lesson.test.prep_seconds]);

  /* ── 선생님 한마디 + 아래 버튼 ───────────────────────────────── */
  let line = "";
  let buttons: { label: string; onClick: () => void; ghost?: boolean }[] = [];
  const fill = lesson.fill[fillIdx];
  const shadowLine = lesson.practice.model[shadowIdx];

  if (phase === "intro") {
    line = L.intro!;
    buttons = [{ label: "좋아요", onClick: () => setPhase("picture") }];
  } else if (phase === "picture") {
    line = L.picture!;
    buttons = [{ label: "예시 듣기", onClick: () => setPhase("listen") }];
  } else if (phase === "listen") {
    line = L.listen!;
    buttons = [{ label: "다 들었어요", onClick: () => setPhase("fill") }];
  } else if (phase === "fill" && fill) {
    const right = fill.options.find((o) => o.correct)!.label;
    if (!fillPicked) line = fill.ask;
    else if (fillPicked === right) line = fill.praise;
    else line = `${L.wrong_lead} ${fill.why}`;
    if (fillPicked)
      buttons = [
        {
          label: "다음",
          onClick: () => {
            setFillPicked(null);
            if (fillIdx + 1 < lesson.fill.length) setFillIdx(fillIdx + 1);
            else setPhase("shadow");
          },
        },
      ];
  } else if (phase === "shadow" && shadowLine) {
    const ok = shadowText != null && slotUsed(slotOf(shadowLine.slot), shadowText);
    line = shadowText == null ? L.shadow! : ok ? L.shadow_ok! : `${L.shadow_miss} ${slotOf(shadowLine.slot).phrase}`;
    if (shadowText != null)
      buttons = [
        { label: "다시 말하기", ghost: true, onClick: () => setShadowText(null) },
        {
          label: shadowIdx + 1 < lesson.practice.model.length ? "다음 문장" : "틀만 보고 말하기",
          onClick: () => {
            setShadowText(null);
            if (shadowIdx + 1 < lesson.practice.model.length) setShadowIdx(shadowIdx + 1);
            else setPhase("recall");
          },
        },
      ];
  } else if (phase === "recall") {
    line = !recall ? L.recall! : recall.usedCount === lesson.template.length ? L.recall_done! : L.result_partial!;
    if (recall)
      buttons = [
        { label: "다시 말하기", ghost: true, onClick: () => setRecall(null) },
        { label: "실전으로", onClick: () => setPhase("testIntro") },
      ];
  } else if (phase === "testIntro") {
    line = L.test!;
    buttons = [{ label: "시작", onClick: () => setPhase("prep") }];
  } else if (phase === "prep") {
    line = L.prep!;
    buttons = [{ label: "준비됐어요", onClick: () => setPhase("speak") }];
  } else if (phase === "speak") {
    line = L.speak!;
  } else if (phase === "result" && result) {
    const n = result.check.usedCount;
    line = n === lesson.template.length ? L.result_full! : n >= 2 ? L.result_partial! : L.result_low!;
    buttons = [
      { label: "다시 해 볼래요", ghost: true, onClick: () => { setResult(null); setPhase("prep"); } },
      { label: "끝내기", onClick: onClose },
    ];
  }

  const picture = phase === "testIntro" || phase === "prep" || phase === "speak" || phase === "result" ? lesson.test : lesson.practice;
  const showPicture = phase !== "intro";

  return (
    <div className="sp">
      <header className="sp-top">
        <span className="sp-chip">{lesson.title}</span>
        <button type="button" className="sp-close" aria-label="학습 종료" onClick={onClose}>
          ×
        </button>
      </header>
      <ol className="sp-steps" aria-label="진행">
        {STEPS.map((s, i) => (
          <li key={s.label} className={i < stepNow ? "done" : i === stepNow ? "now" : ""}>
            {s.label}
          </li>
        ))}
      </ol>

      <div className="sp-body">
        {phase === "intro" || phase === "recall" || phase === "prep" ? <TemplateBoard template={lesson.template} /> : null}

        {showPicture ? (
          <figure className="sp-pic">
            <img src={picture.image} alt={picture.alt} />
            {phase === "prep" || phase === "speak" ? <span className="sp-timer">{phase === "prep" ? `준비 ${left}초` : null}</span> : null}
          </figure>
        ) : null}

        {phase === "listen" ? <ModelLines lines={lesson.practice.model} template={lesson.template} autoplay /> : null}

        {phase === "fill" && fill ? (
          <div className="sp-fill">
            <p className={`sp-sentence slot-${slotIndex(fill.slot)}`}>
              {fill.sentence.split("___").map((part, i, arr) => (
                <span key={i}>
                  {part}
                  {i < arr.length - 1 ? (
                    <b className="sp-blank">{fillPicked ? fill.options.find((o) => o.correct)!.label : "____"}</b>
                  ) : null}
                </span>
              ))}
            </p>
            {!fillPicked ? (
              <div className="sp-options">
                {fill.options.map((o, i) => (
                  <button key={o.label} type="button" className="sp-pill" onClick={() => setFillPicked(o.label)}>
                    {i + 1} {o.label}
                  </button>
                ))}
              </div>
            ) : null}
          </div>
        ) : null}

        {phase === "shadow" && shadowLine ? (
          <div className="sp-shadow">
            <div className="sp-shadow-head">
              <span className={`sp-slot slot-${slotIndex(shadowLine.slot)}`}>{slotOf(shadowLine.slot).label}</span>
              <span className="sp-count">
                {shadowIdx + 1} / {lesson.practice.model.length}
              </span>
            </div>
            <ModelLines lines={[shadowLine]} template={lesson.template} />
            {shadowText == null ? (
              <MicBox
                key={`shadow-${shadowIdx}`}
                noMicLine={L.no_mic!}
                onDone={(text) => {
                  setShadowText(text);
                  saveAttempt({ lesson: lesson.id, step: "shadow", slot: shadowLine.slot, text });
                }}
              />
            ) : (
              <Heard text={shadowText} />
            )}
          </div>
        ) : null}

        {phase === "recall" ? (
          recall == null ? (
            <MicBox
              key="recall"
              noMicLine={L.no_mic!}
              onDone={(text) => {
                const check = checkSpeech(lesson.template, lesson.practice, text);
                setRecall(check);
                saveAttempt({ lesson: lesson.id, step: "recall", text, used: check.usedCount });
              }}
            />
          ) : (
            <SlotChecklist check={recall} template={lesson.template} />
          )
        ) : null}

        {phase === "speak" ? (
          <MicBox
            key="speak"
            autoStart
            seconds={lesson.test.speak_seconds ?? 30}
            withRecording
            noMicLine={L.no_mic!}
            onDone={(text, audio, seconds) => {
              const check = checkSpeech(lesson.template, lesson.test, text);
              setResult({ check, text, audio, seconds });
              saveAttempt({ lesson: lesson.id, step: "test", text, used: check.usedCount, words: check.words, seconds });
              setPhase("result");
            }}
          />
        ) : null}

        {phase === "result" && result ? (
          <div className="sp-result">
            <SlotChecklist check={result.check} template={lesson.template} />
            <dl className="sp-stats">
              <div>
                <dt>말한 시간</dt>
                <dd>{result.seconds}초</dd>
              </div>
              <div>
                <dt>단어</dt>
                <dd>{result.check.words}개</dd>
              </div>
              <div>
                <dt>사진 내용</dt>
                <dd>{result.check.keywordHits.length}개</dd>
              </div>
            </dl>
            {result.audio ? (
              <div className="sp-mine">
                <small>내 답변 다시 듣기</small>
                <audio controls src={result.audio} />
              </div>
            ) : null}
            <Heard text={result.text} label="받아 적은 내 답변" />
            <details className="sp-model">
              <summary>예시 답변 보기</summary>
              <ModelLines lines={lesson.test.model} template={lesson.template} />
            </details>
          </div>
        ) : null}
      </div>

      <div className="sp-teacher">
        <img src="/assets/dajung-teacher.webp" alt="다정쌤" width={650} height={616} draggable={false} />
        <p className="sp-bubble">{line}</p>
      </div>
      <div className="sp-actions">
        {buttons.map((b) => (
          <button key={b.label} type="button" className={`sp-pill${b.ghost ? " ghost" : ""}`} onClick={b.onClick}>
            {b.label}
          </button>
        ))}
      </div>
    </div>
  );
}

/** 칠판 — 네 칸 틀 */
function TemplateBoard({ template }: { template: TemplateSlot[] }) {
  return (
    <div className="sp-board">
      <small>사진 묘사 틀</small>
      <ol>
        {template.map((s, i) => (
          <li key={s.key} className={`slot-${i}`}>
            <b>{s.label}</b>
            <span>{s.phrase}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}

/** 예시 답변 — 칸마다 색, 누르면 그 문장을 읽어 준다. autoplay면 처음부터 끝까지 한 번 */
function ModelLines({ lines, template, autoplay }: { lines: ModelLine[]; template: TemplateSlot[]; autoplay?: boolean }) {
  const [playing, setPlaying] = useState<number | null>(null);
  const alive = useRef(true);
  useEffect(() => {
    alive.current = true;
    // 이번 실행만의 표시 — 개발 모드(StrictMode)는 effect를 두 번 돌린다. 공유 ref만 보면 두 번째 실행이
    // alive를 다시 켜서 첫 번째 읽기도 살아나고, 둘이 서로 끊어 소리가 안 났다
    let run = true;
    if (autoplay) {
      (async () => {
        for (let i = 0; i < lines.length && run; i++) {
          setPlaying(i);
          await say(lines[i]!.en);
        }
        if (run) setPlaying(null);
      })();
    }
    return () => {
      run = false;
      alive.current = false;
      stopSaying();
    };
  }, [autoplay, lines]);
  const play = async (i: number) => {
    setPlaying(i);
    await say(lines[i]!.en);
    if (alive.current) setPlaying(null);
  };
  return (
    <ul className="sp-lines">
      {lines.map((m, i) => (
        <li key={m.en} className={`slot-${template.findIndex((s) => s.key === m.slot)}${playing === i ? " playing" : ""}`}>
          <button type="button" onClick={() => play(i)} aria-label="듣기">
            🔊
          </button>
          <div>
            <p>{m.en}</p>
            <small>{m.ko}</small>
          </div>
        </li>
      ))}
    </ul>
  );
}

/**
 * 말하기 — 음성 인식으로 받아 적고, 안 되는 브라우저는 입력창으로.
 * seconds가 있으면 그 시간이 지나면 저절로 끝난다(실전).
 */
function MicBox({
  onDone,
  noMicLine,
  autoStart,
  seconds,
  withRecording,
}: {
  onDone: (text: string, audio: string | null, seconds: number) => void;
  noMicLine: string;
  autoStart?: boolean;
  seconds?: number;
  withRecording?: boolean;
}) {
  const [mode, setMode] = useState<"idle" | "listening" | "typing">(canRecognize() ? "idle" : "typing");
  const [live, setLive] = useState("");
  const [typed, setTyped] = useState("");
  const [left, setLeft] = useState(seconds ?? 0);
  const [failed, setFailed] = useState<string | null>(null);
  const listener = useRef<Listener | null>(null);
  const recorder = useRef<Recorder | null>(null);
  const startedAt = useRef(0);
  const finished = useRef(false);

  const finish = async (fromTyping?: string) => {
    if (finished.current) return;
    finished.current = true;
    const spent = startedAt.current ? Math.round((Date.now() - startedAt.current) / 1000) : 0;
    const text = fromTyping ?? (listener.current ? await listener.current.stop() : live);
    const audio = recorder.current ? await recorder.current.stop() : null;
    onDone(text, audio, seconds && !fromTyping ? Math.min(spent, seconds) : spent);
  };

  const start = async () => {
    startedAt.current = Date.now();
    setMode("listening");
    listener.current = listen(setLive, (err) => {
      setFailed(err);
      listener.current = null;
      setMode("typing");
    });
    if (!listener.current) setMode("typing");
    if (withRecording) recorder.current = await record();
  };

  useEffect(() => {
    if (autoStart && mode === "idle") void start();
    if (mode === "typing" && seconds) startedAt.current = Date.now();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 실전 타이머 — 듣는 중이든 입력 중이든 시간이 다 되면 끝
  useEffect(() => {
    if (!seconds) return;
    const id = window.setInterval(() => {
      setLeft((n) => {
        if (n <= 1) {
          window.clearInterval(id);
          void finish(mode === "typing" ? typed : undefined);
          return 0;
        }
        return n - 1;
      });
    }, 1000);
    return () => window.clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [seconds, mode, typed]);

  if (mode === "typing") {
    return (
      <div className="sp-mic typing">
        {failed !== null || !canRecognize() ? <p className="sp-nomic">{noMicLine}</p> : null}
        {seconds ? <span className="sp-left">남은 시간 {left}초</span> : null}
        <textarea
          value={typed}
          onChange={(e) => setTyped(e.target.value)}
          placeholder="영어로 말할 내용을 입력해 보세요"
          rows={3}
        />
        <button type="button" className="sp-pill" disabled={!typed.trim()} onClick={() => void finish(typed)}>
          확인
        </button>
      </div>
    );
  }

  return (
    <div className={`sp-mic${mode === "listening" ? " on" : ""}`}>
      {mode === "idle" ? (
        <button type="button" className="sp-mic-btn" onClick={() => void start()}>
          🎤 말하기
        </button>
      ) : (
        <>
          <div className="sp-live">
            <span className="sp-dot" />
            {seconds ? `남은 시간 ${left}초` : "듣고 있어요"}
          </div>
          <p className="sp-live-text">{live || "…"}</p>
          <button type="button" className="sp-pill" onClick={() => void finish()}>
            다 말했어요
          </button>
        </>
      )}
      {mode === "idle" ? (
        <button type="button" className="sp-link" onClick={() => setMode("typing")}>
          말 대신 입력할래요
        </button>
      ) : null}
    </div>
  );
}

function Heard({ text, label = "받아 적은 내 말" }: { text: string; label?: string }) {
  return (
    <div className="sp-heard">
      <small>{label}</small>
      <p>{text || "(들린 말이 없어요)"}</p>
    </div>
  );
}

/** 칸마다 채웠는지 — 빠진 칸은 「이 표현도 넣어 봐요」 */
function SlotChecklist({ check, template }: { check: SpeechCheck; template: TemplateSlot[] }) {
  return (
    <ul className="sp-check">
      {check.slots.map((s, i) => (
        <li key={s.key} className={s.used ? "ok" : "miss"}>
          <span className={`sp-slot slot-${i}`}>{s.label}</span>
          {s.used ? <b>✓</b> : <em>이 표현도 넣어 봐요 · {template[i]!.phrase}</em>}
        </li>
      ))}
    </ul>
  );
}
