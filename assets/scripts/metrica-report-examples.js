(() => {
  for (const carousel of document.querySelectorAll('[data-report-carousel]')) {
    const track = carousel.querySelector('[data-carousel-track]');
    const previous = carousel.querySelector('[data-carousel-prev]');
    const next = carousel.querySelector('[data-carousel-next]');
    const status = carousel.querySelector('[data-carousel-status]');
    const slides = [...track.querySelectorAll('[data-carousel-slide]')];
    let index = 0;

    const update = () => {
      const active = Math.max(0, Math.min(slides.length - 1, index));
      index = active;
      track.scrollTo({left: slides[active].offsetLeft - track.offsetLeft, behavior: 'auto'});
      status.textContent = `${active + 1} из ${slides.length}`;
      previous.disabled = active === 0;
      next.disabled = active === slides.length - 1;
    };

    previous.addEventListener('click', () => { index -= 1; update(); });
    next.addEventListener('click', () => { index += 1; update(); });
    track.addEventListener('scroll', () => {
      const left = track.scrollLeft;
      index = slides.reduce((best, slide, current) =>
        Math.abs(slide.offsetLeft - left) < Math.abs(slides[best].offsetLeft - left) ? current : best, 0);
      status.textContent = `${index + 1} из ${slides.length}`;
      previous.disabled = index === 0;
      next.disabled = index === slides.length - 1;
    }, {passive: true});
    update();
  }
})();
