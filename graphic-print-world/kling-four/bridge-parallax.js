(() => {
  const bridge = document.querySelector('#bridge-parallax');
  const make = document.querySelector('#make');
  const delivery = document.querySelector('#delivery');
  const props = bridge ? [...bridge.querySelectorAll('.bridge-prop')] : [];
  if (!bridge || !make || !delivery || !props.length) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
  const ease = (value) => value * value * (3 - 2 * value);
  const lerp = (a, b, t) => a + (b - a) * t;
  let range = { start: 0, end: 1 };
  let frame = 0;

  function measure() {
    // Begin only when the Deliver panel starts entering from the bottom of the viewport.
    const deliveryTop = delivery.getBoundingClientRect().top + window.scrollY;
    const start = deliveryTop - window.innerHeight;
    const end = delivery.getBoundingClientRect().bottom + window.scrollY;
    range = { start, end: Math.max(start + 1, end) };
    update();
  }

  function setProp(selector, opacity, x, y, rotate) {
    const prop = bridge.querySelector(selector);
    if (!prop) return;
    prop.style.opacity = String(clamp(opacity));
    prop.style.setProperty('--bridge-x', `${x}vw`);
    prop.style.setProperty('--bridge-y', `${y}px`);
    prop.style.setProperty('--bridge-rotate', `${rotate}deg`);
  }

  function update() {
    frame = 0;
    if (reduced.matches) {
      bridge.dataset.active = 'false';
      return;
    }

    const progress = clamp((window.scrollY - range.start) / Math.max(1, range.end - range.start));
    const active = progress > 0.01 && progress < 0.99;
    bridge.dataset.active = active ? 'true' : 'false';
    if (!active) {
      props.forEach((prop) => { prop.style.opacity = '0'; });
      return;
    }

    // A lemon rolls out from the left, crosses the open paper, then returns before delivery takes over.
    const lemonT = progress < .5 ? ease(clamp(progress / .5)) : ease(clamp((1 - progress) / .5));
    setProp('.bridge-lemon', .12 + .88 * Math.sin(Math.PI * clamp(progress / .9)), lerp(-24, 34, lemonT), Math.sin(progress * Math.PI * 2) * 8, lerp(-18, 14, lemonT));

    // The parcel begins on the right, reaches the centre, then hands off to the delivery artwork on the right.
    const parcelT = progress < .58 ? ease(clamp(progress / .58)) : ease(clamp((.98 - progress) / .4));
    setProp('.bridge-parcel', .12 + .88 * Math.sin(Math.PI * progress), lerp(30, -16, parcelT), lerp(10, -8, parcelT), lerp(9, -4, parcelT));
  }

  function schedule() {
    if (frame) return;
    frame = requestAnimationFrame(update);
  }

  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', measure, { passive: true });
  window.addEventListener('pageshow', measure);
  reduced.addEventListener('change', schedule);
  if ('ResizeObserver' in window) new ResizeObserver(measure).observe(document.body);
  document.fonts?.ready.then(measure);
  measure();
})();
