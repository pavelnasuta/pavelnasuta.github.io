from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://nasuta.ru"
PAGES = sorted(page for page in ROOT.rglob("*.html") if page.name != "404.html")


class SeoCoverageTests(unittest.TestCase):
    def test_every_indexable_page_has_complete_search_and_social_metadata(self):
        self.assertGreater(len(PAGES), 0)
        for page in PAGES:
            with self.subTest(page=page.relative_to(ROOT)):
                html = page.read_text(encoding="utf-8")
                self.assertRegex(html, r'<title>[^<]+</title>')
                self.assertIn('name="description"', html)
                route = "/" if page == ROOT / "index.html" else "/" + str(page.parent.relative_to(ROOT)) + "/"
                self.assertIn(f'<link rel="canonical" href="{SITE}{route}">', html)
                for key in ("og:title", "og:description", "og:url", "og:image"):
                    self.assertIn(f'property="{key}"', html)
                for key in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
                    self.assertIn(f'name="{key}"', html)
                blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
                self.assertTrue(blocks)
                for block in blocks:
                    json.loads(block)

    def test_every_indexable_page_is_in_the_sitemap(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for page in PAGES:
            route = "/" if page == ROOT / "index.html" else "/" + str(page.parent.relative_to(ROOT)) + "/"
            self.assertIn(f"{SITE}{route}", sitemap)

    def test_readme_makes_whole_site_seo_a_content_requirement(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("seo", readme)
        self.assertIn("каждой", readme)
        self.assertIn("страницы", readme)


if __name__ == "__main__":
    unittest.main()
