# Lab 8 - Auto-scaling in action

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

As described [here](http://docs.openfaas.com/architecture/autoscaling/) in the documentation Open FaaS ships with auto-scaling in this lab we will have a look how the auto-scaling works in action.

## Pre-requisites:

* At this point, it is expected you already have set up Open FaaS for Docker Swarm as described in [Lab 1](https://github.com/openfaas/workshop/blob/master/lab1.md).

* As we need a way to invoke our lambda to demonstrate auto-scaling it is expected that you have access to [Curl](http://macappstore.org/curl/) or another to which allows you to do an HTTP-Request.


## Exploring Auto-Scaling:

Before dive into a hands-on session, we will have a brief look how we can configure the auto-scaling out of the box. 

Out of the box Open FaaS is set up in a way that it will auto-scale based on the received `request per seconds`. If the defined threshold for the `request per seconds` is exceeded the AlertManager will fire. 

> If you want the scaling happening based on CPU and Memory usage please have a brief look at [this blog](https://stefanprodan.com/2018/kubernetes-scaleway-baremetal-arm-terraform-installer/#horizontal-pod-autoscaling)

For each fired alarm the auto-scaler will add 5 instances to the affected lambda. Open FaaS has two configuration options that allow to specify the starting/minimum amount of instances and also allows to ceil the maximum amount of instances:

You can control the minimum amount of instances for lambda by setting `com.openfaas.scale.min`, the default value is currently `1`. 

You can control the maximum amount of instances that can spawn for a lambda by setting `com.openfaas.scale.max`, the default value is currently `20`. 

> Note: If you set `com.openfaas.scale.min` and `com.openfaas.scale.max` to the same value you are disabling the auto-scaling feature. So pay attention to not do this accidentally. 

## Hands-on:

### Preparing Prometheus:

Firstly we will discover under which port our Prometheus is accessible. As it will allow us later to see the auto-scaling kicking in.

Using  `$  docker ps --filter "name=func_prometheus*" --format "{{.Names}} : {{.Status}} | {{.Ports}}"` you should be able to see the port.

> Sample Output: `func_prometheus.1.dvffhruuarhf9xp5iqojpmexk : Up 9 minutes | 9090/tcp`

Now you should be able using the discovered port to open your Prometheus in the browser of your choice by visiting `http://localhost:9090/graph`. 

 Let's add a graph with all successful invocation of the deployed lambdas. We can do this by executing `gateway_function_invocation_total{code="200"}` as a query. Resulting in a page that looks like this: 

 ![](./screenshot/prometheus_graph.png)

 Go ahead an open a new tab in which you navigate to the alert section using `http://localhost:9090/alerts`. On this page, you can later see when the threshold for the `request per seconds` is exceeded.

 ![](./screenshot/prometheus_alerts.png)

 ### Invoking Lambda:

 Using the following little bash-command we can constantly invoke the `func_nodeinfo` lambda.

 ```bash
$ while [ true ]; do curl -X POST http://localhost:8080/function/func_nodeinfo; done;
 ```

### Observing Auto Scaling:

You should now be able to see the increase of invocation for the `func_nodeinfo` lambda in the graph we did earlier. Move over to the tab where you have open the alerts page. After a time period, you should start seeing that the `APIHighInvocationRate` state (and color) changes to `Pending` before then once again changing to `Firing`.

 ![](./screenshot/prometheus_firing.png)

Now you can verify using `$ docker ps` that new instances of `func_nodeinfo` got spawned. Which also concludes this lab on auto-scaling. Now you can return to the [main page](./README.md).
