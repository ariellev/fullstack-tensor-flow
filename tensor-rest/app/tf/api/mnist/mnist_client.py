#!/usr/bin/env python2.7

"""A client that talks to tensorflow_model_server loaded with mnist model.
Typical usage example:
    ./mnist_client.py --server localhost:9000 --image data/mnist/mnist_0_1ly8hh9slc91y-t9.jpg
"""

from __future__ import print_function
import operator
import logging
import tensorflow as tf
from grpc.beta import implementations
import numpy as np
from scipy import misc
from PIL import Image
import cStringIO as StringIO
import env
import os
import random
import string
import io

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from tensorflow.examples.tutorials.mnist import input_data as mnist_input_data

log = logging.getLogger(__name__)
image_width = os.getenv('MNIST_WIDTH', env.MNIST_WIDTH)
image_height = os.getenv('MNIST_HEIGHT', env.MNIST_HEIGHT)


def generate_string(size=16, chars=string.ascii_lowercase + "-" + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def __create_classification_request__(model, image):
    '''
    Creates prediction request to TensorFlow server for MNIST model
    :param model: Model name
    :param: Byte array, image for prediction
    :return: PredictRequest object
    '''
    # create predict request
    request = predict_pb2.PredictRequest()
    request.model_spec.name = model
    request.model_spec.signature_name = os.getenv('MNIST_MODEL_SIGNATURE_NAME', env.MNIST_MODEL_SIGNATURE_NAME)
    key = os.getenv('MNIST_MODEL_INPUTS_KEY', env.MNIST_MODEL_INPUTS_KEY)

    stream = StringIO.StringIO(image)
    img = np.array(Image.open(stream)).astype(np.float32)

    tensor_proto = tf.contrib.util.make_tensor_proto(img, shape=[1, image_width, image_height, 1])
    request.inputs[key].CopyFrom(tensor_proto)

    return request


def classify(hostport, model, image):
    '''
    Sends Predict request over a channel stub to TensorFlow server
    :param hostport: Server host:port
    :param model: Model name
    :param image: image object
    :return: List of tuples, digits with their probabilities
    '''
    host, port = hostport.split(':')
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    request = __create_classification_request__(model, image)

    result = stub.Predict(request, 5.0)  # 5 seconds
    probs = np.array(result.outputs['scores'].float_val)
    value_dict = {idx: prob for idx, prob in enumerate(probs)}

    sorted_values = sorted(
        value_dict.items(),
        key=operator.itemgetter(1),
        reverse=True)

    return sorted_values


def __extract_mnist_to_jpegs__(destination_dir, tmp_dir="tmp", total=100):
    test = mnist_input_data.read_data_sets(tmp_dir).test
    images, labels = test.next_batch(total)

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, exist_ok=True)

    for i in range(total):
        img = images[i]
        label = labels[i]
        file_name = "%s/mnist_%s_%s.jpg" % (destination_dir, label, generate_string())
        misc.imsave(file_name, img.reshape(image_width, image_height))


def main():
    tf.app.flags.DEFINE_string('server', None, 'PredictionService host:port')
    tf.app.flags.DEFINE_string('extract', None, 'Folder for extracting MNIST as jpg')
    tf.app.flags.DEFINE_string('image', None, 'MNIST Image to classify')

    FLAGS = tf.app.flags.FLAGS

    if not FLAGS.server:
        print('--server must be specified [host:port]')
        return

    if not FLAGS.image:
        print('--image must be specified')
        return

    if FLAGS.extract:
        __extract_mnist_to_jpegs__(FLAGS.extract)

    with open(FLAGS.image, 'rb') as fin:
        image = io.BytesIO(fin.read()).read()
        result = classify(FLAGS.server, "mnist-cnn", image)
        print('Result: %s' % result)


if __name__ == "__main__":
    main()
