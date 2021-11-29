# Lab 11 - Advanced feature - Trust with HMAC

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

## Pre-amble

Traditional authentication strategies used with microservices work exactly the same with functions. In this lab we will discuss one of several methods available using a shared secret and Hash-based Message Authentication Code (HMAC). For additional authentication strategies and ideas see: [openfaas-function-auth](https://github.com/openfaas-incubator/openfaas-function-auth/blob/master/README.md)

This is by no means an extensive list, security and authentication is a complex field and best left to the experts using tried-and-tested methods.

## Prepare your environment

Before starting this lab create a new folder

```bash
mkdir -p lab11 \
   && cd lab11
```

also make sure your `faas-cli` version is `0.7.4` or above with the following command:

```
$ faas-cli version
```

## What is HMAC

Without any form of authentication or trust our functions may be exposed to anyone who can guess their URL. If our functions are accessible on the Internet or the local network then they could be invoked by a bad actor. By default functions respond to any request. However, if we want to control access to functions we can use Hash-based Message Authentication Code (HMAC) to validate the source of information.

From [alexellis/hmac](https://github.com/alexellis/hmac):
> HMAC uses a symmetric key that both sender/receiver share ahead of time. The sender will generate a hash when wanting to transmit a message - this data is sent along with the payload. The recipient will then sign payload with the shared key and if the hash matches then the payload is assumed to be from the sender.

This way we close our functions from being invoked with invalid or even dangerous information.

## Using HMAC

We will use the `--sign` flag provided by faas-cli to include a header, which contains the hashed message created using the shared key which we provide with the `--key` flag.

> Note: Both `--sign` and `--key` must be present.

Let's first inspect what the flag does by deploying the `env` function which will print all of the environmental variables accessible inside the function:

```bash
$ faas-cli deploy --name env --fprocess="env" --image="functions/alpine:latest"
```

* Invoke the function without `--sign` flag:

```
$ echo "The message" | faas-cli invoke env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=d2c1a2cb20c2
fprocess=env
HOME=/root
Http_X_Call_Id=b84947c6-2970-4fcf-ba3b-66dde6943999
Http_X_Forwarded_For=10.255.0.2:34974
Http_X_Forwarded_Host=127.0.0.1:8080
Http_Content_Length=0
Http_Accept_Encoding=gzip
Http_Content_Type=text/plain
Http_User_Agent=Go-http-client/1.1
Http_X_Start_Time=1538725657952768349
...
```

* Invoke the function again but this time with `--sign` flag:

```
$ echo -n "The message" | faas-cli invoke env --sign=HMAC --key=cookie
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=d2c1a2cb20c2
fprocess=env
HOME=/root
Http_User_Agent=Go-http-client/1.1
Http_Content_Length=0
Http_Accept_Encoding=gzip
...
Http_Hmac=sha1=9239edfe20185eafd7a5513c303b03d207d22f64
...
```

We see the `HMAC` being provided as the environmental variable `Http_Hmac`. The generated value is the hash of `The message` after being signed with the key `cookie`, which is then prepended with the hashing method `sha1`.

## HMAC in action

For our purpose we are going to create a new Python 3 function. Let’s call it `hmac-protected`:

```bash
$ faas-cli new --lang python3 hmac-protected --prefix="<your-docker-username>"
```

Add `payload-secret` which will serve as the key that will hash the payload. 

Create `payload-secret` like we did in [lab10](https://github.com/openfaas/workshop/blob/master/lab10.md):

```bash
$ echo -n "<your-secret>" | faas-cli secret create payload-secret
```

> Note: Remember the string you put in place of  `<your-secret>`

Our `hmac-protected.yml` should look like:

```yml
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  hmac-protected:
    lang: python3
    handler: ./hmac-protected
    image: <your-docker-username>/hmac-protected:latest
    secrets:
      - payload-secret
```

Replace the content of the `handler.py` with the following code:

```python
import os, hmac, hashlib

def validateHMAC(message, secret, hash):

    # GitHub and the sign flag prefix the hash with "sha1="
    receivedHash = getHash(hash)

    # Hash message with secret
    expectedMAC = hmac.new(secret.encode(), message.encode(), hashlib.sha1)
    createdHash = expectedMAC.hexdigest()

    return receivedHash == createdHash

def getHash(hash):
    if "sha1=" in hash:
        hash=hash[5:]
    return hash

def handle(req):
    # We receive the hashed message in form of a header
    messageMAC = os.getenv("Http_Hmac")

    # Read secret from inside the container
    with open("/var/openfaas/secrets/payload-secret","r") as secretContent:
        payloadSecret = secretContent.read()

    # Function to validate the HMAC
    if validateHMAC(req, payloadSecret, messageMAC):
        return "Successfully validated: " + req
    return "HMAC validation failed."
```

> The source code is also available at [hmac-protected/hmac-protected/handler.py](./hmac-protected/hmac-protected/handler.py)

* Build, push and deploy the function in one command by using `faas-cli up` :

```
$ faas-cli up -f ./hmac-protected.yml
```

### Invoke function

We will invoke the function by sending two values:

* The normal request message

* A header containing the hash of the same message, when signed with the value of the `--key` flag

On receipt of the request, the function will use `payload-secret` to sign the request message in the same way as the sender did. This will create a second HMAC which is compared to the transmitted header value, 'Http-Hmac`.

Here we compare the generated and received hashes:

```python
...
    # Function to validate the HMAC
    if validateHMAC(req, payloadKey, receivedHMAC):
        return "Successfully validated: " + req
    return "HMAC validation failed."
...
```

* Invoke the function with the flag:

```bash
$ echo -n "This is a message" | faas-cli invoke hmac-protected --sign hmac --key=<your-secret>
```

Check the response and confirm it matches the conveyed message. In our case we should get:

```
Successfully validated: This is a message
```

* Invoke the function with the wrong `--key` and check the failure message:

```
$ echo -n "This is a message" | faas-cli invoke hmac-protected --sign hmac --key=wrongkey
HMAC validation failed.
```

As a follow-up task you could apply HMAC to secure your endpoint on `issue-bot` from [lab 5](https://github.com/openfaas/workshop/blob/master/lab5.md)

You have completed the labs and can return to the [main page](./README.md).