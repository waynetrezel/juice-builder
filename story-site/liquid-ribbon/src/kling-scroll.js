const story = document.querySelector('#kling-story');
const frame = document.querySelector('#kling-frame');
const timeLabel = document.querySelector('#kling-time');
const chapters = [...document.querySelectorAll('.kling-chapters article')];
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Direct mapping is intentional: every scroll target maps to a concrete frame.
// The current 12fps extraction is sampled at 6fps here to restore the earlier
// non-eased behavior without regenerating the source assets.
const frameCount = 121;
const duration = 20.04;
const frameRoot = './assets/processed/kling-frames/';
const cache = new Map();
const preloadRadius = 8;
let targetFrame = 0;
let lastPrefetchFrame = -1;
let raf = 0;

function framePath(index) {
  const sourceIndex = index * 2;
  return `${frameRoot}frame-${String(sourceIndex + 1).padStart(3, '0')}.webp`;
}

function formatTime(seconds) {
  const safe = Math.max(0, Number.isFinite(seconds) ? seconds : 0);
  return `00:${String(Math.floor(safe)).padStart(2, '0')}`;
}

function loadFrame(index) {
  if (index < 0 || index >= frameCount) return null;
  if (cache.has(index)) return cache.get(index);
  const image = new Image();
  image.decoding = 'async';
  image.src = framePath(index);
  cache.set(index, image);
  image.onload = () => {
    if (targetFrame === index) frame.src = image.src;
  };
  return image;
}

function prefetchAround(index) {
  if (Math.abs(index - lastPrefetchFrame) < 2) return;
  lastPrefetchFrame = index;
  loadFrame(index);
  for (let offset = 1; offset <= preloadRadius; offset += 1) {
    loadFrame(index - offset);
    loadFrame(index + offset);
  }
  for (const [cachedIndex, image] of cache) {
    if (Math.abs(cachedIndex - index) > preloadRadius * 2 && image.complete) cache.delete(cachedIndex);
  }
}

function paint() {
  raf = 0;
  const range = Math.max(1, story.offsetHeight - window.innerHeight);
  const progress = Math.min(1, Math.max(0, (window.scrollY - story.offsetTop) / range));
  const nextFrame = reduceMotion ? 0 : Math.round(progress * (frameCount - 1));
  targetFrame = nextFrame;
  prefetchAround(nextFrame);
  const image = loadFrame(nextFrame);
  if (image.complete && image.naturalWidth) frame.src = image.src;
  const activeChapter = chapters.reduce((last, chapter, index) => progress >= Number(chapter.dataset.start) ? index : last, 0);
  chapters.forEach((chapter, index) => chapter.classList.toggle('is-active', index === activeChapter));
  timeLabel.textContent = formatTime(progress * duration);
}

function requestPaint() {
  if (!raf) raf = requestAnimationFrame(paint);
}

window.addEventListener('scroll', requestPaint, { passive: true });
window.addEventListener('resize', requestPaint);
if (new URLSearchParams(window.location.search).get('bg') !== 'warm') {
  document.body.classList.add('kling-black');
} else {
  document.body.classList.add('kling-warm');
}
loadFrame(0);
loadFrame(frameCount - 1);
requestPaint();
