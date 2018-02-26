# openfaas-workshop

This is a self-paced workshop on OpenFaaS running on Kubernetes.

Requirements:

* Functions will be written in Python, so prior programming or scripting experience is preferred 
* Preferred OS: MacOS, Linux, Windows 10 Pro
* Kubernetes
 * Docker for Mac Edge
 * Or an account on DigitalOcean to provision a small Kubernetes cluster

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

## [Lab 3 - Introduction to Functions](./lab1.md)

* Scaffold or generate a new function
* Add dependencies with `pip`
* Use third-party language templates

## [Lab 4 - Go deeper with functions](./lab1.md)

* Enable verbose output on functions with `write_debug`
* Extend timeouts with `read_timeout`
* Inject configuration through environmental variables
* Use HTTP context - querystring / headers etc

# [Lab 4 - Asynchronous Functions](./lab1.md)

* Call a function asynchronously vs synchronously
* View the queue-worker's logs
* Use an `X-Callback-Url` with requestbin and ngrok

# [Lab 5 - Chain Functions](./lab1.md)

* Make use of another function
* Director pattern

# [Lab 6 - Put it all together](./lab1.md)

> Triaging customer feedback from Twitter

* Receiving Tweets from IFTTT.com
* Filtering out unwanted messages
* Sorting good + bad with SentimentAnalysis
* Forwarding to two different Slack channels

You can start with the first lab [Lab 1](lab1.md).



Advanced topics:

* Monitoring your functions with a dashboard in Grafana
* TLS
* Basic auth
* Add a new language template
* Object storage with Minio
