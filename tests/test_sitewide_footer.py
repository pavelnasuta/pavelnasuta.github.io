from pathlib import Path
import tempfile
import unittest

from tools.apply_site_footer import update_page


ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.rglob("*.html"))
REQUIRED_LINKS = (
    'href="/articles/"',
    'href="/skills/"',
    'href="/create/"',
    'href="/biases/"',
    'href="/about/"',
    'href="/contact/"',
    'href="/pomokitty/"',
    'href="https://menhausen.com/"',
    'href="https://t.me/niimozgii"',
    'href="https://www.linkedin.com/in/nasuta"',
    'href="https://github.com/pavelnasuta"',
    'href="mailto:pavelnasuta@gmail.com"',
)


class SitewideFooterTests(unittest.TestCase):
    def test_every_html_page_has_the_same_navigable_footer(self):
        self.assertGreater(len(PAGES), 0)
        for page in PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                html = page.read_text(encoding="utf-8")
                self.assertIn('href="/assets/styles/footer.css"', html)
                self.assertIn('<footer class="site-footer" data-site-footer="global">', html)
                self.assertIn('aria-label="Навигация в подвале"', html)
                for link in REQUIRED_LINKS:
                    self.assertIn(link, html)

    def test_sitewide_footer_has_descriptive_navigation_groups(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for label in ("Разделы", "Проекты", "Связь"):
            self.assertIn(f">{label}</h2>", html)
        self.assertIn("Product builder · AI-агенты · автоматизация", html)

    def test_footer_generator_is_idempotent(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary_directory:
            page = Path(temporary_directory) / "index.html"
            page.write_text(source, encoding="utf-8")
            self.assertFalse(update_page(page))
            self.assertEqual(page.read_text(encoding="utf-8"), source)


if __name__ == "__main__":
    unittest.main()
