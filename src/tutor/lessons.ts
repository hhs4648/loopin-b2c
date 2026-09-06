import moeui18 from "../../content/tutor/lessons/moeui-2027-09-18-decline-speech.json";
import moeui19 from "../../content/tutor/lessons/moeui-2027-09-19-katie-sarah.json";
import moeui20 from "../../content/tutor/lessons/moeui-2027-09-20-lifelong-learning.json";
import moeui21 from "../../content/tutor/lessons/moeui-2027-09-21-autocomplete-mirror.json";
import moeui22 from "../../content/tutor/lessons/moeui-2027-09-22-front-row.json";
import moeui23 from "../../content/tutor/lessons/moeui-2027-09-23-dopamine.json";
import moeui24 from "../../content/tutor/lessons/moeui-2027-09-24-aging-boundaries.json";
import moeui26 from "../../content/tutor/lessons/moeui-2027-09-26-chuck-jones.json";
import moeui29 from "../../content/tutor/lessons/moeui-2027-09-29-empathy-leader.json";
import moeui30 from "../../content/tutor/lessons/moeui-2027-09-30-garden-pests.json";
import moeui31 from "../../content/tutor/lessons/moeui-2027-09-31-glossophobia.json";
import moeui32 from "../../content/tutor/lessons/moeui-2027-09-32-tickle-surprise.json";
import moeui33 from "../../content/tutor/lessons/moeui-2027-09-33-balzac-description.json";
import moeui34 from "../../content/tutor/lessons/moeui-2027-09-34-joke-canyon.json";
import moeui35 from "../../content/tutor/lessons/moeui-2027-09-35-tourist-selection.json";
import moeui36 from "../../content/tutor/lessons/moeui-2027-09-36-mixed-signals.json";
import moeui37 from "../../content/tutor/lessons/moeui-2027-09-37-salmon-breeding.json";
import moeui38 from "../../content/tutor/lessons/moeui-2027-09-38-citizen-science.json";
import moeui39 from "../../content/tutor/lessons/moeui-2027-09-39-music-attention.json";
import moeui40 from "../../content/tutor/lessons/moeui-2027-09-40-selective-visibility.json";
import moeui41a from "../../content/tutor/lessons/moeui-2027-09-41-curious-nonbelief-1.json";
import moeui41b from "../../content/tutor/lessons/moeui-2027-09-41-curious-nonbelief-2.json";
import moeui43a from "../../content/tutor/lessons/moeui-2027-09-43-mickey-walk-1.json";
import moeui43b from "../../content/tutor/lessons/moeui-2027-09-43-mickey-walk-2.json";
import resignation from "../../content/tutor/lessons/resignation-letter.json";
import suneung19 from "../../content/tutor/lessons/suneung-19-anna-rescue.json";
import suneung20 from "../../content/tutor/lessons/suneung-20-adult-learners.json";
import suneung21 from "../../content/tutor/lessons/suneung-21-wine-perception.json";
import suneung22 from "../../content/tutor/lessons/suneung-22-multilingual-emotion.json";
import suneung23 from "../../content/tutor/lessons/suneung-23-social-death.json";
import suneung24 from "../../content/tutor/lessons/suneung-24-future-generations.json";
import suneung26 from "../../content/tutor/lessons/suneung-26-ilya-prigogine.json";
import suneung27 from "../../content/tutor/lessons/suneung-27-safe-manual.json";
import suneung28 from "../../content/tutor/lessons/suneung-28-poetry-competition.json";
import suneung29 from "../../content/tutor/lessons/suneung-29-crossing-cultures.json";
import suneung30 from "../../content/tutor/lessons/suneung-30-geometry-landmarks.json";
import suneung31 from "../../content/tutor/lessons/suneung-31-losing-metaphor.json";
import suneung32 from "../../content/tutor/lessons/suneung-32-altruists-no-choice.json";
import suneung33 from "../../content/tutor/lessons/suneung-33-stoic-control.json";
import suneung34 from "../../content/tutor/lessons/suneung-34-japanese-ao.json";
import suneung35 from "../../content/tutor/lessons/suneung-35-translingual.json";
import suneung36 from "../../content/tutor/lessons/suneung-36-creative-spectrum.json";
import suneung37 from "../../content/tutor/lessons/suneung-37-urban-planning.json";
import suneung38 from "../../content/tutor/lessons/suneung-38-insurance-realtime.json";
import suneung39 from "../../content/tutor/lessons/suneung-39-perspective-painting.json";
import suneung40 from "../../content/tutor/lessons/suneung-40-brain-plasticity.json";
import suneung41a from "../../content/tutor/lessons/suneung-41-narrator-1.json";
import suneung41b from "../../content/tutor/lessons/suneung-41-narrator-2.json";
import suneung43a from "../../content/tutor/lessons/suneung-43-baseball-card-1.json";
import suneung43b from "../../content/tutor/lessons/suneung-43-baseball-card-2.json";
import thales from "../../content/tutor/lessons/thales-participial-phrase-front.json";
import type { Lesson } from "../../content/tutor/types";

/**
 * 레슨 목록.
 *
 * **지문을 추가할 때 고치는 유일한 코드**다 — 한 줄 import + 배열에 넣기.
 * 문장·칭찬·힌트·오류 대사는 전부 JSON 안에 있다.
 */
const LESSONS = [resignation, suneung19, suneung20, suneung21, suneung22, suneung23, suneung24, suneung26, suneung27, suneung28, suneung29, suneung30, suneung31, suneung32, suneung33, suneung34, suneung35, suneung36, suneung37, suneung38, suneung39, suneung40, suneung41a, suneung41b, suneung43a, suneung43b, moeui18, moeui19, moeui20, moeui21, moeui22, moeui23, moeui24, moeui26, moeui29, moeui30, moeui31, moeui32, moeui33, moeui34, moeui35, moeui36, moeui37, moeui38, moeui39, moeui40, moeui41a, moeui41b, moeui43a, moeui43b, thales] as unknown as Lesson[];

export const DEFAULT_LESSON_ID = LESSONS[0]!.id;

export function getLesson(id?: string | null): Lesson {
  if (!id) return LESSONS[0]!;
  return LESSONS.find((lesson) => lesson.id === id) ?? LESSONS[0]!;
}

export function lessonIds(): string[] {
  return LESSONS.map((lesson) => lesson.id);
}
