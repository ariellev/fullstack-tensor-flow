#!/bin/bash
set -e

env=tf3.6
exists=$(conda info --envs | grep -c $env)

if [ "$exists" -eq "0" ]
then
  conda create -y -n $env python=3.6 anaconda
else
  echo "woohoo! conda environment=$env exists, don't have to install that one"
fi

source activate $env
pip install -r docker/tensor-jupyter/requirements.txt

echo "done."
