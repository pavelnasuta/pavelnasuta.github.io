"""Shared sitewide footer for every static route."""

STYLESHEET = '<link rel="stylesheet" href="/assets/styles/footer.css">'

SITE_FOOTER = '''<footer class="site-footer" data-site-footer="global">
  <div class="site-footer__grid">
    <div class="site-footer__brand">
      <a class="site-footer__name" href="/">Павел Насута</a>
      <p>Product builder · AI-агенты · автоматизация</p>
    </div>
    <nav class="site-footer__group" aria-label="Навигация в подвале">
      <h2>Разделы</h2>
      <a href="/articles/">Блог</a>
      <a href="/skills/">Skills для AI-агентов</a>
      <a href="/create/">Framework C.R.E.A.T.E.</a>
      <a href="/biases/">Когнитивные искажения</a>
      <a href="/about/">Обо мне</a>
    </nav>
    <nav class="site-footer__group" aria-label="Проекты">
      <h2>Проекты</h2>
      <a href="https://menhausen.com/" target="_blank" rel="noopener">Menhausen ↗</a>
      <a href="/pomokitty/">pomokitty</a>
      <a href="/create/">C.R.E.A.T.E.</a>
    </nav>
    <nav class="site-footer__group" aria-label="Связь">
      <h2>Связь</h2>
      <a href="/contact/">Все способы связи</a>
      <a href="https://t.me/niimozgii" target="_blank" rel="noopener">Telegram ↗</a>
      <a href="https://www.linkedin.com/in/nasuta" target="_blank" rel="noopener">LinkedIn ↗</a>
      <a href="https://github.com/pavelnasuta" target="_blank" rel="noopener">GitHub ↗</a>
      <a href="mailto:pavelnasuta@gmail.com">Email</a>
    </nav>
  </div>
  <div class="site-footer__bottom">
    <span>© 2026 Павел Насута</span>
    <a href="/contact/">Написать</a>
  </div>
</footer>'''
