from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
LANDING = (ROOT / "index.html").read_text(encoding="utf-8")
STYLES = (ROOT / "assets/styles/home.css").read_text(encoding="utf-8")


class ProductIconsTest(unittest.TestCase):
    def test_product_names_include_their_compact_app_icons(self):
        self.assertIn(
            '<img class="product-title__icon" src="assets/images/menhausen-app-icon.png" alt="" />',
            LANDING,
        )
        self.assertIn(
            '<img class="product-title__icon" src="assets/images/pomokitty-app-icon.png" alt="" />',
            LANDING,
        )
        self.assertIn('<span>Menhausen</span>', LANDING)
        self.assertIn('<span>pomokitty</span>', LANDING)

    def test_compact_icons_do_not_reflow_product_card_dimensions(self):
        self.assertIn('.product-title{display:flex;align-items:center;gap:10px}', STYLES)
        self.assertIn('.product-title__icon{width:19px;height:19px;flex:0 0 19px;border-radius:6px', STYLES)


if __name__ == "__main__":
    unittest.main()
