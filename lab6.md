# Lab 6 - HTML for your functions

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

Before starting this lab, create a new folder for your files:

```
$ mkdir -p lab6 \
   && cd lab6
```

## Generate and return basic HTML from a function

Functions can return HTML and also set the `Content-Type` to `text/html`. Hence the HTML returned by the function can be rendered via a browser. Let's create a simple function who generates and returns a basic HTML.

```
$ faas-cli new --lang python3 show-html --prefix="<your-docker-username-here>"
```

Edit `handler.py`:

```python
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    html = '<html><h2>Hi, from your function!</h2></html>'

    return html
```

This will return HTML to the caller.  One more thing we should do is to set the `Content-Type` of the response. We are 100% sure that this function will return an HTML so the `Content-Type` should always be `text/html`. We can set this by taking advantage of the `environment` section of the `show-html.yml` file.

Edit `show-html.yml`:

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

The `content_type` key inside `environment` will set the `Content-Type` of the response.

Now build, push and deploy the function:

```sh
$ faas-cli up -f show-html.yml
```

Run the following to get the function URL:

```sh
faas-cli describe -f show-html.yml show-html

URL: http://127.0.0.1:8080/function/show-html
```

The HTML should be properly rendered.

## Read and return a static HTML file from disk

Typically, when you serve HTML you have a static HTML file upfront. Let's see how we can pack HTML file inside the function and serve the contents from the HTML file.

First, let's create a HTML file:

Create a directory called `html` and put a file called `new.html` so that the structure looks like as follows:

```
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

Now change your `handler.py` to the following:

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

Now build, push and deploy the function:

```
$ faas-cli up -f show-html.yml
```

Open your browser and access http://127.0.0.1:8080/function/show-html. You should see a "Here's a new page!" HTML page rendered in the browser.

Now we're going to add a path to the function URL.

Inside `html` folder add new `list.html` file with this content:

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

Edit your `handler.py` to the following:

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

Build, push and deploy the function:

```
$ faas-cli up -f show-html.yml
```

Now open your web page on http://127.0.0.1:8080/function/show-html/new or http://127.0.0.1:8080/function/show-html/list.
This will output:
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

## Read the query string and return different HTML

Now that we've understood how to serve html via functions, let's dynamically change the HTML to serve via query strings. As we learned in [Lab 4](./lab4.md), query strings can be retrieved via an environment variable called `Http_Query`. Suppose we made a query that looks like this:

 http://127.0.0.1:8080/function/show-html?action=new

The query string is `action=new`, hence the value of `Http_Query` would be `action=new`. We can also use the `parse_qs` function from the `urllib.parse` package and easily parse this query string.

The structure of the directory of our function looks like this:

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


Change your `handler.py`: 

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

Now build, push and deploy the function:

```
$ faas-cli up -f show-html.yml
```

Open your browser and first access:

http://127.0.0.1:8080/function/show-html?action=new

You should see the "Here's a new page!" as you saw in the previous section. Now access:

http://127.0.0.1:8080/function/show-html?action=list

You should see a HTML showing a list.

## Collaborate with other functions

Finally, let's see how we can collaborate with another function (e.g. the *figlet* function) from the HTML function by taking advantage of JavaScript and Ajax.

First of all, let's create another HTML file called `figlet.html`. So the structure should look like the following now:

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

Edit`figlet.html`:

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

Don't worry if you don't understand JavaScript much. All this page does is:

* Type text inside the `input`
* Press the `Generate` button
* Create an Ajax request to the *figlet* function endpoint (`/function/figlet`)
* Apply the result to the `textarea`

There is no need to change the `handler.py` because it can dynamically serve HTML from the previous section. Despite not changing the `handler.py` , we need to build and push the function image because we need to pack the new `figlet.html` inside the function container.

Now build, push and deploy the function:

```
$ faas-cli up -f show-html.yml
```

This section assumes you have already deployed the *figlet* function from [Lab 2](./lab2.md).  

Open your browser and first access:

http://127.0.0.1:8080/function/show-html?action=figlet

You should see the "Figlet" page and should see an input. Type any text you want to and click the "Generate" button. If the request succeeds, the `textarea` should contain the figlet you typed inside the `input`. This is a trivial example, but by using this technique you can even create powerful SPAs (Single Page Application) with functions, too.

In this lab you learned how you can serve HTML from your function and set the `Content-Type` of the response. In addition, you have also learned how you can call other functions with HTML + JavaScript and create a dynamic page with functions, too.

Now move onto [Lab 7](lab7.md)
