# Exercise 4.7

## GitOps deployment strategy

In earlier exercises, we already used GitHub actions to automatically deploy the apps to GKE. Thus, for this exercise it made most sense
to configure GitOps deployment to local cluster, especially as this requires pull-style approach using ArgoCD or similar service.

### Architecture

The GitOps process is configure as follows:

1. Push event automatically builds the docker images and pushes them to GCP Artifact registry 
2. Kustomize is used configure both GKE and local deployment to use these image. This change is committed to branches main-gke-deploy / main-local-deploy.
3. ArgoCD running on local cluster is configured to watch branch 'main-local-deploy' and it automatically deploys a new version when a new commit is detected
4. GitHub Actions and kubectl are still used to deploy to GKE but only if the cluster is running

### Pulling from GCP Artifact registry on local cluster

To pull images from private GCP Artifact registry on the local cluster, authentication must be configured. This could be done using existing Service Accounts, but I decided to configure a new one with only the required permissions:

```
gcloud iam service-accounts create sa-docker-pull-from-local --display-name "Service Account For Pulling from Local Cluster"

gcloud projects add-iam-policy-binding dwk-gke-iku \
   --member="serviceAccount:my-service-account@dwk-gke-iku.iam.gserviceaccount.com" \
   --role="roles/artifactregistry.reader"

gcloud iam service-accounts keys create ~/.secrets/sa-docker-pull-from-local.key \
   --iam-account sa-docker-pull-from-local@dwk-gke-iku.iam.gserviceaccount.com

kubectl create secret docker-registry gcp-artifact-registry \
   --docker-server=europe-north1-docker.pkg.dev \
   --docker-username=_json_key \
   --docker-password="$(cat ~/.secrets/sa-docker-pull-from-local.key)" \
   --docker-email=<redacted>
```

And to use the secret when pulling images in deployment manifest:

```
      ...
      imagePullSecrets:
      - name: gcp-artifact-registry
      containers:
      ...
```

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
k get gateway # Note 'ADDRESS' for log-output-gateway
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
