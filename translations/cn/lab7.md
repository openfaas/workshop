# 实验 7--异步函数

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

在开始这个实验之前，为你的文件创建一个新的文件夹。

```plain
$ mkdir -p lab7 \
   && cd lab7
```

## 同步与异步地调用一个函数

当你同步调用一个函数时，一个连接会通过网关连接到你的函数，并且在整个执行过程中保持开放。同步调用是*阻塞的，所以你应该看到你的客户端暂停，变得不活跃，直到该函数完成其任务。

* 网关使用的路由是。`/function/<function_name>`。
* 你必须等待，直到它完成
* 你在调用后得到结果
* 你知道它是通过还是失败

异步任务以类似的方式运行，但有一些区别。

* 网关使用不同的路由：`/async-function/<function_name>`。
* 客户端从网关得到一个立即的*202 接受*的响应。
* 该函数稍后使用一个队列工作器来调用
* 默认情况下，结果被丢弃

让我们试一试快速演示。

```plain
$ faas-cli new --lang dockerfile long-task --prefix="<your-docker-username-here>"
```

编辑`long-task/Dockerfile`并将 fprocess 改为`sleep 1`。

现在构建、部署并同步调用你的函数 10 次，像这样。

```plain
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
```

现在异步调用该函数 10 次。

```plain
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
```

你观察到了什么？第一个例子应该花了 10 秒，而第二个例子会在一秒或更短的时间内返回到你的提示。这项工作仍然需要 10x1 秒来完成，但现在要放在队列中延迟执行。

异步函数调用非常适用于那些可以推迟到以后执行的任务，或者你不需要客户端上的结果。

> 一个很好的例子是在接收 GitHub 的 webhooks 时--可能有一个最大的处理时间，GitHub 会允许你的连接保持开放，一个异步调用接受工作并立即返回。

## 查看队列工作者的日志

OpenFaaS 的默认栈使用 NATS 流来排队和延迟执行。你可以用以下命令查看日志。

```plain
kubectl logs deployment/queue-worker -n openfaas
```

## 使用一个`X-Callback-Url'与 requirebin

如果你需要一个异步调用的函数的结果，你有两个选择。

* 改变它的代码，用它的结果通知一个端点或消息系统

这个选项可能不是在所有情况下都适用，并且需要编写额外的代码。

* 利用回调的内置行为

内置的回调允许对一个函数的调用提供一个 URL，队列工作器将自动报告函数的成功或失败，以及结果。
一些额外的请求头被发送到回调，完整的列表见[回调请求头](https://docs.openfaas.com/reference/async/#callback-request-headers)

前往 requestbin 并创建一个新的 `bin` --这将是公共互联网上的一个 URL，可以接收你的函数的结果。

> 为了这个实验室的目的，一定要取消勾选 `私有` 复选框，这将使你不需要登录。

https://requestbin.com/

现在复制 "Bin URL "并将其粘贴在下面。

例如(`http://requestbin.com/r/1i7i1we1`)

```plain
$ echo -n "LaterIsBetter" | faas-cli invoke figlet --async --header "X-Callback-Url http://requestbin.com/r/1i7i1we1"
```

现在刷新 requestbin 站点上的页面，你将看到来自 `figlet` 的结果。


```plain
 _          _           ___     ____       _   _            
| |    __ _| |_ ___ _ _|_ _|___| __ )  ___| |_| |_ ___ _ __ 
| |   / _` | __/ _ \ '__| |/ __|  _ \ / _ \ __| __/ _ \ '__|
| |__| (_| | ||  __/ |  | |\__ \ |_) |  __/ |_| ||  __/ |   
|_____\__,_|\__\___|_| |___|___/____/ \___|\__|\__\___|_|   
                                                            
```

> 建议：也可以使用另一个函数作为 `X-Callback-Url` --这对于在异步工作负载被处理时通过 Slack 或 Email 通知自己是非常好的。要用结果调用另一个函数，将`X-Callback-Url`设置为`http://gateway:8080/function/<function_name>`。

现在进入[实验室 8](lab8.md)
