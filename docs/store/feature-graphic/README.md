# Google Play 그래픽 이미지

- 최종: `loopin-feature-graphic.png` (1024×500, 24비트 PNG, 투명 배경 없음)
- 원본: `src/final.html` — 로고 `public/brand/loopin-logo-cream.svg`, 캐릭터 `public/brand/loopin-characters.png`
- 다시 뽑기 (Chrome 헤드리스, 저장소 루트에서):

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1024,500 --virtual-time-budget=4000 --screenshot="$(cygpath -w $PWD)\docs\store\feature-graphic\raw.png" "file:///$(cygpath -m $PWD)/docs/store/feature-graphic/src/final.html"
py -c "from PIL import Image; Image.open('docs/store/feature-graphic/raw.png').convert('RGB').save('docs/store/feature-graphic/loopin-feature-graphic.png')"
```

로고 색(2026-10-22 확정): 글자 #2b2430 · ∞ 왼쪽 핑크 #f8a0a4 · 오른쪽 보라 #b498f4 · i 점 핑크 #f8a0a4 (캐릭터 몸 색에서 뽑음).
원본 흰 로고(파란 배경용)는 `public/brand/loopin-logo.svg`, 크림용은 같은 색을 넣은 `loopin-logo-cream.svg`(벡터). PNG가 필요하면 `loopin-logo-cream.png`(832×304).
