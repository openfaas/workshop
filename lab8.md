# Lab 8 - Advanced function features

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
$ faas-cli new --lang python3 sleep-for --prefix="<your-docker-username-here>"
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
  gateway: http://127.0.0.1:8080

functions:
  sleep-for:
    lang: python3
    handler: ./sleep-for
    image: <your-docker-username-here>/sleep-for:0.1
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

## Use of Secrets

[Lab 5](./lab5.md) looked at how the `issue-bot` could obtain the GitHub *Personal Access Token* from an environment variable (`auth_token`).  An alternative approach is to use a **secret** to store sensitive information.

From the Docker documentation: 
> .. a secret is a blob of data, such as a password, SSH private key, SSL certificate, or another piece of data that should not be transmitted over a network or stored unencrypted in a Dockerfile or in your application’s source code.

This is a more secure alternative to environmental variables. Environmental variables are easier to use but are best suited to non-confidential configuration items.  Seems a good fit for storing the `auth_token` value.  

### Create a secret

> Use of underscores (_) in secret names should be avoided to make it easier to move between Docker Swarm and Kubernetes. 

From a terminal run the following command:

```
$ echo -n <auth_token> | docker secret create auth-token -
```

Test that the secret was created:

```
$ docker secret inspect auth-token
```

When the secret is mounted by a function it will be presented as a file under `/run/secrets/auth-token`. This can be read by `handler.py` to obtain the GitHub *Personal Access Token*.

### Update issue-bot.yml

Replace the reference to `env.yml` with an instruction to make the `auth-token` secret available to the function:

```yml
provider:
  name: faas
  gateway: http://127.0.0.1:8080

functions:
  issue-bot:
    lang: python3
    handler: ./issue-bot
    image: <your-username>/issue-bot
    environment:
      write_debug: true
      gateway_hostname: "gateway"
      positive_threshold: 0.25
    secrets:
      - auth-token

```

### Update the `issue-bot` function

The function handler requires changing in order to cause it to read the `auth-token` secret, rather than the environment variable.  This is a single line change where:

```python
g = Github(os.getenv("auth_token"))
``` 
is replaced with 
```python
with open("/run/secrets/auth-token","r") as authToken:  
    g = Github(authToken.read())
```

> The full source code is  available at [issue-bot-secrets/bot-handler/handler.py](./issue-bot-secrets/bot-handler/handler.py)

* Build and deploy

Use the CLI to build and deploy the function:

```
$ faas-cli build -f issue-bot.yml \
  && faas-cli push -f issue-bot.yml \
  && faas-cli deploy -f issue-bot.yml
```

## Auto-scaling in action

As described in the [documentation](http://docs.openfaas.com/architecture/autoscaling/) OpenFaaS ships with auto-scaling. In this lab we will have a look how the auto-scaling works in action.

### Pre-requisites:

* Having completed the set-up of OpenFaaS in [Lab 1](./lab1.md) you will have everything required to trigger auto-scaling.

* Multiple tools can be used to create enough traffic to trigger auto-scaling - in this example `curl` will be used as it is easily available for Mac, Linux and is packaged with Git Bash on Windows.

### Background on auto-scaling

Out of the box OpenFaaS is configured such that it will auto-scale based upon the `request per seconds` metric as measured through Prometheus.  This measure is captured as traffic passes through the API Gateway. If the defined threshold for `request per seconds` is exceeded the AlertManager will fire. This threshold should be reconfigured to an appropriate level for production usage as for demonstration purposes it has been set to a low value in this example.

> Find more information on auto-scaling in the [documentation site](http://docs.openfaas.com/architecture/autoscaling/).

Each time the alert is fired by AlertManager the API Gateway will add a certain number of replicas of your function into the cluster. OpenFaaS has two configuration options that allow to specify the starting/minimum amount of replicas and also allows to ceil the maximum amount of replicas:

You can control the minimum amount of replicas for function by setting `com.openfaas.scale.min`, the default value is currently `1`. 

You can control the maximum amount of replicas that can spawn for a function by setting `com.openfaas.scale.max`, the default value is currently `20`. 

> Note: If you set `com.openfaas.scale.min` and `com.openfaas.scale.max` to the same value you are disabling the auto-scaling feature. 

### Check out Prometheus

Open Prometheus in a web-browser: `http://127.0.0.1:9090/graph`

Now add a graph with all successful invocation of the deployed functions. We can do this by executing `rate( gateway_function_invocation_total{code="200"} [20s])` as a query. Resulting in a page that looks like this:

 ![](./screenshot/prometheus_graph.png)

 Go ahead an open a new tab in which you navigate to the alert section using `http://127.0.0.1:9090/alerts`. On this page, you can later see when the threshold for the `request per seconds` is exceeded.

 ![](./screenshot/prometheus_alerts.png)

### Trigger scaling of NodeInfo

First deploy nodeinfo via the store:

```bash
$ faas store deploy nodeinfo
```

Now check the UI to see when the nodeinfo function becomes available.

Use this script to invoke the `nodeinfo` function over and over until you see the replica count go from 1 to 5 and so on. You can monitor this value in Prometheus by adding a graph for `gateway_service_count` or by viewing the API Gateway with the function selected.

 ```bash
$ while [ true ]; do curl -X POST http://127.0.0.1:8080/function/nodeinfo; done;
 ```

### Monitor for alerts

You should now be able to see an increase in invocations of the `nodeinfo` function in the graph that was created earlier. Move over to the tab where you have open the alerts page. After a time period, you should start seeing that the `APIHighInvocationRate` state (and colour) changes to `Pending` before then once again changing to `Firing`. You are also able to see the auto-scaling using the `$ faas-cli list` or over the [ui](http://127.0.0.1:8080)

 ![](./screenshot/prometheus_firing.png)

Now you can verify using `$ docker service ps nodeinfo` that new replicas of `nodeinfo` have been started.

Now stop the bash script and you will see the replica count return to 1 replica after a few seconds.

You can return to the [main page](./README.md).