# 实验室 2--测试东西

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

在开始这个实验之前，创建一个新的文件夹。

```sh
$ mkdir -p lab2 \
   && cd lab2
```

## 使用 UI 门户

现在你可以测试一下 OpenFaaS 的用户界面了。

如果你已经设置了一个`$OPENFAAS_URL`，那么就可以得到这个 URL，然后点击它。

```sh
echo $OPENFAAS_URL
http://127.0.0.1:31112
```

如果你没有设置"$OPENFAAS_URL"，那么默认情况下是这样的。[http://127.0.0.1:8080](http://127.0.0.1:8080).

我们可以部署一些样本函数，然后用它们来测试一下。

```sh
faas-cli deploy -f https://raw.githubusercontent.com/openfaas/faas/master/stack.yml
```

![](../../screenshot/markdown_portal.png)

你可以在用户界面中试用它们，比如将 Markdown 代码转换为 HTML 的 Markdown 函数。

在*Request*字段中键入以下内容。

```sh
## The **OpenFaaS** _workshop_
```

现在点击*Invoke*，看到响应出现在屏幕的下半部分。

即。

```sh
<h2>The <strong>OpenFaaS</strong> <em>workshop</em></h2>
```

你将看到以下字段显示。

- 状态 - 该函数是否准备好运行。在状态显示准备好之前，你将不能从用户界面调用该函数。
- Replicas - 在集群中运行的函数的副本数量
- 镜像 - 发布在 Docker Hub 或 Docker 资源库中的 Docker 图像名称和版本
- 调用次数 - 这显示了该函数被调用的次数，每 5 秒更新一次

点击*Invoke*若干次，看到*Invocation count*的增加。

## 通过函数库进行部署

你可以从 OpenFaaS 商店中部署一个函数。该商店是一个由社区维护的免费函数集合。

- 点击 部署新的函数
- 点击 from store

- 点击 _Figlet_ 或在搜索栏中输入 _figlet_ ，然后点击 _Deploy_ 。

Figlet 函数现在将出现在你左边的函数列表中。给它一点时间从 Docker Hub 下载，然后输入一些文本，像我们对 Markdown 函数所做的那样，点击 Invoke。

你会看到一个 ASCII 码的标志，像这样生成。

```sh
 _ ___ ___ _ __
/ |/ _ \ / _ (_)/ /
| | | | | | | |/ /
| | |_| | |_| / /_
|_|\___/ \___/_/(_)
```

## 了解 CLI 的情况

你现在可以测试一下 CLI 了，但首先要注意一下备用网关的 URL。

如果你的*网关没有*部署在<http://127.0.0.1:8080>，那么你将需要指定替代位置。有几种方法来实现这一点。

1. 设置环境变量`OPENFAAS_URL`，`faas-cli`将指向当前 shell 会话中的那个端点。例如：`export OPENFAAS_URL http://openfaas.endpoint.com:8080`。如果你是按照 Kubernetes 的指示，这已经在[Lab 1](./lab1.md)中设置好了。
2. 用 `g`或`--gateway`标志在线指定正确的端点： `faas deploy --gateway http://openfaas.endpoint.com:8080`。
3. 在你的部署 YAML 文件中，改变`gateway:`对象在`provider:`下指定的值。

### 列出已部署的函数

这将显示这些函数，你有多少个副本和调用次数。

```sh
faas-cli list
```

你应该看到*markdown*函数是 `markdown`，*figlet*函数也被列出来了，还有你调用了多少次。

现在试试使用 verbose 标志

```sh
faas-cli list --verbose
```

或

```sh
faas-cli list -v
```

现在你可以看到 Docker 镜像以及函数的名称。

### 调用一个函数

从你在`faas-cli list`上看到的函数中挑选一个，比如`markdown`。

```sh
faas-cli invoke markdown
```

现在你会被要求输入一些文本。完成后点击 Control + D。

或者你可以使用一个命令，如`echo`或`curl`作为`invoke`命令的输入，该命令通过使用管道工作。

```sh
$ echo "# Hi" | faas-cli invoke markdown

$ curl -sLS https://raw.githubusercontent.com/openfaas/faas/master/README.md\。
  | faas-cli invoke markdown
```

## 监测仪表板

OpenFaaS 使用 Prometheus 自动跟踪你的函数的指标。这些指标可以通过免费的开源工具变成一个有用的仪表盘，比如[Grafana](https://grafana.com)。

在 OpenFaaS Kubernetes 命名空间运行 Grafana。

```sh
kubectl -n openfaas run \
--image=stefanprodan/faas-grafana:4.6.3 \
--port=3000 \
grafana
```

用 NodePort 暴露 Grafana。

```sh
kubectl -n openfaas expose pod grafana \
--type=NodePort \
--name=grafana
```

找到 Grafana 节点的端口地址。

```sh
GRAFANA_PORT=$(kubectl -n openfaas get svc grafana -o jsonpath="{.spec.ports[0].nodePort}")
GRAFANA_URL=http://IP_ADDRESS:$GRAFANA_PORT/dashboard/db/openfaas
```

其中`IP_ADDRESS`是你在 Kubernetes 的对应 IP。

或者你可以运行这个端口转发命令，以便能够在`http://127.0.0.1:3000`上访问 Grafana。

```sh
kubectl port-forward pod/grafana 3000:3000 -n openfaas
```

如果你使用的是 Kubernetes 1.17 或更早的版本，请使用`deploy/grafana`而不是上面命令中的`pod/`。

服务创建后，在浏览器中打开 Grafana，用用户名`admin`密码`admin`登录，并导航到预先制作的 OpenFaaS 仪表板`$GRAFANA_URL`。

<a href="https://camo.githubusercontent.com/24915ac87ecf8a31285f273846e7a5ffe82eeceb/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f4339636145364358554141585f36342e6a70673a6c61726765"><img src="https://camo.githubusercontent.com/24915ac87ecf8a31285f273846e7a5ffe82eeceb/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f4339636145364358554141585f36342e6a70673a6c61726765" width="600px" /></a>

_图：使用 Grafana 的 OpenFaaS 仪表板的例子_。

现在转到[实验室 3](./lab3.md)
