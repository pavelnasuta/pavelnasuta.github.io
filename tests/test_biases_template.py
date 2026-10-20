from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from tools.build_biases import build, load_catalogue, render_detail


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "content" / "biases" / "catalogue.json"
COUNTER_ID = "27865374"


class BiasesTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.items = load_catalogue(CATALOGUE)
        self.sample_item = next(item for item in self.items if item["slug"] == "confirmation-bias")

    def test_rendered_card_has_expanded_category_cta_and_seo(self) -> None:
        html = render_detail(self.sample_item, None, None)

        self.assertIn("Когда информации слишком много", html)
        self.assertIn("<h1>Предвзятость подтверждения</h1>", html)
        self.assertIn('<meta name="description" content="', html)
        self.assertIn('<link rel="canonical" href="https://nasuta.ru/biases/confirmation-bias/">', html)
        self.assertIn('"@type":"Article"', html)
        self.assertIn("Персональный тренер для вашего агента", html)
        self.assertIn("Павел Насута — AI-powered product builder", html)
        self.assertIn('href="https://t.me/niimozgii" target="_blank" rel="noopener"', html)
        self.assertIn('href="https://t.me/pavelnasuta" target="_blank" rel="noopener"', html)
        self.assertIn('href="https://www.linkedin.com/in/nasuta" target="_blank" rel="noopener"', html)
        self.assertIn('href="mailto:pavelnasuta@gmail.com"', html)
        self.assertIn('aria-label="Telegram Павла Насуты"', html)
        self.assertIn('aria-label="LinkedIn Павла Насуты"', html)
        self.assertIn('aria-label="Написать Павлу Насуте"', html)
        self.assertEqual(html.count("<svg"), 3)
        self.assertEqual(html.count("https://mc.yandex.ru/metrika/tag.js"), 1)
        self.assertEqual(html.count(f"ym({COUNTER_ID}, 'init'"), 1)
        self.assertEqual(html.count(f"https://mc.yandex.ru/watch/{COUNTER_ID}"), 1)

    def test_build_writes_only_published_detail_pages_and_a_linked_catalogue(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            built = build(root, self.items)
            catalogue = (root / "biases" / "index.html").read_text(encoding="utf-8")

            self.assertEqual(len(built), 21)
            self.assertEqual(catalogue.count('<a class="bias-row"'), 20)
            self.assertIn('href="availability-heuristic/index.html"', catalogue)
            self.assertIn('href="confirmation-bias/index.html"', catalogue)
            self.assertIn('href="anchoring/index.html"', catalogue)
            self.assertIn("Слишком много информации", catalogue)
            self.assertNotIn("Когда информации слишком много", catalogue)
            self.assertIn("availability-heuristic/index.html", catalogue)

    def test_detail_styles_provide_separate_vertical_rhythm_and_responsive_cta(self) -> None:
        css = (ROOT / "assets" / "styles" / "biases.css").read_text(encoding="utf-8")

        self.assertIn(".article-head .eyebrow", css)
        self.assertIn(".article h1", css)
        self.assertIn(".article .article-dek{margin:31px 0 0}", css)
        self.assertIn(".article .article-dek{margin-top:25px}", css)
        self.assertIn(".bias-cta", css)
        self.assertIn(".bias-cta__social", css)
        self.assertIn("@media(max-width:800px)", css)


if __name__ == "__main__":
    unittest.main()
