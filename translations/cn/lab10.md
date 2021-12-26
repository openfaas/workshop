# Lab 10 - 高级函数 - secret

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

在开始本实验室之前，为你的文件创建一个新的文件夹。由于本实验室是建立在先前的实验室基础上的，因此请复制 lab5。

```plain
$ cp -r lab5 lab10\
   && cd lab10
```

## 使用secret

[实验室 5](./lab5.md)研究了`issue-bot`如何从环境变量（`auth_token`）获得 GitHub 的个人访问令牌。 另一种方法是使用**机密**来存储敏感信息。

来自 Docker 文档。
> ... secret是一团数据，如密码、SSH 私钥、SSL 证书或其他数据，不应通过网络传输或未经加密存储在 Docker 文件或应用程序的源代码中。

这是一个比环境变量更安全的选择。环境变量更容易使用，但最适合于非保密的配置项目。 似乎很适合用于存储`auth_token`值。 

请参阅[docs](https://docs.openfaas.com/reference/secrets/)中关于secret的更多信息和它的设计。

### 创建一个secret

> secret名称必须遵循 DNS-1123 惯例，由小写字母数字字符或'-'组成，并且必须以一个字母数字字符开始和结束 

从一个终端运行以下命令。

```plain
$ echo -n <auth_token> | faas-cli secret create auth-token
```

测试secret是否被创建。

```plain
$ faas-cli secret ls
```
> 注意：请记住，`-g`标志可以在网关之间轻松切换。 这也适用于secret。

```plain
kubectl get secret auth-token -n openfaas-fn -o json
```

> 注意：如果你在远程网关上部署你的函数，确保你在你用于网关的虚拟机上创建你的secret。

当secret被函数挂载时，它将以文件形式出现在`/var/openfaas/secrets/auth-token`下。这可以由`handler.py`读取，以获得 GitHub 的*个人访问令牌*。

### 更新 issue-bot.yml

用一个指令取代对`env.yml`的引用，使`auth-token`的secret对函数可用。

```yml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  issue-bot:
    lang: python3
    handler: ./issue-bot
    image: <your-username>/issue-bot
    environment:
      write_debug: true
      gateway_hostname: "gateway.openfaas"
      positive_threshold: 0.25
    secrets:
      - auth-token
```

### 更新`issue-bot`函数

函数处理程序需要改变，以使其读取`auth-token`secret，而不是环境变量。 这只是一个单行的改动，在这里。

python
g = Github(os.getenv("auth_token"))
```plain
被替换为 
```python
with open("/var/openfaas/secrets/auth-token", "r") as authToken:  
    g = Github(authToken.read())
```

> 完整的源代码可在[issue-bot-secrets/bot-handler/handler.py](./issue-bot-secrets/bot-handler/handler.py)

* 构建和部署

使用 CLI 来构建和部署该函数。

```plain
$ faas-cli up -f issue-bot.yml
```

现在转到[Lab 11](lab11.md)。