from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.rglob("*.html"))
NAVIGATION_MARKER = '<nav class="site-navigation" data-site-navigation="global" aria-label="Основная навигация">'
REQUIRED_LABELS = (
    "Блог",
    "Установка Hermes",
    "Библиотека",
    "Skills для AI-агентов",
    "Когнитивные искажения",
    "C.R.E.A.T.E.",
    "Проекты",
    "Menhausen",
    "pomokitty",
    "Обо мне",
    "Контакты",
    "Личный Telegram",
    "НИИ «МОЗГИ»",
    "LinkedIn",
    "Email",
)
REQUIRED_LINKS = (
    'href="/"',
    'href="/articles/"',
    'href="/articles/hermes-agent-installation/"',
    'href="/skills/"',
    'href="/biases/"',
    'href="/create/"',
    'href="https://menhausen.com/"',
    'href="/pomokitty/"',
    'href="/about/"',
    'href="/contact/"',
    'href="https://t.me/pavelnasuta"',
    'href="https://t.me/niimozgii"',
    'href="https://www.linkedin.com/in/nasuta"',
    'href="mailto:pavelnasuta@gmail.com"',
)


class SitewideNavigationTests(unittest.TestCase):
    def test_every_html_page_has_the_same_sitewide_navigation(self):
        self.assertGreater(len(PAGES), 0)
        navigations = []
        for page in PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                html = page.read_text(encoding="utf-8")
                self.assertIn('href="/assets/styles/navigation.css?v=contacts-nav"', html)
                self.assertIn(NAVIGATION_MARKER, html)
                navigation = re.search(r'<nav class="site-navigation".*?</nav>', html, re.S)
                if navigation is None:
                    self.fail(f"Navigation markup is missing: {page.relative_to(ROOT)}")
                navigation_html = navigation.group(0)
                navigations.append(navigation_html)
                for label in REQUIRED_LABELS:
                    self.assertIn(label, navigation_html)
                for link in REQUIRED_LINKS:
                    self.assertIn(link, navigation_html)
        self.assertEqual({*navigations}, {navigations[0]})

    def test_navigation_has_accessible_dropdowns_and_mobile_control(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for control in ("site-navigation__toggle", "site-navigation__submenu-toggle"):
            self.assertIn(control, html)
        self.assertIn('aria-controls="site-navigation-panel"', html)
        self.assertIn('aria-expanded="false"', html)
        self.assertIn('site-navigation__group--contacts', html)
        css = (ROOT / "assets" / "styles" / "navigation.css").read_text(encoding="utf-8")
        self.assertIn('.site-navigation__group--contacts .site-navigation__submenu { right:0; left:auto; }', css)
        self.assertIn('target="_blank" rel="noopener"', html)

    def test_opening_a_dropdown_closes_the_other_dropdowns(self):
        script = (ROOT / "assets" / "scripts" / "navigation.js").read_text(encoding="utf-8")
        self.assertIn("group.addEventListener('toggle'", script)
        self.assertIn("other.open = false", script)


if __name__ == "__main__":
    unittest.main()
