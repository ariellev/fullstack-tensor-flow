import io
import logging
import traceback
import os
import env
from flask import request
from flask_restplus import Resource
import mnist_client as mnist_client
from werkzeug.datastructures import FileStorage
from tf.api.api import api, host_port

# DEFAULTS
limit = os.getenv('MNIST_LIMIT', env.MNIST_LIMIT)

log = logging.getLogger(__name__)

# MNIST Namespace
ns = api.namespace('mnist', description='MNIST models')

# Flask-RestPlus specific parser for image uploading
UPLOAD_KEY = 'image'
UPLOAD_LOCATION = 'files'
upload_parser = api.parser()
upload_parser.add_argument(UPLOAD_KEY,
                           location=UPLOAD_LOCATION,
                           type=FileStorage,
                           required=True)


@ns.route('/<string:model>')
@ns.doc(params={'model': 'TensorFlow Model Name'},
        responses={
            200: 'Success',
            400: 'Serving Error',
            404: 'Not Found',
            500: "Internal server error"
            })
class MNIST(Resource):
    @ns.response(200, 'Success')
    @ns.expect(upload_parser)
    def post(self, model):
        try:
            image_file = request.files[UPLOAD_KEY]
            image = io.BytesIO(image_file.read())
        except Exception as inst:
            traceback.print_exc()
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400

        try:
            print("host_port=" + host_port)
            results = mnist_client.classify(host_port, model, image.read())
            results_json = [{'digit': res[0], 'probability': res[1]} for res in results[0:limit]]
            return {'classification_result': results_json}, 200
        except Exception as inst:
            traceback.print_exc()
            return {'message': 'internal error: {}'.format(inst)}, 500
