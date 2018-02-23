# Lab 1 - The setup

OpenFaaS runs on top of several major platforms including Docker Swarm and Kubernetes. For this tutorial we will get started with Docker Swarm on your local computer.

The basic primitive for any OpenFaaS function is a Docker image, which is built using the `faas-cli` tool-chain.

## Pre-requisites:

### Docker

For Mac

* Docker CE for Mac

For Windows 

* Windows 10 Pro or Enterprise only
* Docker CE for Windows

Linux - Ubuntu or Debian

* Docker CE for Linux

You can install Docker CE from the [Docker Store](https://store.docker.com).

### Docker Hub

Sign up for a Docker Hub account. The [Docker Hub](https://hub.docker.com) allows you to publish your Docker images on the Internet for use on multi-node clusters or to share with the wider community. We will be using the Docker Hub to publish our functions during the workshop.

You can sign up here: [Docker Hub](https://hub.docker.com)

> Note: The Docker Hub can also be setup to automate builds of Docker images.

### OpenFaaS CLI

You can install the OpenFaaS CLI with `brew` on a Mac or with a utility script on Mac or Linux:

```
$ curl -sL cli.openfaas.com | sudo sh
```

On Windows download the the latest `faas-cli.exe` from the [releases page](https://github.com/openfaas/faas-cli). You can place it in a local directory or in the C:\Windows path so that it's available from a command prompt.

> If you're an advanced Windows user, place the CLI in a directory of your choice and then add that folder to your PATH environmental variable.

We will use the `faas-cli` to scaffold new functions, build, deploy and invoke functions. You can find out commands available for the cli with `faas-cli --help`.

### Setup a single-node Docker Swarm

OpenFaaS works with Docker Swarm and Kubernetes. For this workshop we will use Docker Swarm because it's easier to set up but there are [deployment guides for both options in the documentation](https://github.com/openfaas/faas/tree/master/guide).

On your laptop or VM setup a single-node Docker Swarm:

```
$ docker swarm init
```

> If you receive an error then pass the `--advertise-addr` parameter along with your laptop's IP address.

### Deploy OpenFaaS

The instructions for deploying OpenFaaS change from time to time as we strive to make this easier. Head over to the official deployment guide in the official guide and follow the steps:

* [Deployment guide](https://github.com/openfaas/faas/blob/master/guide/deployment_swarm.md)

You should now have OpenFaaS deployed. If you are on a shared WiFi connection at an event then it may take several minutes to pull down all the Docker images and start them.

Check the services show `1/1` and `running` on this screen:

```
$ docker service ls
```

## Test-out the UI

You can now test out the OpenFaaS UI by going to http://localhost:8080 or http://127.0.0.1:8080 - if you're deploying to a Linux VM then replace localhost with the IP address from the output you see on the `ifconfig` command.

Note: on some Linux distributions accessing `localhost` may hang, if that happens then oplease use `127.0.0.1` instead and replace it wherever you see `localhost`.

In the default stack we deploy several sample functions.

You can try them out in the UI such as the Markdown function which converts Markdown code into HTML.

Type in for example:

```
## The **OpenFaaS** _workshop_
```

Now click *Invoke* and see the response appear in the bottom half of the screen.

I.e.

```
<h2>The <strong>OpenFaaS</strong> <em>workshop</em></h2>
```

You will see the following fields displayed:

* Replicas - the amount of replicas of your function running in the swarm cluster
* Image - the Docker image name and version as published to the Docker Hub or Docekr repository
* Invocation count - this shows how many times the function has been invoked and is updated every 5 seconds

Click *Invoke* a number of times and see the *Invocation count* increase.

### Deploy a function from the store

You can deploy a function from the OpenFaaS store. The store is a free collection of functions curated by the community.

* Click *Deploy New Function*
* Click *From Store*
* Click *Figlet* or enter *figlet* into the search bar and then click *Deploy*

The Figlet function will now appear in your left-hand list of functions. Give this a few moments to be downloaded from the Docker Hub and then type in some text and click Invoke like we did for the Markdown function.

You'll see an ASCII logo generated like this:

```
 _  ___   ___ _  __
/ |/ _ \ / _ (_)/ /
| | | | | | | |/ / 
| | |_| | |_| / /_ 
|_|\___/ \___/_/(_)
``` 

## Test out the CLI

You can now test out the CLI.

* Note on alternate gateways:

If your gateway is not deployed at http://localhost:8080 then you will need to specify the `--gateway` flag followed by the alternate URL such as http://127.0.0.1:8080/

### List the deployed functions

This will show the functions, how many replicas you have and the invocation count.

```
$ faas-cli list
```

You should see the markdown function and the figlet function listed too along with how many times you've invoked them.

Now try the verbose flag

```
$ faas-cli list --verbose
```

You can now see the Docker image along with the names of the functions.

> Note: There is a shortcut for `--verbose` of `-v`.

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