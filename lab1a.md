# Lab 1a - Set-up OpenFaaS with Docker Swarm

<img src="https://www.ibm.com/blogs/bluemix/wp-content/uploads/2018/10/swarm1-300x300.png" width="300px"></img>

### Setup a single-node cluster

OpenFaaS works both with Kubernetes and Docker Swarm. If you're taking part in a workshop event then the organiser will probably ask you to use Docker Swarm because it's much easier to set up in a short period of time. There are [deployment guides for both options in the documentation](https://docs.openfaas.com/deployment/).

On your laptop or VM setup a single-node Docker Swarm:

```sh
$ docker swarm init
```

> If you receive an error then pass the `--advertise-addr` parameter along with your laptop's IP address.

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
