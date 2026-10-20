from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "create-med-sprint" / "index.html"
PDF = ROOT / "assets" / "downloads" / "CREATE_MED_SPRINT_ГИД_ДЛЯ_СТУДЕНТОВ.pdf"
CSS = ROOT / "assets" / "styles" / "create-med-sprint.css"
SCRIPT = ROOT / "assets" / "scripts" / "create-med-sprint.js"
OG_IMAGE = ROOT / "assets" / "images" / "og-create-med-sprint.jpg"
COUNTER_ID = "27865374"


class CreateMedSprintPageTests(unittest.TestCase):
    def test_page_is_a_complete_off_main_navigation_course_guide(self):
        self.assertTrue(PAGE.is_file())
        self.assertTrue(PDF.is_file())
        self.assertTrue(CSS.is_file())
        self.assertTrue(SCRIPT.is_file())

        html = PAGE.read_text(encoding="utf-8")
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

    def test_contact_blocks_use_brand_icons_and_the_page_has_a_dedicated_og_image(self):
        html = PAGE.read_text(encoding="utf-8")
        self.assertTrue(OG_IMAGE.is_file())
        self.assertIn("https://nasuta.ru/assets/images/og-create-med-sprint.jpg", html)
        self.assertIn('<meta property="og:image:width" content="1200">', html)
        self.assertIn('<meta property="og:image:height" content="630">', html)
        self.assertIn('<meta property="og:image:alt" content="CREATE MED Sprint — практический гид для студентов">', html)
        self.assertIn('<meta name="twitter:image:alt" content="CREATE MED Sprint — практический гид для студентов">', html)

        coach = html[html.index('class="coach-card"'):html.index('class="letters med-letters"')]
        for label in (
            "Telegram-канал НИИ «МОЗГИ»",
            "Telegram Павла Насуты",
            "LinkedIn Павла Насуты",
            "Написать Павлу по email",
        ):
            self.assertIn(f'aria-label="{label}"', coach)
        self.assertEqual(coach.count("coach-contact-icon"), 4)
        self.assertGreaterEqual(coach.count("<svg"), 4)

        contacts = html[html.index('id="contact"'):html.index("</section>", html.index('id="contact"'))]
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


    def test_guide_is_scannable_with_toc_collapsed_prompts_and_no_data_tables(self):
        html = PAGE.read_text(encoding="utf-8")

        self.assertIn('<nav class="toc" aria-label="Оглавление CREATE MED Sprint">', html)
        for step in range(8):
            self.assertIn(f'href="#step-{step}"', html)
            self.assertIn(f'id="step-{step}"', html)
        self.assertNotIn("<table", html)
        self.assertGreaterEqual(html.count('class="fact-grid"'), 3)
        self.assertEqual(html.count('class="prompt-details"'), html.count("data-copy-prompt"))
        self.assertNotIn('class="prompt-block"><button', html)

        first_prompt = html.index('class="prompt-details"')
        first_prompt_end = html.index("</details>", first_prompt)
        self.assertNotIn("Открыть", html[first_prompt:first_prompt_end])
        self.assertNotIn("Свернуть", html[first_prompt:first_prompt_end])

        step_7 = html.index('id="step-7"')
        step_7_end = html.index("</section>", step_7)
        medical_boundaries = html.index("5. Медицинские и этические границы")
        self.assertGreater(medical_boundaries, step_7_end)

    def test_prompts_are_embedded_in_the_sprint_flow_without_reference_markers(self):
        html = PAGE.read_text(encoding="utf-8")

        self.assertNotIn('class="quick-links"', html)
        self.assertNotIn("[1]", html)
        self.assertNotIn("[2]", html)

        step_1 = html.index("Шаг 1. Создайте Project и главный чат")
        step_2 = html.index("Шаг 2. Не переходите к решению")
        step_3 = html.index("Шаг 3. Сделайте только нужный ресёрч")
        step_4 = html.index("Шаг 4. Сузьте первый сегмент")
        step_5 = html.index("Шаг 5. Зафиксируйте Карточку концепции")
        step_6 = html.index("Шаг 6. Сделайте простой прототип")
        step_7 = html.index("Шаг 7. Подготовьте защиту")

        system_prompt = html.index("<h5>Системный промпт для Project в ChatGPT</h5>")
        project_workflow = html.index("<h5>Как устроить работу в ChatGPT Project</h5>")
        research_prompts = html.index("<h5>Rapid Research в Perplexity</h5>")
        concept_map = html.index("<h5>Рабочая карта концепции</h5>")
        prototype_prompts = html.index("<h5>Промпт: лендинг и кликабельный прототип</h5>")
        visual_philosophy = html.index("<h5>Визуальная философия PDF")
        pitch_prompts = html.index("<h5>Питч и защита</h5>")

        self.assertLess(step_1, system_prompt)
        self.assertLess(project_workflow, step_2)
        self.assertLess(step_3, research_prompts)
        self.assertLess(research_prompts, step_4)
        self.assertLess(step_5, concept_map)
        self.assertLess(concept_map, step_6)
        self.assertLess(step_6, prototype_prompts)
        self.assertLess(visual_philosophy, step_7)
        self.assertLess(step_7, pitch_prompts)

    def test_contextual_materials_keep_the_sprint_heading_hierarchy(self):
        html = PAGE.read_text(encoding="utf-8")
        for title in (
            "Системный промпт для Project в ChatGPT",
            "Rapid Research в Perplexity",
            "Рабочая карта концепции",
            "Промпт: лендинг и кликабельный прототип",
            "Питч и защита",
        ):
            self.assertIn(f"<h5>{title}</h5>", html)
            self.assertNotIn(f"<h2>{title}</h2>", html)


if __name__ == "__main__":
    unittest.main()
