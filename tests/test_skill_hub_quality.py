from pathlib import Path
import json
import re
import unittest

from PIL import Image

from tools.build_skills import load_registry, public_items


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://nasuta.ru"


class SkillHubQualityTests(unittest.TestCase):
    def test_home_omits_hub_but_sitemap_lists_it_and_every_visible_skill(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertNotIn('href="skills/index.html"', home)
        self.assertIn(f"{SITE}/skills/", sitemap)
        for item in public_items(load_registry(ROOT / "data/skills.json")):
            route = item["page_url"].removesuffix("index.html")
            self.assertTrue((ROOT / item["page_url"]).is_file())
            self.assertIn(f"{SITE}/{route}", sitemap)

    def test_public_skill_html_has_no_private_source_markers_or_fake_repository_links(self):
        for item in public_items(load_registry(ROOT / "data/skills.json")):
            html = (ROOT / item["page_url"]).read_text(encoding="utf-8")
            with self.subTest(slug=item["slug"]):
                self.assertNotRegex(html, r"/(?:root|home|srv)/")
                self.assertNotIn("withheld", html)
                if item["repository_url"]:
                    self.assertTrue(item["repository_url"].startswith("https://github.com/"))
                    self.assertIn(item["repository_url"], html)

    def test_hub_structured_data_is_valid_collection_page(self):
        hub = (ROOT / "skills/index.html").read_text(encoding="utf-8")
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', hub, re.S)
        self.assertEqual(len(blocks), 1)
        schema = json.loads(blocks[0])
        self.assertEqual(schema["@type"], "CollectionPage")
        self.assertEqual(len(schema["hasPart"]), 3)

    def test_each_skill_and_the_catalogue_have_distinct_og_images(self):
        expected = {
            "skills/index.html": "og-skills-hub.jpg",
            "skills/book-summary/index.html": "og-skill-book-summary.jpg",
            "skills/adaptive-support-dialogue/index.html": "og-skill-adaptive-support.jpg",
            "skills/management-assistant/index.html": "og-skill-management-assistant.jpg",
        }
        image_urls = []
        for page, image_name in expected.items():
            html = (ROOT / page).read_text(encoding="utf-8")
            with self.subTest(page=page):
                og_image = re.search(r'<meta property="og:image" content="([^"]+)">', html)
                twitter_image = re.search(r'<meta name="twitter:image" content="([^"]+)">', html)
                self.assertIsNotNone(og_image)
                self.assertIsNotNone(twitter_image)
                if og_image is None or twitter_image is None:
                    self.fail("Social image metadata is missing")
                self.assertTrue(og_image.group(1).endswith(f"/assets/images/{image_name}"))
                self.assertEqual(og_image.group(1), twitter_image.group(1))
                image_path = ROOT / "assets/images" / image_name
                self.assertTrue(image_path.is_file())
                with Image.open(image_path) as image:
                    self.assertEqual(image.size, (1200, 630))
                    self.assertEqual(image.format, "JPEG")
                image_urls.append(og_image.group(1))
        self.assertEqual(len(image_urls), len(set(image_urls)))


if __name__ == "__main__":
    unittest.main()
