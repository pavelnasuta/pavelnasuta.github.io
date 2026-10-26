from pathlib import Path
import unittest

from PIL import Image

from tools.build_skills import load_registry, public_items


ROOT = Path(__file__).resolve().parents[1]
SLUG = "telegram-channel-analytics"
PAGE = ROOT / "skills" / SLUG / "index.html"
IMAGE = ROOT / "assets" / "images" / "og-skill-telegram-channel-analytics.jpg"
REPO = "https://github.com/pavelnasuta/telegram-channel-analytics-skill"


class TelegramChannelAnalyticsPageTests(unittest.TestCase):
    def test_registry_and_skill_hub_publish_the_skill(self):
        records = public_items(load_registry(ROOT / "data/skills.json"))
        record = next(item for item in records if item["slug"] == SLUG)
        self.assertEqual(record["status"], "released")
        self.assertEqual(record["visibility"], "public")
        self.assertEqual(record["version"], "1.0.2")
        self.assertEqual(record["repository_url"], REPO)
        self.assertEqual(record["page_url"], "skills/telegram-channel-analytics/index.html")
        hub = (ROOT / "skills" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Telegram Channel Analytics", hub)
        self.assertIn("telegram-channel-analytics/index.html", hub)

    def test_page_has_truthful_metadata_boundaries_and_original_og_image(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn(REPO, html)
        for key in (
            "og:title",
            "og:description",
            "og:image",
            "og:image:width",
            "og:image:height",
            "og:image:alt",
            "twitter:image",
        ):
            self.assertIn(key, html)
        for boundary in ("append-only", "watchlist", "MTProto", "24 часа", "14 дней"):
            self.assertIn(boundary, html)
        self.assertIn("og-skill-telegram-channel-analytics.jpg", html)
        self.assertTrue(IMAGE.is_file())
        with Image.open(IMAGE) as image:
            self.assertEqual(image.size, (1200, 630))
            self.assertEqual(image.format, "JPEG")

    def test_home_page_has_a_link_to_the_new_skill(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="skills/telegram-channel-analytics/index.html"', home)


if __name__ == "__main__":
    unittest.main()
