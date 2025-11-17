## Use Pod Identity in EKS

### Install the Addon in the cluster
```bash
aws eks create-addon \
  --cluster-name $CLUSTER_NAME \
  --addon-name eks-pod-identity-agent

# verify the addon status
aws eks describe-addon \
  --cluster-name $CLUSTER_NAME \
  --addon-name eks-pod-identity-agent \
  --query addon.status
```

### Setup the variables
```bash
export CLUSTER_NAME="demo-eks"
export REGION="ap-south-1"
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Your EXISTING IAM Role
export IAM_ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/rolename"
```

### Create the SA and Namespace
```bash
kubectl create namespace demo
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: s3-reader-sa
  namespace: demo
EOF
```

### Create the pod identity mapping
```bash
aws eks create-pod-identity-association \
  --cluster-name $CLUSTER_NAME \
  --namespace demo \
  --service-account s3-reader-sa \
  --role-arn $IAM_ROLE_ARN

# list the mappings/association
aws eks list-pod-identity-associations --cluster-name $CLUSTER_NAME
```

### Deploy a sample pod that uses the Service Account
```bash
kubectl apply -f - <<EOF
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
        command: ["/bin/sh", "-c"]
        args:
          - |
            echo "Testing AWS STS identity:"
            aws sts get-caller-identity
            echo "Listing S3 buckets:"
            aws s3 ls
            sleep 3600
        env:
        - name: AWS_REGION
          value: ap-south-1
EOF
``` 
### validate the pod logs and Clean up
```bash
POD=$(kubectl get pod -n demo -l app=s3-test -o jsonpath='{.items[0].metadata.name}')
kubectl logs -n demo $POD

# Clean up
aws eks delete-pod-identity-association \
  --cluster-name $CLUSTER_NAME \
  --namespace demo \
  --service-account s3-reader-sa

kubectl delete namespace demo
```
