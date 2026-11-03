(() => {
  const params = new URLSearchParams(window.location.search);
  if (params.get('copy') !== 'feeling-led') return;

  const setTitle = (selector, html) => {
    const node = document.querySelector(selector);
    if (node) node.innerHTML = html;
  };
  const setCopy = (selector, text) => {
    const node = document.querySelector(selector);
    if (node) node.textContent = text;
  };

  setTitle('#title-imagine', '<span class="title-line title-line-left">Start with a feeling.</span><br><span class="title-line title-line-right">Make it <em>yours.</em></span>');
  setCopy('#imagine .story-copy > p:last-child', 'Begin with the feeling you want from your drink, then turn that instinct into something made for you.');

  setTitle('#title-discover', 'Find your spark.<br><em>Make it yours.</em>');
  setCopy('#discover .panel-copy > p:last-child', 'A flavour, ritual, or wellbeing idea catches your eye. Bring the inspiration and we will help shape it around you.');

  setTitle('#title-decide', 'Choose your blend.<br><em>Choose your balance.</em>');
  setCopy('#decide .panel-copy > p:last-child', 'Pick ingredients for the taste you love, the benefits you seek, and the way you want your drink to fit into everyday life.');

  setTitle('#title-make', 'Bring it<br>to <em>life.</em>');
  setCopy('#make .story-copy > p:last-child', 'Your choices become a fresh, bespoke drink, prepared with care from the first pour to the final bottle.');

  setTitle('#title-delivery', 'Made around you.<br>On its <em>way.</em>');
  setCopy('#delivery .panel-copy > p:last-child', 'Your finished drink is prepared, sealed, and sent straight from the workshop to your door.');

  setTitle('#title-sip', 'Meet your<br><em>moment.</em>');
  setCopy('#sip .story-copy > p:last-child', 'A personalised drink, ready for the pause, ritual, or reset you had in mind.');

  setTitle('#title-enjoy', 'Made for<br><em>your rhythm.</em>');
  setCopy('#enjoy .story-copy > p:last-child', 'A drink that starts with your idea and fits the way you choose to live.');

  document.body.dataset.copyVariant = 'feeling-led';
})();
