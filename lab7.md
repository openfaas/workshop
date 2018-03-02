# Lab 7 - Put it all together

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

## Get a GitHub account

* Sign up for a [GitHub account](https://github.com) if you do not already have one.

* Create a new repository and call it *bot-tester*

## Set up a tunnel with ngrok

You will need to receive incoming webhooks from GitHub. In production you will have a clear route for incoming traffic but within the constraints of a workshop we have to be creative.

Head over to ngrok.com and download the tool and unzip it.

Run this on your local computer:

```
$ ngrok http 8080
```

You will be given a URL that you can access over the Internet, it will connect directly to your OpenFaaS API Gateway.

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

Now edit the function's YAML file and add an environmental variable of `write_debug: true`.

* Deploy the function

```
$ faas deploy -f ./issue-bot.yml
```

## Receive webhooks from GitHub

Log back into GitHub and navigate to your repo *bot-tester*

Click Settings -> Webhooks

Now enter the URL you were given from Ngrok adding `/function/issue-bot` to the end, for example:

```
http://fuh83fhfj.ngrok.io/function/issue-bot
```

For content-type pick: application/json

And select "Send me everything"

## Check it worked

Now go to GitHub and create a new issue. Type "test" for the title and description.

Check how many times the function has been called:

```
$ faas list
Function    Invocations
issue-bot   1
```

Each time you create an issue the count will increase. You can see the payload sent via GitHub by typing in `docker service logs -f issue-bot`.

## Analyse new Issues on GitHub

## Apply labels via the GitHub API


Now return to the [main page for Q&A](./README.md).
