from pathlib import Path
import json
import re
import unittest

from PIL import Image

from tools.build_skills import load_registry, public_items


ROOT = Path(__file__).resolve().parents[1]
SLUG = "adaptive-english-tutor"
PAGE = ROOT / "skills" / SLUG / "index.html"
IMAGE = ROOT / "assets" / "images" / "og-skill-adaptive-english-tutor.jpg"
REPOSITORY = "https://github.com/pavelnasuta/adaptive-english-tutor"


class AdaptiveEnglishTutorPageTests(unittest.TestCase):
    def test_public_registry_entry_is_complete_and_truthful(self):
        record = next(item for item in public_items(load_registry(ROOT / "data/skills.json")) if item["slug"] == SLUG)
        self.assertEqual(record["status"], "released")
        self.assertEqual(record["repository_url"], REPOSITORY)
        self.assertEqual(record["page_url"], f"skills/{SLUG}/index.html")
        self.assertEqual(record["version"], "0.1.0")
        self.assertEqual(record["license"], "MIT")
        self.assertEqual(record["compatibility"]["hermes"], "verified")
        self.assertEqual(record["compatibility"]["claude-code"], "not-applicable")
        self.assertEqual(record["compatibility"]["codex"], "not-applicable")
        self.assertEqual(record["compatibility"]["opencode"], "not-applicable")
        self.assertEqual(record["compatibility"]["agents-md"], "not-applicable")

    def test_page_has_installation_truth_privacy_boundaries_and_social_image(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn(REPOSITORY, html)
        self.assertIn("hermes skills tap add pavelnasuta/adaptive-english-tutor", html)
        self.assertIn("hermes skills install pavelnasuta/adaptive-english-tutor/skills/adaptive-english-tutor", html)
        self.assertIn("не определяет официальный уровень CEFR", html)
        self.assertIn("не публикует переписки и голосовые", html)
        self.assertIn('href="/skills/"', html)
        self.assertIn('rel="noopener"', html)
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        self.assertEqual(len(blocks), 1)
        schema = json.loads(blocks[0])
        self.assertEqual(schema["@type"], "SoftwareSourceCode")
        self.assertEqual(schema["codeRepository"], REPOSITORY)
        self.assertIn("og-skill-adaptive-english-tutor.jpg", html)
        with Image.open(IMAGE) as image:
            self.assertEqual(image.size, (1200, 630))
            self.assertEqual(image.format, "JPEG")

    def test_hero_heading_preserves_words_for_screen_readers_and_search(self):
        html = PAGE.read_text(encoding="utf-8")
        heading = re.search(r"<h1>(.*?)</h1>", html, re.S)
        self.assertIsNotNone(heading)
        assert heading is not None
        self.assertEqual(re.sub(r"<[^>]+>", "", heading.group(1)).strip(), "Adaptive English Tutor")

    def test_discoverability_files_list_the_live_page(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("https://nasuta.ru/skills/adaptive-english-tutor/", sitemap)
        self.assertIn("https://nasuta.ru/skills/adaptive-english-tutor/", llms)


if __name__ == "__main__":
    unittest.main()
