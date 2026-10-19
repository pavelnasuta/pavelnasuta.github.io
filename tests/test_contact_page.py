from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
CONTACT = ROOT / "contact/index.html"


class ContactPageTests(unittest.TestCase):
    def test_home_footer_describes_the_current_site(self):
        html = HOME.read_text(encoding="utf-8")
        self.assertIn("Product builder · AI-агенты · автоматизация", html)
        self.assertNotIn("Локальный макет", html)
        self.assertNotIn("ещё редактируются", html)

    def test_contact_page_has_three_direct_contact_options(self):
        html = CONTACT.read_text(encoding="utf-8")
        self.assertEqual(html.count('class="contact-card"'), 3)
        self.assertIn('href="https://www.linkedin.com/in/nasuta"', html)
        self.assertIn('href="https://t.me/niimozgii"', html)
        self.assertIn('href="mailto:pavelnasuta@gmail.com"', html)
        self.assertIn("LinkedIn", html)
        self.assertIn("Telegram", html)
        self.assertIn("Email", html)
        self.assertNotIn("Новых контактов и email", html)


if __name__ == "__main__":
    unittest.main()
