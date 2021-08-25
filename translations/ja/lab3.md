# Lab 3 - はじめてのfunction

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

このラボを始める前に作業用のディレクトリを作成しましょう：

```
$ mkdir -p lab3 \
   && cd lab3
```

## 新規functionの作り方

新規functionには２つの作り方があります：

* ビルトインまたはコミュニティで作られたコードのテンプレートを基にscaffold（スキャフォールド）
* 既にもっているバイナリをfunctionに変換（上級者用）


### 新規functionの生成またはscaffold（スキャフォールド）について

テンプレートから新規functionを作る前に [Github上のテンプレート](https://github.com/openfaas/templates) をダウンロードしておきましょう：

```
$ faas-cli template pull

Fetch templates from repository: https://github.com/openfaas/templates.git
 Attempting to expand templates from https://github.com/openfaas/templates.git
2021/08/25 15:58:10 Fetched 13 template(s) : [csharp dockerfile go java11 java11-vert-x node node12 node14 php7 python python3 python3-debian ruby] from https://github.com/openfaas/templates.git
```

次のコマンドでどの言語が使えるか確認することができます：

```
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

現時点ではPython, Python 3, Ruby, Go, Node, CSharp などのfunctionが作成可能です。

* ワークショップのサンプルのfunctionについて

このワークショップのfunctionの例はOpenFaaSのコミュニティによって全て十分に*Python 3*でテストされていますが、 *Python 2.7* でも互換性はあるはずです。

もし、Python 3ではなくPython 2.7を使いたい場合は `faas-cli new --lang python3` を `faas-cli new --lang python` に変えてください。

### PythonでHello world

それではhello-world functionをPythonで作って、その後依存パッケージを使うようなfunctionも作ってみましょう。

* functionの基礎をscaffold

```
$ faas-cli new --lang python3 hello-openfaas --prefix="<ここにDocker Hubのユーザー名を入力>"
```

`--prefix` パラメータを使うことで `hello-openfaas.yml` で記載される `image:` の部分にDocker Hubのアカウント名を指定することができます。例えば [OpenFaaS](https://hub.docker.com/r/functions) のアカウントは `functions` という名前を使っているため、 `image: functions/hello-openfaas` としたいです。よって、 `--prefix="functions"` と指定することになります。

もし `--prefix` を指定しなかったとしても、あとからYAMLを直接編集することができます。

上のコマンドで以下の3つのファイルとディレクトリが作成されます：

```
./hello-openfaas.yml
./hello-openfaas
./hello-openfaas/handler.py
./hello-openfaas/requirements.txt
```

YAML(.yml)ファイルはCLIがfunctionのビルド、Dockerイメージのプッシュ、そしてデプロイをするための設定が記載されています。

> 注：KubernetesやリモートのOpenFaaSへfunctionをデプロイするときは、あらかじめfunctionをビルド後にプッシュしておく必要があります。
>
> このとき、gatewayのデフォルトのURL `127.0.0.1:8080` は `export OPENFAAS_URL=127.0.0.1:31112` することで環境変数で上書きすることができます。

YAMLの中身は以下のようになります：

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  hello-openfaas:
    lang: python3
    handler: ./hello-openfaas
    image: <Docker Hubのユーザー名>/hello-openfaas
```

* functionの名前は `functions` 直下のキーで指定します（例： `hello-openfaas` ）
* 開発言語は `lang` で指定します
* ビルドに使われるディレクトリは `handler` という名前になります。ファイルではなくディレクトリでなければいけません
* Dockerイメージの名前は `image` で指定します

`gateway` のURLはYAMLあるいはCLI（ `-g`, `--gateway` あるいは `OPENFAAS_URL` 環境変数）から上書きすることができます。

`handler.py` の中身は以下のとおり：

```python
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return req
```

このfunctionは流れてきた情報をそのまま返します。なので、 `echo` functionのようなものです。

ここでメッセージを `Hello OpenFaaS` にしてみましょう。

```
    return "Hello OpenFaaS"
```

標準出力に渡された値はすべて呼び出し元のプログラムに返されます。戻り値以外にも `print()` を使って標準出力からレスポンスを返す方法もあります。

以下がfunction開発時のデベロッパーのワークフローになります：

```
$ faas-cli up -f hello-openfaas.yml
```

このあとUI、CLI、 `curl` やアプリケーションからfunctionを呼び出すことになります。

functionには必ず以下のようなURLが割り振られます：

```
http://127.0.0.1:8080/function/<functionの名前>
http://127.0.0.1:8080/function/figlet
http://127.0.0.1:8080/function/hello-openfaas
```

> Tips：YAMLファイルを `stack.yml` に変更するとCLI実行時に `-f` フラグが不要になります。

functionは `GET` または `POST` でのみ呼び出すことができます。

* functionを呼び出してみよう

それでは `faas-cli invoke` を使ってfunctionを呼び出してみましょう。 `faas-cli invoke --help` で他のオプションも確認できます。



### astronaut-finder function（宇宙飛行士検索 function）を作ろう

これから `astronaut-finder` function（宇宙飛行士検索 function）を作ります。国際宇宙ステーション（ISS）にいる宇宙飛行士の名前をランダムに引っ張ってくるfunctionです。

```
$ faas-cli new --lang python3 astronaut-finder --prefix="<DockerHubのユーザー名>"
```

上のコマンドを実行すると３つのファイルが生成されます：

```
./astronaut-finder/handler.py
```

これはfunctionのハンドラです。 `req` オブジェクトには生のリクエストが渡ってくるので、これをコンソールに出力することができます。

```
./astronaut-finder/requirements.txt
```

`pip` モジュールとして含めておきたいモジュール名のリストです。例えば `requests` や `urllib` を記載します。

```
./astronaut-finder.yml
```

このファイルでfunctionの管理をします。functionの名前であったり、Dockerイメージ名や他にもカスタマイズしたい情報はここに記載します。

*  `./astronaut-finder/requirements.txt` に以下を記載しましょう

```
requests
```

これを記載することで、サードパーティの [requests](http://docs.python-requests.org/en/master/) というモジュールが必要だということを宣言します。HTTPで様々なWebサイトをアクセスするために使います。

* functionのコーディングをしましょう：

データはこちらから取得します: http://api.open-notify.org/astros.json

レスポンスのサンプルは以下のとおり:

```json
{"number": 6, "people": [{"craft": "ISS", "name": "Alexander Misurkin"}, {"craft": "ISS", "name": "Mark Vande Hei"}, {"craft": "ISS", "name": "Joe Acaba"}, {"craft": "ISS", "name": "Anton Shkaplerov"}, {"craft": "ISS", "name": "Scott Tingle"}, {"craft": "ISS", "name": "Norishige Kanai"}], "message": "success"}
```

 `handler.py` を編集しましょう:

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

> 注: この例では `req` を使いませんが、functionの引数としては残しておきます。

functionをビルドしましょう:

```
$ faas-cli build -f ./astronaut-finder.yml
```

> 注：astronaut-finder.ymlを `stack.yml` にリネームすることで、上のコマンドでは `-f` を省略することができます。CLIがデフォルトで探すファイルが `stack.yml`  であるためです。

functionをデプロイしましょう:

```
$ faas-cli deploy -f ./astronaut-finder.yml
```

functionを実行してみましょう：

```
$ echo | faas-cli invoke astronaut-finder
Anton Shkaplerov is in space

$ echo | faas-cli invoke astronaut-finder
Joe Acaba is in space
```

## トラブルシュート：コンテナのログを探そう

functionがいつごろ呼ばれたか、というのはコンテナのログから確認することができます：

```
$ docker service logs -f astronaut-finder
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:25 Forking fprocess.
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:26 Wrote 18 Bytes - Duration: 0.063269 seconds
```

## トラブルシュート： `write_debug` を使ってデバッグしてみよう

functionのログ出力を増やしてみましょう。functionのログを溢れさせないためにもこの機能はデフォルトでは無効化してあります。特にバイナリデータをレスポンスで返すfunctionなどでは、意味のない文字列が大量に出力されてしまうからです。

以下が通常のYAMLファイルです：

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

YAMLに「environment」のセクションを追加して以下のようにしましょう：

```yaml
  astronaut-finder:
    lang: python3
    handler: ./astronaut-finder
    image: astronaut-finder
    environment:
      write_debug: true
```

では、再び次のコマンドでデプロイします。  `faas-cli deploy -f ./astronaut-finder.yml`

functionを実行してからまたログを確認してみましょう：

```
$ docker service logs -f astronaut-finder
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:25 Forking fprocess.
astronaut-finder.1.szobw9pt3m60@nuc    | 2018/02/26 14:49:57 Query  
astronaut-finder.1.szobw9pt3m60@nuc    | 2018/02/26 14:49:57 Path  /function/hello-openfaas
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:26 Hello World
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:26 Duration: 0.063269 seconds
```

### 複数のfunctionの管理

CLIのYAMLでは複数のfunctionをグルーピングして一つのスタックとして管理することができます。こうすることで関連し合うfunctionを一元管理することができます。

2つのfunctionを作ってみて実際にみてみましょう:

```
$ faas-cli new --lang python3 first
```

2個目のfunctionでは `--append` フラグを使いましょう：

```
$ faas-cli new --lang python3 second --append=./first.yml
```

わかりやすくするために `first.yml` を `example.yml` にリネームしましょう。

```
$ mv first.yml example.yml
```

それでは中身をみてみましょう:

```
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

以下のフラグもfunctionを管理していく上で便利です：

* ビルドの並列実行：

```sh
$ faas-cli build -f ./example.yml --parallel=2
```

* ビルドまたはプッシュを一つのfunctionに絞り込む：

```sh
$ faas-cli build -f ./example.yml --filter=second
```

他にも `faas-cli build --help` や `faas-cli push --help` をCLIで実行することでオプションを確認することができます。

`faas-cli build && faas-cli push && faas-cli deploy` を一緒に実行するには `faas-cli up` を使ってください。

> 注: CLIがデフォルトで探しにいくファイルは `stack.yml` です。 `-f` パラメータでファイルを指定するのが煩わしい場合は活用しましょう。

デプロイ対象のfunctionのYAMLはHTTP(s)ごしでも指定することができます `faas-cli -f https://....`。

### サードパーティ製のテンプレートを使ってみよう

自分で作ったfunctionの言語テンプレートがある場合やPHPテンプレートのようにコミュニティが作ったテンプレートを見つけた場合、次のコマンドで使用することができます：

```
$ faas-cli template pull https://github.com/itscaro/openfaas-template-php

...

$ faas-cli new --list | grep php
- php
- php5
```

コミュニティで管理しているテンプレートの一覧は[OpenFaaS CLIのREADME](https://github.com/openfaas/faas-cli)に記載されています。

それでは、おまけのワークショップにこのまま進むか、次の [Lab 4](lab4.md) に進みましょう。

### カスタムバイナリをfunctionに (任意のワークショップ)

カスタムバイナリであったりコンテナをfunctionとして使うこともできます。ただし、ほとんどの場合すでに用意されている言語のテンプレートで要件は満たせるはずです。

カスタムバイナリまたはDockerfileを作るには言語に `dockerfile` を指定します：

```
$ faas-cli new --lang dockerfile sorter --prefix="<DockerHubのユーザー名>"
```

`sorter` というディレクトリと `sorter.yml` が生成されます。

`sorter/Dockerfile` を開いて `fprocess` の行を編集します。ここにbashの `sort` コマンドを記載しましょう。このfunctionで文字列の一覧を昇順に並べ替えることができます。

```
ENV fprocess="sort"
```

では build, push そして deployしましょう：

```
$ faas-cli up -f sorter.yml
```

UIまたはCLIからfunctionを実行しましょう：

```
$ echo -n '
elephant
zebra
horse
ardvark
monkey'| faas-cli invoke sorter

ardvark
elephant
horse
monkey
zebra
```

この例では [BusyBox](https://busybox.net/downloads/BusyBox.html) の `sort` を使いましたが、他にも `sha512sum` だったり `bash` やシェルスクリプトもあります。さらに、こういった元からあるバイナリだけでなく、どんなバイナリあるいはコンテナであってもOpenFaaSのwatchdogと連携することでサーバーレスfunctionになることができます。

> 注: OpenFaaSはWindowsバイナリもサポートしています。C#、VB、Powershellなどもfunctionで使えます

それでは [Lab 4](lab4.md) に進みましょう。
