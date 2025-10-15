# Exercise 1.5

## Deploying

```sh
kubectl apply -f manifests/deployment.yaml
```

## Do Port Forwarding

```sh
kubectl port-forward deployment/todo-app-deployment 5555:5000 &
```

## Verify output

```sh
curl http://127.0.0.1:5555
```

## (Re)Building the docker image

```sh
docker build . -t <namespace>/todo_app:1.2
```
