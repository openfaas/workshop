# Lab 8 - 高级函数 - 超时

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

在开始这个实验之前，为你的文件创建一个新的文件夹。

```plain
$ mkdir -p lab8 \
   && cd lab8
```

## 用`read_timeout`扩展超时时间

*timeout*对应于一个函数可以运行多长时间，直到被执行。它对防止分布式系统中的误操作很重要。

有几个地方可以为你的函数配置超时，在每个地方都可以通过使用环境变量来完成。

* 函数超时

* `read_timeout` - 允许函数通过 HTTP 读取一个请求的时间
* `write_timeout` - 允许函数在 HTTP 上写一个响应的时间
* `exec_timeout` - 一个函数在被终止前可以运行的最大时间。

API 网关的默认时间是 20 秒，所以我们来测试一下在一个函数上设置一个更短的超时时间。

```plain
$ faas-cli new --lang python3 sleep-for --prefix="<your-docker-username-here>"
```

编辑`handler.py`。

```python
import time
import os

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    sleep_duration = int(os.getenv("sleep_duration", "10"))
    preSleep = "Starting to sleep for %d" % sleep_duration
    time.sleep(sleep_duration)  # Sleep for a number of seconds
    postSleep = "Finished the sleep"
    return preSleep + "\n" + postSleep
```

现在编辑`sleep-for.yml`文件，添加这些环境变量。

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  sleep-for:
    lang: python3
    handler: ./sleep-for
    image: <your-docker-username-here>/sleep-for:0.1
    environment:
      sleep_duration: 10
      read_timeout: "5s"
      write_timeout: "5s"
      exec_timeout: "5s"
```

使用 CLI 来构建、推送、部署和调用该函数。

```sh
$ echo | faas-cli invoke sleep-for
Server returned unexpected status code: 502 -
```

你应该看到它没有打印消息就终止了，因为`sleep_duration`比超时值高。

现在把`sleep_duration`设置为一个较低的数字，如`2`，然后再次运行`faas-cli deploy`。在编辑函数的 YAML 文件时，你不需要重建这个函数。

```sh
$ echo | faas-cli invoke sleep-for
Starting to sleep for 2
Finished the sleep
```

* API 网关

要为你的函数设置超出默认限制的扩展超时，请遵循以下教程。[扩展的超时](https://docs.openfaas.com/tutorials/expanded-timeouts/)

现在转到[实验室 9](lab9.md)