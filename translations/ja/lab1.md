# Lab 1 - まずはOpenFaaSの準備

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

OpenFaaSはDocker SwarmやKubernetesといった様々なプラットフォーム上で動きます。このワークショップではローカルの環境でDocker Swarmを使います。

どんなOpenFaaSのfunctionであっても基礎となるのはDockerイメージです。これは `faas-cli` を活用することで容易にビルドすることができます。

## 必要なもの

### Docker

Mac

* [Docker CE for Mac Edge Edition](https://store.docker.com/editions/community/docker-ce-desktop-mac) をインストール

Windows

* Windows 10 ProまたはEnterprise

* [Docker CE for Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows) をインストール

* [Git Bash](https://git-scm.com/downloads) をインストール

  > 注：このワークショップではWSL(Windows Subsystem for Linux)やBash for Windowsではなく、Git Bashを使うことを強くおすすめします。

Linux - UbuntuまたはDebian

* Docker CE for Linux

  > 注： [Docker Store](https://store.docker.com) からDocker CEをインストールできます。



> 注：上のどの方法も用意できない場合は https://labs.play-with-docker.com/ でワークショップを進めていくことができます。

### シングルノードのクラスタをセットアップ

##### Docker Swarm

OpenFaaSはKubernetesとDocker Swarmどちらでも動きますが、ワークショップのイベントなどではDocker Swarmを使うことが多いかと思います。というのも、Docker Swarmの方がセットアップや使用するのが簡単だからです。公式ドキュメントにはKubernetesとDocker Swarm両方のクラスタを構築する方法が [載っています](https://github.com/openfaas/faas/tree/master/guide) 。

それではまずはローカルあるいはVM環境でシングルノードのDocker Swarmをセットアップします：

```
$ docker swarm init
```

> もしエラーが起きる場合は `--advertise-addr` と環境のIPを指定してください

##### Kubernetes

Kubernetes上で構築したOpenFaaSでもこのワークショップを進めていくことができます。ただし、読み替えが必要な箇所が少しあります。例えば、OpenFaaSのgatewayサービスのアドレスは `http://gateway:8080` ではなく、 `http://gateway.openfaas:8080` になります。

また、gatewayに `NodePort` を使用している場合はOpenFaaSのCLIからアクセスする場合は http://IP_ADDRESS:31112/ としてください。

### Docker Hub

[Docker Hub](https://hub.docker.com)のアカウントが必要になりますので登録してください。Docker Hubを使うことでDockerイメージをインターネット上に公開してマルチノードクラスタで使ったり、世界中の様々なコミュニティ向けに容易に共有できるようになります。このワークショップではDocker Hub上にfunctionを公開します。

Docker Hubのアカウント登録は [こちら](https://hub.docker.com) から行います。

> 注：Docker Hubを使うことでDockerイメージのビルドを自動化することも可能です。

ターミナルまたはGit Bashを開き下記コマンドを実行します。Docker Hubに登録した認証情報でログインします。

```
$ docker login
```

> 注：コミュニティからのアドバイス - Windowsで上記コマンドを実行してエラーが発生する場合は、タスクバーのDocker for Windowsアイコンをクリックして「Sign in / Create Docker ID」からログインしてください。

### OpenFaaS CLI

OpenFaaS CLIはMacであれば `brew` でインストールできますし、MacやLinuxであれば下記コマンドでインストールできます：

```
# MacOS users may need to run "bash" first if this command fails
$ curl -sL cli.openfaas.com | sudo sh
```

Windowsを使用している場合は [こちらのリリースページ](https://github.com/openfaas/faas-cli/releases) から最新の `faas-cli.exe` をダウンロードしてください。ローカルのディレクトリに格納してもいいいですし、 `C:\Windows\` 配下に置いてコマンドプロンプトから使えるようにしておくこともできます。

> Windowsを使い慣れている方であれば、CLIを格納したディレクトリをPATH環境変数に追加するのも一つの方法です。

このワークショップでは `faas-cli` を使って新規functionの作成、ビルド、デプロイ、そして呼び出しも行います。CLIで使えるコマンドは `faas-cli --help` でも確認可能です。

`faas-cli` を試してみましょう

ターミナルまたはGit Bashを開いて以下のコマンドを実行します：

```
$ faas-cli help
$ faas-cli version
```

### OpenFaaSをデプロイ

以下のコマンドを使えば約60秒で簡単にOpenFaaSがデプロイできます。：

* まずはリポジトリをクローンします:

```
$ git clone https://github.com/openfaas/faas
```

* 最新版をチェックアウトします

```
$ cd faas && \
  git checkout master
```

> 注: 最新版のリリースに関しては [release page](https://github.com/openfaas/faas/releases) で確認できます。

* Docker Swarmでスタックをデプロイします：

```
$ ./deploy_stack.sh --no-auth
```

もしイベントに参加しながら上記コマンドを実行した場合はDockerイメージのpullなどに数分かかる可能性があります。

以下のコマンドを実行した場合に画面上に `1/1` が出ていることと、 `running` ステータスであることを確認してください：

```
$ docker service ls
```

もし何か問題が発生する場合は [Docker Swarmのデプロイ手順(英語)](https://github.com/openfaas/faas/blob/master/guide/deployment_swarm.md) を確認してみてください。

それでは [Lab 2](./lab2.md) に進みましょう。