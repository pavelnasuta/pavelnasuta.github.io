from pathlib import Path
import unittest

from tools.build_skills import build


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "book-summary": "OPEN SOURCE",
    "adaptive-support-dialogue": "OPEN SOURCE",
    "management-assistant": "PRIVATE PILOT",
    "anytype-agent-skill": "PUBLIC REPOSITORY",
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
        self.assertIn("Anytype Agent Skill", self.html)
        self.assertIn("Art-directing visuals", self.html)
        self.assertIn("Telegram Channel Analytics", self.html)
        self.assertIn("Yandex Metrica Analytics Full", self.html)
        self.assertEqual(self.html.count('class="skill-card"'), 7)

    def test_hub_has_metadata_filters_and_real_local_links(self):
        self.assertIn('<link rel="canonical" href="https://nasuta.ru/skills/">', self.html)
        self.assertIn('"@type":"CollectionPage"', self.html)
        self.assertIn('data-filter="category"', self.html)
        self.assertIn('href="book-summary/index.html"', self.html)
        self.assertIn('href="management-assistant/index.html"', self.html)
        self.assertIn('href="anytype-agent-skill/index.html"', self.html)
        self.assertIn('href="art-directing-visuals/index.html"', self.html)
        self.assertIn('href="telegram-channel-analytics/index.html"', self.html)
        self.assertIn('href="yandex-metrica-analytics-full/index.html"', self.html)
        self.assertIn('assets/styles/skills-index.css', self.html)

    def test_hub_keeps_social_preview_without_an_inline_hero_illustration(self):
        self.assertIn('https://nasuta.ru/assets/images/og-skills-hub.jpg', self.html)
        self.assertNotIn('class="hero-visual"', self.html)

    def test_each_current_skill_page_has_hub_sections_and_return_route(self):
        for slug, status in PAGES.items():
            html = (ROOT / "skills" / slug / "index.html").read_text(encoding="utf-8")
            with self.subTest(slug=slug):
                for section in REQUIRED_SECTIONS:
                    self.assertIn(f'id="{section}"', html)
                self.assertIn('href="/skills/"', html)
                self.assertIn(status, html)
                self.assertIn("Последнее существенное обновление", html)
                self.assertIn('class="hero-mark', html)
                self.assertGreaterEqual(html.count('class="skill-icon"'), 4)
                self.assertIn('aria-hidden="true"', html)
    def test_anytype_page_uses_the_site_canonical_network_icon(self):
        html = (ROOT / "skills" / "anytype-agent-skill" / "index.html").read_text(encoding="utf-8")
        self.assertIn('<rect x="16" y="16" width="6" height="6" rx="1">', html)
        self.assertIn('<path d="M12 12V8">', html)


if __name__ == "__main__":
    unittest.main()
