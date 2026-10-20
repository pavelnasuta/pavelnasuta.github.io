from pathlib import Path
import unittest

from tools.build_skills import build


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "book-summary": "OPEN SOURCE",
    "adaptive-support-dialogue": "OPEN SOURCE",
    "management-assistant": "PRIVATE PILOT",
}
REQUIRED_SECTIONS = ("purpose", "scenarios", "start", "workflow", "agents", "limits", "release")


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

    def test_each_current_skill_page_has_hub_sections_and_return_route(self):
        for slug, status in PAGES.items():
            html = (ROOT / "skills" / slug / "index.html").read_text(encoding="utf-8")
            with self.subTest(slug=slug):
                for section in REQUIRED_SECTIONS:
                    self.assertIn(f'id="{section}"', html)
                self.assertIn('href="../index.html"', html)
                self.assertIn(status, html)
                self.assertIn("Последнее существенное обновление", html)


if __name__ == "__main__":
    unittest.main()
