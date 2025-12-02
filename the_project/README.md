# Exercise 3.11

## DBaaS vs DIY

| Aspect | DBaaS (e.g., Google Cloud SQL) | DIY (e.g., Postgres SQL in GKE) |
| :---         |     :---      |          :--- |
| Easy of use     | Easy to set up, no low-level DB knowledge and expertice required.       | Set up requires knowledge of implementation details and must be documented well.      |
| Costs        | Pure service costs may be higher, but the total cost of ownership can be lower due to lower maintenance costs and better productivity.     | Service costs can be optimized by selecting the cheapest VM provider. |
| Maintenance     | Requires little or no maintanance.        | The user must maintain the instance(s) and handle updates.  |
| Backups     | Automatic and production-proven backups.       | The user must handle backups: higher risk of losing data due to bad backup practices.     |
| Scaling     | Flexible and automatic scaling | Requires more manual control and may be limited.      |
| Security     | High-level security and compliance handled by security experts      | Handle by the user and thus more prone to poor decisions and user error if      |
| Flexibility     | Can result in vendor-locking       | Generally unlimited      |

In general, DBaaS is generally safer choice to start with. 

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

### Decrypt secrets (only for local deployments)

```
export SOPS_AGE_KEY_FILE=$HOME/key.txt
sops --decrypt manifests/secret.enc.yaml | kubectl apply -f -
```

When deploying from GitHub Actions, Kubernetes secrets are automatically created from repo secrets.

### Build, push and deploy using Github Actions

1. Make sure the cluster exists
2. Create secrets
3. Push to GitHub

Actions will automatically build the docker image, push the to GKE
artifact repo and deploy app to a namespace corresponding to git branch name (or 'project' if 'master') by applying the manifests.

### Build, push and deploy using a local runner with Act

1. Install Act `brew install act`
2. Run act from repo root:

```
act --container-architecture linux/amd64 --var ACTIONS_RUNNER_DEBUG=true -s
GKE_PROJECT=<redacted> -s GKE_SA_KEY=(cat ~/.secrets/gke-sa-key.json | base64) -s
GITHUB_TOKEN=<redacted> -s POSTGRESS_PASSWORD=<redacted>
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

## Postgres DB backup CronJob

This seemingly simple exercise proved to be rather time consuming. Most online examples mounted the Google Service Account key to the container, which seemed cumbersome and an insecure solution. After some research, I found that "Workload Identity Binding" is the proper way of providing access from the CronJob pod to the storage bucket.

0. Make sure the cluster is created with "--workload-pool=<project-id>.svc.id.goog"
1. Create a Cloud storage bucket from the Cloud Console
2. Create a service account that has Admin permission for the bucket from the Console
3. Create a service account for the CronJob (referenced in the manifest):

```
kubectl create serviceaccount postgres-backup-sa
```

4. Do the Workload Identity Binding:

```
gcloud iam service-accounts add-iam-policy-binding \
    --role="roles/iam.workloadIdentityUser" \
    --member="serviceAccount:dwk-gke-iku.svc.id.goog[project/postgres-backup-sa]" \
     todo-db-backup@dwk-gke-iku.iam.gserviceaccount.com

kubectl annotate serviceaccount postgres-backup-sa \
    iam.gke.io/gcp-service-account=todo-db-backup@dwk-gke-iku.iam.gserviceaccount.com
```

5. Apply manually:

```
k apply -f todo_backend/manifests/06-backup.yml
```

6. Verify that backup is working (interval was set to 5 minutes for testing):

```
$ gsutil ls gs://dwk-project-todo-db-backup/
gs://dwk-project-todo-db-backup/todo-backup-2025-12-02--13-20.pgdump.gz
gs://dwk-project-todo-db-backup/todo-backup-2025-12-02--13-25.pgdump.gz
gs://dwk-project-todo-db-backup/todo-backup-2025-12-02--13-30.pgdump.gz
gs://dwk-project-todo-db-backup/todo-backup-2025-12-02--13-35.pgdump.gz
```

## Set resource requests and limits

1. Check current CPU and memory usage using `k top pods`:

```
NAME                                       CPU(cores)   MEMORY(bytes)
postgres-stset-0                           1m           37Mi
todo-app-deployment-8b4dc544-ml4kj         2m           136Mi
todo-backend-deployment-67dbfb5cd9-zkkmx   2m           43Mi
```

2. Add request and limits that are bit higher and re-deploy.
3. Verify that limits are applied:

```
$ k describe pods todo-app-deployment-7cf8d77c8b-klvzq | grep -A 5 Limits
    Limits:
      cpu:     500m
      memory:  256Mi
    Requests:
      cpu:     50m
      memory:  150Mi
```

## GKE Log explorer

1. Adjusted logging to error because Gunicorn was writing all debug logging to stderr and GKE Logging sets severity = Error for all entries written in stderr.

An example from Logs Explorer when adding new todo item from browser is shown below.

![Example view from GKE Log Explorer](log-example.png "Log Explorer view")

