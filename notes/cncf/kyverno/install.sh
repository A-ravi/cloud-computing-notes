#!/bin/bash
echo "==============================="
echo "Starting Kyverno installation..."
echo "==============================="

# Install Kyverno in a Kubernetes cluster
helm repo add kyverno https://kyverno.github.io/kyverno
helm repo update
helm install kyverno kyverno/kyverno -n kyverno --create-namespace --set replicaCount=1


kubectl get crds | grep kyverno.io

echo "==============================="
echo "Kyverno installation completed."
echo "To verify, run: kubectl get pods -n kyverno"
echo "==============================="