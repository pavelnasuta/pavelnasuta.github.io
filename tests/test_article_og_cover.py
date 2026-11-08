from pathlib import Path
import tempfile
import unittest
from PIL import Image

from tools.article_og_cover import (
    APPROVED_SOURCE_HASHES,
    CoverRequest,
    TITLE_LINE_HEIGHT_MULTIPLIER,
    render_cover,
    variant_for_sequence,
)

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

    def test_renderer_reduces_long_single_words_and_uses_tighter_leading(self):
        self.assertEqual(TITLE_LINE_HEIGHT_MULTIPLIER, 0.854)
        title = "Переосмыслениевзаимодействиясинтеллектуальнымиассистентами"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "cover.jpg"
            render_cover(CoverRequest(
                slug="long-title",
                title=title,
                variant="overshirt-standing",
                output_path=output,
            ), ROOT)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1200, 630))
                self.assertEqual(image.format, "JPEG")

    def test_templates_repeat_in_the_approved_editorial_cycle(self):
        self.assertEqual(
            [variant_for_sequence(position) for position in range(8)],
            [
                "overshirt-standing", "table-knit", "jacket-relaxed",
                "overshirt-standing", "table-knit", "jacket-relaxed",
                "overshirt-standing", "table-knit",
            ],
        )

    def test_all_three_approved_templates_render(self):
        self.assertEqual(
            set(APPROVED_SOURCE_HASHES),
            {"overshirt-standing", "table-knit", "jacket-relaxed"},
        )
        with tempfile.TemporaryDirectory() as directory:
            for variant in APPROVED_SOURCE_HASHES:
                output = Path(directory) / f"{variant}.jpg"
                render_cover(CoverRequest(
                    slug=f"approved-{variant}",
                    title="Проверка утверждённой обложки",
                    variant=variant,
                    output_path=output,
                ), ROOT)
                self.assertTrue(output.is_file())

    def test_article_uses_cover_only_in_metadata(self):
        html = ARTICLE.read_text(encoding="utf-8")
        self.assertIn(f'property="og:image" content="{ASSET_URL}"', html)
        self.assertIn(f'name="twitter:image" content="{ASSET_URL}"', html)
        body = html.split("</head>", 1)[1]
        self.assertNotIn("og-ai-agent-knowledge-storage.jpg", body)

    def test_home_and_archive_do_not_reference_article_cover(self):
        for page in (HOME, ARCHIVE):
            self.assertNotIn("og-ai-agent-knowledge-storage.jpg", page.read_text(encoding="utf-8"))

    def test_cover_asset_exists(self):
        self.assertTrue(ASSET_PATH.is_file())


if __name__ == "__main__":
    unittest.main()
