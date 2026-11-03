(() => {
  const journey = document.querySelector('.discovery-journey');
  const discover = journey?.querySelector('#discover');
  const trail = journey?.querySelector('.ingredient-trail');
  if (!discover || !trail) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const items = [...trail.querySelectorAll('[data-trail-item]')].map((element) => ({
    element,
    x: Number(element.dataset.driftX) || 0,
    y: Number(element.dataset.driftY) || 0,
    turn: Number(element.dataset.driftTurn) || 0,
  }));
  let inView = false;
  let scheduled = false;
  let seam = -1;

  function render() {
    scheduled = false;
    if (reduced.matches || !inView) return;
    const rect = trail.getBoundingClientRect();
    const progress = Math.max(0, Math.min(1, (innerHeight - rect.top) / (innerHeight + rect.height)));
    const eased = progress * progress * (3 - 2 * progress);
    const phase = eased * 2 - 1;

    for (const { element, x, y, turn } of items) {
      element.style.setProperty('--drift-x', `${(phase * rect.height * x).toFixed(2)}px`);
      element.style.setProperty('--drift-y', `${(phase * rect.height * y).toFixed(2)}px`);
      element.style.setProperty('--drift-turn', `${(phase * turn).toFixed(2)}deg`);
    }
  }

  function schedule() {
    if (scheduled || reduced.matches || !inView) return;
    scheduled = true;
    requestAnimationFrame(render);
  }

  function measure() {
    // Attach to the actual section boundary; these decorations add no layout height.
    const nextSeam = discover.offsetHeight;
    if (nextSeam !== seam) {
      seam = nextSeam;
      journey.style.setProperty('--trail-seam', `${seam}px`);
    }
    schedule();
  }

  const visibility = new IntersectionObserver(([entry]) => {
    inView = entry.isIntersecting;
    schedule();
  }, { rootMargin: '160px 0px' });
  visibility.observe(trail);

  if ('ResizeObserver' in window) new ResizeObserver(measure).observe(discover);
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', measure, { passive: true });
  window.addEventListener('pageshow', measure);
  reduced.addEventListener('change', () => {
    if (reduced.matches) {
      for (const { element } of items) {
        element.style.removeProperty('--drift-x');
        element.style.removeProperty('--drift-y');
        element.style.removeProperty('--drift-turn');
      }
    } else schedule();
  });
  document.fonts?.ready.then(measure);
  measure();
})();
