from pathlib import Path
import re
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class AIAgentGuideTests(unittest.TestCase):
    def test_hub_and_guides_form_a_connected_entry_route(self):
        hub = (ROOT / 'articles' / 'ai-agents' / 'index.html').read_text(encoding='utf-8')
        home = (ROOT / 'index.html').read_text(encoding='utf-8')
        archive = (ROOT / 'articles' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('Практика AI-агентов', hub)
        self.assertIn('articles/ai-agents/index.html', home)
        self.assertIn('articles/hermes-agent-installation/index.html', home)
        for link in ('ai-agents/index.html', 'hermes-agent-installation/index.html', 'hermes-agent-telegram-vps/index.html'):
            self.assertIn(link, archive)

    def test_pillar_has_direct_service_and_funnel_links_without_public_sources(self):
        page = (ROOT / 'articles' / 'hermes-agent-installation' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('https://hermes-agent.nousresearch.com/desktop', page)
        self.assertIn('https://timeweb.cloud/', page)
        self.assertIn('https://chatgpt.com/', page)
        self.assertIn('https://plati.market/', page)
        for link in ('../how-to-choose-an-ai-task/', '../../skills/', '../../contact/'):
            self.assertIn(link, page)
        self.assertNotIn('<h2>Sources</h2>', page)
        self.assertNotIn('<h2>Источники</h2>', page)
        visible = re.sub(r'<script.*?</script>', '', page, flags=re.S)
        self.assertIsNone(re.search(r'\[\d+\]', visible))

    def test_new_covers_are_unique_jpegs_at_social_size(self):
        names = ('og-ai-agent-practice.jpg', 'og-hermes-agent-installation.jpg', 'og-hermes-agent-telegram-vps.jpg')
        images = [ROOT / 'assets' / 'images' / name for name in names]
        self.assertEqual(len({image.read_bytes() for image in images}), len(images))
        for image in images:
            with Image.open(image) as opened:
                self.assertEqual(opened.size, (1200, 630))


if __name__ == '__main__':
    unittest.main()
