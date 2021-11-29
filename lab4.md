# Lab 4 - Go deeper with functions

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

Before starting this lab, create a new folder for your files. As this lab builds on an earlier lab make a copy of lab3:

```
$ cp -r lab3 lab4 \
   && cd lab4
```

## Inject configuration through environmental variables

It is useful to be able to control how a function behaves at runtime, we can do that in at least two ways:

### At deployment time

* Set environmental variables at deployment time

We did this with `write_debug` in [Lab 3](./lab3.md) - you can also set any custom environmental variables you want here too - for instance if you wanted to configure a language for your *hello world* function you may introduce a `spoken_language` variable.

### Use HTTP context - querystring / headers

* Use querystring and HTTP headers

The other option which is more dynamic and can be altered at a per-request level is the use of querystrings and HTTP headers, both can be passed through the `faas-cli` or `curl`.

These headers become exposed through environmental variables so they are easy to consume within your function. So any header is prefixed with `Http_` and all `-` hyphens are replaced with an `_` underscore.

Let's try it out with a querystring and a function that lists off all environmental variables.

* Deploy a function that prints environmental variables using a built-in BusyBox command:

```
$ faas-cli deploy --name env --fprocess="env" --image="functions/alpine:latest"
```

* Invoke the function with a querystring:

```
$ echo "" | faas-cli invoke env --query workshop=1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=05e8db360c5a
fprocess=env
HOME=/root
Http_Connection=close
Http_Content_Type=text/plain
Http_X_Call_Id=cdbed396-a20a-43fe-9123-1d5a122c976d
Http_X_Forwarded_For=10.255.0.2
Http_X_Start_Time=1519729562486546741
Http_User_Agent=Go-http-client/1.1
Http_Accept_Encoding=gzip
Http_Method=POST
Http_ContentLength=-1
Http_Path=/
...
Http_Query=workshop=1
...
```

In Python code you'd type in `os.getenv("Http_Query")`.

* Append the path to your function URL

Invoke the env function with:

```
$ curl -X GET $OPENFAAS_URL/function/env/some/path -d ""
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=fae2ac4b75f9
fprocess=env
HOME=/root
Http_X_Forwarded_Host=127.0.0.1:8080
Http_X_Start_Time=1539370471902481800
Http_Accept_Encoding=gzip
Http_User_Agent=curl/7.54.0
Http_Accept=*/*
Http_X_Forwarded_For=10.255.0.2:60460
Http_X_Call_Id=bb86b4fb-641b-463d-ae45-af68c1aa0d42
Http_Method=GET
Http_ContentLength=0
...
Http_Path=/some/path
...
```

As you can see the `Http_Path` header contains your path.
If you'd like to use it in your code, just get it with `os.getenv("Http_Path")`

* Now invoke it with a header:

```
$ curl $OPENFAAS_URL/function/env --header "X-Output-Mode: json" -d ""
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=05e8db360c5a
fprocess=env
HOME=/root
Http_X_Call_Id=8e597bcf-614f-4ca5-8f2e-f345d660db5e
Http_X_Forwarded_For=10.255.0.2
Http_X_Start_Time=1519729577415481886
Http_Accept=*/*
Http_Accept_Encoding=gzip
Http_Connection=close
Http_User_Agent=curl/7.55.1
Http_Method=GET
Http_ContentLength=0
Http_Path=/
...
Http_X_Output_Mode=json
...
```

In Python code you'd type in `os.getenv("Http_X_Output_Mode")`.

You can see that all other HTTP context is also provided such as `Content-Length` when the `Http_Method` is a `POST`, the `User_Agent`, Cookies and anything else you'd expect to see from a HTTP request.

## Security: read-only filesystems

One of the security features of containers which is available to OpenFaaS is the ability to make the root filesystem of our execution environment read-only. This can reduce the attack surface if a function were to become compromised.

Generate a function to save files into the function's filesystem:

```sh
faas-cli new --lang python3 ingest-file --prefix=your-name
```

Update the handler:

```python
import os
import time

def handle(req):
    # Read the path or a default from environment variable
    path = os.getenv("save_path", "/home/app/")

    # generate a name using the current timestamp
    t = time.time()
    file_name = path + str(t)

    # write a file
    with open(file_name, "w") as f:
        f.write(req)
        f.close()

    return file_name
```

Build the example:

```sh
faas-cli up -f ingest-file.yml
```

Invoke the example:

```sh
echo "Hello function" > message.txt

cat message.txt | faas-cli invoke -f ingest-file.yml ingest-file
```

The file will be written to the `/home/app` path.

Now edit the ingest-file.yml and make the function read-only.

```yaml
...
functions:
  ingest-file:
    lang: python3
    handler: ./ingest-file
    image: alexellis2/ingest-file:latest
    readonly_root_filesystem: true
```

> See also: [YAML reference](https://docs.openfaas.com/reference/yaml/#function-read-only-root-filesystem)

Deploy again:

```sh
faas-cli up -f ingest-file.yml
```

This will now fail:

```sh
echo "Hello function" > message.txt

cat message.txt | faas-cli invoke -f ingest-file.yml ingest-file
```

See the error:

```sh
Server returned unexpected status code: 500 - exit status 1
Traceback (most recent call last):
  File "index.py", line 19, in <module>
    ret = handler.handle(st)
  File "/home/app/function/handler.py", line 13, in handle
    with open(file_name, "w") as f:
OSError: [Errno 30] Read-only file system: '/home/app/1556714998.092464'
```

In order to write to a temporary area set the environment variable `save_path`

```yaml
...
functions:
  ingest-file:
    lang: python3
    handler: ./ingest-file
    image: alexellis2/ingest-file:latest
    readonly_root_filesystem: true
    environment:
        save_path: "/tmp/"
```

You can now test the fix by running `faas-cli up -f ingest-file.yml` one more time and the files will be written into `/tmp/`.

We now have the ability to lock-down our function's code so that it cannot be changed accidentally or updated maliciously. 

## Making use of logging

The OpenFaaS watchdog operates by passing in the HTTP request and reading an HTTP response via the standard I/O streams `stdin` and `stdout`. This means that the process running as a function does not need to know anything about the web or HTTP.

An interesting case is when a function exits with a non-zero exit code and `stderr` is not empty.
By default a function's `stdout/stderr` is combined and `stderr` is not printed to the logs.

Lets check that with the `hello-openfaas` function from [Lab 3](./lab3.md#hello-world-in-python).

Change the `handler.py` code to

```python
import sys
import json

def handle(req):

    sys.stderr.write("This should be an error message.\n")
    return json.dumps({"Hello": "OpenFaaS"})
```

Build and deploy

```sh
$ faas-cli up -f hello-openfaas.yml
```

Now invoke the function with

```sh
$ echo | faas-cli invoke hello-openfaas
```

You should see the combined output:

```
This should be an error message.
{"Hello": "OpenFaaS"}
```

> Note: If you check the container logs with `docker service logs hello-openfaas` (or `kubectl logs deployment/hello-openfaas -n openfaas-fn`) you should not see the stderr output.

In the example we need the function to return valid JSON that can be parsed. Unfortunately the log message makes the output invalid,
so we need to redirect the messages from stderr to the container's logs.
OpenFaaS provides a solution so you can print the error messages to the logs and keep the function response clear, returning only `stdout`.
You should use the `combine_output` flag for that purposes.

Let's try it. Open the `hello-openfaas.yml` file and add those lines:

```yaml
    environment:
      combine_output: false
```

Deploy and invoke the function.

The output should be:

```
{"Hello": "OpenFaaS"}
```

Check the container logs for `stderr`. You should see a message like:

```
hello-openfaas.1.2xtrr2ckkkth@linuxkit-025000000001    | 2018/04/03 08:35:24 stderr: This should be an error message.
```

## Create Workflows

There will be situations where it will be useful to take the output of one function and use it as an input to another.  This is achievable both client-side and via the API Gateway. 

### Chaining functions on the client-side

You can pipe the result of one function into another using `curl`, the `faas-cli` or some of your own code. Here's an example:

Pros:

* requires no code - can be done with CLI programs
* fast for development and testing
* easy to model in code

Cons:

* additional latency - each function goes back to the server
* chatty (more messages)

Example:

* Deploy the NodeInfo function from the *Function Store*

* Then push the output from NodeInfo through the Markdown converter

```sh
$ echo -n "" | faas-cli invoke nodeinfo | faas-cli invoke markdown
<p>Hostname: 64767782518c</p>

<p>Platform: linux
Arch: x64
CPU count: 4
Uptime: 1121466</p>
```

You will now see the output of the NodeInfo function decorated with HTML tags such as: `<p>`.

Another example of client-side chaining of functions may be to invoke a function that generates an image, then send that image into another function which adds a watermark.

### Call one function from another

The easiest way to call one function from another is make a call over HTTP via the OpenFaaS *API Gateway*. This call does not need to know the external domain name or IP address, it can simply refer to the API Gateway as `gateway` through a DNS entry.

When accessing a service such as the API gateway from a function it's best practice to use an environmental variable to configure the hostname, this is important for two reasons - the name may change and in Kubernetes a suffix is sometimes needed.

Pros:

* functions can make use of each other directly
* low latency since the functions can access each other on the same network

Cons:

* requires a code library for making the HTTP request

Example:

In [Lab 3](./lab3.md) we introduced the requests module and used it to call a remote API to get the name of an astronaut aboard the ISS. We can use the same technique to call another function deployed on OpenFaaS.

* Using the UI, go to the *Function Store* and deploy the *Sentiment Analysis* function.

Alternatively use the CLI:
```
$ faas-cli store deploy SentimentAnalysis
```

The Sentiment Analysis function will tell you the subjectivity and polarity (positivity rating) of any sentence. The result of the function is formatted in JSON as per the example below:

```sh
$ echo -n "California is great, it's always sunny there." | faas-cli invoke sentimentanalysis
{"polarity": 0.8, "sentence_count": 1, "subjectivity": 0.75}
```

So the result shows us that our test sentence was both very subjective (75%) and very positive (80%). The values for these two fields are always between `-1.00` and `1.00`.

The following code can be used to call the *Sentiment Analysis* function or any other function:

Suffix the gateway host with `openfaas` namespace:
```python
    r = requests.get("http://gateway.openfaas:8080/function/sentimentanalysis", text= test_sentence)
```

Or via an environmental variable:

```python
    gateway_hostname = os.getenv("gateway_hostname", "gateway.openfaas") # uses a default of "gateway.openfaas" for when "gateway_hostname" is not set
    test_sentence = "California is great, it's always sunny there."
    r = requests.get("http://" + gateway_hostname + ":8080/function/sentimentanalysis", data= test_sentence)
```

Since the result is always in JSON format we can make use of the helper function `.json()` to convert the response:

```python
    result = r.json()
    if result["polarity"] > 0.45:
       return "That was probably positive"
    else:
        return "That was neutral or negative"
```

Now create a new function in Python and bring it all together

```python
import os
import requests
import sys

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    gateway_hostname = os.getenv("gateway_hostname", "gateway.openfaas") # uses a default of "gateway" for when "gateway_hostname" is not set

    test_sentence = req

    r = requests.get("http://" + gateway_hostname + ":8080/function/sentimentanalysis", data= test_sentence)

    if r.status_code != 200:
        sys.exit("Error with sentimentanalysis, expected: %d, got: %d\n" % (200, r.status_code))

    result = r.json()
    if result["polarity"] > 0.45:
        return "That was probably positive"
    else:
        return "That was neutral or negative"
```

* Remember to add `requests` to your `requirements.txt` file

Note: you do not need to modify or alter the source for the SentimentAnalysis function, we have already deployed it and will access it via the API gateway.

Now move on to [Lab 5](lab5.md).
