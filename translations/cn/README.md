# openfaas-workshop

这是一个自定进度的研讨会，学习如何使用 OpenFaaS 构建、部署和运行无服务器函数。

![](https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png)

在这个研讨会中，你将首先把 OpenFaaS 部署到你的笔记本电脑或使用 Docker for Mac 或 Windows 的远程集群。然后你将对 OpenFaaS 的用户界面、CLI 和函数商店进行测试。在用 Python 构建、部署和调用你自己的无服务器函数之后，你将继续学习以下内容：用 pip 管理依赖关系，通过安全secret处理 API 令牌，用 Prometheus 监控函数，异步调用函数以及将函数连接起来创建应用程序。实验的高潮是让你创建自己的 GitHub 机器人，可以自动响应问题。同样的方法可以通过 IFTTT.com 连接到在线事件流--这将使你能够建立机器人、自动回复器以及与社交媒体和物联网设备的集成。

最后，实验室涵盖了更多的高级主题，并给出了进一步学习的建议。

**译文**

* [日本語](./translations/ja)
* [简体中文](./translations/cn)

## 免费学习，作为 GitHub 赞助商表示感谢

OpenFaaS 连同这些材料都是免费提供的，需要时间和精力来维护。

* 成为[OpenFaaS on GitHub](https://github.com/sponsor/openfaas)的赞助商。

## 要求

我们在[Lab 1](./lab1.md)中讲解了如何安装这些需求。请在参加讲师指导的研讨会之前做[Lab 1](./lab1.md)。

* 函数将用 Python 语言编写，所以有编程或脚本经验者优先。
* 安装推荐的代码编辑器/IDE [VSCode](https://code.visualstudio.com/download)
* 对于 Windows，安装[Git Bash](https://git-scm.com/downloads)
* 首选的操作系统。MacOS, Windows 10 Pro/Enterprise, Ubuntu Linux

Docker。

* Docker CE for [Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)/[Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows) **边缘版**。
* Docker CE for Linux

> 注意：作为最后的手段，如果你有一台不兼容的 PC，你可以在<https://labs.play-with-docker.com/> 上运行该研讨会。

## 教员指导的研讨会

如果你正在参加一个由教师指导的研讨会，那么我们将分享一个链接，以加入 OpenFaaS Slack 社区。使用研讨会的指定频道来讨论评论、问题和建议。

## 挑选你的路线

在实验室 1 中，你将选择你的路线，然后在整个实验室中注意你所需要的特殊命令。

### Kubernetes

你也可以使用 OpenFaaS 学习 Kubernetes 上的 Serverless。

OpenFaaS 社区的建议是，你在生产中运行 Kubernetes，但你的所有知识都是可以转移的，函数也不必重新构建。

## [Lab 1 - Prepare for OpenFaaS](./lab1.md)

* 安装前提条件
* 用 Kubernetes 建立一个单节点集群
* Docker Hub 账户
* OpenFaaS CLI
* 部署 OpenFaaS

## [Lab 2 - Test things out](./lab2.md)

* 使用 UI 门户
* 通过函数商店进行部署
* 了解 CLI 的情况
* 用 Prometheus 查找指标

## [Lab 3 - Introduction to Functions](./lab3.md)

* 架构或生成一个新的函数
* 建立 astronaut-finder 函数
* 用`pip`添加依赖性
* 故障排除：找到容器的日志
* 故障排除：用`write_debug`进行粗略输出
* 使用自定义和第三方语言模板
* 使用模板商店发现社区模板

## [Lab 4 - Go deeper with functions](./lab4.md)

* [通过环境变量注入配置](lab4.md#inject-configuration-through-environmental-variables)
  * 在部署时使用 yaml
  * 动态地使用 HTTP 上下文--查询字符串/头信息等
* 安全性：只读的文件系统
* [利用日志](lab4.md#making-use-of-logging)
* [创建工作流](lab4.md#creat-workflows)
  * 在客户端串联函数
  * 从另一个函数中调用一个函数

## [Lab 5 - Create a GitHub bot](./lab5.md)

> 建立 `issue-bot`--GitHub 问题的自动回复者

* 获得一个 GitHub 账户
* 用 ngrok 建立一个隧道
* 创建一个 webhook 接收器`issue-bot`。
* 接收来自 GitHub 的 webhooks
* 部署 SentimentAnalysis 函数
* 通过 GitHub 的 API 应用标签
* 完成函数

## [Lab 6 - HTML for your functions](./lab6.md)

* 从一个函数生成并返回基本的 HTML
* 从磁盘读取并返回一个静态 HTML 文件
* 与其他函数协作

## [Lab 7 - Asynchronous Functions](./lab7.md)

* 同步地与异步地调用一个函数
* 查看队列工作者的日志

* 在 requestbin 和 ngrok 中使用`X-Callback-Url`。

## [Lab 8 - Advanced Feature - Timeouts](./lab8.md)

* 用`read_timeout`调整超时时间
* 适配长时间运行函数

## [Lab 9 - Advanced Feature - Auto-scaling](./lab9.md)

* 查看自动缩放的操作
  * 关于最小和最大副本的一些见解
  * 发现并访问本地 Prometheus
  * 执行和普罗米修斯查询
  * 使用 curl 调用一个函数
  * 观察自动缩放的启动

## [Lab 10 - Advanced Feature - Secrets](./lab10.md)

* 调整 issue-bot 以使用一个secret
  * 用 faas-cli 创建一个 Kubernetes secret
  * 在函数中访问secret

## [Lab 11 - Advanced feature - Trust with HMAC](./lab11.md)

* 使用 HMAC 对函数应用信任

你可以从第一个实验室[Lab 1](lab1.md)开始。

## 拆解/清理

你可以找到如何停止和删除 OpenFaaS[这里](https://docs.openfaas.com/deployment/troubleshooting/#uninstall-openfaas)

## 接下来的步骤

如果你在一个教师指导的研讨会上，并且已经完成了实验，你可能想回到实验室，编辑/修改代码和值，或者进行一些你自己的实验。

以下是一些后续任务/主题的想法。

### OpenFaaS 云

试试 OpenFaaS 的多用户管理体验--在社区集群上，或者通过托管你自己的 OpenFaaS 云。

* [Docs: OpenFaaS Cloud](https://docs.openfaas.com/openfaas-cloud/intro/)

### TLS

* [用 Kubernetes Ingress 在你的网关上启用 HTTPS](https://docs.openfaas.com/reference/ssl/kubernetes-with-cert-manager/)

### CI/CD

设置 Jenkins、Google Cloud Build 或 GitLab，使用 OpenFaaS CLI 构建和部署你自己的函数。

* [CI/CD 介绍](https://docs.openfaas.com/reference/cicd/intro/)

### 存储/数据库

* [用 Minio 尝试开源对象存储](https://blog.alexellis.io/openfaas-storage-for-your-functions/)

* [尝试用 Mongo 存储数据的 OpenFaaS](https://blog.alexellis.io/serverless-databases-with-openfaas-and-mongo/)

### 仪器仪表/监控

* [探索 Prometheus 中可用的指标](https://docs.openfaas.com/architecture/metrics/#monitoring-functions)

### 其他博文和教程

* [OpenFaaS 博客上的教程](https://www.openfaas.com/blog/)

* [社区博客文章](https://github.com/openfaas/faas/blob/master/community.md)

### 附录

[附录](./appendix.md)包含一些额外的内容。

## Acknowledgements

感谢@iyovcheva, @BurtonR, @johnmccabe, @laurentgrangeau, @stefanprodan, @kenfdev, @templum & @rgee0 对实验室的贡献、测试和翻译。
