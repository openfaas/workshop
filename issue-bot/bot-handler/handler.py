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
