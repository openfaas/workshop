# Lab 8 - Auto-scaling in action

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

As described [here](http://docs.openfaas.com/architecture/autoscaling/) in the documentation OpenFaaS ships with auto-scaling in this lab we will have a look how the auto-scaling works in action.

## Pre-requisites:

* At this point, it is expected you already have set up OpenFaaS for Docker Swarm as described in [Lab 1](https://github.com/openfaas/workshop/blob/master/lab1.md).

* As we need a way to invoke our function to demonstrate auto-scaling it is expected that you have access to Curl or another to which allows you to do an HTTP-Request.


## Explore Auto-scaling:

Before dive into a hands-on session, we will have a brief look how we can configure the auto-scaling out of the box. You can find more information on auto-scaling in the [official documentation](http://docs.openfaas.com/architecture/autoscaling/).

Out of the box OpenFaaS is set up in a way that it will auto-scale based on the received `request per seconds`. If the defined threshold for the `request per seconds` is exceeded the AlertManager will fire. 

For each fired alarm the auto-scaler will add 5 instances to the affected function. OpenFaaS has two configuration options that allow to specify the starting/minimum amount of instances and also allows to ceil the maximum amount of instances:

You can control the minimum amount of instances for function by setting `com.openfaas.scale.min`, the default value is currently `1`. 

You can control the maximum amount of instances that can spawn for a function by setting `com.openfaas.scale.max`, the default value is currently `20`. 

> Note: If you set `com.openfaas.scale.min` and `com.openfaas.scale.max` to the same value you are disabling the auto-scaling feature. So pay attention to not do this accidentally. 

## Hands-on:

### Preparing Prometheus:

Firstly we will visit our local Prometheus, you can do so by visiting `http://localhost:9090/graph` in the browser of your choice. Prometheus will allow us later to see the auto-scaling in action.

Let's add a graph with all successful invocation of the deployed functions. We can do this by executing `gateway_function_invocation_total{code="200"}` as a query. Resulting in a page that looks like this: 

 ![](./screenshot/prometheus_graph.png)

 Go ahead an open a new tab in which you navigate to the alert section using `http://localhost:9090/alerts`. On this page, you can later see when the threshold for the `request per seconds` is exceeded.

 ![](./screenshot/prometheus_alerts.png)

 ### Invoking function:

 Using the following little bash-command we can constantly invoke the `func_nodeinfo` function.

 ```bash
$ while [ true ]; do curl -X POST http://localhost:8080/function/func_nodeinfo; done;
 ```

### Observing AutoScaling:

You should now be able to see an increase of invocation for the `func_nodeinfo` function in the graph we created earlier. Move over to the tab where you have open the alerts page. After a time period, you should start seeing that the `APIHighInvocationRate` state (and color) changes to `Pending` before then once again changing to `Firing`. You are also able to see the auto-scaling using the `$ faas-cli list` or over the [Ui](http://localhost:8080)

 ![](./screenshot/prometheus_firing.png)

Now you can verify using `$ docker ps` that new instances of `func_nodeinfo` got spawned. Which also concludes this lab on auto-scaling. 

You can return to the [main page](./README.md).
