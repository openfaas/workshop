# openfaas-workshop

This is a self-paced workshop for learning how to build, deploy and run serverless functions with OpenFaaS.

![](https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png)

In this workshop you begin by deploying OpenFaaS to your laptop or a remote cluster with Docker for Mac or Windows. You will then kick the tires with the OpenFaaS UI, CLI and Function Store. After building, deploying an invoking your own Serverless Functions in Python you'll go on to cover topics such as: managing dependencies with pip, dealing with API tokens through secure secrets, monitoring functions with Prometheus, invoking functions asynchronously and chaining functions together to create applications. The labs culminate by having you create your very own GitHub bot which can respond to issues automatically. The same method could be applied by connecting to online event-streams through IFTTT.com - this will enable you to build bots, auto-responders and integrations with social media and IoT devices.

Finally the labs cover more advanced topics and give suggestions for further learning.

**Translations**

* [日本語](./translations/ja)

## Learn for free, show your appreciation as a GitHub Sponsor

OpenFaaS along with these materials are provided for free and require time and effort to maintain.

* Become a sponsor for [OpenFaaS on GitHub](https://github.com/sponsor/openfaas)

## Requirements:

We walk through how to install these requirements in [Lab 1](./lab1.md). Please do [Lab 1](./lab1.md) before you attend an instructor-led workshop.

* Functions will be written in Python, so prior programming or scripting experience is preferred 
* Install the recommended code-editor / IDE [VSCode](https://code.visualstudio.com/download)
* For Windows install [Git Bash](https://git-scm.com/downloads)
* Preferred OS: MacOS, Windows 10 Pro/Enterprise, Ubuntu Linux

Docker:

* Docker CE for [Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)/[Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows) **Edge edition**
* Docker CE for Linux

> Note: As a last resort if you have an incompatible PC you can run the workshop on https://labs.play-with-docker.com/.

## Instructor-led workshops

If you're taking an instructor-led workshops then a link will be shared to join the OpenFaaS Slack community. Use the designated channel for the workshop to discuss comments, questions and suggestions.

## Pick your track

In Lab 1 you will pick your track and then throughout the labs look out for any special commands needed for the container orchestrator for your track.

### Kubernetes

You can also learn about Serverless on Kubernetes using OpenFaaS.

The recommendation from the OpenFaaS community is that you run Kubernetes in production, but all the knowledge you can is transferrable and functions do not have to be rebuilt.

## [Lab 1 - Prepare for OpenFaaS](./lab1.md)

* Install pre-requisites
* Set up a single-node cluster with Kubernetes
* Docker Hub account
* OpenFaaS CLI
* Deploy OpenFaaS

## [Lab 2 - Test things out](./lab2.md)

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
* Use custom and third-party language templates
* Discover community templates using the Template Store

## [Lab 4 - Go deeper with functions](./lab4.md)

* [Inject configuration through environmental variables](lab4.md#inject-configuration-through-environmental-variables)
  * At deployment using yaml
  * Dynamically using HTTP context - querystring / headers etc
* Security: read-only filesystems
* [Making use of logging](lab4.md#making-use-of-logging)
* [Create Workflows](lab4.md#create-workflows)
  * Chaining functions on the client-side
  * Call one function from another

## [Lab 5 - Create a GitHub bot](./lab5.md)

> Build `issue-bot` - an auto-responder for GitHub Issues

* Get a GitHub account
* Set up a tunnel with ngrok
* Create an webhook receiver `issue-bot`
* Receive webhooks from GitHub
* Deploy SentimentAnalysis function
* Apply labels via the GitHub API
* Complete the function

## [Lab 6 - HTML for your functions](./lab6.md)

* Generate and return basic HTML from a function
* Read and return a static HTML file from disk
* Collaborate with other functions

## [Lab 7 - Asynchronous Functions](./lab7.md)

* Call a function synchronously vs asynchronously
* View the queue-worker's logs
* Use an `X-Callback-Url` with requestbin and ngrok

## [Lab 8 - Advanced Feature - Timeouts](./lab8.md)

* Adjust timeouts with `read_timeout`
* Accommodate longer running functions

## [Lab 9 - Advanced Feature - Auto-scaling](./lab9.md)

* See auto-scaling in action
  * Some insights on min and max replicas
  * Discover and visit local Prometheus
  * Execute and Prometheus query
  * Invoke a function using curl
  * Observe auto-scaling kicking in

## [Lab 10 - Advanced Feature - Secrets](./lab10.md)

* Adapt issue-bot to use a secret
  * Create a Kubernetes secret with faas-cli
  * Access the secret within the function

## [Lab 11 - Advanced feature - Trust with HMAC](./lab11.md)

* Apply trust to functions using HMAC

You can start with the first lab [Lab 1](lab1.md).

## Tear down / Clear up

You can find how to stop and remove OpenFaaS [here](https://docs.openfaas.com/deployment/troubleshooting/#uninstall-openfaas)

## Next steps

If you're in an instructor-led workshop and have finished the labs you may want to go back through the labs and edit/alter the code and values or carry out some of your own experiments.

Here are some ideas for follow-on tasks / topics:

### OpenFaaS Cloud

Try the multi-user, managed experience of OpenFaaS - either on the Community Cluster, or by hosting your own OpenFaaS Cloud.

* [Docs: OpenFaaS Cloud](https://docs.openfaas.com/openfaas-cloud/intro/)

### TLS

* [Enable HTTPS on your gateway with Kubernetes Ingress](https://docs.openfaas.com/reference/ssl/kubernetes-with-cert-manager/)

### CI/CD

Setup Jenkins, Google Cloud Build or GitLab and build and deploy your own functions using the OpenFaaS CLI:

* [Intro to CI/CD](https://docs.openfaas.com/reference/cicd/intro/)

### Storage / databases

* [Try open-source object storage with Minio](https://blog.alexellis.io/openfaas-storage-for-your-functions/)

* [Try OpenFaaS with Mongo for storing data](https://blog.alexellis.io/serverless-databases-with-openfaas-and-mongo/)

### Instrumentation / monitoring

* [Explore the metrics available in Prometheus](https://docs.openfaas.com/architecture/metrics/#monitoring-functions)

### Additional blog posts and tutorials

* [Tutorials on the OpenFaaS blog](https://www.openfaas.com/blog/)

* [Community blog posts](https://github.com/openfaas/faas/blob/master/community.md)

### Appendix

The [appendix](./appendix.md) contains some additional content.

## Acknowledgements

Thanks to @iyovcheva, @BurtonR, @johnmccabe, @laurentgrangeau, @stefanprodan, @kenfdev, @templum & @rgee0 for contributing to, testing and translating the labs.
