from pathlib import Path
import json
import unittest

from PIL import Image

from tools.build_skills import load_registry, public_items


ROOT = Path(__file__).resolve().parents[1]
SLUG = "yandex-metrica-analytics-full"
PAGE = ROOT / "skills" / SLUG / "index.html"
IMAGE = ROOT / "assets" / "images" / "og-skill-yandex-metrica-analytics-full.jpg"
REPO = "https://github.com/pavelnasuta/yandex-metrica-analytics-full-skill"


class YandexMetricaAnalyticsPageTests(unittest.TestCase):
    def test_registry_and_page_are_a_released_public_skill(self):
        record = next(item for item in public_items(load_registry(ROOT / "data/skills.json")) if item["slug"] == SLUG)
        self.assertEqual(record["status"], "released")
        self.assertEqual(record["visibility"], "public")
        self.assertEqual(record["repository_url"], REPO)
        self.assertEqual(record["page_url"], "skills/yandex-metrica-analytics-full/index.html")
        self.assertTrue(PAGE.is_file())

    def test_page_explains_scope_install_and_data_boundaries(self):
        html = PAGE.read_text(encoding="utf-8")
        for text in ("metrika:read", "CAC, ROAS и ROI", "Вебмастера", REPO, "og-skill-yandex-metrica-analytics-full.jpg"):
            self.assertIn(text, html)
        self.assertNotIn("YANDEX_METRICA_TOKEN", html)
        self.assertNotIn("/root/", html)
        self.assertIn('href="/skills/"', html)

    def test_page_uses_a_distinct_valid_social_image(self):
        self.assertTrue(IMAGE.is_file())
        with Image.open(IMAGE) as image:
            self.assertEqual(image.size, (1200, 630))
            self.assertEqual(image.format, "JPEG")


if __name__ == "__main__":
    unittest.main()
