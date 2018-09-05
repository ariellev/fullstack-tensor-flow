FROM tensorflow/tensorflow:latest-py3

MAINTAINER Ariel Lev

# ML User
ENV ML_USER ml

# ML User Id
ENV ML_UID 1000

# ML Group Id
ENV ML_GID 100

ARG HOME=/home/$ML_USER

# The Log directory of the trained TensorFlow models
ENV LOGS_PATH $HOME/logs

# Output directory of the trained TensorFlow models
ENV MODELS_PATH $HOME/models

# Output directory of the trained keras models
ENV KERAS_PATH $HOME/models-keras

# Checkpoint directory of the trained TensorFlow models
ENV CHECKPOINTS_PATH $HOME/checkpoints

# Path to Jupyter Notebooks
ENV NOTEBOOK_PATH $HOME/notebook/

# Path for storing intermediate data sets
ENV DATA_PATH $HOME/data/

# Create ml user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN useradd -m -g $ML_GID -u $ML_UID $ML_USER && \
    mkdir $NOTEBOOK_PATH && \
    mkdir $LOGS_PATH && \
    mkdir $MODELS_PATH && \
    mkdir $KERAS_PATH && \
    mkdir $CHECKPOINTS_PATH && \
    mkdir $DATA_PATH && \
    chown $ML_USER:$ML_GID -R $HOME && \
    chown $ML_USER:$ML_GID /run_jupyter.sh

RUN pip uninstall -y jupyter

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash && \
    apt-get install -y nodejs build-essential

# Install Python requirements
COPY requirements.txt $HOME/requirements.txt
RUN pip install -r $HOME/requirements.txt

RUN jupyter labextension install jupyterlab_bokeh

RUN mkdir $HOME/.keras/
COPY keras.json $HOME/.keras/

RUN apt-get install -y tree
CMD jupyter lab --ip=* --port=8888 --no-browser --notebook-dir=$NOTEBOOK_PATH --NotebookApp.token='' --allow-root
