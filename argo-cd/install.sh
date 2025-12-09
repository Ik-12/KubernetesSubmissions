
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
echo "Waiting 30s for Argo CD server to be ready..."
sleep 30s

# Config must applied after installation
kubectl apply -f argo-cm-config.yaml
kubectl delete --all pods -n argocd

echo "Waiting another 30s for Argo CD server to restart..."
sleep 30s
echo "The admin password is (without the trailing % sign):"
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo ""
kubectl port-forward svc/argocd-server -n argocd 8080:443 &
echo ""
echo "Argo CD server is accessible at https://localhost:8080"
echo "Login with username: admin"
echo ""
echo "If port forwading is fails try to delete pod argocd-serverd and retry."

