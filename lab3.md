# Lab 3 - Introduction to functions

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

## Creating a new function

There are two ways to create a new function:

* scaffold a function using a built-in or community code template (default)
* take an existing binary and use it as your function (advanced)

### Scaffold or generate a new function

Before creating a new function from a template make sure you pull the [templates from GitHub](https://github.com/openfaas/templates):

```
$ faas-cli template pull

Fetch templates from repository: https://github.com/openfaas/templates.git
 Attempting to expand templates from https://github.com/openfaas/templates.git
 Fetched 11 template(s) : [csharp dockerfile go go-armhf node node-arm64 node-armhf python python-armhf python3 ruby]
```

After that, to find out which languages are available type in:

```
$ faas-cli new --list
Languages available as templates:
- csharp
- dockerfile
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

* A note on our examples

All of our examples for this workshop have been thoroughly tested by the OpenFaaS community with *Python 3*, but should be compatible with *Python 2.7* also.

If you'd prefer to use Python 2.7 instead of Python 3 then swap `faas-cli new --lang python3` for `faas-cli new --lang python`.

### Hello world in Python

We will create a hello-world function in Python, then move onto something that uses additional dependencies too.

* Scaffold the function

```
$ faas-cli new --lang python3 hello-openfaas --prefix="<your-docker-username-here>"
```

The `--prefix` parameter will update `image: ` value in `hello-openfaas.yml` with a prefix which should be your Docker Hub account. For [OpenFaaS](https://hub.docker.com/r/functions) this is `image: functions/hello-openfaas` and the parameter will be `--prefix="functions"`.

If you don't specify a prefix when you create the function then edit the YAML file after creating it.

This will create three files and a directory:

```
./hello-openfaas.yml
./hello-openfaas
./hello-openfaas/handler.py
./hello-openfaas/requirements.txt
```

The YAML (.yml) file is used to configure the CLI for building, pushing and deploying your function.

> Note: Whenever you need to deploy a function on Kubernetes or on a remote OpenFaaS instance you must always push your function after building it.
>       In this case you can also override the default gateway URL of `127.0.0.1:8080` with an environmental variable: `export OPENFAAS_URL=127.0.0.1:31112`.

Here's the contents of the YAML file:

```yaml
provider:
  name: faas
  gateway: http://127.0.0.1:8080

functions:
  hello-openfaas:
    lang: python3
    handler: ./hello-openfaas
    image: hello-openfaas
```

* The name of the function is represented by the key under `functions` i.e. `hello-openfaas`
* The language is represented by the `lang` field
* The folder used to build from is called `handler`, this must be a folder not a file
* The Docker image name to be used is under the field `image`

Remember that the `gateway` URL can be overriden in the YAML file (by editing the `gateway:` value under `provider:`) or on the CLI (by using `--gateway` or setting the `OPENFAAS_URL` environment variable).

Here is the contents of the `handler.py` file:

```python
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return req
```

This function will just return the input, so it's effectively an `echo` function.

Edit the message so it returns `hello world` instead i.e.

```
    return "Hello World"
```

Any values returned to stdout will subsequently be returned to the calling program. Alternatively a `print()` statement could be employed which would exhibit a similar flow through to the calling program.

This is the local developer-workflow for functions:

```
$ faas-cli build -f ./hello-openfaas.yml
$ faas-cli push -f ./hello-openfaas.yml
$ faas-cli deploy -f ./hello-openfaas.yml
```

Followed by invoking the function via the UI, CLI, `curl` or another application.

The function will always get a route, for example:

```
http://127.0.0.1:8080/function/<function_name>
http://127.0.0.1:8080/function/figlet
http://127.0.0.1:8080/function/hello-openfaas
```

> Pro-tip: if you rename your YAML file to `stack.yml` then you need not pass the `-f` flag to any of the commands.

Functions can be invoked via a `GET` or `POST` method only.

* Invoke your function

Test out the function with `faas-cli invoke`, check `faas-cli invoke --help` for more options.

### Example function: astronaut-finder

We'll create a function called `astronaut-finder` that pulls in a random name of someone in space aboard the International Space Station (ISS).

```
$ faas-cli new --lang python3 astronaut-finder --prefix="<your-docker-username-here>"
```

This will write three files for us:

```
./astronaut-finder/handler.py
```

The handler for the function - you get a `req` object with the raw request and can print the result of the function to the console.

```
./astronaut-finder/requirements.txt
```

Use this file to list any `pip` modules you want to install, such as `requests` or `urllib`

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

```json
{"number": 6, "people": [{"craft": "ISS", "name": "Alexander Misurkin"}, {"craft": "ISS", "name": "Mark Vande Hei"}, {"craft": "ISS", "name": "Joe Acaba"}, {"craft": "ISS", "name": "Anton Shkaplerov"}, {"craft": "ISS", "name": "Scott Tingle"}, {"craft": "ISS", "name": "Norishige Kanai"}], "message": "success"}
```

Update `handler.py`:

```python
import requests
import random

def handle(req):
    r = requests.get("http://api.open-notify.org/astros.json")
    result = r.json()
    index = random.randint(0, len(result["people"])-1)
    name = result["people"][index]["name"]

    return "%s is in space" % (name)
```

> Note: in this example we do not make use of the parameter `req` but must keep it in the function's header.

Now build the function:

```
$ faas-cli build -f ./astronaut-finder.yml
```

> Tip: Try renaming astronaut-finder.yml to `stack.yml` and calling just `faas-cli build`. `stack.yml` is the default file-name for the CLI.

Deploy the function:

```
$ faas-cli deploy -f ./astronaut-finder.yml
```

Invoke the function

```
$ echo | faas-cli invoke astronaut-finder
Anton Shkaplerov is in space

$ echo | faas-cli invoke astronaut-finder
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

```yaml
provider:
  name: faas
  gateway: http://127.0.0.1:8080

functions:
  astronaut-finder:
    lang: python3
    handler: ./astronaut-finder
    image: astronaut-finder
```

Edit your YAML file for the function and add an "environment" section.

```yaml
  astronaut-finder:
    lang: python3
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

### Managing multiple functions

The YAML file for the CLI allows functions to be grouped together into stacks, this is helpful when working with a set of related functions.

To see how this works generate two functions:

```
$ faas-cli new --lang python3 first
```

For the second function use the `--append` flag:

```
$ faas-cli new --lang python3 second --append=./first.yml
```

For convenience let's rename `first.yml` to `example.yml`.

```
$ mv first.yml example.yml
```

Now look at the file:

```
provider:
  name: faas
  gateway: http://127.0.0.1:8080

functions:
  first:
    lang: python3
    handler: ./first
    image: first
  second:
    lang: python3
    handler: ./second
    image: second
```

Here are several flags that help when working with a stack of functions:

* Build in parallel:

`faas-cli build -f ./example.yml --parallel=2`

* Build / push only one function:

`faas-cli build -f ./example.yml --filter=second`

Look at the options for `faas-cli build --help` and `faas-cli push --help` for more information.

> Pro-tip: `stack.yml` is the default name the faas-cli will look for if you don't want to pass a `-f` parameter.

You can also deploy function stack (yaml) files over HTTP(s) using `faas-cli -f https://....`.

### Make use of custom templates

If you have your own language template or have found a community template such as the PHP template then you can add that with the following command:

```
$ faas-cli template pull https://github.com/itscaro/openfaas-template-php

...

faas-cli new --list|grep php
- php
- php5
```

A list of community templates is maintained on the [OpenFaaS CLI README page](https://github.com/openfaas/faas-cli).

Continue to the optional exercise or move onto [Lab 4](lab4.md).

### Custom binaries as functions (optional)

Custom binaries or containers can be used as functions, but most of the time using the language templates should cover all the most common scenarios.

To use a custom binary or Dockerfile create a new function using the `dockerfile` language:

```
$ faas-cli new --lang dockerfile sorter --prefix="<your-docker-username-here>"
```

You'll see a folder created named `sorter` and `sorter.yml`.

Edit `sorter/Dockerfile` and update the line which sets the `fprocess`. Let's change it to the built-in bash command of `sort`. We can use this to sort a list of strings in alphanumeric order.

```
ENV fprocess="sort"
```

Now build, push and deploy the function:

```
$ faas-cli build -f sorter.yml \
  && faas-cli push -f sorter.yml \
  && faas-cli deploy -f sorter.yml
```

Now invoke the function through the UI or via the CLI:

```
$ echo -n '
elephant
zebra
horse
ardvark
monkey'| faas-cli invoke sorter -g 127.0.0.1:8080

ardvark
elephant
horse
monkey
zebra
```

In the example we used `sort` from [BusyBox](https://busybox.net/downloads/BusyBox.html) which is built into the function. There are other useful commands such as `sha512sum` and even a `bash` or shell script, but you are not limited to these built-in commands. Any binary or existing container can be made a serverless function by adding the OpenFaaS function watchdog.

> Tip: did you know that OpenFaaS supports Windows binaries too? Like C#, VB or PowerShell?

Now move onto [Lab 4](lab4.md)
