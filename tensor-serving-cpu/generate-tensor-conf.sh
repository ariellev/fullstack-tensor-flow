#!/bin/bash

tf_serving_dir=/serving
tf_conf=/tensorflow-serving-model.conf

tf_models=$(ls $tf_serving_dir)

echo "model_config_list: {" > $tf_conf

for m in $tf_models; do
  echo "config: {
      name: '$m',
      base_path: '$tf_serving_dir/$m',
      model_platform: 'tensorflow'
    }," >> $tf_conf
done

echo "}" >> $tf_conf

cat $tf_conf
