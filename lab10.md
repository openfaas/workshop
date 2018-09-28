# Lab 10 - Advanced feature - Secrets

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

Before starting this lab, create a new folder for your files. As this lab builds on an earlier lab make a copy of lab5:

```
$ cp -r lab5 lab10 \
   && cd lab10
```

## Using Secrets

[Lab 5](./lab5.md) looked at how the `issue-bot` could obtain the GitHub *Personal Access Token* from an environment variable (`auth_token`).  An alternative approach is to use a **secret** to store sensitive information.

From the Docker documentation: 
> .. a secret is a blob of data, such as a password, SSH private key, SSL certificate, or another piece of data that should not be transmitted over a network or stored unencrypted in a Dockerfile or in your application’s source code.

This is a more secure alternative to environmental variables. Environmental variables are easier to use but are best suited to non-confidential configuration items.  Seems a good fit for storing the `auth_token` value.  

### Create a secret

> Use of underscores (_) in secret names should be avoided to make it easier to move between Docker Swarm and Kubernetes. 

From a terminal run the following command:

```
$ echo -n <auth_token> | docker secret create auth-token -
```

Test that the secret was created:

```
$ docker secret inspect auth-token
```
> Note: If you are deploying your function on a remote gateway make sure you create your secret on the virtual machine you use for the gateway.

When the secret is mounted by a function it will be presented as a file under `/var/openfaas/secrets/auth-token`. This can be read by `handler.py` to obtain the GitHub *Personal Access Token*.

### Update issue-bot.yml

Replace the reference to `env.yml` with an instruction to make the `auth-token` secret available to the function:

```yml
provider:
  name: faas
  gateway: http://127.0.0.1:8080

functions:
  issue-bot:
    lang: python3
    handler: ./issue-bot
    image: <your-username>/issue-bot
    environment:
      write_debug: true
      gateway_hostname: "gateway"
      positive_threshold: 0.25
    secrets:
      - auth-token

```

### Update the `issue-bot` function

The function handler requires changing in order to cause it to read the `auth-token` secret, rather than the environment variable.  This is a single line change where:

```python
g = Github(os.getenv("auth_token"))
``` 
is replaced with 
```python
with open("/var/openfaas/secrets/auth-token","r") as authToken:  
    g = Github(authToken.read())
```

> The full source code is  available at [issue-bot-secrets/bot-handler/handler.py](./issue-bot-secrets/bot-handler/handler.py)

* Build and deploy

Use the CLI to build and deploy the function:

```
$ faas-cli up -f issue-bot.yml
```

You can return to the [main page](./README.md).