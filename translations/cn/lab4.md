# 实验 4--更深入地使用函数

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

在开始本实验之前，为你的文件创建一个新的文件夹。由于本实验是建立在早期实验的基础上的，所以请复制 lab3。

```plain
$ cp -r lab3 lab4\
   && cd lab4
```

## 通过环境变量注入配置

能够控制一个函数在运行时的行为方式是很有用的，我们至少可以通过两种方式来实现这一点。

### 在部署时

* 在部署时设置环境变量

我们在[Lab 3](./lab3.md)中用`write_debug`做了这个 - 你也可以在这里设置任何你想要的自定义环境变量 - 例如，如果你想为你的*hello world*函数配置一种语言，你可以引入一个`spoken_language`变量。

### 使用 HTTP 上下文--querystring / headers

* 使用 querystring 和 HTTP headers

另一个更动态的、可以在每个请求层面上改变的选项是使用查询字符串和 HTTP 头信息，两者都可以通过`faas-cli`或`curl`传递。

这些头信息通过环境变量暴露出来，所以它们很容易在你的函数中被使用。所以任何头信息都以`Http_`为前缀，所有`-`连字符都被替换成`_`下划线。

让我们用 querystring 和一个列出所有环境变量的函数来试试。

* 使用 BusyBox 的内置命令，部署一个打印环境变量的函数。

```plain
faas-cli deploy --name env --fprocess="env" --image="function/alpine:latest"
```

* 用一个查询字符串调用该函数。

```sh
$ echo "" | faas-cli invoke env --query workshop=1
PATH=/usr/local/bin:/usr/local/bin:/usr/bin:/sbin:/bin
HOSTNAME=05e8db360c5a
fprocess=env
HOME=/root
Http_Connection=close
Http_Content_Type=text/plain
Http_X_Call_Id=cdbed396-a20a-43fe-9123-1d5a122c976d
Http_X_Forwarded_For=10.255.0.2
Http_X_Start_Time=1519729562486546741
Http_User_Agent=Go-http-client/1.1
Http_Accept_Encoding=gzip
Http_Method=POST
Http_ContentLength=-1
Http_Path=/
...
Http_Query=workshop=1
...
```

在 Python 代码中，你会输入`os.getenv("Http_Query")`。

* 将路径附加到你的函数 URL 上

用以下方法调用 env 函数。

```sh
$ curl -X GET $OPENFAAS_URL/function/env/some/path -d ""
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/sbin:/bin
HOSTNAME=fae2ac4b75f9
fprocess=env
HOME=/root
Http_X_Forwarded_Host=127.0.0.1:8080
Http_X_Start_Time=1539370471902481800
Http_Accept_Encoding=gzip
Http_User_Agent=curl/7.54.0
Http_Accept=*/*
Http_X_Forwarded_For=10.255.0.2:60460
Http_X_Call_Id=bb86b4fb-641b-463d-ae45-af68c1aa0d42
Http_Method=GET
Http_ContentLength=0
...
Http_Path=/some/path
...
```

正如你所看到的，`Http_Path`头包含你的路径。
如果你想在你的代码中使用它，只要用`os.getenv("Http_Path")`来获取它。

* 现在用标头来调用它。

```sh
$ curl $OPENFAAS_URL/function/env --header "X-Output-Mode: json" -d ""
PATH=/usr/local/bin:/usr/local/bin:/usr/bin:/sbin:/bin
HOSTNAME=05e8db360c5a
fprocess=env
HOME=/root
Http_X_Call_Id=8e597bcf-614f-4ca5-8f2e-f345d660db5e
Http_X_Forwarded_For=10.255.0.2
Http_X_Start_Time=1519729577415481886
Http_Accept=*/*
Http_Accept_Encoding=gzip
Http_Connection=close
Http_User_Agent=curl/7.55.1
Http_Method=GET
Http_ContentLength=0
Http_Path=/
...
Http_X_Output_Mode=json
...
```

在 Python 代码中，你会输入`os.getenv("Http_X_Output_Mode")'。

你可以看到所有其他的 HTTP 上下文也被提供了，比如当 `Http_Method`是 `POST`时的 `Content-Length`，`User_Agent`，Cookies 和其他你期望从 HTTP 请求中看到的东西。

## 安全：只读文件系统

OpenFaaS 可以使用的容器安全特性之一是使我们执行环境的根文件系统只读的能力。如果一个函数被破坏，这可以减少攻击面。

生成一个函数，将文件保存到函数的文件系统中。

```sh
faas-cli new --lang python3 ingest-file --prefix=your-name
```

更新处理程序。

```python
import os
import time

def handle(req):
    # Read the path or a default from environment variable
    path = os.getenv("save_path", "/home/app/")

    # generate a name using the current timestamp
    t = time.time()
    file_name = path + str(t)

    # write a file
    with open(file_name, "w") as f:
        f.write(req)
        f.close()

    return file_name
```

建立这个例子。

```sh
faas-cli up -f ingest-file.yml
```

调用该例子。

```sh
echo "Hello function" > message.txt

cat message.txt | faas-cli invoke -f ingest-file.yml ingest-file
```

该文件将被写入`/home/app`路径中。

现在编辑 ingest-file.yml 并使该函数为只读。

```yaml
...
functions:
  ingest-file:
    lang: python3
    handler: ./ingest-file
    image: alexellis2/ingest-file:latest
    readonly_root_filesystem: true
```

> 也请参见。[YAML 参考](https://docs.openfaas.com/reference/yaml/#function-read-only-root-filesystem)

再次部署。

```sh
faas-cli up -f ingest-file.yml
```

现在这将会失败。

```sh
echo "Hello function" > message.txt

cat message.txt | faas-cli invoke -f ingest-file.yml ingest-file
```

请看错误。

```sh
Server returned unexpected status code: 500 - exit status 1
Traceback (most recent call last):
  File "index.py", line 19, in <module>
    ret = handler.handle(st)
  File "/home/app/function/handler.py", line 13, in handle
    with open(file_name, "w") as f:
OSError: [Errno 30] Read-only file system: '/home/app/1556714998.092464'
```

为了写到一个临时区域，设置环境变量`save_path`。

```yaml
...
functions:
  ingest-file:
    lang: python3
    handler: ./ingest-file
    image: alexellis2/ingest-file:latest
    readonly_root_filesystem: true
    environment:
        save_path: "/tmp/"
```

现在你可以再运行一次`faas-cli up -f ingest-file.yml`来测试这个修正，文件将被写入`/tmp/`。

我们现在有能力锁定我们的函数代码，使其不能被意外改变或恶意更新。

## 利用日志记录

OpenFaaS 看门狗通过标准 I/O 流`stdin`和`stdout`传入 HTTP 请求和读取 HTTP 响应来运行。这意味着作为一个函数运行的进程不需要知道任何关于网络或 HTTP 的信息。

一个有趣的情况是，当一个函数以非零退出代码退出时，`stderr`不是空的。
默认情况下，一个函数的`stdout/stderr`是合并的，`stderr`不被打印到日志中。

让我们用[Lab 3](./lab3.md#hello-world-in-python)中的`hello-openfaas`函数来检查。

将`handler.py`的代码改为

```python
import sys
import json

def handle(req):

    sys.stderr.write("This should be an error message.\n")
    return json.dumps({"Hello": "OpenFaaS"})
```

构建和部署

```sh
faas-cli up -f hello-openfaas.yml
```

现在用以下方法调用该函数

```sh
echo | faas-cli invoke hello-openfaas
```

你应该看到合并输出。

```plain
This should be an error message.
{"Hello": "OpenFaaS"}
```

> 注意：如果你用`docker service logs hello-openfaas`检查容器日志（或者`kubectl logs deployment/hello-openfaas -n openfaas-fn`），你应该看不到 stderr 输出。

在这个例子中，我们需要这个函数返回有效的 JSON，可以被解析。不幸的是，日志信息使输出无效。
所以我们需要将这些信息从 stderr 重定向到容器的日志中。
OpenFaaS 提供了一个解决方案，所以你可以将错误信息打印到日志中，并保持函数响应的清晰，只返回`stdout`。
为此你应该使用`combine_output`标志。

让我们来试试。打开`hello-openfaas.yml`文件，添加这些行。

```yaml
    environment:
      combine_output: false
```

部署并调用该函数。

输出应该是。

```plain
{"Hello": "OpenFaaS"}
```

检查容器日志中的`stderr`。你应该看到类似的信息。

```plain
hello-openfaas.1.2xtrr2ckkkth@linuxkit-025000000001    | 2018/04/03 08:35:24 stderr: This should be an error message.
```

## 创建工作流

在有些情况下，把一个函数的输出作为另一个函数的输入是很有用的。 这在客户端和通过 API 网关都可以实现。

### 客户端上的连锁函数

你可以使用`curl`、`faas-cli`或一些你自己的代码将一个函数的结果输送到另一个函数。这里有一个例子。

优点。

* 不需要代码 - 可以用 CLI 程序完成
* 快速开发和测试
* 容易在代码中建模

缺点。

* 额外的延迟 - 每个函数都要返回到服务器上
* 聊天（更多的信息）

例子。

* 从*函数库*部署 NodeInfo 函数

* 然后通过 Markdown 转换器推送 NodeInfo 的输出

```sh
$ echo -n "" | faas-cli invoke nodeinfo | faas-cli invoke markdown
<p>Hostname: 64767782518c</p>

<p>Platform: linux
Arch: x64
CPU count: 4
Uptime: 1121466</p>
```

现在你会看到 NodeInfo 函数的输出被装饰成 HTML 标签，例如。`<p>`.

另一个客户端函数链的例子可能是调用一个生成图像的函数，然后将该图像发送到另一个添加水印的函数中。

### 从另一个函数中调用一个函数

从另一个函数中调用一个函数的最简单方法是通过 OpenFaaS *API 网关*通过 HTTP 进行调用。这个调用不需要知道外部域名或 IP 地址，它可以简单地通过 DNS 条目将 API 网关称为`gateway`。

当从一个函数访问 API 网关等服务时，最好的做法是使用环境变量来配置主机名，这很重要，有两个原因--名称可能会改变，在 Kubernetes 中有时需要一个后缀。

优点。

* 函数之间可以直接利用对方
* 低延迟，因为函数可以在同一网络上相互访问

缺点。

* 需要一个代码库来进行 HTTP 请求

例子。

在[实验室 3](./lab3.md)中，我们介绍了 request 模块，并使用它来调用一个远程 API，以获得国际空间站上的一个宇航员的名字。我们可以使用同样的技术来调用部署在 OpenFaaS 上的另一个函数。

* 使用用户界面，进入*函数商店*并部署*情感分析*函数。

或者使用 CLI。

```plain
faas-cli store deploy SentimentAnalysis
```

情感分析函数将告诉你任何句子的主观性和极性（积极性评级）。该函数的结果是以 JSON 格式显示的，如下面的例子。

```sh
$ echo -n "California is great, it's always sunny there." | faas-cli invoke sentimentanalysis
{"polarity": 0.8, "sentence_count": 1, "subjectivity": 0.75}
```

因此，结果显示我们的测试句子既非常主观（75%）又非常积极（80%）。这两个字段的值总是在`-1.00`和`1.00`之间。

下面的代码可以用来调用*情绪分析*函数或任何其他函数。

给网关主机加上`openfaas`命名空间的后缀。

```python
    r = requests.get("http://gateway.openfaas:8080/function/sentimentanalysis", text= test_sentence)
```

或者通过一个环境变量。

```python
    gateway_hostname = os.getenv("gateway_hostname", "gateway.openfaas") # uses a default of "gateway.openfaas" for when "gateway_hostname" is not set
    test_sentence = "California is great, it's always sunny there."
    r = requests.get("http://" + gateway_hostname + ":8080/function/sentimentanalysis", data= test_sentence)
```

由于结果总是以 JSON 格式出现，我们可以利用辅助函数`.json()`来转换响应。

```python
    result = r.json()
    if result["polarity"] > 0.45:
       return "That was probably positive"
    else:
        return "That was neutral or negative"
```

现在，在 Python 中创建一个新的函数，并将其全部整合起来

```python
import os
import requests
import sys

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    gateway_hostname = os.getenv("gateway_hostname", "gateway.openfaas") # uses a default of "gateway" for when "gateway_hostname" is not set

    test_sentence = req

    r = requests.get("http://" + gateway_hostname + ":8080/function/sentimentanalysis", data= test_sentence)

    if r.status_code != 200:
        sys.exit("Error with sentimentanalysis, expected: %d, got: %d\n" % (200, r.status_code))

    result = r.json()
    if result["polarity"] > 0.45:
        return "That was probably positive"
    else:
        return "That was neutral or negative"
```

* 记得在你的`requirements.txt`文件中加入`requests`。

注意：你不需要修改或改变 SentimentAnalysis 函数的源代码，我们已经部署了它并将通过 API 网关访问它。

现在转到[实验室 5](lab5.md)。
