# Lab 1 - 为 OpenFaaS 做准备

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px">

OpenFaaS 需要一个[Kubernetes](https://kubernetes.io)集群来运行。你可以使用一个单节点集群或多节点集群，不管是在你的笔记本电脑上还是在云端。

任何 OpenFaaS 函数的基本原件都是一个 Docker 镜像，它是使用`faas-cli`工具链构建的。

## 前提条件

让我们来安装 Docker、OpenFaaS CLI 以及设置 Kubernetes。

### Docker

适用于 Mac

- [Docker CE for Mac Edge Edition](https://store.docker.com/editions/community/docker-ce-desktop-mac)

适用于 Windows

- 仅使用 Windows 10 Pro 或企业版
- 安装[Docker CE for Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows)

> 请确保通过使用 Windows 任务栏通知区的 Docker 菜单来使用**Linux**容器的 Docker 守护程序。

- 安装[Git Bash](https://git-scm.com/downloads)

当你安装 git bash 时，选择以下选项：`install UNIX commands`和`use true-type font`。

> 注意：请在所有步骤中使用*Git Bash*：不要试图使用*PowerShell*、*WSL*或*Bash for Windows*。

Linux - Ubuntu 或 Debian

- Docker CE for Linux

> 你可以从[Docker Store]（<https://store.docker.com>）安装 Docker CE。

注意：作为最后的手段，如果你有一台不兼容的 PC，你可以在<https://labs.play-with-docker.com/>上面体验。

### OpenFaaS CLI

你可以使用官方的 bash 脚本来安装 OpenFaaS CLI，`brew`也可以使用，但可能会落后一到两个版本。

在 MacOS 或 Linux 下，在终端运行以下程序。

```sh
# MacOS users may need to run "bash" first if this command fails
$ curl -sLSf https://cli.openfaas.com | sudo sh
```

对于 Windows，在*Git Bash*中运行这个。

```sh
curl -sLSf https://cli.openfaas.com | sh
```

> 如果你遇到任何问题，你可以从[releases page](https://github.com/openfaas/faas-cli/releases)手动下载最新的`faas-cli.exe`。你可以把它放在本地目录或`C:\Windows\`路径中，这样它就可以从命令提示符中获得。

我们将使用`faas-cli`来搭建新的函数，构建、部署和调用函数。你可以通过`faas-cli --help`找到 cli 的可用命令。

测试 `faas-cli`：打开一个终端或 Git Bash 窗口，键入

```sh
faas-cli help
faas-cli version
```

## 配置 Docker Hub

注册一个 Docker Hub 账户：[Docker Hub](https://hub.docker.com)允许你在互联网上发布你的 Docker 镜像，以便在多节点集群上使用或与更广泛的社区分享。我们将在研讨会期间使用 Docker Hub 来发布我们的函数。

你可以在这里注册：[Docker Hub](https://hub.docker.com)

打开一个终端或 Git Bash 窗口，用你上面注册的用户名登录 Docker Hub。

```sh
docker login
```

> 注意：来自社区的提示--如果你在 Windows 机器上试图运行这个命令时遇到错误，那么点击任务栏中的 Docker for Windows 图标，在那里登录 Docker，而不是 `登录/创建 Docker ID`。

- 为新镜像设置你的 OpenFaaS 前缀

OpenFaaS 镜像存储在 Docker 注册表或 Docker Hub 中，我们可以设置一个环境变量，使你的用户名自动添加到你创建的新函数中。这将在研讨会过程中为你节省一些时间。

编辑`~/.bashrc`或`~/.bash_profile`--如果该文件不存在，则创建它。

现在添加以下内容--按照你上面看到的 URL 进行修改。

```sh
export OPENFAAS_PREFIX="" # Populate with your Docker Hub username
```

### 设置一个单节点集群

实验室使用 Kubernetes，Swarm 已经不再被 OpenFaaS 社区支持。有些实验室可以用于 faasd，但你可能需要改变命令，而且当使用 faasd 的时候，我们不提供对该实验室的支持。

- Kubernetes。[Lab 1b](./lab1b.md)
