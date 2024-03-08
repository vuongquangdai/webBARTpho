import unittest
from BARTpho import app

class TestRegistration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_existing_user_registration(self):
        response = self.app.post('/register', data=dict(
            username='existing_user',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already exists', response.data)

if __name__ == '__main__':
    unittest.main()