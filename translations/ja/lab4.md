# Lab 4 - functionについてさらに掘り下げてみよう

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

このラボを始める前に作業用のディレクトリを作成しましょう：

```
$ cp -r lab3 lab4 \
   && cd lab4
```

## 環境変数で任意の値を注入

functionの挙動を実行時に変える方法があると何かと便利です。少なくとも次の2種類の方法で実現することができます：

### デプロイ時

* デプロイ時に環境変数を注入する

これは先程 [Lab 3](./lab3.md) で `write_debug` を使ったときの手法です。同じやり方で任意の環境変数の値を設定することができます。例えば *hello world* functionを多言語対応したい場合に `spoken_language` という環境変数を用いることができます。

### クエリ文字列やヘッダなどのHTTPコンテキストを活用してみよう

* クエリ文字列やHTTPヘッダを使う

違う方法かつより動的な方法としてはクエリ文字列やHTTPヘッダを使う、というものがあります。これはリクエスト毎に挙動を変えることができますし、 `faas-cli` あるいは `curl` の双方で使えます。

これらのヘッダは環境変数を通してアクセスできるので、functionから使うのは簡単です。ヘッダはすべて `Http_` プレフィックスがついて、 `-` ハイフンは `_` アンダースコアに変換されます。

では、クエリ文字列を使ってみて、環境変数を一覧表示するfunctionを実行してみましょう。

* 環境変数を一覧表示してくれるfunctionをデプロイします（BusyBoxを内蔵しています）。

```
$ faas-cli deploy --name env --fprocess="env" --image="functions/alpine:latest" --network=func_functions
```

functionをクエリ文字列付きで実行してみましょう：

```
$ echo "" | faas-cli invoke env --query workshop=1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
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
Http_Path=/function/env
...
Http_Query=workshop=1
...
```

Pythonであれば `os.getenv("Http_Query")` でこの値を取得できます。

* HTTPヘッダ付きで実行します

```
$ echo "" | curl http://127.0.0.1:8080/function/env --header "X-Output-Mode: json"
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
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
Http_Path=/function/env
...
Http_X_Output_Mode=json
...
```

Pythonであれば `os.getenv("Http_X_Output_Mode")` でこの値を取得できます。

上の結果をみてもわかるように、`Content-Length` や `Http_Method` 、それに `User_Agent` や `Cookie` など、通常のHTTPリクエストと同様の情報が取得できます。

## ログの活用方法

OpenFaaSのwatchdogは受信したHTTPリクエストを標準入力（ `stdin` ）に渡し、標準出力（ `stdout` ）に返ってきたものをHTTPレスポンスとして返します。つまり、実装が必要なハンドラの部分はwebのことやHTTPのことを意識する必要はありません。

では、標準エラー出力を使った場合どうなるでしょうか？
実はデフォルトでは `stdout/stderr` の内容は結合されて、 `stderr` はfunctionのログには出力されません。

[Lab 3](./lab3.md) の `hello-openfaas` で実際に見てみましょう。

`handler.py` を以下の内容にします

```python
import sys
import json

def handle(req):

    sys.stderr.write("This should be an error message.\n")
    return json.dumps({"Hello": "OpenFaaS"})
```

buildしてdeployしましょう

```sh
$ faas-cli up -f hello-openfaas.yml
```

では、functionを呼び出してみましょう

```sh
$ echo | faas-cli invoke hello-openfaas
```

`stderr` の内容が結合された結果になるのがわかります

```
This should be an error message.
{"Hello": "OpenFaaS"}
```

> 注： `docker service logs hello-openfaas` を見ると、コンテナのログには `stderr` の内容が出力されていないのが確認できます

このままでは `stderr` が原因でfunctionの戻り値は無効なJSONの形になってしまいます。よって、 `stderr` の中身は戻り値には結合せず、コンテナのログにだけ出力するように挙動を変えたいです。これを実現するために `combine_output` フラグを設定することができます。

では、実際に `hello-openfaas.yml` に設定してみましょう：

```yaml
    environment:
      combine_output: false
```

push, deployしてfunctionを呼び出してみましょう。

結果は下のようになります：

```
{"Hello": "OpenFaaS"}
```

functionのコンテナのログを見てみましょう。以下のように表示されているのが確認できます：

```
hello-openfaas.1.2xtrr2ckkkth@linuxkit-025000000001    | 2018/04/03 08:35:24 stderr: This should be an error message.
```

## ワークフローを作ってみよう

あるfunctionの出力を違うfunctionの入力として使いたい場合がでてきます。これはクライアント側からもできれば、API Gatewayを経由して実現することもできます。

### クライアント側でfunctionを連鎖させよう

functionの結果は `curl`  や `faas-cli` 、あるいは自分の作ったコードのクライアントからも他のfunctionへ渡すことができます：

良い点：

* functionに追加のコードが必要ない - CLIでできる
* 素早く開発・テストができる
* 一つ一つのfunctionがモデリングしやすい

悪い点：

* レイテンシーが増す - functionを呼ぶ度にクライアントからサーバーの往復が発生する
* 飛び交うメッセージ量が不必要に増加する

例：

* NodeInfo functionを *Function Store* からデプロイ
* NodeInfoの結果をMarkdown functionに渡して変換

```sh
$ echo -n "" | faas-cli invoke nodeinfo | faas-cli invoke markdown
<p>Hostname: 64767782518c</p>

<p>Platform: linux
Arch: x64
CPU count: 4
Uptime: 1121466</p>
```

NodeInfo functionの結果にHTMLタグ（ `<p>` ）が付加されているのが確認できます。

他にクライアント側での連鎖の例として、画像を生成するfunctionを呼び出して、その画像にウォーターマークを付加するfunctionを連鎖させるというものもあるでしょう。

### function内で別のfunctionを呼び出してみよう

functionから他のfunctionを呼ぶ最も簡単な方法はHTTPでOpenFaaSの *API Gateway* を呼ぶ方法です。この呼出しには外部ドメイン名やIPアドレスは必要ありません。SwarmのDNSエントリがあるので単純に `gateway` を指定するだけで大丈夫です。

API gatewayなどの他のサービスをfunctionから使う場合はホスト名を環境変数で持たせることがベストプラクティスです。ホスト名が将来変わるかもしれないということと、Kubernetesの場合はサフィックス（ `gateway.xxx` ）が必要になることがあるからです。

良い点：

* function同士で相互作用が可能になる
* クライアントに毎回リクエストが戻る必要がなく、ほとんどの場合同じネットワーク内でfunction同士が動いているので低レイテンシーとなる

悪い点：

* functionがHTTPリクエストを行う必要があるので、そのためのライブラリが必要となる

例：

Lab 3では requests モジュールを使って外部のAPIを呼び出し、国際宇宙ステーションの宇宙飛行士を取得する方法をワークショップをやりました。これと同じ方法でOpenFaaSの別のfunctionを呼び出すことができます。

* *Function Store* から *Sentiment Analysis* function をデプロイしてください

Sentiment Analysis functionは与えられた（英語の）文章に対して主観性と（ポジティブかどうかの）極性を数値で返します。結果のJSONは下の例のようになります：

```sh
$ echo -n "California is great, it's always sunny there." | faas-cli invoke sentimentanalysis
{"polarity": 0.8, "sentence_count": 1, "subjectivity": 0.75}
```

この結果から上の文章はとても主観的（75%）でポジティブ（80%）だということがわかります。これらの値は必ず `-1.00` から `1.00` の値をとります。

以下のようなコードで他のfunctionから *Sentiment Analysis* function を呼び出すことができます：

```python
    test_sentence = "California is great, it's always sunny there."
    r = requests.get("http://gateway:8080/function/sentimentanalysis", text= test_sentence)
```

また、環境変数を使った場合は次のようになります:

```python
    gateway_hostname = os.getenv("gateway_hostname", "gateway.openfaas") # gateway_hostnameという環境変数が無い場合はデフォルト値の"gateway"に設定
    test_sentence = "California is great, it's always sunny there."
    r = requests.get("http://" + gateway_hostname + ":8080/function/sentimentanalysis", text= test_sentence)
```

結果は必ずJSONで返ってくるとわかっているので `.json()` というヘルパー関数を使ってレスポンスを変換します：

```python
    result = r.json()
    if result["polarity"] > 0.45:
        print("That was probably positive")
    else:
        print("That was neutral or negative")
```

では、新しいfunctionをPythonで作って全部組み合わせてみましょう

```python
import os
import requests
import sys

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    gateway_hostname = os.getenv("gateway_hostname", "gateway.openfaas") # gateway_hostnameという環境変数が無い場合はデフォルト値の"gateway"に設定

    test_sentence = req

    r = requests.get("http://" + gateway_hostname + ":8080/function/sentimentanalysis", data= test_sentence)

    if r.status_code != 200:
        sys.exit("Error with sentimentanalysis, expected: %d, got: %d\n" % (200, r.status_code))


    result = r.json()
    if result["polarity"] > 0.45:
        print("That was probably positive")
    else:
        print("That was neutral or negative")
```

* `requirements.txt` に `requests` を記載するのを忘れないでください

> 注: SentimentAnalysis functionの編集は特に必要ありません。既にfunction storeからデプロイ済みですし、API gateway経由で呼び出します。

それでは [Lab 5](lab5.md) に進みましょう。
