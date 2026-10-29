"""Apply the shared navigation to every static HTML route."""

from pathlib import Path
import re

try:
    from tools.site_navigation import LEGACY_STYLESHEET, SCRIPT, SITE_NAVIGATION, STYLESHEET
except ModuleNotFoundError:  # Direct execution from tools/.
    from site_navigation import LEGACY_STYLESHEET, SCRIPT, SITE_NAVIGATION, STYLESHEET


ROOT = Path(__file__).resolve().parents[1]
LEGACY_NAVIGATION = re.compile(r'\s*<nav class="(?:site-nav|nav)"[^>]*>.*?</nav>\s*', re.S)
SHARED_NAVIGATION = re.compile(r'\s*<nav class="site-navigation"[^>]*>.*?</nav>\s*', re.S)
BODY_PREFIX = re.compile(
    r'(?P<body><body\b[^>]*>)(?P<prefix>\s*(?:(?:<!--.*?-->\s*)?<noscript\b.*?</noscript>\s*(?:<!--.*?-->\s*)?)?)',
    re.S,
)


def update_page(page: Path) -> bool:
    html = page.read_text(encoding="utf-8")
    original = html
    html = LEGACY_NAVIGATION.sub("\n", html, count=1)
    html = SHARED_NAVIGATION.sub("\n", html, count=1)
    html = html.replace(LEGACY_STYLESHEET, STYLESHEET)
    if STYLESHEET not in html:
        html = html.replace("</head>", f"  {STYLESHEET}\n</head>", 1)
    if SCRIPT not in html:
        html = html.replace("</head>", f"  {SCRIPT}\n</head>", 1)

    def inject(match: re.Match[str]) -> str:
        return f"{match.group('body')}{match.group('prefix')}\n  {SITE_NAVIGATION}\n"

    html, inserted = BODY_PREFIX.subn(inject, html, count=1)
    if inserted != 1:
        raise RuntimeError(f"Could not add navigation to {page.relative_to(ROOT)}")
    if html != original:
        page.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    pages = sorted(ROOT.rglob("*.html"))
    changed = sum(update_page(page) for page in pages)
    print(f"Updated {changed} of {len(pages)} HTML pages")


if __name__ == "__main__":
    main()
