import unittest

from .server import app


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='application/json; charset=UTF-8')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
