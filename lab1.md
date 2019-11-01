# Lab 1 - Prepare for OpenFaaS

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

OpenFaaS requires a [Kubernetes](https://kubernetes.io) or [Docker Swarm](https://docs.docker.com/engine/swarm/) cluster to operate. You can use a single-node cluster or a multi-node cluster, whether that's on your laptop or in the cloud.

The basic primitive for any OpenFaaS function is a Docker image, which is built using the `faas-cli` tool-chain.

## Pre-requisites:

Let's install Docker, the OpenFaaS CLI and pick Kubernetes or Swarm to proceed.

### Docker

For Mac

* [Docker CE for Mac Edge Edition](https://store.docker.com/editions/community/docker-ce-desktop-mac)

For Windows 

* Use Windows 10 Pro or Enterprise only
* Install [Docker CE for Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows)

> Please ensure you use the **Linux** containers Docker daemon by using the Docker menu in the Windows task bar notification area.

* Install [Git Bash](https://git-scm.com/downloads)

When you install git bash pick the following options: `install UNIX commands` and `use true-type font`.

> Note: please use *Git Bash* for all steps: do not attempt to use *PowerShell*, *WSL* or *Bash for Windows*.

Linux - Ubuntu or Debian

* Docker CE for Linux

> You can install Docker CE from the [Docker Store](https://store.docker.com).

Note: As a last resort if you have an incompatible PC you can run the workshop on https://labs.play-with-docker.com/.

### OpenFaaS CLI

You can install the OpenFaaS CLI using the official bash script, `brew` is also available but can lag one or two versions behind.

With MacOS or Linux run the following in a Terminal:

```sh
$ curl -sLSf https://cli.openfaas.com | sudo sh
```

For Windows, run this in *Git Bash*:

```sh
$ curl -sLSf https://cli.openfaas.com | sh
```

> If you run into any issues then you can download the latest `faas-cli.exe` manually from the [releases page](https://github.com/openfaas/faas-cli/releases). You can place it in a local directory or in the `C:\Windows\` path so that it's available from a command prompt.

We will use the `faas-cli` to scaffold new functions, build, deploy and invoke functions. You can find out commands available for the cli with `faas-cli --help`.

Test the `faas-cli`. Open a Terminal or Git Bash window and type in:

```sh
$ faas-cli help
$ faas-cli version
```

### Setup a single-node cluster

If you're taking part in an instructor-lead event then the organiser may ask you to use Docker Swarm, because it's much quicker and easier to set up in a short period of time. For some workshops you will be using Kubernetes.

If you are working independently then choice is entirely your own.

Start the first lab by picking one of the tracks below:

* Docker Swarm: [Lab 1a](./lab1a.md)

* Kubernetes: [Lab 1b](./lab1b.md)


### Pre-pull the system images (only if using Swarm)

Pull the most recent OpenFaaS images. 

```
curl -sSL https://raw.githubusercontent.com/openfaas/faas/master/docker-compose.yml | grep image | awk -F " " '{print $NF}' | xargs -L1 docker pull
```

This should offset the impact on the workshop WiFi of multiple attendees trying to pull the images at the same time.
