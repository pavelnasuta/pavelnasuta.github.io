from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / 'index.html').read_text(encoding='utf-8')

class HomeArticleFeatureTests(unittest.TestCase):
    def test_new_article_is_first_in_home_blog_and_all_articles_remain(self):
        links = [
            'articles/ai-agent-knowledge-storage/index.html',
            'articles/how-to-choose-an-ai-task/index.html',
            'articles/how-to-verify-ai-automation/index.html',
        ]
        positions = [HOME.index(link) for link in links]
        self.assertEqual(positions, sorted(positions))

    def test_existing_articles_share_the_current_editorial_style(self):
        stylesheet = '../../assets/styles/articles-editorial.css'
        for slug in ['how-to-choose-an-ai-task', 'how-to-verify-ai-automation']:
            html = (ROOT / 'articles' / slug / 'index.html').read_text(encoding='utf-8')
            self.assertIn(stylesheet, html)
        self.assertTrue((ROOT / 'assets/styles/articles-editorial.css').is_file())

if __name__ == '__main__':
    unittest.main()
