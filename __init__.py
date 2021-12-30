from flask import Flask
from flask_restful_swagger_2 import Api
from flask_cors import CORS
from config import Config

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = Config.TEST_API_JSON_AS_ASCII
api = Api(app, api_version='0.0', api_spec_url='/api/swagger')
CORS(app, supports_credentials=True)


@app.route('/restful_swagger')
def show_swagger():
    return """
    <head>
    <meta http-equiv="refresh" content="0; url=http://petstore.swagger.io/?url=http://127.0.0.1:8000/api/swagger.json" />
    </head>
    """


def create_app():

    return app
