from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "assets/styles/home.css").read_text(encoding="utf-8")


class HomepageBiasesPromoTests(unittest.TestCase):
    def test_homepage_has_full_width_biases_promo_in_the_correct_position(self):
        self.assertIn('class="biases"', HOME)
        self.assertIn('href="/biases/"', HOME)
        self.assertIn('Когнитивные искажения — 180+ ловушек мышления', HOME)
        self.assertIn('принимать решения точнее.', HOME)
        self.assertNotIn('Раздел о мышлении', HOME)
        self.assertNotIn('180+ когнитивных искажений', HOME)
        self.assertLess(HOME.index('class="content-section skills"'), HOME.index('class="biases"'))
        self.assertLess(HOME.index('class="biases"'), HOME.index('class="telegram"'))
        self.assertRegex(CSS, r'\.biases\{[^}]*margin:0 -42px')


if __name__ == "__main__":
    unittest.main()
