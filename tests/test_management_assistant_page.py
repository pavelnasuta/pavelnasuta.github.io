from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "skills/management-assistant/index.html"


class ManagementAssistantPageTests(unittest.TestCase):
    def test_page_exposes_installation_and_repository_link(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn("Ассистент руководителя", html)
        self.assertIn("PRIVATE PILOT", html)
        self.assertIn("pavelnasuta/management-assistant-kit", html)
        self.assertIn("hermes skills install pavelnasuta/management-assistant-kit/skills/management-assistant", html)
        self.assertIn("target=\"_blank\"", html)
        self.assertIsNone(re.search(r"\bЦИП\b", html))
        self.assertIn('href="../../contact/index.html"', html)
        self.assertIn("Запросить доступ", html)

    def test_generated_bytecode_is_ignored(self):
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("__pycache__/", ignore)
        self.assertIn("*.pyc", ignore)

    def test_home_tile_links_to_site_article(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="skills/management-assistant/index.html"', home)
        self.assertIn("Ассистент руководителя", home)

    def test_page_includes_dedicated_style_and_social_metadata(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn("skills-management-assistant-index.css", html)
        self.assertIn("og-management-assistant.jpg", html)
        self.assertTrue((ROOT / "assets/styles/skills-management-assistant-index.css").is_file())
        self.assertTrue((ROOT / "assets/images/og-management-assistant.jpg").is_file())


if __name__ == "__main__":
    unittest.main()
