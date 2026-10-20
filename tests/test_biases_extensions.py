import json
from pathlib import Path
import re
import unittest
from tools.build_biases import render_catalogue

ROOT = Path(__file__).resolve().parents[1]

class BiasesExtensionsTests(unittest.TestCase):
    def setUp(self):
        self.items = json.loads((ROOT / 'content/biases/catalogue.json').read_text())['items']

    def test_extension_is_appended_without_renumbering_original_cards(self):
        self.assertEqual(len(self.items), 189)
        self.assertEqual(self.items[111]['slug'], 'dunningkruger-effect')
        self.assertEqual(self.items[152]['slug'], 'bikeshedding-effect')
        self.assertEqual(self.items[187]['slug'], 'tip-of-the-tongue-phenomenon')
        card = self.items[188]
        self.assertEqual(card['slug'], 'texas-sharpshooter-fallacy')
        self.assertEqual(card['detail_category'], 'Когда не хватает смысла')
        self.assertTrue(card['published'])

    def test_catalogue_search_includes_alternative_names(self):
        catalogue = render_catalogue(self.items)
        for slug, alias in [('bikeshedding-effect', 'велосипедного гаража'), ('dunningkruger-effect', 'даннинга крюгера')]:
            match = re.search(r'<a class="bias-row"[^>]*href="'+slug+r'/index.html"[^>]*data-search="([^"]*)"', catalogue)
            self.assertIsNotNone(match)
            self.assertIn(alias, match.group(1))

if __name__ == '__main__':
    unittest.main()
