# Extract readable UI from KakaoTalk bundled HTML prototypes.
import json
import re
from pathlib import Path

srcs = [
    Path(r"c:\Users\user\Documents\카카오톡 받은 파일\학습첫화면_대답버튼.html"),
    Path(r"c:\Users\user\Documents\카카오톡 받은 파일\상냥쌤 문장 학습.html"),
]
out_dir = Path(r"C:\Users\user\.cursor\loopin-b2c\docs\tutor\refs")
out_dir.mkdir(parents=True, exist_ok=True)

def extract_template(raw: str) -> str:
    m = re.search(r'<script type="__bundler/template">\s*(.*?)\s*</script>', raw, re.S)
    if not m:
        # fallback: first giant quoted HTML
        m = re.search(r'"<!DOCTYPE html>\\n.*?"', raw)
        if not m:
            raise SystemExit("no template")
        return json.loads(m.group(0))
    return json.loads(m.group(1))

def strip_fonts(html: str) -> str:
    html = re.sub(r"@font-face\s*\{[^}]+\}", "", html)
    html = re.sub(r"url\(\"data:[^\"]+\"\)", 'url("")', html)
    html = re.sub(r"src:\s*url\(\"[^\"]+\"\)[^;]*;", "", html)
    return html

def visible_strings(html: str) -> list[str]:
    texts = []
    for pat in [
        r">([^<>]{2,80})<",
        r'placeholder="([^"]+)"',
        r'aria-label="([^"]+)"',
        r'title="([^"]+)"',
    ]:
        texts.extend(re.findall(pat, html))
    cleaned = []
    for t in texts:
        t = re.sub(r"\s+", " ", t).strip()
        if not t or t.startswith("{") or t in {"Bundled Page", "Unpacking..."}:
            continue
        if re.fullmatch(r"[\d\s./:-]+", t):
            continue
        if len(t) < 2:
            continue
        cleaned.append(t)
    # unique preserve order
    seen = set()
    out = []
    for t in cleaned:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out[:400]

def css_tokens(html: str) -> dict:
    colors = sorted(set(re.findall(r"#[0-9a-fA-F]{3,8}", html)))
    fonts = sorted(set(re.findall(r"font-family:\s*([^;]+);", html)))[:40]
    return {"colors_sample": colors[:80], "fonts_sample": fonts}

for src in srcs:
    raw = src.read_text(encoding="utf-8", errors="replace")
    html = extract_template(raw)
    slim = strip_fonts(html)
    stem = src.stem
    (out_dir / f"{stem}.slim.html").write_text(slim, encoding="utf-8")
    strings = visible_strings(html)
    meta = {
        "source": str(src),
        "html_chars": len(html),
        "slim_chars": len(slim),
        "visible_strings": strings,
        "css": css_tokens(html),
    }
    (out_dir / f"{stem}.extract.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(stem, "strings", len(strings), "slim", len(slim))
