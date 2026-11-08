from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / "index.html").read_text(encoding="utf-8")
ARCHIVE = (ROOT / "articles" / "index.html").read_text(encoding="utf-8")
ARTICLE_ROUTES = sorted((ROOT / "articles").glob("*/index.html"))


class BlogCoverContractTests(unittest.TestCase):
    def test_og_assets_never_render_inside_article_bodies(self):
        for route in ARTICLE_ROUTES:
            with self.subTest(route=route):
                html = route.read_text(encoding="utf-8")
                body = html.split("</head>", 1)[1]
                self.assertNotRegex(body, r"og-[a-z0-9-]+\.jpg")

    def test_home_and_archive_do_not_render_og_assets_as_thumbnails(self):
        for html in (HOME, ARCHIVE):
            body = html.split("</head>", 1)[1]
            self.assertNotRegex(body, r"og-[a-z0-9-]+\.jpg")
            self.assertNotIn("case-cover", body)
            self.assertNotIn("item-cover", body)

    def test_home_blog_features_only_three_current_articles_and_archive_link(self):
        blog = HOME.split('id="blog"', 1)[1].split('id="ai-agents"', 1)[0]
        links = re.findall(r'<a class="case[^\"]*" href="([^\"]+)"', blog)
        self.assertEqual(links, [
            "/articles/agent-in-marketing-agency/",
            "/articles/ai-agent-pilot-for-agency/",
            "/articles/ai-operating-system-marketing-agency/",
        ])
        self.assertIn('href="/articles/">Все материалы →', blog)


if __name__ == "__main__":
    unittest.main()
