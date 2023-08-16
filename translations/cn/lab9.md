# Lab 9 - 高级函数 - 自动缩放

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

## 自动缩放函数的应用

正如[文档](http://docs.openfaas.com/architecture/autoscaling/)中描述的那样，OpenFaaS 带有自动扩展函数。在这个实验室中，我们将看看自动扩展是如何运作的。

### 前提条件

* 在完成了[Lab 1](./lab1.md)中对 OpenFaaS 的设置后，你将拥有触发自动扩展所需的一切。

* 多个工具可以用来创建足够的流量来触发自动扩展 - 在这个例子中，`curl'将被使用，因为它很容易在 Mac 和 Linux 上使用，并在 Windows 上与 Git Bash 打包。

### 自动扩展的背景

开箱即用的 OpenFaaS 是这样配置的，它将根据 Prometheus 测量的 `每秒请求`指标进行自动扩展。 这个指标是在流量通过 API 网关的时候捕获的。如果超过了定义的 `每秒请求`的阈值，AlertManager 就会启动。这个阈值应该被重新配置为适合生产使用的水平，因为在这个例子中，为了演示，它被设置为一个低值。

> 在[文档网站](http://docs.openfaas.com/architecture/autoscaling/)中找到更多关于自动缩放的信息。

每次警报被 AlertManager 触发时，API 网关将把你的函数的一定数量的副本添加到集群中。OpenFaaS 有两个配置选项，允许指定副本的起始/最低数量，也允许停止副本的最大数量。

你可以通过设置`com.openfaas.scale.min`来控制函数的最小副本量，目前默认值为`1`。

你可以通过设置`com.openfaas.scale.max`来控制一个函数可以产生的最大副本量，目前默认值是`20`。

> 注意: 如果你把`com.openfaas.scale.min`和`com.openfaas.scale.max`设置成相同的值，你就会禁用自动缩放函数。

### 查看 Prometheus

你需要运行这个端口转发命令，以便能够在`http://127.0.0.1:9090`访问 Prometheus。
```plain
$ kubectl port-forward deployment/prometheus 9090:9090 -n openfaas
```

现在添加一个所有成功调用部署的函数的图。我们可以通过执行`rate( gateway_function_invocation_total{code="200"} [20s])`作为查询来实现。导致一个看起来像这样的页面。

 ![](../../screenshot/prometheus_graph.png)

 继续打开一个新的标签，在其中使用`http://127.0.0.1:9090/alerts`导航到警报部分。在这个页面上，你以后可以看到什么时候超过了 `每秒请求` 的阈值。

 ![](../../screenshot/prometheus_alerts.png)

### 触发缩放的 Go 函数

首先是 Alex Ellis 的 `echo-fn`函数。

```bash
$ git clone https://github.com/alexellis/echo-fn \
 && cd echo-fn \
 && faas-cli template store pull golang-http \
 && faas-cli deploy \
  --label com.openfaas.scale.max=10 \
  --label com.openfaas.scale.min=1
```

现在检查用户界面，看什么时候 `go-echo`函数从 `不准备`变成 `准备`。你也可以用`faas-cli describe go-echo`来检查。

使用这个脚本反复调用 `go-echo` 函数，直到你看到副本数从 1 变成 5，以此类推。你可以在 Prometheus 中通过添加`gateway_service_count'的图表或在选择该函数的情况下查看 API 网关来监控这个值。

```bash
$ for i in {0..10000};
do
   echo -n "Post $i" | faas-cli invoke go-echo && echo;
done;
```

> 注意：如果你在 Kubernetes 上运行，使用`$OPENFAAS_URL`而不是`http://127.0.0.1:8080`。

### 监控警报

现在你应该可以看到，在之前创建的图表中，`go-echo`函数的调用量有所增加。移动到你打开警报页面的标签。一段时间后，你应该开始看到 `APIHighInvocationRate`的状态（和颜色）变为 "待定"，然后再次变为 "发射"。你也可以使用`$ faas-cli list`或通过[ui](http://127.0.0.1:8080)看到自动缩放的情况。

 ![](../../screenshot/prometheus_firing.png)

现在你可以使用`$ docker service ps go-echo`来验证`go-echo`的新副本是否已经启动。

现在停止 bash 脚本，你会看到副本的数量在几秒钟后回到 1 个副本。

### 疑难解答

如果你认为你的自动扩展没有被触发，那么请检查以下内容。

* 普罗米修斯中的警报页面 - 这应该是红色/粉色的，并显示 `FIRING` - 即在http://127.0.0.1:9090/alerts。
* 检查核心服务的日志，即网关、Prometheus / AlertManager。

为了获得核心服务的日志，运行`docker service ls`，然后`docker service logs <service-name>`。

### 负载测试(可选)

需要注意的是，在受控环境中应用科学方法和工具与在你自己的笔记本电脑上运行拒绝服务攻击是有区别的。你的笔记本电脑不适合做负载测试，因为一般来说，你是在 Windows 或 Mac 主机上的 Linux 虚拟机中运行 OpenFaaS，而这也是一个单节点。这并不代表生产部署。

请看[构建一个合适的性能测试](https://docs.openfaas.com/architecture/performance/)的文档。

如果`curl`没有为你的测试产生足够的流量，或者你想获得一些关于事情如何分解的统计数据，那么你可以试试`hey`工具。`hey`可以通过每秒的请求或给定的持续时间产生结构化的负载。

这里有一个在 1GHz 的 2016 年 12 英寸 MacBook 上运行的例子，带有 Docker Desktop。这是一台非常低功率的计算机，正如所描述的，不代表生产性能。

```bash
$ hey -z=30s -q 5 -c 2 -m POST -d=Test http://127.0.0.1:8080/function/go-echo
Summary:
  Total:        30.0203 secs
  Slowest:      0.0967 secs
  Fastest:      0.0057 secs
  Average:      0.0135 secs
  Requests/sec: 9.9932

  Total data:   1200 bytes
  Size/request: 4 bytes

Response time histogram:
  0.006 [1]     |
  0.015 [244]   |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.024 [38]    |■■■■■■
  0.033 [10]    |■■
  0.042 [4]     |■
  0.051 [1]     |
  0.060 [0]     |
  0.069 [0]     |
  0.078 [0]     |
  0.088 [0]     |
  0.097 [2]     |


Latency distribution:
  10% in 0.0089 secs
  25% in 0.0101 secs
  50% in 0.0118 secs
  75% in 0.0139 secs
  90% in 0.0173 secs
  95% in 0.0265 secs
  99% in 0.0428 secs

Details (average, fastest, slowest):
  DNS+dialup:   0.0000 secs, 0.0057 secs, 0.0967 secs
  DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0000 secs
  req write:    0.0001 secs, 0.0000 secs, 0.0016 secs
  resp wait:    0.0131 secs, 0.0056 secs, 0.0936 secs
  resp read:    0.0001 secs, 0.0000 secs, 0.0013 secs

Status code distribution:
  [200] 300 responses
```

以上模拟了两个活跃的用户`-c`，每秒 5 个请求`-q`，持续时间`-z`为 30 秒。

要使用`hey`，你必须在本地计算机上安装 Golang。

也请参见。[hey on GitHub](https://github.com/rakyll/hey)

### 尝试从零开始扩展

如果你把你的函数规模缩小到 0 个副本，你仍然可以调用它。该调用将触发网关将函数缩放到一个非零值。

用下面的命令试试吧。

```plain
$ kubectl scale deployment --replicas=0 nodeinfo -n openfaas-fn
```

打开 OpenFaaS 用户界面，检查 nodeinfo 是否有 0 个副本，或者通过`kubectl get deployment nodeinfo -n openfaas-fn'。

现在调用该函数并检查它是否扩展到 1 个副本。

现在转到[Lab 10](lab10.md)。
