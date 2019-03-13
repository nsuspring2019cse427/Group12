# encoding: utf-8

"""

Configuration of Flask for different cases.

"""

# no imports
import os


class BaseConfig(object):
    # configuration

    DEBUG = False
    TESTING = False

    SECRET_KEY = 'weneedthemarks'
    USERNAME = 'admin'
    PASSWORD = '123'

    basedir = os.path.abspath(os.path.dirname(__file__))

    DATABASE = 'burger_wagon.db'

    # define the full path for the database
    DATABASE_PATH = os.path.join(basedir, DATABASE)

    # database config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}



