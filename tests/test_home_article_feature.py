from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / 'index.html').read_text(encoding='utf-8')

class HomeArticleFeatureTests(unittest.TestCase):
    def test_home_blog_features_the_three_current_articles_only(self):
        blog = HOME.split('id="blog"', 1)[1].split('id="ai-agents"', 1)[0]
        links = [
            '/articles/agent-in-marketing-agency/',
            '/articles/ai-agent-pilot-for-agency/',
            '/articles/ai-operating-system-marketing-agency/',
        ]
        positions = [blog.index(link) for link in links]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('/articles/ai-agent-knowledge-storage/', blog)

    def test_existing_articles_share_the_current_editorial_style(self):
        stylesheet = '../../assets/styles/articles-editorial.css'
        for slug in ['how-to-choose-an-ai-task', 'how-to-verify-ai-automation']:
            html = (ROOT / 'articles' / slug / 'index.html').read_text(encoding='utf-8')
            self.assertIn(stylesheet, html)
        self.assertTrue((ROOT / 'assets/styles/articles-editorial.css').is_file())

if __name__ == '__main__':
    unittest.main()
