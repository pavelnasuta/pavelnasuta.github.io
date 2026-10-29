from pathlib import Path
import re
import unittest
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://nasuta.ru"
SITEMAP_NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class SeoGeoFrontPageTests(unittest.TestCase):
    def test_home_explains_the_human_controlled_ai_operating_model(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for phrase in (
            "управляемую работу с AI-ассистентами",
            "критичные шаги под контролем человека",
            "Hermes",
            "https://www.linkedin.com/in/nasuta",
            "https://t.me/pavelnasuta",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, html)

    def test_skill_hub_defines_a_skill_and_its_boundary(self):
        html = (ROOT / "skills" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Skills для AI-агентов, собранные из реальной работы.", html)
        self.assertIn("не плагин и не набор промптов", html)
        self.assertIn("повторяемая рабочая процедура", html)

    def test_sitemap_has_a_lastmod_for_every_canonical_url(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        urls = root.findall("s:url", SITEMAP_NS)
        self.assertTrue(urls)
        entries = {
            entry.findtext("s:loc", namespaces=SITEMAP_NS): entry.findtext("s:lastmod", namespaces=SITEMAP_NS)
            for entry in urls
        }
        self.assertTrue(all(entries.values()))
        self.assertIn(f"{SITE}/about/", entries)
        self.assertIn(f"{SITE}/skills/yandex-metrica-analytics-full/", entries)

    def test_home_entry_links_use_canonical_directory_urls(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('href="articles/index.html"', html)
        self.assertNotIn('href="skills/index.html"', html)
        self.assertIn('href="/articles/"', html)
        self.assertIn('href="/skills/"', html)



if __name__ == "__main__":
    unittest.main()
