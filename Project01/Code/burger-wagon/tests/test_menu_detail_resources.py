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

    def test_api_can_get_menu_item_by_id(self):
        """ - Test API can get a single item by using it's id. """

        """ GRAPH PARTITIONING: corresponding graph:
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/get%20function%20by%20id%20graph.jpg

        covers edges: {1,2}
        test path: [1,2]
        """

        res = self.client().post('/menu', data=self.menu_item2, content_type='application/json')
        self.assertEqual(res.status_code, 201)

        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(f'/menu/{format(result_in_json["id"])}')

        self.assertEqual(result.status_code, 200)
        self.assertIn('Naga burger', str(result.data))

    def test_api_can_not_get_menu_item_by_id(self):
        """ - Test API can not get a single item list by using it's id."""

        """ GRAPH PARTITIONING: corresponding graph:
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/get%20function%20by%20id%20graph.jpg

        covers edges: {1,3}
        test path: [1,3]
        """

        res = self.client().post('/menu', data=self.menu_item2, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res1 = self.client().delete('/menu/1')
        self.assertEqual(res1.status_code, 204)
        result = self.client().get(f'/menu/{format(result_in_json["id"])}')
        self.assertEqual(result.status_code, 404)

    def test_menu_item_can_be_edited_not_found(self):
        """ - Test API cannot edit an existing menu item which cannot be found. (PUT request).

        GRAPH PARTITIONING: corresponding graph can be found here
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/put%20method%20graph.jpg

        covers edges: {1,2},{2,3}
        test path: [1,2,3]
        """

        res = self.client().put('/menu/0', data=json.dumps(
            {"title": "Molten Cheese Burger", "description": "Tasty!", "price": 123.0}))

        self.assertEqual(res.status_code, 404)
        self.assertIn('item not found', str(res.data))

    def test_menu_item_can_be_edited(self):
        """ - Test API can edit an existing menu item. (PUT request).

        GRAPH PARTITIONING: corresponding graph can be found here
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/put%20method%20graph.jpg

        covers edges: {1,2},{2,4},{4,6},{6,8},{8,9},{9,11},{11,12},{12,13}
        test path: [1,2,,4,6,8,9,11,12,13]
        """

        res = self.client().post('/menu', data=self.menu_item2)
        self.assertEqual(res.status_code, 201)

        res = self.client().put('/menu/1', data=json.dumps(
            {"title": "Molten Cheese Burger", "description": "Tasty!", "price": 123.0}))
        self.assertEqual(res.status_code, 200)

        results = self.client().get('/menu/1')
        self.assertIn('Molten', str(results.data))

    def test_menu_item_cannot_be_edited_with_empty_title(self):
        """ - Test API cannot edit an existing menu item with an empty string title. (PUT request).

        GRAPH PARTITIONING: corresponding graph can be found here
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/put%20method%20graph.jpg

        covers edges: {1,2},{2,4},{4,5}
        test path: [1,2,,4,5]
        """

        res = self.client().post('/menu', data=self.menu_item2)
        self.assertEqual(res.status_code, 201)

        res = self.client().put('/menu/1', data=json.dumps(
            {"title": " ", "description": "Tasty!", "price": 123.0}))
        self.assertEqual(res.status_code, 400)
        self.assertIn('invalid input: title cannot be empty', str(res.data))

    def test_menu_item_deletion_not_found(self):
        """ - Test API can delete an existing menu item. (DELETE request). """

        """ GRAPH PARTITIONING: corresponding graph:
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/delete%20method%20graph.jpg
        
        covers edges: {1,3}
        test path: [1,3]
        """

        json_data = json.dumps({'title': 'Regular burger', 'price': 23})
        res = self.client().post('/menu', data=json_data, content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/menu/44')
        self.assertEqual(res.status_code, 404)

    def test_menu_item_deletion(self):
        """ - Test API can delete an existing menu item. (DELETE request). """

        """ GRAPH PARTITIONING: corresponding graph:
        https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/delete%20method%20graph.jpg
         
        covers edges: {1,2}
        test path: [1,2]
        """

        json_data = json.dumps({'title': 'Regular burger', 'price': 23})
        res = self.client().post('/menu', data=json_data, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/menu/1')
        self.assertEqual(res.status_code, 204)
        # Test to see if it exists, should return a 404
        result = self.client().get('/menu/1')
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
