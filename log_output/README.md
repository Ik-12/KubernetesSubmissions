# Exercise 1.1

## Deploying

```sh
kubectl create deployment log-output --image=iku1/log_output:1.1
```

## Verify output

```sh
kubectl logs deployment/log_output --all-pods=true
```

## (Re)Building the docker image

```sh
docker build . -t <namespace>/log_output:1.1
```
