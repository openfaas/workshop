# Lab 6 - functionでHTMLを扱ってみよう

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

このラボを始める前に作業用のディレクトリを作成しましょう：

```
$ mkdir -p lab6 \
   && cd lab6
```

## 簡単なHTMLをfunctionから返す

functionではHTMLを生成して返すことができます。また、ヘッダの `Content-Type` を `text/html` とすることも可能なので、ブラウザで表示させることもできます。HTMLを生成して返す簡単なfunctionを作ってみましょう。

```
$ faas-cli new --lang python3 show-html --prefix="<Docker Hubのユーザー名>"
```

`handler.py` を編集します:

```python
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    html = '<html><h2>Hi, from your function!</h2></html>'

    return html

```

これで呼び出し元にHTMLを返すことができます。続いて、 `Content-Type` を設定しましょう。このfunctionは必ずHTMLを返すので、 `Content-Type` は `text/html` にするべきです。これは `show-html.yml` の  `environment` で設定することができます。

`show-html.yml` を編集します：

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  show-html:
    lang: python3
    handler: ./show-html
    image: <Docker Hubのユーザー名>/show-html
    environment:
      content_type: text/html

```

`content_type` キーに設定した値が `Content-Type` としてレスポンスで設定されます。

それではfunctionのbuild, push, deployをしましょう：

```
$ faas-cli up -f show-html.yml
```

ブラウザを開いて http://127.0.0.1:8080/function/show-html にアクセスしましょう。functionで生成したHTMLが表示されているのが確認できます。

## HTMLファイルを読み込んで返すfunction

HTMLを配信したいとき、ほとんどの場合静的なHTMLをあらかじめ準備しているはずです。次のfunctionではHTMLファイルをfunctionのコンテナに内包して配信してみましょう。

まずはHTMLファイルを作ります。

`html` というディレクトリを作ってその中に `new.html` というファイルを作りましょう。次のような構造になります：

```
├── show-html
│   ├── __init__.py
│   ├── handler.py
│   ├── html
│   │   └── new.html
│   └── requirements.txt
└── show-html.yml
```

 `new.html`  を編集します：

```html
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>OpenFaaS</title>
</head>
<body>
  <h2>Here's a new page!</h2>
</body>
</html>
```

次に `handler.py` を以下のようにします：

```python
import os

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'html', 'new.html')

    with(open(path, 'r')) as file:
        html = file.read()

    return html

```

functionをbuild、push、deployしましょう：

```
$ faas-cli up -f show-html.yml
```

ブラウザを開いて http://127.0.0.1:8080/function/show-html にアクセスしましょう。ファイルであらかじめ用意していたHTMLが表示されるのが確認できます。

## クエリ文字列によって配信するHTMLを切り替える

functionからHTMLを配信する方法がわかったところで、動的に配信するHTMLをクエリ文字列で切り替える方法を試してみましょう。 [Lab 4](./lab4.md) で学んだように、クエリ文字列は `Http_Query` という環境変数で取得することができます。例えば以下のようにリクエストを受け取ったとします：

 http://127.0.0.1:8080/function/show-html?action=new

クエリ文字列は `action=new` なので、 `Http_Query` の値は `action=new` となります。さらに、 `urllib.parse` パッケージの `parse_qs` 関数を使うことで簡単にクエリ文字列をパースすることもできます。

まずは新たに `list.html` というファイルを作りましょう。ディレクトリ構造は以下のようになります：

```
├── show-html
│   ├── __init__.py
│   ├── handler.py
│   ├── html
│   │   ├── list.html
│   │   └── new.html
│   └── requirements.txt
└── show-html.yml
```

 `list.html` を編集します：

```html
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>OpenFaaS</title>
</head>
<body>
  <h2>This is a list!</h2>
  <ul>
    <li>One</li>
    <li>Two</li>
    <li>Three</li>
  </ul>
</body>
</html>
```

`handler.py` を編集します： 

```python
import os
from urllib.parse import parse_qs

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    query = os.environ['Http_Query']
    params = parse_qs(query)
    action = params['action'][0]

    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'html', action + '.html')

    with(open(path, 'r')) as file:
        html = file.read()

    return html
```

functionをbuild、push、deployしましょう：

```
$ faas-cli up -f show-html.yml
```

ブラウザを開いてまずは以下にアクセスしましょう：

http://127.0.0.1:8080/function/show-html?action=new

「Here's a new page!」というページが先程のセクションと同じように表示されます。次に以下にアクセスします：

http://127.0.0.1:8080/function/show-html?action=list

リストを表示するページが確認できます。

## 他のfunctionとの組み合わせ

最後に、HTML、JavaScriptとAjaxを組み合わせて、他のfunctionをどのように利用できるか見てみましょう（ *figlet* functionを使います）。

まず、 `figlet.html` というファイルを作ります。ディレクトリ構造は以下のようになります：

```
├── show-html
│   ├── __init__.py
│   ├── handler.py
│   ├── html
│   │   ├── figlet.html
│   │   ├── list.html
│   │   └── new.html
│   └── requirements.txt
└── show-html.yml
```

`figlet.html` を編集します：

```html
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>OpenFaaS</title>
  <script
  src="https://code.jquery.com/jquery-3.3.1.min.js"
  integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
  crossorigin="anonymous"></script>
  <style>
    .result {
        font-family: 'Roboto Mono', monospace;
    }
    </style>
</head>
<body>
  <h2>Figlet</h2>
  <p>
    Text: <input type="text" name="text" id="text"> 
    <button id="generate">Generate</button>
  </p>
  
  <textarea class="result" cols="80" rows="10"></textarea>

  <script type="text/javascript">
    $(function(){
      // Generate button click
      $('#generate').on('click', function() {
        // Execute ajax request
        $.ajax({
          url:'./figlet',
          type:'POST',
          data:$('#text').val()
        })
        .done(function(data) {
          // ajax success
          $('.result').val(data);
          console.log(data);
        })
        .fail(function(data) {
          // ajax failure
          $('.result').val(data);
          console.log(data);
        });
      });
    });
  </script>
</body>
</html>
```

JavaScriptについてあまりわからない人も気にしないでください。このページでやっていることは：

* `input` に文字を入力して
* `Generate` ボタンを押して
* `figlet` functionのエンドポイント（ `/function/figlet` ）にリクエストを投げて
* 結果を `textarea` に反映する

前のセクションで配信するHTMLを動的に切り替えられるようにしているので、 `handler.py` を編集する必要はありません。ただし、追加で配信するHTML（ `figlet.html` ）をイメージに内包する必要があるので、buildとpushは必要になります。

それではfunctionのbuild、push、deployをしましょう：

```
$ faas-cli up -f show-html.yml
```

ここでは [Lab 2](./lab2.md) での *figlet* functionをデプロイ済みであるとします。

ブラウザを開いて以下にアクセスします：

http://127.0.0.1:8080/function/show-html?action=figlet

「Figlet」のページが表示されるはずです。何かしらの**英数字**を入力して「Generate」ボタンを押します。 `input` に入力した文字列がfiglet（文字のアスキーアート）となって `textarea` に反映されるはずです。このサンプルは非常に簡単な例になりますが、応用することでSPA（Single Page Application）をfunctionで作ることも可能になります。

このLabではfunctionからHTMLを配信し、 `Content-Type` も設定する方法について学びました。さらに、HTML + JavaScriptを使って他のfunctionを呼び出し、動的なページを作る方法についても学びました。

それでは [Lab 7](lab7.md) に進みましょう。