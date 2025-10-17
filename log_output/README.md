# Exercise 2.5

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
curl -s http://192.168.65.3:8081/log | head
```

## (Re)Building the docker images

```sh
docker build ./log-reader-api -t <namespace>/log_output_reader_api:2.5
```
