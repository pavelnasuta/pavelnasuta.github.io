from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.rglob("*.html"))
POLICY_ROUTE = ROOT / "cookies" / "index.html"


class CookieNoticeTests(unittest.TestCase):
    def test_every_public_page_offers_the_same_cookie_notice_and_policy(self):
        """Removing the global notice must not leave a route without disclosure."""
        self.assertGreater(len(PAGES), 0)
        for page in PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                document = page.read_text(encoding="utf-8")
                self.assertEqual(document.count('<aside class="cookie-notice" data-cookie-notice'), 1)
                self.assertIn('href="/cookies/"', document)
                self.assertIn('href="/assets/styles/cookie-notice.css"', document)
                self.assertIn('src="/assets/scripts/cookie-notice.js"', document)

    def test_policy_route_explains_metrica_and_browser_choice(self):
        """The notice link must lead to a useful explanation, not a placeholder."""
        document = POLICY_ROUTE.read_text(encoding="utf-8")
        self.assertIn("Яндекс.Метрика", document)
        self.assertIn("cookie", document.lower())
        self.assertIn("браузер", document.lower())
        self.assertIn('data-cookie-notice', document)


if __name__ == "__main__":
    unittest.main()
