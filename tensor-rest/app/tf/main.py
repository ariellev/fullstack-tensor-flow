#!/usr/bin/env python2.7
from flask import Flask, Blueprint
from flask_restplus import Api
import os
import env
import logging.config
from .api.mnist.endpoints import ns as mnist_ns

# from api.api import api
from werkzeug.contrib.fixers import ProxyFix

logging.getLogger('flask_cors').level = logging.DEBUG
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
# app.config['SERVER_NAME'] = "localhost:9090"

api = Api(version='1.0',
          title='TensorFlow Serving REST Api',
          description='RESTful API wrapper for TensorFlow Serving')

blueprint = Blueprint('tf', __name__, url_prefix='/tf')
api.init_app(blueprint)
api.add_namespace(mnist_ns)
app.register_blueprint(blueprint)

# to enable CORS see https://pypi.python.org/pypi/Flask-Cors
# CORS(app)


def __get_flask_server_params__():
    '''
    Returns connection parameters of the Flask application

    :return: Tripple of server name, server port and debug settings
    '''
    server_host = os.getenv('FLASK_SERVER_HOST', env.FLASK_SERVER_HOST)
    server_port = os.getenv('FLASK_SERVER_PORT', env.FLASK_SERVER_PORT)

    flask_debug = os.getenv('FLASK_DEBUG', env.FLASK_DEBUG)
    flask_debug = True if flask_debug == '1' else False

    return server_host, server_port, flask_debug


def configure_app(flask_app, server_host, server_port):
    '''
    Configure Flask application

    :param flask_app: instance of Flask() class
    '''
    flask_app.config['SERVER_NAME'] = server_host + ':' + server_port
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = env.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = env.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = env.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = env.RESTPLUS_ERROR_404_HELP


def main():
    server_host, server_port, flask_debug = __get_flask_server_params__()
    configure_app(app, server_host, server_port)
    println('>>>>> Starting TF Serving API at http://{}:{}/ [debug={}]>>>>>'.format(server_host, server_port, flask_debug))
    app.run(debug=flask_debug, host=server_host, port=int(server_port))


if __name__ == '__main__':
    main()
