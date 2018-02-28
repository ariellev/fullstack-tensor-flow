# Fullstack TensorFlow

## Build & Run

##### Localhost

Build the docker images and push them to a docker registry.
```
> export PATH="$(realpath ./bin):$PATH"
> push-all-docker.sh --group lab
```
To work with a local private registry make sure that:
1. docker is installed
2. a private docker registry is running on localhost:5000. see [here](https://docs.docker.com/registry/deploying/)
3. the private registry is marked insecured: [Mac Os ](https://stackoverflow.com/questions/32808215/where-to-set-the-insecure-registry-flag-on-mac-os) | [Linux](https://docs.docker.com/registry/insecure/)
4. `export registry=localhost:5000`

```
# start docker-compose
> compose.sh up -f docker/.deploy/localhost-compose.yml

..
compose.sh up -f docker/.deploy/localhost-compose.yml
-------------------------------------------------------
docker-compose           up
-------------------------------------------------------
compose_file     docker/.deploy/localhost-compose.yml
env_file         localhost-compose.env
project          lab
docker_ip        192.168.0.212
registry         localhost:5000
Creating tensor-serving-cpu ... done
-------------------------------------------------------
Creating tensor-rest ... done
Creating tensor-serving-cpu ...
Creating tensor-rest ...
Creating tensor-jupyter ...
--------------------------------------
service-ip 192.168.0.212
--------------------------------------
done

> docker ps

CONTAINER ID        IMAGE                                          COMMAND                   CREATED              STATUS              PORTS                              NAMES
b4e4962c1ff5        localhost:5000/lab/tensor-jupyter:latest       "/bin/sh -c '/run_ju…"    About a minute ago   Up About a minute   6006/tcp, 0.0.0.0:8888->8888/tcp   tensor-jupyter
22a74f45e1f0        localhost:5000/lab/tensor-rest:latest          "/entrypoint.sh /usr…"    About a minute ago   Up About a minute   443/tcp, 0.0.0.0:8080->80/tcp      tensor-rest
69d883c74986        localhost:5000/lab/tensor-serving-cpu:latest   "/bin/sh -c \"entrypo…"   About a minute ago   Up About a minute   0.0.0.0:9000->9000/tcp             tensor-serving-cpu
46b73f804c4f        registry:2                                     "/entrypoint.sh /etc…"    2 weeks ago          Up 30 hours         0.0.0.0:5000->5000/tcp             registry

# stop docker-compose
> compose.sh down -f .deploy/localhost-compose.yml
```
###### Resources
1. [Jupyter notebook](http://localhost:8888/)
2. [Tensor-Board](http://localhost:6006/)
3. [RESTful API](http://localhost:8080/tf/)


## Development
* Install [conda](https://conda.io/docs/user-guide/install/index.html) and a bunch of handy utilities: [csvkit](https://csvkit.readthedocs.io/en/1.0.2/)

* Create a development environment for tensor-serving:
```
# Create a Tensor-Flow conda environment
# Unfortunately tensor-serving-api is only available for python 2.7

> conda env create -y -f=docker/tensor-rest/requirements.txt -n tf2.7

# activate the environment
> source activate tf2.7
```

* Create a development environment for tensor-jupyter:
```
> ./create-conda-env.sh
```

* Setup an IDE, for example [Atom](https://atom.io/) or [PyCharm](https://www.jetbrains.com/pycharm/)
```
# Atom, see https://medium.com/@andrealmar/how-to-setup-atom-as-your-python-development-environment-a67fe8738bd3
> apm install ide-python linter-flake8 linter-pep8 autocomplete-python django-templates

# activate your development environment, for example:
> source activate tf3.6

# install packages
> pip install pep8 flake8 jedi python-language-server
```

* Install uswgi
```
> pip install uwsgi

# Run tensor-rest directly on localhost, without docker
> cd docker/tensor-rest/app
> uwsgi uwsgi.ini

# open web browser
> open http://localhost:9090/tf/

```
