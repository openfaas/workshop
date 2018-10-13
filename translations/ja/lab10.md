# Lab 10 - 応用編 - secretの使い方

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

このラボを始める前にlab5からコピーを作成しましょう。

```
$ cp -r lab5 lab10 \
   && cd lab10
```

[Lab 5](./lab5.md) では `issue-bot` がGitHubの *Personal Access Token* を環境変数（ `auth_token` ）から取得する方法についてみました。違う方法として **secret** を使って機密性の高い情報を扱うやり方があります。

Dockerのドキュメントでは：

> .. a secret is a blob of data, such as a password, SSH private key, SSL certificate, or another piece of data that should not be transmitted over a network or stored unencrypted in a Dockerfile or in your application’s source code.

と書かれているように、機密性の高いデータを平文で扱いたくない場合に環境変数の代替として **secret** を使うことができます。環境変数は簡単に使えるのですが、機密性の低いデータを使う場合だけに使用されるべきです。 `auth_token` の値はといえば、 **secret** で保護するべきデータになります。

## secretの作成

> secretの名前にアンダースコア（_）を使用することは非推奨です。Docker SwarmからKubernetesへの移行もスムーズに行えるように使用は控えましょう。

ターミナルで次のコマンドを実行します（ `auth_token` には実際のトークンの値を入れてください）：

```
$ echo -n <auth_token> | docker secret create auth-token -
```

secretが作られたことを確認します：

```
$ docker secret inspect auth-token
```

> 注：functionを（ローカル環境ではなく）リモートのgatewayにデプロイする場合は、そのリモートの環境にsecretを作ってください。

secretが作られてfunctionにマウントされると `/var/openfaas/secrets/auth-token` というファイルになります。これを `handler.py` で読み込んでGitHubの *Personal Access Token* を取得することができます。

## issue-bot.ymlを更新

`env.yml` を参照していた箇所をやめて、以下のように `auth-token` というsecretがfunctionで使える設定に変更します：

```yml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  issue-bot:
    lang: python3
    handler: ./issue-bot
    image: <Docker Hubのユーザー名>/issue-bot
    environment:
      write_debug: true
      gateway_hostname: "gateway"
      positive_threshold: 0.25
    secrets:
      - auth-token

```

## `issue-bot` functionの更新

functionのハンドラも `auth-token` というsecretを使うようにロジックを変更する必要があります。これは簡単で、次の1行を変更するだけです：

```python
g = Github(os.getenv("auth_token"))
```
を以下に置き換えます：
```python
with open("/var/openfaas/secrets/auth-token","r") as authToken:  
    g = Github(authToken.read())
```

> 完全なソースコードは [issue-bot-secrets/bot-handler/handler.py](../../issue-bot-secrets/bot-handler/handler.py) で確認することができます。

* build、push、deployしましょう

```
$ faas-cli up -f issue-bot.yml
```

それでは [目次](./README.md) に戻りましょう。