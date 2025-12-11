# Exercise 5.6

## Installing Knative to k3d

Install the service:

```
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.0/serving-core.yaml
kubectl apply -f https://github.com/knative-extensions/net-kourier/releases/download/knative-v1.20.0/kourier.yaml
kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'
```

Verify that installation was successful:

```
kubectl get pods -n knative-serving
```

Get the External IP for DNS configuration to be done later:

```
kubectl --namespace kourier-system get service kourier
```

Configure DNS:

```
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.0/serving-default-domain.yaml
```

Finally, install autoscaling:

```
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.0/serving-hpa.yaml
```

Install also 'kn' CLI utility as running the examples is easier with it (rather than using yaml manifests):

```
brew install kn
```

## Deploying a Knative Service:

```
kn service create hello \
--image ghcr.io/knative/helloworld-go:latest \
--port 8080 \
--env TARGET=World
```

Test that it works:

```
curl http://hello.exercises.192.168.97.2.sslip.io
```

## Autoscaling

Watch pods in one terminal using `kubectl get pod -l serving.knative.dev/service=hello -w` and
query the service multiple times with curl `"$(kn service describe hello -o url)"`` from another, and see the containers created and terminated:

```
$ kubectl get pod -l serving.knative.dev/service=hello -w
NAME                                      READY   STATUS    RESTARTS   AGE
hello-00001-deployment-6755d786d8-gbrdd   2/2     Running   0          48s
hello-00001-deployment-6755d786d8-gbrdd   2/2     Terminating   0          2m4s
hello-00001-deployment-6755d786d8-kbhbm   0/2     Pending       0          0s
hello-00001-deployment-6755d786d8-kbhbm   0/2     Pending       0          0s
hello-00001-deployment-6755d786d8-kbhbm   0/2     ContainerCreating   0          0s
hello-00001-deployment-6755d786d8-kbhbm   0/2     ContainerCreating   0          0s
hello-00001-deployment-6755d786d8-kbhbm   1/2     Running             0          1s
hello-00001-deployment-6755d786d8-kbhbm   2/2     Running             0          1s
hello-00001-deployment-6755d786d8-gbrdd   1/2     Terminating         0          2m31s
hello-00001-deployment-6755d786d8-gbrdd   0/2     Completed           0          2m34s
hello-00001-deployment-6755d786d8-gbrdd   0/2     Completed           0          2m34s
hello-00001-deployment-6755d786d8-gbrdd   0/2     Completed           0          2m35s
hello-00001-deployment-6755d786d8-gbrdd   0/2     Completed           0          2m35s
hello-00001-deployment-6755d786d8-kbhbm   2/2     Terminating         0          62s
hello-00001-deployment-6755d786d8-kbhbm   1/2     Terminating         0          91s
hello-00001-deployment-6755d786d8-kbhbm   0/2     Completed           0          93s
hello-00001-deployment-6755d786d8-kbhbm   0/2     Completed           0          93s

```

## Traffic splitting

Modify the configuration of the example service:

```
kn service update hello --env TARGET=Knative
```

Verify the change and the creation of a new revision:

```
$ curl "$(kn service describe hello -o url)"
Accessing URL http://hello.exercises.192.168.97.2.sslip.io
Hello Knative!

$ kn revisions list
NAME          SERVICE   TRAFFIC   TAGS   GENERATION   AGE   CONDITIONS   READY   REASON
hello-00002   hello     100%             2            37s   4 OK / 4     True
hello-00001   hello                      1            12m   3 OK / 4     True
```

Now route traffic 50/50 between the revisions for a canary update (similarly as in the istio routing exercise):

```
$ kn service update hello --traffic hello-00001=50 --traffic @latest=50
...
$ kn revisions list
NAME          SERVICE   TRAFFIC   TAGS   GENERATION   AGE     CONDITIONS   READY   REASON
hello-00002   hello     50%              2            4m43s   3 OK / 4     True
hello-00001   hello     50%              1            16m     3 OK / 4     True
```

And test that routing works:

```
$ for i in $(seq 1 100); do curl -s curl http://hello.exercises.192.168.97.2.sslip.io >> curl.log ; done
$ sort curl.log | uniq -c
     47 Hello Knative!
     53 Hello World!
```

Seems ok!
