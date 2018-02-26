# Lab 2 - Testing things out

## Test-out the UI

You can now test out the OpenFaaS UI by going to http://localhost:8080 or http://127.0.0.1:8080 - if you're deploying to a Linux VM then replace localhost with the IP address from the output you see on the `ifconfig` command.

Note: on some Linux distributions accessing `localhost` may hang, if that happens then oplease use `127.0.0.1` instead and replace it wherever you see `localhost`.

In the default stack we deploy several sample functions.

You can try them out in the UI such as the Markdown function which converts Markdown code into HTML.

Type the below into the *Request* field:

```
## The **OpenFaaS** _workshop_
```

Now click *Invoke* and see the response appear in the bottom half of the screen.

I.e.

```
<h2>The <strong>OpenFaaS</strong> <em>workshop</em></h2>
```

You will see the following fields displayed:

* Replicas - the amount of replicas of your function running in the swarm cluster
* Image - the Docker image name and version as published to the Docker Hub or Docekr repository
* Invocation count - this shows how many times the function has been invoked and is updated every 5 seconds

Click *Invoke* a number of times and see the *Invocation count* increase.

### Deploy a function from the store

You can deploy a function from the OpenFaaS store. The store is a free collection of functions curated by the community.

* Click *Deploy New Function*
* Click *From Store*
* Click *Figlet* or enter *figlet* into the search bar and then click *Deploy*

The Figlet function will now appear in your left-hand list of functions. Give this a few moments to be downloaded from the Docker Hub and then type in some text and click Invoke like we did for the Markdown function.

You'll see an ASCII logo generated like this:

```
 _  ___   ___ _  __
/ |/ _ \ / _ (_)/ /
| | | | | | | |/ / 
| | |_| | |_| / /_ 
|_|\___/ \___/_/(_)
``` 

## Test out the CLI

You can now test out the CLI, but first a note on alternate gateways URLs:

If your gateway is not deployed at http://localhost:8080 then you will need to specify the `--gateway` flag followed by the alternate URL such as http://127.0.0.1:8080/. 

> A shorter versions of flags are available most of the time so `--gateway` can be shortened to `-g` too. Check `faas-cli --help` for more information.

### List the deployed functions

This will show the functions, how many replicas you have and the invocation count.

```
$ faas-cli list
```

You should see the *markdown* function as `func_markdown` and the *figlet* function listed too along with how many times you've invoked them.

Now try the verbose flag

```
$ faas-cli list --verbose
```
or

```
$ faas-cli list -v
```

You can now see the Docker image along with the names of the functions.

### Invoke a function

Pick one of the functions you saw appear on `faas-cli list` such as `func_markdown`:

```
$ faas-cli invoke func_markdown
```

You'll now be asked to type in some text. Hit Control + D when you're done.

Alternatively you can use a command such as `echo` or `uname -a` as input to the `invoke` command which works through the use of pipes.

```
$ echo Hi | faas-cli invoke func_markdown

$ uname -a | faas-cli invoke func_markdown
```

You can even generate a HTML file from this lab's markdown file with the following:

```
$ cat lab2.md | faas-cli invoke func_markdown
```

Now move onto [Lab 3](./lab3.md)
