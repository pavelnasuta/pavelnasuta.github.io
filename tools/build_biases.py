"""Validate and render the published cognitive-bias catalogue."""

from __future__ import annotations

import argparse
from datetime import date
import html
import json
from pathlib import Path
import re
from typing import Any, Iterable
import xml.etree.ElementTree as ET

try:
    from tools.site_footer import SITE_FOOTER, STYLESHEET
except ModuleNotFoundError:  # Direct execution from tools/.
    from site_footer import SITE_FOOTER, STYLESHEET


DETAIL_CATEGORIES = frozenset(
    {
        "Когда информации слишком много",
        "Когда не хватает смысла",
        "Когда нужно действовать быстро",
        "Когда мы решаем, что запомнить",
    }
)
IDENTITY_FIELDS = frozenset(
    {
        "slug",
        "russian_name",
        "english_name",
        "catalogue_category",
        "detail_category",
        "problem",
        "published",
    }
)
EDITORIAL_FIELDS = frozenset(
    {
        "lede",
        "scenario",
        "mechanism",
        "watch_for",
        "helps",
        "status_note",
        "sources",
        "seo",
        "diagram",
    }
)
CATEGORY_FILTERS = {
    "Слишком много информации": "information",
    "Не хватает смысла": "meaning",
    "Нужно действовать": "action",
    "Что мы запоминаем": "memory",
}
COUNTER_ID = "27865374"
SAFE_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SITE_ORIGIN = "https://nasuta.ru"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def load_catalogue(path: str | Path) -> list[dict[str, Any]]:
    """Load the registry object and return its ordered identity records."""
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("items"), list):
        raise ValueError("Catalogue must be a JSON object with an items array")
    return document["items"]


def validate_catalogue(
    items: Iterable[dict[str, Any]], *, expected_count: int = 189
) -> None:
    """Reject malformed identities and incomplete entries marked for publication."""
    entries = list(items)
    if len(entries) != expected_count:
        raise ValueError(f"Catalogue must contain exactly {expected_count} entries")

    slugs: set[str] = set()
    for item in entries:
        if not isinstance(item, dict):
            raise ValueError("Catalogue entries must be JSON objects")
        missing_identity = IDENTITY_FIELDS - item.keys()
        if missing_identity:
            raise ValueError(
                f"Incomplete identity: {item.get('slug', '<unknown>')}: "
                f"{sorted(missing_identity)}"
            )
        if not isinstance(item["slug"], str) or not item["slug"].strip():
            raise ValueError("Every identity requires a non-empty slug")
        if not SAFE_SLUG.fullmatch(item["slug"]):
            raise ValueError(f"Invalid slug: {item['slug']}")
        if item["slug"] in slugs:
            raise ValueError(f"Duplicate slug: {item['slug']}")
        slugs.add(item["slug"])
        for field in IDENTITY_FIELDS - {"slug", "published"}:
            if not isinstance(item[field], str) or not item[field].strip():
                raise ValueError(f"Identity field is empty: {item['slug']}: {field}")
        if not isinstance(item["published"], bool):
            raise ValueError(f"published must be a boolean: {item['slug']}")
        if not item["published"]:
            continue

        missing_editorial = EDITORIAL_FIELDS - item.keys()
        if missing_editorial:
            raise ValueError(
                f"Incomplete published entry: {item['slug']}: "
                f"{sorted(missing_editorial)}"
            )
        if item["detail_category"] not in DETAIL_CATEGORIES:
            raise ValueError(f"Unknown detail category: {item['slug']}")
        for field in EDITORIAL_FIELDS - {"sources", "seo", "diagram"}:
            if not isinstance(item[field], str) or not item[field].strip():
                raise ValueError(f"Published field is empty: {item['slug']}: {field}")
        if not isinstance(item["sources"], list) or not item["sources"]:
            raise ValueError(f"Published entry requires sources: {item['slug']}")
        for source in item["sources"]:
            if (
                not isinstance(source, dict)
                or not isinstance(source.get("url"), str)
                or not source["url"].strip()
                or not isinstance(source.get("citation"), str)
                or not source["citation"].strip()
            ):
                raise ValueError(f"Published source is incomplete: {item['slug']}")
        if (
            not isinstance(item["seo"], dict)
            or not isinstance(item["seo"].get("title"), str)
            or not item["seo"]["title"].strip()
            or not isinstance(item["seo"].get("description"), str)
            or not item["seo"]["description"].strip()
        ):
            raise ValueError(f"Published entry requires SEO fields: {item['slug']}")
        if item["diagram"] is not None and not isinstance(item["diagram"], dict):
            raise ValueError(f"Diagram must be an object or null: {item['slug']}")


def _text(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _metrika() -> str:
    return f'''<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,'script','https://mc.yandex.ru/metrika/tag.js','ym');ym({COUNTER_ID}, 'init', {{clickmap:true, referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});</script><!-- /Yandex.Metrika counter -->'''


def _metrika_pixel() -> str:
    return f'''<!-- Yandex.Metrika counter (noscript) --><noscript><div><img src="https://mc.yandex.ru/watch/{COUNTER_ID}" style="position:absolute;left:-9999px;" alt=""></div></noscript><!-- /Yandex.Metrika counter (noscript) -->'''


def render_cta() -> str:
    """Render the identical, accessible author CTA for each detail page."""
    return '''<aside class="bias-cta" aria-labelledby="bias-cta-title">
      <p class="bias-cta__label">НИИ «МОЗГИ»</p>
      <h2 id="bias-cta-title">Персональный тренер для вашего агента</h2>
      <p class="bias-cta__author">Павел Насута — AI-powered product builder</p>
      <a class="bias-cta__button" href="https://t.me/niimozgii" target="_blank" rel="noopener">Открыть канал <span aria-hidden="true">↗</span></a>
      <nav class="bias-cta__social" aria-label="Связаться с Павлом Насутой">
        <a href="https://t.me/pavelnasuta" target="_blank" rel="noopener" aria-label="Telegram Павла Насуты"><svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M21.6 3.2 18.4 20c-.2 1.2-.9 1.5-1.8.9l-5-3.7-2.4 2.3c-.3.3-.5.5-1 .5l.4-5.1 9.3-8.4c.4-.4-.1-.6-.6-.3L5.8 13.5.9 12c-1.1-.3-1.1-1.1.2-1.6L20.3 3c.9-.3 1.7.2 1.3.2Z"/></svg><span class="sr-only">Telegram</span></a>
        <a href="https://www.linkedin.com/in/nasuta" target="_blank" rel="noopener" aria-label="LinkedIn Павла Насуты"><svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M5.3 8.3H1.8V22h3.5V8.3ZM3.5 2A2 2 0 0 0 1.5 4a2 2 0 0 0 2 2 2 2 0 0 0 0-4ZM22.5 14.1c0-4.1-2.2-6-5.1-6-2.4 0-3.5 1.3-4.1 2.2V8.3H9.8V22h3.5v-6.8c0-1.8.3-3.5 2.5-3.5 2.2 0 2.2 2 2.2 3.6V22h3.5v-7.9Z"/></svg><span class="sr-only">LinkedIn</span></a>
        <a href="mailto:pavelnasuta@gmail.com" aria-label="Написать Павлу Насуте"><svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M2 5.5C2 4.7 2.7 4 3.5 4h17c.8 0 1.5.7 1.5 1.5v13c0 .8-.7 1.5-1.5 1.5h-17c-.8 0-1.5-.7-1.5-1.5v-13Zm2 .7v.3l8 5.2 8-5.2v-.3H4Zm16 2.7-8 5.2-8-5.2V18h16V8.9Z"/></svg><span class="sr-only">Email</span></a>
      </nav>
    </aside>'''


def _route_link(label: str, name: str, href: str) -> str:
    return f'<a class="route-link" href="{href}"><span>{_text(label)}</span>{_text(name)}</a>'


def render_detail(
    item: dict[str, Any], previous: dict[str, Any] | None, next_item: dict[str, Any] | None,
    *, number: int = 1,
) -> str:
    """Render one complete published card from the validated registry."""
    if not item.get("published"):
        raise ValueError(f"Item is not published: {item.get('slug', '<unknown>')}")
    validate_catalogue([item], expected_count=1)

    slug = _text(item["slug"])
    name = _text(item["russian_name"])
    seo = item["seo"]
    description = _text(seo["description"])
    article_schema = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "@id": f"https://nasuta.ru/biases/{item['slug']}/#article",
            "headline": item["russian_name"],
            "description": item["lede"],
            "image": "https://nasuta.ru/assets/images/og-cognitive-biases.jpg",
            "author": {"@type": "Person", "@id": "https://nasuta.ru/#pavel-nasuta", "name": "Павел Насута", "url": "https://nasuta.ru/about/"},
            "dateModified": "2026-10-19",
            "inLanguage": "ru-RU",
            "mainEntityOfPage": f"https://nasuta.ru/biases/{item['slug']}/",
            "about": {"@type": "Thing", "name": item["russian_name"]},
        },
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    source_rows = "\n".join(
        f'          <li><a href="{_text(source["url"])}" target="_blank" rel="noopener">{_text(source["citation"])}</a></li>'
        for source in item["sources"]
    )
    route_links = [_route_link("К списку", "К каталогу", "../index.html")]
    if previous:
        route_links.insert(0, _route_link("Предыдущее", f"← {previous['russian_name']}", f"../{previous['slug']}/index.html"))
    if next_item:
        route_links.append(_route_link("Следующее", f"{next_item['russian_name']} →", f"../{next_item['slug']}/index.html"))
    random_target = next_item or previous or item
    route_links.append(
        f'<a class="route-link route-link--random" href="../{_text(random_target["slug"])}/index.html" id="random-bias"><span>Выбрать иначе</span>Случайное</a>'
    )
    random_routes = []
    for candidate in (previous, next_item):
        if candidate and candidate["slug"] != item["slug"]:
            route = f"../{candidate['slug']}/index.html"
            if route not in random_routes:
                random_routes.append(route)
    if not random_routes:
        random_routes.append(f"../{item['slug']}/index.html")

    return f'''<!doctype html>
<html lang="ru">
<head>
  <link rel="icon" type="image/svg+xml" href="../../favicon.svg"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{description}"><title>{_text(seo['title'])}</title>
  <link rel="stylesheet" href="../../assets/styles/biases.css"><link rel="canonical" href="https://nasuta.ru/biases/{slug}/">
  <meta property="og:type" content="article"><meta property="og:locale" content="ru_RU"><meta property="og:title" content="{_text(seo['title'])}"><meta property="og:description" content="{description}"><meta property="og:url" content="https://nasuta.ru/biases/{slug}/"><meta property="og:image" content="https://nasuta.ru/assets/images/og-cognitive-biases.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Когнитивные искажения — справочник Павла Насуты">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{_text(seo['title'])}"><meta name="twitter:description" content="{description}"><meta name="twitter:image" content="https://nasuta.ru/assets/images/og-cognitive-biases.jpg"><meta name="twitter:image:alt" content="Когнитивные искажения — справочник Павла Насуты">
  <script type="application/ld+json">{article_schema}</script>
  {STYLESHEET}
  {_metrika()}
</head>
<body>
  {_metrika_pixel()}
  <div class="shell">
    <nav class="quiet-nav" aria-label="Навигация раздела"><a class="brand" href="../../index.html">Павел Насута</a><a class="back-link" href="../index.html">К каталогу <span aria-hidden="true">↗</span></a></nav>
    <main class="article">
      <header class="article-head">
        <div class="article-kicker"><p class="eyebrow">{_text(item['detail_category'])}</p><p class="article-number" aria-label="Номер карточки в каталоге">№ {number:02}</p></div>
        <h1>{name}</h1>
        <p class="article-dek">{_text(item['lede'])}</p>
        <p class="article-meta">{_text(item['english_name'])}</p>
      </header>
      <section><h2>Как это выглядит</h2><p>{_text(item['scenario'])}</p></section>
      <section class="mechanism"><div class="mechanism-label">Механика</div><div><p>{_text(item['mechanism'])}</p></div></section>
      <section><h2>Когда стоит насторожиться</h2><p>{_text(item['watch_for'])}</p></section>
      <section><h2>Что помогает</h2><p>{_text(item['helps'])}</p></section>
      <section><h2>Откуда взялось понятие</h2><p class="article-note">{_text(item['status_note'])}</p><ul class="source-list">
{source_rows}
        </ul></section>
      {render_cta()}
      <nav class="route-nav" aria-label="Продолжить изучение">{''.join(route_links)}</nav>
    </main>
    {SITE_FOOTER}
  </div>
  <script>const random=document.getElementById('random-bias');const routes={json.dumps(random_routes, ensure_ascii=False)};random.addEventListener('click',(event)=>{{event.preventDefault();window.location.href=routes[Math.floor(Math.random()*routes.length)]}});</script>
</body>
</html>'''


def render_catalogue(items: Iterable[dict[str, Any]]) -> str:
    """Render the public catalogue from complete published records only."""
    published = [item for item in items if item["published"]]
    rows = []
    for number, item in enumerate(published, start=1):
        category = item["catalogue_category"]
        group = CATEGORY_FILTERS.get(category)
        if group is None:
            raise ValueError(f"Unknown catalogue category: {category}")
        search = " ".join((item["russian_name"], item["english_name"], item["lede"], *item.get("search_aliases", []))).lower()
        rows.append(
            f'''          <li><a class="bias-row" href="{_text(item['slug'])}/index.html" data-group="{group}" data-search="{_text(search)}"><span class="bias-row__number">{number:02}</span><span class="bias-row__body"><span class="bias-row__title">{_text(item['russian_name'])}</span><span class="bias-row__summary">{_text(item['lede'])}</span></span><span class="bias-row__category bias-row__category--{group}">{_text(category)}</span><span class="bias-row__arrow" aria-hidden="true">→</span></a></li>'''
        )
    return f'''<!doctype html>
<html lang="ru">
<head>
  <link rel="icon" type="image/svg+xml" href="../favicon.svg"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="Когнитивные искажения: понятный каталог с примерами, механизмами и источниками исследований."><title>Когнитивные искажения · Павел Насута</title>
  <link rel="stylesheet" href="../assets/styles/biases.css"><link rel="canonical" href="https://nasuta.ru/biases/">
  <meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:title" content="Когнитивные искажения · Павел Насута"><meta property="og:description" content="Когнитивные искажения: понятный каталог с примерами, механизмами, способами самопроверки и источниками исследований."><meta property="og:url" content="https://nasuta.ru/biases/"><meta property="og:image" content="https://nasuta.ru/assets/images/og-cognitive-biases.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Когнитивные искажения — справочник Павла Насуты">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Когнитивные искажения · Павел Насута"><meta name="twitter:description" content="Когнитивные искажения: понятный каталог с примерами, механизмами, способами самопроверки и источниками исследований."><meta name="twitter:image" content="https://nasuta.ru/assets/images/og-cognitive-biases.jpg"><meta name="twitter:image:alt" content="Когнитивные искажения — справочник Павла Насуты">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","@id":"https://nasuta.ru/biases/#webpage","url":"https://nasuta.ru/biases/","name":"Когнитивные искажения","description":"Понятный каталог когнитивных искажений с примерами, механизмами и источниками.","inLanguage":"ru-RU","about":{{"@type":"Thing","name":"Когнитивные искажения"}},"isPartOf":{{"@id":"https://nasuta.ru/#website"}}}}</script>
  {STYLESHEET}
  {_metrika()}
</head>
<body>
  {_metrika_pixel()}
  <div class="shell">
    <nav class="quiet-nav" aria-label="Навигация раздела"><a class="brand" href="../index.html">Павел Насута</a><a class="back-link" href="../index.html">К сайту <span aria-hidden="true">↗</span></a></nav>
    <main>
      <header class="hero hero--catalog"><p class="eyebrow">Справочник</p><h1>Когнитивные<br>искажения.</h1><p class="lede">Как мозг упрощает сложное, где это мешает принимать решения и как вовремя заметить ловушку.</p></header>
      <section class="catalog" aria-labelledby="catalog-title">
        <div class="catalog-head catalog-head--list"><div><h2 id="catalog-title">Каталог</h2></div><div class="catalog-controls"><label class="search" for="bias-search"><span class="sr-only">Найти искажение</span><input id="bias-search" type="search" placeholder="Найти искажение" autocomplete="off"></label><div class="filters" aria-label="Фильтр по группе"><button class="filter" type="button" data-filter="all" aria-pressed="true">Все</button><button class="filter" type="button" data-filter="information" aria-pressed="false">Информация</button><button class="filter" type="button" data-filter="meaning" aria-pressed="false">Смысл</button><button class="filter" type="button" data-filter="action" aria-pressed="false">Действие</button><button class="filter" type="button" data-filter="memory" aria-pressed="false">Память</button></div></div></div>
        <ol class="bias-list" id="bias-list">
{chr(10).join(rows)}
        </ol><p class="empty-state" id="empty-state" hidden>Ничего не найдено. Попробуй другое слово или фильтр.</p>
      </section>
    </main>{SITE_FOOTER}
  </div>
  <script>const search=document.getElementById('bias-search');const filters=[...document.querySelectorAll('[data-filter]')];const rows=[...document.querySelectorAll('.bias-row')];const empty=document.getElementById('empty-state');let group='all';const update=()=>{{const query=search.value.trim().toLowerCase();let visible=0;rows.forEach((row)=>{{const show=(group==='all'||row.dataset.group===group)&&(!query||row.dataset.search.includes(query));row.hidden=!show;if(show)visible+=1}});empty.hidden=visible!==0}};filters.forEach((button)=>button.addEventListener('click',()=>{{group=button.dataset.filter;filters.forEach((item)=>item.setAttribute('aria-pressed',String(item===button)));update()}}));search.addEventListener('input',update);</script>
</body>
</html>'''


def _remove_stale_generated_routes(root: Path, published_slugs: set[str]) -> None:
    """Remove obsolete generated detail documents without deleting unrelated files."""
    biases_root = root / "biases"
    if not biases_root.exists():
        return
    for page in biases_root.glob("*/index.html"):
        if page.parent.name not in published_slugs:
            page.unlink()


def refresh_sitemap(root: Path, published: Iterable[dict[str, Any]]) -> None:
    """Preserve existing non-bias URLs and replace the generated bias URL set."""
    sitemap_path = root / "sitemap.xml"
    url_tag = f"{{{SITEMAP_NS}}}url"
    loc_tag = f"{{{SITEMAP_NS}}}loc"
    lastmod_tag = f"{{{SITEMAP_NS}}}lastmod"
    ET.register_namespace("", SITEMAP_NS)
    if sitemap_path.exists():
        sitemap = ET.parse(sitemap_path).getroot()
    else:
        sitemap = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    for entry in list(sitemap):
        loc = entry.find(loc_tag)
        if loc is not None and (loc.text or "").startswith(f"{SITE_ORIGIN}/biases/"):
            sitemap.remove(entry)
    urls = [f"{SITE_ORIGIN}/biases/"]
    urls.extend(f"{SITE_ORIGIN}/biases/{item['slug']}/" for item in published)
    for url in urls:
        entry = ET.SubElement(sitemap, url_tag)
        ET.SubElement(entry, loc_tag).text = url
        ET.SubElement(entry, lastmod_tag).text = date.today().isoformat()
    ET.ElementTree(sitemap).write(sitemap_path, encoding="utf-8", xml_declaration=True)


def build(
    root: str | Path, catalogue: Iterable[dict[str, Any]], *, expected_count: int = 189
) -> list[Path]:
    """Generate the catalogue and complete detail routes for published entries."""
    items = list(catalogue)
    validate_catalogue(items, expected_count=expected_count)
    root_path = Path(root)
    published = [item for item in items if item["published"]]
    _remove_stale_generated_routes(root_path, {item["slug"] for item in published})
    built: list[Path] = []
    for index, item in enumerate(published):
        page = root_path / "biases" / item["slug"] / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            render_detail(
                item,
                published[index - 1] if len(published) > 1 else None,
                published[(index + 1) % len(published)] if len(published) > 1 else None,
                number=index + 1,
            ),
            encoding="utf-8",
        )
        built.append(page)
    catalogue_page = root_path / "biases" / "index.html"
    catalogue_page.parent.mkdir(parents=True, exist_ok=True)
    catalogue_page.write_text(render_catalogue(items), encoding="utf-8")
    refresh_sitemap(root_path, published)
    return [catalogue_page, *built]


def main() -> None:
    parser = argparse.ArgumentParser(description="Render published cognitive-bias pages.")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--catalogue", type=Path, default=Path("content/biases/catalogue.json"))
    parser.add_argument("--published-count", type=int, default=189)
    args = parser.parse_args()
    items = load_catalogue(args.catalogue)
    published_count = sum(item["published"] for item in items)
    if published_count > args.published_count:
        raise ValueError(f"Catalogue has {published_count} published items; limit is {args.published_count}")
    build(args.root, items)


if __name__ == "__main__":
    main()
