# Create the cluster with proper ingress
k3d cluster create -a 2 --k3s-arg "--tls-san=127.0.0.1@server:0" --port 8082:30080@agent:0 -p 8081:80@loadbalancer

# Create dir for persitent storage
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube

# Create namespaces
kubectl apply -f namespaces/

# Create persistent volems
kubectl apply -f namespaces/
