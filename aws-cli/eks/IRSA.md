## Usage of IRSA for EKS

### Associate IAM OIDC provider with the EKS cluster
```bash
eksctl utils associate-iam-oidc-provider --region=<aws-region-code> --cluster=<cluster-name> --approve
```
### Create an IAM Policy
```bash
cat > s3-read-only-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "s3:ListAllMyBuckets",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF

aws iam create-policy \
  --policy-name S3ListOnlyPolicy \
  --policy-document file://s3-read-only-policy.json

export POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`S3ListOnlyPolicy`].Arn' --output text)

```

### Create an IAM Role and attach the policy
```bash
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export OIDC_PROVIDER=$(aws eks describe-cluster --name $CLUSTER_NAME --region $REGION \
  --query "cluster.identity.oidc.issuer" --output text | sed -e "s|^https://||")

cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::$ACCOUNT_ID:oidc-provider/$OIDC_PROVIDER"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "$OIDC_PROVIDER:sub": "system:serviceaccount:demo:s3-reader-sa"
        }
      }
    }
  ]
}
EOF

# create the role
aws iam create-role \
  --role-name eks-irsa-s3-reader \
  --assume-role-policy-document file://trust-policy.json

## Attach the role
aws iam attach-role-policy \
  --role-name eks-irsa-s3-reader \
  --policy-arn $POLICY_ARN

export IAM_ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/eks-irsa-s3-reader"
```

### Create K8s SA and Namespace
```bash
kubectl create namespace demo

cat > serviceaccount.yaml <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: s3-reader-sa
  namespace: demo
  annotations:
    eks.amazonaws.com/role-arn: $IAM_ROLE_ARN
EOF

kubectl apply -f serviceaccount.yaml
```
### Deploy a application that uses IRSA
```bash
cat > deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: s3-test
  namespace: demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: s3-test
  template:
    metadata:
      labels:
        app: s3-test
    spec:
      serviceAccountName: s3-reader-sa
      containers:
      - name: aws-cli
        image: amazon/aws-cli
        command: ["sh", "-c", "aws sts get-caller-identity && aws s3 ls && sleep 3600"]
        env:
        - name: AWS_REGION
          value: $REGION
EOF

kubectl apply -f deployment.yaml
```
### Verify the setup
```bash
POD=$(kubectl get pod -n demo -l app=s3-test -o jsonpath='{.items[0].metadata.name}')
kubectl logs -n demo $POD

### Clean up
kubectl delete namespace demo
```
