# Exercise 3.1

## Google Kubernetes Engine (GKE) Cluster Configuration

Spin a up cluster in GKE:

```
gcloud auth login
gcloud config set project dwk-gke-iku
gcloud services enable container.googleapis.com
gcloud container clusters create dwk-cluster --zone=europe-north1-b --cluster-version=1.32 --gateway-api=standard --disk-size=32 --num-nodes=3 --machine-type=e2-medium
gcloud components install gke-gcloud-auth-plugin
gcloud container clusters get-credentials dwk-cluster --location=europe-north1-b
kubectl cluster-info
```

## Deploy to GKE

GKE specific manifests are stored in `gke/manifests/`. Unmodified ones are just symlinks
to originals used for local deployment.

```
k apply -f gke/manifests/
k get ing # Note 'ADDRESS' for ping-pong-ingress
```

Verify that app is working:

```
curl http://<addressp>/pingpong
```

## Local Cluster Configuration

Make sure the cluster has required port mapping for docker:

```sh
k3d cluster create -a 2 --k3s-arg "--tls-san=192.168.65.3@server:0" --port 8082:30080@agent:0 -p 8081:80@loadbalancer
```

Note: `--tls-san=192.168.65.3@server:0` is neeed to allow Lens running on local machine to cluster running on VM. ```

## Local Deploy

```sh
kubectl apply -f manifests/
```

## Verify output

```sh
curl http://192.168.65.3:8081/pingpong
curl http://192.168.65.3:8081/pingpong
curl http://192.168.65.3:8081/pingpong
kubectl exec -it postgres-stset-0 -- su postgres -c pg_dump | egrep '^COPY public.pong_counter' -A 1
```

## (Re)Building the docker image

```sh
docker build . -t <namespace>/ping_pong:2.7
```
