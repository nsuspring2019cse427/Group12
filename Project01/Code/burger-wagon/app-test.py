import os
import unittest

from app import create_app


class BasicTestCase(unittest.TestCase):
    """ Basic initial testings. """

    def test_index(self):
        """ Tests index in other words where the server is running fine. """

        tester = create_app('testing').test_client(self)
        response = tester.get('/', content_type='application/json; charset=UTF-8')
        self.assertEqual(response.status_code, 200)

    def test_database_filepath(self):
        """ Tests whether database exists. """

        exists = os.path.exists('burger_wagon.db')
        self.assertTrue(exists)


if __name__ == '__main__':
    unittest.main()
