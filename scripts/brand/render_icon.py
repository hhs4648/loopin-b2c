"""Rasterize public/brand/loopin-icon.svg into the PWA and store PNGs.

The SVG is the source. Run from the repo root:

  py scripts/brand/render_icon.py
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SVG = ROOT / "public" / "brand" / "loopin-icon.svg"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

LOOP = (
    "M87.0977 19.0039C97.7518 19.0039 106.363 27.6611 106.363 38.3076"
    "C106.363 48.954 97.7517 57.6104 87.0977 57.6104C80.6865 57.6103 "
    "75.0161 54.4748 71.5156 49.6582C68.0151 54.4748 62.3448 57.6104 "
    "55.9336 57.6104C45.2797 57.6101 36.6681 48.9539 36.668 38.3076"
    "C36.668 27.6612 45.2796 19.0041 55.9336 19.0039C62.3447 19.0039 "
    "68.0151 22.1395 71.5156 26.9561C75.0162 22.1394 80.6866 19.004 "
    "87.0977 19.0039ZM55.9336 30.0352C51.3999 30.0354 47.6992 33.7246 "
    "47.6992 38.3076C47.6993 42.8905 51.4 46.5799 55.9336 46.5801"
    "C60.4674 46.5801 64.1688 42.8906 64.1689 38.3076C64.1689 33.7245 "
    "60.4675 30.0352 55.9336 30.0352ZM87.0977 30.0352C82.5639 30.0353 "
    "78.8633 33.7246 78.8633 38.3076C78.8634 42.8906 82.5639 46.58 "
    "87.0977 46.5801C91.6315 46.5801 95.3329 42.8906 95.333 38.3076"
    "C95.333 33.7245 91.6315 30.0352 87.0977 30.0352Z"
)

# Logo path bounds, then 1px of pad so the rim is not clipped.
X0, Y0, LW, LH = 36.668, 19.0039, 69.695, 38.6065
PAD = 1.0
# Loop width as a fraction of the square. 62% sits inside Android's 66% circle.
FRAC = 0.62


def master_svg() -> str:
    vb_w, vb_h = LW + PAD * 2, LH + PAD * 2
    loop_w = 1024 * FRAC
    port_w = loop_w * (vb_w / LW)
    port_h = port_w * (vb_h / vb_w)
    x = (1024 - port_w) / 2
    y = (1024 - port_h) / 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Loopin 앱 아이콘 (2026-10-22). 로고 oo 고리만. 배경 #2b2430 · 왼쪽 #f8a0a4 · 오른쪽 #b498f4.
       고리 너비는 정사각의 62% (Android 원형 안전 영역 안). 모서리는 OS가 자른다. -->
  <rect width="1024" height="1024" fill="#2b2430"/>
  <svg x="{x:.3f}" y="{y:.3f}" width="{port_w:.3f}" height="{port_h:.3f}" viewBox="{X0 - PAD} {Y0 - PAD} {vb_w} {vb_h}">
    <defs>
      <path id="loop" d="{LOOP}"/>
      <clipPath id="left"><rect x="0" y="0" width="71.5156" height="76"/></clipPath>
      <clipPath id="right"><rect x="71.5156" y="0" width="40" height="76"/></clipPath>
    </defs>
    <use xlink:href="#loop" fill="#f8a0a4" clip-path="url(#left)"/>
    <use xlink:href="#loop" fill="#b498f4" clip-path="url(#right)"/>
  </svg>
</svg>
"""


def screenshot(html: Path, png: Path, width: int, height: int) -> None:
    url = html.resolve().as_posix()
    if not url.startswith("/"):
        url = "/" + url
    subprocess.run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            "--virtual-time-budget=4000",
            f"--screenshot={png}",
            f"file://{url}",
        ],
        check=True,
        capture_output=True,
    )


def save_rgb(im: Image.Image, path: Path, size: int) -> None:
    out = im.convert("RGB").resize((size, size), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    out.save(path, "PNG", optimize=True)
    corner = out.getpixel((0, 0))
    if corner != (43, 36, 48):
        raise SystemExit(f"{path.name} corner {corner} is not #2b2430")


def main() -> None:
    svg = master_svg()
    SVG.write_text(svg, encoding="utf-8")
    (ROOT / "public" / "favicon.svg").write_text(svg, encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        html = folder / "raster.html"
        html.write_text(
            "<!doctype html><style>html,body{margin:0;background:#2b2430}"
            "svg{width:1024px;height:1024px;display:block}</style>"
            + svg,
            encoding="utf-8",
        )
        raw = folder / "raw-1024.png"
        screenshot(html, raw, 1024, 1024)
        with Image.open(raw) as opened:
            im = opened.convert("RGB")
    if im.size != (1024, 1024):
        raise SystemExit(f"screenshot is {im.size}, expected 1024x1024")

    save_rgb(im, ROOT / "docs" / "store" / "loopin-icon-1024.png", 1024)
    save_rgb(im, ROOT / "public" / "icons" / "icon-512.png", 512)
    save_rgb(im, ROOT / "public" / "icons" / "icon-512-maskable.png", 512)
    save_rgb(im, ROOT / "public" / "icons" / "icon-192.png", 192)
    print("wrote icons")


if __name__ == "__main__":
    main()
