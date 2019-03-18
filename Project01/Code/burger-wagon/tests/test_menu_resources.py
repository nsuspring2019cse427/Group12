import json
import unittest

from app import create_app, db


class MenuResourceTestCase(unittest.TestCase):
    """ This class represents the MenuResource test case. """

    # @before fixture
    def setUp(self):
        """ Define test variables and initialize app. """

        # create app with Test Configuration instead of production or development
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # fixture: dummy used for POST endpoints
        self.menu_item = json.dumps({
            "title": "Exotic expired cheese burger",
            "description": "pet kharap hobe na 50%",
            "price": 120.00
        })

        self.menu_item2 = json.dumps({
            "title": "Naga burger",
            "description": "Extremely spicy burgers for the spice lovers!",
            "price": 125.00
        })

        # binds the app to the current context
        with self.app.app_context():
            # create all tables of database
            db.create_all()

    def test_empty_database(self):
        """ Ensure database is blank. """

        res = self.client().get('/menu')
        self.assertIn('', str(res.data))
        self.assertEqual(res.status_code, 404)

    def test_menu_item_creation_without_title_value(self):
        """ Test API cannot create a menu item without title value (POST request). """

        res = self.client().post('/menu', data=json.dumps({"price": 120}), content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('both the title and price of the item must be provided', str(res.data))

    def test_menu_item_creation_without_price_value(self):
        """ Test API cannot create a menu item without price value (POST request). """

        res = self.client().post('/menu', data=json.dumps({"title": "Burger"}), content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('both the title and price of the item must be provided', str(res.data))

    def test_menu_item_creation(self):
        """ Test API can create a menu item (POST request). """

        res = self.client().post('/menu', data=self.menu_item, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('Exotic expired cheese burger', str(res.data))

    def test_api_can_get_menu_list(self):
        """ Test API can get a bucketlist (GET request)."""

        res = self.client().post('/menu', data=self.menu_item, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/menu', data=self.menu_item2, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/menu')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Exotic expired cheese burger', str(res.data))
        self.assertIn('Naga burger', str(res.data))

    # @after
    def tearDown(self):
        """ Tear down all initialized variables and database. """

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()