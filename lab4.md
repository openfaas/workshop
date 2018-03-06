# Lab 4 - Go deeper with functions

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

## Extend timeouts with `read_timeout`

The *timeout* corresponds to how long a function can run for until it is executed. It is important for preventing misuse in distributed systems.

There are several places where a timeout can be configured for your function, in each place this is done through the use of environmental variables.

* Function timeout

* `read_timeout` - time allowed fo the function to read a request over HTTP
* `write_timeout` - time allowed for the function to write a response over HTTP
* `exec_timeout` - the maximum duration a function can run before being terminated

The API Gateway has a default of 20 seconds, so let's test out setting a shorter timeout on a function.

```
$ faas-cli new --lang python sleep-for --prefix="<your-docker-username-here>"
```

Edit `handler.py`:

```python
import time
import os

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    sleep_duration = int(os.getenv("sleep_duration", "10"))
    print("Starting to sleep for %d" % sleep_duration)
    time.sleep(sleep_duration)  # Sleep for a number of seconds
    print("Finished the sleep")
```

Now edit the `sleep-for.yml` file and add these environmental variables:

```yaml
provider:
  name: faas
  gateway: http://localhost:8080

functions:
  sleep-for:
    lang: python
    handler: ./sleep-for
    image: sleep-for:0.1
    environment:
      sleep_duration: 10
      read_timeout: 5
      write_timeout: 5
      exec_timeout: 5
```

Use the CLI to build, push, deploy and invoke the function.

```
$ echo | faas-cli invoke sleep-for
Server returned unexpected status code: 500 - Can't reach service: sleep-for
```

You should see it terminate without printing the message.

Now set `sleep_duration` to a lower number like `2` and run `faas-cli deploy` again. You don't need to rebuild the function when editing the function's YAML file.

```
$ echo | faas-cli invoke sleep-for
Starting to sleep for 2
Finished the sleep
```

* API Gateway

This is the maximum timeout duration as set at the gateway, it will override the function timeout. At the time of writing the maximum timeout is configured at "20s", but can be configured to a longer or shorter value.

To update the gateway value set `read_timeout` and `write_timeout` in the `docker-compose.yml` file for the `gateway` and `faas-swarm` service then run `./deploy_stack.sh`.

## Inject configuration through environmental variables

It is useful to be able to control how a function behaves at runtime, we can do that in at least two ways:

### At deployment time

* Set environmental variables at deployment time

We did this with `write_debug` and `exec_timeout` - you can also set any custom environmental variables you want here too - for instance if you wanted to configure a language for your *hello world* function you may introduce a `spoken_language` variable.

### Use HTTP context - querystring / headers

* Use querystring and HTTP headers

The other option which is more dynamic and can be altered at a per-request level is the use of querystrings and HTTP headers, both can be passed through the `faas-cli` or `curl`.

These headers become exposed through environmental variables so they are easy to consume within your function. So any header is prefixed with `Http_` and all `-` hyphens are replaced with an `_` underscore.

Let's try it out with a querystring and a function that lists off all environmental variables.

* Deploy a function that prints environmental variables using a built-in BusyBox command:

```
$ faas-cli deploy --name env --fprocess="env" --image="functions/alpine:latest" --network=func_functions
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
Http_Path=/function/env
...
Http_Query=workshop=1
...
```

In Python code you'd type in `os.getenv("Http_Query")`.

* Now invoke it with a header:

```
$ echo "" | curl http://127.0.0.1:8080/function/env --header "X-Output-Mode: json"
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
Http_Path=/function/env
...
Http_X_Output_Mode=json
...
```

In Python code you'd type in `os.getenv("Http_X_Output_Mode")`.

You can see that all other HTTP context is also provided such as `Content-Length` when the `Http_Method` is a `POST`, the `User_Agent`, Cookies and anything else you'd expect to see from a HTTP request.

### Summarising environmental variables.

In Python you can find environmental variables through the `os.getenv(key, default_value)` function or `os.environ` array after importing the `os` package. The OpenFaaS watchdog provides all HTTP context to your function through environmental variables. They can be used at deployment time or at runtime to alter the behaviour of your code.

i.e.

```python
import os

def handle(st):
    print os.getenv("Http_Method")          # will be "NoneType" if empty
    print os.getenv("Http_Method", "GET")   # provide a default of "GET" if empty
    print os.environ["Http_Method"]         # throws an exception is not present
    print os.environ                        # array of environment
```

Now move onto [Lab 5](lab5.md)
