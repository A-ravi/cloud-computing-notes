## Setup KEDA in EKS

<!-- Ref. https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/event-driven-auto-scaling-with-eks-pod-identity-and-keda.html -->

#### Create a Role for the keda operator
Create a role for eks pod services and named the role keda-operator.
```json
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "pods.eks.amazonaws.com"
            },
            "Action": [
                "sts:AssumeRole",
                "sts:TagSession"
            ]
        }
    ]
```

#### Create an  IAM role for the application to use
Create the IAM role for the sample application
```json
{
    "Version": "2012-10-17",		 	 	 
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "pods.eks.amazonaws.com",
                "AWS": "arn:aws:iam::<account number>:role/keda-operator"
            },
            "Action": [
                "sts:AssumeRole",
                "sts:TagSession"
            ]
        }
    ]
}
```
On  Add permission page, attach the required permissions
for role name use keda-identity.

#### Install the KEDA 
```bash
# Add Helm Repo for Keda
helm repo add kedacore https://kedacore.github.io/charts
# Update Helm repo
helm repo update
# Install Keda
helm install keda kedacore/keda --namespace keda --create-namespace

kubectl get po -n keda

# Assign the role to service accout via pod mapping 
aws eks create-pod-identity-association --cluster-name clusterName --role-arn RoleARN --namespace keda --service-account keda-operator

```
#### Deploy the application, associate the service account with keda-identity role and configure the KEDA configuration
```bash
aws eks create-pod-identity-association \
   --cluster-name clusterName \
   --role-arn arn:aws:iam::ACCOUNTNUMBER:role/keda-identity \
   --namespace ns \
   --service-account serviceAccount
```
```yaml
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: q-read-trigger-auth
  namespace: security
spec:
  podIdentity:
    provider: aws
    roleArn: RoleARN
---
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: k8s-sqs-read-msg-keda
  namespace: security
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: q-read
  # pollingInterval:  10
  # cooldownPeriod:   60
  # idleReplicaCount: 1
  # minReplicaCount:  2
  maxReplicaCount:  10
  triggers:
  - type: aws-sqs-queue
    name: q-read-trigger
    authenticationRef:
      name: q-read-trigger-auth
    metadata:
      queueURL: https://sqs.us-west-2.amazonaws.com/013894306680/event-messages-queue
      queueLength: "5"
      awsRegion: us-west-2
```
```bash
# check the keda logs 
kubectl logs -n keda -l app=keda-operator -c keda-operator

kubectl get po -A
```