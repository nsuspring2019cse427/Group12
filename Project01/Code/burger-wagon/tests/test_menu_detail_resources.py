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

    # @after
    def tearDown(self):
        """ Tear down all initialized variables and database. """

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
