# EKS commands for setting up and managing Amazon EKS clusters

What does eksctl do?
1. create a vpc with public and private subnets across multiple AZs
2. create IGW and NAT gateways
3. Create route table and associate with subnets
4. Create the EKS cluster control plane
5. Create worker node groups and associate with the cluster

## Basic Commands:
```bash

# get the kubeconfig file:
aws eks update-kubeconfig --name eks-demo --region us-east-1
# verify access to the cluster
kubectl get nodes

# install the AWS Load Balancer Controller
#1. get the IAM roles
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.14.0/docs/install/iam_policy.json

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json

# associate the OIDC provider with your cluster first
eksctl utils associate-iam-oidc-provider --region=<aws-region-code> --cluster=<cluster-name> --approve

# create a service account with the IAM role and attach the policy created above
eksctl create iamserviceaccount \
    --cluster=<cluster-name> \
    --namespace=kube-system \
    --name=aws-load-balancer-controller \
    --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --region <aws-region-code> \
    --approve

# install the controller using helm
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks

helm install aws-load-balancer-controller eks/aws-load-balancer-controller   -n kube-system   --set clusterName=eks-lab-cluster   --set serviceAccount.create=false   --set serviceAccount.name=aws-load-balancer-controller   --version 1.13.0

kubectl get deployment -n kube-system aws-load-balancer-controller

# sample ingress, now you can create ingress and use the ALB controller

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: catalog-multi
  namespace: catalog
  labels:
    app.kubernetes.io/created-by: eks-workshop
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/healthcheck-path: /health
    # HIGHLIGHT
    alb.ingress.kubernetes.io/group.name: retail-app-group
spec:
  ingressClassName: alb
  rules:
    - http:
        paths:
          - path: /catalog
            pathType: Prefix
            backend:
              service:
                name: catalog
                port:
                  number: 80



# EBS
#########################################
#Creat the role with the requird policy
eksctl create iamserviceaccount \
        --name ebs-csi-controller-sa \
        --namespace kube-system \
        --cluster my-cluster \
        --role-name AmazonEKS_EBS_CSI_DriverRole \
        --role-only \
        --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
        --approve

### For KMS need to create a custom poilcy with permission for keys and add policy to role.

# Install the EBS CSI driver as an EKS add-on
aws eks create-addon --cluster-name $EKS_CLUSTER_NAME --addon-name aws-ebs-csi-driver \
  --service-account-role-arn $EBS_CSI_ADDON_ROLE \
  --configuration-values '{"defaultStorageClass":{"enabled":true}}'
aws eks wait addon-active --cluster-name $EKS_CLUSTER_NAME --addon-name aws-ebs-csi-driver

# Verify the installation
kubectl get daemonset ebs-csi-node -n kube-system
kubectl get storageclass



# EFS
#########################################
#!!! EFS should be created in the same VPC, subnets as the EKS cluster, also check for SG rules.
# create a role for the EFS CSI Driver with required permission this link
# https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html 
export cluster_name=eks-lab-cluster
export role_name=AmazonEKS_EFS_CSI_DriverRole
eksctl create iamserviceaccount \
    --name efs-csi-controller-sa \
    --namespace kube-system \
    --cluster $cluster_name \
    --role-name $role_name \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy \
    --approve
TRUST_POLICY=$(aws iam get-role --output json --role-name $role_name --query 'Role.AssumeRolePolicyDocument' | \
    sed -e 's/efs-csi-controller-sa/efs-csi-*/' -e 's/StringEquals/StringLike/')
aws iam update-assume-role-policy --role-name $role_name --policy-document "$TRUST_POLICY"

# Install via EKS Add-on
aws eks create-addon --cluster-name $EKS_CLUSTER_NAME --addon-name aws-efs-csi-driver \
  --service-account-role-arn $EFS_CSI_ADDON_ROLE
# Verify the Installation

# create a storage class using the EFS file system created
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: efs-sc
provisioner: efs.csi.aws.com
parameters:
  provisioningMode: efs-ap
  fileSystemId: ${EFS_ID}
  directoryPerms: "700"

# use the SC in your PVC 

# Mountpoint for Amazon S3
#########################################
#!!!
# create the bucket first and then policy attach it to the role, then install the add-on 
# https://docs.aws.amazon.com/eks/latest/userguide/s3-csi-create.html

CLUSTER_NAME=my-cluster
REGION=region-code
ROLE_NAME=AmazonEKS_S3_CSI_DriverRole
POLICY_ARN=AmazonEKS_S3_CSI_DriverRole_ARN
eksctl create iamserviceaccount \
    --name s3-csi-driver-sa \
    --namespace kube-system \
    --cluster $CLUSTER_NAME \
    --attach-policy-arn $POLICY_ARN \
    --approve \
    --role-name $ROLE_NAME \
    --region $REGION \
    --role-only


aws eks create-addon --cluster-name $EKS_CLUSTER_NAME --addon-name aws-mountpoint-s3-csi-driver \
  --service-account-role-arn $S3_CSI_ADDON_ROLE

#check the installation
kubectl get pods -n kube-system | grep s3-csi


# Managed Node Groups
#########################################

# check the nodegroup details
eksctl get nodegroup --name $EKS_DEFAULT_MNG_NAME --cluster $EKS_CLUSTER_NAME

# update or scale the nodes
aws eks update-nodegroup-config --cluster-name $EKS_CLUSTER_NAME \
  --nodegroup-name $EKS_DEFAULT_MNG_NAME --scaling-config minSize=4,maxSize=6,desiredSize=4


# AutoScaler Installation
#########################################

# create a policy for the autoscaler
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DescribeScalingActivities",
        "ec2:DescribeImages",
        "ec2:DescribeInstanceTypes",
        "ec2:DescribeLaunchTemplateVersions",
        "ec2:GetInstanceTypesFromInstanceRequirements",
        "eks:DescribeNodegroup"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup"
      ],
      "Resource": ["*"]
    }
  ]
}

# create iam role and attach the policy for OIDC provider via console

# install via helm
helm repo add autoscaler https://kubernetes.github.io/autoscaler

helm upgrade --install cluster-autoscaler autoscaler/cluster-autoscaler \
  --namespace "kube-system" \
  --set "autoDiscovery.clusterName=${EKS_CLUSTER_NAME}" \
  --set "awsRegion=${AWS_REGION}" \
  --set "rbac.serviceAccount.name=cluster-autoscaler" \
  --set "rbac.serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"="$CLUSTER_AUTOSCALER_ROLE" \
  --wait
# BOOM!!!


# Spot Instance NodeGroup
#########################################

aws eks create-nodegroup \
  --cluster-name $EKS_CLUSTER_NAME \
  --nodegroup-name managed-spot \
  --node-role $SPOT_NODE_ROLE \
  --subnets $PRIMARY_SUBNET_1 $PRIMARY_SUBNET_2 $PRIMARY_SUBNET_3 \
  --instance-types c5.large c5d.large c5a.large c5ad.large c6a.large \
  --capacity-type SPOT \
  --scaling-config minSize=2,maxSize=3,desiredSize=2 \
  --disk-size 20

# Verify the nodes
kubectl get nodes -L eks.amazonaws.com/capacityType,eks.amazonaws.com/nodegroup

# Running pod on SPOT instance:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: catalog
spec:
  template:
    spec:
      nodeSelector:
        eks.amazonaws.com/capacityType: SPOT

# Karpentar
#########################################
# opensource project for autoscaling project build for kubernetes
# it requires roles to call AWS APIs, a role and instance profile for the EC2 instances that karpenter will create, an EKS access entry for the node IAM role so the nodes can join the cluster and an SQS queue to receive spot interruption notices.

# Ref to this docs: https://catalog.workshops.aws/karpenter/en-US/install-karpenter
# or 
# https://karpenter.sh/docs/getting-started/migrating-from-cas/


# Fargate
#########################################
# Create a Exectuion role for the fargate pods, specify the namespace and label that will use fargate profile and done update the label in the workload yaml file

# Manually create role then create the fargate profile
# OR
eksctl create fargateprofile \
  --cluster eks-lab-cluster \
  --name fargate-profile-1 \
  --namespace default \
  --labels fargate=yes

# KEDA
#########################################

# Need to creat a role for KEDA with required policies
# install via helm and role should have permissino to access the scraper aws services and that's it.

# Logging with Fluent Bit
#########################################
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-logs-FluentBit.html 
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Observability-EKS-addon.html#install-CloudWatch-Observability-EKS-addon-workernodes 


# Open Source Observability EKS 
#########################################

# AWS Distro for OpenTelemetry (ADOT) Collector

# https://aws-otel.github.io/docs/getting-started/adot-eks-add-on 

# deploy cert-manager and then only procced with the ADOT installation via EKS add-on




```

## Tutorials Steps
```bash

# Create a cluster using eksctl
eksctl create cluster \
--name eks-lab-cluster \
--nodegroup-name worknodes-1 \
--node-type t3.medium \
--nodes 2 \
--nodes-min 1 \
--nodes-max 4 \
--managed \
--version 1.34 \
--spot \
--region ${AWS_DEFAULT_REGION}

# Create a ECR repository
aws ecr create-repository \
 --repository-name <repo-name> \
 --region ${AWS_DEFAULT_REGION}

#Get the ECR repository URI
export ECR_REPO_URI=$(aws ecr describe-repositories \
 --repository-names <repo-name> \
 --region ${AWS_DEFAULT_REGION} \
 --query 'repositories[*].repositoryUri' \
 --output text)

#login to ECR
aws ecr get-login-password \
--region ${AWS_DEFAULT_REGION} \
 | docker login \
 --username AWS \
 --password-stdin $ACCOUNT_NUMBER.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com

#push the images to ECR
docker tag <image>:latest $ECR_REPO_URI:latest
docker push $ECR_REPO_URI:latest


#Set the AWS_DEFAULT_REGION variable
echo "export AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}" >> ~/.bash_profile
source ~/.bash_profile
aws configure set default.region $AWS_DEFAULT_REGION

$ check status of Cluster
aws eks describe-cluster \
 --name eks-lab-cluster \
 --query 'cluster.status' \
 --output text

# update the kubeconfig file
aws eks update-kubeconfig \
 --region $AWS_DEFAULT_REGION \
 --name eks-lab-cluster

# Install the AWS Load Balancer Controller
###########################################

# Set ACCOUNT_NUMBER vairable
export ACCOUNT_NUMBER=$(aws sts get-caller-identity --query 'Account' --output text)
# Create an IAM OIDC (Open ID Connect) provider
echo "Running: eksctl utils associate-iam-oidc-provider --region us-west-2 --cluster eks-lab-cluster --approve"
eksctl utils associate-iam-oidc-provider --region us-west-2 --cluster eks-lab-cluster --approve
# Create a Kubernetes service account named aws-load-balancer-controller in the kube-system namespace for the AWS Load Balancer Controller and annotate the Kubernetes service account with the name of the IAM role.
echo "Running: eksctl create iamserviceaccount --cluster=eks-lab-cluster --namespace=kube-system --name=aws-load-balancer-controller --role-name "AmazonEKSLoadBalancerControllerRole" --attach-policy-arn=arn:aws:iam::$ACCOUNT_NUMBER:policy/AWSLoadBalancerControllerIAMPolicy --approve"
eksctl create iamserviceaccount --cluster=eks-lab-cluster --namespace=kube-system --name=aws-load-balancer-controller --role-name "AmazonEKSLoadBalancerControllerRole" --attach-policy-arn=arn:aws:iam::$ACCOUNT_NUMBER:policy/AWSLoadBalancerControllerIAMPolicy --approve
sleep 5
# Add helm eks-charts repository
echo "Running: helm repo add eks https://aws.github.io/eks-charts"
helm repo add eks https://aws.github.io/eks-charts
# helm update
echo "Running: helm repo update"
helm repo update
# Install the AWS Load Balancer Controller.
## Reference: https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html
echo "Running: helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=eks-lab-cluster --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller"
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=eks-lab-cluster --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller


# Configure Application access to AWS API
###########################################

# Policy are already created beforehand using eksctl create iamserviceaccount command

eksctl create iamserviceaccount \
    --name iampolicy-sa \
    --namespace containers-lab \
    --cluster eks-lab-cluster \
    --role-name "eksRole4serviceaccount" \
    --attach-policy-arn arn:aws:iam::$ACCOUNT_NUMBER:policy/eks-lab-read-policy \
    --approve \
    --override-existing-serviceaccounts

kubectl get sa iampolicy-sa -n containers-lab -o yaml

kubectl set serviceaccount \
 deployment eks-lab-deploy \
 iampolicy-sa -n containers-lab

kubectl describe deployment.apps/eks-lab-deploy \
 -n containers-lab | grep 'Service Account'

kubectl get ingress -n containers-lab

```