from flask import Flask, request
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy

# initialize sql-alchemy before app creation
db = SQLAlchemy()

from app import models
from config import app_config


def create_app(config_name):
    """ create_app creates the flask server instance with specified configuration.

        :param      config_name: configuration type of the flask environment
        :type       config_name: str
        :return:    flask app instance
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    api = Api(app, version='1.0', title='Burger Wagon', description='api endpoints')
    api.namespace(name='', description='menu of all the items available and CRUD operations')

    # ----------------------- controllers  -----------------------------

    class MenuResource(Resource):
        """ Api endpoints for Menu.
            :API endpoint: /menu
        """

        def get(self):
            """ GET: menu list.

             GRAPH PARTITIONING: corresponding graph can be found here-
             https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/get%20function%20for%20getting%20bucketlist%20graph.jpg

            """

            query_list = models.Menu.query.all()
            # if query not empty return a list of the serialized query_list
            if query_list:
                return [i.serialize for i in query_list], 200

            return '', 404

        def post(self):
            """ CREATE: menu item.

             GRAPH PARTITIONING: corresponding graph can be found here-
             https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/post%20method%20graph.jpg

            """

            # json response
            data = request.get_json(force=True)

            if 'title' in data and 'price' in data:

                title = data['title'].replace(' ', '')
                if not title:
                    return {'error': 'invalid input: title cannot be empty'}, 400
                if not title.isalpha():
                    return {'error': 'invalid input: food title can only be alphabets'}, 400

                price = data['price']
                if not is_number(price):
                    return {'error': 'price has to be a valid positive number'}, 400
                if price < 1.0:
                    return {'error': 'price has to be a valid positive number'}, 400

                new_entry = models.Menu(data['title'], data['price'])
            else:
                return {'error': 'both the title and price of the item must be provided'}, 400

            if 'description' in data:
                if is_number(data['description']):
                    return {'error': 'description has to be a valid text content'}, 400
                new_entry.description = data['description']

            new_entry.save()

            response = {
                'id': new_entry.id,
                'title': new_entry.title,
                'description': new_entry.description,
                'price': new_entry.price,
                'date_created': new_entry.date_created.isoformat()
            }

            return response, 201

    class MenuDetailsResource(Resource):
        """ Api endpoints for Menu details.
            :API endpoint: /menu/<int:menu_id>
        """

        def get(self, menu_id):
            """ GET:  menu item with given menu ID.

             GRAPH PARTITIONING: corresponding graph can be found here
             https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/get%20function%20by%20id%20graph.jpg

            """

            entries = models.Menu.query.get(menu_id)
            if entries:
                return entries.serialize, 200

            return {"error": "not found"}, 404

        def put(self, menu_id):
            """ PUT:  menu item with given menu ID. """

            data = request.get_json(force=True)

            item = models.Menu.query.get(menu_id)

            if not item:
                return {"error": "item not found"}, 404

            if 'title' in data and 'price' in data:

                title = data['title'].replace(' ', '')
                if not title:
                    return {'error': 'invalid input: title cannot be empty'}, 400
                if not title.isalpha():
                    return {'error': 'invalid input: food title can only be alphabets'}, 400

                price = data['price']
                if not is_number(price):
                    return {'error': 'price has to be a valid positive number'}, 400
                if price < 1.0:
                    return {'error': 'price has to be a valid positive number'}, 400
            else:
                return {'error': 'both the title and price of the item must be provided'}, 400

            item.title = title
            item.price = price

            if 'description' in data:
                item.description = data['description']

            item.save()

            response = {
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'price': item.price,
                'date_created': item.date_created.isoformat()
            }

            return response, 200

        def delete(self, menu_id):
            """ DELETE:  menu item with given menu ID.

             GRAPH PARTITIONING: corresponding graph can be found here-
             https://github.com/nsuspring2019cse427/Group12/blob/master/Project01/Documentation/resources/delete%20method%20graph.jpg

            """

            entries = models.Menu.query.get(menu_id)

            if entries:
                return entries.delete(), 204

            return {"error": "not found"}, 404

    # -----------------------       urls        -----------------------------

    api.add_resource(MenuResource, "/menu")
    api.add_resource(MenuDetailsResource, "/menu/<int:menu_id>")

    return app


def is_number(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False
