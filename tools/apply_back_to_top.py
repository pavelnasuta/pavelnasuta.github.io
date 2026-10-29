"""Apply the shared floating back-to-top control to every static HTML route."""

from pathlib import Path
import re

try:
    from tools.site_back_to_top import BACK_TO_TOP, LEGACY_SCRIPT, MARKER, SCRIPT, STYLESHEET
except ModuleNotFoundError:  # Direct execution from tools/.
    from site_back_to_top import BACK_TO_TOP, LEGACY_SCRIPT, MARKER, SCRIPT, STYLESHEET


ROOT = Path(__file__).resolve().parents[1]
BODY_TAG = re.compile(r"<body(?P<attributes>\s[^>]*)?>", re.I)
BACK_TO_TOP_CONTROL = re.compile(r"<(?:button|a)\b[^>]*data-back-to-top[^>]*>.*?</(?:button|a)>", re.S | re.I)


def ensure_top_anchor(html: str) -> str:
    def replace(match: re.Match[str]) -> str:
        attributes = match.group("attributes") or ""
        if re.search(r"\\bid\\s*=", attributes, re.I):
            return match.group(0)
        return f'<body id="top"{attributes}>'

    return BODY_TAG.sub(replace, html, count=1)


def update_page(page: Path) -> bool:
    html = page.read_text(encoding="utf-8")
    original = html
    html = ensure_top_anchor(html)
    if STYLESHEET not in html:
        html = html.replace("</head>", f"  {STYLESHEET}\n</head>", 1)
    html = html.replace(LEGACY_SCRIPT, SCRIPT)
    if SCRIPT not in html:
        html = html.replace("</head>", f"  {SCRIPT}\n</head>", 1)
    if MARKER in html:
        html = BACK_TO_TOP_CONTROL.sub(BACK_TO_TOP, html, count=1)
    else:
        html = html.replace("</body>", f"  {BACK_TO_TOP}\n</body>", 1)
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
