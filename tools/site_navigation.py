"""Shared responsive navigation for every public static route."""

STYLESHEET = '<link rel="stylesheet" href="/assets/styles/navigation.css?v=contacts-nav">'
LEGACY_STYLESHEET = '<link rel="stylesheet" href="/assets/styles/navigation.css">'
SCRIPT = '<script defer src="/assets/scripts/navigation.js"></script>'

SITE_NAVIGATION = '''<nav class="site-navigation" data-site-navigation="global" aria-label="Основная навигация">
  <div class="site-navigation__inner">
    <a class="site-navigation__brand" href="/">Павел Насута</a>
    <button class="site-navigation__toggle" type="button" aria-controls="site-navigation-panel" aria-expanded="false">
      <span class="site-navigation__toggle-label">Меню</span><span class="site-navigation__toggle-icon" aria-hidden="true"></span>
    </button>
    <div class="site-navigation__panel" id="site-navigation-panel">
      <a href="/articles/">Блог</a>
      <a href="/articles/hermes-agent-installation/">Установка Hermes</a>
      <details class="site-navigation__group">
        <summary class="site-navigation__submenu-toggle">Библиотека <span aria-hidden="true">⌄</span></summary>
        <div class="site-navigation__submenu">
          <a href="/skills/" aria-label="Открыть каталог Skills для AI-агентов">Skills для AI-агентов</a>
          <a href="/biases/">Когнитивные искажения</a>
        </div>
      </details>
      <a href="/create/">C.R.E.A.T.E.</a>
      <details class="site-navigation__group">
        <summary class="site-navigation__submenu-toggle">Проекты <span aria-hidden="true">⌄</span></summary>
        <div class="site-navigation__submenu">
          <a href="https://menhausen.com/" target="_blank" rel="noopener">Menhausen ↗</a>
          <a href="/pomokitty/">pomokitty</a>
        </div>
      </details>
      <a href="/about/">Обо мне</a>
      <details class="site-navigation__group site-navigation__group--contacts">
        <summary class="site-navigation__submenu-toggle">Контакты <span aria-hidden="true">⌄</span></summary>
        <div class="site-navigation__submenu">
          <a href="/contact/">Все контакты</a>
          <a href="https://t.me/pavelnasuta" target="_blank" rel="noopener">Личный Telegram ↗</a>
          <a href="https://t.me/niimozgii" target="_blank" rel="noopener">НИИ «МОЗГИ» ↗</a>
          <a href="https://www.linkedin.com/in/nasuta" target="_blank" rel="noopener">LinkedIn ↗</a>
          <a href="mailto:pavelnasuta@gmail.com">Email</a>
        </div>
      </details>
    </div>
  </div>
</nav>'''
