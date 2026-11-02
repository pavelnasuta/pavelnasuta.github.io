from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SLUG = "ai-maturity-in-company"
ROUTE = f"https://nasuta.ru/articles/{SLUG}/"
PAGE = ROOT / "articles" / SLUG / "index.html"


class AIMaturityArticleTests(unittest.TestCase):
    def test_article_has_required_seo_editorial_contract_without_visible_sources(self):
        self.assertTrue(PAGE.is_file())
        html = PAGE.read_text(encoding="utf-8")

        self.assertIn('<link rel="canonical" href="https://nasuta.ru/articles/ai-maturity-in-company/">', html)
        self.assertIn('name="description"', html)
        self.assertIn('property="og:type" content="article"', html)
        self.assertIn('name="twitter:card" content="summary_large_image"', html)
        self.assertIn('"@type":"BlogPosting"', html)
        self.assertIn('"datePublished":"2026-11-02"', html)
        self.assertIn('"dateModified":"2026-11-02"', html)
        self.assertIn('Почему компанию нельзя «сделать AI-native» одним внедрением', html)
        self.assertIn('Это не сертификация и не попытка поставить компании оценку.', html)
        self.assertNotIn('<section class="sources">', html)
        self.assertNotIn('id="source-', html)
        self.assertNotIn('<sup><a href="#source-', html)
        self.assertNotIn('From adoption to impact: Three horizons of AI transformation', html)
        self.assertNotIn('Superagency in the workplace', html)
        self.assertNotIn('https://mckinsey.com', html.lower())
        self.assertEqual(html.count("https://mc.yandex.ru/metrika/tag.js"), 1)
        self.assertEqual(html.count("ym(27865374, 'init'"), 1)
        self.assertIn('../../assets/styles/articles-editorial.css', html)

    def test_article_is_first_on_home_blog_and_articles_index(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        blog = (ROOT / "articles" / "index.html").read_text(encoding="utf-8")
        home_route = "/articles/ai-maturity-in-company/"
        blog_route = 'href="ai-maturity-in-company/index.html"'

        self.assertIn(home_route, home)
        self.assertIn(blog_route, blog)
        self.assertLess(home.index(home_route), home.index('/articles/ai-agent-knowledge-storage/'))
        self.assertLess(blog.index(blog_route), blog.index('href="ai-agents/index.html"'))

    def test_article_is_listed_in_sitemap_and_llms(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")

        self.assertIn(ROUTE, sitemap)
        self.assertIn(ROUTE, llms)


if __name__ == "__main__":
    unittest.main()
