import unittest
from BARTpho import app

class TestSearchAndSuggestion(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_search(self):
        response = self.app.get('/search?keyword=thesis_keyword')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'Results for "thesis_keyword"', response.data)

    def test_suggestion(self):
        response = self.app.get('/suggest?keyword=thesis_keyword')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()