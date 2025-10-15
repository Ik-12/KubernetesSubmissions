# Exercise 1.4

## Deploying

```sh
kubectl apply -f manifests/deployment.yaml
```

## Verify output

```sh
kubectl logs deployment/todo-app-deployment
```

## (Re)Building the docker image

```sh
docker build . -t <namespace>/todo_app:1.2
```
