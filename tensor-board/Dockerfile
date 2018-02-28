FROM frolvlad/alpine-miniconda3:python3.6

MAINTAINER Ariel Lev 

# The Log directory of the trained TensorFlow models
ENV LOG_DIR /logs

RUN \
    apk add --update libstdc++ && \
    pip install tensorflow tensorboard && \
    mkdir $LOG_DIR

CMD tensorboard --logdir $LOG_DIR
