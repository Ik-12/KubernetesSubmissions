# Create the cluster with proper ingress
k3d cluster create -a 2 --k3s-arg "--tls-san=127.0.0.1@server:0" --port 8082:30080@agent:0 -p 8081:80@loadbalancer

# Create dir for persitent storage
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube

# Create namespaces
kubectl apply -f namespaces/

# Create persistent volumes
kubectl apply -f volumes/

# Create secrets
export SOPS_AGE_KEY_FILE=$HOME/key.txt
sops --decrypt the_project/manifest/ssecret.enc.yaml | kubectl apply -f -

# Create GCP Artifact Registry docker-registry secret in all namespaces
namespaces=$(kubectl get ns -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}')
for ns in $namespaces; do
    kubectl create secret docker-registry gcp-artifact-registry \
       --docker-server=europe-north1-docker.pkg.dev \
       --docker-username=_json_key \
       --docker-password="$(cat ~/.secrets/sa-docker-pull-from-local.key)" \
       --docker-email=ikujamaki@gmail.com
done

