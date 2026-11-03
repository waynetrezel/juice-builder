(() => {
  const story = document.querySelector('#story');
  const stage = document.querySelector('.stage');
  const svg = document.querySelector('#paper-art');
  const copies = [...document.querySelectorAll('.copy')];
  const sceneNumber = document.querySelector('#scene-number');
  const progressFill = document.querySelector('#progress-fill');
  const scrollCue = document.querySelector('.scroll-cue');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const get = (id) => document.getElementById(id);
  const layers = {
    profile: get('profile'), orange: get('idea-orange'), kiwi: get('idea-kiwi'),
    leaves: get('idea-leaves'), card: get('idea-card'), ideas: get('ideas'),
    bottle: get('bottle-motion'), bottleArt: get('bottle-art'), bottleFinal: get('bottle-final'),
    bottleOpen: get('bottle-open'), liquid: get('liquid'), liquidDots: get('liquid-dots'),
    label: get('label-wrap'), cap: get('cap'), marks: get('print-marks'),
    proofs: get('proofs'), labelHand: get('label-hand'), sipHands: get('sip-hands'), person: get('sip-person'),
    table: get('table-strip')
  };
  let scheduled = false;

  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
  const segment = (value, start, end) => clamp((value - start) / (end - start));
  const ease = (value) => value * value * (3 - 2 * value);
  const mix = (start, end, amount) => start + (end - start) * amount;
  const opacity = (element, value) => element.setAttribute('opacity', clamp(value).toFixed(3));
  const number = (value) => Math.round(value * 100) / 100;

  function update() {
    scheduled = false;
    const rect = story.getBoundingClientRect();
    const travel = Math.max(1, story.offsetHeight - window.innerHeight);
    const scrollProgress = clamp(-rect.top / travel);
    const p = reduced.matches
      ? scrollProgress < .26 ? .12 : scrollProgress < .56 ? .54 : scrollProgress < .77 ? .71 : scrollProgress < .94 ? .86 : .99
      : scrollProgress;
    const ideaExit = ease(segment(p, .18, .39));
    const bottleEnter = ease(segment(p, .17, .42));
    const fill = ease(segment(p, .37, .55));
    const labelEnter = ease(segment(p, .55, .68));
    const sipEnter = ease(segment(p, .75, .83));
    const sipExit = ease(segment(p, .88, .96));
    const sipAngle = mix(0, 58, ease(segment(p, .78, .85))) * (1 - ease(segment(p, .86, .94)));
    const finalSettle = ease(segment(p, .89, .96));

    opacity(layers.profile, 1 - ideaExit);
    layers.profile.setAttribute('transform', `translate(${number(-290 * ideaExit)} 0)`);
    opacity(layers.ideas, 1 - ease(segment(p, .22, .39)));
    layers.orange.setAttribute('transform', `translate(${number(-60 * ideaExit)} ${number(35 * ideaExit)}) translate(1110 266) scale(.78)`);
    layers.kiwi.setAttribute('transform', `translate(${number(-125 * ideaExit)} ${number(70 * ideaExit)}) translate(1260 395) scale(.73)`);
    layers.leaves.setAttribute('transform', `translate(${number(-100 * ideaExit)} ${number(-55 * ideaExit)}) translate(1170 594)`);
    layers.card.setAttribute('transform', `translate(${number(-185 * ideaExit)} ${number(-25 * ideaExit)}) translate(1345 458) rotate(9)`);

    opacity(layers.bottle, ease(segment(p, .18, .3)));
    const scale = mix(.23, 1.2, bottleEnter);
    const bottleCx = mix(1360, 1150, bottleEnter) - 47 * sipAngle / 58;
    const bottleCy = mix(455, 475, bottleEnter) + 21 * finalSettle;
    layers.bottle.setAttribute('transform', `translate(${number(bottleCx)} ${number(bottleCy)}) rotate(${number(sipAngle)}) scale(${number(scale)}) translate(-130 -320)`);

    const liquidHeight = 352 * fill;
    for (const element of [layers.liquid, layers.liquidDots]) {
      element.setAttribute('y', number(583 - liquidHeight));
      element.setAttribute('height', number(liquidHeight));
    }
    opacity(layers.label, labelEnter);
    layers.label.setAttribute('transform', `translate(${number(180 * (1 - labelEnter))} 0)`);
    opacity(layers.cap, 1 - ease(segment(p, .79, .83)) * (1 - ease(segment(p, .92, .97))));
    const texturedBottle = ease(segment(p, .61, .7));
    const openBottle = ease(segment(p, .79, .84)) * (1 - ease(segment(p, .91, .96)));
    opacity(layers.bottleArt, 1 - texturedBottle);
    opacity(layers.bottleFinal, texturedBottle * (1 - openBottle));
    opacity(layers.bottleOpen, texturedBottle * openBottle);

    opacity(layers.marks, ease(segment(p, .32, .49)) * (1 - ease(segment(p, .88, .98))));
    opacity(layers.proofs, ease(segment(p, .49, .61)) * (1 - ease(segment(p, .72, .84))));
    layers.proofs.setAttribute('transform', `translate(${number(65 * (1 - labelEnter))} 0)`);
    opacity(layers.labelHand, ease(segment(p, .58, .67)) * (1 - ease(segment(p, .7, .78))));
    layers.labelHand.setAttribute('transform', `translate(${number(320 * (1 - labelEnter))} 0)`);
    opacity(layers.person, sipEnter * (1 - sipExit));
    layers.person.setAttribute('transform', `translate(${number(400 * (1 - sipEnter))} 0)`);
    opacity(layers.sipHands, sipEnter * (1 - sipExit));
    layers.sipHands.setAttribute('transform', `translate(${number(250 * (1 - sipEnter))} 0) rotate(-20 1000 600)`);
    opacity(layers.table, finalSettle);

    const chapter = scrollProgress < .26 ? 0 : scrollProgress < .56 ? 1 : scrollProgress < .77 ? 2 : scrollProgress < .94 ? 3 : 4;
    copies.forEach((copy, index) => copy.classList.toggle('is-visible', index === chapter));
    sceneNumber.textContent = `${String(Math.min(chapter + 1, 4)).padStart(2, '0')} / 04`;
    progressFill.style.width = `${scrollProgress * 100}%`;
    scrollCue.style.opacity = String(1 - ease(segment(scrollProgress, .03, .23)));
    stage.classList.toggle('is-scrolling', scrollProgress > .01);
  }

  function schedule() {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(update);
    }
  }

  function responsiveArt() {
    svg.setAttribute('preserveAspectRatio', window.innerWidth < 600 ? 'xMaxYMid slice' : 'xMidYMid slice');
    schedule();
  }

  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', responsiveArt);
  reduced.addEventListener('change', schedule);
  responsiveArt();
})();
