from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ABOUT = ROOT / "about" / "index.html"
CSS = ROOT / "assets" / "styles" / "about-index.css"


class AboutPageTests(unittest.TestCase):
    def setUp(self):
        self.html = ABOUT.read_text(encoding="utf-8")
        self.css = CSS.read_text(encoding="utf-8")

    def test_about_page_explains_the_human_controlled_ai_workflow(self):
        self.assertIn("управляемую работу с AI-ассистентами", self.html)
        self.assertIn("Процесс → правила → AI-ассистент → проверка → накопление знания", self.html)
        self.assertIn("Hermes использую как рабочую среду", self.html)
        self.assertIn("критичные шаги под контролем человека", self.html)

    def test_about_page_has_experience_specialties_and_clear_boundary(self):
        for phrase in (
            "30%",
            "25–50%",
            "40% компании",
            "100+ пользовательских интервью",
            "8% конверсии",
            "Специализации",
            "Где моя роль заканчивается",
            "RAG",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.html)
        self.assertIn('class="evidence-grid"', self.html)
        self.assertIn('class="workflow"', self.html)
        self.assertIn('class="specialties"', self.html)
        self.assertIn('.evidence-grid{', self.css)
        self.assertIn('.workflow{', self.css)


if __name__ == "__main__":
    unittest.main()
