#/bin/bash
generate-tensor-conf.sh && tensorflow_model_server --port=9000 --model_config_file=/tensorflow-serving-model.conf
