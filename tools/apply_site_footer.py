"""Apply the shared footer and cookie notice to every static HTML route."""

from pathlib import Path
import re

try:
    from tools.site_footer import SITE_FOOTER, STYLESHEET
except ModuleNotFoundError:  # Direct execution from tools/.
    from site_footer import SITE_FOOTER, STYLESHEET


ROOT = Path(__file__).resolve().parents[1]


def update_page(page: Path) -> bool:
    html = page.read_text(encoding="utf-8")
    original = html
    for asset in STYLESHEET.splitlines():
        asset = asset.strip()
        if asset and asset not in html:
            html = html.replace("</head>", f"  {asset}\n</head>", 1)

    html = re.sub(
        r'\s*<aside class="cookie-notice"(?=\s|>).*?</aside>\s*',
        "\n",
        html,
        flags=re.S,
    )
    updated, count = re.subn(r"<footer\b[^>]*>.*?</footer>", SITE_FOOTER, html, count=1, flags=re.S)
    if count == 0:
        updated, injected = re.subn(r"</body>", SITE_FOOTER + "\n</body>", html, count=1, flags=re.S)
        if injected != 1:
            raise RuntimeError(f"Could not add a footer to {page.relative_to(ROOT)}")
    elif count != 1:
        raise RuntimeError(f"Expected one footer in {page.relative_to(ROOT)}, found {count}")
    if updated != original:
        page.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    pages = sorted(ROOT.rglob("*.html"))
    changed = sum(update_page(page) for page in pages)
    print(f"Updated {changed} of {len(pages)} HTML pages")


if __name__ == "__main__":
    main()
