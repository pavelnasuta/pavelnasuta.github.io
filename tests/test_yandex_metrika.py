from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
COUNTER_ID = "27865374"
HTML_PAGES = sorted(ROOT.rglob("*.html"))


class YandexMetrikaTests(unittest.TestCase):
    def test_every_html_page_has_one_configured_counter(self):
        self.assertGreater(len(HTML_PAGES), 0)

        for page in HTML_PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                html = page.read_text(encoding="utf-8")
                self.assertEqual(html.count("https://mc.yandex.ru/metrika/tag.js"), 1)
                self.assertEqual(html.count(f"ym({COUNTER_ID}, 'init'"), 1)
                self.assertEqual(html.count(f"https://mc.yandex.ru/watch/{COUNTER_ID}"), 1)
                self.assertIn("clickmap:true", html)
                self.assertIn("accurateTrackBounce:true", html)
                self.assertIn("trackLinks:true", html)

                script_start = html.index("https://mc.yandex.ru/metrika/tag.js")
                self.assertLess(script_start, html.index("</head>"))

                noscript_start = html.index(f"https://mc.yandex.ru/watch/{COUNTER_ID}")
                self.assertGreater(noscript_start, html.index("<body"))

    def test_counter_has_no_duplicate_script_loaders(self):
        for page in HTML_PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                html = page.read_text(encoding="utf-8")
                self.assertEqual(
                    len(re.findall(r"document\.scripts\.length", html)),
                    1,
                )


if __name__ == "__main__":
    unittest.main()
