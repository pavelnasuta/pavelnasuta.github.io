from pathlib import Path
import unittest


PAGE = Path(__file__).resolve().parents[1] / "404.html"


class NotFoundPageTests(unittest.TestCase):
    def test_404_page_offers_a_playful_recovery_route(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertIn('class="not-found-illustration"', html)
        self.assertIn("Кажется, этот маршрут ещё не собрали", html)
        self.assertIn('href="index.html"', html)
        self.assertIn('href="articles/how-to-choose-an-ai-task/index.html"', html)
        self.assertIn('href="articles/how-to-verify-ai-automation/index.html"', html)
        self.assertIn("prefers-reduced-motion", html)


if __name__ == "__main__":
    unittest.main()
