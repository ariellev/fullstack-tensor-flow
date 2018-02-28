import logging

from flask_restplus import Api
import env
import os

host_port = os.getenv('TF_SERVER_HOST_PORT', env.TF_SERVER_HOST_PORT)

log = logging.getLogger(__name__)

# Create a Flask-RESTPlus API
api = Api(version='1.0',
          title='TensorFlow Serving REST Api',
          description='RESTful API wrapper for TensorFlow Serving')


# define default error handler
@api.errorhandler
def default_error_handler(error):
    '''
    Default error handler, if something unexpected occured

    :param error: Contains specific error information
    :return: Tuple of JSON object with error information and 500 status code
    '''
    message = 'Unexpected error occured: {}'.format(error.specific)
    log.exception(message)

    if not env.FLASK_DEBUG:
        return {'message': message}, 500
