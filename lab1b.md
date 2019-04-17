# Lab 1 - Set-up OpenFaaS with Kubernetes

<img src="https://kubernetes.io/images/kubernetes-horizontal-color.png" width="500px"></img>

### Setup a single-node cluster

You can follow the labs whilst using Kubernetes, but you may need to make some small changes along the way. The service address for the gateway changes from `http://gateway:8080` to `http://gateway.openfaas:8080`. As far as possible these differences have been documented and alternatives are provided in each lab.

#### Create a local cluster on your laptop

Depending on the option you may also need to install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

##### _Docker for Mac_

* [Install Docker for Mac](https://docs.docker.com/v17.12/docker-for-mac/install/)
> Note that Kubernetes is only available in Docker for Mac 17.12 CE and higher

##### _With Minikube_

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

#### Create a remote cluster on the cloud

You can create a remote cluster in the cloud and enjoy the same experience as if you were developing locally whilst saving on RAM/CPU and battery. The costs for running a cluster for 1-2 days is minimal.

##### _Run on DigitalOcean's Kubernetes Service_

You can use free credits to create a cluster through DigitalOcean's UI.

The DigitalOcean dashboard will then guide you through how to configure your `kubectl` and `KUBECONFIG` file for use in the labs.

* [Claim your free credits - $100 in credit over 60 days](https://m.do.co/c/8d4e75e9886f)

> Note: Even if you have already claimed free credit, the running costs for a 2-3 node cluster for 24-48 hours is negligible.

Once logged in, click the *Kubernetes* menu item and create a Cluster.

It is recommended to use the latest Kubernetes version available and the to select your nearest Datacenter region to minimize latency.

Under "Add node pool(s)" chance the instance type to 4GB / 2vCPU and pick between 1 and 3 nodes. More can be added at a later date.

* Download the `doctl` CLI

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

##### _Run on GKE (Google Kubernetes Engine)_

* Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs) - this will make the `gcloud` and `kubectl` commands available.

For Windows follow the instructions from the [Documentation](https://cloud.google.com/sdk/docs/#windows)

*  Create a Kubernetes cluster using the Google Cloud Platform.

In the GCP console, go to *Kubernetes Engine* then *Clusters* and create new cluster.

* When the cluster has been created you can download your KUBECONFIG with the following steps.

(You can copy the command from the GCP console after clicking `Connect`):

```
$ gcloud container clusters get-credentials <cluster_name> --zone <cluster_zone> --project <project_name>
```

Now verify `kubectl` is configured to the GKE cluster:

```
$ kubectl get nodes
NAME                                   STATUS    ROLES     AGE       VERSION
gke-name-default-pool-eceef152-qjmt   Ready     <none>    1h        v1.10.7-gke.2
```

### Configure a registry - The Docker Hub

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

```sh
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

The instructions for deploying OpenFaaS change from time to time as we strive to make this even easier.

Deploy OpenFaaS to Kubernetes using the instructions for Helm:

* Install helm

You can install helm and tiller using [these instructions](https://github.com/openfaas/faas-netes/blob/master/HELM.md)

* Install the OpenFaaS helm chart

We first create two namespaces `openfaas` and `openfaas-fn`:

```sh
kubectl apply -f https://raw.githubusercontent.com/openfaas/faas-netes/master/namespaces.yml
```

Now add the helm chart repo for the project:

```sh
helm repo add openfaas https://openfaas.github.io/faas-netes/
```

If you're running on a local cluster run the following:

```sh
helm repo update \
 && helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set basic_auth=false \
    --set functionNamespace=openfaas-fn
```

If you're running on a remote cluster run the following:

```sh

# generate a random password
PASSWORD=$(head -c 12 /dev/urandom | shasum| cut -d' ' -f1)

kubectl -n openfaas create secret generic basic-auth \
--from-literal=basic-auth-user=admin \
--from-literal=basic-auth-password="$PASSWORD"

echo $PASSWORD > gateway-password.txt

helm repo update \
 && helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set basic_auth=true \
    --set serviceType=LoadBalancer
    --set functionNamespace=openfaas-fn
```

#### Determine your Gateway URL

Depending on your installation method and Kubernetes distribution the Gateway URL may vary as will how you access it from your laptop during the workshop.

#### NodePort (local Kubernetes, excluding KinD)

The default installation for OpenFaaS exposes the gateway through a Kubernetes Service of type `NodePort`. The gateway address will generally be: http://IP_ADDRESS:31112/

#### LoadBalancer (remote Kubernetes, or KinD)

If you're using a remote cluster or KinD then you can either use a LoadBalancer or run a command to port-forward the gateway to your local computer over the internet.

* A) Get the LoadBalancer address 

```sh
kubectl get svc -o wide gateway-external
```

* B) Or start port-forwarding:

```sh
kubectl port-forward svc/gateway -n openfaas 8080:8080
```

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

If you run into any problems, please consult the [helm chart README](https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/README.md).

Now move onto [Lab 2](./lab2.md)
