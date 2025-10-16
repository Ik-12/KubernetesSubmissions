# Exercise 1.11

## Cluster configuration

Make sure the cluster has required port mapping for docker:

```sh
k3d cluster create -a 2 --k3s-arg "--tls-san=192.168.65.3@server:0" --port 8082:30080@agent:0 -p 8081:80@loadbalancer
```

Note: `--tls-san=192.168.65.3@server:0` is neeed to allow Lens running on local machine to cluster running on VM. ```

### Create directory for persistent storage

```sh
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
```

Fix permission for containers running as non-root user:

```sh
docker exec k3d-k3s-default-agent-0 chmod 777 /tmp/kube
```

## Deploy

```sh
kubectl apply -f ../volumes/
kubectl apply -f manifests/
kubectl apply -f ../log_output/manifests/
```

## Verify output

```sh
curl http://127.0.0.1:8081/log
curl http://127.0.0.1:8081/pingpong
curl http://127.0.0.1:8081/pingpong
curl http://127.0.0.1:8081/log

```

## (Re)Building the docker images

```sh
docker build ./log-reader-api -t <namespace>/log_output_reader_api:1.11
docker build ./log-writer -t <namespace>/log_output_writer:1.11
```
