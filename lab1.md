# Lab 1 - Prepare for OpenFaaS

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

OpenFaaS runs on top of several major platforms including Docker Swarm and Kubernetes. For this tutorial you can choose one of both on your local computer.

The basic primitive for any OpenFaaS function is a Docker image, which is built using the `faas-cli` tool-chain.

## Pre-requisites:

### Docker

For Mac

* [Docker CE for Mac Edge Edition](https://store.docker.com/editions/community/docker-ce-desktop-mac)

For Windows 

* Use Windows 10 Pro or Enterprise only
* Install [Docker CE for Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows)

> Please ensure you use the **Linux** containers Docker daemon by using the Docker menu in the Windows task bar notification area.

* Install [Git Bash](https://git-scm.com/downloads)

> Note: please use Git Bash for all steps: do not attempt to use *WSL* or *Bash for Windows*.

Linux - Ubuntu or Debian

* Docker CE for Linux

> You can install Docker CE from the [Docker Store](https://store.docker.com).

Note: As a last resort if you have an incompatible PC you can run the workshop on https://labs.play-with-docker.com/.

If you're taking part in a workshop event then the organiser will probably ask you to use Docker Swarm because it's much easier to set up in a short period of time. There are [deployment guides for both Swarm and Kubernetes in the documentation](https://github.com/openfaas/faas/tree/master/guide).

In order to set up OpenFaaS with Docker Swarm, go to [Lab 1a](./lab1a.md)

If you're going to use Kubernetes, follow [Lab 1b](./lab1b.md)
