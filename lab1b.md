# Lab 1 - Set-up OpenFaaS with Kubernetes

<img src="https://kubernetes.io/images/kubernetes-horizontal-color.png" width="500px"></img>

### Setup a single-node cluster

You can follow the labs whilst using Kubernetes, but you may need to make some small changes along the way. The service address for the gateway changes from `http://gateway:8080` to `http://gateway.openfaas:8080`.

If using a `NodePort` then the gateway address for the OpenFaaS CLI is normally http://IP_ADDRESS:31112/

You can choose different options to run Kubernetes on your machine.

Before proceeding, [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

#### _With Minikube_

* To install Minikube download the proper installer from [latest release](https://github.com/kubernetes/minikube/releases) depending on your platform.
* [Install Helm client](https://docs.helm.sh/using_helm/#installing-the-helm-client)

* Now run Minikube with
```
$ minikube start
```

> Note: If you're having any issues on starting minikube, try
> ```
> $ minikube stop && minikube delete
> ```
> and then run `minikube start` again.

* Initialize Helm and install Tiller with
```
$ helm init
```

The minikube VM is exposed to the host system via a host-only IP address. Check this IP with `minikube ip`.
This is the IP you will later use for the gateway URL.

#### _Docker for Mac_

* [Install Docker for Mac](https://docs.docker.com/v17.12/docker-for-mac/install/)
> Note that Kubernetes is only available in Docker for Mac 17.12 CE and higher

#### _Run on GKE (Google Kubernetes Engine)_

* Install [Google Cloud SDK](https://cloud.google.com/sdk/docs)

Mac:
```
$ brew cask install google-cloud-sdk
```

Ubuntu:
```
$ sudo apt-get update && sudo apt-get install google-cloud-sdk
```

For Windows follow the instructions from the [Documentation](https://cloud.google.com/sdk/docs/#windows)

*  Create Kubernetes cluster using the Google Cloud Platform.

In the GCP console, go to Kubernetes Engine -> Clusters and create new cluster.

* Once you have it, configure `kubectl` command-line access by running the following command:
(You can copy the command from the GCP console after clicking `Connect`):
```
$ gcloud container clusters get-credentials <cluster_name> --zone <cluster_zone> --project <project_name>
```

Now verify `kubectl` is configured to the GKE cluster by
```
$ kubectl get nodes
NAME                                   STATUS    ROLES     AGE       VERSION
gke-name-default-pool-eceef152-qjmt   Ready     <none>    1h        v1.10.7-gke.2
```

* Create Load Balancer

From GCP console, go to Network services -> Load balancing and create new load balancer for TCP.
Select Instance group to match your cluster's group. Set port to `31112` and IP to `Ephemeral`.

Save your load balancer IP as you will need it to set the gateway URL.

### Docker Hub

Sign up for a Docker Hub account. The [Docker Hub](https://hub.docker.com) allows you to publish your Docker images on the Internet for use on multi-node clusters or to share with the wider community. We will be using the Docker Hub to publish our functions during the workshop.

You can sign up here: [Docker Hub](https://hub.docker.com)

> Note: The Docker Hub can also be setup to automate builds of Docker images.

Open a Terminal or Git Bash window and log into the Docker Hub using the username you signed up for above.

```
$ docker login
```

> Note: Tip from community - if you get an error while trying to run this command on a Windows machine, then click on the Docker for Windows icon in the taskbar and log into Docker there instead "Sign in / Create Docker ID".

### OpenFaaS CLI

You can install the OpenFaaS CLI with `brew` on a Mac or with a utility script on Mac or Linux:

Using a Terminal on Mac or Linux:

```
$ curl -sL cli.openfaas.com | sudo sh
```

On Windows download the the latest `faas-cli.exe` from the [releases page](https://github.com/openfaas/faas-cli/releases). You can place it in a local directory or in the `C:\Windows\` path so that it's available from a command prompt.

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

To deploy on Kubernetes, you can run the commands from the [Documentation](https://docs.openfaas.com/deployment/kubernetes/#b-deploy-using-kubectlyaml-for-development-only)

Now set the `OPENFAAS_URL` variable to link to the proper IP:
```bash
export OPENFAAS_URL=http://IP_ADDRESS:31112
```

You should now have OpenFaaS deployed. If you are on a shared WiFi connection at an event then it may take several minutes to pull down all the Docker images and start them.

Check the services show `1/1` on this screen:

```
$ kubectl get pods -n openfaas
NAME                            READY     STATUS    RESTARTS   AGE
alertmanager-f5b4dfb8b-ztbb7    1/1       Running   0          1h
gateway-d8477b4b6-m962x         2/2       Running   0          1h
nats-86955fb749-8w65j           1/1       Running   0          1h
prometheus-7d78d54b57-nncss     1/1       Running   0          1h
queue-worker-8698f5bb78-qfv6n   1/1       Running   0          1h
```

If you run into any problems, please consult the [Deployment guide](https://github.com/openfaas/faas/blob/master/guide/deployment_swarm.md) for Docker Swarm.

Now move onto [Lab 2](./lab2.md)
