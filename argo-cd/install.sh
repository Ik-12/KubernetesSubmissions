
kubectl create namespace argocd
kubectl apply -f argo-cm-config.yaml
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
echo "Waiting 30s for Argo CD server to be ready..."
sleep 30s
echo "The admin password is (without the trailing % sign):"
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
kubectl port-forward svc/argocd-server -n argocd 8080:443 &
echo "Argo CD server is accessible at https://localhost:8080"
