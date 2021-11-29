# Lab 1 - Set-up OpenFaaS with Kubernetes

<img src="https://kubernetes.io/images/kubernetes-horizontal-color.png" width="500px"></img>

## Install latest `kubectl`

Install `kubectl` for your operating system using the instructions below or the [official documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

* Linux

```sh
export VER=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO https://storage.googleapis.com/kubernetes-release/release/$VER/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin/
```

* MacOS

```sh
export VER=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO https://storage.googleapis.com/kubernetes-release/release/$VER/bin/darwin/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin/
```

* Windows

```sh
export VER=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO https://storage.googleapis.com/kubernetes-release/release/$VER/bin/windows/amd64/kubectl.exe
chmod +x kubectl.exe
mkdir -p $HOME/bin/
mv kubectl $HOME/bin/
```

## Setup a Kubernetes cluster

You can follow the labs whilst using Kubernetes, but you may need to make some small changes along the way. The service address for the gateway changes from `http://gateway:8080` to `http://gateway.openfaas:8080`. As far as possible these differences have been documented and alternatives are provided in each lab.

### Create a local cluster on your laptop

#### *k3s using k3d*

If you have Docker on your computer, then you can use the `k3d` tool, hosted by Rancher Labs. It installs a lightweight version of Kubernetes called `k3s` and runs it within a Docker container, meaning it will work on any computer that has Docker.

* [Install k3d](https://github.com/rancher/k3d)

* Start a cluster

1. `k3d cluster create CLUSTER_NAME` to create a new single-node cluster (= 1 container running k3s + 1 loadbalancer container)
2. The context for kubectl will be updated automatically, you can check this with `kubectl config get-contexts`
3. execute some commands like `kubectl get pods --all-namespaces`
If you want to delete default cluster `k3d cluster delete CLUSTER_NAME`

#### _Docker for Mac_

* [Install Docker for Mac](https://docs.docker.com/v17.12/docker-for-mac/install/)

> Note that Kubernetes is only available in Docker for Mac 17.12 CE and higher

#### _With Minikube_

* To install Minikube download the proper installer from [latest release](https://github.com/kubernetes/minikube/releases) depending on your platform.

* Now run Minikube with

```
$ minikube start
```

The minikube VM is exposed to the host system via a host-only IP address. Check this IP with `minikube ip`.
This is the IP you will later use for the gateway URL.

> Note: Minikube also requires a Hypervisor such as VirtualBox or Hyperkit (on MacOS). Follow the minikube instructions and documentation

### Create a remote cluster on the cloud

You can create a remote cluster in the cloud and enjoy the same experience as if you were developing locally whilst saving on RAM/CPU and battery. The costs for running a cluster for 1-2 days is minimal.

#### _Run on DigitalOcean's Kubernetes Service_

You can use free credits to create a cluster through DigitalOcean's UI.

The DigitalOcean dashboard will then guide you through how to configure your `kubectl` and `KUBECONFIG` file for use in the labs.

* [Claim your free credits - $50 in credit over 30 days.](https://m.do.co/c/8d4e75e9886f)

Even if you have already claimed free credit, the running costs for a 2-3 node cluster for 24-48 hours is negligible.

* Click on *Kubernetes* on the left panel of the dashboard and then click "Enable Limited Access"

* Once logged in, click the *Kubernetes* menu item and create a Cluster.

It is recommended to use the latest Kubernetes version available and the to select your nearest Datacenter region to minimize latency.

* Under "Add node pool(s)"

Use 2x 4GB / 2vCPU

> Note: You can add more capacity at a later time, if required

* Download the [doctl](https://github.com/digitalocean/doctl#installing-doctl) CLI and place it in your path.

* Create an [API Key in your DigitalOcean dashboard](https://cloud.digitalocean.com/account/api/tokens/new)

Keep track of your API key (copy it to clipboard)

* Authenticate the CLI

```sh
$ doctl auth init
```

Paste in your API key

* Now get the cluster's name:

```sh
$ doctl k8s cluster list
GUID    workshop-lon1      nyc1      1.13.5-do.1    provisioning    workshop-lon1-1
```

* Save a config file so that `kubectl` is pointing at the new cluster:

```sh
$ doctl k8s cluster kubeconfig save workshop-lon1
```

You now need to switch your Kubernetes context to point at the new cluster.

Find the cluster name with `kubectl config get-contexts`, if it's not highlighted type in `kubectl config set-context <context-name>`.

#### _Run on GKE (Google Kubernetes Engine)_

Login into Google Cloud, create a project and enable billing for it. If you don’t have an account you can sign up [here](https://cloud.google.com/free/) for free credits.

Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs) - this will make the `gcloud` and `kubectl` commands available.
For Windows follow the instructions from the [documentation](https://cloud.google.com/sdk/docs/#windows).

After installing the gcloud command line utility, configure your project with `gcloud init` and set the default project, compute region and zone (replace `PROJECT_ID` with your own project):

```sh
$ gcloud config set project PROJECT_ID 
$ gcloud config set compute/region us-central1
$ gcloud config set compute/zone us-central1-a
```

Enable the Kubernetes service:

```sh
$ gcloud services enable container.googleapis.com
```

Install kubectl:

```sh
gcloud components install kubectl
```

Create a Kubernetes cluster:

```sh
$ gcloud container clusters create openfaas \
--zone=us-central1-a \
--num-nodes=1 \
--machine-type=n1-standard-2 \
--disk-size=30 \
--no-enable-cloud-logging
```

Set up credentials for `kubectl`:

```sh
$ gcloud container clusters get-credentials openfaas
```

Create a cluster admin role binding:

```sh
$ kubectl create clusterrolebinding "cluster-admin-$(whoami)" \
--clusterrole=cluster-admin \
--user="$(gcloud config get-value core/account)"
```

Now verify `kubectl` is configured to the GKE cluster:

```
$ kubectl get nodes
NAME                                   STATUS    ROLES     AGE       VERSION
gke-name-default-pool-eceef152-qjmt   Ready     <none>    1h        v1.10.7-gke.2
```

## Deploy OpenFaaS

The instructions for deploying OpenFaaS change from time to time as we strive to make this even easier.

### Install OpenFaaS

There are three ways to install OpenFaaS and you can pick whatever makes sense for you and your team. In this workshop we will use the official installer `arkade`.

* `arkade app install` - arkade installs OpenFaaS using its official helm chart. It can also offer other software with a user-friendly CLI such as `cert-manager` and `nginx-ingress`. It's the easiest and quickest way to get up and running.

* Helm chart - sane defaults and easy to configure through YAML or CLI flags. Secure options such as `helm template` or `helm 3` also exist for those working within restrictive environments

* Plain YAML files - hard-coded settings/values. Tools like Kustomize can offer custom settings

#### Install with `arkade`

* Get arkade

For MacOS / Linux:

```sh
# MacOS users may need to run "bash" first if this command fails
curl -SLsf https://dl.get-arkade.dev/ | sudo sh
```

For Windows:

```sh
curl -SLsf https://dl.get-arkade.dev/ | sh
```

* Install the OpenFaaS app

If you're using a managed cloud Kubernetes service which supplies LoadBalancers, then run the following:

```sh
arkade install openfaas --load-balancer
```

> Note: the `--load-balancer` flag has a default of `false`, so by passing the flag, the installation will request one from your cloud provider.

If you're using a local Kubernetes cluster or a VM, then run:

```sh
arkade install openfaas
```

In a later lab, we'll show you how to set up a custom domain with TLS using Kubernetes Ingress.

#### Or install with helm (advanced)

If you prefer, you can install OpenFaaS using the [helm chart](https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/README.md) instructions.

### Log into your OpenFaaS gateway

* Check the gateway is ready

```sh
kubectl rollout status -n openfaas deploy/gateway
```

If you're using your laptop, a VM, or any other kind of Kubernetes distribution run the following instead:

```sh
kubectl port-forward svc/gateway -n openfaas 8080:8080
```

This command will open a tunnel from your Kubernetes cluster to your local computer so that you can access the OpenFaaS gateway. There are other ways to access OpenFaaS, but that is beyond the scope of this workshop.

Your gateway URL is: `http://127.0.0.1:8080`

If you're using a managed cloud Kubernetes service then get the LoadBalancer's IP address or DNS entry from the `EXTERNAL-IP` field from the command below.

```sh
kubectl get svc -o wide gateway-external -n openfaas
```

Your URL will be the IP or DNS entry above on port `8080`.

* Log in:

```sh
export OPENFAAS_URL="" # Populate as above

# This command retrieves your password
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)

# This command logs in and saves a file to ~/.openfaas/config.yml
echo -n $PASSWORD | faas-cli login --username admin --password-stdin
```

* Check that `faas-cli list` works:

```sh
faas-cli list
```

### Permanently save your OpenFaaS URL
 
Edit `~/.bashrc` or `~/.bash_profile` - create the file if it doesn't exist.

Now add the following - changing the URL as per the one you saw above.

```sh
export OPENFAAS_URL="" # populate as above
```

Now move onto [Lab 2](lab2.md)
