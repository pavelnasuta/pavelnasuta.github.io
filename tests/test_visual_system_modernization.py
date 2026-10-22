from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ABOUT = ROOT / "about" / "index.html"
CONTACT = ROOT / "contact" / "index.html"
NOT_FOUND = ROOT / "404.html"
BIASES_CSS = ROOT / "assets" / "styles" / "biases.css"
ABOUT_CSS = ROOT / "assets" / "styles" / "about-index.css"
CONTACT_CSS = ROOT / "assets" / "styles" / "contact-index.css"


class EditorialVisualSystemTests(unittest.TestCase):
    def test_secondary_pages_use_editorial_shared_tokens(self):
        for stylesheet in (ABOUT_CSS, CONTACT_CSS, BIASES_CSS):
            with self.subTest(stylesheet=stylesheet.name):
                css = stylesheet.read_text(encoding="utf-8")
                self.assertIn("--paper:#f4f7f3", css)
                self.assertIn("--ink:#102e3d", css)
                self.assertIn("--teal:#08716e", css)
                self.assertIn("@media(max-width", css)

    def test_about_and_contact_keep_external_content_but_use_stylesheets(self):
        about = ABOUT.read_text(encoding="utf-8")
        contact = CONTACT.read_text(encoding="utf-8")
        self.assertIn('href="../assets/styles/about-index.css"', about)
        self.assertIn('href="../assets/styles/contact-index.css"', contact)
        self.assertNotIn("<style>", contact)
        self.assertIn('href="https://www.linkedin.com/in/nasuta"', contact)
        self.assertIn('href="https://t.me/niimozgii"', contact)
        self.assertIn('href="mailto:pavelnasuta@gmail.com"', contact)

    def test_404_uses_dedicated_editorial_stylesheet_and_keeps_recovery_links(self):
        html = NOT_FOUND.read_text(encoding="utf-8")
        self.assertIn('href="/assets/styles/not-found.css"', html)
        self.assertNotIn("<style>", html)
        css = (ROOT / "assets" / "styles" / "not-found.css").read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn('href="/"', html)
        self.assertIn('href="/articles/index.html"', html)

    def test_biases_detail_template_uses_the_shared_catalogue_stylesheet(self):
        source = (ROOT / "tools" / "build_biases.py").read_text(encoding="utf-8")
        self.assertIn('href="../../assets/styles/biases.css"', source)
        self.assertIn('href="../assets/styles/biases.css"', source)


if __name__ == "__main__":
    unittest.main()
