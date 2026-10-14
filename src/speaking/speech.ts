/**
 * 브라우저에 들어 있는 음성 기능만 쓴다 — 서버·LLM 없음, 비용 0.
 *
 * - 읽어 주기: `speechSynthesis` (시범용. 상용에선 미리 녹음·생성해 둔 음성 파일로 바꾼다)
 * - 음성 인식: `SpeechRecognition` (Chrome·Safari·Edge). 없는 브라우저는 입력창으로 대신한다
 * - 녹음: `MediaRecorder` — 학생이 자기 답을 다시 들어 본다. 실패해도 수업은 그대로 간다
 */

/* 브라우저마다 이름이 다르고 TS 기본 타입에 없다 — 필요한 만큼만 적는다 */
type RecognitionResult = { isFinal: boolean; 0: { transcript: string } };
type RecognitionEvent = { resultIndex: number; results: ArrayLike<RecognitionResult> };
type Recognition = {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  onresult: ((e: RecognitionEvent) => void) | null;
  onerror: ((e: { error: string }) => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
};

function recognitionCtor(): (new () => Recognition) | null {
  const w = window as unknown as { SpeechRecognition?: new () => Recognition; webkitSpeechRecognition?: new () => Recognition };
  return w.SpeechRecognition ?? w.webkitSpeechRecognition ?? null;
}

export function canRecognize(): boolean {
  return typeof window !== "undefined" && recognitionCtor() != null;
}

export type Listener = {
  /** 멈추고 지금까지 받아 적은 글자를 돌려준다 */
  stop(): Promise<string>;
};

/**
 * 듣기 시작. `onText`로 받아 적는 중간 결과를 계속 알려 준다.
 * 권한이 없거나 네트워크 오류면 `onFail` — 화면은 입력창으로 바꾼다.
 */
export function listen(onText: (text: string) => void, onFail: (error: string) => void): Listener | null {
  const Ctor = recognitionCtor();
  if (!Ctor) return null;
  const rec = new Ctor();
  rec.lang = "en-US";
  rec.continuous = true;
  rec.interimResults = true;
  let finals = "";
  let interim = "";
  let stopped = false;
  let resolveEnd: (() => void) | null = null;
  rec.onresult = (e) => {
    interim = "";
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const r = e.results[i]!;
      if (r.isFinal) finals += `${r[0].transcript} `;
      else interim += r[0].transcript;
    }
    onText(`${finals}${interim}`.trim());
  };
  rec.onerror = (e) => {
    if (e.error !== "no-speech" && e.error !== "aborted") onFail(e.error);
  };
  rec.onend = () => {
    // 말을 잠깐 멈추면 브라우저가 스스로 끝낸다 — 학생이 멈추기 전이면 다시 듣는다
    if (!stopped) {
      try {
        rec.start();
        return;
      } catch {
        /* 다시 못 열면 여기서 끝 */
      }
    }
    resolveEnd?.();
  };
  try {
    rec.start();
  } catch (err) {
    onFail(String(err));
    return null;
  }
  return {
    stop() {
      stopped = true;
      return new Promise((resolve) => {
        resolveEnd = () => resolve(`${finals}${interim}`.trim());
        try {
          rec.stop();
        } catch {
          resolveEnd();
        }
        // onend가 안 오는 브라우저도 있다
        window.setTimeout(() => resolveEnd?.(), 1200);
      });
    },
  };
}

/**
 * 영어 목소리 — Chrome은 목록을 늦게 채운다(`voiceschanged`). 목소리 없이 읽으면 소리가 안 날 때가 있다.
 * 미국 영어 > 영어 아무거나 순. 기다려도 없으면 null (브라우저 기본으로 읽는다)
 */
let voiceCache: SpeechSynthesisVoice | null | undefined;
function englishVoice(synth: SpeechSynthesis): Promise<SpeechSynthesisVoice | null> {
  if (voiceCache !== undefined) return Promise.resolve(voiceCache);
  const pick = () => {
    const vs = synth.getVoices();
    return vs.find((v) => v.lang === "en-US" && /samantha|google us|aria|jenny/i.test(v.name)) ?? vs.find((v) => v.lang === "en-US") ?? vs.find((v) => v.lang.startsWith("en")) ?? null;
  };
  const now = pick();
  if (now) return Promise.resolve((voiceCache = now));
  return new Promise((resolve) => {
    const done = () => {
      synth.removeEventListener("voiceschanged", done);
      resolve((voiceCache = pick()));
    };
    synth.addEventListener("voiceschanged", done);
    window.setTimeout(done, 1500);
  });
}

/**
 * 영어 문장을 읽어 준다. 끝나면 resolve.
 * Chrome은 `cancel()` 바로 뒤에 `speak()`하면 소리 없이 넘어가는 일이 있다 — 읽는 중일 때만 멈추고, 잠깐 쉬었다 읽는다.
 * 멈춤 상태로 굳는 일도 있어 `resume()`을 먼저 부른다. 끝 소식(onend)이 안 오는 일도 있어 길이로 시간 제한을 둔다
 */
export async function say(text: string, rate = 0.95): Promise<void> {
  const synth = typeof window !== "undefined" ? window.speechSynthesis : undefined;
  if (!synth) return;
  const voice = await englishVoice(synth);
  if (synth.speaking || synth.pending) {
    synth.cancel();
    await new Promise((r) => window.setTimeout(r, 120));
  }
  synth.resume();
  await new Promise<void>((resolve) => {
    const u = new SpeechSynthesisUtterance(text);
    u.lang = voice?.lang ?? "en-US";
    if (voice) u.voice = voice;
    u.rate = rate;
    const limit = window.setTimeout(resolve, 2000 + text.length * 120);
    const end = () => {
      window.clearTimeout(limit);
      resolve();
    };
    u.onend = end;
    u.onerror = end;
    synth.speak(u);
  });
}

export function stopSaying(): void {
  window.speechSynthesis?.cancel();
}

export type Recorder = { stop(): Promise<string | null> };

/** 녹음 시작 — 끝나면 다시 들을 수 있는 주소(blob URL). 마이크·브라우저가 안 되면 null */
export async function record(): Promise<Recorder | null> {
  try {
    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") return null;
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const rec = new MediaRecorder(stream);
    const chunks: Blob[] = [];
    rec.ondataavailable = (e) => e.data.size && chunks.push(e.data);
    rec.start();
    return {
      stop() {
        return new Promise((resolve) => {
          rec.onstop = () => {
            stream.getTracks().forEach((t) => t.stop());
            resolve(chunks.length ? URL.createObjectURL(new Blob(chunks, { type: rec.mimeType })) : null);
          };
          rec.stop();
        });
      },
    };
  } catch {
    return null;
  }
}
