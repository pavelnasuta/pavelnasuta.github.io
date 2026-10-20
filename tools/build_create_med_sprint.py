#!/usr/bin/env python3
"""Build the CREATE MED Sprint long-form guide from its canonical materials."""

from __future__ import annotations

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "content" / "create-med-sprint"
OUTPUT = ROOT / "create-med-sprint" / "index.html"
PDF_TEXT = SOURCE_DIR / "CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.txt"

CORE_GUIDE = "08_ГИД_ДЛЯ_СТУДЕНТОВ.md"

# Full materials appear immediately after the sprint step where they are used.
STEP_MATERIALS = {
    "### Шаг 1. Создайте Project и главный чат": (
        "01_СИСТЕМНЫЙ_ПРОМПТ_CHATGPT.md",
        "07_КАК_РАБОТАТЬ_В_CHATGPT_PROJECT.md",
    ),
    "### Шаг 3. Сделайте только нужный ресёрч в Perplexity": (
        "02_ПРОМПТЫ_PERPLEXITY.md",
    ),
    "### Шаг 5. Зафиксируйте Карточку концепции v1": (
        "06_РАБОЧАЯ_КАРТА_КОНЦЕПЦИИ.md",
    ),
    "### Шаг 6. Сделайте простой прототип": (
        "04_ПРОМПТ_ЛЕНДИНГ_И_ПРОТОТИП.md",
        "10_ВИЗУАЛЬНАЯ_ФИЛОСОФИЯ.md",
    ),
    "### Шаг 7. Подготовьте защиту": (
        "05_ПИТЧ_И_ЗАЩИТА.md",
    ),
}

FINAL_MATERIALS = ("11_ПРОДУКТОВЫЙ_ТЕЗАУРУС.md",)


def inline(text: str) -> str:
    text = escape(text.strip())
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1 ↗</a>', text)
    return text


def render_table(lines: list[str]) -> str:
    rows = [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in lines]
    rows = [row for row in rows if not all(re.fullmatch(r"[-: ]+", cell) for cell in row)]
    if not rows:
        return ""
    head, *body = rows
    result = ['<dl class="fact-grid">']
    for row in body:
        result.append('<div class="fact-card">')
        for label, cell in zip(head, row):
            result.append(f"<dt>{inline(label)}</dt><dd>{inline(cell)}</dd>")
        result.append("</div>")
    result.append("</dl>")
    return "".join(result)


def render_markdown(source: str, heading_offset: int = 0) -> str:
    source = re.sub(r"\[\d+\]", "", source)
    lines = source.replace("\r\n", "\n").split("\n")
    result: list[str] = []
    i = 0
    copy_number = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            fence = line[3:].strip()
            i += 1
            code: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            copy_number += 1
            language = escape(fence or "text")
            result.append(
                "<details class=\"prompt-details\">"
                "<summary>Промпт для работы</summary>"
                "<div class=\"prompt-content\">"
                f"<button type=\"button\" class=\"copy\" data-copy-prompt aria-label=\"Скопировать промпт {copy_number}\">Скопировать</button>"
                f"<pre><code class=\"language-{language}\">{escape(chr(10).join(code))}</code></pre></div></details>"
            )
        elif re.match(r"^#{1,4}\s+", line):
            level = len(line) - len(line.lstrip("#"))
            text = line[level:].strip()
            level = min(level + 1 + heading_offset, 6)
            result.append(f"<h{level}>{inline(text)}</h{level}>")
        elif line.strip() == "---":
            result.append("<hr>")
        elif line.startswith("|"):
            table: list[str] = []
            while i < len(lines) and lines[i].startswith("|"):
                table.append(lines[i])
                i += 1
            result.append(render_table(table))
            continue
        elif re.match(r"^[-*]\s+", line):
            items: list[str] = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append(re.sub(r"^[-*]\s+", "", lines[i]))
                i += 1
            result.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ul>")
            continue
        elif re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i]))
                i += 1
            result.append("<ol>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ol>")
            continue
        elif line.startswith("> "):
            quote: list[str] = []
            while i < len(lines) and lines[i].startswith("> "):
                quote.append(lines[i][2:])
                i += 1
            result.append(f"<blockquote><p>{inline(' '.join(quote))}</p></blockquote>")
            continue
        elif not line.strip():
            pass
        else:
            paragraph = [line.strip()]
            while (
                i + 1 < len(lines)
                and lines[i + 1].strip()
                and not re.match(r"^(#{1,4}\s+|```|\||[-*]\s+|\d+\.\s+|> |---$)", lines[i + 1])
            ):
                i += 1
                paragraph.append(lines[i].strip())
            result.append(f"<p>{inline(' '.join(paragraph))}</p>")
        i += 1
    return "\n".join(result)


TELEGRAM_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.6 3.2 18.4 20c-.2 1.2-.9 1.5-1.8.9l-5-3.7-2.4 2.3c-.3.3-.5.5-1 .5l.4-5.1 9.3-8.4c.4-.4-.1-.6-.6-.3L5.8 13.5.9 12c-1.1-.3-1.1-1.1.2-1.6L20.3 3c.9-.3 1.7.2 1.3.2Z"/></svg>'
LINKEDIN_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.3 8.3H1.8V22h3.5V8.3ZM3.5 2A2 2 0 1 0 3.5 6a2 2 0 0 0 0-4ZM22.5 14.1c0-4.1-2.2-6-5.1-6-2.4 0-3.5 1.3-4.1 2.2V8.3H9.8V22h3.5v-6.8c0-1.8.3-3.5 2.5-3.5 2.2 0 2.2 2 2.2 3.6V22h3.5v-7.9Z"/></svg>'
EMAIL_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5.5h18v13H3v-13Zm1.8 1.8 7.2 5.6 7.2-5.6H4.8Zm14.4 9.4V9.6L12 15.2 4.8 9.6v7.1h14.4Z"/></svg>'
CONTACTS = (
    ("Telegram-канал НИИ «МОЗГИ»", "https://t.me/niimozgii", TELEGRAM_ICON, "Telegram-канал НИИ «МОЗГИ»"),
    ("Telegram Павла Насуты", "https://t.me/pavelnasuta", TELEGRAM_ICON, "Telegram Павла"),
    ("LinkedIn Павла Насуты", "https://www.linkedin.com/in/nasuta", LINKEDIN_ICON, "LinkedIn"),
    ("Написать Павлу по email", "mailto:pavelnasuta@gmail.com", EMAIL_ICON, "Email"),
)


def compact_contact_icons() -> str:
    return "".join(
        f'<a class="coach-contact-icon" href="{url}" target="_blank" rel="noopener" aria-label="{label}">{icon}<span class="sr-only">{visible}</span></a>'
        for label, url, icon, visible in CONTACTS
    )


def contact_section() -> str:
    links = "".join(
        f'<a class="contact-link" href="{url}" target="_blank" rel="noopener" aria-label="{label}">{icon}<span>{visible}</span></a>'
        for label, url, icon, visible in CONTACTS
    )
    return (
        '<section class="contact-section" id="contact">'
        '<div class="kicker">Контакты</div><div>'
        '<p class="contact-org">НИИ «МОЗГИ»</p>'
        '<h2>Персональный тренер для вашего агента</h2>'
        '<p>Павел Насута — AI-powered product builder</p>'
        '<div class="contact-links">' + links + '</div>'
        '</div></section>'
    )


def metrika() -> str:
    return """<!-- Yandex.Metrika counter -->
<script type=\"text/javascript\">
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,'script','https://mc.yandex.ru/metrika/tag.js','ym');
ym(27865374, 'init', {clickmap:true, referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
</script>
<!-- /Yandex.Metrika counter -->"""


def contextual_material(filename: str) -> str:
    content = render_markdown(
        (SOURCE_DIR / filename).read_text(encoding="utf-8"), heading_offset=3
    )
    return (
        '<section class="material contextual-material">'
        '<div class="kicker">Рабочий материал для этого шага</div>'
        f'<div class="material-body">{content}</div>'
        '</section>'
    )


STEP_TOC = (
    ("Шаг 0", "Выберите проблему"),
    ("Шаг 1", "Создайте Project"),
    ("Шаг 2", "Утвердите проблему"),
    ("Шаг 3", "Проведите ресёрч"),
    ("Шаг 4", "Сузьте сегмент и оффер"),
    ("Шаг 5", "Зафиксируйте карточку"),
    ("Шаг 6", "Сделайте прототип"),
    ("Шаг 7", "Подготовьте защиту"),
)


def table_of_contents() -> str:
    items = "".join(
        f'<a href="#step-{number}"><span>{label}</span>{title}</a>'
        for number, (label, title) in enumerate(STEP_TOC)
    )
    return (
        '<nav class="toc" aria-label="Оглавление CREATE MED Sprint">'
        '<div><p class="kicker">Маршрут спринта</p><h2>Пройдите по порядку</h2>'
        '<p>Каждый шаг оставляет артефакт для следующего. Промпты раскрываются там, где нужны.</p></div>'
        f'<div class="toc-links">{items}</div></nav>'
    )


def render_guide_with_materials() -> str:
    source = (SOURCE_DIR / CORE_GUIDE).read_text(encoding="utf-8")
    sections = re.split(r"(?=^### Шаг \d+\. )", source, flags=re.MULTILINE)
    rendered = [table_of_contents(), '<div class="guide-intro">' + render_markdown(sections[0]) + '</div>']
    post_step_content = ""
    for section in sections[1:]:
        heading = section.split("\n", 1)[0]
        match = re.match(r"### Шаг (\d+)\. ", heading)
        step_number = match.group(1) if match else ""
        if step_number == "7":
            step_and_reference = re.split(r"\n---\n(?=\n## )", section, maxsplit=1)
            section = step_and_reference[0]
            if len(step_and_reference) == 2:
                post_step_content = step_and_reference[1]
        body = [render_markdown(section)]
        for filename in STEP_MATERIALS.get(heading, ()):
            body.append(contextual_material(filename))
        rendered.append(
            f'<section class="sprint-step" id="step-{step_number}">'
            f'<div class="step-marker">Шаг {step_number}</div>'
            + "\n".join(body)
            + '</section>'
        )
    if post_step_content:
        rendered.append('<section class="guide-reference">' + render_markdown(post_step_content) + '</section>')
    rendered.extend(contextual_material(filename) for filename in FINAL_MATERIALS)
    return '<section class="guide-copy" id="guide"><div class="kicker">Полная инструкция</div>' + "\n".join(rendered) + "</section>"


def main() -> None:
    rendered = [render_guide_with_materials()]
    pdf_text = re.sub(r"\[\d+\]", "", PDF_TEXT.read_text(encoding="utf-8"))
    rendered.append(
        '<section class="material">'
        '<details class="material-details pdf-source">'
        '<summary><span>Полнота материала</span>Текстовая версия PDF-раздатки</summary>'
        '<div class="material-body"><p>Этот блок сохраняет полный извлечённый текст оригинальной раздатки. Для чтения используйте инструкцию выше; для печати и передачи — скачайте PDF.</p>'
        f'<pre class="pdf-text">{escape(pdf_text)}</pre>'
        '</div></details></section>'
    )
    rendered.append(contact_section())

    page = f"""<!doctype html>
<html lang="ru">
<head>
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="CREATE MED Sprint — полная практическая инструкция для студентов: от наблюдаемой проблемы до исследования, прототипа и честной защиты.">
  <title>CREATE MED Sprint — практический гид для студентов</title>
  <link rel="stylesheet" href="../assets/styles/create-med-sprint.css?v=20261020-readability">
  <link rel="canonical" href="https://nasuta.ru/create-med-sprint/">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:site_name" content="Павел Насута">
  <meta property="og:title" content="CREATE MED Sprint — практический гид для студентов">
  <meta property="og:description" content="Полный маршрут от наблюдаемой проблемы до фактов, прототипа и первого разговора с пользователем.">
  <meta property="og:url" content="https://nasuta.ru/create-med-sprint/">
  <meta property="og:image" content="https://nasuta.ru/assets/images/og-create-med-sprint.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="CREATE MED Sprint — практический гид для студентов">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="CREATE MED Sprint — практический гид для студентов">
  <meta name="twitter:description" content="Полный маршрут от наблюдаемой проблемы до фактов, прототипа и первого разговора с пользователем.">
  <meta name="twitter:image" content="https://nasuta.ru/assets/images/og-create-med-sprint.jpg">
  <meta name="twitter:image:alt" content="CREATE MED Sprint — практический гид для студентов">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Course","name":"CREATE MED Sprint","description":"Практический гид для студентов: от наблюдаемой проблемы к понятной демонстрации, фактам и первому разговору с пользователем.","inLanguage":"ru-RU","url":"https://nasuta.ru/create-med-sprint/","provider":{{"@type":"Person","name":"Павел Насута","url":"https://nasuta.ru/about/"}},"isAccessibleForFree":true}}</script>
  {metrika()}
</head>
<body>
<noscript><div><img src="https://mc.yandex.ru/watch/27865374" style="position:absolute;left:-9999px;" alt=""></div></noscript>
<div class="shell">
  <nav class="nav" aria-label="Навигация страницы"><a class="brand" href="../index.html">Павел Насута</a><div class="nav-right"><a href="../create/">CREATE</a><a href="#guide">Инструкция</a><a href="#contact">Контакты</a><a href="../assets/downloads/CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.pdf" download>Скачать PDF ↓</a></div></nav>
  <main>
    <header class="hero med-hero">
      <div class="hero-grid">
        <div><div class="kicker">Практический гид для студентов · октябрь 2026</div><h1><em>CREATE MED</em><br>Sprint</h1><p class="lede">От наблюдаемой проблемы — к понятной демонстрации, фактам и первому разговору с пользователем.</p><div class="hero-actions"><a class="button" href="../assets/downloads/CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.pdf" download>Забрать PDF с собой ↓</a><a class="text-link" href="#guide">Начать инструкцию →</a></div></div>
        <aside class="coach-card"><p class="kicker">НИИ «МОЗГИ»</p><h2>Персональный тренер для вашего агента</h2><p>Павел Насута — AI-powered product builder</p><nav class="coach-links" aria-label="Связаться с Павлом Насутой">{compact_contact_icons()}</nav></aside>
      </div>
      <div class="letters med-letters"><div class="letter"><b>C</b><span>CONTEXT<br>ситуация</span></div><div class="letter"><b>R</b><span>RESEARCH<br>факты</span></div><div class="letter"><b>E</b><span>ELABORATION<br>Offer / MVP</span></div><div class="letter"><b>A</b><span>ASSEMBLE<br>демо</span></div><div class="letter"><b>T</b><span>TEST<br>проверка</span></div></div>
    </header>
    <aside class="bias-note"><div class="kicker">Проверка мышления</div><div><h2>Не выдавайте первую правдоподобную версию за факт.</h2><p>Когда отделяете факт от гипотезы и проверяете источник, помогает <a href="../biases/index.html">справочник когнитивных искажений</a>: он даёт язык для ловушек мышления, которые мешают исследованию и продуктовым решениям.</p></div></aside>
    {''.join(rendered)}
  </main>
  <footer class="footer"><span>© Павел Насута</span><span>CREATE MED Sprint · практический гид</span></footer>
</div>
<script src="../assets/scripts/create-med-sprint.js" defer></script>
</body>
</html>
"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
