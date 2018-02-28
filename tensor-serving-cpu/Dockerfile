FROM ubuntu:16.04

MAINTAINER Ariel Lev 

RUN apt-get update && apt-get install -y curl apt-utils

ENV TERM xterm

RUN echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" > \
    /etc/apt/sources.list.d/tensorflow-serving.list && \
    curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | apt-key add - && \
    apt-get update && apt-get install -y tensorflow-model-server

# TensorFlow Serving default port
ARG port=9000
EXPOSE $port

# ML User
ENV ML_USER ml

# ML User Id
ENV ML_UID 1000

# ML Group Id
ENV ML_GID 100

ADD serving /serving
RUN useradd -m -g $ML_GID -u $ML_UID $ML_USER && \
    chown $ML_USER:$ML_GID -R /serving

VOLUME /serving

ADD generate-tensor-conf.sh /usr/bin/

ADD entrypoint.sh /usr/bin/

RUN chown $ML_USER:$ML_GID /usr/bin/generate-tensor-conf.sh
RUN chown $ML_USER:$ML_GID /usr/bin/entrypoint.sh
RUN touch /tensorflow-serving-model.conf && chown $ML_USER:$ML_GID /tensorflow-serving-model.conf

USER $ML_USER

RUN generate-tensor-conf.sh

CMD ["/bin/bash"]

ENTRYPOINT "entrypoint.sh"
