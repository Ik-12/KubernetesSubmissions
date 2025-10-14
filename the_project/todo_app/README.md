# Exercise 1.2

## Deploying

```sh
kubectl create deployment todo_app --image=docker.io/iku1/todo_app:1.2
```

## Verify output

```sh
kubectl logs deployment/todo_app --all-pods=true
```

## (Re)Building the docker image

```sh
docker build . -t <namespace>/todo_app:1.2
```
