from pathlib import Path
import json
import re
import unittest

from PIL import Image

from tools.build_skills import load_registry, public_items


ROOT = Path(__file__).resolve().parents[1]
SLUG = "art-directing-visuals"
PAGE = ROOT / "skills" / SLUG / "index.html"
IMAGE = ROOT / "assets" / "images" / "og-skill-art-directing-visuals.jpg"
REPO = "https://github.com/pavelnasuta/art-directing-visuals-skill"


class ArtDirectingVisualsPageTests(unittest.TestCase):
    def test_registry_and_skill_hub_publish_the_skill(self):
        records = public_items(load_registry(ROOT / "data/skills.json"))
        record = next(item for item in records if item["slug"] == SLUG)
        self.assertEqual(record["status"], "released")
        self.assertEqual(record["repository_url"], REPO)
        self.assertEqual(record["page_url"], "skills/art-directing-visuals/index.html")
        hub = (ROOT / "skills" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Art-directing visuals", hub)
        self.assertIn("/skills/art-directing-visuals/", hub)

    def test_page_has_complete_social_metadata_and_original_og_image(self):
        html = PAGE.read_text(encoding="utf-8")
        css = (ROOT / "assets/styles/skills-art-directing-visuals-index.css").read_text(encoding="utf-8")
        self.assertIn(".content{min-width:0}", css)
        self.assertIn("overflow-wrap:anywhere", css)
        self.assertIn(REPO, html)
        for key in ("og:title", "og:description", "og:image", "og:image:width", "og:image:height", "og:image:alt", "twitter:image"):
            self.assertIn(key, html)
        self.assertIn("og-skill-art-directing-visuals.jpg", html)
        self.assertTrue(IMAGE.is_file())
        with Image.open(IMAGE) as image:
            self.assertEqual(image.size, (1200, 630))
            self.assertEqual(image.format, "JPEG")

    def test_home_page_has_a_link_to_the_new_skill(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="/skills/art-directing-visuals/"', home)


if __name__ == "__main__":
    unittest.main()
