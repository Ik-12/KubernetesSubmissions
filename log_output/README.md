# Exercise 2.3

## Cluster configuration

Make sure the cluster has required port mapping for docker:

```sh
k3d cluster create -a 2 --k3s-arg "--tls-san=192.168.65.3@server:0" --port 8082:30080@agent:0 -p 8081:80@loadbalancer
```

Note: `--tls-san=192.168.65.3@server:0` is neeed to allow Lens running on local machine to cluster running on VM. ```

## Deploy

### Move persintent volume claims

Persistent volume claims have a namespace so we must also them to 'exercises' namespace. Easiest option is to delete and recreate them after updating manifests:

```sh
kubectl ns default
kubectl delete pvc log-volume-claim
kubectl delete delete pv mooc-pv
kubectl apply -f ../volumes/ # namespace is defined in manifest
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
