# Lab 5 - Create a GitHub bot

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

Before starting this lab, create a new folder for your files:

```
$ mkdir -p lab5 \
   && cd lab5
```

We're going to use OpenFaaS functions to create a GitHub bot named `issue-bot`.

The job of issue-bot is to triage new issues by analysing the sentiment of the "description" field, it will then apply a label of *positive* or *review*. This will help the maintainers with their busy schedule so they can prioritize which issues to look at first.

![Diagram of the issue bot](./diagram/issue-bot.png)

## Get a GitHub account

* Sign up for a [GitHub account](https://github.com) if you do not already have one.

* Create a new repository and call it *bot-tester*

Note: we will only use this repository as a testing ground for creating Issues. You don't need to commit any code there.

## Set up a tunnel with inlets

You will need to receive incoming webhooks from GitHub. Fortunately, inlets makes this very quick and simple. It's available on a monthly or annual subscription, so if you are not sure if you are going to need it all year, you can just pay for a single month.

inlets has a Kubernetes integration called the inlets-operator. You can use it to setup LoadBalancers or Ingress with TLS. It works by creating a cloud VM for you and running a tunnel server there, it then runs a tunnel client as a Pod for you and you get incoming traffic.

Create a write access token under the API page of your preferred cloud provider, such as DigitalOcean, then save the contents to `digital-ocean-api-token.txt`.

After setting your subscription, save your key to `$HOME/.inlets/LICENSE` and run the following:

```bash
arkade install inlets-operator \
  --provider digitalocean \
  --region lon1 \
  --token-file $HOME/digital-ocean-api-token.txt
```

This will deploy the inlets-operator and instruct it to provision new hosts on DigitalOcean into the London region for your tunnel servers. Other providers and regions are available, [see the docs for more](https://docs.inlets.dev/reference/inlets-operator/).

## Log into your gateway with the Gateway's public IP

Retrieve your gateway password with the message from:

```bash
arkade info openfaas
```

The public IP for the LoadBalancer will take around 10-30 seconds to appear:

```bash
kubectl get svc -n openfaas gateway-external
NAME               TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
gateway-external   LoadBalancer   10.96.29.46   <pending>     8080:32278/TCP   5h56m
gateway-external   LoadBalancer   10.96.29.46   165.227.233.227   8080:32278/TCP   5h56m
```

Then save it into an environment variable:

```bash
export OPENFAAS_URL=http://165.227.233.227:8080
```

Log in with the password you were given to the public IP:

```bash
echo $PASSWORD | faas-cli login --password-stdin
```

Finally test the remote URL such as http://165.227.233.227:8080

You can run commands against the remote gateway by setting the `OPENFAAS_URL` environment variable or by using the `--gateway` flag.

If you'd like to expose OpenFaaS with a TLS certificate and a custom domain, you can follow these instructions instead:

```bash
arkade install ingress-nginx
arkade install cert-manager
arkade install openfaas
arkade install openfaas-ingress \
  --email web@example.com \
  --domain openfaas.example.com
```

Then create a DNS A record pointing at the IP address of ingress-nginx:

```bash
kubectl get svc ingress-nginx-controller
NAME                       TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
NAME                       TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller   LoadBalancer   10.96.179.20   <pending>     80:30319/TCP,443:31591/TCP   20s
ingress-nginx-controller   LoadBalancer   10.96.179.20   209.97.135.63   80:30319/TCP,443:31591/TCP   52s
```

That'll now give you a custom TLS record for `https://openfaas.example.com`

## Create a webhook receiver `issue-bot`

```bash
export OPENFAAS_PREFIX="docker.io/your-username"
$ faas-cli new --lang python3 \
  issue-bot
```

Now edit the function's YAML file `issue-bot.yml` and add an environmental variable of `write_debug: true`:

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  issue-bot:
    lang: python3
    handler: ./issue-bot
    image: docker.io/your-username/issue-bot
    environment:
      write_debug: true
```

* Build, push and deploy the function with

```bash
$ faas-cli up -f ./issue-bot.yml
```

## Receive webhooks from GitHub

Log back into GitHub and navigate to your repository *bot-tester*

Click *Settings* -> *Webhooks* -> *Add Webhook*

![Adding the webhook](./screenshot/add_github_webhook.png)

Now enter the URL you were given from inlets or your custom domain adding `/function/issue-bot` to the end, for example:

```
https://openfaas.example.com
```

![Adding the webhook](./screenshot/issue-bot-webhook.png)

For *Content-type* select: *application/json*

Leave *Secret* blank for now.

And select "Let me select individual events"

For events select **Issues** and **Issue comment**

![Setting the events](./screenshot/WebhookEventsSettings.png)

## Check it worked

Now go to GitHub and create a new issue. Type "test" for the title and description.

Check how many times the function has been called - this number should be at least `1`.

```
$ faas-cli list
Function    Invocations
issue-bot   2
```

Each time you create an issue the count will increase due to GitHub's API invoking the function.

You can see the payload sent via GitHub by typing in `docker service logs -f issue-bot` (or `kubectl logs deployment/issue-bot -n openfaas-fn`).

The GitHub Webhooks page will also show every message sent under "Recent Deliveries", you can replay a message here and see the response returned by your function.

![Replaying an event](./screenshot/github_replay.png)

### Deploy SentimentAnalysis function

In order to use this issue-bot function, you will need to deploy the SentimentAnalysis function first.
This is a python function that provides a rating on sentiment positive/negative (polarity -1.0-1.0) and subjectivity provided to each of the sentences sent in via the TextBlob project.

If you didnt do so in [Lab 4](./lab4.md) you can deploy "SentimentAnalysis" from the **Function Store**

```
$ echo -n "I am really excited to participate in the OpenFaaS workshop." | faas-cli invoke sentimentanalysis
Polarity: 0.375 Subjectivity: 0.75

$ echo -n "The hotel was clean, but the area was terrible" | faas-cli invoke sentimentanalysis
Polarity: -0.316666666667 Subjectivity: 0.85
```

### Update the `issue-bot` function

Open `issue-bot/handler.py` and replace the template with this code:

```python
import requests, json, os, sys

def handle(req):

    event_header = os.getenv("Http_X_Github_Event")

    if not event_header == "issues":
        sys.exit("Unable to handle X-GitHub-Event: " + event_header)
        return

    gateway_hostname = os.getenv("gateway_hostname", "gateway.openfaas")

    payload = json.loads(req)

    if not payload["action"] == "opened":
        return

    #sentimentanalysis
    res = requests.post('http://' + gateway_hostname + ':8080/function/sentimentanalysis', data=payload["issue"]["title"]+" "+payload["issue"]["body"])

    if res.status_code != 200:
        sys.exit("Error with sentimentanalysis, expected: %d, got: %d\n" % (200, res.status_code))

    return res.json()
```

Update your `requirements.txt` file with the requests module for HTTP/HTTPs:

```
requests
```

Add `gateway_hostname` environment variable to `issue-bot.yml` file and set its value to `gateway.openfaas`.
``` 
    ...
    environment:
      gateway_hostname: "gateway.openfaas"
    ...
```

The following line from the code above posts the GitHub Issue's title and body to the `sentimentanalysis` function as text. The response will be in JSON format.

```python
res = requests.post('http://' + gateway_hostname + ':8080/function/sentimentanalysis', data=payload["issue"]["title"]+" "+payload["issue"]["body"])
```

* Build and deploy

Use the CLI to build and deploy the function:

```
$ faas-cli up -f issue-bot.yml
```

Now create a new issue in the `bot-tester` repository. GitHub will respond by sending a JSON payload to your function via the Inlets tunnel we configured earlier.

You can view the request/response directly on GitHub - navigate to *Settings* -> *Webhook* as below:

![](./screenshot/WebhookResponse.png)

## Respond to GitHub

The next step will be for us to apply a label of `positive` or `review`, but because this action involves writing to the repository we need to get a *Personal Access Token* from GitHub.

### Create a Personal Access Token for GitHub

Go to your *GitHub profile* -> *Settings/Developer settings* -> *Personal access tokens* and then click *Generate new token*.

![](./screenshot/PersonalAccessTokens.png)

Tick the box for "repo" to allow access to your repositories

![](./screenshot/NewPAT.png)

Click the "Generate Token" button at the bottom of the page

Create a file called `env.yml` in the directory where your `issue-bot.yml` file is located with the following content:

```yaml
environment:
  auth_token: <auth_token_value>
```

Update the `auth_token` variable with your token from GitHub.

Now update your issue-bot.yml file and tell it to use the `env.yml` file:

```yaml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  issue-bot:
    lang: python3
    handler: ./issue-bot
    image: <your-username>/issue-bot
    environment:
      write_debug: true
      gateway_hostname: "gateway.openfaas"
      positive_threshold: 0.25
    environment_file:
    - env.yml
```
> The `positive_threshold` environmental variable is used to fine-tune whether an Issue gets the `positive` or `review` label.

Any sensitive information is placed in an external file (i.e. `env.yml`) so that it can be included in a `.gitignore` file which will help prevent that information getting stored in a public Git repository.

OpenFaaS also supports the use of native Docker and Kubernetes secrets, details can be found in [Lab 10](lab10.md)

### Apply labels via the GitHub API

You can use the API to perform many different tasks, the [documentation is available here](https://github.com/PyGithub/PyGithub).

Here's a sample of Python code that we could use to apply a label, but you do not add it to your function yet.

```python
issue_number = 1
repo_name = "alexellis/issue_bot"
auth_token = "xyz"

g = Github(auth_token)
repo = g.get_repo(repo_name)
issue = repo.get_issue(issue_number)
```

This library for GitHub is provided by the community and is not official, but appears to be popular. It can be pulled in from `pip` through our `requirements.txt` file.

## Complete the function

* Update your `issue-bot/requirements.txt` file and add a line for `PyGithub`

```
requests
PyGithub
```

* Open `issue-bot/handler.py` and replace the code with this:

```python
import requests, json, os, sys
from github import Github

def handle(req):
    event_header = os.getenv("Http_X_Github_Event")

    if not event_header == "issues":
        sys.exit("Unable to handle X-GitHub-Event: " + event_header)
        return

    gateway_hostname = os.getenv("gateway_hostname", "gateway.openfaas")

    payload = json.loads(req)

    if not payload["action"] == "opened":
        sys.exit("Action not supported: " + payload["action"])
        return

    # Call sentimentanalysis
    res = requests.post('http://' + gateway_hostname + ':8080/function/sentimentanalysis', 
                        data= payload["issue"]["title"]+" "+payload["issue"]["body"])

    if res.status_code != 200:
        sys.exit("Error with sentimentanalysis, expected: %d, got: %d\n" % (200, res.status_code))

    # Read the positive_threshold from configuration
    positive_threshold = float(os.getenv("positive_threshold", "0.2"))

    polarity = res.json()['polarity']

    # Call back to GitHub to apply a label
    apply_label(polarity,
        payload["issue"]["number"],
        payload["repository"]["full_name"],
        positive_threshold)

    return "Repo: %s, issue: %s, polarity: %f" % (payload["repository"]["full_name"], payload["issue"]["number"], polarity)

def apply_label(polarity, issue_number, repo, positive_threshold):
    g = Github(os.getenv("auth_token"))
    repo = g.get_repo(repo)
    issue = repo.get_issue(issue_number)

    has_label_positive = False
    has_label_review = False
    for label in issue.labels:
        if label == "positive":
            has_label_positive = True
        if label == "review":
            has_label_review = True

    if polarity > positive_threshold and not has_label_positive:
        issue.set_labels("positive")
    elif not has_label_review:
        issue.set_labels("review")
```

> The source code is also available at [issue-bot/bot-handler/handler.py](./issue-bot/bot-handler/handler.py)

* Build and deploy

Use the CLI to build and deploy the function:

```
$ faas-cli up -f issue-bot.yml
```

Now try it out by creating some new issues in the `bot-tester` repository. Check whether `positive` and `review` labels were properly applied and consult the GitHub Webhooks page if you are not sure that the messages are getting through or if you suspect an error is being thrown.

![](./screenshot/bot_label_applied.png)

> Note: If the labels don't appear immediately, first try refreshing the page

## Validate payload with HMAC

In [Lab 11](lab11.md) we will learn how to protect a serverless function from tampering through the use of HMAC.

Now move on to [Lab 6](lab6.md).
