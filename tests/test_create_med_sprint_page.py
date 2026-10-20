from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "create-med-sprint" / "index.html"
PDF = ROOT / "assets" / "downloads" / "CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.pdf"
CSS = ROOT / "assets" / "styles" / "create-med-sprint.css"
SCRIPT = ROOT / "assets" / "scripts" / "create-med-sprint.js"
COUNTER_ID = "27865374"


class CreateMedSprintPageTests(unittest.TestCase):
    def test_page_is_a_complete_off_main_navigation_course_guide(self):
        self.assertTrue(PAGE.is_file())
        self.assertTrue(PDF.is_file())
        self.assertTrue(CSS.is_file())
        self.assertTrue(SCRIPT.is_file())

        html = PAGE.read_text(encoding="utf-8")
        self.assertIn(
            '<link rel="stylesheet" href="../assets/styles/create-med-sprint.css?v=20261020-contacts">',
            html,
        )
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        create = (ROOT / "create" / "index.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

        self.assertIn('<link rel="canonical" href="https://nasuta.ru/create-med-sprint/">', html)
        self.assertIn('href="../assets/downloads/CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.pdf"', html)
        self.assertIn("download", html)
        self.assertIn('href="../biases/index.html"', html)
        self.assertIn('Персональный тренер для вашего агента', html)
        for contact_url in (
            "https://t.me/niimozgii",
            "https://t.me/pavelnasuta",
            "https://www.linkedin.com/in/nasuta",
            "mailto:pavelnasuta@gmail.com",
        ):
            self.assertIn(contact_url, html)

        required_guide_sections = (
            "Что вы реально получите",
            "Три инструмента — три разные роли",
            "Правило трёх статусов",
            "Сделайте быстрый, но честный ресёрч",
            "Медицинские и этические границы",
            "Финальная проверка",
            "Приложение. Библиотека промптов",
            "Рабочая карта концепции",
            "Как устроить работу в ChatGPT Project",
            "Продуктовый тезаурус CREATE MED Sprint",
        )
        for section in required_guide_sections:
            self.assertIn(section, html)

        self.assertGreaterEqual(html.count('data-copy-prompt'), 16)
        self.assertEqual(html.count("https://mc.yandex.ru/metrika/tag.js"), 1)
        self.assertEqual(html.count(f"ym({COUNTER_ID}, 'init'"), 1)
        self.assertEqual(html.count(f"https://mc.yandex.ru/watch/{COUNTER_ID}"), 1)
        self.assertNotIn("create-med-sprint", home)
        self.assertIn('href="../create-med-sprint/"', create)
        self.assertIn("https://nasuta.ru/create-med-sprint/", sitemap)

    def test_coach_card_uses_brand_icons_without_changing_channel_button_and_contacts_repeat_it(self):
        html = PAGE.read_text(encoding="utf-8")
        coach = html[html.index('class="coach-card"'):html.index('class="letters med-letters"')]

        self.assertIn(
            '<a class="button" href="https://t.me/niimozgii" target="_blank" rel="noopener">Открыть канал ↗</a>',
            coach,
        )
        for label, url in (
            ("Telegram Павла Насуты", "https://t.me/pavelnasuta"),
            ("LinkedIn Павла Насуты", "https://www.linkedin.com/in/nasuta"),
            ("Написать Павлу по email", "mailto:pavelnasuta@gmail.com"),
        ):
            self.assertIn(f'href="{url}"', coach)
            self.assertIn(f'aria-label="{label}"', coach)
        self.assertEqual(coach.count('class="coach-contact-icon"'), 3)
        self.assertGreaterEqual(coach.count("<svg"), 3)

        contacts = html[html.index('class="contact-section"'):html.index("</section>", html.index('class="contact-section"'))]
        for item in (
            "НИИ «МОЗГИ»",
            "Персональный тренер для вашего агента",
            "Павел Насута — AI-powered product builder",
            "https://t.me/niimozgii",
            "https://t.me/pavelnasuta",
            "https://www.linkedin.com/in/nasuta",
            "mailto:pavelnasuta@gmail.com",
        ):
            self.assertIn(item, contacts)


if __name__ == "__main__":
    unittest.main()
