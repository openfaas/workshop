# Lab 1 - Prepare for OpenFaaS

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

OpenFaaS runs on top of several major platforms including Docker Swarm and Kubernetes. For this tutorial we will get started with Docker Swarm on your local computer.

The basic primitive for any OpenFaaS function is a Docker image, which is built using the `faas-cli` tool-chain.

## Pre-requisites:

### Docker

For Mac

* [Docker CE for Mac Edge Edition](https://store.docker.com/editions/community/docker-ce-desktop-mac)

For Windows 

* Use Windows 10 Pro or Enterprise only
* Install [Docker CE for Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows)
* Install [Git Bash](https://git-scm.com/downloads)

> Note: please use Git Bash for all steps: do not attempt to use *WSL* or *Bash for Windows*.

Linux - Ubuntu or Debian

* Docker CE for Linux

> You can install Docker CE from the [Docker Store](https://store.docker.com).

Note: As a last resort if you have an incompatible PC you can run the workshop on https://labs.play-with-docker.com/.

### Setup a single-node Docker Swarm

OpenFaaS works with Docker Swarm and Kubernetes. For this workshop we will use Docker Swarm because it's easier to set up but there are [deployment guides for both options in the documentation](https://github.com/openfaas/faas/tree/master/guide).

On your laptop or VM setup a single-node Docker Swarm:

```
$ docker swarm init
```

> If you receive an error then pass the `--advertise-addr` parameter along with your laptop's IP address.

### Docker Hub

Sign up for a Docker Hub account. The [Docker Hub](https://hub.docker.com) allows you to publish your Docker images on the Internet for use on multi-node clusters or to share with the wider community. We will be using the Docker Hub to publish our functions during the workshop.

You can sign up here: [Docker Hub](https://hub.docker.com)

> Note: The Docker Hub can also be setup to automate builds of Docker images.

Open a Terminal or Git Bash window and log into the Docker Hub using the username you signed up for above.

```
$ docker login
```
> On Windows if you see 'Error: Cannot perform an interactive login from a non TTY device' try running 'winpty docker login'

### OpenFaaS CLI

You can install the OpenFaaS CLI with `brew` on a Mac or with a utility script on Mac or Linux:

Using a Terminal on Mac or Linux:

```
$ curl -sL cli.openfaas.com | sudo sh
```

On Windows download the the latest `faas-cli.exe` from the [releases page](https://github.com/openfaas/faas-cli). You can place it in a local directory or in the `C:\Windows\` path so that it's available from a command prompt.

> If you're an advanced Windows user, place the CLI in a directory of your choice and then add that folder to your PATH environmental variable.

We will use the `faas-cli` to scaffold new functions, build, deploy and invoke functions. You can find out commands available for the cli with `faas-cli --help`.

Test the `faas-cli`

Open a Terminal or Git Bash window and type in:

```
$ faas-cli help
$ faas-cli version
```


### Deploy OpenFaaS

The instructions for deploying OpenFaaS change from time to time as we strive to make this easier. The following will get OpenFaaS deployed in around 60 seconds:

* First clone the repo:

```
$ git clone https://github.com/openfaas/faas
```

* Now checkout the latest version with Git

```
$ cd faas && \
  git checkout master
```

> Note: you can see the latest releases on the [project release page](https://github.com/openfaas/faas/releases).

* Now deploy the stack with Docker Swarm:

```
$  ./deploy_stack.sh
```

You should now have OpenFaaS deployed. If you are on a shared WiFi connection at an event then it may take several minutes to pull down all the Docker images and start them.

Check the services show `1/1` on this screen:

```
$ docker service ls
```

If you run into any problems, please consult the [Deployment guide](https://github.com/openfaas/faas/blob/master/guide/deployment_swarm.md) for Docker Swarm.

Now move onto [Lab 2](./lab2.md)
