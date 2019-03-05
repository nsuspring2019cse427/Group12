from flask import Flask
from flask_restful import Api

# creates an instance of server app
app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run()
