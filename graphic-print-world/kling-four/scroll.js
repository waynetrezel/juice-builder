(() => {
  const chapters = [...document.querySelectorAll('.film-chapter')];
  const textTargets = [...document.querySelectorAll('.film-chapter, .story-panel')];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = (n) => Math.max(0, Math.min(1, n));
  let scheduled = false;

  function update() {
    scheduled = false;
    const height = window.innerHeight;
    for (const chapter of chapters) {
      const rect = chapter.getBoundingClientRect();
      const progress = clamp(-rect.top / Math.max(1, rect.height - height));
      const progressBar = chapter.querySelector('.chapter-progress');
      const progressFill = progressBar ? progressBar.querySelector('span') : null;
      if (progressFill) progressFill.style.width = `${progress * 100}%`;
      if (progressBar) progressBar.classList.toggle('is-complete', progress >= 0.999);
      const video = chapter.querySelector('video');
      if (reduced.matches || !chapter.classList.contains('has-video') || !video || !Number.isFinite(video.duration)) continue;
      const target = progress * Math.max(0, video.duration - 0.04);
      if (!video.seeking && Math.abs(video.currentTime - target) > 1 / 30) video.currentTime = target;
    }
  }

  const textObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) entry.target.classList.add('is-visible');
    }
  }, { threshold: 0.12 });
  textTargets.forEach((target) => textObserver.observe(target));

  function schedule() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(update);
  }

  // The files are optional until the four approved Kling exports are available.
  if (!reduced.matches) {
    fetch('./videos/manifest.json')
      .then((response) => response.json())
      .then((manifest) => {
        const available = new Set(manifest.clips);
        const observer = new IntersectionObserver((entries) => {
          for (const entry of entries) {
            if (!entry.isIntersecting) continue;
            const chapter = entry.target;
            observer.unobserve(chapter);
            // A Blob URL lets the local preview seek even on servers without HTTP Range support.
            fetch(chapter.dataset.video).then((response) => response.blob()).then((blob) => {
              const url = URL.createObjectURL(blob);
              const video = chapter.querySelector('video');
              video.src = url;
              video.preload = 'metadata';
              video.addEventListener('loadeddata', () => { chapter.classList.add('has-video'); schedule(); }, { once: true });
              video.addEventListener('seeked', schedule);
              video.addEventListener('error', () => chapter.classList.remove('has-video'));
            });
          }
        }, { rootMargin: '120% 0px' });
        chapters.forEach((chapter, index) => {
          if (!available.has(index + 1)) return;
          observer.observe(chapter);
        });
      });
  }

  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  reduced.addEventListener('change', () => location.reload());
  schedule();
})();
