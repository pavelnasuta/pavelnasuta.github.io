from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AnytypeSkillHomepageTests(unittest.TestCase):
    def test_homepage_links_to_the_local_anytype_skill_page(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Anytype Agent Skill", home)
        self.assertIn('href="skills/anytype-agent-skill/index.html"', home)
        self.assertIn("structured Anytype knowledge spaces", home)


if __name__ == "__main__":
    unittest.main()
