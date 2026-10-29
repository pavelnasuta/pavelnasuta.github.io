from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

home = ROOT / 'index.html'
text = home.read_text(encoding='utf-8')
insert = '''<section class="content-section ai-agent-entry" id="ai-agents">
  <div class="section-head"><div><p class="section-kicker">ПРАКТИКА AI-АГЕНТОВ</p><h2>Поставить агента мало. Нужно дать ему работу.</h2><p class="section-description">Гайды и рабочие маршруты: Hermes, Telegram, VPS, память, навыки и безопасная автоматизация без обещаний магии.</p></div><a href="articles/ai-agents/index.html">Все гайды →</a></div>
  <div class="case-grid">
    <a class="case" href="articles/hermes-agent-installation/index.html"><div class="case-meta"><span>ГЛАВНЫЙ ГАЙД · 25 МИН</span></div><h3>Как установить Hermes Agent на Mac, Windows и VPS</h3><p>Выбрать Desktop или сервер, подключить Telegram и не отдать агенту лишние доступы.</p></a>
    <a class="case" href="articles/hermes-agent-telegram-vps/index.html"><div class="case-meta"><span>ПРАКТИКА · 12 МИН</span></div><h3>Hermes + Telegram на VPS: агент 24/7</h3><p>Как сделать серверный контур, который переживает закрытый ноутбук и перезагрузку.</p></a>
    <a class="case" href="articles/ai-agent-knowledge-storage/index.html"><div class="case-meta"><span>ПАМЯТЬ · 14 МИН</span></div><h3>Агенту нужно куда складывать работу</h3><p>Как связать Hermes и Anytype, чтобы результат можно было открыть, найти и использовать.</p></a>
  </div>
</section>'''
needle = '</section>\n      <section class="method author-quote">'
assert needle in text
text = text.replace(needle, '</section>\n      ' + insert + '\n      <section class="method author-quote">', 1)
home.write_text(text, encoding='utf-8')

archive = ROOT / 'articles' / 'index.html'
text = archive.read_text(encoding='utf-8')
new_list = '''<section class="list">
<a class="item" href="ai-agents/index.html"><div class="item-meta">ГАЙДЫ<br>AI-АГЕНТЫ</div><div><h2>Практика AI-агентов</h2><p>Маршруты от первого процесса и установки Hermes до устойчивого результата, который можно проверить.</p></div><span class="arrow">→</span></a>
<a class="item" href="hermes-agent-installation/index.html"><div class="item-meta">ГЛАВНЫЙ ГАЙД<br>25 МИН</div><div><h2>Как установить Hermes Agent на Mac, Windows и VPS</h2><p>Подробная инструкция для России: Desktop, Telegram, сервер, безопасность и первый сценарий.</p></div><span class="arrow">→</span></a>
<a class="item" href="hermes-agent-telegram-vps/index.html"><div class="item-meta">ПРАКТИКА<br>12 МИН</div><div><h2>Hermes + Telegram на VPS: агент 24/7</h2><p>Как сделать агент доступным в Telegram и не превратить сервер в открытую дверь.</p></div><span class="arrow">→</span></a>
<a class="item" href="ai-agent-knowledge-storage/index.html"><div class="item-meta">СТАТЬЯ<br>14 МИН</div><div><h2>Агенту нужно не только помнить. Ему нужно куда складывать работу</h2><p>Как связать Hermes и Anytype, чтобы результат работы агента можно было открыть, найти и использовать.</p></div><span class="arrow">→</span></a>
<a class="item" href="how-to-choose-an-ai-task/index.html"><div class="item-meta">СТАТЬЯ<br>8 МИН</div><div><h2>Естественный интеллект — раньше искусственного</h2><p>Как выбрать задачу для AI: проблема, гипотеза, критерий результата и цена ошибки — до инструмента.</p></div><span class="arrow">→</span></a>
<a class="item" href="how-to-verify-ai-automation/index.html"><div class="item-meta">ПРАКТИКА<br>8 МИН</div><div><h2>Как проверять результат AI-автоматизации до запуска</h2><p>Семь вопросов о качестве, человеческом контроле и стоп-условиях.</p></div><span class="arrow">→</span></a>
</section>'''
text, count = re.subn(r'<section class="list">.*?</section></main>', new_list + '</main>', text, count=1, flags=re.S)
assert count == 1
archive.write_text(text, encoding='utf-8')

sitemap = ROOT / 'sitemap.xml'
text = sitemap.read_text(encoding='utf-8')
for route in ('articles/ai-agents/', 'articles/hermes-agent-installation/', 'articles/hermes-agent-telegram-vps/'):
    url = f'https://nasuta.ru/{route}'
    if url not in text:
        text = text.replace('</urlset>', f'  <url><loc>{url}</loc><lastmod>2026-10-29</lastmod></url>\n</urlset>')
sitemap.write_text(text, encoding='utf-8')

# New pages use the site-wide header/footer maintained by the repository tools.
