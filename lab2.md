# Lab 2 - Test things out

<img src="https://github.com/openfaas/media/raw/master/OpenFaaS_Magnet_3_1_png.png" width="500px"></img>

Before starting this lab, create a new folder for your files:

```sh
$ mkdir -p lab2 \
   && cd lab2
```

## Use the UI Portal

You can now test out the OpenFaaS UI:

If you have set an `$OPENFAAS_URL` then get the URL and then click on it:

```sh
echo $OPENFAAS_URL
http://127.0.0.1:31112
```

If you haven't set an `$OPENFAAS_URL` then the default is normally: [http://127.0.0.1:8080](http://127.0.0.1:8080).

We can deploy some sample functions and then use them to test things out:

```sh
faas-cli store deploy markdown
faas-cli store deploy nodeinfo
faas-cli store deploy env
```

![](./screenshot/markdown_portal.png)

You can try them out in the UI such as the Markdown function which converts Markdown code into HTML.

Type the below into the *Request* field:

```sh
## The **OpenFaaS** _workshop_
```

Now click *Invoke* and see the response appear in the bottom half of the screen.

I.e.

```sh
<h2>The <strong>OpenFaaS</strong> <em>workshop</em></h2>
```

You will see the following fields displayed:

* Status - whether the function is ready to run. You will not be able to invoke the function from the UI until the status shows Ready.
* Replicas - the amount of replicas of your function running in the cluster
* Image - the Docker image name and version as published to the Docker Hub or Docker repository
* Invocation count - this shows how many times the function has been invoked and is updated every 5 seconds

Click *Invoke* a number of times and see the *Invocation count* increase.

## Deploy via the Function Store

You can deploy a function from the OpenFaaS store. The store is a free collection of functions curated by the community.

* Click *Deploy New Function*
* Click *From Store*
* Click *Figlet* or enter *figlet* into the search bar and then click *Deploy*

The Figlet function will now appear in your left-hand list of functions. Give this a few moments to be downloaded from the Docker Hub and then type in some text and click Invoke like we did for the Markdown function.

You'll see an ASCII logo generated like this:

```sh
 _  ___   ___ _  __
/ |/ _ \ / _ (_)/ /
| | | | | | | |/ /
| | |_| | |_| / /_
|_|\___/ \___/_/(_)
```

## Learn about the CLI

You can now test out the CLI, but first a note on alternate gateways URLs:

If your *gateway is not* deployed at http://127.0.0.1:8080 then you will need to specify the alternative location. There are several ways to accomplish this:

1. Set the environment variable `OPENFAAS_URL` and the `faas-cli` will point to that endpoint in your current shell session. For example: `export OPENFAAS_URL=http://openfaas.endpoint.com:8080`. This is already set in [Lab 1](./lab1.md) if you are following the Kubernetes instructions.
2. Specify the correct endpoint inline with the `-g` or `--gateway` flag: `faas deploy --gateway http://openfaas.endpoint.com:8080`
3. In your deployment YAML file, change the value specified by the `gateway:` object under `provider:`.

### List the deployed functions

This will show the functions, how many replicas you have and the invocation count.

```sh
$ faas-cli list
```

You should see the *markdown* function as `markdown` and the *figlet* function listed too along with how many times you've invoked them.

Now try the verbose flag

```sh
$ faas-cli list --verbose
```
or

```sh
$ faas-cli list -v
```

You can now see the Docker image along with the names of the functions.

### Invoke a function

Pick one of the functions you saw appear on `faas-cli list` such as `markdown`:

```sh
$ faas-cli invoke markdown
```

You'll now be asked to type in some text. Hit Control + D when you're done.

Alternatively you can use a command such as `echo` or `curl` as input to the `invoke` command which works through the use of pipes.

```sh
$ echo "# Hi" | faas-cli invoke markdown

$ curl -sLS https://raw.githubusercontent.com/openfaas/faas/master/README.md \
  | faas-cli invoke markdown
```

## Monitoring dashboard

OpenFaaS tracks metrics on your functions automatically using Prometheus. The metrics can be turned into a useful dashboard with free and Open Source tools like [Grafana](https://grafana.com).

Run Grafana in OpenFaaS Kubernetes namespace:

```sh
arkade install --namespace openfaas grafana
```

Get the `admin` password:

```sh
kubectl get secret --namespace openfaas grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

Find Grafana node port address:

```sh
$ GRAFANA_PORT=$(kubectl -n openfaas get svc grafana -o jsonpath="{.spec.ports[0].nodePort}")
$ GRAFANA_URL=http://IP_ADDRESS:$GRAFANA_PORT/dashboard/db/openfaas
```
where `IP_ADDRESS` is your corresponding IP for Kubernetes.

Or you may run this port-forwarding command in order to be able to access Grafana on `http://127.0.0.1:3000`:

```sh
kubectl port-forward svc/grafana 3000:80 -n openfaas
```

If you're using Kubernetes 1.17 or older, use `deploy/grafana` instead of `pod/` in the command above.

After the service has been created open Grafana in your browser, login with username `admin` password that you retrieved in the step above and navigate to the pre-made OpenFaaS dashboard at `$GRAFANA_URL` or if using the port forward `http://127.0.0.1:3000`.

<a href="https://camo.githubusercontent.com/24915ac87ecf8a31285f273846e7a5ffe82eeceb/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f4339636145364358554141585f36342e6a70673a6c61726765"><img src="https://camo.githubusercontent.com/24915ac87ecf8a31285f273846e7a5ffe82eeceb/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f4339636145364358554141585f36342e6a70673a6c61726765" width="600px" /></a>

*Pictured: example of an OpenFaaS dashboard with Grafana*

### Configuring Grafana

1. Setup `Datasource`

After you login you will need to add the Datasource in order to Grafana knows where to collect the data to show.
To do that mouse over in the `Engine` icon and then click in the `Data Soruces`

![Data Sources](./screenshot/grafana_data_sources.png)

1.1. Click in `Add data source`

![Add data source](./screenshot/grafana_add_data_source.png)

1.2. Click in the `Select` button for the Prometheus Data Source

![Prometheus data source](./screenshot/grafana_prometheus_data_source.png)

1.3. Prometheus is installed with OpenFaaS and you can access that in the cluster using the service that is exposed `http://prometheus.openfaas:9090``

Add that information in the `URL` field and then click in the `Save & Test` button to save and validate the connection.

![Prometheus](./screenshot/grafana_prometheus.png)


### Load initial Grafana Dashboard

1.1 Click in the `Grafana` logo to return to the main page and mouse over the `plus` icon and then click in the `Import`

![Import](./screenshot/grafana_import.png)

1.2 Copy the contents of the file located in [grafana-dashboards/openfaas-dash.json](grafana-dashboards/openfaas-dash.json) and paste it
in the box under `Or paste JSON` and then click `Load`

![Import JSON](./screenshot/grafana_import_json.png)

1.3 Give a name for your Dashboard and click `Import`

![Dashboard Name](./screenshot/grafana_dashboard_name.png)

It will load and show the initial OpenFaaS Dashboards.
Now invoke some functions and you will see the graphs getting updated.

![Dashboards](./screenshot/grafana_dashboard.png)


Now move onto [Lab 3](./lab3.md)
