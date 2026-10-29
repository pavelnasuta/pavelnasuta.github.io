from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.rglob("*.html"))


class BackToTopTests(unittest.TestCase):
    def test_every_static_route_has_one_shared_back_to_top_control(self):
        self.assertGreater(len(PAGES), 0)
        for page in PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                html = page.read_text(encoding="utf-8")
                self.assertIn('href="/assets/styles/back-to-top.css?v=1"', html)
                self.assertIn('<script defer src="/assets/scripts/back-to-top.js?v=1"></script>', html)
                self.assertEqual(html.count('data-back-to-top'), 1)
                self.assertIn('<a class="back-to-top" href="#top" data-back-to-top', html)
                self.assertIn('<body id="top"', html)
                self.assertIn('class="lucide lucide-arrow-up"', html)

    def test_button_respects_motion_preference_and_only_shows_after_scrolling(self):
        script = (ROOT / "assets" / "scripts" / "back-to-top.js").read_text(encoding="utf-8")
        css = (ROOT / "assets" / "styles" / "back-to-top.css").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion: reduce", script)
        self.assertIn("document.documentElement.scrollHeight > window.innerHeight * 1.5", script)
        self.assertIn("window.scrollTo({ top: 0", script)
        self.assertIn("@media(prefers-reduced-motion:reduce)", css)


if __name__ == "__main__":
    unittest.main()
