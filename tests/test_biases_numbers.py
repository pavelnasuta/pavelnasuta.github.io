import re
from pathlib import Path
import tempfile
import unittest

from tools.build_biases import build, load_catalogue

ROOT = Path(__file__).resolve().parents[1]


class BiasesNumbersTests(unittest.TestCase):
    def test_every_detail_number_matches_its_catalogue_row(self):
        items = load_catalogue(ROOT / 'content/biases/catalogue.json')
        published = [item for item in items if item['published']]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build(root, items)
            catalogue = (root / 'biases/index.html').read_text()
            numbers = re.findall(r'class="bias-row__number">(\d+)</span>', catalogue)
            self.assertEqual(len(numbers), len(published))
            for number, item in zip(numbers, published):
                with self.subTest(slug=item['slug']):
                    detail = (root / 'biases' / item['slug'] / 'index.html').read_text()
                    self.assertIn(f'class="article-number" aria-label="Номер карточки в каталоге">№ {number}</p>', detail)
                    self.assertIn(f'<h1>{item["russian_name"]}</h1>', detail)
                    self.assertIn(f'<p class="eyebrow">{item["detail_category"]}</p>', detail)


if __name__ == '__main__':
    unittest.main()
