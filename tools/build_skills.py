"""Validate and render the private registry that drives the public Skill Hub."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any


SAFE_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
AGENT_STATES = frozenset({"verified", "compatible", "planned", "not-applicable"})
AGENTS = frozenset({"hermes", "claude-code", "codex", "opencode", "agents-md"})
VISIBILITIES = frozenset({"public", "private-pilot", "withheld"})
STATUSES = frozenset({"draft", "reviewed", "released", "private-pilot", "withheld"})
SOURCE_STATUSES = frozenset({"not-started", "sanitizing", "review-ready", "published"})
SITE_ORIGIN = "https://nasuta.ru"
REQUIRED_FIELDS = frozenset(
    {
        "slug", "name", "summary", "category", "tags", "status", "visibility",
        "source_status", "compatibility", "updated", "version", "license",
        "repository_url", "page_url", "privacy_review", "release_notes", "release_priority",
    }
)
STATUS_LABELS = {"released": "OPEN SOURCE", "private-pilot": "PRIVATE PILOT"}
AGENT_LABELS = {
    "hermes": "Hermes", "claude-code": "Claude Code", "codex": "Codex",
    "opencode": "OpenCode", "agents-md": "AGENTS.md",
}


def load_registry(path: Path) -> list[dict[str, Any]]:
    """Load a registry document with an ordered `items` array."""
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("items"), list):
        raise ValueError("Skill registry must be a JSON object with an items array")
    return document["items"]


def _require_text(item: dict[str, Any], field: str) -> None:
    if not isinstance(item[field], str) or not item[field].strip():
        raise ValueError(f"Skill field must be non-empty text: {item['slug']}: {field}")


def validate_registry(items: list[dict[str, Any]]) -> None:
    """Reject malformed public records before they can reach the site."""
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Skill records must be JSON objects")
        missing = REQUIRED_FIELDS - item.keys()
        if missing:
            raise ValueError(f"Incomplete skill record: {item.get('slug', '<unknown>')}: {sorted(missing)}")
        slug = item["slug"]
        if not isinstance(slug, str) or not SAFE_SLUG.fullmatch(slug):
            raise ValueError(f"Invalid skill slug: {slug!r}")
        if slug in seen:
            raise ValueError(f"Duplicate skill slug: {slug}")
        seen.add(slug)
        for field in ("name", "summary", "category", "status", "visibility", "source_status", "updated", "version", "license", "privacy_review", "release_notes"):
            _require_text(item, field)
        if item["status"] not in STATUSES:
            raise ValueError(f"Unknown status: {slug}: {item['status']}")
        if item["visibility"] not in VISIBILITIES:
            raise ValueError(f"Unknown visibility: {slug}: {item['visibility']}")
        if item["source_status"] not in SOURCE_STATUSES:
            raise ValueError(f"Unknown source status: {slug}: {item['source_status']}")
        if not isinstance(item["tags"], list) or not item["tags"] or not all(isinstance(tag, str) and tag.strip() for tag in item["tags"]):
            raise ValueError(f"Skill requires non-empty tags: {slug}")
        if not isinstance(item["release_priority"], int) or item["release_priority"] < 1:
            raise ValueError(f"Skill requires positive release priority: {slug}")
        if not isinstance(item["compatibility"], dict) or set(item["compatibility"]) != AGENTS:
            raise ValueError(f"Skill requires a complete compatibility map: {slug}")
        if not set(item["compatibility"].values()) <= AGENT_STATES:
            raise ValueError(f"Skill compatibility contains an invalid state: {slug}")
        for field in ("repository_url", "page_url"):
            if not isinstance(item[field], str):
                raise ValueError(f"Skill URL must be text: {slug}: {field}")
        if item["visibility"] == "public":
            if not item["page_url"]:
                raise ValueError(f"Public skill has no local page: {slug}")
            if item["status"] not in {"released", "private-pilot"}:
                raise ValueError(f"Public skill has an invalid publication status: {slug}")
        elif item["repository_url"] or item["page_url"]:
            raise ValueError(f"Non-public skill exposes a URL: {slug}")


def public_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the records allowed to appear in the public catalogue."""
    return [item for item in items if item["visibility"] == "public" and item["page_url"]]


def render_card(item: dict[str, Any]) -> str:
    """Render one accessible card for a visible skill."""
    badges = "".join(
        f'<span class="agent-badge agent-badge--{state}">{AGENT_LABELS[agent]} · {state}</span>'
        for agent, state in item["compatibility"].items()
        if state != "not-applicable"
    )
    tags = "".join(f'<li>{html.escape(tag)}</li>' for tag in item["tags"])
    status = item.get("catalogue_label") or STATUS_LABELS[item["status"]]
    return f'''<article class="skill-card" data-category="{html.escape(item['category'])}" data-search="{html.escape(' '.join([item['name'], item['summary'], item['category'], *item['tags']]).lower())}">
      <p class="skill-card__meta">{status} · {html.escape(item['category'])}</p>
      <h2><a href="{html.escape(item['page_url'].removeprefix('skills/'))}">{html.escape(item['name'])}</a></h2>
      <p>{html.escape(item['summary'])}</p>
      <ul class="skill-card__tags">{tags}</ul>
      <div class="skill-card__agents" aria-label="Совместимость с агентами">{badges}</div>
    </article>'''


def render_hub(items: list[dict[str, Any]]) -> str:
    """Render the complete SEO-ready catalogue from public records only."""
    visible = public_items(items)
    categories = sorted({item["category"] for item in visible})
    category_controls = "".join(
        f'<button type="button" class="filter-button" data-filter="category" data-value="{html.escape(category)}">{html.escape(category)}</button>'
        for category in categories
    )
    cards = "\n".join(render_card(item) for item in visible)
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": f"{SITE_ORIGIN}/skills/#collection",
        "name": "Skills для AI-агентов",
        "description": "Публичный каталог агентных навыков, собранных из практики работы с AI-агентами.",
        "url": f"{SITE_ORIGIN}/skills/",
        "inLanguage": "ru-RU",
        "author": {"@type": "Person", "@id": f"{SITE_ORIGIN}/#pavel-nasuta", "name": "Павел Насута"},
        "hasPart": [{"@type": "SoftwareSourceCode", "name": item["name"], "url": f"{SITE_ORIGIN}/{item['page_url'].removesuffix('index.html')}"} for item in visible],
    }, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return f'''<!doctype html>
<html lang="ru">
<head>
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="Публичный каталог навыков для AI-агентов: реальные workflows, собранные из продуктовой, редакционной и операционной практики.">
  <title>Skills для AI-агентов · Павел Насута</title>
  <link rel="canonical" href="https://nasuta.ru/skills/">
  <link rel="stylesheet" href="../assets/styles/skills-index.css">
  <meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Павел Насута"><meta property="og:title" content="Skills для AI-агентов · Павел Насута"><meta property="og:description" content="Публичный каталог практических навыков для AI-агентов."><meta property="og:url" content="https://nasuta.ru/skills/"><meta property="og:image" content="https://nasuta.ru/assets/images/og-skills-hub.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Skills для AI-агентов">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Skills для AI-агентов · Павел Насута"><meta name="twitter:description" content="Публичный каталог практических навыков для AI-агентов."><meta name="twitter:image" content="https://nasuta.ru/assets/images/og-skills-hub.jpg"><meta name="twitter:image:alt" content="Skills для AI-агентов">
  <script type="application/ld+json">{schema}</script>
  <script type="text/javascript">(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,'script','https://mc.yandex.ru/metrika/tag.js','ym');ym(27865374, 'init', {{clickmap:true, referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});</script>
</head>
<body>
  <noscript><div><img src="https://mc.yandex.ru/watch/27865374" style="position:absolute;left:-9999px;" alt=""></div></noscript>
  <div class="shell">
    <nav class="nav" aria-label="Основная навигация"><a class="brand" href="../index.html">Павел Насута</a><a href="../articles/index.html">Блог</a><a href="../create/index.html">CREATE</a><a href="../about/index.html">Обо мне</a><a class="nav-telegram" href="https://t.me/niimozgii" target="_blank" rel="noopener">Telegram ↗</a></nav>
    <main>
      <header class="hero"><p class="eyebrow">ПРАКТИКА · AI-АГЕНТЫ · OPEN WORKFLOWS</p><h1>Skills, собранные из реальной работы.</h1><p>Не набор промптов, а проверяемые рабочие контуры: задача, границы, онбординг, адаптеры агентов и способ проверить результат.</p></header>
      <section class="catalogue" aria-labelledby="catalogue-title"><div class="catalogue-head"><div><p class="eyebrow">КАТАЛОГ</p><h2 id="catalogue-title">Открытые и пилотные навыки</h2></div><label class="search"><span class="sr-only">Поиск по навыкам</span><input type="search" id="skill-search" placeholder="Найти навык" autocomplete="off"></label></div>
        <div class="filters" aria-label="Фильтр по категории"><button type="button" class="filter-button is-active" data-filter="category" data-value="all">Все</button>{category_controls}</div>
        <div class="skill-grid" id="skill-grid">{cards}</div>
        <p id="no-results" class="no-results" hidden>По этому запросу пока нет опубликованного навыка.</p>
      </section>
      <section class="method"><p class="eyebrow">КАК ПОЯВЛЯЮТСЯ НАВЫКИ</p><h2>Сначала практика, затем открытый выпуск.</h2><p>Каждый новый навык проходит обезличивание, проверку границ и адаптацию для агентных сред. Исходники появляются на GitHub только после отдельного ревью.</p></section>
    </main>
    <footer class="footer"><span>© Павел Насута</span><span>Skills для AI-агентов</span></footer>
  </div>
  <script>const search=document.getElementById('skill-search');const buttons=[...document.querySelectorAll('[data-filter="category"]')];const cards=[...document.querySelectorAll('.skill-card')];const none=document.getElementById('no-results');let category='all';function apply(){{const query=search.value.trim().toLowerCase();let shown=0;cards.forEach((card)=>{{const matchCategory=category==='all'||card.dataset.category===category;const matchQuery=!query||card.dataset.search.includes(query);const visible=matchCategory&&matchQuery;card.hidden=!visible;if(visible)shown+=1;}});none.hidden=shown!==0;}}buttons.forEach((button)=>button.addEventListener('click',()=>{{category=button.dataset.value;buttons.forEach((item)=>item.classList.toggle('is-active',item===button));apply();}}));search.addEventListener('input',apply);</script>
</body>
</html>'''


def build(root: Path, registry_path: Path) -> None:
    """Validate the registry and write the public hub entry page."""
    items = load_registry(registry_path)
    validate_registry(items)
    output = root / "skills" / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_hub(items), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and render the Skill Hub")
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    items = load_registry(args.registry)
    validate_registry(items)
    if args.root:
        build(args.root, args.registry)
    print(json.dumps({"validated": len(items), "public": len(public_items(items))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
