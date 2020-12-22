# OpenFaaSワークショップ

このワークショップではOpenFaaSの使い方（functionのビルドからデプロイまで）を自分のペースで学んでいくことができます。

![](https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png)

> このワークショップではまずローカルの開発環境にDocker for MacあるいはWindowsを使ってOpenFaaSをデプロイします。その次にPythonで作ったServerless functionをビルド、デプロイして実際に実行します。ここで扱うトピックとしては、pipを使った依存パッケージの管理、シークレットでAPIトークンを扱う方法、Prometheusでfunctionを監視、非同期に複数のfunctionを実行してアプリケーションを作る方法です。最後にIFTTT.comのイベントストリームに繋ぎます。これによってボットや自動返信機能、ソーシャルメディアやIoT機器との連携が可能になります。

## 必要なもの:

ここに記載している内容は [Lab 1](./lab1.md) で詳しく説明しますが、インストラクターが指導するワークショップに参加される場合はあらかじめ準備しておいてください。

* ワークショップで作成するfunctionはPythonで書きます。よって、プログラミングやスクリプト経験があることが推奨されます。
*  [VSCode](https://code.visualstudio.com/download) のようなエディタをインストールしてください。
* Windowsであれば [Git Bash](https://git-scm.com/downloads) をインストールしてください。
* 推奨OS：MacOS、Windows 10 Pro/Enterprise、Ubuntu Linux

Docker：

* Docker CE for [Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)/[Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows) **Edge edition**
* Docker CE for Linux

> 注: もし上記の環境が準備できない場合は代替手段としては https://labs.play-with-docker.com/ で動作確認することができます。

## インストラクター指導型のワークショップ

インストラクターが指導するワークショップではOpenFaaSのSlackへの招待リンクが共有されます。Slackの指定されたチャンネルをワークショップでのディスカッションや質問、提案などに活用してください。

## [Lab 1 - まずはOpenFaaSの準備](./lab1.md)

* 必要なものをインストール
* Docker Hubのアカウントについて
* OpenFaaS CLI
* OpenFaaSをデプロイ

## [Lab 2 - OpenFaaSを試してみよう](./lab2.md)

* UIを使ってみよう
* Function Storeからデプロイ
* OpenFaaSのCLIについて
* Prometheusのメトリクスについて

## [Lab 3 - はじめてのfunction](./lab3.md)

* 新規functionの生成またはscaffold（スキャフォールド）について
* astronaut-finder function（宇宙飛行士検索 function）を作ろう
  * 依存パッケージを `pip` で追加しよう
  * トラブルシュート：コンテナのログを探そう
* トラブルシュート： `write_debug` を使ってデバッグしてみよう
* サードパーティ製のテンプレートを使ってみよう

## [Lab 4 - functionについてさらに掘り下げてみよう](./lab4.md)

* 環境変数で任意の値を注入
  * deploy時のyamlで指定
  * クエリ文字列やヘッダなどのHTTPコンテキストで動的に指定
* ログの活用方法
* ワークフローを作ってみよう
  * クライアント側でfunctionを連鎖させよう
  * function内で別のfunctionを呼び出してみよう

## [Lab 5 - Gitbotを作ろう](./lab5.md)

> `issue-bot` というGithubのIssueに自動返信するボットを作ります

* GitHubのアカウントを取得
* ngrokでトンネルを作る
* webhookを受け取れる `issue-bot` を作る
* Sentiment Analysis functionのデプロイ
* GitHub APIを使ってラベルを適用する方法
* functionの仕上げ

## [Lab 6 - functionでHTMLを扱ってみよう](./lab6.md)

* 簡単なHTMLをfunctionから返す
* HTMLファイルを読み込んで返すfunction
* 他のfunctionとの組み合わせ

## [Lab 7 - 非同期 function](./lab7.md)

* 非同期 vs 同期 function
* queue-worker のログを見てみよう
* requestbinやngrokで `X-Callback-Url` を活用してみよう

## [Lab 8 - 応用編 - タイムアウト](./lab8.md)

* `read_timeout` でタイムアウトを調整しよう
* 動作時間の長いfunctionに適応しよう

## [Lab 9 - 応用編 - functionのオートスケール](./lab9.md)

> オートスケールを実際に発火させよう

* レプリカの最小数、最大数について
* Prometheusでの確認
* Prometheusのクエリを確認
* functionをcurlで繰り返し呼び出す
* オートスケールを監視

## [Lab 10 - 応用編 - secretの使い方](./lab10.md)
* issue-botでsecretを使うようにしよう
  * のsecretを作ろう
  * functionからsecretにアクセスしよう

[Lab 1](lab1.md) から順番に進めていくことができます。

## OpenFaaSの削除方法

OpenFaaSが必要なくなった場合に、削除する方法は [こちら](https://github.com/openfaas/faas/blob/master/guide/troubleshooting.md#stop-and-remove-openfaas) にまとめてあります。

## おわりに

インストラクターが指導するワークショップであればここからQ&Aの時間とし、他にもさらなる応用トピックについて話しましょう。

* functionのオートスケール
* セキュリティについて
  * TLS / Basic認証
* オブジェクトストレージ
* テンプレートのカスタマイズ方法

他にも [appendix](./appendix.md) の追加情報も合わせて参考にしてください。

## 謝辞

このワークショップの作成やテストに協力していただけた @iyovcheva, @BurtonR, @johnmccabe, @laurentgrangeau, @stefanprodan, @kenfdev, @templum, rgee0 に心より感謝します。
