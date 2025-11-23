# Exercise 3.2

## Google Kubernetes Engine Configuration

If GKE cluster is not alread running, create it:

```
gcloud auth login
gcloud config set project dwk-gke-iku
gcloud services enable container.googleapis.com
gcloud container clusters create dwk-cluster --zone=europe-north1-b --cluster-version=1.32 --gateway-api=standard --disk-size=32 --num-nodes=3 --machine-type=e2-medium
gcloud components install gke-gcloud-auth-plugin
gcloud container clusters get-credentials dwk-cluster --location=europe-north1-b

```

## Deploy to GKE

GKE specific manifests are stored in `gke/manifests/`. Unmodified ones are just symlinks
to originals used for local deployment.

```
k apply -f gke/manifests/
k get ing # Note 'ADDRESS' for log-output-ingress
```

Verify that getting logs works:

```
curl http://<address>/log
```

Note that ping/pong count will not work if pingpong app is not already running.

## Local Cluster Configuration

Make sure the cluster has required port mapping for docker:

```sh
k3d cluster create -a 2 --k3s-arg "--tls-san=192.168.65.3@server:0" --port 8082:30080@agent:0 -p 8081:80@loadbalancer
```

Note: `--tls-san=192.168.65.3@server:0` is neeed to allow Lens running on local machine to cluster running on VM. ```

## Deploy

```sh
kubectl apply -f manifests/
```

## Verify output

```sh
curl -s http://192.168.65.3:8081/log | head
```

## (Re)Building the docker images

```sh
docker build ./log-reader-api -t <namespace>/log_output_reader_api:2.5
```
