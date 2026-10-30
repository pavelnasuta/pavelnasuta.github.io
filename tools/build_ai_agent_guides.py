from __future__ import annotations

import html
import json
import re
import subprocess
from pathlib import Path

try:
    from tools.site_back_to_top import BACK_TO_TOP, SCRIPT as BACK_TO_TOP_SCRIPT, STYLESHEET as BACK_TO_TOP_STYLESHEET
    from tools.site_footer import SITE_FOOTER, STYLESHEET as FOOTER_ASSETS
    from tools.site_navigation import SCRIPT as NAVIGATION_SCRIPT, SITE_NAVIGATION, STYLESHEET as NAVIGATION_STYLESHEET
except ModuleNotFoundError:  # Direct execution from tools/.
    from site_back_to_top import BACK_TO_TOP, SCRIPT as BACK_TO_TOP_SCRIPT, STYLESHEET as BACK_TO_TOP_STYLESHEET
    from site_footer import SITE_FOOTER, STYLESHEET as FOOTER_ASSETS
    from site_navigation import SCRIPT as NAVIGATION_SCRIPT, SITE_NAVIGATION, STYLESHEET as NAVIGATION_STYLESHEET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('/srv/hermes-artifacts/projects/nasuta-hermes-guide/2026-10-29-hermes-agent-setup-guide.md')
DATE = '2026-10-29'

SHARED_ASSETS = f'''{NAVIGATION_STYLESHEET}
  {NAVIGATION_SCRIPT}
  {FOOTER_ASSETS}
  {BACK_TO_TOP_STYLESHEET}
  {BACK_TO_TOP_SCRIPT}'''
METRIKA = '''<script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,'script','https://mc.yandex.ru/metrika/tag.js','ym');ym(27865374, 'init', {clickmap:true,referrer:document.referrer,url:location.href,accurateTrackBounce:true,trackLinks:true});</script>'''
NOSCRIPT = '<noscript><div><img src="https://mc.yandex.ru/watch/27865374" style="position:absolute;left:-9999px;" alt=""></div></noscript>'


def page(*, title: str, description: str, url: str, image: str, image_alt: str, headline: str, lead: str, meta: str, body: str, keywords: list[str]) -> str:
    jsonld = {
        '@context': 'https://schema.org', '@type': 'BlogPosting', '@id': url + '#article',
        'headline': headline, 'description': description, 'image': image,
        'author': {'@type': 'Person', '@id': 'https://nasuta.ru/#pavel-nasuta', 'name': 'Павел Насута', 'url': 'https://nasuta.ru/about/'},
        'datePublished': DATE, 'dateModified': DATE, 'inLanguage': 'ru-RU',
        'mainEntityOfPage': url, 'isPartOf': {'@id': 'https://nasuta.ru/articles/#webpage'}, 'keywords': keywords,
    }
    return f'''<!doctype html>
<html lang="ru">
<head>
  <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{html.escape(description, quote=True)}">
  <title>{html.escape(title)} · Павел Насута</title>
  <link rel="stylesheet" href="../../assets/styles/articles-editorial.css">
  <link rel="stylesheet" href="../../assets/styles/ai-agent-guides.css">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Павел Насута">
  <meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}"><meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{html.escape(image_alt, quote=True)}">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title, quote=True)}"><meta name="twitter:description" content="{html.escape(description, quote=True)}"><meta name="twitter:image" content="{image}"><meta name="twitter:image:alt" content="{html.escape(image_alt, quote=True)}">
  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
  {METRIKA}
  {SHARED_ASSETS}
</head>
<body id="top">{NOSCRIPT}
{SITE_NAVIGATION}
<div class="shell">
    <main>
      <header class="hero ai-agent-hero"><div class="meta">ПРАКТИКА AI-АГЕНТОВ · {meta}</div><h1>{headline}</h1><p class="lede">{lead}</p><figure class="hero-visual"><img src="{image.replace('https://nasuta.ru', '../..')}" alt="{html.escape(image_alt, quote=True)}"></figure></header>
      {body}
    </main>
    {SITE_FOOTER}
  </div>
  {BACK_TO_TOP}
</body></html>'''


def strip_citations(markdown: str) -> str:
    markdown = re.sub(r'^---\n.*?\n---\n', '', markdown, count=1, flags=re.S)
    markdown = re.split(r'\n## Sources\n', markdown, maxsplit=1)[0]
    markdown = re.sub(r'\[(?:\d+)\]', '', markdown)
    markdown = re.sub(r' {2,}', ' ', markdown)
    return markdown.strip()


def build_pillar() -> None:
    source = SOURCE.read_text(encoding='utf-8')
    clean = strip_citations(source)
    # Canonical research version stays detailed, but does not expose citation markers or a sources appendix.
    SOURCE.write_text(clean + '\n', encoding='utf-8')
    body = subprocess.run(['pandoc', '--from', 'markdown', '--to', 'html5', '--wrap=none'], input=clean, text=True, capture_output=True, check=True).stdout
    body = re.sub(r'<h1[^>]*>.*?</h1>', '', body, count=1, flags=re.S)
    body = body.replace('<h2 id="что-делать-дальше">Что делать дальше</h2>', '''<section class="agent-cta"><div><div class="eyebrow">Следующий шаг</div><h2>Не добавляйте всё подряд</h2><p>После установки агенту нужен один полезный рабочий цикл. Выберите процесс, который повторяется, оставляет проверяемый результат и не требует передачи необратимого решения машине.</p></div><div class="agent-cta__links"><a href="../how-to-choose-an-ai-task/">Выбрать первую задачу →</a><a href="../../skills/">Посмотреть готовые skills →</a><a href="../../contact/">Разобрать свой процесс →</a></div></section><h2 id="что-делать-дальше">Что делать дальше</h2>''')
    body = body.replace('Timeweb Cloud', '<a href="https://timeweb.cloud/" target="_blank" rel="noopener">Timeweb Cloud</a>')
    body = body.replace('ChatGPT в браузере', '<a href="https://chatgpt.com/" target="_blank" rel="noopener">ChatGPT в браузере</a>')
    body = body.replace('Plati', '<a href="https://plati.market/" target="_blank" rel="noopener">Plati</a>')
    article = f'''<section class="article"><aside class="toc"><div class="eyebrow">Маршруты</div><a href="#быстрый-выбор-компьютер-или-vps">Компьютер или VPS</a><a href="#маршрут-1-установка-hermes-desktop-без-терминала">Desktop</a><a href="#telegram-бот-и-организация-работы">Telegram</a><a href="#маршрут-4-постоянный-hermes-на-собственном-vps">VPS</a><a href="#шесть-сценариев-где-агент-сильнее-обычного-чата">Сценарии</a><a href="#что-делать-дальше">Следующий шаг</a></aside><article class="content ai-guide-content"><div class="route-box"><strong>Если хотите попробовать:</strong> начните с Desktop на своём компьютере. <strong>Если агент должен отвечать в Telegram круглосуточно:</strong> переходите к маршруту VPS. <a href="https://hermes-agent.nousresearch.com/desktop" target="_blank" rel="noopener">Официальный Hermes Desktop ↗</a></div>{body}</article></section>'''
    output = ROOT / 'articles' / 'hermes-agent-installation' / 'index.html'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page(title='Как установить Hermes Agent на Mac, Windows и VPS', description='Подробная инструкция по установке Hermes Agent в России: Mac, Windows, VPS, Telegram, навыки, безопасность и первые сценарии.', url='https://nasuta.ru/articles/hermes-agent-installation/', image='https://nasuta.ru/assets/images/og-hermes-agent-installation.jpg', image_alt='Ноутбук, компьютер и сервер соединены в один рабочий путь AI-агента', headline='Как установить Hermes Agent на Mac, Windows и VPS', lead='Большая инструкция для тех, кому нужен не ещё один чат, а личный AI-агент: на компьютере, в Telegram и при необходимости на постоянном сервере.', meta='29 ОКТЯБРЯ 2026 · 25 МИНУТ', body=article, keywords=['Hermes Agent', 'установка Hermes Agent', 'VPS', 'Telegram', 'AI-агент', 'Windows', 'macOS']), encoding='utf-8')


def build_hub() -> None:
    body = '''<section class="article"><article class="content ai-guide-content"><p>AI-агент полезен не потому, что умеет красиво отвечать. Он становится полезен, когда берёт повторяющийся кусок работы, оставляет понятный результат и не забирает у человека право на решение.</p><p>В этой ветке собраны материалы именно про это: как поставить агента, где хранить его результаты, какой процесс выбрать первым и как не перепутать автоматизацию с красивой демонстрацией.</p><div class="decision-flow"><div><span>1</span><strong>Есть работа</strong><p>Повторяющийся процесс, где уже есть входящие данные и понятный результат.</p></div><div><span>2</span><strong>Есть граница</strong><p>Человек оставляет за собой публикации, деньги, доступы и необратимые решения.</p></div><div><span>3</span><strong>Есть артефакт</strong><p>Итог можно открыть, проверить, передать дальше или найти через месяц.</p></div></div><h2>С чего начать</h2><div class="guide-cards"><a href="../hermes-agent-installation/"><span>УСТАНОВКА</span><h3>Hermes на Mac, Windows и VPS</h3><p>Выберите Desktop или постоянный сервер, подключите Telegram и не потеряйте контроль над доступами.</p></a><a href="../hermes-agent-telegram-vps/"><span>24/7</span><h3>Telegram-агент на VPS</h3><p>Как устроить серверный контур, который не исчезает вместе с закрытым ноутбуком.</p></a><a href="../ai-agent-knowledge-storage/"><span>ПАМЯТЬ</span><h3>Агенту нужно куда складывать работу</h3><p>Зачем связать Hermes и Anytype, чтобы результат жил не только в переписке.</p></a><a href="../how-to-choose-an-ai-task/"><span>ВЫБОР</span><h3>Как выбрать первую задачу</h3><p>Проверить проблему, цену ошибки и способ человеческого контроля до покупки инструмента.</p></a><a href="../hermes-commands/"><span>СПРАВОЧНИК</span><h3>Команды Hermes в Telegram и консоли</h3><p>Полный список встроенных команд: новая сессия, фоновые задачи, доступы, gateway и терминал.</p></a></div><h2>Не начинайте с пустого чата</h2><p>Если уже знаете свою задачу, лучше взять готовый workflow и адаптировать его под себя. В <a href="../../skills/">Skill Hub</a> собраны навыки для аудиосаммари, работы руководителя и базы знаний. Если нужна практика и новые разборы, подписывайтесь на <a href="https://t.me/niimozgii" target="_blank" rel="noopener">НИИ «МОЗГИ» ↗</a>.</p><section class="agent-cta"><div><div class="eyebrow">Свой процесс</div><h2>Сначала разложите работу, потом автоматизируйте</h2><p>Не уверены, есть ли у процесса потенциал для агента? Начните с проблемы, входящих данных, критерия результата и цены ошибки.</p></div><div class="agent-cta__links"><a href="../how-to-choose-an-ai-task/">Выбрать задачу →</a><a href="../../contact/">Разобрать процесс →</a></div></section></article></section>'''
    output = ROOT / 'articles' / 'ai-agents' / 'index.html'; output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page(title='Практика AI-агентов', description='Гайды по AI-агентам: Hermes, Telegram, VPS, память, Anytype, skills и безопасная автоматизация рабочих процессов.', url='https://nasuta.ru/articles/ai-agents/', image='https://nasuta.ru/assets/images/og-ai-agent-practice.jpg', image_alt='Карта пути AI-агента от компьютера и сервера к проверяемым рабочим материалам', headline='Практика AI-агентов', lead='Не витрина нейросетей, а рабочие маршруты: поставить агента, дать ему одну задачу, сохранить результат и не потерять контроль.', meta='ГАЙДЫ · AI-АГЕНТЫ · АВТОМАТИЗАЦИЯ', body=body, keywords=['AI-агенты', 'автоматизация', 'Hermes', 'Telegram', 'VPS', 'skills']), encoding='utf-8')


def build_vps() -> None:
    body = '''<section class="article"><aside class="toc"><div class="eyebrow">В статье</div><a href="#when">Когда нужен VPS</a><a href="#shape">Как выглядит контур</a><a href="#start">Порядок запуска</a><a href="#security">Доступы и безопасность</a><a href="#operating">Еженедельная проверка</a></aside><article class="content ai-guide-content"><p>Ноутбук удобен, пока агент нужен в рабочее время и рядом лежат ваши файлы. Но как только он должен отвечать в Telegram утром, ночью, в поездке или по расписанию, домашний компьютер превращается в ненадёжную часть системы.</p><p>VPS решает не проблему «где взять магию». Он решает простую задачу: где живёт постоянно работающая программа, пока вы занимаетесь своей жизнью.</p><h2 id="when">Когда VPS действительно нужен</h2><ul><li>бот должен отвечать, когда ноутбук закрыт;</li><li>есть регулярные обзоры, напоминания или мониторинг;</li><li>агенту нужен устойчивый адрес и отдельная среда;</li><li>вы готовы раз в неделю проверить состояние сервера и резервных копий.</li></ul><p>Если вы только пробуете сценарий с файлами на своём компьютере, VPS можно отложить. Не нужно арендовать сервер, чтобы задать первый хороший вопрос.</p><h2 id="shape">Контур, который стоит собирать</h2><div class="decision-flow"><div><span>1</span><strong>VPS</strong><p>Отдельный пользователь для Hermes. Не root. Обновления и только нужные сетевые доступы.</p></div><div><span>2</span><strong>Gateway</strong><p>Сервис Hermes держит соединение с Telegram и запускается снова после перезагрузки.</p></div><div><span>3</span><strong>Человек</strong><p>Получает итог в Telegram, проверяет его и подтверждает необратимые действия.</p></div></div><h2 id="start">Порядок запуска без инфраструктурного фетиша</h2><ol><li>Выберите VPS у провайдера, который показывает страну размещения, стоимость и резервные опции. Например, <a href="https://timeweb.cloud/services/servers-europe" target="_blank" rel="noopener">Timeweb Cloud</a> предлагает зарубежные локации через привычную панель.</li><li>Создайте отдельного пользователя для Hermes и не запускайте агента от root.</li><li>Поставьте Hermes по <a href="https://hermes-agent.nousresearch.com/docs/getting-started/installation" target="_blank" rel="noopener">официальной инструкции</a>.</li><li>Подключите Telegram через интерфейс Hermes или создайте бота в <a href="https://t.me/BotFather" target="_blank" rel="noopener">BotFather ↗</a>.</li><li>Разрешите писать боту только тем аккаунтам, которым доверяете.</li><li>Включите автозапуск gateway, перезагрузите сервер и отправьте тестовое сообщение.</li></ol><p>Не открывайте веб-интерфейс агента в интернет ради удобства. Telegram не требует от вас публичного webhook для базового сценария, а админский доступ лучше оставлять за SSH или закрытой сетью.</p><h2 id="security">Где чаще всего ломается безопасность</h2><p>Не в сложной криптографии. Обычно всё ломается в момент, когда токен бота отправляют в чат, сервер оставляют с парольным root-входом, а агенту дают доступ ко всему сразу.</p><div class="route-box"><strong>Минимальное правило:</strong> один бот, один ответственный владелец, отдельный пользователь на сервере, ограниченный список Telegram-пользователей и человек перед публикацией, платежом, удалением или изменением прав.</div><p>Если для вашей работы нужен личный VPN, не смешивайте его с агентом на одном сервере только ради экономии. Это разные контуры доступа и разные последствия ошибки.</p><h2 id="operating">Десять минут в неделю</h2><p>Раз в неделю проверьте: отвечает ли бот, хватает ли места на диске, прошли ли обновления, есть ли резервная копия и понятна ли карта восстановления. Серверный агент не должен быть хрупкой штукой, о которой вспоминают только после тишины в Telegram.</p><section class="agent-cta"><div><div class="eyebrow">После VPS</div><h2>Сервер не является сценарием</h2><p>Когда агент стабильно доступен, выберите одну полезную работу: аудиосаммари, помощник руководителя, рыночный радар или база знаний.</p></div><div class="agent-cta__links"><a href="../../skills/">Выбрать skill →</a><a href="../hermes-agent-installation/">Полная инструкция Hermes →</a><a href="../../contact/">Разобрать процесс →</a></div></section></article></section>'''
    output = ROOT / 'articles' / 'hermes-agent-telegram-vps' / 'index.html'; output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page(title='Hermes + Telegram на VPS: агент 24/7', description='Как настроить Hermes Agent на VPS для Telegram: когда нужен сервер, как запустить gateway, ограничить доступы и проверить работу после перезагрузки.', url='https://nasuta.ru/articles/hermes-agent-telegram-vps/', image='https://nasuta.ru/assets/images/og-hermes-agent-telegram-vps.jpg', image_alt='Серверный AI-агент ночью передаёт сообщение и проверяемый отчёт человеку', headline='Hermes + Telegram на VPS: агент 24/7', lead='Как сделать так, чтобы агент был доступен в Telegram, когда ноутбук закрыт, но не превратить собственный сервер в открытую дверь.', meta='ПРАКТИЧЕСКИЙ ГАЙД · 12 МИНУТ', body=body, keywords=['Hermes Telegram', 'Hermes VPS', 'Telegram бот', 'AI-агент 24/7', 'VPS']), encoding='utf-8')


def main() -> None:
    build_pillar(); build_hub(); build_vps()

if __name__ == '__main__':
    main()
