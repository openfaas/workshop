# Lab 8 - Advanced feature - Timeouts

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

Now move onto [Lab 9](lab9.md)