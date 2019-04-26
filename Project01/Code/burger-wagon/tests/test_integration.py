import json
import unittest

from app import create_app, db


class IntegrationTestCase(unittest.TestCase):

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

    def test_api_integration(self):

        """tests all api functions get,put,post and delete at once"""

        res = self.client().post('/menu', data=self.menu_item, content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client().post('/menu', data=self.menu_item2, content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client().put('/menu/1', data=json.dumps(
            {"title": "Molten Cheese Burger", "description": "Tasty!", "price": 123.0}))
        self.assertEqual(res.status_code, 200)

        res = self.client().put('/menu/2', data=json.dumps(
            {"title": "double cheese burger", "description": "Deadly!", "price": 255.0}))
        self.assertEqual(res.status_code, 200)

        res1 = self.client().delete('/menu/1')
        self.assertEqual(res1.status_code, 204)

        res2 = self.client().delete('/menu/2')
        self.assertEqual(res2.status_code, 204)

        result = self.client().get('/menu')
        self.assertEqual(result.status_code, 404)

    # @after
    def tearDown(self):
        """ Tear down all initialized variables and database. """

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
