from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "biases" / "index.html"
DETAIL = ROOT / "biases" / "confirmation-bias" / "index.html"
COUNTER_ID = "27865374"


class BiasesPreviewTests(unittest.TestCase):
    def test_catalog_is_a_filterable_list_without_reading_instructions(self):
        html = CATALOG.read_text(encoding="utf-8")
        self.assertEqual(html.count('class="bias-row"'), 20)
        self.assertIn("Когнитивные искажения", html)
        self.assertIn("Предвзятость подтверждения", html)
        self.assertIn('id="bias-search"', html)
        self.assertEqual(html.count('data-filter='), 5)
        self.assertNotIn("Как читать каталог", html)
        self.assertNotIn("Первые 20", html)

    def test_catalog_is_not_added_to_primary_navigation(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('href="biases/', home)

    def test_preview_routes_keep_the_site_metrika_counter(self):
        for page in (CATALOG, DETAIL):
            html = page.read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertEqual(html.count("https://mc.yandex.ru/metrika/tag.js"), 1)
                self.assertEqual(html.count(f"ym({COUNTER_ID}, 'init'"), 1)
                self.assertEqual(html.count(f"https://mc.yandex.ru/watch/{COUNTER_ID}"), 1)

    def test_confirmation_card_links_readers_to_underlying_research(self):
        html = DETAIL.read_text(encoding="utf-8")
        self.assertIn('href="https://doi.org/10.1080/17470216008416717"', html)
        self.assertIn('href="https://doi.org/10.1037/1089-2680.2.2.175"', html)

    def test_detail_page_offers_catalog_and_continuation_choices(self):
        html = DETAIL.read_text(encoding="utf-8")
        self.assertIn("К каталогу", html)
        self.assertIn("Следующее", html)
        self.assertIn("Случайное", html)
        self.assertIn("confirmation-bias", html)


if __name__ == "__main__":
    unittest.main()
