from pathlib import Path
import re
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
            '<link rel="stylesheet" href="../assets/styles/create-med-sprint.css?v=20261020-disclosure-icons">',
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
            "Зачем нужен этот спринт",
            "Инструменты: кто за что отвечает",
            "Правило трёх статусов",
            "Сделайте только нужный ресёрч",
            "Медицинские и этические границы",
            "Финальный чек-лист",
            "Рабочая карта концепции",
            "Как работать в ChatGPT Project",
            "Полный продуктовый тезаурус",
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

    def test_bottom_contact_source_and_pdf_text_blocks_are_removed(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertNotIn('<section class="contact-section"', html)
        self.assertNotIn('>Контакты</h2>', html)
        self.assertNotIn('>Sources</h2>', html)
        self.assertNotIn('Текстовая версия PDF-раздатки', html)
        self.assertIn('href="../assets/downloads/CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.pdf"', html)

    def test_working_materials_are_embedded_at_the_relevant_sprint_steps(self):
        html = PAGE.read_text(encoding="utf-8")

        def position(text: str) -> int:
            return html.index(text)

        def material_position(title: str) -> int:
            return html.index(
                '<summary><span>Дополнительный материал</span><strong class="disclosure-title">' + title + '</strong><svg class="disclosure-icon"'
            )

        step_1 = position("Шаг 1. Создайте Project и главный чат")
        step_2 = position("Шаг 2. Не переходите к решению")
        step_3 = position("Шаг 3. Сделайте только нужный ресёрч")
        step_4 = position("Шаг 4. Сузьте первый сегмент")
        step_5 = position("Шаг 5. Зафиксируйте Карточку концепции")
        step_6 = position("Шаг 6. Сделайте простой прототип")
        step_7 = position("Шаг 7. Подготовьте защиту")

        materials = (
            ("Системный промпт для ChatGPT Project", step_1, step_2),
            ("Как работать в ChatGPT Project", step_1, step_2),
            ("Промпты для Perplexity", step_3, step_4),
            ("Полный продуктовый тезаурус", step_4, step_5),
            ("Рабочая карта концепции", step_5, step_6),
            ("Лендинг и кликабельный прототип", step_6, step_7),
            ("Визуальная философия", step_6, step_7),
            ("Питч и защита", step_7, position("5. Медицинские и этические границы")),
        )
        for title, before, after in materials:
            self.assertEqual(
                html.count(
                    '<summary><span>Дополнительный материал</span><strong class="disclosure-title">' + title + '</strong><svg class="disclosure-icon"'
                ),
                1,
            )
            self.assertLess(before, material_position(title))
            self.assertLess(material_position(title), after)

        contextual_details = re.findall(
            r'<section class="material contextual-material"[^>]*>\s*(<details[^>]*>)', html
        )
        self.assertEqual(len(contextual_details), len(materials))
        self.assertTrue(all(" open" not in details for details in contextual_details))
        self.assertEqual(html.count('class="copy"'), 25)
        self.assertEqual(html.count('class="disclosure-icon"'), len(materials))
        css = CSS.read_text(encoding="utf-8")
        self.assertIn(".disclosure-icon", css)
        self.assertIn(".material-details[open] .disclosure-icon", css)
        self.assertEqual(html.count('id="materials"'), 1)
        self.assertIn("</section>\n<hr>\n<h3>5. Медицинские и этические границы", html)


if __name__ == "__main__":
    unittest.main()
