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
        """ Api endpoints for Menu. """

        def post(self):
            data = request.get_json(force=True)

            if 'title' in data:
                new_entry = models.Menu(data['title'], data['price'])
            else:
                return {'message': 'both the title and price of the item must be provided'}, 400

            if 'description' in data:
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

    # -----------------------       urls        -----------------------------

    api.add_resource(MenuResource, "/menu")

    return app
