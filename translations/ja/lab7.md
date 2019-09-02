# Lab 7 - 非同期 function

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

このラボを始める前に作業用のディレクトリを作成しましょう：

```
$ mkdir -p lab7 \
   && cd lab7
```

## 非同期 vs 同期 function

同期的にfunctionを実行した場合、gatewayとfunctionは実行時間の間ずっとコネクションを張っています。同期的な呼び出しは*ブロック* が発生します。なので、呼び出し元のクライアントはfunctionが完了するまで一時停止状態になってしまいます。

* gatewayは `/function/<function名>` というURLを使います
* クライアントは実行が完了するまで待たなければいけません
* 実行完了とともに結果がもらえます
* 成功したかどうかはその場でわかります

非同期な呼び出しは似たような動きをしますが、次の点が異なります：

* gatewayのURLは `/async-function/<function名>` 
* クライアントはfunctionの実行後すぐに *202 Accepted* をgatewayから受け取ります
* functionはqueue-workerを通して後で実行されます
* デフォルトでは結果は破棄されます

簡単なデモを試してみましょう。

```
$ faas-cli new --lang dockerfile long-task --prefix="<DockerHubのユーザー名>"
```

`long-task/Dockerfile` を開いてfprocessを `sleep 1` に変更しましょう。

build, deployしてfunctionを次のように10回、同期的に実行しましょう：

```
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
echo -n "" | faas-cli invoke long-task
```

それでは次に10回非同期に実行しましょう：

```
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
echo -n "" | faas-cli invoke long-task --async
```

いかがでしたか？最初の例は10秒ほどかかり、次の例は1秒もかからなかったのではないでしょうか。実行自体は10x1秒かかりますが、実行する責任はキューに委譲されています。

非同期functionはすぐに実行しなくても良い、あるいはクライアント側で結果が必要ない場合に有用です。

> 良い例として、Githubのwebhookについて考えてみましょう。Github側からはコネクションの長さに制限があるかもしれませんが、非同期functionを使うことでレスポンスをすぐに返すことができます。

## queue-worker のログを見てみよう

OpenFaaSのデフォルトのスタックはキューや非同期実行のためにNATS Streamingを採用しています。以下のコマンドでログを参照できます：

```
docker service logs -f func_queue-worker
```

## requestbinやngrokで `X-Callback-Url` を活用してみよう

非同期functionの結果が必要な場合もあります。それには次の2種類の方法が可能です：

* functionの挙動として、最後に何かしらのエンドポイントやメッセージングシステムに結果を通知させる

このやり方がかならずしも良いとは限りませんし、追加のコーディングが必要になります。

* OpenFaaSの標準機能であるコールバックの仕組みを使う

OpenFaaSのコールバックの仕組みを使うことで、非同期functionを実行するqueue-workerが自動的に指定されたURLに結果を通知することができます。

それではrequestbinを使って新しい「bin」を作ってみましょう。requestbinはインターネット上でリクエストを受け取れるサービスです。

https://requestbin.com/

「Bin URL」をコピーして次のように呼び出してみましょう。

例えば `http://requestbin.com/r/1i7i1we1` の場合

```
$ echo -n "LaterIsBetter" | faas-cli invoke figlet --async --header "X-Callback-Url=http://requestbin.com/r/1i7i1we1"
```

呼び出し後、requestbinのページをリフレッシュしましょう。次のように `figlet` の結果が表示されます：

```
 _          _           ___     ____       _   _            
| |    __ _| |_ ___ _ _|_ _|___| __ )  ___| |_| |_ ___ _ __ 
| |   / _` | __/ _ \ '__| |/ __|  _ \ / _ \ __| __/ _ \ '__|
| |__| (_| | ||  __/ |  | |\__ \ |_) |  __/ |_| ||  __/ |   
|_____\__,_|\__\___|_| |___|___/____/ \___|\__|\__\___|_|   
                                                            
```

> 注： `X-Callback-Url` には違うfunctionを指定することもできます。この仕組みを使えば完了時にSlackやEmailに非同期functionの結果を通知することができます。違うfunctionを呼ぶには `X-Callback-Url` に `http://gateway:8080/function/<function名>` を設定します。

それでは [Lab 8](lab8.md) に進みましょう。