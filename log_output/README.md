# Exercise 1.3

## Deploying

```sh
kubectl apply -f manifests/deployment.yaml
```

## Verify output

```sh
kubectl logs deployment/log-output-deployment
```

## (Re)Building the docker image

```sh
docker build . -t <namespace>/log_output:1.1
```
