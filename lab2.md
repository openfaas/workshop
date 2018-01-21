# Lab 2 - Functions

## Creating a new function

There are two ways to create a new function:

* scaffold a function using a built-in or community code template (default)
* take an existing binary and use it as your function (advanced)

### Scaffolding a new function

To find out which languages are available type in:

```
faas new --list
Languages available as templates:
- csharp
- go
- go-armhf
- node
- node-arm64
- node-armhf
- python
- python-armhf
- python3
- ruby

Or alternatively create a folder containing a Dockerfile, then pick
the "Dockerfile" lang type in your YAML file.
```

At this point you can create a new function for Python, Python 3, Ruby, Go, Node, CSharp etc.

* Let's pick Python:

We'll create a function that pulls in a random name of someone in space aboard the International Space Station (ISS).

```
faas new --lang python space-counter
```

This will write three files for us:

```
./space-counter/handler.py
```

The handler for the function - you get a `req` object with the raw request and can print the result of the function to the console.

```
./space-counter/requirements.txt
```

This file lists any `pip` modules you want to install, such as `requests` or `urllib`

```
./space-counter.yml
```

This file is used to manage the function - it has the name of the function, the Docker image and any other customisations needed.

* Edit `requirements.txt`

```
echo "requests" > ./space-counter/requirements.txt
```

This tells the function it needs to use a third-party module for accessing websites.

* Write the function's code:

We'll be pulling in data from: http://api.open-notify.org/astros.json

Here's an example of the result:

```
{"number": 6, "people": [{"craft": "ISS", "name": "Alexander Misurkin"}, {"craft": "ISS", "name": "Mark Vande Hei"}, {"craft": "ISS", "name": "Joe Acaba"}, {"craft": "ISS", "name": "Anton Shkaplerov"}, {"craft": "ISS", "name": "Scott Tingle"}, {"craft": "ISS", "name": "Norishige Kanai"}], "message": "success"}
```

Update `handler.py`:

```
import requests
import random

def handle(st):
    r = requests.get("http://api.open-notify.org/astros.json")
    result = r.json()
    index = random.randint(0, len(result["people"])-1)
    name = result["people"][index]["name"]

    print (name + " is in space") 
```

Now build the function:

```
faas build -f ./space-counter.yml
```

> Tip: If you rename space-counter.yml to `stack.yml` then you can leave off the `-f` argument. `stack.yml` is the default file-name for the CLI.

Deploy the function:

```
faas deploy -f ./space-counter.yml
```

Invoke the function

```
echo | faas invoke space-counter
Anton Shkaplerov is in space

echo | faas invoke space-counter
Joe Acaba is in space
```

### Making use of custom templates

If you have your own language template or have found a community template such as the PHP template then you can add that with the following command:

```
faas template pull https://github.com/itscaro/openfaas-template-php

...

faas new --list|grep php
- php
- php5
```

A list of community templates is maintained on the [OpenFaaS CLI site](https://github.com/openfaas/faas-cli).

## Accessing the HTTP request / query-string

The `faas-cli invoke` can accept other parameters such as `--query` to provide a querystring. Any parameters will be available as environmental variables within your code.

Here's an example where we scaffold a new Node.js function using the `faas new` command:

```
faas new --lang node print-env
mv print-env.yml stack.yml
```

The `new` command will create two files for a Node.js template:

```
./print-env/handler.js
./stack.yml
```

If you need to add `npm` modules later on you can create a `package.json` file in the `print-env` folder.

Edit `print-env/handler.js`:

```
"use strict"

module.exports = (context, callback) => {
    callback(undefined, { "environment": process.env });
}
```

This will print out the environmental variables available to the function. So let's build / deploy and invoke it:

```
faas build
faas deploy
echo -n "openfaas" | faas invoke print-env --query workshop=true

{"environment":{"PATH":"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","HOSTNAME":"59cc01de25a6",
"fprocess":"node index.js","NODE_VERSION":"8.9.1","YARN_VERSION":"1.3.2","NPM_CONFIG_LOGLEVEL":"warn",
"cgi_headers":"true","HOME":"/home/app",
"Http_User_Agent":"Go-http-client/1.1",
"Http_Accept_Encoding":"gzip",
"Http_Content_Type":"text/plain",
"Http_Connection":"close",
"Http_Method":"POST",
"Http_ContentLength":"-1",
"Http_Query":"workshop=true",
"Http_Path":"/function/print-env"}}
```

As part of the output you can see the Http headers and request data revealed in environmental variables.

Our querystring of `workshop=true` is available in the environmental variable `Http_Query`.

In Python you can find environmental variables through the `os.getenv(key, default_value)` function or `os.environ` array after importing the `os` package.

i.e.

```
import os

def handle(st):
    print os.getenv("Http_Method")          # will be "NoneType" if empty
    print os.getenv("Http_Method", "GET")   # provide a default of "GET" if empty
    print os.environ["Http_Method"]         # throws an exception is not present
    print os.environ                        # array of environment
```
