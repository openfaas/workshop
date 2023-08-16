# 实验 3--函数介绍

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

在开始这个实验之前，为你的文件创建一个新的文件夹。

```sh
$ mkdir -p lab3\`s
   && cd lab3
```

## 创建一个新的函数

有两种方法来创建一个新的函数。

* 使用一个内置的或社区的代码模板建立一个函数（默认情况下）
* 使用一个现有的二进制文件并将其作为你的函数（高级）

### 构建或生成一个新函数

在用模板创建新函数之前，请确保你从 GitHub 上提取了[模板](https://github.com/openfaas/templates)。

```sh
$ faas-cli template pull

Fetch templates from repository: https://github.com/openfaas/templates.git
 Attempting to expand templates from https://github.com/openfaas/templates.git
2021/08/25 15:58:10 Fetched 13 template(s) : [csharp dockerfile go java11 java11-vert-x node node12 node14 php7 python python3 python3-debian ruby] from https://github.com/openfaas/templates.git
```

之后，要想知道哪些语言是可用的，请键入。

```sh
$ faas-cli new --list
Languages available as templates:
- csharp
- dockerfile
- go
- java11
- java11-vert-x
- node
- node12
- node14
- php7
- python
- python3
- python3-debian
- ruby
```

或者创建一个包含`Dockerfile`的文件夹，然后在 YAML 文件中选择 `Dockerfile`语言类型。

在这一点上，你可以为 Python、Python 3、Ruby、Go、Node、CSharp 等创建一个新函数。

* 关于我们的例子的说明

我们这次研讨会的所有例子都经过了 OpenFaaS 社区对*Python 3*的全面测试，但也应该与*Python 2.7*兼容。

如果你喜欢使用 Python 2.7 而不是 Python 3，那么把`faas-cli new --lang python3`换成`faas-cli new --lang python`。

### Python 中的 Hello world

我们将在 Python 中创建一个 hello-world 函数，然后转到也使用额外依赖的东西上。

* 构建函数的脚手架

```sh
faas-cli new --lang python3 hello-openfaas --prefix="<your-docker-username-here>"
```

参数`--prefix`将更新`image:`--prefix`参数将更新`hello-openfaas.yml`中的值，其前缀应该是你的Docker Hub账号。对于[OpenFaaS](https://hub.docker.com/r/functions)来说，这是`image: functions/hello-openfaas`，参数将是`--prefix="function"`。

如果你在创建函数时没有指定前缀，那么在创建后编辑 YAML 文件。

这将创建三个文件和一个目录。

```sh
./hello-openfaas.yml
./hello-openfaas
./hello-openfaas/handler.py
./hello-openfaas/requirements.txt
```

YAML (.yml) 文件是用来配置 CLI 来构建、推送和部署你的函数。

> 注意：每当你需要在 Kubernetes 或远程 OpenFaaS 实例上部署一个函数时，你必须在构建函数后推送它。在这种情况下，你也可以用一个环境变量覆盖默认的网关 URL，即 127.0.0.1:8080`。`export OPENFAAS_URL=127.0.0.1:31112`.

下面是 YAML 文件的内容。

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  hello-openfaas:
    lang: python3
    handler: ./hello-openfaas
    image: hello-openfaas
```

* 函数的名称由`functions`下的键表示，即`hello-openfaas`。
* 语言由 `lang` 字段表示。
* 用于构建的文件夹被称为 `handler`，它必须是一个文件夹而不是一个文件。
* 要使用的 Docker 镜像名称在`image`字段下。

请记住，`gateway`URL 可以在 YAML 文件中（通过编辑`provider:`下的`gateway:`值）或在 CLI 上（通过使用`--gateway`或设置`OPENFAAS_URL`环境变量）进行覆盖。

下面是`handler.py`文件的内容。

```python
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return req
```

这个函数将只是返回输入，所以它实际上是一个`echo`函数。

编辑信息，使其返回 `Hello OpenFaaS`，例如。

```python
    return "Hello OpenFaaS"
```

任何返回到 stdout 的值都会随后返回到调用程序。另外，也可以使用`print()`语句，它将表现出类似的流向，并传递给调用程序。

这是本地开发人员对函数的工作流程。

```sh
faas-cli up -f hello-openfaas.yml
```

> 注意：在运行这个命令之前，请确保你已经用`docker login`命令登录了 docker 注册中心。

> 注意: `faas-cli up`命令将`faas-cli`的构建、推送和部署命令合并为一条命令。

随后通过用户界面、CLI、`curl`或其他应用程序调用该函数。

该函数将始终获得一个路由，例如。

```sh
$OPENFAAS_URL/function/<function_name>（函数名）。
$OPENFAAS_URL/function/figlet
$OPENFAAS_URL/function/hello-openfaas
```

> 提示：如果你把 YAML 文件重命名为`stack.yml`，那么你就不需要向任何命令传递`-f`标志。

函数只能通过`GET`或`POST`方法来调用。

* 调用你的函数

用`faas-cli invoke`测试函数，查看`faas-cli invoke --help`获取更多选项。

### 示例函数：astronaut-finder

我们将创建一个名为 `astronaut-finder` 的函数，在国际空间站（ISS）上随机拉出一个太空人的名字。

```sh
faas-cli new --lang python3 astronaut-finder --prefix="<your-docker-username-here>"
```

这将为我们写三个文件。

```sh
./astronaut-finder/handler.py
```

函数的处理程序--你会得到一个带有原始请求的`req`对象，并可以将函数的结果打印到控制台。

```sh
./astronaut-finder/requirements.txt
```

这个文件用来管理函数--它有函数的名称、Docker 镜像和任何其他需要的定制。

```sh
./astronaut-finder.yml
```

使用该文件列出你要安装的任何`pip`模块，如`requests`或`urllib`。

* 编辑`./astronaut-finder/requirements.txt`。

```sh
requests
```

这告诉函数它需要使用一个名为[requests](http://docs.python-requests.org/en/master/)的第三方模块，用于通过 HTTP 访问网站。

* 编写该函数的代码。

我们将从以下地方拉入数据： <http://api.open-notify.org/astros.json>

下面是一个结果的例子。

```json
{"number": 6, "people": [{"craft": "ISS", "name": "Alexander Misurkin"}, {"craft": "ISS", "name": "Mark Vande Hei"}, {"craft": "ISS", "name": "Joe Acaba"}, {"craft": "ISS", "name": "Anton Shkaplerov"}, {"craft": "ISS", "name": "Scott Tingle"}, {"craft": "ISS", "name": "Norishige Kanai"}], "message": "success"}
```

更新`handler.py`。

```python
import requests
import random

def handle(req):
    r = requests.get("http://api.open-notify.org/astros.json")
    result = r.json()
    index = random.randint(0, len(result["people"])-1)
    name = result["people"][index]["name"]

    return "%s is in space" % (name)
```

> 注意：在这个例子中，我们没有使用参数`req`，但必须把它放在函数的头部。

现在建立这个函数。

```sh
faas-cli build -f ./astronaut-finder.yml
```

> 提示。试着把 astronaut-finder.yml 重命名为`stack.yml`，然后只调用`faas-cli build`。`stack.yml`是 CLI 的默认文件名。

推送函数。

```sh
faas-cli push -f ./astronaut-finder.yml
```

部署该函数。

```sh
faas-cli deploy -f ./astronaut-finder.yml
```

调用该函数

```sh
$ echo | faas-cli invoke astronaut-finder
安东-史卡普勒夫在太空中

$ echo | faas-cli invoke astronaut-finder
乔-阿卡巴在太空中
```

## 故障排除：找到容器的日志

你可以通过容器的日志找到你的函数的每次调用的高级信息。

```sh
kubectl logs deployment/astronaut-finder -n openfaas-fn
```

## 故障排除：使用`write_debug'的 verbose 输出

让我们为你的函数打开 verbose 输出。这在默认情况下是关闭的，这样我们就不会用数据淹没你的函数的日志--这在处理二进制数据时尤其重要，因为二进制数据在日志中没有意义。

这是标准的 YAML 配置。

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  astronaut-finder:
    lang: python3
    handler: ./astronaut-finder
    image: astronaut-finder
```

为该函数编辑 YAML 文件，并添加一个 `environment` 部分。

```yaml
  astronaut-finder:
    lang: python3
    handler: ./astronaut-finder
    image: astronaut-finder
    environment:
      write_debug: true
```

现在用`faas-cli deploy -f ./astronaut-finder.yml`再次部署你的函数。

调用该函数，然后再次检查日志，查看函数的响应。

```sh
kubectl logs deployment/astronaut-finder -n openfaas-fn
```

### 管理多个函数

CLI 的 YAML 文件允许将函数分组为堆栈，这在处理一组相关函数时很有帮助。

为了了解它是如何工作的，生成两个函数。

```sh
faas-cli new --lang python3 first
```

对于第二个函数使用`--append`标志。

```sh
faas-cli new --lang python3 second --append=./first.yml
```

为了方便起见，我们把`first.yml`改名为`example.yml`。

```sh
mv first.yml example.yml
```

现在看看这个文件。

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  first:
    lang: python3
    handler: ./first
    image: first
  second:
    lang: python3
    handler: ./second
    image: second
```

这里有几个标志，在处理函数堆栈时有帮助。

* 以并行方式构建。

```sh
faas-cli build -f ./example.yml --parallel=2
```

* 只建立/推送一个函数。

```sh
faas-cli build -f ./example.yml --filter=second
```

花点时间来探索`build`/`push`和`deploy`的选项。

* `faas-cli build --help`。
* `faas-cli push --help`。
* `faas-cli deploy --help`。

要同时运行`faas-cli build &&faas-cli push &&faas-cli deploy`，请使用`faas-cli up`代替。

> 专业提示：如果你不想传递`-f`参数，`stack.yml`是 faas-cli 寻找的默认名称。

你也可以使用`faas-cli deploy -f https://....`通过 HTTP（s）部署远程函数栈（yaml）文件。

### 自定义模板

如果你有自己的一套分叉模板或自定义模板，那么你可以把它们拉下来，用 CLI 使用。

下面是一个获取 Python 3 模板的例子，它使用 Debian Linux。

使用 `git` URL 拉取模板。

```sh
faas-cli template pull https://github.com/openfaas-incubator/python3-debian
```

现在键入 `faas-cli new --list`。

```sh
$ faas-cli new --list | grep python
- python
- python3
- python3-debian
```

这些新模板会被保存在你当前的工作目录下`./templates/`。

#### 自定义模板。模板商店

模板商店*是一个类似于*函数商店*的概念，它使用户可以通过分享他们的模板来进行协作。模板商店也意味着你不必记住任何 URL 来利用你喜欢的社区或项目模板。

你可以使用以下两个命令来搜索和发现模板。

```sh
$ faas-cli template store list
$ faas-cli template store list -v

NAME                     SOURCE             DESCRIPTION
csharp                   openfaas           Classic C# template
dockerfile               openfaas           Classic Dockerfile template
go                       openfaas           Classic Golang template
...
```

为了获得更多的细节，你可以使用`--verbose`标志，或者`describe`命令。

让我们找到一个具有 HTTP 格式的 Golang 模板。

```bash
faas-cli template store list | grep golang

golang-http openfaas 
Golang HTTP template 
golang-middleware openfaas 
Golang Middleware template
```

然后查看其上游仓库。

```sh
$ faas-cli template store describe golang-http

Name:              golang-http
Platform:          x86_64
Language:          Go
Source:            openfaas
Description:       Golang HTTP template
Repository:        https://github.com/openfaas/golang-http-template
Official Template: true
```

把模板拉下来。

```sh
faas-cli template store pull golang-http
```

现在你可以通过输入以下内容用这个模板创建一个函数。

bash
faas-cli new --lang golang-http NAME

```plain

为了比运行`faas-cli template store pull golang-http`来创建函数更容易，你可以在你的stack.yml文件中附加以下内容。

```yaml
configuration:
  templates:
    - name: golang-http
```

然后运行以下内容，而不是指定模板名称。

```bash
faas-cli template store pull
```

也请参见。

* [OpenFaaS YAML 参考指南](https://docs.openfaas.com/reference/yaml/)
* [函数与模板存储](https://github.com/openfaas/store/)

### YAML 文件中的变量替换（可选练习)

用于配置 CLI 的`.yml`文件能够进行变量替换，这样你就能够使用同一个`.yml`文件进行多种配置。

其中一个例子是，当开发和生产图像有不同的注册表时，这就很有用。你可以使用变量替换，使本地和测试环境使用默认账户，而 CI 服务器可以被配置为使用生产账户。

> 这是由[envsubst 库]（<https://github.com/drone/envsubst>）提供的。遵循该链接可以看到支持的变量的例子

编辑你的`astronaut-finder.yml`以匹配以下内容。

```yml
  astronaut-finder:
    lang: python3
    handler: ./astronaut-finder
    image: ${DOCKER_USER:-development}/astronaut-finder
    environment:
      write_debug: true
```

你会注意到`image`属性已被更新，包括一个变量定义（`DOCKER_USER`）。该值将被替换为同名的环境变量的值。如果环境变量不存在，或为空，将使用默认值（`development`）。

该变量将在整个文件中被替换成该值。所以，如果你的`.yml`文件中有几个函数，所有对`DOCKER_USER`变量的引用将被替换为该环境变量的值

运行下面的命令并观察输出。

`faas-cli build -f ./astronaut-finder.yml`。

输出应该显示，构建的镜像被标记为`development/astronaut-finder:latest`。

现在，将环境变量设置为你的 Docker Hub 账户名（在这个例子中，我们将使用 OpenFaaS 的 `function`账户）。

```sh
export DOCKER_USER=functions
```

运行与之前相同的构建命令，观察输出。

`faas-cli build -f ./astronaut-finder.yml`。

现在输出应该显示，镜像是用更新的标签 `functions/astronaut-finder:latest`构建的。

### 自定义二进制文件作为函数(可选练习)

自定义二进制文件或容器可以作为函数使用，但大多数时候，使用语言模板应该涵盖所有最常见的情况。

为了使用自定义二进制文件或 Dockerfile，使用`dockerfile`语言创建一个新函数。

```sh
faas-cli new --lang dockerfile sorter --prefix="<your-docker-username-here>"
```

你会看到一个名为 `sorter`和 `sorter.yml`的文件夹被创建。

编辑`sorter/Dockerfile`并更新设置`fprocess'的那一行。让我们把它改成内置的bash命令`sort`。我们可以用它来对一个字符串列表按字母数字顺序进行排序。

```dockerfile
ENV fprocess="sort"
```

现在构建、推送和部署该函数。

```sh
faas-cli up -f sorter.yml
```

现在通过用户界面或 CLI 来调用该函数。

```sh
$ echo -n '
elephant
zebra
horse
aardvark
monkey'| faas-cli invoke sorter

aardvark
elephant
horse
monkey
zebra
```

在这个例子中，我们使用了[BusyBox](https://busybox.net/downloads/BusyBox.html)中的`sort`，它是内置的函数。还有其他有用的命令，如`sha512sum`，甚至是`bash`或 shell 脚本，但你并不局限于这些内置命令。任何二进制或现有的容器都可以通过添加 OpenFaaS 函数看门狗而成为无服务器函数。

> 提示：你知道 OpenFaaS 也支持 Windows 二进制文件吗？比如 C#、VB 或 PowerShell？

现在进入[实验室 4](lab4.md)
