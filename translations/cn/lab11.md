# Lab 11 - 高级函数 - 使用 HMAC 的信任

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"> </img>

## 前言

用于微服务的传统认证策略与函数的工作原理完全相同。在这个实验室中，我们将讨论使用共享secret和基于哈希的消息验证码（HMAC）的几种可用方法之一。有关其他认证策略和想法，请参见。[openfaas-function-auth](https://github.com/openfaas-incubator/openfaas-function-auth/blob/master/README.md)

这绝不是一个广泛的清单，安全和认证是一个复杂的领域，最好留给专家使用经过试验的方法。

## 准备好你的环境

在开始这个实验之前，创建一个新的文件夹

```bash
mkdir -p lab11\`bash
   && cd lab11
```

也要确保你的`faas-cli'版本是`0.7.4'或以上，使用以下命令。

```plain
$ faas-cli version
```

## 什么是 HMAC

如果没有任何形式的认证或信任，我们的函数可能会暴露给任何能猜到其 URL 的人。如果我们的函数可以在互联网或本地网络上访问，那么它们就可能被坏的行为者调用。默认情况下，函数会对任何请求做出响应。然而，如果我们想控制对函数的访问，我们可以使用基于哈希的消息验证码（HMAC）来验证信息的来源。

来自[alexellis/hmac]（https://github.com/alexellis/hmac）。
> HMAC 使用发送方/接收方提前共享的对称密钥。发送方在想要传输信息时将产生一个哈希值--该数据与有效载荷一起发送。然后，收件人将用共享密钥签署有效载荷，如果哈希值匹配，则假定有效载荷来自发件人。

这样我们就可以避免我们的函数被无效的甚至是危险的信息所调用。

## 使用 HMAC

我们将使用 faas-cli 提供的`--sign`标志来包含一个头，其中包含使用我们用`--key`标志提供的共享密钥创建的散列信息。

> 注意: `--sign`和`--key`必须同时存在。

让我们首先通过部署`-env`函数来检查该标志的作用，该函数将打印函数中可访问的所有环境变量。

```bash
$ faas-cli deploy --name env --fprocess="env" --image="function/alpine:new"
```

* 调用不带`--sign`标志的函数。

```plain
$ echo "The message" | faas-cli invoke env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/sbin:/bin
HOSTNAME=d2c1a2cb20c2
fprocess=env
HOME=/root
Http_X_Call_Id=b84947c6-2970-4fcf-ba3b-66dde6943999
Http_X_Forwarded_For=10.255.0.2:34974
Http_X_Forwarded_Host=127.0.0.1:8080
Http_Content_Length=0
Http_Accept_Encoding=gzip
Http_Content_Type=text/plain
Http_User_Agent=Go-http-client/1.1
Http_X_Start_Time=1538725657952768349
...
```

* 再次调用该函数，但这次有`--sign`标志。

```plain
$ echo -n "The message" | faas-cli invoke env --sign=HMAC --key=cookie
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=d2c1a2cb20c2
fprocess=env
HOME=/root
Http_User_Agent=Go-http-client/1.1
Http_Content_Length=0
Http_Accept_Encoding=gzip
...
Http_Hmac=sha1=9239edfe20185eafd7a5513c303b03d207d22f64
...
```

我们看到`HMAC`被作为环境变量`Http_Hmac`提供。生成的值是用钥匙`cookie`签名后的`消息`的哈希值，然后用散列方法`sha1`进行预处理。

## HMAC 在行动

为了我们的目的，我们将创建一个新的 Python 3 函数。让我们把它叫做`hmac-protected`。

```bash
$ faas-cli new --lang python3 hmac-protected --prefix="<your-docker-username>"
```

添加`payload-secret`，它将作为哈希有效载荷的密钥。

像我们在[lab10](https://github.com/openfaas/workshop/blob/master/lab10.md)中那样创建`payload-secret`。

```bash
$ echo -n "<your-secret>" ! | faas-cli secret create payload-secret
```

> 注意：记住你放在"<your-secret>"位置的字符串。

我们的 `hmac-protected.yml`应该看起来像。

```yml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  hmac-protected:
    lang: python3
    handler: ./hmac-protected
    image: <your-docker-username>/hmac-protected:latest
    secrets:
      - payload-secret
```

用以下代码替换`handler.py`的内容。

```python
import os, hmac, hashlib

def validateHMAC(message, secret, hash):

    # GitHub and the sign flag prefix the hash with "sha1="
    receivedHash = getHash(hash)

    # Hash message with secret
    expectedMAC = hmac.new(secret.encode(), message.encode(), hashlib.sha1)
    createdHash = expectedMAC.hexdigest()

    return receivedHash == createdHash

def getHash(hash):
    if "sha1=" in hash:
        hash=hash[5:]
    return hash

def handle(req):
    # We receive the hashed message in form of a header
    messageMAC = os.getenv("Http_Hmac")

    # Read secret from inside the container
    with open("/var/openfaas/secrets/payload-secret","r") as secretContent:
        payloadSecret = secretContent.read()

    # Function to validate the HMAC
    if validateHMAC(req, payloadSecret, messageMAC):
        return "Successfully validated: " + req
    return "HMAC validation failed."
```

> 源代码也可在[hmac-protected/hmac-protected/handler.py](./hmac-protected/hmac-protected/handler.py)

* 通过使用`faas-cli up`在一个命令中构建、推送和部署该函数。

```plain
$ faas-cli up -f ./hmac-protected.yml
```

### 调用函数

我们将通过发送两个值来调用该函数。

* 正常的请求信息

* 一个包含同一消息的哈希值的头，当用`--key`标志的值签名时

在收到请求后，该函数将使用`payload-secret`以与发送者相同的方式签署请求信息。这将创建第二个 HMAC，并与传输的头信息 `Http-Hmac`进行比较。

这里我们比较生成和接收的哈希值。

```python
...
    # Function to validate the HMAC
    if validateHMAC(req, payloadKey, receivedHMAC):
        return "Successfully validated: " + req
    return "HMAC validation failed."
...
```

* 用标志来调用该函数。

```bash
$ echo -n "This is a message" | faas-cli invoke hmac-protected --sign hmac --key=<your-secret>
```

检查响应并确认它与所传达的信息相符。在我们的例子中，我们应该得到。

```plain
Successfully validated: This is a message
```

* 用错误的`--key`调用函数，检查失败信息。

```bash
$ echo -n "This is a message" | faas-cli invoke hmac-protected --sign hmac --key=wrongkey
HMAC validation failed.
```

作为后续任务，你可以应用 HMAC 来保护你在[实验室 5](https://github.com/openfaas/workshop/blob/master/lab5.md)的`issue-bot`上的端点。

你已经完成了实验，可以返回到[主页](./README.md)。