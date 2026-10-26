from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class HomeSkillHubEntryTests(unittest.TestCase):
    def test_home_has_a_clear_skill_hub_entry_and_description(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="skills/index.html"', home)
        self.assertIn('aria-label="Открыть каталог Skills для AI-агентов"', home)
        self.assertIn('Все skills →', home)
        self.assertIn('Каталог готовых навыков для AI-агентов', home)


if __name__ == "__main__":
    unittest.main()
