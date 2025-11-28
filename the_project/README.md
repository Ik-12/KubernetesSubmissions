# Exercise 3.6

## Namespace configuration

```sh
kubectl apply -f ../namespaces/
```

## Create secrets for backend DB

1. Base64 encode the Postgres DB password: `echo -n '<password>' | base64`
2. Create secret.yaml that is NOT included in the repo:

```
apiVersion: v1
kind: Secret
metadata:
  name: pg-password
  namespace: project
data:
  POSTGRESS_PASSWORD: <base64-encode-password-from-step-1>
```

3. Encrypt the `secret.yaml` with age and SOPS:

```
age-keygen -o ~/key.txt
sops --encrypt --age <public-key-form-age> --encrypted-regex '^(data)$' ~/secret.yaml > manifests/00-secret.enc.yaml
```

## Recreate the storage to correct namespace

First delete the deployment so that volume can deleted, then recreate volume in new namespace.

```sh
kubectl delete deployments.apps todo-app-deployment
kubectl delete deployments.apps todo-backend-deployment
sleep 30s
kubectl delete pvc image-cache
kubectl delete pv image-cache-vol
kubectl apply -f ../volumes/persistent_cache.yml
kubectl apply -f ../volumes/persistent_imgcache_claim.yaml
```

## Update deployments

### Decrypt secrets

export SOPS_AGE_KEY_FILE=$HOME/key.txt
sops --decrypt manifests/secret.enc.yaml | kubectl apply -f -

### Build, push and deploy using Github Actions

1. Make sure the cluster exists
2. Create secrets 
3. Push to GitHub 

Actions will automatically build the docker image, push the to GKE
artifact repo and deploy app by applying the manifests.

### Build, push and deploy using a local runner with Act

1. Install Act `brew install act`
2. Run act from repo root:

```
act --container-architecture linux/amd64 --var ACTIONS_RUNNER_DEBUG=true -s
GKE_PROJECT=<redacted> -s GKE_SA_KEY=(cat ~/.secrets/gke-sa-key.json | base64) -s
GITHUB_TOKEN=<redacted>
```

### Deploy to GKE manually

```
k --load-restrictor LoadRestrictionsNone kustomize gke/manifests/ | kubectl apply -f -
```

### Deploy in local cluster

```sh
kubectl apply -f todo_backend/manifests/
kubectl apply -f todo_app/manifests/

```
