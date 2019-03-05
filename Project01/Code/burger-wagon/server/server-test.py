import unittest
import os

from .server import app


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """ Tests index in other words where the server is running fine. """
        tester = app.test_client(self)
        response = tester.get('/', content_type='application/json; charset=UTF-8')
        self.assertEqual(response.status_code, 404)

    def test_database(self):
        exists = os.path.exists('burger_wagon.db')

        self.assertTrue(exists)


if __name__ == '__main__':
    unittest.main()
