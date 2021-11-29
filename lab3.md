# Lab 3 - Introduction to functions

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

Before starting this lab, create a new folder for your files:

```sh
$ mkdir -p lab3 \
   && cd lab3
```

## Creating a new function

There are two ways to create a new function:

* scaffold a function using a built-in or community code template (default)
* take an existing binary and use it as your function (advanced)

### Scaffold or generate a new function

Before creating a new function from a template make sure you pull the [templates from GitHub](https://github.com/openfaas/templates):

```sh
$ faas-cli template pull

Fetch templates from repository: https://github.com/openfaas/templates.git
 Attempting to expand templates from https://github.com/openfaas/templates.git
2021/08/25 15:58:10 Fetched 13 template(s) : [csharp dockerfile go java11 java11-vert-x node node12 node14 php7 python python3 python3-debian ruby] from https://github.com/openfaas/templates.git
```

After that, to find out which languages are available type in:

```sh
$ faas-cli new --list
Languages available as templates:
- csharp
- dockerfile
- go
- java11
- java11-vert-x
- node
- node12
- node14
- php7
- python
- python3
- python3-debian
- ruby
```

Or alternatively create a folder containing a `Dockerfile`, then pick the "Dockerfile" lang type in your YAML file.

At this point you can create a new function for Python, Python 3, Ruby, Go, Node, CSharp etc.

* A note on our examples

All of our examples for this workshop have been thoroughly tested by the OpenFaaS community with *Python 3*, but should be compatible with *Python 2.7* also.

If you'd prefer to use Python 2.7 instead of Python 3 then swap `faas-cli new --lang python3` for `faas-cli new --lang python`.

### Hello world in Python

We will create a hello-world function in Python, then move onto something that uses additional dependencies too.

* Scaffold the function

```sh
$ faas-cli new --lang python3 hello-openfaas --prefix="<your-docker-username-here>"
```

The `--prefix` parameter will update `image: ` value in `hello-openfaas.yml` with a prefix which should be your Docker Hub account. For [OpenFaaS](https://hub.docker.com/r/functions) this is `image: functions/hello-openfaas` and the parameter will be `--prefix="functions"`.

If you don't specify a prefix when you create the function then edit the YAML file after creating it.

This will create three files and a directory:

```sh
./hello-openfaas.yml
./hello-openfaas
./hello-openfaas/handler.py
./hello-openfaas/requirements.txt
```

The YAML (.yml) file is used to configure the CLI for building, pushing and deploying your function.

> Note: Whenever you need to deploy a function on Kubernetes or on a remote OpenFaaS instance you must always push your function after building it. In this case you can also override the default gateway URL of `127.0.0.1:8080` with an environmental variable: `export OPENFAAS_URL=127.0.0.1:31112`.

Here's the contents of the YAML file:

```yaml
provider:
  name: openfaas
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

Edit the message so it returns `Hello OpenFaaS` instead i.e.

```sh
    return "Hello OpenFaaS"
```

Any values returned to stdout will subsequently be returned to the calling program. Alternatively a `print()` statement could be employed which would exhibit a similar flow through to the calling program.

This is the local developer-workflow for functions:

```sh
$ faas-cli up -f hello-openfaas.yml
```
> Note: Please make sure that you have logged in to docker registry with `docker login` command before running this command.

> Note: `faas-cli up` command combines build, push and deploy commands of `faas-cli` in a single command.

Followed by invoking the function via the UI, CLI, `curl` or another application.

The function will always get a route, for example:

```sh
$OPENFAAS_URL/function/<function_name>
$OPENFAAS_URL/function/figlet
$OPENFAAS_URL/function/hello-openfaas
```

> Pro-tip: if you rename your YAML file to `stack.yml` then you need not pass the `-f` flag to any of the commands.

Functions can be invoked via a `GET` or `POST` method only.

* Invoke your function

Test out the function with `faas-cli invoke`, check `faas-cli invoke --help` for more options.

### Example function: astronaut-finder

We'll create a function called `astronaut-finder` that pulls in a random name of someone in space aboard the International Space Station (ISS).

```sh
$ faas-cli new --lang python3 astronaut-finder --prefix="<your-docker-username-here>"
```

This will write three files for us:

```sh
./astronaut-finder/handler.py
```

The handler for the function - you get a `req` object with the raw request and can print the result of the function to the console.

```sh
./astronaut-finder/requirements.txt
```
This file is used to manage the function - it has the name of the function, the Docker image and any other customisations needed.

```sh
./astronaut-finder.yml
```
Use this file to list any `pip` modules you want to install, such as `requests` or `urllib`

* Edit `./astronaut-finder/requirements.txt`

```sh
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

```sh
$ faas-cli build -f ./astronaut-finder.yml
```

> Tip: Try renaming astronaut-finder.yml to `stack.yml` and calling just `faas-cli build`. `stack.yml` is the default file-name for the CLI.


Push the function:

```sh
$ faas-cli push -f ./astronaut-finder.yml
```

Deploy the function:

```sh
$ faas-cli deploy -f ./astronaut-finder.yml
```

Invoke the function

```sh
$ echo | faas-cli invoke astronaut-finder
Anton Shkaplerov is in space

$ echo | faas-cli invoke astronaut-finder
Joe Acaba is in space
```

## Troubleshooting: find the container's logs

You can find out high-level information on every invocation of your function via the container's logs:

```sh
$ kubectl logs deployment/astronaut-finder -n openfaas-fn
```

## Troubleshooting: verbose output with `write_debug`

Let's turn on verbose output for your function. This is turned-off by default so that we do not flood your function's logs with data - that is especially important when working with binary data which makes no sense in the logs.

This is the standard YAML configuration:

```yaml
provider:
  name: openfaas
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

```sh
$ kubectl logs deployment/astronaut-finder -n openfaas-fn
```

### Managing multiple functions

The YAML file for the CLI allows functions to be grouped together into stacks, this is helpful when working with a set of related functions.

To see how this works generate two functions:

```sh
$ faas-cli new --lang python3 first
```

For the second function use the `--append` flag:

```sh
$ faas-cli new --lang python3 second --append=./first.yml
```

For convenience let's rename `first.yml` to `example.yml`.

```sh
$ mv first.yml example.yml
```

Now look at the file:

```yaml
provider:
  name: openfaas
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

```sh
$ faas-cli build -f ./example.yml --parallel=2
```

* Build / push only one function:

```sh
$ faas-cli build -f ./example.yml --filter=second
```

Take a few moments to explore the options for `build`/`push` and `deploy`.

* `faas-cli build --help`
* `faas-cli push --help`
* `faas-cli deploy --help`

To run `faas-cli build && faas-cli push && faas-cli deploy` together, use `faas-cli up` instead.

> Pro-tip: `stack.yml` is the default name the faas-cli will look for if you don't want to pass a `-f` parameter.

You can also deploy remote function stack (yaml) files over HTTP(s) using `faas-cli deploy -f https://....`.

### Custom templates

If you have your own set of forked or custom templates, then you can pull them down for use with the CLI.

Here's an example of fetching a Python 3 template which uses Debian Linux.

Pull the template using the `git` URL:

```sh
$ faas-cli template pull https://github.com/openfaas-incubator/python3-debian
```

Now type in: `faas-cli new --list`

```sh
$ faas-cli new --list | grep python
- python
- python3
- python3-debian
```

These new templates are saved in your current working directory in `./templates/`.

#### Custom templates: Template Store

The *Template Store* is a similar concept to the *Function Store*, it enables users to collaborate by sharing their templates. The template store also means that you don't have to remember any URLs for making use of your favourite community or project templates.

You can Search and discover templates using the following two commands:

```sh
$ faas-cli template store list
$ faas-cli template store list -v

NAME                     SOURCE             DESCRIPTION
csharp                   openfaas           Classic C# template
dockerfile               openfaas           Classic Dockerfile template
go                       openfaas           Classic Golang template
...
```

To get more details you can use the `--verbose` flag, or the `describe` command.

Let's find a Golang template with a HTTP format:

``bash
faas-cli template store list | grep golang

golang-http              openfaas           Golang HTTP template
golang-middleware        openfaas           Golang Middleware template
```

Then check out its upstream repository:

```sh
$ faas-cli template store describe golang-http

Name:              golang-http
Platform:          x86_64
Language:          Go
Source:            openfaas
Description:       Golang HTTP template
Repository:        https://github.com/openfaas/golang-http-template
Official Template: true
```

Pull the template down:

```sh
$ faas-cli template store pull golang-http
```

You can now create a function with this template by typing in:

```bash
faas-cli new --lang golang-http NAME
```

To make it easier than having to run `faas-cli template store pull golang-http` for functions, you can append the following to your stack.yml file:

```yaml
configuration:
  templates:
    - name: golang-http
```

Then run the following instead of specifying the template name:

```bash
$ faas-cli template store pull
```

See also:

* [OpenFaaS YAML reference guide](https://docs.openfaas.com/reference/yaml/)
* [Function & Template Store](https://github.com/openfaas/store/)

### Variable Substitution in YAML File (optional exercise)

The `.yml` file used to configure the CLI is capable of variable substitution so that you are able to use the same `.yml` file for multiple configurations.

One example of where this can be useful is when there are different registries for development and production images. You can use the variable substitution so that local and test environments use the default account, and the CI server can be configured to use the production account.

> This is provided by the [envsubst library](https://github.com/drone/envsubst). Follow the link to see examples of supported variables

Edit your `astronaut-finder.yml` to match the following:

```yml
  astronaut-finder:
    lang: python3
    handler: ./astronaut-finder
    image: ${DOCKER_USER:-development}/astronaut-finder
    environment:
      write_debug: true
```

You'll notice the `image` property has been updated to include a variable definition (`DOCKER_USER`). That value will be replaced with the value of the environment variable with the same name. If the environment variable is not present, or is empty, the default value (`development`) will be used.

The variable will be replaced with the value throughout the file. So, if you have several functions in your `.yml` file, all references to the `DOCKER_USER` variable will be replaced with the value of that environment variable

Run the following command and observe the output:

`faas-cli build -f ./astronaut-finder.yml`

The output should show that the image built is labeled as `development/astronaut-finder:latest`

Now, set the environment variable to your Docker Hub account name (for the example, we'll use the OpenFaaS "functions" account)

```sh
export DOCKER_USER=functions
```

Run the same build command as before and observe the output:

`faas-cli build -f ./astronaut-finder.yml`

The output should now show that the image was built with the updated label `functions/astronaut-finder:latest`

### Custom binaries as functions (optional exercise)

Custom binaries or containers can be used as functions, but most of the time using the language templates should cover all the most common scenarios.

To use a custom binary or Dockerfile create a new function using the `dockerfile` language:

```sh
$ faas-cli new --lang dockerfile sorter --prefix="<your-docker-username-here>"
```

You'll see a folder created named `sorter` and `sorter.yml`.

Edit `sorter/Dockerfile` and update the line which sets the `fprocess`. Let's change it to the built-in bash command of `sort`. We can use this to sort a list of strings in alphanumeric order.

```dockerfile
ENV fprocess="sort"
```

Now build, push and deploy the function:

```sh
$ faas-cli up -f sorter.yml
```

Now invoke the function through the UI or via the CLI:

```sh
$ echo -n '
elephant
zebra
horse
aardvark
monkey'| faas-cli invoke sorter

aardvark
elephant
horse
monkey
zebra
```

In the example we used `sort` from [BusyBox](https://busybox.net/downloads/BusyBox.html) which is built into the function. There are other useful commands such as `sha512sum` and even a `bash` or shell script, but you are not limited to these built-in commands. Any binary or existing container can be made a serverless function by adding the OpenFaaS function watchdog.

> Tip: did you know that OpenFaaS supports Windows binaries too? Like C#, VB or PowerShell?

Now move onto [Lab 4](lab4.md)
