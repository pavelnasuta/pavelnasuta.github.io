from pathlib import Path
import re
import unittest
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "articles" / "ai-agent-knowledge-storage" / "index.html"
CSS = ROOT / "assets" / "styles" / "articles-ai-agent-knowledge-storage-index.css"
HERO = ROOT / "assets" / "images" / "og-agent-knowledge-storage.jpg"
DIAGRAM = ROOT / "assets" / "images" / "agent-knowledge-storage-architecture.svg"
COUNTER_ID = "27865374"


class AgentKnowledgeStorageArticleTests(unittest.TestCase):
    def test_article_is_complete_search_ready_and_human_readable(self):
        self.assertTrue(PAGE.is_file())
        self.assertTrue(CSS.is_file())
        self.assertTrue(HERO.is_file())
        self.assertTrue(DIAGRAM.is_file())
        html = PAGE.read_text(encoding="utf-8")

        self.assertIn('<link rel="canonical" href="https://nasuta.ru/articles/ai-agent-knowledge-storage/">', html)
        self.assertIn('name="description"', html)
        self.assertIn('property="og:image" content="https://nasuta.ru/assets/images/og-agent-knowledge-storage.jpg"', html)
        self.assertIn('"@type":"BlogPosting"', html)
        self.assertIn('"datePublished":"2026-10-22"', html)
        self.assertEqual(html.count("https://mc.yandex.ru/metrika/tag.js"), 1)
        self.assertEqual(html.count(f"ym(27865374, 'init'"), 1)
        self.assertEqual(html.count(f"https://mc.yandex.ru/watch/{COUNTER_ID}"), 1)

        self.assertNotIn("## Sources", html)
        self.assertNotIn('class="sources"', html)
        self.assertNotIn('<sup><a href="#source-', html)
        self.assertIn('https://github.com/pavelnasuta/anytype-agent-skill', html)
        self.assertIn('href="../../skills/anytype-agent-skill/index.html"', html)
        self.assertIn('agent-knowledge-storage-architecture.svg', html)

    def test_assets_match_the_article_contract(self):
        with Image.open(HERO) as hero:
            self.assertEqual(hero.size, (1200, 630))
        svg = DIAGRAM.read_text(encoding="utf-8")
        self.assertIn('Архитектура связки Hermes и Anytype', svg)
        self.assertIn('ЧЕЛОВЕК', svg)
        self.assertIn('ANYTYPE SPACE', svg)
        self.assertIn('HERMES', svg)

    def test_article_is_linked_from_blog_sitemap_and_llms(self):
        blog = (ROOT / "articles" / "index.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        route = "https://nasuta.ru/articles/ai-agent-knowledge-storage/"

        self.assertIn('href="ai-agent-knowledge-storage/index.html"', blog)
        self.assertIn(route, sitemap)
        self.assertIn(route, llms)


if __name__ == "__main__":
    unittest.main()
