#!/bin/bash

echo "Checking helm installation"
helm version
echo ""

echo "Adding Helm repo for Prometheus"
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
echo""

echo "Creating the namespace monitoring"
kubectl create namespace monitoring
echo ""

echo "Installing Prometheus and Grafana using Helm"
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring
echo ""

sleep 10

echo "Checking the pods status in the monitoring namespace"
kubectl get pods -n monitoring
echo ""

# kubectl port-forward svc/kube-prometheus-stack-prometheus --address 0.0.0.0 -n monitoring 9090:9090 &
# kubectl port-forward svc/kube-prometheus-stack-grafana --address 0.0.0.0 -n monitoring 3000:80 &

# Get the Grafana admin password
#  kubectl get secret -n monitoring kube-prometheus-stack-grafana -o json   | jq -r '.data["admin-password"]'   | base64 --decode; echo