# Exercise 5.4

## Wikipedia pod with init and sidecar containers

Apply the manifest and expose using port forward:

```
kubectl apply -f wikipedia-sidecar/manifests/wikipedia.yaml
kubectl port-forward svc/wikipedia-svc 7000:80 &
```

