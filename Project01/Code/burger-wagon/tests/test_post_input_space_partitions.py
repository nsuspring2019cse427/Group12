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

        # binds the app to the current context
        with self.app.app_context():
            # create all tables of database
            db.create_all()

    def test_menu_item_creation_should_not_accept_empty_title(self):
        """ - Test API should not create a menu item with empty title (POST request). """

        """ GRAPH PARTITIONING: corresponding graph:
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg

        cover edges: {1,2},{2,4},{4,5}
        test path: [1,2,4,5]
        """

        res = self.client().post('/menu', data=self.menu_item_numerical, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('food title can only be alphabets', str(res.data))

    def test_menu_item_creation_should_not_accept_numerical_title(self):
        """ - Test API should not create a menu item with numerical title value (POST request). """

        """ GRAPH PARTITIONING: corresponding graph:
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg

        cover edges: {1,2},{2,4},{4,6},{6,7}
        test path: [1,2,4,6,7]
        """

        res = self.client().post('/menu', data=self.menu_item_numerical, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('food title can only be alphabets', str(res.data))

    # @after
    def tearDown(self):
        """ Tear down all initialized variables and database. """

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
