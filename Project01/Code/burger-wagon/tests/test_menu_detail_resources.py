import json
import unittest

from app import create_app, db


class MenuDetailsResourceTestCase(unittest.TestCase):
    """ This class represents the MenuResource test case. """

    # @before fixture
    def setUp(self):
        """Define test variables and initialize app."""

        # create app with Test Configuration instead of production or development
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # fixture: dummy used for POST endpoints
        self.menu_item = json.dumps({
            "title": "Triple cheese burger",
            "description": "Extremely cheesy!",
            "price": 120.00
        })
        self.menu_item2 = json.dumps({
            "title": "Naga burger",
            "description": "Extremely spicy burgers for the spice lovers!",
            "price": 125.00
        })

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_menu_item_can_be_edited_not_found(self):
        """ Test API cannot edit an existing menu item which cannot be found. (PUT request). """

        res = self.client().put('/menu/0', data=json.dumps(
            {"title": "Molten Cheese Burger", "description": "Tasty!", "price": 123.0}))

        self.assertEqual(res.status_code, 404)
        self.assertIn('item not found', str(res.data))

    def test_menu_item_can_be_edited(self):
        """ Test API can edit an existing menu item. (PUT request). """

        res = self.client().post('/menu', data=self.menu_item2)
        self.assertEqual(res.status_code, 201)

        res = self.client().put('/menu/1', data=json.dumps(
            {"title": "Molten Cheese Burger", "description": "Tasty!", "price": 123.0}))
        self.assertEqual(res.status_code, 200)

        results = self.client().get('/menu/1')
        self.assertIn('Molten', str(results.data))

    def test_menu_item_deletion_not_found(self):
        """ Test API can delete an existing menu item. (DELETE request). """

        json_data = json.dumps({'title': 'Regular burger', 'price': 23})
        res = self.client().post('/menu', data=json_data, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/menu/44')
        self.assertEqual(res.status_code, 404)


    # @after
    def tearDown(self):
        """ Tear down all initialized variables and database. """

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
