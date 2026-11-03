import { chapters, getProgress, SEQUENCE_FRAME_COUNT } from './story-data.js?v=8';

const copy = document.querySelector('#chapters');
const stage = document.querySelector('.story-stage');
const list = document.querySelector('#ingredient-list');
const chapterElements = [];
const animaticMode = new URLSearchParams(window.location.search).get('animatic') === '1';
const stageImage = stage.querySelector('.stage-image');
const animaticBadge = document.querySelector('.animatic-badge');
if (animaticMode) {
  stage.classList.add('is-animatic');
  animaticBadge.hidden = false;
  stage.querySelector('.stage-series').textContent = 'JUICEBUILDER / STORY ANIMATIC';
}

copy.innerHTML = chapters.map((chapter, index) => `
  <article class="chapter" data-chapter="${chapter.id}" data-index="${index}" aria-labelledby="chapter-${chapter.id}">
    <div class="chapter-inner">
      <p class="eyebrow"><span class="eyebrow-line"></span>${chapter.kicker}</p>
      <h2 id="chapter-${chapter.id}">${chapter.title}<br /><em>${chapter.emphasis}</em></h2>
      <p class="chapter-body">${chapter.body}</p>
      ${chapter.ingredient ? `<span class="chapter-side-note">INGREDIENT / ${chapter.ingredientNumber}</span>` : ''}
    </div>
  </article>`).join('');
chapterElements.push(...copy.querySelectorAll('.chapter'));

list.innerHTML = chapters.filter(({ ingredient }) => ingredient).map(({ ingredient, ingredientNumber }) => `
  <li><span>${ingredientNumber}</span><strong>${ingredient}</strong><i aria-hidden="true">↗</i></li>`).join('');

const counter = stage.querySelector('.stage-counter');
const current = stage.querySelector('.stage-current');
const percent = stage.querySelector('.stage-percent');
const progress = stage.querySelector('.stage-line i');
const caption = stage.querySelector('.stage-caption');
let activeIndex = -1;
let activeSequenceFrame = -1;
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function activate(index) {
  const chapter = chapters[index];
  if (!chapter || activeIndex === index) return;
  activeIndex = index;
  chapterElements.forEach((element, chapterIndex) => {
    element.classList.toggle('is-active', chapterIndex === index);
    if (chapterIndex === index) element.setAttribute('aria-current', 'step');
    else element.removeAttribute('aria-current');
  });
  stage.dataset.frame = chapter.frame;
  if (animaticMode) {
    activeSequenceFrame = -1;
    stageImage.setAttribute('aria-label', `Blender scroll sequence: ${chapter.ingredient || chapter.kicker}`);
  }
  counter.innerHTML = `${chapter.number} <i>/</i> ${String(chapters.length).padStart(2, '0')}`;
  current.textContent = chapter.kicker.toUpperCase();
  const amount = getProgress(index, chapters.length);
  percent.textContent = `${String(amount).padStart(2, '0')}%`;
  progress.style.width = `${amount}%`;
  caption.classList.remove('caption-in');
  requestAnimationFrame(() => caption.classList.add('caption-in'));
}

let scrollQueued = false;
function syncChapterToScroll() {
  const viewportCenter = window.innerHeight / 2;
  let nearestIndex = 0;
  let nearestDistance = Infinity;
  chapterElements.forEach((chapter, index) => {
    const bounds = chapter.getBoundingClientRect();
    const distance = Math.abs((bounds.top + bounds.bottom) / 2 - viewportCenter);
    if (distance < nearestDistance) {
      nearestDistance = distance;
      nearestIndex = index;
    }
  });
  activate(nearestIndex);
  if (animaticMode) {
    const centers = chapterElements.map((chapter) => {
      const bounds = chapter.getBoundingClientRect();
      return bounds.top + window.scrollY + bounds.height / 2;
    });
    const storyPoint = window.scrollY + viewportCenter;
    let storyProgress = 0;
    if (storyPoint >= centers[centers.length - 1]) storyProgress = 1;
    else if (storyPoint > centers[0]) {
      const segment = centers.findIndex((center, index) => index < centers.length - 1 && storyPoint <= centers[index + 1]);
      if (segment >= 0) {
        const segmentProgress = (storyPoint - centers[segment]) / (centers[segment + 1] - centers[segment]);
        storyProgress = (segment + segmentProgress) / (centers.length - 1);
      }
    }
    let sequenceFrame = chapters[0].sequenceFrame;
    if (prefersReducedMotion.matches) {
      sequenceFrame = chapters[nearestIndex].sequenceFrame;
    } else if (storyPoint >= centers[centers.length - 1]) {
      sequenceFrame = SEQUENCE_FRAME_COUNT - 1;
    } else if (storyPoint > centers[0]) {
      const segment = centers.findIndex((center, index) => index < centers.length - 1 && storyPoint <= centers[index + 1]);
      if (segment >= 0) {
        const segmentProgress = (storyPoint - centers[segment]) / (centers[segment + 1] - centers[segment]);
        const frameStart = chapters[segment].sequenceFrame;
        const frameEnd = chapters[segment + 1].sequenceFrame;
        sequenceFrame = frameStart + (frameEnd - frameStart) * segmentProgress;
      }
    }
    const frameIndex = Math.max(0, Math.min(SEQUENCE_FRAME_COUNT - 1, Math.round(sequenceFrame)));
    if (frameIndex !== activeSequenceFrame) {
      activeSequenceFrame = frameIndex;
      const filename = `frame-${String(frameIndex).padStart(3, '0')}.webp`;
      stageImage.style.backgroundImage = `url('./assets/sequence/${filename}?v=6')`;
      const ahead = new Image();
      const nextIndex = Math.min(SEQUENCE_FRAME_COUNT - 1, frameIndex + 1);
      ahead.src = `./assets/sequence/frame-${String(nextIndex).padStart(3, '0')}.webp?v=6`;
    }
    const amount = Math.round(storyProgress * 100);
    percent.textContent = `${String(amount).padStart(2, '0')}%`;
    progress.style.width = `${amount}%`;
  }
}

window.addEventListener('scroll', () => {
  if (scrollQueued) return;
  scrollQueued = true;
  requestAnimationFrame(() => {
    syncChapterToScroll();
    scrollQueued = false;
  });
}, { passive: true });
window.addEventListener('resize', syncChapterToScroll, { passive: true });
syncChapterToScroll();

document.documentElement.classList.add('story-ready');
