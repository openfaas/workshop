# Lab 6 - Chain or combine Functions into workflows

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

## Call one function from another

The easiest way to call one function from another is make a call over HTTP back to the API Gateway in OpenFaaS. This call does not need to know the external domain name or IP address, it can simply refer to the API Gateway as `gateway`.

Example:

In Lab 3 we introduced the requests module and used it to call a remote API to get the name of an astronaut aboard the ISS. We can use the same technique to call another function deployed on OpenFaaS.

* Go to the *Function Store* and deploy the *Sentiment Analysis* function. 

The Sentiment Analysis function will take any string and give whether it's subjective and positive or negative in a JSON response. The key field we want is `polarity`.

```
echo -n "California is great, it's always sunny there." | faas invoke sentimentanalysis
{"polarity": 0.8, "sentence_count": 1, "subjectivity": 0.75}
```

So the result shows us that our test sentence was both very subjective (75%) and very positive (80%).

The following code can be used to call the *Sentiment Analysis* function or any other function:

```
    test_sentence = "California is great, it's always sunny there."
    r = requests.get("http://gateway:8080/function/sentimentanalysis", text= test_sentence)
```

Since the result is always in JSON format we can make use of the helper function `.json()` to convert the response:

```
    result = r.json()
    if result["polarity" > 0.45]:
        print("That was probably positive")
    else:
        print("That was neutral or negative")
```

Try generating a new function in Python putting it all together, remember to add `requests` to your `requirements.txt` file.

## The Director pattern


Now move onto [Lab 7](lab7.md)
