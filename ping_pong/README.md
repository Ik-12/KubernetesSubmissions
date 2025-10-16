# Exercise 1.9

## Cluster configuration

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
curl http://127.0.0.1:8081/pingpong
```

## (Re)Building the docker image

```sh
docker build . -t <namespace>/ping_pong:1.9
```
