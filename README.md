# openfaas-workshop

This is a self-paced workshop for learning how to build, deploy and run OpenFaaS functions.

![](https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png)

> This workshop starts by deploying OpenFaaS your laptop with Docker for Mac or Windows and then shows how to build, deploy and invoke Serverless functions in Python. Topics will include: managing dependencies with pip, dealing with API tokens through secure secrets, monitoring functions with Prometheus, invoking functions asynchronously and chaining functions together to create applications. We finish by connecting to online event-streams through IFTTT.com - this will enable you to build bots, auto-responders and integrations with social media and IoT devices.

Requirements:

* Functions will be written in Python, so prior programming or scripting experience is preferred 
* Install the recommended code-editor / IDE [VSCode](https://code.visualstudio.com/download)
* For Windows install [Git Bash](https://git-scm.com/downloads)
* Preferred OS: MacOS, Windows 10 Pro/Enterprise, Ubuntu Linux

Docker:

* Docker for Mac/Windows **Edge edition**
* Docker CE for Linux

> Note: As a last resort if you have an incompatible PC you can run the workshop on [http://play-with-docker.com](play-with-docker.com).

Disclaimer: this workshop is a work-in-progress - labs 2-5 are ready.

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
* Build the astronaut-finder function
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
