import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from tools.build_biases import build, load_catalogue


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "content" / "biases" / "catalogue.json"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class BiasesQualityTests(unittest.TestCase):
    def test_build_refreshes_sitemap_without_dropping_other_site_routes(self):
        items = load_catalogue(CATALOGUE)
        published = [item for item in items if item["published"]]

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sitemap.xml").write_text(
                """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url><loc>https://nasuta.ru/about/</loc></url>
  <url><loc>https://nasuta.ru/biases/obsolete/</loc></url>
</urlset>""",
                encoding="utf-8",
            )

            build(root, items)

            urls = {
                element.text
                for element in ET.parse(root / "sitemap.xml").findall("sm:url/sm:loc", NS)
            }
            self.assertIn("https://nasuta.ru/about/", urls)
            self.assertIn("https://nasuta.ru/biases/", urls)
            self.assertNotIn("https://nasuta.ru/biases/obsolete/", urls)
            self.assertEqual(
                {
                    url
                    for url in urls
                    if url.startswith("https://nasuta.ru/biases/") and url != "https://nasuta.ru/biases/"
                },
                {f"https://nasuta.ru/biases/{item['slug']}/" for item in published},
            )

    def test_rendered_published_cards_have_cta_sources_and_no_draft_copy(self):
        items = load_catalogue(CATALOGUE)
        published = [item for item in items if item["published"]]

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build(root, items)
            for item in published:
                with self.subTest(slug=item["slug"]):
                    html = (root / "biases" / item["slug"] / "index.html").read_text(encoding="utf-8").lower()
                    self.assertIn("персональный тренер для вашего агента", html)
                    self.assertIn("https://t.me/niimozgii", html)
                    self.assertIn("https://t.me/pavelnasuta", html)
                    self.assertIn("https://www.linkedin.com/in/nasuta", html)
                    self.assertIn("mailto:pavelnasuta@gmail.com", html)
                    self.assertIn("https://mc.yandex.ru/metrika/tag.js", html)
                    self.assertIn('class="source-list"', html)
                    self.assertNotRegex(html, r"чернов|в разработке|в сборке|добавим|placeholder")


if __name__ == "__main__":
    unittest.main()
