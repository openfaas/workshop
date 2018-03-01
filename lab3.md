# Lab 3 - Introduction to Functions

## Creating a new function

There are two ways to create a new function:

* scaffold a function using a built-in or community code template (default)
* take an existing binary and use it as your function (advanced)

### Scaffold or generate a new function

To find out which languages are available type in:

```
$ faas new --list
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

### Hello world in Python

We will create a hello-world function in Python, then move onto something that uses additional dependencies too.

* Scaffold the function

```
$ faas new --lang python hello-openfaas
```

This will create three files for us:

```
./hello-openfaas.yml
./hello-openfaas
./hello-openfaas/handler.py
./hello-openfaas/requirements.txt
```

The YAML (.yml) file is used to configure the CLI for building, pushing and deploying your function.

> Note: Whenever you need to deploy a function on Kubernetes or on a remote OpenFaaS instance you must always push your function after building it.

Here's the contents of the YAML file:

```
provider:
  name: faas
  gateway: http://localhost:8080

functions:
  hello-openfaas:
    lang: python
    handler: ./hello-openfaas
    image: hello-openfaas
```

On the line `image: ` make sure the name is prefixed with your Docker Hub account. For Alex Ellis this is `image: alexellis2/hello-openfaas`. Update this for your name every time you create a new function.

Here is the contents of the `handler.py` file:

```
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    print(req)
```

This function will just print the input, so it's effectively an `echo` function.

Edit the message so it prints `hello world` instead i.e.

```
    print("Hello World")
```

This is the local developer-workflow for functions:

```
$ faas build -f ./hello-openfaas.yml
$ faas push -f ./hello-openfaas.yml
$ faas deploy -f ./hello-openfaas.yml
```

Followed by invoking the function via the UI, CLI, `curl` or another application.

The function will always get a route, for example:

```
http://localhost:8080/function/<function_name>
http://localhost:8080/function/figlet
http://localhost:8080/function/hello-openfaas
```

> Pro-tip: if you rename your YAML file to `stack.yml` then you will not need to pass a `-f` flag to any commands.

Functions can be invoked via a `GET` or `POST` method only.

* Invoke your function

Test out the function with `faas-cli invoke`, check `faas-cli invoke --help` for more options.

### Example function: astronaut-finder

We'll create a function called `astronaut-finder` that pulls in a random name of someone in space aboard the International Space Station (ISS).

```
$ faas new --lang python astronaut-finder
```

This will write three files for us:

```
./astronaut-finder/handler.py
```

The handler for the function - you get a `req` object with the raw request and can print the result of the function to the console.

```
./astronaut-finder/requirements.txt
```

This file lists any `pip` modules you want to install, such as `requests` or `urllib`

```
./astronaut-finder.yml
```

This file is used to manage the function - it has the name of the function, the Docker image and any other customisations needed.

* Edit `./astronaut-finder/requirements.txt`

```
requests
```

This tells the function it needs to use a third-party module named [requests](http://docs.python-requests.org/en/master/) for accessing websites over HTTP.

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

def handle(req):
    r = requests.get("http://api.open-notify.org/astros.json")
    result = r.json()
    index = random.randint(0, len(result["people"])-1)
    name = result["people"][index]["name"]

    print (name + " is in space") 
```

> Note: in this example we do not make use of the parameter `req` but must keep it in the function's header.

Now build the function:

```
$ faas build -f ./astronaut-finder.yml
```

> Tip: If you rename astronaut-finder.yml to `stack.yml` then you can leave off the `-f` argument. `stack.yml` is the default file-name for the CLI.

Deploy the function:

```
$ faas deploy -f ./astronaut-finder.yml
```

Invoke the function

```
$ echo | faas invoke astronaut-finder
Anton Shkaplerov is in space

$ echo | faas invoke astronaut-finder
Joe Acaba is in space
```

## Troubleshooting: find the container's logs

You can find out high-level information on every invocation of your function via the container's logs:

```
$ docker service logs -f astronaut-finder
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:25 Forking fprocess.
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:26 Wrote 18 Bytes - Duration: 0.063269 seconds
```

## Troubleshooting: verbose output with `write_debug`

Let's turn on verbose output for your function. This is turned-off by default so that we do not flood your function's logs with data - that is especially important when working with binary data which makes no sense in the logs.

This is the standard YAML configuration:

```
provider:
  name: faas
  gateway: http://localhost:8080

functions:
  astronaut-finder:
    lang: python
    handler: ./astronaut-finder
    image: astronaut-finder
```

Edit your YAML file for the function and add an "environment" section.

```
  astronaut-finder:
    lang: python
    handler: ./astronaut-finder
    image: astronaut-finder
    environment:
      write_debug: true
```

Now deploy your function again with `faas-cli deploy -f ./astronaut-finder.yml`.

Invoke the function and then checkout the logs again to view the function responses:

```
$ docker service logs -f astronaut-finder
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:25 Forking fprocess.
astronaut-finder.1.szobw9pt3m60@nuc    | 2018/02/26 14:49:57 Query  
astronaut-finder.1.szobw9pt3m60@nuc    | 2018/02/26 14:49:57 Path  /function/hello-openfaas
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:26 Hello World
astronaut-finder.1.1e1ujtsijf6b@nuc    | 2018/02/21 14:53:26 Duration: 0.063269 seconds
```

### Make use of custom templates

If you have your own language template or have found a community template such as the PHP template then you can add that with the following command:

```
$ faas template pull https://github.com/itscaro/openfaas-template-php

...

faas new --list|grep php
- php
- php5
```

A list of community templates is maintained on the [OpenFaaS CLI README page](https://github.com/openfaas/faas-cli).

Continue to the optional exercise or go move onto [Lab 4](lab4.md).

### Custom binaries as functions (optional)

Custom binaries or containers can be used as functions, but most of the time using the language templates should cover all the most common scenarios.

To use a custom binary or Dockerfile create a new function using the `dockerfile` language:

```
$ faas new --lang dockerfile sorter
```

You'll see a folder created named `sorter` and `sorter.yml`.

Edit `sorter/Dockerfile` and update the line which sets the `fprocess`. Let's change it to the built-in bash command of `sort`. We can use this to sort a list of strings in alphanumeric order.

```
ENV fprocess="sort"
```

Edit `sorter.yml` and add your username as a prefix to the `image: sorter` field such as `image: alexellis2/sorter`.

Now build, push and deploy the function:

```
$ faas build -f sorter.yml \
  && faas push -f sorter.yml
  && faas deploy -f sorter.yml
```

Now invoke the function through the UI or via the CLI:

```
$ echo -n '
elephant
zebra
horse
ardvark
monkey'| faas invoke sorter -g 127.0.0.1:8081

ardvark
elephant
horse
monkey
zebra
```

In the example we used sort from [BusyBox](https://busybox.net/downloads/BusyBox.html) which is built into the function. There are other useful commands such as `sha512sum` and even a `bash` or shell script, but you are not limited to these built-in commands. Any binary or existing container can be made a serverless function by adding the OpenFaaS function watchdog.

> Tip: did you know that OpenFaaS supports Windows binaries too? Like C#, VB or PowerShell?

Now move onto [Lab 4](lab4.md)
