(() => {
  const layer = document.querySelector('#route-parallax');
  const svg = layer?.querySelector('.route-parallax-line');
  const path = document.querySelector('#route-parallax-path');
  const underlay = document.querySelector('.route-parallax-underlay');
  const revealMask = document.querySelector('#route-parallax-mask');
  const markerLayer = document.querySelector('#route-parallax-markers');
  const bottle = document.querySelector('.route-parallax-bottle');
  const imagine = document.querySelector('#imagine');
  const discover = document.querySelector('#discover');
  const decide = document.querySelector('#decide');
  const make = document.querySelector('#make');
  if (!layer || !svg || !path || !underlay || !revealMask || !markerLayer || !bottle || !imagine || !discover || !decide || !make) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
  let range = { start: 0, end: 1 };
  let length = 1;
  let frame = 0;
  let markers = [];

  const absTop = (element) => element.getBoundingClientRect().top + window.scrollY;
  const absBottom = (element) => element.getBoundingClientRect().bottom + window.scrollY;

  function pointPath(width, start, end) {
    const x = (ratio) => Math.round(width * ratio);
    const y = (absoluteY) => Math.round(clamp((absoluteY - start) / Math.max(1, end - start), 0, 1) * 1000);
    const discoverBottom = absBottom(discover);
    const decideBottom = absBottom(decide);
    const makeTop = absTop(make);
    const makeBottom = absBottom(make);
    return [
      `M ${x(.82)} ${y(start + 100)}`,
      `L ${x(.97)} ${y(start + 100)}`,
      `L ${x(.97)} ${y(discoverBottom - 90)}`,
      `L ${x(.04)} ${y(discoverBottom - 90)}`,
      `L ${x(.04)} ${y(decideBottom - 90)}`,
      `L ${x(.96)} ${y(decideBottom - 90)}`,
      `L ${x(.96)} ${y(makeTop + 220)}`,
      `L ${x(.04)} ${y(makeTop + 220)}`,
      `L ${x(.04)} ${y(makeBottom - 320)}`,
      `L ${x(.36)} ${y(makeBottom - 320)}`,
      `L ${x(.36)} ${y(end - 60)}`,
    ].join(' ');
  }

  function buildMarkers() {
    markerLayer.replaceChildren();
    markers = Array.from({ length: 10 }, (_, index) => {
      const node = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      node.classList.add('route-parallax-marker');
      const distance = length * ((index + 1) / 11);
      const point = path.getPointAtLength(distance);
      node.setAttribute('cx', point.x);
      node.setAttribute('cy', point.y);
      node.setAttribute('r', index % 3 === 0 ? '7' : '5');
      markerLayer.append(node);
      return { node, distance };
    });
  }

  function measure() {
    const imagineBottom = absBottom(imagine);
    const makeBottom = absBottom(make);
    range = {
      start: imagineBottom - window.innerHeight,
      end: Math.max(imagineBottom + 1, makeBottom - window.innerHeight * .15),
    };

    const width = Math.max(1, document.documentElement.clientWidth);
    const height = Math.max(1, range.end - range.start);
    const definition = pointPath(width, range.start, range.end);
    layer.style.top = `${range.start}px`;
    layer.style.height = `${height}px`;
    svg.setAttribute('viewBox', `0 0 ${width} 1000`);
    revealMask.setAttribute('x', '0');
    revealMask.setAttribute('y', '0');
    revealMask.setAttribute('width', String(width));
    revealMask.setAttribute('height', '1000');
    path.setAttribute('d', definition);
    underlay.setAttribute('d', definition);
    revealMask.setAttribute('d', definition);
    length = path.getTotalLength();
    revealMask.style.strokeDasharray = `0 ${length}`;
    buildMarkers();
    update();
  }

  function update() {
    frame = 0;
    if (reduced.matches) {
      layer.dataset.active = 'false';
      return;
    }

    const rawProgress = (window.scrollY - range.start) / Math.max(1, range.end - range.start);
    const progress = clamp(rawProgress);
    const active = rawProgress >= 0 && rawProgress < 1;
    layer.dataset.active = active ? 'true' : 'false';
    if (!active) {
      revealMask.style.strokeDashoffset = `${length}`;
      markers.forEach(({ node }) => { node.style.opacity = '0'; });
      return;
    }

    const eased = progress * progress * (3 - 2 * progress);
    const distance = length * eased;
    // A single leading dash reveals the route from its document-space origin.
    // This avoids the reversed/hidden segment behaviour of animating dashoffset
    // on a full-length mask path in Chromium.
    revealMask.style.strokeDasharray = `${distance} ${length}`;
    revealMask.style.strokeDashoffset = '0';
    markers.forEach(({ node, distance: markerDistance }) => {
      node.style.opacity = distance >= markerDistance ? '1' : '0';
    });

    const point = path.getPointAtLength(distance);
    bottle.style.transform = `translate3d(${point.x}px,${(point.y / 1000) * layer.offsetHeight}px,0) translate(-50%,-50%)`;
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
