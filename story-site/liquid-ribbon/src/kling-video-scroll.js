const story = document.querySelector('#kling-story');
const video = document.querySelector('#kling-video');
const timeLabel = document.querySelector('#kling-time');
const durationLabel = document.querySelector('#kling-duration');

let raf = 0;
let duration = 25.041667;

function clamp(value, min = 0, max = 1) {
  return Math.min(max, Math.max(min, value));
}

function formatTime(seconds) {
  const safe = Math.max(0, Number.isFinite(seconds) ? seconds : 0);
  return `00:${String(Math.floor(safe)).padStart(2, '0')}`;
}

function scrollProgress() {
  const range = Math.max(1, story.offsetHeight - window.innerHeight);
  return clamp((window.scrollY - story.offsetTop) / range);
}

function paint() {
  raf = 0;
  const progress = scrollProgress();
  const targetTime = progress * duration;

  if (video.readyState >= HTMLMediaElement.HAVE_METADATA && Math.abs(video.currentTime - targetTime) > 0.01) {
    video.currentTime = targetTime;
  }

  timeLabel.textContent = formatTime(targetTime);
}

function requestPaint() {
  if (!raf) raf = requestAnimationFrame(paint);
}

video.pause();
video.addEventListener('loadedmetadata', () => {
  if (Number.isFinite(video.duration) && video.duration > 0) duration = video.duration;
  durationLabel.textContent = formatTime(duration);
  requestPaint();
});

window.addEventListener('scroll', requestPaint, { passive: true });
window.addEventListener('resize', requestPaint);
requestPaint();
