# Lab 6 - Chain or combine Functions into workflows

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

## Chaining functions on the client-side

You can pipe the result of one function into another using `curl`, the `faas-cli` or some of your own code. Here's an example:

Pros:

* requires no code - can be done with CLI programs
* fast for development and testing
* easy to model in code

Cons:

* additional latency - each function goes back to the server
* chatty (more messages)

Example:

* Deploy the NodeInfo function from the *Function Store*

* Then push the output from NodeInfo through the Markdown converter

```
$ echo -n "" | faas invoke nodeinfo | faas invoke func_markdown
<p>Hostname: 64767782518c</p>

<p>Platform: linux
Arch: x64
CPU count: 4
Uptime: 1121466</p>
```

You will now see the output of the NodeInfo function decorated with HTML tags such as: `<p>`.

Another example of client-side chaining of functions may be to invoke a function that generates an image, then send that image into another function which adds a watermark.

## Call one function from another

The easiest way to call one function from another is make a call over HTTP via the OpenFaaS *API Gateway*. This call does not need to know the external domain name or IP address, it can simply refer to the API Gateway as `gateway` through a DNS entry.

When accessing a service such as the API gateway from a function it's best practice to use an environmental variable to configure the hostname, this is important for two reasons - the name may change and in Kubernetes a suffix is sometimes needed.

Pros:

* functions can make use of each other directly
* low latency since the functions can access each other on the same network

Cons:

* requires a code library for making the HTTP request

Example:

In Lab 3 we introduced the requests module and used it to call a remote API to get the name of an astronaut aboard the ISS. We can use the same technique to call another function deployed on OpenFaaS.

* Go to the *Function Store* and deploy the *Sentiment Analysis* function. 

The Sentiment Analysis function will tell you the subjectivity and polarity (positivity rating) of any sentence. The result of the function is formatted in JSON as per the example below:

```
echo -n "California is great, it's always sunny there." | faas invoke sentimentanalysis
{"polarity": 0.8, "sentence_count": 1, "subjectivity": 0.75}
```

So the result shows us that our test sentence was both very subjective (75%) and very positive (80%). The values for these two fields are always between `-1.00` and `1.00`.

The following code can be used to call the *Sentiment Analysis* function or any other function:

```python
    test_sentence = "California is great, it's always sunny there."
    r = requests.get("http://gateway:8080/function/sentimentanalysis", text= test_sentence)
```

Or via an environmental variable:

```python
    gateway_hostname = os.getenv("gateway_hostname", "gateway") # uses a default of "gateway" for when "gateway_hostname" is not set
    test_sentence = "California is great, it's always sunny there."
    r = requests.get("http://" + gateway_hostname + ":8080/function/sentimentanalysis", text= test_sentence)
```

Since the result is always in JSON format we can make use of the helper function `.json()` to convert the response:

```python
    result = r.json()
    if result["polarity" > 0.45]:
        print("That was probably positive")
    else:
        print("That was neutral or negative")
```

Now create a new function in Python and it all together

* Remember to add `requests` to your `requirements.txt` file

Note: you do not need to modify or alter the source for the SentimentAnalysis function, we have already deployed it and will access it via the API gateway.

## The Director pattern

The *Director pattern* as [documented here](https://github.com/openfaas/faas/blob/master/guide/chaining_functions.md#function-director-pattern) is where one function *the director* exists only to call another function and return the result. It is a mixture of the two techniques we explored above.

![](./diagram/director_function.png)


In the diagram above the *director function* named "RSS Feed to MP3" creates a workflow by calling two functions on the server-side and then returning the result. The advantage of using a director function is that this function can be versioned, built and deployed in exactly the same way as the functions it makes use of.

The URL passes through the director to the "Get RSS feed" function, the result (a parsed RSS feed) would be fed into the "Text-To-Speech" function resulting in an MP3 file as an output.


Now move onto [Lab 7](lab7.md)
