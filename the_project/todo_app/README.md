# Exercise 1.12

## Recreate cluster with proper port mapping

```sh
k3d cluster create -a 2 --k3s-arg "--tls-san=192.168.65.3@server:0" --port 8082:30080@agent:0 -p 8081:80@loadbalancer
```

Note: `--tls-san=192.168.65.3@server:0` is neeed to allow Lens running on local machine to cluster running on VM.  

## Deploying

```sh
kubectl apply -f ../../volumes/persistent_cache.yml
kubectl apply -f ../../volumes/persistent_imgcache_claim.yaml
kubectl apply -f manifests/
```

## Verify output

Open http://127.0.0.1:8081 in browser (or using the VM ip address).

Restarts and check that image didn't change:

```sh
kubectl delete deployments.apps todo-app-deployment
kubectl apply -f manifests/
```

## (Re)Building the docker image

```sh
docker build . -t <namespace>/todo_app:1.12
```
