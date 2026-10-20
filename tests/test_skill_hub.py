from pathlib import Path
import unittest

from tools.build_skills import build


ROOT = Path(__file__).resolve().parents[1]


class SkillHubTests(unittest.TestCase):
    def setUp(self):
        build(ROOT, ROOT / "data/skills.json")
        self.html = (ROOT / "skills/index.html").read_text(encoding="utf-8")

    def test_hub_lists_only_the_current_public_records(self):
        self.assertIn("Book Summary Skill", self.html)
        self.assertIn("Adaptive Support Dialogue", self.html)
        self.assertIn("Ассистент руководителя", self.html)
        self.assertNotIn("Art-directing visuals", self.html)
        self.assertEqual(self.html.count('class="skill-card"'), 3)

    def test_hub_has_metadata_filters_and_real_local_links(self):
        self.assertIn('<link rel="canonical" href="https://nasuta.ru/skills/">', self.html)
        self.assertIn('"@type":"CollectionPage"', self.html)
        self.assertIn('data-filter="category"', self.html)
        self.assertIn('href="book-summary/index.html"', self.html)
        self.assertIn('href="management-assistant/index.html"', self.html)
        self.assertIn('assets/styles/skills-index.css', self.html)


if __name__ == "__main__":
    unittest.main()
