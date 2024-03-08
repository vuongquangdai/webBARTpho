import unittest
from BARTpho import app

class TestLogin(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_unsuccessful_login(self):
        # Test login with invalid credentials
        response = self.app.post('/login', data=dict(
            username='test_user',
            password='wrong_password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login unsuccessful', response.data)

if __name__ == '__main__':
    unittest.main()