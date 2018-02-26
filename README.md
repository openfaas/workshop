# openfaas-workshop

This is a self-paced workshop on OpenFaaS running on Kubernetes.

Requirements:

* Functions will be written in Python, so prior programming or scripting experience is preferred 
* Preferred OS: MacOS, Linux, Windows 10 Pro
* Kubernetes
 * Docker for Mac Edge
 * Or an account on DigitalOcean to provision a small Kubernetes cluster
* Installed [VSCode](https://code.visualstudio.com/download)

> Disclaimer: this is a work-in-progress.

## [Lab 1 - Prepare for OpenFaaS](./lab1.md)

* Install pre-requisites
* Docker Hub account
* OpenFaaS CLI
* Set up a single-node cluster with Docker Swarm
* Deploy OpenFaaS

## [Lab 2 - Test things out](./lab2.md)

* Use the UI Portal
* Learn about the CLI
* Deploy via the Function Store
* Find metrics with Prometheus

## [Lab 3 - Introduction to Functions](./lab3.md)

* Scaffold or generate a new function
* Build the space-counter function
 * Add dependencies with `pip`
* Troubleshooting: verbose output with `write_debug`
* Troubleshooting: find the container's logs
* Use third-party language templates

## [Lab 4 - Go deeper with functions](./lab4.md)

* Extend timeouts with `read_timeout`
* Inject configuration through environmental variables
* Use HTTP context - querystring / headers etc

## [Lab 5 - Asynchronous Functions](./lab5.md)

* Call a function asynchronously vs synchronously
* View the queue-worker's logs
* Use an `X-Callback-Url` with requestbin and ngrok

## [Lab 6 - Chain or combine Functions into workflows](./lab6.md)

* Make use of another function
* Director pattern

## [Lab 7 - Put it all together](./lab7.md)

> Triaging customer feedback from Twitter

* Receiving Tweets from IFTTT.com
* Filtering out unwanted messages
* Sorting good + bad with SentimentAnalysis
* Forwarding to two different Slack channels

You can start with the first lab [Lab 1](lab1.md).

## Wrapping up

If you're taking an instructor-led workshop, we'll now take Q&A and cover some advanced topics too.

* What is auto-scaling and how does it work?
* How to monitoring functions with a dashboard in Grafana
* How to enable TLS for security
* How to lock down the gateway with Basic Authentication
* Object storage with S3/Minio
* How to build your own templates
    * How to customise the templates
