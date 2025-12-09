# Argo CD

## Configuration

To allow loading of shared resources from parent directories apply following manifest:

```
kubectl apply -f argo-cm-config.yaml
```

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-cm
    app.kubernetes.io/part-of: argocd
data:
    kustomize.buildOptions: --load-restrictor LoadRestrictionsNone
```

## Installation

```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Get `admin` password:

```
kubectl get -n argocd secrets argocd-initial-admin-secret -o json | jq .data.password
```

Get access using portmapping:

```
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
