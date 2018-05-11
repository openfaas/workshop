import requests
import random

def handle(req):
    r = requests.get("http://api.open-notify.org/astros.json")
    result = r.json()
    
    index = random.randint(0, len(result["people"])-1)
    name = result["people"][index]["name"]

    return "%s is in space" % (name)
