# Lab 2 - OpenFaaSを試してみよう

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

このラボを始める前に作業用のディレクトリを作成しましょう：

```
$ mkdir -p lab2 \
   && cd lab2
```

## UIを使ってみよう

デプロイが完了したところで http://127.0.0.1:8080 にアクセスすることでOpenFaaSのUIが表示されます。

> 注：`localhost` ではなく `127.0.0.1` を使っている点に注意してください。Linuxの環境によっては `localhost` ではIPv4/IPv6の競合が原因で固まることがあるためです。

下のコマンドでサンプルのfunctionをデプロイすることができます：

```
$ faas-cli deploy -f https://raw.githubusercontent.com/openfaas/faas/master/stack.yml
```

![](../../screenshot/markdown_portal.png)

これらはUIから直接試すことができます。例えばMarkdown functionを試してみましょう。MarkdownがHTMLに変換されます。

*Request*のフィールドに以下を入力しましょう：

```
## The **OpenFaaS** _workshop_
```

では、 *Invoke* ボタンを押して Response body を確認しましょう。下のようなレスポンスが表示されるはずです。

```
<h2>The <strong>OpenFaaS</strong> <em>workshop</em></h2>
```

他にも次のフィールドを見てみましょう：

* Status - functionが実行可能な状態かどうか。この状態がReadyでない限りfunctionはUIから呼び出せません。
* Replicas - Swarmのクラスタに存在しているfunctionのレプリカの数
* Image - Docker HubあるいはDockerリポジトリに置いているDockerイメージの名前
* Invocation count - これはfunctionが呼び出された回数を表示しており、5秒毎に更新しています

何度か *Invoke* してみて *Invocation count* が増えていくのを確認してみてください。



## Function Storeからデプロイ

OpenFaaSのFunction storeからもfunctionをデプロイすることができます。storeはコミュニティによって集められたfunctionのコレクションです。（もちろん、無料です）

* *Deploy New Function* をクリック
* *From Store* が選択されていることを確認
* *Figlet* というfunctionを選択（検索バーからも絞込ができます）して *Deploy* をクリック

左のfunction一覧に Figlet functionが表示されます。Docker Hubからのダウンロードが終わるまでしばらく待ってから、何か半角文字列を入力してMarkdown functionのときみたいに *Invoke* をクリックしてみましょう。

下のようなASCIIロゴが生成されるはずです（ `100%` と入力した場合）：

```
 _  ___   ___ _  __
/ |/ _ \ / _ (_)/ /
| | | | | | | |/ / 
| | |_| | |_| / /_ 
|_|\___/ \___/_/(_)
```

## OpenFaaSのCLIについて

CLIについて見ていこうと思いますが、その前にgatewayのURLについて：

もし http://127.0.0.1:8080 にOpenFaaSのgatewayをデプロイしていない場合はCLIにその場所を教える必要があります。以下のいずれかの方法で設定できます：

1. `OPENFAAS_URL` 環境変数を設定することで、同一セッション内であれば `faas-cli` はその値を参照します。例えば：  `export OPENFAAS_URL=http://openfaas.endpoint.com:8080`
2. `faas-cli` のオプションとして `-g` または `--gateway` を指定することができます： `faas deploy --gateway http://openfaas.endpoint.com:8080`
3. デプロイに使うYAML内で`provider:` の下の `gateway:` の値で設定することもできます。

### デプロイしたfunctionを一覧表示

下のコマンドを入力することでfunctionの一覧とともにレプリカの数や呼び出し回数を表示できます。

```
$ faas-cli list
```

*markdown* functionであれば `markdown` 、さらには *figlet* functionも呼び出し回数とともに表示されるはずです。

それでは `verbose` フラグを試してみましょう

```
$ faas-cli list --verbose
```

または

```
$ faas-cli list -v
```

このオプションでDockerイメージ名も表示されるようになります。

### function呼び出し

それでは `faas-cli list` で表示されたfunctionをどれか選択してみましょう（ここでは `markdown` にします：

```
$ faas-cli invoke markdown
```

ここで、何か文字列を入力するように促されます。何かを入力して Control+D を押します。

他にも `echo` や `uname -a` を `invoke` のインプットとしてパイプすることができます。

```sh
$ echo Hi | faas-cli invoke markdown

$ uname -a | faas-cli invoke markdown
```

さらにはこのLabのmarkdownもHTMLに変換することだってできます：

```sh
$ git clone https://github.com/openfaas/workshop \
   && cd workshop

$ cat lab2.md | faas-cli invoke markdown
```

## モニタリング用のダッシュボード

OpenFaaSはPrometheusでメトリクスを測定しています。これらのメトリクスは [Grafana](https://grafana.com) などのオープンソースツールを使うことで可視化することができます。

下のコマンドでGrafanaをデプロイしてみましょう：

```bash
$ docker service create -d \
--name=grafana \
--publish=3000:3000 \
--network=func_functions \
stefanprodan/faas-grafana:4.6.3
```

サービスの作成が完了したらGrafanaをブラウザで開いてみましょう。ユーザー名 `admin` 、パスワードも `admin` で下のダッシュボードにアクセスしてみましょう：

http://127.0.0.1:3000/dashboard/db/openfaas


<a href="https://camo.githubusercontent.com/24915ac87ecf8a31285f273846e7a5ffe82eeceb/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f4339636145364358554141585f36342e6a70673a6c61726765"><img src="https://camo.githubusercontent.com/24915ac87ecf8a31285f273846e7a5ffe82eeceb/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f4339636145364358554141585f36342e6a70673a6c61726765" width="600px" /></a>

*Grafanaを使ってOpenFaaSのメトリクスを可視化した様子*

それでは [Lab 3](./lab3.md) に進みましょう。
