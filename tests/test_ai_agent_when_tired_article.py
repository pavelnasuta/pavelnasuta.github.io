from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SLUG = "ai-agent-when-tired"
ROUTE = f"https://nasuta.ru/articles/{SLUG}/"
ASSET = f"https://nasuta.ru/assets/images/og-{SLUG}.jpg"
PAGE = ROOT / "articles" / SLUG / "index.html"


class AiAgentWhenTiredArticleTests(unittest.TestCase):
    def test_article_has_private_research_and_public_editorial_contract(self):
        self.assertTrue(PAGE.is_file())
        html = PAGE.read_text(encoding="utf-8")

        self.assertIn('<link rel="canonical" href="https://nasuta.ru/articles/ai-agent-when-tired/">', html)
        self.assertIn('name="description"', html)
        self.assertIn('property="og:type" content="article"', html)
        self.assertIn(f'property="og:image" content="{ASSET}"', html)
        self.assertIn(f'name="twitter:image" content="{ASSET}"', html)
        self.assertIn('"@type":"BlogPosting"', html)
        self.assertIn('Курс запускал мой близкий друг.', html)
        self.assertNotIn('<section class="sources">', html)
        self.assertNotIn('pubmed.ncbi.nlm.nih.gov', html)
        self.assertNotIn('src="../../assets/images/og-ai-agent-when-tired.jpg"', html)

    def test_new_article_is_featured_first_with_its_cover(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        archive = (ROOT / "articles" / "index.html").read_text(encoding="utf-8")

        self.assertIn('/articles/ai-agent-when-tired/', home)
        self.assertIn('href="ai-agent-when-tired/index.html"', archive)
        self.assertIn('/assets/images/og-ai-agent-when-tired.jpg', home)
        self.assertIn('/assets/images/og-ai-agent-when-tired.jpg', archive)
        self.assertLess(home.index('/articles/ai-agent-when-tired/'), home.index('/articles/ai-maturity-in-company/'))
        self.assertLess(archive.index('href="ai-agent-when-tired/index.html"'), archive.index('href="ai-maturity-in-company/index.html"'))

    def test_article_is_discoverable_and_cover_is_a_valid_jpeg(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        asset = ROOT / "assets" / "images" / "og-ai-agent-when-tired.jpg"

        self.assertIn(ROUTE, sitemap)
        self.assertIn(ROUTE, llms)
        self.assertTrue(asset.is_file())


if __name__ == "__main__":
    unittest.main()
