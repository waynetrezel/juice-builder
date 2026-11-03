const story = document.querySelector('#scroll-story');
const image = document.querySelector('#story-frame');
const progressFill = document.querySelector('#progress-fill');
const progressNumber = document.querySelector('#progress-number');
const count = document.querySelector('#scene-count');
const kicker = document.querySelector('#scene-kicker');
const title = document.querySelector('#scene-title');
const description = document.querySelector('#scene-description');

const frameCount = 72;
const chapters = [
  { start: 0, frame: 9, kicker: 'THE INTRODUCTION', title: 'Meet the kiwi.', description: 'Fresh, vivid, and ready for its moment.' },
  { start: .24, frame: 25, kicker: 'THE REVEAL', title: 'Look inside.', description: 'A bright cut face reveals the detail within.' },
  { start: .50, frame: 43, kicker: 'THE MOVEMENT', title: 'Into the blender.', description: 'Small pieces spiral down into the pitcher.' },
  { start: .70, frame: 52, kicker: 'THE TRANSFORMATION', title: 'Made into juice.', description: 'The blades turn and a fresh green whirl rises.' },
  { start: .86, frame: 71, kicker: 'THE FINISH', title: 'Ready to pour.', description: 'A fresh green drink settles into two bottles.' },
];

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const urlFor = (index) => `./assets/kiwi/scroll/frame-${String(index).padStart(3, '0')}.webp?v=6`;
const cache = new Map();
let requestedFrame = 0;
let shownChapter = -1;
let queued = false;

function loadFrame(index) {
  if (index < 0 || index >= frameCount || cache.has(index)) return;
  const preloaded = new Image();
  preloaded.decoding = 'async';
  preloaded.src = urlFor(index);
  cache.set(index, preloaded);
  preloaded.addEventListener('load', () => {
    if (requestedFrame === index) image.src = preloaded.src;
  }, { once: true });
  // Decoded images are expensive on mobile; the browser still caches the files.
  if (cache.size > 14) cache.delete(cache.keys().next().value);
}

function chapterAt(progress) {
  for (let index = chapters.length - 1; index >= 0; index -= 1) {
    if (progress >= chapters[index].start) return index;
  }
  return 0;
}

function update() {
  queued = false;
  const start = story.getBoundingClientRect().top + window.scrollY;
  const length = Math.max(1, story.offsetHeight - window.innerHeight);
  const progress = Math.max(0, Math.min(1, (window.scrollY - start) / length));
  const chapterIndex = chapterAt(progress);
  const chapter = chapters[chapterIndex];
  const frame = reducedMotion.matches ? chapter.frame : Math.round(progress * (frameCount - 1));

  if (frame !== requestedFrame) {
    requestedFrame = frame;
    loadFrame(frame);
    const cached = cache.get(frame);
    if (cached?.complete && cached.naturalWidth) image.src = cached.src;
    if (!reducedMotion.matches) {
      for (let offset = -2; offset <= 3; offset += 1) loadFrame(frame + offset);
    }
  }

  if (chapterIndex !== shownChapter) {
    shownChapter = chapterIndex;
    kicker.textContent = chapter.kicker;
    title.textContent = chapter.title;
    description.textContent = chapter.description;
    count.textContent = `${String(chapterIndex + 1).padStart(2, '0')} / 04`;
  }
  progressFill.style.width = `${Math.round(progress * 100)}%`;
  progressNumber.textContent = `${String(Math.round(progress * 100)).padStart(2, '0')}%`;
}

function requestUpdate() {
  if (!queued) {
    queued = true;
    window.requestAnimationFrame(update);
  }
}

loadFrame(0);
loadFrame(1);
loadFrame(2);
window.addEventListener('scroll', requestUpdate, { passive: true });
window.addEventListener('resize', requestUpdate);
reducedMotion.addEventListener('change', requestUpdate);
requestUpdate();
