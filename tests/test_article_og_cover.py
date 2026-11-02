from pathlib import Path
import unittest
from PIL import Image

from tools.article_og_cover import CoverRequest, render_cover

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "articles" / "ai-agent-knowledge-storage" / "index.html"
HOME = ROOT / "index.html"
ARCHIVE = ROOT / "articles" / "index.html"
ASSET_URL = "https://nasuta.ru/assets/images/og-ai-agent-knowledge-storage.jpg"
ASSET_PATH = ROOT / "assets" / "images" / "og-ai-agent-knowledge-storage.jpg"


class ArticleOgCoverTests(unittest.TestCase):
    def test_renderer_writes_1200_by_630_jpeg(self):
        output = ROOT / "assets" / "images" / "og-ai-agent-knowledge-storage.jpg"
        render_cover(CoverRequest(
            slug="ai-agent-knowledge-storage",
            title="Агенту нужно не только помнить. Ему нужно куда складывать работу",
            variant="overshirt-standing",
            output_path=output,
        ), ROOT)
        with Image.open(output) as image:
            self.assertEqual(image.size, (1200, 630))
            self.assertEqual(image.format, "JPEG")

    def test_article_uses_cover_in_metadata_and_hero_after_explicit_approval(self):
        html = ARTICLE.read_text(encoding="utf-8")
        self.assertIn(f'property="og:image" content="{ASSET_URL}"', html)
        self.assertIn(f'name="twitter:image" content="{ASSET_URL}"', html)
        self.assertIn('src="../../assets/images/og-ai-agent-knowledge-storage.jpg"', html)

    def test_home_and_archive_reference_same_cover(self):
        for page in (HOME, ARCHIVE):
            self.assertIn("og-ai-agent-knowledge-storage.jpg", page.read_text(encoding="utf-8"))

    def test_cover_asset_exists(self):
        self.assertTrue(ASSET_PATH.is_file())


if __name__ == "__main__":
    unittest.main()
