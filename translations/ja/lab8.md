# Lab 8 - 応用編 - タイムアウト

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

このラボを始める前に作業用のディレクトリを作成しましょう：

```
$ mkdir -p lab8 \
   && cd lab8
```

## `read_timeout` でタイムアウトを延ばす

タイムアウトとは、functionが許容される実行時間を指します。この時間をすぎるとfunctionは強制的に停止されます。分散システムなどでAPIが悪用されないための重要な役割を果たします。

functionのタイムアウトには複数の種類があり、それぞれを環境変数で設定することができます。

* Function timeout



* `read_timeout` - functionがHTTPリクエストを読み込むときのタイムアウト
* `write_timout` - functionがHTTPレスポンスを書き込むときのタイムアウト
* `exec_timeout` - functionの実行が許容される最大の時間

API Gatewayにはデフォルトで20秒が設定されているので、さらに短い時間に設定してみましょう。

```
$ faas-cli new --lang python3 sleep-for --prefix="<Docker Hubのユーザー名>"
```

`handler.py` を編集します：

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

それでは `sleep-for.yml` に環境変数を設定しましょう。

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  sleep-for:
    lang: python3
    handler: ./sleep-for
    image: <Docker Hubのユーザー名>/sleep-for:0.1
    environment:
      sleep_duration: 10
      read_timeout: 5
      write_timeout: 5
      exec_timeout: 5
```

CLIを使ってbuild、push、deployしてからfunctionを実行してみましょう。

```
$ echo | faas-cli invoke sleep-for
Server returned unexpected status code: 500 - Can't reach service: sleep-for
```

メッセージが返却される前に終了しているのが確認できます。

それでは `sleep_duration` を `2` に設定してもっと短くしましょう。再び `faas-cli deploy` を実行します。functionのYAMLを編集した場合はリビルドの必要はありません。

```
$ echo | faas-cli invoke sleep-for
Starting to sleep for 2
Finished the sleep
```

* API Gateway timeout

gatewayに設定するタイムアウトが最も優先されます。執筆時点ではこの値は「20s」に設定されていますが、任意の値に設定することができます。

gatewayの設定を変更する場合は `docker-compose.yml` の `gateway` と `faas-swarm` の `read_timeout` や `write_timeout` の値を変更します。変更後は `./deploy_stack.sh` を実行して反映します。

それでは [Lab 9](lab9.md) に進みましょう。