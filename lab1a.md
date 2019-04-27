# Lab 1a - Set-up OpenFaaS with Docker Swarm

<img src="https://www.ibm.com/blogs/bluemix/wp-content/uploads/2018/10/swarm1-300x300.png" width="300px"></img>

### Setup a single-node cluster

OpenFaaS works both with Kubernetes and Docker Swarm. If you're taking part in a workshop event then the organiser will probably ask you to use Docker Swarm because it's much easier to set up in a short period of time. There are [deployment guides for both options in the documentation](https://github.com/openfaas/faas/tree/master/guide).

On your laptop or VM setup a single-node Docker Swarm:

```sh
$ docker swarm init
```

> If you receive an error then pass the `--advertise-addr` parameter along with your laptop's IP address.

### Docker Hub

Sign up for a Docker Hub account. The [Docker Hub](https://hub.docker.com) allows you to publish your Docker images on the Internet for use on multi-node clusters or to share with the wider community. We will be using the Docker Hub to publish our functions during the workshop.

You can sign up here: [Docker Hub](https://hub.docker.com)

> Note: The Docker Hub can also be setup to automate builds of Docker images.

Open a Terminal or Git Bash window and log into the Docker Hub using the username you signed up for above.

```sh
$ docker login
```

> Note: Tip from community - if you get an error while trying to run this command on a Windows machine, then click on the Docker for Windows icon in the taskbar and log into Docker there instead "Sign in / Create Docker ID".

### OpenFaaS CLI

You can install the OpenFaaS CLI with `brew` on a Mac or with a utility script on Mac or Linux:

Using a Terminal on Mac or Linux:

```sh
$ curl -sL cli.openfaas.com | sudo sh
```

On Windows download the the latest `faas-cli.exe` from the [releases page](https://github.com/openfaas/faas-cli/releases). You can place it in a local directory or in the `C:\Windows\` path so that it's available from a command prompt.

> If you're an advanced Windows user, place the CLI in a directory of your choice and then add that folder to your PATH environmental variable.

We will use the `faas-cli` to scaffold new functions, build, deploy and invoke functions. You can find out commands available for the cli with `faas-cli --help`.

Test the `faas-cli`

Open a Terminal or Git Bash window and type in:

```sh
$ faas-cli help
$ faas-cli version
```

### Deploy OpenFaaS

The instructions for deploying OpenFaaS change from time to time as we strive to make this easier. The following will get OpenFaaS deployed in around 60 seconds:

* First clone the repo:

```sh
$ git clone https://github.com/openfaas/faas
```

* Now checkout the latest version with Git

```sh
$ cd faas && \
  git checkout master
```

> Note: you can see the latest releases on the [project release page](https://github.com/openfaas/faas/releases).

* Now deploy the stack with Docker Swarm:

```sh
$ ./deploy_stack.sh
```

Watch out for the password and then run the command you are given in the output.

* Run the `faas-cli login` command

* Check if the services are up and showing 1/1 for each:

```sh
$ docker service ls
```

If you run into any problems, please consult the [Deployment guide](https://docs.openfaas.com/deployment/docker-swarm/) for Docker Swarm.

Now move onto [Lab 2](./lab2.md)
