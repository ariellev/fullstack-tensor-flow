Fullstack TensorFlow
====================

![alt Fullstack TensorFlow](https://raw.githubusercontent.com/ariellev/fullstack-tensor-flow/master/images/winery.jpg)

## Table of Contents
1. [Introduction](#introduction)
2. [Get started](#get-started)
3. [Run the TensorFlow stack](#run-the-tensorFlow-stack)
4. [Tweak and re-deploy](#tweak-and-re-deploy)
5. [Under the Hood](#under-the-hood)
6. [Beyond localhost](#beyond-localhost)

## Introduction
Among the excellent tutorials, blogs and many other online resources out there in the web, cleverly demonstrating how to train a neural network with less than 2 lines of code, it seems to be only a few, which can guide one through sometimes a quite challenging trial, of turning a sour neural liquid into an enjoyable, delightful, winy, production-ready service - a task which might become even more trickier, especially when deploying an application to a complex productive environment.

This blog post is there to help you navigating your way in this *DevOps* jungle. It won't take you all the way to the promise land, yet it would show you a path to follow, one that you can later extend, improve and finalize to fit your specific requirements. The content of this blog was not just born out of nowhere, instead it adds to the terrific work of [*Vitaly Bezgachev*](https://becominghuman.ai/creating-restful-api-to-tensorflow-models-c5c57b692c10) and other contributors from the community.

The overall structure is going to be pretty much straight forward. We'll start with a basic setup, run the stack, and then I would like to demonstrate, how easy it is to tweak the code and redeploy it within a few single steps. The benefit is a shippable product from day *zero*, allowing you to spend less time on the structure and concentrate solely on the content. I will put more focus on delivery, automation and continuity rather than on designing the best neural network architecture mankind has ever known - which ain't gonna happen anyway, at least not with the data set I chose for this tutorial, yes you got it right, the most elementary chewed out data set in the universe - the one and only **MNIST**.

The technology stack used in this entry consists mainly of the core `TensorFlow` frameworks: `Keras`, `TensorFlow Serving` and `TensorBoard` - with `Flask` and `Nginx` for *RESTifying* the API and `Docker` for deployment. The code is hosted on [github.com](https://github.com/ariellev/fullstack-tensor-flow) and completely available for you to download and experiment with.

One last point. The tutorial speaks mainly *Linux'ish*. Nevertheless I hope that windows users, also when not necessarily able to take advantage of the related scripts, can still benefit from the overall content. If installing a virtual machine is an option, then I would recommend one of two awesome products: [VMWare](https://my.vmware.com/en/web/vmware/free#desktop_end_user_computing/vmware_workstation_player/14_0) or [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

## Get started
So after a short introduction we are finally able to dive into the implementation part. The basic setup encompasses `docker-engine` (community edition), a `docker-registry` and a `docker-compose` - all running on `localhost`. Visit [store.docker.com](https://store.docker.com/search?type=edition&offering=community), select an appropriate edition and follow the hints for downloading and installing the engine on your machine. Having docker-engine in place you may want to proceed and install [compose](https://docs.docker.com/compose/install/#install-compose) and look into [manage-docker-as-a-non-root-user](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user). Finally run the following one-liner to install the registry:
```bash
# see https://docs.docker.com/registry/deploying/
> docker run -d -p 5000:5000 --restart=always --name registry registry:2
```
You can `docker ps` to make sure the registry's running. The catalog endpoint `/v2/_catalog` should respond with an empty repository.
```bash
> docker ps

CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
1e423a956a70        registry:2          "/entrypoint.sh /etc…"   3 seconds ago       Up 1 second         0.0.0.0:5000<center>5000/tcp   registry

# calling the catalog endpoint shows as expected, that the registry is still empty.
> curl localhost:5000/v2/_catalog
{"repositories":[]}
```
By the way, I am a big fan of administrating docker with the **CLI**. Nevertheless there are some wonderful GUIs out there to help you accomplishing exactly the same task perhaps with a much more visually appealing interface. Check for example [kitematic](
https://kitematic.com/)

The last step is to tell the local `docker-engine` that our registry is insecured<sup>[1](#private-registry)</sup>. Open the page [*Test an insecure registry*](https://docs.docker.com/registry/insecure/) and follow the section *Deploy a plain HTTP registry*. Let's smoke test the connection! We can pull a standard image from [Docker Hub](https://hub.docker.com/) and see what happens, we when push it to our private docker registry we have just created.
```bash
> docker pull hello-world
> docker tag hello-world localhost:5000/hello-world
> docker push localhost:5000/hello-world

The push refers to repository [localhost:5000/hello-world]
ee83fc5847cb: Pushed
latest: digest: sha256:aca41a608e5eb015f1ec6755f490f3be26b48010b178e78c00eac21ffbe246f1 size: 524
```
By calling the catalog endpoint once again, we can magically notice a new image:
```bash
> curl localhost:5000/v2/_catalog
{"repositories":["hello-world"]}
```
Well done! You have just accomplished all the necessary steps needed to run the application on your local machine.

## Run the TensorFlow stack
### Build & push
Now that we are capable of deploying the TensorFlow stack on localhost, let's clone the [fullstack-tensor-flow](https://github.com/ariellev/fullstack-tensor-flow.git) repository and proceed with the following commands
```bash
> git clone https://github.com/ariellev/fullstack-tensor-flow.git
> cd fullstack-tensor-flow

> export registry=localhost:5000
> export PATH="$(realpath ./bin):$PATH"
> push-all-docker.sh --group lab  

------------------------------------------------
registry    localhost:5000
dockerfile  /Users/ariellev/sandbox/fullstack-tensor-flow/tensor-board
image       lab/tensor-board:latest
------------------------------------------------
Sending build context to Docker daemon  2.048kB
Step 1/5 : FROM frolvlad/alpine-miniconda3:python3.6
 --<center> f2c7e6ebb9a7
 ..
```
The `push-all-docker.sh` script scans the working directory recursively for Dockerfiles. Any match is being built and subsequently pushed to a given registry. The script takes several minutes to complete and it produces a fair amount of output. At the end you can expect to see 4 new images created:
```bash
> docker images | grep 'lab\|REPOSITORY'

REPOSITORY                                 TAG                 IMAGE ID            CREATED             SIZE
localhost:5000/lab/tensor-rest             latest              6579ef0639ea        2 days ago          1.71GB
localhost:5000/lab/tensor-serving-cpu      latest              f2252bea248c        2 days ago          381MB
localhost:5000/lab/tensor-jupyter          latest              7d4a53488525        2 days ago          1.8GB
localhost:5000/lab/tensor-board            latest              282d3217ac0b        2 days ago          712MB
```
`curl localhost:5000/v2/_catalog` should yield a simliar listing:
```json
{  
   "repositories":[  
      "hello-world",
      "lab/tensor-board",
      "lab/tensor-jupyter",
      "lab/tensor-rest",
      "lab/tensor-serving-cpu"
   ]
}
```
### Architecture

The `push-all-docker.sh` script created 4 new images:

* **tensor-jupyter**: Running a **JupterLab** instance, which is *"An extensible environment for interactive and reproducible computing"*<sup>[2](#jupyterlab)</sup>. You will use this web based IDE to run the code for training and exporting the **MNIST** neural network.
* **tensor-serving-cpu**: Running a **TensorFlow Serving** server, to which we will be deploying the exported **MNIST** model. More info on [tensorflow/serving](https://github.com/tensorflow/serving)
* **tensor-board**: Running **TensorBoard** - a suite of visualization tools for debugging and assessing TensorFlow programs. See [summaries_and_tensorboard](https://www.tensorflow.org/guide/summaries_and_tensorboard)
* **tensor-rest**: An adapter for accessing **tensor-serving-cpu** with a convenient REST API. The image contains a *Flask* Server proxied by *Nginx*

The diagram below depicts the overall architecture:

![alt architecture](https://raw.githubusercontent.com/ariellev/fullstack-tensor-flow/master/images/fullstack-tensor-flow.001.jpeg)

### Launch
Having built the images we are set to move forward and launch them locally using **Docker Compose** - *"a tool for defining and running multi-container Docker applications."*<sup>[3](#docker-compose)</sup> But instead of calling `docker-compose` directly we will execute another wrapper script called `compose.sh`, which sets up a few environment variables before calling the underlying `docker-compose` command. Feel free to look into [.deploy/localhost-compose.yml](https://github.com/ariellev/fullstack-tensor-flow/blob/master/.deploy/localhost-compose.yml) to see the details regarding the configuration of the application.
```bash
> compose.sh up -f .deploy/localhost-compose.yml

-------------------------------------------------------
docker-compose           up
-------------------------------------------------------
compose_file     .deploy/localhost-compose.yml
env_file         localhost-compose.env
project          lab
docker_ip
registry         localhost:5000
tag              latest
-------------------------------------------------------
Creating network "lab_default" with the default driver
Creating tensor-board       ... done
Creating tensor-serving-cpu ... done
Creating tensor-rest        ... done
Creating tensor-jupyter     ... done
```
Calling `docker ps` should list all 4 containers:

```bash
> docker ps | grep 'IMAGE\|lab'
CONTAINER ID        IMAGE                                          COMMAND                   CREATED              STATUS              PORTS                              NAMES
0fc0b78f488d        localhost:5000/lab/tensor-jupyter:latest       "/bin/sh -c 'jupyter…"    About a minute ago   Up About a minute   6006/tcp, 0.0.0.0:8888<center>8888/tcp   tensor-jupyter
ce2b800ac07a        localhost:5000/lab/tensor-rest:latest          "/entrypoint.sh /usr…"    About a minute ago   Up About a minute   443/tcp, 0.0.0.0:8080<center>80/tcp      tensor-rest
8fb04a403fe0        localhost:5000/lab/tensor-serving-cpu:latest   "/bin/sh -c \"entrypo…"   About a minute ago   Up About a minute   0.0.0.0:9000<center>9000/tcp             tensor-serving-cpu
4438e3d1dd41        localhost:5000/lab/tensor-board:latest         "/bin/sh -c 'tensorb…"    About a minute ago   Up About a minute   0.0.0.0:6006<center>6006/tcp             tensor-board
```
The services below, followed by their screenshots, are now accessible in your browser:
* [Jupyter Lab](http://localhost:8888/)
* [Tensor-Board](http://localhost:6006/)
* [RESTful API](http://localhost:8080/tf/#!/mnist/post_mnist)

<center><i>Jupyter Lab</i></center>

![alt Juypter Lab](https://raw.githubusercontent.com/ariellev/fullstack-tensor-flow/master/images/jupyter.png)

<center><i>Tensor Board</i></center>

![alt TensorBoard](https://raw.githubusercontent.com/ariellev/fullstack-tensor-flow/master/images/tensor-board-0.png)

<center><i>Interactive RESTful API with Swagger</i></center>

![alt RESTful API](https://raw.githubusercontent.com/ariellev/fullstack-tensor-flow/master/images/rest-1.png)

### Try it out!
Open the [Swagger UI](http://localhost:8080/tf/#!/mnist/post_mnist) in your browser. In the `model` value field enter the name `mnist-net`. Next we need to upload a digit image for prediction. Inside the [tensor-rest/data/mnist](https://github.com/ariellev/fullstack-tensor-flow/tree/master/tensor-rest/data/mnist) folder in your repository you'll find 100 images I extracted in advance. The files are named with the following convention: `mnist_[N]_[id].jpg`, where `N = a digit from 0 to 9` and `id = some random string`, i.e. the prefix `mnist_2` implies an image of the digit `2` and so on. Finally click ```Try it out!``` and.. ***Voilà!***
```json
{
  "classification_result": [
    {
      "digit": 2,
      "probability": 1
    },
    {
      "digit": 0,
      "probability": 0
    },
    {
      "digit": 1,
      "probability": 0
    }
  ]
}
```
**Congratulations!** you have just built, deployed and tested the application on your `localhost`!  
In the next section I'd like to show you, how you can easily tweak the code and ship any update almost seamlessly.

## Tweak and re-deploy
In your browser open the [Jupater Lab](http://localhost:8888) tab and navigate to the `MnistNet` notebook in the file explorer on the left side of the screen (`MNIST -> MnistNet.ipyb`). Once opened scroll down to the 2nd block, find the line in which the training context is being declared, and rename the model from `mnist-net` to a name of your wish, say `mnist-tutorial`
```python
cxt = Context('mnist-tutorial', 1)
```
Now let's run the notebook. In the toolbar go to: `Run -> Run All Cells`, and wait a few minutes for the execution to complete. During the executing a double layered convolutional neural network will be trained over the MNIST dataset. At the end, the model is serialized and written to the file system. Upon running `docker exec tensor-jupyter tree /home/ml/models` you may expect to see a new folder called `mnist-tutorial`
```bash
/home/ml/models
|-- mnist-net
|   `-- 1
|       |-- saved_model.pb
|       `-- variables
|           |-- variables.data-00000-of-00001
|           `-- variables.index
`-- mnist-tutorial
    `-- 1
        |-- saved_model.pb
        `-- variables
            |-- variables.data-00000-of-00001
            `-- variables.index
```
If you looked carefully into `.deploy/localhost-compose.yml` you have probably noticed, that the `/home/ml/models` folder listed above is shared along with `tensor-serving`. Each time the container is being restarted, it creates a unified model config file, that includes all models found under the model directoy. I assume it might sound a bit complicated, but in reality, it is merely a bash script that echos JSON snippets into a file. Go ahead and refer to `./tensor-serving-cpu/generate-tensor-conf.sh` to discover some more. I encourage you to also take a look into the caller of the script, namely: `./tensor-serving-cpu/entrypoint.sh`. If we restart the container and output the logs (`docker restart tensor-serving-cpu && docker logs tensor-serving-cpu`) we'll notice right away the new configuration of the `mnist-tutorial` model we have just exported:
```bash
model_config_list: {
config: {
      name: 'mnist-net',
      base_path: '/serving/mnist-net',
      model_platform: 'tensorflow'
    },
config: {
      name: 'mnist-tutorial',
      base_path: '/serving/mnist-tutorial',
      model_platform: 'tensorflow'
    },
}
```
Let's return to our little [Swagger UI](http://localhost:8080/tf/#!/mnist/post_mnist). This time instead of `mnist-net` let's type in `mnist-tutorial` into the model value input field. When you next click on `Try it out!` you'll see a response with the same payload as before, nevertheless the data has originated this time from the model you had freshly deployed.

**Isn't that insane ?!** you can repeatedly modify the code - improve the architecture, fix bugs, enhance the data acquisition or boost the feature engineering - and as you go, you only have to restart a single container to make the changes visible to the end user.

## TensorBoard
If you look again into the training code @ `MnistNet.ipyb` you'll note, that the `model.fit` function is given a callback argument named `tensor_board`. This callback basically writes logs for `TensorBoard` to crunch, which in turn allows you to visualize dynamic graphs of your training and test metrics, as well as activation histograms for the different layers in your model. The logs are written to a folder called `/home/ml/logs`, which is just happened to be shared with the `tensor-board` container. You may open [TensorBoard](http://localhost:6006/) once again in your browser and recognize, that this time, the view is populated with all kinds of metrics:  
![alt Scalars](https://raw.githubusercontent.com/ariellev/fullstack-tensor-flow/master/images/tensor-board-1.png)
![alt Activations](https://raw.githubusercontent.com/ariellev/fullstack-tensor-flow/master/images/tensor-board-2.png)
![alt Graph](https://raw.githubusercontent.com/ariellev/fullstack-tensor-flow/master/images/tensor-board-3.png)

We are mostly done with the basic part - you master essentially everything a *DevOps Tiger* has to know, in order to bring a trained neural network to production. So you may stop here if you wish to. Otherwise, if you still curious and want to discover some more about what actually happens under the hood, then the next part is all about revealing some more of the mystery.

## Under the Hood

### Flask
The RESTful service running inside `tensor-rest` is developed with [Flask](http://flask.pocoo.org/) - a python based microframework. The swagger interactive documentation is automatically generated by an extension called `flask-restplus`. Both packages can be easily installed using `pip`.

The API exposed by `Flask` is merely an abstraction layer on top of `tensor-serving-cpu`. You may call it an adapter if you want, cause that what it actually does. HTTP Request flows in; it is then serialized using [gRPC](https://grpc.io/) ( more or less a byte array representation of a predefined domain model, that can be interpreted by the upstream server `TensorServing`); the payload is transmitted futher down the wire to `tensor-serving-cpu`; whose response gets converted back to HTTP containing a *JSONic* payload.

If you want to take a look into the specifics of the implementation you may refert to [endpoints.py](https://github.com/ariellev/fullstack-tensor-flow/blob/master/tensor-rest/app/tf/api/mnist/endpoints.py) and
[mnist_client.py](https://github.com/ariellev/fullstack-tensor-flow/blob/master/tensor-rest/app/tf/api/mnist/mnist_client.py)

### Nginx
Flask's default development server is not meant under any circumstances to be "client facing", as it does not scale well and by default serves only one request at a time. According to the official [documentation](http://flask.pocoo.org/docs/1.0/tutorial/deploy/#run-with-a-production-server):

*When running publicly rather than in development, you should not use the built-in development server (flask run). The development server is provided by Werkzeug for convenience, but is not designed to be particularly efficient, stable, or secure.*

Hence `tensor-rest` comes with a web server, more precisely with [Nginx](https://www.nginx.com/), which functions as a reverse proxy for the `Flask` application server. Just for the record, the decision of wrapping the two components side by side into a single image is not carved in stone - simplicity is just being traded for modularity. So pulling `Nginx` to a different image makes totally sense - especially if one wants to gain a finer operational controll. The two components speak [WSGI](http://wsgi.tutorial.codepoint.net/) und communicate over a socket. To get the complete picture concerning the configuration take a look into the following files:
1. `tensor-rest/nginx.conf`
```bash
location ~* {
      ..

      # proxy pass to /tmp/tf.sock      
      uwsgi_pass unix:///tmp/tf.sock;
}
```
2. `tensor-rest/app/uwsgi.ini`
```bash
#
# uwsgi listens on /tmp/tf.sock , http on port 9090.
# WSGI application points to the global variable 'app' of tf.main
#
[uwsgi]
http = :9090
socket = /tmp/tf.sock
module = tf.main
callable = app
```

3. `tensor-rest/app/tf/main.py`
```python
app = Flask(__name__)
```

4. `tensor-rest/Dockefile`
```bash
#
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/
#
# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /app/uwsgi.ini
```

## Beyond localhost
The container orchestration market is highly saturated<sup>[4](#container-adoption-survey)</sup> meaning at the very least, that the number of well established products we had to theoretically cover is unfortunately above and beyond any feasible scope. Still dockerizing an application and running it locally, also when not exactly the final destination, is a remarkable step forward in achieving the goal of deploying the application to a productive environment. So **way to go!** you are now mastering a powerful skill.

And regarding the future.. well..  
*Roll your sleeves up! Nail the services to the cloud and Good Luck!*

![alt Cloud](https://raw.githubusercontent.com/ariellev/fullstack-tensor-flow/master/images/blah-blah-cloud.png)

___
<a name="private-registry">1. Depending on the version of your docker engine this step may be obsolete.</a>   
<a name="jupyterlab" href="https://github.com/jupyterlab/jupyterlab">2. Jupyter Lab</a>  
<a name="docker-compose" href="https://docs.docker.com/compose/">3. Docker Compose</a>  
<a name="container-adoption-survey" href="https://portworx.com/2017-container-adoption-survey/">4. 2017 Container Adoption Survey</a>
