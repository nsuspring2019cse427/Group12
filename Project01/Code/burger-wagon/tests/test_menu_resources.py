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
        """ - Ensure database is blank. """

        res = self.client().get('/menu')
        self.assertIn('', str(res.data))
        self.assertEqual(res.status_code, 404)

    def test_menu_item_creation_without_title_value(self):
        """ - Test API cannot create a menu item without title value (POST request).

        GRAPH PARTITIONING: corresponding graph can be found here-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg
                    
        cover edges: {1,3}
        test path: [1,3]
        """

        res = self.client().post('/menu', data=json.dumps({"price": 120}), content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('both the title and price of the item must be provided', str(res.data))

    def test_menu_item_creation_without_price_value(self):
        """ - Test API cannot create a menu item without price value (POST request).

        GRAPH PARTITIONING: corresponding graph can be found here-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg

        cover edges:{1,3}
        test path: [1,3]
        """

        res = self.client().post('/menu', data=json.dumps({"title": "Burger"}), content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('both the title and price of the item must be provided', str(res.data))

    def test_menu_item_creation(self):
        """ - Test API can create a menu item (POST request).

        GRAPH PARTITIONING: corresponding graph can be found here-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg
                    
        cover edges: {1,2},{2,4},{4,6},{6,8},{8,9},{9,11},{11,12},{12,14},{14,15}.
        test path: [1,2,4,6,8,9,11,12,14,15]
        """

        res = self.client().post('/menu', data=self.menu_item, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('Exotic expired cheese burger', str(res.data))

    def test_api_can_get_menu_list(self):
        """  - Test API can get a bucketlist (GET request)."""

        """ GRAPH PARTITIONING: corresponding graph-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/get%20function%20for%20getting%20bucketlist%20graph.jpg
                                             
        cover edges:{1,2}
        test path: [1,2]
        """

        res = self.client().post('/menu', data=self.menu_item, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/menu', data=self.menu_item2, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/menu')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Exotic expired cheese burger', str(res.data))
        self.assertIn('Naga burger', str(res.data))

    def test_api_can_not_get_menu_list(self):
        """ - Test API can not get a bucketlist (GET request)."""

        """ GRAPH PARTITIONING: corresponding graph-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/get%20function%20for%20getting%20bucketlist%20graph.jpg
        
        cover edges:{1,3}
        test path: [1,3]
        """

        res = self.client().post('/menu', data=self.menu_item, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/menu', data=self.menu_item2, content_type='application/json')
        self.assertEqual(res.status_code, 201)
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
