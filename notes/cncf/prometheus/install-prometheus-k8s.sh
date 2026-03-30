#!/bin/bash

#########################################################
# For Persistent Storage, we need to install EBS CSI driver
# Install it using this link: https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html
#  Install helm using the values.yaml below just add -f values.yaml



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

#####################################
# values.yaml for persistent prometheus installation

# prometheus:
#   prometheusSpec:
#     storageSpec:
#       volumeClaimTemplate:
#         metadata:
#           name: prometheus-storage
#         spec:
#           accessModes: ["ReadWriteOnce"]
#           storageClassName: gp2
#           resources:
#             requests:
#               storage: 50Gi

# alertmanager:
#   alertmanagerSpec:
#     storage:
#       volumeClaimTemplate:
#         metadata:
#           name: alertmanager-storage
#         spec:
#           accessModes: ["ReadWriteOnce"]
#           storageClassName: gp2
#           resources:
#             requests:
#               storage: 10Gi

# grafana:
#   persistence:
#     enabled: true
#     type: pvc
#     storageClassName: gp2
#     accessModes:
#       - ReadWriteOnce
#     size: 10Gi
# }