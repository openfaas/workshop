# Lab 1 - Set-up OpenFaaS with Kubernetes

<img src="https://kubernetes.io/images/kubernetes-horizontal-color.png" width="500px"></img>

## Install latest `kubectl`

Install kubectl for your operating system using the [official instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl/). If you're on Windows use the instructions on the page and place the binary in `/usr/local/bin/` or `C:\windows\`.

### Linux

```sh
export VER=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO https://storage.googleapis.com/kubernetes-release/release/$VER/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin/
```

### MacOS

```sh
export VER=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO https://storage.googleapis.com/kubernetes-release/release/$VER/bin/darwin/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin/
```

> Note: you should install the latest version because the version you have may be out of date.

## Install kubectx

[kubectx](https://github.com/ahmetb/kubectx/blob/master/kubectx) can help you switch between multiple clusters.

If you're using Windows then download from the [releases page](https://github.com/ahmetb/kubectx/releases) and place in `/usr/bin/` or `C:\Windows\`.

On MacOS or Linux:

```sh
curl -sSLf https://raw.githubusercontent.com/ahmetb/kubectx/master/kubectx > kubectx
chmod +x kubectx
sudo mv kubectx /usr/local/bin/
```

## OpenFaaS CLI

You can install the OpenFaaS CLI with `brew` on a Mac or with a utility script on Mac or Linux:

Using a Terminal on Mac or Linux:

```sh
$ curl -sL cli.openfaas.com | sudo sh
```

On Windows download the the latest `faas-cli.exe` from the [releases page](https://github.com/openfaas/faas-cli/releases). You can place it in `C:\Windows\` or `/usr/local/bin/`

> If you're an advanced Windows user, place the CLI in a directory of your choice and then add that folder to your PATH environmental variable.

We will use the `faas-cli` to scaffold new functions, build, deploy and invoke functions. You can find out commands available for the cli with `faas-cli --help`.

Test the `faas-cli`

Open a Terminal or Git Bash window and type in:

```
$ faas-cli help
$ faas-cli version
```

Later in the lab, after setting up OpenFaaS we will run `faas-cli login` to save the password for our OpenFaaS gateway.

## Setup a Kubernetes cluster

You can follow the labs whilst using Kubernetes, but you may need to make some small changes along the way. The service address for the gateway changes from `http://gateway:8080` to `http://gateway.openfaas:8080`. As far as possible these differences have been documented and alternatives are provided in each lab.

### Create a local cluster on your laptop

Depending on the option you may also need to install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

#### _Docker for Mac_

* [Install Docker for Mac](https://docs.docker.com/v17.12/docker-for-mac/install/)
> Note that Kubernetes is only available in Docker for Mac 17.12 CE and higher

#### _With Minikube_

* To install Minikube download the proper installer from [latest release](https://github.com/kubernetes/minikube/releases) depending on your platform.
* [Install Helm client](https://docs.helm.sh/using_helm/#installing-the-helm-client)

* Now run Minikube with

```
$ minikube start
```

The minikube VM is exposed to the host system via a host-only IP address. Check this IP with `minikube ip`.
This is the IP you will later use for the gateway URL.

### Create a remote cluster on the cloud

You can create a remote cluster in the cloud and enjoy the same experience as if you were developing locally whilst saving on RAM/CPU and battery. The costs for running a cluster for 1-2 days is minimal.

#### _Run on DigitalOcean's Kubernetes Service_

You can use free credits to create a cluster through DigitalOcean's UI.

The DigitalOcean dashboard will then guide you through how to configure your `kubectl` and `KUBECONFIG` file for use in the labs.

* [Claim your free credits - $100 in credit over 60 days](https://m.do.co/c/8d4e75e9886f)

      Even if you have already claimed free credit, the running costs for a 2-3 node cluster for 24-48 hours is negligible.

* Click on *Kubernetes* on the left panel of the dashboard and then click "Enable Limited Access"

* Once logged in, click the *Kubernetes* menu item and create a Cluster.

      It is recommended to use the latest Kubernetes version available and the to select your nearest Datacenter region to minimize latency.

* Under "Add node pool(s)"

      Use 2x 4GB / 2vCPU
      (More can be added at a later date.)

* Download the [doctl](https://github.com/digitalocean/doctl#installing-doctl) CLI

* Create an API Key in your DigitalOcean dashboard

* Authenticate the CLI

```sh
$ doctl auth init
```

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

Find the cluster name with `kubectx`, if it's not highlighted type in `kubectx <context-name>`.

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

## Configure a registry - The Docker Hub

Sign up for a Docker Hub account. The [Docker Hub](https://hub.docker.com) allows you to publish your Docker images on the Internet for use on multi-node clusters or to share with the wider community. We will be using the Docker Hub to publish our functions during the workshop.

You can sign up here: [Docker Hub](https://hub.docker.com)

Open a Terminal or Git Bash window and log into the Docker Hub using the username you signed up for above.

```
$ docker login
```

> Note: Tip from community - if you get an error while trying to run this command on a Windows machine, then click on the Docker for Windows icon in the taskbar and log into Docker there instead "Sign in / Create Docker ID".

## Deploy OpenFaaS

The instructions for deploying OpenFaaS change from time to time as we strive to make this even easier.

Deploy OpenFaaS to Kubernetes using the instructions for Helm:

* Install helm (required step)


### Install the helm CLI/client

Instructions for latest Helm install

* On Linux and Mac/Darwin:

```sh
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
```

* Or via Homebrew on Mac:

```sh
brew install kubernetes-helm
```
      
On Windows [download the helm.exe file](https://helm.sh) and place it in $PATH or /usr/bin/.

### Install tiller

* Create RBAC permissions for tiller

```sh
kubectl -n kube-system create sa tiller \
  && kubectl create clusterrolebinding tiller \
  --clusterrole cluster-admin \
  --serviceaccount=kube-system:tiller
```

* Install the server-side Tiller component on your cluster

```sh
helm init --skip-refresh --upgrade --service-account tiller
```

### Install OpenFaaS with helm

* Install the OpenFaaS helm chart

We first create two namespaces `openfaas` and `openfaas-fn`:

```sh
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
```

Now add the helm chart repo for the project:

```sh
helm repo add openfaas https://openfaas.github.io/faas-netes/
```

Create a password for your OpenFaaS gateway:

```sh
# generate a random password
PASSWORD=$(head -c 12 /dev/urandom | shasum| cut -d' ' -f1)

kubectl -n openfaas create secret generic basic-auth \
--from-literal=basic-auth-user=admin \
--from-literal=basic-auth-password="$PASSWORD"

echo $PASSWORD > gateway-password.txt
```

>Note: If you get any issues with `helm upgrade` then you can reset it with `helm delete --purge openfaas`

### A) For local clusters

If you're running on a local cluster run the following:

```sh
helm repo update \
 && helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set basic_auth=true \
    --set functionNamespace=openfaas-fn
```

### B) For remote clusters

If you're running on a remote cluster run the following which will also expose a LoadBalancer with a public IP so that you can access it easily from your own laptop.

```sh
helm repo update \
 && helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set basic_auth=true \
    --set serviceType=LoadBalancer \
    --set functionNamespace=openfaas-fn
```


### Determine your Gateway URL

Depending on your installation method and Kubernetes distribution the Gateway URL may vary as will how you access it from your laptop during the workshop.

#### NodePort (local Kubernetes, excluding KinD)

The default installation for OpenFaaS exposes the gateway through a Kubernetes Service of type `NodePort`. The gateway address will generally be: `http://IP_ADDRESS:31112/`

The default for Docker for Mac would be `http://127.0.0.1:31112`

#### LoadBalancer (remote Kubernetes, or KinD)

If you're using a remote cluster or KinD then you can either use a LoadBalancer or run a command to port-forward the gateway to your local computer over the internet.

* A) Get the LoadBalancer address

It may take a couple of minutes for the `EXTERNAL-IP` address to become available, it will remain `<pending>` during that time.

```sh
kubectl get svc -o wide gateway-external -n openfaas
```

* B) Or start port-forwarding:

```sh
kubectl port-forward svc/gateway -n openfaas 8080:8080
```

Now set the `OPENFAAS_URL` variable to link to the proper IP:
```bash
export OPENFAAS_URL=http://IP_ADDRESS:8080
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

If you run into any problems, please consult the [helm chart README](https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/README.md).

### Login to the OpenFaaS Gateway

If you are running on a remote cluster and deployed openfaas with `basic_auth=true`, then you need to log in to access openfaas gateway. 

If you are accessing the gateway in the browser then it will prompt you for username and password. Username will be `admin` and password will be the value of environment variable `PASSWORD`

To access openfaas gateway from openfaas CLI, you need to log in using `faas-cli login` command.

Log in with the CLI and check connectivity:

```
echo -n $PASSWORD | faas-cli login -g $OPENFAAS_URL -u admin --password-stdin
```

### Permanently save your OpenFaaS URL

Edit `~/.bashrc` or `~/.bash_profile` - create the file if it doesn't exist.

Now add the following - changing the URL as per the one you saw above.

```
export OPENFAAS_URL=http://
```

This URL will now be saved for each new terminal window that you open.

Now move onto [Lab 2](./lab2.md)

