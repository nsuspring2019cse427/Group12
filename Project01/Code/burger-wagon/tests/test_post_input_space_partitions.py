import json
import unittest

from app import create_app, db


class PostInputSpaceTestCase(unittest.TestCase):
    """ This class represents testing input space partitioning of all POST endpoints. """

    # @before fixture
    def setUp(self):
        """ Define test variables and initialize app. """

        # create app with Test Configuration instead of production or development
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # fixture/ data-points : dummy used for POST endpoints
        self.menu_item_numerical = json.dumps({
            "title": "57983479",
            "description": "pet kharap hobe na 50%",
            "price": 1200.00
        })

        self.menu_item_empty_title = json.dumps({
            "title": " ",
            "description": "pet kharap hobe na 50%",
            "price": "Twenty bucks!"
        })

        self.menu_item_price_zero = json.dumps({
            "title": "Just a burger",
            "description": "pet kharap hobe na 50%",
            "price": 0
        })

        self.menu_item_price_negative = json.dumps({
            "title": "Just a burger",
            "description": "pet kharap hobe na 50%",
            "price": -10.1
        })

        self.menu_item_price_string = json.dumps({
            "title": "Just a burger",
            "description": "pet kharap hobe na 50%",
            "price": "APPLE"
        })

        self.menu_item_int_description = json.dumps({
            "title": "Apple burger",
            "description": 1235,
            "price": 25
        })

        # binds the app to the current context
        with self.app.app_context():
            # create all tables of database
            db.create_all()

    def test_menu_item_creation_should_not_accept_empty_title(self):
        """ - Test API should not create a menu item with empty title (POST request).

        GRAPH PARTITIONING: corresponding graph can be found here-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg

        cover edges: {1,2},{2,4},{4,5}
        test path: [1,2,4,5]
        """

        res = self.client().post('/menu', data=self.menu_item_empty_title, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('invalid input: title cannot be empty', str(res.data))

    def test_menu_item_creation_should_not_accept_numerical_title(self):
        """ - Test API should not create a menu item with numerical title value (POST request).

        GRAPH PARTITIONING: corresponding graph can be found here-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg

        cover edges: {1,2},{2,4},{4,6},{6,7}
        test path: [1,2,4,6,7]
        """

        res = self.client().post('/menu', data=self.menu_item_numerical, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('food title can only be alphabets', str(res.data))

    def test_menu_item_creation_should_not_accept_less_than_1_price(self):
        """ - Test API should not create a menu item with a price less than 1.00 (POST request).

        GRAPH PARTITIONING: corresponding graph can be found here-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg

        cover edges: {1,2},{2,4},{4,6},{6,8},{8,9},{9,10}
        test path: [1,2,4,6,8,9,10]
        """

        res = self.client().post('/menu', data=self.menu_item_price_zero, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('price has to be a valid positive number', str(res.data))

    def test_menu_item_creation_should_not_accept_less_than_string_price(self):
        """ - Test API cannot create a menu item with a price that is not a valid number (PUT request).

        GRAPH PARTITIONING: corresponding graph can be found here-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg

        cover edges: {1,2},{2,4},{4,6},{6,8},{8,9},{9,10}
        test path: [1,2,4,6,8,9,10]
        """

        res = self.client().post('/menu', data=self.menu_item_price_string, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('price has to be a valid positive number', str(res.data))

    def test_menu_item_creation_should_not_accept_invalid_description(self):
        """ - Test API cannot create a menu item with number description instead of valid text (PUT request).

        GRAPH PARTITIONING: corresponding graph can be found here-
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg

        cover edges: {1,2},{2,4},{4,6},{6,8},{8,9},{9,11},{11,12},{12,13}.
        test path: [1,2,4,6,8,9,11,12,13]

        """

        res = self.client().post('/menu', data=self.menu_item_int_description, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('description has to be a valid text content', str(res.data))

    # @after
    def tearDown(self):
        """ Tear down all initialized variables and database. """

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
