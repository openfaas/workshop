# openfaas-workshop

This is a self-paced workshop for learning how to build, deploy and run OpenFaaS functions.

![](https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png)

> This workshop starts by deploying OpenFaaS to your laptop with Docker for Mac or Windows and then shows how to build, deploy and invoke Serverless functions in Python. Topics will include: managing dependencies with pip, dealing with API tokens through secure secrets, monitoring functions with Prometheus, invoking functions asynchronously and chaining functions together to create applications. We finish by creating a GitHub bot which automatically respond to issues. The same method could be applied by connecting to online event-streams through IFTTT.com - this will enable you to build bots, auto-responders and integrations with social media and IoT devices.

## Requirements:

We walk through how to install these requirements in [Lab 1](./lab1.md), but please do this before you attend an instructor-led workshop.

* Functions will be written in Python, so prior programming or scripting experience is preferred 
* Install the recommended code-editor / IDE [VSCode](https://code.visualstudio.com/download)
* For Windows install [Git Bash](https://git-scm.com/downloads)
* Preferred OS: MacOS, Windows 10 Pro/Enterprise, Ubuntu Linux

Docker:

* Docker CE for [Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)/[Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows) **Edge edition**
* Docker CE for Linux

> Note: As a last resort if you have an incompatible PC you can run the workshop on [https://labs.play-with-docker.com/](play-with-docker.com).

## Instructor-led workshops

If you're taking an instructor-led workshops then a link will be shared to join the OpenFaaS Slack community. Use the designated channel for the workshop to discuss comments, questions and suggestions.

## [Lab 1 - Preparing OpenFaaS](./lab1.md)

* Install pre-requisites
* Set up a single-node cluster with Docker Swarm
* Docker Hub account
* OpenFaaS CLI
* Deploy OpenFaaS

## [Lab 2 - Testing things out](./lab2.md)

* Use the UI Portal
* Deploy via the Function Store
* Learn about the CLI
* Find metrics with Prometheus

## [Lab 3 - Introduction to Functions](./lab3.md)

* Scaffold or generate a new function
* Build the astronaut-finder function
 * Add dependencies with `pip`
 * Troubleshooting: find the container's logs
* Troubleshooting: verbose output with `write_debug`
* Use third-party language templates

## [Lab 4 - Go deeper with functions](./lab4.md)

* Extend timeouts with `read_timeout`
* Inject configuration through environmental variables
* Use HTTP context - querystring / headers etc

## [Lab 5 - Asynchronous Functions](./lab5.md)

* Call a function synchronously vs asynchronously
* View the queue-worker's logs
* Use an `X-Callback-Url` with requestbin and ngrok

## [Lab 6 - Chain or combine Functions into workflows](./lab6.md)

* Chaining functions on the client-side
* Call one function from another

## [Lab 7 - Put it all together](./lab7.md)

> Build `issue-bot` - an auto-responder for GitHub Issues

* Get a GitHub account
* Set up a tunnel with ngrok
* Create an webhook receiver `issue-bot`
* Receive webhooks from GitHub
* Deploy SentimentAnalysis function
* Apply labels via the GitHub API
* Complete the function

You can start with the first lab [Lab 1](lab1.md).

## Tear down / Clear up

You can find how to stop and remove OpenFaaS [here](https://github.com/openfaas/faas/blob/master/guide/troubleshooting.md#stop-and-remove-openfaas)

## Wrapping up

If you're taking an instructor-led workshop, we'll now take Q&A and cover some advanced topics:

* Auto-scaling
* Security
  * TLS / Basic Authentication
* Object storage
* Customisations for templates

The [appendix](./appendix.md) contains some additional content.

## Acknowledgements

Thanks to @iyovcheva, @BurtonR, @johnmccabe, @laurentgrangeau, @stefanprodan  for testing and contributing to the labs.
