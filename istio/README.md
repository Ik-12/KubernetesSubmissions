# Exercise 5.2 - Getting started with Istio service mesh

## Installation

Recreate the cluster with proper arguments:

```
k3d cluster delete k3s-default
k3d cluster create --api-port 6550 -p '9080:80@loadbalancer' -p '9443:443@loadbalancer' --agents 2 --k3s-arg '--disable=traefik@server:*'
```

Add istio helm repo:

```
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
```

Install:

Contrary to the document, must use profile `k3s` even with `k3d` cluster (see https://github.com/istio/istio/pull/57110)

```
brew install istioctl
istioctl install --set profile=ambient --skip-confirmation --set values.global.platform=k3s 
```
## Sample app

### Deploy the

```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/platform/kube/bookinfo.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/platform/kube/bookinfo-versions.yaml

```

### Add ingress

The instructions told to create the cluster with traefik disabled, which apparently caused that Gateway and HTTPRoute CRDs are not created. Create them manually before applying the gateway manifests: 

```
kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
  { kubectl kustomize "github.com/kubernetes-sigs/gateway-api/config/crd?ref=v1.4.0" | kubectl apply -f -; }
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/gateway-api/bookinfo-gateway.yaml
kubectl port-forward svc/bookinfo-gateway-istio 8080:80 &
```

Now sample app can be accessed at http://localhost:8080/productpage.

### Add Bookinfo to the mesh

```
kubectl label namespace default istio.io/dataplane-mode=ambient
```

### Metrics

```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/addons/kiali.yaml

```

Access the dashboard and generate some traffic:

```
istioctl dashboard kiali &
for i in $(seq 1 100); do curl -sSI -o /dev/null http://localhost:8080/productpage; done
```

### Layer-4 authorization policies

Apply policy to limits access to `productpage` only from istio:

```
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-ztunnel
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/bookinfo-gateway-istio
EOF
```

Verify to trying access elsewhere returns an error:

```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/curl/curl.yaml
kubectl exec deploy/curl -- curl -s "http://productpage:9080/productpage"
```

### Layer-7 authorization policy

Create waypoint proxy:

```
istioctl waypoint apply --enroll-namespace --wait
```

Apply policy to allow accessing `productpage` from curl:

```
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-waypoint
  namespace: default
spec:
  targetRefs:
  - kind: Service
    group: ""
    name: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/curl
    to:
    - operation:
        methods: ["GET"]
EOF
```

Update L4 policy to allow connection from the waypoint:

```
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-ztunnel
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/bookinfo-gateway-istio
        - cluster.local/ns/default/sa/waypoint
EOF
```

Now access from curl should work:

```
kubectl exec deploy/curl -- curl -s http://productpage:9080/productpage | grep -o "<title>.*</title>"
```

But other operation should fail, e.g.:

```
kubectl exec deploy/curl -- curl -s "http://productpage:9080/productpage" -X DELETE
```

### Splitting traffic

Configure routing 90% of request to reviews v1 and 10% to v2:

```
kubectl apply -f - <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: reviews
spec:
  parentRefs:
  - group: ""
    kind: Service
    name: reviews
    port: 9080
  rules:
  - backendRefs:
    - name: reviews-v1
      port: 9080
      weight: 90
    - name: reviews-v2
      port: 9080
      weight: 10
EOF
```

Test that routing works:

```
kubectl exec deploy/curl -- sh -c "for i in \$(seq 1 100); do curl -s http://productpage:9080/productpage | grep reviews-v.-; done" | cut -d '-' -f 2 | sort | uniq -c
```

This results in the following, which seems ok:

```
    186 v1
     14 v2
```

## Cleanup

Remove everything:

```
kubectl label namespace default istio.io/dataplane-mode-

kubectl label namespace default istio.io/use-waypoint-
istioctl waypoint delete --all
kubectl delete httproute reviews
kubectl delete authorizationpolicy productpage-viewer
kubectl delete -f samples/curl/curl.yaml
kubectl delete -f samples/bookinfo/platform/kube/bookinfo.yaml
kubectl delete -f samples/bookinfo/platform/kube/bookinfo-versions.yaml
kubectl delete -f samples/bookinfo/gateway-api/bookinfo-gateway.yaml

istioctl uninstall -y --purge
kubectl delete namespace istio-system
kubectl delete -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/experimental-install.yaml

```
