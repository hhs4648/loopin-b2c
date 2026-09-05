export type DemoPath = "P1" | "P2" | "P3" | "E";

export type UnitMatch = {
  p1: string[][];
  p2: string[];
  p3: string[];
  p2_unless?: string[];
};

function compact(s: string): string {
  return s
    .toLowerCase()
    .replace(/[“”"'’.,!?~\-]/g, "")
    .replace(/\s+/g, "");
}

const UNKNOWN_RE =
  /잘모르|모르겠어|모르겠어요|몰라요|몰라|힌트|포기|잘모르겠/;

export function isUnknownInput(text: string): boolean {
  const n = compact(text);
  return !n || UNKNOWN_RE.test(n);
}

function has(n: string, xs: string[]): boolean {
  return xs.some((x) => n.includes(compact(x)));
}

export function classifyUnit(text: string, rule: UnitMatch): DemoPath {
  if (isUnknownInput(text)) return "E";
  const n = compact(text);
  if (rule.p3.length && has(n, rule.p3)) return "P3";
  if (rule.p2.length && has(n, rule.p2) && !has(n, rule.p2_unless ?? [])) return "P2";
  if (rule.p1.length && rule.p1.every((group) => has(n, group))) return "P1";
  return "E";
}

export function matchChoice(text: string, labels: string[]): string | null {
  const n = compact(text);
  for (const label of labels) {
    if (n === compact(label) || n.includes(compact(label))) return label;
  }
  return null;
}
