# Lab 1 - 用 Kubernetes 设置 OpenFaaS

<img src="https://kubernetes.io/images/kubernetes-horizontal-color.png" width="500px"> </img>

## 安装最新的 `kubectl`

使用下面的说明或[官方文档](https://kubernetes.io/docs/tasks/tools/install-kubectl/)为你的操作系统安装`kubectl`。

- Linux

```sh
export VER=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO https://storage.googleapis.com/kubernetes-release/release/$VER/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin/
```

- MacOS

```sh
export VER=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO https://storage.googleapis.com/kubernetes-release/release/$VER/bin/darwin/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin/
```

- Windows

```sh
export VER=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO https://storage.googleapis.com/kubernetes-release/release/$VER/bin/windows/amd64/kubectl.exe
chmod +x kubectl.exe
mkdir -p $HOME/bin/
mv kubectl $HOME/bin/
```

## 设置一个 Kubernetes 集群

你可以在使用 Kubernetes 的同时按照实验进行操作，但你可能需要沿途做一些小改动。网关的服务地址从`http://gateway:8080`改为`http://gateway.openfaas:8080`。这些差异已经尽可能地被记录下来，每个实验室都提供了替代方案。

### 在你的笔记本电脑上创建一个本地集群

#### _k3s 使用 k3d_

如果你的电脑上有 Docker，那么你可以使用 Rancher 实验室托管的`k3d`工具。它安装了一个轻量级的 Kubernetes 版本，叫做`k3s`，并在 Docker 容器中运行，这意味着它可以在任何有 Docker 的电脑上运行。

- [安装 k3d](https://github.com/rancher/k3d)

- 启动一个集群

1. `k3d cluster create CLUSTER_NAME`创建一个新的单节点集群（=1 个运行 k3s 的容器+1 个负载均衡器容器）
2. 2.kubectl 的上下文会自动更新，你可以用`kubectl config get-contexts`来检查。
3. 执行一些命令，如`kubectl get pods --all-namespaces`。
   如果你想删除默认集群`k3d cluster delete CLUSTER_NAME`。

#### _Docker for Mac_

- [安装 Docker for Mac](https://docs.docker.com/v17.12/docker-for-mac/install/)

> 请注意，Kubernetes 仅在 Docker for Mac 17.12 CE 及以上版本中可用。

#### _使用 Minikube_

- 要安装 Minikube，请根据你的平台从[最新版本](https://github.com/kubernetes/minikube/releases)下载适当的安装程序。

- 现在运行 Minikube

```sh
minikube start
```

minikube 虚拟机通过一个仅限主机的 IP 地址暴露给主机系统。用`minikube ip`检查这个 IP。
这是你以后将用于网关 URL 的 IP。

> 注意：Minikube 还需要一个 Hypervisor，如 VirtualBox 或 Hyperkit（在 MacOS 上）。按照 minikube 的说明和文件

### 在云上创建一个远程集群

你可以在云端创建一个远程集群，享受与本地开发一样的体验，同时节省 RAM/CPU 和电池。运行一个集群 1-2 天的费用是最低的。

#### _在 DigitalOcean 的 Kubernetes 服务上运行_

你可以使用免费点数通过 DigitalOcean 的用户界面创建一个集群。

然后 DigitalOcean 的仪表板将指导你如何配置你的`kubectl`和`KUBECONFIG`文件，以便在实验室中使用。

- [申请你的免费点数--30 天内有 50 美元的点数。](https://m.do.co/c/8d4e75e9886f)

即使你已经申请了免费学分，一个 2-3 个节点的集群 24-48 小时的运行费用也是可以忽略不计的。

*点击仪表板左侧面板上的 Kubernetes*，然后点击 `启用有限访问`

*一旦登录，点击 Kubernetes*菜单项并创建一个集群。

建议使用最新的 Kubernetes 版本，并选择离你最近的数据中心区域，以尽量减少延时。

- 在 `添加节点池`下

使用 2 个 4GB / 2vCPU

> 注意：如果需要，你可以在以后添加更多的容量

- 下载[doctl](https://github.com/digitalocean/doctl#installing-doctl)CLI 并把它放在你的路径中。

- 在您的 DigitalOcean 仪表板上创建一个[API 密钥](https://cloud.digitalocean.com/account/api/tokens/new)

追踪您的 API 密钥（将其复制到剪贴板）。

- 认证 CLI

```sh
doctl auth init
```

粘贴你的 API 密钥

- 现在获得集群的名称。

```sh
$ doctl k8s cluster list
GUID workshop-lon1 nyc1 1.13.5-do.1 provisioning workshop-lon1-1
```

- 保存一个配置文件，使`kubectl`指向新集群。

```sh
doctl k8s cluster kubeconfig save workshop-lon1
```

现在你需要切换你的 Kubernetes 上下文以指向新的集群。

用`kubectl config get-contexts`找到集群名称，如果它没有突出显示，则输入`kubectl config set-context <context-name>`。

#### _在 GKE（谷歌 Kubernetes 引擎）上运行_

登录到谷歌云，创建一个项目，并为其启用计费。如果你没有账户，你可以[在这里](https://cloud.google.com/free/)注册，获得免费点数。

安装[Google Cloud SDK](https://cloud.google.com/sdk/docs) - 这将使`gcloud`和`kubectl`命令可用。
对于 Windows，请按照[文档](https://cloud.google.com/sdk/docs/#windows)中的说明。

安装 gcloud 命令行工具后，用`gcloud init`配置你的项目，并设置默认项目、计算区域和区域（用你自己的项目替换`PROJECT_ID`）。

```sh
gcloud config set project PROJECT_ID
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a
```

启用 Kubernetes 服务。

```sh
gcloud services enable container.googleapis.com
```

安装 kubectl。

```sh
gcloud components install kubectl
```

创建一个 Kubernetes 集群。

```sh
$ gcloud container clusters create openfaas \
--zone=us-central1-a \
--num-nodes=1 \
--machine-type=n1-standard-2 \
--disk-size=30 \
--no-enable-cloud-logging
```

为 `kubectl`设置凭证。

```sh
gcloud container clusters get-credentials openfaas
```

创建一个集群管理员角色绑定:

```sh
$ kubectl create clusterrolebinding "cluster-admin-$(whoami)" \
--clusterrole=cluster-admin \
--user="$(gcloud config get-value core/account)"
```

现在验证`kubectl`已经配置到 GKE 集群。

```plain
$ kubectl get nodes
NAME                                   STATUS    ROLES     AGE       VERSION
gke-name-default-pool-eceef152-qjmt   Ready     <none>    1h        v1.10.7-gke.2
```

## 部署 OpenFaaS

部署 OpenFaaS 的说明会时常改变，因为我们努力使其更加简单。

### 安装 OpenFaaS

有三种方式来安装 OpenFaaS，你可以选择对你和你的团队有意义的方式。在这个研讨会上，我们将使用官方的安装程序`arkade`。

- `arkade应用安装` - arkade 使用其官方舵手图安装 OpenFaaS。它还可以通过用户友好的 CLI 提供其他软件，如`cert-manager`和`nginx-ingress`。这是最简单和最快速的方式来启动和运行。

- 舵手图 - 理智的默认值，易于通过 YAML 或 CLI 标志进行配置。安全选项，如 `Helm 模板`或 `Helm 3`，也适用于那些在限制性环境中工作的人。

- 普通 YAML 文件 - 硬编码的设置/值。像 Kustomize 这样的工具可以提供自定义设置

#### 用`arkade`安装

- 获取 arkade

对于 MacOS / Linux:

```sh
# MacOS users may need to run "bash" first if this command fails
curl -SLsf https://dl.get-arkade.dev/ | sudo sh
```

对于 Windows。

```sh
curl -SLsf https://dl.get-arkade.dev/ | sh
```

- 安装 OpenFaaS 应用程序

如果你使用的是提供 LoadBalancers 的管理云 Kubernetes 服务，那么运行以下内容。

```sh
arkade install openfaas --load-balancer
```

> 注意：`--load-balancer`标志的默认值是`false`，所以通过该标志，安装将向你的云提供商请求一个。

如果你使用的是本地 Kubernetes 集群或虚拟机，那么请运行。

```sh
arkade install openfaas
```

在后面的实验室中，我们将向你展示如何使用 Kubernetes Ingress 设置一个带有 TLS 的自定义域。

#### 或者用 helm 安装（高级）

如果你愿意，你可以使用[helm chart](https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/README.md)的说明来安装 OpenFaaS。

### 登录你的 OpenFaaS 网关

- 检查网关是否准备好了

```sh
kubectl rollout status -n openfaas deploy/gateway
```

如果你使用你的笔记本电脑，虚拟机，或任何其他类型的 Kubernetes 分布，请运行以下内容。

```sh
kubectl port-forward svc/gateway -n openfaas 8080:8080
```

这个命令将打开一个从 Kubernetes 集群到本地计算机的隧道，这样你就可以访问 OpenFaaS 网关。还有其他方法可以访问 OpenFaaS，但这已经超出了本次研讨会的范围。

你的网关 URL 是：`http://127.0.0.1:8080`

如果你使用的是管理云 Kubernetes 服务，那么从下面的命令中的`EXTERNAL-IP`字段中获取 LoadBalancer 的 IP 地址或 DNS 条目。

```sh
kubectl get svc -o wide gateway-external -n openfaas
```

你的 URL 将是上面的 IP 或 DNS 条目，端口为`8080`。

- 登录。

```sh
export OPENFAAS_URL="" # Populate as above

# This command retrieves your password
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)

# This command logs in and saves a file to ~/.openfaas/config.yml
echo -n $PASSWORD | faas-cli login --username admin --password-stdin
```

- 检查`faas-cli list`是否工作。

```sh
faas-cli list
```

### 永久保存你的 OpenFaaS URL

编辑`~/.bashrc`或`~/.bash_profile`--如果该文件不存在，则创建它。

现在添加以下内容--按照你上面看到的 URL 进行修改。

```sh
export OPENFAAS_URL="" # populate as above
```

现在转到[实验室 2](lab2.md)
