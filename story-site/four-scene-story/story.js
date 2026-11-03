const scenes = [...document.querySelectorAll('.scene')];
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let frameRequested = false;

function clamp(value) {
  return Math.max(0, Math.min(1, value));
}

function progressFor(scene) {
  const distance = Math.max(1, scene.offsetHeight - window.innerHeight);
  return clamp((window.scrollY - scene.offsetTop) / distance);
}

function paint() {
  frameRequested = false;

  for (const scene of scenes) {
    const progress = progressFor(scene);
    scene.style.setProperty('--progress', progress.toFixed(4));

    if (!reduceMotion) {
      const fadeIn = clamp(progress / .08);
      const fadeOut = scene.classList.contains('scene-final') ? 1 : clamp((1 - progress) / .08);
      scene.style.setProperty('--image-opacity', Math.min(fadeIn, fadeOut).toFixed(3));
      scene.style.setProperty('--art-scale', (1 + progress * .045).toFixed(4));
      scene.style.setProperty('--drift-x', `${((progress - .5) * 12).toFixed(1)}px`);
      if (scene.classList.contains('scene-final')) {
        scene.style.setProperty('--end-opacity', clamp((progress - .58) / .2).toFixed(3));
      }
    }

    const video = scene.querySelector('.scene-video');
    if (video?.readyState >= HTMLMediaElement.HAVE_METADATA && !reduceMotion) {
      const target = Math.min(Math.max(0, video.duration - .03), progress * video.duration);
      if (Math.abs(video.currentTime - target) > .04) video.currentTime = target;
    }
  }
}

function requestPaint() {
  if (!frameRequested) {
    frameRequested = true;
    requestAnimationFrame(paint);
  }
}

const observer = new IntersectionObserver(entries => {
  for (const entry of entries) {
    if (!entry.isIntersecting || reduceMotion) continue;
    const scene = entry.target;
    const video = scene.querySelector('.scene-video');
    const source = video?.dataset.videoSrc;
    if (!source || video.src) continue;
    video.src = source;
    video.load();
    video.addEventListener('loadeddata', () => {
      video.classList.add('is-ready');
      scene.classList.add('has-video');
      requestPaint();
    }, { once: true });
  }
}, { rootMargin: '100% 0px' });

scenes.forEach(scene => observer.observe(scene));
window.addEventListener('scroll', requestPaint, { passive: true });
window.addEventListener('resize', requestPaint);
requestPaint();
