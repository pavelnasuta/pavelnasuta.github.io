from pathlib import Path
import json
import re
import unittest

from PIL import Image

from tools.build_skills import load_registry, public_items


ROOT = Path(__file__).resolve().parents[1]
SLUG = "hermes-repo-quarantine"
PAGE = ROOT / "skills" / SLUG / "index.html"
IMAGE = ROOT / "assets" / "images" / "og-skill-hermes-repo-quarantine.jpg"
REPO = "https://github.com/pavelnasuta/hermes-repo-quarantine"
ROUTE = "https://nasuta.ru/skills/hermes-repo-quarantine/"


class HermesRepoQuarantinePageTests(unittest.TestCase):
    def test_registry_hub_home_and_sitemap_publish_the_skill(self):
        records = public_items(load_registry(ROOT / "data/skills.json"))
        record = next(item for item in records if item["slug"] == SLUG)
        self.assertEqual(record["status"], "released")
        self.assertEqual(record["version"], "0.2.0")
        self.assertEqual(record["repository_url"], REPO)
        self.assertEqual(record["page_url"], "skills/hermes-repo-quarantine/index.html")
        self.assertIn("Hermes RepoQuarantine", (ROOT / "skills" / "index.html").read_text(encoding="utf-8"))
        self.assertIn('href="/skills/hermes-repo-quarantine/"', (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn(ROUTE, (ROOT / "sitemap.xml").read_text(encoding="utf-8"))

    def test_page_has_verified_install_contract_and_social_metadata(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn(REPO, html)
        self.assertIn("pavelnasuta/hermes-repo-quarantine/skills/hermes-repo-quarantine", html)
        self.assertIn("ALLOW_READ_ONLY", html)
        self.assertIn("не sandbox и не антивирус", html)
        self.assertIn("Claude Code", html)
        self.assertIn("Codex", html)
        for key in ("og:title", "og:description", "og:image", "og:image:width", "og:image:height", "og:image:alt", "twitter:image"):
            self.assertIn(key, html)
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        self.assertEqual(len(blocks), 1)
        schema = json.loads(blocks[0])
        self.assertEqual(schema["codeRepository"], REPO)
        self.assertEqual(schema["softwareVersion"], "0.2.0")

    def test_original_social_image_is_a_1200_by_630_jpeg(self):
        self.assertTrue(IMAGE.is_file())
        with Image.open(IMAGE) as image:
            self.assertEqual(image.size, (1200, 630))
            self.assertEqual(image.format, "JPEG")


if __name__ == "__main__":
    unittest.main()
