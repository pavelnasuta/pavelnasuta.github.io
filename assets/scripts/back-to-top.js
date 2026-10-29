(() => {
  const button = document.querySelector('[data-back-to-top]');
  if (!button) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let scheduled = false;

  const update = () => {
    scheduled = false;
    const pageIsLong = document.documentElement.scrollHeight > window.innerHeight * 1.5;
    const pastIntro = window.scrollY > Math.max(300, window.innerHeight * 0.6);
    button.classList.toggle('is-visible', pageIsLong && pastIntro);
  };

  const requestUpdate = () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(update);
  };

  button.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
  });

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  update();
})();
