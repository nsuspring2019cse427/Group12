from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initialize sql-alchemy before app creation
from config import app_config

db = SQLAlchemy()


def create_app(config_name):
    """ create_app creates the flask server instance with specified configuration

        :param config_name: configuration type of the flask environment
        type config_nam: str
        :return: flask app instance
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    return app
