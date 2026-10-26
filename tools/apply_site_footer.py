from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

FOOTER = '''<footer class="site-footer" data-site-footer="global">
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
      <a href="mailto:pavelnasuta@gmail.com">Email</a>
    </nav>
  </div>
  <div class="site-footer__bottom">
    <span>© 2026 Павел Насута</span>
    <a href="/contact/">Написать</a>
  </div>
</footer>'''


def update_page(page: Path) -> bool:
    html = page.read_text(encoding="utf-8")
    if '<link rel="stylesheet" href="/assets/styles/footer.css">' not in html:
        html = html.replace(
            "</head>",
            '  <link rel="stylesheet" href="/assets/styles/footer.css">\n</head>',
            1,
        )
    updated, count = re.subn(r"<footer\b[^>]*>.*?</footer>", FOOTER, html, count=1, flags=re.S)
    if count == 0:
        updated, injected = re.subn(r"</body>", FOOTER + "\n</body>", html, count=1, flags=re.S)
        if injected != 1:
            raise RuntimeError(f"Could not add a footer to {page.relative_to(ROOT)}")
    elif count != 1:
        raise RuntimeError(f"Expected one footer in {page.relative_to(ROOT)}, found {count}")
    if updated != page.read_text(encoding="utf-8"):
        page.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    pages = sorted(ROOT.rglob("*.html"))
    changed = sum(update_page(page) for page in pages)
    print(f"Updated {changed} of {len(pages)} HTML pages")


if __name__ == "__main__":
    main()
