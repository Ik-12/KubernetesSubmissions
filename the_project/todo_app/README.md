# Exercise 1.6

## Recreate cluster with proper port mapping

```sh
k3d cluster create -a 2 --k3s-arg "--tls-san=192.168.65.3@server:0" --port 8082:30080@agent:0 -p 8081:80@loadbalancer
```

Note: `--tls-san=192.168.65.3@server:0` is neeed to allow Lens running on local machine to cluster running on VM.  

## Deploying

```sh
kubectl apply -f manifests/
```

## Verify output

From localhost:

```sh
 curl http://127.0.0.1:8082
```

Inside cluster:

```sh
docker exec -it k3d-k3s-default-agent-1 wget -qO- http://10.43.127.7:1234
```

Where `10.43.127.7` is ClusterIP from output of following command:

```sh
kubectl get svc todo-app-svc
```

## (Re)Building the docker image

```sh
docker build . -t <namespace>/todo_app:1.2
```
