(() => {
  const layer = document.querySelector('.polaroid-cards');
  const cards = [...document.querySelectorAll('.polaroid-card')];
  const discover = document.querySelector('#discover');
  const decide = document.querySelector('#decide');
  const journey = document.querySelector('.discovery-journey');
  if (!layer || !cards.length || !discover || !decide) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const timers = new WeakMap();
  let frame = 0;
  let range = { start: 0, end: 1 };

  function measure() {
    const discoverTop = discover.getBoundingClientRect().top + window.scrollY;
    const decideBottom = decide.getBoundingClientRect().bottom + window.scrollY;
    range = { start: discoverTop, end: Math.max(discoverTop + 1, decideBottom) };
    update();
  }

  function hide(card) {
    card.dataset.cardActive = 'false';
    card.style.opacity = '0';
  }

  function show(card) {
    if (reduced.matches) return;
    card.dataset.cardActive = 'true';
    card.style.opacity = '1';
    const existing = timers.get(card);
    if (existing) clearTimeout(existing);
    const timer = setTimeout(() => hide(card), 1000);
    timers.set(card, timer);
  }

  function update() {
    frame = 0;
    const amount = clamp((window.scrollY - range.start) / Math.max(1, range.end - range.start), 0, 1);
    const activeRange = amount > 0 && amount < 1;
    if (journey) journey.dataset.polaroidsActive = activeRange ? 'true' : 'false';
    cards.forEach((card) => {
      const trigger = Number(card.dataset.at || 0);
      const x = Number(card.dataset.x || 50);
      const y = Number(card.dataset.y || 50);
      const rotate = Number(card.dataset.rotate || 0);
      // Keep the torn edges visible on narrow screens while retaining the chosen positions.
      card.style.left = `clamp(calc(var(--card-size) / 2 + 12px), ${x}%, calc(100% - var(--card-size) / 2 - 12px))`;
      card.style.top = `${y}%`;
      card.style.transform = `translate3d(-50%, -50%, 0) rotate(${rotate}deg)`;
      card.style.setProperty('--card-y', y);
      card.style.setProperty('--card-rotate', `${rotate}deg`);
      if (!activeRange || reduced.matches) {
        hide(card);
        card.dataset.cardFired = 'false';
        return;
      }
      const fired = card.dataset.cardFired === 'true';
      if (amount >= trigger && !fired) {
        card.dataset.cardFired = 'true';
        show(card);
      } else if (amount < trigger - .025) {
        card.dataset.cardFired = 'false';
        hide(card);
      }
    });
  }

  function requestUpdate() {
    if (frame) return;
    frame = requestAnimationFrame(update);
  }

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', measure, { passive: true });
  window.addEventListener('pageshow', measure);
  reduced.addEventListener('change', requestUpdate);
  if ('ResizeObserver' in window) new ResizeObserver(measure).observe(document.body);
  document.fonts?.ready.then(measure);
  measure();
})();
