(() => {
  const navigation = document.querySelector('[data-site-navigation="global"]');
  if (!navigation) return;

  const toggle = navigation.querySelector('.site-navigation__toggle');
  const panel = navigation.querySelector('.site-navigation__panel');
  if (!toggle || !panel) return;

  const close = () => {
    navigation.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', () => {
    const opening = !navigation.classList.contains('is-open');
    navigation.classList.toggle('is-open', opening);
    toggle.setAttribute('aria-expanded', String(opening));
  });

  panel.addEventListener('click', (event) => {
    if (event.target.closest('a')) close();
  });

  window.addEventListener('resize', () => {
    if (window.matchMedia('(min-width: 861px)').matches) close();
  });
})();
