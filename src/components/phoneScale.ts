/**
 * 액자(`.phone`)를 화면에 맞춰 줄인 비율 — 390×844를 `transform: scale()`로 줄여 그린다(`styles.css`).
 *
 * 끌기 칩은 손가락이 움직인 화면 거리(clientX·Y 차이)를 `translate`로 옮기는데, 그 translate도 같이 줄어든다.
 * 그대로 쓰면 칩이 손가락보다 덜 따라와서, 칩을 칸에 맞춰 놓아도 손가락은 칸 아래에 있다 — 짝이 안 맞아
 * 「좀 위에 놔야 맞춰진다」 (2026-10-22 선생님). 끈 거리를 이 비율로 나눠 칩이 손가락 밑에 붙어 있게 한다.
 */
export function phoneScale(el: Element | null): number {
  const phone = el?.closest<HTMLElement>(".phone");
  if (!phone || !phone.offsetWidth) return 1;
  return phone.getBoundingClientRect().width / phone.offsetWidth || 1;
}
