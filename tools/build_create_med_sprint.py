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

DOCUMENTS = (
    ("08_ГИД_ДЛЯ_СТУДЕНТОВ.md", "Практический гид для студентов", True),
    ("01_СИСТЕМНЫЙ_ПРОМПТ_CHATGPT.md", "Системный промпт для ChatGPT Project", False),
    ("02_ПРОМПТЫ_PERPLEXITY.md", "Промпты для Perplexity", False),
    ("04_ПРОМПТ_ЛЕНДИНГ_И_ПРОТОТИП.md", "Лендинг и кликабельный прототип", False),
    ("05_ПИТЧ_И_ЗАЩИТА.md", "Питч и защита", False),
    ("06_РАБОЧАЯ_КАРТА_КОНЦЕПЦИИ.md", "Рабочая карта концепции", False),
    ("07_КАК_РАБОТАТЬ_В_CHATGPT_PROJECT.md", "Как работать в ChatGPT Project", False),
    ("10_ВИЗУАЛЬНАЯ_ФИЛОСОФИЯ.md", "Визуальная философия", False),
    ("11_ПРОДУКТОВЫЙ_ТЕЗАУРУС.md", "Полный продуктовый тезаурус", False),
)


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
    result = ["<div class=\"table-wrap\"><table><thead><tr>"]
    result.extend(f"<th>{inline(cell)}</th>" for cell in head)
    result.append("</tr></thead><tbody>")
    for row in body:
        result.append("<tr>")
        result.extend(f"<td>{inline(cell)}</td>" for cell in row)
        result.append("</tr>")
    result.append("</tbody></table></div>")
    return "".join(result)


def render_markdown(source: str) -> str:
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
                "<div class=\"prompt-block\">"
                f"<button type=\"button\" class=\"copy\" data-copy-prompt aria-label=\"Скопировать промпт {copy_number}\">Скопировать</button>"
                f"<pre><code class=\"language-{language}\">{escape(chr(10).join(code))}</code></pre></div>"
            )
        elif re.match(r"^#{1,4}\s+", line):
            level = len(line) - len(line.lstrip("#"))
            text = line[level:].strip()
            level = min(level + 1, 5)
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


def metrika() -> str:
    return """<!-- Yandex.Metrika counter -->
<script type=\"text/javascript\">
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,'script','https://mc.yandex.ru/metrika/tag.js','ym');
ym(27865374, 'init', {clickmap:true, referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
</script>
<!-- /Yandex.Metrika counter -->"""


def main() -> None:
    rendered: list[str] = []
    for document_index, (filename, label, is_core) in enumerate(DOCUMENTS):
        content = render_markdown((SOURCE_DIR / filename).read_text(encoding="utf-8"))
        if is_core:
            rendered.append(f'<section class="guide-copy" id="guide"><div class="kicker">Полная инструкция</div>{content}</section>')
        else:
            material_id = ' id="materials"' if document_index == 1 else ""
            rendered.append(
                f'<section class="material"{material_id}>'
                '<details class="material-details">'
                f'<summary><span>Дополнительный материал</span>{escape(label)}</summary>'
                f'<div class="material-body">{content}</div></details></section>'
            )
    rendered.append(
        '<section class="material">'
        '<details class="material-details pdf-source">'
        '<summary><span>Полнота материала</span>Текстовая версия PDF-раздатки</summary>'
        '<div class="material-body"><p>Этот блок сохраняет полный извлечённый текст оригинальной раздатки. Для чтения используйте инструкцию выше; для печати и передачи — скачайте PDF.</p>'
        f'<pre class="pdf-text">{escape(PDF_TEXT.read_text(encoding="utf-8"))}</pre>'
        '</div></details></section>'
    )

    page = f"""<!doctype html>
<html lang="ru">
<head>
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="CREATE MED Sprint — полная практическая инструкция для студентов: от наблюдаемой проблемы до исследования, прототипа и честной защиты.">
  <title>CREATE MED Sprint — практический гид для студентов</title>
  <link rel="stylesheet" href="../assets/styles/create-med-sprint.css?v=initial-7febd99">
  <link rel="canonical" href="https://nasuta.ru/create-med-sprint/">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:site_name" content="Павел Насута">
  <meta property="og:title" content="CREATE MED Sprint — практический гид для студентов">
  <meta property="og:description" content="Полный маршрут от наблюдаемой проблемы до фактов, прототипа и первого разговора с пользователем.">
  <meta property="og:url" content="https://nasuta.ru/create-med-sprint/">
  <meta property="og:image" content="https://nasuta.ru/assets/images/og-pavel-nasuta-agents.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="CREATE MED Sprint — практический гид для студентов">
  <meta name="twitter:description" content="Полный маршрут от наблюдаемой проблемы до фактов, прототипа и первого разговора с пользователем.">
  <meta name="twitter:image" content="https://nasuta.ru/assets/images/og-pavel-nasuta-agents.jpg">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Course","name":"CREATE MED Sprint","description":"Практический гид для студентов: от наблюдаемой проблемы к понятной демонстрации, фактам и первому разговору с пользователем.","inLanguage":"ru-RU","url":"https://nasuta.ru/create-med-sprint/","provider":{{"@type":"Person","name":"Павел Насута","url":"https://nasuta.ru/about/"}},"isAccessibleForFree":true}}</script>
  {metrika()}
</head>
<body>
<noscript><div><img src="https://mc.yandex.ru/watch/27865374" style="position:absolute;left:-9999px;" alt=""></div></noscript>
<div class="shell">
  <nav class="nav" aria-label="Навигация страницы"><a class="brand" href="../index.html">Павел Насута</a><div class="nav-right"><a href="../create/">CREATE</a><a href="#guide">Инструкция</a><a href="../assets/downloads/CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.pdf" download>Скачать PDF ↓</a></div></nav>
  <main>
    <header class="hero med-hero">
      <div class="hero-grid">
        <div><div class="kicker">Практический гид для студентов · октябрь 2026</div><h1><em>CREATE MED</em><br>Sprint</h1><p class="lede">От наблюдаемой проблемы — к понятной демонстрации, фактам и первому разговору с пользователем.</p><div class="hero-actions"><a class="button" href="../assets/downloads/CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.pdf" download>Забрать PDF с собой ↓</a><a class="text-link" href="#guide">Начать инструкцию →</a></div></div>
        <aside class="coach-card"><p class="kicker">НИИ «МОЗГИ»</p><h2>Персональный тренер для вашего агента</h2><p>Павел Насута — AI-powered product builder</p><a class="button" href="https://t.me/niimozgii" target="_blank" rel="noopener">Открыть канал ↗</a><nav class="coach-links" aria-label="Связаться с Павлом Насутой"><a href="https://t.me/pavelnasuta" target="_blank" rel="noopener">Telegram Павла</a><a href="https://www.linkedin.com/in/nasuta" target="_blank" rel="noopener">LinkedIn</a><a href="mailto:pavelnasuta@gmail.com">Написать по email</a></nav></aside>
      </div>
      <div class="letters med-letters"><div class="letter"><b>C</b><span>CONTEXT<br>ситуация</span></div><div class="letter"><b>R</b><span>RESEARCH<br>факты</span></div><div class="letter"><b>E</b><span>ELABORATION<br>Offer / MVP</span></div><div class="letter"><b>A</b><span>ASSEMBLE<br>демо</span></div><div class="letter"><b>T</b><span>TEST<br>проверка</span></div></div>
    </header>
    <section class="how quick-links"><div class="kicker">На странице</div><div><h2>Работайте по порядку. Все промпты копируются одним нажатием.</h2><div class="how-steps"><a class="how-step" href="#guide"><b>ИНСТРУКЦИЯ</b><p>Полный маршрут, правила и чек-листы.</p></a><a class="how-step" href="#materials"><b>МАТЕРИАЛЫ</b><p>Рабочая карта, тезаурус и подробные инструкции.</p></a><a class="how-step" href="../assets/downloads/CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.pdf" download><b>PDF</b><p>Версия раздатки для скачивания и печати.</p></a></div></div></section>
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
