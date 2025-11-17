### Use Pod Security Group

#### Add the AmazonEKSVPCResourceController managed IAM policy to the cluster role that is associated with your Amazon EKS cluster. 
```bash
cluster_role=$(aws eks describe-cluster --name my-cluster --query cluster.roleArn --output text | cut -d / -f 2)

aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEKSVPCResourceController --role-name $cluster_role

```

#### Enable security group for pods on VPC CNI
```bash
# set the required variable
kubectl set env daemonset aws-node -n kube-system ENABLE_POD_ENI=true
kubectl set env daemonset aws-node -n kube-system POD_SECURITY_GROUP_ENFORCING_MODE=standard

# Verfity it
kubectl get ds aws-node -n kube-system -o yaml | grep ENABLE_POD_ENI

## Not all instance type support Pod ENI chceck it here:  https://github.com/aws/amazon-vpc-resource-controller-k8s/blob/master/pkg/aws/vpc/limits.go#L321 
## you will need to create a new nodegroup that supports POD ENI.
```
#### Create a security group for the pods
```bash
# create the SG which allow inbound/outbound to kubelet and node and desired traffic.
aws ec2 create-security-group \
  --group-name pod-sg \
  --description "SG for pod" \
  --vpc-id vpc-xxxx

# Create  the SecurityGroupPolicy with correct labels
cat >my-security-group-policy.yaml <<EOF
apiVersion: vpcresources.k8s.aws/v1beta1
kind: SecurityGroupPolicy
metadata:
  name: my-security-group-policy
  namespace: my-namespace
spec:
  podSelector:
    matchLabels:
      role: my-role
  securityGroups:
    groupIds:
      - my_pod_security_group_id
EOF

## that's it done, get the pods status.