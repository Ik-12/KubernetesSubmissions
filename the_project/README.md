# Exercise 2.4

## Namespace configuration

```sh
kubectl apply -f manifests/
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

```sh
kubectl apply -f todo_backend/manifests/
kubectl apply -f todo_app/manifests/

```
