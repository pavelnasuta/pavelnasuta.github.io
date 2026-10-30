from __future__ import annotations

import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'articles' / 'hermes-commands' / 'source.md'
OUTPUT = ROOT / 'articles' / 'hermes-commands' / 'index.html'
URL = 'https://nasuta.ru/articles/hermes-commands/'
SOCIAL_IMAGE = 'https://nasuta.ru/assets/images/og-hermes-commands.jpg'
HERO_IMAGE = '../../assets/images/hermes-commands-hero.jpg'
DATE = '2026-10-30'
TITLE = 'Справочник команд Hermes: Telegram и консоль'
DESCRIPTION = 'Полная справка по командам Hermes Agent: 69 встроенных команд Telegram, типичные команды терминала, сценарии и границы доступа.'
IMAGE_ALT = 'Телефон, терминал и карточка команд Hermes соединены в рабочий контур'

METRIKA = '''<script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,'script','https://mc.yandex.ru/metrika/tag.js','ym');ym(27865374, 'init', {clickmap:true,referrer:document.referrer,url:location.href,accurateTrackBounce:true,trackLinks:true});</script>'''
NOSCRIPT = '<noscript><div><img src="https://mc.yandex.ru/watch/27865374" style="position:absolute;left:-9999px;" alt=""></div></noscript>'


def shared_navigation_and_footer() -> tuple[str, str]:
    reference = (ROOT / 'articles' / 'ai-agent-knowledge-storage' / 'index.html').read_text(encoding='utf-8')
    navigation = re.search(r'(<nav class="site-navigation".*?</nav>)', reference, re.S)
    footer = re.search(r'(<footer class="site-footer".*?</footer>\s*<aside class="cookie-notice".*?</aside>\s*</div>\s*<a class="back-to-top".*?</a>)', reference, re.S)
    if not navigation or not footer:
        raise RuntimeError('Could not extract the shared site navigation or footer')
    return navigation.group(1), footer.group(1)


def article_body() -> str:
    markdown = SOURCE.read_text(encoding='utf-8')
    rendered = subprocess.run(
        ['pandoc', '--from', 'markdown', '--to', 'html5', '--wrap=none'],
        input=markdown,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    rendered = re.sub(r'<h1[^>]*>.*?</h1>', '', rendered, count=1, flags=re.S)
    # The page shell owns the only H1; source sections start at H2 for a sound outline.
    return re.sub(r'<(/?)h1\b', r'<\1h2', rendered)


def build_page() -> None:
    navigation, footer = shared_navigation_and_footer()
    jsonld = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        '@id': URL + '#article',
        'headline': TITLE,
        'description': DESCRIPTION,
        'image': SOCIAL_IMAGE,
        'author': {
            '@type': 'Person', '@id': 'https://nasuta.ru/#pavel-nasuta',
            'name': 'Павел Насута', 'url': 'https://nasuta.ru/about/',
        },
        'datePublished': DATE,
        'dateModified': DATE,
        'inLanguage': 'ru-RU',
        'mainEntityOfPage': URL,
        'isPartOf': {'@id': 'https://nasuta.ru/articles/#webpage'},
        'keywords': ['Hermes Agent', 'команды Hermes', 'Telegram', 'CLI', 'AI-агент'],
    }
    toc = '''<aside class="toc"><div class="eyebrow">В справочнике</div><a href="#как-устроен-справочник">Как читать</a><a href="#telegram-команды-бота">Telegram</a><a href="#консоль-типичные-команды-hermes">Консоль</a><a href="#быстрые-сценарии">Сценарии</a><a href="#источники-и-границы-справки">Источники</a></aside>'''
    page = f'''<!doctype html>
<html lang="ru">
<head>
  <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{html.escape(DESCRIPTION, quote=True)}">
  <title>{html.escape(TITLE)} · Павел Насута</title>
  <link rel="stylesheet" href="../../assets/styles/articles-editorial.css">
  <link rel="stylesheet" href="../../assets/styles/ai-agent-guides.css">
  <link rel="canonical" href="{URL}">
  <meta property="og:type" content="article"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Павел Насута">
  <meta property="og:title" content="{html.escape(TITLE, quote=True)}"><meta property="og:description" content="{html.escape(DESCRIPTION, quote=True)}"><meta property="og:url" content="{URL}">
  <meta property="og:image" content="{SOCIAL_IMAGE}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{IMAGE_ALT}">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(TITLE, quote=True)}"><meta name="twitter:description" content="{html.escape(DESCRIPTION, quote=True)}"><meta name="twitter:image" content="{SOCIAL_IMAGE}"><meta name="twitter:image:alt" content="{IMAGE_ALT}">
  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
  {METRIKA}
  <link rel="stylesheet" href="/assets/styles/navigation.css?v=contacts-nav">
  <script defer src="/assets/scripts/navigation.js"></script>
  <link rel="stylesheet" href="/assets/styles/footer.css">
  <link rel="stylesheet" href="/assets/styles/back-to-top.css?v=1">
  <script defer src="/assets/scripts/back-to-top.js?v=1"></script>
  <link rel="stylesheet" href="/assets/styles/cookie-notice.css">
  <script defer src="/assets/scripts/cookie-notice.js"></script>
</head>
<body id="top">{NOSCRIPT}
{navigation}
<div class="shell">
  <main>
    <header class="hero ai-agent-hero"><div class="meta">ПРАКТИКА AI-АГЕНТОВ · СПРАВОЧНИК · 30 ОКТЯБРЯ 2026</div><h1>{TITLE}</h1><p class="lede">Какие команды доступны в диалоге с ботом и какие нужны в терминале. Сначала короткий ориентир, затем полный список с назначением каждой команды.</p><figure class="hero-visual"><img src="{HERO_IMAGE}" alt="{IMAGE_ALT}"></figure></header>
    <section class="article">{toc}<article class="content ai-guide-content">{article_body()}</article></section>
  </main>
  {footer}
</body></html>'''
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(page, encoding='utf-8')


def update_sitemap() -> None:
    sitemap = ROOT / 'sitemap.xml'
    entry = f'  <url><loc>{URL}</loc><lastmod>{DATE}</lastmod></url>\n'
    current = sitemap.read_text(encoding='utf-8')
    if URL not in current:
        sitemap.write_text(current.replace('</urlset>', entry + '</urlset>'), encoding='utf-8')


if __name__ == '__main__':
    build_page()
    update_sitemap()
