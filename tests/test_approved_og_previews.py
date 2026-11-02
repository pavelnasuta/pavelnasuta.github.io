from pathlib import Path
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
ARTICLE = ROOT / "articles" / "ai-maturity-in-company" / "index.html"
HOME_ASSET = ROOT / "assets" / "images" / "og-pavel-nasuta-agents.jpg"
ARTICLE_ASSET = ROOT / "assets" / "images" / "og-ai-maturity-in-company.jpg"


class ApprovedOgPreviewTests(unittest.TestCase):
    def test_home_uses_approved_personal_preview_asset(self):
        html = HOME.read_text(encoding="utf-8")
        url = "https://nasuta.ru/assets/images/og-pavel-nasuta-agents.jpg"
        self.assertIn(f'property="og:image" content="{url}"', html)
        self.assertIn(f'name="twitter:image" content="{url}"', html)
        with Image.open(HOME_ASSET) as image:
            self.assertEqual(image.size, (1200, 630))
            self.assertEqual(image.format, "JPEG")

    def test_latest_article_uses_its_own_approved_preview_asset(self):
        html = ARTICLE.read_text(encoding="utf-8")
        url = "https://nasuta.ru/assets/images/og-ai-maturity-in-company.jpg"
        self.assertIn(f'property="og:image" content="{url}"', html)
        self.assertIn(f'name="twitter:image" content="{url}"', html)
        self.assertIn(f'"image":"{url}"', html)
        with Image.open(ARTICLE_ASSET) as image:
            self.assertEqual(image.size, (1200, 630))
            self.assertEqual(image.format, "JPEG")


if __name__ == "__main__":
    unittest.main()
