from pathlib import Path
import unittest

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SERIES = (
    (
        "agent-in-marketing-agency",
        "Агент в маркетинговом агентстве: как вернуть контекст в операционную работу",
    ),
    (
        "ai-agent-pilot-for-agency",
        "Как внедрять AI-агента в агентство: пилот, данные и границы",
    ),
    (
        "ai-operating-system-marketing-agency",
        "AI Operating System для маркетингового агентства: продажи, production, знания и экономика в одном контуре",
    ),
)


class AgencyAiSeriesTests(unittest.TestCase):
    def test_each_article_has_complete_publication_contract(self):
        for slug, title in SERIES:
            with self.subTest(slug=slug):
                page = ROOT / "articles" / slug / "index.html"
                self.assertTrue(page.is_file())
                html = page.read_text(encoding="utf-8")
                route = f"https://nasuta.ru/articles/{slug}/"
                cover = f"https://nasuta.ru/assets/images/og-{slug}.jpg"
                self.assertIn(f"<h1>{title}</h1>", html)
                self.assertIn(f'<link rel="canonical" href="{route}">', html)
                self.assertIn(f'property="og:image" content="{cover}"', html)
                self.assertIn(f'name="twitter:image" content="{cover}"', html)
                self.assertIn('"@type": "BlogPosting"', html)
                self.assertNotIn('sources">', html)

    def test_series_is_linked_from_home_archive_hub_and_discovery_files(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        archive = (ROOT / "articles" / "index.html").read_text(encoding="utf-8")
        hub = (ROOT / "articles" / "ai-agents" / "index.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        for slug, _ in SERIES:
            with self.subTest(slug=slug):
                route = f"https://nasuta.ru/articles/{slug}/"
                self.assertIn(f"/articles/{slug}/", home)
                self.assertIn(f'href="/articles/{slug}/"', archive)
                self.assertIn(f"/articles/{slug}/", hub)
                self.assertIn(route, sitemap)
                self.assertIn(route, llms)

    def test_each_article_has_a_distinct_valid_social_cover(self):
        covers = []
        for slug, _ in SERIES:
            path = ROOT / "assets" / "images" / f"og-{slug}.jpg"
            self.assertTrue(path.is_file())
            with Image.open(path) as image:
                self.assertEqual(image.size, (1200, 630))
                self.assertEqual(image.format, "JPEG")
            covers.append(path.read_bytes())
        self.assertEqual(len(covers), len(set(covers)))


if __name__ == "__main__":
    unittest.main()
