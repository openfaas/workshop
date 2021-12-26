# 实验 6--你的函数的 HTML

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

在开始这个实验之前，为你的文件创建一个新的文件夹。

```plain
$ mkdir -p lab6\
   && cd lab6
```

## 从一个函数中生成并返回基本的 HTML

函数可以返回 HTML，并将`Content-Type`设置为`text/html`。因此，函数返回的 HTML 可以通过浏览器进行渲染。让我们创建一个简单的函数，生成并返回一个基本的 HTML。

```plain
$ faas-cli new --lang python3 show-html --prefix="<your-docker-username-here>"
```

编辑`handler.py`。

```python
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    html = '<html><h2>Hi, from your function!</h2></html>'

    return html
```

这将返回 HTML 给调用者。 还有一件事我们应该做的是设置响应的`Content-Type'。我们100%确定这个函数将返回一个HTML，所以`Content-Type`应该总是`text/html`。我们可以利用`show-html.yml`文件中的`environment`部分来设置。

编辑`show-html.yml`。

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  show-html:
    lang: python3
    handler: ./show-html
    image: <your-docker-username-here>/show-html
    environment:
      content_type: text/html

```

`environment`中的`content_type`键将设置响应的`Content-Type`。

现在构建、推送和部署该函数。

```sh
$ faas-cli up -f show-html.yml
```

运行以下程序以获得函数的 URL。

```sh
faas-cli describe -f show-html.yml show-html

URL: http://127.0.0.1:8080/function/show-html
```

HTML 应该被正确渲染。

## 从磁盘上读取并返回一个静态的 HTML 文件

一般来说，当你提供 HTML 服务时，你有一个静态的 HTML 文件在前面。让我们看看我们如何在函数中打包 HTML 文件，并从 HTML 文件中提供内容。

首先，让我们创建一个 HTML 文件。

创建一个名为`html`的目录，并放置一个名为`new.html`的文件，使其结构看起来像下面这样。

```plain
├── show-html
│   ├── __init__.py
│   ├── handler.py
│   ├── html
│   │   └── new.html
│   └── requirements.txt
└── show-html.yml
```

Edit `new.html` :

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

现在把你的`handler.py`改为以下内容。

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

现在构建、推送和部署该函数。

```plain
$ faas-cli up -f show-html.yml
```

打开你的浏览器，访问http://127.0.0.1:8080/function/show-html。你应该看到一个 `这里有一个新的页面！` 在浏览器中呈现的 HTML 页面。

现在我们要为这个函数的 URL 添加一个路径。

在`html`文件夹中添加新的`list.html`文件，内容如下。

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

将你的`handler.py`编辑成以下内容。

```python
import os

def handle(req):
    
    path = os.environ['Http_Path']
    pathArr = path.split("/")
    pageName = pathArr[1]
    
    dirname = os.path.dirname(__file__)
    page = os.path.join(dirname, 'html', pageName + '.html')

    with(open(page, 'r')) as file:
        html = file.read()

    return html
```

构建、推送和部署该函数。

```plain
$ faas-cli up -f show-html.yml
```

现在在http://127.0.0.1:8080/function/show-html/new 或 http://127.0.0.1:8080/function/show-html/list 上打开你的网页。
这将输出。
```html
<h2>Here's a new page!</h2>
```
and
```html
<h2>This is a list!</h2>
  <ul>
    <li>One</li>
    <li>Two</li>
    <li>Three</li>
  </ul>
```

## 读取查询字符串并返回不同的 HTML

现在我们已经了解了如何通过函数来提供 HTML，让我们动态地改变通过查询字符串提供的 HTML。正如我们在[实验室 4](./lab4.md)中学到的，查询字符串可以通过一个叫做`Http_Query`的环境变量来检索。假设我们做了一个看起来像这样的查询。

 http://127.0.0.1:8080/function/show-html?action=new

查询字符串是`action=new`，因此`Http_Query`的值将是`action=new`。我们也可以使用`urllib.parse`包中的`parse_qs`函数，轻松解析这个查询字符串。

我们的函数的目录结构看起来是这样的。

```plain
├── show-html
│   ├── __init__.py
│   ├── handler.py
│   ├── html
│   │   ├── list.html
│   │   └── new.html
│   └── requirements.txt
└── show-html.yml
```


改变你的`handler.py`。

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

现在构建、推送和部署该函数。

```plain
$ faas-cli up -f show-html.yml
```

打开你的浏览器，首先访问。

http://127.0.0.1:8080/function/show-html?action=new

你应该看到 `这里有一个新的页面！`就像你在上一节看到的那样。现在访问。

http://127.0.0.1:8080/function/show-html?action=list

你应该看到一个显示列表的 HTML。

## 与其他函数协作

最后，让我们看看如何利用 JavaScript 和 Ajax 的优势，从 HTML 函数中与另一个函数（例如*figlet*函数）协作。

首先，让我们再创建一个名为`figlet.html`的 HTML 文件。所以现在的结构应该是这样的。

```plain
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

编辑`figlet.html`。

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

如果你不太了解 JavaScript，请不要担心。这个页面所做的就是。

* 在 `input`中输入文字
* 按下 `生成`按钮
* 创建一个 Ajax 请求到*figlet*函数端点（`/function/figlet`）。
* 将结果应用到 `textarea` 中。

没有必要改变`handler.py`，因为它可以动态地提供上一节中的 HTML。尽管没有改变`handler.py`，我们还是需要构建和推送函数镜像，因为我们需要在函数容器中打包新的`figlet.html`。

现在构建、推送和部署这个函数。

```plain
$ faas-cli up -f show-html.yml
```

本节假设你已经部署了[实验室 2](./lab2.md)中的*figlet*函数。 

打开你的浏览器，首先访问。

http://127.0.0.1:8080/function/show-html?action=figlet

你应该看到 `Figlet` 页面，并且应该看到一个输入。输入任何你想输入的文本，然后点击 `生成` 按钮。如果请求成功，`textarea` 应该包含你在 `input` 中输入的 figlet。这是一个微不足道的例子，但通过使用这种技术，你甚至可以用函数创建强大的 SPA（单页应用程序）。

在这个实验室中，你学到了如何从你的函数中提供 HTML，并设置响应的`Content-Type`。此外，你还学会了如何用 HTML+JavaScript 调用其他函数，以及用函数创建动态页面。

现在进入[实验室 7](lab7.md)
