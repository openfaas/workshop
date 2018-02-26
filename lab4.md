# Lab 4 - Go deeper with functions

## Extend timeouts with `read_timeout`

## Inject configuration through environmental variables

## Use HTTP context - querystring / headers etc


## Accessing the HTTP request / query-string

The `faas-cli invoke` can accept other parameters such as `--query` to provide a querystring. Any parameters will be available as environmental variables within your code.

Here's an example where we scaffold a new Node.js function using the `faas new` command:

```
faas new --lang node print-env
mv print-env.yml stack.yml
```

The `new` command will create two files for a Node.js template:

```
./print-env/handler.js
./stack.yml
```

If you need to add `npm` modules later on you can create a `package.json` file in the `print-env` folder.

Edit `print-env/handler.js`:

```
"use strict"

module.exports = (context, callback) => {
    callback(undefined, { "environment": process.env });
}
```

This will print out the environmental variables available to the function. So let's build / deploy and invoke it:

```
faas build
faas deploy
echo -n "openfaas" | faas invoke print-env --query workshop=true

{"environment":{"PATH":"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","HOSTNAME":"59cc01de25a6",
"fprocess":"node index.js","NODE_VERSION":"8.9.1","YARN_VERSION":"1.3.2","NPM_CONFIG_LOGLEVEL":"warn",
"cgi_headers":"true","HOME":"/home/app",
"Http_User_Agent":"Go-http-client/1.1",
"Http_Accept_Encoding":"gzip",
"Http_Content_Type":"text/plain",
"Http_Connection":"close",
"Http_Method":"POST",
"Http_ContentLength":"-1",
"Http_Query":"workshop=true",
"Http_Path":"/function/print-env"}}
```

As part of the output you can see the Http headers and request data revealed in environmental variables.

Our querystring of `workshop=true` is available in the environmental variable `Http_Query`.

In Python you can find environmental variables through the `os.getenv(key, default_value)` function or `os.environ` array after importing the `os` package.

i.e.

```
import os

def handle(st):
    print os.getenv("Http_Method")          # will be "NoneType" if empty
    print os.getenv("Http_Method", "GET")   # provide a default of "GET" if empty
    print os.environ["Http_Method"]         # throws an exception is not present
    print os.environ                        # array of environment
```

Now move onto [Lab 5](lab5.md)
