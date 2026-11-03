(() => {
  const story = document.querySelector('.story');
  const frames = [...document.querySelectorAll('.frame')];
  const copies = [...document.querySelectorAll('.copy')];
  const number = document.querySelector('#scene-number');
  const progressFill = document.querySelector('#progress-fill');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const stops = [0, 0.25, 0.5, 0.75, 0.91];
  let scheduled = false;

  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const smoothstep = (value) => value * value * (3 - 2 * value);

  function update() {
    scheduled = false;
    const rect = story.getBoundingClientRect();
    const travel = Math.max(1, story.offsetHeight - window.innerHeight);
    const progress = clamp(-rect.top / travel, 0, 1);
    progressFill.style.width = `${progress * 100}%`;

    let current = stops.length - 1;
    for (let i = 0; i < stops.length - 1; i++) {
      if (progress < stops[i + 1]) { current = i; break; }
    }
    const next = Math.min(current + 1, frames.length - 1);
    const local = next === current ? 0 : (progress - stops[current]) / (stops[next] - stops[current]);
    const blend = reduceMotion.matches ? (local > .5 ? 1 : 0) : smoothstep(clamp((local - .72) / .28, 0, 1));

    frames.forEach((frame, index) => {
      const opacity = index === current ? 1 - blend : index === next ? blend : 0;
      frame.style.opacity = String(opacity);
      frame.style.transform = reduceMotion.matches ? 'none' : `scale(${1.025 - opacity * .025})`;
      frame.classList.toggle('is-visible', opacity > .5);
    });
    const activeCopy = blend > .5 ? next : current;
    copies.forEach((copy, index) => copy.classList.toggle('is-visible', index === activeCopy));
    number.textContent = `${String(Math.min(activeCopy + 1, 4)).padStart(2, '0')} / 04`;
  }

  function schedule() {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(update);
    }
  }

  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  reduceMotion.addEventListener('change', schedule);
  update();
})();
