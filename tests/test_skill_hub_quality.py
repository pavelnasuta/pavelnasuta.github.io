from pathlib import Path
import json
import re
import unittest

from tools.build_skills import load_registry, public_items


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://nasuta.ru"


class SkillHubQualityTests(unittest.TestCase):
    def test_home_and_sitemap_link_to_the_hub_and_every_visible_skill(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn('href="skills/index.html"', home)
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


if __name__ == "__main__":
    unittest.main()
