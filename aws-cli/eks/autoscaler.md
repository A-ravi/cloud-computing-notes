## Setup AutoScaler in EKS

### Get the  OIDC and check the association
```bash
aws eks describe-cluster \
  --name cluster-name \
  --region region \
  --query "cluster.identity.oidc.issuer" \
  --output text

eksctl utils associate-iam-oidc-provider --region=region --cluster=cluster-name --approve

```

### Create a policy for the AutoScaler:
```bash
cat > cluster-autoscaler-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DescribeTags",
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup"
      ],
      "Resource": "*"
    }
  ]
}
EOF

aws iam create-policy \
  --policy-name EKS-ClusterAutoscaler \
  --policy-document file://cluster-autoscaler-policy.json

```

### Create the IAM Role for IRSA

```bash
eksctl create iamserviceaccount \
  --name cluster-autoscaler \
  --namespace kube-system \
  --cluster eks-demo \
  --region us-west-2 \
  --role-name EKS-ClusterAutoscaler-Role \
  --attach-policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/EKS-ClusterAutoscaler \
  --approve \
  --override-existing-serviceaccounts
```

### Deploy the Cluster AutoScaler and Update it configuration
```bash
helm repo add autoscaler https://kubernetes.github.io/autoscaler

helm upgrade --install cluster-autoscaler autoscaler/cluster-autoscaler \
  --namespace "kube-system" \
  --set "autoDiscovery.clusterName=${EKS_CLUSTER_NAME}" \
  --set "awsRegion=${AWS_REGION}" \
  --set "rbac.serviceAccount.name=cluster-autoscaler" \
  --set "rbac.serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"="$CLUSTER_AUTOSCALER_ROLE" \
  --wait

```

### Add the required tags to Nodegroups
```bash
k8s.io/cluster-autoscaler/enabled
k8s.io/cluster-autoscaler/clusterName # Replate the ClusterName with actual ClusterName
```

### Annotate Autoscaler pod to Ignore Itself and Verify the Installation
```bash
kubectl -n kube-system annotate deployment cluster-autoscaler \
    cluster-autoscaler.kubernetes.io/safe-to-evict="false"

kubectl -n kube-system logs -f deployment/cluster-autoscaler

```
