from pathlib import Path
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ROUTE = 'articles/hermes-commands/'


class HermesCommandsPageTests(unittest.TestCase):
    def test_reference_page_is_listed_in_the_blog_and_ai_agent_guides(self):
        archive = (ROOT / 'articles' / 'index.html').read_text(encoding='utf-8')
        guides = (ROOT / 'articles' / 'ai-agents' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('hermes-commands/index.html', archive)
        self.assertIn('../hermes-commands/', guides)

    def test_reference_page_has_complete_public_metadata_and_core_sections(self):
        page = (ROOT / ROUTE / 'index.html').read_text(encoding='utf-8')
        expected = (
            'Справочник команд Hermes: Telegram и консоль',
            'https://nasuta.ru/articles/hermes-commands/',
            'https://nasuta.ru/assets/images/og-hermes-commands.jpg',
            'Telegram: команды бота',
            '2. Консоль: типичные команды <code>hermes</code>',
            '<code>/new [название]</code>',
            'hermes gateway setup',
            'https://hermes-agent.nousresearch.com/docs/reference/slash-commands',
        )
        for marker in expected:
            self.assertIn(marker, page)
        self.assertIn('"@type": "BlogPosting"', page)
        self.assertIn('ym(27865374', page)
        self.assertIn('site-navigation', page)
        self.assertIn('site-footer', page)
        self.assertEqual(page.count('<h1'), 1)
        self.assertTrue(page.endswith('</a>\n</body></html>'))

    def test_reference_page_has_a_unique_social_image_and_sitemap_entry(self):
        image = ROOT / 'assets' / 'images' / 'og-hermes-commands.jpg'
        with Image.open(image) as opened:
            self.assertEqual(opened.size, (1200, 630))
        sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
        self.assertIn('https://nasuta.ru/articles/hermes-commands/', sitemap)


if __name__ == '__main__':
    unittest.main()
