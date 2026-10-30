from pathlib import Path
import json
import unittest

from PIL import Image

from tools.build_skills import load_registry, public_items


ROOT = Path(__file__).resolve().parents[1]
SLUG = "yandex-metrica-analytics-full"
PAGE = ROOT / "skills" / SLUG / "index.html"
IMAGE = ROOT / "assets" / "images" / "og-skill-yandex-metrica-analytics-full.jpg"
REPO = "https://github.com/pavelnasuta/yandex-metrica-analytics-full-skill"


class YandexMetricaAnalyticsPageTests(unittest.TestCase):
    def test_registry_and_page_are_a_released_public_skill(self):
        record = next(item for item in public_items(load_registry(ROOT / "data/skills.json")) if item["slug"] == SLUG)
        self.assertEqual(record["status"], "released")
        self.assertEqual(record["visibility"], "public")
        self.assertEqual(record["repository_url"], REPO)
        self.assertEqual(record["page_url"], "skills/yandex-metrica-analytics-full/index.html")
        self.assertTrue(PAGE.is_file())

    def test_page_explains_scope_install_and_data_boundaries(self):
        html = PAGE.read_text(encoding="utf-8")
        for text in ("metrika:read", "CAC, ROAS и ROI", "Вебмастера", REPO, "og-skill-yandex-metrica-analytics-full.jpg"):
            self.assertIn(text, html)
        self.assertNotIn("YANDEX_METRICA_TOKEN", html)
        self.assertNotIn("/root/", html)
        self.assertIn('href="/skills/"', html)
        self.assertIn('skills-metrica-details.css?v=2', html)

    def test_examples_are_explicitly_synthetic_and_have_three_visual_and_text_cards(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn('id="examples"', html)
        self.assertIn("синтетические примеры", html)
        self.assertIn("вымышлены", html)
        self.assertEqual(html.count('class="report-carousel__slide report-visual"'), 3)
        self.assertEqual(html.count('class="report-carousel__slide text-report"'), 3)
        self.assertIn('metrica-report-examples.js', html)
        self.assertNotIn("Воронка показывает", html)
        for image_name in ("metrica-demo-traffic.jpg", "metrica-demo-funnel.jpg", "metrica-demo-sources.jpg"):
            image_path = ROOT / "assets" / "images" / image_name
            self.assertTrue(image_path.is_file())
            with Image.open(image_path) as image:
                self.assertEqual(image.size, (1080, 1920))
                self.assertEqual(image.format, "JPEG")

    def test_role_section_sells_the_skill_without_expanding_its_data_claims(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn('id="roles"', html)
        self.assertEqual(html.count('class="role-card"'), 5)
        for role in ("ВЕБ-АНАЛИТИКУ", "SEO-СПЕЦИАЛИСТУ", "МАРКЕТОЛОГУ", "ТАРГЕТОЛОГУ", "МЕНЕДЖЕРУ ПРОДУКТА"):
            self.assertIn(role, html)
        self.assertNotIn("ПРОДУКТОВИКУ", html)
        self.assertIn("отдельный источник затрат", html)
        self.assertIn("агрегированными отчётами", html)
        self.assertIn('href="#roles"', html)

    def test_role_note_has_a_specific_top_gap_rule(self):
        styles = (ROOT / "assets/styles/skills-metrica-details.css").read_text(encoding="utf-8")
        self.assertIn(".content .role-cases__note{margin:28px 0 0", styles)

    def test_page_uses_a_distinct_valid_social_image(self):
        self.assertTrue(IMAGE.is_file())
        with Image.open(IMAGE) as image:
            self.assertEqual(image.size, (1200, 630))
            self.assertEqual(image.format, "JPEG")


if __name__ == "__main__":
    unittest.main()
