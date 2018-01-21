# Lab 1 - The setup

OpenFaaS runs on top of several major platforms including Docker Swarm and Kubernetes. For this tutorial we will get started with Docker Swarm on your local computer.

The basic primitive for any OpenFaaS function is a Docker image, which is built using the `faas-cli` tool-chain.

## Pre-requisites:

### Docker

* Docker CE for Windows
* Docker CE for Mac
* Docker CE for Linux (i.e. Ubuntu/Debian)

You can install Docker CE from the [Docker Store](https://store.docker.com).


### Docker Hub

Sign up for a Docker Hub account. The Docker Hub allows you to publish your Docker images on the Internet for use on multi-node clusters or to share with the wider community.

You can sign up here: [Docker Hub](https://hub.docker.com)

The Docker Hub can also be setup to automate builds of your Docker images.

### OpenFaaS CLI

You can install the OpenFaaS CLI with `brew` on a Mac or with a utility script on Mac or Linux:

```
$ curl -sL cli.openfaas.com | sudo sh
```

On Windows download the the latest `faas-cli.exe` from the [releases page](https://github.com/openfaas/faas-cli). You can place it in a local directory or in the C:\Windows path so that it's available from a command prompt.

> If you're an advanced Windows user, place the CLI in a directory of your choice and then add that folder to your PATH environmental variable.

### Setup a single-node Docker Swarm

On your laptop or VM setup a single-node Docker Swarm

```
$ docker swarm init
```

> If you receive an error then pass the `--advertise-addr` parameter along with your public IP address.

### Deploy OpenFaaS

We're always striving to improve the deployment method for OpenFaaS, so the first port of call should be our deployment guide in the official guide.

* [Deployment guide](https://github.com/openfaas/faas/blob/master/guide/deployment_swarm.md)

## Test-out the UI

You can test out the OpenFaaS UI by going to http://localhost:8080 or http://127.0.0.1:8080 - if you're deploying to a Linux VM then replace localhost with the IP address from the output you see on the `ifconfig` command.

In the default stack we deploy several sample functions. Try them out in the UI.

## Test out the CLI

You can now test out the CLI.

* Note on alternate gateways:

If your gateway is not deployed at http://localhost:8080 then you will need to specify the `--gateway` flag followed by the alternate URL such as http://127.0.0.1:8080/

### List the deployed functions

This will show the functions, how many replicas you have and the invocation count.

```
faas-cli list
```

Get verbose information (includes the Docker image)

```
faas-cli list --verbose
```

### Invoke a function

Pick one of the names from above such as `func_echoit` and enter it below:

```
faas-cli invoke func_echoit
```

You'll now be asked to type in some text. Hit Control + D when you're done.

Alternatively you can use a command such as `echo` or `uname -a` as input to the `invoke` command.

```
echo Hi | faas-cli invoke func_echoit

uname -a | faas-cli invoke func_echoit
```

Move onto [Lab 2](lab2.md)