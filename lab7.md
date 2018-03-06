# Lab 7 - Put it all together

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

We're going to create a GitHub bot with OpenFaaS functions named `issue-bot`.

The job of issue-bot is to triage new issues by analysing the sentiment of the "description" field, it will then apply a label of *positive* or *review*. This will help the maintainers with their busy schedule so they can prioritize which issues to look at first.

![](./diagram/issue-bot.png)

## Get a GitHub account

* Sign up for a [GitHub account](https://github.com) if you do not already have one.

* Create a new repository and call it *bot-tester*

Note: we will only use this repository as a testing ground for creating Issues. You don't need to commit any code there.

## Set up a tunnel with ngrok

You will need to receive incoming webhooks from GitHub. In production you will have a clear route for incoming traffic but within the constraints of a workshop we have to be creative.

Open a new Terminal and type in:

```
$ docker run -p 4040:4040 -it --rm --net=func_functions \
  alexellis2/ngrok-admin http gateway:8080
```

Use the built-in UI of `ngrok` at http://localhost:4040 to find your HTTP URL. You will be given a URL that you can access over the Internet, it will connect directly to your OpenFaaS API Gateway.

Test the URL such as http://fuh83fhfj.ngrok.io

```
$ faas-cli list --gateway http://fuh83fhfj.ngrok.io/
```

## Create an webhook receiver `issue-bot`

```
$ faas new --lang python issue-bot --prefix="<your-docker-username-here>"
$ faas build -f ./issue-bot.yml
$ faas push -f ./issue-bot.yml
```

Now edit the function's YAML file `issue-bot.yml` and add an environmental variable of `write_debug: true`:

```
provider:
  name: faas
  gateway: http://localhost:8080

functions:
  issue-bot:
    lang: python
    handler: ./issue-bot
    image: <user-name>/issue-bot
    environment:
      write_debug: true
```

* Deploy the function

```
$ faas deploy -f ./issue-bot.yml
```

## Receive webhooks from GitHub

Log back into GitHub and navigate to your repository *bot-tester*

Click *Settings* -> *Webhooks* -> *Add Webhook*

![](./screenshot/add_github_webhook.png)

Now enter the URL you were given from Ngrok adding `/function/issue-bot` to the end, for example:

```
http://fuh83fhfj.ngrok.io/function/issue-bot
```

![](https://raw.githubusercontent.com/iyovcheva/github-issue-bot/master/media/WebhookURLSettings.png)

For *Content-type* select: *application/json*

Leave *Secret* blank for now.

And select "Let me select individual events"

For events select **Issues** and **Issue comment**

![](https://raw.githubusercontent.com/iyovcheva/github-issue-bot/master/media/WebhookEventsSettings.png)

## Check it worked

Now go to GitHub and create a new issue. Type "test" for the title and description.

Check how many times the function has been called:

```
$ faas list
Function    Invocations
issue-bot   2
```

Each time you create an issue the count will increase due to GitHub's API invoking the function.
> _Github will invoke the function via a ping request once while setting up the webhook. That's why there are at least 2 invocations at this point_

You can see the payload sent via GitHub by typing in `docker service logs -f issue-bot`.

The GitHub Webhooks page will also show every message sent under "Recent Deliveries", you can replay a message here and see the response returned by your function.

![](./screenshot/github_replay.png)

## Analyse new Issues on GitHub


### Deploy SentimentAnalysis function

In order to use this issue-bot function, you will need to deploy the SentimentAnalysis function first.
This is a python function that provides a rating on sentiment positive/negative (polarity -1.0-1.0) and subjectivity provided to each of the sentences sent in via the TextBlob project.

You can deploy "SentimentAnalysis" from the **Function Store**

and test

```
# echo -n "I am really excited to participate in the OpenFaaS workshop." | faas-cli invoke sentimentanalysis
Polarity: 0.375 Subjectivity: 0.75

# echo -n "The hotel was clean, but the area was terrible" | faas-cli invoke sentimentanalysis
Polarity: -0.316666666667 Subjectivity: 0.85
```

### Update the `issue-bot` function

Open `issue-bot/handler.py` and replace the template with this code:

```
import requests, json, os, sys

def handle(req):

    event_header = os.getenv("Http_X_Github_Event")

    if not event_header == "issues":
        sys.exit(1)
        return

    gateway_hostname = os.getenv("gateway_hostname", "gateway")

    payload = json.loads(req)

    if not payload["action"] == "opened":
        return

    #sentimentanalysis
    res = requests.post('http://' + gateway_hostname + ':8080/function/sentimentanalysis', data=payload["issue"]["title"]+" "+payload["issue"]["body"])

    print(res.json())
```

Update your `requirements.txt` file with the requests module for HTTP/HTTPs:

```
requests
```

The following line from the code above posts the GitHub Issue's title and body to the `sentimentanalysis` function as text. The response will be in JSON format.

```
res = requests.post('http://' + gateway_hostname + ':8080/function/sentimentanalysis', data=payload["issue"]["title"]+" "+payload["issue"]["body"])
```

### Build and Deploy:

Use the CLI to build and deploy the function:

```
$ faas build -f issue-bot.yml \
  && faas push -f issue-bot.yml \
  && faas deploy -f issue-bot.yml
```

Now create a new issue in the `bot-tester` repository. GitHub will respond by sending a JSON payload to your function via the Ngrok tunnel we set up at the start.

You can view the request/response directly on GitHub - navigate to *Settings* -> *Webhook* as below:

![](https://raw.githubusercontent.com/iyovcheva/github-issue-bot/master/media/WebhookResponse.png)

### Create a Personal Access Token for GitHub

The next step will be for us to apply a label of `positive` or `review`, but because this action involves writing to the repository we need to get a *Personal Access Token* from GitHub.

Go to your *GitHub profile* -> *Settings/Developer settings* -> *Personal access tokens* and then click *Generate new token*.

![](https://raw.githubusercontent.com/iyovcheva/github-issue-bot/master/media/PersonalAccessTokens.png)

Tick the box for "repo" to allow access to your repositories

![](https://raw.githubusercontent.com/iyovcheva/github-issue-bot/master/media/NewPAT.png)

Click the "Generate Token" button at the bottom of the page


Create a file called `env.yml` in the directory where your `issue-bot.yml` file is located with the following content:

```
environment:
  auth_token: <auth_token_value>
  repo: <github_username>/bot-tester
  positive_threshold: 0.6
```
Update the values to match your specifics
* update the `auth_token` variable
* update `repo`

> The `positive_threshold` environmental variable is used to fine-tune whether an Issue gets the `positive` or `review` label.

Now update your issue-bot.yml file and tell it to use the `env.yml` file:

```
provider:
  name: faas
  gateway: http://localhost:8080

functions:
  issue-bot:
    lang: python
    handler: ./issue-bot
    image: <your-username>/issue-bot
    environment:
      gateway_hostname: "gateway"
      write_debug: true
    environment_file:
    - env.yml
```

## Apply labels via the GitHub API

You can use the API to perform many different tasks, the [documentation is available here](https://github.com/PyGithub/PyGithub).

Here's a sample of Python code that we could use to apply a label, but you do not add it to your function yet.

```
issue_number = 1
repo_name = "issue_bot"
auth_token = "xyz"

g = Github("auth_token")
repo = g.get_repo(repo_name)
issue = repo.get_issue(issue_number)
```

This library for GitHub is provided by the community and is not official, but appears to be popular. It can be pulled in from `pip` through our `requirements.txt` file.

### Putting the whole function together

* Update your `issue-bot/requirements.txt` file and add a line for `PyGithub`

* Open `issue-bot/handler.py` and replace the code with this:

```python
import requests, json, os, sys
from github import Github

def handle(req):

    event_header = os.getenv("Http_X_Github_Event")

    if not event_header == "issues":
        sys.exit(1)
        return

    gateway_hostname = os.getenv("gateway_hostname", "gateway")

    payload = json.loads(req)

    if not payload["action"] == "opened":
        return

    #sentimentanalysis
    res = requests.post('http://' + gateway_hostname + ':8080/function/sentimentanalysis', data=payload["issue"]["title"]+" "+payload["issue"]["body"])

    # positive_threshold
    positive_threshold = float(os.getenv("positive_threshold", "0.2"))

    g = Github(os.getenv("auth_token"))
    repo = g.get_repo(os.getenv("repo"))
    issue = repo.get_issue(payload["issue"]["number"])

    has_label_positive = False
    has_label_review = False
    for label in issue.labels:
        if label == "positive":
            has_label_positive = True
        if label == "review":
            has_label_review = True

    if res.json()['polarity']  >  positive_threshold and not has_label_positive:
        issue.set_labels("positive")
    elif not has_label_review:
        issue.set_labels("review")

    print(res.json())
```

### Build and Deploy:

Use the CLI to build and deploy the function:

```
$ faas build -f issue-bot.yml \
  && faas push -f issue-bot.yml \
  && faas deploy -f issue-bot.yml
```

Now try it out by creating some new issues in the `bot-tester` repository. Check whether `positive` and `review` labels were properly applied and consult the GitHub Webhooks page if you are not sure that the messages are getting through or if you suspect an error is being thrown.

> If the labels don't appear immediately, first try refreshing the page

Now return to the [main page](./README.md) for Q&A or to read the appendix.
